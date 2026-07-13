"""
Feature 8 — Final Report Generator.

Generates a comprehensive final analytical report in Markdown and
styled HTML, including:
  - Dataset overview
  - Scraping method
  - Extracted data summary
  - Analysis results
  - Charts (embedded images)
  - Key findings
  - Limitations
  - Conclusion
"""

import base64
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.analyzer import load_data, get_top_keywords

PROCESSED_DIR = Path("data/processed")
CHARTS_DIR = Path("output/charts")
OUTPUT_DIR = Path("output")

SECTIONS_CSV = PROCESSED_DIR / "sections.csv"
LINKS_CSV = PROCESSED_DIR / "links.csv"
CODE_EXAMPLES_CSV = PROCESSED_DIR / "code_examples.csv"

TARGET_URL = "https://www.crummy.com/software/BeautifulSoup/bs4/doc/"


def _img_to_base64(path: Path) -> str:
    """Read an image file and return its base64-encoded string."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _build_markdown(results: dict, chart_paths: list[Path]) -> str:
    """Build the full Markdown report content."""
    df_sections, df_links, df_code = load_data()

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ── Dataset Overview ──
    md = f"""# BeautifulSoup Documentation Analytics — Final Report

**Generated:** {now}
**Target URL:** {TARGET_URL}

---

## 1. Dataset Overview

| Dataset | File | Rows | Columns |
|---------|------|------|---------|
| Sections | `data/processed/sections.csv` | {len(df_sections)} | {len(df_sections.columns)} |
| Links | `data/processed/links.csv` | {len(df_links)} | {len(df_links.columns)} |
| Code Examples | `data/processed/code_examples.csv` | {len(df_code)} | {len(df_code.columns)} |

**Section columns:** {", ".join(df_sections.columns)}
**Link columns:** {", ".join(df_links.columns)}
**Code example columns:** {", ".join(df_code.columns)}

---

## 2. Scraping Method

The system uses the following Python libraries to collect and parse the
BeautifulSoup documentation:

1. **`requests`** — Sends an HTTP GET request to the target URL and
   retrieves the raw HTML content. The response status code is checked
   via `raise_for_status()` to ensure a successful download.
2. **`BeautifulSoup4`** — Parses the raw HTML into a navigable DOM tree
   using Python's built-in `html.parser`.
3. **`pandas`** — Structures the extracted data into DataFrames and
   exports them to CSV files for downstream analysis.
4. **`numpy`** — Supports numerical operations during analytics.
5. **`matplotlib`** — Generates the data visualization charts.

**Pipeline flow:**

```
Download HTML → Parse with BeautifulSoup → Extract Sections / Links / Code
→ Save to CSV → Analyze with Pandas+NumPy → Visualize → Generate Report
```

---

## 3. Extracted Data Summary

### 3.1 Sections

| Metric | Value |
|--------|-------|
| Total sections | {results['q1_total_sections']} |
| Section levels | {", ".join(df_sections['section_level'].unique())} |
| Average word count | {df_sections['word_count'].mean():.1f} |
| Total code blocks | {df_sections['code_block_count'].sum()} |
| Total links in sections | {df_sections['link_count'].sum()} |

### 3.2 Links

| Link Type | Count |
|-----------|-------|
"""

    q6 = results["q6_link_counts"]
    for ltype, count in q6.items():
        md += f"| {ltype} | {count} |\n"

    md += f"""
### 3.3 Code Examples

| Metric | Value |
|--------|-------|
| Total code examples | {len(df_code)} |
| Average line count | {df_code['line_count'].mean():.2f} |
| Max line count | {df_code['line_count'].max()} |
| Examples using `find_all()` | {results['q7_find_all_count']} |
| Examples using `get_text()` | {results['q8_get_text_count']} |

---

## 4. Analysis Results

### 4.1 Required Questions

| # | Question | Answer |
|---|----------|--------|
| Q1 | How many sections are in the documentation? | {results['q1_total_sections']} |
| Q2 | Which section has the highest word count? | "{results['q2_max_word_section']['title']}" ({results['q2_max_word_section']['word_count']} words) |
| Q3 | Which section contains the most code examples? | "{results['q3_max_code_section']['title']}" ({results['q3_max_code_section']['code_block_count']} blocks) |
| Q4 | Which section contains the most links? | "{results['q4_max_link_section']['title']}" ({results['q4_max_link_section']['link_count']} links) |
| Q6 | How many internal and external links? | Internal: {q6['internal_anchor']}, Doc: {q6['documentation_link']}, External: {q6['external_link']} |
| Q7 | Code examples using `find_all()`? | {results['q7_find_all_count']} |
| Q8 | Code examples using `get_text()`? | {results['q8_get_text_count']} |

### 4.2 Top 10 Technical Keywords (Q5)

| Rank | Keyword | Frequency |
|------|---------|-----------|
"""
    for i, (word, count) in enumerate(results["q5_top_10_keywords"], start=1):
        md += f"| {i} | {word} | {count} |\n"

    q9 = results["q9_code_line_stats"]
    md += f"""
