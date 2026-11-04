"""Batch 4 - HR, scheduling and payroll."""

from common import *  # noqa: F401,F403

FORMS = []


def add(**kw):
    kw.setdefault("cat", "hr")
    FORMS.append(kw)


DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
TS_COLS = [("Day", 1.5), ("Date", 1.1), ("Time In", 1), ("Lunch Out", 1), ("Lunch In", 1), ("Time Out", 1),
           ("Regular Hrs", 1.1), ("Overtime Hrs", 1.1), ("Stat / Vacation", 1.2), ("Total", 1)]


def employee_rows():
    return fields([("Employee Name", 2), ("Employee ID", 1), ("Department / Position", 1.6)],
                  [("Supervisor", 2), ("Pay Period Start", 1), ("Pay Period End", 1)])


add(
    slug="job-application",
    title="Employment Application",
    subtitle="Please type or print clearly",
    meta=["Position Applied For", "Date"],
    body=[
        para("Accommodation is available on request for candidates taking part in all aspects of the selection process.", "s"),
        section("Applicant"),
        fields([("Full Name", 2), ("Preferred Name", 1), ("Phone", 1)],
               [("Street Address", 2), ("Email", 1.6)],
               [("City", 2), ("Province", 1, "prov"), ("Postal Code", 1.1)]),
        section("Position & Availability"),
        options("Employment sought:", ["Full-time", "Part-time", "Seasonal", "Casual", "Contract"]),
        fields([("Date Available to Start", 1), ("Desired Pay", 1), ("Hours Available per Week", 1)]),
        matrix(DAYS, ["Morning", "Afternoon", "Evening", "Overnight"], comment=False, first="Availability", rh=15),
        yesno(["Are you legally entitled to work in Canada?",
               "Do you hold a valid driver's licence (if required for this position)?",
               "Have you worked for this company before?",
               "Can you work weekends and holidays if scheduled?"]),
        section("Education & Training"),
        table([("School / Program", 4), ("City", 2), ("Diploma / Certificate", 3), ("Completed", 1.2)], rows=3),
        table([("Certifications / Licences (e.g., first aid, food handler, trade ticket)", 6), ("Expiry", 1.4)], rows=2),
        pagebreak(),
        section("Employment History (most recent first)"),
        *[fields([(f"Employer {n}", 2), ("Phone", 1), ("City", 1)],
                 [("Job Title", 2), ("Start (mm/yy)", 1), ("End (mm/yy)", 1)],
                 [("Duties", 2.6), ("Reason for Leaving", 1.6)],
                 [("Supervisor", 2), ("May we contact?  Yes / No", 1.4)]) for n in (1, 2, 3)],
        section("References (not related to you)"),
        table([("Name", 2.4), ("Relationship", 2), ("Company", 2.2), ("Phone / Email", 2.4)], rows=3, rh=20),
        area("Skills, languages or anything else you would like us to know", 52),
        section("Declaration"),
        para("I confirm that the information in this application is true and complete. I understand that false or "
             "misleading information may be grounds for not hiring me or for ending employment. I authorize the employer to "
             "contact the references and past employers listed above.", "s"),
        signatures(["Applicant Signature"]),
    ],
    name="Job Application Form", short="Employment Application",
    about="A two-page employment application for Canadian small businesses: availability grid, education, three past jobs, references and a declaration - without questions about age, marital status or SIN.",
    tags=["job application", "employment app", "hiring form", "applicant form",
          "application form", "new hire form", "canadian employer"],
    price=4.45,
)

