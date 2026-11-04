# 21 · Monthly Retainer Invoices

> On the 1st of every month, emails each retainer client a professional invoice with a Pay button, logs it to your Invoices sheet, and hands it to the reminder workflow.

**File to import:** `21-monthly-retainer-invoices.json`  
**Trigger:** Schedule Trigger  
**Difficulty:** ⭐ Easy · about 20 minutes

## What it does

- Runs on the 1st of each month at 8am and reads your **Clients** sheet.
- For every active client, creates a clean HTML invoice (number, period, amount, due date, pay button, bank details).
- Emails it to the client (BCC to you) and adds it to your **Invoices** sheet as `Unpaid`.
- Workflow 03 (Invoice Reminders) then chases it automatically if it's not paid on time.
- Won't double-invoice: it records the month in *Last Invoiced*.

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **Google Sheets OAuth2** — used by: *Get Clients*, *Add to Invoices Sheet*, *Mark Client Invoiced*
- **SMTP (any email provider: Gmail, Outlook, Zoho, your host...)** — used by: *Email Invoice*
- A Google Sheet with the tab(s): **Clients**, **Invoices** (templates included as CSV files in this folder).

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `21-monthly-retainer-invoices.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. Create two tabs: **Clients** and **Invoices**, using `sheet-Clients.csv` and `sheet-Invoices.csv`.
3. Fill in **Config**: payment terms, bank/payment instructions, your business details (address, tax ID) and currency.
4. Optional: give each client a reusable payment link (Stripe Payment Link, PayPal.me, Square) in the *Payment Link* column.
5. Pick your **Google Sheets** (3 nodes) and **SMTP** credentials, then **Activate**.

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Google Sheet columns

Column names must match exactly (capital letters and spaces included). Extra columns are fine. Use dates like `2026-11-20`.

**Tab `Clients`** — template: `sheet-Clients.csv` (*File → Import → Upload* in Google Sheets, choose *Insert new sheet*, then rename the tab to `Clients`)

| Client ID | Client Name | Contact Name | Client Email | Monthly Fee | Currency | Description | Active | Payment Link | Last Invoiced |
|---|---|---|---|---|---|---|---|---|---|
| C001 | Acme Ltd | Jordan Fox | accounts@acme.example | 1200 | USD | Monthly marketing retainer | Yes | https://buy.stripe.com/test_123 |  |

**Tab `Invoices`** — template: `sheet-Invoices.csv` (*File → Import → Upload* in Google Sheets, choose *Insert new sheet*, then rename the tab to `Invoices`)

| Invoice ID | Client Name | Client Email | Amount | Currency | Due Date | Status | Payment Link | Last Reminder Stage | Last Reminder Date |
|---|---|---|---|---|---|---|---|---|---|
| INV-202611-C001 | Acme Ltd | accounts@acme.example | 1200 | USD | 2026-11-15 | Unpaid | https://buy.stripe.com/test_123 |  |  |

## Test it

Add yourself as an active client with a small fee, click **Test workflow**, then delete the test rows. (If you test twice in the same month, clear *Last Invoiced* first.)

## Customize it

- Set *Active* to `No` to pause a client without deleting them.
- Need tax lines (VAT/GST)? Add them to the invoice table in the **Build Invoices** code.

## Nodes used

| Node | Type | Notes |
|---|---|---|
| 1st of Month 8am | Schedule Trigger | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Get Clients | Google Sheets |  |
| Build Invoices | Code (JavaScript) |  |
| Email Invoice | Send Email (SMTP) |  |
| Add to Invoices Sheet | Google Sheets |  |
| Mark Client Invoiced | Google Sheets |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
