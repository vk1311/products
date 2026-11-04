"""Batch 5 - health & safety, incidents, security and food service."""

from common import *  # noqa: F401,F403

FORMS = []


def add(**kw):
    kw.setdefault("cat", "safety")
    FORMS.append(kw)


def where_when():
    return fields([("Date of Incident", 1), ("Time", 0.8), ("Date Reported", 1), ("Reported To", 1.4)],
                  [("Exact Location", 2), ("City", 1), ("Province", 0.7, "prov")])


add(
    slug="incident-report",
    title="Incident Report",
    meta=["Report No.", "Date"],
    body=[
        section("Incident"),
        where_when(),
        options("Type:", ["Injury", "Near miss", "Property damage", "Security", "Vehicle", "Environmental"], other=True),
        section("People Involved"),
        table([("Name", 2.4), ("Role (employee, customer, visitor, contractor)", 3), ("Phone", 1.6), ("Injured?", 1)], rows=3),
        area("What happened? (sequence of events, facts only)", 80),
        area("Injuries or damage", 40),
        area("Immediate actions taken", 40),
        section("Witnesses"),
        table([("Name", 3), ("Phone / Email", 3), ("Statement Taken?", 1.4)], rows=2),
        area("Recommended corrective actions", 40),
        signatures(["Reported By", "Supervisor"]),
    ],
    name="Incident Report Form", short="Incident Report",
    about="A general incident report for any workplace event - injury, near miss, damage, security or vehicle - with people involved, facts, actions and witnesses.",
    tags=["incident report", "accident report", "workplace incident", "incident form",
          "event report", "safety report", "report form"],
    price=3.45,
)

BODY = ["Head / face", "Eye", "Neck", "Shoulder", "Arm / elbow", "Hand / wrist", "Finger", "Back",
        "Chest", "Hip", "Leg / knee", "Foot / ankle"]
add(
    slug="workplace-injury-report",
    title="Workplace Injury Report",
    subtitle="Employee report of injury or illness",
    meta=["Report No.", "Date"],
    body=[
        section("Employee"),
        fields([("Employee Name", 2), ("Job Title", 1.4), ("Supervisor", 1.4)],
               [("Phone", 1), ("Date Hired", 1), ("Usual Shift", 1)]),
        section("Injury"),
        where_when(),
        checklist(BODY, cols=4),
        options("Side:", ["Left", "Right", "Both", "N/A"]),
        options("Nature:", ["Cut", "Strain / sprain", "Burn", "Bruise", "Fracture", "Illness"], other=True),
        area("How did the injury happen? What were you doing?", 60),
        section("Treatment"),
        options("Treatment:", ["First aid only", "Clinic / doctor", "Hospital", "None"]),
        fields([("First Aid Given By", 1.4), ("Clinic / Hospital", 1.6), ("Lost Time?  Yes / No", 1)]),
        fields([("Workers' Comp Board Notified (date)", 1.4), ("Claim No.", 1), ("Return-to-Work Date", 1)]),
        signatures(["Employee", "Supervisor"]),
        para("Report every workplace injury right away. Employers must report certain injuries to their provincial "
             "workers' compensation board within set time limits.", "s"),
    ],
    name="Workplace Injury Report", short="Injury Report",
    about="An employee workplace injury report with body part and injury type checkboxes, treatment, lost time and fields for your workers' compensation claim number.",
    tags=["injury report", "workplace injury", "employee injury", "accident report",
          "work injury form", "first aid report", "ohs form"],
    price=3.45,
)

