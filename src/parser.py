"""
Feature 2 — HTML Parser.

Reads the saved HTML file and parses it using BeautifulSoup.
"""

from pathlib import Path

from bs4 import BeautifulSoup


def load_html(path: Path | str) -> str:
    """Read raw HTML from a file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_html(html: str, parser: str = "html.parser") -> BeautifulSoup:
    """
    Parse HTML text into a BeautifulSoup object.

    Parameters
    ----------
    html : str
        Raw HTML content.
    parser : str, optional
        Parser to use. Options: "html.parser", "lxml", "html5lib".
        Default is Python's built-in "html.parser".

    Returns
    -------
    BeautifulSoup
    """
    return BeautifulSoup(html, parser)


def get_page_title(soup: BeautifulSoup) -> str:
    """Extract the page title from the soup object."""
    return soup.title.get_text(strip=True) if soup.title else "No title found"


def parse(raw_path: Path | str = "data/raw/beautifulsoup_doc.html") -> BeautifulSoup:
    """
    High-level entry point: load HTML and return a parsed soup.

    Returns
    -------
    BeautifulSoup
    """
    path = Path(raw_path)
    print(f"Loading HTML from: {path}")
    html = load_html(path)
    soup = parse_html(html)
    print(f"Page title: {get_page_title(soup)}")
    return soup


if __name__ == "__main__":
    soup = parse()
    print(f"Parsed successfully.")
