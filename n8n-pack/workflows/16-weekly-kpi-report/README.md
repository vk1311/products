# 16 · Weekly Business KPI Report

> Every Monday morning, emails you a one-page report on last week: revenue, orders, average order, new leads, lead sources, best days and top customers — each compared with the week before.

**File to import:** `16-weekly-kpi-report.json`  
**Trigger:** Schedule Trigger  
**Difficulty:** ⭐ Easy · about 20 minutes

## What it does

- Runs Mondays at 8am and reads your **Leads** and **Sales** sheets (from workflows 02 and 09, or your own).
- Compares last week (Mon–Sun) with the previous week, with ▲/▼ percentages.
- Shows where leads came from, your best sales days and top customers.
- No dashboards to log into — it just lands in your inbox.

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **Google Sheets OAuth2** — used by: *Get Leads*, *Get Sales*
- **SMTP (any email provider: Gmail, Outlook, Zoho, your host...)** — used by: *Email Report*
- A Google Sheet with the tab(s): **Leads**, **Sales** (templates included as CSV files in this folder).

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `16-weekly-kpi-report.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. Make sure your sheet has a **Leads** tab (`Date`, `Source`) and a **Sales** tab (`Date`, `Amount`, `Customer Name`). See the CSV templates.
3. Fill in **Config** and pick your **Google Sheets** (2 nodes) and **SMTP** credentials.
4. Click **Activate**.

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Google Sheet columns

Column names must match exactly (capital letters and spaces included). Extra columns are fine. Use dates like `2026-11-20`.

**Tab `Leads`** — template: `sheet-Leads.csv` (*File → Import → Upload* in Google Sheets, choose *Insert new sheet*, then rename the tab to `Leads`)

| Date | Name | Email | Phone | Message | Source | Campaign | Status | Follow-ups Sent | Last Follow-up |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-02 10:15 | Jane Smith | jane@example.com | +15551234567 | Hi! | google |  |  |  |  |

**Tab `Sales`** — template: `sheet-Sales.csv` (*File → Import → Upload* in Google Sheets, choose *Insert new sheet*, then rename the tab to `Sales`)

| Date | Order ID | Customer Name | Customer Email | Amount | Currency | Source |
|---|---|---|---|---|---|---|
| 2026-11-03 13:05 | cs_test_a1b2c3 | Jane Smith | jane@example.com | 89 | USD | Stripe |

## Test it

Click **Test workflow** — you'll get the report for last week straight away.

## Customize it

- Add more metrics in the **Calculate KPIs** code (e.g. refunds, bookings) — each line in the table is one `row(...)` call.
- CC your business partner or accountant via *Email Report → Options → CC*.

## Nodes used

| Node | Type | Notes |
|---|---|---|
| Mondays 8am | Schedule Trigger | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Get Leads | Google Sheets |  |
| Get Sales | Google Sheets |  |
| Calculate KPIs | Code (JavaScript) |  |
| Email Report | Send Email (SMTP) |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