add(
    slug="near-miss-report",
    title="Near Miss Report",
    subtitle="Close calls are warnings - report them",
    meta=["Report No.", "Date"],
    body=[
        fields([("Reported By (optional)", 2), ("Department / Crew", 1.4)]),
        where_when(),
        options("Category:", ["Slip / trip", "Falling object", "Equipment", "Vehicle", "Electrical", "Chemical"], other=True),
        area("What happened?", 70),
        area("What could have happened?", 50),
        options("Potential severity:", ["Low", "Medium", "High", "Critical"]),
        area("Suggested fix", 50),
        section("Follow-up"),
        fields([("Action Taken", 3), ("Assigned To", 1.2), ("Date Closed", 1)]),
        signatures(["Supervisor"]),
    ],
    name="Near Miss Report Form", short="Near Miss Report",
    about="A near miss (close call) report that captures what happened, what could have happened, severity and the fix - with optional anonymous reporting.",
    tags=["near miss report", "close call", "near miss form", "hazard report",
          "safety report", "incident form", "ohs form"],
    price=2.95,
)

add(
    slug="accident-investigation",
    title="Accident Investigation Report",
    meta=["Report No.", "Investigation Date"],
    body=[
        fields([("Related Incident Report No.", 1.4), ("Investigated By", 2), ("Joint H&S Committee Member", 2)]),
        where_when(),
        area("Description of the accident", 60),
        section("Contributing Factors"),
        groups({
            "People": ["Training", "Fatigue", "Rushing", "Not following procedure"],
            "Equipment": ["Defective / worn", "Guarding missing", "Wrong tool", "Not maintained"],
            "Environment": ["Lighting", "Weather / ice", "Housekeeping", "Noise"],
            "Organization": ["No procedure", "Supervision", "Staffing", "Communication"],
        }, cols=4),
        area("Root cause(s)", 46),
        table([("Corrective Action", 5), ("Responsible", 1.8), ("Due", 1.1), ("Completed", 1.2)], rows=4),
        signatures(["Investigator", "Manager"]),
    ],
    name="Accident Investigation Form", short="Accident Investigation",
    about="An accident investigation report with contributing factors (people, equipment, environment, organization), root cause and corrective action plan.",
    tags=["accident investigation", "root cause", "incident investigation", "safety form",
          "ohs form", "jhsc form", "corrective action"],
    price=3.45,
)

add(
    slug="first-aid-log",
    title="First Aid Log",
    subtitle="Record of first aid treatment",
    meta=["Location", "Year"],
    body=[
        fill_table([("Date", 1), ("Time", 0.8), ("Name of Person", 2), ("Injury / Illness", 2.8), ("Treatment Given", 2.8),
                    ("First Aider", 1.6), ("Referred?", 0.9)], rh=22),
        para("Keep first aid records confidential and for the period your province requires.", "s"),
    ],
    name="First Aid Log", short="First Aid Log",
    about="A first aid treatment log that records every minor injury, the treatment given, the first aider and whether the person was referred on.",
    tags=["first aid log", "first aid record", "injury log", "treatment log", "first aid form",
          "workplace first aid", "ohs log"],
    price=2.95,
)

add(
    slug="vehicle-accident-report",
    title="Vehicle Accident Report",
    subtitle="Keep in the glove box",
    meta=["Date", "Time"],
    body=[
        fields([("Location (street, intersection, highway & km marker)", 3), ("City", 1), ("Province", 0.7, "prov")],
               [("Police Service", 1.6), ("Officer Name / Badge", 1.6), ("Report / Occurrence No.", 1.4)]),
        pair("Your Vehicle", [
            [("Driver", 1)], [("Licence No.", 1), ("Plate", 0.8)], [("Year / Make / Model", 1)],
            [("Insurer", 1), ("Policy No.", 1)],
        ], "Other Vehicle", [
            [("Driver", 1)], [("Licence No.", 1), ("Plate", 0.8)], [("Year / Make / Model", 1)],
            [("Insurer", 1), ("Policy No.", 1)],
        ]),
        options("Conditions:", ["Dry", "Wet", "Snow / ice", "Dark", "Fog"]),
        area("What happened?", 56),
        area("Damage to vehicles / property", 36),
        area("Injuries", 30),
        table([("Witness Name", 3), ("Phone", 2), ("Email", 3)], rows=2),
        area("Sketch of the scene", 70),
        signatures(["Driver"]),
    ],
    name="Vehicle Accident Report", short="Car Accident Form",
    about="A glove-box vehicle accident report for company drivers: other driver and insurance details, police occurrence number, conditions, witnesses and a sketch box.",
    tags=["accident report", "car accident form", "vehicle accident", "fleet form",
          "glove box form", "collision report", "driver form"],
    price=2.95,
)

