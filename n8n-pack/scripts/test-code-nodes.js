// Runs the JavaScript inside every Code node against sample data, using a small mock of n8n's runtime,
// and syntax-checks every {{ expression }} in the pack.
//
//   npm install luxon        (the date library n8n uses)
//   node scripts/test-code-nodes.js
const fs = require('fs');
const path = require('path');
const { DateTime } = require('luxon');
const PACK = process.argv[2] || path.join(__dirname, '..');

const files = fs.readdirSync(path.join(PACK, 'workflows')).sort()
  .map((d) => path.join(PACK, 'workflows', d, d + '.json'));

let failures = 0;
const fail = (m) => { failures++; console.log('  ✗ ' + m); };

// ---------- 1. expression syntax check ----------
let exprCount = 0;
function walk(v, where, cb) {
  if (typeof v === 'string') cb(v, where);
  else if (Array.isArray(v)) v.forEach((x, i) => walk(x, where + '[' + i + ']', cb));
  else if (v && typeof v === 'object') Object.entries(v).forEach(([k, x]) => walk(x, where + '.' + k, cb));
}
for (const f of files) {
  const wf = JSON.parse(fs.readFileSync(f));
  for (const n of wf.nodes) {
    if (n.type.endsWith('.code')) {
      try { new Function('$input', '$', 'DateTime', '$getWorkflowStaticData', '$execution', `return (async () => {\n${n.parameters.jsCode}\n})`); }
      catch (e) { fail(`${path.basename(f)} / ${n.name}: JS syntax error ${e.message}`); }
      continue;
    }
    walk(n.parameters, n.name, (s, where) => {
      if (!s.startsWith('=')) return;
      const re = /\{\{([\s\S]*?)\}\}/g; let m;
      while ((m = re.exec(s))) {
        exprCount++;
        try { new Function('$json', '$', '$now', 'DateTime', `return (${m[1]});`); }
        catch (e) { fail(`${path.basename(f)} / ${where}: bad expression {{${m[1]}}} → ${e.message}`); }
      }
    });
  }
}
console.log(`Expressions syntax-checked: ${exprCount}`);

// ---------- 2. run Code nodes with scenarios ----------
const load = (slug) => JSON.parse(fs.readFileSync(files.find((f) => f.includes(slug))));
function configOf(wf) {
  const c = wf.nodes.find((n) => n.name === 'Config');
  return Object.fromEntries(c.parameters.assignments.assignments.map((a) => [a.name, a.value]));
}
const staticData = {};
async function run(slug, nodeName, { input = [], nodes = {}, mode = 'production', cfg = {} } = {}) {
  const wf = load(slug);
  const node = wf.nodes.find((n) => n.name === nodeName);
  if (!node) throw new Error('no node ' + nodeName);
  const conf = { ...configOf(wf), ...cfg };
  const wrap = (arr) => arr.map((j) => ({ json: j }));
  const items = { Config: wrap([conf]), ...Object.fromEntries(Object.entries(nodes).map(([k, v]) => [k, wrap(v)])) };
  const $ = (name) => {
    if (!items[name]) throw new Error(`$('${name}') not mocked`);
    return { all: () => items[name], first: () => items[name][0], item: items[name][0] };
  };
  const $input = { all: () => wrap(input), first: () => wrap(input)[0] };
  staticData[slug] = staticData[slug] || {};
  const fn = new Function('$input', '$', 'DateTime', '$getWorkflowStaticData', '$execution', `return (async () => {\n${node.parameters.jsCode}\n})();`);
  const out = await fn($input, $, DateTime, () => staticData[slug], { mode });
  if (!Array.isArray(out)) throw new Error('Code node must return an array');
  out.forEach((o) => { if (!o || typeof o.json !== 'object') throw new Error('item without json'); });
  return out.map((o) => o.json);
}

const tz = 'America/New_York';
const now = DateTime.now().setZone(tz);
const d = (days) => now.plus({ days }).toISODate();
const check = (label, cond, extra = '') => (cond ? console.log('  ✓ ' + label) : fail(label + ' ' + extra));

