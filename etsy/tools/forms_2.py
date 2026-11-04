"""Batch 2 - sales, purchasing and bookkeeping."""

from common import *  # noqa: F401,F403

FORMS = []


def add(**kw):
    FORMS.append(kw)


CASL = ("I agree to receive emails from this business about my account, offers and news. "
        "I can unsubscribe at any time.")

add(
    slug="purchase-order", cat="billing",
    title="Purchase Order",
    subtitle="Amounts in Canadian dollars",
    meta=["PO No.", "Date", "Required By"],
    body=[
        pair("Vendor", client_rows(), "Ship To", [
            [("Company Name", 1)], [("Attention", 1)], [("Address", 1)],
            [("City", 2), ("Province", 1, "prov"), ("Postal Code", 1.2)],
        ]),
        fields([("Requested By", 1), ("Department", 1), ("Shipping Method", 1), ("Payment Terms", 1)]),
        line_items(cols=[("Item No.", 1.4), ("Description", 5), ("Qty", 1), ("Unit Price", 1.4), ("Amount", 1.6)]),
        totals(["Subtotal", "Shipping", "GST / HST  ____ %", "PST / QST  ____ %", "Total (CAD)"],
               notes="Special Instructions"),
        signatures(["Authorized By"]),
    ],
    name="Purchase Order Form", short="Purchase Order",
    about="A purchase order for buying supplies, inventory and equipment from vendors, with ship-to details, line items and Canadian tax lines.",
    tags=["purchase order", "po form", "vendor order", "purchasing form", "supply order",
          "procurement form", "order template"],
    price=3.95,
)

add(
    slug="order-form", cat="billing",
    title="Order Form",
    subtitle="Customer order  ·  Amounts in Canadian dollars",
    meta=["Order No.", "Order Date", "Needed By"],
    body=[
        *contact_block("Customer"),
        line_items(cols=[("Item / SKU", 1.6), ("Description", 4.2), ("Size / Colour", 1.8), ("Qty", 0.9),
                         ("Price", 1.3), ("Total", 1.5)]),
        totals(["Subtotal", "Shipping / Delivery", "GST / HST  ____ %", "PST / QST  ____ %",
                "Order Total (CAD)", "Deposit Paid", "Balance Due"], notes="Personalization / Notes"),
        options("Delivery:", ["Pickup", "Local delivery", "Ship by mail"]),
        payment_options(),
    ],
    name="Customer Order Form", short="Order Form",
    about="A product order form for makers, bakers, boutiques and wholesalers, with size and colour column, personalization notes, delivery choice and deposit tracking.",
    tags=["order form", "product order form", "custom order form", "craft order form",
          "bakery order form", "wholesale order", "sales order"],
    price=3.95,
)

add(
    slug="change-order", cat="billing",
    title="Change Order",
    subtitle="Project change request & approval",
    meta=["Change Order No.", "Date", "Original Contract No."],
    body=[
        section("Project"),
        fields([("Project Name", 2), ("Client", 1.4)],
               [("Project Address", 2), ("Contractor", 1.4)]),
        area("Description of Change", 70),
        area("Reason for Change", 44),
        table([("Cost Item", 5), ("Qty", 1), ("Unit Cost", 1.4), ("Amount", 1.6)], rows=6),
        totals(["Original Contract Amount", "Previous Change Orders", "This Change Order",
                "GST / HST  ____ %", "Revised Contract Total"], notes="Schedule Impact"),
        signatures(["Client Approval", "Contractor"]),
    ],
    name="Change Order Form", short="Change Order",
    about="A construction and project change order that documents the change, the reason, cost and schedule impact, and the revised contract total.",
    tags=["change order", "construction form", "contractor form", "project change",
          "renovation form", "scope change", "change request"],
    price=3.95,
)

add(
    slug="price-list", cat="billing",
    title="Price List",
    subtitle="Products & services  ·  Prices in Canadian dollars",
    meta=["Effective Date", "Updated"],
    body=[
        fields([("Business Name", 2), ("Phone", 1), ("Website / Email", 1.4)]),
        fill_table([("Item / Service", 2.6), ("Description", 4.4), ("Unit", 1), ("Price (CAD)", 1.4)]),
        para("Prices exclude applicable GST/HST and PST/QST unless noted. Prices subject to change.", "s"),
    ],
    name="Price List Template", short="Price List",
    about="A simple price list for products or services that you can type on screen, print for your counter or attach to quotes.",
    tags=["price list", "service menu", "pricing sheet", "rate sheet", "price sheet",
          "service price list", "product price list"],
    price=2.95,
)

