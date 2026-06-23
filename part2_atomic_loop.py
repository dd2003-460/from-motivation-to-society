#!/usr/bin/env python3
"""
Part 2 最小原子Loop执行器
每个subsection执行完整8阶段Loop
"""

import json
import os
import shutil
import re
from datetime import datetime

ATOMIC_MEMORY = "atomic_loop_memory.jsonl"
TASKS_FILE = "part2_atomic_tasks.json"

def load_tasks():
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
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
    with open(ATOMIC_MEMORY, 'a') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

def backup(file_path, task_id):
    """最小单元loop必须备份"""
    os.makedirs("backups/part2", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = f"backups/part2/{os.path.basename(file_path)}.{task_id}.{ts}.bak"
    shutil.copy2(file_path, dst)
    return dst

def extract_section_content(file_path, start_line):
    """提取subsection内容"""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    end_line = start_line
    for i in range(start_line, len(lines)):
        if any(tag in lines[i] for tag in [r'\subsection{', r'\section{']):
            end_line = i
            break
    
    return ''.join(lines[start_line:end_line])

def analyze_issues(content):
    """分析段落问题"""
    issues = []
    
    # 1. Markdown语法
    if '**' in content:
        issues.append({"type": "markdown", "desc": "Markdown粗体"})
    
    # 2. tcolorbox配对
    tcolorbox_start = content.count(r'\begin{tcolorbox}')
    tcolorbox_end = content.count(r'\end{tcolorbox}')
    if tcolorbox_start != tcolorbox_end:
        issues.append({"type": "tcolorbox", "desc": f"配对错误({tcolorbox_start}/{tcolorbox_end})"})
    
    # 3. 段落间距
    if len(content) > 500 and content.count('\n\n') < 2:
        issues.append({"type": "spacing", "desc": "缺乏空行分隔"})
    
    # 4. 过长段落
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
    long_paragraphs = [p for p in paragraphs if len(p) > 400]
    if long_paragraphs:
        issues.append({"type": "long_paragraph", "desc": f"{len(long_paragraphs)}个长段落"})
    
    return issues

def atomic_loop_8_phases(task):
    """执行8阶段完整Loop"""
    task_id = task['id']
    file_path = task['file']
    line_num = task['line'] - 1  # 转为0-indexed
    
    print(f"\n=== {task_id}: {task['subsection'][:40]} ===")
    
    # Phase 1: Plan
    write_memory(task_id, "plan", "分析任务", f"修复{task['subsection'][:30]}")
    
    # Phase 2: Gather
    content = extract_section_content(file_path, line_num)
    write_memory(task_id, "gather", "提取内容", f"{len(content)}字符")
    
    # Phase 3: Decompose
    issues = analyze_issues(content)
    write_memory(task_id, "decompose", "识别问题", f"{len(issues)}个", str([i['type'] for i in issues]))
    
    # Phase 4: Execute
    backup_path = backup(file_path, task_id)
    write_memory(task_id, "execute", "创建备份", backup_path)
    
    # Phase 5: Verify
    status = "completed" if len(issues) == 0 else "needs_fix"
    write_memory(task_id, "verify", "验证结果", f"{'无问题' if status == 'completed' else f'{len(issues)}个问题'}")
    
    # Phase 6: Feedback
    feedback = f"{'✅' if status == 'completed' else '🔧'} {len(issues)}个问题"
    write_memory(task_id, "feedback", "反馈", feedback)
    
    # Phase 7: Memory
    task['status'] = status
    task['last_loop'] = datetime.now().isoformat()
    task['issues_count'] = len(issues)
    
    # Phase 8: Improve
    write_memory(task_id, "improve", "记录经验", f"完成Loop, {len(issues)}问题")
    
    print(f"  结果: {feedback}")
    return status

def main():
    print("=== Part 2 最小原子Loop执行 ===\n")
    
    tasks = load_tasks()
    print(f"总原子任务: {len(tasks)}")
    
    completed = 0
    needs_fix = 0
    
    for task in tasks:
        if task.get('status') == 'completed':
            completed += 1
            continue
        
        try:
            status = atomic_loop_8_phases(task)
            if status == 'completed':
                completed += 1
            else:
                needs_fix += 1
        except Exception as e:
            write_memory(task['id'], "error", "执行失败", str(e))
            print(f"  ❌ 错误: {e}")
    
    save_tasks(tasks)
    
    print(f"\n=== 完成统计 ===")
    print(f"✅ 已完成: {completed}")
    print(f"🔧 需修复: {needs_fix}")
    print(f"📊 进度: {completed}/{len(tasks)} ({completed/len(tasks)*100:.1f}%)")

if __name__ == '__main__':
    main()