"""Templates 21-30."""

import datetime as dt

from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.utils import get_column_letter as GL

from .common import (AS_OF_NOTE, FILL_AMBER, FILL_GREEN, FILL_GREY, FILL_RED, FILL_TOTAL, F_SUB, YEAR,
                     Col, add_list, add_table, calc, d, finalize, flag_rule, header, inp, instructions,
                     label, lists_sheet, new_workbook, section, title, widths)
from .templates_a import MONTHS, _settings


# ===================================================== 21 Fixed asset register
def fixed_assets(path):
    wb = new_workbook()
    instructions(
        wb, "Fixed Asset Register & Depreciation",
        "List your equipment, vehicles and other assets and see depreciation and net book value for any year.",
        ["On Settings, choose the report year.",
         "On Assets, enter each asset's purchase date, cost, salvage value and useful life.",
         "Pick a method: Straight-line (equal amount each year) or Declining balance (enter the annual rate).",
         "Depreciation for the year, accumulated depreciation and net book value calculate automatically."],
        [("Settings", "Report year."), ("Assets", "Asset register with depreciation."),
         ("Summary", "Cost, depreciation and book value by category."), ("Lists", "Categories and methods.")],
        ["Depreciation is counted in full months from the purchase date to year end.",
         "This is book (accounting) depreciation. Tax depreciation in Canada uses CCA classes, the half-year/"
         "AIIP rules and pooled balances - your accountant handles that on Schedule 8 / T2125.",
         "Declining-balance rates often mirror CCA rates: Class 8 equipment 20%, Class 10 vehicles 30%, "
         "Class 50 computers 55%."])
    st, s = _settings(wb, [("Report year", YEAR, "0", None)])
    Y = s["Report year"]
    lw, lists = lists_sheet(wb, {"Category": ["Equipment", "Vehicles", "Computers", "Furniture",
                                              "Leasehold improvements", "Other"],
                                 "Method": ["Straight-line", "Declining balance"]})
    ws = wb.create_sheet("Assets", 2)
    title(ws, "Fixed Asset Register", "Depreciation for the report year on Settings")

    def months(yr):
        return f'IF([Purchase Date]>DATE({yr},12,31),0,DATEDIF([Purchase Date],DATE({yr},12,31)+1,"m"))'

    def accum(mcol):
        return (f'IF([Method]="Declining balance",[Cost]-MAX([Salvage Value],[Cost]*(1-[DB Rate])^({mcol}/12)),'
                f'MIN([Cost]-[Salvage Value],([Cost]-[Salvage Value])/[Useful Life (yrs)]*{mcol}/12))')
    cols = [Col("Asset ID", 9), Col("Description", 26), Col("Category", 14, dv=lists["Category"]),
            Col("Purchase Date", 12, fmt="date"), Col("Cost", 12, fmt="money", total="sum"),
            Col("Salvage Value", 11, fmt="money"), Col("Useful Life (yrs)", 9, fmt="0"),
            Col("Method", 15, dv=lists["Method"], default="Straight-line"), Col("DB Rate", 8, fmt="0%"),
            Col("Months to Prior YE", 9, f=months(f"{Y}-1"), fmt="0"),
            Col("Months to Report YE", 9, f=months(Y), fmt="0"),
            Col("Accum. Dep. Prior YE", 12, f=accum("[Months to Prior YE]"), fmt="money", total="sum"),
            Col("Accum. Dep. Report YE", 12, f=accum("[Months to Report YE]"), fmt="money", total="sum"),
            Col("Depreciation This Year", 12, f="[Accum. Dep. Report YE]-[Accum. Dep. Prior YE]", fmt="money", total="sum"),
            Col("Net Book Value", 12, f="[Cost]-[Accum. Dep. Report YE]", fmt="money", total="sum"),
            Col("Disposed? (Y/N)", 9, dv="Y,N", default="N", align="center"), Col("Notes", 20)]
    assets = [("FA-001", "Excavator - Kubota KX040", "Equipment", d(2024, 1, 1), 68000, 8000, 10, "Straight-line", None),
              ("FA-002", "Ford Transit van", "Vehicles", d(2025, 4, 15), 52000, 0, 6, "Declining balance", 0.30),
              ("FA-003", "Laptops (x4)", "Computers", d(YEAR, 2, 1), 7200, 0, 3, "Declining balance", 0.55),
              ("FA-004", "Office furniture", "Furniture", d(2022, 7, 1), 9500, 500, 7, "Straight-line", None),
              ("FA-005", "Shop renovation", "Leasehold improvements", d(2023, 9, 1), 24000, 0, 5, "Straight-line", None)]
    samples = [dict(zip(["Asset ID", "Description", "Category", "Purchase Date", "Cost", "Salvage Value",
                         "Useful Life (yrs)", "Method", "DB Rate"], a)) for a in assets]
    t = add_table(ws, cols, samples, n=200)
    sm = wb.create_sheet("Summary", 3)
    title(sm, "Asset Summary", "For the report year on Settings")
    header(sm, 4, 1, ["Category", "Cost", "Depreciation This Year", "Accumulated", "Net Book Value"])
    widths(sm, {"A": 24, "B": 14, "C": 14, "D": 14, "E": 14})
    for i in range(16):
        r = 5 + i
        calc(sm, f"A{r}", f'IF(Lists!A{3 + i}="","",Lists!A{3 + i})')
        for L, h in zip("BCDE", ["Cost", "Depreciation This Year", "Accum. Dep. Report YE", "Net Book Value"]):
            calc(sm, f"{L}{r}", f'IF($A{r}="","",SUMIFS({t.rng(h)},{t.rng("Category")},$A{r}))', "money")
    label(sm, "A21", "Total", bold=True, fill=FILL_TOTAL)
    for L in "BCDE":
        calc(sm, f"{L}21", f"SUM({L}5:{L}20)", "money", bold=True, fill=FILL_TOTAL)
    finalize(wb, path)

    def mo(pd, yr):
        end = dt.date(yr + 1, 1, 1)
        if pd > dt.date(yr, 12, 31):
            return 0
        m = (end.year - pd.year) * 12 + end.month - pd.month - (1 if end.day < pd.day else 0)
        return m

    def acc(a, yr):
        _, _, _, pd, cost, salv, life, meth, rate = a
        m = mo(pd, yr)
        if meth == "Declining balance":
            return cost - max(salv, cost * (1 - rate) ** (m / 12))
        return min(cost - salv, (cost - salv) / life * m / 12)
    dep = sum(acc(a, YEAR) - acc(a, YEAR - 1) for a in assets)
    nbv = sum(a[4] - acc(a, YEAR) for a in assets)
    return [("Assets", t.cell("Depreciation This Year", 0), 6000), ("Summary", "C21", dep),
            ("Summary", "E21", nbv), ("Assets", t.cell("Net Book Value", 3), 9500 - min(9000, 9000 / 7 * mo(d(2022, 7, 1), YEAR) / 12))]