add(
    slug="bid-proposal", cat="billing",
    title="Bid Proposal",
    subtitle="Proposal for work  ·  Amounts in Canadian dollars",
    meta=["Bid No.", "Date", "Valid Until"],
    body=[
        parties("Submitted By", "Submitted To", right_extra=[("Project Location", 1)]),
        area("Scope of Work", 56),
        table([("Work Item", 5.5), ("Qty", 1), ("Unit Price", 1.4), ("Amount", 1.6)], rows=6),
        totals(["Subtotal", "GST / HST  ____ %", "PST / QST  ____ %", "Total Bid (CAD)"],
               notes="Exclusions"),
        fields([("Start Date", 1), ("Completion Date", 1), ("Payment Schedule", 2)]),
        signatures(["Submitted By", "Accepted By"]),
    ],
    name="Bid Proposal Form", short="Bid Proposal",
    about="A bid proposal for contractors and service companies to quote a project with scope, itemized pricing, exclusions, timeline and acceptance.",
    tags=["bid proposal", "bid form", "job proposal", "contractor bid", "project bid",
          "construction bid", "proposal template"],
    price=3.95,
)

add(
    slug="refund-request", cat="billing",
    title="Refund Request Form",
    subtitle="Customer refund request",
    meta=["Request No.", "Date"],
    body=[
        *contact_block("Customer"),
        section("Purchase"),
        fields([("Order / Receipt No.", 1), ("Purchase Date", 1), ("Amount Paid (CAD)", 1)],
               [("Product / Service", 1)]),
        options("Reason:", ["Defective", "Not as described", "Wrong item", "Cancelled", "Changed mind"], other=True),
        area("Details", 60),
        options("Refund to:", ["Original payment", "Store credit", "Cheque", "Exchange"]),
        section("Office Use"),
        options("Decision:", ["Approved", "Partially approved", "Declined"]),
        fields([("Refund Amount (CAD)", 1), ("Tax Refunded", 1), ("Date Processed", 1), ("Processed By", 1)]),
        signatures(["Customer Signature", "Approved By"]),
    ],
    name="Refund Request Form", short="Refund Form",
    about="A refund request form that captures the purchase, reason and preferred refund method, with an office-use section for approval and tax refunded.",
    tags=["refund form", "refund request", "return form", "customer service",
          "store policy form", "money back form", "retail form"],
    price=3.45,
)

add(
    slug="return-authorization", cat="billing",
    title="Return Authorization",
    subtitle="Return merchandise authorization (RMA)",
    meta=["RMA No.", "Date Issued"],
    body=[
        *contact_block("Customer"),
        fields([("Original Order / Invoice No.", 1), ("Purchase Date", 1)]),
        table([("Item / SKU", 1.6), ("Description", 4), ("Qty", 0.9), ("Reason for Return", 3), ("Condition", 1.5)], rows=7),
        options("Requested:", ["Refund", "Exchange", "Repair", "Store credit"]),
        area("Return Shipping Instructions", 44),
        section("Received (Office Use)"),
        fields([("Date Received", 1), ("Inspected By", 1), ("Restocking Fee", 1), ("Credit Issued", 1)]),
        signatures(["Authorized By"]),
    ],
    name="Return Authorization Form", short="RMA Form",
    about="A return merchandise authorization (RMA) form listing returned items, reasons and condition, with shipping instructions and a receiving section.",
    tags=["return form", "rma form", "return authorization", "product return",
          "returns policy", "merchandise return", "warranty return"],
    price=3.45,
)

