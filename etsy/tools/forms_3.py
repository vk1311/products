"""Batch 3 - operations, jobs and inventory."""

from common import *  # noqa: F401,F403

FORMS = []


def add(**kw):
    kw.setdefault("cat", "ops")
    FORMS.append(kw)


add(
    slug="work-order",
    title="Work Order",
    subtitle="Job authorization & completion record",
    meta=["Work Order No.", "Date", "Scheduled For"],
    body=[
        pair("Customer", client_rows(), "Job Details", [
            [("Job Site Address", 1)], [("Requested By", 1), ("Phone", 1)],
            [("Assigned To", 1), ("Priority", 0.8)], [("Est. Start", 1), ("Est. Finish", 1)],
        ]),
        area("Description of Work", 50),
        table([("Labour / Task", 5), ("Technician", 2), ("Hours", 1), ("Rate", 1.2), ("Amount", 1.4)], rows=4),
        table([("Parts / Materials", 5), ("Qty", 1), ("Unit Cost", 1.4), ("Amount", 1.5)], rows=4),
        totals(["Labour", "Parts / Materials", "GST / HST  ____ %", "PST / QST  ____ %", "Total (CAD)"],
               notes="Work Completed / Notes"),
        options("Status:", ["Completed", "Partially completed", "Return visit needed"]),
        signatures(["Customer Sign-off", "Technician"]),
    ],
    name="Work Order Form", short="Work Order",
    about="A one-page work order for trades, repair and field service jobs: customer, job details, labour, parts, Canadian tax lines and customer sign-off.",
    tags=["work order", "job order form", "service order", "repair order", "field service",
          "trades form", "handyman form"],
    price=3.95,
)

add(
    slug="service-call-report",
    title="Service Call Report",
    subtitle="Field service visit summary",
    meta=["Report No.", "Date", "Technician"],
    body=[
        *contact_block("Customer"),
        fields([("Equipment / System", 2), ("Make / Model", 1.4), ("Serial No.", 1.2)],
               [("Time Arrived", 1), ("Time Departed", 1), ("Total Hours", 1), ("Km Travelled", 1)]),
        options("Call type:", ["Repair", "Maintenance", "Installation", "Inspection", "Warranty"], other=True),
        area("Problem Reported", 40),
        area("Diagnosis / Findings", 40),
        area("Work Performed", 40),
        table([("Parts Used", 5), ("Qty", 1), ("Price", 1.4)], rows=4),
        yesno(["Problem resolved?", "Follow-up visit required?", "Quote for further work needed?"]),
        signatures(["Customer Signature", "Technician Signature"]),
    ],
    name="Service Call Report", short="Service Report",
    about="A field service report for HVAC, appliance, IT and repair techs that records the problem, diagnosis, work performed, parts and customer sign-off.",
    tags=["service report", "service call form", "technician report", "hvac form",
          "repair report", "field service", "maintenance report"],
    price=3.95,
)

add(
    slug="job-sheet",
    title="Job Sheet",
    subtitle="Daily job card",
    meta=["Job No.", "Date"],
    body=[
        fields([("Customer", 2), ("Phone", 1)], [("Job Address", 2), ("Province", 0.6, "prov"), ("Postal Code", 0.8)]),
        fields([("Start Time", 1), ("Finish Time", 1), ("Break", 1), ("Total Hours", 1)]),
        area("Tasks Completed", 70),
        table([("Crew Member", 3), ("Start", 1), ("Finish", 1), ("Hours", 1)], rows=5),
        table([("Materials Used", 5), ("Qty", 1), ("Supplier", 2)], rows=5),
        area("Issues / Notes for Next Visit", 50),
        signatures(["Crew Lead", "Customer"]),
    ],
    name="Job Sheet Template", short="Job Sheet",
    about="A daily job sheet for crews and tradespeople to log tasks, crew hours, materials and notes for the next visit.",
    tags=["job sheet", "job card", "daily job log", "crew log", "trades form",
          "contractor form", "time and materials"],
    price=3.45,
)

