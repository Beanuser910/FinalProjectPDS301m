"""
Main entry point — Thành viên 1: HTML Collector & Section Extractor.

Orchestrates Features 1, 2, 3 in sequence:
  1. Web Page Collector  (collector.py)
  2. HTML Parser        (parser.py)
  3. Section Extractor  (extractor.py)

Usage
-----
    python src/main.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src import collector, parser, extractor


def main() -> None:
    print("\n" + "=" * 55)
    print("  Thành viên 1: HTML Collector & Section Extractor")
    print("=" * 55)

    # ── Feature 1: Web Page Collector ─────────────────────────────
    print("\n[Feature 1] Web Page Collector")
    html = collector.collect()

    # ── Feature 2: HTML Parser ────────────────────────────────────
    print("\n[Feature 2] HTML Parser")
    soup = parser.parse_html(html)
    print("  Parsed successfully.")

    # ── Feature 3: Section Extractor ───────────────────────────────
    print("\n[Feature 3] Section Extractor")
    extractor.extract(soup)

    print("\n" + "=" * 55)
    print("  All features completed.")
    print("=" * 55)


if __name__ == "__main__":
    main()
