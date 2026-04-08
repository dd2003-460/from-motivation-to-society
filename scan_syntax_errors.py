#!/usr/bin/env python3
"""
语法错误扫描器 - 针对 LaTeX 和 Markdown 文件
错误类型:
1. 没换行: 行长度 > 80 字符
2. LaTeX 语法错误:
   - \begin{...} 与 \end{...} 不匹配
   - {} 配对错误
   - 特殊字符未转义（% 在非注释行）
3. Markdown 混入: 在 .tex 文件中出现 #、*、_ 等（非 LaTeX 命令）
"""

import os
import re
import json
from pathlib import Path

BASE_DIR = Path("/Users/chenglu/Desktop/写作/动机社会")
TARGET_DIRS = ["part2_geological_determinism", "part3_systematic_expansion"]
MAX_LINE_LENGTH = 80

def scan_file(filepath):
    issues = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    # 1. 检查每行长度
    for i, line in enumerate(lines, 1):
        line_no_tab = line.replace('\t', '    ')
        if len(line_no_tab.rstrip('\n')) > MAX_LINE_LENGTH:
            issues.append({
                "type": "line_too_long",
                "line": i,
                "length": len(line_no_tab.rstrip('\n')),
                "snippet": line_no_tab.rstrip('\n')[:100] + "..."
            })

    content = ''.join(lines)

    # 2. LaTeX 环境匹配 \begin{...} \end{...}
    begins = re.findall(r'\\begin\{([^}]+)\}', content)
    ends = re.findall(r'\\end\{([^}]+)\}', content)
    env_counts = {}
    for env in begins:
        env_counts[env] = env_counts.get(env, 0) + 1
    for env in ends:
        env_counts[env] = env_counts.get(env, 0) - 1
    for env, count in env_counts.items():
        if count != 0:
            issues.append({
                "type": "begin_end_mismatch",
                "environment": env,
                "balance": count,
                "detail": f"\\begin{{{env}}} 出现次数 - \\end{{{env}}} 出现次数 = {count}"
            })

    # 3. 大括号 {} 配对（简化版：逐字符扫描）
    brace_stack = []
    for i, ch in enumerate(content):
        if ch == '{':
            brace_stack.append(i)
        elif ch == '}':
            if brace_stack:
                brace_stack.pop()
            else:
                issues.append({
                    "type": "unmatched_brace",
                    "position": i,
                    "context": content[max(0, i-30):i+30]
                })
    # 检查未闭合的左括号
    if brace_stack:
        issues.append({
            "type": "unmatched_brace",
            "position": brace_stack[-1],
            "context": f"未闭合的 {{ 在位置 {brace_stack[-1]}"
        })

    # 4. 特殊字符 % 在非注释行且不是转义
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('%') or stripped == '':
            continue
        # 查找行内的 %（排除转义的\%）
        j = 0
        while j < len(line):
            if line[j] == '\\' and j+1 < len(line) and line[j+1] == '%':
                j += 2
                continue
            if line[j] == '%':
                # 找到 %，检查前面是否有 \ 转义
                issues.append({
                    "type": "unescaped_percent",
                    "line": i,
                    "snippet": line.rstrip('\n')
                })
                break
            j += 1

    # 5. Markdown 混入（检测 #、*、_、- 开头的行，除非是 LaTeX 命令）
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith('\\'):
            continue
        # 检测标题符号 #
        if stripped.startswith('#') and not stripped.startswith('\#'):
            issues.append({
                "type": "markdown_mixed",
                "line": i,
                "snippet": stripped[:80],
                "detail": "发现 MD 标题符号 #"
            })
        # 检测列表符号 * 或 -（简单判断）
        if (stripped.startswith('* ') or stripped.startswith('- ')) and not stripped.startswith('\*') and not stripped.startswith('\-'):
            issues.append({
                "type": "markdown_mixed",
                "line": i,
                "snippet": stripped[:80],
                "detail": "发现 MD 列表符号"
            })
        # 检测强调 _ 或 * 成对出现（简化）
        if '_' in line and not line.count('_') % 2 == 0:
            # 可能是 LaTeX 下标 _{}，暂时不报
            if not re.search(r'_[^\{]', line):
                pass
            else:
                issues.append({
                    "type": "markdown_mixed",
                    "line": i,
                    "snippet": stripped[:80],
                    "detail": "发现可能 MD 强调符号 _"
                })

    return issues

def main():
    results = {}
    total_issues = 0
    for target in TARGET_DIRS:
        dir_path = BASE_DIR / target
        if not dir_path.exists():
            results[target] = {"error": "directory not found"}
            continue
        tex_files = list(dir_path.rglob("*.tex"))
        results[target] = {
            "file_count": len(tex_files),
            "files": {}
        }
        for tex_file in tex_files:
            rel_path = str(tex_file.relative_to(BASE_DIR))
            issues = scan_file(tex_file)
            if issues:
                results[target]["files"][rel_path] = {
                    "issue_count": len(issues),
                    "issues": issues
                }
                total_issues += len(issues)
        # 文件摘要

    summary = {
        "scan_time": "2026-03-26T00:50+08:00",
        "base_dir": str(BASE_DIR),
        "targets": TARGET_DIRS,
        "total_issues": total_issues,
        "details": results
    }

    # 写入报告
    report_path = BASE_DIR / "syntax_issues_2026-03-26.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # 同时在 workspace 记忆库中保存一份
    mem_report = BASE_DIR.parent / ".openclaw" / "workspace-zero" / "memory" / "syntax_issues_2026-03-26.json"
    mem_report.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy(report_path, mem_report)

    print(f"Scan complete: {total_issues} issues found in {len(tex_files)} files")
    print(f"Report: {report_path}")

if __name__ == '__main__':
    main()