### 4.3 Additional Questions

**Q9: Code line statistics**
- Average lines per code example: {q9['average_line_count']:.2f}
- Longest code example: "{q9['longest_example_section']}" ({q9['longest_example_lines']} lines)

**Q10: Statistics by heading level**

| Level | Avg Word Count | Avg Code Blocks | Avg Links |
|-------|---------------|-----------------|-----------|
"""
    q10 = results["q10_level_statistics"]
    # q10 comes from a MultiIndex DataFrame .to_dict() — keys are tuples like
    # ("word_count", "mean"). Handle both tuple-key and nested-dict formats.
    def _get(metric: str, agg: str) -> dict:
        if (metric, agg) in q10:
            return q10[(metric, agg)]
        if metric in q10 and isinstance(q10[metric], dict) and agg in q10[metric]:
            return q10[metric][agg]
        return {}

    wc_mean = _get("word_count", "mean")
    cb_mean = _get("code_block_count", "mean")
    lc_mean = _get("link_count", "mean")
    for level in sorted(wc_mean.keys()):
        md += f"| {level.upper()} | {wc_mean[level]:.1f} | {cb_mean[level]:.1f} | {lc_mean[level]:.1f} |\n"

    # ── Charts ──
    md += """
---

## 5. Charts

The following charts were generated as part of Feature 7 (Data Visualization)
and saved to `output/charts/`.

"""
    chart_titles = [
        "Chart 1: Top 10 Sections by Word Count",
        "Chart 2: Code Examples by Section",
        "Chart 3: Link Type Distribution",
        "Chart 4: Code Example Line Count Distribution",
    ]
    for title, path in zip(chart_titles, chart_paths):
        md += f"### {title}\n\n![{title}]({path})\n\n"

    # ── Key Findings ──
    md += f"""---

## 6. Key Findings

1. The BeautifulSoup documentation contains **{results['q1_total_sections']} sections**
   across h1, h2, and h3 heading levels.
2. The section with the most content is
   **"{results['q2_max_word_section']['title']}"**
   with {results['q2_max_word_section']['word_count']} words.
3. **"{results['q3_max_code_section']['title']}"** has the most code examples
   ({results['q3_max_code_section']['code_block_count']} blocks), making it the
   most code-heavy section.
4. **"{results['q4_max_link_section']['title']}"** contains the most links
   ({results['q4_max_link_section']['link_count']}), indicating it is the most
   reference-rich section.
5. The most frequent technical keyword is
   **"{results['q5_top_10_keywords'][0][0]}"**
   ({results['q5_top_10_keywords'][0][1]} occurrences).
6. Link classification shows {q6['internal_anchor']} internal anchors,
   {q6['documentation_link']} documentation links, and {q6['external_link']}
   external links.
7. {results['q7_find_all_count']} code examples use `find_all()` and
   {results['q8_get_text_count']} use `get_text()`, confirming these are the
   most demonstrated BeautifulSoup APIs.
8. The average code example is {q9['average_line_count']:.1f} lines long,
   with the longest at {q9['longest_example_lines']} lines in
   "{q9['longest_example_section']}".

---

## 7. Limitations

1. **Single-page scope:** Only the main BeautifulSoup documentation page was
   scraped; sub-pages and linked external resources were not crawled.
2. **Parser dependency:** Results may vary slightly depending on the HTML
   parser used (`html.parser` vs `lxml` vs `html5lib`).
3. **Dynamic content:** JavaScript-rendered content is not captured by
   `requests`; only static HTML is analyzed.
4. **Keyword filtering:** Stopword list is manually curated and may not
   capture all domain-irrelevant terms.
5. **Code example detection:** Only `<pre>` blocks are treated as code
   examples; inline `<code>` snippets within paragraphs are not counted
   as separate examples.

---

## 8. Conclusion

This project successfully built an end-to-end Python data pipeline that
collects, parses, extracts, analyzes, and visualizes the BeautifulSoup
official documentation. The system leverages `requests` for web scraping,
`BeautifulSoup4` for HTML parsing, `pandas` and `numpy` for data analysis,
and `matplotlib` for visualization.

The analysis reveals that the documentation is well-structured with
{results['q1_total_sections']} sections, rich in code examples
({len(df_code)} total), and heavily cross-referenced with
{len(df_links)} links. The most frequently demonstrated APIs are
`find_all()` and `get_text()`, which aligns with BeautifulSoup's core
usage patterns.

The generated charts and this report provide a clear, reproducible summary
of the documentation's structure and content, demonstrating the team's
ability to apply data engineering techniques to real-world technical
documentation.

---