add(
    slug="daily-construction-report",
    title="Daily Construction Report",
    subtitle="Site diary",
    meta=["Report No.", "Date", "Day"],
    body=[
        fields([("Project", 2), ("Project No.", 1), ("Superintendent", 1.4)],
               [("Site Address", 2), ("Province", 0.6, "prov")]),
        options("Weather:", ["Sunny", "Cloudy", "Rain", "Snow", "Wind"], other=False),
        fields([("Temp. AM (°C)", 1), ("Temp. PM (°C)", 1), ("Ground Conditions", 2)]),
        table([("Trade / Company", 3), ("Workers", 1), ("Hours", 1), ("Work Performed", 5)], rows=6),
        table([("Equipment on Site", 3), ("Hours Used", 1), ("Idle", 1), ("Notes", 4)], rows=3),
        area("Deliveries / Materials Received", 30),
        area("Delays, Issues & Visitors", 30),
        yesno(["Safety meeting held today?", "Any incidents or near misses?", "Inspections completed today?"]),
        signatures(["Prepared By"]),
    ],
    name="Daily Construction Report", short="Daily Site Report",
    about="A daily construction report (site diary) with weather in °C, trades on site, equipment, deliveries, delays and safety questions.",
    tags=["daily report", "construction report", "site diary", "daily log", "job site log",
          "construction form", "superintendent"],
    canada="Canadian-ready: temperatures in degrees Celsius, province/territory drop-down and a snow option for the weather.",
    price=3.95,
)

add(
    slug="punch-list",
    title="Punch List",
    subtitle="Deficiency list / project close-out",
    meta=["Project", "Date", "Page"],
    body=[
        fields([("Site Address", 2), ("Contractor", 1.4), ("Inspected By", 1.4)]),
        fill_table([("No.", 0.6), ("Location / Room", 2), ("Deficiency Description", 5), ("Assigned To", 1.6),
                    ("Due", 1), ("Done", 0.8)], numbered=True),
        signatures(["Owner / Client", "Contractor"]),
    ],
    name="Construction Punch List", short="Punch List",
    about="A numbered punch list (deficiency list) to track final fixes by location, who is responsible and the completion date.",
    tags=["punch list", "deficiency list", "construction form", "renovation checklist",
          "final walkthrough", "contractor form", "project closeout"],
    price=2.95,
)

INSPECT = ["Site access & signage", "Fencing / barricades", "Housekeeping & debris", "Excavations protected",
           "Scaffolds tagged", "Ladders secured", "Fall protection in use", "Guardrails / openings covered",
           "Electrical cords & panels", "Fire extinguishers available", "First aid kit stocked",
           "PPE worn by all workers", "Equipment inspected", "Materials stored safely",
           "Hazardous products labelled", "Washroom facilities"]
add(
    slug="site-inspection-checklist",
    title="Site Inspection Checklist",
    subtitle="Construction / job site walk-through",
    meta=["Date", "Time", "Inspector"],
    body=[
        fields([("Project / Site", 2), ("Address", 2), ("Province", 0.7, "prov")]),
        matrix(INSPECT, ["OK", "Fix", "N/A"]),
        area("Corrective Actions Required", 60),
        signatures(["Inspector", "Site Supervisor"]),
    ],
    name="Site Inspection Checklist", short="Site Inspection",
    about="A 16-point job site inspection checklist covering access, fall protection, electrical, fire, first aid, PPE and housekeeping with corrective actions.",
    tags=["site inspection", "safety inspection", "construction form", "job site form",
          "inspection checklist", "site walk", "safety checklist"],
    price=3.45,
)

add(
    slug="quality-control-checklist",
    title="Quality Control Checklist",
    subtitle="Product / job quality inspection",
    meta=["Inspection No.", "Date", "Inspector"],
    body=[
        fields([("Product / Job", 2), ("Batch / Order No.", 1), ("Customer", 1.4)],
               [("Quantity Inspected", 1), ("Sample Size", 1), ("Specification / Standard", 2)]),
        fill_table([("No.", 0.5), ("Check Point / Requirement", 4.4), ("Pass", 0.8), ("Fail", 0.8),
                    ("Measurement / Notes", 3)], numbered=True, rh=19),
        options("Result:", ["Accepted", "Accepted with deviation", "Rejected", "Rework"]),
        area("Corrective Action", 40),
        signatures(["Inspector", "Approved By"]),
    ],
    name="Quality Control Checklist", short="QC Checklist",
    about="A quality control inspection form for products or completed work with numbered check points, pass/fail, measurements and corrective action.",
    tags=["quality control", "qc checklist", "inspection form", "quality check",
          "product inspection", "manufacturing form", "qa checklist"],
    price=3.45,
)

