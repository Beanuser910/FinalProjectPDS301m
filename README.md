# Final Project - BeautifulSoup Documentation Analytics System

## Project Scenario
This project is developed by **Thành viên 1: HTML Collector & Section Extractor**.

The team builds a Python-based analytics system that collects, parses, and extracts data from the official BeautifulSoup documentation page:

https://www.crummy.com/software/BeautifulSoup/bs4/doc/

## Main Features (Thành viên 1)

1. **Feature 1 — Web Page Collector**: Send HTTP request to the target URL, check status code, and save raw HTML to `data/raw/beautifulsoup_doc.html`.
2. **Feature 2 — HTML Parser**: Parse the HTML using BeautifulSoup.
3. **Feature 3 — Section Extractor**: Extract all documentation sections, compute word count, code block count, and link count per section, and save to `data/processed/sections.csv`.

## Project Structure

```text
FinalProjectPDS301m/
├── src/
│   ├── __init__.py
│   ├── collector.py      # Feature 1: Web Page Collector
│   ├── parser.py        # Feature 2: HTML Parser
│   ├── extractor.py     # Feature 3: Section Extractor
│   └── main.py          # Orchestrates Features 1-3
├── data/
│   ├── raw/
│   │   └── beautifulsoup_doc.html
│   └── processed/
│       └── sections.csv
├── notebooks/
│   └── FinalProject_BeautifulSoup_Analysis.ipynb
├── README.md
├── requirements.txt
└── .gitignore
```

## How to Run

### Option 1: Run as Python script (headless)

```bash
pip install -r requirements.txt
python src/main.py
```

### Option 2: Run as Jupyter Notebook (interactive)

```bash
pip install -r requirements.txt
jupyter notebook
```

Then open `notebooks/FinalProject_BeautifulSoup_Analysis.ipynb` and run all cells from top to bottom.

## Output Files

After running the pipeline, the following files will be generated:

- `data/raw/beautifulsoup_doc.html`
- `data/processed/sections.csv`

## Notes

This is the work of **Thành viên 1**. Other team members will build upon these outputs.
