#!/usr/bin/env python3
"""
创建最小原子任务清单 - 每个subsubsection段落都是最小原子
"""

import re
import json
from datetime import datetime

def extract_atomic_tasks(file_path, chapter_name):
    """提取最小原子任务"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
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
        
        # 检测subsection
        elif r'\subsection{' in line:
            match = re.search(r'\\subsection\{([^}]+)\}', line)
            if match:
                current_subsection = match.group(1)
        
        # 检测subsubsection (最小原子)
        elif r'\subsubsection*' in line:
            match = re.search(r'\\subsubsection\*\{([^}]+)\}', line)
            if match:
                current_subsubsection = match.group(1)
                
                # 创建最小原子任务
                task_id = f"{chapter_name}.{len(tasks)+1:03d}"
                task = {
                    "id": task_id,
                    "chapter": chapter_name,
                    "section": current_section,
                    "subsection": current_subsection,
                    "subsubsection": current_subsubsection,
                    "line_number": i + 1,
                    "status": "pending",
                    "loop_phase": "plan",
                    "backup": None,
                    "errors": [],
                    "created": datetime.now().isoformat()
                }
                tasks.append(task)
    
    return tasks

def main():
    # 定义要处理的文件
    files = [
        ("part3_systematic_expansion/chapter2_culture_folk_institutions.tex", "Ch2_Culture"),
        ("part3_systematic_expansion/chapter3_politics_power_structure.tex", "Ch3_Politics"),
        ("part3_systematic_expansion/chapter4_law_institutional_form.tex", "Ch4_Law"),
    ]
    
    all_tasks = []
    
    for file_path, chapter_name in files:
        print(f"提取 {chapter_name} 的原子任务...")
        tasks = extract_atomic_tasks(file_path, chapter_name)
        all_tasks.extend(tasks)
        print(f"  - 找到 {len(tasks)} 个最小原子任务")
    
    # 保存任务清单
    with open("atomic_tasks_minimal.json", 'w', encoding='utf-8') as f:
        json.dump(all_tasks, f, ensure_ascii=False, indent=2)
    
    print(f"\n总计: {len(all_tasks)} 个最小原子任务")
    print("任务清单已保存到 atomic_tasks_minimal.json")

if __name__ == '__main__':
    main()
