# 17 · Blog Post → Auto-Share to Social

> Publish a blog post and it's automatically shared to X, LinkedIn, your Facebook Page and Telegram within the hour — with the title, a short teaser and the link.

**File to import:** `17-blog-rss-to-social.json`  
**Trigger:** RSS Feed Trigger  
**Difficulty:** ⭐⭐ Moderate · about 30 minutes

## What it does

- Checks your blog's RSS feed every hour (WordPress, Ghost, Squarespace, Wix, Webflow, Substack, Shopify blogs all have one).
- For each new article, writes a platform-appropriate post (short for X, longer teaser for LinkedIn/Facebook/Telegram).
- Shares it everywhere at once, with link previews.
- Ignores old articles, so turning it on won't spam your followers with your archive.

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **X (Twitter) OAuth2** — used by: *Post to X*
- **LinkedIn OAuth2** — used by: *Post to LinkedIn*
- **Facebook Graph API (Page access token)** — used by: *Post to Facebook Page*
- **Telegram Bot API (token from @BotFather)** — used by: *Post to Telegram Channel*
- _You only need credentials for the platforms you keep._

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `17-blog-rss-to-social.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. Open **New Blog Post (RSS)** and paste your feed URL (usually `yoursite.com/feed`, `/rss` or `/blog/rss.xml`).
3. Set up credentials for the platforms you use (see workflow 06's README for X, LinkedIn, Facebook and Telegram instructions) and fill in **Config**.
4. Delete the "Post to ..." nodes for platforms you don't use.
5. Click **Activate**.

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Test it

Click **Test workflow** — n8n fetches the latest article from your feed so you can see the composed posts. (Disable the posting nodes first if you don't want a real post.)

## Customize it

- Change the intro text ("New on the blog:") in **Compose Posts**.
- Also works with YouTube channels (`https://www.youtube.com/feeds/videos.xml?channel_id=...`) and podcasts.

## Nodes used

| Node | Type | Notes |
|---|---|---|
| New Blog Post (RSS) | RSS Feed Trigger | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Compose Posts | Code (JavaScript) |  |
| Post to X | X (Twitter) |  |
| Post to LinkedIn | LinkedIn |  |
| Post to Facebook Page | Facebook Graph API |  |
| Post to Telegram Channel | Telegram |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
