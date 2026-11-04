# 24 · New Google Review Alert

> Checks your Google Business reviews every 6 hours, posts each new review to Slack, and emails you right away about any bad review so you can respond fast.

**File to import:** `24-new-google-review-alert.json`  
**Trigger:** Schedule Trigger  
**Difficulty:** ⭐⭐ Moderate · about 25 minutes

## What it does

- Uses the official Google Places API to fetch your latest reviews.
- Remembers which reviews it's already seen, so you only hear about new ones.
- Posts every new review to Slack (🎉 for good ones, 🚨 for bad ones).
- Emails you about 1–3 star reviews (threshold configurable) with tips for replying.

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **Header Auth: name `X-Goog-Api-Key`, value = your Google Places API key** — used by: *Get Google Reviews*
- **Slack API (bot token)** — used by: *Post Review to Slack*
- **SMTP (any email provider: Gmail, Outlook, Zoho, your host...)** — used by: *Email Owner: Respond Fast*

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `24-new-google-review-alert.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. In Google Cloud Console, create a project, enable **Places API (New)** and create an API key (restrict it to Places API). Google gives a generous free monthly allowance — checking every 6 hours stays well within it.
3. In n8n, create a **Header Auth** credential: *Name* `X-Goog-Api-Key`, *Value* = your API key. Select it on *Get Google Reviews*.
4. Find your Place ID with Google's Place ID Finder (search "Google Place ID Finder") and paste it into **Config → placeId**.
5. Fill in the rest of **Config** and pick your **Slack** and **SMTP** credentials.
6. Click **Activate**. The first live run quietly records your existing reviews; alerts start with the next new one.

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Test it

Click **Test workflow** — test runs always post your most recent review (marked "test run") so you can check everything works.

## Customize it

- Google's API returns your 5 most relevant recent reviews, which is plenty for a 6-hour check. For very busy locations, run it every hour.
- No Slack? Replace the Slack node with Telegram or delete it and keep just the email.

## Nodes used

| Node | Type | Notes |
|---|---|---|
| Every 6 Hours | Schedule Trigger | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Get Google Reviews | HTTP Request |  |
| Find New Reviews | Code (JavaScript) |  |
| Post Review to Slack | Slack |  |
| Negative Review? | If |  |
| Email Owner: Respond Fast | Send Email (SMTP) |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
