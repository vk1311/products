// Keep open CanadaBuys notices delivered to (or bought from) the provinces you list in Settings,
// plus national "*Canada" ones (tagged CANADA so a subscriber can opt in). One clean item per tender.
const REGIONS = {
  NS: ['nova scotia', 'halifax', 'dartmouth', 'greenwood', 'shearwater', 'sydney', 'truro', 'kentville', 'yarmouth', 'bridgewater', 'antigonish', 'new glasgow'],
  NB: ['new brunswick', 'oromocto', 'gagetown', 'fredericton', 'moncton', 'saint john', 'shediac', 'bathurst', 'miramichi', 'edmundston', 'dieppe'],
  PE: ['prince edward island', 'charlottetown', 'summerside'],
  NL: ['newfoundland', "st. john's", 'st johns', 'gander', 'goose bay', 'corner brook', 'labrador'],
  QC: ['quebec', 'québec', 'montreal', 'montréal', 'gatineau', 'laval'],
  ON: ['ontario', 'ottawa', 'toronto', 'kingston', 'hamilton', 'london', 'sudbury', 'thunder bay'],
  MB: ['manitoba', 'winnipeg', 'brandon'],
  SK: ['saskatchewan', 'regina', 'saskatoon'],
  AB: ['alberta', 'calgary', 'edmonton', 'red deer'],
  BC: ['british columbia', 'vancouver', 'victoria', 'esquimalt', 'kelowna', 'nanaimo'],
  YT: ['yukon', 'whitehorse'], NT: ['northwest territories', 'yellowknife'], NU: ['nunavut', 'iqaluit'],
  CANADA: ['canada'],
};
const WANT = String($('Settings').first().json.provinces || 'NS,NB,PE,NL').split(',').map((x) => x.trim().toUpperCase()).concat(['CANADA']);
const CATEGORY = { GD: 'Goods', SRV: 'Services', CNST: 'Construction', SRVTGD: 'Services related to goods' };
const now = Date.now(), seen = new Set(), out = [];
const clean = (s) => String(s || '').replace(/<br\s*\/?>/gi, ' ').replace(/<[^>]+>/g, ' ').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim();
for (const it of $input.all()) {
  const r = {};
  for (const k of Object.keys(it.json || {})) r[k.replace(/^﻿/, '').replace(/^"|"$/g, '').trim()] = it.json[k];
  const g = (k) => String(r[k] == null ? '' : r[k]).trim();
  const id = g('referenceNumber-numeroReference');
  if (!id || seen.has(id)) continue;
  if (g('tenderStatus-appelOffresStatut-eng') && g('tenderStatus-appelOffresStatut-eng') !== 'Open') continue;
  const closing = g('tenderClosingDate-appelOffresDateCloture');
  if (closing && Date.parse(closing) && Date.parse(closing) < now) continue;
  let places = g('regionsOfDelivery-regionsLivraison-eng').split(/[\r\n]+/).map((x) => x.replace(/^\*/, '').trim()).filter(Boolean);
  if (!places.length) places = [g('contractingEntityAddressProvince-entiteContractanteAdresseProvince-eng'), g('contractingEntityAddressCity-entiteContractanteAdresseVille-eng')].filter(Boolean);
  const codes = [];
  for (const p of places) {
    const pl = p.toLowerCase();
    for (const code of Object.keys(REGIONS)) {
      if (codes.includes(code) || !WANT.includes(code)) continue;
      if (REGIONS[code].some((n) => pl === n || pl.startsWith(n))) codes.push(code);
    }
  }
  if (!codes.length) continue;
  seen.add(id);
  const title = clean(g('title-titre-eng'));
  const description = clean(g('tenderDescription-descriptionAppelOffres-eng')).slice(0, 700);
  const gsin = clean(g('gsinDescription-nibsDescription-eng').replace(/\*/g, ' '));
  const unspsc = clean(g('unspscDescription-eng').replace(/\*/g, ' '));
  const cat = g('procurementCategory-categorieApprovisionnement').split(/[\r\n]+/).map((x) => CATEGORY[x.replace(/^\*/, '').trim()] || x.replace(/^\*/, '').trim()).filter(Boolean).join(', ');
  const solicitation = g('solicitationNumber-numeroSollicitation');
  const url = g('noticeURL-URLavis-eng') || 'https://canadabuys.canada.ca/en/tender-opportunities?search_filter=' + encodeURIComponent(solicitation || id);
  out.push({ json: { tender_id: id, title, description, category: cat, buyer: g('contractingEntityName-nomEntitContractante-eng'),
    published: g('publicationDate-datePublication'), closing_date: closing, regions: codes, region_names: places.join(', '), url,
    search_text: (title + ' ' + description + ' ' + gsin + ' ' + unspsc + ' ' + cat).toLowerCase() } });
}
return out;
