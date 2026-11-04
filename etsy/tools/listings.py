"""Etsy listing copy generated from each form spec."""

import io

from engine import build
from common import TAX

GENERIC_TAGS = [
    "canadian business", "small business form", "fillable pdf", "printable form",
    "business template", "instant download", "office printable", "letter size form",
    "business printable", "editable pdf form",
]

CAT_TAGS = {
    "billing": ["invoice template", "billing form", "bookkeeping form", "gst hst"],
    "finance": ["bookkeeping form", "accounting form", "expense tracker", "finance printable"],
    "ops": ["operations form", "work form", "job form", "service business"],
    "hr": ["hr form", "employee form", "human resources", "payroll form"],
    "safety": ["safety form", "workplace safety", "ohs form", "incident form"],
    "cleaning": ["cleaning checklist", "cleaning business", "janitorial form", "cleaning service"],
    "rental": ["rental property", "landlord form", "property manager", "rental printable"],
    "food": ["restaurant form", "food safety", "kitchen form", "cafe printable"],
}

CANADA = {
    "billing": "Canadian-ready: GST/HST and PST/QST tax lines, a province/territory drop-down, postal code fields and amounts in Canadian dollars.",
    "finance": "Canadian-ready: amounts in Canadian dollars, kilometres instead of miles where relevant, and GST/HST columns where you need them.",
    "ops": "Canadian-ready: province/territory drop-down, postal code fields, metric-friendly and Canadian spelling throughout.",
    "hr": "Canadian-ready: written with Canadian workplaces in mind (provinces, SIN, CPP/EI, TD1 where relevant) and avoids questions that provincial human rights codes discourage on applications.",
    "safety": "Canadian-ready: written for Canadian workplaces with province/territory fields, metric units and space to note your provincial workers' compensation board claim number.",
    "cleaning": "Canadian spelling throughout, province/territory and postal code fields where needed.",
    "rental": "Canadian-ready: province/territory drop-down, postal codes and amounts in Canadian dollars. Check your provincial residential tenancy rules before use.",
    "food": "Canadian-ready: temperatures in degrees Celsius and metric units throughout.",
}

TITLE_MAX = 140


def _title(f):
    name = f["name"]
    segs = [name, "Fillable PDF", f"Printable {f['short']}", "Canada Small Business Form",
            "Letter Size", "Instant Download"]
    if f.get("prov"):
        segs.insert(3, "GST HST Invoice")
    while True:
        t = ", ".join(segs)
        if len(t) <= TITLE_MAX:
            return t
        segs.pop(-1 if len(segs) > 3 else 2)


def _tags(f):
    out = []
    for t in f.get("tags", []) + CAT_TAGS[f["cat"]] + GENERIC_TAGS:
        t = t.lower().strip()
        if 0 < len(t) <= 20 and t not in out:
            out.append(t)
    assert len(out) >= 13, f["slug"]
    return out[:13]


def _join(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def _contents(f):
    out = []
    named = sum(1 for el in f["body"] if el["t"] in ("section", "pair"))
    for el in f["body"]:
        t = el["t"]
        if t == "table" and named >= 2 and el.get("rows") != "fill":
            continue
        if t == "section":
            out.append(el["title"].title() if el["title"].isupper() else el["title"])
        elif t == "pair":
            out += [el["l"][0], el["r"][0]]
        elif t == "table":
            out.append("table with " + _join(c[0] for c in el["cols"]) + " columns")
        elif t in ("groups",):
            out.append("checklist: " + _join(g[0] for g in el["groups"]))
        elif t == "checklist":
            out.append(f"{len(el['items'])}-item checklist")
        elif t == "matrix":
            out.append(f"{len(el['items'])}-point check grid ({' / '.join(el['cols'])})")
        elif t == "totals":
            out.append("totals: " + _join(l if isinstance(l, str) else l[0] for l in el["lines"]))
        elif t == "signatures":
            out.append("signature and date lines")
        elif t == "rules":
            out.append(f"{len(el['items'])} pre-written points")
        elif t == "elist":
            n = sum(1 for x in el["items"] if x)
            out.append(f"{n} pre-written lines you can edit or replace" if n else "blank lines")
        elif t == "yesno":
            out.append(f"{len(el['qs'])} yes/no questions")
        elif t == "cards":
            out.append(f"{el['n']} cut-apart copies per page")
    seen, res = set(), []
    for o in out:
        k = o.lower()
        if k not in seen:
            seen.add(k)
            res.append(o)
    return res


def _pages(f):
    return build(io.BytesIO(), f)


def listing(f, fname):
    pages = _pages(f)
    canada = f.get("canada") or CANADA[f["cat"]]
    if f.get("prov"):
        pname, taxes, _ = TAX[f["prov"]]
        canada = (f"Made for {pname}: the totals are labelled " +
                  _join(f"{n} {r}" for n, r in taxes) +
                  " (rates current as of 2026), with a province/territory drop-down, postal code fields and amounts in Canadian dollars.")
    lines = [
        f["about"].rstrip(".") + ".",
        "",
        "WHAT YOU GET",
        f"- 1 PDF file, {pages} page{'s' if pages > 1 else ''}, US Letter size (8.5 x 11 in)",
        "- Fillable fields: type on screen, save and print - or print blank copies and fill by hand",
        "- Clean, minimal design that prints well in black and white and saves ink",
    ]
    contents = _contents(f)
    if contents:
        lines.append("- Includes: " + "; ".join(contents))
    lines += [
        "",
        "MADE FOR CANADA",
        "- " + canada,
        "",
        "HOW TO USE",
        "1. Download the PDF after purchase.",
        "2. Open it in any free PDF reader app to type into the fields (checkboxes and drop-downs included).",
        "3. Save a filled copy for each job or client, or print as many blank copies as you need.",
        "",
        "PLEASE NOTE",
        "- This is a digital download. No physical item will be shipped.",
    ] + (["- Totals are typed in, not auto-calculated."] if any(e["t"] == "totals" for e in f["body"]) else []) + [
        "- This template is not legal, tax or accounting advice and is not an official government form. Rules differ by province and change over time, so confirm what applies to you.",
        "- For use in your own business. Please do not resell or share the file.",
    ]
    return {
        "file": f"forms/{fname}",
        "title": _title(f),
        "description": "\n".join(lines),
        "tags": _tags(f),
        "price": f["price"],
    }
