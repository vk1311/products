"""Minimal layout engine for fillable, letter-size business forms.

A form is a dict:
    {
        "slug": "invoice-canada",
        "title": "Invoice",
        "subtitle": "GST/HST ready",          # optional
        "meta": ["Invoice No.", "Date"],      # optional fields at top-right
        "body": [ elements... ],
    }

Elements are small tuples/dicts built with the helper functions at the bottom
of this file (section, fields, table, checklist, ...). Every element knows its
own height, so the engine can paginate and let "fill" tables use whatever room
is left on the page.
"""

import re

from reportlab.lib.colors import HexColor, transparent
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas

# ---------------------------------------------------------------- style ---
INK = HexColor("#1F2933")
MUTED = HexColor("#6B7280")
LINE = HexColor("#C3CAD2")
SOFT = HexColor("#EEF2F4")
ACCENT = HexColor("#2C5F6E")

PAGE_W, PAGE_H = letter
MARGIN_X = 46
TOP = PAGE_H - 44
BOTTOM = 52
WIDTH = PAGE_W - 2 * MARGIN_X

FONT = "Helvetica"
BOLD = "Helvetica-Bold"

PROVINCES = [
    " ", "AB", "BC", "MB", "NB", "NL", "NS", "NT", "NU", "ON", "PE", "QC", "SK", "YT",
]

PARA = ParagraphStyle("p", fontName=FONT, fontSize=9, leading=12.5, textColor=INK)
SMALL = ParagraphStyle("s", fontName=FONT, fontSize=7.5, leading=10, textColor=MUTED)


def _slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:28] or "f"


