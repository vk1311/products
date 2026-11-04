#!/usr/bin/env python3
"""Validate every workflow JSON in this pack.

Basic checks (always run, no dependencies):
  * file parses as JSON and has the fields n8n needs to import it
  * node names and IDs are unique, positions/typeVersions are well-formed
  * every connection points at a real node; every node is reachable from a trigger
  * only built-in node types (n8n-nodes-base.*)
  * credentials are placeholders only, and nothing that looks like a real API key is present

Deep checks (optional): pass the node definitions shipped in the `n8n-nodes-base` npm package
  npm pack n8n-nodes-base && tar xzf n8n-nodes-base-*.tgz
  python3 scripts/validate.py --nodes-json package/dist/types/nodes.json --creds-json package/dist/types/credentials.json
This verifies each node type + typeVersion exists, each parameter name exists for that version,
option values are allowed, and credential types match what the node accepts.

Exit code is non-zero if any error is found.
"""
import argparse
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TRIGGER_TYPES = {"formTrigger", "webhook", "scheduleTrigger", "stripeTrigger", "rssFeedReadTrigger", "emailReadImap"}
PLACEHOLDER = "REPLACE_WITH_YOUR_CREDENTIAL"
SECRET_PATTERNS = [
    (r"sk_(live|test)_[0-9a-zA-Z]{10,}", "Stripe secret key"),
    (r"rk_(live|test)_[0-9a-zA-Z]{10,}", "Stripe restricted key"),
    (r"xox[abpr]-[0-9A-Za-z-]{10,}", "Slack token"),
    (r"AIza[0-9A-Za-z_\-]{30,}", "Google API key"),
    (r"\b\d{8,10}:[A-Za-z0-9_-]{30,}\b", "Telegram bot token"),
    (r"AC[0-9a-f]{32}", "Twilio Account SID"),
    (r"ghp_[0-9A-Za-z]{30,}", "GitHub token"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key"),
]


# ---------------------------------------------------------------- deep check helpers
def versions(defn):
    v = defn["version"]
    return v if isinstance(v, list) else [v]


def cnd_ok(cond, value):
    if not isinstance(cond, dict) or "_cnd" not in cond:
        return cond == value
    c = cond["_cnd"]
    for op, ref in c.items():
        try:
            if op == "eq" and not value == ref: return False
            if op == "not" and not value != ref: return False
            if op == "gte" and not value >= ref: return False
            if op == "lte" and not value <= ref: return False
            if op == "gt" and not value > ref: return False
            if op == "lt" and not value < ref: return False
            if op == "between" and not (ref["from"] <= value <= ref["to"]): return False
            if op == "startsWith" and not str(value).startswith(ref): return False
            if op == "endsWith" and not str(value).endswith(ref): return False
            if op == "includes" and ref not in str(value): return False
            if op == "regex" and not re.search(ref, str(value)): return False
            if op == "exists" and (value is None) == ref: return False
        except TypeError:
            return False
    return True


def matches(allowed, value):
    if isinstance(value, str) and value.startswith("="):
        return True  # expression - can't evaluate statically
    return any(cnd_ok(a, value) for a in allowed)


def visible(prop, siblings, root, version, props, root_props=None, depth=0):
    """Is `prop` shown, given the values set (falling back to the default of whichever
    same-named property is itself visible - this is how n8n resolves e.g. `operation`)."""
    do = prop.get("displayOptions") or {}
    root_props = root_props if root_props is not None else props

    def default_of(key, values, plist):
        if depth > 6:
            return None
        for p in plist:
            if p["name"] == key and visible(p, values, root, version, plist, root_props, depth + 1):
                return p.get("default")
        return None

    def lookup(key):
        if key == "@version":
            return version
        if key.startswith("/"):
            k = key[1:]
            if "." in k:  # e.g. /columns.mappingMode
                head, tail = k.split(".", 1)
                return (root.get(head) or {}).get(tail)
            return root[k] if k in root else default_of(k, root, root_props)
        return siblings[key] if key in siblings else default_of(key, siblings, props)

    for key, allowed in (do.get("show") or {}).items():
        if not matches(allowed, lookup(key)):
            return False
    for key, allowed in (do.get("hide") or {}).items():
        if matches(allowed, lookup(key)):
            return False
    return True


def check_value(prop, value, path, errors, root, version, root_props):
    t = prop.get("type")
    if isinstance(value, str) and value.startswith("="):
        return
    if t in ("options",) and isinstance(prop.get("options"), list) and not prop.get("typeOptions", {}).get("loadOptionsMethod"):
        allowed = [o.get("value") for o in prop["options"]]
        if allowed and value not in allowed:
            errors.append(f"{path}: value {value!r} not one of {allowed[:12]}")
    elif t == "multiOptions" and isinstance(prop.get("options"), list) and isinstance(value, list) \
            and not prop.get("typeOptions", {}).get("loadOptionsMethod"):
        allowed = [o.get("value") for o in prop["options"]]
        for v in value:
            if allowed and v not in allowed:
                errors.append(f"{path}: value {v!r} not allowed")
    elif t == "collection" and isinstance(value, dict):
        check_props(prop.get("options", []), value, path, errors, root, version, True, root_props)
    elif t == "fixedCollection" and isinstance(value, dict):
        groups = {o["name"]: o for o in prop.get("options", [])}
        for gname, entries in value.items():
            if gname not in groups:
                errors.append(f"{path}.{gname}: unknown group (expected one of {list(groups)})")
                continue
            for j, entry in enumerate(entries if isinstance(entries, list) else [entries]):
                if isinstance(entry, dict):
                    check_props(groups[gname].get("values", []), entry, f"{path}.{gname}[{j}]", errors, root, version, True, root_props)


def check_props(props, params, path, errors, root, version, nested=False, root_props=None):
    root_props = root_props if root_props is not None else props
    for key, value in params.items():
        cands = [p for p in props if p["name"] == key]
        if not cands:
            errors.append(f"{path}.{key}: unknown parameter")
            continue
        vis = [p for p in cands if visible(p, params, root, version, props, root_props)]
        if not vis:
            errors.append(f"{path}.{key}: parameter is hidden for these settings (would be ignored)")
            continue
        sub = []
        for p in vis:
            e = []
            check_value(p, value, f"{path}.{key}", e, root, version, root_props)
            if not e:
                break
            sub.append(e)
        else:
            errors.extend(sub[0])


def deep_check(node, defs, cred_types, errors):
    short = node["type"].split(".", 1)[1]
    ver = node["typeVersion"]
    defn = next((d for d in defs if d["name"] == short and ver in versions(d)), None)
    if defn is None:
        avail = [versions(d) for d in defs if d["name"] == short]
        errors.append(f"node '{node['name']}': type {short} v{ver} does not exist (available: {avail})")
        return
    check_props(defn["properties"], node.get("parameters", {}), f"node '{node['name']}'", errors, node.get("parameters", {}), ver)
    allowed = {c["name"] for c in defn.get("credentials", [])}
    for ctype in node.get("credentials", {}):
        if cred_types is not None and ctype not in cred_types:
            errors.append(f"node '{node['name']}': credential type {ctype} does not exist")
        if short == "httpRequest":
            p = node["parameters"]
            want = p.get("nodeCredentialType") or p.get("genericAuthType")
            if ctype != want:
                errors.append(f"node '{node['name']}': credential {ctype} doesn't match auth setting {want}")
        elif ctype not in allowed:
            errors.append(f"node '{node['name']}': credential {ctype} not accepted (accepts {sorted(allowed)})")


# ---------------------------------------------------------------- basic checks
def basic_check(path, wf, errors):
    for key in ("name", "nodes", "connections", "settings"):
        if key not in wf:
            errors.append(f"missing top-level field '{key}'")
    nodes = wf.get("nodes", [])
    names = [n.get("name") for n in nodes]
    ids = [n.get("id") for n in nodes]
    for dup in {x for x in names if names.count(x) > 1}:
        errors.append(f"duplicate node name '{dup}'")
    for dup in {x for x in ids if ids.count(x) > 1}:
        errors.append(f"duplicate node id '{dup}'")
    by_name = {n["name"]: n for n in nodes}
    for n in nodes:
        for f in ("id", "name", "type", "typeVersion", "position", "parameters"):
            if f not in n:
                errors.append(f"node '{n.get('name')}' missing '{f}'")
        if not str(n.get("type", "")).startswith("n8n-nodes-base."):
            errors.append(f"node '{n.get('name')}' is not a built-in node: {n.get('type')}")
        pos = n.get("position")
        if not (isinstance(pos, list) and len(pos) == 2 and all(isinstance(x, (int, float)) for x in pos)):
            errors.append(f"node '{n.get('name')}' has invalid position")
        for ctype, c in (n.get("credentials") or {}).items():
            if c.get("id") != PLACEHOLDER:
                errors.append(f"node '{n['name']}' credential {ctype} is not a placeholder")
        if n.get("type", "").split(".")[-1] in ("webhook", "formTrigger", "stripeTrigger", "wait") and not n.get("webhookId"):
            errors.append(f"node '{n['name']}' should have a webhookId")
    # connections
    targets = {}
    for src, outs in wf.get("connections", {}).items():
        if src not in by_name:
            errors.append(f"connection from unknown node '{src}'")
        for out_list in outs.get("main", []):
            for c in out_list or []:
                if c.get("node") not in by_name:
                    errors.append(f"connection from '{src}' to unknown node '{c.get('node')}'")
                targets.setdefault(src, []).append(c.get("node"))
    # reachability
    triggers = [n["name"] for n in nodes if n["type"].split(".")[-1] in TRIGGER_TYPES]
    if not triggers:
        errors.append("no trigger node")
    seen, stack = set(), list(triggers)
    while stack:
        cur = stack.pop()
        if cur in seen:
            continue
        seen.add(cur)
        stack.extend(targets.get(cur, []))
    for n in nodes:
        if n["type"].endswith("stickyNote"):
            continue
        if n["name"] not in seen:
            errors.append(f"node '{n['name']}' is not connected to any trigger")
    # secrets
    raw = json.dumps(wf)
    for pat, label in SECRET_PATTERNS:
        if re.search(pat, raw):
            errors.append(f"possible {label} found in file")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nodes-json")
    ap.add_argument("--creds-json")
    ap.add_argument("files", nargs="*")
    a = ap.parse_args()
    defs = json.load(open(a.nodes_json)) if a.nodes_json else None
    cred_types = {c["name"] for c in json.load(open(a.creds_json))} if a.creds_json else None
    files = a.files or sorted(glob.glob(os.path.join(ROOT, "workflows", "*", "*.json")))
    total = 0
    for f in files:
        errors = []
        try:
            wf = json.load(open(f))
        except json.JSONDecodeError as e:
            errors.append(f"invalid JSON: {e}")
            wf = None
        if wf is not None:
            basic_check(f, wf, errors)
            if defs:
                for n in wf.get("nodes", []):
                    if n.get("type", "").startswith("n8n-nodes-base."):
                        deep_check(n, defs, cred_types, errors)
        rel = os.path.relpath(f, ROOT)
        if errors:
            total += len(errors)
            print(f"✗ {rel}")
            for e in errors:
                print(f"    - {e}")
        else:
            n = len([x for x in wf["nodes"] if not x["type"].endswith("stickyNote")])
            print(f"✓ {rel} ({n} nodes)")
    mode = "basic + deep (n8n node definitions)" if defs else "basic"
    print(f"\n{len(files)} workflow files checked [{mode}] — {total} error(s)")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
