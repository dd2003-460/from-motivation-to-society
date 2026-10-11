# RALPH 子代理任务卡

- **Card ID**: `01-r1-builder-task_spec-context`
- **阶段**: `01-r1`
- **角色**: `task_spec-writer-context`
- **标题**: 任务规格构造·context
- **任务目标**: 只填写 task_spec 的语义角色：background, decision_object, objective。
- **原始任务**: 

## 必读文件

- `loop-artifacts/contracts/01-r1-stage-contract.md`
- `loop-artifacts/contracts/01-r1-submission-template.json`
- `loop-artifacts/stages/01/r1/task_spec.partial.context.json`

## 执行边界

1. 你**只负责** task_spec 的这几个语义角色：background, decision_object, objective；不要写其他角色。
2. 用 **Write** 工具把你的部分写入 `loop-artifacts/stages/01/r1/task_spec.partial.context.json`。文件顶层对象只需包含：`semantic_map`（只列你负责的角色，每条给 2-4 个真实条目）、`attribute_matrix`（只列这些角色的叶节点，含 concept/role/attribute/disposition/rationale，disposition ∈ {confirmed,inferred,assume,research}）、以及可选的 `assumptions`/`scenarios`/`requirements_audit`。
3. 其他角色一律不要出现在文件里（不要留空数组占位），避免与同阶段其他 builder 的输出冲突。
4. 禁止再派发任何子代理（不得调用 Agent）；你自己用 Write 完成，嵌套子代理只会增加断流风险。
5. 不要写入 loop-state.json 或其他受控文件；不要替 Commander 做独立门禁审计（那是 gate 的职责）。
6. 完成后只把结构化结论简短返回给 Commander，并确认文件已写好。
7. 参考阶段方法论（源自 loop/1-loop，补充要求，不覆盖上方门禁/边界规则）：
8. 本阶段 = 目标 / 背景 / 约束 + 初步分解：把「要做什么」整理成 task_spec。
9. 搜索优先、不问可搜：派发前先搜索所有可搜索信息（项目结构、依赖、代码、文档、数据、工具、外部论文/GitHub），搜索齐全后才允许问用户。
10. 问题必须一次性完整、必须是选择题且带推荐项；禁止逐个追问、禁止“你觉得呢”式开放提问。
11. 约束按分类标记：已确认 / 可推断(记录证据+置信度+可逆性) / 假设(默认策略+置信度) / 待研究 / 必须追问。
12. 提问闸门（先推断后提问）：仅当同时满足“用户/项目/环境均无答案、不能推断或研究、会改变硬可行性/硬预算/验收标准/价值授权、不能用场景覆盖”四项，才生成用户问题。
13. 置信度门槛：所有 MUST 类约束已确认、整体置信度 ≥ 0.7 才继续；< 0.5 回退重新澄清。
14. 分解项先记为 concept，其需要的事实标 research_required，供 02 调研。

**切片填写方式（关键）**：`loop-artifacts/stages/01/r1/task_spec.partial.context.json` 已由运行时预生成为骨架（结构完整、含占位/示例值）。
你**必须用 Write 工具把整个填充后的切片写入 `loop-artifacts/stages/01/r1/task_spec.partial.context.json`**（直接整体覆盖骨架），不要只返回 JSON 文本。
**严禁把 JSON 作为纯文本返回**：只有写入了 `{slice_ref}` 文件才算完成；只回自然语言会被判定为未提交并退回重做。
**增量填写**：`semantic_map` 中仍为空数组的语义角色才需要补充；已填角色不要重写，只针对空角色补真实条目，并补上对应 `attribute_matrix` 叶节点（concept/role/attribute/disposition/rationale，disposition∈{confirmed,inferred,assume,research}）。七类角色（background/decision_object/objective/comparison_set/constraints/deliverable/uncertainty）都非空后才算完成。
若 Commander 派发时附带门禁回执（`<RALPH_GATE_REVIEW>`），只修正回执中 `status:"fail"` 的 check 对应的字段，其余保持不变。

## 允许工具

`Read`, `Glob`, `Grep`, `Write`

## 输出接口

```json
{
  "assumptions": [],
  "attribute_matrix": [
    {
      "alternative_scenario": "",
      "attribute": "",
      "concept": "",
      "confidence": 0.0,
      "disposition": "confirmed",
      "evidence_refs": [],
      "impact": "material",
      "rationale": "",
      "reversible": true,
      "role": ""
    }
  ],
  "constraints": [],
  "open_questions": [],
  "requirements_audit": {
    "artifact_ref": "",
    "card_id": "01-r1-requirements-auditor",
    "summary": ""
  },
  "scenarios": [
    {
      "id": "S1",
      "name": ""
    }
  ],
  "semantic_map": {
    "background": [],
    "comparison_set": [],
    "constraints": [],
    "decision_object": [],
    "deliverable": [],
    "objective": [],
    "uncertainty": []
  },
  "success_criteria": []
}
```

## 返回给 Commander 的格式

- 已确认事实 / 来源 / 适用条件
- 不确定或冲突项
- 对应任务卡的结构化结论
- 不要修改 `loop-state.json`，不要替 Commander 决定后续阶段。
