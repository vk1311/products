# Lead & Site-Health n8n Pack (3 workflows)

Three ready-to-import n8n workflows for agencies, freelancers and consultants who sell to small businesses.

| File | What it does | Credentials needed |
|---|---|---|
| 01-email-website-health-check.json | Checks a domain's SPF, DKIM, DMARC, MX, HTTPS, five security headers and subdomains in public certificate logs. Scores it out of 11. | None |
| 02-website-signal-score.json | Opens each website on your prospect list and scores it 0-100 on gaps: no booking or quote form, not mobile-ready, no HTTPS, stale copyright, DIY builder, no analytics, plus review demand. Every point is explained. | None |
| 03-public-tender-alerts.json | Downloads the Government of Canada (CanadaBuys) open tenders file, keeps the provinces you choose, matches tenders to each subscriber's trade keywords and sends one digest each. Remembers what was sent. | Your email node (Gmail, Outlook, SMTP or Resend) |

## Import
n8n > Workflows > Add workflow > ... menu > Import from file. Each workflow has a yellow "How to use" note.

## Notes
- Built and tested on n8n 1.x (Code node v2). Uses only built-in nodes.
- The tender workflow uses CanadaBuys open data (Open Government Licence - Canada). Confirm every deadline on the official notice.
- Commercial email in Canada is covered by CASL: send alerts only to people who signed up, with your mailing address and an unsubscribe.
- The signal score is for prioritising who to talk to. It reads public homepages once per run with a polite pause.

Made by Waypoint Software, Kentville, Nova Scotia. hello@waypointns.ca
