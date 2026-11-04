# 12 · No-Show Follow-Up

> Turns missed appointments back into bookings: every evening, sends no-shows a friendly, no-guilt message with a link to rebook.

**File to import:** `12-no-show-follow-up.json`  
**Trigger:** Schedule Trigger  
**Difficulty:** ⭐⭐ Moderate · about 25 minutes

## What it does

- Runs every day at 6pm and reads your **Appointments** sheet (same sheet as workflow 05).
- Finds appointments with **Status** = `No-show` from the last 7 days.
- Emails a warm "we missed you — pick a new time" message with your booking link (optional SMS too).
- Marks the row so each client only gets one follow-up.

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **Google Sheets OAuth2** — used by: *Get Appointments*, *Mark Followed Up*
- **SMTP (any email provider: Gmail, Outlook, Zoho, your host...)** — used by: *Email: Let's Rebook*
- **Twilio (Account SID + Auth Token)** — used by: *SMS: Let's Rebook (optional)*
- A Google Sheet with the tab(s): **Appointments** (templates included as CSV files in this folder).

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `12-no-show-follow-up.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. Use the **Appointments** tab from workflow 05 (headers in `sheet-Appointments.csv`).
3. Fill in **Config**, especially your `bookingLink` (Calendly, Square, Acuity, Fresha, your website...).
4. Pick your **Google Sheets** (2 nodes) and **SMTP** credentials. Optional: enable the SMS node and add **Twilio**.
5. When a client doesn't show, set their **Status** to `No-show`. Click **Activate**.

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Google Sheet columns

Column names must match exactly (capital letters and spaces included). Extra columns are fine. Use dates like `2026-11-20`.

**Tab `Appointments`** — template: `sheet-Appointments.csv` (*File → Import → Upload* in Google Sheets, choose *Insert new sheet*, then rename the tab to `Appointments`)

| Appointment ID | Client Name | Client Email | Client Phone | Date | Time | Service | Status | Reminder 24h Sent | Reminder 2h Sent | No-show Followed Up |
|---|---|---|---|---|---|---|---|---|---|---|
| A-3002 | Tom Baker | tom@example.com | +15559876543 | 2026-11-04 | 10:00 | Consultation | No-show | 2026-11-03 10:00 | 2026-11-04 08:00 |  |

## Test it

Mark a test appointment from today as `No-show` (using your own email) and click **Test workflow**.

## Customize it

- Add a small incentive ("10% off if you rebook this week") to the email to boost rebooking rates.

## Nodes used

| Node | Type | Notes |
|---|---|---|
| Every Day 6pm | Schedule Trigger | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Get Appointments | Google Sheets |  |
| Find No-Shows | Code (JavaScript) |  |
| Has Email? | Filter |  |
| Email: Let's Rebook | Send Email (SMTP) |  |
| SMS: Let's Rebook (optional) | Twilio | Off by default (optional) |
| Mark Followed Up | Google Sheets |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
