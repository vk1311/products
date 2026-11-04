# 13 · Quote Request Intake & Routing

> A professional quote request form that scores how hot each lead is, sends it to the right person on your team, logs it to a sheet and confirms with the customer.

**File to import:** `13-quote-request-router.json`  
**Trigger:** n8n Form Trigger  
**Difficulty:** ⭐ Easy · about 20 minutes

## What it does

- Hosted quote form: contact details, service, budget, timeline, project details, address.
- Gives each request a reference number (e.g. `Q-261104-7KD2`).
- Scores priority: **HOT** (ASAP + big budget), **Warm** (one of the two) or **Normal**.
- Routes it to the right team member based on the service chosen (you're BCC'd so nothing slips).
- Logs everything to a **Quotes** sheet — your simple pipeline.
- Sends the customer a confirmation with their reference number.

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **Google Sheets OAuth2** — used by: *Save Quote Request*
- **SMTP (any email provider: Gmail, Outlook, Zoho, your host...)** — used by: *Email Assigned Team Member*, *Confirm to Customer*
- A Google Sheet with the tab(s): **Quotes** (templates included as CSV files in this folder).

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `13-quote-request-router.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. Create a sheet tab named **Quotes** with the headers in `sheet-Quotes.csv`.
3. In **Config**, set your emails, sheet ID and `routingRules` — a simple list of *service → email*, e.g. `{"Repair":"mike@you.com"}`. Anything not listed goes to `ownerEmail`.
4. Edit the form's *Service* and *Budget* options to match what you sell. (If you change budget options, update the `BUDGETS` list in **Route & Prioritize** too.)
5. Pick your **Google Sheets** and **SMTP** credentials.
6. Activate and link the form's **Production URL** from your website's "Get a quote" button.

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Google Sheet columns

Column names must match exactly (capital letters and spaces included). Extra columns are fine. Use dates like `2026-11-20`.

**Tab `Quotes`** — template: `sheet-Quotes.csv` (*File → Import → Upload* in Google Sheets, choose *Insert new sheet*, then rename the tab to `Quotes`)

| Quote ID | Date | Name | Email | Phone | Service | Budget | Timeline | Details | Address | Priority | Assigned To | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q-261104-7KD2 | 2026-11-04 09:12 | Maria Garcia | maria@example.com | +15551112222 | Installation | $2,000 - $10,000 | ASAP | New kitchen lighting, 12 fittings | 90210 | HOT | sales@yourbusiness.com | New |

## Test it

Click **Test workflow**, open the Test URL and submit a request with your own email.

## Customize it

- Add a Slack or Telegram node after *Save Quote Request* to ping the team about HOT leads instantly.
- Use the **Status** column (`New` → `Quoted` → `Won`/`Lost`) as a lightweight sales pipeline.

## Nodes used

| Node | Type | Notes |
|---|---|---|
| Quote Request Form | n8n Form Trigger | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Route & Prioritize | Code (JavaScript) |  |
| Save Quote Request | Google Sheets |  |
| Email Assigned Team Member | Send Email (SMTP) |  |
| Confirm to Customer | Send Email (SMTP) |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