add(
    slug="credit-application", cat="billing",
    title="Business Credit Application",
    subtitle="Application for trade credit / open account",
    meta=["Date"],
    body=[
        section("Business Information"),
        fields([("Legal Business Name", 2), ("Operating Name", 1.4)],
               [("Address", 2), ("City", 1)],
               [("Province", 0.7, "prov"), ("Postal Code", 0.9), ("Phone", 1), ("Email", 1.4)],
               [("Business Number (BN)", 1), ("Years in Business", 0.8), ("Credit Limit Requested", 1)]),
        options("Structure:", ["Sole proprietor", "Partnership", "Corporation", "Non-profit"], other=True),
        section("Accounts Payable Contact"),
        fields([("Name", 1.4), ("Phone", 1), ("Email", 1.4)]),
        section("Bank Reference"),
        fields([("Bank / Credit Union", 1.4), ("Branch / Address", 1.6), ("Phone", 1)]),
        section("Trade References"),
        table([("Company", 3), ("Contact", 2), ("Phone", 1.6), ("Email", 2.4)], rows="fill", min=3, rh=20),
        para("The applicant certifies the information above is accurate and authorizes the seller to contact the references listed "
             "to assess credit. Payment terms are as stated on invoices unless otherwise agreed in writing.", "s"),
        signatures(["Authorized Signature & Title", "Approved By (Office)"]),
    ],
    name="Business Credit Application", short="Credit Application",
    about="A business credit (open account) application with company details, accounts payable contact, bank and trade references and authorization.",
    tags=["credit application", "trade credit", "net 30 application", "b2b form",
          "account application", "wholesale account", "credit form"],
    price=3.95,
)

add(
    slug="customer-information", cat="ops",
    title="Customer Information Form",
    subtitle="Customer profile",
    meta=["Customer No.", "Date"],
    body=[
        *contact_block("Customer"),
        fields([("Company (if applicable)", 2), ("Alternate Phone", 1)]),
        section("Billing Address (if different)"),
        fields([("Street Address", 2), ("City", 1)], [("Province", 1, "prov"), ("Postal Code", 1), ("Country", 1.4, "value=Canada")]),
        section("Preferences"),
        options("Preferred contact:", ["Phone", "Text", "Email"]),
        options("How did you hear about us?", ["Referral", "Online search", "Social media", "Sign / flyer"], other=True),
        area("Notes / Special Requests", 56),
        consent(CASL),
        signatures(["Customer Signature"]),
    ],
    name="Customer Information Form", short="Customer Info Form",
    about="A customer information sheet to collect contact, billing and preference details, including an opt-in checkbox for email marketing consent.",
    tags=["customer info form", "client info sheet", "customer profile", "contact form",
          "new customer form", "client record", "intake form"],
    canada="Canadian-ready: province/territory drop-down and postal code fields, plus an express email-consent checkbox to help with Canada's anti-spam rules.",
    price=3.45,
)

add(
    slug="client-intake", cat="ops",
    title="Client Intake Form",
    subtitle="New client questionnaire",
    meta=["Date"],
    body=[
        *contact_block("Client"),
        fields([("Business / Organization", 2), ("Website", 1.4)]),
        section("Project / Service"),
        fields([("Service Requested", 2), ("Ideal Start Date", 1)],
               [("Budget Range (CAD)", 1), ("Deadline", 1), ("Decision Maker", 1)]),
        area("What do you need help with?", 64),
        area("What does success look like?", 48),
        options("Preferred contact:", ["Phone", "Text", "Email", "Video call"]),
        options("Referred by:", ["Friend / client", "Online search", "Social media"], other=True),
        consent(CASL),
        signatures(["Client Signature"]),
    ],
    name="Client Intake Form", short="Client Intake",
    about="A new client intake questionnaire for consultants, agencies, coaches and service providers - goals, budget, timeline and contact preferences on one page.",
    tags=["client intake form", "new client form", "intake questionnaire", "client onboarding",
          "consultation form", "coaching intake", "service intake"],
    canada="Canadian-ready: province/territory drop-down and postal code fields, plus an express email-consent checkbox to help with Canada's anti-spam rules.",
    price=3.45,
)

add(
    slug="client-onboarding-checklist", cat="ops",
    title="Client Onboarding Checklist",
    subtitle="From signed agreement to first delivery",
    meta=["Client", "Start Date", "Account Lead"],
    body=[
        groups({
            "Before Kickoff": ["Proposal / quote accepted", "Agreement signed", "Deposit or retainer received",
                               "Client added to CRM / contact list", "Invoice schedule set up",
                               "Welcome email sent"],
            "Information & Access": ["Intake form completed", "Brand files / documents received",
                                     "Logins and access shared securely", "Key contacts confirmed",
                                     "Billing contact confirmed", "Tax registration numbers on file"],
            "Kickoff": ["Kickoff meeting booked", "Goals and scope reviewed", "Timeline and milestones agreed",
                        "Communication channel agreed", "Meeting cadence set", "Next steps sent in writing"],
            "First 30 Days": ["First deliverable sent", "Feedback collected", "First invoice issued",
                              "Check-in call held", "Testimonial / review requested", "Onboarding closed"],
        }),
        area("Notes", 90),
    ],
    name="Client Onboarding Checklist", short="Onboarding Checklist",
    about="A 24-step client onboarding checklist for service businesses covering paperwork, access, kickoff and the first 30 days.",
    tags=["client onboarding", "onboarding checklist", "new client checklist", "agency checklist",
          "freelance checklist", "client welcome", "service checklist"],
    price=3.45,
)

