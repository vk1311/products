# 11 · Customer Feedback Router

> A 2-question feedback form that sends happy customers to Google to leave a review — and sends unhappy customers straight to you, so you can fix things privately.

**File to import:** `11-feedback-review-router.json`  
**Trigger:** n8n Form Trigger  
**Difficulty:** ⭐ Easy · about 20 minutes

## What it does

- Hosted feedback form: *How likely are you to recommend us? (0–10)* + *Why?*
- Logs every response to a **Feedback** sheet (great for tracking your NPS over time).
- **9–10 (promoters):** emails them a thank-you with your Google review link.
- **7–8 (passives):** thanks them and asks what would make it a 10.
- **0–6 (detractors):** alerts you immediately and sends the customer a sincere apology saying you'll be in touch.

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **Google Sheets OAuth2** — used by: *Log Feedback*
- **SMTP (any email provider: Gmail, Outlook, Zoho, your host...)** — used by: *Ask for Google Review*, *Alert Owner*, *Apology to Customer*, *Thank Passive Customer*
- A Google Sheet with the tab(s): **Feedback** (templates included as CSV files in this folder).

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `11-feedback-review-router.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. Create a sheet tab named **Feedback** with the headers in `sheet-Feedback.csv`.
3. Fill in **Config** (emails, sheet ID, Google review link).
4. Pick your **Google Sheets** credential (*Log Feedback*) and **SMTP** credential (4 email nodes).
5. Activate, then copy the **Production URL** from *Feedback Form*. Send it after every job/visit (or put it on receipts as a QR code).

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Google Sheet columns

Column names must match exactly (capital letters and spaces included). Extra columns are fine. Use dates like `2026-11-20`.

**Tab `Feedback`** — template: `sheet-Feedback.csv` (*File → Import → Upload* in Google Sheets, choose *Insert new sheet*, then rename the tab to `Feedback`)

| Date | Name | Email | Score | Category | Comment |
|---|---|---|---|---|---|
| 2026-11-04 16:20 | Chris Doe | chris@example.com | 10 | Promoter | Fast and friendly! |

## Test it

Click **Test workflow**, open the form's Test URL and submit once with a 10 and once with a 3.

## Customize it

- Review platforms have rules about "review gating". To stay on the safe side, the passive and detractor emails can also include your review link — add it if you prefer.
- Send the form automatically after each job by replacing the review link in workflow 04 with this form's URL.

## Nodes used

| Node | Type | Notes |
|---|---|---|
| Feedback Form | n8n Form Trigger | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Score Feedback | Edit Fields (Set) |  |
| Log Feedback | Google Sheets |  |
| Promoter (9-10)? | If |  |
| Ask for Google Review | Send Email (SMTP) |  |
| Detractor (0-6)? | If |  |
| Alert Owner | Send Email (SMTP) |  |
| Apology to Customer | Send Email (SMTP) |  |
| Thank Passive Customer | Send Email (SMTP) |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
