#!/usr/bin/env python3
"""
修复缺少"读者可能还会问"的subsection
"""

import re
import os
import shutil
from datetime import datetime

def backup_file(file_path):
    """备份文件"""
    os.makedirs("backups/reader_q", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = f"backups/reader_q/{os.path.basename(file_path)}.{ts}.bak"
    shutil.copy2(file_path, dst)
    return dst

def find_subsection_end(lines, start_idx):
    """找到subsection的结束位置（在下一个subsection或section之前）"""
    for i in range(start_idx, len(lines)):
        if r'\subsection{' in lines[i] or r'\section{' in lines[i]:
            return i
    return len(lines)

def add_reader_questions(file_path, subsection_title, questions):
    """在指定subsection末尾添加读者提问"""
    backup_file(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 找到subsection位置
    for i, line in enumerate(lines):
        if subsection_title in line and r'\subsection{' in line:
            # 找到subsection结束位置
            end_idx = find_subsection_end(lines, i + 1)
            
            # 在结束位置前插入读者提问
            reader_q_block = [
                '\n',
                '\\paragraph*{读者可能还会问}\n',
                '\\begin{itemize}\n'
            ]
            for q in questions:
                reader_q_block.append(f'\t\\item {q}\n')
            reader_q_block.append('\\end{itemize}\n')
            reader_q_block.append('\n')
            
            # 插入
            lines = lines[:end_idx] + reader_q_block + lines[end_idx:]
            
            # 写回
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            return True
    
    return False

def main():
    file_path = 'part2_geological_determinism/chapter1_materialist_historical_view.tex'
    
    # 需要修复的subsection和对应的读者提问
    fixes = [
        {
            'title': '地理环境作为不可变更的初始条件',
            'questions': [
                '为什么地理环境在历史分析中比文化更有解释力？',
                '如果地理如此重要，为什么同一地理环境下会产生不同制度？',
                '技术进步是否可以完全克服地理约束？',
                '为什么理解了地理的不可变更性，下一个问题就是"如何追溯因果链"？（指向下一小节：因果链条的回溯方法）'
            ]
        },
        {
            'title': '因果链条的回溯方法：如何识别输入变量',
            'questions': [
                '为什么回溯因果链比正向预测更可靠？',
                '如何区分"相关性"和"因果性"在历史分析中？',
                '为什么地理环境通常是因果链的最远端？',
                '为什么理解了回溯方法，下一个问题就是"如何验证这个框架"？（指向下一小节：地理→历史路径）'
            ]
        },
        {
            'title': '大分流之谜：为什么东方集权，西方分权？',
            'questions': [
                '为什么地理差异会导致如此不同的政治制度？',
                '治水需求在集权形成中到底有多重要？',
                '为什么欧洲不能像中国一样实现大一统？',
                '为什么理解了大分流现象，下一个问题就是"中国案例如何具体运作"？（指向下一小节：东方案例）'
            ]
        }
    ]
    
    print("=== 修复读者提问 ===\n")
    
    for fix in fixes:
        title = fix['title']
        questions = fix['questions']
        
        success = add_reader_questions(file_path, title, questions)
        if success:
            print(f'✅ 已修复: {title[:40]}')
        else:
            print(f'❌ 未找到: {title[:40]}')
    
    print(f'\n修复完成！备份保存在 backups/reader_q/')

if __name__ == '__main__':
    main()