"""Templates 01-10."""

import datetime as dt
import random

from openpyxl.chart import BarChart, LineChart, Reference

from .common import (AS_OF_NOTE, FILL_AMBER, FILL_GREEN, FILL_RED, FILL_SECTION, FILL_TOTAL,
                     YEAR, Col, F_SUB, add_list, add_table, calc, d, finalize, flag_rule, header,
                     inp, instructions, label, lists_sheet, new_workbook, qs, ref, section,
                     settings_block, title, widths)
from openpyxl.utils import get_column_letter as GL

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


# =============================================================== 01 Budget
def budget(path):
    wb = new_workbook()
    instructions(
        wb, "Monthly Budget (Budget vs Actual)",
        "Plan income and expenses by month, record actuals, and see variances automatically.",
        ["On the Budget tab, list your categories in column A and mark each as Income or Expense.",
         "Type your planned amount for each month (yellow cells).",
         "On the Actual tab, type what really happened each month - categories copy across automatically.",
         "Open the Summary tab to see annual and monthly variances (positive = better than plan)."],
        [("Budget", "Planned amounts by category and month."),
         ("Actual", "Actual amounts. Category names and types are pulled from the Budget tab."),
         ("Summary", "Budget vs actual by category and by month, with variance and % of budget.")],
        ["Variance is shown so that a positive number is always good: more income than planned, "
         "or less spending than planned."])

    rng = random.Random(1)
    income = [("Product sales", 12000), ("Service income", 3000)]
    expense = [("Rent", 2500), ("Wages", 6000), ("Utilities", 400), ("Insurance", 250),
               ("Marketing", 800), ("Software & subscriptions", 200), ("Phone & internet", 150),
               ("Vehicle & fuel", 600), ("Supplies", 300), ("Accounting & legal", 250),
               ("Bank fees", 50), ("Meals & entertainment", 150), ("Miscellaneous", 100)]
    cats = [(n, "Income", v) for n, v in income] + [(n, "Expense", v) for n, v in expense]
    N = 30
    first, last = 5, 5 + N - 1
    actual_vals = {}

    def grid(ws, is_actual):
        title(ws, "Actual" if is_actual else "Budget",
              f"Fiscal year {YEAR} - amounts in dollars")
        header(ws, 4, 1, ["Category", "Type"] + MONTHS + ["Annual Total"])
        widths(ws, {"A": 26, "B": 10, "O": 14})
        for c in range(3, 15):
            ws.column_dimensions[GL(c)].width = 10
        for i in range(N):
            r = first + i
            if is_actual:
                calc(ws, f"A{r}", f'IF(Budget!A{r}="","",Budget!A{r})')
                calc(ws, f"B{r}", f'IF(Budget!B{r}="","",Budget!B{r})')
                ws[f"A{r}"].font = ws[f"A{r}"].font.copy(color="008000")
            else:
                inp(ws, f"A{r}", cats[i][0] if i < len(cats) else None)
                inp(ws, f"B{r}", cats[i][1] if i < len(cats) else None)
            for m in range(12):
                L = GL(3 + m)
                v = None
                if i < len(cats):
                    base = cats[i][2]
                    if is_actual:
                        v = round(base * rng.uniform(0.85, 1.15)) if m < 9 else None
                        actual_vals[(i, m)] = v or 0
                    else:
                        v = base
                inp(ws, f"{L}{r}", v, "money0")
            calc(ws, f"O{r}", f'IF(A{r}="","",SUM(C{r}:N{r}))', "money0", bold=True)
        if not is_actual:
            add_list(ws, f"B{first}:B{last}", "Income,Expense")
        tr = last + 2
        for k, (lab, f) in enumerate([("Total Income", 'SUMIF($B${f}:$B${l},"Income",{L}${f}:{L}${l})'),
                                      ("Total Expenses", 'SUMIF($B${f}:$B${l},"Expense",{L}${f}:{L}${l})'),
                                      ("Net (Income - Expenses)", "{L}{r1}-{L}{r2}")]):
            r = tr + k
            label(ws, f"A{r}", lab, bold=True, fill=FILL_TOTAL)
            ws[f"B{r}"].fill = FILL_TOTAL
            for c in range(3, 16):
                L = GL(c)
                calc(ws, f"{L}{r}", f.format(f=first, l=last, L=L, r1=tr, r2=tr + 1), "money0",
                     bold=True, fill=FILL_TOTAL)
        ws.freeze_panes = "C5"
        return tr

    wsb = wb.create_sheet("Budget")
    tr = grid(wsb, False)
    wsa = wb.create_sheet("Actual")
    grid(wsa, True)

    ws = wb.create_sheet("Summary")
    title(ws, "Budget vs Actual Summary", "Positive variance = better than plan")
    header(ws, 4, 1, ["Category", "Type", "Annual Budget", "Actual to Date", "Variance", "% of Budget"])
    widths(ws, {"A": 26, "B": 10, "C": 15, "D": 15, "E": 15, "F": 12})
    for i in range(N):
        r = 5 + i
        calc(ws, f"A{r}", f'IF(Budget!A{r}="","",Budget!A{r})')
        calc(ws, f"B{r}", f'IF(Budget!B{r}="","",Budget!B{r})')
        calc(ws, f"C{r}", f'IF(A{r}="","",Budget!O{r})', "money0")
        calc(ws, f"D{r}", f'IF(A{r}="","",Actual!O{r})', "money0")
        calc(ws, f"E{r}", f'IF(A{r}="","",IF(B{r}="Income",D{r}-C{r},C{r}-D{r}))', "money0")
        calc(ws, f"F{r}", f'IF(A{r}="","",IFERROR(D{r}/C{r},0))', "pct")
    flag_rule(ws, f"E5:E{4 + N}", "AND(ISNUMBER(E5),E5<0)")
    r0 = 6 + N
    section(ws, f"A{r0}", "By month")
    header(ws, r0 + 1, 1, ["Month", "Budget Net", "Actual Net", "Variance"])
    for m in range(12):
        r = r0 + 2 + m
        L = GL(3 + m)
        label(ws, f"A{r}", MONTHS[m])
        calc(ws, f"B{r}", f"Budget!{L}{tr + 2}", "money0")
        calc(ws, f"C{r}", f"Actual!{L}{tr + 2}", "money0")
        calc(ws, f"D{r}", f"C{r}-B{r}", "money0")
    rt = r0 + 14
    label(ws, f"A{rt}", "Year", bold=True, fill=FILL_TOTAL)
    for L in "BCD":
        calc(ws, f"{L}{rt}", f"SUM({L}{r0 + 2}:{L}{r0 + 13})", "money0", bold=True, fill=FILL_TOTAL)
    finalize(wb, path)

    budget_exp = sum(v for _, t, v in cats if t == "Expense") * 12
    act_net = sum(actual_vals[(i, m)] * (1 if cats[i][1] == "Income" else -1)
                  for i in range(len(cats)) for m in range(12))
    return [("Budget", f"O{tr + 1}", budget_exp), ("Summary", f"C{rt}", act_net),
            ("Actual", f"O{tr + 2}", act_net)]


