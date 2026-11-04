"""Batch 1 - invoices, quotes and receipts (Canadian tax ready)."""

from common import *  # noqa: F401,F403

CAT = "billing"
FORMS = []


def add(**kw):
    kw.setdefault("cat", CAT)
    FORMS.append(kw)


# 1. Flexible Canadian invoice --------------------------------------------
add(
    slug="invoice-canada",
    title="Invoice",
    subtitle="GST / HST / PST ready  ·  Amounts in Canadian dollars",
    meta=["Invoice No.", "Date", "Due Date"],
    body=[
        parties(),
        line_items(),
        totals(tax_lines()),
        payment_options(),
        para("Thank you for your business.", "s"),
    ],
    name="Canadian Invoice Template",
    short="Invoice",
    about="A clean, all-purpose invoice for Canadian small businesses with blank GST/HST and PST/QST lines so it works in every province and territory.",
    tags=["canadian invoice", "invoice template", "gst hst invoice", "fillable invoice",
          "printable invoice", "invoice pdf", "small business form", "billing form"],
    price=3.95,
)

# 2-14. Province & territory invoices --------------------------------------
TAX_IDS = {
    "AB": ("GST Registration No.",), "NT": ("GST Registration No.",),
    "NU": ("GST Registration No.",), "YT": ("GST Registration No.",),
    "ON": ("HST Registration No.",), "NB": ("HST Registration No.",),
    "NL": ("HST Registration No.",), "NS": ("HST Registration No.",),
    "PE": ("HST Registration No.",),
    "QC": ("GST No.", "QST No."), "BC": ("GST No.", "PST No."),
    "SK": ("GST No.", "PST No."), "MB": ("GST No.", "RST No."),
}
SLUG = {
    "AB": "alberta", "BC": "british-columbia", "MB": "manitoba", "NB": "new-brunswick",
    "NL": "newfoundland-labrador", "NS": "nova-scotia", "NT": "northwest-territories",
    "NU": "nunavut", "ON": "ontario", "PE": "pei", "QC": "quebec",
    "SK": "saskatchewan", "YT": "yukon",
}
PROV_TAGS = {
    "AB": ["alberta invoice", "alberta business", "gst invoice"],
    "BC": ["bc invoice", "bc business", "pst invoice", "gst pst invoice"],
    "MB": ["manitoba invoice", "manitoba business", "rst invoice"],
    "NB": ["new brunswick", "nb invoice", "hst invoice"],
    "NL": ["newfoundland", "nl invoice", "hst invoice"],
    "NS": ["nova scotia invoice", "nova scotia", "hst invoice"],
    "NT": ["nwt invoice", "northwest territory", "gst invoice"],
    "NU": ["nunavut invoice", "nunavut business", "gst invoice"],
    "ON": ["ontario invoice", "ontario business", "hst invoice", "13 hst"],
    "PE": ["pei invoice", "pei business", "hst invoice"],
    "QC": ["quebec invoice", "qst invoice", "tps tvq", "gst qst invoice"],
    "SK": ["sask invoice", "saskatchewan", "pst invoice", "gst pst invoice"],
    "YT": ["yukon invoice", "yukon business", "gst invoice"],
}

for code in ["ON", "QC", "BC", "AB", "MB", "SK", "NS", "NB", "NL", "PE", "YT", "NT", "NU"]:
    pname, taxes, _ = TAX[code]
    taxdesc = " + ".join(f"{n} {r}" for n, r in taxes)
    add(
        slug=f"invoice-{SLUG[code]}",
        title=f"Invoice",
        subtitle=f"{pname}  ·  {taxdesc}  ·  Amounts in Canadian dollars",
        meta=["Invoice No.", "Date", "Due Date"],
        body=[
            parties(tax_ids=TAX_IDS[code]),
            line_items(),
            totals(tax_lines(code)),
            payment_options(),
            para("Thank you for your business.", "s"),
        ],
        name=f"{pname} Invoice Template",
        short=f"{pname} Invoice",
        about=f"An invoice set up for {pname} with {taxdesc} lines already labelled, plus space for your {' and '.join(TAX_IDS[code])}",
        tags=PROV_TAGS[code] + ["canadian invoice", "invoice template", "fillable invoice",
                                "printable invoice"],
        prov=code,
        price=3.95,
    )

