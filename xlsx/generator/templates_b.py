"""Templates 11-20."""

import datetime as dt

from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter as GL

from .common import (AS_OF_NOTE, FILL_AMBER, FILL_GREEN, FILL_RED, FILL_TOTAL, F_SUB, YEAR, Col,
                     PatternFill, add_list, add_table, calc, d, finalize, flag_rule, header, inp,
                     instructions, label, lists_sheet, new_workbook, section, settings_block, title,
                     widths)
from .templates_a import MONTHS, _settings


def _month_bounds(Y, m):
    return f"DATE({Y},{m},1)", f"DATE({Y},{m + 1},1)" if m < 12 else f"DATE({Y}+1,1,1)"


# ========================================================== 11 Expense tracker
def expense_tracker(path):
    wb = new_workbook()
    instructions(
        wb, "Business Expense Tracker",
        "Log every business expense with its HST so you can see spending by category and month.",
        ["Enter each expense on the Expenses tab: date, vendor, category, payment method and the total paid.",
         "Enter the HST shown on the receipt. The pre-tax (net) amount is calculated.",
         "Mark whether you have the receipt and whether it can be billed back to a client.",
         "The Summary tab shows net spending by category and month for the year on Settings."],
        [("Settings", "Year for the summary."), ("Expenses", "One row per expense."),
         ("Summary", "Category x month table of net (pre-tax) spending."),
         ("Lists", "Categories and payment methods - edit to suit your business.")],
        ["HST paid on business expenses can usually be claimed back as input tax credits - see the HST Tracker template.",
         "Rows flagged in red are missing a receipt."])
    st, s = _settings(wb, [("Summary year", YEAR, "0", None)])
    Y = s["Summary year"]
    cats = ["Advertising", "Meals & entertainment", "Office supplies", "Software", "Travel", "Vehicle & fuel",
            "Phone & internet", "Professional fees", "Rent", "Repairs & maintenance", "Other"]
    lw, lists = lists_sheet(wb, {"Category": cats, "Payment Method": ["Company Visa", "Debit", "Cash",
                                                                      "E-transfer", "Personal card"]})
    ws = wb.create_sheet("Expenses", 2)
    title(ws, "Expenses")
    cols = [Col("Date", 12, fmt="date"), Col("Vendor", 20), Col("Category", 20, dv=lists["Category"]),
            Col("Description", 26), Col("Payment Method", 14, dv=lists["Payment Method"]),
            Col("Total Paid", 12, fmt="money", total="sum"), Col("HST Included", 11, fmt="money", total="sum"),
            Col("Net (pre-tax)", 12, f="[Total Paid]-[HST Included]", fmt="money", total="sum"),
            Col("Receipt? (Y/N)", 9, dv="Y,N", default="Y", align="center"),
            Col("Billable? (Y/N)", 9, dv="Y,N", default="N", align="center"), Col("Client / Job", 16)]
    data = [("Staples", "Office supplies", 84.75), ("Google Ads", "Advertising", 350.00),
            ("Petro-Canada", "Vehicle & fuel", 92.40), ("Rogers", "Phone & internet", 135.60),
            ("Tim Hortons", "Meals & entertainment", 38.42), ("Adobe", "Software", 33.89),
            ("Air Canada", "Travel", 512.30), ("Home Depot", "Repairs & maintenance", 226.00),
            ("Esso", "Vehicle & fuel", 88.15), ("QuickBooks", "Software", 101.70),
            ("Office landlord", "Rent", 2260.00), ("CPA firm", "Professional fees", 1130.00)]
    samples = []
    for i, (v, c, amt) in enumerate(data):
        hst = round(amt - amt / 1.13, 2)
        samples.append({"Date": d(YEAR, 1 + i, 5 + i), "Vendor": v, "Category": c, "Description": "",
                        "Payment Method": "Company Visa", "Total Paid": amt, "HST Included": hst,
                        "Receipt? (Y/N)": "N" if i == 4 else "Y", "Billable? (Y/N)": "Y" if i == 6 else "N",
                        "Client / Job": "J-104" if i == 6 else None})
    t = add_table(ws, cols, samples, n=500)
    flag_rule(ws, f"I{t.first}:I{t.last}", f'I{t.first}="N"')
    sm = wb.create_sheet("Summary", 3)
    title(sm, "Net Spending by Category and Month", "Pre-tax amounts for the year on Settings")
    header(sm, 4, 1, ["Category"] + MONTHS + ["Year Total"])
    widths(sm, {"A": 24, "N": 13})
    for c in range(2, 14):
        sm.column_dimensions[GL(c)].width = 10
    N, D, C = t.rng("Net (pre-tax)"), t.rng("Date"), t.rng("Category")
    nrows = len(cats) + 10
    for i in range(nrows):
        r = 5 + i
        calc(sm, f"A{r}", f'IF(Lists!A{3 + i}="","",Lists!A{3 + i})')
        for m in range(1, 13):
            a, b = _month_bounds(Y, m)
            calc(sm, f"{GL(1 + m)}{r}", f'IF($A{r}="","",SUMIFS({N},{C},$A{r},{D},">="&{a},{D},"<"&{b}))', "money0")
        calc(sm, f"N{r}", f'IF(A{r}="","",SUM(B{r}:M{r}))', "money0", bold=True)
    tr = 5 + nrows
    label(sm, f"A{tr}", "Total", bold=True, fill=FILL_TOTAL)
    for c in range(2, 15):
        L = GL(c)
        calc(sm, f"{L}{tr}", f"SUM({L}5:{L}{tr - 1})", "money0", bold=True, fill=FILL_TOTAL)
    sm.freeze_panes = "B5"
    finalize(wb, path)
    net = round(sum(a - round(a - a / 1.13, 2) for _, _, a in data), 2)
    veh = round(sum(a - round(a - a / 1.13, 2) for _, c, a in data if c == "Vehicle & fuel"), 2)
    return [("Summary", f"N{tr}", net), ("Summary", "N10", veh), ("Expenses", t.total("Net (pre-tax)"), net)]


