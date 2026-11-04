"""Batch 6 - cleaning, rentals, property and seasonal services."""

from common import *  # noqa: F401,F403

FORMS = []


def add(**kw):
    kw.setdefault("cat", "cleaning")
    FORMS.append(kw)


add(
    slug="house-cleaning-checklist",
    title="House Cleaning Checklist",
    subtitle="Standard residential clean",
    meta=["Client", "Date", "Cleaner"],
    body=[
        groups({
            "Kitchen": ["Wipe counters and backsplash", "Clean sink and faucet", "Wipe appliance fronts",
                        "Clean stovetop", "Microwave inside and out", "Wipe cabinet fronts", "Empty garbage and recycling",
                        "Sweep and mop floor"],
            "Bathrooms": ["Clean toilet inside and out", "Scrub tub / shower", "Clean sink and counter", "Polish mirrors",
                          "Wipe fixtures", "Replace towels", "Empty garbage", "Mop floor"],
            "Living Areas": ["Dust surfaces and shelves", "Dust electronics", "Wipe light switches and handles",
                             "Fluff cushions, fold throws", "Vacuum carpets and rugs", "Vacuum / mop floors",
                             "Empty garbage"],
            "Bedrooms": ["Make beds / change linens", "Dust furniture", "Wipe mirrors", "Tidy surfaces", "Vacuum floors",
                         "Empty garbage"],
            "Entry & Extras": ["Shake out entry mats", "Wipe front door", "Clean boot tray", "Inside fridge (add-on)",
                               "Inside oven (add-on)", "Interior windows (add-on)", "Laundry (add-on)"],
        }),
        area("Notes for Client / Next Visit", 40),
        fields([("Time In", 1), ("Time Out", 1), ("Total Hours", 1), ("Client Initials", 1)]),
    ],
    name="House Cleaning Checklist", short="Cleaning Checklist",
    about="A 36-task house cleaning checklist by room for home cleaners and cleaning businesses, with add-on services and time tracking.",
    tags=["house cleaning", "cleaning checklist", "home cleaning", "maid checklist",
          "cleaning schedule", "room checklist", "cleaner form"],
    price=2.95,
)

add(
    slug="deep-cleaning-checklist",
    title="Deep Cleaning Checklist",
    subtitle="Top-to-bottom detailed clean",
    meta=["Client", "Date", "Team"],
    body=[
        groups({
            "Whole Home": ["Ceiling corners and cobwebs", "Light fixtures and fans", "Vents and returns", "Baseboards",
                           "Door frames and doors", "Switch plates and outlets", "Window sills and tracks",
                           "Blinds", "Behind and under furniture"],
            "Kitchen": ["Inside oven", "Inside fridge and freezer", "Inside microwave", "Range hood and filter",
                        "Inside cabinets and drawers", "Small appliances", "Degrease backsplash", "Dishwasher filter",
                        "Garbage can washed"],
            "Bathrooms": ["Descale shower and glass", "Grout scrubbed", "Exhaust fan cover", "Inside vanity",
                          "Behind toilet", "Shower curtain / liner", "Drains cleared"],
            "Bedrooms & Living": ["Under beds", "Mattress vacuumed", "Closet floors and shelves", "Upholstery vacuumed",
                                  "Lamps and shades", "Picture frames", "Interior windows"],
        }),
        area("Products Used / Notes", 40),
        fields([("Time In", 1), ("Time Out", 1), ("Total Hours", 1), ("Client Sign-off", 1.4)]),
    ],
    name="Deep Cleaning Checklist", short="Deep Clean Checklist",
    about="A 32-task deep cleaning checklist for detailed cleans - baseboards, vents, inside appliances, grout and under furniture.",
    tags=["deep cleaning", "deep clean list", "spring cleaning", "cleaning checklist",
          "detailed cleaning", "cleaning business", "house cleaning"],
    price=2.95,
)

