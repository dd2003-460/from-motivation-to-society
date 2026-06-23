#!/usr/bin/env python3
"""
统一Part 3格式，模仿Part 1的风格
"""

import re
import os

def read_part1_style():
    """读取Part 1的格式标准"""
    part1_file = 'part1_core_logic/chapter3_language_information.tex'
    with open(part1_file, 'r', encoding='utf-8') as f:
        return f.read()

def unify_section_structure(content):
    """统一section结构"""
    # 移除中文section标题，只保留英文
    content = re.sub(r'\\section{([^}]+)\s*\(([^)]+)\)}', r'\\section{\2}', content)
    
    # 统一subsection格式
    content = re.sub(r'\\subsection{([^}]+)\s*\(([^)]+)\)}', r'\\subsection{\2}', content)
    
    return content

def add_empty_lines(content):
    """添加适当的空行分隔"""
    lines = content.split('\n')
    result_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 在主要环境之间添加空行
        if (line.strip().startswith('\\begin{') and 
            any(env in line for env in ['motivation', 'logicmap', 'questionbox', 'readingnote', 'tcolorbox'])):
            if result_lines and result_lines[-1].strip():
                result_lines.append('')
        
        result_lines.append(line)
        
        # 在主要环境结束之后添加空行
        if (line.strip().startswith('\\end{') and 
            any(env in line for env in ['motivation', 'logicmap', 'questionbox', 'readingnote', 'tcolorbox'])):
            if i + 1 < len(lines) and lines[i + 1].strip():
                result_lines.append('')
        
        i += 1
    
    return '\n'.join(result_lines)

def break_long_paragraphs(content):
    """分割长段落"""
    # 将过长的段落按句子分割
    sentences = re.split(r'([。！？；\n])', content)
    
    result = []
    current_paragraph = []
    
    for sentence in sentences:
        if sentence.strip():
            current_paragraph.append(sentence)
            
            # 如果句子结束且段落较长，分割段落
            if sentence in ['。', '！', '？', '；', '\n']:
                paragraph = ''.join(current_paragraph).strip()
                if len(paragraph) > 200:  # 超过200字符的段落
                    # 按逗号分割
                    parts = re.split(r'，', paragraph)
                    if len(parts) > 2:
                        result.extend(parts[:-1])
                        result.append(parts[-1])
                    else:
                        result.append(paragraph)
                else:
                    result.append(paragraph)
                current_paragraph = []
    
    return '\n'.join(result)

def replace_tcolorbox_with_readingnote(content):
    """将tcolorbox替换为readingnote以统一格式"""
    # 简单的替换，保持内容不变
    content = re.sub(
        r'\\begin{tcolorbox}\[colback=yellow!5,title=\\textit{读者行为预测}\]',
        '\\begin{readingnote}',
        content
    )
    content = re.sub(r'\\end{tcolorbox}', '\\end{readingnote}', content)
    
    return content

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
    
    # 读取Part 1格式作为参考
    part1_style = read_part1_style()
    
    for chapter in chapters:
        print(f"统一格式 {chapter}...")
        
        try:
            with open(chapter, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 统一section结构
            content = unify_section_structure(content)
            print(f"  - 统一了section结构")
            
            # 替换tcolorbox为readingnote
            content = replace_tcolorbox_with_readingnote(content)
            print(f"  - 统一了环境类型")
            
            # 添加空行分隔
            content = add_empty_lines(content)
            print(f"  - 添加了段落间距")
            
            # 分割长段落
            content = break_long_paragraphs(content)
            print(f"  - 分割了长段落")
            
            # 清理多余空白
            content = clean_extra_whitespace(content)
            print(f"  - 清理了多余空白")
            
            # 备份原文件
            with open(chapter + '.format_backup', 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 写入修复后的内容
            with open(chapter, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  - {chapter} 格式统一完成")
            
        except Exception as e:
            print(f"  - 错误: {e}")
            continue

if __name__ == '__main__':
    main()