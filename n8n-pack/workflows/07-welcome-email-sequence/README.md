# 07 · New Customer Welcome Sequence

> Sends every new customer a 3-email welcome series over a week: a warm welcome, helpful tips, then a thank-you offer and review request.

**File to import:** `07-welcome-email-sequence.json`  
**Trigger:** Webhook  
**Difficulty:** ⭐ Easy · about 15 minutes

## What it does

- Gives you a webhook URL that your shop, booking tool, CRM or form can call when someone becomes a customer.
- Day 0: welcome email. Day 3: tips email. Day 7: discount code + review request.
- Every email comes from you and replies go to your inbox — it feels personal, not like a newsletter.

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **SMTP (any email provider: Gmail, Outlook, Zoho, your host...)** — used by: *Email 1: Welcome*, *Email 2: Tips*, *Email 3: Offer + Review*

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `07-welcome-email-sequence.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. Fill in **Config**: business name, emails, website, discount code and review link.
3. Pick your **SMTP** credential on all three email nodes.
4. Edit the wording of the three emails (especially the tips in *Email 2*).
5. Activate, copy the **Production URL** from *New Customer Webhook*.
6. Have your tool send a POST with at least `email` (and ideally `first_name` or `name`) to that URL. Shopify, WooCommerce, Square, Calendly, Typeform, Jotform etc. all support webhooks.

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Test it

Click **Test workflow** and run:

```bash
curl -X POST 'YOUR_TEST_WEBHOOK_URL' -H 'Content-Type: application/json' -d '{"email":"you@example.com","first_name":"Alex"}'
```

Tip: while testing, temporarily set the Wait nodes to 1 minute.

## Customize it

- Change the gaps in the **Wait** nodes, or add more emails by copying a Wait + Email pair.
- Waiting executions are stored by n8n, so this works on n8n Cloud and self-hosted (with a database) even across restarts.

## Nodes used

| Node | Type | Notes |
|---|---|---|
| New Customer Webhook | Webhook | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Customer Details | Edit Fields (Set) |  |
| Has Valid Email? | Filter |  |
| Email 1: Welcome | Send Email (SMTP) |  |
| Wait 3 Days | Wait |  |
| Email 2: Tips | Send Email (SMTP) |  |
| Wait 4 Days | Wait |  |
| Email 3: Offer + Review | Send Email (SMTP) |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