add(
    slug="customer-incident-report",
    title="Customer / Visitor Incident Report",
    meta=["Report No.", "Date"],
    body=[
        section("Person Involved"),
        fields([("Name", 2), ("Phone", 1), ("Email", 1.4)], [("Address", 2), ("City", 1), ("Province", 0.6, "prov")]),
        options("Person is a:", ["Customer", "Visitor", "Guest", "Contractor", "Delivery"]),
        section("Incident"),
        where_when(),
        area("Description of what happened (in their words, if possible)", 60),
        options("Injury:", ["None", "Minor", "Medical attention needed", "Ambulance called"]),
        area("Action taken by staff", 40),
        fields([("Area Condition (floor, lighting, signs)", 3), ("Photos Taken?  Yes / No", 1.2)]),
        table([("Witness", 3), ("Phone", 2), ("Statement?", 1.2)], rows=2),
        signatures(["Staff Member", "Manager"]),
    ],
    name="Customer Incident Report", short="Customer Incident",
    about="An incident report for customers, guests and visitors who are hurt or involved in an event on your premises - condition of the area, staff action and witnesses.",
    tags=["customer incident", "visitor incident", "guest injury", "slip and fall",
          "store incident", "incident report", "liability form"],
    price=2.95,
)

add(
    slug="witness-statement",
    title="Witness Statement",
    meta=["Related Report No.", "Date"],
    body=[
        section("Witness"),
        fields([("Full Name", 2), ("Phone", 1), ("Email", 1.4)],
               [("Role (employee, customer, visitor)", 2), ("Employer / Company", 1.6)]),
        section("Event Witnessed"),
        fields([("Date of Event", 1), ("Time", 0.8), ("Location", 2.4)]),
        area("Describe exactly what you saw and heard, in the order it happened", 220),
        area("Where were you standing? What was your view?", 50),
        para("I confirm this statement is true and complete to the best of my knowledge.", "s"),
        signatures(["Witness", "Statement Taken By"]),
    ],
    name="Witness Statement Form", short="Witness Statement",
    about="A witness statement form for workplace incidents, accidents and complaints with plenty of space for a full written account.",
    tags=["witness statement", "witness form", "incident witness", "statement form",
          "investigation form", "hr investigation", "safety form"],
    price=2.45,
)

add(
    slug="hazard-report",
    title="Hazard Report",
    meta=["Report No.", "Date"],
    body=[
        fields([("Reported By", 2), ("Department", 1.4), ("Phone / Ext.", 1)],
               [("Location of Hazard", 3), ("Time Observed", 1)]),
        options("Hazard type:", ["Physical", "Chemical", "Biological", "Ergonomic", "Psychosocial"], other=True),
        area("Describe the hazard", 70),
        options("Risk:", ["Low", "Medium", "High - stop work"]),
        area("Suggested control / fix", 50),
        yesno(["Was the area made safe or barricaded?", "Was a supervisor told right away?"]),
        section("Supervisor Response"),
        fields([("Action Taken", 3), ("Date Completed", 1)]),
        area("Feedback given to worker", 34),
        signatures(["Supervisor"]),
    ],
    name="Hazard Report Form", short="Hazard Report",
    about="A workplace hazard report so workers can flag unsafe conditions, rate the risk, suggest a fix and get a documented supervisor response.",
    tags=["hazard report", "unsafe condition", "hazard form", "safety concern",
          "ohs form", "workplace hazard", "safety report"],
    price=2.95,
)

