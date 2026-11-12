import json, os, uuid
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "..", "workflows")
os.makedirs(OUT, exist_ok=True)
js = lambda f: open(os.path.join(H, f)).read()
nid = lambda: str(uuid.uuid4())
def node(name, typ, ver, pos, params, **kw): return {"id": nid(), "name": name, "type": typ, "typeVersion": ver, "position": pos, "parameters": params, **kw}
def code(name, pos, src, mode="runOnceForAllItems", **kw): return node(name, "n8n-nodes-base.code", 2, pos, {"mode": mode, "language": "javaScript", "jsCode": src}, **kw)
def note(name, pos, text, color=4, w=420, h=300): return node(name, "n8n-nodes-base.stickyNote", 1, pos, {"content": text, "color": color, "width": w, "height": h})
def chain(*names): return {a: {"main": [[{"node": b, "type": "main", "index": 0}]]} for a, b in zip(names, names[1:])}
def dns(name, pos, qname, qtype): return node(name, "n8n-nodes-base.httpRequest", 4.5, pos, {"method": "GET", "url": "https://dns.google/resolve", "sendQuery": True, "specifyQuery": "keypair",
    "queryParameters": {"parameters": [{"name": "name", "value": qname}, {"name": "type", "value": qtype}]}, "options": {"timeout": 15000, "response": {"response": {"neverError": True}}}}, executeOnce=True)
def save(fn, name, nodes, conns):
    json.dump({"name": name, "nodes": nodes, "connections": conns, "settings": {"executionOrder": "v1"}, "pinData": {}}, open(os.path.join(OUT, fn), "w"), indent=2)

D = "$('Domain to check').first().json.domain"
nodes = [node("Run check", "n8n-nodes-base.manualTrigger", 1, [0, 0], {}),
  code("Domain to check", [224, 0], "// Change the domain here, then click Execute workflow\nreturn [{ json: { domain: 'example.com' } }];"),
  dns("Root TXT (SPF)", [448, 0], "={{ " + D + " }}", "TXT"),
  dns("DMARC", [672, 0], "=_dmarc.{{ " + D + " }}", "TXT"),
  dns("MX", [896, 0], "={{ " + D + " }}", "MX"),
  node("Website", "n8n-nodes-base.httpRequest", 4.5, [1120, 0], {"method": "GET", "url": "=https://{{ " + D + " }}", "options": {"timeout": 15000, "response": {"response": {"fullResponse": True, "neverError": True, "responseFormat": "text"}}}}, executeOnce=True),
  node("Certificate log (crt.sh)", "n8n-nodes-base.httpRequest", 4.5, [1344, 0], {"method": "GET", "url": "https://crt.sh/", "sendQuery": True, "specifyQuery": "keypair",
       "queryParameters": {"parameters": [{"name": "q", "value": "=%.{{ " + D + " }}"}, {"name": "output", "value": "json"}]}, "options": {"timeout": 30000, "response": {"response": {"neverError": True, "responseFormat": "text"}}}}, executeOnce=True, onError="continueRegularOutput"),
  code("DKIM selectors", [1568, 0], "const d = " + D + ";\nreturn ['google', 'selector1', 'selector2', 'default', 'k1', 'resend', 'mail', 's1', 'mxvault', 'zoho'].map(s => ({ json: { selector: s, name: s + '._domainkey.' + d } }));", executeOnce=True),
  node("DKIM lookup", "n8n-nodes-base.httpRequest", 4.5, [1792, 0], {"method": "GET", "url": "https://dns.google/resolve", "sendQuery": True, "specifyQuery": "keypair",
       "queryParameters": {"parameters": [{"name": "name", "value": "={{ $json.name }}"}, {"name": "type", "value": "TXT"}]}, "options": {"timeout": 15000, "response": {"response": {"neverError": True}}}}),
  code("Build report", [2016, 0], js("health_report.js")),
  note("How to use", [0, 200], "## Email + website health check\n\n1. Open **Domain to check** and type the domain.\n2. Click **Execute workflow**.\n3. Open **Build report** to read the result: SPF, DKIM, DMARC, MX, HTTPS, five security headers, and subdomains seen in public certificate logs.\n\nNo credentials needed. Uses Google public DNS and crt.sh. Nothing is sent anywhere.\n\nTip: run it on a prospect's domain before a sales call, or monthly on your clients' domains.")]
save("01-email-website-health-check.json", "Email + website health check", nodes,
     chain("Run check", "Domain to check", "Root TXT (SPF)", "DMARC", "MX", "Website", "Certificate log (crt.sh)", "DKIM selectors", "DKIM lookup", "Build report"))

