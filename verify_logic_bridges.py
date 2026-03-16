#!/usr/bin/env python3
from pathlib import Path

file = Path('part3_systematic_expansion/chapter3_politics_power_structure.tex')
lines = file.read_text(encoding='utf-8').splitlines()

sections = []
for i, line in enumerate(lines):
    if r'\section{' in line:
        sections.append((i, line.strip()))

print(f"Found {len(sections)} sections:")
for idx, (ln, title) in enumerate(sections):
    print(f"  {idx+1}. Line {ln+1}: {title[:80]}")

# Check logic bridges
bridges = [i for i, l in enumerate(lines) if '逻辑衔接' in l]
print(f"\nFound {len(bridges)} logic bridges at lines: {[b+1 for b in bridges]}")

# Expect: 3 section-level bridges between 4 sections
if len(sections) >= 4 and len(bridges) >= 3:
    print("\n✅ Logic bridge count appears correct")
else:
    print(f"\n⚠️  Warning: Expected at least 3 bridges for {len(sections)} sections")
