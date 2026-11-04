"""Shared building blocks for the Excel templates.

Every template is built from the same pieces so they look and behave alike:

* an Instructions tab (always first),
* yellow cells with blue text = things you type (unlocked),
* grey cells with black text = formulas (locked),
* every sheet protected with NO password (Review > Unprotect Sheet to customise).
"""

import datetime as dt
import re

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Protection, Side
from openpyxl.utils import get_column_letter
from openpyxl.workbook.properties import CalcProperties
from openpyxl.worksheet.datavalidation import DataValidation

FONT = "Arial"
NAVY = "1F3864"

FILL_INPUT = PatternFill("solid", fgColor="FFF2CC")
FILL_CALC = PatternFill("solid", fgColor="F2F2F2")
FILL_HEADER = PatternFill("solid", fgColor=NAVY)
FILL_TOTAL = PatternFill("solid", fgColor="D9E1F2")
FILL_SECTION = PatternFill("solid", fgColor="DDEBF7")
FILL_RED = PatternFill("solid", fgColor="F8CBAD")
FILL_AMBER = PatternFill("solid", fgColor="FFE699")
FILL_GREEN = PatternFill("solid", fgColor="C6EFCE")
FILL_GREY = PatternFill("solid", fgColor="D9D9D9")

F_INPUT = Font(name=FONT, size=10, color="0000FF")
F_CALC = Font(name=FONT, size=10, color="000000")
F_CALC_B = Font(name=FONT, size=10, color="000000", bold=True)
F_LABEL = Font(name=FONT, size=10)
F_LABEL_B = Font(name=FONT, size=10, bold=True)
F_HEADER = Font(name=FONT, size=10, bold=True, color="FFFFFF")
F_TITLE = Font(name=FONT, size=16, bold=True, color=NAVY)
F_SUB = Font(name=FONT, size=10, italic=True, color="595959")
F_H2 = Font(name=FONT, size=12, bold=True, color=NAVY)

THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

UNLOCKED = Protection(locked=False)
LOCKED = Protection(locked=True)

FMT = {
    "money": '$#,##0.00;($#,##0.00);"-"',
    "money0": '$#,##0;($#,##0);"-"',
    "pct": '0.0%;(0.0%);"-"',
    "date": "yyyy-mm-dd",
    "month": "mmm yyyy",
    "mon": "mmm",
    "int": '#,##0;(#,##0);"-"',
    "num1": '#,##0.0;(#,##0.0);"-"',
    "num2": '#,##0.00;(#,##0.00);"-"',
    "time": "h:mm AM/PM",
    "rate": "$#,##0.000",
    "general": "General",
}

YEAR = 2026
AS_OF_NOTE = ("'As-of date' defaults to =TODAY(). Type a fixed date over it to see the "
              "workbook as of that day.")


def d(y, m, day):
    return dt.date(y, m, day)


def fmt(key):
    if key is None:
        return None
    return FMT.get(key, key)


def qs(title):
    """Sheet name ready for a formula reference."""
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", title):
        return title
    return "'" + title.replace("'", "''") + "'"


def ref(ws, cell, absolute=True):
    """Absolute cross-sheet reference like 'Settings'!$B$4."""
    m = re.fullmatch(r"([A-Z]+)(\d+)", cell)
    c = f"${m.group(1)}${m.group(2)}" if absolute else cell
    return f"{qs(ws.title)}!{c}"


# ---------------------------------------------------------------- cell styling
def inp(ws, cell, value=None, f=None, align=None):
    c = ws[cell]
    c.value = value
    c.font = F_INPUT
    c.fill = FILL_INPUT
    c.border = BORDER
    c.protection = UNLOCKED
    if f:
        c.number_format = fmt(f)
    if align:
        c.alignment = Alignment(horizontal=align)
    return c


