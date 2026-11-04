# 01 · Contact Form → Email

> A hosted contact form that emails you every inquiry and sends the customer an instant, friendly auto-reply.

**File to import:** `01-contact-form-to-email.json`  
**Trigger:** n8n Form Trigger  
**Difficulty:** ⭐ Easy · about 15 minutes

## What it does

- Gives you a ready-made contact form page (hosted by n8n — no website plugin needed). Link to it or embed it.
- Emails you each inquiry with all the details. Hit *Reply* and you're answering the customer directly.
- Sends the customer an instant "we got your message" email so they know you're on it.

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **SMTP (any email provider: Gmail, Outlook, Zoho, your host...)** — used by: *Email Owner*, *Auto-Reply to Customer*

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `01-contact-form-to-email.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. Open the **Config** node and fill in your business name, your email, the address emails are sent from, and your usual reply time.
3. Open **Email Owner** and pick (or create) your **SMTP** credential. Do the same on **Auto-Reply to Customer**.
4. Optional: open **Contact Form** to change the title, fields or the thank-you message.
5. Click **Activate**. Open the **Contact Form** node and copy the **Production URL** — that's your form link.
6. Put the link on your website (button, menu item or `<iframe>`), Google Business Profile, Instagram bio, etc.

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Test it

Click **Test workflow**, open the *Test URL* shown in the Contact Form node, submit the form, and check both inboxes.

## Customize it

- Add fields (e.g. *Service needed* dropdown) in the Contact Form node, then reference them in the emails with `{{ $('Contact Form').item.json['Field label'] }}`.
- Want the inquiry in a spreadsheet too? Add a Google Sheets *Append* node after Email Owner (see workflow 02 for an example).

## Nodes used

| Node | Type | Notes |
|---|---|---|
| Contact Form | n8n Form Trigger | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Email Owner | Send Email (SMTP) |  |
| Auto-Reply to Customer | Send Email (SMTP) |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