# ======================================================= 22 Pricing calculator
def pricing_calculator(path):
    wb = new_workbook()
    instructions(
        wb, "Pricing & Margin Calculator",
        "Set prices from your costs and a target margin, and compare markup vs margin at a glance.",
        ["On Settings, set your HST rate and price rounding (e.g. 0.05 rounds up to the next 5 cents).",
         "On Products, enter material, labour and overhead cost per unit and your target margin.",
         "The suggested price is calculated. Type your actual price in 'Your Price' to override it.",
         "Check markup, margin and profit per unit. Red margin = below target."],
        [("Settings", "HST rate and rounding."), ("Products", "Cost build-up and pricing per product."),
         ("Margin vs Markup", "Quick reference table - they are not the same thing!")],
        ["Margin = profit / price. Markup = profit / cost. A 50% margin is a 100% markup.",
         "Suggested price = cost / (1 - target margin), rounded UP to the rounding increment."])
    st, s = _settings(wb, [("HST rate", 0.13, "pct", None), ("Round prices up to", 0.05, "money", "e.g. 0.05, 0.25, 1.00")])
    rate, rnd = s["HST rate"], s["Round prices up to"]
    ws = wb.create_sheet("Products", 2)
    title(ws, "Product Pricing")
    cols = [Col("Product / Service", 24), Col("Material Cost", 11, fmt="money"), Col("Labour Cost", 11, fmt="money"),
            Col("Overhead / Other", 11, fmt="money"),
            Col("Total Unit Cost", 11, f="N([Material Cost])+N([Labour Cost])+N([Overhead / Other])", fmt="money"),
            Col("Target Margin", 9, fmt="0.0%"),
            Col("Suggested Price", 11, f=f'IF([Target Margin]>=1,"n/a",CEILING([Total Unit Cost]/(1-[Target Margin]),{rnd}))', fmt="money"),
            Col("Your Price (optional)", 11, fmt="money"),
            Col("Price Used", 11, f='IF([Your Price (optional)]<>"",[Your Price (optional)],[Suggested Price])', fmt="money"),
            Col("Profit / Unit", 11, f="[Price Used]-[Total Unit Cost]", fmt="money"),
            Col("Markup %", 9, f="IFERROR([Profit / Unit]/[Total Unit Cost],0)", fmt="0.0%"),
            Col("Margin %", 9, f="IFERROR([Profit / Unit]/[Price Used],0)", fmt="0.0%"),
            Col("Price incl. HST", 11, f=f"ROUND([Price Used]*(1+{rate}),2)", fmt="money")]
    prods = [("Custom cutting board", 18.40, 22.00, 4.10, 0.45, None), ("Charcuterie board (large)", 31.25, 35.00, 6.50, 0.50, None),
             ("Engraving add-on", 0.80, 9.00, 1.20, 0.60, 30), ("Coaster set (4)", 6.10, 8.50, 1.40, 0.40, None),
             ("Workshop seat (2 hrs)", 12.00, 40.00, 15.00, 0.35, 99)]
    samples = [dict(zip(["Product / Service", "Material Cost", "Labour Cost", "Overhead / Other", "Target Margin",
                         "Your Price (optional)"], p)) for p in prods]
    t = add_table(ws, cols, samples, n=200)
    flag_rule(ws, f"L{t.first}:L{t.last}", f"AND(ISNUMBER(L{t.first}),ISNUMBER(F{t.first}),L{t.first}<F{t.first})")
    rf = wb.create_sheet("Margin vs Markup", 3)
    title(rf, "Margin vs Markup", "Type any margin in the yellow cells")
    header(rf, 4, 1, ["Margin", "Equivalent Markup", "Price for $100 cost"])
    widths(rf, {"A": 12, "B": 18, "C": 20})
    for i, m in enumerate([0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7]):
        r = 5 + i
        inp(rf, f"A{r}", m, "0%")
        calc(rf, f"B{r}", f'IF(A{r}>=1,"n/a",A{r}/(1-A{r}))', "0.0%")
        calc(rf, f"C{r}", f'IF(A{r}>=1,"n/a",100/(1-A{r}))', "money")
    finalize(wb, path)
    import math
    c0 = 18.40 + 22.00 + 4.10
    sug = math.ceil(round(c0 / 0.55 / 0.05, 6)) * 0.05
    c2 = 0.8 + 9 + 1.2
    return [("Products", "G6", round(sug, 2)), ("Products", "L8", (30 - c2) / 30), ("Margin vs Markup", "B13", 1.0)]


# ===================================================== 23 Subscription tracker
def subscription_tracker(path):
    wb = new_workbook()
    instructions(
        wb, "Subscription & Recurring Expense Tracker",
        "See every recurring charge in one place, its true monthly and annual cost, and what renews soon.",
        ["List each subscription/recurring bill with its billing frequency and the amount charged per bill.",
         "Enter the next renewal date and whether it auto-renews.",
         "Monthly and annual equivalents are calculated so different billing cycles can be compared.",
         "Active items renewing within the notice window on Settings are flagged RENEWS SOON."],
        [("Settings", "As-of date and renewal notice window."), ("Subscriptions", "One row per recurring charge."),
         ("Summary", "Total monthly/annual cost by category."), ("Lists", "Frequencies, categories, statuses.")],
        [AS_OF_NOTE, "Cancelled items are excluded from totals."])
    st, s = _settings(wb, [("As-of date", "=TODAY()", "date", "Overwrite with a date to freeze the report."),
                           ("Renewal notice window (days)", 30, "0", None)])
    asof, win = s["As-of date"], s["Renewal notice window (days)"]
    freq = ["Weekly", "Monthly", "Quarterly", "Semi-annual", "Annual"]
    per_year = [52, 12, 4, 2, 1]
    cats = ["Software", "Telecom", "Insurance", "Marketing", "Banking", "Memberships", "Other"]
    lw, lists = lists_sheet(wb, {"Frequency": freq, "Bills per Year": per_year, "Category": cats,
                                 "Status": ["Active", "Trial", "Cancelled"]})
    ws = wb.create_sheet("Subscriptions", 2)
    title(ws, "Subscriptions & Recurring Charges")
    cols = [Col("Service", 20), Col("Category", 13, dv=lists["Category"]), Col("Vendor", 16),
            Col("Billing Frequency", 11, dv=lists["Frequency"], default="Monthly"), Col("Cost per Bill", 11, fmt="money"),
            Col("Status", 10, dv=lists["Status"], default="Active"),
            Col("Bills / Year", 8, f="IFERROR(INDEX(Lists!$C$3:$C$17,MATCH([Billing Frequency],Lists!$A$3:$A$17,0)),0)", fmt="0"),
            Col("Annual Cost", 11, f='IF([Status]="Cancelled",0,[Cost per Bill]*[Bills / Year])', fmt="money", total="sum"),
            Col("Monthly Equivalent", 11, f="[Annual Cost]/12", fmt="money", total="sum"),
            Col("Next Renewal", 12, fmt="date"),
            Col("Days to Renewal", 9, f=f'IF([Next Renewal]="","",[Next Renewal]-{asof})', fmt="0"),
            Col("Auto-renew? (Y/N)", 9, dv="Y,N", default="Y", align="center"), Col("Payment Method", 13),
            Col("Alert", 13, f=f'IF(AND([Status]<>"Cancelled",[Days to Renewal]<>"",[Days to Renewal]<={win}),"RENEWS SOON","")', align="center")]
    subs = [("Microsoft 365", "Software", "Microsoft", "Monthly", 34.80, "Active"),
            ("QuickBooks Online", "Software", "Intuit", "Monthly", 90.00, "Active"),
            ("Cell plans (3 lines)", "Telecom", "Telus", "Monthly", 195.00, "Active"),
            ("Business insurance", "Insurance", "Intact", "Annual", 2150.00, "Active"),
            ("Website hosting", "Marketing", "Shopify", "Monthly", 52.00, "Active"),
            ("Chamber of Commerce", "Memberships", "Local CoC", "Annual", 395.00, "Active"),
            ("Canva Pro", "Marketing", "Canva", "Annual", 164.99, "Cancelled"),
            ("Business bank plan", "Banking", "RBC", "Monthly", 30.00, "Active"),
            ("Security monitoring", "Other", "ADT", "Quarterly", 135.00, "Active"),
            ("Dropbox trial", "Software", "Dropbox", "Monthly", 24.00, "Trial")]
    samples = [dict(zip(["Service", "Category", "Vendor", "Billing Frequency", "Cost per Bill", "Status"], x),
                    **{"Next Renewal": d(YEAR, 11, 10) + dt.timedelta(days=17 * i), "Payment Method": "Company Visa"})
               for i, x in enumerate(subs)]
    t = add_table(ws, cols, samples, n=200)
    flag_rule(ws, f"N{t.first}:N{t.last}", f'N{t.first}="RENEWS SOON"', fill=FILL_AMBER, bold=True)
    sm = wb.create_sheet("Summary", 3)
    title(sm, "Recurring Cost Summary", "Active and trial items")
    header(sm, 4, 1, ["Category", "# Items", "Monthly", "Annual"])
    widths(sm, {"A": 18, "B": 10, "C": 13, "D": 13})
    for i in range(len(cats) + 10):
        r = 5 + i
        calc(sm, f"A{r}", f'IF(Lists!E{3 + i}="","",Lists!E{3 + i})')
        calc(sm, f"B{r}", f'IF(A{r}="","",COUNTIFS({t.rng("Category")},A{r},{t.rng("Status")},"<>Cancelled"))', "0")
        calc(sm, f"C{r}", f'IF(A{r}="","",SUMIFS({t.rng("Monthly Equivalent")},{t.rng("Category")},A{r}))', "money")
        calc(sm, f"D{r}", f'IF(A{r}="","",SUMIFS({t.rng("Annual Cost")},{t.rng("Category")},A{r}))', "money")
    tr = 5 + len(cats) + 10
    label(sm, f"A{tr}", "Total", bold=True, fill=FILL_TOTAL)
    for L, fm in zip("BCD", ["0", "money", "money"]):
        calc(sm, f"{L}{tr}", f"SUM({L}5:{L}{tr - 1})", fm, bold=True, fill=FILL_TOTAL)
    finalize(wb, path)
    py = dict(zip(freq, per_year))
    annual = sum(c * py[f] for *_, f, c, stt in subs if stt != "Cancelled")
    return [("Summary", f"D{tr}", round(annual, 2)), ("Subscriptions", t.total("Monthly Equivalent"), round(annual / 12, 6)),
            ("Summary", f"B{tr}", 9)]


