"""
Feature 7 — Data Visualization.

Generates at least 4 charts from the processed CSV datasets using
Matplotlib and saves them to output/charts/.

Required charts:
  1. Bar chart: Top 10 sections by word count
  2. Bar chart: Number of code examples by section
  3. Pie chart: Link type distribution
  4. Histogram: Code example line count distribution
"""

from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROCESSED_DIR = Path("data/processed")
CHARTS_DIR = Path("output/charts")

SECTIONS_CSV = PROCESSED_DIR / "sections.csv"
LINKS_CSV = PROCESSED_DIR / "links.csv"
CODE_EXAMPLES_CSV = PROCESSED_DIR / "code_examples.csv"


def _load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load the three processed CSV files into DataFrames."""
    df_sections = pd.read_csv(SECTIONS_CSV)
    df_links = pd.read_csv(LINKS_CSV)
    df_code = pd.read_csv(CODE_EXAMPLES_CSV)
    return df_sections, df_links, df_code


def _truncate(text: str, max_len: int = 30) -> str:
    """Truncate long section titles for readable axis labels."""
    return text if len(text) <= max_len else text[:max_len] + "..."


def chart_top_sections_by_word_count(df_sections: pd.DataFrame) -> Path:
    """Bar chart: Top 10 sections by word count."""
    top10 = df_sections.nlargest(10, "word_count")

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(
        [_truncate(t, 35) for t in top10["section_title"][::-1]],
        top10["word_count"][::-1],
        color="#2b6cb0",
        edgecolor="white",
    )
    ax.set_xlabel("Word Count", fontsize=11)
    ax.set_title("Top 10 Sections by Word Count", fontsize=14, fontweight="bold")
    ax.bar_label(bars, fmt="%d", padding=3, fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()

    path = CHARTS_DIR / "chart_top_sections_word_count.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def chart_code_examples_by_section(df_code: pd.DataFrame) -> Path:
    """Bar chart: Number of code examples by section."""
    counts = df_code["section_title"].value_counts()

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(
        [_truncate(t, 25) for t in counts.index],
        counts.values,
        color="#2f855a",
        edgecolor="white",
    )
    ax.set_xlabel("Section", fontsize=11)
    ax.set_ylabel("Number of Code Examples", fontsize=11)
    ax.set_title("Code Examples by Section", fontsize=14, fontweight="bold")
    ax.bar_label(bars, fmt="%d", padding=3, fontsize=9)
    plt.xticks(rotation=45, ha="right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()

    path = CHARTS_DIR / "chart_code_examples_by_section.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def chart_link_type_distribution(df_links: pd.DataFrame) -> Path:
    """Pie chart: Link type distribution."""
    type_counts = df_links["link_type"].value_counts()

    colors = ["#3182ce", "#38a169", "#dd6b20", "#d69e2e", "#e53e3e", "#805ad5"]

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        type_counts.values,
        labels=type_counts.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors[: len(type_counts)],
        textprops={"fontsize": 10},
        pctdistance=0.75,
    )
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontweight("bold")
    ax.set_title("Link Type Distribution", fontsize=14, fontweight="bold")
    ax.axis("equal")
    fig.tight_layout()

    path = CHARTS_DIR / "chart_link_type_distribution.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def chart_code_line_count_histogram(df_code: pd.DataFrame) -> Path:
    """Histogram: Code example line count distribution."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(
        df_code["line_count"],
        bins=range(1, int(df_code["line_count"].max()) + 2),
        color="#6b46c1",
        edgecolor="white",
        align="left",
    )
    ax.set_xlabel("Line Count", fontsize=11)
    ax.set_ylabel("Frequency", fontsize=11)
    ax.set_title("Code Example Line Count Distribution", fontsize=14, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()

    path = CHARTS_DIR / "chart_code_line_count_histogram.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def visualize() -> list[Path]:
    """
    Generate all required charts and save them to output/charts/.

    Returns
    -------
    list of Path
        Paths to the generated chart files.
    """
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)

    df_sections, df_links, df_code = _load_data()

    print("\n" + "=" * 60)
    print("           FEATURE 7: DATA VISUALIZATION")
    print("=" * 60)

    paths = []

    p1 = chart_top_sections_by_word_count(df_sections)
    print(f"  [1/4] Bar chart - Top 10 sections by word count  -> {p1}")
    paths.append(p1)

    p2 = chart_code_examples_by_section(df_code)
    print(f"  [2/4] Bar chart - Code examples by section       -> {p2}")
    paths.append(p2)

    p3 = chart_link_type_distribution(df_links)
    print(f"  [3/4] Pie chart  - Link type distribution        -> {p3}")
    paths.append(p3)

    p4 = chart_code_line_count_histogram(df_code)
    print(f"  [4/4] Histogram  - Code line count distribution  -> {p4}")
    paths.append(p4)

    print(f"\n  All {len(paths)} charts saved to: {CHARTS_DIR}")
    print("=" * 60)

    return paths


if __name__ == "__main__":
    visualize()