# =========================================================== 02 Cash flow
def cash_flow(path):
    wb = new_workbook()
    instructions(
        wb, "12-Month Cash Flow Forecast",
        "Project cash coming in and going out each month and spot shortfalls before they happen.",
        ["On the Cash Flow tab, enter your opening bank balance, the first month, and a minimum cash cushion.",
         "Type expected cash in and cash out for each month (yellow cells). Rename line items as needed.",
         "Closing balance rolls forward automatically into the next month's opening balance.",
         "Months where cash falls below your cushion are flagged LOW in red."],
        [("Cash Flow", "Monthly forecast with totals, running balance, low-cash warning and chart.")],
        ["Record cash when it actually moves (when a customer pays, not when you invoice)."])
    ws = wb.create_sheet("Cash Flow")
    title(ws, "12-Month Cash Flow Forecast", "Amounts in dollars")
    s = settings_block(ws, 3, [("Opening bank balance", 15000, "money0", None),
                               ("First month", d(YEAR, 1, 1), "month", "Any date in the first month"),
                               ("Minimum cash cushion", 5000, "money0", "Months below this are flagged")])
    widths(ws, {"A": 30, "O": 14})
    for c in range(2, 14):
        ws.column_dimensions[GL(c)].width = 11
    hr = 7
    header(ws, hr, 1, ["Line item"] + [""] * 12 + ["12-Month Total"])
    for m in range(12):
        calc(ws, f"{GL(2 + m)}{hr}", f"EDATE(DATE(YEAR($B$4),MONTH($B$4),1),{m})", "mon",
             fill=None, align="center")
        ws[f"{GL(2 + m)}{hr}"].font = ws["A7"].font.copy()
        ws[f"{GL(2 + m)}{hr}"].fill = ws["A7"].fill.copy()
    ins = [("Cash sales", [9000, 8500, 10000, 11000, 12500, 13000, 12000, 11500, 12500, 11000, 10500, 14000]),
           ("Collections from customers (A/R)", [6000] * 12),
           ("Loans / owner investment", [0, 0, 10000] + [0] * 9),
           ("Other income", [200] * 12)]
    outs = [("Inventory / materials", [5000, 4800, 5500, 6000, 6800, 7000, 6500, 6200, 6800, 6000, 5800, 7500]),
            ("Wages & payroll remittances", [7000] * 12),
            ("Rent", [2500] * 12),
            ("Utilities & phone", [550] * 12),
            ("Marketing", [800] * 12),
            ("Insurance", [250] * 12),
            ("Loan payments", [600] * 12),
            ("HST remittance", [0, 0, 0, 3200, 0, 0, 3800, 0, 0, 3600, 0, 0]),
            ("Equipment purchases", [0, 0, 8000] + [0] * 9),
            ("Owner draws", [1500] * 12),
            ("Other expenses", [300] * 12)]
    r = hr + 1
    label(ws, f"A{r}", "Opening balance", bold=True)
    open_r = r
    r += 1
    section(ws, f"A{r}", "Cash in")
    r += 1
    in_first = r
    for name, vals in ins + [("", [None] * 12)] * 2:
        inp(ws, f"A{r}", name or None)
        for m in range(12):
            inp(ws, f"{GL(2 + m)}{r}", vals[m], "money0")
        calc(ws, f"N{r}", f"SUM(B{r}:M{r})", "money0")
        r += 1
    in_last = r - 1
    label(ws, f"A{r}", "Total cash in", bold=True, fill=FILL_TOTAL)
    tin = r
    r += 2
    section(ws, f"A{r}", "Cash out")
    r += 1
    out_first = r
    for name, vals in outs + [("", [None] * 12)] * 3:
        inp(ws, f"A{r}", name or None)
        for m in range(12):
            inp(ws, f"{GL(2 + m)}{r}", vals[m], "money0")
        calc(ws, f"N{r}", f"SUM(B{r}:M{r})", "money0")
        r += 1
    out_last = r - 1
    label(ws, f"A{r}", "Total cash out", bold=True, fill=FILL_TOTAL)
    tout = r
    r += 2
    net_r, close_r, flag_r = r, r + 1, r + 2
    label(ws, f"A{net_r}", "Net cash flow", bold=True)
    label(ws, f"A{close_r}", "Closing balance", bold=True, fill=FILL_TOTAL)
    label(ws, f"A{flag_r}", "Cash check", bold=True)
    for m in range(13):
        L = GL(2 + m)
        if m < 12:
            calc(ws, f"{L}{open_r}", "$B$3" if m == 0 else f"{GL(1 + m)}{close_r}", "money0")
            calc(ws, f"{L}{close_r}", f"{L}{open_r}+{L}{net_r}", "money0", bold=True, fill=FILL_TOTAL)
            calc(ws, f"{L}{flag_r}", f'IF({L}{close_r}<$B$5,"LOW","OK")', align="center")
        else:
            calc(ws, f"{L}{open_r}", "B{0}".format(open_r), "money0")
            calc(ws, f"{L}{close_r}", f"M{close_r}", "money0", bold=True, fill=FILL_TOTAL)
        calc(ws, f"{L}{tin}", f"SUM({L}{in_first}:{L}{in_last})", "money0", bold=True, fill=FILL_TOTAL)
        calc(ws, f"{L}{tout}", f"SUM({L}{out_first}:{L}{out_last})", "money0", bold=True, fill=FILL_TOTAL)
        calc(ws, f"{L}{net_r}", f"{L}{tin}-{L}{tout}", "money0", bold=True)
    flag_rule(ws, f"B{flag_r}:M{flag_r}", f'B{flag_r}="LOW"', bold=True)
    flag_rule(ws, f"B{close_r}:M{close_r}", f"B{close_r}<$B$5")
    ws.freeze_panes = f"B{hr + 1}"

    ch = LineChart()
    ch.title = "Closing cash balance"
    ch.height, ch.width = 7, 18
    ch.add_data(Reference(ws, min_col=1, max_col=13, min_row=close_r), titles_from_data=True, from_rows=True)
    ch.set_categories(Reference(ws, min_col=2, max_col=13, min_row=hr))
    ch.y_axis.numFmt = "$#,##0"
    ws.add_chart(ch, f"B{flag_r + 2}")
    finalize(wb, path)

    total_in = sum(sum(v) for _, v in ins)
    total_out = sum(sum(v) for _, v in outs)
    return [("Cash Flow", f"M{close_r}", 15000 + total_in - total_out),
            ("Cash Flow", f"N{tin}", total_in)]


# ======================================================= 03 Invoice tracker
def _settings(wb, items, name="Settings"):
    ws = wb.create_sheet(name)
    title(ws, name, "Change the yellow cells - every tab uses these values")
    widths(ws, {"A": 28, "B": 18, "C": 60})
    return ws, settings_block(ws, 4, items)


def invoice_tracker(path):
    wb = new_workbook()
    instructions(
        wb, "Invoice Tracker (Accounts Receivable)",
        "Log every invoice you send, track payments, and see who owes you what and how overdue it is.",
        ["On Settings, enter your HST rate (13% Ontario by default).",
         "On Invoices, add one row per invoice: number, client, date, terms, subtotal and whether HST applies.",
         "When a client pays, enter the amount and date paid. Balance and status update automatically.",
         "The Summary tab shows totals, an aging report (current / 1-30 / 31-60 / 61-90 / 90+ days) "
         "and balances by client."],
        [("Settings", "HST rate and as-of date."),
         ("Invoices", "One row per invoice. Due date, HST, total, balance, status and days overdue are calculated."),
         ("Summary", "Totals, aging buckets and a by-client table (type client names in the yellow cells)."),
         ("Lists", "Drop-down choices (payment terms).")],
        [AS_OF_NOTE, "Partial payments are supported - enter the total received to date."])
    st, s = _settings(wb, [("HST rate", 0.13, "pct", "13% = Ontario. Use 0.05 for GST-only provinces."),
                           ("As-of date", "=TODAY()", "date", "Overwrite with a date to freeze the report.")])
    lw, lists = lists_sheet(wb, {"Terms (days)": [0, 15, 30, 45, 60]})
    ws = wb.create_sheet("Invoices", 2)
    title(ws, "Invoices", "Yellow = type here. Grey = calculated.")
    rate, asof = s["HST rate"], s["As-of date"]
    cols = [
        Col("Invoice #", 11), Col("Client", 24), Col("Invoice Date", 12, fmt="date"),
        Col("Terms (days)", 9, dv=lists["Terms (days)"], default=30), Col("Description", 26),
        Col("Subtotal", 12, fmt="money", total="sum"),
        Col("HST? (Y/N)", 8, dv="Y,N", default="Y", align="center"),
        Col("HST", 11, f=f'IF([HST? (Y/N)]="Y",ROUND([Subtotal]*{rate},2),0)', fmt="money", total="sum"),
        Col("Total", 12, f="[Subtotal]+[HST]", fmt="money", total="sum"),
        Col("Due Date", 12, f="[Invoice Date]+[Terms (days)]", fmt="date"),
        Col("Amount Paid", 12, fmt="money", total="sum"),
        Col("Date Paid", 12, fmt="date"),
        Col("Balance", 12, f="[Total]-[Amount Paid]", fmt="money", total="sum"),
        Col("Status", 10, f=f'IF([Balance]<=0,"Paid",IF({asof}>[Due Date],"Overdue","Open"))', align="center"),
        Col("Days Overdue", 9, f=f"IF(AND([Balance]>0,{asof}>[Due Date]),{asof}-[Due Date],0)", fmt="int"),
    ]
    clients = ["Maple Ridge Dental", "Northshore Builders", "Bayview Cafe", "Trillium Property Mgmt",
               "Lakeside Yoga Studio"]
    samples = []
    base = d(YEAR, 6, 2)
    exp_total = exp_bal = 0
    for i in range(14):
        sub = [1250, 3400, 680, 2200, 975, 5400, 1500, 820, 2650, 430, 3100, 1890, 760, 4200][i]
        tax = "N" if i == 9 else "Y"
        paid_full = i % 3 != 2
        total = round(sub + (round(sub * 0.13, 2) if tax == "Y" else 0), 2)
        idate = base + dt.timedelta(days=11 * i)
        paid = total if (paid_full and i < 10) else (500 if i == 11 else None)
        samples.append({"Invoice #": f"INV-{1001 + i}", "Client": clients[i % 5], "Invoice Date": idate,
                        "Terms (days)": 30, "Description": "Services rendered", "Subtotal": sub,
                        "HST? (Y/N)": tax, "Amount Paid": paid,
                        "Date Paid": idate + dt.timedelta(days=25) if paid else None})
        exp_total += total
        exp_bal += total - (paid or 0)
    t = add_table(ws, cols, samples, n=200)
    flag_rule(ws, f"N{t.first}:N{t.last}", f'N{t.first}="Overdue"', bold=True)
    flag_rule(ws, f"N{t.first}:N{t.last}", f'N{t.first}="Paid"', fill=FILL_GREEN)

    sm = wb.create_sheet("Summary", 3)
    title(sm, "Receivables Summary", "All figures update from the Invoices tab")
    widths(sm, {"A": 30, "B": 16, "C": 16, "D": 16})
    rows = [("Invoices issued", f'COUNTIF({t.rng("Invoice #")},"?*")', "int"),
            ("Total invoiced", f"SUM({t.rng('Total')})", "money"),
            ("Total collected", f"SUM({t.rng('Amount Paid')})", "money"),
            ("Outstanding balance", f"SUM({t.rng('Balance')})", "money"),
            ("Overdue balance", f'SUMIFS({t.rng("Balance")},{t.rng("Status")},"Overdue")', "money"),
            ("Average days overdue (overdue only)",
             f'IFERROR(AVERAGEIFS({t.rng("Days Overdue")},{t.rng("Status")},"Overdue"),0)', "num1")]
    for i, (lab, f, fm) in enumerate(rows):
        label(sm, f"A{4 + i}", lab, bold=True)
        calc(sm, f"B{4 + i}", f, fm)
    section(sm, "A11", "Aging (unpaid balances)")
    header(sm, 12, 1, ["Bucket", "Balance", "% of total"])
    buckets = [("Current (not yet due)", f'SUMIFS({t.rng("Balance")},{t.rng("Days Overdue")},0)'),
               ("1-30 days", f'SUMIFS({t.rng("Balance")},{t.rng("Days Overdue")},">=1",{t.rng("Days Overdue")},"<=30")'),
               ("31-60 days", f'SUMIFS({t.rng("Balance")},{t.rng("Days Overdue")},">=31",{t.rng("Days Overdue")},"<=60")'),
               ("61-90 days", f'SUMIFS({t.rng("Balance")},{t.rng("Days Overdue")},">=61",{t.rng("Days Overdue")},"<=90")'),
               ("Over 90 days", f'SUMIFS({t.rng("Balance")},{t.rng("Days Overdue")},">90")')]
    for i, (lab, f) in enumerate(buckets):
        r = 13 + i
        label(sm, f"A{r}", lab)
        calc(sm, f"B{r}", f, "money")
        calc(sm, f"C{r}", f"IFERROR(B{r}/$B$18,0)", "pct")
    label(sm, "A18", "Total", bold=True, fill=FILL_TOTAL)
    calc(sm, "B18", "SUM(B13:B17)", "money", bold=True, fill=FILL_TOTAL)
    calc(sm, "C18", "SUM(C13:C17)", "pct", bold=True, fill=FILL_TOTAL)
    section(sm, "A20", "By client (type client names)")
    header(sm, 21, 1, ["Client", "Invoiced", "Collected", "Balance"])
    for i in range(15):
        r = 22 + i
        inp(sm, f"A{r}", clients[i] if i < 5 else None)
        calc(sm, f"B{r}", f'IF(A{r}="","",SUMIFS({t.rng("Total")},{t.rng("Client")},A{r}))', "money")
        calc(sm, f"C{r}", f'IF(A{r}="","",SUMIFS({t.rng("Amount Paid")},{t.rng("Client")},A{r}))', "money")
        calc(sm, f"D{r}", f'IF(A{r}="","",SUMIFS({t.rng("Balance")},{t.rng("Client")},A{r}))', "money")
    finalize(wb, path)
    return [("Summary", "B5", round(exp_total, 2)), ("Summary", "B7", round(exp_bal, 2)),
            ("Summary", "B18", ("=", "Summary", "B7")), ("Summary", "B4", 14)]


