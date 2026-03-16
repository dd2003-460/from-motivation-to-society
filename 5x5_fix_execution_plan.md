# 5×5 结构修复执行计划

## 📊 修复需求统计
- **新Sections**: 7个
- **新Subsections**: 92个
- **总计**: 99个最小原子任务

## 🎯 修复优先级

### P1: Part 3 政治与法律（最严重）
**P3Ch3 政治**: 2新sec + 22新sub = 24个原子任务
**P3Ch4 法律**: 2新sec + 19新sub = 21个原子任务

### P2: Part 2 地理决定论
**P2Ch1**: 2新sec + 14新sub = 16个原子任务
**P2Ch2**: 1新sec + 20新sub = 21个原子任务

### P3: Part 3 经济与文化（较轻）
**P3Ch1**: 0新sec + 8新sub = 8个原子任务
**P3Ch2**: 0新sec + 9新sub = 9个原子任务

## 🔧 最小原子Loop执行框架

### 每个原子任务的8阶段Loop
1. **Plan**: 分析缺失的section/subsection内容
2. **Gather**: 收集相关理论和案例
3. **Decompose**: 分解为5个why段落
4. **Execute**: 创建内容并插入
5. **Verify**: 检查语法和格式
6. **Feedback**: 记录修复结果
7. **Memory**: 写入atomic_loop_memory.jsonl
8. **Improve**: 优化后续修复

### 备份策略
- 每个原子任务执行前创建备份
- 备份路径: backups/5x5_fix/[章节]/[任务ID].bak
- 支持回滚到修复前状态

## 📋 执行顺序

### 阶段1: Part 3 政治与法律（45个任务）
1. P3Ch3 新增2个section
2. P3Ch3 新增22个subsection
3. P3Ch4 新增2个section  
4. P3Ch4 新增19个subsection

### 阶段2: Part 2 地理决定论（37个任务）
1. P2Ch1 新增2个section
2. P2Ch1 新增14个subsection
3. P2Ch2 新增1个section
4. P2Ch2 新增20个subsection

### 阶段3: Part 3 经济与文化（17个任务）
1. P3Ch1 新增8个subsection
2. P3Ch2 新增9个subsection

## ⏰ 时间估算
- 每个原子任务: 5-10分钟
- 总计: 99个任务 × 7.5分钟 ≈ 12小时
- 建议分3天完成，每天33个任务

## 🔄 Cron任务配合
- 每2小时自动检查语法和格式
- 自动修复Markdown粗体、tcolorbox配对等问题
- 确保新增内容符合Part 1格式标准