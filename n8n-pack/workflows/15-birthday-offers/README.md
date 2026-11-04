# 15 · Customer Birthday Offers

> Sends every customer a warm birthday email with a discount code on their birthday — a simple, personal touch customers remember.

**File to import:** `15-birthday-offers.json`  
**Trigger:** Schedule Trigger  
**Difficulty:** ⭐ Easy · about 20 minutes

## What it does

- Runs every morning and reads your **Customers** sheet.
- Finds customers whose birthday is today (year optional; leap-day birthdays handled).
- Sends a cheerful birthday email with your offer code.
- Records the year so nobody gets two in one year, and respects a `Marketing OK = No` opt-out.

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **Google Sheets OAuth2** — used by: *Get Customers*, *Mark as Sent This Year*
- **SMTP (any email provider: Gmail, Outlook, Zoho, your host...)** — used by: *Send Birthday Email*
- A Google Sheet with the tab(s): **Customers** (templates included as CSV files in this folder).

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `15-birthday-offers.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. Create a sheet tab named **Customers** with the headers in `sheet-Customers.csv`. Collect birthdays at sign-up or checkout ("Get a treat on your birthday!").
3. Create the discount code in your shop/POS (Shopify, Square, WooCommerce...) and enter it in **Config → offerCode**.
4. Fill in the rest of **Config**, pick your **Google Sheets** and **SMTP** credentials, then **Activate**.

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Google Sheet columns

Column names must match exactly (capital letters and spaces included). Extra columns are fine. Use dates like `2026-11-20`.

**Tab `Customers`** — template: `sheet-Customers.csv` (*File → Import → Upload* in Google Sheets, choose *Insert new sheet*, then rename the tab to `Customers`)

| Name | Email | Phone | Birthday | Marketing OK | Last Birthday Email |
|---|---|---|---|---|---|
| Olivia Brown | olivia@example.com | +15553334444 | 1990-11-04 | Yes |  |

## Test it

Add yourself with today's date as birthday (e.g. `11-04`) and click **Test workflow**.

## Customize it

- Swap birthdays for *customer anniversaries* (first purchase date) by changing the column name in the code.
- Add an optional Twilio SMS node after the email for a double touch.

## Nodes used

| Node | Type | Notes |
|---|---|---|
| Every Day 8am | Schedule Trigger | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Get Customers | Google Sheets |  |
| Find Birthdays Today | Code (JavaScript) |  |
| Send Birthday Email | Send Email (SMTP) |  |
| Mark as Sent This Year | Google Sheets |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