# ============================================================ 24 KPI dashboard
def kpi_dashboard(path):
    wb = new_workbook()
    instructions(
        wb, "KPI Dashboard",
        "Track your key numbers against monthly targets, with year-to-date attainment and traffic-light status.",
        ["On the Targets tab, list your KPIs, choose whether higher or lower is better, how they add up "
         "(Sum, Average or Latest) and enter monthly targets.",
         "Enter actual results each month on the Actuals tab (KPI names copy across).",
         "On the Dashboard, pick the month to report through (1-12).",
         "Green = on track (100%+ of target), amber = within 10%, red = behind."],
        [("Targets", "KPI definitions and monthly targets."), ("Actuals", "Monthly actual results."),
         ("Dashboard", "Selected month and year-to-date vs target with status.")],
        ["Sum = add the months (e.g. revenue). Average = average of the months (e.g. margin %). "
         "Latest = most recent month only (e.g. headcount, cash balance).",
         "For 'Lower is better' KPIs (e.g. complaints, days to pay), attainment = target / actual."])
    kpis = [("Revenue", "$", "Higher", "Sum", [50000 + 2000 * m for m in range(12)]),
            ("Gross margin %", "%", "Higher", "Average", [0.42] * 12),
            ("New customers", "#", "Higher", "Sum", [25] * 12),
            ("Avg days to get paid", "days", "Lower", "Average", [30] * 12),
            ("Customer complaints", "#", "Lower", "Sum", [4] * 12),
            ("Cash balance", "$", "Higher", "Latest", [40000] * 12),
            ("Website leads", "#", "Higher", "Sum", [120 + 5 * m for m in range(12)])]
    acts = [[51200, 53900, 52100, 57800, 59500, 60100, 61800, 63000, 66900, 69800],
            [0.41, 0.43, 0.44, 0.40, 0.42, 0.45, 0.43, 0.41, 0.44, 0.46],
            [22, 28, 31, 19, 26, 27, 30, 24, 29, 33],
            [34, 31, 29, 33, 28, 27, 30, 26, 25, 27],
            [5, 3, 6, 2, 4, 3, 5, 2, 3, 1],
            [38000, 41000, 39500, 43000, 45500, 44800, 47200, 46100, 49800, 52300],
            [118, 131, 126, 140, 152, 149, 160, 171, 168, 182]]
    N = 20
    for name in ("Targets", "Actuals"):
        ws = wb.create_sheet(name)
        title(ws, f"KPI {name}", "Monthly values")
        hdr = ["KPI", "Unit", "Direction", "Aggregation"] if name == "Targets" else ["KPI", "Unit", "", ""]
        header(ws, 4, 1, hdr + MONTHS)
        widths(ws, {"A": 24, "B": 7, "C": 10, "D": 11})
        for c in range(5, 17):
            ws.column_dimensions[GL(c)].width = 10
        for i in range(N):
            r = 5 + i
            k = kpis[i] if i < len(kpis) else None
            if name == "Targets":
                inp(ws, f"A{r}", k[0] if k else None)
                inp(ws, f"B{r}", k[1] if k else None)
                inp(ws, f"C{r}", k[2] if k else None)
                inp(ws, f"D{r}", k[3] if k else None)
            else:
                for L in "AB":
                    calc(ws, f"{L}{r}", f'IF(Targets!{L}{r}="","",Targets!{L}{r})')
            for m in range(12):
                v = None
                if k:
                    v = k[4][m] if name == "Targets" else (acts[i][m] if m < len(acts[i]) else None)
                fm = "0.0%" if (k and k[1] == "%") else "#,##0"
                inp(ws, f"{GL(5 + m)}{r}", v, fm)
        if name == "Targets":
            add_list(ws, f"C5:C{4 + N}", "Higher,Lower")
            add_list(ws, f"D5:D{4 + N}", "Sum,Average,Latest")
            add_list(ws, f"B5:B{4 + N}", "$,%,#,days,hrs")
        ws.freeze_panes = "E5"
    db = wb.create_sheet("Dashboard", 1)
    title(db, "KPI Dashboard", "Year-to-date through the selected month")
    label(db, "A3", "Report through month (1-12)", bold=True)
    inp(db, "B3", 10, "0")
    calc(db, "C3", 'INDEX({"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"},MAX(1,MIN(12,B3)))')
    header(db, 5, 1, ["KPI", "Unit", "Month Target", "Month Actual", "Month %", "YTD Target", "YTD Actual",
                      "YTD Attainment", "Status"])
    widths(db, {"A": 26, "B": 7, "C": 13, "D": 13, "E": 10, "F": 13, "G": 13, "H": 12, "I": 11})

    def ytd(sheet, r):
        rng = f"{sheet}!$E{r}:$P{r}"
        s = f"SUMPRODUCT((COLUMN({rng})-COLUMN({sheet}!$E{r})+1<=$B$3)*{rng})"
        return f'IF(Targets!$D{r}="Average",{s}/$B$3,IF(Targets!$D{r}="Latest",INDEX({rng},$B$3),{s}))'
    for i in range(N):
        r = 6 + i
        sr = 5 + i
        g = f'IF(Targets!$A{sr}="","",'
        calc(db, f"A{r}", f'IF(Targets!A{sr}="","",Targets!A{sr})')
        calc(db, f"B{r}", f'IF(Targets!B{sr}="","",Targets!B{sr})')
        calc(db, f"C{r}", g + f"INDEX(Targets!$E{sr}:$P{sr},$B$3))")
        calc(db, f"D{r}", g + f"INDEX(Actuals!$E{sr}:$P{sr},$B$3))")
        calc(db, f"E{r}", g + f'IFERROR(IF(Targets!$C{sr}="Lower",C{r}/D{r},D{r}/C{r}),0))', "0%")
        calc(db, f"F{r}", g + ytd("Targets", sr) + ")")
        calc(db, f"G{r}", g + ytd("Actuals", sr) + ")")
        calc(db, f"H{r}", g + f'IFERROR(IF(Targets!$C{sr}="Lower",F{r}/G{r},G{r}/F{r}),0))', "0%")
        calc(db, f"I{r}", g + f'IF(H{r}>=1,"On track",IF(H{r}>=0.9,"Watch","Behind")))', align="center")
        for L in "CDFG":
            db[f"{L}{r}"].number_format = "#,##0"
    from openpyxl.formatting.rule import Rule
    from openpyxl.styles.differential import DifferentialStyle
    from openpyxl.styles.numbers import NumberFormat
    pct = DifferentialStyle(numFmt=NumberFormat(numFmtId=200, formatCode="0.0%"))
    db.conditional_formatting.add(f"C6:D{5 + N}", Rule(type="expression", formula=['$B6="%"'], dxf=pct))
    db.conditional_formatting.add(f"F6:G{5 + N}", Rule(type="expression", formula=['$B6="%"'], dxf=pct))
    flag_rule(db, f"I6:I{5 + N}", 'I6="On track"', fill=FILL_GREEN, bold=True)
    flag_rule(db, f"I6:I{5 + N}", 'I6="Watch"', fill=FILL_AMBER, bold=True)
    flag_rule(db, f"I6:I{5 + N}", 'I6="Behind"', fill=FILL_RED, bold=True)
    finalize(wb, path)
    m = 10
    rev_t = sum(50000 + 2000 * k for k in range(m))
    rev_a = sum(acts[0][:m])
    days_t, days_a = 30, sum(acts[3][:m]) / m
    return [("Dashboard", "H6", rev_a / rev_t), ("Dashboard", "H9", days_t / days_a),
            ("Dashboard", "G11", 52300), ("Dashboard", "I6", "On track" if rev_a >= rev_t else ("Watch" if rev_a / rev_t >= 0.9 else "Behind"))]


