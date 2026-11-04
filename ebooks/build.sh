#!/usr/bin/env bash
# Build the ebooks from Markdown to PDF.
#
#   ./build.sh                  build every book
#   ./build.sh 05-hst-basics    build one book (folder name)
#
# Needs: pandoc (2.19+), Node.js (18+), and Playwright with Chromium
#   (npm install playwright && npx playwright install chromium)
# Output: pdf/<folder-name>.pdf
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS="$ROOT/_tools"
BUILD="$ROOT/_build"
OUT="$ROOT/pdf"
mkdir -p "$BUILD" "$OUT"

if [ "$#" -gt 0 ]; then
  BOOKS=("$@")
else
  BOOKS=()
  for d in "$ROOT"/[0-9][0-9]-*/; do BOOKS+=("$(basename "$d")"); done
fi

for book in "${BOOKS[@]}"; do
  book="${book%/}"
  src="$ROOT/$book/book.md"
  if [ ! -f "$src" ]; then
    echo "skip: $book (no book.md)"
    continue
  fi
  html="$BUILD/$book.html"
  pdf="$OUT/$book.pdf"

  pandoc "$src" \
    --from markdown+task_lists+fenced_divs+pipe_tables+smart \
    --to html5 \
    --standalone \
    --template "$TOOLS/template.html" \
    --css "$TOOLS/book.css" \
    --toc --toc-depth=2 \
    --metadata lang=en-CA \
    --output "$html"

  node "$TOOLS/print-pdf.js" "$html" "$pdf"

  pages="?"
  if command -v pdfinfo >/dev/null 2>&1; then
    pages="$(pdfinfo "$pdf" | awk '/^Pages:/ {print $2}')"
  fi
  printf '%-30s %3s pages  ->  %s\n' "$book" "$pages" "${pdf#$ROOT/}"
done
