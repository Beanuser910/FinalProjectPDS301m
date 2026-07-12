"""
Advanced Requirement: Local Analytics Application (GUI).
Uses Tkinter to provide a graphical user interface for non-technical users
to execute the complete analytics workflow and view charts/results.
"""

import sys
import os
from pathlib import Path
import tkinter as tk
from src import collector, parser, extractor, analyzer


class AnalyticsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BeautifulSoup Documentation Analytics System")
        self.geometry("900x600")
        self.configure(bg="#f8f9fa")

        # Set minimum window size
        self.minsize(900, 600)

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Color definitions
        self.primary_color = "#2b5c8f"
        self.accent_color = "#e6550d"
        self.bg_light = "#f8f9fa"

        # Apply styles
        self.style.configure(".", background=self.bg_light, font=("Segoe UI", 10))
        self.style.configure("TFrame", background=self.bg_light)
        
        # Header Style
        self.style.configure(
            "Header.TFrame", 
            background=self.primary_color
        )
        self.style.configure(
            "Header.TLabel", 
            background=self.primary_color, 
            foreground="white", 
            font=("Segoe UI", 16, "bold")
        )

        # Button Style
        self.style.configure(
            "Action.TButton", 
            foreground="white", 
            background=self.primary_color, 
            font=("Segoe UI", 10, "bold"),
            padding=6
        )
        self.style.map(
            "Action.TButton",
            background=[("active", "#1c436b"), ("disabled", "#cccccc")]
        )

        # Variables
        self.soup = None
        self.analytics_data = None
        
        self.build_ui()

    def build_ui(self):
        # 1. Header Banner
        header = ttk.Frame(self, style="Header.TFrame", height=60)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        
        lbl_title = ttk.Label(
            header, 
            text=" BeautifulSoup Documentation Analytics System", 
            style="Header.TLabel"
        )
        lbl_title.pack(side=tk.LEFT, padx=20, pady=12)
        
        # 2. Main Content Layout (Left Panel: Controls & Logs; Right Panel: Charts/Results)
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Left Panel (Width: 350)
        left_panel = ttk.Frame(main_container, width=350)
        left_panel.pack(fill=tk.BOTH, side=tk.LEFT, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Right Panel (Flexible)
        self.right_panel = ttk.Frame(main_container)
        self.right_panel.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        # --- Left Panel Widgets ---
        # Pipeline Operations Group
        group_ops = ttk.LabelFrame(left_panel, text=" Pipeline Operations ", padding=10)
        group_ops.pack(fill=tk.X, pady=(0, 10))
        
        self.btn_collect = ttk.Frame(group_ops) # Wrap in frame for layout
        self.btn_collect.pack(fill=tk.X, pady=4)
        ttk.Button(
            self.btn_collect, 
            text="1. Run Web Page Collector (HTML)", 
            style="Action.TButton",
            command=self.run_collector
        ).pack(fill=tk.X)

        self.btn_parse = ttk.Frame(group_ops)
        self.btn_parse.pack(fill=tk.X, pady=4)
        ttk.Button(
            self.btn_parse, 
            text="2. Run HTML Parser & Extractors", 
            style="Action.TButton",
            command=self.run_extractors
        ).pack(fill=tk.X)

        self.btn_analyze = ttk.Frame(group_ops)
        self.btn_analyze.pack(fill=tk.X, pady=4)
        ttk.Button(
            self.btn_analyze, 
            text="3. Run Documentation Analytics (Feature 6)", 
            style="Action.TButton",
            command=self.run_analytics
        ).pack(fill=tk.X)
        
        # Log Output Frame
        group_logs = ttk.LabelFrame(left_panel, text=" Console & Process Logs ", padding=10)
        group_logs.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(
            group_logs, 
            wrap=tk.WORD, 
            bg="#1e1e1e", 
            fg="#d4d4d4", 
            font=("Consolas", 9), 
            padx=5, 
            pady=5
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scroll = ttk.Scrollbar(group_logs, command=self.log_text.yview)
        scroll.pack(fill=tk.Y, side=tk.RIGHT)
        self.log_text.config(yscrollcommand=scroll.set)
        
        self.log("System initialized. Press '1. Run Web Page Collector' to begin.")

        # --- Right Panel View (Analytics Results Table) ---
        self.results_txt = tk.Text(
            self.right_panel, 
            wrap=tk.WORD, 
            bg="white", 
            fg="#333333", 
            font=("Segoe UI", 10), 
            padx=10, 
            pady=10
        )
        self.results_txt.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        res_scroll = ttk.Scrollbar(self.right_panel, command=self.results_txt.yview)
        res_scroll.pack(fill=tk.Y, side=tk.RIGHT)
        self.results_txt.config(yscrollcommand=res_scroll.set)
        self.results_txt.insert(tk.END, "Perform analytics to display results here.")
        self.results_txt.config(state=tk.DISABLED)

    def log(self, message: str):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def run_collector(self):
        try:
            self.log("\n[Step 1] Starting HTTP Web Collector...")
            html = collector.collect()
            self.log(f"Successfully downloaded BeautifulSoup Docs! Cached locally.")
            messagebox.showinfo("Success", "Web Page collected and saved locally.")
        except Exception as e:
            self.log(f"Error in Collector: {str(e)}")
            messagebox.showerror("Error", f"Failed to collect web page: {str(e)}")

    def run_extractors(self):
        try:
            self.log("\n[Step 2] Parsing HTML and executing Data Extractors...")
            # Load raw html
            raw_path = PROJECT_ROOT / "data" / "raw" / "beautifulsoup_doc.html"
            if not raw_path.exists():
                messagebox.showwarning("Warning", "Please run step 1 first to download the HTML.")
                return
            
            html = parser.load_html(raw_path)
            self.soup = parser.parse_html(html)
            self.log("Parsed HTML DOM successfully.")
            
            self.log("Running Extractor pipelines...")
            extractor.extract(self.soup)
            self.log("Successfully extracted: sections.csv, links.csv, and code_examples.csv.")
            messagebox.showinfo("Success", "HTML parsed and all datasets extracted successfully.")
        except Exception as e:
            self.log(f"Error in Extractors: {str(e)}")
            messagebox.showerror("Error", f"Failed to parse or extract: {str(e)}")

    def run_analytics(self):
        try:
            self.log("\n[Step 3] Running Documentation Analytics (Feature 6)...")
            self.analytics_data = analyzer.analyze()
            
            # Print to GUI text field
            self.results_txt.config(state=tk.NORMAL)
            self.results_txt.delete("1.0", tk.END)
            
            output = "=" * 60 + "\n"
            output += "           DOCUMENTATION ANALYTICS SUMMARY RESULTS\n"
            output += "=" * 60 + "\n\n"
            
            output += f"Q1: Total Documentation Sections: {self.analytics_data['q1_total_sections']}\n\n"
            
            q2 = self.analytics_data['q2_max_word_section']
            output += f"Q2: Section with highest word count:\n"
            output += f"    -> \"{q2['title']}\" ({q2['word_count']} words)\n\n"
            
            q3 = self.analytics_data['q3_max_code_section']
            output += f"Q3: Section with most code blocks:\n"
            output += f"    -> \"{q3['title']}\" ({q3['code_block_count']} code blocks)\n\n"
            
            q4 = self.analytics_data['q4_max_link_section']
            output += f"Q4: Section with most hyperlinks:\n"
            output += f"    -> \"{q4['title']}\" ({q4['link_count']} links)\n\n"
            
            output += "Q5: Top 10 Frequent Technical Keywords:\n"
            for idx, (word, count) in enumerate(self.analytics_data['q5_top_10_keywords'], start=1):
                output += f"    {idx}. {word}: {count} times\n"
            output += "\n"
            
            q6 = self.analytics_data['q6_link_counts']
            output += "Q6: Hyperlink Classification Counts:\n"
            output += f"    -> Page-internal anchor links: {q6['internal_anchor']}\n"
            output += f"    -> Documentation links (same domain): {q6['documentation_link']}\n"
            output += f"    -> External domain links: {q6['external_link']}\n"
            output += f"    -> Image links: {q6['image_link']}\n"
            output += f"    -> Empty/Invalid links: {q6['empty_or_invalid']}\n\n"
            
            output += f"Q7: Code examples using find_all(): {self.analytics_data['q7_find_all_count']}\n"
            output += f"Q8: Code examples using get_text(): {self.analytics_data['q8_get_text_count']}\n\n"
            
            output += "-" * 60 + "\n"
            output += "           ADDITIONAL ANALYTICS\n"
            output += "-" * 60 + "\n\n"
            
            q9 = self.analytics_data['q9_code_line_stats']
            output += f"Q9: Average line count per code example: {q9['average_line_count']:.2f} lines\n"
            output += f"    -> Longest code example is inside section \"{q9['longest_example_section']}\" ({q9['longest_example_lines']} lines)\n\n"
            
            output += "Q10: Stats by heading level (average count):\n"
            q10_stats = self.analytics_data['q10_level_statistics']
            for lvl in sorted(q10_stats['word_count']['mean'].keys()):
                output += f"    {lvl.upper()}: Word count avg: {q10_stats['word_count']['mean'][lvl]:.1f} | Code blocks avg: {q10_stats['code_block_count']['mean'][lvl]:.1f} | Links avg: {q10_stats['link_count']['mean'][lvl]:.1f}\n"
                
            self.results_txt.insert(tk.END, output)
            self.results_txt.config(state=tk.DISABLED)
            
            self.log("Analytics completed and displayed in the Summary panel.")
            messagebox.showinfo("Success", "Analytics calculated and panel updated.")
        except Exception as e:
            self.log(f"Error in Analytics: {str(e)}")
            messagebox.showerror("Error", f"Failed to compute analytics: {str(e)}")


if __name__ == "__main__":
    app = AnalyticsApp()
    app.mainloop()
