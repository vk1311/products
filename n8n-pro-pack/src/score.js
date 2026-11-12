// SIGNAL SCORE: 0-100. Higher = more likely to need a better website, booking or quoting tool.
// Every point is listed here so the score is never a black box.
// A. No usable website: no_website 60 | social_only 50 | site_down 45
// B. Website gaps (only when the page loaded): no_booking_or_quote 18 | no_form 15 | no_viewport 12 |
//    no_https 10 | stale_copyright 10 | no_crm_or_chat 8 | diy_builder 6 | no_tel_link 5 | no_analytics 4 |
//    has_field_software -8 (already uses Jobber or Housecall Pro)
// C. Demand: reviews >= 100: 12 | >= 40: 8 | >= 15: 4 | google rating >= 4.5: 3
// score_reliable = false when a bot wall blocked the check or the page is a JavaScript-only shell.
const site = $('One site at a time').item.json;
const settings = $('Settings').first().json;
const STALE_YEAR = Number(settings.stale_year || 2022);
const THIS_YEAR = new Date().getFullYear();
const httpsRes = $('Fetch homepage over HTTPS').item.json || {};
const httpsStatus = Number(httpsRes.statusCode || 0);
const httpsOk = httpsStatus >= 200 && httpsStatus < 400;
const res = httpsStatus ? httpsRes : ($json || {});
const status = Number(res.statusCode || 0);
const headers = res.headers || {};
const raw = typeof res.body === 'string' ? res.body : (typeof res.data === 'string' ? res.data : '');
const html = raw.toLowerCase();
const errObj = res.error || httpsRes.error || {};
const errMsg = String(errObj.message || errObj.code || res.message || '').slice(0, 200);
const website = String(site.website || '');
const hdr = (k) => String(headers[k] || headers[k.toLowerCase()] || '').toLowerCase();
const has = (...xs) => xs.some((x) => html.includes(x));
const textLen = html.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<style[\s\S]*?<\/style>/g, '').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim().length;
const signals = [], breakdown = [];
let score = 0;
const add = (name, pts) => { signals.push(name); if (pts) { score += pts; breakdown.push(name + ' ' + (pts > 0 ? '+' : '') + pts); } };
const generatorMatch = raw.match(/<meta[^>]+name=["']generator["'][^>]*content=["']([^"']+)["']/i) || raw.match(/<meta[^>]+content=["']([^"']+)["'][^>]*name=["']generator["']/i);
const generator = generatorMatch ? generatorMatch[1].slice(0, 80) : '';
const gen = generator.toLowerCase(), server = hdr('server'), link = hdr('link');
const PLATFORMS = [
  ['Wix', () => has('wixstatic.com', 'parastorage.com', 'wix-code') || gen.includes('wix') || server.includes('pepyaka') || !!hdr('x-wix-request-id')],
  ['Squarespace', () => has('static1.squarespace.com', 'squarespace-cdn.com', 'squarespace.com/') || gen.includes('squarespace')],
  ['Shopify', () => has('cdn.shopify.com', 'shopify.theme', 'myshopify.com') || !!hdr('x-shopid') || !!hdr('x-shopify-stage')],
  ['GoDaddy Website Builder', () => has('img1.wsimg.com', 'websites.godaddy.com', 'godaddysites.com') || gen.includes('go daddy') || gen.includes('godaddy') || gen.includes('starfield')],
  ['Weebly', () => has('weebly.com', 'editmysite.com', 'weeblycloud.com') || gen.includes('weebly')],
  ['Webflow', () => has('data-wf-page', 'data-wf-site', 'webflow.js', 'website-files.com') || gen.includes('webflow')],
  ['Duda', () => has('irp.cdn-website.com', 'cdn-website.com', 'multiscreensite.com', 'dudaone') || gen.includes('duda')],
  ['WordPress', () => has('wp-content/', 'wp-includes/', 'wp-json') || gen.includes('wordpress') || link.includes('api.w.org')],
];
let platform = 'custom/unknown';
for (const [name, test] of PLATFORMS) { if (test()) { platform = name; break; } }
const BOOKING = [['Calendly', ['calendly.com']], ['Acuity', ['acuityscheduling.com', '.as.me/', 'app.acuityscheduling']],
  ['Square Appointments', ['squareup.com/appointments', 'square.site/book', 'app.squareup.com/appointments']], ['Jobber', ['getjobber.com', 'clienthub.getjobber', 'jobber.com/']],
  ['Housecall Pro', ['housecallpro.com']], ['Setmore', ['setmore.com']], ['SimplyBook', ['simplybook.me', 'simplybook.it']], ['Booksy', ['booksy.com']],
  ['Fresha', ['fresha.com']], ['Jane App', ['janeapp.com', 'janeapp.ca']]];
const CRM_CHAT = [['HubSpot', ['js.hs-scripts.com', 'hsforms', 'hs-analytics', 'hubspot.com', 'hs-banner']], ['Mailchimp', ['list-manage.com', 'chimpstatic.com', 'mailchimp.com']],
  ['Tawk', ['embed.tawk.to', 'tawk.to']], ['Intercom', ['widget.intercom.io', 'intercomcdn.com', 'intercom.io']]];
const ANALYTICS = [['Facebook pixel', ['fbevents.js', "fbq('init'", 'fbq("init"']], ['Google Analytics', ['google-analytics.com/analytics.js', 'gtag/js?id=g-', 'gtag/js?id=ua-', "gtag('config'", 'gtag("config"']],
  ['Google Tag Manager', ['googletagmanager.com/gtm.js', 'googletagmanager.com/ns.html', 'gtm-']]];
const detect = (list) => list.filter(([, needles]) => needles.some((n) => html.includes(n))).map(([name]) => name);
const social = /(^|\/\/|\.)(facebook\.com|fb\.com|instagram\.com|linktr\.ee)/i.test(website);
const noWebsite = !website.trim();
const challenge = textLen < 2000 && /just a moment|cf-challenge|cf_chl|challenge-platform|captcha|access denied|attention required/.test(html);
const blocked = !noWebsite && !social && ([401, 403, 406, 429].includes(status) || (status === 503 && challenge) || challenge || /timeout|timed out|etimedout|esockettimedout|aborted/i.test(errMsg));
const dead = !noWebsite && !social && !blocked && (!status || status === 404 || status === 410 || status >= 500);
const shell = !noWebsite && !social && !blocked && !dead && textLen < 300;
const loaded = !noWebsite && !social && !blocked && !dead && !shell;
let hasViewport = null, hasForm = null, hasBookingOrQuote = null, hasTel = null, copyrightYear = null;
let bookingTools = [], crmChatTools = [], analyticsTools = [];
if (loaded) {
  bookingTools = detect(BOOKING); crmChatTools = detect(CRM_CHAT); analyticsTools = detect(ANALYTICS);
  hasViewport = /<meta[^>]+name=["']?viewport/.test(html);
  hasForm = html.includes('<form') || has('typeform.com', 'jotform', 'formspree', 'wpforms', 'gravityform', 'wpcf7', 'hsforms', 'cognitoforms', 'wufoo', 'wix-forms', 'docs.google.com/forms', 'forms.gle', 'formstack');
  hasBookingOrQuote = bookingTools.length > 0 || has('book now', 'book online', 'book an appointment', 'schedule service', 'schedule an appointment', 'request service', 'request a quote', 'get a quote', 'free quote', 'request a free', 'free estimate', 'get an estimate', 'request an estimate', 'online booking', 'reserve now');
  hasTel = html.includes('href="tel:') || html.includes("href='tel:") || html.includes('href=tel:');
  const years = []; const re = /(?:©|&copy;|&#169;|copyright)[^0-9<]{0,20}((?:19|20)\d{2})(?:\s*(?:-|–|—|&ndash;|&#8211;|to)\s*((?:19|20)\d{2}))?/gi; let m;
  while ((m = re.exec(raw)) !== null) { const y = Number(m[2] || m[1]); if (y >= 1995 && y <= THIS_YEAR + 1) years.push(y); }
  copyrightYear = years.length ? Math.max(...years) : null;
}
if (noWebsite) add('no_website', 60); else if (social) add('social_only', 50); else if (dead) add('site_down', 45);
else if (blocked) add('check_blocked', 0); else if (shell) add('js_only_page', 0);
if (!noWebsite && !social && !httpsOk && status >= 200 && status < 400) add('no_https', 10);
if (loaded) {
  if (!hasBookingOrQuote) add('no_booking_or_quote', 18);
  if (!hasForm) add('no_form', 15);
  if (!hasViewport) add('no_viewport', 12);
  if (copyrightYear !== null && copyrightYear <= STALE_YEAR) add('stale_copyright', 10);
  if (!crmChatTools.length) add('no_crm_or_chat', 8);
  if (['Wix', 'Squarespace', 'GoDaddy Website Builder', 'Weebly', 'Duda'].includes(platform)) add('diy_builder', 6);
  if (!hasTel) add('no_tel_link', 5);
  if (!analyticsTools.length) add('no_analytics', 4);
  if (bookingTools.includes('Jobber') || bookingTools.includes('Housecall Pro')) add('has_field_software', -8);
}
const reviews = Number(site.review_count || 0), rating = Number(site.google_rating || 0);
if (reviews >= 100) add('reviews_100plus', 12); else if (reviews >= 40) add('reviews_40plus', 8); else if (reviews >= 15) add('reviews_15plus', 4);
if (rating >= 4.5) add('rating_4_5plus', 3);
score = Math.max(0, Math.min(100, score));
return { json: { name: site.name, website, http_status: status || null, https_ok: httpsOk, fetch_error: errMsg,
  platform: loaded || blocked || shell ? platform : '', generator, booking_tools: bookingTools.join(', '), crm_chat_tools: crmChatTools.join(', '),
  analytics_tools: analyticsTools.join(', '), has_viewport: hasViewport, has_form: hasForm, has_booking_or_quote: hasBookingOrQuote, has_tel_link: hasTel,
  copyright_year: copyrightYear, signals: signals.join(', '), signal_score: score, score_reliable: !blocked && !shell, score_breakdown: breakdown.join(', '),
  checked_at: new Date().toISOString() } };