add(
    slug="interview-evaluation",
    title="Interview Evaluation Form",
    meta=["Date", "Interviewer"],
    body=[
        fields([("Candidate Name", 2), ("Position", 2), ("Interview Type", 1.2)]),
        rating(["Relevant experience", "Job-specific skills", "Communication", "Problem solving",
                "Customer focus", "Teamwork", "Reliability / availability", "Fit with role requirements"],
               scale=("1", "2", "3", "4", "5"), first="Criteria (1 = poor, 5 = excellent)"),
        area("Strengths", 50),
        area("Concerns / Areas to Explore", 50),
        options("Recommendation:", ["Hire", "Second interview", "Hold", "Do not proceed"]),
        fields([("Overall Score", 1), ("Reference Check Done", 1), ("Salary Expectation", 1)]),
        para("Evaluate only job-related criteria. Do not record information about protected grounds under human rights law.", "s"),
        signatures(["Interviewer"]),
    ],
    name="Interview Evaluation Form", short="Interview Scorecard",
    about="A structured interview scorecard with eight job-related criteria rated 1-5, strengths, concerns and a hiring recommendation.",
    tags=["interview form", "interview scorecard", "candidate rating", "hiring form",
          "interview notes", "recruitment form", "evaluation form"],
    price=3.45,
)

add(
    slug="reference-check",
    title="Reference Check Form",
    meta=["Date", "Checked By"],
    body=[
        fields([("Candidate", 2), ("Position Applied For", 2)],
               [("Reference Name", 2), ("Company", 1.6), ("Phone / Email", 1.6)],
               [("Reference's Title", 2), ("Relationship to Candidate", 2)]),
        para("Candidate consent to contact this reference was obtained:  Yes / No  (circle or type)", "s"),
        *[x for q in [
            "Dates of employment and position held",
            "Main duties and responsibilities",
            "Strengths",
            "Areas for improvement",
            "Reliability and attendance",
            "How did they work with coworkers, customers and supervisors?",
            "Reason for leaving",
        ] for x in [area(q, 34)]],
        yesno(["Would you rehire this person?"]),
        area("Other Comments", 30),
    ],
    name="Reference Check Form", short="Reference Check",
    about="A reference check form with consent confirmation and the key questions to ask former employers about duties, strengths, reliability and rehire eligibility.",
    tags=["reference check", "employment ref", "hiring form", "reference form",
          "recruiting form", "background check", "reference questions"],
    price=3.45,
)

add(
    slug="new-hire-onboarding-checklist",
    title="New Hire Onboarding Checklist",
    subtitle="Canadian employers",
    meta=["Employee", "Start Date", "Manager"],
    body=[
        groups({
            "Before Day One": ["Offer letter signed and filed", "Start date, hours and pay confirmed",
                               "Workspace, uniform and tools ready", "Accounts and email set up",
                               "Keys / access card ordered", "Welcome message sent"],
            "Paperwork": ["Federal TD1 completed", "Provincial TD1 completed", "SIN recorded securely",
                          "Direct deposit form and void cheque", "Emergency contact form", "Signed policies / handbook"],
            "Health & Safety": ["Workplace safety orientation", "WHMIS training", "Emergency exits and first aid shown",
                                "Hazards of the job reviewed", "Right to refuse unsafe work explained",
                                "PPE issued"],
            "Payroll & Benefits": ["Added to payroll", "CPP / EI / tax deductions set up", "Vacation pay rate confirmed",
                                   "Benefits enrolment (if any)", "Probation period explained",
                                   "Employment standards poster shown"],
            "First Week": ["Team introductions", "Job duties and expectations reviewed", "Systems training",
                           "Schedule for first month", "Buddy / mentor assigned", "End-of-week check-in"],
            "First 90 Days": ["30-day check-in", "60-day check-in", "Probation review completed",
                              "Training record updated", "Goals set for next period", "Onboarding file complete"],
        }),
        area("Notes", 40),
        signatures(["Employee", "Manager"]),
    ],
    name="New Hire Onboarding Checklist", short="Onboarding Checklist",
    about="A 36-step new hire onboarding checklist for Canadian employers covering TD1 forms, SIN, direct deposit, WHMIS and safety orientation, payroll set-up and the first 90 days.",
    tags=["onboarding checklist", "new hire checklist", "employee onboarding", "hr checklist",
          "new employee", "orientation form", "first day checklist"],
    price=3.95,
)

