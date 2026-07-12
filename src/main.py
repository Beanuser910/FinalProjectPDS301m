"""
Main entry point — BeautifulSoup Documentation Analytics System.

Orchestrates Features 1-6 in sequence:
  1. Web Page Collector  (collector.py)
  2. HTML Parser        (parser.py)
  3. Section Extractor  (extractor.py)
  4. Link Extractor     (extractor.py)
  5. Code Example Extr  (extractor.py)
  6. Doc Analytics      (analyzer.py)

Usage
-----
    python src/main.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src import collector, parser, extractor, analyzer


def main() -> None:
    print("\n" + "=" * 60)
    print("  BeautifulSoup Documentation Analytics System - Main Pipeline")
    print("=" * 60)

    # ── Feature 1: Web Page Collector ─────────────────────────────
    print("\n[Feature 1] Web Page Collector")
    html = collector.collect()

    # ── Feature 2: HTML Parser ────────────────────────────────────
    print("\n[Feature 2] HTML Parser")
    soup = parser.parse_html(html)
    print("  Parsed HTML successfully.")

    # ── Features 3, 4, 5: Extractors ───────────────────────────────
    print("\n[Features 3, 4, 5] Data Extractors (Sections, Links, Code Examples)")
    extractor.extract(soup)

    # ── Feature 6: Documentation Analytics ─────────────────────────
    print("\n[Feature 6] Documentation Analytics")
    analytics_results = analyzer.analyze()

    print("\n" + "=" * 60)
    print("  All features (1-6) executed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()


