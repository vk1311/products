# 08 · Stripe Failed Payment Recovery

> When a Stripe subscription or invoice payment fails, instantly emails the customer a friendly "update your card" link and alerts your team on Slack.

**File to import:** `08-failed-payment-recovery.json`  
**Trigger:** Stripe Trigger  
**Difficulty:** ⭐⭐ Moderate · about 25 minutes

## What it does

- Listens for Stripe's `invoice.payment_failed` event (subscriptions and invoices).
- Emails the customer in plain, friendly language with a secure link to Stripe's hosted invoice page where they can update their card and pay.
- Posts a Slack alert with the amount, attempt number and next automatic retry date.
- Recovers revenue you'd otherwise lose to expired cards.

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **Stripe API (secret key, use a restricted key if you can)** — used by: *Stripe: Payment Failed*
- **SMTP (any email provider: Gmail, Outlook, Zoho, your host...)** — used by: *Email Customer*
- **Slack API (bot token)** — used by: *Alert Team on Slack*

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `08-failed-payment-recovery.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. Add a **Stripe** credential (Stripe Dashboard → Developers → API keys). A restricted key with *Webhook Endpoints: write* and *Invoices: read* is enough.
3. Fill in **Config** and pick your **SMTP** and **Slack** credentials.
4. Click **Activate** — n8n registers the webhook in Stripe for you automatically.

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Test it

In Stripe *test mode*, use the card `4000 0000 0000 0341` on a subscription to trigger a failed payment, or run `stripe trigger invoice.payment_failed` with the Stripe CLI.

## Customize it

- Not on Slack? Replace the Slack node with Telegram or an email to yourself.
- Add a Google Sheets node to keep a log of failed payments.

## Nodes used

| Node | Type | Notes |
|---|---|---|
| Stripe: Payment Failed | Stripe Trigger | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Payment Details | Edit Fields (Set) |  |
| Email Customer | Send Email (SMTP) |  |
| Alert Team on Slack | Slack |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