def calc(ws, cell, formula, f=None, bold=False, fill=FILL_CALC, align=None):
    c = ws[cell]
    c.value = formula if str(formula).startswith("=") else "=" + str(formula)
    c.font = F_CALC_B if bold else F_CALC
    if fill is not None:
        c.fill = fill
    c.border = BORDER
    c.protection = LOCKED
    if f:
        c.number_format = fmt(f)
    if align:
        c.alignment = Alignment(horizontal=align)
    return c


def label(ws, cell, text, bold=False, font=None, fill=None, wrap=False, align=None):
    c = ws[cell]
    c.value = text
    c.font = font or (F_LABEL_B if bold else F_LABEL)
    if fill is not None:
        c.fill = fill
    if wrap or align:
        c.alignment = Alignment(wrap_text=wrap, horizontal=align, vertical="top" if wrap else None)
    return c


def header(ws, row, col, texts, height=30):
    for i, t in enumerate(texts):
        c = ws.cell(row=row, column=col + i, value=t)
        c.font = F_HEADER
        c.fill = FILL_HEADER
        c.border = BORDER
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[row].height = height


def title(ws, text, subtitle=None):
    ws["A1"].value = text
    ws["A1"].font = F_TITLE
    ws.row_dimensions[1].height = 24
    if subtitle:
        ws["A2"].value = subtitle
        ws["A2"].font = F_SUB


def section(ws, cell, text, width=1):
    c = ws[cell]
    c.value = text
    c.font = F_H2
    return c


def widths(ws, mapping):
    for col, w in mapping.items():
        ws.column_dimensions[col].width = w


def add_list(ws, rng, source, prompt=None):
    """Drop-down list. `source` is either 'a,b,c' or a formula like =Lists!$A$2:$A$20."""
    # Excel stores list sources without a leading "=" (a range) or as a quoted CSV string.
    f1 = source[1:] if source.startswith("=") else '"' + source + '"'
    dv = DataValidation(type="list", formula1=f1, allow_blank=True, showDropDown=False)
    dv.error = "Pick a value from the list (or edit the list on the Lists tab)."
    dv.errorTitle = "Invalid entry"
    dv.errorStyle = "warning"
    dv.showErrorMessage = True
    if prompt:
        dv.prompt = prompt
        dv.showInputMessage = True
    ws.add_data_validation(dv)
    dv.add(rng)
    return dv


def flag_rule(ws, rng, formula, fill=FILL_RED, bold=False):
    ws.conditional_formatting.add(
        rng, FormulaRule(formula=[formula], fill=fill, font=Font(name=FONT, bold=bold) if bold else None))


# --------------------------------------------------------------- data tables
class Col:
    """One column of a data table.

    h      header text (also used as a placeholder name in formulas)
    w      column width
    f      formula template (no leading '='); None means an input column.
           Use [Header] for "this row of column Header" and [[Header]] for the
           whole data range of that column, e.g. "[Qty]*[Unit Cost]", and
           [^Header] for the running range from the first data row to this row.
    fmt    number format key
    dv     drop-down source ('a,b,c' or '=Lists!$A$2:$A$20')
    total  'sum' | 'count' | 'avg' | None  -> shown on the totals row
    guard  wrap formula as IF(key="","",...) so empty rows stay blank
    """

    def __init__(self, h, w=14, f=None, fmt=None, dv=None, total=None, guard=True, align=None,
                 default=None):
        self.h, self.w, self.f, self.fmt, self.dv = h, w, f, fmt, dv
        self.total, self.guard, self.align, self.default = total, guard, align, default


class Table:
    def __init__(self, ws, cols, first, last, letters, totals_row, header_row):
        self.ws, self.cols, self.first, self.last = ws, cols, first, last
        self.letters, self.totals_row, self.header_row = letters, totals_row, header_row

    def L(self, h):
        return self.letters[h]

    def rng(self, h, external=True):
        L = self.letters[h]
        r = f"${L}${self.first}:${L}${self.last}"
        return f"{qs(self.ws.title)}!{r}" if external else r

    def cell(self, h, i):
        """Cell address of sample row i (0-based)."""
        return f"{self.letters[h]}{self.first + i}"

    def total(self, h):
        return f"{self.letters[h]}{self.totals_row}"

    def span(self, external=False):
        a = f"$A${self.first}:${get_column_letter(len(self.cols))}${self.last}"
        return a