# ===================================================== 25 Equipment maintenance
def maintenance_log(path):
    wb = new_workbook()
    instructions(
        wb, "Equipment Maintenance Log",
        "Schedule preventive maintenance, log service work and costs, and see what's overdue.",
        ["On Equipment, list each asset with its service interval (days) and in-service date.",
         "Log every service on the Service Log tab with date, equipment ID, work done, cost and downtime.",
         "Last service, next due date and status (OVERDUE / DUE SOON / OK) update automatically.",
         "Total maintenance cost and downtime per asset are summed from the log."],
        [("Settings", "As-of date and due-soon window."), ("Equipment", "Asset list and maintenance status."),
         ("Service Log", "Every service visit."), ("Lists", "Locations and technicians.")],
        [AS_OF_NOTE, "If an asset has no service logged yet, the in-service date is used as the last service."])
    st, s = _settings(wb, [("As-of date", "=TODAY()", "date", "Overwrite with a date to freeze the report."),
                           ("Due-soon window (days)", 14, "0", None)])
    asof, win = s["As-of date"], s["Due-soon window (days)"]
    lw, lists = lists_sheet(wb, {"Location": ["Shop", "Yard", "Truck 1", "Truck 2", "Office"],
                                 "Technician": ["In-house", "Dealer", "Contractor"]})
    wl = wb.create_sheet("Service Log", 2)
    we = wb.create_sheet("Equipment", 2)
    title(wl, "Service Log")
    lcols = [Col("Date", 12, fmt="date"), Col("Equipment ID", 11),
             Col("Equipment (auto)", 24, f='IFERROR(INDEX(Equipment!$B$6:$B$205,MATCH([Equipment ID],Equipment!$A$6:$A$205,0)),"UNKNOWN ID")'),
             Col("Work Performed", 30), Col("Technician", 12, dv=lists["Technician"]),
             Col("Cost", 11, fmt="money", total="sum"), Col("Downtime (hrs)", 9, fmt="num1", total="sum"), Col("Notes", 22)]
    eq = [("EQ-01", "Forklift - Toyota 8FGU25", "Shop", 90, d(2023, 3, 1)),
          ("EQ-02", "Air compressor 60 gal", "Shop", 180, d(2022, 6, 15)),
          ("EQ-03", "Generator 7500W", "Yard", 365, d(2024, 5, 1)),
          ("EQ-04", "Service truck - F-350", "Truck 1", 120, d(2025, 1, 10)),
          ("EQ-05", "Table saw - SawStop", "Shop", 60, d(YEAR, 8, 1))]
    logs = [(d(YEAR, 3, 4), "EQ-01", "Oil, filters, inspection", 420.00, 3), (d(YEAR, 6, 2), "EQ-01", "Oil change", 260.00, 2),
            (d(YEAR, 9, 1), "EQ-01", "Brake service", 890.00, 6), (d(YEAR, 4, 18), "EQ-02", "Drain & valve check", 95.00, 1),
            (d(YEAR, 5, 20), "EQ-03", "Annual service", 310.00, 2), (d(YEAR, 7, 15), "EQ-04", "Tires & alignment", 1480.00, 8),
            (d(YEAR, 10, 1), "EQ-02", "Belt replaced", 140.00, 2)]
    ls_ = [{"Date": a, "Equipment ID": b, "Work Performed": c, "Technician": "In-house", "Cost": e, "Downtime (hrs)": f}
           for a, b, c, e, f in logs]
    tl = add_table(wl, lcols, ls_, n=500, key="Equipment ID")
    flag_rule(wl, f"C{tl.first}:C{tl.last}", f'C{tl.first}="UNKNOWN ID"')
    title(we, "Equipment & Maintenance Status")
    LD, LI, LC, LH = tl.rng("Date"), tl.rng("Equipment ID"), tl.rng("Cost"), tl.rng("Downtime (hrs)")
    ecols = [Col("Equipment ID", 11), Col("Description", 26), Col("Location", 10, dv=lists["Location"]),
             Col("Serial #", 14), Col("Service Interval (days)", 10, fmt="0"), Col("In-service Date", 12, fmt="date"),
             Col("Last Service", 12, f=f"MAX([In-service Date],_xlfn.MAXIFS({LD},{LI},[Equipment ID]))", fmt="date"),
             Col("Next Due", 12, f="[Last Service]+[Service Interval (days)]", fmt="date"),
             Col("Days Until Due", 9, f=f"[Next Due]-{asof}", fmt="0"),
             Col("Status", 11, f=f'IF([Days Until Due]<0,"OVERDUE",IF([Days Until Due]<={win},"DUE SOON","OK"))', align="center"),
             Col("# Services", 8, f=f"COUNTIF({LI},[Equipment ID])", fmt="0"),
             Col("Total Cost", 11, f=f"SUMIFS({LC},{LI},[Equipment ID])", fmt="money", total="sum"),
             Col("Total Downtime (hrs)", 10, f=f"SUMIFS({LH},{LI},[Equipment ID])", fmt="num1", total="sum")]
    es = [{"Equipment ID": a, "Description": b, "Location": c, "Serial #": f"SN-{4400 + i}",
           "Service Interval (days)": iv, "In-service Date": ins} for i, (a, b, c, iv, ins) in enumerate(eq)]
    te = add_table(we, ecols, es, n=200)
    flag_rule(we, f"J{te.first}:J{te.last}", f'J{te.first}="OVERDUE"', bold=True)
    flag_rule(we, f"J{te.first}:J{te.last}", f'J{te.first}="DUE SOON"', fill=FILL_AMBER)
    flag_rule(we, f"J{te.first}:J{te.last}", f'J{te.first}="OK"', fill=FILL_GREEN)
    add_list(wl, f"B{tl.first}:B{tl.last}", f"=Equipment!$A${te.first}:$A${te.last}")
    finalize(wb, path)
    return [("Equipment", te.cell("Next Due", 0), d(YEAR, 9, 1) + dt.timedelta(days=90)),
            ("Equipment", te.cell("Total Cost", 0), 1570), ("Equipment", te.cell("Last Service", 4), d(YEAR, 8, 1)),
            ("Equipment", te.total("Total Cost"), sum(x[3] for x in logs))]