add(
    slug="new-employee-information",
    title="New Employee Information",
    subtitle="Confidential - store securely",
    meta=["Start Date", "Employee ID"],
    body=[
        section("Personal"),
        fields([("Legal Name", 2), ("Preferred Name", 1), ("Pronouns (optional)", 1)],
               [("Street Address", 2), ("City", 1)],
               [("Province", 0.7, "prov"), ("Postal Code", 0.8), ("Phone", 1), ("Email", 1.5)],
               [("Social Insurance Number (SIN)", 1.4), ("Date of Birth (for payroll & benefits)", 1.4)]),
        section("Position"),
        fields([("Job Title", 2), ("Department", 1.4), ("Manager", 1.4)],
               [("Work Location", 2), ("Pay Rate (CAD)", 1), ("Pay Frequency", 1)]),
        options("Status:", ["Full-time", "Part-time", "Seasonal", "Casual", "Temporary"]),
        options("Pay type:", ["Hourly", "Salary", "Commission"]),
        section("Emergency Contact"),
        fields([("Name", 2), ("Relationship", 1.2), ("Phone", 1.2)],
               [("Alternate Contact", 2), ("Relationship", 1.2), ("Phone", 1.2)]),
        section("Documents Received"),
        checklist(["Federal TD1", "Provincial TD1", "Direct deposit / void cheque", "Signed offer letter",
                   "Proof of work eligibility", "Copies of certifications"], cols=3),
        area("Notes / Accommodations", 40),
        signatures(["Employee", "HR / Manager"]),
    ],
    name="New Employee Information Form", short="Employee Info Form",
    about="A confidential new employee information form with SIN, position, pay details, emergency contacts and a document checklist for TD1 forms and direct deposit.",
    tags=["employee info form", "new hire form", "employee record", "hr form",
          "personnel form", "staff details", "employee file"],
    price=3.45,
)

add(
    slug="emergency-contact-form",
    title="Employee Emergency Contact Form",
    subtitle="Confidential",
    meta=["Date"],
    body=[
        section("Employee"),
        fields([("Full Name", 2), ("Employee ID", 1), ("Department", 1.4)],
               [("Home Address", 2), ("City", 1), ("Province", 0.6, "prov")],
               [("Home Phone", 1), ("Mobile Phone", 1), ("Personal Email", 1.4)]),
        *[x for n, t in ((1, "Primary Contact"), (2, "Secondary Contact"), (3, "Third Contact")) for x in [
            section(t),
            fields([("Name", 2), ("Relationship", 1.2)], [("Mobile Phone", 1), ("Other Phone", 1), ("Email", 1.4)]),
        ]],
        section("Medical (optional)"),
        area("Allergies, medical conditions or medications responders should know about", 44),
        fields([("Family Doctor", 1.4), ("Doctor Phone", 1), ("Provincial Health Card No. (optional)", 1.6)]),
        para("This information is voluntary, kept confidential and used only in an emergency.", "s"),
        signatures(["Employee Signature"]),
    ],
    name="Emergency Contact Form", short="Emergency Contact",
    about="An employee emergency contact form with three contacts and an optional medical section, written for confidential use only in an emergency.",
    tags=["emergency contact", "employee contact", "hr form", "staff emergency",
          "contact sheet", "employee record", "emergency form"],
    price=2.95,
)

add(
    slug="direct-deposit-authorization",
    title="Direct Deposit Authorization",
    subtitle="Payroll direct deposit - Canadian bank account",
    meta=["Date"],
    body=[
        section("Employee"),
        fields([("Full Name", 2), ("Employee ID", 1)], [("Address", 2), ("Phone", 1)]),
        options("Request:", ["New set-up", "Change account", "Cancel direct deposit"]),
        section("Bank Account"),
        fields([("Financial Institution", 2), ("Branch Address", 2)],
               [("Institution No. (3 digits)", 1), ("Transit No. (5 digits)", 1), ("Account No.", 1.6)]),
        options("Account type:", ["Chequing", "Savings"]),
        fields([("Amount or % to deposit (if splitting)", 1), ("Remainder to", 1)]),
        para("Please attach a void cheque or a direct deposit form from your bank. On a Canadian cheque the numbers along the "
             "bottom read: cheque no. - transit no. (5) - institution no. (3) - account no.", "s"),
        section("Authorization"),
        para("I authorize my employer to deposit my pay into the account above and, if an error occurs, to correct it "
             "by adjusting a future deposit. This authorization stays in effect until I give written notice.", "s"),
        signatures(["Employee Signature", "Received By (Payroll)"]),
        area("Payroll Use", 40),
    ],
    name="Direct Deposit Form", short="Direct Deposit Form",
    about="A Canadian payroll direct deposit authorization with institution, transit and account number fields, account type and void-cheque instructions.",
    tags=["direct deposit", "payroll form", "bank form", "deposit authorization",
          "void cheque", "employee payroll", "hr form"],
    canada="Built for Canadian banking: 3-digit institution number, 5-digit transit number and a guide to reading a void cheque.",
    price=2.95,
)

