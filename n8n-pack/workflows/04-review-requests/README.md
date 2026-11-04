# 04 · Google Review Requests

> Automatically asks happy customers for a Google review a day after their job is done — by email, and optionally by SMS.

**File to import:** `04-review-requests.json`  
**Trigger:** Schedule Trigger  
**Difficulty:** ⭐⭐ Moderate · about 25 minutes

## What it does

- Runs daily and reads your **Jobs** sheet.
- Finds jobs completed at least `delayDays` ago (default 1) and less than 30 days ago that haven't been asked yet.
- Emails the customer a short, personal request with a one-click **Leave a review** button.
- Optional: also texts them via Twilio (node is included but switched off until you enable it).
- Marks the row `Review Requested = Yes` so nobody is ever asked twice.

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **Google Sheets OAuth2** — used by: *Get Completed Jobs*, *Mark as Requested*
- **SMTP (any email provider: Gmail, Outlook, Zoho, your host...)** — used by: *Email Review Request*
- **Twilio (Account SID + Auth Token)** — used by: *Text Review Request (optional)*
- A Google Sheet with the tab(s): **Jobs** (templates included as CSV files in this folder).

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `04-review-requests.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. Get your Google review link: Google Business Profile → *Ask for reviews* → copy the link (looks like `https://g.page/r/.../review`).
3. Create a sheet tab named **Jobs** with the headers in `sheet-Jobs.csv`.
4. Fill in **Config**: business name, emails, sheet ID, review link, timezone.
5. Pick credentials: **Google Sheets** (2 nodes) and **SMTP** (*Email Review Request*).
6. Optional SMS: right-click *Text Review Request (optional)* → **Activate**, add your **Twilio** credential and set `twilioFrom` in Config.
7. Add a row whenever you finish a job (or connect your booking/invoicing tool to the sheet), then click **Activate**.

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Google Sheet columns

Column names must match exactly (capital letters and spaces included). Extra columns are fine. Use dates like `2026-11-20`.

**Tab `Jobs`** — template: `sheet-Jobs.csv` (*File → Import → Upload* in Google Sheets, choose *Insert new sheet*, then rename the tab to `Jobs`)

| Job ID | Customer Name | Customer Email | Customer Phone | Completed Date | Review Requested | Review Requested Date |
|---|---|---|---|---|---|---|
| J-2041 | Sam Lee | sam@example.com | +15551234567 | 2026-11-03 |  |  |

## Test it

Add a row with your own email and yesterday's date as *Completed Date*, then click **Test workflow**.

## Customize it

- Swap the review link for Facebook, Yelp, Trustpilot or TripAdvisor — any URL works.
- Want to filter unhappy customers first? Use workflow 11 (Feedback Router) instead, which only sends promoters to Google.

## Nodes used

| Node | Type | Notes |
|---|---|---|
| Every Day 10am | Schedule Trigger | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Get Completed Jobs | Google Sheets |  |
| Find Customers to Ask | Code (JavaScript) |  |
| Email Review Request | Send Email (SMTP) |  |
| Text Review Request (optional) | Twilio | Off by default (optional) |
| Mark as Requested | Google Sheets |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