# ======================================================== 26 Purchase orders
def po_tracker(path):
    wb = new_workbook()
    instructions(
        wb, "Purchase Order Tracker",
        "Track what you've ordered, from whom, what's been received, and which orders are late.",
        ["Enter each PO line on the Purchase Orders tab: PO #, vendor, item, quantity, unit cost and expected date.",
         "As goods arrive, update Qty Received and the received date.",
         "Status shows Received, Partial, Late or Open. Outstanding value = what's still to arrive.",
         "The Summary tab shows open commitments and status counts by vendor."],
        [("Settings", "HST rate and as-of date."), ("Purchase Orders", "One row per PO line."),
         ("Summary", "Open value, late orders and spend by vendor.")],
        [AS_OF_NOTE, "For multi-line POs, repeat the PO # on each line."])
    st, s = _settings(wb, [("HST rate", 0.13, "pct", None),
                           ("As-of date", "=TODAY()", "date", "Overwrite with a date to freeze the report.")])
    rate, asof = s["HST rate"], s["As-of date"]
    ws = wb.create_sheet("Purchase Orders", 2)
    title(ws, "Purchase Orders")
    cols = [Col("PO #", 10), Col("Order Date", 12, fmt="date"), Col("Vendor", 20), Col("Item / Description", 26),
            Col("Qty Ordered", 9, fmt="int"), Col("Unit Cost", 10, fmt="money"),
            Col("Subtotal", 12, f="[Qty Ordered]*[Unit Cost]", fmt="money", total="sum"),
            Col("Taxable? (Y/N)", 8, dv="Y,N", default="Y", align="center"),
            Col("HST", 10, f=f'IF([Taxable? (Y/N)]="Y",ROUND([Subtotal]*{rate},2),0)', fmt="money", total="sum"),
            Col("PO Total", 12, f="[Subtotal]+[HST]", fmt="money", total="sum"),
            Col("Expected Date", 12, fmt="date"), Col("Qty Received", 9, fmt="int"), Col("Received Date", 12, fmt="date"),
            Col("Qty Outstanding", 9, f="MAX(0,[Qty Ordered]-N([Qty Received]))", fmt="int"),
            Col("Outstanding Value", 12, f="[Qty Outstanding]*[Unit Cost]", fmt="money", total="sum"),
            Col("Status", 10, f=f'IF(N([Qty Received])>=[Qty Ordered],"Received",IF(AND([Expected Date]<>"",{asof}>[Expected Date]),"Late",IF(N([Qty Received])>0,"Partial","Open")))', align="center"),
            Col("Days Late", 8, f=f'IF(AND([Status]<>"Received",[Expected Date]<>"",{asof}>[Expected Date]),{asof}-[Expected Date],0)', fmt="0")]
    pos = [("PO-301", "Kent Building Supplies", "2x4x8 SPF studs", 240, 4.85, 240), ("PO-301", "Kent Building Supplies", "1/2in drywall 4x8", 80, 17.95, 80),
           ("PO-302", "Wolseley", "PEX fittings assortment", 10, 64.00, 6), ("PO-303", "Nedco", "LED pot lights (12 pk)", 6, 189.00, 0),
           ("PO-304", "Uline", "Shipping boxes (bundle)", 15, 42.50, 15), ("PO-305", "Grand & Toy", "Office chairs", 4, 289.00, 0),
           ("PO-306", "Fastenal", "Anchor bolts", 500, 0.68, 250)]
    samples, exp = [], {"tot": 0, "out": 0}
    for i, (po, v, it, q, uc, rcv) in enumerate(pos):
        od = d(YEAR, 9, 1) + dt.timedelta(days=9 * i)
        samples.append({"PO #": po, "Order Date": od, "Vendor": v, "Item / Description": it, "Qty Ordered": q,
                        "Unit Cost": uc, "Expected Date": od + dt.timedelta(days=14), "Qty Received": rcv or None,
                        "Received Date": od + dt.timedelta(days=12) if rcv else None})
        sub = q * uc
        exp["tot"] += sub + round(sub * 0.13, 2)
        exp["out"] += max(0, q - rcv) * uc
    t = add_table(ws, cols, samples, n=300)
    flag_rule(ws, f"P{t.first}:P{t.last}", f'P{t.first}="Late"', bold=True)
    flag_rule(ws, f"P{t.first}:P{t.last}", f'P{t.first}="Received"', fill=FILL_GREEN)
    flag_rule(ws, f"P{t.first}:P{t.last}", f'P{t.first}="Partial"', fill=FILL_AMBER)
    sm = wb.create_sheet("Summary", 3)
    title(sm, "Purchasing Summary")
    widths(sm, {"A": 26, "B": 14, "C": 14, "D": 14, "E": 10})
    S = t.rng("Status")
    for i, (lab, f, fm) in enumerate([("Total ordered (incl. HST)", f"SUM({t.rng('PO Total')})", "money"),
                                      ("Outstanding value (pre-tax)", f"SUM({t.rng('Outstanding Value')})", "money"),
                                      ("Late lines", f'COUNTIF({S},"Late")', "0"),
                                      ("Partial lines", f'COUNTIF({S},"Partial")', "0"),
                                      ("Open lines", f'COUNTIF({S},"Open")', "0"),
                                      ("Received lines", f'COUNTIF({S},"Received")', "0")]):
        label(sm, f"A{4 + i}", lab, bold=True)
        calc(sm, f"B{4 + i}", f, fm)
    section(sm, "A11", "By vendor (type vendor names)")
    header(sm, 12, 1, ["Vendor", "Ordered (pre-tax)", "Outstanding", "Late Lines"])
    vendors = sorted({p[1] for p in pos})
    for i in range(15):
        r = 13 + i
        inp(sm, f"A{r}", vendors[i] if i < len(vendors) else None)
        calc(sm, f"B{r}", f'IF(A{r}="","",SUMIFS({t.rng("Subtotal")},{t.rng("Vendor")},A{r}))', "money")
        calc(sm, f"C{r}", f'IF(A{r}="","",SUMIFS({t.rng("Outstanding Value")},{t.rng("Vendor")},A{r}))', "money")
        calc(sm, f"D{r}", f'IF(A{r}="","",COUNTIFS({t.rng("Vendor")},A{r},{S},"Late"))', "0")
    finalize(wb, path)
    return [("Summary", "B4", round(exp["tot"], 2)), ("Summary", "B5", round(exp["out"], 2)),
            ("Purchase Orders", t.cell("Status", 0), "Received")]