add(
    slug="maintenance-request",
    title="Maintenance Request",
    subtitle="Facility / building repair request",
    meta=["Request No.", "Date"],
    body=[
        fields([("Requested By", 2), ("Department / Unit", 1.4), ("Phone / Ext.", 1)],
               [("Location / Room", 2), ("Email", 1.4)]),
        options("Category:", ["Electrical", "Plumbing", "HVAC", "Carpentry", "Cleaning", "Grounds"], other=True),
        options("Priority:", ["Emergency", "Urgent (24 h)", "Routine", "Planned"]),
        area("Describe the Problem", 70),
        options("Permission to enter if absent:", ["Yes", "No"]),
        section("Maintenance Use"),
        fields([("Assigned To", 1.4), ("Date Received", 1), ("Date Completed", 1), ("Hours", 0.7)]),
        area("Work Performed / Materials", 60),
        signatures(["Completed By", "Requester Sign-off"]),
    ],
    name="Maintenance Request Form", short="Maintenance Request",
    about="A building and facility maintenance request with category, priority, permission to enter and a maintenance-use section for completion.",
    tags=["maintenance request", "repair request", "work request", "facility form",
          "building maintenance", "property maintenance", "service request"],
    price=3.45,
)

add(
    slug="equipment-maintenance-log",
    title="Equipment Maintenance Log",
    subtitle="Service history",
    meta=["Equipment ID"],
    body=[
        fields([("Equipment", 2), ("Make / Model", 1.4), ("Serial No.", 1.2)],
               [("Location", 1.4), ("Purchase Date", 1), ("Service Interval", 1), ("Warranty Expires", 1)]),
        fill_table([("Date", 1.1), ("Hours / Km", 1.1), ("Service Type", 1.6), ("Work Performed / Parts", 4.2),
                    ("Cost", 1), ("Done By", 1.4), ("Next Due", 1.1)]),
    ],
    name="Equipment Maintenance Log", short="Maintenance Log",
    about="An equipment maintenance log that keeps the full service history, parts, costs and next due date for each machine or tool.",
    tags=["maintenance log", "equipment log", "service log", "machine log", "repair log",
          "fleet maintenance", "preventive maint"],
    price=2.95,
)

VEH = ["Headlights / high beams", "Brake & signal lights", "Mirrors & windshield", "Wipers & washer fluid",
       "Tires & wheel nuts", "Brakes (service & parking)", "Horn", "Steering", "Seat belts",
       "Fluid levels / leaks", "Exhaust", "Coupling / hitch", "Cargo secured", "Emergency kit & extinguisher",
       "Heater / defroster", "Registration & insurance"]
add(
    slug="vehicle-inspection-checklist",
    title="Vehicle Pre-Trip Inspection",
    subtitle="Daily vehicle inspection report",
    meta=["Date", "Time", "Odometer (km)"],
    body=[
        fields([("Driver", 2), ("Unit / Vehicle No.", 1), ("Licence Plate", 1), ("Trailer No.", 1)],
               [("Location of Inspection", 2), ("Province", 0.7, "prov")]),
        matrix(VEH, ["OK", "Defect"]),
        options("Defects found:", ["None", "Minor", "Major - do not operate"]),
        area("Describe Defects", 40),
        signatures(["Driver", "Repairs Completed By"]),
    ],
    name="Vehicle Inspection Checklist", short="Pre-Trip Inspection",
    about="A daily pre-trip vehicle inspection checklist for company cars, vans and light trucks with defect reporting and repair sign-off.",
    tags=["vehicle inspection", "pre trip inspection", "fleet checklist", "driver checklist",
          "truck inspection", "daily inspection", "van checklist"],
    canada="Canadian-ready: odometer in kilometres, province/territory drop-down and winter items like the heater and defroster. Commercial vehicles may need a specific provincial schedule.",
    price=3.45,
)

