# Small Business Automation Pack: 25 n8n Workflows

**TL;DR:** 25 ready-to-import n8n workflows that handle the repetitive jobs every small business has: contact forms, lead capture, invoice chasing, review requests, appointment reminders, social posting, sales reports and more. Import a file, fill in one **Config** node, pick your logins, click **Activate**.

- ✅ **Built-in nodes only.** No community nodes to install, so it works on n8n Cloud and self-hosted.
- ✅ **No real keys inside.** Every login is a placeholder you swap for your own in a dropdown.
- ✅ **One place to edit.** Your business name, emails, sheet ID, links, etc. all live in a single **Config** node at the start of each workflow.
- ✅ **Setup notes on the canvas.** Each workflow opens with a sticky note listing its setup steps, and each folder has a step-by-step README.
- ✅ **Validated.** Every file was checked against n8n's official node definitions, and the JavaScript logic was run against test data (see [Validation](#validation)).

---

## What's inside

```
n8n-pack/
├── README.md                ← you are here
├── sales-page.md            ← Gumroad listing copy
├── LICENSE.md
├── sheet-templates/         ← every Google Sheet tab used by the pack, as CSV
├── scripts/validate.py      ← checks every workflow file (optional)
└── workflows/
    ├── 01-contact-form-to-email/
    │   ├── 01-contact-form-to-email.json   ← import this into n8n
    │   ├── README.md                       ← what it does, setup steps, nodes used
    │   └── sheet-*.csv                     ← Google Sheet template (if the workflow uses one)
    └── … 25 folders in total
```

## Quick start (about 10 minutes for your first workflow)