# ============================================================ 12 Mileage log
def mileage_log(path):
    wb = new_workbook()
    instructions(
        wb, "Vehicle Mileage Log",
        "Keep a CRA-style logbook of business driving and calculate the tax-free per-km allowance.",
        ["On Settings, check the per-km rates (CRA publishes new rates each year) and the 5,000 km tier.",
         "Log every trip in date order: start and end odometer, purpose, and whether it was Business or Personal.",
         "Distance, year-to-date business km and the reimbursement (tiered rate) are calculated per trip.",
         "The Summary tab shows total km, business-use % and the total allowance."],
        [("Settings", "Per-km rates and tier threshold."), ("Log", "One row per trip."),
         ("Summary", "Totals and business-use percentage.")],
        ["Default rates are CRA's 2025 reasonable allowance rates for the provinces (72 cents first 5,000 km, "
         "66 cents after). Update them for the current year at canada.ca (search 'automobile allowance rates').",
         "Enter trips in date order - the 5,000 km tier is applied in row order.",
         "CRA expects a logbook showing date, destination, purpose and km for each business trip."])
    st, s = _settings(wb, [("Rate - first tier ($/km)", 0.72, "rate", "Update yearly from CRA."),
                           ("Tier threshold (km)", 5000, "int", "Business km per year at the first rate."),
                           ("Rate - after threshold ($/km)", 0.66, "rate", None)])
    r1, thr, r2 = s["Rate - first tier ($/km)"], s["Tier threshold (km)"], s["Rate - after threshold ($/km)"]
    ws = wb.create_sheet("Log", 2)
    title(ws, "Mileage Log")
    prev = "([Business km YTD]-[Distance (km)])"
    first_tier = f"MIN([Distance (km)],MAX(0,{thr}-{prev}))"
    cols = [Col("Date", 12, fmt="date"), Col("Vehicle", 12), Col("Purpose", 26), Col("From", 14), Col("To", 16),
            Col("Start Odometer", 11, fmt="int"), Col("End Odometer", 11, fmt="int"),
            Col("Distance (km)", 10, f='IF(OR([Start Odometer]="",[End Odometer]=""),0,[End Odometer]-[Start Odometer])', fmt="num1", total="sum"),
            Col("Trip Type", 11, dv="Business,Personal", default="Business"),
            Col("Business km YTD", 11, f='SUMIF([^Trip Type],"Business",[^Distance (km)])', fmt="num1"),
            Col("Allowance", 12, f=f'IF([Trip Type]<>"Business",0,{first_tier}*{r1}+([Distance (km)]-{first_tier})*{r2})', fmt="money", total="sum")]
    trips, odo, samples = [], 48210, []
    for i in range(24):
        km = [182, 45, 320, 64, 410, 25, 275, 90, 515, 38, 460, 150][i % 12] + (i // 12) * 7
        typ = "Personal" if i % 5 == 3 else "Business"
        samples.append({"Date": d(YEAR, 1, 8) + dt.timedelta(days=13 * i), "Vehicle": "2022 F-150",
                        "Purpose": "Client site visit" if typ == "Business" else "Personal",
                        "From": "Office", "To": f"Site {i + 1}", "Start Odometer": odo, "End Odometer": odo + km,
                        "Trip Type": typ})
        trips.append((km, typ))
        odo += km + 12
    t = add_table(ws, cols, samples, n=500)
    sm = wb.create_sheet("Summary", 3)
    title(sm, "Mileage Summary")
    widths(sm, {"A": 28, "B": 14})
    D, T, A = t.rng("Distance (km)"), t.rng("Trip Type"), t.rng("Allowance")
    for i, (lab, f, fm) in enumerate([("Total km logged", f"SUM({D})", "num1"),
                                      ("Business km", f'SUMIF({T},"Business",{D})', "num1"),
                                      ("Personal km", f'SUMIF({T},"Personal",{D})', "num1"),
                                      ("Business use %", "IFERROR(B5/B4,0)", "pct"),
                                      ("Total allowance", f"SUM({A})", "money")]):
        label(sm, f"A{4 + i}", lab, bold=True)
        calc(sm, f"B{4 + i}", f, fm)
    finalize(wb, path)
    cum, allow = 0, 0
    for km, typ in trips:
        if typ != "Business":
            continue
        ft = min(km, max(0, 5000 - cum))
        allow += ft * 0.72 + (km - ft) * 0.66
        cum += km
    return [("Summary", "B8", round(allow, 2)), ("Summary", "B5", cum),
            ("Summary", "B4", sum(k for k, _ in trips))]


# =============================================================== 13 P&L
def profit_loss(path):
    wb = new_workbook()
    instructions(
        wb, "Profit & Loss Statement (Monthly)",
        "A 12-month income statement: revenue, cost of sales, gross profit, expenses and net income.",
        ["Rename line items in column A to match your chart of accounts (yellow cells).",
         "Enter monthly amounts. Totals, gross margin and net margin calculate automatically.",
         "Set your estimated income tax rate at the top to see after-tax profit.",
         "The '% of Revenue' column shows each line as a share of annual revenue."],
        [("P&L", "Monthly profit and loss with annual totals and margins.")],
        ["Default tax rate 12.2% = combined federal + Ontario small business rate for a CCPC on active business "
         "income (verify for your situation).", "Enter expenses as positive numbers."])
    ws = wb.create_sheet("P&L")
    title(ws, f"Profit & Loss - Fiscal {YEAR}", "Amounts in dollars")
    label(ws, "A3", "Estimated income tax rate", bold=True)
    inp(ws, "B3", 0.122, "pct")
    widths(ws, {"A": 30, "N": 13, "O": 11})
    for c in range(2, 14):
        ws.column_dimensions[GL(c)].width = 10
    header(ws, 5, 1, ["Line item"] + MONTHS + ["Year Total", "% of Revenue"])
    rev = [("Product sales", 18000, 400), ("Service revenue", 6500, 150), ("Other income", 300, 0)]
    cogs = [("Materials & inventory", 7200, 160), ("Direct labour", 3100, 50)]
    opex = [("Wages & benefits", 4800), ("Rent", 2500), ("Utilities", 420), ("Insurance", 260),
            ("Advertising & marketing", 900), ("Software & subscriptions", 240), ("Phone & internet", 160),
            ("Vehicle", 650), ("Professional fees", 400), ("Office & supplies", 180), ("Bank & merchant fees", 210),
            ("Travel & meals", 300)]
    other = [("Interest expense", 220), ("Depreciation / amortization", 450)]
    r = 6
    rows = {}

    def block(name, items, growth=True):
        nonlocal r
        section(ws, f"A{r}", name)
        r += 1
        a = r
        for it in items + [("", 0, 0)] * 2:
            n, base = it[0], it[1]
            g = it[2] if len(it) > 2 else 0
            inp(ws, f"A{r}", n or None)
            for m in range(12):
                inp(ws, f"{GL(2 + m)}{r}", (base + g * m) if n else None, "money0")
            calc(ws, f"N{r}", f"SUM(B{r}:M{r})", "money0")
            calc(ws, f"O{r}", f"IFERROR(N{r}/N$REV,0)", "pct")
            r += 1
        return a, r - 1

    def total_row(lab, formula_fn, key, pct=True, fill=FILL_TOTAL):
        nonlocal r
        label(ws, f"A{r}", lab, bold=True, fill=fill)
        for c in range(2, 15):
            L = GL(c)
            calc(ws, f"{L}{r}", formula_fn(L), "money0", bold=True, fill=fill)
        if pct:
            calc(ws, f"O{r}", f"IFERROR(N{r}/N$REV,0)", "pct", bold=True, fill=fill)
        rows[key] = r
        r += 1

    a, b = block("Revenue", rev)
    total_row("Total Revenue", lambda L: f"SUM({L}{a}:{L}{b})", "rev")
    r += 1
    a, b = block("Cost of Sales", cogs)
    total_row("Total Cost of Sales", lambda L: f"SUM({L}{a}:{L}{b})", "cogs")
    total_row("GROSS PROFIT", lambda L: f"{L}{rows['rev']}-{L}{rows['cogs']}", "gp")
    label(ws, f"A{r}", "Gross margin %")
    for c in range(2, 15):
        L = GL(c)
        calc(ws, f"{L}{r}", f"IFERROR({L}{rows['gp']}/{L}{rows['rev']},0)", "pct")
    r += 2
    a, b = block("Operating Expenses", [(n, v) for n, v in opex])
    total_row("Total Operating Expenses", lambda L: f"SUM({L}{a}:{L}{b})", "opex")
    total_row("OPERATING INCOME", lambda L: f"{L}{rows['gp']}-{L}{rows['opex']}", "oi")
    r += 1
    a, b = block("Other Expenses", [(n, v) for n, v in other])
    total_row("Total Other Expenses", lambda L: f"SUM({L}{a}:{L}{b})", "oth")
    total_row("NET INCOME BEFORE TAX", lambda L: f"{L}{rows['oi']}-{L}{rows['oth']}", "nibt")
    total_row("Estimated income tax", lambda L: f"MAX(0,{L}{rows['nibt']})*$B$3", "tax", fill=None)
    total_row("NET INCOME", lambda L: f"{L}{rows['nibt']}-{L}{rows['tax']}", "ni")
    label(ws, f"A{r}", "Net margin %")
    for c in range(2, 15):
        L = GL(c)
        calc(ws, f"{L}{r}", f"IFERROR({L}{rows['ni']}/{L}{rows['rev']},0)", "pct")
    # patch revenue row references
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and "$REV" in c.value:
                c.value = c.value.replace("$REV", f"${rows['rev']}")
    ws.freeze_panes = "B6"
    finalize(wb, path)
    R = sum(base * 12 + g * 66 for _, base, g in rev)
    C = sum(base * 12 + g * 66 for _, base, g in cogs)
    O = sum(v * 12 for _, v in opex)
    X = sum(v * 12 for _, v in other)
    nibt = R - C - O - X
    tax = sum(max(0, ((sum(b_ + g * m for _, b_, g in rev) - sum(b_ + g * m for _, b_, g in cogs)) - sum(v for _, v in opex) - sum(v for _, v in other))) * 0.122 for m in range(12))
    return [("P&L", f"N{rows['nibt']}", nibt), ("P&L", f"N{rows['ni']}", nibt - tax), ("P&L", f"O{rows['rev']}", 1)]


# =========================================================== 14 Break-even
def break_even(path):
    wb = new_workbook()
    instructions(
        wb, "Break-Even Analysis",
        "Find how many units (and how much revenue) you need to cover your costs and hit a profit target.",
        ["List your monthly fixed costs in the yellow table (rent, salaries, insurance...).",
         "Enter your selling price and variable cost per unit (materials, commissions, shipping...).",
         "Enter your target monthly profit and expected unit sales.",
         "Read break-even units/revenue, margin of safety, the profit table, chart and price sensitivity."],
        [("Break-Even", "Inputs, results, profit-by-volume table, chart and price sensitivity.")],
        ["Contribution margin = price - variable cost. Break-even units = fixed costs / contribution margin.",
         "If contribution margin is zero or negative you can never break even - results show 'n/a'."])
    ws = wb.create_sheet("Break-Even")
    title(ws, "Break-Even Analysis", "Monthly figures")
    widths(ws, {"A": 30, "B": 14, "C": 4, "D": 16, "E": 14, "F": 14, "G": 14, "H": 4, "I": 14, "J": 14})
    section(ws, "A4", "Fixed costs (per month)")
    fixed = [("Rent", 3000), ("Salaries", 9000), ("Insurance", 400), ("Utilities", 600), ("Software", 250),
             ("Loan payments", 750), ("Other", 500)]
    for i in range(10):
        r = 5 + i
        inp(ws, f"A{r}", fixed[i][0] if i < len(fixed) else None)
        inp(ws, f"B{r}", fixed[i][1] if i < len(fixed) else None, "money0")
    label(ws, "A15", "Total fixed costs", bold=True, fill=FILL_TOTAL)
    calc(ws, "B15", "SUM(B5:B14)", "money0", bold=True, fill=FILL_TOTAL)
    section(ws, "A17", "Unit economics")
    for i, (lab, v, fm) in enumerate([("Selling price per unit", 85, "money"), ("Variable cost per unit", 38, "money"),
                                      ("Target profit (per month)", 5000, "money0"),
                                      ("Expected unit sales (per month)", 400, "int")]):
        label(ws, f"A{18 + i}", lab, bold=True)
        inp(ws, f"B{18 + i}", v, fm)
    section(ws, "A23", "Results")
    res = [("Contribution margin per unit", "B18-B19", "money"),
           ("Contribution margin ratio", "IFERROR(B24/B18,0)", "pct"),
           ("Break-even units", 'IF(B24<=0,"n/a",B15/B24)', "num1"),
           ("Break-even revenue", 'IF(B24<=0,"n/a",B26*B18)', "money0"),
           ("Units for target profit", 'IF(B24<=0,"n/a",(B15+B20)/B24)', "num1"),
           ("Revenue for target profit", 'IF(B24<=0,"n/a",B28*B18)', "money0"),
           ("Profit at expected sales", "B21*B24-B15", "money0"),
           ("Margin of safety (units)", 'IF(B24<=0,"n/a",B21-B26)', "num1"),
           ("Margin of safety (%)", 'IF(B24<=0,"n/a",IFERROR(B31/B21,0))', "pct")]
    for i, (lab, f, fm) in enumerate(res):
        label(ws, f"A{24 + i}", lab, bold=True)
        calc(ws, f"B{24 + i}", f, fm, bold=i in (2, 3))
    section(ws, "D4", "Profit by volume")
    header(ws, 5, 4, ["Units sold", "Revenue", "Total costs", "Profit"])
    for k in range(13):
        r = 6 + k
        calc(ws, f"D{r}", f'ROUND(IF(ISNUMBER($B$26),$B$26,$B$21)*{k}/6,0)', "int")
        calc(ws, f"E{r}", f"D{r}*$B$18", "money0")
        calc(ws, f"F{r}", f"$B$15+D{r}*$B$19", "money0")
        calc(ws, f"G{r}", f"E{r}-F{r}", "money0")
    flag_rule(ws, "G6:G18", "G6<0")
    flag_rule(ws, "G6:G18", "G6>=0", fill=FILL_GREEN)
    section(ws, "I4", "Price sensitivity")
    header(ws, 5, 9, ["Price", "Break-even units"])
    for k, pct in enumerate([-0.2, -0.15, -0.1, -0.05, 0, 0.05, 0.1, 0.15, 0.2]):
        r = 6 + k
        calc(ws, f"I{r}", f"$B$18*(1+{pct})", "money")
        calc(ws, f"J{r}", f'IF(I{r}-$B$19<=0,"n/a",$B$15/(I{r}-$B$19))', "num1")
    ch = LineChart()
    ch.title = "Revenue vs total costs"
    ch.height, ch.width = 8, 16
    ch.add_data(Reference(ws, min_col=5, max_col=6, min_row=5, max_row=18), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=4, min_row=6, max_row=18))
    ch.y_axis.numFmt = "$#,##0"
    ch.x_axis.title = "Units"
    ws.add_chart(ch, "D21")
    finalize(wb, path)
    F = sum(v for _, v in fixed)
    be = F / (85 - 38)
    return [("Break-Even", "B26", be), ("Break-Even", "B28", (F + 5000) / 47),
            ("Break-Even", "D12", round(be)), ("Break-Even", "B30", 400 * 47 - F)]