# ========================================================= 04 Quote tracker
def quote_tracker(path):
    wb = new_workbook()
    instructions(
        wb, "Quote & Estimate Tracker",
        "Track every quote you send, never miss a follow-up, and measure your win rate.",
        ["Add one row per quote on the Quotes tab: number, date, client, salesperson and amount.",
         "Set a follow-up date. Quotes still Draft/Sent on or after that date show FOLLOW UP.",
         "Change Status to Won, Lost or Expired when you hear back and enter the decision date.",
         "The Summary tab shows quote value by status, win rate and results by salesperson."],
        [("Settings", "As-of date."), ("Quotes", "One row per quote."),
         ("Summary", "Pipeline by status, win rate, results by salesperson."),
         ("Lists", "Status and salesperson drop-downs.")],
        [AS_OF_NOTE, "Win rate = won / (won + lost). Draft, Sent and Expired quotes are excluded."])
    st, s = _settings(wb, [("As-of date", "=TODAY()", "date", "Overwrite with a date to freeze the report.")])
    asof = s["As-of date"]
    reps = ["Alex", "Jordan", "Sam"]
    statuses = ["Draft", "Sent", "Won", "Lost", "Expired"]
    lw, lists = lists_sheet(wb, {"Status": statuses, "Salesperson": reps})
    ws = wb.create_sheet("Quotes", 2)
    title(ws, "Quotes", "Yellow = type here. Grey = calculated.")
    cols = [Col("Quote #", 10), Col("Quote Date", 12, fmt="date"), Col("Client", 24),
            Col("Description", 26), Col("Salesperson", 12, dv=lists["Salesperson"]),
            Col("Amount (pre-tax)", 13, fmt="money", total="sum"),
            Col("Status", 10, dv=lists["Status"], default="Sent"),
            Col("Follow-up Date", 12, fmt="date"), Col("Decision Date", 12, fmt="date"),
            Col("Days Open", 9, f=f'IF(OR([Status]="Won",[Status]="Lost"),IF([Decision Date]="","",[Decision Date]-[Quote Date]),{asof}-[Quote Date])', fmt="int"),
            Col("Won Amount", 12, f='IF([Status]="Won",[Amount (pre-tax)],0)', fmt="money", total="sum"),
            Col("Action", 12, f=f'IF(AND(OR([Status]="Draft",[Status]="Sent"),[Follow-up Date]<>"",[Follow-up Date]<={asof}),"FOLLOW UP","")', align="center")]
    amounts = [4500, 12800, 2300, 7600, 15400, 980, 6200, 3300, 21000, 5100, 8800, 1750]
    stats = ["Won", "Lost", "Won", "Sent", "Won", "Lost", "Sent", "Expired", "Won", "Draft", "Lost", "Sent"]
    samples = []
    for i in range(12):
        qd = d(YEAR, 5, 4) + dt.timedelta(days=12 * i)
        samples.append({"Quote #": f"Q-{2001 + i}", "Quote Date": qd, "Client": f"Client {chr(65 + i)} Ltd.",
                        "Description": "Renovation estimate", "Salesperson": reps[i % 3],
                        "Amount (pre-tax)": amounts[i], "Status": stats[i],
                        "Follow-up Date": qd + dt.timedelta(days=7),
                        "Decision Date": qd + dt.timedelta(days=18) if stats[i] in ("Won", "Lost") else None})
    t = add_table(ws, cols, samples, n=200)
    flag_rule(ws, f"L{t.first}:L{t.last}", f'L{t.first}="FOLLOW UP"', fill=FILL_AMBER, bold=True)

    sm = wb.create_sheet("Summary", 3)
    title(sm, "Quote Summary")
    widths(sm, {"A": 26, "B": 12, "C": 16, "D": 14, "E": 14})
    header(sm, 4, 1, ["Status", "# Quotes", "Value"])
    for i, stt in enumerate(statuses):
        r = 5 + i
        calc(sm, f"A{r}", f"Lists!A{3 + i}")
        calc(sm, f"B{r}", f'IF(A{r}="","",COUNTIFS({t.rng("Status")},A{r}))', "int")
        calc(sm, f"C{r}", f'IF(A{r}="","",SUMIFS({t.rng("Amount (pre-tax)")},{t.rng("Status")},A{r}))', "money")
    label(sm, "A10", "Total", bold=True, fill=FILL_TOTAL)
    calc(sm, "B10", "SUM(B5:B9)", "int", bold=True, fill=FILL_TOTAL)
    calc(sm, "C10", "SUM(C5:C9)", "money", bold=True, fill=FILL_TOTAL)
    kp = [("Win rate (by count)", 'IFERROR(COUNTIFS({S},"Won")/(COUNTIFS({S},"Won")+COUNTIFS({S},"Lost")),0)', "pct"),
          ("Win rate (by value)", 'IFERROR(SUMIFS({A},{S},"Won")/(SUMIFS({A},{S},"Won")+SUMIFS({A},{S},"Lost")),0)', "pct"),
          ("Average quote value", "IFERROR(AVERAGE({A}),0)", "money"),
          ("Open pipeline (Draft + Sent)", 'SUMIFS({A},{S},"Draft")+SUMIFS({A},{S},"Sent")', "money"),
          ("Follow-ups due", 'COUNTIF({F},"FOLLOW UP")', "int")]
    for i, (lab, f, fm) in enumerate(kp):
        label(sm, f"A{12 + i}", lab, bold=True)
        calc(sm, f"B{12 + i}", f.format(S=t.rng("Status"), A=t.rng("Amount (pre-tax)"), F=t.rng("Action")), fm)
    section(sm, "A18", "By salesperson")
    header(sm, 19, 1, ["Salesperson", "# Quotes", "Quoted", "Won", "Win rate"])
    for i in range(8):
        r = 20 + i
        calc(sm, f"A{r}", f'IF(Lists!C{3 + i}="","",Lists!C{3 + i})')
        calc(sm, f"B{r}", f'IF(A{r}="","",COUNTIFS({t.rng("Salesperson")},A{r}))', "int")
        calc(sm, f"C{r}", f'IF(A{r}="","",SUMIFS({t.rng("Amount (pre-tax)")},{t.rng("Salesperson")},A{r}))', "money")
        calc(sm, f"D{r}", f'IF(A{r}="","",SUMIFS({t.rng("Won Amount")},{t.rng("Salesperson")},A{r}))', "money")
        calc(sm, f"E{r}", f'IF(A{r}="","",IFERROR(COUNTIFS({t.rng("Salesperson")},A{r},{t.rng("Status")},"Won")/(COUNTIFS({t.rng("Salesperson")},A{r},{t.rng("Status")},"Won")+COUNTIFS({t.rng("Salesperson")},A{r},{t.rng("Status")},"Lost")),0))', "pct")
    finalize(wb, path)
    won = sum(a for a, s_ in zip(amounts, stats) if s_ == "Won")
    lost = sum(1 for s_ in stats if s_ == "Lost")
    nwon = stats.count("Won")
    return [("Summary", "C7", won), ("Summary", "B12", nwon / (nwon + lost)),
            ("Quotes", "K4", won), ("Summary", "B10", 12)]


