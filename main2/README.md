# main2/ — v2 重构版《谁在推动未来》

动机社会重构版。与 `../main/`（v1）完全独立，章节文件不改动 v1。

## 一、书籍结构（六段式：导论 + 五部）

| 位置 | 标题 | 核心问题 | 对应文件（`main2/` 下） |
|---|---|---|---|
| 导论 | 为什么算得最准的人，预测得最离谱 | 引入「预测未来」目标，2008 危机开场 | `frontmatter/preface_v2.tex` + `part1_motivation_goal/introduction_v2.tex` |
| Part I | 驱动未来的引擎：动机与目标 | 预测未来得先看人想要什么 | `part1_motivation_goal/chapter1_motivation.tex`、`chapter2_goal.tex` |
| Part II | 谁是真正的推手：预测与因果 | 凭什么能预测？因果。相关≠原因 | `part2_prediction_causality/chapter6_prediction_cause.tex`、`chapter7_correlation_causation.tex` |
| Part III | 法庭上的时光机：多因分账 | 一堆原因搅一起怎么算？法律界早跑通了 | `part3_courtroom/chapter8_butfor_test.tex`、`chapter9_multiple_causes.tex` |
| Part IV | 社会的四大齿轮：观念、经济、权力、法律 | 社会因果具体长啥样，拆四个通道 | `part4_gears/chapter10_channel_generator.tex`、`chapter11_meme.tex`、`chapter12_economy.tex`、`chapter13_politics.tex`、`chapter14_law.tex` |
| Part V | 回到循环：预测如何改变预测 | 预测出的未来塑造新动机 | `part5_loop/chapter15_forecast.tex`、`chapter16_closure.tex` |
| 附录 | 数学 | 条件概率框架形式化 | `appendix/appendix_v2_math.tex` |

> ⚠️ `main2.tex` 里的 `\subfile` 路径是**权威章节划分**。写正文时按这些文件名在 `main2/` 下建 / 改 `.tex`，**不要写在 `draft/` 里**——`draft/` 只是早期旧草稿原料（v1 框架文字「解释的起点」），仅作参考。

## 二、写作约束（最高优先级）

### A. 读者易懂性 —— 对标著名社科科普
只借「怎么写得让人读得下去」，**不借结构**。标杆：《人类简史》《枪炮、病菌与钢铁》《思考，快与慢》。
- 叙事驱动：每个抽象概念先给具体人物 / 事件 / 场景，再抽规律。禁止一上来就定义。
- 反直觉钩子：章 / 节首用「多数人以为 X，其实……」勾人。
- 比喻落地：类比必须配具体例子。
- 少术语、晚公式：Part I–II 零公式；公式从 Part III 起且前必有真实案例（详见 `../skills/motivation-society-style/SKILL.md` 第八节）。

### B. 逻辑与动机衔接 —— 本书原创方法论（必须保留）
- 每段要是上一句「但是，为什么……」的答案（前向推导链）。
- 每章开头必须是上一章遗留的问题（`\begin{motivation}` 引用上章未解问题）。
- 每小节末尾必须有 `\paragraph*{逻辑衔接}` 显式写「下一节将……」。
- Part I / II 末尾埋「微观如何汇聚成宏观」追问，Part IV 开头正面回答（成对，不许只埋不收）。

### C. 章末思考题（2026-10-11 新增，结构必需）
每章末尾 1–3 道 `thinkbox` 思考题，引导读者用本书方法自己推真实 / 反事实问题；至少一道反事实推演。详见 `../skills/motivation-society-style/SKILL.md` 第十节。`main2.tex` 已定义 `thinkbox` 环境。

### D. 作者声音
语气按 `../skills/author-voice/SKILL.md`：短句（~40 字）、第一人称落在决策上、口语精确、少用「换句话说」、禁用 `值得注意的是 / 综上所述`。**Part I 才是作者亲笔可靠依据**，书正文（Part II/III）不可当作者声音学。

## 三、当前进度与待办

- `main2.tex`：六段式 scaffold 已就绪（含 `thinkbox` 环境定义）。
- `draft/`：Arena 早期草稿（v1 框架文字「解释的起点」），偏 AI 味，**需按 v2 + A–D 约束重写**，内容可作原料参考。
- **待续写**：按 `main2.tex` 的章节文件名，逐章写 / 改正文，套用 A–D 约束 + 每章 `thinkbox`。

## 四、Arena 续写简报（任务说明摘要）

Arena 应：
1. 读 `../skills/motivation-society-style/SKILL.md`（重点：第八 / 十 / 十一节）与 `../skills/author-voice/SKILL.md`。
2. 以 `main2.tex` 的 `\subfile` 路径为权威，在 `main2/` 下逐章写对应 `.tex`（与引用文件名一致）。
3. 参考 `draft/` 旧稿内容，但**重写**为：读者易懂（对标社科科普）、逻辑衔接、每章带 `thinkbox` 思考题的版本。
4. 保证 `xelatex main2.tex` 能编译出 PDF。

> 详细执行指令见派发 Arena 时的 prompt；本文件是「总纲要 + 约束」，不替代 skill。
