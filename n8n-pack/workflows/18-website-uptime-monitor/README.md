# 18 · Website Uptime Monitor

> Checks your website(s) every 5 minutes and alerts you by email and Telegram the moment one goes down — and again when it's back.

**File to import:** `18-website-uptime-monitor.json`  
**Trigger:** Schedule Trigger  
**Difficulty:** ⭐ Easy · about 20 minutes

## What it does

- Checks each URL you list every 5 minutes (with one automatic retry to avoid false alarms).
- Treats timeouts, errors and HTTP 4xx/5xx as "down". Optionally also checks that a word appears on the page (catches blank or hacked pages).
- Alerts only on changes — one message when it goes down, one when it recovers (with downtime length). No spam.
- Replaces paid uptime-monitoring tools for most small businesses.

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **SMTP (any email provider: Gmail, Outlook, Zoho, your host...)** — used by: *Email Alert*
- **Telegram Bot API (token from @BotFather)** — used by: *Telegram Alert*

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `18-website-uptime-monitor.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. In **Config**, list your URLs separated by commas. Optionally set `mustContain` to a word that's always on your homepage (e.g. your business name).
3. Fill in your email and Telegram chat ID (see workflow 09's README for how to get a chat ID).
4. Pick your **SMTP** and **Telegram** credentials (or delete the alert node you don't want).
5. Click **Activate**. The "remember last status" feature only works while the workflow is active.

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Test it

Temporarily add a fake URL such as `https://this-does-not-exist-12345.com` to Config and click **Test workflow** — you'll get a DOWN alert.

## Customize it

- Change the check frequency in the trigger (every 1–15 minutes is typical).
- Monitor your booking page, online shop checkout, or API endpoints too.

## Nodes used

| Node | Type | Notes |
|---|---|---|
| Every 5 Minutes | Schedule Trigger | Trigger |
| Config | Edit Fields (Set) | Your settings |
| One Item per URL | Code (JavaScript) |  |
| Check Website | HTTP Request |  |
| Detect Status Changes | Code (JavaScript) |  |
| Email Alert | Send Email (SMTP) |  |
| Telegram Alert | Telegram |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
