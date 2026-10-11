# notes/ — 过程笔记

| 文件 | 内容 |
|---|---|
| `search-log.md` | **检索式与渠道**：按 Q1–Q5 列出全部检索式、命中结果、失败尝试；含 7 条**纠错记录**（记错的 DOI / 期刊 / 题名）；含可复现的 OpenAlex / Semantic Scholar 检索模板 |
| `open-questions.md` | **未解问题**：7 个明确的证据缺口（每个都按「无」诚实标注，不是遗漏）；5 条待二次核实的数字；4 组方法学张力；下一轮研究的优先级排序；给写作侧的「待补证据」清单 |

---

## 一句话速览

- **沙箱网络限制**：bash 侧不能直连 OpenAlex / arXiv / Semantic Scholar API，**必须走 fetch_page 工具**。
- **最重要的教训**：DOI / 期刊 / 题名**一律不能凭记忆写**。本次纠出 4 处记忆错误（Cantoni 的 DOI、Bonnasse-Gahot 的期刊、Pennycook & Rand 的期刊、Banerjee 的题名），全部靠 OpenAlex 核验才发现。
- **最重要的发现**：`R0` 检索同时返回 >1 与 <1 的文献，逐条核对后确认差异源于**层级**（话题级 vs 内容级）——这是 synthesis §〇 的第一条。
