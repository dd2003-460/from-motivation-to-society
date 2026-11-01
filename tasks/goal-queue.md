# 全局任务优先级队列（2026-11-01 更新）

> 排序: P1 实际问题 > P2 完成度低优先 > P3 可理解性。阻塞跳过不卡。
> 位置: motivation_society/tasks/goal-queue.md（全局唯一，跨项目）。

## 当前活跃

| # | 任务 | 项目 | 状态 | 备注 |
|---|------|------|------|------|
| 4 | 动机社会: v1编译修复 + meme章试写(H5+H6) | D1-writing | **done 2026-11-01** | cde82ed+后续commit, H5问题钩子+H6矛盾优先(§2改矛盾开头), xelatex 0err, 待用户验收 |

## 排队（按序）

| # | 任务 | 项目 | 前置 | 备注 |
|---|------|------|------|------|
| 5 | 动机社会: v2 全 17 章自然语言重写(v3 prompt H1-H6) | D1-writing | #4 用户验收 | 每章先花20-30%找真矛盾+双源验证, 有矛盾用矛盾开头否则问题钩子, 每章 commit |
| 6 | 动机社会: v1 Part II/III 重写 | D1-writing | #5 done | Part I 只微调 |
| 7 | bh 任务C: 遗迹MF+PISN间隙图 | bh-mass-spectrum | — | subagent 失败(本地模型循环), 改主会话做 |
| 8 | bh 任务A: 多红移BHMF+占据率两图 | bh-mass-spectrum | — | 同上 |
| 9 | ORF paper_en.tex 英文版 | 时钟与引力波响应 | — | 同上 |
| 10 | ORF Phase 3: 完整探测器 ORF 互校 | 时钟与引力波响应 | #9 done | eps=0 边界声明 |
| 11 | bh S3: 全天光锥分布 | bh-mass-spectrum | #7 done | 需全 9 树 |

## 已完成

| # | 任务 | 时间戳 | 产出 |
|---|------|--------|------|
| 4b | 动机社会: v1编译修复+meme章人味重写 | 2026-11-01 | commit 071dd1d, xelatex 0err |
| 1 | bh docstring 修复 (3 failed→0) | 2026-11-01 | commit 2a0c3fb, pytest 175 passed |
| 2 | pfb pre-commit hook 安装 | 2026-11-01 | commit 577773e |
| 3 | 压缩调参 (timeout 600, threshold 0.75) | 2026-11-01 | config.yaml patched |
| 4 | 动机社会前置: 语感素材+融合prompt+任务卡 | 2026-11-01 | commit c559c97 (test branch) |

## 维护模式（不主动推）

- pfb judge matrix（等数据积累）
- market-alpha options（已闭环）
- D1-gpu 矩阵修正（等 web-llm 登录）

## 规则
- 完成→标 done + 时间戳
- 新任务插入时重排
- 阻塞 >2h 跳过做下一个
- **subagent 在本地 27b 下不可靠（循环卡死），重活主会话直接做**