add(
    slug="timesheet-weekly",
    title="Weekly Timesheet",
    meta=["Week Of"],
    body=[
        employee_rows(),
        table(TS_COLS, rows=7, prefill=DAYS, rh=34),
        totals(["Regular Hours", "Overtime Hours", "Stat Holiday / Vacation", "Total Hours"], notes="Notes"),
        signatures(["Employee", "Supervisor Approval"]),
        area("Payroll Use / Comments", 40),
    ],
    name="Weekly Timesheet", short="Weekly Timesheet",
    about="A weekly employee timesheet with time in/out, lunch, regular hours, overtime and a column for statutory holiday or vacation hours.",
    tags=["weekly timesheet", "timesheet", "time sheet", "employee hours", "time card",
          "work hours log", "payroll form", "hours tracker"],
    price=2.95,
)

add(
    slug="timesheet-biweekly",
    title="Bi-Weekly Timesheet",
    meta=["Pay Period"],
    body=[
        employee_rows(),
        table(TS_COLS, rows=14, prefill=DAYS + DAYS, rh=26),
        totals(["Week 1 Total", "Week 2 Total", "Overtime Hours", "Stat Holiday / Vacation", "Total Hours"],
               notes="Notes"),
        signatures(["Employee", "Supervisor Approval"]),
    ],
    name="Bi-Weekly Timesheet", short="Biweekly Timesheet",
    about="A two-week (bi-weekly) timesheet for payroll with daily time in/out, lunch, overtime, stat holiday hours and approvals.",
    tags=["biweekly timesheet", "bi weekly", "timesheet", "time sheet", "pay period",
          "employee hours", "payroll form"],
    price=2.95,
)

add(
    slug="timesheet-monthly",
    title="Monthly Timesheet",
    meta=["Month", "Year"],
    body=[
        fields([("Employee Name", 2), ("Employee ID", 1), ("Position", 1.4), ("Supervisor", 1.4)]),
        table([("Date", 0.7), ("Time In", 1), ("Time Out", 1), ("Break", 0.8), ("Regular", 1), ("Overtime", 1),
               ("Stat / Vac. / Sick", 1.3), ("Total", 0.9), ("Notes", 2.4)], rows=31, rh=16.4,
              prefill=[str(i) for i in range(1, 32)]),
        fields([("Total Regular", 1), ("Total Overtime", 1), ("Total Stat / Vacation / Sick", 1.4), ("Grand Total", 1)]),
        signatures(["Employee", "Supervisor Approval"]),
    ],
    name="Monthly Timesheet", short="Monthly Timesheet",
    about="A one-page monthly timesheet with all 31 days, regular and overtime hours, stat/vacation/sick column and approval signatures.",
    tags=["monthly timesheet", "timesheet", "time sheet", "monthly hours", "employee hours",
          "attendance log", "payroll form"],
    price=2.95,
)

add(
    slug="employee-time-card",
    title="Employee Time Card",
    subtitle="Two cards per page",
    body=[
        *[x for _ in range(2) for x in [
            fields([("Employee", 2), ("Week Ending", 1), ("Dept.", 1)]),
            table([("Day", 1.4), ("In", 1), ("Out", 1), ("In", 1), ("Out", 1), ("Hours", 1), ("OT", 0.9)],
                  rows=7, prefill=DAYS, rh=25),
            fields([("Total Hours", 1), ("Employee Signature", 1.6), ("Approved By", 1.6)]),
            spacer(14),
        ]],
    ],
    name="Employee Time Card", short="Time Card",
    about="Two weekly punch-style time cards per page with split shifts (in/out twice a day), daily hours, overtime and approval.",
    tags=["time card", "punch card", "employee time", "weekly hours", "timesheet",
          "time clock card", "shift hours"],
    price=2.45,
)

