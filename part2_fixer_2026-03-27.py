#!/usr/bin/env python3
"""
Part2 语法修复器 - 基于问题报告精确修复
修复类型: markdown_mixed (MD列表符号), line_too_long (行超长)
"""

import json
import re
from pathlib import Path

BASE_DIR = Path("/Users/chenglu/Desktop/写作/动机社会")
REPORT_PATH = BASE_DIR / "syntax_issues_2026-03-26.json"

# 加载问题报告
with open(REPORT_PATH, 'r', encoding='utf-8') as f:
    report = json.load(f)

def fix_markdown_mixed(file_path, issues):
    """修复 markdown_mixed: 将 - 和 * 列表转换为 LaTeX itemize"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 收集需要修改的行
    item_lines = []
    for issue in issues:
        line_num = issue['line'] - 1
        snippet = issue['snippet']
        stripped = snippet.strip()
        if stripped.startswith('- ') or stripped.startswith('* '):
            item_lines.append(line_num)

    if not item_lines:
        return False

    # 找出连续的块
    item_lines_set = set(item_lines)
    visited = set()
    groups = []

    for line in sorted(item_lines):
        if line in visited:
            continue
        # 扩展这个块
        block = [line]
        visited.add(line)
        # 向前扩展
        prev = line - 1
        while prev in item_lines_set:
            block.insert(0, prev)
            visited.add(prev)
            prev -= 1
        # 向后扩展
        nxt = line + 1
        while nxt in item_lines_set:
            block.append(nxt)
            visited.add(nxt)
            nxt += 1
        groups.append(block)

    # 从后向前处理每个块（行号大的先处理，避免插入影响）
    groups.sort(reverse=True, key=lambda g: g[0])

    for block in groups:
        start = block[0]
        end = block[-1]

        # 检查是否已包裹
        already = False
        for i in range(max(0, start-3), start):
            if '\\begin{itemize}' in lines[i]:
                already = True
                break
        if not already:
            for i in range(end+1, min(len(lines), end+4)):
                if '\\end{itemize}' in lines[i]:
                    already = True
                    break
        if already:
            continue

        # 确定缩进（用起始行的缩进）
        indent_match = re.match(r'^(\s*)', lines[start])
        indent = indent_match.group(1) if indent_match else ''

        # 插入 \begin{itemize}
        lines.insert(start, f"{indent}\\begin{{itemize}}\n")
        # 修改块内的每一行，现在行号都+1了
        for i, orig_line in enumerate(block):
            actual = orig_line + 1  # 因为 begin 插入在原 start 前
            line = lines[actual]
            # 去掉列表符号
            new_content = re.sub(r'^[-*]\s*', '', line.lstrip())
            lines[actual] = f"{indent}  \\item {new_content}"
        # 插入 \end{itemize} 到块后
        end_insert = end + 1 + 1  # 原 end + begin插入 + 1（放在最后一行后）
        lines.insert(end_insert, f"{indent}\\end{{itemize}}\n")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    return True

def fix_line_too_long(file_path, issues, max_length=80):
    """修复超长行：在合适位置断行"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 按行号从大到小处理
    sorted_issues = sorted(issues, reverse=True, key=lambda x: x['line'])
    modified = False

    for issue in sorted_issues:
        line_num = issue['line'] - 1
        if line_num >= len(lines):
            continue
        line = lines[line_num]
        if len(line.rstrip('\n')) <= max_length:
            continue

        content = line.rstrip('\n')
        indent = re.match(r'^(\s*)', line).group(1)

        # 跳过 LaTeX 命令、数学环境、已有换行的段落等
        if '\\begin{' in content or '\\end{' in content or '\\textbf{' in content:
            continue
        # 如果包含数学公式，跳过
        if '$' in content:
            continue
        # 如果已经是短段落（比如多个空行分隔），跳过
        if content.strip() == '':
            continue

        # 寻找合适的断点：逗号、句号、分号、空格
        # 计算可接受的最大位置（不超过 max_length）
        target = max_length
        # 在超出位置之前寻找最近的断点
        candidates = [m.start() for m in re.finditer(r'[，。；！？]|\s+', content) if m.start() <= target]
        if not candidates:
            continue
        break_pos = candidates[-1]  # 最靠近 target 的断点

        if break_pos < 10:  # 断得太短
            continue

        line1 = content[:break_pos+1]
        line2 = content[break_pos+1:].lstrip()

        if line2:
            lines[line_num] = f"{indent}{line1}\n"
            lines.insert(line_num+1, f"{indent}{line2}\n")
            modified = True

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

    return modified

# 只处理 Part2
part2 = report['details']['part2_geological_determinism']
for rel_path, data in part2['files'].items():
    file_path = BASE_DIR / rel_path
    issues = data['issues']

    markdown_issues = [i for i in issues if i['type'] == 'markdown_mixed']
    longline_issues = [i for i in issues if i['type'] == 'line_too_long']

    print(f"\n=== {rel_path} ===")
    print(f"  markdown_mixed: {len(markdown_issues)}")
    print(f"  line_too_long: {len(longline_issues)}")

    if markdown_issues:
        print("  修复 markdown_mixed...")
        fix_markdown_mixed(file_path, markdown_issues)
    if longline_issues:
        print("  修复 line_too_long...")
        fix_line_too_long(file_path, longline_issues, max_length=80)

print("\nPart2 修复完成。")
