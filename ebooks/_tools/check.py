#!/usr/bin/env python3
"""Quality checks for the ebooks. Run:  python3 _tools/check.py [folder ...]

Checks each book.md and listing.md for:
  * US spellings that should be Canadian (errors)
  * outcome-promise language (errors)
  * statistic-like phrasing that must be reviewed by a human (warnings)
  * presence of a "not legal/tax advice" style notice in the body (warning)
  * listing.md fields: title, subtitle, ~150-word description, price, 5 tags
  * PDF page count between 15 and 25 (if pdf/<folder>.pdf exists and pdfinfo is installed)
Exit code 1 if any error is found.
"""
import re, sys, subprocess, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

US_TO_CA = {
    r"\bcolor(s|ed|ing|ful)?\b": "colour",
    r"\bfavor(s|ed|ing|ite|ites|able)?\b": "favour",
    r"\bhonor(s|ed|ing)?\b": "honour",
    r"\blabor(s|ed|ing)?\b": "labour",
    r"\bbehavior(s|al)?\b": "behaviour",
    r"\bneighbor(s|hood|hoods|ing)?\b": "neighbour",
    r"\bcenter(s|ed)?\b": "centre",
    r"\bmeter(s)?\b": "metre",
    r"\btheater(s)?\b": "theatre",
    r"\bcatalog(s|ed)?\b": "catalogue",
    r"\bdialog(s)?\b": "dialogue",
    r"\bdefense\b": "defence",
    r"\boffense\b": "offence",
    r"\btraveled|traveling|traveler(s)?\b": "travelled/travelling/traveller",
    r"\bcanceled|canceling\b": "cancelled/cancelling",
    r"\blabeled|labeling\b": "labelled/labelling",
    r"\bmodeled|modeling\b": "modelled/modelling",
    r"\bfueled|fueling\b": "fuelled/fuelling",
    r"\benrollment|enroll(s|ed)?\b": "enrolment/enrol",
    r"\bfulfill(s|ment)?\b": "fulfil/fulfilment",
    r"\bjudgment\b": "judgement",
    r"\bpaycheck(s)?\b": "pay cheque",
    r"\bcheckbook(s)?\b": "chequebook",
    r"\bcheck(s)? (payment|deposit)": "cheque",
    r"\bpay(ing)? by check\b": "cheque",
    r"\bwrite (a|the) check\b": "cheque",
    r"\bprogram(me)? license\b|\b(a|your|business|the) license\b": "licence (noun)",
    r"\bpractice(s|d)? (your|the|it|this|saying|answering)\b": "practise (verb)",
    r"\banalyze|analyzed|analyzing\b": "analyse",
    r"\bgray\b": "grey",
    r"\bjewelry\b": "jewellery",
    r"\bmom\b": "mom is fine in Canada; check context",
    r"\bzip code(s)?\b": "postal code",
    r"\bstate tax\b|\bsales tax permit\b|\bIRS\b|\bSSN\b|\bW-2\b|\b1099\b|\bLLC\b": "US term",
    r"\$\d[\d,]*\.\d\d\s*USD": "USD amount",
}
# 'mom' is fine; remove from errors
US_TO_CA.pop(r"\bmom\b")

PROMISE = [
    r"\bguarantee(d|s)?\b", r"\bwill (double|triple|skyrocket|explode|boost)\b",
    r"\b(increase|grow|boost) (your )?(revenue|sales|profits?|income) by\b",
    r"\bproven (to|method|system|strategy)\b", r"\bin (just )?\d+ days\b",
    r"\bget rich\b", r"\bsix[- ]figure", r"\bnever (lose|miss) (a|another)\b",
    r"\b10x\b", r"\bsecret(s)? (to|that)\b", r"\bfoolproof\b", r"\brisk[- ]free\b",
]
STATLIKE = [
    r"\b\d{1,3}(\.\d+)?\s?%(?! HST| GST)", r"\bstud(y|ies) (show|find|found|suggest)",
    r"\bresearch (shows|finds|found|suggests)\b", r"\bsurvey(s|ed)?\b",
    r"\bstatistic(s|ally)?\b", r"\bmost (customers|consumers|people|shoppers|businesses)\b",
    r"\b\d+ (out of|in) \d+\b", r"\bon average\b", r"\bpercent\b",
]
NOTICE = re.compile(r"not (legal|tax|accounting|financial)[^.]{0,40}advice|general information", re.I)

