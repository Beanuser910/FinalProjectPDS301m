# Final Project - BeautifulSoup Documentation Analytics System

## Project Scenario
This project builds a Python-based analytics system that collects, parses, extracts, analyzes, and visualizes data from the official BeautifulSoup documentation page:

https://www.crummy.com/software/BeautifulSoup/bs4/doc/

The project is designed to run in **Jupyter Notebook**.

## Main Features

1. Download the BeautifulSoup documentation page using `requests`.
2. Save raw HTML into `data/raw/beautifulsoup_doc.html`.
3. Parse HTML content using `BeautifulSoup`.
4. Extract documentation sections into `data/processed/sections.csv`.
5. Extract hyperlinks into `data/processed/links.csv`.
6. Extract code examples into `data/processed/code_examples.csv`.
7. Analyze data using `Pandas` and `NumPy`.
8. Create charts using `Matplotlib`.
9. Prepare final report content inside the notebook.

## Project Structure

```text
FinalProject/
├── data/
│   ├── raw/
│   │   └── beautifulsoup_doc.html
│   └── processed/
│       ├── sections.csv
│       ├── links.csv
│       └── code_examples.csv
├── output/
│   └── charts/
│       ├── word_count_by_section.png
│       ├── code_examples_by_section.png
│       ├── link_type_distribution.png
│       └── code_linecount_hist.png
├── FinalProject_BeautifulSoup_Analysis.ipynb
├── README.md
├── requirements.txt
└── .gitignore
```

## How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Open Jupyter Notebook:

```bash
jupyter notebook
```

3. Open this file:

```text
FinalProject_BeautifulSoup_Analysis.ipynb
```

4. Run all cells from top to bottom.

## Output Files

After running the notebook, the following files will be generated:

- `data/raw/beautifulsoup_doc.html`
- `data/processed/sections.csv`
- `data/processed/links.csv`
- `data/processed/code_examples.csv`
- `output/charts/word_count_by_section.png`
- `output/charts/code_examples_by_section.png`
- `output/charts/link_type_distribution.png`
- `output/charts/code_linecount_hist.png`

## Notes

The final analytical report can be written directly in the notebook using Markdown cells and exported to PDF.