add(
    slug="move-out-cleaning-checklist",
    title="Move-Out Cleaning Checklist",
    subtitle="Move-in / move-out clean for tenants, landlords & cleaners",
    meta=["Address", "Date"],
    body=[
        groups({
            "Kitchen": ["Inside and outside fridge (unplugged / defrosted)", "Inside oven and drawer", "Stovetop and hood",
                        "Inside all cabinets and drawers", "Counters and backsplash", "Sink and faucet",
                        "Dishwasher inside", "Floor, including under appliances"],
            "Bathrooms": ["Toilet, base and behind", "Tub, shower and grout", "Vanity inside and out", "Mirror and medicine cabinet",
                          "Exhaust fan cover", "Floor and baseboards"],
            "All Rooms": ["Walls spot-cleaned", "Nail holes noted", "Baseboards", "Doors and handles", "Switch plates",
                          "Light fixtures (bulbs working)", "Window sills, tracks and glass", "Closets emptied and wiped",
                          "Floors vacuumed and washed"],
            "Final": ["Balcony / patio swept", "Garbage removed", "Keys and fobs returned", "Photos taken",
                      "Utilities transferred", "Forwarding address given"],
        }),
        area("Notes / Items Left Behind", 40),
        signatures(["Tenant / Cleaner", "Landlord / Agent"]),
    ],
    name="Move Out Cleaning Checklist", short="Move Out Checklist",
    about="A move-out (and move-in) cleaning checklist for tenants, landlords and cleaning companies - inside appliances, cabinets, walls, keys and photos.",
    tags=["move out cleaning", "move in cleaning", "end of lease", "tenant checklist",
          "rental cleaning", "cleaning checklist", "landlord form"],
    price=2.95,
)

add(
    slug="office-cleaning-checklist",
    title="Office Cleaning Checklist",
    meta=["Location", "Week Of"],
    body=[
        matrix(["Empty garbage and recycling", "Dust desks and surfaces", "Wipe phones and keyboards", "Clean glass doors",
                "Vacuum carpets", "Mop hard floors", "Kitchen counters and sink", "Wipe microwave and fridge handles",
                "Load / unload dishwasher", "Restock kitchen supplies", "Clean washrooms", "Restock soap and paper",
                "Disinfect handles and switches", "Reception desk", "Meeting rooms reset", "Entrance mats"],
               ["Mon", "Tue", "Wed", "Thu", "Fri"], comment=False, first="Daily Tasks", rh=17),
        matrix(["Dust vents and high surfaces", "Wipe baseboards", "Clean inside fridge", "Wash garbage bins",
                "Interior windows", "Spot-clean walls"], ["Week 1", "Week 2", "Week 3", "Week 4"], comment=False,
               first="Weekly / Monthly Tasks", rh=17),
        area("Supplies Needed / Notes", 40),
        signatures(["Cleaner", "Supervisor"]),
    ],
    name="Office Cleaning Checklist", short="Office Cleaning",
    about="A weekly office cleaning checklist with 16 daily tasks ticked Monday to Friday plus a monthly task grid for deeper jobs.",
    tags=["office cleaning", "commercial cleaning", "janitorial list", "cleaning schedule",
          "workplace cleaning", "cleaning checklist", "office checklist"],
    price=2.95,
)

add(
    slug="janitorial-cleaning-log",
    title="Janitorial Cleaning Log",
    subtitle="Commercial cleaning service record",
    meta=["Client / Site", "Month"],
    body=[
        fill_table([("Date", 1), ("Time In", 0.9), ("Time Out", 0.9), ("Areas Cleaned", 3.4), ("Supplies Used / Needed", 2.4),
                    ("Issues Reported", 2.2), ("Cleaner", 1.1), ("Client Initials", 1)], rh=22),
    ],
    name="Janitorial Cleaning Log", short="Cleaning Log",
    about="A commercial cleaning log for janitorial companies to record each visit, areas cleaned, supplies, issues and client initials.",
    tags=["cleaning log", "janitorial log", "commercial cleaning", "cleaning record",
          "service log", "cleaning business", "visit log"],
    price=2.45,
)

add(
    slug="restroom-cleaning-log",
    title="Restroom Cleaning Log",
    subtitle="Post on the inside of the door",
    meta=["Location", "Date"],
    body=[
        fill_table([("Time", 1), ("Toilets / Urinals", 1.1), ("Sinks & Mirrors", 1.1), ("Floors", 0.9), ("Soap & Paper Restocked", 1.4),
                    ("Garbage Emptied", 1.2), ("Initials", 1), ("Notes", 2.2)], rh=24),
        para("Please report any problem to staff. Thank you for helping keep this washroom clean.", "s"),
    ],
    name="Restroom Cleaning Log", short="Washroom Log",
    about="A washroom / restroom cleaning log to post on the door, showing each check time, tasks done and initials.",
    tags=["restroom log", "washroom log", "bathroom cleaning", "cleaning log", "toilet check",
          "restaurant form", "janitorial log"],
    price=2.45,
)