add(
    slug="delivery-receipt",
    title="Delivery Receipt",
    subtitle="Proof of delivery",
    meta=["Delivery No.", "Date", "Order / Invoice No."],
    body=[
        pair("Shipper", biz_rows(()), "Deliver To", client_rows()),
        fields([("Carrier / Driver", 2), ("Vehicle", 1), ("Time Delivered", 1), ("No. of Pieces", 1)]),
        table([("Item / SKU", 1.6), ("Description", 5), ("Qty Ordered", 1.2), ("Qty Delivered", 1.2), ("Condition", 1.4)], rows="fill"),
        options("Received:", ["In good condition", "With damage (noted below)", "Short / missing items"]),
        area("Exceptions / Damage Notes", 36),
        signatures(["Received By (print & sign)", "Driver"]),
    ],
    name="Delivery Receipt Form", short="Delivery Receipt",
    about="A proof-of-delivery receipt listing items ordered vs. delivered, condition on arrival, exceptions and signatures from the driver and receiver.",
    tags=["delivery receipt", "proof of delivery", "pod form", "delivery note",
          "courier form", "shipping receipt", "delivery form"],
    price=3.45,
)

add(
    slug="packing-slip",
    title="Packing Slip",
    meta=["Order No.", "Order Date", "Ship Date"],
    body=[
        pair("From", biz_rows(()), "Ship To", client_rows()),
        fields([("Shipping Method", 1), ("Tracking No.", 2), ("Boxes", 0.6), ("Weight (kg)", 0.8)]),
        table([("Item / SKU", 1.6), ("Description", 5), ("Qty Ordered", 1.2), ("Qty Shipped", 1.2), ("Back-ordered", 1.3)], rows="fill"),
        area("Message / Gift Note", 40),
        para("Thank you for your order! Please check your items on arrival and contact us within 7 days with any questions.", "s"),
    ],
    name="Packing Slip Template", short="Packing Slip",
    about="A packing slip for online shops and wholesalers showing what was ordered, shipped and back-ordered, plus a gift note area.",
    tags=["packing slip", "shipping slip", "order insert", "packing list",
          "small shop form", "online shop", "order packing"],
    canada="Canadian-ready: province/territory drop-down, postal codes and weights in kilograms.",
    price=2.95,
)

add(
    slug="shipping-log",
    title="Shipping Log",
    subtitle="Outgoing shipments",
    meta=["Month / Year"],
    body=[
        fill_table([("Date", 1.1), ("Order No.", 1.2), ("Customer", 2.2), ("Destination", 2), ("Carrier", 1.3),
                    ("Tracking No.", 2.2), ("Cost", 0.9), ("Delivered", 1)]),
    ],
    name="Shipping Log", short="Shipping Log",
    about="A shipping log to record every outgoing parcel with order number, destination, carrier, tracking number, cost and delivery date.",
    tags=["shipping log", "shipment tracker", "parcel log", "mailing log", "order tracker",
          "online shop", "tracking log"],
    price=2.95,
)

add(
    slug="inventory-sheet",
    title="Inventory Sheet",
    subtitle="Stock on hand",
    meta=["Date", "Location", "Counted By"],
    body=[
        fill_table([("Item No. / SKU", 1.5), ("Description", 3.6), ("Unit", 0.9), ("Qty on Hand", 1.1),
                    ("Unit Cost", 1.1), ("Total Value", 1.3), ("Reorder Level", 1.2)]),
        fields([("Total Items", 1), ("Total Inventory Value (CAD)", 1.4), ("Verified By", 1.4)]),
    ],
    name="Inventory Sheet", short="Inventory Sheet",
    about="An inventory sheet for recording stock on hand, unit cost, total value and reorder levels for any shop, warehouse or studio.",
    tags=["inventory sheet", "stock sheet", "inventory list", "stock take", "product inventory",
          "warehouse form", "retail inventory", "inventory tracker"],
    price=2.95,
)

add(
    slug="inventory-count-sheet",
    title="Inventory Count Sheet",
    subtitle="Physical count / cycle count",
    meta=["Count Date", "Area / Aisle", "Sheet No."],
    body=[
        fields([("Counter", 1.4), ("Checker", 1.4), ("Start Time", 1), ("End Time", 1)]),
        fill_table([("Location / Bin", 1.4), ("Item No. / SKU", 1.5), ("Description", 3.4), ("Unit", 0.8),
                    ("System Qty", 1.1), ("Count 1", 1), ("Count 2", 1), ("Variance", 1)]),
        signatures(["Counter", "Supervisor"]),
    ],
    name="Inventory Count Sheet", short="Count Sheet",
    about="A physical inventory and cycle count sheet with bin locations, system quantity, two count columns and variance.",
    tags=["inventory count", "stock count", "cycle count", "year end count", "stocktake form",
          "warehouse form", "count sheet"],
    price=2.95,
)

