#!/usr/bin/env python3
import re
from pathlib import Path

base = Path('part3_systematic_expansion')
chapters = list(base.glob('chapter*.tex'))

report = {}
for ch in chapters:
    content = ch.read_text(encoding='utf-8')
    
    # Count subsections mistakenly placed under wrong section
    # Heuristic: after a \\section{, there should be \\subsection{, but before next \\section there should be no \\section
    issues = []
    
    # Check for malformed \begin{motivation>}
    malformed = content.count(r'\begin{motivation>')
    if malformed:
        issues.append(f"Malformed motivation env: {malformed} occurrences")
    
    # Check for \extbf{
    malformed_bf = content.count(r'\extbf{')
    if malformed_bf:
        issues.append(f"Malformed \\extbf{{: {malformed_bf} occurrences")
    
    # Check for misplaced \subsection before first \section (in chapter content, after \chapter)
    lines = content.splitlines()
    first_section_line = None
    for i, l in enumerate(lines):
        if r'\section{' in l:
            first_section_line = i
            break
    if first_section_line:
        # Check lines before first section for \subsection
        for i in range(0, first_section_line):
            if r'\subsection{' in lines[i]:
                issues.append(f"Misplaced \\subsection before first \\section at line {i+1}")
                break
    
    # Count \subsubsection* paragraphs (should be all \textbf{段落N} converted)
    subsub_count = len(re.findall(r'\\subsubsection\*', content))
    issues.append(f"Total \\subsubsection* paragraphs: {subsub_count}")
    
    # Count logic bridges
    bridge_count = content.count('逻辑衔接')
    issues.append(f"Logic bridges found: {bridge_count}")
    
    report[ch.name] = issues

# Print summary
for ch, issues in report.items():
    print(f"\n=== {ch} ===")
    for issue in issues:
        print(f"  - {issue}")
