#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
detect_ai_tell.py — 动机社会项目去 AI 化检测器

方法（三类信号，来源见 lexicon.json 的 meta 字段）：
  1. 词表黑名单：正式连接词 / 空泛量化词 / 宏大比喻黑话 / 用力过猛最高级 /
     模糊魔法副词 / 英文 AI 腔词 / 套路填充语。
  2. 格式启发式：
     - over_bold：段落内 **加粗** 过多 → 等于没有重点
     - em_dash：单段破折号 —— 过多
     - not_x_but_y：『不是 X，而是 Y』戏剧化句式
     - from_x_to_y：『从 X 到 Y』虚假跨度
  3. 输出：每个文件列出 (行号, 类别, 命中度, 片段)，并给汇总计数。

本工具只做『提示』，不自动改写——最终是否改由人定。

用法：
  python3 detect_ai_tell.py <path> [<path> ...] [--json out.json] [--lexicon lexicon.json]
  <path> 可以是 .md 文件或目录（目录会递归扫描 *.md）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_LEXICON = Path(__file__).with_name("lexicon.json")

# 段落级启发式阈值（也可被 lexicon.json 的 heuristics 覆盖）
PARA_BOLD_MIN = 5
PARA_WORD_MIN = 40
BOLD_RATIO_MAX = 0.12
PARA_EMDASH_MIN = 3