# ======================================================== 27 Time billing
def time_billing(path):
    wb = new_workbook()
    instructions(
        wb, "Time Tracking & Billing",
        "Log billable hours by client, see what's unbilled, track retainers and staff utilization.",
        ["On Clients, enter each client's hourly rate and any retainer received.",
         "Log time on the Time Log tab: date, client, staff, task, hours and whether it's billable.",
         "The client's rate fills in automatically (type a Rate Override for special pricing).",
         "When you invoice, mark entries Invoiced = Y. Clients shows unbilled amounts and retainer balance."],
        [("Clients", "Rates, billable/unbilled totals and retainer balance."), ("Time Log", "Every time entry."),
         ("Staff", "Hours and utilization by person."), ("Lists", "Staff names.")],
        ["Retainer remaining = retainer received - amount invoiced.",
         "Utilization = billable hours / total hours logged."])
    staff = ["Alex", "Jordan", "Sam"]
    lw, lists = lists_sheet(wb, {"Staff": staff})
    wt = wb.create_sheet("Time Log", 1)
    wc = wb.create_sheet("Clients", 1)
    title(wt, "Time Log")
    clients = [("Maple Ridge Dental", 125, 2000), ("Northshore Builders", 110, 0), ("Chen Law LLP", 150, 5000),
               ("Bayview Cafe", 95, 0)]
    CR = "Clients!$A$6:$A$105"
    CRATE = "Clients!$B$6:$B$105"
    tcols = [Col("Date", 12, fmt="date"), Col("Client", 20, dv=f"={CR}"), Col("Project / Matter", 18),
             Col("Staff", 10, dv=lists["Staff"]), Col("Task Description", 28), Col("Hours", 7, fmt="num2", total="sum"),
             Col("Billable? (Y/N)", 8, dv="Y,N", default="Y", align="center"), Col("Rate Override", 9, fmt="money"),
             Col("Rate", 9, f=f'IF([Rate Override]<>"",[Rate Override],IFERROR(INDEX({CRATE},MATCH([Client],{CR},0)),0))', fmt="money"),
             Col("Amount", 11, f='IF([Billable? (Y/N)]="Y",ROUND([Hours]*[Rate],2),0)', fmt="money", total="sum"),
             Col("Invoiced? (Y/N)", 8, dv="Y,N", default="N", align="center"), Col("Invoice #", 10)]
    entries = []
    for i in range(20):
        c = clients[i % 4]
        hrs = [1.5, 3.0, 0.75, 2.25, 4.0][i % 5]
        bill = "N" if i % 6 == 5 else "Y"
        inv = "Y" if i < 10 else "N"
        ovr = 80 if i == 7 else None
        entries.append({"Date": d(YEAR, 10, 1) + dt.timedelta(days=i), "Client": c[0], "Project / Matter": "General",
                        "Staff": staff[i % 3], "Task Description": "Consulting", "Hours": hrs, "Billable? (Y/N)": bill,
                        "Rate Override": ovr, "Invoiced? (Y/N)": inv, "Invoice #": f"INV-{900 + i // 5}" if inv == "Y" else None})
    tt = add_table(wt, tcols, entries, n=1000)
    title(wc, "Clients")
    A, C, H, B, I = tt.rng("Amount"), tt.rng("Client"), tt.rng("Hours"), tt.rng("Billable? (Y/N)"), tt.rng("Invoiced? (Y/N)")
    ccols = [Col("Client", 22), Col("Hourly Rate", 10, fmt="money"), Col("Retainer Received", 11, fmt="money", total="sum"),
             Col("Hours Logged", 9, f=f"SUMIFS({H},{C},[Client])", fmt="num2", total="sum"),
             Col("Billable Hours", 9, f=f'SUMIFS({H},{C},[Client],{B},"Y")', fmt="num2", total="sum"),
             Col("Billable Amount", 12, f=f"SUMIFS({A},{C},[Client])", fmt="money", total="sum"),
             Col("Invoiced", 12, f=f'SUMIFS({A},{C},[Client],{I},"Y")', fmt="money", total="sum"),
             Col("Unbilled (WIP)", 12, f="[Billable Amount]-[Invoiced]", fmt="money", total="sum"),
             Col("Retainer Remaining", 12, f='IF(N([Retainer Received])=0,"",[Retainer Received]-[Invoiced])', fmt="money")]
    tc = add_table(wc, ccols, [dict(zip(["Client", "Hourly Rate", "Retainer Received"], c)) for c in clients], n=100)
    flag_rule(wc, f"I{tc.first}:I{tc.last}", f"AND(ISNUMBER(I{tc.first}),I{tc.first}<0)")
    sw = wb.create_sheet("Staff", 3)
    title(sw, "Staff Utilization")
    header(sw, 4, 1, ["Staff", "Total Hours", "Billable Hours", "Utilization", "Billable Amount"])
    widths(sw, {"A": 16, "B": 12, "C": 12, "D": 12, "E": 14})
    ST = tt.rng("Staff")
    for i in range(10):
        r = 5 + i
        calc(sw, f"A{r}", f'IF(Lists!A{3 + i}="","",Lists!A{3 + i})')
        calc(sw, f"B{r}", f'IF(A{r}="","",SUMIFS({H},{ST},A{r}))', "num2")
        calc(sw, f"C{r}", f'IF(A{r}="","",SUMIFS({H},{ST},A{r},{B},"Y"))', "num2")
        calc(sw, f"D{r}", f'IF(A{r}="","",IFERROR(C{r}/B{r},0))', "0%")
        calc(sw, f"E{r}", f'IF(A{r}="","",SUMIFS({A},{ST},A{r}))', "money")
    finalize(wb, path)
    rates = {c[0]: c[1] for c in clients}
    amt = {c[0]: 0 for c in clients}
    inv = {c[0]: 0 for c in clients}
    for e in entries:
        if e["Billable? (Y/N)"] == "Y":
            a = round(e["Hours"] * (e["Rate Override"] or rates[e["Client"]]), 2)
            amt[e["Client"]] += a
            if e["Invoiced? (Y/N)"] == "Y":
                inv[e["Client"]] += a
    return [("Clients", tc.total("Billable Amount"), sum(amt.values())),
            ("Clients", tc.total("Unbilled (WIP)"), sum(amt.values()) - sum(inv.values())),
            ("Clients", tc.cell("Retainer Remaining", 0), 2000 - inv["Maple Ridge Dental"])]


# ======================================================== 28 Commission
def commission(path):
    wb = new_workbook()
    instructions(
        wb, "Sales Commission Calculator",
        "Calculate tiered (marginal) commissions, quota attainment and total pay for each sales rep.",
        ["On Settings, set the commission period dates and the tier table (sales from $X earn Y%).",
         "Optionally set a bonus paid when a rep reaches 100% of quota.",
         "List reps with base pay and quota on the Reps tab; log closed deals on the Sales tab.",
         "Commission is calculated per rep for deals dated inside the period."],
        [("Settings", "Period and commission tiers."), ("Reps", "Quota attainment, commission and total pay."),
         ("Sales", "Closed deals."),],
        ["Tiers are marginal (like tax brackets): only the sales ABOVE each threshold earn that tier's rate.",
         "Fill tiers from the top down with increasing thresholds; leave unused tiers blank.",
         "Rep names on the Sales tab must match the Reps tab (use the drop-down)."])
    ws = wb.create_sheet("Settings")
    title(ws, "Settings", "Change the yellow cells")
    widths(ws, {"A": 28, "B": 16, "C": 14, "D": 16})
    for i, (lab, v, fm) in enumerate([("Period start", d(YEAR, 10, 1), "date"), ("Period end", d(YEAR, 12, 31), "date"),
                                      ("Quota bonus (at 100%+)", 1000, "money0")]):
        label(ws, f"A{4 + i}", lab, bold=True)
        inp(ws, f"B{4 + i}", v, fm)
    section(ws, "A8", "Commission tiers (marginal)")
    header(ws, 9, 1, ["Tier", "Sales From ($)", "Rate", "Rate Step (calc)"])
    tiers = [(0, 0.05), (50000, 0.07), (100000, 0.10)]
    for i in range(5):
        r = 10 + i
        label(ws, f"A{r}", f"Tier {i + 1}")
        inp(ws, f"B{r}", tiers[i][0] if i < len(tiers) else None, "money0")
        inp(ws, f"C{r}", tiers[i][1] if i < len(tiers) else None, "0.0%")
        prev = "0" if i == 0 else f"N(C{r - 1})"
        calc(ws, f"D{r}", f'IF(OR(B{r}="",C{r}=""),0,C{r}-{prev})', "0.0%")
    wsa = wb.create_sheet("Sales")
    wr = wb.create_sheet("Reps", 2)
    title(wsa, "Closed Deals")
    reps = [("Alex Martin", 3500, 120000), ("Jordan Lee", 3200, 90000), ("Sam Patel", 3000, 60000)]
    deals = [("Alex Martin", 42000), ("Alex Martin", 38500), ("Alex Martin", 51000), ("Jordan Lee", 22000),
             ("Jordan Lee", 31000), ("Jordan Lee", 18500), ("Sam Patel", 27000), ("Sam Patel", 14500),
             ("Alex Martin", 9000), ("Sam Patel", 21000)]
    samples = [{"Close Date": d(YEAR, 10, 3) + dt.timedelta(days=8 * i), "Rep": r, "Customer": f"Customer {i + 1}",
                "Deal": "Annual contract", "Amount": a} for i, (r, a) in enumerate(deals)]
    samples.append({"Close Date": d(YEAR, 9, 28), "Rep": "Alex Martin", "Customer": "Prior period",
                    "Deal": "(outside period - not counted)", "Amount": 15000})
    ta = add_table(wsa, [Col("Close Date", 12, fmt="date"), Col("Rep", 16, dv="=Reps!$A$6:$A$55"), Col("Customer", 20),
                         Col("Deal", 28), Col("Amount", 12, fmt="money", total="sum"),
                         Col("In Period?", 9, f='IF(AND([Close Date]>=Settings!$B$4,[Close Date]<=Settings!$B$5),"Yes","No")', align="center")],
                   samples, n=500, key="Rep")
    title(wr, "Rep Commissions", "For the period on Settings")
    AM, RP, DT = ta.rng("Amount"), ta.rng("Rep"), ta.rng("Close Date")
    comm = "SUMPRODUCT(--([Period Sales]>Settings!$B$10:$B$14),([Period Sales]-Settings!$B$10:$B$14),Settings!$D$10:$D$14)"
    tr = add_table(wr, [Col("Rep", 16), Col("Base Pay (period)", 11, fmt="money", total="sum"), Col("Quota", 12, fmt="money0", total="sum"),
                        Col("Period Sales", 12, f=f'SUMIFS({AM},{RP},[Rep],{DT},">="&Settings!$B$4,{DT},"<="&Settings!$B$5)', fmt="money", total="sum"),
                        Col("Quota Attainment", 10, f="IFERROR([Period Sales]/[Quota],0)", fmt="0.0%"),
                        Col("Commission", 12, f=comm, fmt="money", total="sum"),
                        Col("Effective Rate", 9, f="IFERROR([Commission]/[Period Sales],0)", fmt="0.00%"),
                        Col("Quota Bonus", 11, f="IF([Quota Attainment]>=1,Settings!$B$6,0)", fmt="money", total="sum"),
                        Col("Total Pay", 12, f="[Base Pay (period)]+[Commission]+[Quota Bonus]", fmt="money", total="sum")],
                  [dict(zip(["Rep", "Base Pay (period)", "Quota"], r)) for r in reps], n=50)
    flag_rule(wr, f"E{tr.first}:E{tr.last}", f"AND(ISNUMBER(E{tr.first}),E{tr.first}>=1)", fill=FILL_GREEN, bold=True)
    finalize(wb, path)

    def cm(s_):
        tot = 0
        for i, (th, rt) in enumerate(tiers):
            nxt = tiers[i + 1][0] if i + 1 < len(tiers) else float("inf")
            tot += max(0, min(s_, nxt) - th) * rt
        return tot
    sales = {r[0]: sum(a for n, a in deals if n == r[0]) for r in reps}
    total_pay = sum(base + cm(sales[n]) + (1000 if sales[n] >= q else 0) for n, base, q in reps)
    return [("Reps", tr.cell("Commission", 0), cm(sales["Alex Martin"])), ("Reps", tr.total("Total Pay"), total_pay),
            ("Reps", tr.cell("Period Sales", 0), sales["Alex Martin"])]