# 15. Quote / estimate --------------------------------------------------------
add(
    slug="quote-estimate",
    title="Quote",
    subtitle="Price quotation  ·  Amounts in Canadian dollars",
    meta=["Quote No.", "Date", "Valid Until"],
    body=[
        parties("From", "Prepared For"),
        line_items(),
        totals(tax_lines(paid=False) + ["Deposit Required"], notes="Terms & Conditions"),
        signatures(["Customer Acceptance (signature)", "Authorized By"]),
    ],
    name="Price Quote Template",
    short="Quote Form",
    about="A professional price quote with GST/HST and PST/QST lines, a validity date, deposit line and a customer acceptance signature.",
    tags=["quote template", "estimate form", "price quote", "quotation form",
          "canadian quote", "job quote", "fillable quote"],
    price=3.95,
)

# 16. Contractor estimate ----------------------------------------------------
add(
    slug="contractor-estimate",
    title="Contractor Estimate",
    subtitle="Labour & materials estimate  ·  Amounts in Canadian dollars",
    meta=["Estimate No.", "Date", "Valid Until"],
    body=[
        parties("Contractor", "Customer", right_extra=[("Job Site Address", 1)]),
        area("Scope of Work", 46),
        table([("Labour Description", 6), ("Hours", 1.1), ("Rate", 1.4), ("Amount", 1.6)], rows=5),
        table([("Materials", 6), ("Qty", 1.1), ("Unit Cost", 1.4), ("Amount", 1.6)], rows="fill"),
        totals(["Labour", "Materials", "Subtotal", "GST / HST  ____ %", "PST / QST  ____ %",
                "Total Estimate (CAD)"], notes="Exclusions / Notes"),
        signatures(["Customer Acceptance", "Contractor"]),
    ],
    name="Contractor Estimate Form",
    short="Contractor Estimate",
    about="Estimate form for trades and renovation contractors that splits labour and materials, with Canadian sales tax lines and a sign-off area.",
    tags=["contractor estimate", "job estimate", "renovation quote", "construction form",
          "trades estimate", "labour estimate", "contractor form"],
    price=4.45,
)

# 17. Hourly service invoice --------------------------------------------------
add(
    slug="service-invoice-hourly",
    title="Service Invoice",
    subtitle="Hourly services  ·  Amounts in Canadian dollars",
    meta=["Invoice No.", "Date", "Due Date"],
    body=[
        parties(),
        line_items(cols=[("Date", 1.4), ("Service Description", 5), ("Hours", 1), ("Rate", 1.3), ("Amount", 1.6)]),
        totals(tax_lines()),
        payment_options(),
    ],
    name="Hourly Service Invoice",
    short="Service Invoice",
    about="An hourly-billing invoice for consultants, freelancers and service providers, with date, hours and rate columns and Canadian tax lines.",
    tags=["service invoice", "hourly invoice", "freelance invoice", "consultant invoice",
          "canadian invoice", "billing form", "fillable invoice"],
    price=3.95,
)

