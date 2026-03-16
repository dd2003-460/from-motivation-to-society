# 严格 5×5 结构分析与修复计划

## 📊 当前状态检查

### Part 2
| 章节 | Sections | 需要 | Subsections | 需要 | 状态 |
|------|----------|------|-------------|------|------|
| P2Ch1 | 3 | 5 | 11 | 25 | ❌ 缺2sec, 14sub |
| P2Ch2 | 4 | 5 | 5 | 25 | ❌ 缺1sec, 20sub |

### Part 3
| 章节 | Sections | 需要 | Subsections | 需要 | 状态 |
|------|----------|------|-------------|------|------|
| P3Ch1 | 5 | 5 | 17 | 25 | ❌ 缺8sub |
| P3Ch2 | 5 | 5 | 16 | 25 | ❌ 缺9sub |
| P3Ch3 | 3 | 5 | 3 | 25 | ❌ 缺2sec, 22sub |
| P3Ch4 | 3 | 5 | 6 | 25 | ❌ 缺2sec, 19sub |

## 🔧 修复策略

### 原则
1. **每个chapter必须有5个section**
2. **每个section必须有5个subsection**
3. **每个subsection必须有5个why段落**
4. **每个subsection必须有逻辑衔接和读者提问**

### 修复优先级
1. **P1**: Part 3是核心，优先修复
2. **P2**: Part 2需要补充sections
3. **P3**: 确保所有章节满足5×5结构

## 📋 详细修复任务

### P3Ch3 政治（最严重：3sec→5sec, 3sub→25sub）
需要新增：
- 2个新section
- 22个新subsection
- 每个subsection 5个why段落

### P3Ch4 法律（严重：3sec→5sec, 6sub→25sub）
需要新增：
- 2个新section
- 19个新subsection
- 每个subsection 5个why段落

### P2Ch1 地理决定论（中等：3sec→5sec, 11sub→25sub）
需要新增：
- 2个新section
- 14个新subsection

### P2Ch2 生存策略（轻度：4sec→5sec, 5sub→25sub）
需要新增：
- 1个新section
- 20个新subsection

## ⏰ Cron任务设置
- **频率**: 每2小时检查一次
- **任务**: 修复语法问题，统一格式参考Part 1
- **目标**: 确保所有章节满足5×5结构