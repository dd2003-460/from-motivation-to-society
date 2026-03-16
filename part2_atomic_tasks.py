#!/usr/bin/env python3
"""
Part 2 最小原子任务分解
"""

import json
import re
from datetime import datetime

def extract_atomic_tasks(file_path, chapter_name):
    """提取最小原子任务"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    tasks = []
    current_section = None
    current_subsection = None
    
    for i, line in enumerate(lines):
        if r'\section{' in line:
            match = re.search(r'\\section\{([^}]+)\}', line)
            if match:
                current_section = match.group(1)
        
        elif r'\subsection{' in line:
            match = re.search(r'\\subsection\{([^}]+)\}', line)
            if match:
                current_subsection = match.group(1)
                task_id = f"{chapter_name}.{len(tasks)+1:03d}"
                tasks.append({
                    "id": task_id,
                    "chapter": chapter_name,
                    "level": "subsection",
                    "section": current_section,
                    "subsection": current_subsection,
                    "line": i + 1,
                    "file": file_path,
                    "status": "pending",
                    "created": datetime.now().isoformat()
                })
    
    return tasks

def main():
    files = [
        ("part2_geological_determinism/chapter1_materialist_historical_view.tex", "P2Ch1"),
        ("part2_geological_determinism/chapter2_survival_strategy_divergence.tex", "P2Ch2"),
    ]
    
    all_tasks = []
    
    for file_path, chapter_name in files:
        print(f"\n=== {chapter_name} ===")
        tasks = extract_atomic_tasks(file_path, chapter_name)
        all_tasks.extend(tasks)
        print(f"最小原子级别: subsection")
        print(f"原子任务数: {len(tasks)}")
        for t in tasks:
            print(f"  [{t['id']}] 行{t['line']}: {t['subsection'][:50]}")
    
    # 保存
    with open("part2_atomic_tasks.json", 'w', encoding='utf-8') as f:
        json.dump(all_tasks, f, ensure_ascii=False, indent=2)
    
    print(f"\n总计: {len(all_tasks)} 个最小原子任务")

if __name__ == '__main__':
    main()