UA = {"parameters": [{"name": "User-Agent", "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"}, {"name": "Accept", "value": "text/html,application/xhtml+xml"}]}
FETCH = lambda url: {"method": "GET", "url": url, "sendHeaders": True, "headerParameters": UA, "options": {"timeout": 15000, "redirect": {"redirect": {"followRedirects": True, "maxRedirects": 5}}, "response": {"response": {"fullResponse": True, "neverError": True, "responseFormat": "text"}}}}
sites_js = """// One line per business. Paste from a spreadsheet, or replace this node with a Google Sheets / Airtable / CRM node
// that outputs items with the same fields: name, website, review_count, google_rating (the last two are optional).
const sites = [
  { name: 'Example Plumbing', website: 'example.com', review_count: 42, google_rating: 4.7 },
  { name: 'Sample Salon', website: 'https://www.example.org', review_count: 8, google_rating: 4.2 },
];
return sites.map((s) => {
  const bare = String(s.website || '').trim().replace(/^[a-z]+:\\/\\//i, '').replace(/\\/+$/, '');
  return { json: { ...s, website: String(s.website || ''), https_url: bare ? 'https://' + bare : '', http_url: bare ? 'http://' + bare : '' } };
});"""
nodes = [node("Run now", "n8n-nodes-base.manualTrigger", 1, [0, 0], {}),
  node("Settings", "n8n-nodes-base.set", 3.5, [224, 0], {"mode": "manual", "includeOtherFields": False, "assignments": {"assignments": [
       {"id": "s1", "name": "stale_year", "value": 2022, "type": "number"}, {"id": "s2", "name": "pause_seconds", "value": 3, "type": "number"}]}}),
  code("Websites to check", [448, 0], sites_js),
  node("One site at a time", "n8n-nodes-base.splitInBatches", 3, [672, 0], {"batchSize": 1, "options": {}}),
  node("Fetch homepage over HTTPS", "n8n-nodes-base.httpRequest", 4.5, [896, 120], FETCH("={{ $json.https_url }}"), alwaysOutputData=True, onError="continueRegularOutput"),
  node("Did HTTPS answer?", "n8n-nodes-base.if", 2.3, [1120, 120], {"conditions": {"options": {"caseSensitive": True, "leftValue": "", "typeValidation": "loose", "version": 2},
       "conditions": [{"leftValue": "={{ Number($json.statusCode || 0) }}", "rightValue": 0, "operator": {"type": "number", "operation": "gt"}}], "combinator": "and"}, "options": {}}),
  node("Try plain HTTP instead", "n8n-nodes-base.httpRequest", 4.5, [1344, 260], FETCH("={{ $('One site at a time').item.json.http_url }}"), alwaysOutputData=True, onError="continueRegularOutput"),
  code("Detect tech and score", [1568, 120], js("score.js"), mode="runOnceForEachItem"),
  node("Polite pause", "n8n-nodes-base.wait", 1.1, [1792, 120], {"resume": "timeInterval", "amount": "={{ $('Settings').first().json.pause_seconds }}", "unit": "seconds"}, webhookId=nid()),
  code("Results, highest score first", [896, -160], "return $('Detect tech and score').all().sort((a, b) => b.json.signal_score - a.json.signal_score);"),
  note("How to use", [224, 300], "## Website signal score\n\n1. Put your list in **Websites to check** (or swap that node for Google Sheets).\n2. Click **Execute workflow**.\n3. Open **Results, highest score first**.\n\nEach site is opened once (15 s timeout, 3 s pause between sites). It detects the platform (Wix, Squarespace, WordPress...), booking, CRM/chat and analytics tools, and scores 0-100. Higher = more gaps a better site, booking or quoting tool would fix. Every point is listed at the top of **Detect tech and score**.\n\nRows with score_reliable = false were blocked by a bot wall or are JavaScript-only pages: check those by hand.\n\nUse it to prioritise who to talk to, not to send bulk email. In Canada, CASL applies to commercial email.", w=460, h=380)]
conns = chain("Run now", "Settings", "Websites to check", "One site at a time")
conns["One site at a time"] = {"main": [[{"node": "Results, highest score first", "type": "main", "index": 0}], [{"node": "Fetch homepage over HTTPS", "type": "main", "index": 0}]]}
conns["Fetch homepage over HTTPS"] = {"main": [[{"node": "Did HTTPS answer?", "type": "main", "index": 0}]]}
conns["Did HTTPS answer?"] = {"main": [[{"node": "Detect tech and score", "type": "main", "index": 0}], [{"node": "Try plain HTTP instead", "type": "main", "index": 0}]]}
conns["Try plain HTTP instead"] = {"main": [[{"node": "Detect tech and score", "type": "main", "index": 0}]]}
conns["Detect tech and score"] = {"main": [[{"node": "Polite pause", "type": "main", "index": 0}]]}
conns["Polite pause"] = {"main": [[{"node": "One site at a time", "type": "main", "index": 0}]]}
save("02-website-signal-score.json", "Website signal score (prospect list)", nodes, conns)

