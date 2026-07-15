import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import squarify
import os
from matplotlib.patches import Patch

# Load data
df_sections = pd.read_csv('data/processed/sections.csv')
df_links = pd.read_csv('data/processed/links.csv')
df_code = pd.read_csv('data/processed/code_examples.csv')

os.makedirs('output/charts', exist_ok=True)

# Color palette
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'success': '#2E7D32',
    'info': '#00838F'
}

# ============================================
# CHART 2: Code Distribution (Treemap)
# ============================================
code_by_section = df_code['section_title'].value_counts()
threshold = 3
main_sections = code_by_section[code_by_section >= threshold]
other_count = code_by_section[code_by_section < threshold].sum()

labels = list(main_sections.index) + ['Other\nsections'] if other_count > 0 else list(main_sections.index)
values = list(main_sections.values) + [other_count] if other_count > 0 else list(main_sections.values)

data = [{'label': t[:30] + '...' if len(t) > 30 else t, 'value': v} 
        for t, v in zip(labels, values)]
data = sorted(data, key=lambda x: x['value'], reverse=True)

def get_color(val, max_val):
    ratio = val / max_val
    if ratio > 0.5: return '#1a5f2a'
    elif ratio > 0.25: return '#2e8b45'
    elif ratio > 0.1: return '#4caf50'
    else: return '#81c784'

max_val = max(d['value'] for d in data)
colors = [get_color(d['value'], max_val) for d in data]

fig, ax = plt.subplots(figsize=(14, 10))
fig.patch.set_facecolor('#f8f9fa')

squarify.plot(sizes=[d['value'] for d in data],
              label=[d['label'] for d in data],
              color=colors, alpha=0.9, edgecolor='white', linewidth=2,
              text_kwargs={'fontsize': 9, 'fontweight': 'bold', 'color': 'white'},
              ax=ax)

ax.set_title('Code Examples Distribution by Section\nHow Are Code Examples Distributed?',
             fontsize=14, fontweight='bold', pad=15)
ax.axis('off')

summary = 'Total: ' + str(sum(values)) + ' code examples\nTop: ' + data[0]['label'] + ' (' + str(data[0]['value']) + ')'
ax.annotate(summary, xy=(0.02, 0.98), xycoords='axes fraction',
            fontsize=11, va='top',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#2e8b45', alpha=0.95))

legend_elements = [Patch(facecolor='#1a5f2a', label='50+ examples'),
                   Patch(facecolor='#2e8b45', label='25-49 examples'),
                   Patch(facecolor='#4caf50', label='10-24 examples'),
                   Patch(facecolor='#81c784', label='< 10 examples')]
ax.legend(handles=legend_elements, loc='lower right', frameon=True, fontsize=10)

plt.tight_layout()
plt.savefig('output/charts/chart_02_code_distribution.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print('Chart 2 saved: chart_02_code_distribution.png')

# ============================================
# CHART 3: Link Type Distribution (Donut)
# ============================================
link_counts = df_links['link_type'].value_counts()

link_colors = {
    'internal_anchor': '#4CAF50',
    'documentation_link': '#2196F3',
    'external_link': '#FF9800',
    'image_link': '#9C27B0',
    'empty_or_invalid': '#9E9E9E'
}

colors = [link_colors.get(lt, '#607D8B') for lt in link_counts.index]

fig, ax = plt.subplots(figsize=(10, 10))

wedges, texts, autotexts = ax.pie(link_counts.values, 
                                   labels=link_counts.index,
                                   colors=colors,
                                   autopct='%1.1f%%',
                                   startangle=90,
                                   pctdistance=0.75,
                                   explode=[0.02] * len(link_counts))

for text in texts:
    text.set_fontsize(11)
    text.set_fontweight('bold')
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(11)
    autotext.set_fontweight('bold')

centre_circle = plt.Circle((0, 0), 0.50, fc='white')
ax.add_patch(centre_circle)

ax.text(0, 0, 'Total\n' + str(len(df_links)), ha='center', va='center', 
        fontsize=16, fontweight='bold')

ax.set_title('Link Types Distribution\nWhat Types of Links Are in the Documentation?',
             fontsize=14, fontweight='bold', pad=15)

plt.tight_layout()
plt.savefig('output/charts/chart_03_link_types.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print('Chart 3 saved: chart_03_link_types.png')

# ============================================
# CHART 4: Code Length Distribution
# ============================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

ax1 = axes[0]
ax1.hist(df_code['line_count'], bins=20, color=COLORS['secondary'], 
         edgecolor='white', linewidth=1.5, alpha=0.8)
ax1.axvline(df_code['line_count'].mean(), color='#d32f2f', linestyle='--', 
            linewidth=2, label='Mean: ' + str(round(df_code['line_count'].mean(), 1)))
ax1.axvline(df_code['line_count'].median(), color='#1976d2', linestyle='--', 
            linewidth=2, label='Median: ' + str(round(df_code['line_count'].median(), 1)))

ax1.set_xlabel('Number of Lines', fontsize=12)
ax1.set_ylabel('Frequency', fontsize=12)
ax1.set_title('Code Example Length Distribution\nHow Long Are Code Examples?', 
               fontsize=13, fontweight='bold')
ax1.legend(fontsize=10)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

ax2 = axes[1]
ax2.axis('off')

stats_text = '''
    Code Example Statistics
    ------------------------
    
    Total Examples: ''' + str(len(df_code)) + '''
    
    Average Length: ''' + str(round(df_code['line_count'].mean(), 1)) + ''' lines
    Median Length: ''' + str(round(df_code['line_count'].median(), 1)) + ''' lines
    Shortest Example: ''' + str(df_code['line_count'].min()) + ''' line(s)
    Longest Example: ''' + str(df_code['line_count'].max()) + ''' lines
    
    Standard Deviation: ''' + str(round(df_code['line_count'].std(), 1)) + '''
    
    Most Common Range: 1-10 lines
'''
ax2.text(0.1, 0.5, stats_text, fontsize=12, family='monospace',
         verticalalignment='center', 
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#f5f5f5', edgecolor='#bdbdbd'))

plt.tight_layout()
plt.savefig('output/charts/chart_04_code_length.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print('Chart 4 saved: chart_04_code_length.png')

# ============================================
# CHART 5: API Usage (Bonus)
# ============================================
api_usage = {
    'find_all()': int(df_code['contains_find_all'].sum()),
    'find()': int(df_code['contains_find'].sum()),
    'select()': int(df_code['contains_select'].sum()),
    'get_text()': int(df_code['contains_get_text'].sum()),
    'requests': int(df_code['contains_requests'].sum())
}

fig, ax = plt.subplots(figsize=(10, 6))

colors_api = [COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['success'], COLORS['info']]
bars = ax.bar(api_usage.keys(), api_usage.values(), 
               color=colors_api, edgecolor='white', linewidth=2)

for bar, val in zip(bars, api_usage.values()):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
            str(val), ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_xlabel('BeautifulSoup API Method', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Code Examples', fontsize=12, fontweight='bold')
ax.set_title('Most Used BeautifulSoup API Methods in Documentation\nWhich Functions Are Demonstrated Most?',
             fontsize=13, fontweight='bold', pad=15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(0, max(api_usage.values()) + 10)

plt.tight_layout()
plt.savefig('output/charts/chart_05_api_usage.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print('Chart 5 saved: chart_05_api_usage.png')

print('\nAll charts created successfully!')
