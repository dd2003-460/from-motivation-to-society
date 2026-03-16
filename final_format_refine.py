#!/usr/bin/env python3
"""
最终格式完善：统一环境类型，完善排版
"""

import re

def replace_tcolorbox_with_readingnote(content):
    """将tcolorbox替换为readingnote"""
    # 替换begin
    content = re.sub(
        r'\\begin{tcolorbox}\[colback=yellow!5,title=\\textit{读者行为预测}\]',
        '\\begin{readingnote}',
        content
    )
    
    # 替换end
    content = re.sub(r'\\end{tcolorbox}', '\\end{readingnote}', content)
    
    return content

def add_section_structure(content):
    """添加section结构"""
    # 如果没有section，添加基本的section结构
    if r'\section{' not in content:
        lines = content.split('\n')
        new_lines = []
        
        # 添加chapter标题后立即添加section
        for i, line in enumerate(lines):
            new_lines.append(line)
            
            # 在chapter后添加section
            if r'\chapter{' in line and i + 1 < len(lines):
                if not lines[i + 1].strip().startswith(r'\section{'):
                    new_lines.append('')
                    new_lines.append(r'\section{Main Section}')
                    new_lines.append('')
        
        content = '\n'.join(new_lines)
    
    return content

def refine_paragraph_spacing(content):
    """优化段落间距"""
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # 在主要环境前后添加空行
        if (line.strip().startswith(r'\begin{') and 
            any(env in line for env in ['motivation', 'logicmap', 'questionbox', 'readingnote'])):
            if i + 1 < len(lines) and not lines[i + 1].strip():
                new_lines.append('')
        
        if (line.strip().startswith(r'\end{') and 
            any(env in line for env in ['motivation', 'logicmap', 'questionbox', 'readingnote'])):
            if i + 1 < len(lines) and lines[i + 1].strip():
                new_lines.append('')
    
    return '\n'.join(new_lines)

def main():
    chapters = [
        'part3_systematic_expansion/chapter2_culture_folk_institutions.tex',
        'part3_systematic_expansion/chapter3_politics_power_structure.tex',
        'part3_systematic_expansion/chapter4_law_institutional_form.tex'
    ]
    
    for chapter in chapters:
        print(f"最终完善 {chapter}...")
        
        try:
            with open(chapter, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 替换tcolorbox为readingnote
            content = replace_tcolorbox_with_readingnote(content)
            print(f"  - 统一了环境类型")
            
            # 添加section结构
            content = add_section_structure(content)
            print(f"  - 完善了section结构")
            
            # 优化段落间距
            content = refine_paragraph_spacing(content)
            print(f"  - 优化了段落间距")
            
            # 备份并写入
            with open(chapter + '.final_backup', 'w', encoding='utf-8') as f:
                f.write(content)
            
            with open(chapter, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  - {chapter} 最终完善完成")
            
        except Exception as e:
            print(f"  - 错误: {e}")

if __name__ == '__main__':
    main()