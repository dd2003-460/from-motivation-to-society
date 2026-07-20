# RALPH 子代理任务卡

- **Card ID**: `01-r1-requirements-auditor`
- **阶段**: `01-r1`
- **角色**: `requirements-auditor`
- **标题**: 需求、遗漏和假设审计
- **任务目标**: 独立检查 Commander 对用户意图的语义分解，找出会改变决策的遗漏属性与隐含假设。
- **原始任务**: 

## 必读文件

- `loop-artifacts/contracts/01-r1-stage-input-package.json`
- `loop-artifacts/contracts/01-r1-stage-contract.md`
- `loop-artifacts/contracts/01-r1-submission-template.json`
- `loop-artifacts/stages/01-r1-result.json`

## 上下文隔离

你是独立门禁审计代理：不得依赖 Commander 主对话、隐藏推理或未列出的历史资料。
只以本卡列出的阶段输入包、阶段契约和提交模板作判断；输入不足时应给出 rollback 或 blocked_human，而不是猜测。

## 执行边界

1. 你是独立阶段门禁，不继承 Commander 主对话；只读取任务卡中的阶段输入包、契约和提交模板。
2. 只分析已给输入与项目内已有资料；不得开始外部调研或给出最终推荐。
3. 按背景、决策对象、目标、比较集合、约束、交付物、不确定性逐项审计。
4. 先执行需求分流闸门：显式输入或项目证据标记 confirmed；由多条证据高置信推导出的结论标记 inferred；可用默认策略推进的标记 assume；可以通过本地/网页证据解决的标记 research；只有不可自行解析且会改变可行性、硬预算、验收标准或价值授权的才标记 ask_human。
5. 每个叶节点必须记录 disposition、rationale、evidence_refs、confidence、impact 和 reversible；不要把‘字段没有单独出现’当成必须追问。
6. 返回一次性问题包：仅包含同时满足‘未被输入或环境确定、不能推断/研究、会改变关键分支、不能用场景覆盖’四条件的问题，并为每题给推荐选项。
7. 如果模型档位未明确，先读取已有模型/配置；仍未知时建立 30-35B 与更大模型档位的场景并把内存需求列为 research，不因模型名未知而阻塞。
8. 如果用户明确要购买本地 GPU/硬件，标记本地硬件采购为 confirmed 或 inferred；候选集合已经包含云服务时，不再追问云服务是否比较，而是按‘主方案/补充基线’记录假设或场景。
9. 返回 requirements_audit：覆盖缺口、冲突、默认假设风险和建议场景分支。
10. 参考阶段方法论（源自 loop/1-loop，补充要求，不覆盖上方门禁/边界规则）：
11. 本阶段 = 目标 / 背景 / 约束 + 初步分解：把「要做什么」整理成 task_spec。
12. 搜索优先、不问可搜：派发前先搜索所有可搜索信息（项目结构、依赖、代码、文档、数据、工具、外部论文/GitHub），搜索齐全后才允许问用户。
13. 问题必须一次性完整、必须是选择题且带推荐项；禁止逐个追问、禁止“你觉得呢”式开放提问。
14. 约束按分类标记：已确认 / 可推断(记录证据+置信度+可逆性) / 假设(默认策略+置信度) / 待研究 / 必须追问。
15. 提问闸门（先推断后提问）：仅当同时满足“用户/项目/环境均无答案、不能推断或研究、会改变硬可行性/硬预算/验收标准/价值授权、不能用场景覆盖”四项，才生成用户问题。
16. 置信度门槛：所有 MUST 类约束已确认、整体置信度 ≥ 0.7 才继续；< 0.5 回退重新澄清。
17. 分解项先记为 concept，其需要的事实标 research_required，供 02 调研。

## 允许工具

`Read`, `Glob`, `Grep`

## 输出接口

```json
{
  "check_status_values": [
    "pass",
    "fail",
    "uncertain"
  ],
  "required": [
    "reviewer_card_id",
    "verdict",
    "recommended_action",
    "checked_input_refs",
    "checked_output_refs",
    "checks",
    "blocking_findings",
    "summary"
  ],
  "stage": "01",
  "type": "object",
  "verdict_values": [
    "pass",
    "rollback",
    "blocked_human"
  ]
}
```

## 必填门禁回执模板

完成时必须填写下列 JSON，并用 `<RALPH_GATE_REVIEW>` 标记返回给 Commander。
如果任何检查失败、不确定或需要人类输入，填写 `rollback` 或 `blocked_human`，不要伪造 `pass`。

```json
{
  "blocking_findings": [],
  "checked_input_refs": [
    "loop-artifacts/contracts/01-r1-stage-input-package.json"
  ],
  "checked_output_refs": [],
  "checks": [
    {
      "criterion": "填写本阶段契约中的一项可验证验收条件",
      "evidence_refs": [],
      "note": "填写独立审计依据；不确定或失败不能写 pass。",
      "status": "pass"
    }
  ],
  "context_mode": "bounded_artifacts",
  "recommended_action": "advance",
  "reviewer_card_id": "01-r1-requirements-auditor",
  "summary": "填写独立审计的结论与边界。",
  "verdict": "pass"
}
```

## 返回给 Commander 的格式

- 已确认事实 / 来源 / 适用条件
- 不确定或冲突项
- 对应任务卡的结构化结论
- 不要修改 `loop-state.json`，不要替 Commander 决定后续阶段。