add(
    slug="kitchen-cleaning-schedule",
    title="Commercial Kitchen Cleaning Schedule",
    meta=["Kitchen", "Week Of"],
    body=[
        matrix(["Prep surfaces sanitized", "Cutting boards washed and sanitized", "Grill and flat-top scraped",
                "Fryers wiped down", "Range and oven exterior", "Hood filters (as needed)", "Reach-in fridge handles and seals",
                "Dish machine cleaned and drained", "Sinks scrubbed", "Floors swept and mopped", "Floor drains cleared",
                "Garbage and compost emptied", "Sanitizer strength checked"],
               ["M", "T", "W", "T", "F", "S", "S"], comment=False, first="Daily", rh=17),
        matrix(["Walk-in cooler shelves", "Ovens deep cleaned", "Hood filters degreased", "Ice machine sanitized",
                "Dry storage swept and rotated", "Walls and splash zones", "Grease trap checked"],
               ["Wk 1", "Wk 2", "Wk 3", "Wk 4"], comment=False, first="Weekly / Monthly", rh=17),
        area("Notes / Corrective Actions", 40),
        signatures(["Kitchen Manager"]),
    ],
    name="Kitchen Cleaning Schedule", short="Kitchen Schedule",
    about="A commercial kitchen cleaning schedule with 13 daily tasks for every day of the week and 7 weekly/monthly deep-clean tasks.",
    tags=["kitchen cleaning", "cleaning schedule", "restaurant form", "commercial kitchen",
          "food safety", "kitchen checklist", "sanitation log"],
    cat="food",
    price=2.95,
)

add(
    slug="vacation-rental-turnover-checklist",
    title="Rental Turnover Checklist",
    subtitle="Short-term / vacation rental cleaning between guests",
    meta=["Property", "Date", "Cleaner"],
    body=[
        fields([("Guest Checked Out", 1), ("Next Check-in", 1), ("No. of Guests", 0.8), ("Time In / Out", 1)]),
        groups({
            "Bedrooms": ["Strip and remake beds", "Check under beds", "Dust surfaces", "Hangers in closets",
                         "Check drawers for items left"],
            "Bathrooms": ["Clean and disinfect", "Fresh towels set out", "Restock toilet paper (2 / roll holder)",
                          "Restock soap, shampoo", "Hair dryer in place"],
            "Kitchen": ["Dishes washed and put away", "Fridge emptied of guest food", "Coffee, tea, sugar restocked",
                        "Dish soap and sponge", "Garbage, recycling, compost out"],
            "Living & Outdoor": ["Vacuum and mop", "Remotes wiped, batteries OK", "Wi-Fi card in place",
                                 "Patio / BBQ cleaned", "Hot tub checked (if any)"],
            "Final Check": ["Thermostat set", "Windows and doors locked", "Lights off", "Damage or missing items noted",
                            "Photos taken", "Keys / lockbox code reset"],
        }),
        area("Damage, Missing Items or Maintenance Needed", 40),
        table([("Supplies Running Low", 4), ("Qty Needed", 1)], rows=3),
    ],
    name="Vacation Rental Cleaning Checklist", short="Turnover Checklist",
    about="A short-term rental turnover cleaning checklist for hosts and cleaners - beds, bathrooms, restocking, final checks, damage notes and supplies.",
    tags=["rental cleaning", "turnover checklist", "str cleaning", "host checklist",
          "cottage rental", "cleaning checklist", "guest turnover"],
    cat="rental",
    canada="Canadian spelling throughout and handy for cottage, cabin and chalet rentals as well as city short-term rentals.",
    price=3.45,
)

add(
    slug="cleaning-client-walkthrough",
    title="Cleaning Client Walk-Through",
    subtitle="New cleaning client & estimate",
    meta=["Date", "Estimator"],
    body=[
        *contact_block("Client"),
        section("Home / Space"),
        fields([("Bedrooms", 1), ("Bathrooms", 1), ("Approx. Size (sq ft / m²)", 1.4), ("Floors / Levels", 1)]),
        options("Type:", ["House", "Condo / apartment", "Office", "Rental turnover", "Move in / out"]),
        options("Frequency:", ["One-time", "Weekly", "Bi-weekly", "Monthly"]),
        options("Flooring:", ["Hardwood", "Laminate", "Tile", "Carpet", "Vinyl"]),
        yesno(["Pets in the home?", "Any allergies or product sensitivities?", "Will a key / lockbox code be provided?",
               "Alarm system?", "Client supplies products and equipment?"]),
        area("Priority Areas & Special Requests", 40),
        area("Do-Not-Touch / Areas to Avoid", 30),
        fields([("Estimated Hours", 1), ("Price per Visit (CAD)", 1), ("GST / HST", 1), ("Start Date", 1)]),
        signatures(["Client", "Cleaning Company"]),
    ],
    name="Cleaning Client Intake Form", short="Cleaning Intake",
    about="A walk-through and intake form for new cleaning clients: home size, frequency, flooring, pets, access, priorities and a per-visit price.",
    tags=["cleaning intake", "cleaning estimate", "client walkthrough", "cleaning quote",
          "new client form", "cleaning business", "house cleaner"],
    price=2.95,
)