subs_js = """// Your subscribers. Replace these examples, or swap this node for Google Sheets / a data table.
// keywords: comma list of word starts ("landscap" catches landscaping). regions: NS,NB,PE,NL,QC,ON,MB,SK,AB,BC,YT,NT,NU,CANADA
return [
  { name: 'Sample Landscaping', email: 'owner@example.com', keywords: 'landscap, snow, grounds', regions: 'NS,CANADA', active: true },
  { name: 'Sample Electric', email: 'office@example.com', keywords: 'electric, lighting, generator', regions: 'NS,NB', active: true },
].map((s) => ({ json: s }));"""
nodes = [node("Run now", "n8n-nodes-base.manualTrigger", 1, [0, 0], {}),
  node("Daily 9:43am (off)", "n8n-nodes-base.scheduleTrigger", 1.4, [0, 200], {"rule": {"interval": [{"field": "cronExpression", "expression": "43 9 * * 1-5"}]}}, disabled=True),
  node("Settings", "n8n-nodes-base.set", 3.5, [224, 100], {"mode": "manual", "includeOtherFields": False, "assignments": {"assignments": [
       {"id": "t1", "name": "canadabuys_csv_url", "value": "https://canadabuys.canada.ca/opendata/pub/openTenderNotice-ouvertAvisAppelOffres.csv", "type": "string"},
       {"id": "t2", "name": "provinces", "value": "NS,NB,PE,NL", "type": "string"},
       {"id": "t3", "name": "max_per_digest", "value": 30, "type": "number"},
       {"id": "t4", "name": "sender_name", "value": "Your Business Tender Alerts", "type": "string"},
       {"id": "t5", "name": "postal_address", "value": "", "type": "string"}]}}),
  node("Download CanadaBuys open tenders", "n8n-nodes-base.httpRequest", 4.5, [448, 100], {"method": "GET", "url": "={{ $('Settings').first().json.canadabuys_csv_url }}",
       "options": {"timeout": 120000, "redirect": {"redirect": {"followRedirects": True, "maxRedirects": 5}}, "response": {"response": {"responseFormat": "file", "outputPropertyName": "data"}}}}, retryOnFail=True, maxTries=3, waitBetweenTries=5000, executeOnce=True),
  node("Read the CSV", "n8n-nodes-base.extractFromFile", 1.1, [672, 100], {"operation": "csv", "binaryPropertyName": "data", "options": {"headerRow": True, "enableBOM": True, "relaxQuotes": True}}),
  code("Keep tenders in my provinces", [896, 100], js("tenders_keep.js")),
  code("Subscribers", [336, 300], subs_js),
  code("Match tenders to subscribers", [1120, 100], js("tenders_match.js")),
  code("Build per-subscriber digests", [1344, 100], js("tenders_digest.js")),
  node("Send email (connect your account)", "n8n-nodes-base.noOp", 1, [1568, 100], {}),
  note("How to use", [224, 420], "## Public tender alerts (CanadaBuys)\n\nDownloads the CanadaBuys open tender notices CSV (Government of Canada open data), keeps tenders delivered to the provinces in **Settings**, matches them to each subscriber's keywords and regions, skips ones already sent, and builds one HTML digest per subscriber.\n\n1. Edit **Settings** (provinces, sender name, your mailing address).\n2. Replace the examples in **Subscribers**.\n3. Run it and open **Build per-subscriber digests** to read the emails.\n4. Replace **Send email** with your Gmail, Outlook, SMTP or Resend node: to = {{ $json.to }}, subject = {{ $json.subject }}, HTML = {{ $json.html }}.\n5. Turn on the daily trigger and activate.\n\nAlready-sent tenders are remembered only in production runs. CASL: email only people who signed up, and fill in your mailing address.", color=2, w=520, h=420)]
conns = chain("Settings", "Subscribers", "Download CanadaBuys open tenders", "Read the CSV", "Keep tenders in my provinces", "Match tenders to subscribers", "Build per-subscriber digests", "Send email (connect your account)")
conns["Run now"] = {"main": [[{"node": "Settings", "type": "main", "index": 0}]]}
conns["Daily 9:43am (off)"] = {"main": [[{"node": "Settings", "type": "main", "index": 0}]]}
save("03-public-tender-alerts.json", "Public tender alerts (CanadaBuys)", nodes, conns)
print("built", os.listdir(OUT))
