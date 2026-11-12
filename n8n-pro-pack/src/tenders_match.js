// Pair every subscriber with every tender that matches one of their keywords AND one of their regions.
// Keywords match at the start of a word: "landscap" catches "landscaping", "electric" catches "electrical".
// Tenders already sent to a subscriber are skipped (remembered in this workflow's static data,
// which n8n keeps between production runs; manual test runs do not save it).
const tenders = $input.all().map((i) => i.json);
const subs = $('Subscribers').all().map((i) => i.json).filter((s) => s && s.email && s.active !== false);
const sent = $getWorkflowStaticData('global'); sent.keys = sent.keys || {};
const esc = (s) => s.replace(/[.*+?^$()|[\]\\{}]/g, '\\$&');
const out = [];
for (const s of subs) {
  const email = String(s.email).trim().toLowerCase();
  const kws = String(s.keywords || '').split(',').map((k) => k.trim().toLowerCase()).filter(Boolean);
  const regions = String(s.regions || '').split(',').map((r) => r.trim().toUpperCase()).filter(Boolean);
  if (!kws.length || !regions.length) continue;
  const tests = kws.map((k) => ({ k, re: new RegExp('(^|[^a-z0-9])' + esc(k)) }));
  for (const t of tenders) {
    const key = email + '|' + t.tender_id;
    if (sent.keys[key]) continue;
    const regionHit = (t.regions || []).filter((r) => regions.includes(r));
    if (!regionHit.length) continue;
    const hits = tests.filter((x) => x.re.test(t.search_text || '')).map((x) => x.k);
    if (!hits.length) continue;
    out.push({ json: { seen_key: key, subscriber_name: s.name || '', subscriber_email: email, matched_keywords: hits.join(', '),
      tender_id: t.tender_id, title: t.title, category: t.category, buyer: t.buyer, closing_date: t.closing_date, region_names: t.region_names, url: t.url } });
  }
}
return out;
