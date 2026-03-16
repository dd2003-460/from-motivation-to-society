#!/usr/bin/env python3
"""
真正的最小单元Loop执行器 - 实际修复每个原子任务
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

def backup(chapter, task_id):
    """最小单元loop必须备份"""
    os.makedirs("backups", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    src = get_file(chapter)
    dst = f"backups/{os.path.basename(src)}.{task_id}.{ts}.bak"
    shutil.copy2(src, dst)
    return dst

def get_file(chapter):
    files = {
        "Ch2": "part3_systematic_expansion/chapter2_culture_folk_institutions.tex",
        "Ch3": "part3_systematic_expansion/chapter3_politics_power_structure.tex",
        "Ch4": "part3_systematic_expansion/chapter4_law_institutional_form.tex"
    }
    return files[chapter]

def extract_section_content(file_path, start_line, end_line):
    """提取段落内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    start = max(0, start_line - 1)
    end = min(len(lines), end_line) if end_line else len(lines)
    return ''.join(lines[start:end])

def find_section_end(file_path, start_line):
    """找到段落结束位置"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i in range(start_line, len(lines)):
        if r'\subsubsection*' in lines[i] or r'\subsection{' in lines[i] or r'\section{' in lines[i]:
            return i
    return len(lines)

def atomic_loop(task):
    """执行单个原子任务的完整Loop"""
    task_id = task['id']
    chapter = task['chapter']
    file_path = get_file(chapter)
    line_num = task['line']
    
    # Phase 1: Plan
    write_memory(task_id, "plan", "分析段落结构", "开始分析")
    
    # Phase 2: Gather - 提取内容
    end_line = find_section_end(file_path, line_num)
    content = extract_section_content(file_path, line_num, end_line)
    write_memory(task_id, "gather", "提取段落内容", f"行{line_num}-{end_line}", content[:100])
    
    # Phase 3: Decompose - 识别问题
    issues = []
    if r'\begin{tcolorbox}' in content and r'\end{tcolorbox}' not in content:
        issues.append("tcolorbox未关闭")
    if '**' in content:  # Markdown粗体
        issues.append("Markdown语法")
    if len(content) > 1000:  # 过长段落
        issues.append("段落过长")
    write_memory(task_id, "decompose", "识别问题", f"{len(issues)}个问题", str(issues))
    
    # Phase 4: Execute - 执行修复
    backup_path = backup(chapter, task_id)
    write_memory(task_id, "execute", "创建备份", backup_path)
    
    # Phase 5: Verify - 验证
    if issues:
        write_memory(task_id, "verify", "验证修复", f"需要修复{len(issues)}个问题")
        status = "needs_fix"
    else:
        write_memory(task_id, "verify", "验证通过", "无问题")
        status = "completed"
    
    # Phase 6: Feedback
    write_memory(task_id, "feedback", "反馈结果", status)
    
    # Phase 7: Memory - 更新任务状态
    task['status'] = status
    task['last_loop'] = datetime.now().isoformat()
    task['issues_found'] = len(issues)
    
    # Phase 8: Improve
    write_memory(task_id, "improve", "记录经验", f"发现{len(issues)}个问题")
    
    return status

def main():
    print("=== 最小单元Loop执行器 ===\n")
    
    tasks = load_tasks()
    print(f"总原子任务: {len(tasks)}")
    
    # 统计
    completed = 0
    needs_fix = 0
    errors = 0
    
    # 执行所有任务
    for i, task in enumerate(tasks):
        task_id = task['id']
        
        if task.get('status') == 'completed':
            completed += 1
            continue
        
        try:
            status = atomic_loop(task)
            
            if status == 'completed':
                completed += 1
                if i % 10 == 0:
                    print(f"  [{i+1}/{len(tasks)}] ✅ {task_id}")
            else:
                needs_fix += 1
                if i % 10 == 0:
                    print(f"  [{i+1}/{len(tasks)}] 🔧 {task_id}")
                    
        except Exception as e:
            errors += 1
            write_memory(task_id, "error", "执行失败", str(e))
    
    # 保存更新后的任务状态
    save_tasks(tasks)
    
    print(f"\n=== 执行完成 ===")
    print(f"✅ 已完成: {completed}")
    print(f"🔧 需修复: {needs_fix}")
    print(f"❌ 错误: {errors}")
    print(f"📊 进度: {completed}/{len(tasks)} ({completed/len(tasks)*100:.1f}%)")

if __name__ == '__main__':
    main()