# Small Business Basics · Canada — ebook series

Ten plain-language PDF guides for Canadian small-business owners, written to sell on Gumroad.
Each book lives in its own folder with its Markdown source (`book.md`) and its Gumroad listing
copy (`listing.md`). Built PDFs are in `pdf/`.

| # | Folder | Book |
|---|--------|------|
| 01 | `01-invoicing` | Invoicing |
| 02 | `02-quoting` | Quotes and estimates |
| 03 | `03-hiring-first-employee` | Hiring your first employee |
| 04 | `04-wcb-nova-scotia` | WCB basics for Nova Scotia employers |
| 05 | `05-hst-basics` | GST/HST basics |
| 06 | `06-google-business-profile` | Google Business Profile |
| 07 | `07-booking-systems` | Online booking systems |
| 08 | `08-handling-reviews` | Handling online reviews |
| 09 | `09-going-paperless` | Going paperless |
| 10 | `10-pricing-services` | Pricing your services |

## Folder layout

```
ebooks/
  NN-topic/book.md       the book (pandoc Markdown + YAML front matter)
  NN-topic/listing.md    Gumroad title, subtitle, description, price, tags
  pdf/NN-topic.pdf       built PDF (upload this to Gumroad)
  build.sh               Markdown -> PDF
  _tools/                template, stylesheet, PDF printer, quality checker
  _guide/STYLE.md        writing rules for the series
  _guide/FACTS.md        the verified facts the books rely on (with sources to re-check)
```

## Build the PDFs

You need [pandoc](https://pandoc.org/installing.html), Node.js 18+, and Playwright's Chromium:

```bash
cd ebooks
npm install playwright
npx playwright install chromium
```

Then:

```bash
./build.sh                  # all ten books
./build.sh 05-hst-basics    # one book
```

PDFs are written to `pdf/`. If you already have Chrome installed you can point the build at it
instead of downloading Chromium: `CHROME_PATH=/path/to/chrome ./build.sh`.

## Check a book before publishing

```bash
python3 _tools/check.py                 # all books
python3 _tools/check.py 05-hst-basics   # one book
```

The checker flags US spellings, outcome-promise wording ("guaranteed", "proven"...), anything
that looks like a statistic (for a human to review), a missing not-advice notice, the listing
format (150-word description, 5 tags), and PDF page count (15–25).

## Before you upload — keep the books current

- **Re-check the facts in `_guide/FACTS.md` before each sale season.** Tax rates, WCB Nova
  Scotia deadlines, CRA thresholds and Google's features change. The books tell readers to
  confirm with the official source, but you should still keep them accurate.
- **Add your name or business name** by adding `author: "Your Name"` to the front matter at the
  top of each `book.md`, then rebuild. It appears on the cover and the copyright line.
- Update `edition:` in the front matter when you revise a book.
- These guides are general information, not legal or tax advice. If you want extra comfort,
  have an accountant read the HST book and a lawyer or WCB-savvy adviser read the hiring and
  WCB books before you sell them.

## Publishing on Gumroad

For each book: create a product, paste the title, subtitle, description, price and tags from
`listing.md`, upload `pdf/NN-topic.pdf`, and add a cover image (a screenshot of page 1 of the
PDF works). Bundling all ten at a discount is an option Gumroad supports.
