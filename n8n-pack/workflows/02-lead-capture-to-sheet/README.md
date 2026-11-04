# 02 · Lead Capture → Google Sheet + Slack

> Catches leads from any website form, filters out junk and bots, saves them to a Google Sheet (no duplicates) and pings your team on Slack.

**File to import:** `02-lead-capture-to-sheet.json`  
**Trigger:** Webhook  
**Difficulty:** ⭐ Easy · about 20 minutes

## What it does

- Gives you a webhook URL that any website form can send to (Webflow, WordPress, Wix, Framer, Carrd, Squarespace via code block, plain HTML).
- Understands common field names automatically (`name`, `first_name`, `email`, `phone`, `message`, `utm_source`...).
- Rejects invalid emails and spam bots (hidden "honeypot" field).
- Adds the lead to your **Leads** sheet — or updates the row if that email already exists, so no duplicates.
- Posts a Slack message to your team so someone follows up fast.

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **Google Sheets OAuth2** — used by: *Save Lead to Sheet*
- **Slack API (bot token)** — used by: *Notify Team on Slack*
- A Google Sheet with the tab(s): **Leads** (templates included as CSV files in this folder).

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `02-lead-capture-to-sheet.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. Create a Google Sheet with a tab named **Leads** and the header row from `sheet-Leads.csv` (or import that file).
3. Copy the sheet ID from its URL (`docs.google.com/spreadsheets/d/`**`THIS_PART`**`/edit`) into **Config → sheetId**.
4. In **Config**, set your Slack channel ID (right-click channel → *View channel details* → bottom of the window) and timezone.
5. Pick your **Google Sheets** credential on *Save Lead to Sheet* and your **Slack** credential on *Notify Team on Slack*. Invite the Slack bot to the channel (`/invite @YourBot`).
6. Activate the workflow, then copy the **Production URL** from the *Lead Webhook* node.
7. Point your website form at that URL (POST). See the HTML snippet below if your builder doesn't have a "webhook" option.

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Google Sheet columns

Column names must match exactly (capital letters and spaces included). Extra columns are fine. Use dates like `2026-11-20`.

**Tab `Leads`** — template: `sheet-Leads.csv` (*File → Import → Upload* in Google Sheets, choose *Insert new sheet*, then rename the tab to `Leads`)

| Date | Name | Email | Phone | Message | Source | Campaign | Status | Follow-ups Sent | Last Follow-up |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-02 10:15 | Jane Smith | jane@example.com | +15551234567 | Do you offer weekend appointments? | google | fall-promo |  |  |  |

### Plain HTML / JavaScript snippet

```html
<form id="lead-form">
  <input name="name" placeholder="Name" required>
  <input name="email" type="email" placeholder="Email" required>
  <input name="phone" placeholder="Phone">
  <textarea name="message" placeholder="How can we help?"></textarea>
  <!-- honeypot: hidden from humans, bots fill it in -->
  <input name="website_url" style="display:none" tabindex="-1" autocomplete="off">
  <button>Send</button>
</form>
<script>
document.getElementById('lead-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target));
  data.source = new URLSearchParams(location.search).get('utm_source') || document.referrer || 'Website';
  const res = await fetch('YOUR_PRODUCTION_WEBHOOK_URL', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data)
  });
  e.target.outerHTML = res.ok ? '<p>Thanks! We\'ll be in touch soon.</p>' : '<p>Please check your email address.</p>';
});
</script>
```

## Test it

Click **Test workflow**, then send a test request:

```bash
curl -X POST 'YOUR_TEST_WEBHOOK_URL' -H 'Content-Type: application/json' -d '{"name":"Test Lead","email":"test@example.com","message":"Hi!"}'
```

## Customize it

- Not on Slack? Swap the Slack node for **Send Email**, **Telegram** or **Microsoft Teams**.
- Blank **Status** means "new". Type `Contacted`, `Won` or `Lost` as you work leads — workflow 14 uses this column to send follow-ups.

## Nodes used

| Node | Type | Notes |
|---|---|---|
| Lead Webhook | Webhook | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Clean Up Lead | Code (JavaScript) |  |
| Valid Lead? | If |  |
| Save Lead to Sheet | Google Sheets |  |
| Notify Team on Slack | Slack |  |
| Respond: Success | Respond to Webhook |  |
| Respond: Invalid | Respond to Webhook |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
