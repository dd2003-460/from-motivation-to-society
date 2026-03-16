#!/usr/bin/env python3
"""
修复5×5结构 - 确保每个chapter有5个section，每个section有5个subsection
"""

import json
import os
import shutil
from datetime import datetime

def analyze_structure(file_path):
    """分析章节结构"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 统计sections和subsections
    sections = content.count(r'\section{')
    subsections = content.count(r'\subsection{')
    subsubsections = content.count(r'\subsubsection*')
    
    return {
        'sections': sections,
        'subsections': subsections,
        'subsubsections': subsubsections,
        'needs_sections': max(0, 5 - sections),
        'needs_subsections': max(0, 25 - subsections)
    }

def create_missing_sections_template(chapter_title, missing_count):
    """创建缺失section的模板"""
    templates = []
    for i in range(missing_count):
        section_num = i + 1
        template = f"""
\\section{{New Section {section_num}: [Title]}}

\\begin{{motivation}}
[Enter motivation content here]
\\end{{motivation}}

\\begin{{logicmap}}
[Enter logic chain here]
\\end{{logicmap}}

\\begin{{questionbox}}
[Enter key question here]
\\end{{questionbox}}
"""
        templates.append(template)
    return templates

def create_missing_subsections_template(section_title, missing_count):
    """创建缺失subsection的模板"""
    templates = []
    for i in range(missing_count):
        sub_num = i + 1
        template = f"""
\\subsection{{New Subsection {sub_num}: [Title]}}

\\begin{{motivation}}
[Enter motivation content here]
\\end{{motivation}}

\\begin{{logicmap}}
[Enter logic chain here]
\\end{{logicmap}}

\\begin{{questionbox}}
[Enter key question here]
\\end{{questionbox}}

\\textbf{{段落1（why1：[Topic]）}}：
[Enter paragraph 1 content]

\\textbf{{段落2（why2：[Topic]）}}：
[Enter paragraph 2 content]

\\textbf{{段落3（why3：[Topic]）}}：
[Enter paragraph 3 content]

\\textbf{{段落4（why4：[Topic]）}}：
[Enter paragraph 4 content]

\\textbf{{段落5（why5并引出下一小节：[Topic]）}}：
[Enter paragraph 5 content]

\\paragraph*{{逻辑衔接}}
[Enter logic transition]

\\paragraph*{{读者可能还会问}}
\\begin{{itemize}}
\\item [Question 1]
\\item [Question 2]
\\item [Question 3]
\\item [Question 4]
\\end{{itemize}}
"""
        templates.append(template)
    return templates

def main():
    print("=== 5×5 结构修复分析 ===\n")
    
    files = [
        ('part2_geological_determinism/chapter1_materialist_historical_view.tex', 'P2Ch1'),
        ('part2_geological_determinism/chapter2_survival_strategy_divergence.tex', 'P2Ch2'),
        ('part3_systematic_expansion/chapter1_economic_base.tex', 'P3Ch1'),
        ('part3_systematic_expansion/chapter2_culture_folk_institutions.tex', 'P3Ch2'),
        ('part3_systematic_expansion/chapter3_politics_power_structure.tex', 'P3Ch3'),
        ('part3_systematic_expansion/chapter4_law_institutional_form.tex', 'P3Ch4'),
    ]
    
    total_missing_sections = 0
    total_missing_subsections = 0
    
    for file_path, ch_name in files:
        if os.path.exists(file_path):
            analysis = analyze_structure(file_path)
            print(f'{ch_name}:')
            print(f'  Sections: {analysis["sections"]}/5 (缺{analysis["needs_sections"]})')
            print(f'  Subsections: {analysis["subsections"]}/25 (缺{analysis["needs_subsections"]})')
            
            total_missing_sections += analysis['needs_sections']
            total_missing_subsections += analysis['needs_subsections']
            
            if analysis['needs_sections'] > 0 or analysis['needs_subsections'] > 0:
                print(f'  ⚠️ 需要修复')
            else:
                print(f'  ✅ 结构完整')
            print()
    
    print(f'=== 总计 ===')
    print(f'需要新增Sections: {total_missing_sections}')
    print(f'需要新增Subsections: {total_missing_subsections}')
    
    # 保存修复计划
    plan = {
        'timestamp': datetime.now().isoformat(),
        'total_missing_sections': total_missing_sections,
        'total_missing_subsections': total_missing_subsections,
        'files_analyzed': len(files)
    }
    
    with open('5x5_fix_plan.json', 'w') as f:
        json.dump(plan, f, indent=2)
    
    print(f'修复计划已保存到 5x5_fix_plan.json')

if __name__ == '__main__':
    main()