# 任务卡：动机社会 — 两版自然语言重写（2026-11-01）

## 用户指令原文
"这些都干完之后下一个是动机社会，原来版本和重构版都要用最自然的语言叙述，允许包含思考（因为有人味），允许写之前搜集点人类的prompt方便激活语感"

## 现状盘点（2026-11-01 实测）
- v1 (main/): 21416 words, main_flat.tex 可编译; main.tex 坏——appendix_V_math 引用 4 个不存在的附录子文件
- v2 (main2/): 5667 words, xelatex 编译通过 (893KB PDF), 17 个 subfile 全部就位
- 风格资产: skills/author-voice/SKILL.md + skills/motivation-society-style/SKILL.md + test/comparison.md (六法对比)
- test/fused/ 空——融合 prompt 还没做出来
- 当前问题: v1/v2 正文偏"讲座腔"——结构工整但缺作者第一人称的思考痕迹、犹豫、自我修正

## 执行步骤

### Step 1: 修复 v1 编译（前置，L0）
appendix_V_math.tex 里注释掉 4 个缺失的 \subfile 行。

### Step 2: 从语料提取"人类 prompt 素材"（激活语感用）
来源: ../author-voice-mining/outputs/user_corpus.jsonl (271条, TIER-1 95条 high_conf)
- 只取 TIER-1 探索轮（有思考痕迹: "我觉得…但是…"、"等等，这样不对"）
- 挑含自我修正/犹豫/不确定表达的片段
- 目标: 15-25 条短片段（50-200字），覆盖不同话题
- 产出: prompts/human-voice-excerpts.md

### Step 3: 构建融合 prompt（test/fused/ 补上）
基于 comparison.md 融合方向 + 新增"允许思考痕迹"规则:
- B+F 量化自检 + G 长文一致性 + I few-shot
- 每章至少 1-2 处作者暴露思考过程
- 产出: test/fused/writing-prompt-v3.md

### Step 4: 试写一章验证
选 v2 part4 chapter11_meme 试写 → ai-tell + 量化指标 + 人味密度对照
效果好→批量推；不好→调 prompt

### Step 5: 批量重写
v2: part1→part2→part3→part4→part5→附录
v1: 修编译后 part1→part2→part3→conclusion
每章: 读原稿→重写→ai-tell→量化自检→commit

## 验收标准
1. 两版 xelatex 编译 0 error
2. ai-tell 全书 0 命中
3. 每章 ≥1 处"思考痕迹"
4. 第一人称率 0.2-0.3
5. 句长 ≤40 字
6. 逻辑链检验通过
7. 用户确认试写章"有人味"才批量推

## 注意
- v1 Part I 作者亲笔只修自然度，Part II/III 可大改
- "允许思考"≠ 全倒出来——选择性暴露 1-2 处关键犹豫点
- 不破坏现有结构（motivation/logicmap/readingnote/questionbox）
