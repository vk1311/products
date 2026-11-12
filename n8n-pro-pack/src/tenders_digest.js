// One digest per subscriber: soonest-closing first, capped at max_per_digest.
// Anything over the cap is not marked as sent, so it rolls into the next digest.
const settings = $('Settings').first().json;
const MAX = Number(settings.max_per_digest || 30);
const h = (s) => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const day = (d) => (String(d || '').slice(0, 10) || 'not stated');
const groups = {};
for (const it of $input.all()) { const m = it.json; (groups[m.subscriber_email] = groups[m.subscriber_email] || { name: m.subscriber_name, rows: [] }).rows.push(m); }
const today = new Date().toISOString().slice(0, 10);
const sent = $getWorkflowStaticData('global'); sent.keys = sent.keys || {};
const out = [];
for (const email of Object.keys(groups)) {
  const g = groups[email];
  const rows = g.rows.sort((a, b) => String(a.closing_date || '9999').localeCompare(String(b.closing_date || '9999')));
  const shown = rows.slice(0, MAX), extra = rows.length - shown.length;
  const items = shown.map((t) => '<tr><td style="padding:10px 8px;border-bottom:1px solid #e5e5e5;vertical-align:top"><a href="' + h(t.url) + '" style="color:#0b5cad;font-weight:600;text-decoration:none">' + h(t.title) + '</a>' +
    '<div style="color:#555;font-size:13px;margin-top:4px">' + h(t.buyer) + (t.category ? ' &middot; ' + h(t.category) : '') + '</div>' +
    '<div style="color:#777;font-size:12px;margin-top:4px">Delivery: ' + h(t.region_names) + ' &middot; Matched: ' + h(t.matched_keywords) + '</div></td>' +
    '<td style="padding:10px 8px;border-bottom:1px solid #e5e5e5;vertical-align:top;white-space:nowrap;font-size:13px">' + h(day(t.closing_date)) + '</td></tr>').join('');
  const html = '<div style="font-family:Arial,Helvetica,sans-serif;max-width:680px;color:#222"><h2 style="margin:0 0 4px">' + shown.length + ' new tender' + (shown.length === 1 ? '' : 's') + ' for you</h2>' +
    '<p style="margin:0 0 16px;color:#555">Hi ' + h(g.name || 'there') + ', these public tenders match your trades and regions. Soonest closing first.</p>' +
    '<table style="border-collapse:collapse;width:100%"><tr><th align="left" style="padding:6px 8px;border-bottom:2px solid #222">Tender</th><th align="left" style="padding:6px 8px;border-bottom:2px solid #222">Closes</th></tr>' + items + '</table>' +
    (extra > 0 ? '<p style="color:#555">' + extra + ' more matched and will come in your next digest.</p>' : '') +
    '<p style="color:#888;font-size:12px;margin-top:24px">Source: CanadaBuys open tender notices (Open Government Licence - Canada). Always confirm details and deadlines on the official notice.<br>' +
    h(settings.sender_name) + (settings.postal_address ? ' &middot; ' + h(settings.postal_address) : '') + '<br>To stop these emails, reply with STOP.</p></div>';
  // Mark as sent only in production runs, so test runs can be repeated.
  if ($execution.mode !== 'manual') for (const t of shown) sent.keys[t.seen_key] = today;
  out.push({ json: { to: email, subject: shown.length + ' new tender' + (shown.length === 1 ? '' : 's') + ' matching your trades (' + today + ')', html, tender_count: shown.length, held_for_next_digest: extra } });
}
return out;
