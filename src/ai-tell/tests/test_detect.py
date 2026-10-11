#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""detect_ai_tell.py 的最小契约测试：验证三类核心信号能命中、且放过正当用法。"""
import sys
import tempfile
from pathlib import Path

# 让脚本可被 import
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import detect_ai_tell as d  # noqa: E402


def _scan(text: str) -> list:
    p = Path(tempfile.mktemp(suffix=".md"))
    p.write_text(text, encoding="utf-8")
    lex = d.load_lexicon(ROOT / "lexicon.json")
    try:
        return d.scan_file(p, lex)
    finally:
        p.unlink()


def test_connector_hit():
    fs = _scan("综上所述，这一段值得注意。\n\n此外，我们还需考虑。")
    cats = {f["category"] for f in fs}
    assert "connector_formal" in cats, "应命中正式连接词"


def test_metaphor_hit():
    fs = _scan("道德化语言是一把双刃剑，需要赋能组织。")
    cats = {f["category"] for f in fs}
    assert "metaphor_cliche" in cats, "应命中宏大比喻黑话"


def test_superlative_hit():
    fs = _scan("这是最稳健的结论，也是最狠的一刀。")
    hits = [f["hit"] for f in fs]
    assert "最稳健" in hits and "最狠" in hits, "应命中用力最高级"


def test_over_bold_hit():
    # 单段塞 6 个加粗
    para = "**甲** 和 **乙** 与 **丙** 及 **丁** 同 **戊** 跟 **己** 都重要。"
    fs = _scan(para)
    cats = {f["category"] for f in fs}
    assert "over_bold" in cats, "应命中过度加粗"


def test_table_exempt():
    # 表格行多加粗不应判过度加粗
    table = "| **A** | **B** | **C** | **D** | **E** | **F** |\n|---|---|---|---|---|---|\n"
    fs = _scan(table)
    assert not any(f["category"] == "over_bold" for f in fs), "表格加粗应豁免"


def test_stats_significant_not_flagged():
    # 统计『显著』是正当用法，不应出现在自动命中
    fs = _scan("年龄效应依然显著（p<0.001），系数 0.02。")
    assert not any(f["category"] == "quantifier_filler" and f["hit"] == "显著"
                   for f in fs), "统计『显著』不应误报"


def test_author_voice_not_flagged():
    # 作者正当口语
    fs = _scan("说白了就是：这件事其实没那么复杂。")
    assert not any(f["category"] in ("filler_cliche", "connector_formal")
                   for f in fs), "说白了/其实 是作者正当口语，不应命中"


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
