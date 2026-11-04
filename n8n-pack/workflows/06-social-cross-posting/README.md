# 06 · Social Media Cross-Posting

> Write a post once in a simple form and publish it to X, LinkedIn, your Facebook Page and your Telegram channel in one click.

**File to import:** `06-social-cross-posting.json`  
**Trigger:** n8n Form Trigger  
**Difficulty:** ⭐⭐ Moderate · about 30 minutes

## What it does

- Gives you a private posting form (bookmark it on your phone).
- You type the post, add an optional link, and tick where it should go.
- Automatically shortens the X version to fit 280 characters and adds your default hashtags.
- Publishes to every platform you ticked at the same time.

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **X (Twitter) OAuth2** — used by: *Post to X*
- **LinkedIn OAuth2** — used by: *Post to LinkedIn*
- **Facebook Graph API (Page access token)** — used by: *Post to Facebook Page*
- **Telegram Bot API (token from @BotFather)** — used by: *Post to Telegram Channel*
- _You only need credentials for the platforms you keep._

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `06-social-cross-posting.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. **X:** create an app at developer.x.com, add an *X OAuth2* credential in n8n and select it on *Post to X*.
3. **LinkedIn:** add a *LinkedIn OAuth2* credential, then open *Post to LinkedIn*, switch *Person* to *From list* and pick yourself — or paste your person ID into Config.
4. **Facebook:** add a *Facebook Graph API* credential using a **Page** access token (with `pages_manage_posts`), and put your Page ID in **Config → facebookPageId**.
5. **Telegram:** create a bot with @BotFather, add it as an admin of your channel, add a *Telegram* credential and set **Config → telegramChannel** (e.g. `@mychannel`).
6. Don't use a platform? Delete its two nodes ("... Selected?" and "Post to ...") and remove it from the form's *Post to* options.
7. Activate, then open the form's **Production URL** and bookmark it.

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Test it

Click **Test workflow**, open the form's *Test URL*, and post to one platform first (Telegram is the quickest to set up).

## Customize it

- Change default hashtags in **Config → hashtags** (leave empty for none).
- Want to log posts? Add a Google Sheets *Append* node after *Prepare Post*.
- Posting from a blog automatically? See workflow 17 (Blog RSS → Social).

## Nodes used

| Node | Type | Notes |
|---|---|---|
| New Post Form | n8n Form Trigger | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Prepare Post | Code (JavaScript) |  |
| X Selected? | Filter |  |
| LinkedIn Selected? | Filter |  |
| Facebook Selected? | Filter |  |
| Telegram Selected? | Filter |  |
| Post to X | X (Twitter) |  |
| Post to LinkedIn | LinkedIn |  |
| Post to Facebook Page | Facebook Graph API |  |
| Post to Telegram Channel | Telegram |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