# ======================================================== 29 Attendance
def attendance(path):
    wb = new_workbook()
    instructions(
        wb, "Employee Attendance Tracker",
        "Mark daily attendance for the month with simple codes and get totals and attendance % per employee.",
        ["On the Attendance tab, enter any date in the month you're tracking (cell B3).",
         "List employees in column A.",
         "Mark each working day with a code from the legend (P, R, L, A, S, V, H, U). Weekends are shaded.",
         "Totals and attendance % calculate on the right. Copy the file (or the sheet) for each month."],
        [("Attendance", "Monthly grid with totals per employee and per day."),
         ("Lists", "Attendance codes and meanings (edit labels, keep codes short).")],
        ["Attendance % = (Present + Remote + Late) / scheduled days, where scheduled days excludes Holidays and blanks.",
         "Codes: P Present, R Remote, L Late, A Absent (unexcused), S Sick, V Vacation, H Holiday, U Unpaid leave."])
    codes = [("P", "Present"), ("R", "Remote"), ("L", "Late"), ("A", "Absent"), ("S", "Sick"), ("V", "Vacation"),
             ("H", "Holiday"), ("U", "Unpaid leave")]
    lw, lists = lists_sheet(wb, {"Code": [c for c, _ in codes], "Meaning": [m for _, m in codes]}, extra=0)
    ws = wb.create_sheet("Attendance", 1)
    title(ws, "Monthly Attendance")
    label(ws, "A3", "Month (any date in it):", bold=True)
    inp(ws, "B3", d(YEAR, 10, 1), "mmmm yyyy")
    for L in "CDEFG":
        inp(ws, f"{L}3")
    ws.merge_cells("B3:G3")
    label(ws, "I3", "Starts:", font=F_SUB)
    calc(ws, "K3", "DATE(YEAR(B3),MONTH(B3),1)", "yyyy-mm-dd")
    for L in "LMN":
        calc(ws, f"{L}3", '""')
    ws.merge_cells("K3:N3")
    widths(ws, {"A": 22, "B": 14})
    header(ws, 5, 1, ["Employee"], height=18)
    header(ws, 6, 1, [""], height=18)
    sumcols = ["Present", "Remote", "Late", "Absent", "Sick", "Vacation", "Holiday", "Unpaid", "Sched. Days", "Attend. %"]
    for k in range(31):
        c = 2 + k
        L = GL(c)
        ws.column_dimensions[L].width = 4.2
        header(ws, 5, c, [None], height=18)
        header(ws, 6, c, [None], height=18)
        ws[f"{L}5"].value = f'=IF(MONTH($K$3+{k})=MONTH($K$3),$K$3+{k},"")'
        ws[f"{L}5"].number_format = "d"
        ws[f"{L}6"].value = f'=IF({L}5="","",LEFT(TEXT({L}5,"ddd"),2))'
    sc = 2 + 31
    header(ws, 5, sc, sumcols, height=18)
    header(ws, 6, sc, [""] * len(sumcols), height=18)
    for i in range(len(sumcols)):
        ws.column_dimensions[GL(sc + i)].width = 8.5
    N = 40
    emps = ["Maria Lopez", "Dev Sharma", "Chris Taylor", "Aisha Khan", "Ben Okafor"]
    pattern = {0: {}, 1: {6: "S", 7: "S"}, 2: {13: "L", 20: "L", 27: "A"}, 3: {19: "V", 20: "V", 21: "V", 22: "V", 23: "V"},
               4: {1: "R", 8: "R", 15: "R", 22: "R", 29: "R"}}
    exp_present = {}
    first_day = d(YEAR, 10, 1)
    for i in range(N):
        r = 7 + i
        inp(ws, f"A{r}", emps[i] if i < len(emps) else None)
        cnt = 0
        for k in range(31):
            day = first_day + dt.timedelta(days=k)
            v = None
            if i < len(emps) and day.month == 10 and day.weekday() < 5:
                v = "H" if day == d(YEAR, 10, 12) else pattern[i].get(day.day, "P")
                if v in ("P", "R", "L"):
                    cnt += 1
            inp(ws, f"{GL(2 + k)}{r}", v, align="center")
        if i < len(emps):
            exp_present[i] = cnt
        rg = f"$B{r}:$AF{r}"
        for j, code in enumerate(["P", "R", "L", "A", "S", "V", "H", "U"]):
            calc(ws, f"{GL(sc + j)}{r}", f'IF($A{r}="","",COUNTIF({rg},"{code}"))', "0", align="center")
        S, H = GL(sc + 8), GL(sc + 6)
        calc(ws, f"{S}{r}", f'IF($A{r}="","",COUNTA({rg})-{H}{r})', "0", align="center")
        calc(ws, f"{GL(sc + 9)}{r}", f'IF($A{r}="","",IFERROR(({GL(sc)}{r}+{GL(sc + 1)}{r}+{GL(sc + 2)}{r})/{S}{r},0))', "0%", align="center")
    add_list(ws, f"B7:AF{6 + N}", lists["Code"])
    tr = 7 + N
    label(ws, f"A{tr}", "Present that day", bold=True, fill=FILL_TOTAL)
    for k in range(31):
        L = GL(2 + k)
        calc(ws, f"{L}{tr}", f'COUNTIF({L}7:{L}{tr - 1},"P")+COUNTIF({L}7:{L}{tr - 1},"R")+COUNTIF({L}7:{L}{tr - 1},"L")', "0",
             fill=FILL_TOTAL, align="center")
    grid = f"B7:AF{6 + N}"
    ws.conditional_formatting.add(grid, FormulaRule(formula=['AND(B$5<>"",WEEKDAY(B$5,2)>5)'], fill=FILL_GREY))
    ws.conditional_formatting.add(grid, FormulaRule(formula=['B$5=""'], fill=FILL_GREY))
    for code, fill in [("A", FILL_RED), ("S", FILL_AMBER), ("V", FILL_GREEN)]:
        ws.conditional_formatting.add(grid, CellIsRule(operator="equal", formula=[f'"{code}"'], fill=fill))
    ws.freeze_panes = "B7"
    finalize(wb, path)
    sched = sum(1 for k in range(31) if (first_day + dt.timedelta(days=k)).weekday() < 5) - 1
    return [("Attendance", f"{GL(sc)}7", exp_present[0]), ("Attendance", f"{GL(sc + 9)}9", (sched - 1) / sched),
            ("Attendance", f"{GL(sc + 8)}7", sched), ("Attendance", "AF5", d(YEAR, 10, 31))]


