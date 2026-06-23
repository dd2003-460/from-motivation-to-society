#!/usr/bin/env python3
"""
修复 LaTeX 语法错误 - 最小更改原则
- 只修复检测到的错误，不重写内容
"""

import re
import json
from pathlib import Path

BASE_DIR = Path("/Users/chenglu/Desktop/写作/动机社会")
REPORT_PATH = BASE_DIR / "syntax_issues_2026-03-26.json"

def fix_line_too_long(content, lines, max_len=80):
    """给长行插入软换行（优先在空格处换行）"""
    new_lines = []
    for line in lines:
        if len(line.rstrip('\n')) <= max_len:
            new_lines.append(line)
            continue
        # 在空格处断开
        broken_lines = []
        current = line.rstrip('\n')
        while len(current) > max_len:
            # 从 max_len 往前找空格
            split_pos = current.rfind(' ', 0, max_len)
            if split_pos == -1:
                split_pos = max_len  # 强拆
            broken_lines.append(current[:split_pos] + '\n')
            current = current[split_pos:].lstrip()
        broken_lines.append(current + '\n')
        new_lines.extend(broken_lines)
    return new_lines

def fix_unescaped_percent(lines):
    """给行内的 % 添加转义（非注释行，且前面无转义）"""
    new_lines = []
    for line in lines:
        if line.strip().startswith('%') or line.strip() == '':
            new_lines.append(line)
            continue
        # 替换未转义的 % 为 \%
        new_line = []
        i = 0
        while i < len(line):
            if line[i] == '\\' and i+1 < len(line) and line[i+1] == '%':
                new_line.append(line[i:i+2])
                i += 2
            elif line[i] == '%':
                new_line.append('\\%')
                i += 1
            else:
                new_line.append(line[i])
                i += 1
        new_lines.append(''.join(new_line))
    return new_lines

def main():
    if not REPORT_PATH.exists():
        print(f"Error: {REPORT_PATH} not found")
        return

    data = json.load(open(REPORT_PATH, encoding='utf-8'))
    # 统计优先级：先修复导致编译失败的
    targets = ["part2_geological_determinism", "part3_systematic_expansion"]

    for target in targets:
        info = data['details'].get(target, {})
        files = info.get('files', {})
        for rel_path, file_info in files.items():
            filepath = BASE_DIR / rel_path
            if not filepath.exists():
                continue
            # 读取原文件
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                original_lines = f.readlines()

            # 收集问题类型
            issue_types = [i['type'] for i in file_info['issues']]

            new_lines = original_lines

            # 1. 修复 % 转义（高优先级）
            if 'unescaped_percent' in issue_types:
                new_lines = fix_unescaped_percent(new_lines)
                print(f"[{target}] {rel_path}: fixed unescaped %")

            # 2. 修复长行（低优先级，可选）
            # 这里暂不自动换行，因为可能改变排版

            # 写回（如果有更改）
            if new_lines != original_lines:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                print(f" => {filepath} updated")

    print("Fix pass 1 complete (only unescaped %)")

if __name__ == '__main__':
    main()
