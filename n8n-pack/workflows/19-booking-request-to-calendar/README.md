# 19 · Booking Form → Google Calendar

> A simple booking form that checks your Google Calendar, books the slot if you're free (with a calendar invite to the customer) or politely asks them to pick another time.

**File to import:** `19-booking-request-to-calendar.json`  
**Trigger:** n8n Form Trigger  
**Difficulty:** ⭐ Easy · about 20 minutes

## What it does

- Hosted booking form: name, contact details, service, date and time.
- Checks your Google Calendar for conflicts in real time.
- **Free:** creates the event, sends the customer a Google Calendar invite and a confirmation email (you're BCC'd).
- **Busy or too soon (under 2 hours' notice):** emails the customer asking them to choose another time.
- A free alternative to paid booking tools for simple appointment businesses.

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **Google Calendar OAuth2** — used by: *Check Calendar Availability*, *Create Calendar Event*
- **SMTP (any email provider: Gmail, Outlook, Zoho, your host...)** — used by: *Email Confirmation*, *Email: Pick Another Time*

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `19-booking-request-to-calendar.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. Add a **Google Calendar OAuth2** credential in n8n and select it on *Check Calendar Availability* and *Create Calendar Event*.
3. In **Config**, set your timezone, appointment length (`durationMinutes`), address and `calendarId` (`primary` = your main calendar; for another calendar use its ID from Google Calendar → Settings → *Integrate calendar*).
4. Edit the form's *Service* and *Time* options to match your offering and opening hours.
5. Pick your **SMTP** credential on both email nodes.
6. Activate, copy the form's **Production URL**, paste it into **Config → bookingFormUrl**, save, and share the link on your website.

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Test it

Click **Test workflow**, open the Test URL and book a slot tomorrow. Then book the same slot again — you should get the "pick another time" email.

## Customize it

- Combine with workflow 05 (Appointment Reminders) by adding a Google Sheets *Append* node after *Create Calendar Event*.
- Block out lunch or days off simply by adding events to your calendar — the availability check respects them.

## Nodes used

| Node | Type | Notes |
|---|---|---|
| Booking Request Form | n8n Form Trigger | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Build Event | Code (JavaScript) |  |
| Check Calendar Availability | HTTP Request |  |
| Slot Free? | If |  |
| Create Calendar Event | HTTP Request |  |
| Email Confirmation | Send Email (SMTP) |  |
| Email: Pick Another Time | Send Email (SMTP) |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
