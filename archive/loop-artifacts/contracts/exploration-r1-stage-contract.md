# RALPH 字段中心 · 阶段契约

阶段：exploration-r1

## 你只维护一张字段表（不强制子代理卡片）

- 权威输入：`loop-state.json`、`loop-artifacts/contracts/exploration-r1-stage-contract.md`、`loop-artifacts/contracts/exploration-r1-submission-template.json`。
- 用 `ralph field-apply` 把字段原子写入字段表（**禁止直接 Write/Edit `loop-state.json`**，运行时只读它）。
- 每条字段形如：concept / role / attribute / disposition / rationale / evidence_refs / confidence / impact / reversible。
- disposition 取英文枚举值之一：confirmed / assumed_default / research_required / pending；直接照抄。
- 例：{"concept": "字段名", "role": "背景", "attribute": "具体属性", "disposition": "confirmed", "rationale": "...", "evidence_refs": [], "confidence": 1.0, "impact": "material", "reversible": true}。
- `confirmed`=已知背景；`assumed_default`=不确定偏好（默认全范围，无人类输入）；
`research_required`=未知事实（派单字段调研 subagent 带回 evidence_refs）；`pending`=尚未处理。
- 对每个 `research_required` 字段，用 Agent 派**只填这一个字段**的窄调研 subagent；它把该字段 JSON 交回，你合并进表。
- 每回填一个字段，若引出新的未知项，作为新的 `pending` 字段加进同一张表（差集=新字段，自动增殖）。
- **只回传空缺**：系统只告诉你还差哪些 `pending` 字段；你照着补，不会因为没一次交齐而失败。
- `loop-artifacts/` 下的长文档（契约/输入包/提交模板）由子代理读取；Commander 自身直接维护字段表，不要再派发任务卡。

## 提交（用命令，不要输出 token）

字段 + 本阶段 required_outputs 齐全后，**用命令显式推进**——运行时不会解析聊天里的 `<RALPH_STAGE_RESULT>` token（只有 stage 01 字段齐全会**自动**推进）。
正确动作：
1. 若本阶段字段有更新，先落盘：`ralph field-apply . loop-artifacts/exploration-r1.json`（或把 action 写进同一文件）。
2. 写 advance 动作文件 `loop-artifacts/exploration-r1.advance.json`：
```json
{
  "action": "advance",
  "status": "passed",
  "stage_id": "exploration",
  "revision": "r1",
  "next_stage": "<节点图上本阶段的后继 id>",
  "payload": { "stage_review": "<简述已满足的字段条件与依据>", 
                "task_spec": "<即 loop-state.json 里的 task_spec（含完整 attribute_matrix）>" }
}
```
3. 运行 **`ralph apply . loop-artifacts/exploration-r1.advance.json`**（等效 `ralph validate --result ... --apply`）即完成推进；运行时自动校验、原子落盘。

只有「用户/项目/环境都无答案、不能推断或研究、且会改变硬可行性/硬预算/验收」的字段，
才在 `payload.questions` 一次性提问；否则不要用 `blocked_human` 卡住。

## 探索：自主发现新任务并写回任务板（字段化）

先读 `tasks/TASKS.md` 并跑 `ralph task-next .`；有 ready 任务则 selected_task + selection_mode=task_board 进入 01。
无 ready 任务时，自主做轻量调研发现 1~3 个候选方向，并直接把每个候选写成 `tasks/TASKS.md` 的新表格行（ID / 任务(目标) / 状态 / 优先级 / 依赖 / 背景），即入队。
写完后重跑 `ralph task-next .` 选最高优先级 ready 任务进入 01；其「背景」列作为 01 输入。