1. **Import** a workflow: in n8n, *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose the `.json` file. (You can also copy the file's contents and paste them straight onto the canvas.)
2. **Read the yellow sticky note** on the left of the canvas. It lists that workflow's setup steps.
3. **Open the `Config` node** and replace the example values with your own: business name, emails, Google Sheet ID, links, timezone.
4. **Connect your logins.** Any node with a ⚠️ warning needs a credential. Open it and pick yours from the *Credential* dropdown, or choose *Create new credential*. (Logins you create once can be reused by every workflow.)
5. **Test**, then **Activate.** Click *Test workflow* and check the result, then flip the *Active* switch (top right).

> **New to n8n?** n8n is an automation tool, like Zapier but more flexible and much cheaper at volume. You can use [n8n Cloud](https://n8n.io) or host it yourself. Everything in this pack works with either.

## The 25 workflows

| # | Workflow | What it does | Trigger | Logins needed |
|---|---|---|---|---|
| 01 | [Contact Form → Email](workflows/01-contact-form-to-email/README.md) | A hosted contact form that emails you every inquiry and sends the customer an instant, friendly auto-reply. | n8n Form Trigger | SMTP |
| 02 | [Lead Capture → Google Sheet + Slack](workflows/02-lead-capture-to-sheet/README.md) | Catches leads from any website form, filters out junk and bots, saves them to a Google Sheet (no duplicates) and pings your team on Slack. | Webhook | Google Sheets, Slack |
| 03 | [Invoice Payment Reminders](workflows/03-invoice-reminders/README.md) | Every morning, checks your invoice sheet and emails clients a reminder at the right moment — a friendly nudge before the due date, then gradually firmer notices if it's late. | Schedule Trigger | Google Sheets, SMTP |
| 04 | [Google Review Requests](workflows/04-review-requests/README.md) | Automatically asks happy customers for a Google review a day after their job is done — by email, and optionally by SMS. | Schedule Trigger | Google Sheets, SMTP, Twilio |
| 05 | [Appointment Reminders](workflows/05-appointment-reminders/README.md) | Cuts no-shows by reminding clients 24 hours and 2 hours before their appointment, by email and (optionally) SMS. | Schedule Trigger | Google Sheets, SMTP, Twilio |
| 06 | [Social Media Cross-Posting](workflows/06-social-cross-posting/README.md) | Write a post once in a simple form and publish it to X, LinkedIn, your Facebook Page and your Telegram channel in one click. | n8n Form Trigger | X, LinkedIn, Facebook Graph, Telegram |
| 07 | [New Customer Welcome Sequence](workflows/07-welcome-email-sequence/README.md) | Sends every new customer a 3-email welcome series over a week: a warm welcome, helpful tips, then a thank-you offer and review request. | Webhook | SMTP |
| 08 | [Stripe Failed Payment Recovery](workflows/08-failed-payment-recovery/README.md) | When a Stripe subscription or invoice payment fails, instantly emails the customer a friendly "update your card" link and alerts your team on Slack. | Stripe Trigger | Stripe, SMTP, Slack |
| 09 | [Stripe New Sale → Sheet + Telegram](workflows/09-new-sale-to-sheet/README.md) | Logs every Stripe sale to a Google Sheet and sends a 💰 notification to your phone via Telegram. | Stripe Trigger | Stripe, Google Sheets, Telegram |
| 10 | [Daily Sales Summary](workflows/10-daily-sales-summary/README.md) | Every evening, emails you a clean one-glance summary of the day's sales: revenue, orders, average order value and how it compares with yesterday and last week. | Schedule Trigger | Google Sheets, SMTP |
| 11 | [Customer Feedback Router](workflows/11-feedback-review-router/README.md) | A 2-question feedback form that sends happy customers to Google to leave a review — and sends unhappy customers straight to you, so you can fix things privately. | n8n Form Trigger | Google Sheets, SMTP |
| 12 | [No-Show Follow-Up](workflows/12-no-show-follow-up/README.md) | Turns missed appointments back into bookings: every evening, sends no-shows a friendly, no-guilt message with a link to rebook. | Schedule Trigger | Google Sheets, SMTP, Twilio |
| 13 | [Quote Request Intake & Routing](workflows/13-quote-request-router/README.md) | A professional quote request form that scores how hot each lead is, sends it to the right person on your team, logs it to a sheet and confirms with the customer. | n8n Form Trigger | Google Sheets, SMTP |
| 14 | [Automatic Lead Follow-Ups](workflows/14-lead-follow-up-reminders/README.md) | Never let a lead go cold again: automatically sends polite follow-up emails on day 2, 5 and 10 to leads who haven't replied, and emails you a daily digest of who to call. | Schedule Trigger | Google Sheets, SMTP |
| 15 | [Customer Birthday Offers](workflows/15-birthday-offers/README.md) | Sends every customer a warm birthday email with a discount code on their birthday — a simple, personal touch customers remember. | Schedule Trigger | Google Sheets, SMTP |
| 16 | [Weekly Business KPI Report](workflows/16-weekly-kpi-report/README.md) | Every Monday morning, emails you a one-page report on last week: revenue, orders, average order, new leads, lead sources, best days and top customers — each compared with the week before. | Schedule Trigger | Google Sheets, SMTP |
| 17 | [Blog Post → Auto-Share to Social](workflows/17-blog-rss-to-social/README.md) | Publish a blog post and it's automatically shared to X, LinkedIn, your Facebook Page and Telegram within the hour — with the title, a short teaser and the link. | RSS Feed Trigger | X, LinkedIn, Facebook Graph, Telegram |
| 18 | [Website Uptime Monitor](workflows/18-website-uptime-monitor/README.md) | Checks your website(s) every 5 minutes and alerts you by email and Telegram the moment one goes down — and again when it's back. | Schedule Trigger | SMTP, Telegram |
| 19 | [Booking Form → Google Calendar](workflows/19-booking-request-to-calendar/README.md) | A simple booking form that checks your Google Calendar, books the slot if you're free (with a calendar invite to the customer) or politely asks them to pick another time. | n8n Form Trigger | Google Calendar, SMTP |
| 20 | [Abandoned Cart Recovery](workflows/20-abandoned-cart-recovery/README.md) | Wins back lost sales: 1 hour after someone abandons their cart, sends a friendly reminder; 24 hours later, if they still haven't bought, sends a discount code. | Webhook | Google Sheets, SMTP |
| 21 | [Monthly Retainer Invoices](workflows/21-monthly-retainer-invoices/README.md) | On the 1st of every month, emails each retainer client a professional invoice with a Pay button, logs it to your Invoices sheet, and hands it to the reminder workflow. | Schedule Trigger | Google Sheets, SMTP |
| 22 | [Support Inbox Triage](workflows/22-support-inbox-triage/README.md) | Watches your support inbox, sorts each email into Urgent / Billing / Booking / Complaint / General, logs it to a sheet, alerts your team on Slack and sends the customer an instant acknowledgement with a ticket number. | Email Trigger (IMAP) | IMAP, Google Sheets, Slack, SMTP |
| 23 | [Low Stock Alert](workflows/23-low-stock-alert/README.md) | Every morning, checks your inventory sheet and emails you a list of products that are low or out of stock — and can optionally email each supplier a ready-made reorder request. | Schedule Trigger | Google Sheets, SMTP |
| 24 | [New Google Review Alert](workflows/24-new-google-review-alert/README.md) | Checks your Google Business reviews every 6 hours, posts each new review to Slack, and emails you right away about any bad review so you can respond fast. | Schedule Trigger | Header Auth, Slack, SMTP |
| 25 | [Missed Call → Instant Text-Back](workflows/25-missed-call-text-back/README.md) | When you can't pick up, the caller instantly gets a friendly text from your business number — so they message you instead of calling your competitor. | Webhook | Twilio, Telegram |

### Workflows that work well together

| Bundle | Workflows | Shared sheet tab |
|---|---|---|
| **Get paid on time** | 21 Monthly Retainer Invoices → 03 Invoice Reminders | `Invoices` |
| **Sales autopilot** | 09 Stripe Sale → Sheet → 10 Daily Summary, 16 Weekly KPIs, 20 Abandoned Cart | `Sales` |
| **Lead machine** | 02 Lead Capture → 14 Lead Follow-Ups → 16 Weekly KPIs | `Leads` |
| **Fewer no-shows** | 19 Booking Form, 05 Appointment Reminders, 12 No-Show Follow-Up | `Appointments` |
| **5-star reputation** | 11 Feedback Router, 04 Review Requests, 24 New Review Alert | `Feedback`, `Jobs` |

Tip: use **one Google Spreadsheet** with several tabs (Leads, Sales, Invoices…). Put the same sheet ID in every workflow's Config and the workflows share data automatically.

## How every workflow is built

| Convention | What it means for you |
|---|---|
| **Config node** | The first node after the trigger. All your settings live here. Other nodes read from it, so you rarely need to open them. |
| **Sticky note** | Setup steps right on the canvas. Delete it once you're done if you like. |
| **Credential placeholders** | Logins are named like `SMTP account` / `Google Sheets account` with the ID `REPLACE_WITH_YOUR_CREDENTIAL`. Just select your own. |
| **Optional nodes are switched off** | Extras such as SMS via Twilio or auto-emailing suppliers come *deactivated* (greyed out). Right-click → *Activate* to turn them on. |
| **Plain-English code** | Where logic is needed (e.g. "which invoices are overdue?") it's in a Code node with the editable parts (wording, timings, rules) at the top. |
| **No double-sends** | Workflows that email from a sheet write back a "sent" marker, so customers never get the same message twice. |
| **SMTP for email** | Emails go out through SMTP, so they work with Gmail, Outlook/Microsoft 365, Zoho, Fastmail, your web host, Brevo, Mailgun, SendGrid… |

## Credentials you may need

You only need the ones for the workflows you use. Set each one up once in n8n (*Overview → Credentials → Create*) and reuse it everywhere.

| Credential (n8n type) | Used by workflows |
|---|---|
| SMTP (any email provider: Gmail, Outlook, Zoho, your host...) | 01, 03, 04, 05, 07, 08, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24 |
| Google Sheets OAuth2 | 02, 03, 04, 05, 09, 10, 11, 12, 13, 14, 15, 16, 20, 21, 22, 23 |
| Telegram Bot API (token from @BotFather) | 06, 09, 17, 18, 25 |
| Slack API (bot token) | 02, 08, 22, 24 |
| Twilio (Account SID + Auth Token) | 04, 05, 12, 25 |
| X (Twitter) OAuth2 | 06, 17 |
| LinkedIn OAuth2 | 06, 17 |
| Facebook Graph API (Page access token) | 06, 17 |
| Stripe API (secret key, use a restricted key if you can) | 08, 09 |
| Google Calendar OAuth2 | 19 |
| IMAP (the inbox to watch) | 22 |
| Header Auth: name `X-Goog-Api-Key`, value = your Google Places API key | 24 |

**Where to find things:**

- **Google Sheet ID:** the long code in the sheet's URL: `docs.google.com/spreadsheets/d/`**`THIS_PART`**`/edit`.
- **SMTP with Gmail:** host `smtp.gmail.com`, port `465`, SSL on, user = your Gmail address, password = an [App Password](https://myaccount.google.com/apppasswords) (needs 2-Step Verification). Outlook/Microsoft 365: `smtp.office365.com`, port `587`.
- **Slack channel ID:** right-click the channel → *View channel details* → the ID is at the bottom (starts with `C`). Invite your bot to the channel with `/invite @YourBot`.
- **Telegram chat ID:** create a bot with [@BotFather](https://t.me/BotFather), send it a message, then open `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` and copy `chat.id`.
- **Twilio:** Account SID + Auth Token from the Twilio Console home page. Phone numbers must use the `+15551234567` format.
- **Stripe:** Dashboard → Developers → API keys. A *restricted key* is safer. n8n creates the Stripe webhook for you when you activate.
- **Google APIs (Sheets, Calendar):** n8n Cloud has one-click Google sign-in. Self-hosted users follow [n8n's Google OAuth guide](https://docs.n8n.io/integrations/builtin/credentials/google/).

## Google Sheet tabs

| Tab | Used by workflows | Template |
|---|---|---|
| `Leads` | 02, 14, 16 | `sheet-templates/Leads.csv` |
| `Invoices` | 03, 21 | `sheet-templates/Invoices.csv` |
| `Jobs` | 04 | `sheet-templates/Jobs.csv` |
| `Appointments` | 05, 12 | `sheet-templates/Appointments.csv` |
| `Sales` | 09, 10, 16, 20 | `sheet-templates/Sales.csv` |
| `Feedback` | 11 | `sheet-templates/Feedback.csv` |
| `Quotes` | 13 | `sheet-templates/Quotes.csv` |
| `Customers` | 15 | `sheet-templates/Customers.csv` |
| `Clients` | 21 | `sheet-templates/Clients.csv` |
| `Support Log` | 22 | `sheet-templates/Support Log.csv` |
| `Inventory` | 23 | `sheet-templates/Inventory.csv` |

Import a template in Google Sheets with *File → Import → Upload → Insert new sheet(s)*, then rename the tab exactly as shown. **Column names must match exactly.** You can add extra columns anywhere. Write dates as `2026-11-20` (other common formats are understood too).

## Troubleshooting

| Problem | Fix |
|---|---|
| Red ⚠️ on a node after import | It just needs your credential. Open the node and pick one from the dropdown. |
| "Column not found" / nothing written to the sheet | Check the tab name and column headers match the template exactly, including capitals and spaces. |
| Webhook works in testing but not live | Test runs use the **Test URL**. Once activated, use the **Production URL** (shown in the Webhook/Form node). |
| Emails arrive at the wrong time | Set the timezone in **Config** *and* in *Workflow settings → Timezone*. |
| Gmail SMTP "invalid login" | Use an App Password, not your normal password. |
| Scheduled workflow didn't run | Make sure it's **Active**. Schedules don't run while a workflow is inactive. |
| Wait-based workflows (07, 20) | Waiting runs are stored by n8n and resume automatically. While testing, set the Wait nodes to 1 minute. |
| I don't use Slack / Telegram | Swap the node for any other notification node (Email, Teams, Discord, WhatsApp via Twilio…) or delete it. |

## Validation

Every workflow in this pack has been checked automatically:

- **Structure:** valid JSON, unique node names and IDs, every connection points to a real node, every node is reachable from its trigger.
- **Against n8n's own node definitions** (from the official `n8n-nodes-base` package): each node type and version exists, every parameter name is valid for that version, option values are allowed, and credential types match the node.
- **Logic tests:** the JavaScript in every Code node was run against sample data (overdue invoices, upcoming appointments, birthdays, low stock, uptime changes…), and all 495 `{{ expressions }}` were syntax-checked.
- **Real n8n import & run:** all 25 files import with n8n's own importer. The workflows that can run without real Google/Stripe/Twilio accounts (01, 02, 07, 11, 13, 18, 25) were run live against a local test email server, and each one sent the right emails or responses and stopped only at the placeholder logins.
- **Safety:** no real API keys or tokens. All credentials are placeholders.

Run the checks yourself (Python 3, no installs needed for the basic checks):

```bash
python3 scripts/validate.py
```

Run the logic tests for the Code nodes (Node.js 18+):

```bash
npm install luxon
node scripts/test-code-nodes.js
```

For the deep check against n8n's node definitions:

```bash
npm pack n8n-nodes-base && tar xzf n8n-nodes-base-*.tgz
python3 scripts/validate.py --nodes-json package/dist/types/nodes.json --creds-json package/dist/types/credentials.json
```

## License

See [LICENSE.md](LICENSE.md). In short: use these workflows in your own business and for your clients as much as you like. Please don't resell or redistribute the pack itself.
