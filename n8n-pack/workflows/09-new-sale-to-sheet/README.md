# 09 · Stripe New Sale → Sheet + Telegram

> Logs every Stripe sale to a Google Sheet and sends a 💰 notification to your phone via Telegram.

**File to import:** `09-new-sale-to-sheet.json`  
**Trigger:** Stripe Trigger  
**Difficulty:** ⭐⭐ Moderate · about 25 minutes

## What it does

- Listens for Stripe's `checkout.session.completed` event (Payment Links, Stripe Checkout, most website integrations).
- Adds a row to your **Sales** sheet: date, order ID, customer, amount, currency.
- Sends you an instant Telegram message — free, works on any phone.
- The Sales sheet powers workflow 10 (Daily Sales Summary), 16 (Weekly KPI Report) and 20 (Abandoned Cart Recovery).

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **Stripe API (secret key, use a restricted key if you can)** — used by: *Stripe: Checkout Completed*
- **Google Sheets OAuth2** — used by: *Add Sale to Sheet*
- **Telegram Bot API (token from @BotFather)** — used by: *Notify on Telegram*
- A Google Sheet with the tab(s): **Sales** (templates included as CSV files in this folder).

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `09-new-sale-to-sheet.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. Add a **Stripe** credential and select it on the trigger.
3. Create a sheet tab named **Sales** with the headers in `sheet-Sales.csv`; paste the sheet ID into **Config**.
4. Telegram: message @BotFather → `/newbot` → copy the token into a **Telegram** credential. Then message your bot, open `https://api.telegram.org/bot<TOKEN>/getUpdates` and copy your `chat.id` into **Config → telegramChatId**.
5. Pick your **Google Sheets** and **Telegram** credentials, then **Activate** (n8n registers the Stripe webhook automatically).

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Google Sheet columns

Column names must match exactly (capital letters and spaces included). Extra columns are fine. Use dates like `2026-11-20`.

**Tab `Sales`** — template: `sheet-Sales.csv` (*File → Import → Upload* in Google Sheets, choose *Insert new sheet*, then rename the tab to `Sales`)

| Date | Order ID | Customer Name | Customer Email | Amount | Currency | Source |
|---|---|---|---|---|---|---|
| 2026-11-04 13:05 | cs_test_a1b2c3 | Jane Smith | jane@example.com | 89 | USD | Stripe |

## Test it

In Stripe test mode, buy something through a test Payment Link with card `4242 4242 4242 4242`, or run `stripe trigger checkout.session.completed`.

## Customize it

- Selling on Shopify, WooCommerce, Square or Gumroad? Replace the Stripe trigger with a Webhook node and map the fields in *Sale Details*.
- Prefer Slack or email for alerts? Swap the Telegram node.

## Nodes used

| Node | Type | Notes |
|---|---|---|
| Stripe: Checkout Completed | Stripe Trigger | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Sale Details | Edit Fields (Set) |  |
| Add Sale to Sheet | Google Sheets |  |
| Notify on Telegram | Telegram |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
