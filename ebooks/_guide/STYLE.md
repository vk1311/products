# Writing guide for the ebook series

Every book in `/ebooks` follows this guide. Read it before writing or editing a book.

## Who we are writing for

Canadian small-business owners: sole proprietors and small teams (trades, cleaners, salons,
consultants, bookkeepers, photographers, landscapers, tutors, food trucks, small retail).
Busy, practical, not accountants or lawyers. Many are in Nova Scotia or Atlantic Canada, but
every book except the WCB book should work for owners anywhere in Canada (point out where rules
vary by province and say where to check).

## Voice

- Plain language. Short sentences. Explain any term the first time you use it.
- Warm, direct, second person ("you"). No hype, no hustle-culture talk, no exclamation marks.
- Practical: every chapter should leave the reader with something to do, decide, or copy.
- Use realistic, clearly made-up examples ("Say you run a two-person cleaning business in
  Truro..."). Invented *examples* are fine and useful. Invented *facts* are not.

## Hard rules

1. **Canadian spelling.** colour, favour, labour, behaviour, neighbour, centre, cheque,
   licence (noun) / license (verb), practice (noun) / practise (verb), catalogue, cancelled,
   travelled, labelled, enrol/enrolment, fulfil/fulfilment, judgement, defence, analyse, grey,
   jewellery, cheque, pay cheque, postal code. Use "-ize" (organize, recognize) — that is
   standard Canadian. Dates like "November 4, 2026". Money as "$1,250.00" (CAD implied).
2. **No invented statistics.** Do not write "studies show", "most customers", "X% of
   businesses", "on average", survey results, conversion rates, or any number about how people
   behave. If you feel you need a number, use a made-up worked example that is obviously an
   example ("If your hourly cost is $40..."). Real rules (tax rates, thresholds, deadlines) are
   facts, not stats — use only the ones in `FACTS.md`, and always pair them with "confirm the
   current figure at [official source]".
3. **No outcome promises.** Never say the reader will get more customers, more revenue, higher
   rankings, five-star reviews, or save X hours. Use "can help", "makes it easier to", "gives
   you a better chance of", "many owners find it useful to". No "guarantee", "proven", "secret",
   "skyrocket", "in 30 days".
4. **Not legal/tax advice.** Every book opens with a short "Before you start" section that
   says what the book is, who it is for, and that it is general information, not legal, tax,
   or accounting advice (adjust to the topic). Repeat a one-line reminder wherever the reader
   is close to a legal or tax decision. Point to the official source (CRA, WCB Nova Scotia,
   provincial employment standards, etc.) and to the kind of professional who can help.
5. **Software and platforms change.** Describe features generically ("most booking tools let
   you...") and avoid exact menu paths, prices, or plan names. When you mention products, name a
   few as examples only, never rank them, never say one is best. Say "at the time of writing"
   and "check the current version".
6. **No made-up references.** Only cite organizations and websites you are sure exist
   (canada.ca/revenue-agency, wcb.ns.ca, novascotia.ca, Competition Bureau Canada, Service
   Canada, Google Business Profile Help). Give homepage-level addresses, not deep links that
   might be wrong.

## Length and structure

- **Target 6,000–7,000 words of body text.** The PDF must land at 15–25 pages (Letter size);
  in practice about 6,000–6,800 words fills 23–24 pages with this layout.
  Cover, notice page and contents use 3 pages. Each `#` chapter starts on a new page.
- Front matter (YAML) at the top of `book.md`:

  ```yaml
  ---
  title: "Invoicing Made Simple"
  subtitle: "Get paid on time without awkward conversations"
  pagetitle: "Invoicing Made Simple"
  edition: "First edition · November 2026"
  year: 2026
  notice: "One sentence on the book-specific caution, e.g. 'Nothing in this guide is tax advice. GST/HST rules are set by the Canada Revenue Agency and can change.'"
  ---
  ```

  Do not use double quotes inside `pagetitle`.

- Suggested shape (adapt to the topic):
  1. `# Before you start` — what this guide covers, who it is for, the not-advice note,
     how to use the worksheets. (Short.)
  2. 6–9 chapters as `#` headings, each with `##` sections. Use `###` sparingly.
  3. A `# Templates and worksheets` chapter (or similar) with copy-ready material.
  4. `# Checklist` — a one-page action checklist.
  5. `# Where to learn more` — official sources only, plus "talk to a professional" prompts.
- End each main chapter with a `::: keypoints` box (3–5 bullets).

## Formatting toolbox (pandoc Markdown)

Callout boxes are fenced divs. The label is added automatically — do not type it.

```markdown
::: tip
Send the invoice the same day you finish the job.
:::

::: warning
Charging HST before you are registered is not allowed.
:::

::: note
Rules differ by province. Check yours.
:::

::: example
Say you run a two-person landscaping business in Bridgewater...
:::

::: keypoints
- Point one
- Point two
:::

::: checklist
- [ ] Business name and address on every invoice
- [ ] Invoice number
:::

::: template
**Subject:** Invoice #1042 from Harbourview Cleaning

Hi [Client name], ...
:::

::: worksheet
**My hourly labour cost:** $__________

**Hours available per week:** __________
:::
```

- Tables: pipe tables, keep to 2–4 columns so they fit the page.
- Checklists: `- [ ] item`.
- Fill-in lines: use `__________` (10 underscores) inline. Put each fill-in item in its own
  paragraph (blank line between) so it gets its own line.
- Placeholders in templates: `[Client name]`, `[Date]`.
- Force a page break if a template would split badly: a line with `::: pagebreak` then `:::`.
- No HTML, no images, no emoji.

## Before you hand a book in

```bash
./build.sh 05-hst-basics
python3 _tools/check.py 05-hst-basics
```

Fix every ERROR. Read every "review" line and make sure each flagged number is a real rule from
`FACTS.md` or an obviously made-up worked example — never a claim about how people behave.

## listing.md (Gumroad listing copy)

Each book folder has a `listing.md` in exactly this shape. The description must be 140–160
words (aim for 150) and follow the same no-stats / no-promise rules. Tags are lowercase,
one per bullet.

```markdown
# Gumroad listing — [Book title]

## Title
Invoicing Made Simple

## Subtitle
Get paid on time without awkward conversations — a plain-language guide for Canadian small businesses

## Description
[~150 words. Who it is for, what problem it helps with, what is inside (chapters, templates,
checklists), what format (PDF, ~N pages, Letter size, printable worksheets). End with one line
noting it is general information, not legal or tax advice.]

## Suggested price
$X CAD (one sentence on why: length, templates included, comparable to similar guides —
no claims about sales).

## Tags
- tag one
- tag two
- tag three
- tag four
- tag five
```

Price range for this series: $9–$19 CAD depending on depth and how many templates are included.