RULES = [
    "Check-in is after 4:00 p.m. and check-out is before 11:00 a.m.",
    "Maximum of ___ guests. Visitors must be approved by the host in advance.",
    "Quiet hours are from 10:00 p.m. to 8:00 a.m. Please be respectful of our neighbours.",
    "No smoking or vaping of any kind inside the home or on the property.",
    "No parties or events.",
    "Pets are allowed only with prior approval. Please clean up after them.",
    "Please remove outdoor shoes at the door, especially in winter.",
    "Do not leave windows or doors open while the heat or air conditioning is running.",
    "Please sort garbage, recycling and compost into the bins provided.",
    "Report any damage or breakage to the host right away.",
    "The hot tub, fireplace and BBQ are used at your own risk. Follow the posted instructions.",
    "Lock all doors and windows when you leave the property.",
    "Do not move furniture between rooms.",
    "Thank you for treating our home as your own!",
]
add(
    slug="vacation-rental-house-rules",
    title="House Rules",
    subtitle="Vacation rental  ·  Every rule below can be edited",
    body=[
        fields([("Property Name", 2), ("Host Name", 1.4), ("Host Phone", 1.2)]),
        elist(RULES, blank=3, rh=28),
        fields([("Check-in Time", 1), ("Check-out Time", 1), ("Wi-Fi Network", 1.4), ("Password", 1.4)],
               [("Emergency", 0.7, "value=911"), ("Nearest Hospital", 2), ("Non-Emergency Contact", 1.6)]),
        para("By staying at this property you agree to follow these house rules.", "s"),
    ],
    name="Vacation Rental House Rules", short="House Rules Sign",
    about="An editable house rules page for vacation rentals, cottages and guest suites with 14 pre-written rules you can rewrite, plus check-in times, Wi-Fi and emergency info.",
    tags=["house rules", "rental house rules", "guest rules", "host printable",
          "cottage rules", "str sign", "guest house rules", "vacation home"],
    cat="rental",
    price=3.45,
)

WELCOME = [
    "Welcome! We are so glad you are here. Make yourself at home.",
    "Parking: ",
    "Heat / air conditioning: the thermostat is located ",
    "Fireplace / hot tub: please read the instructions posted beside it before use.",
    "Garbage, recycling and compost day: ",
    "Extra blankets and pillows are in ",
    "First aid kit and fire extinguisher are located ",
    "Favourite local spots: ",
    "Coffee: ",
    "Grocery store: ",
]
add(
    slug="guest-welcome-sheet",
    title="Welcome to Our Home",
    subtitle="Guest information sheet",
    body=[
        fields([("Property", 2), ("Your Host", 1.4), ("Host Phone / Text", 1.4)]),
        section("Wi-Fi"),
        fields([("Network Name", 1), ("Password", 1)]),
        section("Stay Details"),
        fields([("Check-in", 1), ("Check-out", 1), ("Door / Lockbox Code", 1.2)]),
        section("Good to Know"),
        elist(WELCOME, blank=4, numbered=False, rh=26),
        section("In an Emergency"),
        fields([("Emergency", 0.7, "value=911"), ("Nearest Hospital / Clinic", 2), ("Address", 2)],
               [("Pharmacy", 1.4), ("Property Address (for 911)", 2.4)]),
    ],
    name="Guest Welcome Sheet", short="Welcome Sheet",
    about="An editable guest welcome sheet for vacation rentals and guest suites with Wi-Fi, check-in details, house tips, local favourites and emergency info.",
    tags=["welcome sheet", "guest welcome", "host printable", "rental welcome",
          "wifi sign", "guest info", "cottage welcome", "welcome book page"],
    cat="rental",
    price=2.95,
)

CHECKOUT = [
    "Check-out time is 11:00 a.m.",
    "Load and start the dishwasher, or wash and put away dishes.",
    "Empty the fridge of any food you brought.",
    "Take garbage, recycling and compost to the outdoor bins.",
    "Leave used towels in the bathtub or laundry basket.",
    "Turn off lights, fireplace and appliances.",
    "Set the thermostat to ___ °C.",
    "Close and lock all windows and doors.",
    "Return keys to the lockbox and scramble the code.",
    "Send the host a quick message when you have left.",
]
add(
    slug="checkout-instructions",
    title="Check-Out Instructions",
    subtitle="Thank you for staying with us",
    body=[
        fields([("Property", 2), ("Host Phone", 1.2)]),
        elist(CHECKOUT, blank=3, rh=27),
        area("A note from your host", 60),
        para("We hope you enjoyed your stay. Reviews help small hosts like us more than you know. Safe travels!", "s"),
    ],
    name="Check Out Instructions", short="Checkout Sign",
    about="An editable check-out instructions sheet for vacation rentals with ten pre-written steps you can change, plus a personal note from the host.",
    tags=["checkout sign", "check out list", "host printable", "rental checkout",
          "guest checkout", "cottage rental", "str sign"],
    cat="rental",
    price=2.45,
)

