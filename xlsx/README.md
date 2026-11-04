# Excel Templates for Small Business (30)

Ready-to-use `.xlsx` templates with working formulas, built with `openpyxl`.
Set up for Canada by default (13% Ontario HST, CRA terms) – every rate is an editable setting.

**TL;DR:** open a file, read the **Instructions** tab, type over the yellow sample rows. Grey cells are formulas and are locked so they can't be broken by accident.

## Templates

| # | Template | What it does |
|---|----------|--------------|
| 01 | [Monthly Budget](templates/01-monthly-budget.xlsx) | Monthly budget vs actual by category, with automatic variance and a by-month summary. |
| 02 | [Cash Flow Forecast](templates/02-cash-flow-forecast.xlsx) | 12-month cash flow forecast with running bank balance, low-cash warnings and chart. |
| 03 | [Invoice Tracker](templates/03-invoice-tracker.xlsx) | Accounts receivable: invoices, HST, payments, overdue status, aging buckets and balances by client. |
| 04 | [Quote Tracker](templates/04-quote-tracker.xlsx) | Quotes/estimates with follow-up reminders, win rate and results by salesperson. |
| 05 | [Job Costing](templates/05-job-costing.xlsx) | Estimated vs actual labour, materials and other costs per job, with profit and margin. |
| 06 | [Payroll Hours](templates/06-payroll-hours.xlsx) | Clock-in/out log that rolls into a weekly timesheet with overtime and gross pay. |
| 07 | [HST Tracker](templates/07-hst-tracker.xlsx) | HST collected vs input tax credits, with quarterly GST/HST return lines (101/103/106/109). |
| 08 | [Inventory](templates/08-inventory.xlsx) | Stock list with in/out movements, on-hand quantity, stock value and reorder alerts. |
| 09 | [CRM Lite](templates/09-crm-lite.xlsx) | Contacts and deal pipeline with stage probabilities, activity log, follow-up flags and pipeline summary. |
| 10 | [Vacation Tracker](templates/10-vacation-tracker.xlsx) | Vacation entitlement, leave log (skips weekends/stat holidays) and remaining balances. |
| 11 | [Expense Tracker](templates/11-expense-tracker.xlsx) | Business expenses with HST split, receipt flags and a category-by-month summary. |
| 12 | [Mileage Log](templates/12-mileage-log.xlsx) | CRA-style vehicle logbook with business-use % and tiered per-km allowance. |
| 13 | [Profit & Loss](templates/13-profit-and-loss.xlsx) | 12-month income statement with gross margin, operating income, tax estimate and net margin. |
| 14 | [Break Even Analysis](templates/14-break-even-analysis.xlsx) | Break-even units and revenue, target-profit volume, margin of safety, sensitivity table and chart. |
| 15 | [Sales Tracker](templates/15-sales-tracker.xlsx) | Sales log with product price/cost lookup and a dashboard by month, product and rep. |
| 16 | [Bill Tracker](templates/16-bill-tracker.xlsx) | Accounts payable: supplier bills, due-in-7-days and overdue flags, aging and balances by vendor. |
| 17 | [Loan Amortization](templates/17-loan-amortization.xlsx) | Loan/mortgage schedule with extra payments, Canadian semi-annual compounding and payoff date. |
| 18 | [Project Tracker](templates/18-project-tracker.xlsx) | Task list with owners, overdue flags, weighted % complete and a 16-week Gantt view. |
| 19 | [Shift Scheduler](templates/19-shift-scheduler.xlsx) | Weekly staff schedule with start/end times, break rule, hours, wages and over-max flags. |
| 20 | [Petty Cash Log](templates/20-petty-cash-log.xlsx) | Petty cash box log with running balance, top-up amount and cash-count reconciliation. |
| 21 | [Fixed Asset Register](templates/21-fixed-asset-register.xlsx) | Asset register with straight-line or declining-balance depreciation and net book value by year. |
| 22 | [Pricing Calculator](templates/22-pricing-calculator.xlsx) | Cost build-up to suggested price from target margin, with markup, margin and HST-inclusive price. |
| 23 | [Subscription Tracker](templates/23-subscription-tracker.xlsx) | Recurring charges normalized to monthly/annual cost, with renewal alerts and category totals. |
| 24 | [KPI Dashboard](templates/24-kpi-dashboard.xlsx) | Monthly KPI targets vs actuals with YTD attainment (sum/average/latest) and traffic-light status. |
| 25 | [Equipment Maintenance](templates/25-equipment-maintenance.xlsx) | Preventive maintenance schedule with service log, next-due dates, overdue flags, cost and downtime. |
| 26 | [Purchase Order Tracker](templates/26-purchase-order-tracker.xlsx) | Purchase orders with HST, partial receipts, late flags, outstanding value and vendor summary. |
| 27 | [Time Billing](templates/27-time-billing.xlsx) | Billable-hours log with client rates, unbilled WIP, retainer balances and staff utilization. |
| 28 | [Commission Calculator](templates/28-commission-calculator.xlsx) | Tiered (marginal) sales commission with quota attainment, bonus and total pay per rep. |
| 29 | [Attendance Tracker](templates/29-attendance-tracker.xlsx) | Monthly attendance grid with codes, weekend shading, per-employee totals and attendance %. |
| 30 | [Cash Drawer Reconciliation](templates/30-cash-drawer-reconciliation.xlsx) | End-of-day till count by denomination, over/short vs POS, deposit amount and daily log. |