def _expand(tmpl, letters, r, first, last):
    def whole(m):
        L = letters[m.group(1)]
        return f"${L}${first}:${L}${last}"

    def one(m):
        return f"{letters[m.group(1)]}{r}"

    def running(m):
        L = letters[m.group(1)]
        return f"${L}${first}:{L}{r}"

    s = re.sub(r"\[\^([^\[\]]+)\]", running, tmpl)
    s = re.sub(r"\[\[([^\[\]]+)\]\]", whole, s)
    s = re.sub(r"\[([^\[\]]+)\]", one, s)
    return s


def add_table(ws, cols, samples, n=100, top=4, key=None, totals_label="TOTALS", freeze_col="B",
              filter=True):
    """Build a data-entry table.

    Row `top` = totals, row top+1 = headers, rows below = data (n rows, with
    formulas pre-filled so users only type in the yellow cells).
    """
    header_row = top + 1
    first = top + 2
    last = first + n - 1
    letters = {c.h: get_column_letter(i + 1) for i, c in enumerate(cols)}
    key = key or next(c.h for c in cols if c.f is None)
    keyL = letters[key]

    header(ws, header_row, 1, [c.h for c in cols], height=32)
    for i, c in enumerate(cols):
        ws.column_dimensions[get_column_letter(i + 1)].width = c.w

    for i in range(n):
        r = first + i
        sample = samples[i] if i < len(samples) else {}
        for j, c in enumerate(cols):
            addr = f"{letters[c.h]}{r}"
            if c.f is None:
                v = sample.get(c.h, c.default if sample else None)
                inp(ws, addr, v, c.fmt, c.align)
            else:
                expr = _expand(c.f, letters, r, first, last)
                if c.guard:
                    expr = f'IF({keyL}{r}="","",{expr})'
                calc(ws, addr, expr, c.fmt, align=c.align)

    if any(c.total for c in cols):
        label(ws, f"A{top}", totals_label, bold=True, fill=FILL_TOTAL)
        for c in cols:
            L = letters[c.h]
            rng = f"{L}{first}:{L}{last}"
            cell = f"{L}{top}"
            if c.total == "sum":
                calc(ws, cell, f"SUM({rng})", c.fmt, bold=True, fill=FILL_TOTAL)
            elif c.total == "count":
                calc(ws, cell, f'COUNTIF({rng},"?*")+COUNT({rng})', "int", bold=True, fill=FILL_TOTAL)
            elif c.total == "avg":
                calc(ws, cell, f"IFERROR(AVERAGE({rng}),0)", c.fmt, bold=True, fill=FILL_TOTAL)
            elif c.h != cols[0].h:
                ws[cell].fill = FILL_TOTAL

    for c in cols:
        if c.dv:
            L = letters[c.h]
            add_list(ws, f"{L}{first}:{L}{last}", c.dv)

    ws.freeze_panes = f"{freeze_col}{first}"
    if filter:
        ws.auto_filter.ref = f"A{header_row}:{get_column_letter(len(cols))}{last}"
    return Table(ws, cols, first, last, letters, top, header_row)


# --------------------------------------------------------------- lists sheet
def lists_sheet(wb, lists, extra=10, title_text="Drop-down lists"):
    """Create an editable Lists tab. Returns {name: '=Lists!$A$2:$A$N'}."""
    ws = wb.create_sheet("Lists")
    out = {}
    label(ws, "A1", title_text + " - edit or add items in the yellow cells; drop-downs update automatically.",
          font=F_SUB)
    col = 1
    for name, items in lists.items():
        L = get_column_letter(col)
        header(ws, 2, col, [name], height=20)
        for i in range(len(items) + extra):
            inp(ws, f"{L}{3 + i}", items[i] if i < len(items) else None)
        last = 2 + len(items) + extra
        out[name] = f"=Lists!${L}$3:${L}${last}"
        ws.column_dimensions[L].width = max(16, len(name) + 4, *(len(str(x)) + 2 for x in items))
        col += 2
    return ws, out


