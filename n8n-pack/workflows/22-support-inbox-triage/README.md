# 22 · Support Inbox Triage

> Watches your support inbox, sorts each email into Urgent / Billing / Booking / Complaint / General, logs it to a sheet, alerts your team on Slack and sends the customer an instant acknowledgement with a ticket number.

**File to import:** `22-support-inbox-triage.json`  
**Trigger:** Email Trigger (IMAP)  
**Difficulty:** ⭐⭐ Moderate · about 30 minutes

## What it does

- Watches any mailbox over IMAP (Gmail, Outlook/Microsoft 365, Zoho, cPanel, Fastmail...).
- Categorizes each new email with simple, editable keyword rules and flags Urgent/Complaint as high priority.
- Logs it to a **Support Log** sheet with a ticket ID — a free, lightweight helpdesk.
- Posts a summary to Slack so the team sees it immediately.
- Auto-replies with a ticket reference — but never to no-reply addresses, out-of-office messages or replies in an existing thread (prevents email loops).

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **IMAP (the inbox to watch)** — used by: *New Support Email*
- **Google Sheets OAuth2** — used by: *Log to Support Sheet*
- **Slack API (bot token)** — used by: *Post to Slack*
- **SMTP (any email provider: Gmail, Outlook, Zoho, your host...)** — used by: *Auto-Acknowledge*
- A Google Sheet with the tab(s): **Support Log** (templates included as CSV files in this folder).

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `22-support-inbox-triage.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. Add an **IMAP** credential for your support inbox. For Gmail: enable IMAP and create an *App Password* (Google Account → Security). Host `imap.gmail.com`, port 993, SSL on.
3. Create a sheet tab named **Support Log** with the headers in `sheet-Support Log.csv`.
4. Fill in **Config** (emails, sheet ID, Slack channel ID, usual reply time).
5. Pick your **Google Sheets**, **Slack** and **SMTP** credentials. Use the *same* address for `fromEmail` as the support inbox.
6. Click **Activate**. Only emails that arrive after activation are processed.

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Google Sheet columns

Column names must match exactly (capital letters and spaces included). Extra columns are fine. Use dates like `2026-11-20`.

**Tab `Support Log`** — template: `sheet-Support Log.csv` (*File → Import → Upload* in Google Sheets, choose *Insert new sheet*, then rename the tab to `Support Log`)

| Ticket ID | Received | From | Name | Subject | Category | Priority | Preview | Status |
|---|---|---|---|---|---|---|---|---|
| T-261104-9QX1 | 2026-11-04 08:41 | pat@example.com | Pat Kim | Urgent: heating not working | Urgent | High | Hi, our heating stopped working last night... | Open |

## Test it

Activate the workflow, send an email to the support inbox from another address with the subject "Urgent: my booking", and check Slack, the sheet and your auto-reply.

## Customize it

- Add categories or keywords in the `RULES` list at the top of **Categorize Email**.
- Route categories to different people: add an *If* or *Switch* node after the Code node and send to different Slack channels/emails.

## Nodes used

| Node | Type | Notes |
|---|---|---|
| New Support Email | Email Trigger (IMAP) | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Categorize Email | Code (JavaScript) |  |
| Log to Support Sheet | Google Sheets |  |
| Post to Slack | Slack |  |
| Send Auto-Reply? | If |  |
| Auto-Acknowledge | Send Email (SMTP) |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