add(
    slug="rental-inventory-checklist",
    title="Rental Inventory Checklist",
    subtitle="Furnished rental contents",
    meta=["Property", "Date", "Checked By"],
    body=[
        fill_table([("Room", 1.4), ("Item", 3), ("Qty", 0.7), ("Condition", 1.3), ("Check-in Qty", 1), ("Check-out Qty", 1),
                    ("Notes", 2.4)], rh=19),
        signatures(["Host / Landlord", "Guest / Tenant"]),
    ],
    name="Rental Inventory Checklist", short="Inventory Checklist",
    about="A furnished rental inventory list to record items by room with condition and check-in/check-out quantities.",
    tags=["rental inventory", "furnished rental", "inventory checklist", "landlord form",
          "contents list", "host printable", "property list"],
    cat="rental",
    price=2.45,
)

add(
    slug="guest-registration-form",
    title="Guest Registration Form",
    meta=["Booking No.", "Date"],
    body=[
        *contact_block("Primary Guest"),
        fields([("Arrival Date", 1), ("Departure Date", 1), ("No. of Nights", 0.8), ("No. of Guests", 0.8)],
               [("Vehicle Make / Model", 1.4), ("Licence Plate", 1), ("Plate Province / State", 1)]),
        table([("Additional Guest Name", 4), ("Adult / Child", 1.4)], rows=5),
        options("Pets:", ["None", "Dog", "Cat"], other=True),
        fields([("Rate per Night (CAD)", 1), ("Taxes / Fees", 1), ("Total (CAD)", 1), ("Security Deposit", 1)]),
        consent("I have read and agree to the house rules and cancellation policy, and accept responsibility for any damage "
                "caused during my stay."),
        signatures(["Guest Signature", "Host"]),
    ],
    name="Guest Registration Form", short="Guest Registration",
    about="A guest registration card for B&Bs, cottages, campgrounds and vacation rentals with guests, vehicles, pets, rates and agreement to house rules.",
    tags=["guest registration", "check in form", "bnb form", "guest card", "host printable",
          "cottage rental", "campground form"],
    cat="rental",
    price=2.95,
)

add(
    slug="guest-damage-report",
    title="Damage Report",
    subtitle="Rental property damage or missing items",
    meta=["Report No.", "Date Found"],
    body=[
        fields([("Property", 2), ("Booking / Lease No.", 1.2), ("Reported By", 1.4)],
               [("Guest / Tenant Name", 2), ("Stay / Tenancy Dates", 2)]),
        table([("Item / Area", 2.8), ("Description of Damage", 4), ("Photo?", 0.8), ("Repair / Replace Cost (CAD)", 1.8)], rows=8, rh=22),
        totals(["Total Cost", "Deposit Held", "Amount Deducted", "Balance Owing / Refund"], notes="Notes"),
        options("Guest notified by:", ["Email", "Phone", "Platform message", "In person"]),
        signatures(["Host / Landlord", "Guest / Tenant"]),
    ],
    name="Rental Damage Report", short="Damage Report",
    about="A damage report for rentals and vacation homes to document damaged or missing items, photos, costs and what comes off the deposit.",
    tags=["damage report", "rental damage", "security deposit", "host printable",
          "landlord form", "guest damage", "property damage"],
    cat="rental",
    price=2.95,
)

add(
    slug="pet-agreement",
    title="Pet Agreement",
    subtitle="Addendum for rentals that allow pets",
    meta=["Date"],
    body=[
        fields([("Property Address", 3), ("Unit", 0.7)], [("Tenant / Guest", 2), ("Landlord / Host", 2)]),
        table([("Pet Name", 1.6), ("Type / Breed", 2), ("Age", 0.7), ("Weight (kg)", 1), ("Colour", 1.2), ("Licence / Tag No.", 1.6)], rows=2),
        fields([("Vet Name & Phone", 2), ("Pet Fee / Pet Deposit (if permitted)", 1.6)]),
        section("The tenant / guest agrees to"),
        elist([
            "Keep the pet under control and on a leash in shared areas.",
            "Pick up after the pet right away and dispose of waste properly.",
            "Not leave the pet unattended for long periods or let it disturb neighbours.",
            "Keep vaccinations and any required municipal licence up to date.",
            "Pay for any damage the pet causes beyond normal wear and tear.",
            "Remove the pet if it becomes a danger or a repeated nuisance.",
        ], blank=2),
        para("Pet rules, pet deposits and pet fees are regulated differently in each province. Some provinces do not allow pet "
             "deposits or fees. Check your provincial residential tenancy rules before use.", "s"),
        signatures(["Tenant / Guest", "Landlord / Host"]),
    ],
    name="Pet Agreement Form", short="Pet Agreement",
    about="An editable pet agreement addendum for landlords and vacation rental hosts with pet details, vet contact and rules the tenant or guest agrees to.",
    tags=["pet agreement", "pet addendum", "pet policy", "landlord form", "rental form",
          "pet friendly", "host printable"],
    cat="rental",
    price=2.95,
)

