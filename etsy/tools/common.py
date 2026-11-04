"""Shared building blocks for Canadian business forms."""

from engine import (area, consent, elist, checklist, fields, groups, matrix, options, pair, para,
                    rating, rules, section, signatures, spacer, table, totals, yesno,
                    cards, pagebreak)

# Province / territory sales tax as printed on the province-specific forms
# (rates current as of 2026 - update here and rebuild if a rate changes).
TAX = {
    "AB": ("Alberta", [("GST", "5%")], []),
    "BC": ("British Columbia", [("GST", "5%"), ("PST", "7%")], ["PST No."]),
    "MB": ("Manitoba", [("GST", "5%"), ("RST", "7%")], ["RST No."]),
    "NB": ("New Brunswick", [("HST", "15%")], []),
    "NL": ("Newfoundland and Labrador", [("HST", "15%")], []),
    "NS": ("Nova Scotia", [("HST", "14%")], []),
    "NT": ("Northwest Territories", [("GST", "5%")], []),
    "NU": ("Nunavut", [("GST", "5%")], []),
    "ON": ("Ontario", [("HST", "13%")], []),
    "PE": ("Prince Edward Island", [("HST", "15%")], []),
    "QC": ("Quebec", [("GST", "5%"), ("QST", "9.975%")], ["QST No."]),
    "SK": ("Saskatchewan", [("GST", "5%"), ("PST", "6%")], ["PST No."]),
    "YT": ("Yukon", [("GST", "5%")], []),
}

PAYMENT = ["Cash", "Cheque", "Credit card", "Debit", "Email money transfer", "Direct deposit"]


def biz_rows(tax_ids=("GST/HST No.",)):
    rows = [
        [("Business Name", 1)],
        [("Address", 1)],
        [("City", 2), ("Province", 1, "prov"), ("Postal Code", 1.2)],
        [("Phone", 1), ("Email", 1.4)],
    ]
    if tax_ids:
        rows.append([(t, 1) for t in tax_ids])
    return rows


def client_rows(extra=None):
    rows = [
        [("Client / Company Name", 1)],
        [("Address", 1)],
        [("City", 2), ("Province", 1, "prov"), ("Postal Code", 1.2)],
        [("Phone", 1), ("Email", 1.4)],
    ]
    if extra:
        rows.append(extra)
    return rows


def parties(left="From", right="Bill To", tax_ids=("GST/HST No.",), right_extra=None):
    return pair(left, biz_rows(tax_ids), right, client_rows(right_extra))


def contact_block(title="Contact Information"):
    return [
        section(title),
        fields(
            [("Full Name", 2), ("Phone", 1)],
            [("Street Address", 2), ("Email", 1.2)],
            [("City", 2), ("Province", 1, "prov"), ("Postal Code", 1.1)],
        ),
    ]


def line_items(rows="fill", cols=None, rh=18):
    cols = cols or [("Description", 6), ("Qty", 1.1), ("Unit Price", 1.6), ("Amount", 1.7)]
    return table(cols, rows=rows, rh=rh)


def tax_lines(prov=None, extra_before=("Discount",), paid=True):
    """Totals block lines, either province-specific or the flexible version."""
    lines = ["Subtotal"] + list(extra_before)
    if prov:
        for name, rate in TAX[prov][1]:
            lines.append(f"{name} ({rate})")
    else:
        lines += ["GST / HST  ____ %", "PST / QST  ____ %"]
    lines.append("Total (CAD)")
    if paid:
        lines += ["Amount Paid", "Balance Due"]
    return lines


def payment_options(label="Payment Method:", choices=None):
    return options(label, choices or PAYMENT[:5])


def sign(*labels):
    return signatures(list(labels))


def fill_table(cols, rh=18, numbered=False):
    return table(cols, rows="fill", rh=rh, numbered=numbered)