# =========================================================== 05 Job costing
def job_costing(path):
    wb = new_workbook()
    instructions(
        wb, "Job Costing",
        "Compare estimated vs actual costs for every job and see profit and margin per job.",
        ["On the Jobs tab, add each job with its contract price and estimated labour, materials and other costs.",
         "Log every cost on the Costs tab as it happens: date, job #, cost type, quantity/hours and rate.",
         "Actual costs roll up to the Jobs tab automatically by job # and cost type.",
         "Watch '% of Estimate Used' and 'Margin' - red means the job is over budget or losing money."],
        [("Jobs", "One row per job: estimate vs actual, profit and margin."),
         ("Costs", "Cost log. Amount = quantity x rate."),
         ("Lists", "Cost types and job statuses.")],
        ["Labour and Materials roll up separately; all other cost types roll up into 'Actual Other'.",
         "Job # on the Costs tab must match the Jobs tab exactly."])
    lw, lists = lists_sheet(wb, {"Cost Type": ["Labour", "Materials", "Subcontract", "Equipment", "Other"],
                                 "Job Status": ["Quoted", "In progress", "Complete", "On hold"]})
    wc = wb.create_sheet("Costs", 1)
    title(wc, "Job Cost Log", "One row per cost. Amount = Qty/Hours x Rate.")
    ccols = [Col("Date", 12, fmt="date"), Col("Job #", 10), Col("Cost Type", 13, dv=lists["Cost Type"]),
             Col("Description", 30), Col("Qty / Hours", 10, fmt="num2"), Col("Unit Cost / Rate", 12, fmt="money"),
             Col("Amount", 13, f="[Qty / Hours]*[Unit Cost / Rate]", fmt="money", total="sum")]
    costs = [
        ("J-101", "Labour", "Framing crew", 64, 45), ("J-101", "Materials", "Lumber package", 1, 6800),
        ("J-101", "Subcontract", "Electrical rough-in", 1, 3200), ("J-101", "Labour", "Finishing", 40, 45),
        ("J-102", "Labour", "Demo & prep", 24, 42), ("J-102", "Materials", "Tile & grout", 1, 2150),
        ("J-102", "Equipment", "Bin rental", 1, 450), ("J-102", "Labour", "Tile install", 36, 48),
        ("J-103", "Labour", "Deck build", 50, 45), ("J-103", "Materials", "Pressure-treated lumber", 1, 4300),
        ("J-103", "Other", "Permit", 1, 275), ("J-104", "Labour", "Site visit", 4, 45),
    ]
    samples = [{"Date": d(YEAR, 7, 1) + dt.timedelta(days=3 * i), "Job #": j, "Cost Type": ct,
                "Description": desc, "Qty / Hours": q, "Unit Cost / Rate": rt}
               for i, (j, ct, desc, q, rt) in enumerate(costs)]
    tc = add_table(wc, ccols, samples, n=300, key="Job #")

    wj = wb.create_sheet("Jobs", 1)
    title(wj, "Jobs - Estimate vs Actual", "Actuals pull from the Costs tab by Job #.")
    A, J, T = tc.rng("Amount"), tc.rng("Job #"), tc.rng("Cost Type")
    jcols = [Col("Job #", 9), Col("Client", 20), Col("Description", 22), Col("Start Date", 11, fmt="date"),
             Col("Status", 11, dv=lists["Job Status"], default="In progress"),
             Col("Contract Price", 12, fmt="money", total="sum"),
             Col("Est. Labour", 11, fmt="money", total="sum"), Col("Est. Materials", 11, fmt="money", total="sum"),
             Col("Est. Other", 11, fmt="money", total="sum"),
             Col("Est. Total", 12, f="[Est. Labour]+[Est. Materials]+[Est. Other]", fmt="money", total="sum"),
             Col("Actual Labour", 11, f=f'SUMIFS({A},{J},[Job #],{T},"Labour")', fmt="money", total="sum"),
             Col("Actual Materials", 11, f=f'SUMIFS({A},{J},[Job #],{T},"Materials")', fmt="money", total="sum"),
             Col("Actual Other", 11, f=f"SUMIFS({A},{J},[Job #])-[Actual Labour]-[Actual Materials]", fmt="money", total="sum"),
             Col("Actual Total", 12, f="[Actual Labour]+[Actual Materials]+[Actual Other]", fmt="money", total="sum"),
             Col("Variance (Est - Act)", 12, f="[Est. Total]-[Actual Total]", fmt="money", total="sum"),
             Col("% of Estimate Used", 10, f="IFERROR([Actual Total]/[Est. Total],0)", fmt="pct"),
             Col("Profit", 12, f="[Contract Price]-[Actual Total]", fmt="money", total="sum"),
             Col("Margin", 9, f="IFERROR([Profit]/[Contract Price],0)", fmt="pct")]
    jobs = [("J-101", "Hendricks Family", "Garage addition", 22000, 5000, 7000, 3000),
            ("J-102", "Bayview Cafe", "Washroom reno", 9500, 3000, 2000, 500),
            ("J-103", "R. Patel", "Backyard deck", 11800, 2400, 4500, 300),
            ("J-104", "Northshore Builders", "Basement finish", 28000, 8000, 9000, 4000)]
    js = [{"Job #": j, "Client": c, "Description": de, "Start Date": d(YEAR, 7, 1) + dt.timedelta(days=7 * i),
           "Status": "Complete" if i < 2 else "In progress", "Contract Price": p, "Est. Labour": el,
           "Est. Materials": em, "Est. Other": eo} for i, (j, c, de, p, el, em, eo) in enumerate(jobs)]
    tj = add_table(wj, jcols, js, n=100)
    flag_rule(wj, f"P{tj.first}:P{tj.last}", f"AND(ISNUMBER(P{tj.first}),P{tj.first}>1)")
    flag_rule(wj, f"R{tj.first}:R{tj.last}", f"AND(ISNUMBER(R{tj.first}),R{tj.first}<0)")
    finalize(wb, path)
    act101 = sum(q * r for j, _, _, q, r in costs if j == "J-101")
    tot = sum(q * r for *_, q, r in costs)
    return [("Jobs", tj.cell("Profit", 0), 22000 - act101), ("Jobs", tj.total("Actual Total"), tot),
            ("Costs", tc.total("Amount"), tot)]


