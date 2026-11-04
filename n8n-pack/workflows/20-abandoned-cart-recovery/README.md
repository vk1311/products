# 20 · Abandoned Cart Recovery

> Wins back lost sales: 1 hour after someone abandons their cart, sends a friendly reminder; 24 hours later, if they still haven't bought, sends a discount code.

**File to import:** `20-abandoned-cart-recovery.json`  
**Trigger:** Webhook  
**Difficulty:** ⭐ Easy · about 20 minutes

## What it does

- Gives you a webhook URL your shop calls when a checkout is started but not finished.
- Waits 1 hour, checks your **Sales** sheet — if they haven't bought, sends a "you left something" email with a link back to their cart.
- Waits another 23 hours, checks again, and if still no purchase sends a discount code.
- Never emails someone who already bought.

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **Google Sheets OAuth2** — used by: *Check Sales Sheet*, *Check Sales Sheet Again*
- **SMTP (any email provider: Gmail, Outlook, Zoho, your host...)** — used by: *Email 1: You Left Something*, *Email 2: Discount Offer*
- A Google Sheet with the tab(s): **Sales** (templates included as CSV files in this folder).

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `20-abandoned-cart-recovery.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. Make sure purchases land in a **Sales** sheet with a `Customer Email` and `Date` column (workflow 09 does this for Stripe). See `sheet-Sales.csv`.
3. Fill in **Config** (emails, sheet ID, discount code). Create the discount code in your shop first.
4. Pick your **Google Sheets** (2 nodes) and **SMTP** (2 nodes) credentials.
5. Activate, copy the **Production URL** from *Cart Abandoned Webhook*, and have your shop/checkout POST to it with: `email`, `first_name`, `cart_url`, optional `items` (list of names) and `total`.

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Google Sheet columns

Column names must match exactly (capital letters and spaces included). Extra columns are fine. Use dates like `2026-11-20`.

**Tab `Sales`** — template: `sheet-Sales.csv` (*File → Import → Upload* in Google Sheets, choose *Insert new sheet*, then rename the tab to `Sales`)

| Date | Order ID | Customer Name | Customer Email | Amount | Currency | Source |
|---|---|---|---|---|---|---|
| 2026-11-04 13:05 | cs_test_a1b2c3 | Jane Smith | jane@example.com | 89 | USD | Stripe |

## Test it

Temporarily set both Wait nodes to 1 minute, click **Test workflow**, then:

```bash
curl -X POST 'YOUR_TEST_WEBHOOK_URL' -H 'Content-Type: application/json' -d '{"email":"you@example.com","first_name":"Sam","cart_url":"https://yourshop.com/cart","items":["Blue mug","Coffee beans"]}'
```

## Customize it

- Shopify and WooCommerce have built-in abandoned-checkout emails; this workflow is ideal for custom sites, booking deposits, course checkouts, or when you want full control of the timing and wording.
- Change timings in the Wait nodes (1h + 23h is the industry sweet spot).

## Nodes used

| Node | Type | Notes |
|---|---|---|
| Cart Abandoned Webhook | Webhook | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Cart Details | Edit Fields (Set) |  |
| Has Email & Cart Link? | Filter |  |
| Wait 1 Hour | Wait |  |
| Check Sales Sheet | Google Sheets |  |
| Purchased Yet? | Code (JavaScript) |  |
| Still Not Purchased? | If |  |
| Email 1: You Left Something | Send Email (SMTP) |  |
| Wait 23 Hours | Wait |  |
| Check Sales Sheet Again | Google Sheets |  |
| Purchased Yet? (2) | Code (JavaScript) |  |
| Still Not Purchased? (2) | If |  |
| Email 2: Discount Offer | Send Email (SMTP) |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
