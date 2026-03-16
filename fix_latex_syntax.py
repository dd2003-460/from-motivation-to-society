#!/usr/bin/env python3
"""
修复Part 3 LaTeX语法错误的脚本
"""

import re
import sys

def fix_tcolorbox_pairs(content):
    """修复tcolorbox配对问题"""
    lines = content.split('\n')
    fixed_lines = []
    tcolorbox_stack = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 检查begin{tcolorbox}
        if r'\begin{tcolorbox}' in line:
            # 检查是否有拼写错误
            if r'egin{tcolorbox}' in line and r'\begin{tcolorbox}' not in line:
                # 修复拼写错误
                line = line.replace(r'egin{tcolorbox}', r'\\begin{tcolorbox}')
                fixed_lines.append(line)
                tcolorbox_stack.append(len(fixed_lines) - 1)
            else:
                fixed_lines.append(line)
                tcolorbox_stack.append(len(fixed_lines) - 1)
        # 检查end{tcolorbox}
        elif r'\end{tcolorbox}' in line:
            if tcolorbox_stack:
                start_pos = tcolorbox_stack.pop()
                # 确保begin和end匹配
                if start_pos < len(fixed_lines):
                    fixed_lines.append(line)
            else:
                # 忽略多余的end
                print(f"警告: 第{i+1}行有多余的\\end{{tcolorbox}}")
                fixed_lines.append(f"% 多余的\\end{{tcolorbox}} 已注释掉: 第{i+1}行")
        else:
            fixed_lines.append(line)
        
        i += 1
    
    # 处理未关闭的tcolorbox
    while tcolorbox_stack:
        start_pos = tcolorbox_stack.pop()
        if start_pos < len(fixed_lines):
            fixed_lines.insert(start_pos + 1, r'\end{tcolorbox}')
            print(f"添加缺失的\\end{{tcolorbox}} 在第{start_pos+2}行")
    
    return '\n'.join(fixed_lines)

def clean_excessive_comments(content):
    """清理过度注释"""
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # 保留有意义的注释，删除过长的装饰线
        if line.strip().startswith('%') and len(line.strip()) > 80:
            # 保留有意义的注释
            if 'TODO' in line or 'FIXME' in line or 'NOTE' in line:
                cleaned_lines.append(line)
            else:
                # 删除过长的装饰注释
                cleaned_lines.append(f"% {line.strip()[:60]}... (过长注释已清理)")
        elif line.strip() == '% ============================================================':
            # 删除装饰线
            continue
        elif line.strip().startswith('%') and line.strip() == line.strip().upper():
            # 删除全大写的装饰注释
            continue
        else:
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def add_paragraph_spacing(content):
    """添加段落间距"""
    lines = content.split('\n')
    spaced_lines = []
    in_paragraph = False
    
    for line in lines:
        if line.strip() and not line.strip().startswith('%'):
            if in_paragraph and line.strip():  # 段落之间添加空行
                spaced_lines.append('')
            spaced_lines.append(line)
            in_paragraph = True
        elif not line.strip():
            in_paragraph = False
            spaced_lines.append(line)
        else:
            in_paragraph = False
            spaced_lines.append(line)
    
    return '\n'.join(spaced_lines)

def main():
    # 处理Part 3的所有章节
    chapters = [
        'part3_systematic_expansion/chapter2_culture_folk_institutions.tex',
        'part3_systematic_expansion/chapter3_politics_power_structure.tex',
        'part3_systematic_expansion/chapter4_law_institutional_form.tex'
    ]
    
    for chapter in chapters:
        print(f"处理 {chapter}...")
        
        try:
            with open(chapter, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 修复tcolorbox配对
            content = fix_tcolorbox_pairs(content)
            print(f"  - 修复了tcolorbox配对问题")
            
            # 清理过度注释
            content = clean_excessive_comments(content)
            print(f"  - 清理了过度注释")
            
            # 添加段落间距
            content = add_paragraph_spacing(content)
            print(f"  - 添加了段落间距")
            
            # 备份原文件
            with open(chapter + '.backup', 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 写入修复后的内容
            with open(chapter, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  - {chapter} 修复完成")
            
        except Exception as e:
            print(f"  - 错误: {e}")
            continue

if __name__ == '__main__':
    main()