class Doc:
    def __init__(self, path, form):
        self.form = form
        self.c = canvas.Canvas(path, pagesize=letter)
        self.c.setTitle(form["title"])
        self.c.setAuthor("")
        self.c.setSubject(form.get("subtitle", form["title"]))
        self.c.setCreator("")
        self.n = 0
        self.page = 0
        self.y = TOP

    # ---- fillable widgets -------------------------------------------------
    def name(self, label):
        self.n += 1
        return f"{_slug(label)}_{self.n}"

    def text(self, label, x, y, w, h=13, size=9, multiline=False, value="", align=None):
        kw = dict(
            name=self.name(label), tooltip=label, value=value, x=x, y=y, width=w,
            height=h, borderWidth=0, fillColor=transparent, textColor=INK,
            fontName=FONT, fontSize=size, maxlen=0,
        )
        if multiline:
            kw["fieldFlags"] = "multiline"
        self.c.acroForm.textfield(**kw)

    def check(self, label, x, y, s=9):
        c = self.c
        c.setStrokeColor(MUTED)
        c.setLineWidth(0.7)
        c.rect(x, y, s, s, stroke=1, fill=0)
        c.acroForm.checkbox(
            name=self.name(label), tooltip=label, x=x, y=y, size=s, borderWidth=0,
            fillColor=transparent, textColor=INK, buttonStyle="check",
            fieldFlags="",
        )

    def province(self, label, x, y, w, h=13):
        self.c.acroForm.choice(
            name=self.name(label), tooltip=label, value=" ", options=PROVINCES,
            x=x, y=y, width=w, height=h, fieldFlags="combo", borderWidth=0,
            fillColor=transparent, textColor=INK, fontName=FONT, fontSize=9,
        )

    # ---- page furniture ---------------------------------------------------
    def new_page(self):
        if self.page:
            self.footer()
            self.c.showPage()
        self.page += 1
        c = self.c
        c.setFillColor(ACCENT)
        c.rect(MARGIN_X, PAGE_H - 26, WIDTH, 3, stroke=0, fill=1)
        if self.page == 1:
            self.header()
        else:
            c.setFont(BOLD, 11)
            c.setFillColor(INK)
            c.drawString(MARGIN_X, TOP - 6, self.form["title"])
            c.setFont(FONT, 8)
            c.setFillColor(MUTED)
            c.drawRightString(MARGIN_X + WIDTH, TOP - 6, "continued")
            self.y = TOP - 22

    def header(self):
        c, f = self.c, self.form
        meta = f.get("meta", [])
        tw = WIDTH - (200 if meta else 0)
        size = 21
        while c.stringWidth(f["title"], BOLD, size) > tw and size > 13:
            size -= 1
        c.setFont(BOLD, size)
        c.setFillColor(INK)
        c.drawString(MARGIN_X, TOP - 16, f["title"])
        y = TOP - 30
        if f.get("subtitle"):
            c.setFont(FONT, 8.5)
            c.setFillColor(MUTED)
            c.drawString(MARGIN_X, y, f["subtitle"])
        # meta fields, right aligned, stacked
        lw = max([c.stringWidth(m, FONT, 7.5) for m in meta] + [56]) + 6
        mw = max(180, lw + 110)
        mx = MARGIN_X + WIDTH - mw
        my = TOP - 2
        for label in meta:
            c.setFont(FONT, 7.5)
            c.setFillColor(MUTED)
            c.drawString(mx, my - 9, label)
            c.setStrokeColor(LINE)
            c.setLineWidth(0.6)
            c.line(mx + lw, my - 11, mx + mw, my - 11)
            self.text(label, mx + lw + 1, my - 10.5, mw - lw - 2, h=12, size=8.5)
            my -= 16
        self.y = min(y - 14, my - 10)

    def footer(self):
        c = self.c
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.line(MARGIN_X, BOTTOM - 14, MARGIN_X + WIDTH, BOTTOM - 14)
        c.setFont(FONT, 7)
        c.setFillColor(MUTED)
        c.drawString(MARGIN_X, BOTTOM - 25, self.form["title"])
        c.drawRightString(MARGIN_X + WIDTH, BOTTOM - 25, f"Page {self.page}")

    # ---- layout loop -------------------------------------------------------
    def build(self):
        self.new_page()
        body = list(self.form["body"])
        if not any(e.get("rows") == "fill" or e["t"] == "cards" for e in body):
            last = [k for k, e in enumerate(body) if e["t"] == "area"]
            if last:
                body[last[-1]] = dict(body[last[-1]], grow=True)
        i = 0
        while i < len(body):
            el = body[i]
            if el["t"] == "pagebreak":
                self.new_page()
                i += 1
                continue
            avail = self.y - BOTTOM
            if el.get("rows") == "fill":
                rest = 0
                for nxt in body[i + 1:]:
                    if nxt["t"] == "pagebreak":
                        break
                    rest += height(nxt)
                rows = int((avail - rest - el["head"] - GAP - 3) // el["rh"])
                el = dict(el, rows=max(rows, el.get("min", 4)))
            if el.get("grow"):
                rest = 0
                for nxt in body[i + 1:]:
                    if nxt["t"] == "pagebreak":
                        break
                    rest += height(nxt)
                el = dict(el, h=max(el["h"], min(avail - rest - 14 - GAP - 2, 240)))
            h = height(el)
            if h > avail:
                if el["t"] == "table" and avail > el["head"] + el["rh"] * 4:
                    fit = int((avail - el["head"]) // el["rh"])
                    draw(self, dict(el, rows=fit))
                    rest = dict(el, rows=el["rows"] - fit,
                                prefill=(el.get("prefill") or [])[fit:] or None,
                                offset=el.get("offset", 0) + fit)
                    body = body[:i] + [rest] + body[i + 1:]
                    self.new_page()
                    continue
                self.new_page()
                if height(el) > self.y - BOTTOM:
                    raise ValueError(f"{self.form['slug']}: element too tall: {el['t']}")
            draw(self, el)
            i += 1
        self.footer()
        self.c.showPage()
        self.c.save()
        return self.page


# --------------------------------------------------------------- elements --
GAP = 8


def pair(left_title, left_rows, right_title, right_rows):
    """Two titled field groups side by side (e.g. From / Bill To)."""
    return {"t": "pair", "l": (left_title, [list(r) for r in left_rows]),
            "r": (right_title, [list(r) for r in right_rows])}


def section(title):
    return {"t": "section", "title": title}


def fields(*rows, h=None):
    """rows: lists of (label, weight[, kind]) where kind in text|prov|area|value=..."""
    return {"t": "fields", "rows": [list(r) for r in rows]}


def table(cols, rows=8, rh=18, head=18, min=4, numbered=False, prefill=None):
    """cols: list of (label, weight). prefill: list of first-column values."""
    return {"t": "table", "cols": cols, "rows": rows, "rh": rh, "head": head,
            "min": min, "numbered": numbered, "prefill": prefill}


def checklist(items, cols=1, comments=False):
    return {"t": "checklist", "items": items, "cols": cols}


def groups(mapping, cols=2):
    """Checklist grouped under small headings, flowed into columns."""
    return {"t": "groups", "groups": list(mapping.items()), "cols": cols}


def consent(text):
    """A checkbox followed by a wrapped sentence (agreements, opt-ins)."""
    return {"t": "consent", "text": text}


def elist(items, blank=0, numbered=True, rh=19):
    """Numbered lines pre-filled with editable text (rules, instructions)."""
    return {"t": "elist", "items": list(items) + [""] * blank, "numbered": numbered, "rh": rh}


def area(label, h=60):
    return {"t": "area", "label": label, "h": h}


def para(text, style="p"):
    return {"t": "para", "text": text, "style": style}


def rules(items):
    return {"t": "rules", "items": items}


def options(label, choices, other=False):
    return {"t": "options", "label": label, "choices": choices, "other": other}


def yesno(questions, na=False, comment=False):
    return {"t": "yesno", "qs": questions, "na": na}


def matrix(items, cols, comment=True, first="Item", rh=16, wcomment=None):
    """Rows of items, each with a checkbox per column and a comment field."""
    return {"t": "matrix", "items": items, "cols": cols, "comment": comment,
            "first": first, "rh": rh}


def rating(items, scale=("1", "2", "3", "4", "5"), first="Criteria"):
    return {"t": "matrix", "items": items, "cols": list(scale), "comment": True,
            "first": first, "rh": 17}


def totals(lines, notes="Notes / Payment Terms", notes_h=None, prefill=None):
    """lines: list of labels, or (label, prefilled_value) tuples."""
    return {"t": "totals", "lines": lines, "notes": notes}


def signatures(labels):
    return {"t": "signatures", "labels": labels}


def spacer(h=8):
    return {"t": "spacer", "h": h}


def pagebreak():
    return {"t": "pagebreak"}


def cards(n, title, body_rows, note=None):
    """n identical bordered cards stacked on the page (gift certificates, receipts)."""
    return {"t": "cards", "n": n, "title": title, "rows": body_rows, "note": note}


# ---------------------------------------------------------------- measure --
FIELD_ROW = 29


def _para_h(text, style, width):
    p = Paragraph(text, PARA if style == "p" else SMALL)
    return p.wrap(width, 2000)[1]


def height(el):
    t = el["t"]
    if t == "section":
        return 24
    if t == "pair":
        return 20 + max(sum(_row_h(r) for r in el[k][1]) for k in ("l", "r")) + 6
    if t == "fields":
        return sum(_row_h(r) for r in el["rows"]) + 2
    if t == "table":
        return el["head"] + el["rh"] * el["rows"] + GAP + 2
    if t == "checklist":
        n = -(-len(el["items"]) // el["cols"])
        return n * 15 + GAP - 2
    if t == "groups":
        return _groups_layout(el)[0] + GAP
    if t == "area":
        return el["h"] + 14 + GAP
    if t == "elist":
        return len(el["items"]) * el["rh"] + GAP
    if t == "consent":
        return _para_h(el["text"], "p", WIDTH - 18) + 8
    if t == "para":
        return _para_h(el["text"], el["style"], WIDTH) + 6
    if t == "rules":
        return sum(_para_h(r, "p", WIDTH - 18) + 4 for r in el["items"]) + 4
    if t == "options":
        return 18 + 15 * (_options_layout(el)[1] - 1)
    if t == "yesno":
        return len(el["qs"]) * 17 + 28
    if t == "matrix":
        return 18 + len(el["items"]) * el["rh"] + GAP + 2
    if t == "totals":
        return max(len(el["lines"]) * 18, 60) + GAP + 4
    if t == "signatures":
        return 36 * (-(-len(el["labels"]) // 2)) + 4
    if t == "spacer":
        return el["h"]
    if t == "cards":
        return 1  # fills the rest of the page
    raise KeyError(t)


def _row_h(row):
    h = FIELD_ROW
    for f in row:
        if len(f) > 2 and isinstance(f[2], (int, float)):
            h = max(h, f[2] + 16)
    return h


def _groups_layout(el):
    cols = el["cols"]
    colh = [0] * cols
    place = []
    for title, items in el["groups"]:
        gh = 20 + len(items) * 14.5 + 6
        k = colh.index(min(colh))
        place.append((k, colh[k], title, items))
        colh[k] += gh
    return max(colh), place


# ------------------------------------------------------------------- draw --
def draw(d, el):
    globals()["_draw_" + el["t"]](d, el)


def _label(c, x, y, s, size=7.2, color=MUTED, bold=False):
    c.setFont(BOLD if bold else FONT, size)
    c.setFillColor(color)
    c.drawString(x, y, s)


def _draw_pair(d, el):
    c = d.c
    gutter = 26
    w = (WIDTH - gutter) / 2
    top = d.y
    low = top
    for k, x in (("l", MARGIN_X), ("r", MARGIN_X + w + gutter)):
        title, rows = el[k]
        d.y = top
        c.setFont(BOLD, 8.5)
        c.setFillColor(ACCENT)
        c.drawString(x, d.y - 12, title.upper())
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        c.line(x, d.y - 16, x + w, d.y - 16)
        d.y -= 18
        _draw_fields(d, {"rows": rows}, x, w)
        low = min(low, d.y)
    d.y = low - 6


def _draw_section(d, el):
    c = d.c
    y = d.y - 14
    c.setFont(BOLD, 8.5)
    c.setFillColor(ACCENT)
    c.drawString(MARGIN_X, y, el["title"].upper())
    tw = c.stringWidth(el["title"].upper(), BOLD, 8.5)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(MARGIN_X + tw + 8, y + 3, MARGIN_X + WIDTH, y + 3)
    d.y -= 24


def _draw_fields(d, el, x0=MARGIN_X, width=WIDTH):
    c = d.c
    for row in el["rows"]:
        rh = _row_h(row)
        total = sum(f[1] for f in row)
        gap = 12
        unit = (width - gap * (len(row) - 1)) / total
        x = x0
        for f in row:
            label, wt = f[0], f[1]
            kind = f[2] if len(f) > 2 else "text"
            w = unit * wt
            if isinstance(kind, (int, float)):  # multi-line box of given height
                bh = kind
                _label(c, x, d.y - 9, label)
                c.setStrokeColor(LINE)
                c.setLineWidth(0.6)
                c.rect(x, d.y - 13 - bh, w, bh, stroke=1, fill=0)
                d.text(label, x + 2, d.y - 12 - bh, w - 4, h=bh - 2, multiline=True)
            elif kind == "label":  # static text only
                _label(c, x, d.y - 16, label, size=8.5, color=INK)
            else:
                _label(c, x, d.y - 9, label)
                ly = d.y - rh + 3
                c.setStrokeColor(LINE)
                c.setLineWidth(0.6)
                c.line(x, ly, x + w, ly)
                if kind == "prov":
                    d.province(label, x, ly + 1, w)
                elif kind.startswith("value="):
                    d.text(label, x + 1, ly + 1, w - 2, value=kind[6:])
                else:
                    d.text(label, x + 1, ly + 1, w - 2)
            x += w + gap
        d.y -= rh
    d.y -= 2


def _draw_table(d, el):
    c = d.c
    cols = el["cols"]
    total = sum(w for _, w in cols)
    ws = [WIDTH * w / total for _, w in cols]
    top = d.y
    head, rh, rows = el["head"], el["rh"], el["rows"]
    c.setFillColor(SOFT)
    c.rect(MARGIN_X, top - head, WIDTH, head, stroke=0, fill=1)
    x = MARGIN_X
    for (label, _), w in zip(cols, ws):
        size = 7.2
        while c.stringWidth(label, BOLD, size) > w - 6 and size > 5.2:
            size -= 0.2
        _label(c, x + 3, top - head + (head - size) / 2 + 1, label, size=size, color=INK, bold=True)
        x += w
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    y = top - head
    for r in range(rows):
        yb = y - rh
        c.line(MARGIN_X, yb, MARGIN_X + WIDTH, yb)
        x = MARGIN_X
        for k, ((label, _), w) in enumerate(zip(cols, ws)):
            val = ""
            if k == 0 and el.get("prefill") and r < len(el["prefill"]):
                val = el["prefill"][r]
            if k == 0 and el.get("numbered"):
                val = str(r + 1 + el.get("offset", 0))
            if val and k == 0:
                _label(c, x + 3, yb + (rh - 8) / 2 + 1, val, size=8, color=INK)
            else:
                d.text(f"{label} {r + 1}", x + 2, yb + 1.5, w - 4, h=rh - 3, size=8.5 if rh >= 16 else 7.5)
            x += w
        y = yb
    # vertical rules
    x = MARGIN_X
    c.setStrokeColor(LINE)
    for w in ws[:-1]:
        x += w
        c.line(x, top, x, y)
    c.rect(MARGIN_X, y, WIDTH, top - y, stroke=1, fill=0)
    d.y = y - GAP - 2


def _draw_checklist(d, el):
    c = d.c
    cols = el["cols"]
    cw = WIDTH / cols
    per = -(-len(el["items"]) // cols)
    for i, item in enumerate(el["items"]):
        col, row = divmod(i, per)
        x = MARGIN_X + col * cw
        y = d.y - 12 - row * 15
        d.check(item, x, y, 9)
        _wrap_label(c, x + 15, y + 1.5, item, cw - 22)
    d.y -= per * 15 + GAP - 2


def _wrap_label(c, x, y, s, maxw, size=8.6):
    while c.stringWidth(s, FONT, size) > maxw and size > 6.4:
        size -= 0.2
    _label(c, x, y, s, size=size, color=INK)


def _draw_groups(d, el):
    c = d.c
    h, place = _groups_layout(el)
    cols = el["cols"]
    gutter = 18
    cw = (WIDTH - gutter * (cols - 1)) / cols
    for k, off, title, items in place:
        x = MARGIN_X + k * (cw + gutter)
        y = d.y - off - 12
        _label(c, x, y, title, size=8.6, color=INK, bold=True)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.line(x, y - 4, x + cw, y - 4)
        y -= 18
        for item in items:
            d.check(f"{title} {item}", x, y - 1, 8.5)
            _wrap_label(c, x + 14, y + 0.5, item, cw - 16, size=8.3)
            y -= 14.5
    d.y -= h + GAP


def _draw_area(d, el):
    c = d.c
    _label(c, MARGIN_X, d.y - 9, el["label"])
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.rect(MARGIN_X, d.y - 13 - el["h"], WIDTH, el["h"], stroke=1, fill=0)
    d.text(el["label"], MARGIN_X + 3, d.y - 12 - el["h"], WIDTH - 6, h=el["h"] - 2, multiline=True)
    d.y -= el["h"] + 14 + GAP


def _draw_elist(d, el):
    c = d.c
    y = d.y
    rh = el["rh"]
    base = 10 if rh >= 24 else 9
    for i, txt in enumerate(el["items"], 1):
        yb = y - rh
        x = MARGIN_X
        if el["numbered"]:
            c.setFont(BOLD, 9)
            c.setFillColor(ACCENT)
            c.drawString(x, yb + 5, f"{i}.")
            x += 18
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.line(x, yb + 2, MARGIN_X + WIDTH, yb + 2)
        size = base
        while stringWidth(txt, FONT, size) > MARGIN_X + WIDTH - x - 6 and size > 7:
            size -= 0.25
        d.text(f"line {i}", x, yb + 3, MARGIN_X + WIDTH - x, h=min(rh - 4, 16), size=size, value=txt)
        y = yb
    d.y = y - GAP


def _draw_consent(d, el):
    p = Paragraph(el["text"], PARA)
    _, h = p.wrap(WIDTH - 18, 2000)
    d.check(el["text"][:40], MARGIN_X, d.y - 11.5, 9)
    p.drawOn(d.c, MARGIN_X + 18, d.y - h - 2)
    d.y -= h + 8


def _draw_para(d, el):
    p = Paragraph(el["text"], PARA if el["style"] == "p" else SMALL)
    _, h = p.wrap(WIDTH, 2000)
    p.drawOn(d.c, MARGIN_X, d.y - h - 2)
    d.y -= h + 6


def _draw_rules(d, el):
    c = d.c
    for i, r in enumerate(el["items"], 1):
        p = Paragraph(r, PARA)
        _, h = p.wrap(WIDTH - 18, 2000)
        c.setFont(BOLD, 9)
        c.setFillColor(ACCENT)
        c.drawString(MARGIN_X, d.y - 11, f"{i}.")
        p.drawOn(c, MARGIN_X + 18, d.y - h - 2)
        d.y -= h + 4
    d.y -= 4


def _options_layout(el):
    """Place each choice; wrap onto extra lines when a row runs out of room."""
    sw = lambda t, f=FONT: stringWidth(t, f, 8.4)
    x0 = MARGIN_X + sw(el["label"], BOLD) + 12
    right = MARGIN_X + WIDTH
    items = [(ch, 13 + sw(ch)) for ch in el["choices"]]
    if el["other"]:
        items.append(("Other:", 13 + sw("Other:") + 110))
    x, line, out = x0, 0, []
    for ch, w in items:
        if x + w > right and x > x0:
            x, line = x0, line + 1
        out.append((ch, x, line))
        x += w + 14
    return out, line + 1


def _draw_options(d, el):
    c = d.c
    y = d.y - 12
    _label(c, MARGIN_X, y + 1.5, el["label"], size=8.4, color=INK, bold=True)
    places, _ = _options_layout(el)
    for ch, x, line in places:
        yy = y - line * 15
        d.check(f"{el['label']} {ch}", x, yy, 9)
        _label(c, x + 13, yy + 1.5, ch, size=8.4, color=INK)
        if el["other"] and ch == "Other:" and (ch, x, line) == places[-1]:
            lx = x + 13 + c.stringWidth("Other:", FONT, 8.4) + 4
            c.setStrokeColor(LINE)
            c.setLineWidth(0.6)
            c.line(lx, yy - 1, MARGIN_X + WIDTH, yy - 1)
            d.text(f"{el['label']} other text", lx + 1, yy, MARGIN_X + WIDTH - lx - 2, h=11, size=8)
    d.y -= height(el)


def _draw_yesno(d, el):
    c = d.c
    marks = ["Yes", "No"] + (["N/A"] if el["na"] else [])
    right = MARGIN_X + WIDTH
    xs = [right - 36 * (len(marks) - k) + 8 for k in range(len(marks))]
    y = d.y - 10
    for x, m in zip(xs, marks):
        _label(c, x - 2, y, m, size=7.2, bold=True)
    y -= 17
    for q in el["qs"]:
        _wrap_label(c, MARGIN_X, y + 1.5, q, xs[0] - MARGIN_X - 12)
        for x, m in zip(xs, marks):
            d.check(f"{q} {m}", x, y, 9)
        c.setStrokeColor(SOFT)
        c.setLineWidth(0.5)
        c.line(MARGIN_X, y - 4, right, y - 4)
        y -= 17
    d.y = y + 17 - GAP - 10


def _draw_matrix(d, el):
    c = d.c
    cols = el["cols"]
    cw = 38 if max(len(x) for x in cols) <= 6 else 54
    first_w = 210 if el["comment"] else WIDTH - cw * len(cols)
    rh = el["rh"]
    top = d.y
    c.setFillColor(SOFT)
    c.rect(MARGIN_X, top - 18, WIDTH, 18, stroke=0, fill=1)
    _label(c, MARGIN_X + 4, top - 12, el["first"], size=7.2, color=INK, bold=True)
    x0 = MARGIN_X + first_w
    for k, col in enumerate(cols):
        c.setFont(BOLD, 7)
        c.setFillColor(INK)
        c.drawCentredString(x0 + k * cw + cw / 2, top - 12, col)
    cx = x0 + cw * len(cols)
    if el["comment"]:
        _label(c, cx + 4, top - 12, "Comments", size=7.2, color=INK, bold=True)
    y = top - 18
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    for item in el["items"]:
        yb = y - rh
        c.line(MARGIN_X, yb, MARGIN_X + WIDTH, yb)
        _wrap_label(c, MARGIN_X + 4, yb + (rh - 8) / 2 + 1, item, first_w - 8, size=8.3)
        for k in range(len(cols)):
            d.check(f"{item} {cols[k]}", x0 + k * cw + cw / 2 - 4.5, yb + (rh - 9) / 2, 9)
        if el["comment"]:
            d.text(f"{item} comments", cx + 2, yb + 1.5, MARGIN_X + WIDTH - cx - 4, h=rh - 3, size=8)
        y = yb
    c.setStrokeColor(LINE)
    for k in range(len(cols) + (1 if el["comment"] else 0)):
        xx = x0 + k * cw
        c.line(xx, top, xx, y)
    c.rect(MARGIN_X, y, WIDTH, top - y, stroke=1, fill=0)
    d.y = y - GAP - 2


def _draw_totals(d, el):
    c = d.c
    lines = el["lines"]
    rw = 220
    rx = MARGIN_X + WIDTH - rw
    h = max(len(lines) * 18, 60)
    if el["notes"]:
        nw = WIDTH - rw - 18
        _label(c, MARGIN_X, d.y - 9, el["notes"])
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        c.rect(MARGIN_X, d.y - h, nw, h - 13, stroke=1, fill=0)
        d.text(el["notes"], MARGIN_X + 3, d.y - h + 1, nw - 6, h=h - 16, multiline=True)
    y = d.y
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    c.line(rx, y, rx + rw, y)
    for i, ln in enumerate(lines):
        label, val = (ln if isinstance(ln, tuple) else (ln, ""))
        last = i == len(lines) - 1
        yb = y - 18
        if last:
            c.setFillColor(SOFT)
            c.rect(rx, yb, rw, 18, stroke=0, fill=1)
        _label(c, rx + 6, yb + 6, label, size=8.4, color=INK, bold=last)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.line(rx, yb, rx + rw, yb)
        d.text(label, rx + 120, yb + 2, rw - 124, h=14, size=9, value=val)
        y = yb
    c.line(rx + 116, d.y, rx + 116, y)
    d.y -= h + GAP + 4


def _draw_signatures(d, el):
    c = d.c
    labels = el["labels"]
    colw = (WIDTH - 24) / 2
    for i, lab in enumerate(labels):
        col, row = i % 2, i // 2
        x = MARGIN_X + col * (colw + 24)
        y = d.y - 26 - row * 36
        sw = colw - 96
        c.setStrokeColor(INK)
        c.setLineWidth(0.6)
        c.line(x, y, x + sw, y)
        c.line(x + sw + 12, y, x + colw, y)
        _label(c, x, y - 9, lab)
        _label(c, x + sw + 12, y - 9, "Date")
        d.text(lab, x + 1, y + 1, sw - 2, h=14, size=10)
        d.text(f"{lab} date", x + sw + 13, y + 1, colw - sw - 14, h=14)
    d.y -= 36 * (-(-len(labels) // 2)) + 4


def _draw_spacer(d, el):
    d.y -= el["h"]


def _draw_cards(d, el):
    c = d.c
    n = el["n"]
    top = d.y
    gap = 14
    ch = (top - BOTTOM - gap * (n - 1)) / n
    for k in range(n):
        yt = top - k * (ch + gap)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.8)
        c.setDash(4, 3)
        c.rect(MARGIN_X - 4, yt - ch, WIDTH + 8, ch, stroke=1, fill=0)
        c.setDash()
        c.setFillColor(ACCENT)
        c.rect(MARGIN_X - 4, yt - ch, 5, ch, stroke=0, fill=1)
        c.setFont(BOLD, 14)
        c.setFillColor(INK)
        c.drawString(MARGIN_X + 12, yt - 24, el["title"])
        # No. field top right
        _label(c, MARGIN_X + WIDTH - 140, yt - 22, "No.")
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        c.line(MARGIN_X + WIDTH - 122, yt - 24, MARGIN_X + WIDTH - 8, yt - 24)
        d.text("No", MARGIN_X + WIDTH - 121, yt - 23, 112, h=12)
        y = yt - 34
        inner = WIDTH - 24
        step = min(44, max(28, (ch - 62) / len(el["rows"])))
        for row in el["rows"]:
            total = sum(f[1] for f in row)
            g = 12
            unit = (inner - g * (len(row) - 1)) / total
            x = MARGIN_X + 12
            for f in row:
                w = unit * f[1]
                _label(c, x, y - 9, f[0])
                c.setStrokeColor(LINE)
                c.line(x, y - 26, x + w, y - 26)
                if len(f) > 2 and f[2] == "prov":
                    d.province(f[0], x, y - 25, w)
                else:
                    d.text(f[0], x + 1, y - 25, w - 2)
                x += w + g
            y -= step
        if el.get("note"):
            p = Paragraph(el["note"], SMALL)
            _, ph = p.wrap(inner, 200)
            p.drawOn(c, MARGIN_X + 12, yt - ch + 8)
    d.y = BOTTOM


def build(path, form):
    return Doc(path, form).build()
