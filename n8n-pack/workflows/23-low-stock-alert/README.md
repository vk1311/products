# 23 · Low Stock Alert

> Every morning, checks your inventory sheet and emails you a list of products that are low or out of stock — and can optionally email each supplier a ready-made reorder request.

**File to import:** `23-low-stock-alert.json`  
**Trigger:** Schedule Trigger  
**Difficulty:** ⭐ Easy · about 20 minutes

## What it does

- Runs at 7am and reads your **Inventory** sheet.
- Flags every product where *Quantity* is at or below its *Reorder Level* (🔴 out of stock, 🟠 low).
- Emails you one tidy digest with suggested order quantities and suppliers.
- Optional: emails each supplier a grouped purchase-order request (switched off by default — you stay in control).
- Won't nag: re-alerts every 3 days (configurable) until you restock.

## What you need

- An n8n account (n8n Cloud or self-hosted, version 1.x or newer).
- **Google Sheets OAuth2** — used by: *Get Inventory*, *Record Alert Date*
- **SMTP (any email provider: Gmail, Outlook, Zoho, your host...)** — used by: *Email Owner*, *Email Supplier (enable when ready)*
- A Google Sheet with the tab(s): **Inventory** (templates included as CSV files in this folder).

## Setup, step by step

1. **Import:** in n8n go to *Workflows → Create workflow → ⋯ (top right) → Import from File* and choose `23-low-stock-alert.json`. (Or open the file, copy everything, and paste it onto an empty canvas.)
2. Create a sheet tab named **Inventory** with the headers in `sheet-Inventory.csv`. Update *Quantity* as you sell/restock (or sync it from your POS export).
3. Fill in **Config** and pick your **Google Sheets** (2 nodes) and **SMTP** credentials.
4. Optional: enable *Email Supplier (enable when ready)* to send reorder requests automatically.
5. Click **Activate**.

> **Tip:** every value you need to change lives in the **Config** node (the first node after the trigger). Nodes with a red warning triangle just need you to pick your own credential from the dropdown.

## Google Sheet columns

Column names must match exactly (capital letters and spaces included). Extra columns are fine. Use dates like `2026-11-20`.

**Tab `Inventory`** — template: `sheet-Inventory.csv` (*File → Import → Upload* in Google Sheets, choose *Insert new sheet*, then rename the tab to `Inventory`)

| SKU | Product | Quantity | Reorder Level | Reorder Qty | Supplier | Supplier Email | Last Alert Date |
|---|---|---|---|---|---|---|---|
| MUG-BLU | Blue ceramic mug | 4 | 10 | 24 | Clayworks Co | orders@clayworks.example |  |

## Test it

Set a test product's *Quantity* below its *Reorder Level*, clear *Last Alert Date* and click **Test workflow**.

## Customize it

- Change the time or make it weekly in the trigger node.
- Prefer a phone alert? Add a Telegram node after *Build Owner Digest*.

## Nodes used

| Node | Type | Notes |
|---|---|---|
| Every Morning 7am | Schedule Trigger | Trigger |
| Config | Edit Fields (Set) | Your settings |
| Get Inventory | Google Sheets |  |
| Find Low Stock | Code (JavaScript) |  |
| Record Alert Date | Google Sheets |  |
| Build Owner Digest | Code (JavaScript) |  |
| Email Owner | Send Email (SMTP) |  |
| Group by Supplier | Code (JavaScript) |  |
| Email Supplier (enable when ready) | Send Email (SMTP) | Off by default (optional) |

All nodes are built-in n8n nodes — no community nodes to install. Credentials in the file are placeholders (`REPLACE_WITH_YOUR_CREDENTIAL`); no real keys are included.
