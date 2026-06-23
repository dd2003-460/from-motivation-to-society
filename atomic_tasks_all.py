#!/usr/bin/env python3
"""
创建最小原子任务清单 - 自动检测最小级别
"""

import re
import json
from datetime import datetime

def extract_atomic_tasks(file_path, chapter_name):
    """提取最小原子任务（subsubsection > subsection > section）"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    # 检测最细粒度
    has_subsubsection = any(r'\subsubsection*' in line for line in lines)
    has_subsection = any(r'\subsection{' in line for line in lines)
    
    tasks = []
    current_section = None
    current_subsection = None
    current_subsubsection = None
    
    for i, line in enumerate(lines):
        # 检测section
        if r'\section{' in line:
            match = re.search(r'\\section\{([^}]+)\}', line)
            if match:
                current_section = match.group(1)
                # 如果没有更细粒度，section就是最小原子
                if not has_subsection and not has_subsubsection:
                    task_id = f"{chapter_name}.{len(tasks)+1:03d}"
                    tasks.append({
                        "id": task_id,
                        "chapter": chapter_name,
                        "level": "section",
                        "section": current_section,
                        "line": i + 1,
                        "status": "pending"
                    })
        
        # 检测subsection
        elif r'\subsection{' in line:
            match = re.search(r'\\subsection\{([^}]+)\}', line)
            if match:
                current_subsection = match.group(1)
                # 如果没有subsubsection，subsection就是最小原子
                if not has_subsubsection:
                    task_id = f"{chapter_name}.{len(tasks)+1:03d}"
                    tasks.append({
                        "id": task_id,
                        "chapter": chapter_name,
                        "level": "subsection",
                        "section": current_section,
                        "subsection": current_subsection,
                        "line": i + 1,
                        "status": "pending"
                    })
        
        # 检测subsubsection (最小原子)
        elif r'\subsubsection*' in line:
            match = re.search(r'\\subsubsection\*\{([^}]+)\}', line)
            if match:
                current_subsubsection = match.group(1)
                task_id = f"{chapter_name}.{len(tasks)+1:03d}"
                tasks.append({
                    "id": task_id,
                    "chapter": chapter_name,
                    "level": "subsubsection",
                    "section": current_section,
                    "subsection": current_subsection,
                    "subsubsection": current_subsubsection,
                    "line": i + 1,
                    "status": "pending"
                })
    
    return tasks

def main():
    files = [
        ("part3_systematic_expansion/chapter2_culture_folk_institutions.tex", "Ch2"),
        ("part3_systematic_expansion/chapter3_politics_power_structure.tex", "Ch3"),
        ("part3_systematic_expansion/chapter4_law_institutional_form.tex", "Ch4"),
    ]
    
    all_tasks = []
    
    for file_path, chapter_name in files:
        print(f"\n=== {chapter_name} ===")
        tasks = extract_atomic_tasks(file_path, chapter_name)
        all_tasks.extend(tasks)
        print(f"最小原子级别: {tasks[0]['level'] if tasks else 'N/A'}")
        print(f"原子任务数: {len(tasks)}")
        for t in tasks[:3]:
            print(f"  [{t['id']}] {t.get('subsection', 'N/A')[:50]}")
    
    # 保存
    with open("atomic_tasks_minimal.json", 'w', encoding='utf-8') as f:
        json.dump(all_tasks, f, ensure_ascii=False, indent=2)
    
    print(f"\n总计: {len(all_tasks)} 个最小原子任务")

if __name__ == '__main__':
    main()