## Where people get them (decided Nov 4, 2026)

Both, free:

1. **waypointns.ca/free-tools** – all 30, direct download, no sign-up. Brings visitors to the Waypoint site.
2. **Gumroad** – each template as a free ($0+) product. Collects buyer emails.

Each Gumroad listing links back to waypointns.ca/free-tools, and the free-tools page links to Gumroad for anyone who wants update emails.

## How every template works

- **Instructions tab first** – what the file does, step-by-step use, what each tab is for, notes and assumptions.
- **Yellow cells, blue text = type here** (unlocked). **Grey cells = formulas** (locked).
- **Sheets are protected with no password.** To change formulas or layout: *Review → Unprotect Sheet*. Sorting, filtering and resizing columns work while protected.
- **Sample data included** (fictional) so you can see it working. Select the yellow sample rows and press Delete – the formulas stay.
- **Formulas are pre-filled** down 100–1,000 rows (varies by template), so new rows just work. Empty rows stay blank.
- **Drop-downs** read from an editable **Lists** tab; rates and dates live on a **Settings** tab.
- Trackers that care about "today" use an **As-of date** (defaults to `=TODAY()`; type a date to freeze a report).
- Excel 2010+ functions only (no XLOOKUP/FILTER), so they also open in LibreOffice and Google Sheets.

> Not tax, legal or accounting advice. Check rates (HST, CRA per-km, ESA rules) for your province and year.

## Rebuild / verify

The `.xlsx` files are generated – edit the Python, not the spreadsheets.

```bash
cd xlsx
python3 build.py          # regenerate all 30 into templates/
python3 build.py 03 17    # regenerate just #03 and #17
python3 verify.py         # recalculates everything in LibreOffice and checks it
```

`verify.py` (needs `openpyxl` + LibreOffice `soffice`):

1. builds each template into a temp folder and recalculates every formula with LibreOffice;
2. fails on any formula error (`#VALUE!`, `#REF!`, `#NAME?`, `#DIV/0!`, `#N/A`...);
3. compares key results (totals, balances, commissions, loan payment, depreciation...) against values computed independently in Python from the sample data;
4. checks structure: Instructions tab is first, every sheet is protected, every formula cell is locked and every input cell is unlocked.

Code layout:

- `generator/common.py` – shared styling, table builder, Instructions tab, protection
- `generator/templates_a.py` – templates 01–10
- `generator/templates_b.py` – templates 11–20
- `generator/templates_c.py` – templates 21–30