WSI = {
    "Floors & Exits": ["Aisles and exits clear", "Exit signs lit", "Floors dry and even", "Mats in place",
                        "Stairs and railings sound"],
    "Fire & Emergency": ["Extinguishers inspected", "Alarm pull stations clear", "Evacuation map posted",
                         "First aid kit stocked", "Eyewash station working"],
    "Electrical": ["Cords in good repair", "No overloaded outlets", "Panels clear (1 m)", "Guards on machines",
                   "Lockout devices available"],
    "Chemicals (WHMIS)": ["Products labelled", "Safety data sheets current", "Stored correctly", "Spill kit available",
                          "Workers trained"],
    "Storage": ["Heavy items low", "Shelving secure", "Ladders inspected", "No stacking hazards", "Waste removed"],
    "General": ["Lighting adequate", "Ventilation / temperature", "Safety board posted", "PPE available",
                "Washrooms clean"],
}
add(
    slug="workplace-safety-inspection",
    title="Workplace Safety Inspection",
    subtitle="Monthly health & safety walk-through",
    meta=["Date", "Area / Department"],
    body=[
        fields([("Inspected By", 2), ("Health & Safety Rep / Committee", 2)]),
        groups(WSI, cols=3),
        table([("Item Needing Action", 4.5), ("Priority", 1), ("Assigned To", 1.6), ("Due", 1), ("Done", 0.9)], rows="fill"),
        signatures(["Inspector", "Manager"]),
    ],
    name="Workplace Safety Inspection", short="Safety Inspection",
    about="A 30-point monthly workplace safety inspection covering exits, fire, electrical, WHMIS chemicals, storage and general conditions with an action list.",
    tags=["safety inspection", "workplace inspection", "jhsc checklist", "ohs checklist",
          "monthly inspection", "safety checklist", "office safety"],
    price=3.45,
)

MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
add(
    slug="fire-extinguisher-inspection-log",
    title="Fire Extinguisher Inspection Log",
    subtitle="Monthly visual inspection - initial each month",
    meta=["Building", "Year"],
    body=[
        fill_table([("Unit No.", 0.9), ("Location", 2.2), ("Type / Size", 1.3)] + [(m, 0.62) for m in MON]
                   + [("Annual Service", 1.2)], rh=22),
        para("Monthly check: in its place and visible · access clear · pressure gauge in the green · pin and seal intact · "
             "no damage, leaks or corrosion · label readable. Annual maintenance by a qualified technician.", "s"),
    ],
    name="Fire Extinguisher Inspection Log", short="Extinguisher Log",
    about="A yearly fire extinguisher inspection log with a column for each month to initial, plus annual service date and a monthly check reminder.",
    tags=["fire extinguisher", "extinguisher log", "fire safety", "monthly inspection",
          "fire inspection", "building safety", "safety log"],
    price=2.95,
)

add(
    slug="fire-drill-record",
    title="Fire Drill Record",
    meta=["Drill Date", "Time"],
    body=[
        fields([("Building / Address", 3), ("Province", 0.7, "prov")],
               [("Drill Coordinator", 2), ("Fire Wardens", 2.4)]),
        options("Type:", ["Announced", "Unannounced", "Partial", "Night / off-shift"]),
        fields([("Alarm Activated", 1), ("Building Clear", 1), ("Total Evacuation Time", 1), ("People Evacuated", 1)],
               [("Assembly Point", 2), ("Weather", 1)]),
        yesno(["Was the alarm heard in all areas?", "Did everyone use the nearest exit?", "Were elevators avoided?",
               "Was everyone accounted for at the assembly point?", "Were people needing assistance helped?",
               "Did doors close behind evacuees?"]),
        area("Problems Observed", 50),
        table([("Corrective Action", 5), ("Responsible", 2), ("Due", 1.2)], rows=3),
        signatures(["Coordinator", "Manager"]),
    ],
    name="Fire Drill Record", short="Fire Drill Log",
    about="A fire drill record with evacuation times, a six-question performance check, problems observed and corrective actions.",
    tags=["fire drill", "fire drill record", "evacuation drill", "fire safety", "emergency drill",
          "fire log", "building safety"],
    price=2.95,
)

