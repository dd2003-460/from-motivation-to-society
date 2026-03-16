#!/usr/bin/env python3
import re
from pathlib import Path

file = Path('part3_systematic_expansion/chapter3_politics_power_structure.tex')
content = file.read_text(encoding='utf-8')

# Pattern: \textbf{段落N（whyN：主题）}：\\
# Replace with: \subsubsection*{段落N：主题}
def repl_para_header(m):
    full = m.group(0)
    # Extract N and topic
    num = re.search(r'段落(\d+)', full).group(1)
    # Extract topic between )(colon) and closing )
    topic_match = re.search(r'why\d+：([^）]+)', full)
    topic = topic_match.group(1) if topic_match else f"待定{num}"
    return f'\t\\subsubsection*{{段落{num}：{topic}}}'

content = re.sub(
    r'\t?\\textbf\{段落\d+（why\d+：[^）]+）\}：\\\\',
    repl_para_header,
    content
)

# Fix malformed motivation environments: \begin{motivation> should be \begin{motivation}
content = content.replace(r'\begin{motivation>', r'\begin{motivation}')
content = content.replace(r'\end{motivation>', r'\end{motivation}')

# Add reader prediction boxes after first sentence of each subsubsection
# Strategy: find each \subsubsection*{段落...} then insert tcolorbox after its first sentence (first 。 or \\t)
def add_prediction_box(match):
    header = match.group(0)
    # The content after header continues until next \subsubsection or \section or \subsection or end
    # We'll process by splitting content at header and then inserting before next structural element
    return header  # placeholder, do later

# This is complex, do it manually per paragraph after headers are fixed
file.write_text(content, encoding='utf-8')
print(f"Fixed headers in {file.name}")
