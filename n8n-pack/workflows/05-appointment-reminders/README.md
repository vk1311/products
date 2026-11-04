# 05 · Appointment Reminders

> Cuts no-shows by reminding clients 24 hours and 2 hours before their appointment, by email and (optionally) SMS.

**File to import:** `05-appointment-reminders.json`  
**Trigger:** Schedule Trigger  
**Difficulty:** ⭐⭐ Moderate · about 25 minutes

## What it does

- Runs every hour and reads your **Appointments** sheet.
- Sends a reminder ~24 hours before, and another ~2 hours before each appointment.
- Skips cancelled / completed / no-show appointments.
- Optional SMS via Twilio (included, switched off until you enable it).
- Stamps the sheet so each reminder only goes out once.

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **Google Sheets OAuth2** — used by: *Get Appointments*, *Mark Reminder Sent*
- **SMTP (any email provider: Gmail, Outlook, Zoho, your host...)** — used by: *Email Reminder*
- **Twilio (Account SID + Auth Token)** — used by: *SMS Reminder (optional)*
- A Google Sheet with the tab(s): **Appointments** (templates included as CSV files in this folder).

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `05-appointment-reminders.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. Create a sheet tab named **Appointments** with the headers in `sheet-Appointments.csv`.
3. Fill in **Config** — especially `timezone` (e.g. `Europe/London`, `Australia/Sydney`), address and phone number.
4. Pick your **Google Sheets** credential (2 nodes) and **SMTP** credential (*Email Reminder*).
5. Optional SMS: enable *SMS Reminder (optional)*, add a **Twilio** credential and set `twilioFrom`. Phone numbers must look like `+15551234567`.
6. Use `YYYY-MM-DD` dates and `14:30` or `2:30 PM` times. Click **Activate**.

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Google Sheet columns

Column names must match exactly (capital letters and spaces included). Extra columns are fine. Use dates like `2026-11-20`.

**Tab `Appointments`** — template: `sheet-Appointments.csv` (*File → Import → Upload* in Google Sheets, choose *Insert new sheet*, then rename the tab to `Appointments`)

| Appointment ID | Client Name | Client Email | Client Phone | Date | Time | Service | Status | Reminder 24h Sent | Reminder 2h Sent | No-show Followed Up |
|---|---|---|---|---|---|---|---|---|---|---|
| A-3001 | Priya Patel | priya@example.com | +15551234567 | 2026-11-05 | 14:30 | Haircut & style | Booked |  |  |  |

## Test it

Add a row with your email, today's date and a time ~90 minutes from now. Click **Test workflow** — you'll get the 2-hour reminder.

## Customize it

- Change the windows (24h / 2h) in the **Find Upcoming Appointments** code.
- Booking tool exports to Google Sheets (Calendly, Acuity, Square, Fresha via Zapier/Make or CSV)? Point this workflow at that sheet and rename the column names in the code.
- Workflow 12 (No-Show Follow-Up) uses this same sheet.

## Nodes used

| Node | Type | Notes |
|---|---|---|
| Every Hour | Schedule Trigger | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Get Appointments | Google Sheets |  |
| Find Upcoming Appointments | Code (JavaScript) |  |
| Has Email? | Filter |  |
| Email Reminder | Send Email (SMTP) |  |
| SMS Reminder (optional) | Twilio | Off by default (optional) |
| Mark Reminder Sent | Google Sheets |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