*Report generated by BeautifulSoup Documentation Analytics System.*
"""

    return md


def _markdown_to_html(md: str, chart_paths: list[Path]) -> str:
    """Convert Markdown report to a self-contained styled HTML with embedded images."""
    # Encode chart images as base64 for a self-contained HTML file
    img_map = {}
    for path in chart_paths:
        b64 = _img_to_base64(path)
        img_map[str(path)] = f"data:image/png;base64,{b64}"

    # Simple Markdown → HTML conversion (sufficient for this report)
    html_lines = []
    in_table = False
    in_code = False

    for line in md.split("\n"):
        # Code blocks
        if line.strip().startswith("```"):
            if in_code:
                html_lines.append("</code></pre>")
                in_code = False
            else:
                html_lines.append('<pre><code>')
                in_code = True
            continue
        if in_code:
            html_lines.append(line.replace("<", "&lt;").replace(">", "&gt;"))
            continue

        # Tables
        if line.strip().startswith("|"):
            if not in_table:
                html_lines.append('<table>')
                in_table = True
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if all(set(c) <= set("-: ") for c in cells):
                continue  # skip separator row
            tag = "th" if html_lines[-1] == "<table>" else "td"
            row = "<tr>" + "".join(f"<{tag}>{c}</{tag}>" for c in cells) + "</tr>"
            html_lines.append(row)
            continue
        elif in_table:
            html_lines.append("</table>")
            in_table = False

        # Headings
        if line.startswith("# "):
            html_lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("### "):
            html_lines.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("#### "):
            html_lines.append(f"<h4>{line[5:]}</h4>")
        elif line.startswith("---"):
            html_lines.append("<hr>")
        elif line.startswith("- ") or line.startswith("* "):
            content = line[2:]
            content = _inline_md(content, img_map)
            html_lines.append(f"<li>{content}</li>")
        elif line.strip() == "":
            html_lines.append("<br>")
        else:
            content = _inline_md(line, img_map)
            html_lines.append(f"<p>{content}</p>")

    if in_table:
        html_lines.append("</table>")

    body = "\n".join(html_lines)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BeautifulSoup Documentation Analytics — Final Report</title>
<style>
  body {{
    font-family: "Segoe UI", Arial, sans-serif;
    max-width: 900px;
    margin: 40px auto;
    padding: 0 20px;
    color: #333;
    line-height: 1.6;
  }}
  h1 {{
    color: #2b5c8f;
    border-bottom: 3px solid #2b5c8f;
    padding-bottom: 10px;
  }}
  h2 {{
    color: #2b6cb0;
    margin-top: 30px;
  }}
  h3 {{
    color: #2f855a;
  }}
  table {{
    border-collapse: collapse;
    width: 100%;
    margin: 15px 0;
  }}
  th, td {{
    border: 1px solid #ddd;
    padding: 8px 12px;
    text-align: left;
  }}
  th {{
    background-color: #2b5c8f;
    color: white;
  }}
  tr:nth-child(even) {{
    background-color: #f8f9fa;
  }}
  pre {{
    background: #ffffff;
    color: #333;
    padding: 15px;
    border-radius: 5px;
    overflow-x: auto;
  }}
  code {{
    background: #f0f0f0;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: Consolas, monospace;
  }}
  pre code {{
    background: none;
    padding: 0;
  }}
  img {{
    max-width: 100%;
    border: 1px solid #ddd;
    border-radius: 5px;
    margin: 10px 0;
  }}
  hr {{
    border: none;
    border-top: 2px solid #e0e0e0;
    margin: 30px 0;
  }}
  li {{
    margin: 5px 0;
  }}
</style>
</head>
<body>
{body}
</body>
</html>"""
    return html


def _inline_md(text: str, img_map: dict) -> str:
    """Convert inline Markdown (bold, code, images) to HTML."""
    import re

    # Images: ![alt](path)
    def img_repl(m):
        alt = m.group(1)
        src = m.group(2)
        real_src = img_map.get(src, src)
        return f'<img src="{real_src}" alt="{alt}">'

    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", img_repl, text)

    # Bold: **text**
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)

    # Inline code: `text`
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)

    return text


def generate_report(results: dict | None = None, chart_paths: list[Path] | None = None) -> tuple[Path, Path]:
    """
    Generate the final report in Markdown and HTML formats.

    Parameters
    ----------
    results : dict, optional
        Analytics results from analyzer.analyze(). If None, will run analyze().
    chart_paths : list of Path, optional
        Paths to chart images. If None, will look in output/charts/.

    Returns
    -------
    tuple of (Path, Path)
        Paths to the generated Markdown and HTML report files.
    """
    from src.analyzer import analyze

    if results is None:
        results = analyze()

    if chart_paths is None:
        chart_paths = sorted(CHARTS_DIR.glob("*.png"))

    if not chart_paths:
        raise FileNotFoundError(
            "No chart images found in output/charts/. Please run the visualizer first."
        )

    print("\n" + "=" * 60)
    print("           FEATURE 8: FINAL REPORT GENERATOR")
    print("=" * 60)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate Markdown
    md_content = _build_markdown(results, chart_paths)
    md_path = OUTPUT_DIR / "final_report.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"  Markdown report saved: {md_path}")

    # Generate HTML
    html_content = _markdown_to_html(md_content, chart_paths)
    html_path = OUTPUT_DIR / "final_report.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"  HTML report saved:     {html_path}")

    print("=" * 60)

    return md_path, html_path


if __name__ == "__main__":
    generate_report()
