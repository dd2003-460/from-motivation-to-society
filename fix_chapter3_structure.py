#!/usr/bin/env python3
from pathlib import Path

file = Path('part3_systematic_expansion/chapter3_politics_power_structure.tex')
lines = file.read_text(encoding='utf-8').splitlines(keepends=True)

# Find line numbers
# §1 ends with the logic bridge line: "textbf{§1→§2 逻辑衔接}...下一节追踪..."
# §2 starts with: "\section{组织的抽象：从个人魅力到机构权威"

logic_bridge_line = None
section2_line = None

for i, line in enumerate(lines):
    if 'textbf{§1→§2 逻辑衔接}' in line:
        logic_bridge_line = i
    if r'\section{组织的抽象：从个人魅力到机构权威' in line:
        section2_line = i

print(f"Logic bridge at line: {logic_bridge_line}")
print(f"Section 2 at line: {section2_line}")

if logic_bridge_line is None or section2_line is None:
    print("Error: Could not find markers")
    exit(1)

# The misplaced subsections are between logic_bridge_line and section2_line
# We want to delete from (logic_bridge_line + 1) up to (section2_line - 1) inclusive
delete_start = logic_bridge_line + 1
delete_end = section2_line - 1

print(f"Will delete lines {delete_start} to {delete_end}")

# Reconstruct
new_lines = lines[:delete_start] + lines[section2_line:]

# Write
file.write_text(''.join(new_lines), encoding='utf-8')
print(f"Fixed structure. New line count: {len(new_lines)}")