# ========================================================== 06 Payroll hours
def payroll_hours(path):
    wb = new_workbook()
    instructions(
        wb, "Payroll Hours & Timesheet",
        "Record clock-in/clock-out times and get weekly hours, overtime and gross pay per employee.",
        ["On Settings, set the week start date, the weekly overtime threshold (44 hrs in Ontario) and OT multiplier.",
         "List employees and hourly rates on the Timesheet tab (yellow cells).",
         "Log each shift on the Punches tab: date, employee, time in, time out and unpaid break minutes.",
         "The Timesheet tab totals hours per day, splits regular vs overtime and calculates gross pay."],
        [("Settings", "Week start, overtime rules."),
         ("Timesheet", "Weekly hours by day, regular/OT split and gross pay."),
         ("Punches", "Clock in/out log. Overnight shifts are handled."),],
        ["Overtime here is weekly (hours over the threshold in the week). Some provinces/industries use daily "
         "overtime or averaging agreements - adjust the rule if needed.",
         "Gross pay only: no deductions (CPP, EI, tax) are calculated.",
         "Employee names on Punches must match the Timesheet exactly."])
    st, s = _settings(wb, [("Week start date", d(YEAR, 11, 2), "date", "Usually a Sunday or Monday."),
                           ("Weekly OT threshold (hours)", 44, "num1", "Ontario ESA default is 44."),
                           ("OT multiplier", 1.5, "num2", "1.5 = time and a half.")])
    wp = wb.create_sheet("Punches")
    title(wp, "Clock In / Out Log", "Times like 8:00 AM. Hours = out - in - unpaid break.")
    pcols = [Col("Date", 12, fmt="date"), Col("Employee", 20), Col("Time In", 11, fmt="time"),
             Col("Time Out", 11, fmt="time"), Col("Unpaid Break (min)", 10, fmt="int", default=30),
             Col("Hours", 9, f='IF(OR([Time In]="",[Time Out]=""),0,ROUND(MOD([Time Out]-[Time In],1)*24-[Unpaid Break (min)]/60,2))',
                 fmt="num2", total="sum"),
             Col("Notes", 24)]
    emps = [("Maria Lopez", 24.50), ("Dev Sharma", 21.00), ("Chris Taylor", 19.75), ("Aisha Khan", 28.00)]
    shifts = {"Maria Lopez": [(8, 0, 17, 0)] * 5 + [(9, 0, 15, 0)],  # 6 days -> OT
              "Dev Sharma": [(9, 0, 17, 30)] * 5,
              "Chris Taylor": [(12, 0, 20, 0)] * 4,
              "Aisha Khan": [(7, 0, 18, 0)] * 5}
    samples, hours = [], {}
    for name, sh in shifts.items():
        for k, (h1, m1, h2, m2) in enumerate(sh):
            samples.append({"Date": d(YEAR, 11, 2) + dt.timedelta(days=k), "Employee": name,
                            "Time In": dt.time(h1, m1), "Time Out": dt.time(h2, m2), "Unpaid Break (min)": 30})
            hours[name] = hours.get(name, 0) + (h2 + m2 / 60 - h1 - m1 / 60) - 0.5
    samples.sort(key=lambda x: (x["Date"], x["Employee"]))
    tp = add_table(wp, pcols, samples, n=400, key="Employee")

    ws = wb.create_sheet("Timesheet", 2)
    title(ws, "Weekly Timesheet", "Daily hours come from the Punches tab.")
    wk, thr, mult = s["Week start date"], s["Weekly OT threshold (hours)"], s["OT multiplier"]
    hdr = ["Employee", "Hourly Rate"] + [""] * 7 + ["Total Hours", "Regular Hours", "OT Hours",
                                                    "Regular Pay", "OT Pay", "Gross Pay"]
    header(ws, 5, 1, hdr, height=34)
    for k in range(7):
        c = calc(ws, f"{GL(3 + k)}4", f"{wk}+{k}", "ddd mmm d", fill=None, align="center")
        ws[f"{GL(3 + k)}5"].value = f'=TEXT({GL(3 + k)}4,"ddd")'
    widths(ws, {"A": 22, "B": 10, "J": 10, "K": 10, "L": 9, "M": 12, "N": 11, "O": 12})
    H, E, D = tp.rng("Hours"), tp.rng("Employee"), tp.rng("Date")
    N = 40
    for i in range(N):
        r = 6 + i
        inp(ws, f"A{r}", emps[i][0] if i < len(emps) else None)
        inp(ws, f"B{r}", emps[i][1] if i < len(emps) else None, "money")
        for k in range(7):
            L = GL(3 + k)
            calc(ws, f"{L}{r}", f'IF($A{r}="","",SUMIFS({H},{E},$A{r},{D},{L}$4))', "num2")
        calc(ws, f"J{r}", f'IF(A{r}="","",SUM(C{r}:I{r}))', "num2", bold=True)
        calc(ws, f"K{r}", f'IF(A{r}="","",MIN(J{r},{thr}))', "num2")
        calc(ws, f"L{r}", f'IF(A{r}="","",MAX(0,J{r}-{thr}))', "num2")
        calc(ws, f"M{r}", f'IF(A{r}="","",K{r}*B{r})', "money")
        calc(ws, f"N{r}", f'IF(A{r}="","",L{r}*B{r}*{mult})', "money")
        calc(ws, f"O{r}", f'IF(A{r}="","",M{r}+N{r})', "money", bold=True)
    tr = 6 + N
    label(ws, f"A{tr}", "TOTALS", bold=True, fill=FILL_TOTAL)
    ws[f"B{tr}"].fill = FILL_TOTAL
    for c in range(3, 16):
        L = GL(c)
        calc(ws, f"{L}{tr}", f"SUM({L}6:{L}{tr - 1})", "money" if c >= 13 else "num2", bold=True, fill=FILL_TOTAL)
    flag_rule(ws, f"L6:L{tr - 1}", "AND(ISNUMBER(L6),L6>0)", fill=FILL_AMBER)
    ws.freeze_panes = "C6"
    finalize(wb, path)
    gross = 0
    for n_, rate in emps:
        h = hours[n_]
        gross += min(h, 44) * rate + max(0, h - 44) * rate * 1.5
    return [("Timesheet", f"O{tr}", round(gross, 2)), ("Timesheet", "L6", hours["Maria Lopez"] - 44),
            ("Timesheet", f"J{tr}", ("=", "Punches", tp.total("Hours")))]


# ============================================================ 07 HST tracker
def hst_tracker(path):
    wb = new_workbook()
    instructions(
        wb, "HST / GST Tracker",
        "Track HST collected on sales and HST paid on purchases (ITCs) to know what you owe CRA each period.",
        ["On Settings, enter your HST rate and the first day of your fiscal year.",
         "Log sales on the Sales tab: net amount and whether HST applies. HST collected is calculated.",
         "Log purchases on the Purchases tab with the HST shown on the receipt and the % that is business use.",
         "The Return Summary tab gives quarterly figures for your GST/HST return (lines 101, 103, 106, 109)."],
        [("Settings", "HST rate and fiscal year start."),
         ("Sales", "Sales and HST collected."),
         ("Purchases", "Expenses and input tax credits (ITCs)."),
         ("Return Summary", "Quarterly net tax owing (or refund if negative).")],
        ["Enter the HST actually charged on each purchase receipt - rates differ by province and some items are "
         "zero-rated or exempt.",
         "Line numbers refer to the CRA GST/HST return (GST34). Adjustments (lines 104/107) are not included.",
         "If you file monthly or annually, use the quarter rows as a guide or adjust the period dates."])
    st, s = _settings(wb, [("HST rate", 0.13, "pct", "13% Ontario; 15% Atlantic HST provinces; 5% GST-only."),
                           ("Fiscal year start", d(YEAR, 1, 1), "date", "First day of your fiscal year.")])
    rate, fys = s["HST rate"], s["Fiscal year start"]
    quarter = f'IF([Date]<{fys},"Before FY",IF([Date]>=EDATE({fys},12),"After FY","Q"&(INT(DATEDIF({fys},[Date],"m")/3)+1)))'
    lw, lists = lists_sheet(wb, {"Expense Category": ["Materials", "Equipment", "Rent", "Utilities", "Vehicle",
                                                      "Office", "Professional fees", "Meals (50%)", "Other"]})
    wsales = wb.create_sheet("Sales", 2)
    title(wsales, "Sales & HST Collected")
    sc = [Col("Date", 12, fmt="date"), Col("Invoice #", 11), Col("Customer", 22), Col("Description", 24),
          Col("Net Sale", 12, fmt="money", total="sum"), Col("Taxable? (Y/N)", 9, dv="Y,N", default="Y", align="center"),
          Col("HST Collected", 12, f=f'IF([Taxable? (Y/N)]="Y",ROUND([Net Sale]*{rate},2),0)', fmt="money", total="sum"),
          Col("Total", 12, f="[Net Sale]+[HST Collected]", fmt="money", total="sum"),
          Col("Quarter", 9, f=quarter, align="center")]
    sales = [3200, 4500, 1800, 6200, 2750, 5100, 3900, 4400, 2100, 7300, 3600, 2900]
    ss = [{"Date": d(YEAR, 1, 15) + dt.timedelta(days=30 * i), "Invoice #": f"INV-{3001 + i}",
           "Customer": f"Customer {i + 1}", "Description": "Consulting", "Net Sale": v,
           "Taxable? (Y/N)": "N" if i == 4 else "Y"} for i, v in enumerate(sales)]
    ts = add_table(wsales, sc, ss, n=300)
    wpur = wb.create_sheet("Purchases", 3)
    title(wpur, "Purchases & Input Tax Credits")
    pc = [Col("Date", 12, fmt="date"), Col("Vendor", 22), Col("Description", 24),
          Col("Category", 15, dv=lists["Expense Category"]), Col("Net Amount", 12, fmt="money", total="sum"),
          Col("HST Paid", 11, fmt="money", total="sum"), Col("Business Use %", 9, fmt="pct", default=1),
          Col("ITC Claimable", 12, f="ROUND([HST Paid]*[Business Use %],2)", fmt="money", total="sum"),
          Col("Quarter", 9, f=quarter, align="center")]
    pur = [(800, 1), (1500, 1), (420, 0.5), (2300, 1), (650, 1), (310, 0.5), (1200, 1), (990, 1)]
    ps = [{"Date": d(YEAR, 2, 3) + dt.timedelta(days=40 * i), "Vendor": f"Supplier {i + 1}",
           "Description": "Supplies", "Category": "Materials", "Net Amount": n_,
           "HST Paid": round(n_ * 0.13, 2), "Business Use %": u} for i, (n_, u) in enumerate(pur)]
    tp = add_table(wpur, pc, ps, n=300)
    wr = wb.create_sheet("Return Summary", 4)
    title(wr, "GST/HST Return Summary", "Positive net tax = amount owing to CRA. Negative = refund.")
    header(wr, 4, 1, ["Period", "From", "To (exclusive)", "Line 101 Sales", "Line 103 HST Collected",
                      "Line 106 ITCs", "Line 109 Net Tax"], height=34)
    widths(wr, {"A": 10, "B": 12, "C": 13, "D": 15, "E": 15, "F": 15, "G": 15})
    for q in range(4):
        r = 5 + q
        label(wr, f"A{r}", f"Q{q + 1}", bold=True)
        calc(wr, f"B{r}", f"EDATE({fys},{3 * q})", "date")
        calc(wr, f"C{r}", f"EDATE({fys},{3 * q + 3})", "date")
        calc(wr, f"D{r}", f'SUMIFS({ts.rng("Net Sale")},{ts.rng("Date")},">="&B{r},{ts.rng("Date")},"<"&C{r})', "money")
        calc(wr, f"E{r}", f'SUMIFS({ts.rng("HST Collected")},{ts.rng("Date")},">="&B{r},{ts.rng("Date")},"<"&C{r})', "money")
        calc(wr, f"F{r}", f'SUMIFS({tp.rng("ITC Claimable")},{tp.rng("Date")},">="&B{r},{tp.rng("Date")},"<"&C{r})', "money")
        calc(wr, f"G{r}", f"E{r}-F{r}", "money", bold=True)
    label(wr, "A9", "Year", bold=True, fill=FILL_TOTAL)
    for L in "DEFG":
        calc(wr, f"{L}9", f"SUM({L}5:{L}8)", "money", bold=True, fill=FILL_TOTAL)
    finalize(wb, path)
    coll = sum(round(v * 0.13, 2) for i, v in enumerate(sales) if i != 4)
    itc = sum(round(round(n_ * 0.13, 2) * u, 2) for n_, u in pur)
    return [("Return Summary", "G9", round(coll - itc, 2)), ("Return Summary", "D9", sum(sales)),
            ("Sales", "I6", "Q1")]


