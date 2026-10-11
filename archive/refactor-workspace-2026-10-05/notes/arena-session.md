# Arena 会话记录

## 当前会话

| 项 | 值 |
|---|---|
| **SESSION_ID** | `01a10b07-df56-72c4-be7a-807001feb103` |
| **会话 URL** | https://arena.ai/agent/01a10b07-df56-72c4-be7a-807001feb103 |
| **挂载仓库** | `dd2003-460/from-motivation-to-society` |
| **挂载分支（基线）** | `refactor-v2-design`（我推送的设计分支，含架构 + prompt + skill） |
| **Arena 实际工作分支** | `arena/01a10b07-from-motivation-to-society` ← **注意：不是我 prompt 里指定的 `arena-refactor-v2`，Arena 用自己的命名约定** |
| **派活时间** | 2026-10-05 15:45 |
| **模式** | Agent（coding-agent） |
| **taskSpace ID** | 见 ego-browser 会话（标签 `dispatch motivation society refactor to arena`） |

## prompt 内容摘要

完整 prompt 见 `notes/arena-prompt.md`。实际发送的是「一次性派活」版本，含：

1. **推送验证前置**（GH_TOKEN 过期防护）
2. **绝对禁止**：不动 `main.tex`、不动任何原章节 `.tex`
3. **必读三件**：`notes/00-architecture.md`、`补充材料/part3_AI执行指导.md`、`part1_core_logic/introduction.tex`
4. **8 条写作铁律**（含逻辑链自检）
5. **诚实性纪律**（猜想标注、禁止空话、停下来问）
6. **交付范围 7 项**：main2.tex / preface / introduction / Part I 两章精写 / Part II–V 骨架 / 附录骨架 / 编译验证
7. **要求报告判断题**

## 监控方法

```bash
# 1. 查远端分支（Arena 是否 push 了）
cd "/Users/a1-6/Desktop/workspace/projects/理论物理/写作-社会系统/D1-writing/motivation_society"
git ls-remote --heads origin | grep arena

# 2. 查会话状态 + branchPushed
ego-browser nodejs -e '
const task = await taskSpace("dispatch motivation society refactor to arena");
const page = task.page("p1");
const r = await page.fetch("/api/coding-agent/sessions/01a10b07-df56-72c4-be7a-807001feb103", {timeout:25000});
const j = JSON.parse(String(r.body));
console.log({status: j.status, branchPushed: j.branchPushed, pr: j.pullRequestNumber});
'
```

**关键指标**：`branchPushed: true` 才算成果安全。`false` = 成果还在沙箱里，token 一过期就丢。

## 已观察到的现象

### 现象 0（v2 追加，最重要）：长 prompt 会触发 "Something went wrong"

第一次发 v2 prompt（7013 字节）时，消息发出去后 agent 报
**`Something went wrong. Please try again.`**，8 分钟无任何新提交。

**诊断**（通过 `/api/coding-agent/sessions/<SID>`）：
- `status: "active"` —— 会话本身没死
- `branchPushed: true` —— 成果没丢
- 说明是**生成响应那一侧失败**，不是任务失败

**解决**：把 prompt 压缩到 **3513 字节**（砍掉重复解释和详细追问链表，
只留「去读 notes/02-architecture-v2.md」这一句指路 + 5 条具体任务），一次就成功了。

**教训**：Arena 的 coding-agent 对超长 prompt 敏感。
**把细节推到仓库文件里，prompt 只留指路 + 任务清单。**
这对 agent 反而更好——它自己读架构文件比被我复述一遍更准。

### 现象 1：仓库挂载需要 sudo 验证（已绕过）

点仓库名按钮不弹选择器（已知坑）。走 GitHub settings → Manage repositories 会跳 GitHub
`installations/select_target`，页面显示「Uh oh!」但其实已有安装记录。
点 Configure 无效（需 sudo 2FA，脚本无法完成）。

**绕过方法**：直接回 arena.ai/agent，用 JS 点仓库按钮 →
`[role=option]` 列表里已有全部仓库（说明 App 有全仓库权限）→ 直接点选即可。
不需要进 GitHub 设置页。

### 现象 2：Arena 忽略了自定义分支名

我在 prompt 里明确写「新分支名固定为 `arena-refactor-v2`」，
Arena 仍然用了自己的 `arena/01a10b07-from-motivation-to-society` 约定。

**结论**：不要在 prompt 里指定分支名。Arena 会用自己的格式（会话 ID 前缀 + 仓库名）。
后续监控直接用 `git ls-remote --heads origin | grep arena` 找，不要找特定名字。

### 现象 6：ProseMirror 状态与 DOM 不同步

文本注入了（`textContent` 长度正确），但 `Send` 按钮仍是 `disabled`。
ProseMirror 的内部状态没被 `insertText` 触发更新。

**解决**：`page.goto()` 重新加载会话页 → **一次性** `insertText(全文)` → 等按钮 enable → 再点。
**分行插入会加剧不同步**（试过逐行 insertText，反而一直 disabled）。

### 现象 5：判断 agent 是否空闲，不能看「看起来做完了」

**实测**：v1 那轮 agent 做完 12 个骨架文件并 push 后说「接下来检查构建、写附录」，
看起来像做完了，实际上还在跑。

**正确判据**：`button[aria-label="Stop generating"]` 存在 = 还在跑。
存在期间输入框是锁定的 —— **此时注入文本会成功但发不出去**（Send 按钮 disabled）。
必须等这个按钮消失。

### 现象 3：Agent 在 TeX 环境上花了大量时间

Agent 发现沙箱没有 xelatex，开始在 GitHub 上找 TeX Live 镜像 / TinyTeX / SwiftLaTeX wasm
等替代方案，考虑过用 GitHub Actions 远程编译再把日志 push 回来。

**评估**：这是负责的表现，但**偏离优先级**。我在 prompt 里已经说过「如果沙箱里没有 xelatex，
明确说无法编译验证，不要谎称通过」——它应该直接写内容而不是先解决编译环境。

**下次派活修正**：把这句话加强为——「**先写内容，编译验证放最后**。沙箱没有 LaTeX 是预期情况，
直接跳过编译步骤，在回复里写『本沙箱无 LaTeX，未编译验证』。不要花时间找 TeX 镜像。」

### 现象 4：挂载基线分支选择

我把基线挂在 `refactor-v2-design`（含架构文档）而不是 `master`，
这样 Agent clone 后第一件事就是读到架构。不挂 master 的理由：master 上没有架构文档，
Agent 会自己臆测结构。

## 后续派活卡

`notes/arena-prompt.md` 里已备好 A–E 五张任务卡：

| 卡 | 内容 | 前置 |
|---|---|---|
| A | Part II 全文（三章） | S3 定稿 |
| B | Part III 全文（**修复断裂点，最关键**） | A 定稿 |
| C | Part IV 全文（五章，**防并列**） | B 定稿 |
| D | Part V + 附录补全（**§13.3 必须真实算例**） | C 定稿 |
| E | 编译验证 + 交叉引用审计（**要求报告架构问题**） | D 定稿 |

*每张卡都要求：写完 commit + push，然后停下来验收，不许连着做下一张。*

---

*记录：2026-10-05 15:55*