add(
    slug="contractor-timesheet",
    title="Contractor Timesheet",
    subtitle="Billable hours  ·  Amounts in Canadian dollars",
    meta=["Period From", "Period To", "Invoice No."],
    body=[
        pair("Contractor", biz_rows(), "Client", client_rows([("Project / PO No.", 1)])),
        fill_table([("Date", 1.1), ("Task / Description", 5), ("Start", 0.9), ("End", 0.9), ("Hours", 0.9)]),
        totals(["Total Hours", "Hourly Rate", "Subtotal", "GST / HST  ____ %", "Total (CAD)"], notes="Notes"),
        signatures(["Contractor", "Client Approval"]),
    ],
    name="Contractor Timesheet", short="Contractor Timesheet",
    about="A billable-hours timesheet for independent contractors and freelancers with hourly rate, GST/HST line and client approval.",
    tags=["contractor timesheet", "freelance hours", "billable hours", "hours log",
          "consultant timesheet", "self employed", "timesheet"],
    cat="finance",
    price=2.95,
)

add(
    slug="weekly-employee-schedule",
    title="Weekly Employee Schedule",
    meta=["Week Of", "Location"],
    body=[
        fill_table([("Employee", 2)] + [(d[:3], 1.25) for d in DAYS] + [("Hours", 0.9)], rh=26),
        para("Write shifts as start-end (e.g., 9-5). OFF = day off, V = vacation, S = sick, STAT = statutory holiday.", "s"),
        fields([("Posted By", 1.4), ("Date Posted", 1), ("Manager Phone", 1.2)]),
    ],
    name="Weekly Employee Schedule", short="Staff Schedule",
    about="A weekly staff schedule (rota) for shops, restaurants and clinics with a row per employee, each day of the week and total hours.",
    tags=["employee schedule", "staff schedule", "work schedule", "shift schedule",
          "weekly rota", "shift planner", "restaurant schedule"],
    price=2.95,
)

add(
    slug="time-off-request",
    title="Time Off Request",
    meta=["Date Submitted"],
    body=[
        fields([("Employee Name", 2), ("Employee ID", 1), ("Department / Position", 1.6)]),
        options("Type:", ["Vacation", "Sick", "Personal", "Bereavement", "Family responsibility"]),
        options("", ["Jury duty", "Unpaid leave", "Stat holiday swap"], other=True),
        fields([("First Day Off", 1), ("Last Day Off", 1), ("Return to Work", 1), ("Total Days / Hours", 1)]),
        options("Partial day:", ["No", "Yes - from / to:"]),
        area("Reason / Coverage Notes (optional)", 52),
        signatures(["Employee"]),
        section("Manager"),
        options("Decision:", ["Approved", "Denied", "Approved with changes"]),
        fields([("Vacation Balance Before", 1), ("Days Used", 1), ("Balance After", 1)]),
        area("Comments", 40),
        signatures(["Manager"]),
    ],
    name="Time Off Request Form", short="Time Off Request",
    about="A time-off request form for vacation, sick, bereavement and family responsibility leave with manager approval and vacation balance tracking.",
    tags=["time off request", "vacation request", "leave request", "pto form", "absence form",
          "holiday request", "hr form"],
    price=2.95,
)

add(
    slug="overtime-authorization",
    title="Overtime Authorization",
    meta=["Date"],
    body=[
        fields([("Employee Name", 2), ("Employee ID", 1), ("Department", 1.4)]),
        table([("Date", 1.2), ("Start Time", 1), ("End Time", 1), ("Hours", 0.9), ("Reason / Task", 5)], rows=6, rh=22),
        options("Compensation:", ["Overtime pay", "Banked time in lieu", "Per employment agreement"]),
        area("Business Reason", 50),
        para("Overtime thresholds and rates are set by provincial employment standards. Check the rules for your province.", "s"),
        signatures(["Employee", "Authorized By"]),
    ],
    name="Overtime Authorization Form", short="Overtime Form",
    about="An overtime request and authorization form with dates, hours, reason and choice of overtime pay or banked time.",
    tags=["overtime form", "overtime request", "ot approval", "extra hours", "hr form",
          "payroll form", "banked time"],
    price=2.95,
)

