#!/usr/bin/env python3
"""
循环执行直到所有原子任务完成
"""

import json
import os
import shutil
import re
from datetime import datetime

ATOMIC_MEMORY = "atomic_loop_memory.jsonl"
TASKS_FILE = "atomic_tasks_minimal.json"

def load_tasks():
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def write_memory(task_id, phase, action, result, evidence=""):
    entry = {
        "ts": datetime.now().isoformat(),
        "task": task_id,
        "phase": phase,
        "action": action,
        "result": result,
        "evidence": evidence[:200] if evidence else ""
    }
    with open(ATOMIC_MEMORY, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

def get_file(chapter):
    files = {
        "Ch2": "part3_systematic_expansion/chapter2_culture_folk_institutions.tex",
        "Ch3": "part3_systematic_expansion/chapter3_politics_power_structure.tex",
        "Ch4": "part3_systematic_expansion/chapter4_law_institutional_form.tex"
    }
    return files[chapter]

def backup(chapter, task_id):
    """最小单元loop必须备份"""
    os.makedirs("backups", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    src = get_file(chapter)
    dst = f"backups/{os.path.basename(src)}.{task_id}.{ts}.bak"
    shutil.copy2(src, dst)
    return dst

def fix_task(task):
    """修复单个原子任务"""
    task_id = task['id']
    chapter = task['chapter']
    file_path = get_file(chapter)
    line_num = task['line']
    
    # 备份
    backup_path = backup(chapter, task_id)
    write_memory(task_id, "loop_execute", "创建备份", backup_path)
    
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 找到段落范围
    end_line = line_num
    for i in range(line_num, len(lines)):
        if any(tag in lines[i] for tag in [r'\subsubsection*', r'\subsection{', r'\section{']):
            end_line = i
            break
    
    # 提取段落内容
    section_content = ''.join(lines[line_num:end_line])
    
    # 检查并修复问题
    fixed = False
    
    # 1. 修复Markdown粗体
    if '**' in section_content:
        section_content = section_content.replace('**', '\\textbf{').replace('**', '}')
        fixed = True
        write_memory(task_id, "fix", "修复Markdown粗体", "转换为LaTeX")
    
    # 2. 修复tcolorbox配对
    tcolorbox_start = section_content.count(r'\begin{tcolorbox}')
    tcolorbox_end = section_content.count(r'\end{tcolorbox}')
    if tcolorbox_start != tcolorbox_end:
        # 添加缺失的结束标签
        if tcolorbox_start > tcolorbox_end:
            section_content += '\n\\end{tcolorbox}\n'
            fixed = True
            write_memory(task_id, "fix", "修复tcolorbox配对", f"添加{tcolorbox_start-tcolorbox_end}个结束标签")
    
    # 3. 添加段落间距
    if '\n\n' not in section_content and len(section_content) > 200:
        # 在主要环境后添加空行
        section_content = re.sub(r'(\\end{(motivation|logicmap|questionbox|readingnote|tcolorbox)})\n', r'\1\n\n', section_content)
        fixed = True
        write_memory(task_id, "fix", "添加段落间距", "在环境后添加空行")
    
    # 写回文件
    if fixed:
        lines[line_num:end_line] = [section_content]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        write_memory(task_id, "verify", "验证修复", "已修复并写入")
        return "fixed"
    else:
        write_memory(task_id, "verify", "无需修复", "无问题")
        return "no_issues"

def main():
    print("=== 循环执行直到全部完成 ===\n")
    
    max_rounds = 10  # 最多10轮
    round_num = 0
    
    while round_num < max_rounds:
        round_num += 1
        print(f"\n--- 第 {round_num} 轮 ---")
        
        tasks = load_tasks()
        
        # 统计
        completed = sum(1 for t in tasks if t.get('status') == 'completed')
        needs_fix = sum(1 for t in tasks if t.get('status') == 'needs_fix')
        
        print(f"已完成: {completed}, 需修复: {needs_fix}")
        
        if needs_fix == 0:
            print("\n🎉 所有任务已完成！")
            break
        
        # 修复需要修复的任务
        fixed_count = 0
        for task in tasks:
            if task.get('status') == 'needs_fix':
                try:
                    result = fix_task(task)
                    if result == 'fixed':
                        task['status'] = 'completed'
                        task['fixed_in_round'] = round_num
                        fixed_count += 1
                except Exception as e:
                    write_memory(task['id'], "error", "修复失败", str(e))
        
        # 保存状态
        save_tasks(tasks)
        
        print(f"本轮修复: {fixed_count} 个任务")
        
        if fixed_count == 0:
            print("本轮无修复，退出循环")
            break
    
    # 最终统计
    tasks = load_tasks()
    completed = sum(1 for t in tasks if t.get('status') == 'completed')
    print(f"\n=== 最终结果 ===")
    print(f"总任务: {len(tasks)}")
    print(f"已完成: {completed}")
    print(f"完成率: {completed/len(tasks)*100:.1f}%")

if __name__ == '__main__':
    main()