# ============================================================== 08 Inventory
def inventory(path):
    wb = new_workbook()
    instructions(
        wb, "Inventory Tracker",
        "Know what's on the shelf, what it's worth, and what needs reordering.",
        ["On the Items tab, add each product with SKU, cost, price, opening quantity and reorder point.",
         "Record stock movements on the Movements tab: In (received), Out (sold/used) or Adjust (+/- count fix).",
         "On-hand quantity, stock value and reorder status update automatically.",
         "Check the Summary tab for total stock value and items to reorder."],
        [("Items", "Product list with on-hand quantity, value and reorder status."),
         ("Movements", "Every stock in/out. The item name fills in from the SKU."),
         ("Summary", "Stock value by category and reorder counts."),
         ("Lists", "Categories and movement types.")],
        ["For Adjust, enter a negative quantity to reduce stock (e.g. -2 for damaged items).",
         "SKUs must be unique on the Items tab."])
    cats = ["Hardware", "Electrical", "Plumbing", "Paint"]
    lw, lists = lists_sheet(wb, {"Category": cats, "Movement Type": ["In", "Out", "Adjust"]})
    wm = wb.create_sheet("Movements", 1)
    wi = wb.create_sheet("Items", 1)
    items = [("HW-001", "Wood screws #8 (box 100)", "Hardware", "Aisle 1", "box", 6.50, 12.99, 40, 15, 30),
             ("HW-002", "Drywall anchors (25 pk)", "Hardware", "Aisle 1", "pack", 4.20, 8.49, 25, 10, 20),
             ("EL-001", "15A duplex receptacle", "Electrical", "Aisle 3", "each", 1.85, 4.99, 60, 25, 50),
             ("EL-002", "14/2 NMD90 wire (75 m)", "Electrical", "Aisle 3", "roll", 78.00, 129.00, 8, 4, 6),
             ("PL-001", "1/2in PEX (100 ft)", "Plumbing", "Aisle 4", "roll", 42.00, 74.99, 10, 5, 10),
             ("PL-002", "SharkBite 1/2in coupling", "Plumbing", "Aisle 4", "each", 6.10, 11.49, 30, 12, 24),
             ("PT-001", "Interior paint 3.78 L", "Paint", "Aisle 6", "can", 28.00, 54.99, 20, 8, 12),
             ("PT-002", "Roller kit 9in", "Paint", "Aisle 6", "kit", 7.50, 15.99, 15, 6, 10)]
    moves = [("HW-001", "Out", 18), ("HW-001", "In", 30), ("EL-001", "Out", 41), ("EL-002", "Out", 5),
             ("PL-001", "Out", 3), ("PT-001", "Out", 14), ("PT-002", "Adjust", -2), ("HW-002", "Out", 17),
             ("PL-002", "Out", 9), ("PT-001", "In", 12), ("EL-001", "Out", 12)]
    title(wm, "Stock Movements", "In = received, Out = sold/used, Adjust = count correction (+/-).")
    SKU_RANGE = "Items!$A$6:$A$505"
    mcols = [Col("Date", 12, fmt="date"), Col("SKU", 10), Col("Type", 9, dv=lists["Movement Type"], align="center"),
             Col("Qty", 8, fmt="int"), Col("Reference", 14), Col("Notes", 22),
             Col("Item (auto)", 28, f=f'IFERROR(INDEX(Items!$B$6:$B$505,MATCH([SKU],{SKU_RANGE},0)),"UNKNOWN SKU")')]
    ms = [{"Date": d(YEAR, 10, 1) + dt.timedelta(days=2 * i), "SKU": s_, "Type": t_, "Qty": q,
           "Reference": f"REF-{500 + i}"} for i, (s_, t_, q) in enumerate(moves)]
    tm = add_table(wm, mcols, ms, n=500, key="SKU")
    flag_rule(wm, f"G{tm.first}:G{tm.last}", f'G{tm.first}="UNKNOWN SKU"')
    title(wi, "Items", "On hand = opening + in - out + adjustments.")
    Q, S, T = tm.rng("Qty"), tm.rng("SKU"), tm.rng("Type")
    icols = [Col("SKU", 10), Col("Item", 28), Col("Category", 12, dv=lists["Category"]), Col("Location", 10),
             Col("Unit", 7), Col("Unit Cost", 10, fmt="money"), Col("Sell Price", 10, fmt="money"),
             Col("Opening Qty", 9, fmt="int"),
             Col("Qty In", 8, f=f'SUMIFS({Q},{S},[SKU],{T},"In")', fmt="int"),
             Col("Qty Out", 8, f=f'SUMIFS({Q},{S},[SKU],{T},"Out")', fmt="int"),
             Col("Adjust", 8, f=f'SUMIFS({Q},{S},[SKU],{T},"Adjust")', fmt="int"),
             Col("On Hand", 9, f="[Opening Qty]+[Qty In]-[Qty Out]+[Adjust]", fmt="int"),
             Col("Reorder Point", 9, fmt="int"), Col("Reorder Qty", 9, fmt="int"),
             Col("Status", 10, f='IF([On Hand]<=0,"OUT",IF([On Hand]<=[Reorder Point],"REORDER","OK"))', align="center"),
             Col("Stock Value", 12, f="[On Hand]*[Unit Cost]", fmt="money", total="sum"),
             Col("Margin %", 9, f="IFERROR(([Sell Price]-[Unit Cost])/[Sell Price],0)", fmt="pct")]
    isamp = [dict(zip(["SKU", "Item", "Category", "Location", "Unit", "Unit Cost", "Sell Price", "Opening Qty",
                       "Reorder Point", "Reorder Qty"], it)) for it in items]
    ti = add_table(wi, icols, isamp, n=500)
    flag_rule(wi, f"O{ti.first}:O{ti.last}", f'O{ti.first}="OUT"', bold=True)
    flag_rule(wi, f"O{ti.first}:O{ti.last}", f'O{ti.first}="REORDER"', fill=FILL_AMBER)
    sm = wb.create_sheet("Summary", 3)
    title(sm, "Inventory Summary")
    widths(sm, {"A": 26, "B": 14, "C": 14, "D": 14})
    for i, (lab, f, fm) in enumerate([
            ("Total stock value", f"SUM({ti.rng('Stock Value')})", "money"),
            ("Items to reorder", f'COUNTIF({ti.rng("Status")},"REORDER")', "int"),
            ("Items out of stock", f'COUNTIF({ti.rng("Status")},"OUT")', "int"),
            ("Units on hand", f"SUM({ti.rng('On Hand')})", "int")]):
        label(sm, f"A{4 + i}", lab, bold=True)
        calc(sm, f"B{4 + i}", f, fm)
    header(sm, 9, 1, ["Category", "Stock Value", "Units", "# Reorder"])
    for i in range(14):
        r = 10 + i
        calc(sm, f"A{r}", f'IF(Lists!A{3 + i}="","",Lists!A{3 + i})')
        calc(sm, f"B{r}", f'IF(A{r}="","",SUMIFS({ti.rng("Stock Value")},{ti.rng("Category")},A{r}))', "money")
        calc(sm, f"C{r}", f'IF(A{r}="","",SUMIFS({ti.rng("On Hand")},{ti.rng("Category")},A{r}))', "int")
        calc(sm, f"D{r}", f'IF(A{r}="","",COUNTIFS({ti.rng("Category")},A{r},{ti.rng("Status")},"REORDER"))', "int")
    finalize(wb, path)
    onhand = {}
    for it in items:
        onhand[it[0]] = it[7]
    for s_, t_, q in moves:
        onhand[s_] += q if t_ in ("In", "Adjust") else -q
    val = sum(onhand[it[0]] * it[5] for it in items)
    reorder = sum(1 for it in items if 0 < onhand[it[0]] <= it[8])
    return [("Items", ti.cell("On Hand", 0), onhand["HW-001"]), ("Summary", "B4", round(val, 2)),
            ("Summary", "B5", reorder)]