add(
    slug="rental-application",
    title="Rental Application",
    subtitle="Residential tenancy application  ·  Do not include your SIN",
    meta=["Property Address", "Date"],
    body=[
        section("Applicant"),
        fields([("Full Name", 2), ("Phone", 1), ("Email", 1.4)],
               [("Desired Move-in Date", 1), ("Length of Lease", 1), ("Number of Occupants", 1)]),
        section("Current & Previous Addresses"),
        *[fields([(f"{t} Address", 2.4), ("City", 1), ("Province", 0.6, "prov"), ("Dates (from - to)", 1)],
                 [("Landlord / Agent", 1.5), ("Landlord Phone", 1), ("Monthly Rent", 0.8), ("Reason for Leaving", 1.6)])
          for t in ("Current", "Previous")],
        section("Employment & Income"),
        fields([("Employer / Source of Income", 2), ("Position", 1.2), ("Length of Time", 1)],
               [("Supervisor / Contact", 1.6), ("Phone", 1), ("Monthly Income (CAD)", 1)]),
        section("Other Occupants"),
        table([("Name", 3), ("Relationship to Applicant", 2.4), ("Adult / Minor", 1.2)], rows=3),
        fields([("Pets (type & number)", 2), ("Vehicles (make, plate)", 2)]),
        section("References"),
        table([("Name", 2.6), ("Relationship", 2), ("Phone / Email", 3)], rows=2),
        consent("I confirm the information above is true. I consent to the landlord contacting the references and landlords listed, "
                "and (if checked) to a credit check, to assess this application."),
        signatures(["Applicant"]),
    ],
    name="Rental Application Form", short="Rental Application",
    about="A residential rental application for Canadian landlords covering addresses, previous landlords, income, occupants, pets, references and consent - without asking for a SIN.",
    tags=["rental application", "tenant application", "landlord form", "lease application",
          "tenant screening", "canadian landlord", "apartment rental"],
    cat="rental",
    canada="Canadian-ready: written for Canadian landlords, with province/territory drop-downs, CAD income and no Social Insurance Number field, as privacy regulators advise. Check your provincial residential tenancy rules before use.",
    price=3.95,
)

ROOMS = {
    "Entrance & Hallway": ["Door, lock & doorbell", "Walls & ceiling", "Floor", "Closet", "Lights & switches"],
    "Living / Dining Room": ["Walls & ceiling", "Floor / carpet", "Windows & screens", "Blinds / coverings", "Lights & outlets"],
    "Kitchen": ["Fridge", "Stove / oven", "Dishwasher", "Sink & faucet", "Cabinets & counters", "Floor", "Walls & ceiling",
                "Exhaust fan"],
    "Bathroom": ["Toilet", "Tub / shower", "Sink & vanity", "Mirror", "Floor", "Exhaust fan", "Walls & ceiling"],
    "Bedroom 1": ["Walls & ceiling", "Floor / carpet", "Closet", "Windows & screens", "Lights & outlets"],
    "Bedroom 2": ["Walls & ceiling", "Floor / carpet", "Closet", "Windows & screens", "Lights & outlets"],
    "Other": ["Smoke & CO alarms", "Heating / thermostat", "Laundry", "Balcony / patio", "Parking / storage", "Keys & fobs issued"],
}
add(
    slug="move-in-move-out-inspection",
    title="Move-In / Move-Out Inspection",
    subtitle="Rental unit condition report  ·  G good  ·  F fair  ·  P poor  ·  D damaged",
    meta=["Unit Address", "Move-In Date", "Move-Out Date"],
    body=[
        fields([("Tenant(s)", 2), ("Landlord / Agent", 2)], [("City", 1.4), ("Province", 0.7, "prov"), ("Postal Code", 0.9)]),
        *[x for room, items in ROOMS.items() for x in [
            table([(room, 3), ("Move-In Condition", 1.6), ("Move-Out Condition", 1.6), ("Notes / Damage", 3.6)],
                  rows=len(items), prefill=items, rh=17)]],
        section("Sign-off"),
        para("Both parties should inspect the unit together and keep a signed copy. Some provinces have their own required "
             "condition inspection report form - use it where one is required.", "s"),
        signatures(["Tenant (Move-In)", "Landlord (Move-In)", "Tenant (Move-Out)", "Landlord (Move-Out)"]),
        area("Deposit Deductions Agreed / Notes", 50),
    ],
    name="Move In Move Out Inspection", short="Inspection Report",
    about="A two-stage rental condition inspection report covering every room, with move-in and move-out condition codes, notes and sign-off from both parties.",
    tags=["move in inspection", "move out form", "condition report", "rental inspection",
          "landlord form", "tenant checklist", "walkthrough form"],
    cat="rental",
    price=3.95,
)

