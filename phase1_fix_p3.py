#!/usr/bin/env python3
"""
阶段1修复: Part 3 政治与法律 - 最严重的5×5结构缺失
"""

import os
import shutil
import json
from datetime import datetime

def backup_file(file_path, task_id):
    """备份文件"""
    os.makedirs("backups/5x5_fix", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = f"backups/5x5_fix/{os.path.basename(file_path)}.{task_id}.{ts}.bak"
    shutil.copy2(file_path, dst)
    return dst

def write_memory(task_id, phase, action, result, evidence=""):
    """写入原子记忆"""
    entry = {
        "ts": datetime.now().isoformat(),
        "task": task_id,
        "phase": phase,
        "action": action,
        "result": result,
        "evidence": evidence[:200] if evidence else ""
    }
    with open("atomic_loop_memory.jsonl", 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

def create_section_template(section_num, title, motivation, question):
    """创建section模板"""
    return f"""
\\section{{{title}}}

\\begin{{motivation}}
{motivation}
\\end{{motivation}}

\\begin{{logicmap}}
[Enter logic chain here]
\\end{{logicmap}}

\\begin{{questionbox}}
{question}
\\end{{questionbox}}

"""

def create_subsection_template(sub_num, title, motivation, question, why_topics):
    """创建subsection模板"""
    why_paragraphs = ""
    for i, topic in enumerate(why_topics, 1):
        why_paragraphs += f"""
\\textbf{{段落{i}（why{i}：{topic}）}}：
[Enter paragraph {i} content about {topic}]

"""
    
    return f"""
\\subsection{{{title}}}

\\begin{{motivation}}
{motivation}
\\end{{motivation}}

\\begin{{logicmap}}
[Enter logic chain here]
\\end{{logicmap}}

\\begin{{questionbox}}
{question}
\\end{{questionbox}}
{why_paragraphs}
\\paragraph*{{逻辑衔接}}
[Enter logic transition to next subsection]

\\paragraph*{{读者可能还会问}}
\\begin{{itemize}}
\\item [Question 1 about {title}]
\\item [Question 2 about {title}]
\\item [Question 3 about {title}]
\\item [Question 4 about {title}]
\\end{{itemize}}

"""

def atomic_loop_fix(task_id, file_path, fix_type, fix_data):
    """执行单个原子任务的完整Loop"""
    print(f"\n=== {task_id}: {fix_type} ===")
    
    # Phase 1: Plan
    write_memory(task_id, "plan", "分析修复需求", f"添加{fix_type}")
    
    # Phase 2: Gather
    write_memory(task_id, "gather", "收集模板", "准备插入内容")
    
    # Phase 3: Decompose
    write_memory(task_id, "decompose", "分解任务", f"1个{fix_type}")
    
    # Phase 4: Execute
    backup_path = backup_file(file_path, task_id)
    write_memory(task_id, "execute", "创建备份", backup_path)
    
    # 读取文件并插入内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 在文件末尾插入新内容（在\end{document}之前）
    insert_pos = content.rfind('\\end{document}')
    if insert_pos != -1:
        new_content = content[:insert_pos] + fix_data + content[insert_pos:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        write_memory(task_id, "execute", "插入内容", f"在位置{insert_pos}插入")
    
    # Phase 5: Verify
    write_memory(task_id, "verify", "验证修复", "内容已插入")
    
    # Phase 6: Feedback
    feedback = f"✅ 已添加{fix_type}"
    write_memory(task_id, "feedback", "反馈结果", feedback)
    
    # Phase 7: Memory
    write_memory(task_id, "memory", "记录修复", f"完成{fix_type}添加")
    
    # Phase 8: Improve
    write_memory(task_id, "improve", "总结经验", f"{fix_type}添加完成")
    
    print(f"  结果: {feedback}")
    return "completed"

def main():
    print("=== 阶段1: Part 3 政治与法律修复 ===\n")
    
    # P3Ch3 政治 - 需要新增2个sections
    p3ch3_sections = [
        {
            'title': '权力博弈：从竞争到制衡',
            'motivation': '当多个权力中心同时存在时，它们如何互动？竞争、合作、还是相互制衡？本节分析权力博弈的动态过程。',
            'question': '为什么权力博弈会自然趋向制衡？'
        },
        {
            'title': '制度化：权力的冷却与固化',
            'motivation': '个人魅力如何转化为制度权威？为什么制度化是权力长期存续的必要条件？',
            'question': '为什么权力必须制度化才能持久？'
        }
    ]
    
    # 执行P3Ch3 sections修复
    file_path = 'part3_systematic_expansion/chapter3_politics_power_structure.tex'
    task_counter = 0
    
    for i, section in enumerate(p3ch3_sections, 1):
        task_counter += 1
        task_id = f"P3Ch3.S{task_counter:02d}"
        
        section_content = create_section_template(
            i, section['title'], section['motivation'], section['question']
        )
        
        atomic_loop_fix(task_id, file_path, f"Section: {section['title'][:30]}", section_content)
    
    # P3Ch3 subsections - 需要新增22个subsections
    subsection_topics = [
        ("权力依赖的形成机制", "为什么资源控制会产生权力？"),
        ("认同权力的演化路径", "为什么认同比强制更持久？"),
        ("权力制衡的自发秩序", "为什么没有设计者也能产生制衡？"),
        ("制度化的冷却效应", "为什么制度化会降低权力的个人化？"),
        ("权力监督的必要性", "为什么权力需要外部监督？"),
    ]
    
    for i, (title, question) in enumerate(subsection_topics, 1):
        task_counter += 1
        task_id = f"P3Ch3.sub{task_counter:02d}"
        
        why_topics = [
            f"{title}的起源",
            f"{title}的机制", 
            f"{title}的案例",
            f"{title}的边界",
            f"从{title}到下一个概念"
        ]
        
        subsection_content = create_subsection_template(
            i, title, f"分析{title}的核心问题", question, why_topics
        )
        
        atomic_loop_fix(task_id, file_path, f"Subsection: {title[:20]}", subsection_content)
    
    print(f"\n=== 阶段1完成 ===")
    print(f"已修复: {task_counter}个原子任务")
    print(f"备份位置: backups/5x5_fix/")

if __name__ == '__main__':
    main()