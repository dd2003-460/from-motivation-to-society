# 风格提取仓库调研（test 分支实验）

> 目的：广泛搜集「从对话语料提取个人思维/语言风格」的仓库，对比它们**实际产出什么**，
> 再让 Arena 基于这些仓库在 `test/examples/` 产出多种风格的「第一章片段」示例，
> 与现有 main 第一章对比，最后融合各仓库优势。
> 本目录全部实验产物，**不触碰** main/、main2/、research/、skills/、src/。

---

## 0. 共享基线（公平对比用）

所有示例都重写同一段：**main 第一章 §1.1「一个最小的解释单元」**（文件
`main2/part1_motivation_goal/chapter1_motivation.tex` 第 27–67 行：
小孩问「为什么」→ 最小三件套（主体/动机/环境）→ 四个群体例子）。

该段已是「作者声音 + 多群体例子 + box」的成品，是评估其它方法的参照系。

---

## 1. 候选仓库总表

| # | 仓库 | 归属 | 方法类型 | 核心产出物 | 对写作适配 |
|---|---|---|---|---|---|
| A | `conversation-raw-materials` | 私有 dd2003-460 | 原料库 | 484 篇本人 + 11 篇朋友 cl 对话（md/json，按平台分目录） | 原料，非方法 |
| B | `author-voice-mining` | 私有 dd2003-460 | prompt/skill（角色校验） | `user_corpus.jsonl` + `voice_features.md` + `author-voice/SKILL.md` | ★★★★★ |
| C | `personal-health-profile` | 私有 dd2003-460 | 结构化抽取管线 | `health_profile.json`（10 类健康条目） | 方法可借鉴，目标不同 |
| D | `chat_analysis` | 私有 dd2003-460 | （弱/未实质开发） | 仅 README 39 字 + project/ | 待评估 |
| E | `self-skill`（公开） | lipG-waver | prompt（四层蒸馏） | System Prompt（量化指纹+质性采样） | ★★★★ |
| F | `ai-conversation-fingerprint`（公开） | sanasol | prompt/skill（细维度） | `STYLE_GUIDE.md` + `DETAILED_PROFILE.md` | ★★★★ |
| G | `ghostwrite`（公开） | brianruggieri | prompt（写作导向） | `voice-profile.md` | ★★★★★（专为写作） |
| H | `Digital-Self-Replica`（公开） | francescobrigante | 模型微调（QLoRA） | LoRA 检查点 | ★（不可控/不可编辑） |
| I | `Clone-A-Friend`（公开） | SwapnilRao619 | few-shot 提示 | 无独立产物（上下文内 persona） | ★★★ |
| J | 写作仓库自身 | 本仓库 | 既有资产 | `skills/author-voice`、`skills/motivation-society-style` §11–13、`src/ai-tell` | 基线 |

---

## 2. 逐仓库详解

### A. conversation-raw-materials（原料）
- 结构：`1-我/`（aistudio/arena/chatgpt/claude/deepseek/main/perplexity/unknown/zero/高质量对话）、`2-我的朋友cl/`、`index/`。
- 格式：markdown（`## 用户`/`## AI`）或 chat-tree JSON。
- **关键陷阱**（被 B 的方法论证）：导出数据的 role 字段普遍不可信——
  corpus_md 的 `## 用户` 混入约一半 AI 回答；high_quality 的 role 指错人（多方案例）。
- 结论：它是所有提取方法的**原料**，但必须先过 role 校验才能用。

### B. author-voice-mining（我们现有的作者声音挖掘）★最核心
- **方法创新 = 三级 role 校验 + user_likelihood 启发式**：
  - TIER-1 `raw_platform/**/*.json` 的 `messages[].role=="user"` 直接采信（黄金来源）。
  - TIER-2/3 用打分过滤：第一人称密度(+)、第三方指向(-)、问号/祈使(+)、>800字总结(-)、
    **AI 泄漏黑名单**（命中即大幅扣分：定位…找到了、值得注意的是、综上所述、需要指出的是…）。
  - 阈值 `user_likelihood>=0.6` 才保留；TIER-1 作已知真值种子校准。
- **实际产出（已验证）**：
  - `user_corpus.jsonl`：271 条用户原话（总字数 263,812）。
  - `voice_features.md` 量化特征：
    - 平均句长 **39.0 字**；轮长均值 973.5，p50=299，p90=2185。
    - 问号率 **0.413**，祈使句率 **0.513**，第一人称率 **0.675**。
    - 连接词频率：所以 220 / 但是 27 / 其实 26 / 不过 19 / 也就是说 6 / 换句话说 2。
    - 指令性:探索性 = 0.897；类比/生活例子轮占 51/271；「不是…而是…」96 次（0.36/千字）。
    - 口头禅 Top：一个/问题/质量/需要/模型/什么/可以/数据/结构/工具。
  - `author-voice/SKILL.md`：增强后的写作 skill（直接可喂给写作 agent）。
- **对写作的适配最高**：产出是可直接消费的 skill，且带真实数字、可核查。