# ------------------------------------------------------------- instructions
def instructions(wb, name, purpose, steps, tabs, notes=()):
    ws = wb.active
    ws.title = "Instructions"
    ws.sheet_view.showGridLines = False
    widths(ws, {"A": 3, "B": 28, "C": 90})
    title(ws, name, purpose)
    r = 4
    section(ws, f"B{r}", "How to use")
    r += 1
    for i, s in enumerate(steps, 1):
        label(ws, f"B{r}", f"Step {i}", bold=True)
        label(ws, f"C{r}", s, wrap=True)
        r += 1
    r += 1
    section(ws, f"B{r}", "Tabs in this workbook")
    r += 1
    for t, desc in tabs:
        label(ws, f"B{r}", t, bold=True)
        label(ws, f"C{r}", desc, wrap=True)
        r += 1
    r += 1
    section(ws, f"B{r}", "Colour legend")
    r += 1
    c = ws[f"B{r}"]
    c.value, c.font, c.fill, c.border = "Type here", F_INPUT, FILL_INPUT, BORDER
    label(ws, f"C{r}", "Input cell (yellow, blue text) - unlocked. Replace the sample data with your own.")
    r += 1
    c = ws[f"B{r}"]
    c.value, c.font, c.fill, c.border = "Calculated", F_CALC, FILL_CALC, BORDER
    label(ws, f"C{r}", "Calculated cell (grey, black text) - locked so formulas can't be overwritten by accident.")
    r += 2
    section(ws, f"B{r}", "Notes")
    r += 1
    base_notes = list(notes) + [
        "Sample data is fictional. Select the yellow sample rows and press Delete to clear them - formulas stay.",
        "Sheets are protected WITHOUT a password. To change formulas or layout: Review > Unprotect Sheet.",
        "Sorting and filtering work while protected (use the filter arrows on table headers).",
        "Not tax, legal or accounting advice. Check rates and rules for your province and year.",
    ]
    for nt in base_notes:
        label(ws, f"B{r}", "•", align="right")
        label(ws, f"C{r}", nt, wrap=True)
        r += 1
    for row in range(5, r):
        txt = ws[f"C{row}"].value
        if isinstance(txt, str) and len(txt) > 95:
            ws.row_dimensions[row].height = 13 * (len(txt) // 95 + 1)
    return ws


def settings_block(ws, row, items, col="A"):
    """items: list of (label, value, fmt, note). Writes label in col, input next to it.
    Returns {label: absolute ref}."""
    out = {}
    lc = col
    vc = get_column_letter(ord(col) - 64 + 1)
    nc = get_column_letter(ord(col) - 64 + 2)
    for i, (lab, val, f, note) in enumerate(items):
        r = row + i
        label(ws, f"{lc}{r}", lab, bold=True)
        if isinstance(val, str) and val.startswith("="):
            inp(ws, f"{vc}{r}", val, f)
        else:
            inp(ws, f"{vc}{r}", val, f)
        if note:
            label(ws, f"{nc}{r}", note, font=F_SUB)
        out[lab] = ref(ws, f"{vc}{r}")
    return out


# ------------------------------------------------------------------ finalise
def protect_all(wb):
    for ws in wb.worksheets:
        p = ws.protection
        p.sheet = True
        p.formatColumns = False
        p.formatRows = False
        p.formatCells = False
        p.autoFilter = False
        p.sort = False
        p.selectLockedCells = False
        p.selectUnlockedCells = False


def finalize(wb, path):
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if c.value is not None and (c.font is None or c.font.name != FONT):
                    f = c.font
                    c.font = Font(name=FONT, size=f.size or 10, bold=f.bold, italic=f.italic,
                                  color=f.color)
    protect_all(wb)
    wb.calculation = CalcProperties(fullCalcOnLoad=True)
    wb.active = 0
    wb.save(path)


def new_workbook():
    return Workbook()