add(
    slug="rent-ledger",
    title="Rent Ledger",
    subtitle="Tenant payment record  ·  Amounts in Canadian dollars",
    meta=["Tenant", "Unit Address", "Year"],
    body=[
        fields([("Monthly Rent", 1), ("Due Day of Month", 1), ("Deposit Held", 1), ("Lease Start", 1)]),
        table([("Month", 1.4), ("Rent Due", 1.1), ("Date Paid", 1.1), ("Amount Paid", 1.2), ("Method", 1.2), ("Late Fee", 1),
               ("Balance", 1.1), ("Receipt No.", 1.1), ("Notes", 1.8)], rows=12, rh=26,
              prefill=["January", "February", "March", "April", "May", "June", "July", "August", "September",
                       "October", "November", "December"]),
        fields([("Total Rent Due", 1), ("Total Paid", 1), ("Balance Owing", 1)]),
        area("Notes (rent increases, notices given)", 50),
    ],
    name="Rent Ledger", short="Rent Tracker",
    about="A 12-month rent ledger for landlords to track rent due, payments, method, balance and receipt numbers for each tenant.",
    tags=["rent ledger", "rent tracker", "rent log", "landlord form", "tenant payments",
          "rental income", "property manager"],
    cat="rental",
    price=2.95,
)

add(
    slug="tenant-maintenance-request",
    title="Tenant Maintenance Request",
    meta=["Request No.", "Date"],
    body=[
        fields([("Tenant Name", 2), ("Unit / Address", 2)], [("Phone", 1), ("Email", 1.4), ("Best Time to Reach", 1)]),
        options("Issue:", ["Plumbing", "Electrical", "Heating", "Appliance", "Pests", "Doors / locks"], other=True),
        options("Urgency:", ["Emergency (no heat, flood, no power)", "Urgent", "Routine"]),
        area("Describe the problem and where it is", 70),
        options("Entry:", ["OK to enter if I'm not home", "Please call first", "I need to be present"]),
        fields([("Pets in Unit", 1), ("Preferred Days / Times", 2)]),
        signatures(["Tenant"]),
        section("Landlord / Property Manager"),
        fields([("Received", 1), ("Notice of Entry Given", 1), ("Assigned To", 1.4), ("Completed", 1)]),
        area("Work Done / Cost", 40),
    ],
    name="Tenant Maintenance Request", short="Repair Request",
    about="A tenant maintenance and repair request with issue type, urgency, entry permission and a landlord section for notice of entry and completion.",
    tags=["maintenance request", "tenant request", "repair request", "landlord form",
          "work order", "property manager", "rental repair"],
    cat="rental",
    price=2.95,
)

add(
    slug="landlord-property-inspection",
    title="Property Inspection Checklist",
    subtitle="Periodic landlord inspection",
    meta=["Property", "Date", "Inspector"],
    body=[
        fields([("Tenant", 2), ("Notice of Entry Given (date)", 1.4), ("Tenant Present?", 1)]),
        matrix(["Smoke & CO alarms tested", "Fire extinguisher", "Furnace filter", "Water heater - leaks / age",
                "Plumbing leaks under sinks", "Caulking - tub & shower", "Windows, screens & locks", "Doors & locks",
                "Walls, ceilings & floors", "Appliances working", "Electrical - outlets & lights", "Signs of pests or mould",
                "Eavestroughs & downspouts", "Roof / siding (visible)", "Driveway, walkways & steps", "Yard / snow clearing"],
               ["Good", "Repair", "N/A"]),
        table([("Repair Needed", 4.6), ("Priority", 1), ("By Whom", 1.6), ("Done", 1)], rows="fill"),
        signatures(["Landlord / Inspector", "Tenant"]),
    ],
    name="Landlord Property Inspection", short="Property Inspection",
    about="A 16-point periodic rental property inspection for landlords - alarms, furnace filter, leaks, pests, eavestroughs and snow clearing - with a repair list.",
    tags=["property inspection", "landlord checklist", "rental inspection", "home inspection",
          "property manager", "landlord form", "maintenance check"],
    cat="rental",
    price=2.95,
)

