#!/usr/bin/env python3
import re
from pathlib import Path

# 数学概念词典（用于识别）
MATH_PATTERNS = {
    'probability': [r'条件概率', r'概率', r'P\(.*\|.*\)', r'Bayes', r'贝叶斯'],
    'game_theory': [r'博弈', r'纳什均衡', r'纳什', r'Nash', r' payoff ', r'收益矩阵'],
    'network_science': [r'网络', r'图\b', r'degree', r'节点', r'边', r'拓扑'],
    'information_theory': [r'信息', r'熵', r'Shannon', r'比特', r'bit'],
    'complexity': [r'复杂度', r'computational', r'算法', r'计算'],
    'differential_equations': [r'微分方程', r'导数', r'动态', r'增长曲线'],
    'statistics': [r'统计', r'回归', r'假设检验', r'p值', r'显著性'],
    'logic': [r'逻辑', r'¬', r'∧', r'∨', r'→', r'命题'],
    'set_theory': [r'集合', r'∈', r'⊆', r'∈', r'∈'],
    'optimization': [r'优化', r'最优化', r'极值', r'最大化', r'最小化'],
    'linear_algebra': [r'矩阵', r'向量', r'线性', r'特征值'],
    'category_theory': [r'范畴', r'Lawvere', r'category', r'functor'],
    'chaitin': [r'Chaitin', r'Ω', r'停机概率', r'mathematical boundary'],
}

def extract_math_from_file(filepath):
    content = Path(filepath).read_text(encoding='utf-8')
    concepts_found = {k: [] for k in MATH_PATTERNS}
    
    for concept, patterns in MATH_PATTERNS.items():
        for pat in patterns:
            matches = re.findall(pat, content, re.IGNORECASE)
            if matches:
                concepts_found[concept].extend(matches)
    
    # Deduplicate and count
    summary = {}
    for concept, matches in concepts_found.items():
        if matches:
            summary[concept] = {
                'count': len(matches),
                'examples': list(set(matches))[:5]  # unique sample
            }
    return summary

def scan_part3():
    base = Path('part3_systematic_expansion')
    chapters = list(base.glob('chapter*.tex'))
    overall = {}
    for ch in chapters:
        overall[ch.name] = extract_math_from_file(ch)
    return overall

if __name__ == '__main__':
    results = scan_part3()
    import json
    print(json.dumps(results, ensure_ascii=False, indent=2))
    # Save
    Path('math_concepts_report.json').write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print("\nSaved to math_concepts_report.json")