# ========================================================== 15 Sales tracker
def sales_tracker(path):
    wb = new_workbook()
    instructions(
        wb, "Sales Tracker & Dashboard",
        "Log sales by product and rep and see monthly revenue, gross profit and top sellers.",
        ["List products with list price and unit cost on the Products tab.",
         "Log each sale on the Sales tab: date, customer, product, rep, quantity and any discount %.",
         "Price and cost fill in from the product list; net sale and gross profit are calculated.",
         "The Dashboard shows the year on Settings by month, by product and by rep, with a chart."],
        [("Settings", "Dashboard year."), ("Products", "Product list with price and cost."),
         ("Sales", "One row per sale (or order line)."), ("Dashboard", "Monthly, product and rep summaries."),
         ("Lists", "Sales reps.")],
        ["Amounts are before HST.", "Product names on the Sales tab must match the Products tab (use the drop-down)."])
    st, s = _settings(wb, [("Dashboard year", YEAR, "0", None)])
    Y = s["Dashboard year"]
    reps = ["Alex", "Jordan", "Sam"]
    lw, lists = lists_sheet(wb, {"Sales Rep": reps})
    wp = wb.create_sheet("Products", 2)
    title(wp, "Products")
    prods = [("Standard Widget", "Widgets", 49.00, 21.00), ("Premium Widget", "Widgets", 89.00, 37.50),
             ("Installation", "Services", 150.00, 60.00), ("Maintenance Plan", "Services", 299.00, 90.00),
             ("Spare Parts Kit", "Parts", 24.00, 9.75)]
    pt = add_table(wp, [Col("Product", 22), Col("Category", 14), Col("List Price", 11, fmt="money"),
                        Col("Unit Cost", 11, fmt="money"),
                        Col("Margin %", 9, f="IFERROR(([List Price]-[Unit Cost])/[List Price],0)", fmt="pct")],
                   [dict(zip(["Product", "Category", "List Price", "Unit Cost"], p)) for p in prods], n=100)
    ws = wb.create_sheet("Sales", 3)
    title(ws, "Sales Log")
    PR, PP, PC = pt.rng("Product"), pt.rng("List Price"), pt.rng("Unit Cost")
    cols = [Col("Date", 12, fmt="date"), Col("Order #", 10), Col("Customer", 20),
            Col("Product", 20, dv=f"=Products!$A${pt.first}:$A${pt.last}"),
            Col("Sales Rep", 10, dv=lists["Sales Rep"]), Col("Qty", 7, fmt="int", total="sum"),
            Col("List Price", 10, f=f"IFERROR(INDEX({PP},MATCH([Product],{PR},0)),0)", fmt="money"),
            Col("Discount %", 9, fmt="pct"),
            Col("Net Sale", 12, f="ROUND([Qty]*[List Price]*(1-[Discount %]),2)", fmt="money", total="sum"),
            Col("Cost", 11, f=f"[Qty]*IFERROR(INDEX({PC},MATCH([Product],{PR},0)),0)", fmt="money", total="sum"),
            Col("Gross Profit", 12, f="[Net Sale]-[Cost]", fmt="money", total="sum"),
            Col("Margin %", 9, f="IFERROR([Gross Profit]/[Net Sale],0)", fmt="pct")]
    samples, exp = [], {"net": 0, "gp": 0, "mar": 0}
    for i in range(36):
        p = prods[i % 5]
        q = [3, 1, 2, 5, 1, 4][i % 6]
        disc = 0.1 if i % 7 == 0 else 0
        dte = d(YEAR, 1 + i // 3, 3 + (i % 3) * 9)
        samples.append({"Date": dte, "Order #": f"SO-{5001 + i}", "Customer": f"Customer {i % 9 + 1}",
                        "Product": p[0], "Sales Rep": reps[i % 3], "Qty": q, "Discount %": disc or None})
        net = round(q * p[2] * (1 - disc), 2)
        exp["net"] += net
        exp["gp"] += net - q * p[3]
        if dte.month == 3:
            exp["mar"] += net
    t = add_table(ws, cols, samples, n=1000)
    db = wb.create_sheet("Dashboard", 4)
    title(db, "Sales Dashboard", "For the year on the Settings tab")
    widths(db, {"A": 20, "B": 13, "C": 13, "D": 10, "F": 20, "G": 9, "H": 13, "I": 13})
    N, G, D, P, R, Q = (t.rng(h) for h in ["Net Sale", "Gross Profit", "Date", "Product", "Sales Rep", "Qty"])
    header(db, 4, 1, ["Month", "Net Sales", "Gross Profit", "Margin %"])
    for m in range(1, 13):
        r = 4 + m
        a, b = _month_bounds(Y, m)
        label(db, f"A{r}", MONTHS[m - 1])
        calc(db, f"B{r}", f'SUMIFS({N},{D},">="&{a},{D},"<"&{b})', "money0")
        calc(db, f"C{r}", f'SUMIFS({G},{D},">="&{a},{D},"<"&{b})', "money0")
        calc(db, f"D{r}", f"IFERROR(C{r}/B{r},0)", "pct")
    label(db, "A17", "Year", bold=True, fill=FILL_TOTAL)
    calc(db, "B17", "SUM(B5:B16)", "money0", bold=True, fill=FILL_TOTAL)
    calc(db, "C17", "SUM(C5:C16)", "money0", bold=True, fill=FILL_TOTAL)
    calc(db, "D17", "IFERROR(C17/B17,0)", "pct", bold=True, fill=FILL_TOTAL)
    yr = f'{D},">="&DATE({Y},1,1),{D},"<"&DATE({Y}+1,1,1)'
    header(db, 4, 6, ["Product", "Units", "Net Sales", "Gross Profit"])
    for i in range(15):
        r = 5 + i
        calc(db, f"F{r}", f'IF(Products!A{pt.first + i}="","",Products!A{pt.first + i})')
        calc(db, f"G{r}", f'IF(F{r}="","",SUMIFS({Q},{P},F{r},{yr}))', "int")
        calc(db, f"H{r}", f'IF(F{r}="","",SUMIFS({N},{P},F{r},{yr}))', "money0")
        calc(db, f"I{r}", f'IF(F{r}="","",SUMIFS({G},{P},F{r},{yr}))', "money0")
    header(db, 21, 6, ["Sales Rep", "Orders", "Net Sales", "Gross Profit"])
    for i in range(8):
        r = 22 + i
        calc(db, f"F{r}", f'IF(Lists!A{3 + i}="","",Lists!A{3 + i})')
        calc(db, f"G{r}", f'IF(F{r}="","",COUNTIFS({R},F{r},{yr}))', "int")
        calc(db, f"H{r}", f'IF(F{r}="","",SUMIFS({N},{R},F{r},{yr}))', "money0")
        calc(db, f"I{r}", f'IF(F{r}="","",SUMIFS({G},{R},F{r},{yr}))', "money0")
    ch = BarChart()
    ch.title = "Net sales and gross profit by month"
    ch.height, ch.width = 8, 16
    ch.add_data(Reference(db, min_col=2, max_col=3, min_row=4, max_row=16), titles_from_data=True)
    ch.set_categories(Reference(db, min_col=1, min_row=5, max_row=16))
    ch.y_axis.numFmt = "$#,##0"
    db.add_chart(ch, "A20")
    finalize(wb, path)
    return [("Dashboard", "B17", round(exp["net"], 2)), ("Dashboard", "C17", round(exp["gp"], 2)),
            ("Dashboard", "B7", round(exp["mar"], 2))]


# =========================================================== 16 Bills / AP
def bill_tracker(path):
    wb = new_workbook()
    instructions(
        wb, "Bill Tracker (Accounts Payable)",
        "Keep track of supplier bills, what's due this week, what's overdue, and how much you owe each vendor.",
        ["Enter each bill on the Bills tab: vendor, bill #, date, terms, category, total and HST portion.",
         "When you pay, enter the amount and date paid.",
         "Status shows Paid, Overdue, Due in 7 days or Open. Days until due counts down from the as-of date.",
         "The Summary tab shows what's due soon, overdue aging and balances by vendor."],
        [("Settings", "As-of date."), ("Bills", "One row per bill."),
         ("Summary", "Cash needed this week/month, aging, by vendor."), ("Lists", "Terms and categories.")],
        [AS_OF_NOTE])
    st, s = _settings(wb, [("As-of date", "=TODAY()", "date", "Overwrite with a date to freeze the report.")])
    asof = s["As-of date"]
    lw, lists = lists_sheet(wb, {"Terms (days)": [0, 10, 15, 30, 45, 60],
                                 "Category": ["Materials", "Subcontractor", "Rent", "Utilities", "Insurance",
                                              "Equipment", "Professional fees", "Other"]})
    ws = wb.create_sheet("Bills", 2)
    title(ws, "Bills")
    cols = [Col("Vendor", 22), Col("Bill #", 11), Col("Bill Date", 12, fmt="date"),
            Col("Terms (days)", 9, dv=lists["Terms (days)"], default=30),
            Col("Due Date", 12, f="[Bill Date]+[Terms (days)]", fmt="date"),
            Col("Category", 14, dv=lists["Category"]), Col("Bill Total", 12, fmt="money", total="sum"),
            Col("HST Portion", 11, fmt="money", total="sum"), Col("Amount Paid", 12, fmt="money", total="sum"),
            Col("Date Paid", 12, fmt="date"),
            Col("Balance", 12, f="[Bill Total]-[Amount Paid]", fmt="money", total="sum"),
            Col("Days Until Due", 9, f=f'IF([Balance]<=0,"",[Due Date]-{asof})', fmt="int"),
            Col("Status", 12, f=f'IF([Balance]<=0,"Paid",IF([Days Until Due]<0,"Overdue",IF([Days Until Due]<=7,"Due in 7 days","Open")))', align="center")]
    vendors = ["Kent Building Supplies", "Hydro One", "Intact Insurance", "Sunbelt Rentals", "Lakeview Plumbing"]
    samples, bal = [], 0
    for i in range(12):
        tot = [2486.00, 412.35, 1150.00, 870.20, 3390.00, 1977.50, 398.80, 640.00, 2825.00, 455.10, 1508.55, 720.00][i]
        paid = tot if i < 6 else (300 if i == 7 else None)
        samples.append({"Vendor": vendors[i % 5], "Bill #": f"B-{7001 + i}",
                        "Bill Date": d(YEAR, 7, 1) + dt.timedelta(days=11 * i), "Terms (days)": 30,
                        "Category": "Materials", "Bill Total": tot, "HST Portion": round(tot - tot / 1.13, 2),
                        "Amount Paid": paid, "Date Paid": d(YEAR, 7, 1) + dt.timedelta(days=11 * i + 20) if paid else None})
        bal += tot - (paid or 0)
    t = add_table(ws, cols, samples, n=300)
    flag_rule(ws, f"M{t.first}:M{t.last}", f'M{t.first}="Overdue"', bold=True)
    flag_rule(ws, f"M{t.first}:M{t.last}", f'M{t.first}="Due in 7 days"', fill=FILL_AMBER)
    flag_rule(ws, f"M{t.first}:M{t.last}", f'M{t.first}="Paid"', fill=FILL_GREEN)
    sm = wb.create_sheet("Summary", 3)
    title(sm, "Payables Summary")
    widths(sm, {"A": 30, "B": 15, "C": 15, "D": 15})
    B, DU = t.rng("Balance"), t.rng("Days Until Due")
    rows = [("Total owed", f"SUM({B})"),
            ("Overdue", f'SUMIFS({B},{DU},"<0")'),
            ("Due in next 7 days", f'SUMIFS({B},{DU},">=0",{DU},"<=7")'),
            ("Due in next 30 days", f'SUMIFS({B},{DU},">=0",{DU},"<=30")'),
            ("Due after 30 days", f'SUMIFS({B},{DU},">30")')]
    for i, (lab, f) in enumerate(rows):
        label(sm, f"A{4 + i}", lab, bold=True)
        calc(sm, f"B{4 + i}", f, "money")
    section(sm, "A10", "Overdue aging")
    for i, (lab, f) in enumerate([("1-30 days late", f'SUMIFS({B},{DU},"<0",{DU},">=-30")'),
                                  ("31-60 days late", f'SUMIFS({B},{DU},"<-30",{DU},">=-60")'),
                                  ("Over 60 days late", f'SUMIFS({B},{DU},"<-60")')]):
        label(sm, f"A{11 + i}", lab)
        calc(sm, f"B{11 + i}", f, "money")
    section(sm, "A15", "By vendor (type vendor names)")
    header(sm, 16, 1, ["Vendor", "Billed", "Paid", "Balance"])
    for i in range(15):
        r = 17 + i
        inp(sm, f"A{r}", vendors[i] if i < len(vendors) else None)
        calc(sm, f"B{r}", f'IF(A{r}="","",SUMIFS({t.rng("Bill Total")},{t.rng("Vendor")},A{r}))', "money")
        calc(sm, f"C{r}", f'IF(A{r}="","",SUMIFS({t.rng("Amount Paid")},{t.rng("Vendor")},A{r}))', "money")
        calc(sm, f"D{r}", f'IF(A{r}="","",SUMIFS({B},{t.rng("Vendor")},A{r}))', "money")
    label(sm, "A32", "Check: overdue + due later = total owed", font=F_SUB)
    calc(sm, "B32", "B5+SUMIFS(" + B + "," + DU + ',">=0")', "money")
    finalize(wb, path)
    return [("Summary", "B4", round(bal, 2)), ("Summary", "B32", ("=", "Summary", "B4"))]


# ======================================================= 17 Loan amortization
def loan_amortization(path):
    wb = new_workbook()
    instructions(
        wb, "Loan & Mortgage Amortization",
        "Full payment schedule for any loan or mortgage, including extra payments and Canadian semi-annual compounding.",
        ["On the Loan tab, enter the amount, annual interest rate, term, payments per year and first payment date.",
         "Set compounding periods per year: 2 for Canadian fixed-rate mortgages, 12 for most other loans.",
         "Optionally add an extra payment each period to see how much faster you pay it off.",
         "The schedule fills automatically; the summary shows the payment, total interest and payoff date."],
        [("Loan", "Inputs, summary and the full amortization schedule (up to 780 payments).")],
        ["Periodic rate = (1 + annual rate / compounding periods)^(compounding periods / payments per year) - 1.",
         "Payments per year: 12 = monthly, 26 = bi-weekly, 52 = weekly.",
         "'Interest saved' compares against the same loan with no extra payments."])
    ws = wb.create_sheet("Loan")
    title(ws, "Loan & Mortgage Amortization")
    widths(ws, {"A": 32, "B": 15, "C": 4, "D": 30, "E": 15})
    ins = [("Loan amount", 350000, "money0"), ("Annual interest rate", 0.0529, "0.00%"),
           ("Term (years)", 25, "0"), ("Payments per year", 12, "0"),
           ("Compounding periods per year", 2, "0"), ("First payment date", d(YEAR, 12, 1), "date"),
           ("Extra payment per period", 200, "money")]
    for i, (lab, v, fm) in enumerate(ins):
        label(ws, f"A{4 + i}", lab, bold=True)
        inp(ws, f"B{4 + i}", v, fm)
    add_list(ws, "B7", "12,26,52")
    add_list(ws, "B8", "1,2,4,12,26,52,365")
    outs = [("Periodic interest rate", "(1+B5/B8)^(B8/B7)-1", "0.0000%"),
            ("Number of scheduled payments", "B6*B7", "0"),
            ("Scheduled payment", "IF(B4<=0,0,IF(E4=0,B4/E5,PMT(E4,E5,-B4)))", "money"),
            ("Payments actually needed", "COUNT(A16:A795)", "0"),
            ("Payoff date", 'IF(E7=0,"",INDEX(B16:B795,E7))', "date"),
            ("Total interest", "SUM(D16:D795)", "money"),
            ("Total paid", "SUM(E16:E795)+SUM(F16:F795)", "money"),
            ("Interest saved by extra payments", "MAX(0,E5*E6-B4-E9)", "money"),
            ("Schedule check", 'IF(E5>780,"Term too long for 780 rows","OK")', None)]
    for i, (lab, f, fm) in enumerate(outs):
        label(ws, f"D{4 + i}", lab, bold=True)
        calc(ws, f"E{4 + i}", f, fm, bold=i in (2, 5))
    header(ws, 15, 1, ["#", "Payment Date", "Beginning Balance", "Interest", "Scheduled Payment",
                       "Extra Payment", "Principal", "Ending Balance", "Cumulative Interest"])
    for c, w in zip("ABCDEFGHI", [6, 12, 15, 12, 13, 12, 13, 15, 14]):
        ws.column_dimensions[c].width = max(ws.column_dimensions[c].width or 0, w)
    ws.column_dimensions["A"].width = 32
    for r in range(16, 796):
        p = r - 1
        if r == 16:
            calc(ws, f"A{r}", 'IF(AND($B$4>0,$E$5>0),1,"")', "0")
            calc(ws, f"C{r}", 'IF(A16="","",$B$4)', "money")
            calc(ws, f"I{r}", 'IF(A16="","",D16)', "money")
        else:
            calc(ws, f"A{r}", f'IF(A{p}="","",IF(OR(H{p}<=0.005,A{p}>=780),"",A{p}+1))', "0")
            calc(ws, f"C{r}", f'IF(A{r}="","",H{p})', "money")
            calc(ws, f"I{r}", f'IF(A{r}="","",I{p}+D{r})', "money")
        calc(ws, f"B{r}", f'IF(A{r}="","",IF($B$7=12,EDATE($B$9,A{r}-1),$B$9+ROUND(365/$B$7,0)*(A{r}-1)))', "date")
        calc(ws, f"D{r}", f'IF(A{r}="","",C{r}*$E$4)', "money")
        calc(ws, f"E{r}", f'IF(A{r}="","",MIN($E$6,C{r}+D{r}))', "money")
        calc(ws, f"F{r}", f'IF(A{r}="","",MIN($B$10,C{r}+D{r}-E{r}))', "money")
        calc(ws, f"G{r}", f'IF(A{r}="","",E{r}+F{r}-D{r})', "money")
        calc(ws, f"H{r}", f'IF(A{r}="","",MAX(0,C{r}-G{r}))', "money")
    ws.freeze_panes = "A16"
    finalize(wb, path)
    P, rate, n, extra = 350000, 0.0529, 300, 200
    rp = (1 + rate / 2) ** (2 / 12) - 1
    pmt = P * rp / (1 - (1 + rp) ** -n)
    bal, k, ti = P, 0, 0
    while k < 780:
        k += 1
        it = bal * rp
        pay = min(pmt, bal + it)
        ex = min(extra, bal + it - pay)
        ti += it
        bal = max(0, bal - (pay + ex - it))
        if bal <= 0.005:
            break
    return [("Loan", "E6", pmt), ("Loan", "E7", k), ("Loan", "E9", ti),
            ("Loan", "E11", n * pmt - P - ti)]


# ========================================================== 18 Project tracker
def project_tracker(path):
    wb = new_workbook()
    instructions(
        wb, "Project & Task Tracker",
        "Plan tasks with owners and dates, track progress, flag overdue work, and see a simple Gantt chart.",
        ["On Settings, enter the project start date (the Gantt timeline starts that week).",
         "Add tasks on the Tasks tab with owner, priority, start date, due date and status.",
         "Update % Done and status as work progresses. Overdue and due-soon tasks are flagged.",
         "The bars to the right show each task's dates by week. The Summary tab shows progress by status and owner."],
        [("Settings", "Project start date and as-of date."), ("Tasks", "Task list with flags and a 16-week Gantt view."),
         ("Summary", "Overall % complete, status counts, open tasks by owner."), ("Lists", "Owners, statuses, priorities.")],
        [AS_OF_NOTE, "Overall % complete is weighted by each task's working days.",
         "Tasks marked Done count as 100% regardless of the % Done entered."])
    st, s = _settings(wb, [("Project start date", d(YEAR, 9, 7), "date", "Gantt starts this week."),
                           ("As-of date", "=TODAY()", "date", "Overwrite with a date to freeze the report."),
                           ("Due-soon window (days)", 3, "0", None)])
    ps, asof, soon = s["Project start date"], s["As-of date"], s["Due-soon window (days)"]
    owners = ["Alex", "Jordan", "Sam", "Priya"]
    statuses = ["Not started", "In progress", "Blocked", "Done"]
    lw, lists = lists_sheet(wb, {"Owner": owners, "Status": statuses, "Priority": ["High", "Medium", "Low"]})
    ws = wb.create_sheet("Tasks", 2)
    title(ws, "Tasks")
    cols = [Col("ID", 5), Col("Task", 28), Col("Phase", 12), Col("Owner", 10, dv=lists["Owner"]),
            Col("Priority", 9, dv=lists["Priority"], default="Medium"), Col("Start", 11, fmt="date"),
            Col("Due", 11, fmt="date"), Col("Status", 11, dv=lists["Status"], default="Not started"),
            Col("% Done", 8, fmt="0%"),
            Col("Work Days", 7, f="IF(OR([Start]=\"\",[Due]=\"\"),0,NETWORKDAYS([Start],[Due]))", fmt="0", total="sum"),
            Col("Effective %", 8, f='IF([Status]="Done",1,N([% Done]))', fmt="0%"),
            Col("Weighted Done", 7, f="[Work Days]*[Effective %]", fmt="num1", total="sum"),
            Col("Days Left", 7, f=f'IF(OR([Status]="Done",[Due]=""),"",[Due]-{asof})', fmt="0"),
            Col("Flag", 10, f=f'IF(OR([Status]="Done",[Due]=""),"",IF({asof}>[Due],"OVERDUE",IF([Due]-{asof}<={soon},"DUE SOON",IF([Status]="Blocked","BLOCKED",""))))', align="center")]
    tasks = [("Kick-off meeting", "Plan", 0, 0, "Done", 1), ("Requirements", "Plan", 1, 6, "Done", 1),
             ("Design mock-ups", "Design", 7, 16, "Done", 1), ("Client review", "Design", 17, 20, "Done", 1),
             ("Build phase 1", "Build", 21, 41, "In progress", 0.6), ("Build phase 2", "Build", 42, 62, "Not started", 0),
             ("Testing", "Test", 55, 69, "Not started", 0), ("Training", "Launch", 70, 74, "Not started", 0),
             ("Go-live", "Launch", 77, 77, "Not started", 0), ("Supplier contract", "Plan", 3, 10, "Blocked", 0.3)]
    samples = []
    for i, (tk, ph, a, b, stt, pc) in enumerate(tasks):
        samples.append({"ID": i + 1, "Task": tk, "Phase": ph, "Owner": owners[i % 4], "Priority": "High" if i < 3 else "Medium",
                        "Start": d(YEAR, 9, 7) + dt.timedelta(days=a), "Due": d(YEAR, 9, 7) + dt.timedelta(days=b),
                        "Status": stt, "% Done": pc})
    t = add_table(ws, cols, samples, n=200, freeze_col="C")
    flag_rule(ws, f"N{t.first}:N{t.last}", f'N{t.first}="OVERDUE"', bold=True)
    flag_rule(ws, f"N{t.first}:N{t.last}", f'N{t.first}="DUE SOON"', fill=FILL_AMBER)
    flag_rule(ws, f"N{t.first}:N{t.last}", f'N{t.first}="BLOCKED"', fill=FILL_AMBER)
    gc = len(cols) + 2
    label(ws, f"{GL(gc)}{t.totals_row}", "Week of:", bold=True)
    for k in range(16):
        L = GL(gc + k)
        ws.column_dimensions[L].width = 6.5
        header(ws, t.header_row, gc + k, [None], height=32)
        calc(ws, f"{L}{t.header_row}", f"{ps}-WEEKDAY({ps},3)+7*{k}", "mmm d", fill=None, align="center")
        hc = ws[f"{L}{t.header_row}"]
        from .common import F_HEADER, FILL_HEADER
        hc.font, hc.fill = F_HEADER, FILL_HEADER
        hc.alignment = Alignment(text_rotation=90, horizontal="center")
        for r in range(t.first, t.last + 1):
            calc(ws, f"{L}{r}", f'IF(OR($F{r}="",$G{r}=""),"",IF(AND({L}${t.header_row}<=$G{r},{L}${t.header_row}+6>=$F{r}),1,""))', ";;;", fill=None)
    grng = f"{GL(gc)}{t.first}:{GL(gc + 15)}{t.last}"
    tl = f"{GL(gc)}{t.first}"
    flag_rule(ws, grng, f'AND({tl}=1,$H{t.first}="Done")', fill=PatternFill("solid", fgColor="70AD47"))
    flag_rule(ws, grng, f"{tl}=1", fill=PatternFill("solid", fgColor="4472C4"))
    ws.row_dimensions[t.header_row].height = 48
    sm = wb.create_sheet("Summary", 3)
    title(sm, "Project Summary")
    widths(sm, {"A": 24, "B": 12, "C": 14})
    label(sm, "A4", "Overall % complete", bold=True)
    calc(sm, "B4", f"IFERROR(Tasks!{t.total('Weighted Done')}/Tasks!{t.total('Work Days')},0)", "0.0%", bold=True)
    label(sm, "A5", "Overdue tasks", bold=True)
    calc(sm, "B5", f'COUNTIF({t.rng("Flag")},"OVERDUE")', "0")
    header(sm, 7, 1, ["Status", "# Tasks"])
    for i in range(len(statuses)):
        calc(sm, f"A{8 + i}", f"Lists!C{3 + i}")
        calc(sm, f"B{8 + i}", f'COUNTIF({t.rng("Status")},A{8 + i})', "0")
    header(sm, 13, 1, ["Owner", "Open Tasks", "Overdue"])
    for i in range(10):
        r = 14 + i
        calc(sm, f"A{r}", f'IF(Lists!A{3 + i}="","",Lists!A{3 + i})')
        calc(sm, f"B{r}", f'IF(A{r}="","",COUNTIFS({t.rng("Owner")},A{r},{t.rng("Status")},"<>Done"))', "0")
        calc(sm, f"C{r}", f'IF(A{r}="","",COUNTIFS({t.rng("Owner")},A{r},{t.rng("Flag")},"OVERDUE"))', "0")
    finalize(wb, path)

    def nwd(a, b):
        return sum(1 for k in range((b - a).days + 1) if (a + dt.timedelta(days=k)).weekday() < 5)
    wdays = [nwd(dt.date(YEAR, 9, 7) + dt.timedelta(days=a), dt.date(YEAR, 9, 7) + dt.timedelta(days=b))
             for _, _, a, b, _, _ in tasks]
    eff = [1 if stt == "Done" else pc for *_, stt, pc in tasks]
    pct = sum(w * e for w, e in zip(wdays, eff)) / sum(wdays)
    return [("Summary", "B4", pct), ("Summary", "B11", 4), ("Tasks", f"{GL(gc)}{t.first}", 1)]


# ========================================================== 19 Shift scheduler
def shift_scheduler(path):
    wb = new_workbook()
    instructions(
        wb, "Weekly Shift Schedule & Labour Cost",
        "Plan staff shifts for the week and see scheduled hours and labour cost by day and by person.",
        ["List staff with role, hourly rate and max weekly hours on the Staff tab.",
         "On Settings, set the week start date and the unpaid-break rule.",
         "On the Schedule tab, pick an employee for each row and type start/end times for each day they work.",
         "Hours, labour cost per day and per person calculate automatically; over-max rows are flagged."],
        [("Settings", "Week start and break rule."), ("Staff", "Team list, rates and scheduled hours."),
         ("Schedule", "The weekly grid with daily hours and labour cost.")],
        ["Ontario ESA requires a 30-minute eating period after 5 hours of work (can be unpaid). Adjust the rule on Settings.",
         "Overnight shifts (end time earlier than start) are handled.",
         "Labour cost is wages only - add a burden % for CPP/EI/WSIB/vacation pay if you want a fuller picture."])
    st, s = _settings(wb, [("Week start date", d(YEAR, 11, 9), "date", None),
                           ("Unpaid break after (hours)", 5, "num1", "Shifts longer than this get a break deducted."),
                           ("Unpaid break length (minutes)", 30, "0", None),
                           ("Labour burden %", 0.12, "pct", "Optional: CPP/EI/WSIB/vacation on top of wages.")])
    wk, bt, bl, burden = (s[k] for k in ["Week start date", "Unpaid break after (hours)",
                                          "Unpaid break length (minutes)", "Labour burden %"])
    wst = wb.create_sheet("Staff", 2)
    wsch = wb.create_sheet("Schedule", 2)
    title(wst, "Staff")
    staff = [("Maria Lopez", "Supervisor", 26.00, 44), ("Dev Sharma", "Cashier", 18.50, 40),
             ("Chris Taylor", "Cook", 21.00, 40), ("Aisha Khan", "Server", 17.60, 32),
             ("Ben Okafor", "Dishwasher", 17.60, 24)]
    sch_total = "Schedule!$X$6:$X$45"
    sch_emp = "Schedule!$A$6:$A$45"
    stt = add_table(wst, [Col("Employee", 20), Col("Role", 14), Col("Hourly Rate", 11, fmt="money"),
                          Col("Max Hours / Week", 10, fmt="num1"),
                          Col("Scheduled Hours", 10, f=f"SUMIF({sch_emp},[Employee],{sch_total})", fmt="num2"),
                          Col("Over Max?", 9, f='IF([Scheduled Hours]>[Max Hours / Week],"OVER","")', align="center")],
                    [dict(zip(["Employee", "Role", "Hourly Rate", "Max Hours / Week"], x)) for x in staff], n=60)
    flag_rule(wst, f"F{stt.first}:F{stt.last}", f'F{stt.first}="OVER"', bold=True)
    title(wsch, "Weekly Schedule", "Type times like 9:00 AM / 5:30 PM. Leave blank for days off.")
    widths(wsch, {"A": 20, "B": 12})
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    header(wsch, 4, 1, ["Employee", "Role"], height=20)
    header(wsch, 5, 1, ["", ""], height=20)
    for k in range(7):
        a = 3 + 2 * k
        header(wsch, 4, a, [None, None], height=20)
        wsch.cell(row=4, column=a).value = f'=TEXT({wk}+{k},"ddd mmm d")'
        wsch.merge_cells(start_row=4, start_column=a, end_row=4, end_column=a + 1)
        header(wsch, 5, a, ["Start", "End"], height=20)
        wsch.column_dimensions[GL(a)].width = 9
        wsch.column_dimensions[GL(a + 1)].width = 9
    header(wsch, 4, 17, ["Hours"] + [""] * 6, height=20)
    wsch.merge_cells("Q4:W4")
    header(wsch, 5, 17, days, height=20)
    header(wsch, 4, 24, ["Total Hours", "Rate", "Wages", "Max Hrs", "Flag"], height=20)
    header(wsch, 5, 24, ["", "", "", "", ""], height=20)
    for c in range(17, 29):
        wsch.column_dimensions[GL(c)].width = 8 if c < 24 else 10
    SR, SN, SM, SRole = stt.rng("Hourly Rate"), stt.rng("Employee"), stt.rng("Max Hours / Week"), stt.rng("Role")
    plan = {"Maria Lopez": [(8, 16.5)] * 5, "Dev Sharma": [None, (10, 18), (10, 18), (10, 18), (12, 20), (9, 17)],
            "Chris Taylor": [(11, 19.5)] * 4 + [None, (11, 21)], "Aisha Khan": [None, None, (16, 23)] + [(16, 23)] * 3,
            "Ben Okafor": [None] * 4 + [(17, 23), (17, 23), (10, 15)]}
    exp_hours = 0
    for i in range(40):
        r = 6 + i
        name = staff[i][0] if i < len(staff) else None
        inp(wsch, f"A{r}", name)
        calc(wsch, f"B{r}", f'IF(A{r}="","",IFERROR(INDEX({SRole},MATCH(A{r},{SN},0)),""))')
        sched = plan.get(name, []) if name else []
        for k in range(7):
            a = 3 + 2 * k
            sl = sched[k] if k < len(sched) else None
            tm = (lambda h: dt.time(int(h), int(round((h % 1) * 60))))
            inp(wsch, f"{GL(a)}{r}", tm(sl[0]) if sl else None, "time")
            inp(wsch, f"{GL(a + 1)}{r}", tm(sl[1]) if sl else None, "time")
            S, E = f"{GL(a)}{r}", f"{GL(a + 1)}{r}"
            calc(wsch, f"{GL(17 + k)}{r}",
                 f'IF(OR({S}="",{E}=""),0,ROUND(MOD({E}-{S},1)*24,4)-IF(ROUND(MOD({E}-{S},1)*24,4)>{bt},{bl}/60,0))', "num2")
            if sl:
                dur = sl[1] - sl[0]
                exp_hours += dur - (0.5 if dur > 5 else 0)
        calc(wsch, f"X{r}", f"SUM(Q{r}:W{r})", "num2", bold=True)
        calc(wsch, f"Y{r}", f'IF(A{r}="",0,IFERROR(INDEX({SR},MATCH(A{r},{SN},0)),0))', "money")
        calc(wsch, f"Z{r}", f"X{r}*Y{r}", "money")
        calc(wsch, f"AA{r}", f'IF(A{r}="","",IFERROR(INDEX({SM},MATCH(A{r},{SN},0)),""))', "num1")
        calc(wsch, f"AB{r}", f'IF(A{r}="","",IF(AND(ISNUMBER(AA{r}),X{r}>AA{r}),"OVER MAX",""))', align="center")
    add_list(wsch, "A6:A45", f"=Staff!$A${stt.first}:$A${stt.last}")
    flag_rule(wsch, "AB6:AB45", 'AB6="OVER MAX"', bold=True)
    for lab, r, fn in [("Hours", 46, lambda L: f"SUM({L}6:{L}45)"),
                       ("Wages", 47, lambda L: f"SUMPRODUCT({L}6:{L}45,$Y$6:$Y$45)"),
                       ("Wages + burden", 48, lambda L: f"{L}47*(1+{burden})")]:
        label(wsch, f"A{r}", lab, bold=True, fill=FILL_TOTAL)
        for c in list(range(17, 25)):
            L = GL(c)
            calc(wsch, f"{L}{r}", fn(L), "num2" if r == 46 else "money0", bold=True, fill=FILL_TOTAL)
    calc(wsch, "Z46", "SUM(Z6:Z45)", "money0", bold=True, fill=FILL_TOTAL)
    wsch.freeze_panes = "C6"
    finalize(wb, path)
    rates = {n: r for n, _, r, _ in staff}
    wages = 0
    for n, sch in plan.items():
        for sl in sch:
            if sl:
                dur = sl[1] - sl[0]
                wages += (dur - (0.5 if dur > 5 else 0)) * rates[n]
    return [("Schedule", "X46", exp_hours), ("Schedule", "Z46", round(wages, 2)),
            ("Schedule", "X47", ("=", "Schedule", "Z46")), ("Staff", stt.cell("Scheduled Hours", 0), 5 * 8)]


# ============================================================== 20 Petty cash
def petty_cash(path):
    wb = new_workbook()
    instructions(
        wb, "Petty Cash Log",
        "Track every dollar in and out of the petty cash box, with a running balance and reconciliation.",
        ["On Settings, enter the float (the amount the box is topped up to) and the custodian.",
         "Log each payout with a voucher number, category and who received it. Log top-ups as Cash In.",
         "The running balance updates on every row.",
         "When you count the box, enter the counted cash on the Summary tab to see any over/short."],
        [("Settings", "Float and custodian."), ("Log", "Every payout and top-up with running balance."),
         ("Summary", "Balance, top-up needed, spending by category, cash count reconciliation."),
         ("Lists", "Categories.")],
        ["Keep a receipt or signed voucher for every payout.",
         "Top-up needed = float - current balance (the cheque to write to refill the box)."])
    st, s = _settings(wb, [("Petty cash float", 300, "money", "Amount the box is topped up to."),
                           ("Custodian", "Office Manager", None, None)])
    flt = s["Petty cash float"]
    cats = ["Office supplies", "Postage & courier", "Meals & coffee", "Parking & transit", "Cleaning", "Other"]
    lw, lists = lists_sheet(wb, {"Category": cats})
    ws = wb.create_sheet("Log", 2)
    title(ws, "Petty Cash Log", "Balance starts from the float on Settings.")
    cols = [Col("Date", 12, fmt="date"), Col("Voucher #", 10), Col("Description", 26),
            Col("Category", 16, dv=lists["Category"]), Col("Paid To / Received By", 18),
            Col("Cash In", 10, fmt="money", total="sum"), Col("Cash Out", 10, fmt="money", total="sum"),
            Col("HST Included", 10, fmt="money", total="sum"),
            Col("Balance", 11, f=f"{flt}+SUM([^Cash In])-SUM([^Cash Out])", fmt="money")]
    entries = [("Printer paper", "Office supplies", None, 24.86), ("Canada Post - parcel", "Postage & courier", None, 18.40),
               ("Coffee for client meeting", "Meals & coffee", None, 32.15), ("Parking - downtown", "Parking & transit", None, 14.00),
               ("Cleaning supplies", "Cleaning", None, 41.27), ("Top-up from bank", None, 130.68, None),
               ("Courier - Purolator", "Postage & courier", None, 22.60), ("Sticky notes & pens", "Office supplies", None, 11.29),
               ("Lunch - staff training", "Meals & coffee", None, 68.90), ("TTC tokens", "Parking & transit", None, 13.20)]
    samples = [{"Date": d(YEAR, 10, 1) + dt.timedelta(days=2 * i), "Voucher #": f"PC-{101 + i}", "Description": de,
                "Category": c or "Other", "Paid To / Received By": "J. Smith", "Cash In": ci, "Cash Out": co,
                "HST Included": round(co - co / 1.13, 2) if co else None} for i, (de, c, ci, co) in enumerate(entries)]
    samples[5]["Category"] = None
    t = add_table(ws, cols, samples, n=300, key="Date")
    sm = wb.create_sheet("Summary", 3)
    title(sm, "Petty Cash Summary")
    widths(sm, {"A": 30, "B": 14})
    rows = [("Float", f"{flt}", "money"), ("Total cash in (top-ups)", f"SUM({t.rng('Cash In')})", "money"),
            ("Total cash out", f"SUM({t.rng('Cash Out')})", "money"), ("Current balance", "B4+B5-B6", "money"),
            ("Top-up needed to restore float", "MAX(0,B4-B7)", "money")]
    for i, (lab, f, fm) in enumerate(rows):
        label(sm, f"A{4 + i}", lab, bold=True)
        calc(sm, f"B{4 + i}", f, fm, bold=i == 3)
    section(sm, "A10", "Cash count")
    label(sm, "A11", "Cash counted in box", bold=True)
    inp(sm, "B11", 172.01, "money")
    label(sm, "A12", "Over / (short)", bold=True)
    calc(sm, "B12", "B11-B7", "money", bold=True)
    flag_rule(sm, "B12", "ROUND(B12,2)<>0")
    header(sm, 14, 1, ["Category", "Spent"])
    for i in range(len(cats) + 10):
        r = 15 + i
        calc(sm, f"A{r}", f'IF(Lists!A{3 + i}="","",Lists!A{3 + i})')
        calc(sm, f"B{r}", f'IF(A{r}="","",SUMIFS({t.rng("Cash Out")},{t.rng("Category")},A{r}))', "money")
    finalize(wb, path)
    out = sum(co for *_, co in entries if co)
    inn = sum(ci for _, _, ci, _ in entries if ci)
    bal = round(300 + inn - out, 2)
    return [("Summary", "B7", bal), ("Log", t.cell("Balance", 9), bal), ("Summary", "B12", round(172.01 - bal, 2))]


TEMPLATES_B = [
    ("11-expense-tracker", expense_tracker, "Business expenses with HST split, receipt flags and a category-by-month summary."),
    ("12-mileage-log", mileage_log, "CRA-style vehicle logbook with business-use % and tiered per-km allowance."),
    ("13-profit-and-loss", profit_loss, "12-month income statement with gross margin, operating income, tax estimate and net margin."),
    ("14-break-even-analysis", break_even, "Break-even units and revenue, target-profit volume, margin of safety, sensitivity table and chart."),
    ("15-sales-tracker", sales_tracker, "Sales log with product price/cost lookup and a dashboard by month, product and rep."),
    ("16-bill-tracker", bill_tracker, "Accounts payable: supplier bills, due-in-7-days and overdue flags, aging and balances by vendor."),
    ("17-loan-amortization", loan_amortization, "Loan/mortgage schedule with extra payments, Canadian semi-annual compounding and payoff date."),
    ("18-project-tracker", project_tracker, "Task list with owners, overdue flags, weighted % complete and a 16-week Gantt view."),
    ("19-shift-scheduler", shift_scheduler, "Weekly staff schedule with start/end times, break rule, hours, wages and over-max flags."),
    ("20-petty-cash-log", petty_cash, "Petty cash box log with running balance, top-up amount and cash-count reconciliation."),
]
