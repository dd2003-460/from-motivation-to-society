#!/usr/bin/env python3
"""
准确提取 Part3 中 \textbf{段落N（...）}：后的实际内容，统计字符数和术语数
"""
import re
import json
from pathlib import Path

PART3_DIR = Path("/Users/chenglu/.claude/workspace/动机社会/part3_systematic_expansion")
OUTPUT = Path("/Users/chenglu/.claude/workspace/动机社会/complex_paragraphs_detailed.json")

# 匹配 \textbf{段落N（...）}：\\ (注意：LaTeX 源码中是两个反斜杠)
PARA_PATTERN = re.compile(
    r'\\\\textbf\{段落\d+[^}]*\}：\\\\\s*(.*?)(?=\\\\textbf\{段落\d+|\\\\section\{|\\\\subsection\*|\Z)',
    re.DOTALL
)

TERM_PATTERN = re.compile(r'\\textbf\{[^}]+\}|\b[A-Za-z]{4,}\b|[\u4e00-\u9fa5]{2,4}(?:论|原理|机制|系统|结构|模型|定理|法则|效应|现象|概念|方法|技术|策略|框架|分支|基础|形式|动力|行为|预测|聚合|选择|压力|编码|长度|退化|传播|载体|内化|代价|社会|经济|政治|文化|法律|权力|责任|信息|博弈|市场|价格|价值|需求|供给|稀缺|垄断|均衡)\b')

def extract_paragraphs(text: str):
    """返回列表 [(match_obj, paragraph_text)]"""
    matches = list(PARA_PATTERN.finditer(text))
    results = []
    for m in matches:
        para_text = m.group(1).strip()
        # 清理 LaTeX 命令，只保留纯文本用于统计
        clean_text = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', para_text)  # 移除 \cmd{...}
        clean_text = re.sub(r'\\[a-zA-Z]+', '', clean_text)  # 移除命令
        char_count = len(clean_text)
        term_count = len(set(TERM_PATTERN.findall(clean_text)))
        results.append({
            "full_match": m.group(0)[:100],
            "char_count": char_count,
            "term_count": term_count,
            "needs_split": char_count > 250 or term_count > 3
        })
    return results

def scan_file(filepath: Path):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return extract_paragraphs(content)
    except Exception as e:
        print(f"Error: {e}")
        return []

def main():
    all_paras = []
    for tex_file in PART3_DIR.glob("*.tex"):
        paras = scan_file(tex_file)
        for p in paras:
            p["file"] = tex_file.name
        all_paras.extend(paras)
    # 统计
    total = len(all_paras)
    needs = sum(1 for p in all_paras if p["needs_split"])
    print(f"📊 总计 {total} 个已标记段落，{needs} 个需要进一步拆分（>250字 或 >3术语）")
    # 保存详细结果
    OUTPUT.write_text(json.dumps(all_paras, ensure_ascii=False, indent=2))
    print(f"📄 详细数据: {OUTPUT}")
    # 输出前10个需要拆分的
    if needs > 0:
        print("\n🔍 需要拆分的段落示例:")
        for i, p in enumerate(all_paras):
            if p["needs_split"]:
                print(f"  {i+1}. {p['file']} | 字符={p['char_count']} 术语={p['term_count']}")
                if i >= 9: break

if __name__ == "__main__":
    main()
