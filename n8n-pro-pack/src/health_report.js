const d = $('Domain to check').first().json.domain;
const ans = (n) => (($(n).first().json.Answer) || []).map(a => String(a.data).replace(/^"|"$/g, '').replace(/" "/g, ''));
const txt = ans('Root TXT (SPF)'), dm = ans('DMARC'), mx = ans('MX');
const spf = txt.filter(t => t.toLowerCase().startsWith('v=spf1'));
const dmarc = dm.find(t => t.toLowerCase().startsWith('v=dmarc1')) || '';
const policy = (dmarc.match(/p=(\w+)/i) || [])[1] || '';
const sels = $('DKIM selectors').all().map(i => i.json.selector);
const dkimFound = $('DKIM lookup').all().map((it, i) => ((it.json.Answer || []).length ? sels[i] : null)).filter(Boolean);
const w = $('Website').first().json; const h = Object.fromEntries(Object.entries(w.headers || {}).map(([k, v]) => [k.toLowerCase(), v]));
const sec = ['strict-transport-security', 'content-security-policy', 'x-content-type-options', 'x-frame-options', 'referrer-policy'];
let subs = [];
try { subs = [...new Set(JSON.parse($('Certificate log (crt.sh)').first().json.data || '[]').flatMap(r => String(r.name_value).split('\n')))].filter(n => n.endsWith(d) && !n.startsWith('*')).sort(); } catch (e) { subs = null; }
const checks = [
  { item: 'SPF record', ok: spf.length === 1, detail: spf.length === 0 ? 'Missing: other servers can send as you' : spf.length > 1 ? 'More than one SPF record (only one is allowed)' : spf[0] },
  { item: 'DMARC record', ok: !!dmarc, detail: dmarc || 'Missing: no instruction for spoofed mail' },
  { item: 'DMARC enforced', ok: /^(quarantine|reject)$/i.test(policy), detail: policy ? 'p=' + policy + (policy === 'none' ? ' (monitoring only, spoofed mail still delivered)' : '') : 'n/a' },
  { item: 'DKIM signing key', ok: dkimFound.length > 0, detail: dkimFound.length ? 'Found: ' + dkimFound.join(', ') : 'None found on common selectors (may use a custom one)' },
  { item: 'Receives email (MX)', ok: mx.length > 0, detail: mx.join(', ') || 'No MX record' },
  { item: 'Website loads over HTTPS', ok: w.statusCode >= 200 && w.statusCode < 400, detail: 'Status ' + (w.statusCode || 'no response') },
  ...sec.map(k => ({ item: 'Header: ' + k, ok: !!h[k], detail: h[k] ? 'Set' : 'Not set' })),
];
const score = checks.filter(c => c.ok).length;
return [{ json: { domain: d, checkedAt: new Date().toISOString(), score: score + ' of ' + checks.length, checks, subdomainsInCertificateLogs: subs === null ? 'crt.sh did not answer, try again later' : subs } }];