def load_lexicon(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def iter_paragraphs(lines):
    """yield (start_line_1based, paragraph_text)。以空行分段。"""
    buf = []
    start = None
    for i, line in enumerate(lines, 1):
        if line.strip() == "":
            if buf:
                yield start, "\n".join(buf)
                buf = []
                start = None
        else:
            if not buf:
                start = i
            buf.append(line)
    if buf:
        yield start, "\n".join(buf)


def count_words(text: str) -> int:
    # 中文字符 + 连续英文/数字 都算词
    cjk = len(re.findall(r"[一-鿿]", text))
    latin = len(re.findall(r"[A-Za-z0-9]+", text))
    return cjk + latin


def is_table_line(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") or re.match(r"^\s*\|?[-:\s|]+\|?\s*$", s) is not None


def scan_file(path: Path, lex: dict) -> list:
    """返回 findings 列表，每项 {file, line, category, hit, snippet, severity}。"""
    findings = []
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")

    # 跳过 fenced code block 的行
    in_code = False
    code_lines = set()
    for i, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            code_lines.add(i)
            continue
        if in_code:
            code_lines.add(i)

    # ---- 词表匹配（逐行）----
    phrases = lex.get("categories", {})
    for i, line in enumerate(lines, 1):
        if i in code_lines:
            continue
        for cat, cfg in phrases.items():
            terms = cfg.get("terms", []) if isinstance(cfg, dict) else cfg
            sev = cfg.get("severity", "med") if isinstance(cfg, dict) else "med"
            for term in terms:
                if not term:
                    continue
                # 英文词大小写不敏感；中文按子串
                if term[0].isascii():
                    if term.lower() in line.lower():
                        findings.append(_mk(path, i, cat, term, line, sev))
                else:
                    if term in line:
                        findings.append(_mk(path, i, cat, term, line, sev))

    # ---- 段落级启发式 ----
    h = lex.get("heuristics", {})
    ob = h.get("over_bold", {})
    bold_min = int(ob.get("para_bold_min", PARA_BOLD_MIN))
    word_min = int(ob.get("para_word_min", PARA_WORD_MIN))
    ratio_max = float(ob.get("bold_ratio_max", BOLD_RATIO_MAX))
    em_min = int(h.get("em_dash", {}).get("para_emdash_min", PARA_EMDASH_MIN))
    nxb = h.get("not_x_but_y", {}).get("pattern")
    fxt = h.get("from_x_to_y", {}).get("pattern")

    for start, para in iter_paragraphs(lines):
        # 跳过纯代码块段落 / 表格段落（表格的加粗是结构，不算过度标记）
        if all(is_table_line(l) for l in para.split("\n") if l.strip()):
            continue
        if para.strip().startswith("```"):
            continue

        bolds = re.findall(r"\*\*.+?\*\*", para)
        words = count_words(para)
        # over_bold
        if len(bolds) >= bold_min or (words > word_min and words > 0
                                      and len(bolds) / max(words, 1) > ratio_max):
            findings.append(_mk(path, start, "over_bold",
                                 f"{len(bolds)}处加粗/{words}词", para, "med"))
        # em_dash
        em = para.count("——")
        if em >= em_min:
            findings.append(_mk(path, start, "em_dash",
                                 f"{em}处破折号", para, "low"))
        # not_x_but_y
        if nxb and re.search(nxb, para):
            findings.append(_mk(path, start, "not_x_but_y",
                                 "不是…而是…", para, "low"))
        # from_x_to_y
        if fxt and re.search(fxt, para):
            findings.append(_mk(path, start, "from_x_to_y",
                                 "从…到…", para, "low"))

    return findings


def _mk(path, line, cat, hit, line_text, sev):
    snippet = line_text.strip().replace("\n", " ")[:140]
    return {
        "file": str(path),
        "line": line,
        "category": cat,
        "hit": hit,
        "severity": sev,
        "snippet": snippet,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="动机社会 去 AI 化检测器")
    ap.add_argument("paths", nargs="+", help=".md 文件或目录")
    ap.add_argument("--lexicon", default=str(DEFAULT_LEXICON),
                    help="词表 JSON 路径（默认同目录 lexicon.json）")
    ap.add_argument("--json", dest="json_out", default=None,
                    help="把结果写成 JSON 到此路径")
    args = ap.parse_args(argv)

    lex = load_lexicon(Path(args.lexicon))
    files = []
    for p in args.paths:
        pp = Path(p)
        if pp.is_dir():
            files.extend(sorted(pp.rglob("*.md")))
        else:
            files.append(pp)

    all_findings = []
    per_file_counts = {}
    for f in files:
        fs = scan_file(f, lex)
        if fs:
            per_file_counts[str(f)] = len(fs)
            all_findings.extend(fs)

    # 控制台报告
    cat_names = {
        "connector_formal": "正式连接词",
        "quantifier_filler": "空泛量化词",
        "metaphor_cliche": "宏大比喻黑话",
        "superlative": "用力最高级",
        "magic_adv": "模糊魔法副词",
        "en_ai": "英文AI腔",
        "filler_cliche": "套路填充语",
        "over_bold": "过度加粗",
        "em_dash": "破折号过多",
        "not_x_but_y": "不是…而是…",
        "from_x_to_y": "从…到…",
    }
    print(f"扫描文件：{len(files)}，命中文件：{len(per_file_counts)}，"
          f"总命中：{len(all_findings)}\n")
    for f, n in sorted(per_file_counts.items(), key=lambda x: -x[1]):
        print(f"### {f}  ({n} 处)")
        for fd in all_findings:
            if fd["file"] != f:
                continue
            label = cat_names.get(fd["category"], fd["category"])
            print(f"  L{fd['line']:<4} [{fd['severity']:<4}] {label}: "
                  f"{fd['hit']}")
            print(f"          {fd['snippet']}")
        print()

    # 类别汇总
    cat_count = {}
    for fd in all_findings:
        cat_count[fd["category"]] = cat_count.get(fd["category"], 0) + 1
    print("== 类别汇总 ==")
    for c, n in sorted(cat_count.items(), key=lambda x: -x[1]):
        print(f"  {cat_names.get(c, c):<12} {n}")

    if args.json_out:
        Path(args.json_out).write_text(
            json.dumps({
                "files_scanned": len(files),
                "total": len(all_findings),
                "per_file": per_file_counts,
                "by_category": cat_count,
                "findings": all_findings,
            }, ensure_ascii=False, indent=2),
            encoding="utf-8")
        print(f"\nJSON 已写出：{args.json_out}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