(async () => {
  try {
    console.log('02 lead capture');
    let o = await run('02-', 'Clean Up Lead', { nodes: { 'Lead Webhook': [
      { body: { first_name: 'Jane', last_name: 'Doe', email: ' Jane@Example.com ', utm_source: 'google' }, query: {}, headers: {} },
      { body: { name: 'Bot', email: 'bot@spam.com', website_url: 'http://x' }, query: {}, headers: {} },
      { body: { name: 'X', email: 'not-an-email' }, query: {}, headers: {} }] } });
    check('normalises name/email/source', o[0].name === 'Jane Doe' && o[0].email === 'jane@example.com' && o[0].source === 'google' && o[0].valid);
    check('honeypot + bad email rejected', !o[1].valid && !o[2].valid);

    console.log('03 invoice reminders');
    o = await run('03-', 'Pick Invoices to Remind', { input: [
      { 'Invoice ID': 'A', 'Client Name': 'Ann Lee', 'Client Email': 'a@x.com', Amount: 450, Currency: 'USD', 'Due Date': d(3), Status: 'Unpaid', 'Payment Link': 'https://pay' },
      { 'Invoice ID': 'B', 'Client Name': 'Bob', 'Client Email': 'b@x.com', Amount: '$1,200.50', 'Due Date': d(0), Status: '' },
      { 'Invoice ID': 'C', 'Client Name': 'Cy', 'Client Email': 'c@x.com', Amount: 99, 'Due Date': d(-8), Status: 'Unpaid', 'Last Reminder Stage': 'due' },
      { 'Invoice ID': 'D', 'Client Name': 'Di', 'Client Email': 'd@x.com', Amount: 99, 'Due Date': d(-8), Status: 'Unpaid', 'Last Reminder Stage': 'overdue-7' },
      { 'Invoice ID': 'E', 'Client Name': 'Ed', 'Client Email': 'e@x.com', Amount: 99, 'Due Date': d(-40), Status: 'Paid' },
      { 'Invoice ID': 'F', 'Client Name': 'Fi', 'Client Email': 'f@x.com', Amount: 99, 'Due Date': now.minus({ days: 31 }).toFormat('M/d/yyyy'), Status: 'Unpaid' },
      { 'Invoice ID': 'G', 'Client Name': 'Gi', 'Client Email': 'g@x.com', Amount: 99, 'Due Date': d(10), Status: 'Unpaid' }] });
    const st = Object.fromEntries(o.map((x) => [x.invoiceId, x.stage]));
    check('stages chosen correctly', JSON.stringify(st) === JSON.stringify({ A: 'before-3', B: 'due', C: 'overdue-7', F: 'final-30' }), JSON.stringify(st));
    check('amount formatted + pay button', o[0].html.includes('$450.00') && o[0].html.includes('https://pay') && o[1].subject.includes('due today'));
    check('subject has no html', !/[<>]/.test(o.map((x) => x.subject).join('')));

    console.log('04 review requests');
    o = await run('04-', 'Find Customers to Ask', { input: [
      { 'Job ID': '1', 'Customer Name': 'Sam Lee', 'Customer Email': 's@x.com', 'Completed Date': d(-1) },
      { 'Job ID': '2', 'Customer Email': 't@x.com', 'Completed Date': d(0) },
      { 'Job ID': '3', 'Customer Email': 'u@x.com', 'Completed Date': d(-2), 'Review Requested': 'Yes' },
      { 'Job ID': '4', 'Customer Email': 'v@x.com', 'Completed Date': d(-45) }] });
    check('only eligible job picked', o.length === 1 && o[0].jobId === '1' && o[0].name === 'Sam');

    console.log('05 appointment reminders');
    const at = (h) => { const t = now.plus({ hours: h }); return { Date: t.toISODate(), Time: t.toFormat('h:mm a') }; };
    o = await run('05-', 'Find Upcoming Appointments', { input: [
      { 'Appointment ID': 'A1', 'Client Name': 'P', 'Client Email': 'p@x.com', ...at(20), Status: 'Booked' },
      { 'Appointment ID': 'A2', 'Client Email': 'q@x.com', ...at(1.5), 'Reminder 24h Sent': 'yes' },
      { 'Appointment ID': 'A3', 'Client Email': 'r@x.com', ...at(20), 'Reminder 24h Sent': '2026-01-01' },
      { 'Appointment ID': 'A4', 'Client Email': 's@x.com', ...at(5), Status: 'Cancelled' },
      { 'Appointment ID': 'A5', 'Client Email': 't@x.com', ...at(30) },
      { 'Appointment ID': 'A6', 'Client Email': 'u@x.com', ...at(-1) }] });
    check('24h + 2h stages', JSON.stringify(o.map((x) => x.appointmentId + ':' + x.stage)) === '["A1:24h","A2:2h"]', JSON.stringify(o.map((x) => x.appointmentId + ':' + x.stage)));
    check('keeps existing stamps', o[1].reminder24 === 'yes' && o[1].reminder2 !== '' && o[0].reminder2 === '');

    console.log('06 social');
    o = await run('06-', 'Prepare Post', { nodes: { 'New Post Form': [{ 'Post text': 'x'.repeat(400), 'Link (optional)': 'https://a.co', 'Post to': ['X (Twitter)', 'Telegram Channel'] }] } });
    check('X post trimmed & flags set', o[0].xPost.length <= 280 + 30 && o[0].toX && o[0].toTelegram && !o[0].toLinkedIn, o[0].xPost.length);

    console.log('10 daily sales');
    o = await run('10-', 'Build Summary', { input: [
      { Date: now.toFormat('yyyy-MM-dd') + ' 09:00', Amount: 100, 'Customer Name': 'A' },
      { Date: now.toFormat('yyyy-MM-dd') + ' 10:00', Amount: '50', 'Customer Name': 'B' },
      { Date: now.minus({ days: 1 }).toFormat('yyyy-MM-dd') + ' 10:00', Amount: 300 }, {}] });
    check('summary totals', o[0].subject.includes('$150.00 from 2 orders'), o[0].subject);
    o = await run('10-', 'Build Summary', { input: [{}], cfg: { skipIfNoSales: true } });
    check('skip when no sales', o.length === 0);

    console.log('12 no-shows');
    o = await run('12-', 'Find No-Shows', { input: [
      { 'Appointment ID': 'N1', 'Client Email': 'a@x.com', Date: d(0), Status: 'No-show' },
      { 'Appointment ID': 'N2', 'Client Email': 'b@x.com', Date: d(-1), Status: 'no show' },
      { 'Appointment ID': 'N3', 'Client Email': 'c@x.com', Date: d(-1), Status: 'No-show', 'No-show Followed Up': d(-1) },
      { 'Appointment ID': 'N4', 'Client Email': 'd@x.com', Date: d(-10), Status: 'No-show' }] });
    check('no-shows picked', o.map((x) => x.appointmentId).join() === 'N1,N2', o.map((x) => x.appointmentId).join());

    console.log('13 quote router');
    o = await run('13-', 'Route & Prioritize', { nodes: { 'Quote Request Form': [{ Name: 'Maria Garcia', Email: 'm@x.com', Phone: '1', Service: 'Repair', Budget: '$2,000 - $10,000', 'When do you need this?': 'ASAP', 'Project details': 'a\n<b>' }] } });
    check('routed + HOT', o[0].assignedTo === 'service@yourbusiness.com' && o[0].priority === 'HOT' && o[0].detailsHtml === 'a<br>&lt;b&gt;');

    console.log('14 lead follow-ups');
    o = await run('14-', 'Find Leads to Follow Up', { input: [
      { Date: d(-3), Name: 'A', Email: 'a@x.com' },
      { Date: d(-6), Name: 'B', Email: 'b@x.com', 'Follow-ups Sent': 1, 'Last Follow-up': d(-4) },
      { Date: d(-6), Name: 'C', Email: 'c@x.com', 'Follow-ups Sent': 1, 'Last Follow-up': d(0) },
      { Date: d(-11), Name: 'D', Email: 'd@x.com', 'Follow-ups Sent': 3 },
      { Date: d(-3), Name: 'E', Email: 'e@x.com', Status: 'Won' },
      { Date: d(-1), Name: 'F', Email: 'f@x.com' }] });
    check('follow-up steps', o.map((x) => x.email + '#' + x.step).join() === 'a@x.com#1,b@x.com#2', o.map((x) => x.email + '#' + x.step).join());
    const dg = await run('14-', 'Build Owner Digest', { input: o });
    check('digest built', dg.length === 1 && dg[0].subject.startsWith('2 lead'));

    console.log('15 birthdays');
    const md = now.toFormat('MM-dd');
    o = await run('15-', 'Find Birthdays Today', { input: [
      { Name: 'O', Email: 'o@x.com', Birthday: '1990-' + md },
      { Name: 'P', Email: 'p@x.com', Birthday: now.toFormat('M/d') },
      { Name: 'Q', Email: 'q@x.com', Birthday: md, 'Last Birthday Email': String(now.year) },
      { Name: 'R', Email: 'r@x.com', Birthday: md, 'Marketing OK': 'No' },
      { Name: 'S', Email: 's@x.com', Birthday: now.plus({ days: 1 }).toFormat('MM-dd') }] });
    check('birthdays matched', o.map((x) => x.name).join() === 'O,P', o.map((x) => x.name).join());

    console.log('16 weekly KPIs');
    const lw = now.startOf('week').minus({ weeks: 1 }).plus({ days: 2 }).toISODate();
    o = await run('16-', 'Calculate KPIs', { nodes: {
      'Get Leads': [{ Date: lw, Source: 'google' }, { Date: lw, Source: 'google' }, { Date: lw, Source: 'facebook' }, {}],
      'Get Sales': [{ Date: lw + ' 10:00', Amount: 100, 'Customer Name': 'A' }, { Date: lw, Amount: 50, 'Customer Name': 'B' }] } });
    check('KPI subject', o[0].subject.includes('$150.00 revenue, 3 new leads'), o[0].subject);

    console.log('17 RSS');
    o = await run('17-', 'Compose Posts', { nodes: { 'New Blog Post (RSS)': [
      { title: 'Hello world', link: 'https://b.co/1', isoDate: now.minus({ hours: 2 }).toISO(), contentSnippet: 'Snippet' },
      { title: 'Old', link: 'https://b.co/0', isoDate: now.minus({ days: 30 }).toISO() }] } });
    check('only fresh posts', o.length === 1 && o[0].xPost.includes('Hello world'));

    console.log('18 uptime');
    const urls = await run('18-', 'One Item per URL', { cfg: { urls: 'https://a.com, b.com\nhttps://c.com' } });
    check('urls split', urls.map((u) => u.url).join() === 'https://a.com,https://b.com,https://c.com');
    const nodes18 = { 'One Item per URL': urls };
    o = await run('18-', 'Detect Status Changes', { nodes: nodes18, input: [{ statusCode: 200, body: 'ok' }, { error: { message: 'ENOTFOUND' } }, { statusCode: 503, statusMessage: 'Service Unavailable' }] });
    check('down alerts', o.map((x) => x.event + ':' + x.url).join() === 'DOWN:https://b.com,DOWN:https://c.com', JSON.stringify(o));
    o = await run('18-', 'Detect Status Changes', { nodes: nodes18, input: [{ statusCode: 200 }, { error: 'x' }, { statusCode: 200 }] });
    check('no repeat + recovery', o.length === 1 && o[0].event === 'UP' && o[0].url === 'https://c.com', JSON.stringify(o));

    console.log('19 booking');
    const day = now.plus({ days: 2 }).toISODate();
    o = await run('19-', 'Build Event', { nodes: { 'Booking Request Form': [{ Name: 'Al Bo', Email: 'a@x.com', Phone: '1', Service: 'Consultation', Date: day, Time: '2:00 PM' }] } });
    check('event built', o[0].valid && o[0].event.start.dateTime.startsWith(day + 'T14:00') && o[0].freeBusy.items[0].id === 'primary', o[0].event.start.dateTime);
    o = await run('19-', 'Build Event', { nodes: { 'Booking Request Form': [{ Name: 'Al', Email: 'a@x.com', Phone: '1', Service: 'C', Date: now.minus({ days: 1 }).toISODate(), Time: '9:00 AM' }] } });
    check('past date invalid', !o[0].valid);

    console.log('20 abandoned cart');
    const cart = { email: 'c@x.com', firstName: 'C', cartUrl: 'u', createdAt: now.toISO() };
    o = await run('20-', 'Purchased Yet?', { nodes: { 'Cart Details': [cart] }, input: [{ Date: now.toFormat('yyyy-MM-dd HH:mm'), 'Customer Email': 'C@x.com' }] });
    check('detects purchase', o[0].purchased === true);
    o = await run('20-', 'Purchased Yet? (2)', { nodes: { 'Cart Details': [cart] }, input: [{ Date: d(-3), 'Customer Email': 'c@x.com' }, {}] });
    check('old purchase ignored', o[0].purchased === false);

    console.log('21 retainer invoices');
    o = await run('21-', 'Build Invoices', { input: [
      { 'Client ID': 'C1', 'Client Name': 'Acme', 'Contact Name': 'Jordan Fox', 'Client Email': 'a@x.com', 'Monthly Fee': 1200, Active: 'Yes', 'Payment Link': 'https://p' },
      { 'Client ID': 'C2', 'Client Email': 'b@x.com', 'Monthly Fee': 500, Active: 'No' },
      { 'Client ID': 'C3', 'Client Email': 'c@x.com', 'Monthly Fee': 500, Active: 'yes', 'Last Invoiced': now.toFormat('yyyy-MM') }] });
    check('invoice built', o.length === 1 && o[0].invoiceId === 'INV-' + now.toFormat('yyyyMM') + '-C1' && o[0].html.includes('$1,200.00') && o[0].html.includes('Hi Jordan'));

    console.log('22 support triage');
    o = await run('22-', 'Categorize Email', { nodes: { 'New Support Email': [
      { from: '"Pat Kim" <Pat@Example.com>', subject: 'Urgent: heating not working', textPlain: 'Please help asap' },
      { from: { value: [{ address: 'billing@shop.com' }], text: 'billing@shop.com' }, subject: 'Refund for invoice 42', textHtml: '<p>I was charged twice</p>' },
      { from: 'noreply@service.com', subject: 'Your receipt', textPlain: 'receipt' },
      { from: 'joe@x.com', subject: 'Re: booking', textPlain: 'thanks' }] } });
    check('categories', o.map((x) => x.category).join() === 'Urgent,Billing,Billing,Booking', o.map((x) => x.category).join());
    check('auto-reply rules', o.map((x) => x.sendAck).join() === 'true,true,false,false' && o[0].fromEmail === 'pat@example.com' && o[0].firstName === 'Pat');

    console.log('23 low stock');
    o = await run('23-', 'Find Low Stock', { input: [
      { SKU: 'A', Product: 'Mug', Quantity: 4, 'Reorder Level': 10, 'Reorder Qty': 24, Supplier: 'Clay', 'Supplier Email': 's@x.com' },
      { SKU: 'B', Product: 'Cup', Quantity: 0, 'Reorder Level': 5, Supplier: 'Clay', 'Supplier Email': 's@x.com' },
      { SKU: 'C', Quantity: 50, 'Reorder Level': 10 },
      { SKU: 'D', Quantity: 1, 'Reorder Level': 5, 'Last Alert Date': d(-1) }] });
    check('low stock found', o.map((x) => x.sku).join() === 'A,B' && o[1].outOfStock && o[1].reorderQty === 10);
    const dig = await run('23-', 'Build Owner Digest', { input: o });
    check('digest subject', dig[0].subject.startsWith('🔴 1 out of stock, 2 items'), dig[0].subject);
    const po = await run('23-', 'Group by Supplier', { input: o });
    check('grouped by supplier', po.length === 1 && po[0].html.includes('24</b> × Mug'));

    console.log('24 google reviews');
    const place = { rating: 4.6, userRatingCount: 120, googleMapsUri: 'https://maps', reviews: [
      { name: 'r1', rating: 5, text: { text: 'Great' }, authorAttribution: { displayName: 'Ann' }, relativePublishTimeDescription: 'a day ago' },
      { name: 'r2', rating: 2, text: { text: 'Meh' }, authorAttribution: { displayName: 'Bo' } }] };
    o = await run('24-', 'Find New Reviews', { input: [place], mode: 'manual' });
    check('test mode shows latest', o.length === 1 && o[0].test && o[0].author === 'Ann');
    o = await run('24-', 'Find New Reviews', { input: [place] });
    check('first live run is silent', o.length === 0);
    place.reviews.unshift({ name: 'r3', rating: 1, text: { text: 'Bad' }, authorAttribution: { displayName: 'Cy' } });
    o = await run('24-', 'Find New Reviews', { input: [place] });
    check('new negative review detected', o.length === 1 && o[0].author === 'Cy' && o[0].negative && o[0].stars === '★☆☆☆☆');
  } catch (e) {
    fail('harness crashed: ' + e.stack);
  }
  const codeNodes = files.flatMap((f) => JSON.parse(fs.readFileSync(f)).nodes.filter((n) => n.type.endsWith('.code')).map((n) => path.basename(f) + ' / ' + n.name));
  console.log(`\nCode nodes in pack: ${codeNodes.length}`);
  console.log(failures ? `${failures} FAILURE(S)` : 'ALL CHECKS PASSED');
  process.exit(failures ? 1 : 0);
})();
