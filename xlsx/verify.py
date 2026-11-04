"""Verify every template.

1. Builds each template into a temp folder.
2. Recalculates all formulas with LibreOffice (headless).
3. Fails if any formula returns an error (#VALUE!, #REF!, #NAME?, #DIV/0!, #N/A ...).
4. Compares key cells against values computed independently in Python from the sample data.
5. Checks structure: Instructions tab first, every sheet protected, every formula cell locked,
   every yellow input cell unlocked.

    python3 verify.py           # needs LibreOffice (soffice) on PATH
"""

import datetime as dt
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from openpyxl import load_workbook

from build import build

ERRORS = ("#VALUE!", "#REF!", "#NAME?", "#DIV/0!", "#N/A", "#NUM!", "#NULL!", "Err:")
INPUT_FILL = "00FFF2CC"


def recalc(src_dir, out_dir):
    files = sorted(str(p) for p in Path(src_dir).glob("*.xlsx"))
    profile = Path(tempfile.mkdtemp()) / "lo-profile"
    cmd = ["soffice", f"-env:UserInstallation=file://{profile}", "--headless", "--calc",
           "--convert-to", "xlsx", "--outdir", str(out_dir)] + files
    subprocess.run(cmd, check=True, capture_output=True, timeout=600)


def norm(v):
    if isinstance(v, dt.datetime):
        return v.date()
    return v


def close(a, b):
    a, b = norm(a), norm(b)
    if isinstance(b, (int, float)) and not isinstance(b, bool):
        return isinstance(a, (int, float)) and abs(a - b) <= max(0.01, abs(b) * 1e-9)
    return a == b


def structure(path):
    problems = []
    wb = load_workbook(path)
    if wb.sheetnames[0] != "Instructions":
        problems.append("first tab is not Instructions")
    n_formula = n_input = 0
    for ws in wb.worksheets:
        if not ws.protection.sheet:
            problems.append(f"{ws.title}: not protected")
        for row in ws.iter_rows():
            for c in row:
                is_formula = isinstance(c.value, str) and c.value.startswith("=")
                is_input = c.fill is not None and c.fill.fgColor is not None and c.fill.fgColor.rgb == INPUT_FILL
                if is_input:
                    n_input += 1
                    if c.protection.locked and ws.title != "Instructions":
                        problems.append(f"{ws.title}!{c.coordinate}: input cell is locked")
                elif is_formula:
                    n_formula += 1
                    if not c.protection.locked:
                        problems.append(f"{ws.title}!{c.coordinate}: formula cell is unlocked")
    return problems, n_formula, n_input


def main():
    tmp = Path(tempfile.mkdtemp())
    src, out = tmp / "src", tmp / "out"
    out.mkdir()
    print("Building templates...")
    checks = build(src)
    print("Recalculating with LibreOffice...")
    recalc(src, out)
    failures = 0
    total_formulas = 0
    for slug, cks in checks.items():
        msgs = []
        sp, nf, ni = structure(src / f"{slug}.xlsx")
        msgs += sp
        total_formulas += nf
        calc_path = out / f"{slug}.xlsx"
        if not calc_path.exists():
            msgs.append("LibreOffice did not produce a recalculated file")
        else:
            wbv = load_workbook(calc_path, data_only=True)
            wbf = load_workbook(src / f"{slug}.xlsx")
            errs = []
            for ws in wbf.worksheets:
                wv = wbv[ws.title]
                for row in ws.iter_rows():
                    for c in row:
                        if isinstance(c.value, str) and c.value.startswith("="):
                            v = wv[c.coordinate].value
                            if isinstance(v, str) and v.startswith(ERRORS):
                                errs.append(f"{ws.title}!{c.coordinate}={v}")
            if errs:
                msgs.append(f"{len(errs)} formula errors, e.g. {errs[:5]}")
            for sheet, cell, expected in cks:
                got = wbv[sheet][cell].value
                if isinstance(expected, tuple) and expected[0] == "=":
                    expected = wbv[expected[1]][expected[2]].value
                if not close(got, expected):
                    msgs.append(f"{sheet}!{cell}: expected {expected!r}, got {got!r}")
        status = "OK  " if not msgs else "FAIL"
        print(f"{status} {slug:32s} formulas={nf:5d} inputs={ni:5d} checks={len(cks)}")
        for m in msgs:
            print(f"       - {m}")
        failures += bool(msgs)
    print(f"\n{len(checks) - failures}/{len(checks)} templates passed; {total_formulas} formulas verified.")
    shutil.rmtree(tmp, ignore_errors=True)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