add(
    slug="petty-cash-log", cat="finance",
    title="Petty Cash Log",
    subtitle="Amounts in Canadian dollars",
    meta=["Month / Period", "Fund Amount", "Custodian"],
    body=[
        fill_table([("Date", 1.2), ("Voucher / Receipt No.", 1.6), ("Paid To", 2.2), ("Purpose", 3),
                    ("Cash In", 1.2), ("Cash Out", 1.2), ("Balance", 1.3)]),
        fields([("Opening Balance", 1), ("Total In", 1), ("Total Out", 1), ("Closing Balance", 1), ("Over / Short", 1)]),
        signatures(["Custodian", "Reviewed By"]),
    ],
    name="Petty Cash Log", short="Petty Cash Log",
    about="A petty cash log to track every cash payment and top-up with voucher numbers, running balance and a reconciliation summary.",
    tags=["petty cash log", "cash log", "cash tracker", "petty cash form", "cash register log",
          "office cash", "cash reconciliation"],
    price=2.95,
)

add(
    slug="expense-report", cat="finance",
    title="Expense Report",
    subtitle="Employee expense reimbursement  ·  Amounts in Canadian dollars",
    meta=["Report No.", "Period From", "Period To"],
    body=[
        fields([("Employee Name", 2), ("Department", 1.2), ("Employee ID", 1)],
               [("Purpose / Project", 2), ("Manager", 1.2), ("Cost Centre", 1)]),
        fill_table([("Date", 1.1), ("Description", 2.8), ("Category", 1.4), ("Vendor", 1.6), ("Pre-Tax", 1.1),
                    ("GST/HST", 1.1), ("PST/QST", 1.1), ("Total", 1.2)]),
        totals(["Total Expenses", "Less: Cash Advance", "Reimbursement Due (CAD)"],
               notes="Receipts attached / Notes"),
        signatures(["Employee", "Approved By"]),
    ],
    name="Expense Report Form", short="Expense Report",
    about="An employee expense report with separate GST/HST and PST/QST columns so you can track recoverable tax, plus advance and reimbursement lines.",
    tags=["expense report", "expense form", "reimbursement form", "business expenses",
          "employee expenses", "travel expenses", "receipt tracker"],
    price=3.45,
)

add(
    slug="mileage-log", cat="finance",
    title="Vehicle Mileage Log",
    subtitle="Business kilometres logbook",
    meta=["Tax Year", "Month"],
    body=[
        fields([("Driver Name", 2), ("Vehicle (year, make, model)", 2), ("Licence Plate", 1)],
               [("Odometer at Start of Year (km)", 1), ("Odometer at End of Year (km)", 1)]),
        fill_table([("Date", 1.1), ("Starting Point", 2.2), ("Destination", 2.2), ("Business Purpose", 3),
                    ("Odometer Start", 1.3), ("Odometer End", 1.3), ("Km", 0.9)]),
        fields([("Business Km This Page", 1), ("Total Km This Page", 1), ("Business Use %", 1)]),
    ],
    name="Vehicle Mileage Log", short="Mileage Log",
    about="A kilometre logbook for self-employed people and employees who drive for work, recording date, destination, purpose and odometer readings for each trip.",
    tags=["mileage log", "kilometre log", "km log", "vehicle logbook", "mileage tracker",
          "business driving", "car expense log", "self employed"],
    canada="Canadian-ready: records kilometres and the trip details (date, destination, purpose, distance) plus start- and end-of-year odometer readings that a vehicle logbook needs at tax time.",
    price=2.95,
)

