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
import numpy as np
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
    """
    Horizontal bar chart: Sections by number of code examples.
    Replaced treemap with horizontal bars to avoid external dependency.
    """
    # Get section counts
    counts = df_code["section_title"].value_counts()

    # Group small sections (< 3 examples) into "Others"
    threshold = 3
    main_sections = counts[counts >= threshold]
    other_count = counts[counts < threshold].sum()

    if other_count > 0:
        labels = list(main_sections.index) + ["Other sections"]
        values = list(main_sections.values) + [other_count]
    else:
        labels = list(main_sections.index)
        values = list(main_sections.values)

    # Prepare data - truncate long labels
    data = [{"label": t[:35] + "..." if len(t) > 35 else t, "value": v}
            for t, v in zip(labels, values)]
    data = sorted(data, key=lambda x: x["value"], reverse=True)[:12]  # Top 12 for readability

    # Create figure
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor("white")

    # Color gradient based on value
    max_val = max(d["value"] for d in data)
    def get_color(value):
        ratio = value / max_val
        if ratio > 0.5:
            return "#276749"
        elif ratio > 0.25:
            return "#38a169"
        elif ratio > 0.1:
            return "#48bb78"
        else:
            return "#68d391"

    colors = [get_color(d["value"]) for d in data]

    # Create horizontal bar chart
    bars = ax.barh(
        [d["label"] for d in data],
        [d["value"] for d in data],
        color=colors,
        edgecolor="white",
        linewidth=0.8
    )

    # Add value labels on bars
    for bar, val in zip(bars, [d["value"] for d in data]):
        ax.text(
            bar.get_width() + 0.5,
            bar.get_y() + bar.get_height() / 2,
            f"{val}",
            va="center",
            ha="left",
            fontsize=10,
            fontweight="bold",
            color="#333333"
        )

    # Title and labels
    ax.set_xlabel("Number of Code Examples", fontsize=12, fontweight="bold")
    ax.set_title(
        "Code Examples by Section\n(How Are Code Examples Distributed?)",
        fontsize=14,
        fontweight="bold",
        pad=15
    )

    # Remove top and right spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Adjust layout
    plt.tight_layout()
    ax.set_xlim(0, max_val * 1.15)  # Add space for labels

    path = CHARTS_DIR / "chart_code_examples_by_section.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def chart_link_type_distribution(df_links: pd.DataFrame) -> Path:
    """Pie chart: Link type distribution with improved label positioning."""
    type_counts = df_links["link_type"].value_counts()

    # Use distinct colors with good contrast
    colors = ["#3182ce", "#38a169", "#dd6b20", "#d69e2e", "#e53e3e", "#805ad5", "#319795", "#d53f8c"]
    # Assign colors based on number of categories
    chart_colors = colors[:len(type_counts)]

    fig, ax = plt.subplots(figsize=(10, 10))

    # Create pie chart with better spacing
    wedges, texts, autotexts = ax.pie(
        type_counts.values,
        labels=None,  # We'll add legend instead of labels to avoid overlap
        autopct=lambda pct: f"{pct:.1f}%" if pct > 3 else "",
        startangle=90,
        colors=chart_colors,
        pctdistance=0.75,
        wedgeprops={"edgecolor": "white", "linewidth": 2},
    )

    # Style the percentage text
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontweight("bold")
        autotext.set_fontsize(11)

    # Add a white circle in the center for donut style (cleaner look)
    centre_circle = plt.Circle((0, 0), 0.50, fc="white")
    ax.add_patch(centre_circle)

    # Add title
    ax.set_title("Link Type Distribution\n(Total: {:,} links)".format(type_counts.sum()),
                 fontsize=14, fontweight="bold", pad=20)

    # Add center text
    ax.text(0, 0, f"{type_counts.sum()}\nLinks", ha="center", va="center",
            fontsize=16, fontweight="bold", color="#333333")

    # Create legend with counts
    legend_labels = [f"{label} ({count:,})" for label, count in type_counts.items()]
    ax.legend(wedges, legend_labels, title="Link Types", loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10, title_fontsize=11)

    ax.axis("equal")
    fig.tight_layout()

    path = CHARTS_DIR / "chart_link_type_distribution.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
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
