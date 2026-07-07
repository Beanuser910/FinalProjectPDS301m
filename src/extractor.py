"""
Feature 3 — Section Extractor.

Extract all documentation sections, compute per-section metadata
(word count, code block count, link count), and save to sections.csv.
"""

import re
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup


HEADING_TAGS = ["h1", "h2", "h3"]
PROCESSED_DIR = Path("data/processed")


def clean_text(text: str | None) -> str:
    """Collapse extra whitespace and newlines into single spaces."""
    if text is None:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def get_content_until_next_heading(heading: BeautifulSoup) -> list:
    """Collect all sibling elements after a heading until the next heading."""
    content = []
    for sibling in heading.find_next_siblings():
        if sibling.name in HEADING_TAGS:
            break
        content.append(sibling)
    return content


def extract_sections(soup: BeautifulSoup) -> pd.DataFrame:
    """
    Extract all documentation sections and their metadata.

    Returns
    -------
    pd.DataFrame
        Columns: section_id, section_level, section_title,
                 section_text, word_count, code_block_count, link_count
    """
    headings = soup.find_all(HEADING_TAGS)
    rows = []

    for idx, heading in enumerate(headings, start=1):
        section_title = clean_text(heading.get_text(" ", strip=True))
        section_level = heading.name
        elements = get_content_until_next_heading(heading)

        text_parts = []
        code_count = 0
        link_count = 0

        for el in elements:
            text_parts.append(clean_text(el.get_text(" ", strip=True)))
            code_count += len(el.find_all(["pre", "code"]))
            link_count += len(el.find_all("a"))

        section_text = clean_text(" ".join(text_parts))

        rows.append({
            "section_id": idx,
            "section_level": section_level,
            "section_title": section_title,
            "section_text": section_text,
            "word_count": len(section_text.split()),
            "code_block_count": code_count,
            "link_count": link_count,
        })

    return pd.DataFrame(rows)


def save_sections(df: pd.DataFrame, path: Path | str | None = None) -> Path:
    """Save sections DataFrame to CSV."""
    path = Path(path) if path else PROCESSED_DIR / "sections.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    return path


def extract(soup: BeautifulSoup) -> pd.DataFrame:
    """
    High-level entry point for Feature 3.

    Returns
    -------
    pd.DataFrame
    """
    sections_df = extract_sections(soup)
    path = save_sections(sections_df)
    print(f"Sections saved: {path}  ({len(sections_df)} rows)")
    return sections_df


if __name__ == "__main__":
    from src.parser import parse
    soup = parse()
    extract(soup)