add(
    slug="shift-swap-request",
    title="Shift Swap Request",
    meta=["Date"],
    body=[
        section("Original Shift"),
        fields([("Employee", 2), ("Position", 1.4)], [("Shift Date", 1), ("Start", 1), ("End", 1)]),
        section("Covering Employee"),
        fields([("Employee", 2), ("Position", 1.4)], [("Their Shift Given in Return (date)", 1.6), ("Start", 1), ("End", 1)]),
        area("Reason (optional)", 40),
        signatures(["Requesting Employee", "Covering Employee"]),
        section("Manager"),
        options("Decision:", ["Approved", "Denied"]),
        area("Comments", 40),
        signatures(["Manager"]),
    ],
    name="Shift Swap Request", short="Shift Swap Form",
    about="A shift swap / shift trade request signed by both employees and approved by a manager.",
    tags=["shift swap", "shift trade", "shift change", "schedule change", "staff form",
          "restaurant staff", "hr form"],
    price=2.45,
)

add(
    slug="attendance-tracker",
    title="Monthly Attendance Tracker",
    meta=["Month", "Year", "Department"],
    body=[
        fill_table([("Employee", 4.2)] + [(str(i), 0.75) for i in range(1, 32)] + [("Total", 1.3)], rh=20),
        para("Codes:  P present  ·  A absent  ·  L late  ·  S sick  ·  V vacation  ·  H statutory holiday  ·  "
             "U unpaid leave  ·  T training", "s"),
    ],
    name="Employee Attendance Tracker", short="Attendance Tracker",
    about="A monthly attendance tracker for a whole team with all 31 days and codes for present, absent, late, sick, vacation and statutory holidays.",
    tags=["attendance tracker", "attendance sheet", "employee tracker", "absence log",
          "staff attendance", "monthly tracker", "hr form"],
    price=2.95,
)

add(
    slug="disciplinary-notice",
    title="Employee Warning Notice",
    subtitle="Corrective action record",
    meta=["Date"],
    body=[
        fields([("Employee Name", 2), ("Position", 1.4), ("Department", 1.4)],
               [("Supervisor", 2), ("Date of Incident", 1), ("Location", 1.4)]),
        options("Notice:", ["Verbal warning (documented)", "Written warning", "Final warning", "Suspension"]),
        options("Concern:", ["Attendance", "Lateness", "Performance", "Conduct", "Safety", "Policy"], other=True),
        area("Description of the Issue (facts, dates, what happened)", 70),
        area("Previous Discussions or Warnings", 34),
        area("Expected Improvement & Support Offered", 50),
        fields([("Review Date", 1), ("Consequence if Not Resolved", 3)]),
        area("Employee Comments", 40),
        para("Signing confirms the employee received this notice. It does not mean they agree with it.", "s"),
        signatures(["Employee", "Supervisor", "Witness"]),
    ],
    name="Employee Warning Notice", short="Write-Up Form",
    about="An employee warning and corrective action form documenting the issue, past discussions, improvement plan, review date and employee comments.",
    tags=["write up form", "employee warning", "disciplinary form", "corrective action",
          "hr form", "warning notice", "employee discipline"],
    price=2.95,
)