add(
    slug="safety-meeting-sign-in",
    title="Safety Meeting Sign-In",
    subtitle="Toolbox talk / tailgate meeting",
    meta=["Date", "Time", "Site"],
    body=[
        fields([("Topic", 3), ("Presented By", 1.6)]),
        area("Key points discussed", 70),
        area("Hazards or concerns raised by workers", 40),
        fill_table([("Name (print)", 3), ("Company / Crew", 2.4), ("Signature", 2.6)], rh=21),
        signatures(["Supervisor"]),
    ],
    name="Toolbox Talk Sign In Sheet", short="Safety Meeting Sheet",
    about="A toolbox talk and safety meeting sign-in sheet with topic, key points, concerns raised and worker signatures.",
    tags=["toolbox talk", "safety meeting", "sign in sheet", "tailgate meeting",
          "safety talk", "crew meeting", "construction form"],
    price=2.95,
)

add(
    slug="field-level-hazard-assessment",
    title="Field Level Hazard Assessment",
    subtitle="Complete before starting work and when conditions change",
    meta=["Date", "Time", "Job No."],
    body=[
        fields([("Location / Site", 2.4), ("Supervisor", 1.4), ("Emergency Muster Point", 1.6)]),
        groups({
            "Environment": ["Weather / cold / heat", "Ice or slippery surfaces", "Poor lighting", "Noise", "Dust"],
            "Access": ["Working at heights", "Ladders / scaffolds", "Excavations", "Confined space", "Traffic"],
            "Equipment": ["Power tools", "Mobile equipment", "Overhead lines", "Lockout needed", "Hot work"],
            "Personal": ["Lifting / awkward posture", "Working alone", "Fatigue", "Pinch points", "Chemicals"],
        }, cols=4),
        table([("Task", 3), ("Hazard", 3), ("Risk (L / M / H)", 1.3), ("Control / How it will be managed", 4)], rows=6, rh=20),
        options("PPE:", ["Hard hat", "Safety glasses", "Hi-vis", "Gloves", "Boots", "Hearing", "Fall arrest"]),
        fill_table([("Worker Name", 3), ("Signature", 3), ("Time In", 1), ("Time Out", 1)], rh=19),
        signatures(["Supervisor Review"]),
    ],
    name="Field Level Hazard Assessment", short="FLHA Form",
    about="A field level hazard assessment (FLHA) for crews to identify job hazards, rate risk, record controls and PPE, and sign on before work starts.",
    tags=["flha", "hazard assessment", "field level", "jha form", "job hazard",
          "construction safety", "tailgate form", "pre job safety"],
    canada="Canadian-ready: the field level hazard assessment format widely used on Canadian job sites, with winter hazards and a crew sign-on table.",
    price=3.45,
)

FORK = ["Forks, chains & carriage", "Mast & hoses (no leaks)", "Tires & wheels", "Fluid levels", "Battery / fuel / LPG",
        "Seat belt", "Horn", "Lights & alarm", "Brakes & parking brake", "Steering", "Hydraulic controls",
        "Load chart / data plate", "Overhead guard", "Fire extinguisher"]
add(
    slug="forklift-daily-checklist",
    title="Forklift Daily Checklist",
    subtitle="Pre-shift lift truck inspection",
    meta=["Date", "Shift"],
    body=[
        fields([("Operator", 2), ("Truck No.", 1), ("Hour Meter", 1)], [("Type", 1.4), ("Location", 2)]),
        matrix(FORK, ["OK", "Defect"]),
        options("Truck is:", ["Safe to operate", "Tagged out - do not use"]),
        area("Defects / Comments", 40),
        signatures(["Operator", "Supervisor / Maintenance"]),
    ],
    name="Forklift Daily Checklist", short="Forklift Checklist",
    about="A pre-shift forklift (lift truck) inspection checklist with 14 checks, defect reporting and tag-out decision.",
    tags=["forklift checklist", "forklift inspection", "lift truck", "pre shift check",
          "warehouse safety", "daily inspection", "equipment check"],
    price=2.95,
)