add(
    slug="stock-reorder-form",
    title="Stock Reorder Form",
    subtitle="Low stock & reorder planner",
    meta=["Date", "Prepared By"],
    body=[
        fill_table([("Item No. / SKU", 1.5), ("Description", 3.4), ("Supplier", 2), ("On Hand", 1), ("Reorder Point", 1.2),
                    ("Order Qty", 1), ("Unit Cost", 1), ("Ordered", 0.9)]),
        fields([("Total Estimated Cost (CAD)", 1.4), ("Approved By", 1.4), ("PO No.", 1)]),
    ],
    name="Stock Reorder Form", short="Reorder Form",
    about="A reorder form that lists low-stock items, reorder points, suppliers and order quantities so restocking is quick and nothing runs out.",
    tags=["reorder form", "stock reorder", "restock list", "inventory reorder", "low stock",
          "purchasing form", "supply list"],
    price=2.95,
)

add(
    slug="supply-request",
    title="Supply Request Form",
    subtitle="Internal supply order",
    meta=["Request No.", "Date", "Needed By"],
    body=[
        fields([("Requested By", 2), ("Department / Location", 1.6), ("Phone / Ext.", 1)]),
        table([("Item", 3), ("Description / Size", 3.6), ("Qty", 0.8), ("Est. Cost", 1.2), ("Supplier", 1.8)], rows="fill"),
        area("Reason / Notes", 40),
        options("Decision:", ["Approved", "Partially approved", "Denied", "On order"]),
        signatures(["Requested By", "Approved By"]),
    ],
    name="Supply Request Form", short="Supply Request",
    about="An internal supply request form for office, cleaning, kitchen or shop supplies with approval section.",
    tags=["supply request", "office supplies", "supply order", "request form",
          "internal order", "purchase request", "office form"],
    price=2.95,
)

add(
    slug="material-requisition",
    title="Material Requisition",
    subtitle="Request for job materials",
    meta=["Requisition No.", "Date", "Required By"],
    body=[
        fields([("Project / Job", 2), ("Job No.", 1), ("Cost Code", 1)],
               [("Requested By", 1.6), ("Deliver To", 2.4)]),
        table([("No.", 0.5), ("Material / Item", 4), ("Spec / Size", 2), ("Unit", 0.8), ("Qty", 0.8), ("Issued", 0.9)],
              rows="fill", numbered=True),
        signatures(["Requested By", "Approved By", "Issued By", "Received By"]),
    ],
    name="Material Requisition Form", short="Material Requisition",
    about="A material requisition for construction, maintenance and manufacturing jobs that tracks requested and issued materials by job and cost code.",
    tags=["material requisition", "requisition form", "material request", "job materials",
          "construction form", "warehouse form", "stores request"],
    price=2.95,
)

add(
    slug="equipment-sign-out-log",
    title="Equipment Sign-Out Log",
    subtitle="Tools & equipment check-out",
    meta=["Location", "Month / Year"],
    body=[
        fill_table([("Date Out", 1.1), ("Equipment / Tool", 2.8), ("ID / Serial", 1.4), ("Borrowed By", 2), ("Signature", 1.6),
                    ("Due Back", 1.1), ("Date In", 1.1), ("Condition", 1.2)]),
    ],
    name="Equipment Sign Out Sheet", short="Sign-Out Log",
    about="An equipment and tool sign-out sheet that records who borrowed what, when it is due back, when it was returned and its condition.",
    tags=["sign out sheet", "equipment log", "tool sign out", "check out log", "tool tracker",
          "equipment checkout", "loan log"],
    price=2.95,
)

add(
    slug="asset-register",
    title="Asset Register",
    subtitle="Fixed assets & equipment list",
    meta=["Business", "As of Date"],
    body=[
        fill_table([("Asset ID", 1), ("Description", 3), ("Serial No.", 1.5), ("Location / User", 1.7), ("Purchase Date", 1.2),
                    ("Cost (CAD)", 1.1), ("CCA Class", 0.9), ("Disposed", 1)]),
    ],
    name="Fixed Asset Register", short="Asset Register",
    about="A fixed asset register listing equipment, computers, tools and vehicles with serial numbers, location, cost, capital cost allowance class and disposal date.",
    tags=["asset register", "asset list", "fixed assets", "equipment list", "asset tracker",
          "it inventory", "cca class"],
    canada="Canadian-ready: includes a column for the capital cost allowance (CCA) class used for Canadian depreciation, and amounts in Canadian dollars.",
    cat="finance",
    price=2.95,
)

