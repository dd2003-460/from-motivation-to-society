# Arena Agent 派活 Prompt

> 这份 prompt 用于 arena.ai 的 Agent Mode（coding-agent）。
> 第一个代码块直接粘贴使用。第二个代码块是分阶段追加的任务卡。

---

## 一次性派活（Part I 完整 + 骨架搭好）

```
## 先做这一件事（最高优先级）

验证推送通道：你的第一个动作就是 git add -A && git commit -m "chore: verify push channel"
&& git push -u origin arena-refactor-v2，立刻推一次，哪怕只改一个 README 的一个字。

上一个会话的失败模式是：全部代码写完（N commits、M 测试绿）之后才第一次 push，
此时沙箱里的 GH_TOKEN 已经过期，git push 被拒，成果全丢。所以：
- 每完成一个子任务立即 commit + push，不要攒到最后。
- 如果 git push 或 gh 报认证错误，立刻在回复里明确写一行 `PUSH_FAILED: <原文错误>`，
  然后继续做下一个任务（不要停下来等我）。
- 不要因为 push 失败就跳过 commit。

分支名固定为 `arena-refactor-v2`。

---

## 任务：动机社会（from-motivation-to-society）结构重构

仓库是 `dd2003-460/from-motivation-to-society`。这是一本已成书的 LaTeX 著作，
作者要做一次**结构性重构**。你的任务是按下面的架构，把 Part I 写完，并把后续章节骨架搭好。

### 绝对禁止（违反即任务失败）

1. **禁止修改 `main.tex`**
2. **禁止修改任何原章节 .tex**：`part1_core_logic/*`、`part2_geological_determinism/*`、
   `part3_systematic_expansion/*`、`conclusion/*`、`frontmatter/*`、`backmatter/*`、
   `appendix/appendix_V_math.tex`
3. 禁止删除、重命名、移动原书任何文件
4. 禁止编译失败——每一步都要能编译

新内容只允许写入：
- `main2.tex`（新建，重构版独立入口）
- `draft/**`（新建，重构版章节）
- `notes/00-architecture.md`（我已提供，你只读不改）

**提交前必须跑 `git diff --stat`，在回复里贴出结果，证明原书文件零改动。**

### 必读材料（clone 后先读）

1. **`notes/00-architecture.md`** — 唯一结构权威。全书五部结构、每章每节内容、
   好奇心追问链、验收标准、写作规则，全部在里面。
2. **`补充材料/part3_AI执行指导.md`** — 原书作者亲笔写的 Part 3 执行指导，314 行。
   这是**写作方法的权威来源**。特别注意：
   - 第三节「Part 3 的正确逻辑链」的五层推导树
   - 第四节「章节写作的执行规则」5 条
   - 第五节「AI 的常见走偏与纠正方式」—— 你很可能会犯这 5 个里的某一个
   - 第七节：不要去"证明"三个命题，只描述并指向附录
3. **`part1_core_logic/introduction.tex`** — 正文语气基准。模仿它的节奏、口语化程度、
   敢用破折号打断的写法。

### 这次重构的实质

原书是**回溯**结构：地理 → 结构 → 经济/文化/政治/法律，问「为什么是这个结果」。
这个结构有两个致命问题（原书自己在 notes/review_report.md 里承认了）：
- 逻辑链在附录 V.2→V.3 断裂（正交化是空间的，条件概率是因果的，两者不同构）
- 四章并列而非嵌套，变成四个独立教科书的组合
- **没有预测能力**

新结构是**前向**：动机 → 目标 → 预测未来 → 条件概率定贡献 → 分解为模因/经济/政治/法律通道。
最终能回答「如果当初没有 X，今天会怎样」——反事实推演是预测的最小单元。

关键转向：原书问「为什么是这个结果」，新书问「**这个结果里各因素各占多少**」。

### 硬依赖（不要搞反顺序）

`Part II 状态空间 → Part III 条件概率`。条件概率必须定义在状态空间上，
不先定义「未来由什么构成」（物质/人/相互作用），概率无从定义。
这条边就是原书断裂点的修复。P2→P3 是硬依赖，不是并列。

### 写作铁律（违反即退回）

1. **每章开头必须是上一章遗留的问题**，不能说「本章讨论 X」。
   句式：「上一章我们看到……但这个『X』到底从哪里来？这就是 Y 诞生的问题。」
2. **每个新概念必须通过「加入一个约束」导出**，不得凭空引入。
   用这个句式：「如果 A 不需要 X，那它的性质是 P。但现在加入约束 X——
   这一步改变了所有性质，这就是 B 从 A 中分离出来的时刻。」
3. **每小节末尾必须有 `\paragraph*{逻辑衔接}`**，显式写「下一节将……」。
4. 每章必须有：`\begin{motivation}`（含上一章遗留问题）+ `\begin{logicmap}`（TikZ）
   + 至少一个 `\begin{reader_anticipation}`。
5. 每小节至少一个 `\begin{readingnote}`（"你有没有想过……"）。
6. 术语格式必须是 **中文（English）**，例如：信息级联（information cascade）。
7. 段落长度 < 300 字符。
8. **逻辑链自检**：相邻两段之间必须能插入一个「但是，为什么……」使逻辑无缝衔接。
   不能 ⇒ 补过渡段。这是原书方法论的核心，违反它等于违反整本书。

### 诚实性纪律（这条比风格规则更重要）

- 猜想就标 `\lowfreq{这是猜想，不是定理}`
- 不要"证明"介观统一论的三个命题，只描述并指向附录（原书第七节明令）
- 方法会失败的地方主动列出来
- 「我们能说什么 / 我们不能说什么」分开写
- **不确定该写什么的时候，停下来问我，不要用空话填充。**
  「值得注意的是」「综上所述」「显而易见」这类无信息量的过渡一律禁止。
  停下来问的成本远低于写出三段废话的成本。

### 交付范围（这次会话只做这些，不要超纲）

1. 建 `main2.tex` — 完整宏包配置 + 全部自定义环境（从 main.tex 复制，但**不要删改任何
   原文件**）。`fontset=none` 和 macOS 字体设置必须保留。
2. 建 `draft/frontmatter/preface_v2.tex` — 重构版前言。说明这本书和原书的关系、
   为什么重构、新结构怎么读。
3. 建 `draft/part1_motivation_goal/introduction_v2.tex` — 重构版引言。
   用原书 introduction.tex 的语气，但引入「预测未来」这个新目标。
4. **精写 Part I 两章**（这是本次会话的重头戏，要写满、写透）：
   - `draft/part1_motivation_goal/chapter1_motivation.tex` — 动机：解释的最小起点
   - `draft/part1_motivation_goal/chapter2_goal.tex` — 目标：把意向写成可比较的量
   按 `notes/00-architecture.md` 里 ch1、ch2 的小节表逐节写，每节都要有完整的
   readingnote / 反驳处理 / 逻辑衔接。追问链必须真的能"但为什么"接上。
5. 为 Part II–V 各章创建**带完整章节骨架的 .tex**：包含 `\chapter`、章首 motivation、
   logicmap、以及每小节的 `\section` + 追问链提示 + 空的逻辑衔接占位。
   **骨架里不要填充正文内容**——那是后续会话的事。但小节标题和追问链必须是最终版，
   不是占位符。
6. 建 `draft/appendix/appendix_v2_math.tex` — 数学附录骨架。至少要有
   条件概率链乘积分解、贡献分解表（$C_A = P(D|A) - P(D|\neg A)$）、多因一果交互项
   这三部分的正式推导。用原书 appendix 的环境风格。
7. 编译验证：跑 `xelatex main2.tex` 两遍，确保零错误。贴出编译输出。
   如果沙箱里没有 xelatex，**明确说"无法编译验证"**，不要谎称编译通过。

### 每章完成后

commit + push。commit message 用中文或英文都可以，格式：
`refactor(P1/ch1): 动机——解释的最小起点`

在回复里给我：
- 写完的章节清单 + 每章行数
- `git diff --stat` 证明原书零改动
- 编译结果（真编译了还是没编译，如实说）
- **你在写作过程中遇到的判断题**——比如某个追问链你不太确定是否成立，
  或者某个概念你找不到好的日常类比。这些我需要知道，因为架构可能需要调整。
  不要为了交差而隐藏这些。

现在开始。
```

---

## 分阶段追加任务卡（后续会话逐个发）

### 任务卡 A：Part II 全文

```
继续 arena-refactor-v2 分支。这次做 Part II（演化状态空间）三章精写：
- draft/part2_state_space/chapter3_state_triple.tex
- draft/part2_state_space/chapter4_survival.tex
- draft/part2_state_space/chapter5_evolution.tex

先读 notes/00-architecture.md 的 Part II 部分，逐节按追问链写。

特别提醒：§5.2「有压扩增 vs 无压扩增」是原书 part3_AI执行指导.md 里的核心分叉，
在原书它被埋在 Part 3 中间，新结构把它提升到 Part II 作为演化引擎的基础。
这是有意改动——原书没有本体论层，无法说明「未来由什么构成」。

原书材料接入点：
- 原书 part2 ch1 地理决定论 → 新 §3.1 物质层（原书的因降级为三元组中的一项）
- 原书 part2 ch2 生存策略分化 → 新 §4.3（人存约束下物质如何推出策略）

写完每章 commit + push，然后停下来。贴出判断题。
```

### 任务卡 B：Part III 全文（最关键）

```
继续 arena-refactor-v2。这次做 Part III 两章精写——**这是整个重构的核心，
原书的断裂点就在这里修复**：
- draft/part3_conditional_probability/chapter6_prediction_math.tex
- draft/part3_conditional_probability/chapter7_contribution.tex

原书断裂点诊断（notes/review_report.md）：
「V.2→V.3 衔接 weak：正交化（空间）vs 条件概率（因果）不同构」

新结构怎么修的：把因果方向统一。原书附录 V.3 把
P(结果|原因) 和 P(原因|结果) 两个方向混着用。新结构只允许
P(未来|现在) = P(R|C_0) = Π P(C_k|C_{k-1}) 单一方向，
每个因子是一个可测量接口。这样"贡献"才有定义。

§7.3 多因一果的交互项处理要特别小心：诚实说明 C_A + C_B 不等于总效应，
交互项必须显式处理，给出至少两种归因方案（Shapley / 边际贡献排序）并说明选择理由。
不要假装交互项可以随便分掉——那是最常见的糊弄。

§7 是全书最重要的技术内容，写慢一点没关系，不要为了推进而糊过去。
```

### 任务卡 C：Part IV 全文

```
继续 arena-refactor-v2。做 Part IV 五个文件：
- chapter8_channel_generator.tex  ← 必须先写完这个，它是后面四章的前提
- chapter9_meme.tex
- chapter10_economy.tex
- chapter11_politics.tex
- chapter12_law.tex

**核心风险：写成并列。这是原书最大的错误，也是你最容易犯的错误。**
原书作者在 part3_AI执行指导.md 里专门列了错误 1 和错误 3。

判定标准：每章开头第一段必须能明确说出「上一章遗留的问题」，
而且这个问题的答案必须依赖上一章的结论。如果一章可以独立阅读，
说明它被写成了并列，回去重写开头。

§10.1「加入稀缺约束」是本 Part 的枢纽节，必须完整写透：
复制（A→A+B）变转移（A→B）→ 无压扩增变有压扩增 → 总量守恒 → 零和博弈。
这是全书"分类原则必须先建立"的最重要实例。

§12.2「法律是 Part III 的现实应用」是全书两半的接合点，
要明确写出 §7 的 C_A = P(D|A) - P(D|¬A) 就是法律定责的公式。

§12.4 嵌套关系要用集合符号写出来，不能只用文字：
文化 ⊃ 经济 ⊃ 政治（按约束嵌套），法律为三者提供定量框架。
```

### 任务卡 D：Part V 全文 + 附录补全

```
继续 arena-refactor-v2。做 Part V 两章 + 补全数学附录：
- draft/part5_backtest/chapter13_forecast.tex
- draft/part5_backtest/chapter14_closure.tex
- draft/appendix/appendix_v2_math.tex（补全推导）

§13.3 有一个硬要求：**必须真实推导一个具体例子**。
不要写"假设某政策出台，某指标会上升"这种空话。要真的算：
给一个读者熟悉的社会事件，逐步算四通道的贡献分解，展示怎么得到概率判断。
这是全书唯一一次"演示如何用这本书"，抽象方法无法自证，必须靠例子。

§13.4 预测失败模式清单要列满 5 条以上。原书没有这一节，
但验收标准要求"少于 3 条说明没认真想失败"。认真想。

附录至少要有三部分完整推导：
- 条件概率链乘积分解 P(R|C_0) = Π P(C_k|C_{k-1})
- 贡献分解 C_A = P(D|A) - P(D|¬A)
- 多因一果交互项的数学处理
```

### 任务卡 E：编译验证与交叉引用审计

```
继续 arena-refactor-v2。这次不改内容，只做验证：

1. xelatex main2.tex 两遍，贴出完整编译输出。要求零错误。
2. 检查所有 \hyperref[...] 和 \mathlink{...}{...} 是否有对应 \label
3. 检查所有 TikZ logicmap 节点是否重叠
4. 检查所有 reader_anticipation 指向的章节是否真实存在
5. 检查原书文件零改动：git diff --stat 贴出结果
6. 对照 notes/00-architecture.md §5 验收标准，逐条自查：
   - 逐章五问
   - 全书四问
7. 列出**你自己发现的、这份架构可能存在的问题**。

第 7 条最重要。架构是我定的，你执行了一遍。如果你发现某处
"按这个架构写下去会写不出来"或者"这个结构会导致读者困惑"，
必须说出来。发现问题比完成进度有价值。
```
