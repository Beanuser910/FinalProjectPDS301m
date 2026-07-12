"""
Feature 6 — Documentation Analytics.

Analyzes sections, links, and code examples using Pandas and NumPy.
Answers 8 required questions and 2 additional questions.
"""

import re
from pathlib import Path
from collections import Counter
import pandas as pd
import numpy as np

# Path configurations
PROCESSED_DIR = Path("data/processed")
SECTIONS_CSV = PROCESSED_DIR / "sections.csv"
LINKS_CSV = PROCESSED_DIR / "links.csv"
CODE_EXAMPLES_CSV = PROCESSED_DIR / "code_examples.csv"


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load the processed CSV datasets into Pandas DataFrames."""
    if not SECTIONS_CSV.exists() or not LINKS_CSV.exists() or not CODE_EXAMPLES_CSV.exists():
        raise FileNotFoundError(
            "Processed CSV files not found. Please run the collector and extractor first."
        )

    df_sections = pd.read_csv(SECTIONS_CSV)
    df_links = pd.read_csv(LINKS_CSV)
    df_code = pd.read_csv(CODE_EXAMPLES_CSV)

    return df_sections, df_links, df_code


def get_top_keywords(df_sections: pd.DataFrame, top_n: int = 10) -> list[tuple[str, int]]:
    """
    Extract the top N most frequent technical keywords from the documentation text.
    Filters out common English stopwords and short words.
    """
    # A list of common English stopwords to filter out
    stopwords = {
        "the", "and", "a", "of", "to", "is", "in", "it", "you", "that", "this",
        "for", "with", "on", "as", "are", "it's", "your", "if", "an", "be", "or",
        "can", "but", "not", "have", "from", "by", "at", "use", "using", "how",
        "more", "about", "like", "will", "so", "they", "there", "what", "all",
        "which", "one", "file", "code", "work", "page", "get", "do", "does",
        "version", "then", "when", "some", "other", "into", "out", "also", "want",
        "see", "only", "then", "its", "them", "these", "here", "were", "was"
    }

    # Extract all text and lowercase
    all_text = " ".join(df_sections["section_text"].dropna().astype(str))
    # Keep only alphanumeric words and split
    words = re.findall(r"\b[a-zA-Z0-9_]+\b", all_text.lower())
    
    # Filter stopwords and words that are strictly numeric or too short (length < 3)
    filtered_words = [
        w for w in words 
        if w not in stopwords and len(w) >= 3 and not w.isdigit()
    ]

    counter = Counter(filtered_words)
    return counter.most_common(top_n)


def analyze() -> dict:
    """
    Run the analysis on BeautifulSoup documentation data.
    
    Returns
    -------
    dict
        A dictionary containing the answers to the analytical questions.
    """
    df_sections, df_links, df_code = load_data()
    results = {}

    print("\n" + "=" * 60)
    print("           FEATURE 6: DOCUMENTATION ANALYTICS")
    print("=" * 60)

    # 1. How many sections are in the documentation?
    total_sections = len(df_sections)
    results["q1_total_sections"] = total_sections
    print(f"Q1: How many sections are in the documentation?\n    -> {total_sections} sections\n")

    # 2. Which section has the highest word count?
    idx_max_word = df_sections["word_count"].idxmax()
    sec_max_word = df_sections.loc[idx_max_word]
    results["q2_max_word_section"] = {
        "title": sec_max_word["section_title"],
        "word_count": int(sec_max_word["word_count"])
    }
    print(f"Q2: Which section has the highest word count?\n    -> \"{sec_max_word['section_title']}\" ({sec_max_word['word_count']} words)\n")

    # 3. Which section contains the most code examples?
    # Note: We can count code blocks directly from sections.csv (code_block_count)
    idx_max_code = df_sections["code_block_count"].idxmax()
    sec_max_code = df_sections.loc[idx_max_code]
    results["q3_max_code_section"] = {
        "title": sec_max_code["section_title"],
        "code_block_count": int(sec_max_code["code_block_count"])
    }
    print(f"Q3: Which section contains the most code examples?\n    -> \"{sec_max_code['section_title']}\" ({sec_max_code['code_block_count']} code blocks)\n")

    # 4. Which section contains the most links?
    idx_max_link = df_sections["link_count"].idxmax()
    sec_max_link = df_sections.loc[idx_max_link]
    results["q4_max_link_section"] = {
        "title": sec_max_link["section_title"],
        "link_count": int(sec_max_link["link_count"])
    }
    print(f"Q4: Which section contains the most links?\n    -> \"{sec_max_link['section_title']}\" ({sec_max_link['link_count']} links)\n")

    # 5. What are the top 10 most frequent technical keywords?
    top_10_keywords = get_top_keywords(df_sections, top_n=10)
    results["q5_top_10_keywords"] = top_10_keywords
    print("Q5: What are the top 10 most frequent technical keywords?")
    for idx, (word, count) in enumerate(top_10_keywords, start=1):
        print(f"    {idx}. {word}: {count} times")
    print()

    # 6. How many internal and external links exist?
    link_types = df_links["link_type"].value_counts().to_dict()
    # Define classification based on our business rules:
    # - internal_anchor links are strictly internal page anchors
    # - documentation_link are links pointing within BeautifulSoup documentation domain
    # - external_link are links pointing to external websites
    internal_count = link_types.get("internal_anchor", 0)
    doc_link_count = link_types.get("documentation_link", 0)
    external_count = link_types.get("external_link", 0)
    image_count = link_types.get("image_link", 0)
    invalid_count = link_types.get("empty_or_invalid", 0)

    results["q6_link_counts"] = {
        "internal_anchor": int(internal_count),
        "documentation_link": int(doc_link_count),
        "external_link": int(external_count),
        "image_link": int(image_count),
        "empty_or_invalid": int(invalid_count)
    }
    print("Q6: How many internal and external links exist?")
    print(f"    -> Page-internal anchor links: {internal_count}")
    print(f"    -> Documentation links (domain-internal): {doc_link_count}")
    print(f"    -> External domain links: {external_count}")
    print(f"    -> Image links: {image_count}")
    print(f"    -> Empty or invalid links: {invalid_count}")
    print(f"    * Note: If documentation links are grouped as internal, total internal is {internal_count + doc_link_count}.\n")

    # 7. How many code examples use find_all()?
    # Sum boolean values
    find_all_count = int(df_code["contains_find_all"].sum())
    results["q7_find_all_count"] = find_all_count
    print(f"Q7: How many code examples use find_all()?\n    -> {find_all_count} examples\n")

    # 8. How many code examples use get_text()?
    get_text_count = int(df_code["contains_get_text"].sum())
    results["q8_get_text_count"] = get_text_count
    print(f"Q8: How many code examples use get_text()?\n    -> {get_text_count} examples\n")

    print("-" * 60)
    print("           ADDITIONAL ANALYTICAL QUESTIONS")
    print("-" * 60)

    # 9. Additional Q1: Average line count of code examples and the section containing the longest code example
    avg_lines = float(df_code["line_count"].mean())
    idx_longest_code = df_code["line_count"].idxmax()
    longest_code_row = df_code.loc[idx_longest_code]
    results["q9_code_line_stats"] = {
        "average_line_count": avg_lines,
        "longest_example_id": longest_code_row["example_id"],
        "longest_example_section": longest_code_row["section_title"],
        "longest_example_lines": int(longest_code_row["line_count"])
    }
    print("Q9 (Additional): Average lines of code examples & section with the longest example?")
    print(f"    -> Average lines per code example: {avg_lines:.2f} lines")
    print(f"    -> Longest code example is in section \"{longest_code_row['section_title']}\" ({longest_code_row['line_count']} lines)")
    print()

    # 10. Additional Q2: Summary stats (average word count, code blocks, links) by heading level (h1, h2, h3)
    # Using pandas aggregation
    level_stats = df_sections.groupby("section_level")[["word_count", "code_block_count", "link_count"]].agg(["mean", "sum"])
    results["q10_level_statistics"] = level_stats.to_dict()
    print("Q10 (Additional): Statistics by heading level (h1, h2, h3):")
    print(level_stats)
    print("=" * 60)

    return results


if __name__ == "__main__":
    analyze()