# ======================================================== 30 Cash drawer
def cash_drawer(path):
    wb = new_workbook()
    instructions(
        wb, "Daily Cash Drawer Reconciliation",
        "Count the till at close, compare to the POS report, and keep a running log of over/short and deposits.",
        ["On Daily Count, enter the date, register and cashier, then count each coin and bill denomination.",
         "Enter the opening float and the cash sales, refunds and payouts from your POS end-of-day report.",
         "Over/short and the deposit amount (counted cash minus the float you keep) are calculated.",
         "Copy the day's results into the Log tab to track over/short trends and deposits over time."],
        [("Daily Count", "Denomination count and reconciliation for one day."),
         ("Log", "Running history of daily totals with over/short and monthly totals.")],
        ["Canada has no pennies - cash totals round to the nearest 5 cents.",
         "Investigate any over/short larger than the tolerance on the Daily Count tab."])
    ws = wb.create_sheet("Daily Count")
    title(ws, "Daily Cash Drawer Count")
    widths(ws, {"A": 26, "B": 12, "C": 12, "D": 4, "E": 30, "F": 14})
    for i, (lab, v, fm) in enumerate([("Date", d(YEAR, 11, 3), "date"), ("Register", "Front till", None),
                                      ("Cashier", "Dev Sharma", None)]):
        label(ws, f"A{3 + i}", lab, bold=True)
        inp(ws, f"B{3 + i}", v, fm)
    header(ws, 7, 1, ["Denomination", "Count", "Amount"])
    den = [("$100 bill", 100, 1), ("$50 bill", 50, 2), ("$20 bill", 20, 18), ("$10 bill", 10, 14), ("$5 bill", 5, 21),
           ("$2 coin (toonie)", 2, 30), ("$1 coin (loonie)", 1, 27), ("25c quarter", 0.25, 44), ("10c dime", 0.10, 38),
           ("5c nickel", 0.05, 22), ("Coin rolls (enter $ value)", 1, 20)]
    for i, (n, v, c) in enumerate(den):
        r = 8 + i
        label(ws, f"A{r}", n)
        inp(ws, f"B{r}", c, "int")
        calc(ws, f"C{r}", f"B{r}*{v}", "money")
    tr = 8 + len(den)
    label(ws, f"A{tr}", "Total cash counted", bold=True, fill=FILL_TOTAL)
    calc(ws, f"C{tr}", f"SUM(C8:C{tr - 1})", "money", bold=True, fill=FILL_TOTAL)
    section(ws, "E6", "Reconciliation")
    rec_in = [("Opening float", 250), ("Cash sales (POS report)", 812.45), ("Cash refunds (POS report)", 35.00),
              ("Paid-outs from drawer", 22.60), ("Card / debit sales (POS, info only)", 2486.30),
              ("Float to keep in drawer", 250), ("Over/short tolerance ($)", 5)]
    for i, (lab, v) in enumerate(rec_in):
        label(ws, f"E{7 + i}", lab, bold=True)
        inp(ws, f"F{7 + i}", v, "money")
    rec = [("Expected cash in drawer", "F7+F8-F9-F10"), ("Cash counted", f"C{tr}"), ("Over / (short)", "F15-F14"),
           ("Within tolerance?", 'IF(ABS(F16)<=F13,"Yes","INVESTIGATE")'), ("Deposit to bank", "MAX(0,F15-F12)"),
           ("Total sales (cash + card)", "F8+F11")]
    for i, (lab, f) in enumerate(rec):
        label(ws, f"E{14 + i}", lab, bold=True)
        calc(ws, f"F{14 + i}", f, None if i == 3 else "money", bold=i in (2, 4), align="center" if i == 3 else None)
    flag_rule(ws, "F17", 'F17="INVESTIGATE"', bold=True)
    wl = wb.create_sheet("Log")
    title(wl, "Daily Cash Log", "One row per register per day")
    cols = [Col("Date", 12, fmt="date"), Col("Register", 12), Col("Cashier", 14),
            Col("Opening Float", 10, fmt="money"), Col("Cash Sales", 11, fmt="money", total="sum"),
            Col("Refunds + Paid-outs", 11, fmt="money", total="sum"), Col("Card Sales", 11, fmt="money", total="sum"),
            Col("Expected Cash", 11, f="[Opening Float]+[Cash Sales]-[Refunds + Paid-outs]", fmt="money"),
            Col("Counted Cash", 11, fmt="money"),
            Col("Over / (Short)", 10, f="ROUND([Counted Cash]-[Expected Cash],2)", fmt="money", total="sum"),
            Col("Deposited", 11, fmt="money", total="sum"), Col("Deposit Slip #", 11)]
    days = [(812.45, 57.60, 2486.30, 0), (640.10, 0, 1980.75, -0.10), (955.35, 12.00, 3120.40, 2.00),
            (701.80, 20.00, 2210.00, 0), (1120.65, 45.25, 3455.10, -5.40), (880.00, 0, 2675.85, 0.05)]
    samples, os_tot = [], 0
    for i, (cs, rp, card, osv) in enumerate(days):
        expc = 250 + cs - rp
        counted = round(expc + osv, 2)
        samples.append({"Date": d(YEAR, 10, 27) + dt.timedelta(days=i), "Register": "Front till", "Cashier": "Dev Sharma",
                        "Opening Float": 250, "Cash Sales": cs, "Refunds + Paid-outs": rp, "Card Sales": card,
                        "Counted Cash": counted, "Deposited": round(counted - 250, 2), "Deposit Slip #": f"D-{60 + i}"})
        os_tot += round(counted - expc, 2)
    t = add_table(wl, cols, samples, n=400)
    flag_rule(wl, f"J{t.first}:J{t.last}", f"AND(ISNUMBER(J{t.first}),ABS(J{t.first})>'Daily Count'!$F$13)", bold=True)
    finalize(wb, path)
    counted = sum(v * c for _, v, c in den)
    expected = 250 + 812.45 - 35 - 22.60
    return [("Daily Count", f"C{tr}", round(counted, 2)), ("Daily Count", "F16", round(counted - expected, 2)),
            ("Log", t.total("Over / (Short)"), round(os_tot, 2)), ("Daily Count", "F18", round(counted - 250, 2))]


TEMPLATES_C = [
    ("21-fixed-asset-register", fixed_assets, "Asset register with straight-line or declining-balance depreciation and net book value by year."),
    ("22-pricing-calculator", pricing_calculator, "Cost build-up to suggested price from target margin, with markup, margin and HST-inclusive price."),
    ("23-subscription-tracker", subscription_tracker, "Recurring charges normalized to monthly/annual cost, with renewal alerts and category totals."),
    ("24-kpi-dashboard", kpi_dashboard, "Monthly KPI targets vs actuals with YTD attainment (sum/average/latest) and traffic-light status."),
    ("25-equipment-maintenance", maintenance_log, "Preventive maintenance schedule with service log, next-due dates, overdue flags, cost and downtime."),
    ("26-purchase-order-tracker", po_tracker, "Purchase orders with HST, partial receipts, late flags, outstanding value and vendor summary."),
    ("27-time-billing", time_billing, "Billable-hours log with client rates, unbilled WIP, retainer balances and staff utilization."),
    ("28-commission-calculator", commission, "Tiered (marginal) sales commission with quota attainment, bonus and total pay per rep."),
    ("29-attendance-tracker", attendance, "Monthly attendance grid with codes, weekend shading, per-employee totals and attendance %."),
    ("30-cash-drawer-reconciliation", cash_drawer, "End-of-day till count by denomination, over/short vs POS, deposit amount and daily log."),
]
