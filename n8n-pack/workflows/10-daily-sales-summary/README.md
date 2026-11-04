# 10 · Daily Sales Summary

> Every evening, emails you a clean one-glance summary of the day's sales: revenue, orders, average order value and how it compares with yesterday and last week.

**File to import:** `10-daily-sales-summary.json`  
**Trigger:** Schedule Trigger  
**Difficulty:** ⭐ Easy · about 20 minutes

## What it does

- Runs at 7pm and reads your **Sales** sheet (the one workflow 09 fills from Stripe — or any sheet with Date + Amount).
- Calculates today's revenue, order count and average order, with ▲/▼ vs yesterday and the same day last week.
- Adds month-to-date revenue and a list of today's orders.
- Emails it to you, nicely formatted for phone or desktop.

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **Google Sheets OAuth2** — used by: *Get Sales*
- **SMTP (any email provider: Gmail, Outlook, Zoho, your host...)** — used by: *Email Summary*
- A Google Sheet with the tab(s): **Sales** (templates included as CSV files in this folder).

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `10-daily-sales-summary.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. Make sure you have a **Sales** tab with at least `Date` and `Amount` columns (see `sheet-Sales.csv`). Workflow 09 creates rows automatically.
3. Fill in **Config** (sheet ID, emails, timezone, currency). Set `skipIfNoSales` to `true` if you don't want an email on zero-sale days.
4. Pick your **Google Sheets** and **SMTP** credentials, then **Activate**.

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Google Sheet columns

Column names must match exactly (capital letters and spaces included). Extra columns are fine. Use dates like `2026-11-20`.

**Tab `Sales`** — template: `sheet-Sales.csv` (*File → Import → Upload* in Google Sheets, choose *Insert new sheet*, then rename the tab to `Sales`)

| Date | Order ID | Customer Name | Customer Email | Amount | Currency | Source |
|---|---|---|---|---|---|---|
| 2026-11-04 13:05 | cs_test_a1b2c3 | Jane Smith | jane@example.com | 89 | USD | Stripe |

## Test it

Add a row with today's date and an amount, then click **Test workflow**.

## Customize it

- Change the send time in the trigger node.
- Log sales from your POS (Square, Shopify, Clover) into the same sheet via their exports or webhooks, and this report just works.

## Nodes used

| Node | Type | Notes |
|---|---|---|
| Every Evening 7pm | Schedule Trigger | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Get Sales | Google Sheets |  |
| Build Summary | Code (JavaScript) |  |
| Email Summary | Send Email (SMTP) |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