def strip_code(text):
    return re.sub(r"`[^`]*`", "", text)

def scan(path, text, errors, warnings, check_stats=True):
    body = strip_code(text)
    for i, line in enumerate(body.splitlines(), 1):
        if line.strip().startswith("<!--"):
            continue
        for pat, fix in US_TO_CA.items():
            for m in re.finditer(pat, line, re.I):
                errors.append(f"{path}:{i}: spelling '{m.group(0)}' -> {fix}")
        for pat in PROMISE:
            for m in re.finditer(pat, line, re.I):
                errors.append(f"{path}:{i}: promise-like wording '{m.group(0)}'")
        if check_stats:
            for pat in STATLIKE:
                for m in re.finditer(pat, line, re.I):
                    warnings.append(f"{path}:{i}: review stat-like wording '{m.group(0)}': {line.strip()[:90]}")

def check_listing(folder, errors, warnings):
    p = folder / "listing.md"
    if not p.exists():
        errors.append(f"{p}: missing")
        return
    text = p.read_text()
    scan(p.relative_to(ROOT), text, errors, warnings, check_stats=True)
    for field in ["## Title", "## Subtitle", "## Description", "## Suggested price", "## Tags"]:
        if field.lower() not in text.lower():
            errors.append(f"{p.relative_to(ROOT)}: missing section '{field}'")
    m = re.search(r"## Description\s*\n(.*?)(\n## |\Z)", text, re.S | re.I)
    if m:
        words = len(re.findall(r"[A-Za-z0-9’'$%.-]+", m.group(1)))
        if not 140 <= words <= 160:
            errors.append(f"{p.relative_to(ROOT)}: description is {words} words (want ~150, 140-160)")
    m = re.search(r"## Tags\s*\n(.*?)(\n## |\Z)", text, re.S | re.I)
    if m:
        tags = [t for t in re.findall(r"^\s*[-*]\s+(.+)$", m.group(1), re.M)]
        if len(tags) != 5:
            errors.append(f"{p.relative_to(ROOT)}: {len(tags)} tags (want 5)")

def pdf_pages(folder):
    pdf = ROOT / "pdf" / f"{folder.name}.pdf"
    if not pdf.exists():
        return None
    try:
        out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
        return int(re.search(r"Pages:\s+(\d+)", out).group(1))
    except Exception:
        return None

def main():
    names = sys.argv[1:] or sorted(p.name for p in ROOT.glob("[0-9][0-9]-*") if p.is_dir())
    total_err = 0
    for name in names:
        folder = ROOT / name.rstrip("/")
        errors, warnings = [], []
        book = folder / "book.md"
        if not book.exists():
            print(f"== {name}: no book.md")
            continue
        text = book.read_text()
        body = text.split("---", 2)[2] if text.startswith("---") else text
        words = len(re.findall(r"\b\w[\w’'-]*\b", body))
        scan(book.relative_to(ROOT), text, errors, warnings)
        if not NOTICE.search(body):
            warnings.append(f"{book.relative_to(ROOT)}: no 'not legal/tax advice' / 'general information' notice in body")
        check_listing(folder, errors, warnings)
        pages = pdf_pages(folder)
        if pages is not None and not 15 <= pages <= 25:
            errors.append(f"pdf/{name}.pdf: {pages} pages (want 15-25)")
        print(f"== {name}: {words} words, {pages if pages is not None else '?'} pages, "
              f"{len(errors)} errors, {len(warnings)} to review")
        for e in errors: print("  ERROR  ", e)
        for w in warnings: print("  review ", w)
        total_err += len(errors)
    sys.exit(1 if total_err else 0)

if __name__ == "__main__":
    main()
