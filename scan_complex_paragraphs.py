#!/usr/bin/env python3
import re, json, sys
from pathlib import Path

# 新术语识别：匹配 \textbf{...} 或 中文新词（大写、特殊强调）
TERM_PATTERN = re.compile(r'\\textbf\{([^}]+)\}|\b[A-Z][A-Za-z]+\b')

def count_terms(text):
    """ Count new/unfamiliar terms in a paragraph """
    matches = TERM_PATTERN.findall(text)
    if not matches:
        return 0
    # flatten if nested groups (from regex with capture groups)
    if isinstance(matches[0], tuple):
        terms = [m for tup in matches for m in tup if m]
    else:
        terms = matches
    return len(terms)

def analyze_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 按段落分割：\par 或 空行
    paragraphs = re.split(r'\n\s*\n|\\par\s*\n', content)
    
    complex_paras = []
    for idx, para in enumerate(paragraphs, 1):
        para = para.strip()
        if not para:
            continue
        char_count = len(para)
        term_count = count_terms(para)
        
        if char_count > 250 or term_count > 3:
            complex_paras.append({
                'index': idx,
                'char_count': char_count,
                'term_count': term_count,
                'preview': para[:100] + ('...' if len(para)>100 else '')
            })
    return complex_paras

if __name__ == '__main__':
    base = Path('.')
    chapters = list(base.glob('part3_systematic_expansion/chapter*.tex'))
    all_complex = {}
    for ch in chapters:
        all_complex[ch.name] = analyze_file(ch)
    
    print(json.dumps(all_complex, ensure_ascii=False, indent=2))
    # Also save to file
    (base / 'complex_paragraphs_report.json').write_text(json.dumps(all_complex, ensure_ascii=False, indent=2))
