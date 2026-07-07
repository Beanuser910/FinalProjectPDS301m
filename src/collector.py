"""
Feature 1 — Web Page Collector.

Downloads the BeautifulSoup documentation page using `requests`
and saves the raw HTML to data/raw/beautifulsoup_doc.html.
"""

import os
from pathlib import Path

import requests


TARGET_URL = "https://www.crummy.com/software/BeautifulSoup/bs4/doc/"
RAW_HTML_PATH = Path("data/raw/beautifulsoup_doc.html")


def download_page(url: str = TARGET_URL, timeout: int = 20) -> str:
    """Send an HTTP GET request and return the response text."""
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text


def save_raw_html(text: str, path: Path | str = RAW_HTML_PATH) -> None:
    """Write raw HTML text to a file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def collect(raw_path: Path | str = RAW_HTML_PATH) -> str:
    """
    High-level entry point: download and save the documentation page.

    Returns
    -------
    str
        The raw HTML content.

    Raises
    ------
    Exception
        If the HTTP response status code is not 200.
    """
    print(f"Downloading: {TARGET_URL}")
    html = download_page(TARGET_URL)
    save_raw_html(html, raw_path)
    print(f"Raw HTML saved to: {raw_path}  ({len(html):,} characters)")
    return html


if __name__ == "__main__":
    collect()