# ================================================================= 09 CRM lite
def crm_lite(path):
    wb = new_workbook()
    instructions(
        wb, "CRM Lite - Contacts & Pipeline",
        "A simple customer list and sales pipeline: who to call, what deals are worth, and what's likely to close.",
        ["On the Contacts tab, add each lead/customer with company, source, stage, deal value and next follow-up.",
         "Log calls, emails and meetings on the Activity tab. 'Last Contact' fills in from the latest activity.",
         "Rows with a follow-up date on or before today show DUE.",
         "The Pipeline tab totals deals by stage and source. Adjust stage probabilities on the Lists tab."],
        [("Settings", "As-of date."), ("Contacts", "One row per contact/deal."),
         ("Activity", "Log of touches (calls, emails, meetings)."),
         ("Pipeline", "Deal value and weighted value by stage and by lead source."),
         ("Lists", "Stages with win probabilities, sources, activity types.")],
        [AS_OF_NOTE, "Weighted value = deal value x stage probability.",
         "Contact names on the Activity tab must match the Contacts tab exactly."])
    st, s = _settings(wb, [("As-of date", "=TODAY()", "date", "Overwrite with a date to freeze the report.")])
    asof = s["As-of date"]
    stages = ["Lead", "Contacted", "Qualified", "Proposal", "Negotiation", "Won", "Lost"]
    probs = [0.05, 0.10, 0.25, 0.50, 0.75, 1.0, 0.0]
    sources = ["Referral", "Website", "Cold call", "Social media", "Trade show", "Other"]
    lw, lists = lists_sheet(wb, {"Stage": stages, "Win Probability": probs, "Source": sources,
                                 "Activity Type": ["Call", "Email", "Meeting", "Site visit", "Other"]})
    for i in range(len(stages) + 10):
        lw[f"C{3 + i}"].number_format = "0%"
    wa = wb.create_sheet("Activity", 2)
    wc = wb.create_sheet("Contacts", 2)
    title(wa, "Activity Log")
    acols = [Col("Date", 12, fmt="date"), Col("Contact", 22), Col("Type", 11, dv=lists["Activity Type"]),
             Col("Notes", 50)]
    people = [("Priya Nair", "Nair Dental", "Referral", "Proposal", 8500),
              ("Tom Becker", "Becker Auto", "Website", "Qualified", 4200),
              ("Lina Chen", "Chen Law LLP", "Trade show", "Negotiation", 15000),
              ("Omar Haddad", "Haddad Bakery", "Cold call", "Lead", 2500),
              ("Grace O'Neil", "O'Neil Realty", "Referral", "Won", 6800),
              ("Raj Singh", "Singh Logistics", "Social media", "Contacted", 9600),
              ("Emily Roy", "Roy Fitness", "Website", "Lost", 3100),
              ("Ben Okafor", "Okafor Clinics", "Referral", "Proposal", 12000)]
    acts = [(0, 0), (0, 14), (1, 3), (2, 6), (2, 20), (4, 1), (5, 9), (7, 12), (7, 25), (3, 2)]
    asamp = [{"Date": d(YEAR, 9, 1) + dt.timedelta(days=dd), "Contact": people[p][0],
              "Type": "Call" if k % 2 else "Email", "Notes": "Discussed scope and timing"}
             for k, (p, dd) in enumerate(acts)]
    ta = add_table(wa, acols, asamp, n=500, key="Contact")
    title(wc, "Contacts & Deals")
    AD, AC = ta.rng("Date"), ta.rng("Contact")
    ccols = [Col("Contact Name", 20), Col("Company", 20), Col("Email", 24), Col("Phone", 14),
             Col("Source", 12, dv=lists["Source"]), Col("Stage", 12, dv=lists["Stage"], default="Lead"),
             Col("Deal Value", 12, fmt="money", total="sum"),
             Col("Probability", 10, f="IFERROR(INDEX(Lists!$C$3:$C$19,MATCH([Stage],Lists!$A$3:$A$19,0)),0)", fmt="pct"),
             Col("Weighted Value", 12, f="[Deal Value]*[Probability]", fmt="money", total="sum"),
             Col("Last Contact", 12, f=f'IF(_xlfn.MAXIFS({AD},{AC},[Contact Name])=0,"",_xlfn.MAXIFS({AD},{AC},[Contact Name]))', fmt="date"),
             Col("Days Since Contact", 9, f=f'IF([Last Contact]="","",{asof}-[Last Contact])', fmt="int"),
             Col("Next Follow-up", 12, fmt="date"),
             Col("Follow-up", 9, f=f'IF(OR([Stage]="Won",[Stage]="Lost",[Next Follow-up]=""),"",IF([Next Follow-up]<={asof},"DUE",""))', align="center"),
             Col("Owner", 10), Col("Notes", 30)]
    csamp = [{"Contact Name": n_, "Company": co, "Email": n_.split()[0].lower() + "@example.com",
              "Phone": f"416-555-01{10 + i}", "Source": src, "Stage": stg, "Deal Value": v,
              "Next Follow-up": d(YEAR, 10, 20) + dt.timedelta(days=5 * i), "Owner": "Alex"}
             for i, (n_, co, src, stg, v) in enumerate(people)]
    tc = add_table(wc, ccols, csamp, n=500)
    flag_rule(wc, f"M{tc.first}:M{tc.last}", f'M{tc.first}="DUE"', fill=FILL_AMBER, bold=True)
    wp = wb.create_sheet("Pipeline", 4)
    title(wp, "Pipeline Summary")
    widths(wp, {"A": 16, "B": 10, "C": 14, "D": 14})
    header(wp, 4, 1, ["Stage", "# Deals", "Deal Value", "Weighted Value"])
    S, V, W, SRC = tc.rng("Stage"), tc.rng("Deal Value"), tc.rng("Weighted Value"), tc.rng("Source")
    for i in range(len(stages)):
        r = 5 + i
        calc(wp, f"A{r}", f"Lists!A{3 + i}")
        calc(wp, f"B{r}", f"COUNTIFS({S},A{r})", "int")
        calc(wp, f"C{r}", f"SUMIFS({V},{S},A{r})", "money")
        calc(wp, f"D{r}", f"SUMIFS({W},{S},A{r})", "money")
    label(wp, "A12", "Open pipeline", bold=True, fill=FILL_TOTAL)
    calc(wp, "B12", "SUM(B5:B9)", "int", bold=True, fill=FILL_TOTAL)
    calc(wp, "C12", "SUM(C5:C9)", "money", bold=True, fill=FILL_TOTAL)
    calc(wp, "D12", "SUM(D5:D9)", "money", bold=True, fill=FILL_TOTAL)
    label(wp, "A13", "Win rate", bold=True)
    calc(wp, "B13", "IFERROR(B10/(B10+B11),0)", "pct")
    header(wp, 15, 1, ["Source", "# Contacts", "Won Value", "Open Value"])
    for i in range(len(sources)):
        r = 16 + i
        calc(wp, f"A{r}", f"Lists!E{3 + i}")
        calc(wp, f"B{r}", f"COUNTIFS({SRC},A{r})", "int")
        calc(wp, f"C{r}", f'SUMIFS({V},{SRC},A{r},{S},"Won")', "money")
        calc(wp, f"D{r}", f'SUMIFS({V},{SRC},A{r})-C{r}-SUMIFS({V},{SRC},A{r},{S},"Lost")', "money")
    ch = BarChart()
    ch.title = "Deal value by stage"
    ch.height, ch.width = 7, 14
    ch.add_data(Reference(wp, min_col=3, max_col=4, min_row=4, max_row=11), titles_from_data=True)
    ch.set_categories(Reference(wp, min_col=1, min_row=5, max_row=11))
    ch.y_axis.numFmt = "$#,##0"
    wp.add_chart(ch, "F4")
    finalize(wb, path)
    pm = dict(zip(stages, probs))
    open_w = sum(v * pm[stg] for *_, stg, v in people if stg not in ("Won", "Lost"))
    last_priya = d(YEAR, 9, 15)
    return [("Pipeline", "D12", open_w), ("Contacts", tc.cell("Last Contact", 0), last_priya),
            ("Pipeline", "B13", 0.5)]