add(
    slug="vehicle-expense-log", cat="finance",
    title="Vehicle Expense Log",
    subtitle="Fuel, maintenance & operating costs  ·  Amounts in Canadian dollars",
    meta=["Tax Year", "Month"],
    body=[
        fields([("Vehicle (year, make, model)", 2), ("Licence Plate", 1), ("Driver", 1.4)]),
        fill_table([("Date", 1.1), ("Expense Type", 1.8), ("Vendor", 2), ("Odometer (km)", 1.3), ("Litres", 0.9),
                    ("Pre-Tax", 1.1), ("GST/HST", 1.1), ("Total", 1.2)]),
        para("Expense types: fuel, oil changes, maintenance and repairs, tires, insurance, licence and registration, "
             "parking, car washes, lease or loan interest.", "s"),
        fields([("Total Fuel", 1), ("Total Maintenance", 1), ("Total Other", 1), ("Grand Total", 1)]),
    ],
    name="Vehicle Expense Log", short="Vehicle Expense Log",
    about="A vehicle expense log for fuel (in litres), maintenance, insurance and parking with odometer and GST/HST columns.",
    tags=["vehicle expense log", "fuel log", "car expenses", "gas log", "auto expense",
          "fleet log", "vehicle tracker"],
    price=2.95,
)

DENOMS = ["$100 bills", "$50 bills", "$20 bills", "$10 bills", "$5 bills", "$2 coins", "$1 coins",
          "25 cent coins", "10 cent coins", "5 cent coins", "Rolled coin", "Cheques", "Card / debit slips"]
add(
    slug="cash-count-sheet", cat="finance",
    title="Daily Cash Count Sheet",
    subtitle="Cash drawer / till reconciliation  ·  Canadian currency",
    meta=["Date", "Register / Till", "Shift"],
    body=[
        table([("Denomination", 3), ("Quantity", 1.4), ("Amount (CAD)", 1.8)], rows=len(DENOMS), prefill=DENOMS, rh=19),
        totals(["Total Counted", "Less: Opening Float", "Net Cash Taken", "Expected (POS Report)", "Over / Short"],
               notes="Notes / Explanation of Variance"),
        signatures(["Counted By", "Verified By"]),
    ],
    name="Daily Cash Count Sheet", short="Cash Count Sheet",
    about="A till and cash drawer count sheet with Canadian bills and coins pre-listed (no pennies), float, expected total and over/short.",
    tags=["cash count sheet", "till count", "cash drawer", "register count", "end of day",
          "cash reconciliation", "retail form", "cash out sheet"],
    canada="Canadian-ready: lists Canadian bills and coins ($100 to 5 cents, no pennies) and amounts in Canadian dollars.",
    price=2.95,
)

add(
    slug="bank-deposit-log", cat="finance",
    title="Bank Deposit Log",
    subtitle="Amounts in Canadian dollars",
    meta=["Account", "Month / Year"],
    body=[
        fill_table([("Date", 1.1), ("Deposit Ref.", 1.4), ("Source / Description", 3.2), ("Cash", 1.2),
                    ("Cheques", 1.2), ("Total", 1.3), ("Deposited By", 1.6), ("Verified", 1)]),
        fields([("Total Cash", 1), ("Total Cheques", 1), ("Total Deposits", 1)]),
    ],
    name="Bank Deposit Log", short="Deposit Log",
    about="A bank deposit log to record every cash and cheque deposit with reference numbers, who made it and who verified it.",
    tags=["bank deposit log", "deposit tracker", "cash deposit", "bookkeeping log",
          "bank log", "deposit record", "cheque log"],
    price=2.95,
)

add(
    slug="accounts-receivable-log", cat="finance",
    title="Accounts Receivable Log",
    subtitle="Who owes you  ·  Amounts in Canadian dollars",
    meta=["Month / Period"],
    body=[
        fill_table([("Invoice Date", 1.2), ("Invoice No.", 1.2), ("Customer", 2.6), ("Amount", 1.2), ("Due Date", 1.2),
                    ("Date Paid", 1.2), ("Paid", 1.1), ("Balance", 1.2), ("Follow-up", 1.4)]),
        fields([("Total Invoiced", 1), ("Total Collected", 1), ("Total Outstanding", 1)]),
    ],
    name="Accounts Receivable Log", short="AR Tracker",
    about="An accounts receivable tracker that shows every invoice, due date, payments received, balance owing and follow-up notes.",
    tags=["accounts receivable", "ar log", "invoice tracker", "payment tracker",
          "unpaid invoices", "collections log", "bookkeeping log"],
    price=2.95,
)