# 18. Contractor invoice ------------------------------------------------------
add(
    slug="contractor-invoice",
    title="Contractor Invoice",
    subtitle="Labour & materials  ·  Amounts in Canadian dollars",
    meta=["Invoice No.", "Date", "Due Date"],
    body=[
        parties("Contractor", "Bill To", right_extra=[("Job Site Address", 1)]),
        table([("Labour Description", 6), ("Hours", 1.1), ("Rate", 1.4), ("Amount", 1.6)], rows=6),
        table([("Materials", 6), ("Qty", 1.1), ("Unit Cost", 1.4), ("Amount", 1.6)], rows="fill"),
        totals(["Labour", "Materials", "Subtotal", "GST / HST  ____ %", "PST / QST  ____ %",
                "Total (CAD)", "Deposit Received", "Balance Due"]),
        payment_options(),
    ],
    name="Contractor Invoice Template",
    short="Contractor Invoice",
    about="An invoice for trades, handyman and renovation work with separate labour and materials tables, deposit tracking and Canadian tax lines.",
    tags=["contractor invoice", "handyman invoice", "trades invoice", "labour invoice",
          "construction form", "canadian invoice", "renovation invoice"],
    price=3.95,
)

# 19. Proforma invoice --------------------------------------------------------
add(
    slug="proforma-invoice",
    title="Proforma Invoice",
    subtitle="Preliminary bill of sale  ·  Not a request for payment",
    meta=["Proforma No.", "Date", "Valid Until"],
    body=[
        parties("Seller", "Buyer"),
        fields([("Shipping Method", 1), ("Est. Ship Date", 1), ("Terms of Sale", 1), ("Currency", 0.7, "value=CAD")]),
        line_items(cols=[("Description", 5), ("HS Code", 1.4), ("Qty", 1), ("Unit Price", 1.4), ("Amount", 1.6)]),
        totals(["Subtotal", "Shipping", "GST / HST  ____ %", "PST / QST  ____ %", "Estimated Total"],
               notes="Notes"),
        signatures(["Authorized Signature"]),
    ],
    name="Proforma Invoice Template",
    short="Proforma Invoice",
    about="A proforma (preliminary) invoice for quoting goods before shipment, with HS code column, terms of sale and Canadian tax lines.",
    tags=["proforma invoice", "pro forma", "export invoice", "shipping invoice",
          "wholesale form", "canadian invoice", "invoice template"],
    price=3.95,
)

# 20. Credit memo -------------------------------------------------------------
add(
    slug="credit-memo",
    title="Credit Memo",
    subtitle="Credit note  ·  Amounts in Canadian dollars",
    meta=["Credit Memo No.", "Date", "Original Invoice"],
    body=[
        parties("From", "Credit To"),
        options("Reason:", ["Return", "Overcharge", "Damaged goods", "Discount", "Cancellation"], other=True),
        line_items(),
        totals(["Credit Subtotal", "GST / HST  ____ %", "PST / QST  ____ %", "Total Credit (CAD)"],
               notes="Credit applied as"),
        signatures(["Authorized By"]),
    ],
    name="Credit Memo Form",
    short="Credit Memo",
    about="A credit memo (credit note) to document returns, overcharges or discounts against an original invoice, including tax reversal lines.",
    tags=["credit memo", "credit note", "refund form", "billing adjustment",
          "accounting form", "canadian business", "invoice credit"],
    price=3.45,
)

# 21. Statement of account ---------------------------------------------------
add(
    slug="statement-of-account",
    title="Statement of Account",
    subtitle="Customer account summary  ·  Amounts in Canadian dollars",
    meta=["Statement Date", "Account No.", "Period"],
    body=[
        parties("From", "Customer"),
        table([("Date", 1.3), ("Reference / Invoice", 2.2), ("Description", 3.4), ("Charges", 1.4),
               ("Payments", 1.4), ("Balance", 1.4)], rows="fill"),
        table([("Current", 1), ("1-30 Days", 1), ("31-60 Days", 1), ("61-90 Days", 1),
               ("Over 90 Days", 1), ("Amount Due", 1)], rows=1, rh=22),
        para("Please include the account number with your payment. Thank you.", "s"),
    ],
    name="Statement of Account",
    short="Account Statement",
    about="A customer statement showing invoices, payments and running balance with a built-in aging summary (current, 30, 60, 90+ days).",
    tags=["account statement", "customer statement", "ar statement", "billing statement",
          "aging summary", "bookkeeping form", "canadian business"],
    price=3.45,
)

