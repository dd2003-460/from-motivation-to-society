#!/usr/bin/env python3
"""Flatten subfile-based LaTeX into a single file"""
import re
from pathlib import Path

base = Path('.')
result_lines = []
included = set()

def include_file(filepath):
    if filepath in included:
        return f"% SKIPPED (already included): {filepath}\n"
    if not filepath.exists():
        return f"% NOT FOUND: {filepath}\n"
    included.add(filepath)
    
    content = filepath.read_text(encoding='utf-8')
    output = []
    
    for line in content.splitlines(True):
        m = re.search(r'\\subfile\{([^}]+)\}', line)
        if m:
            subpath = base / m.group(1)
            if not str(subpath).endswith('.tex'):
                subpath = Path(str(subpath) + '.tex')
            output.append(f"\n% === BEGIN {m.group(1)} ===\n")
            output.append(include_file(subpath))
            output.append(f"% === END {m.group(1)} ===\n")
        elif line.strip().startswith(r'\documentclass') or line.strip().startswith(r'\begin{document}') or line.strip().startswith(r'\end{document}'):
            # Skip these from subfiles
            pass
        else:
            output.append(line)
    
    return ''.join(output)

# Process main.tex
main = base / 'main.tex'
content = main.read_text(encoding='utf-8')

# Keep preamble (everything before \begin{document})
preamble_end = content.find(r'\begin{document}')
if preamble_end > 0:
    # Keep up to and including \begin{document}
    preamble = content[:preamble_end + len(r'\begin{document}')]
    result_lines.append(preamble)
    result_lines.append('\n\n')

# Process all subfiles referenced in main
for line in content.splitlines():
    m = re.search(r'\\subfile\{([^}]+)\}', line)
    if m:
        subpath = base / m.group(1)
        if not str(subpath).endswith('.tex'):
            subpath = Path(str(subpath) + '.tex')
        result_lines.append(f"\n% ========== PART: {m.group(1)} ==========\n")
        result_lines.append(include_file(subpath))

result_lines.append('\n\n\\end{document}\n')
result = ''.join(result_lines)

Path('main_flat.tex').write_text(result, encoding='utf-8')
print(f"Flattened: {len(result)} chars, {len(included)} files included")
for f in sorted(included):
    print(f"  ✓ {f.relative_to(base)}")
