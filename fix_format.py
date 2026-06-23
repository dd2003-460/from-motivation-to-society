#!/usr/bin/env python3
"""
修复正则表达式问题并统一Part 3格式
"""

import re
import os

def unify_section_structure(content):
    """统一section结构"""
    # 移除中文section标题，只保留英文
    try:
        content = re.sub(r'\\section{([^}]+)\s*\(([^)]+)\)}', r'\\section{\2}', content)
        content = re.sub(r'\\subsection{([^}]+)\s*\(([^)]+)\)}', r'\\subsection{\2}', content)
    except:
        print("  - 警告: section结构统一遇到问题，跳过")
    
    return content

def add_empty_lines(content):
    """添加适当的空行分隔"""
    lines = content.split('\n')
    result_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 在主要环境之间添加空行
        if (line.strip().startswith(r'\begin{') and 
            any(env in line for env in ['motivation', 'logicmap', 'questionbox', 'readingnote'])):
            if result_lines and result_lines[-1].strip():
                result_lines.append('')
        
        result_lines.append(line)
        
        # 在主要环境结束之后添加空行
        if (line.strip().startswith(r'\end{') and 
            any(env in line for env in ['motivation', 'logicmap', 'questionbox', 'readingnote'])):
            if i + 1 < len(lines) and lines[i + 1].strip():
                result_lines.append('')
        
        i += 1
    
    return '\n'.join(result_lines)

def clean_extra_whitespace(content):
    """清理多余的空白"""
    # 将多个连续空行替换为单个空行
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    # 移除行尾多余空格
    lines = content.split('\n')
    lines = [line.rstrip() for line in lines]
    
    return '\n'.join(lines)

def main():
    # 处理Part 3的所有章节
    chapters = [
        'part3_systematic_expansion/chapter2_culture_folk_institutions.tex',
        'part3_systematic_expansion/chapter3_politics_power_structure.tex',
        'part3_systematic_expansion/chapter4_law_institutional_form.tex'
    ]
    
    for chapter in chapters:
        print(f"修复格式 {chapter}...")
        
        try:
            with open(chapter, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 统一section结构
            content = unify_section_structure(content)
            print(f"  - 统一了section结构")
            
            # 添加空行分隔
            content = add_empty_lines(content)
            print(f"  - 添加了段落间距")
            
            # 清理多余空白
            content = clean_extra_whitespace(content)
            print(f"  - 清理了多余空白")
            
            # 备份原文件
            with open(chapter + '.format_backup2', 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 写入修复后的内容
            with open(chapter, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  - {chapter} 格式修复完成")
            
        except Exception as e:
            print(f"  - 错误: {e}")
            continue

if __name__ == '__main__':
    main()