add(
    slug="ppe-issue-log",
    title="PPE Issue Log",
    subtitle="Personal protective equipment record",
    meta=["Department / Site", "Year"],
    body=[
        fill_table([("Date", 1), ("Employee", 2.2), ("PPE Item", 2.2), ("Size", 0.8), ("Qty", 0.6),
                    ("Reason (new, replace, lost)", 1.8), ("Issued By", 1.4), ("Employee Signature", 1.8)], rh=21),
        para("Employees confirm they received the PPE listed, were shown how to use and care for it, and will report damage.", "s"),
    ],
    name="PPE Issue Log", short="PPE Log",
    about="A PPE issue log to record safety boots, gloves, glasses, hi-vis and other equipment handed out, with employee signatures.",
    tags=["ppe log", "ppe issue", "safety equipment", "ppe tracker", "protective equipment",
          "ohs log", "safety log"],
    price=2.95,
)

add(
    slug="security-patrol-log",
    title="Security Patrol Log",
    meta=["Date", "Shift", "Site"],
    body=[
        fields([("Officer", 2), ("Badge / Licence No.", 1.4), ("Relieved By", 1.6)]),
        fill_table([("Time", 0.9), ("Area / Checkpoint", 2.6), ("Observations", 4.6), ("Action Taken", 2.4), ("Initials", 0.9)], rh=22),
        signatures(["Officer", "Supervisor"]),
    ],
    name="Security Patrol Log", short="Patrol Log",
    about="A security patrol log for guards to record each round, checkpoint, observation and action taken during a shift.",
    tags=["security log", "patrol log", "guard log", "security form", "night watch",
          "site security", "security guard"],
    price=2.95,
)

add(
    slug="security-daily-activity-report",
    title="Security Daily Activity Report",
    meta=["Date", "Site", "Shift"],
    body=[
        fields([("Officer", 2), ("Licence No.", 1.4), ("Start", 0.8), ("End", 0.8)]),
        options("Weather:", ["Clear", "Rain", "Snow", "Fog", "Extreme cold"]),
        table([("Time", 0.9), ("Activity / Event", 6), ("Reference", 1.4)], rows=14, rh=20),
        yesno(["Any incidents requiring a separate report?", "Police, fire or ambulance called?", "Alarms activated?",
               "Doors and gates secured at end of shift?"]),
        area("Keys, equipment and items handed over", 36),
        signatures(["Officer", "Supervisor"]),
    ],
    name="Security Daily Activity Report", short="Security DAR",
    about="A security guard daily activity report with timed log, incident questions, hand-over notes and supervisor sign-off.",
    tags=["daily activity", "security report", "guard report", "security log", "dar form",
          "security officer", "shift report"],
    price=2.95,
)

add(
    slug="fridge-freezer-temperature-log",
    title="Fridge & Freezer Temperature Log",
    subtitle="Fridge 4 °C or colder  ·  Freezer -18 °C or colder",
    meta=["Month", "Year", "Unit / Location"],
    body=[
        table([("Day", 0.6), ("AM Fridge °C", 1), ("AM Freezer °C", 1), ("Initials", 0.8), ("PM Fridge °C", 1),
               ("PM Freezer °C", 1), ("Initials", 0.8), ("Corrective Action", 3)], rows=31, rh=17.4,
              prefill=[str(i) for i in range(1, 32)]),
        para("If a reading is out of range: re-check, adjust the unit, move food to another unit if needed, discard unsafe food and record "
             "the action. Follow your local public health requirements.", "s"),
        fields([("Reviewed By", 1.4), ("Date", 1)]),
    ],
    name="Fridge Freezer Temperature Log", short="Temperature Log",
    about="A monthly fridge and freezer temperature log in degrees Celsius with AM/PM readings, initials and corrective action for every day.",
    tags=["temperature log", "fridge log", "freezer log", "food safety", "haccp log",
          "celsius log", "kitchen log", "fridge temp"],
    cat="food",
    price=2.95,
)

