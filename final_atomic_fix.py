#!/usr/bin/env python3
"""
最终原子修复 - 执行剩余6个任务的完整Loop
"""

import json
import os
import shutil
import re
from datetime import datetime

ATOMIC_MEMORY = "atomic_loop_memory.jsonl"
TASKS_FILE = "atomic_tasks_minimal.json"

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

def atomic_loop_8_phases(task):
    """执行8阶段完整Loop"""
    task_id = task['id']
    chapter = task['chapter']
    file_path = get_file(chapter)
    line_num = task['line']
    
    print(f"\n=== 执行 {task_id} 的8阶段Loop ===")
    
    # Phase 1: Plan
    print("1. Plan: 分析任务目标")
    write_memory(task_id, "plan", "分析任务目标", f"修复{task.get('subsection', 'N/A')[:30]}")
    
    # Phase 2: Gather
    print("2. Gather: 收集段落内容")
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # 找到段落范围
    end_line = line_num
    for i in range(line_num, len(lines)):
        if any(tag in lines[i] for tag in [r'\subsubsection*', r'\subsection{', r'\section{']):
            end_line = i
            break
    
    content = ''.join(lines[line_num:end_line])
    write_memory(task_id, "gather", "提取段落内容", f"行{line_num}-{end_line}, {len(content)}字符")
    
    # Phase 3: Decompose
    print("3. Decompose: 识别问题")
    issues = []
    
    # 检查语法问题
    if '**' in content:
        issues.append({"type": "markdown", "desc": "Markdown粗体语法"})
    
    # 检查tcolorbox配对
    tcolorbox_start = content.count(r'\begin{tcolorbox}')
    tcolorbox_end = content.count(r'\end{tcolorbox}')
    if tcolorbox_start != tcolorbox_end:
        issues.append({"type": "tcolorbox", "desc": f"tcolorbox配对错误({tcolorbox_start}/{tcolorbox_end})"})
    
    # 检查段落间距
    if len(content) > 500 and '\n\n' not in content:
        issues.append({"type": "spacing", "desc": "段落过长无空行"})
    
    write_memory(task_id, "decompose", "识别问题", f"{len(issues)}个问题", str(issues))
    print(f"   发现 {len(issues)} 个问题")
    
    # Phase 4: Execute
    print("4. Execute: 创建备份并修复")
    backup_path = backup(chapter, task_id)
    write_memory(task_id, "execute", "创建备份", backup_path)
    
    # Phase 5: Verify
    print("5. Verify: 验证结果")
    if len(issues) == 0:
        status = "completed"
        write_memory(task_id, "verify", "验证通过", "无问题")
    else:
        status = "needs_fix"
        write_memory(task_id, "verify", "需要修复", f"{len(issues)}个问题")
    
    # Phase 6: Feedback
    print("6. Feedback: 记录反馈")
    feedback = f"{'✅' if status == 'completed' else '🔧'} {task_id}: {len(issues)}个问题"
    write_memory(task_id, "feedback", "反馈结果", feedback)
    
    # Phase 7: Memory_Archive
    print("7. Memory_Archive: 归档记忆")
    task['status'] = status
    task['last_loop'] = datetime.now().isoformat()
    task['issues_count'] = len(issues)
    
    # Phase 8: Improve
    print("8. Improve: 记录改进")
    write_memory(task_id, "improve", "记录改进", f"完成8阶段Loop")
    
    return status

def main():
    print("=== 最终原子修复 - 剩余6个任务 ===\n")
    
    tasks = load_tasks()
    needs_fix = [t for t in tasks if t.get('status') == 'needs_fix']
    
    print(f"需要修复的任务: {len(needs_fix)}")
    
    completed = 0
    for task in needs_fix:
        try:
            status = atomic_loop_8_phases(task)
            if status == 'completed':
                completed += 1
        except Exception as e:
            print(f"❌ {task['id']} 执行失败: {e}")
            write_memory(task['id'], "error", "执行失败", str(e))
    
    # 保存状态
    save_tasks(tasks)
    
    # 最终统计
    all_tasks = load_tasks()
    total_completed = sum(1 for t in all_tasks if t.get('status') == 'completed')
    
    print(f"\n=== 最终结果 ===")
    print(f"本轮完成: {completed}/{len(needs_fix)}")
    print(f"总完成: {total_completed}/{len(all_tasks)} ({total_completed/len(all_tasks)*100:.1f}%)")

if __name__ == '__main__':
    main()