# 22. Sales receipt -----------------------------------------------------------
add(
    slug="sales-receipt",
    title="Sales Receipt",
    subtitle="Proof of purchase  ·  Amounts in Canadian dollars",
    meta=["Receipt No.", "Date"],
    body=[
        parties("Sold By", "Sold To"),
        line_items(),
        totals(tax_lines(paid=False) + ["Amount Paid"], notes="Return Policy / Notes"),
        payment_options(),
        signatures(["Received By"]),
    ],
    name="Sales Receipt Template",
    short="Sales Receipt",
    about="A full-page sales receipt with item lines, GST/HST and PST/QST lines, payment method and return-policy notes.",
    tags=["sales receipt", "receipt template", "purchase receipt", "payment receipt",
          "canadian receipt", "retail receipt", "fillable receipt"],
    price=3.45,
)

# 23. Rent receipt ------------------------------------------------------------
add(
    slug="rent-receipt",
    title="Rent Receipt",
    subtitle="Residential rent payment  ·  Amounts in Canadian dollars",
    body=[
        cards(3, "Rent Receipt", [
            [("Date Received", 1), ("Amount (CAD)", 1), ("Rental Period", 1.4)],
            [("Received From (Tenant)", 1.6), ("Rental Unit Address", 2)],
            [("Payment Method", 1), ("Landlord / Agent Name", 1.4), ("Signature", 1.4)],
        ], note="Keep this receipt for your records. Tenants may need rent receipts for provincial tax credits."),
    ],
    name="Rent Receipt",
    short="Rent Receipt",
    about="Three fillable rent receipts per page for landlords and property managers, with tenant, unit, rental period and payment method.",
    tags=["rent receipt", "landlord form", "rental receipt", "tenant receipt",
          "property manager", "canadian landlord", "rent payment"],
    cat="rental",
    price=3.45,
)

# 24. Cash receipt ------------------------------------------------------------
add(
    slug="cash-receipt",
    title="Payment Receipt",
    subtitle="Three receipts per page",
    body=[
        cards(3, "Payment Receipt", [
            [("Date", 1), ("Amount (CAD)", 1), ("Payment Method", 1.2)],
            [("Received From", 2), ("Phone / Email", 1.4)],
            [("For", 2.2), ("Received By", 1.2)],
        ]),
    ],
    name="Payment Receipt",
    short="Payment Receipt",
    about="Three fillable payment receipts per page - perfect for cash, cheque or card payments at markets, studios and service calls.",
    tags=["cash receipt", "payment receipt", "receipt book", "simple receipt",
          "money receipt", "fillable receipt", "receipt template"],
    price=2.95,
)

# 25. Deposit receipt ---------------------------------------------------------
add(
    slug="deposit-receipt",
    title="Deposit Receipt",
    subtitle="Acknowledgement of deposit  ·  Amounts in Canadian dollars",
    meta=["Receipt No.", "Date"],
    body=[
        parties("Received By", "Received From"),
        section("Deposit Details"),
        fields(
            [("Deposit Amount (CAD)", 1), ("Total Price (CAD)", 1), ("Balance Remaining", 1)],
            [("Deposit For (product, service, event or booking)", 1)],
            [("Balance Due Date", 1), ("Booking / Order No.", 1)],
        ),
        payment_options(),
        options("Deposit is:", ["Refundable", "Non-refundable", "Partially refundable"]),
        area("Refund & Cancellation Terms", 70),
        signatures(["Received By", "Customer"]),
    ],
    name="Deposit Receipt Form",
    short="Deposit Receipt",
    about="A deposit receipt for bookings, custom orders and services that records the amount, balance remaining and refund terms.",
    tags=["deposit receipt", "booking deposit", "deposit form", "payment receipt",
          "custom order form", "canadian business", "retainer receipt"],
    price=3.45,
)