add(
    slug="performance-review",
    title="Employee Performance Review",
    meta=["Review Date", "Review Period"],
    body=[
        fields([("Employee Name", 2), ("Position", 1.4), ("Reviewer", 1.4)]),
        rating(["Quality of work", "Productivity", "Job knowledge", "Reliability & attendance", "Communication",
                "Teamwork", "Customer service", "Initiative", "Safety practices", "Follows policies"],
               scale=("1", "2", "3", "4", "5"), first="Rating (1 = needs improvement, 5 = outstanding)"),
        area("Key Accomplishments", 44),
        area("Areas for Growth", 44),
        table([("Goal for Next Period", 5), ("Measure of Success", 3), ("Target Date", 1.3)], rows=3, rh=20),
        area("Employee Comments", 34),
        signatures(["Employee", "Reviewer"]),
    ],
    name="Performance Review Form", short="Performance Review",
    about="An employee performance review with ten rated competencies, accomplishments, growth areas, next-period goals and employee comments.",
    tags=["performance review", "employee review", "annual review", "appraisal form",
          "evaluation form", "hr form", "staff review"],
    price=3.45,
)

add(
    slug="probation-review",
    title="Probation Period Review",
    meta=["Review Date"],
    body=[
        fields([("Employee Name", 2), ("Position", 1.4), ("Manager", 1.4)],
               [("Start Date", 1), ("Probation End Date", 1), ("Review Point", 1.2, "value=30 / 60 / 90 days")]),
        rating(["Learns duties quickly", "Quality of work", "Attendance & punctuality", "Follows safety rules",
                "Works well with team", "Customer interactions", "Takes direction"],
               scale=("Below", "Meets", "Exceeds"), first="Area"),
        area("What is going well", 46),
        area("What needs to improve", 46),
        options("Outcome:", ["Pass probation", "Extend probation (if permitted)", "End employment"]),
        para("Probation rules and notice requirements differ by province. Check your provincial employment standards.", "s"),
        signatures(["Employee", "Manager"]),
    ],
    name="Probation Review Form", short="Probation Review",
    about="A probation (30/60/90-day) review for new employees with seven rated areas, feedback and a clear outcome.",
    tags=["probation review", "90 day review", "new hire review", "probationary form",
          "employee review", "hr form", "30 60 90 review"],
    price=2.95,
)

add(
    slug="exit-interview",
    title="Exit Interview",
    meta=["Date", "Interviewer"],
    body=[
        fields([("Employee Name", 2), ("Position", 1.4), ("Department", 1.4)],
               [("Start Date", 1), ("Last Day", 1), ("Manager", 1.6)]),
        options("Reason for leaving:", ["New job", "Pay", "Schedule", "Relocation", "School", "Retirement"], other=True),
        rating(["Job duties matched expectations", "Training and support", "Pay and benefits", "Schedule / workload",
                "Relationship with manager", "Team environment", "Safety culture"],
               scale=("1", "2", "3", "4", "5"), first="How would you rate (1 = poor, 5 = excellent)"),
        area("What did you like most about working here?", 40),
        area("What could we do better?", 40),
        yesno(["Would you recommend us as an employer?", "Would you consider returning in the future?"]),
        area("Other comments", 30),
    ],
    name="Exit Interview Form", short="Exit Interview",
    about="An exit interview questionnaire to learn why employees leave, with rated questions, open feedback and rehire interest.",
    tags=["exit interview", "exit survey", "offboarding form", "employee feedback",
          "resignation form", "hr form", "leaving survey"],
    price=2.95,
)

add(
    slug="offboarding-checklist",
    title="Employee Offboarding Checklist",
    meta=["Employee", "Last Day", "Manager"],
    body=[
        options("Type:", ["Resignation", "Termination", "Layoff", "Retirement", "End of contract"]),
        groups({
            "Notice & Paperwork": ["Resignation / termination letter on file", "Notice period confirmed",
                                   "Exit interview scheduled", "Final schedule set"],
            "Pay": ["Final hours and overtime", "Outstanding vacation pay", "Pay in lieu of notice (if any)",
                    "Expense claims settled", "Record of Employment (ROE) issued", "T4 mailing address confirmed"],
            "Company Property": ["Keys / access cards", "Laptop, phone and chargers", "Uniforms and PPE",
                                 "Tools and equipment", "Company vehicle / fuel card", "Documents and files"],
            "Access & Systems": ["Email and accounts disabled", "Passwords and shared logins changed",
                                 "Alarm codes changed", "Removed from payroll and benefits",
                                 "Website / directory updated", "Clients and team informed"],
        }),
        area("Notes", 50),
        signatures(["Employee", "Manager"]),
    ],
    name="Employee Offboarding Checklist", short="Offboarding Checklist",
    about="A 22-step offboarding checklist for Canadian employers covering final pay, vacation pay, the Record of Employment, company property and system access.",
    tags=["offboarding checklist", "exit checklist", "employee leaving", "termination form",
          "hr checklist", "roe checklist", "resignation form"],
    price=2.95,
)

