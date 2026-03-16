#!/usr/bin/env python3
"""
扫描 Part3 章节，识别复杂段落（>250字符 或 >3个新术语）
输出: JSON 清单 [{file, section, para_id, char_count, term_count, needs_split}]
"""
import re
import json
from pathlib import Path

PART3_DIR = Path("/Users/chenglu/.claude/workspace/动机社会/part3_systematic_expansion")
OUTPUT = Path("/Users/chenglu/.claude/workspace/动机社会/scan_complex_paragraphs.json")

# 简单术语识别：包含中文专业词汇（非停用词）粗略统计
# 这里用启发式：包含 \textbf{...} 或特定术语模式算一个术语
TERM_PATTERN = re.compile(r'\\textbf\{[^}]+\}|\b[A-Za-z]{4,}\b|[\u4e00-\u9fa5]{2,4}(?:论|原理|机制|系统|结构|模型|定理|法则|效应|现象|概念|方法|技术|策略|框架)\b')

def count_terms(text: str) -> int:
    """粗略估计新术语数量"""
    matches = TERM_PATTERN.findall(text)
    return len(set(matches))  # 去重

def extract_paragraphs(content: str):
    """提取段落：以 \paragraph 或 \subsubsection 或空行分隔的文本块"""
    # 简化：按 \par 或 \subsubsection 分割
    blocks = re.split(r'(\\subsubsection\*|\\paragraph)', content)
    paragraphs = []
    current_header = None
    i = 0
    while i < len(blocks):
        if blocks[i].strip().startswith('\\subsubsection') or blocks[i].strip().startswith('\\paragraph'):
            current_header = blocks[i].strip()
            if i+1 < len(blocks):
                para_text = blocks[i+1].strip()
                paragraphs.append((current_header, para_text))
                i += 2
            else:
                i += 1
        else:
            # 纯文本块，可能是一个段落
            txt = blocks[i].strip()
            if txt:
                paragraphs.append((current_header or "（无标题）", txt))
            i += 1
    return paragraphs

def scan_file(filepath: Path):
    results = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        paras = extract_paragraphs(content)
        for header, text in paras:
            char_count = len(text)
            term_count = count_terms(text)
            needs_split = char_count > 250 or term_count > 3
            results.append({
                "file": filepath.name,
                "section": header,
                "char_count": char_count,
                "term_count": term_count,
                "needs_split": needs_split
            })
    except Exception as e:
        print(f"Error scanning {filepath}: {e}")
    return results

def main():
    all_results = []
    for tex_file in PART3_DIR.glob("*.tex"):
        all_results.extend(scan_file(tex_file))
    # 排序：优先需要 split 的，再按字符数降序
    all_results.sort(key=lambda x: (-x['needs_split'], -x['char_count']))
    OUTPUT.write_text(json.dumps(all_results, ensure_ascii=False, indent=2))
    print(f"✅ 扫描完成: {len(all_results)} 个段落，{sum(1 for r in all_results if r['needs_split'])} 个需拆分")
    print(f"📄 结果已保存: {OUTPUT}")

if __name__ == "__main__":
    main()
