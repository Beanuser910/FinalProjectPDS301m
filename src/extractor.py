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
    """Collapse extra whitespace and remove special characters."""
    if text is None:
        return ""
    text = re.sub(r"\s+", " ", text)
    # Remove pilcrow sign (¶) and other special Unicode characters
    text = re.sub(r"[\u00b6\u00a7\u00b2\u00b3\u00bc-\u00be\u00a0]", "", text)
    return text.strip()


def get_closest_section_title(element: BeautifulSoup) -> str:
    """Find the nearest preceding heading to determine the current section title."""
    heading = element.find_previous(HEADING_TAGS)
    return clean_text(heading.get_text(" ", strip=True)) if heading else "Unknown"


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


def extract_links(soup: BeautifulSoup) -> pd.DataFrame:
    """
    Extract all hyperlinks and classify them based on business rules.

    Returns
    -------
    pd.DataFrame
        Columns: link_text, href, link_type, section_title
    """
    rows = []
    for a_tag in soup.find_all("a"):
        href = a_tag.get("href", "").strip()
        link_text = clean_text(a_tag.get_text())
        section_title = get_closest_section_title(a_tag)

        # Apply classification rules
        if not href or href == "#" or href.startswith("javascript:"):
            link_type = "empty_or_invalid"
        elif href.startswith("#"):
            link_type = "internal_anchor"
        elif any(href.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif", ".svg"]):
            link_type = "image_link"
        elif href.startswith(("http://", "https://", "www.")):
            if "beautifulsoup" in href.lower() or "bs4" in href.lower():
                link_type = "documentation_link"
            else:
                link_type = "external_link"
        else:
            link_type = "documentation_link"

        rows.append({
            "link_text": link_text,
            "href": href,
            "link_type": link_type,
            "section_title": section_title
        })

    return pd.DataFrame(rows)


def save_links(df: pd.DataFrame, path: Path | str | None = None) -> Path:
    """Save links DataFrame to CSV."""
    path = Path(path) if path else PROCESSED_DIR / "links.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    return path


def extract_code_examples(soup: BeautifulSoup) -> pd.DataFrame:
    """
    Extract all Python code examples from the documentation.

    Returns
    -------
    pd.DataFrame
        Columns: example_id, section_title, code_text, line_count,
                 contains_find_all, contains_find, contains_select, 
                 contains_get_text, contains_requests
    """
    rows = []
    code_blocks = soup.find_all("pre")
    
    for idx, block in enumerate(code_blocks, start=1):
        code_text = block.get_text()
        if not code_text.strip():
            continue

        section_title = get_closest_section_title(block)
        line_count = len(code_text.strip().split("\n"))

        rows.append({
            "example_id": f"ex_{idx}",
            "section_title": section_title,
            "code_text": code_text.strip(),
            "line_count": line_count,
            "contains_find_all": "find_all" in code_text,
            "contains_find": "find(" in code_text or ".find " in code_text,
            "contains_select": "select" in code_text,
            "contains_get_text": "get_text" in code_text,
            "contains_requests": "requests" in code_text
        })

    return pd.DataFrame(rows)


def save_code_examples(df: pd.DataFrame, path: Path | str | None = None) -> Path:
    """Save code examples DataFrame to CSV."""
    path = Path(path) if path else PROCESSED_DIR / "code_examples.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    return path


def extract(soup: BeautifulSoup) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    High-level entry point: Runs all feature extractors and saves outputs to CSVs.

    Returns
    -------
    tuple of pd.DataFrame
        (links_df, code_df, sections_df)
    """
    # 1. Links Pipeline
    links_df = extract_links(soup)
    links_path = save_links(links_df)
    print(f"Links saved: {links_path}  ({len(links_df)} rows)")

    # 2. Code Examples Pipeline
    code_df = extract_code_examples(soup)
    code_path = save_code_examples(code_df)
    print(f"Code examples saved: {code_path}  ({len(code_df)} rows)")

    # 3. Sections Pipeline
    sections_df = extract_sections(soup)
    sections_path = save_sections(sections_df)
    print(f"Sections saved: {sections_path}  ({len(sections_df)} rows)")

    return links_df, code_df, sections_df


if __name__ == "__main__":
    from src.parser import parse
    soup = parse()
    extract(soup)
