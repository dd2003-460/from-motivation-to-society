#!/usr/bin/env python3
"""
执行计划：一次性完成Part 3 LaTeX修复
"""

import os
import shutil
from datetime import datetime

def create_backups():
    """创建多重备份"""
    chapters = [
        'part3_systematic_expansion/chapter2_culture_folk_institutions.tex',
        'part3_systematic_expansion/chapter3_politics_power_structure.tex',
        'part3_systematic_expansion/chapter4_law_institutional_form.tex'
    ]
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backups_{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)
    
    for chapter in chapters:
        if os.path.exists(chapter):
            shutil.copy2(chapter, f"{backup_dir}/{os.path.basename(chchapter)}")
            print(f"备份: {chapter} -> {backup_dir}/")
    
    return backup_dir

def validate_latex_syntax(content):
    """验证LaTeX语法"""
    errors = []
    lines = content.split('\n')
    
    # 检查tcolorbox配对
    tcolorbox_stack = []
    for i, line in enumerate(lines, 1):
        if r'\\begin{tcolorbox}' in line:
            tcolorbox_stack.append(i)
        elif r'\\end{tcolorbox}' in line:
            if not tcolorbox_stack:
                errors.append(f"第{i}行: 多余的\\end{{tcolorbox}}")
            else:
                tcolorbox_stack.pop()
    
    if tcolorbox_stack:
        errors.extend([f"未关闭的tcolorbox: 第{line}行" for line in tcolorbox_stack])
    
    return errors

def validate_format_consistency(content):
    """验证格式一致性"""
    issues = []
    
    # 检查section结构
    if r'\\section{' not in content:
        issues.append("缺少section结构")
    
    # 检查环境使用
    tcolorbox_count = content.count(r'\\begin{tcolorbox}')
    if tcolorbox_count > 0:
        issues.append(f"仍有{tcolorbox_count}个tcolorbox未替换")
    
    return issues

def validate_paragraph_quality(content):
    """验证段落质量"""
    issues = []
    
    # 检查段落长度
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
    long_paragraphs = [p for p in paragraphs if len(p) > 300]
    
    if long_paragraphs:
        issues.append(f"有{len(long_paragraphs)}个长段落需要分割")
    
    # 检查空行数量
    empty_lines = content.count('\n\n')
    if empty_lines < 100:  # 基本空行数量
        issues.append(f"空行数量不足({empty_lines})")
    
    return issues

def main():
    print("=== Part 3 LaTeX修复执行计划 ===")
    
    # 1. 创建备份
    print("1. 创建备份...")
    backup_dir = create_backups()
    print(f"   备份目录: {backup_dir}")
    
    # 2. 执行修复
    print("2. 执行修复...")
    
    # 3. 验证结果
    print("3. 验证结果...")
    
    chapters = [
        'part3_systematic_expansion/chapter2_culture_folk_institutions.tex',
        'part3_systematic_expansion/chapter3_politics_power_structure.tex',
        'part3_systematic_expansion/chapter4_law_institutional_form.tex'
    ]
    
    for chapter in chapters:
        print(f"\n验证 {chapter}:")
        
        try:
            with open(chapter, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 语法检查
            syntax_errors = validate_latex_syntax(content)
            print(f"  - 语法错误: {len(syntax_errors)}个")
            
            # 格式检查
            format_issues = validate_format_consistency(content)
            print(f"  - 格式问题: {len(format_issues)}个")
            
            # 段落检查
            paragraph_issues = validate_paragraph_quality(content)
            print(f"  - 段落问题: {len(paragraph_issues)}个")
            
            total_issues = len(syntax_errors) + len(format_issues) + len(paragraph_issues)
            print(f"  - 总问题数: {total_issues}")
            
            if total_issues == 0:
                print(f"  - ✅ {chapter} 验证通过")
            else:
                print(f"  - ❌ {chapter} 需要进一步修复")
                
        except Exception as e:
            print(f"  - ❌ 检查失败: {e}")

if __name__ == '__main__':
    main()