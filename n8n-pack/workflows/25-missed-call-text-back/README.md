# 25 · Missed Call → Instant Text-Back

> When you can't pick up, the caller instantly gets a friendly text from your business number — so they message you instead of calling your competitor.

**File to import:** `25-missed-call-text-back.json`  
**Trigger:** Webhook  
**Difficulty:** ⭐ Easy · about 20 minutes

## What it does

- Your Twilio business number forwards calls to your mobile (rings for 20 seconds by default).
- If you answer, nothing else happens.
- If you miss it (no answer, busy, declined), the caller hears a short message and instantly receives an SMS from your business number.
- You get a Telegram notification with the caller's number.
- Gives callers who would otherwise hang up and try the next business a quick way to reach you.

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **Twilio (Account SID + Auth Token)** — used by: *Text the Caller Back*
- **Telegram Bot API (token from @BotFather)** — used by: *Tell You on Telegram*

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `25-missed-call-text-back.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. Buy a phone number in Twilio (or port your existing one). Add a **Twilio** credential in n8n and select it on *Text the Caller Back*.
3. Fill in **Config**: your mobile number (`forwardToPhone`), your Twilio number (`twilioFrom`), ring time and text message. Use `+countrycode` format.
4. Add a **Telegram** credential and chat ID (see workflow 09) — or delete the Telegram node.
5. **Activate** the workflow, open *Incoming Call (Twilio)* and copy its **Production URL**.
6. In Twilio Console → Phone Numbers → your number → *Voice Configuration*: set **A call comes in** → *Webhook*, paste the URL, method **HTTP POST**. Save.
7. That's it — the second webhook (*Call Ended*) is called by Twilio automatically (the TwiML uses a relative URL, so no extra setup).

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Test it

With the workflow active, call your Twilio number from another phone and don't answer on your mobile. Within seconds you should get the text.

## Customize it

- Change `ringSeconds` (15–25 works best before voicemail kicks in on your mobile).
- Want voicemail too? Replace the `<Say>` in *Play Sorry Message* with `<Say>Please leave a message.</Say><Record maxLength="120"/>`.
- In the US/Canada, register your number for A2P 10DLC in Twilio so texts deliver reliably.

## Nodes used

| Node | Type | Notes |
|---|---|---|
| Incoming Call (Twilio) | Webhook | Trigger |
| Call Ended (Twilio) | Webhook | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Is Call-Ended Callback? | If |  |
| Forward Call to Your Phone | Respond to Webhook |  |
| Missed? | If |  |
| Text the Caller Back | Twilio |  |
| Tell You on Telegram | Telegram |  |
| Play Sorry Message | Respond to Webhook |  |
| End Call (answered) | Respond to Webhook |  |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