add(
    slug="food-temperature-log",
    title="Food Temperature Log",
    subtitle="Cooking, hot holding & cooling  ·  Degrees Celsius",
    meta=["Date", "Location"],
    body=[
        para("Typical targets: hot holding 60 °C or hotter  ·  cold holding 4 °C or colder  ·  cool from 60 °C to 20 °C within "
             "2 hours, then to 4 °C within 4 more hours. Use the final cooking temperatures your local public health unit requires.", "s"),
        fill_table([("Time", 0.8), ("Food Item", 2.6), ("Stage (cook, hold, cool, reheat)", 2.2), ("Temp °C", 0.9),
                    ("Within Limit?", 1), ("Corrective Action", 2.8), ("Initials", 0.8)], rh=21),
        signatures(["Supervisor Review"]),
    ],
    name="Food Temperature Log", short="Food Temp Log",
    about="A food temperature log in degrees Celsius for cooking, hot holding, cooling and reheating, with corrective actions and supervisor review.",
    tags=["food temp log", "cooking log", "hot holding", "cooling log", "food safety",
          "haccp form", "kitchen log", "celsius"],
    cat="food",
    price=2.95,
)

add(
    slug="restaurant-opening-checklist",
    title="Restaurant Opening Checklist",
    meta=["Date", "Opening Manager"],
    body=[
        groups({
            "Arrival": ["Disarm alarm, unlock staff door", "Check for overnight issues / leaks", "Lights, music, HVAC on",
                        "Review reservations and notes", "Check staff schedule / call-ins"],
            "Kitchen": ["Record fridge and freezer temps", "Turn on hood, fryers, ovens, grill", "Check deliveries and rotate stock (FIFO)",
                        "Prep list reviewed", "Sanitizer buckets at correct strength", "Handwash sinks stocked",
                        "Date labels on all prepped food"],
            "Front of House": ["Tables and chairs clean and set", "Menus clean, specials board updated",
                               "Washrooms checked and stocked", "Host stand ready", "Patio set (seasonal)",
                               "Entrance and windows clean"],
            "Bar & Cash": ["Bar stocked, garnish prepped", "Ice bins filled", "Float counted into tills",
                           "Card terminals on and tested", "Online order tablets on"],
            "Team": ["Pre-shift meeting held", "Allergens and 86'd items shared", "Sections assigned",
                     "Uniform and hygiene check"],
        }),
        area("Notes / Issues for Manager", 50),
        signatures(["Opening Manager"]),
    ],
    name="Restaurant Opening Checklist", short="Opening Checklist",
    about="A 27-step restaurant opening checklist for arrival, kitchen, front of house, bar and cash, and the pre-shift team meeting.",
    tags=["opening checklist", "restaurant form", "cafe checklist", "kitchen checklist",
          "manager checklist", "restaurant opening", "food service"],
    cat="food",
    price=2.95,
)

add(
    slug="restaurant-closing-checklist",
    title="Restaurant Closing Checklist",
    meta=["Date", "Closing Manager"],
    body=[
        groups({
            "Kitchen": ["Food covered, labelled, dated", "Record fridge and freezer temps", "Equipment off and cleaned",
                        "Fryer oil checked / filtered", "Floors swept and mopped", "Grease traps / drains cleared",
                        "Garbage, recycling and compost out", "Dish area clean, machine drained"],
            "Front of House": ["Tables and chairs wiped", "Condiments refilled", "Floors vacuumed / mopped",
                               "Washrooms cleaned and stocked", "Patio furniture secured", "Lost & found logged"],
            "Bar": ["Bar tops and mats cleaned", "Beer lines / taps cleaned (as scheduled)", "Ice bins emptied",
                    "Alcohol locked up", "Stock count / order list"],
            "Cash & Security": ["Tills counted and reconciled", "Deposit prepared and locked in safe",
                                "Card batch closed", "Doors, windows and back door locked", "Alarm set"],
        }),
        area("Notes for Opening Team", 50),
        signatures(["Closing Manager"]),
    ],
    name="Restaurant Closing Checklist", short="Closing Checklist",
    about="A 24-step restaurant closing checklist for the kitchen, front of house, bar, cash and security, with notes for the opening team.",
    tags=["closing checklist", "restaurant form", "cafe checklist", "kitchen closing",
          "end of day", "restaurant closing", "food service"],
    cat="food",
    price=2.95,
)

