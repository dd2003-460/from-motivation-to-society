# ai-tell — 动机社会去 AI 化检测器

把"AI 味"从书稿/研究文档里揪出来。只提示、不改写；改不改由人定。

## 方法（三类信号）

1. **词表黑名单**（见 `lexicon.json`）
   - 正式过渡连接词：`值得注意的是 / 综上所述 / 换言之 / 此外 / 首先…其次…最后 / 旨在…`
   - 空泛量化词：`广泛 / 全面 / 大幅 / 至关重要 / 前所未有 / 不容忽视…`
   - 宏大比喻黑话：`双刃剑 / 画卷 / 赛道 / 赋能 / 底层逻辑 / 组合拳…`
   - 用力过猛最高级：`最稳健 / 最致命 / 最狠 / 太狠 / 至极…`
   - 模糊魔法副词：`悄然 / 某种意义上 / 不容置疑…`
   - 英文 AI 腔：`delve / leverage / robust / pivotal / tapestry / in conclusion…`
   - 套路填充语：`讲真 / 坦白说 / 老实说…`

2. **格式启发式**
   - `over_bold`：段落内 `**加粗**` 过多（单段 ≥5 处，或长段加粗占比 >12%）→ **等于没标重点**
   - `em_dash`：单段破折号 `——` ≥3 处
   - `not_x_but_y`：`不是 X，而是 Y` 戏剧化句式
   - `from_x_to_y`：`从 X 到 Y` 虚假跨度修辞

3. **来源**：维基百科《Signs of AI writing》、朱雀 AI 检测规则、多篇去 AI 味指南（2026-10-11 检索整理）。

## 用法

```bash
# 扫描单个文件
python3 detect_ai_tell.py ../../research/synthesis.md

# 扫描整个目录（递归 *.md）
python3 detect_ai_tell.py ../../research/ ../../main2/versions/

# 输出 JSON（便于后续批量处理）
python3 detect_ai_tell.py ../../research/ --json /tmp/ai_tell_report.json
```

依赖：Python 3.8+，仅标准库（re / json / argparse / pathlib），无需 pip 安装。

## 设计原则

- **只提示不改写**：本工具输出"哪里像 AI"，最终改写由人（或按 `skills/author-voice` 风格）决定。
- **少误报**：已剔除本作者正当用词（闭环、基石、本质上、说白了、其实等），统计用词（"显著"）不列入自动命中，需结合上下文判断。
- **表格/代码块豁免**：Markdown 表格的加粗是结构、代码块是命令，均不参与过度加粗判定。

## 测试

```bash
python3 tests/test_detect.py
```
