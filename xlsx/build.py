"""Build every template into ./templates.

    python3 build.py            # build all
    python3 build.py 03 07      # build only templates whose file name starts with 03 or 07
"""

import json
import sys
from pathlib import Path

from generator import REGISTRY

HERE = Path(__file__).resolve().parent
OUT = HERE / "templates"


def build(out_dir=OUT, only=None):
    out_dir.mkdir(parents=True, exist_ok=True)
    results = {}
    for slug, fn, _desc in REGISTRY:
        if only and not any(slug.startswith(o) for o in only):
            continue
        path = out_dir / f"{slug}.xlsx"
        checks = fn(str(path))
        results[slug] = checks
        print(f"built {path.name}")
    return results


if __name__ == "__main__":
    build(only=sys.argv[1:] or None)