add(
    slug="retail-opening-closing-checklist",
    title="Retail Opening & Closing Checklist",
    meta=["Date", "Manager"],
    body=[
        groups({
            "Opening": ["Disarm alarm, lights on", "Walk the floor for issues", "Count float into till",
                        "Turn on POS and card terminals", "Check email, online orders and messages",
                        "Displays faced and tidy", "Fitting rooms clean", "Entrance swept, signs out",
                        "Unlock doors on time"],
            "Closing": ["Lock doors at closing time", "Recover fitting rooms", "Restock and face shelves",
                        "Count till and print end-of-day report", "Prepare and lock deposit", "Close card batch",
                        "Garbage and recycling out", "Lights and equipment off", "Set alarm, lock up"],
        }),
        area("Shift Notes", 60),
        signatures(["Opened By", "Closed By"]),
    ],
    name="Retail Opening Closing Checklist", short="Store Checklist",
    about="An opening and closing checklist for retail stores and boutiques covering the till, POS, displays, deposits and lock-up.",
    tags=["retail checklist", "store opening", "store closing", "boutique checklist",
          "shop checklist", "manager checklist", "retail form"],
    cat="ops",
    price=2.95,
)

add(
    slug="lost-and-found-log",
    title="Lost & Found Log",
    meta=["Location", "Year"],
    body=[
        fill_table([("Date Found", 1), ("Item Description", 3), ("Where Found", 1.8), ("Found By", 1.4), ("Storage Spot", 1.2),
                    ("Claimed By / ID", 2), ("Date Claimed", 1)], rh=22),
        para("Hold items for ______ days. Unclaimed items will be donated or disposed of.", "s"),
    ],
    name="Lost and Found Log", short="Lost & Found Log",
    about="A lost and found log for shops, restaurants, gyms, offices and rentals with where items were found, where they are stored and who claimed them.",
    tags=["lost and found", "lost property", "found items", "front desk form", "hotel form",
          "reception log", "office log"],
    cat="ops",
    price=2.45,
)

add(
    slug="customer-complaint-form",
    title="Customer Complaint Form",
    meta=["Complaint No.", "Date Received"],
    body=[
        *contact_block("Customer"),
        options("Received by:", ["In person", "Phone", "Email", "Online review", "Social media"]),
        fields([("Order / Invoice No.", 1), ("Date of Purchase / Service", 1), ("Staff Involved", 1.4)]),
        options("Category:", ["Product", "Service", "Billing", "Staff", "Delivery", "Cleanliness"], other=True),
        area("Complaint details", 70),
        area("What would the customer like us to do?", 40),
        section("Resolution"),
        area("Action taken", 50),
        fields([("Resolved By", 1.4), ("Date Resolved", 1), ("Cost of Resolution (CAD)", 1)]),
        options("Customer satisfied:", ["Yes", "Partly", "No", "Follow-up needed"]),
        signatures(["Manager"]),
    ],
    name="Customer Complaint Form", short="Complaint Form",
    about="A customer complaint form that records the issue, what the customer wants, the action taken and whether they left satisfied.",
    tags=["complaint form", "customer complaint", "complaint log", "customer service",
          "feedback form", "resolution form", "service recovery"],
    cat="ops",
    price=2.95,
)