add(
    slug="accounts-payable-log", cat="finance",
    title="Accounts Payable Log",
    subtitle="Bills to pay  ·  Amounts in Canadian dollars",
    meta=["Month / Period"],
    body=[
        fill_table([("Bill Date", 1.1), ("Vendor", 2.4), ("Invoice No.", 1.2), ("Amount", 1.2), ("GST/HST", 1.1),
                    ("Due Date", 1.1), ("Date Paid", 1.1), ("Cheque / Ref.", 1.3), ("Approved", 1)]),
        fields([("Total Bills", 1), ("Total Paid", 1), ("Total Unpaid", 1), ("GST/HST Paid (ITCs)", 1)]),
    ],
    name="Accounts Payable Log", short="AP Tracker",
    about="An accounts payable log to track vendor bills, due dates, payment references and GST/HST paid for input tax credits.",
    tags=["accounts payable", "ap log", "bill tracker", "bill payment log",
          "vendor payments", "bookkeeping log", "expense log"],
    price=2.95,
)

add(
    slug="invoice-register", cat="finance",
    title="Invoice Register",
    subtitle="Invoice log  ·  Amounts in Canadian dollars",
    meta=["Month / Period"],
    body=[
        fill_table([("Invoice No.", 1.1), ("Date", 1.1), ("Client", 2.6), ("Subtotal", 1.2), ("GST/HST", 1.1),
                    ("PST/QST", 1.1), ("Total", 1.2), ("Status", 1.1)]),
        fields([("Total Subtotal", 1), ("Total GST/HST", 1), ("Total PST/QST", 1), ("Total Invoiced", 1)]),
        para("Status: Sent · Paid · Partial · Overdue · Void", "s"),
    ],
    name="Invoice Register Log", short="Invoice Log",
    about="An invoice register that numbers and tracks every invoice you issue, with GST/HST and PST/QST collected columns for easy tax filing.",
    tags=["invoice log", "invoice register", "invoice tracker", "sales log",
          "billing log", "gst hst log", "bookkeeping log"],
    price=2.95,
)

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
          "October", "November", "December", "Annual Total"]
add(
    slug="gst-hst-tracker", cat="finance",
    title="GST/HST Tracker",
    subtitle="Sales tax collected vs. input tax credits  ·  Amounts in Canadian dollars",
    meta=["Fiscal Year", "Business No. (BN)"],
    body=[
        options("Filing frequency:", ["Monthly", "Quarterly", "Annual"]),
        table([("Month", 1.6), ("Taxable Sales", 1.4), ("GST/HST Collected", 1.6), ("Eligible Purchases", 1.5),
               ("GST/HST Paid (ITCs)", 1.6), ("Net Tax", 1.3), ("Date Filed", 1.2), ("Date Paid", 1.2)],
              rows=13, prefill=MONTHS, rh=21),
        section("Quebec / Provincial Sales Tax (if applicable)"),
        fields([("QST / PST Collected (year)", 1), ("QST / PST Paid", 1), ("Net QST / PST Owing", 1), ("Filed On", 1)]),
        area("Notes / Instalments", 56),
    ],
    name="GST HST Tracker", short="GST/HST Tracker",
    about="A 12-month GST/HST tracker that compares tax collected on sales with input tax credits on purchases, plus a section for QST or PST.",
    tags=["gst tracker", "hst tracker", "sales tax tracker", "gst hst", "input tax credit",
          "tax tracker", "canadian tax", "bookkeeping form"],
    canada="Built for Canadian sales tax: GST/HST collected, input tax credits (ITCs), net tax and filing dates by month, plus QST/PST lines.",
    price=3.45,
)

add(
    slug="income-expense-tracker", cat="finance",
    title="Income & Expense Tracker",
    subtitle="Monthly ledger  ·  Amounts in Canadian dollars",
    meta=["Month", "Year"],
    body=[
        fill_table([("Date", 1.1), ("Description", 3.2), ("Category", 1.6), ("Payment Method", 1.4),
                    ("Income", 1.2), ("Expense", 1.2), ("GST/HST", 1.1)]),
        table([("Total Income", 1), ("Total Expenses", 1), ("Net Profit / Loss", 1), ("GST/HST Collected", 1),
               ("GST/HST Paid", 1)], rows=1, rh=22),
    ],
    name="Income and Expense Tracker", short="Income Expense Log",
    about="A monthly income and expense ledger for small businesses and side hustles with category, payment method and GST/HST columns.",
    tags=["income tracker", "expense tracker", "business ledger", "profit tracker",
          "small business log", "side hustle", "bookkeeping log"],
    price=2.95,
)

