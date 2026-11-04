"""Build the PDFs and listings.csv.

    python3 build.py            # builds every forms_N.py batch that exists
"""

import csv
import importlib
import os

from engine import build
from listings import listing

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "forms")
BATCHES = 6


def all_forms():
    n = 0
    for b in range(1, BATCHES + 1):
        try:
            mod = importlib.import_module(f"forms_{b}")
        except ModuleNotFoundError:
            continue
        for f in mod.FORMS:
            n += 1
            yield n, b, f


def main():
    os.makedirs(OUT, exist_ok=True)
    rows, slugs = [], set()
    for n, b, f in all_forms():
        assert f["slug"] not in slugs, f["slug"]
        slugs.add(f["slug"])
        fname = f"{n:03d}-{f['slug']}.pdf"
        pages = build(os.path.join(OUT, fname), f)
        print(f"{fname}  ({pages} page{'s' if pages > 1 else ''})")
        rows.append(listing(f, fname))
    with open(os.path.join(ROOT, "listings.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["file", "title", "description", "tags", "price"])
        for r in rows:
            w.writerow([r["file"], r["title"], r["description"], ",".join(r["tags"]), f"{r['price']:.2f}"])
    print(f"{len(rows)} listings written")


if __name__ == "__main__":
    main()
