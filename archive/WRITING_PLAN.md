# WRITING_PLAN.md - 写作子项目计划

**最后更新**: 2026-03-16 18:50 GMT+8  
**状态**: 反映真实磁盘状态

## 📊 实际磁盘状态

### Part 1: 核心逻辑 (core_logic)
| 章节 | 状态 | 文件 | 说明 |
|------|------|------|------|
| ch1_nature_motivation | ✅ 存在 | ch1_nature_motivation.tex | 4 sections, 10 subsections, 缺 questionbox 和 reader_anticipation |
| ch2_structure_efficiency | ✅ 存在 | ch2_structure_efficiency.tex | 4 sections, 17 subsections, 缺 reader_anticipation |
| ch3_language_information | ✅ 存在 | ch3_language_information.tex | 7 sections, 9 subsections, 缺 reader_anticipation |

**Part 1**: 3/3 章，部分章节框架元素缺失

### Part 2: 地质决定论 (geological_determinism)
| 章节 | 状态 | 文件 | 说明 |
|------|------|------|------|
| ch1_materialist_historical_view | ✅ 存在 | ch1_materialist_historical_view.tex | 3 sections, 11 subsections, 框架元素齐全 |
| ch2_survival_strategy_divergence | ✅ 存在 | ch2_survival_strategy_divergence.tex | 4 sections, 5 subsections, 框架元素齐全 |

**Part 2**: 2/2 章，✅ 基本合规

### Part 3: 系统展开 (systematic_expansion)
| 章节 | 状态 | 文件 | 说明 |
|------|------|------|------|
| ch1_economic_base | ✅ 存在 | chapter1_economic_base.tex | 5 sections, 17 subsections, ✅ 已补 reader_anticipation |
| ch2_culture_folk_institutions | ✅ 存在 | chapter2_culture_folk_institutions.tex | 5 sections, 13 subsections, ✅ 已补 reader_anticipation |
| ch3_politics_power_structure | ✅ 存在 | chapter3_politics_power_structure.tex | 3 sections, 3 subsections, ✅ 已修复逻辑衔接措辞 |
| ch4_law_institutional_form | ✅ 存在 | chapter4_law_institutional_form.tex | 3 sections, 6 subsections, 缺章级逻辑衔接 |
| ch5_system_integration | ❌ 缺失 | - | 总结章不存在 |

**Part 3**: 4/5 章，ch5 缺失

### Part 4 & Part 5
**状态**: ❌ 完全不存在

### 其他组件
| 组件 | 状态 | 文件 | 说明 |
|------|------|------|------|
| 结语 (conclusion) | ✅ 存在 | circular_closure.tex | 存在 |
| 附录 (appendix) | ✅ 存在 | 7 个文件 | 存在 |
| main.tex | ✅ 存在 | main.tex | 包含 9 个章节文件 |

**总章节数**: 9 个章节文件  
**总行数**: ~5,281 行 (含 appendix)

## 🔄 原子任务队列

### 已完成 (✅)
- [x] scaffold 任务: 39/39 completed, 0 pending
- [x] Part 3 ch1 + ch2: 补写 reader_anticipation (2026-03-16)
- [x] Part 3 ch3: 修复逻辑衔接措辞 (下一节→下一章) (2026-03-16)

### 待执行 (📋)

#### Part 1: 核心逻辑
- [ ] ch1_nature_motivation: 补写 questionbox (0 → 需要 1-2个)
- [ ] ch1_nature_motivation: 补写 reader_anticipation (0 → 需要 4-5个)
- [ ] ch2_structure_efficiency: 补写 reader_anticipation (0 → 需要 4-5个)
- [ ] ch3_language_information: 补写 reader_anticipation (0 → 需要 4-5个)

#### Part 3: 系统展开
- [ ] ch4_law_institutional_form: 补写 reader_anticipation (5 → 需要 4-5个)
- [ ] ch4_law_institutional_form: 补写章级逻辑衔接 → 全书结尾
- [ ] ch5_system_integration: 创建总结章（可选）

#### 全书级别
- [ ] 更新 main.tex 反映 ch5 缺失状态
- [ ] Part 1 双语术语补充
- ] Part 2 双语术语补充
- [ ] `\label{ch:neutral_evolution}` 缺失
- [ ] 最终编译验证（无 xelatex 环境）

## ⚠️ 关键发现

1. **WRITING_PLAN.md 严重失真** - 此前版本声称 Part 3: 5/5 章，实际仅 4 章
2. **Part 4 & Part 5 不存在** - 此前版本声称存在，实际磁盘状态完全缺失
3. **框架元素不完整** - 多个章节缺少 questionbox 和 reader_anticipation

## 📈 原则合规评估

| 原则 | 评估状态 | 说明 |
|------|---------|------|
| P1 Closed-Loop | 🟡 WARN | 无统一任务队列，原子任务无法持续追踪 |
| P2 Evidence Closure | 🟡 WARN | WRITING_PLAN.md 现在反映真实状态 |
| P3 Structural Orthogonality | 🟡 WARN | Part 1 ch3 7 sections vs 其他 4-5 |
| P4 Independent Assurance | PASS | 扫描报告持续产出 |
| P5 Stateful Continuity | 🟡 WARN | WRITING_PLAN.md 已更新反映真实状态 |

## 🎯 下一步计划

### 立即执行 (自主)
1. Part 1 ch1/ch2/ch3: 补写 reader_anticipation
2. Part 3 ch4: 补写 reader_anticipation 和章级逻辑衔接
3. 维持 cron 扫描频率

### 等待用户决策
1. Part 3 ch5 (总结章) 是否需要创建？
2. Part 4 (系统整合) 是否需要创建？
3. Part 5 (展望) 是否需要创建？
4. Part 1 的 questionbox 补充策略

---
*创建时间: 2026-03-16 18:50 GMT+8*  
*基于实际磁盘状态生成*