### C. personal-health-profile（同方法、异目标）
- 管线：对话语料 → 按 10 类健康条目关键词匹配 → `health_profile.json`，每条带关键词/来源/上下文。
- **重要教训**：纯关键词误报率极高（276 文件 121 有信号，人工核对仅 5 条有效）；
  技术同形词（"注意力"=Transformer attention）是主要误报源。**真实使用必须人工核对。**
- 对风格提取的启示：量化特征也要人工校准，不能纯自动采信。

### D. chat_analysis（弱）
- 仅 README 39 字 + `project/`，无实质方法。列为待评估，不纳入示例生产。

### E. self-skill（公开，四层蒸馏）★★★★
- 流程：①数据清洗 → ②**量化指纹** → ③**质性采样** → ④人格合成（编码为 System Prompt）。
- Layer 2 量化维度：消息长度分布、高频句尾（"哈哈"/"吧"占比）、口头禅 Top12（占比>1% 写进 prompt）、
  表情偏好（[旺柴] vs 😂，频率）、标点使用率（40%=连珠炮型）。
- Layer 3 质性（人工读早/中/晚各 60 条）：句式（长/短句、反问密度）、灵魂层面习惯。
- **亮点**：量化+质性双轨；强调"连你自己都没注意到的习惯"——捕捉隐性风格。

### F. ai-conversation-fingerprint（公开，维度最细）★★★★
- 从 AI 聊天历史提取 messaging style fingerprint → 自动装为 Claude skill（100% 本地）。
- **提取维度（最细）**：大小写习惯、标点模式（省句号？省略号？）、语气（命令 vs 礼貌请求）、
  常用短语/开头、技术词汇、缩写（dont/cant/im/btw）、语法怪癖（掉冠词、缺主语）、
  填充词（just/actually/basically）、缩略风格（don't vs do not）、情绪标记（挫败/满意/急迫）。
- 产出：`STYLE_GUIDE.md`（喂 AI 用）+ `DETAILED_PROFILE.md`（全统计）+ 各 AI 集成文件。
- **亮点**：维度最细、自动化、直接生成可用 skill。

### G. ghostwrite（公开，专为写作）★★★★★
- 从 session logs 构建**量化 voice profile**（`voice-profile.md`）→ 应用到写作任务。
- 定位：写邮件/报告/文章时保持个人声音；load profile 即一致。
- **亮点**：唯一明确以"写长文保持声音"为目标的工具，直接命中本书需求。

### H. Digital-Self-Replica（公开，模型微调）
- QLoRA 微调 7B（DeepSeek-R1-Distill-Qwen-7B）模仿个人 WhatsApp 风格 → 数字分身。
- 方法类型：**模型微调**，需 GPU、不可解释、不可编辑。
- **对本书写作不适用**（我们要可控可编辑文本），但"微调克隆"可作融合方向的参考（不主推）。

### I. Clone-A-Friend（公开，少样本）
- 解析聊天记录 → 用朋友消息作 few-shot 例子做 persona priming。
- 方法类型：**少样本提示**，无需训练，但风格靠例子隐式传递、不稳定。

### J. 写作仓库自身资产（基线）
- `skills/author-voice`：作者声音（短句~40字、禁空话）。
- `skills/motivation-society-style` §11–13：拆块/例子密度/数学附录/总目标 K 因子/多版本。
- `src/ai-tell`：AI 痕迹检测器（反向——识别 AI 味，辅助评估示例成色）。

---

## 3. 对比维度矩阵

| 方法 | 类型 | 产出物 | 可控性 | 可解释 | 写作适配 | 数据需求 |
|---|---|---|---|---|---|---|
| B author-voice-mining | prompt/skill | SKILL.md+voice_features | 高 | 高 | ★★★★★ | 中（需 role 校验）|
| E self-skill | prompt | System Prompt | 高 | 高 | ★★★★ | 中 |
| F ai-conversation-fingerprint | prompt/skill | STYLE_GUIDE | 高 | 高 | ★★★★ | 低（自动化）|
| G ghostwrite | prompt | voice-profile | 高 | 中 | ★★★★★（专为写作）| 中 |
| H Digital-Self-Replica | 模型微调 | LoRA | 低 | 低 | ★ | 高+GPU |
| I Clone-A-Friend | few-shot | 无独立物 | 低 | 低 | ★★★ | 低 |

---

## 4. 对「写第一章」的启示（供 Arena 生产示例时参照）

各仓库最值得借的「维度」：
- **B**：用真实数字标定声音（句长/问号率/第一人称率），并以 role 校验保证提取的是「本人」而非 AI。
- **E**：量化指纹 + 质性采样双轨，捕捉隐性习惯（如反问密度）。
- **F**：最细的表层维度（标点/缩写/填充词/情绪标记），可直接写成约束清单。
- **G**：以「写长文保持声音」为目标的 profile 结构。
- **C 的教训**：任何自动提取都要人工核对，别盲信统计。

→ Arena 生产示例时，应**分别从每个仓库的方法视角**重写 §1.1，展示「用这种方法提取+应用」后
第一章长什么样，从而可比。