add(
    slug="key-control-log",
    title="Key Control Log",
    subtitle="Key issue & return record",
    meta=["Property / Building", "Page"],
    body=[
        fill_table([("Key No.", 0.9), ("Door / Area", 2.2), ("Issued To", 2), ("Date Issued", 1.1), ("Issued By", 1.4),
                    ("Signature", 1.6), ("Date Returned", 1.2), ("Received By", 1.4)]),
    ],
    name="Key Control Log", short="Key Log",
    about="A key control log for offices, rentals and facilities to track every key issued, to whom, and when it came back.",
    tags=["key log", "key control", "key sign out", "key register", "property manager",
          "building security", "office security"],
    price=2.95,
)

add(
    slug="visitor-sign-in-log",
    title="Visitor Sign-In Log",
    meta=["Location", "Date"],
    body=[
        fill_table([("Date", 1), ("Name", 2.4), ("Company", 2), ("Visiting", 1.8), ("Purpose", 1.8), ("Time In", 0.9),
                    ("Time Out", 0.9), ("Badge No.", 0.9)], rh=20),
        para("By signing in you agree to follow site safety rules and the directions of staff. "
             "Personal information is collected only for building security and emergency purposes.", "s"),
    ],
    name="Visitor Sign In Sheet", short="Visitor Log",
    about="A visitor sign-in sheet for offices, job sites, clinics and schools with company, person visited, purpose, time in/out and badge number.",
    tags=["visitor log", "sign in sheet", "visitor sign in", "guest log", "reception form",
          "front desk", "office sign in"],
    canada="Canadian-ready: includes a short personal-information purpose statement in the spirit of Canadian privacy law.",
    price=2.95,
)

add(
    slug="meeting-minutes",
    title="Meeting Minutes",
    meta=["Date", "Time", "Location"],
    body=[
        fields([("Meeting Title", 2), ("Facilitator", 1.4), ("Note Taker", 1.4)]),
        area("Attendees", 34),
        table([("Agenda Item", 3), ("Discussion / Decision", 6)], rows=8, rh=26),
        table([("Action Item", 5), ("Owner", 1.8), ("Due Date", 1.3)], rows="fill"),
        fields([("Next Meeting", 1), ("Minutes Approved By", 1.4)]),
    ],
    name="Meeting Minutes Template", short="Meeting Minutes",
    about="A meeting minutes template with attendees, agenda items, decisions and an action-item table with owners and due dates.",
    tags=["meeting minutes", "meeting notes", "minutes template", "board meeting",
          "team meeting", "agenda notes", "action items"],
    price=2.95,
)

add(
    slug="phone-message-log",
    title="Phone Message Log",
    subtitle="While you were out",
    meta=["Week Of"],
    body=[
        fill_table([("Date", 0.9), ("Time", 0.8), ("For", 1.4), ("Caller", 1.8), ("Company", 1.6), ("Phone", 1.5),
                    ("Message", 3.4), ("Done", 0.6)], rh=22),
    ],
    name="Phone Message Log", short="Message Log",
    about="A phone message log for reception desks and small offices to record who called, for whom, their number and the message.",
    tags=["phone message log", "call log", "message pad", "reception log", "front desk form",
          "office log", "phone log"],
    price=2.95,
)

add(
    slug="project-status-report",
    title="Project Status Report",
    meta=["Report Date", "Period", "Prepared By"],
    body=[
        fields([("Project Name", 2), ("Project Manager", 1.4), ("Client / Sponsor", 1.4)]),
        options("Overall status:", ["On track", "At risk", "Off track", "On hold", "Complete"]),
        fields([("Budget (CAD)", 1), ("Spent to Date", 1), ("% Complete", 0.8), ("Target Finish", 1)]),
        area("Summary", 44),
        table([("Milestone", 4), ("Due", 1.2), ("Status", 1.4), ("Notes", 3)], rows=6),
        table([("Risk / Issue", 4), ("Impact", 1.2), ("Owner", 1.4), ("Mitigation", 3)], rows=4),
        area("Next Steps", 40),
    ],
    name="Project Status Report", short="Status Report",
    about="A one-page project status report with overall status, budget, milestones, risks and next steps for clients or your team.",
    tags=["project status", "status report", "project report", "project tracker",
          "weekly report", "project manager", "progress report"],
    price=3.45,
)
