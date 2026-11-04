# 03 · Invoice Payment Reminders

> Every morning, checks your invoice sheet and emails clients a reminder at the right moment — a friendly nudge before the due date, then gradually firmer notices if it's late.

**File to import:** `03-invoice-reminders.json`  
**Trigger:** Schedule Trigger  
**Difficulty:** ⭐ Easy · about 20 minutes

## What it does

- Runs every day at 9am and reads your **Invoices** sheet.
- Skips anything marked `Paid`, `Void` or `Cancelled`.
- Sends one email per stage: 3 days before due → on the due date → 7, 14 and 30 days overdue. Each stage is sent only once.
- Includes a **Pay now** button if you add a payment link (Stripe, PayPal, Square, QuickBooks...).
- Writes the stage and date back to the sheet so you can see who was chased and when.

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **Google Sheets OAuth2** — used by: *Get Invoices*, *Log Reminder in Sheet*
- **SMTP (any email provider: Gmail, Outlook, Zoho, your host...)** — used by: *Send Reminder*
- A Google Sheet with the tab(s): **Invoices** (templates included as CSV files in this folder).

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `03-invoice-reminders.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. Create a Google Sheet with a tab named **Invoices** using the headers in `sheet-Invoices.csv`.
3. Paste the sheet ID into **Config → sheetId** and set your business name, emails, timezone and currency.
4. Pick your **Google Sheets** credential on *Get Invoices* and *Log Reminder in Sheet*, and your **SMTP** credential on *Send Reminder*.
5. Add your invoices (one row each). Use dates like `2026-11-20`. When a client pays, set **Status** to `Paid` — reminders stop instantly.
6. Click **Activate**.

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Google Sheet columns

Column names must match exactly (capital letters and spaces included). Extra columns are fine. Use dates like `2026-11-20`.

**Tab `Invoices`** — template: `sheet-Invoices.csv` (*File → Import → Upload* in Google Sheets, choose *Insert new sheet*, then rename the tab to `Invoices`)

| Invoice ID | Client Name | Client Email | Amount | Currency | Due Date | Status | Payment Link | Last Reminder Stage | Last Reminder Date |
|---|---|---|---|---|---|---|---|---|---|
| INV-1001 | Acme Ltd | accounts@acme.example | 450 | USD | 2026-11-20 | Unpaid | https://buy.stripe.com/test_123 |  |  |

## Test it

Add a test row with your own email, a due date of today, and Status blank. Click **Test workflow** — you should get the "due today" email and see *Last Reminder Stage* = `due` in the sheet.

## Customize it

- Change timing or wording in the `STAGES` list at the top of the **Pick Invoices to Remind** code — it's plain English.
- Remove a stage (e.g. the 30-day final notice) by deleting its line.
- Want to be copied? Add your address under *Send Reminder → Options → BCC*.
- Pairs with workflow 21 (Monthly Retainer Invoices), which adds new invoices to this same sheet automatically.

## Nodes used

| Node | Type | Notes |
|---|---|---|
| Every Morning 9am | Schedule Trigger | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Get Invoices | Google Sheets |  |
| Pick Invoices to Remind | Code (JavaScript) |  |
| Send Reminder | Send Email (SMTP) |  |
| Log Reminder in Sheet | Google Sheets |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