INC = ["Product sales", "Service income", "Other income", "Total Income"]
EXP = ["Rent / lease", "Utilities", "Wages", "CPP / EI / tax remittances", "Inventory / supplies", "Insurance",
       "Marketing", "Phone & internet", "Software & subscriptions", "Vehicle & travel", "Professional fees",
       "Bank & card fees", "Loan payments", "GST/HST / PST remittance", "Other", "Total Expenses"]
add(
    slug="monthly-business-budget", cat="finance",
    title="Monthly Business Budget",
    subtitle="Budget vs. actual  ·  Amounts in Canadian dollars",
    meta=["Month", "Year"],
    body=[
        table([("Income", 3), ("Budget", 1.4), ("Actual", 1.4), ("Difference", 1.4)], rows=len(INC), prefill=INC),
        table([("Expenses", 3), ("Budget", 1.4), ("Actual", 1.4), ("Difference", 1.4)], rows=len(EXP), prefill=EXP),
        fields([("Net Income (Budget)", 1), ("Net Income (Actual)", 1), ("Difference", 1)]),
        area("Notes", 40),
    ],
    name="Monthly Business Budget", short="Business Budget",
    about="A monthly small business budget comparing planned and actual income and expenses, with Canadian payroll remittance and sales tax lines.",
    tags=["business budget", "monthly budget", "budget planner", "budget vs actual",
          "small business plan", "finance planner", "expense planner"],
    price=3.45,
)

add(
    slug="donation-receipt", cat="finance",
    title="Donation Receipt",
    subtitle="Receipt for a gift to a charity or non-profit",
    meta=["Receipt No.", "Date Issued", "Location Issued"],
    body=[
        pair("Organization", [
            [("Organization Name", 1)], [("Address", 1)],
            [("City", 2), ("Province", 1, "prov"), ("Postal Code", 1.2)],
            [("Charitable Registration No.", 1)],
        ], "Donor", [
            [("Donor Name", 1)], [("Address", 1)],
            [("City", 2), ("Province", 1, "prov"), ("Postal Code", 1.2)],
            [("Email", 1)],
        ]),
        section("Gift"),
        fields([("Date Gift Received", 1), ("Amount of Gift (CAD)", 1), ("Value of Advantage", 1), ("Eligible Amount", 1)]),
        options("Type of gift:", ["Cash", "Cheque", "Electronic transfer", "Gift in kind"]),
        area("Gift in kind: description, appraiser name and address (if appraised)", 50),
        para("Canada Revenue Agency: canada.ca/charities-giving", "s"),
        signatures(["Authorized Signature", "Name & Title"]),
        para("Official donation receipts for income tax purposes may only be issued by registered charities and other qualified "
             "donees. Confirm current receipting requirements before issuing.", "s"),
    ],
    name="Donation Receipt Template", short="Donation Receipt",
    about="A donation receipt for charities and non-profits with registration number, eligible amount, advantage and gift-in-kind fields.",
    tags=["donation receipt", "charity receipt", "nonprofit form", "tax receipt",
          "gift receipt", "fundraising form", "charitable gift"],
    canada="Canadian-ready: fields for the charitable registration number, eligible amount and advantage, plus the Canada Revenue Agency website line that official receipts include.",
    price=3.45,
)

add(
    slug="gift-certificate", cat="billing",
    title="Gift Certificate",
    subtitle="Three per page",
    body=[
        cards(3, "Gift Certificate", [
            [("To", 1.4), ("From", 1.4), ("Value / Service", 1.6)],
            [("Business Name", 2), ("Phone / Website", 1.6)],
            [("Date Issued", 1), ("Authorized By", 1.4), ("Message", 2)],
        ], note="Redeemable for products or services of equal value. Not redeemable for cash. No expiry date."),
    ],
    name="Gift Certificate Template", short="Gift Certificate",
    about="Three fillable gift certificates per page for salons, studios, shops and restaurants - type the details, print and cut.",
    tags=["gift certificate", "gift card template", "gift voucher", "salon gift card",
          "business gift card", "voucher template", "printable voucher"],
    canada="Canadian-ready: no expiry-date line, since most provinces restrict expiry dates on gift certificates.",
    price=2.95,
)
