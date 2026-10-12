# test 分支实验：风格提取仓库对比 → 融合

> 目标：对比「从对话语料提取个人思维/语言风格」的各仓库，看它们产出的结果有何不同，
> 据此在写作仓库里产出示例、与 main 第一章对比、再融合优势。
> **本目录所有产物都在 `test/` 下，不改动 main/ main2/ research/ skills/ src/。**

## 四阶段闭环

1. **仓库调研** → `test/survey.md`（已完成）：列出 A–J 共 10 个仓库，含方法、实际产出、对比矩阵。
2. **生产示例** → `test/examples/`：Arena 基于 survey 中各仓库，对 `test/excerpt.md` 的 §1.1 片段
   各产出一个重写版本（每个来源/方法一个文件）。
3. **对比 main 第一章** → `test/comparison.md`：逐方法评估「作者声音 / 少 AI 味 / 多例子 / 共鸣」维度，
   给出推荐。
4. **融合优势** → `test/fused/`：基于对比结论，融合多仓库优势，产出融合版 prompt/技能草稿 + 一个融合示例章节。

## 共享基线
所有示例统一重写 `test/excerpt.md`（= 第一章 §1.1），保证可比。

## 目录
- `survey.md` — 仓库调研
- `excerpt.md` — 共享基线片段
- `examples/` — Arena 产出的多风格示例
- `comparison.md` — 对比评估（阶段 3）
- `fused/` — 融合方案与示例（阶段 4）
