# Printable Business Forms (Canada)

150 fillable, letter-size (8.5 x 11 in) PDF business forms with a clean, minimal design, plus Etsy listing copy.

- `forms/` - the 150 PDFs, numbered `001`-`150`
- `listings.csv` - one row per PDF: `file`, `title` (max 140 characters), `description`, `tags` (13 comma-separated tags, each max 20 characters), `price`
- `tools/` - the Python generator that builds both

## What's in the set

| Nos. | Group |
|------|-------|
| 001-025 | Invoices (general plus one for each of the 13 provinces and territories), quotes, estimates, receipts |
| 026-050 | Purchasing, sales and bookkeeping: purchase orders, order forms, GST/HST tracker, mileage log, cash count, AR/AP, budget |
| 051-075 | Operations and inventory: work orders, job reports, inspections, packing slips, inventory, sign-in and key logs |
| 076-100 | HR and payroll: job application, onboarding, direct deposit, timesheets, schedules, reviews, payroll register |
| 101-125 | Safety and food service: incident and injury reports, hazard assessment (FLHA), fire logs, temperature logs, opening and closing checklists |
| 126-150 | Cleaning and rentals: cleaning checklists, house rules, guest sheets, rental application, move-in/move-out inspection, snow removal log |

## How they're made for Canada

- Province/territory drop-downs, postal codes, amounts in Canadian dollars, metric units (km, kg, °C)
- GST/HST/PST/QST tax lines. Province invoices are pre-labelled with rates current as of 2026 (for example, Ontario HST 13% and Nova Scotia HST 14%)
- HR forms avoid questions that human rights codes discourage on applications (age, marital status, SIN). They cover TD1 forms, CPP/EI and the Record of Employment (ROE)
- No brand names or trademarks in the forms or the listings

## Rebuild

Requires Python 3 with `reportlab` (and `pypdf` if you want to check the output).

```bash
cd etsy/tools && python3 build.py
```

Each `forms_N.py` file holds 25 forms. To change a tax rate, edit `TAX` in `tools/common.py` and rebuild. Listing copy comes from each form's `name`, `about` and `tags`, and from `tools/listings.py`.

## Before you list

- Etsy listings need preview images. They are not included here. You can make them by rendering page 1 of each PDF (for example, `pdftoppm -r 150 -png`).
- Prices are in your shop currency.
- Totals are typed in, not auto-calculated.