add(
    slug="snow-removal-log",
    title="Snow Removal Log",
    subtitle="Plowing, shovelling & salting record",
    meta=["Season", "Client / Site"],
    body=[
        fields([("Site Address", 2.6), ("Contract No.", 1), ("Trigger Depth (cm)", 1)]),
        fill_table([("Date", 1), ("Time In", 0.8), ("Time Out", 0.8), ("Snowfall (cm)", 1), ("Plow", 0.7), ("Shovel", 0.8),
                    ("Salt / Sand", 0.9), ("Qty (kg / bags)", 1.1), ("Areas Serviced", 2.2), ("Operator", 1.1)], rh=21),
        para("Record conditions on arrival and photos of completed areas. Keep this log for the full season.", "s"),
        signatures(["Contractor", "Client"]),
    ],
    name="Snow Removal Log", short="Snow Log",
    about="A seasonal snow removal log for plow operators, landscapers and property managers - snowfall in cm, plowing, shovelling, salting and quantities used.",
    tags=["snow removal", "snow plow log", "snow log", "salting log", "winter service",
          "property manager", "landscaper form"],
    cat="ops",
    canada="Made for Canadian winters: snowfall in centimetres, salt and sand in kilograms or bags, and a trigger depth for seasonal contracts.",
    price=2.95,
)

add(
    slug="landscaping-service-log",
    title="Lawn & Landscaping Service Log",
    meta=["Season", "Client"],
    body=[
        fields([("Property Address", 2.6), ("Province", 0.6, "prov"), ("Service Day", 1)]),
        fill_table([("Date", 1), ("Mow", 0.7), ("Trim", 0.7), ("Edge", 0.7), ("Blow", 0.7), ("Weed", 0.7), ("Fertilize", 0.9),
                    ("Other Work / Notes", 3.4), ("Hours", 0.8), ("Crew", 1)], rh=22),
        para("Tick each service performed. Note watering restrictions, gate codes and pet notes for the crew.", "s"),
        signatures(["Crew Lead", "Client"]),
    ],
    name="Lawn Care Service Log", short="Lawn Service Log",
    about="A lawn care and landscaping visit log with columns to tick mowing, trimming, edging, blowing, weeding and fertilizing for each visit.",
    tags=["lawn care log", "landscaping form", "lawn service", "yard work log", "gardening log",
          "landscaper", "service log"],
    cat="ops",
    price=2.45,
)

add(
    slug="customer-feedback-form",
    title="Customer Feedback Form",
    subtitle="We would love to hear from you",
    meta=["Date"],
    body=[
        fields([("Name (optional)", 2), ("Email (optional)", 2)], [("Product / Service Purchased", 2), ("Date of Visit / Service", 1)]),
        rating(["Overall experience", "Quality", "Value for money", "Friendliness of staff", "Speed of service",
                "Cleanliness", "Likelihood to recommend us"],
               scale=("1", "2", "3", "4", "5"), first="Please rate (1 = poor, 5 = excellent)"),
        area("What did you like most?", 50),
        area("How could we improve?", 50),
        options("How did you find us?", ["Friend", "Online search", "Social media", "Walked by"], other=True),
        consent("You may share my comments (first name only) as a testimonial."),
        consent("I would like to receive emails about news and offers. I can unsubscribe at any time."),
    ],
    name="Customer Feedback Form", short="Feedback Form",
    about="A customer feedback survey with seven 1-5 ratings, open comments, a testimonial permission box and an email opt-in.",
    tags=["feedback form", "customer survey", "comment card", "satisfaction survey",
          "review form", "small business form", "service survey"],
    cat="ops",
    canada="Canadian spelling throughout, with separate express-consent checkboxes for testimonials and email marketing.",
    price=2.45,
)

add(
    slug="guest-feedback-form",
    title="Guest Feedback",
    subtitle="Thank you for staying with us",
    meta=["Stay Dates"],
    body=[
        fields([("Name (optional)", 2), ("Property / Room", 2)]),
        rating(["Cleanliness on arrival", "Comfort of beds", "Kitchen and supplies", "Accuracy of listing",
                "Check-in process", "Communication with host", "Location", "Overall stay"],
               scale=("1", "2", "3", "4", "5"), first="Please rate (1 = poor, 5 = excellent)"),
        area("What did you enjoy most?", 50),
        area("Anything we could add or improve?", 50),
        yesno(["Was anything missing or not working?", "Would you stay with us again?"]),
        consent("You may share my comments (first name only) with future guests."),
    ],
    name="Guest Feedback Form", short="Guest Survey",
    about="A guest feedback form for vacation rentals, cottages and B&Bs with eight 1-5 ratings, open comments and permission to share.",
    tags=["guest feedback", "guest survey", "host printable", "rental feedback", "bnb form",
          "cottage rental", "comment card"],
    cat="rental",
    price=2.45,
)