add(
    slug="training-record",
    title="Employee Training Record",
    meta=["Employee", "Position", "Start Date"],
    body=[
        fill_table([("Date", 1.1), ("Training / Course", 3.4), ("Provider / Trainer", 2), ("Hours", 0.8),
                    ("Certificate No.", 1.4), ("Expiry", 1.1), ("Employee Initials", 1.3)]),
        para("Common Canadian workplace training: WHMIS, first aid / CPR, health & safety orientation, working at heights, "
             "food handler, forklift, fire extinguisher, workplace harassment and violence prevention.", "s"),
        signatures(["Employee", "Supervisor"]),
    ],
    name="Employee Training Record", short="Training Log",
    about="A training record that tracks every course, trainer, hours, certificate number and expiry date for each employee.",
    tags=["training record", "training log", "employee training", "certification log",
          "whmis training", "safety training", "hr form"],
    price=2.95,
)

add(
    slug="payroll-register",
    title="Payroll Register",
    subtitle="Pay period summary  ·  Amounts in Canadian dollars",
    meta=["Pay Period", "Pay Date"],
    body=[
        fill_table([("Employee", 2.2), ("Hours", 0.8), ("Gross Pay", 1.1), ("Vacation Pay", 1.1), ("CPP / QPP", 1.1),
                    ("EI / QPIP", 1), ("Income Tax", 1.1), ("Other Ded.", 1), ("Net Pay", 1.1)], rh=20),
        table([("Total Gross", 1), ("Total CPP / QPP", 1), ("Total EI / QPIP", 1), ("Total Tax", 1),
               ("Employer CPP", 1), ("Employer EI", 1), ("Total Remittance", 1)], rows=1, rh=22),
        fields([("Remittance Due Date", 1), ("Date Remitted", 1), ("Confirmation No.", 1.4)]),
        signatures(["Prepared By", "Approved By"]),
    ],
    name="Payroll Register", short="Payroll Register",
    about="A payroll register for Canadian small businesses with columns for gross pay, vacation pay, CPP/QPP, EI/QPIP and income tax, plus an employer remittance summary.",
    tags=["payroll register", "payroll log", "cpp ei", "payroll summary", "payroll tracker",
          "source deductions", "canadian payroll"],
    canada="Built for Canadian payroll: CPP/QPP, EI/QPIP and income tax columns, employer CPP/EI share and a source-deduction remittance summary.",
    cat="finance",
    price=3.45,
)

add(
    slug="tip-distribution-log",
    title="Tip Distribution Log",
    subtitle="Tip pool / tip-out record  ·  Amounts in Canadian dollars",
    meta=["Date", "Shift", "Location"],
    body=[
        fields([("Total Cash Tips", 1), ("Total Card Tips", 1), ("Total Tip Pool", 1), ("Distribution Method", 1.6)]),
        fill_table([("Employee", 2.4), ("Position", 1.6), ("Hours Worked", 1.1), ("Share / Points", 1.1),
                    ("Tip Amount", 1.2), ("Paid By", 1.2), ("Employee Signature", 2)], rh=20),
        para("Several provinces have rules about tips and gratuities (for example, managers sharing in tips). "
             "Check your provincial employment standards.", "s"),
        signatures(["Prepared By", "Verified By"]),
    ],
    name="Tip Distribution Log", short="Tip Log",
    about="A tip pool and tip-out record for restaurants, bars, salons and cafes with hours, shares, amounts and employee sign-off.",
    tags=["tip log", "tip pool", "tip out sheet", "gratuity log", "restaurant form",
          "server tips", "bar staff form"],
    cat="food",
    price=2.95,
)
