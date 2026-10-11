# 动机社会 / 《谁在推动未来》重构项目

从 `from-motivation-to-society` 原书重构的写作工程。

## 目录结构

| 目录 | 内容 |
|---|---|
| `main/` | **v1 原书**（`main.tex` + 各 part 章节）。原书 Part I 为作者亲笔，Part II/III 为 AI 或合写。**保持原样不改动**。 |
| `main2/` | **v2 重构版**（`main2.tex` + 各 part 章节）。六段式：导论→动机→预测因果→法庭→四大齿轮→循环。当前按 v2 重写中。 |
| `skills/` | 写作规则技能：`author-voice`（作者口吻量化）、`motivation-society-style`（本书写作风格守则，含读者可读性、章末思考题、社科科普对标）。 |
| `archive/` | 历史归档：旧笔记（`notes/`）、大纲、补充材料、`loop-artifacts/`、`backups/`、项目状态。可逆保留，不作为书内容。 |

## v1 vs v2

- **v1（`main/`）**：原书结构，作者亲笔仅 Part I。
- **v2（`main2/`）**：砍掉 v1 的「演化状态空间」层，因果推断从「预测未来」内部长出；法律从通道升格为方法证明；导论用 2008 金融危机开场。详见 `main2/README.md`。

## 写作规则入口

`skills/motivation-society-style/SKILL.md` 是最高权威（提炼自原书 `part3_AI执行指导.md`，归档于 `archive/`）。作者口吻基准见 `skills/author-voice/SKILL.md`。

## 编译

```bash
cd main2 && xelatex main2.tex && xelatex main2.tex
cd ../main && xelatex main.tex && xelatex main.tex
```