# ======================================================== 10 Vacation tracker
def vacation_tracker(path):
    wb = new_workbook()
    instructions(
        wb, "Vacation & Leave Tracker",
        "Track vacation entitlement, time taken and balances, plus sick and personal days, for each employee.",
        ["On Settings, set the year. Check the stat holidays on the Holidays tab (Ontario defaults).",
         "On Employees, enter each person's hire date, annual vacation days and any carry-over.",
         "Log each absence on the Leave Log tab with start and end dates. Working days are counted "
         "automatically (weekends and holidays excluded).",
         "Only leave marked Approved = Yes is deducted. Balances update on the Employees tab."],
        [("Settings", "Tracking year."), ("Employees", "Entitlement, days taken and remaining balance."),
         ("Leave Log", "Every absence request."), ("Holidays", "Statutory holidays (edit for your province)."),
         ("Lists", "Leave types and approval statuses.")],
        ["'ESA minimum' shows Ontario's minimum: 10 days (2 weeks) under 5 years of service, 15 days (3 weeks) at 5+.",
         "Leave is counted in the year it starts. Split leave that crosses Dec 31 into two rows.",
         "Employee names on the Leave Log must match the Employees tab exactly."])
    st, s = _settings(wb, [("Year", YEAR, "0", "Tracking year (calendar).")])
    Y = s["Year"]
    lw, lists = lists_sheet(wb, {"Leave Type": ["Vacation", "Sick", "Personal", "Bereavement", "Unpaid", "Other"],
                                 "Approved": ["Yes", "Pending", "No"]})
    wh = wb.create_sheet("Holidays", 2)
    title(wh, f"Statutory Holidays {YEAR} (Ontario)", "Edit for your province/year. Used to skip days off.")
    header(wh, 4, 1, ["Holiday", "Date", "Weekday"])
    widths(wh, {"A": 26, "B": 13, "C": 11})
    hol = [("New Year's Day", d(YEAR, 1, 1)), ("Family Day", d(YEAR, 2, 16)), ("Good Friday", d(YEAR, 4, 3)),
           ("Victoria Day", d(YEAR, 5, 18)), ("Canada Day", d(YEAR, 7, 1)), ("Labour Day", d(YEAR, 9, 7)),
           ("Thanksgiving", d(YEAR, 10, 12)), ("Christmas Day", d(YEAR, 12, 25)),
           ("Boxing Day (observed Mon)", d(YEAR, 12, 28))]
    for i in range(20):
        r = 5 + i
        inp(wh, f"A{r}", hol[i][0] if i < len(hol) else None)
        inp(wh, f"B{r}", hol[i][1] if i < len(hol) else None, "date")
        calc(wh, f"C{r}", f'IF(B{r}="","",TEXT(B{r},"dddd"))')
    HOL = "Holidays!$B$5:$B$24"
    wl = wb.create_sheet("Leave Log", 2)
    we = wb.create_sheet("Employees", 2)
    title(wl, "Leave Log", "Days = working days between start and end (inclusive), excluding weekends and holidays.")
    lcols = [Col("Employee", 20), Col("Leave Type", 12, dv=lists["Leave Type"], default="Vacation"),
             Col("Start Date", 12, fmt="date"), Col("End Date", 12, fmt="date"),
             Col("Days", 7, f=f"NETWORKDAYS([Start Date],[End Date],{HOL})", fmt="num1", total="sum"),
             Col("Approved", 10, dv=lists["Approved"], default="Yes", align="center"),
             Col("Year", 7, f="YEAR([Start Date])", fmt="0"), Col("Notes", 30)]
    emps = [("Maria Lopez", "Operations", d(2018, 3, 12), 15, 2), ("Dev Sharma", "Sales", d(2023, 6, 1), 10, 0),
            ("Chris Taylor", "Warehouse", d(2021, 9, 20), 10, 1), ("Aisha Khan", "Finance", d(2015, 1, 5), 20, 3)]
    leave = [("Maria Lopez", "Vacation", d(YEAR, 3, 16), d(YEAR, 3, 20), "Yes"),
             ("Maria Lopez", "Vacation", d(YEAR, 6, 29), d(YEAR, 7, 3), "Yes"),  # includes Canada Day
             ("Dev Sharma", "Sick", d(YEAR, 2, 10), d(YEAR, 2, 11), "Yes"),
             ("Dev Sharma", "Vacation", d(YEAR, 8, 10), d(YEAR, 8, 14), "Yes"),
             ("Chris Taylor", "Personal", d(YEAR, 4, 7), d(YEAR, 4, 7), "Yes"),
             ("Aisha Khan", "Vacation", d(YEAR, 12, 21), d(YEAR, 12, 31), "Pending"),
             ("Aisha Khan", "Vacation", d(YEAR, 9, 8), d(YEAR, 9, 11), "Yes")]
    ls_ = [{"Employee": e, "Leave Type": t_, "Start Date": a, "End Date": b, "Approved": ap}
           for e, t_, a, b, ap in leave]
    tl = add_table(wl, lcols, ls_, n=400)
    title(we, "Employees & Balances", "Taken = approved leave in the Settings year.")
    E, T, D_, A_, YR = tl.rng("Employee"), tl.rng("Leave Type"), tl.rng("Days"), tl.rng("Approved"), tl.rng("Year")

    def taken(kind):
        return f'SUMIFS({D_},{E},[Employee],{T},"{kind}",{A_},"Yes",{YR},{Y})'
    ecols = [Col("Employee", 20), Col("Department", 14), Col("Hire Date", 12, fmt="date"),
             Col("Years of Service", 9, f=f'DATEDIF([Hire Date],DATE({Y},12,31),"y")', fmt="0"),
             Col("ESA minimum (days)", 10, f="IF([Years of Service]>=5,15,10)", fmt="0"),
             Col("Annual Entitlement (days)", 11, fmt="num1"), Col("Carry-over (days)", 10, fmt="num1"),
             Col("Total Available", 10, f="[Annual Entitlement (days)]+[Carry-over (days)]", fmt="num1"),
             Col("Vacation Taken", 10, f=taken("Vacation"), fmt="num1", total="sum"),
             Col("Vacation Pending", 10, f=f'SUMIFS({D_},{E},[Employee],{T},"Vacation",{A_},"Pending",{YR},{Y})', fmt="num1"),
             Col("Vacation Remaining", 10, f="[Total Available]-[Vacation Taken]", fmt="num1", total="sum"),
             Col("Sick Taken", 9, f=taken("Sick"), fmt="num1", total="sum"),
             Col("Personal Taken", 9, f=taken("Personal"), fmt="num1", total="sum"),
             Col("Other Leave", 9, f=f'SUMIFS({D_},{E},[Employee],{A_},"Yes",{YR},{Y})-[Vacation Taken]-[Sick Taken]-[Personal Taken]', fmt="num1")]
    es = [{"Employee": e, "Department": dp, "Hire Date": h, "Annual Entitlement (days)": ent,
           "Carry-over (days)": co} for e, dp, h, ent, co in emps]
    te = add_table(we, ecols, es, n=100)
    flag_rule(we, f"K{te.first}:K{te.last}", f"AND(ISNUMBER(K{te.first}),K{te.first}<0)")
    flag_rule(we, f"F{te.first}:F{te.last}", f"AND(ISNUMBER(F{te.first}),ISNUMBER(E{te.first}),F{te.first}<E{te.first})", fill=FILL_AMBER)
    add_list(wl, f"A{tl.first}:A{tl.last}", f"=Employees!$A${te.first}:$A${te.last}")
    finalize(wb, path)
    hset = {h for _, h in hol}

    def wd(a, b):
        return sum(1 for k in range((b - a).days + 1)
                   if (a + dt.timedelta(days=k)).weekday() < 5 and a + dt.timedelta(days=k) not in hset)
    maria = sum(wd(a, b) for e, t_, a, b, ap in leave if e == "Maria Lopez" and t_ == "Vacation" and ap == "Yes")
    pend = sum(wd(a, b) for e, t_, a, b, ap in leave if e == "Aisha Khan" and ap == "Pending")
    return [("Employees", te.cell("Vacation Remaining", 0), 17 - maria), ("Leave Log", tl.cell("Days", 1), wd(d(YEAR, 6, 29), d(YEAR, 7, 3))),
            ("Employees", te.cell("Vacation Pending", 3), pend), ("Employees", te.cell("Years of Service", 0), 8)]


TEMPLATES_A = [
    ("01-monthly-budget", budget, "Monthly budget vs actual by category, with automatic variance and a by-month summary."),
    ("02-cash-flow-forecast", cash_flow, "12-month cash flow forecast with running bank balance, low-cash warnings and chart."),
    ("03-invoice-tracker", invoice_tracker, "Accounts receivable: invoices, HST, payments, overdue status, aging buckets and balances by client."),
    ("04-quote-tracker", quote_tracker, "Quotes/estimates with follow-up reminders, win rate and results by salesperson."),
    ("05-job-costing", job_costing, "Estimated vs actual labour, materials and other costs per job, with profit and margin."),
    ("06-payroll-hours", payroll_hours, "Clock-in/out log that rolls into a weekly timesheet with overtime and gross pay."),
    ("07-hst-tracker", hst_tracker, "HST collected vs input tax credits, with quarterly GST/HST return lines (101/103/106/109)."),
    ("08-inventory", inventory, "Stock list with in/out movements, on-hand quantity, stock value and reorder alerts."),
    ("09-crm-lite", crm_lite, "Contacts and deal pipeline with stage probabilities, activity log, follow-up flags and pipeline summary."),
    ("10-vacation-tracker", vacation_tracker, "Vacation entitlement, leave log (skips weekends/stat holidays) and remaining balances."),
]
