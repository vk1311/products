# 14 · Automatic Lead Follow-Ups

> Never let a lead go cold again: automatically sends polite follow-up emails on day 2, 5 and 10 to leads who haven't replied, and emails you a daily digest of who to call.

**File to import:** `14-lead-follow-up-reminders.json`  
**Trigger:** Schedule Trigger  
**Difficulty:** ⭐ Easy · about 20 minutes

## What it does

- Runs weekday mornings and reads your **Leads** sheet (filled by workflow 02, or by you).
- For leads still marked new (blank Status or `New`), sends follow-up #1 on day 2, #2 on day 5 (with booking link), #3 on day 10 (a friendly "should I close your file?" — a classic break-up email that often gets a reply).
- Updates *Follow-ups Sent* and *Last Follow-up* in the sheet.
- Emails you a digest listing every lead that was followed up, with phone numbers, so you can call the warm ones.
- Stops automatically when you set Status to anything else (`Contacted`, `Won`, `Lost`...).

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **Google Sheets OAuth2** — used by: *Get Leads*, *Update Lead Row*
- **SMTP (any email provider: Gmail, Outlook, Zoho, your host...)** — used by: *Send Follow-Up*, *Email Digest to Owner*
- A Google Sheet with the tab(s): **Leads** (templates included as CSV files in this folder).

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `14-lead-follow-up-reminders.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. Use the **Leads** tab from workflow 02 (headers in `sheet-Leads.csv`).
3. Fill in **Config**: your name (`senderName`), emails, sheet ID, booking link, timezone.
4. Pick your **Google Sheets** (2 nodes) and **SMTP** (2 nodes) credentials.
5. Edit the wording in the `STEPS` list at the top of **Find Leads to Follow Up** to sound like you. Then **Activate**.

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Google Sheet columns

Column names must match exactly (capital letters and spaces included). Extra columns are fine. Use dates like `2026-11-20`.

**Tab `Leads`** — template: `sheet-Leads.csv` (*File → Import → Upload* in Google Sheets, choose *Insert new sheet*, then rename the tab to `Leads`)

| Date | Name | Email | Phone | Message | Source | Campaign | Status | Follow-ups Sent | Last Follow-up |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-01 10:15 | Jane Smith | jane@example.com | +15551234567 | Do you offer weekend appointments? | google |  |  |  |  |

## Test it

Add a lead with your email and a *Date* 3 days ago, then click **Test workflow**.

## Customize it

- Change timings by editing `afterDays` in the STEPS list; add or remove steps freely.
- These are plain-text style emails on purpose — they get more replies than designed newsletters.

## Nodes used

| Node | Type | Notes |
|---|---|---|
| Weekdays 9:30am | Schedule Trigger | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Get Leads | Google Sheets |  |
| Find Leads to Follow Up | Code (JavaScript) |  |
| Send Follow-Up | Send Email (SMTP) |  |
| Update Lead Row | Google Sheets |  |
| Build Owner Digest | Code (JavaScript) |  |
| Email Digest to Owner | Send Email (SMTP) |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
