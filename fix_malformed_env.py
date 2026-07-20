#!/usr/bin/env python3
from pathlib import Path

file = Path('part3_systematic_expansion/chapter3_politics_power_structure.tex')
content = file.read_text(encoding='utf-8')

# Fix \begin{motivation> and \end{motivation}>
content = content.replace(r'\begin{motivation>', r'\begin{motivation}')
content = content.replace(r'\end{motivation>', r'\end{motivation}')

# Fix \extbf{ to \textbf{
content = content.replace(r'\extbf{', r'\textbf{')

file.write_text(content, encoding='utf-8')
print(f"Fixed malformed environments and extbf in {file.name}")
