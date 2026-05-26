# 落地页文案与 SEO 内容 使用说明

## 先说结论

这个 Skill 的主用法不是让你先跑脚本，而是把下面的自然语言 Prompt 复制给 AI Agent / ChatGPT / Claude，让 AI 带你完成这一阶段。

脚本、模板和参考文件都可以保留，但它们是辅助材料：你可以先不用会 Python、Node 或命令行。

## 这个 Skill 解决什么

基于 PRD 输出 9 区块落地页文案、Meta Tags、FAQ、SEO 内容结构，并用 PAS/BAB/FAB/AIDA/4Ps/SSS 和 CORE-EEAT 做自检。

- 阶段：`05-copy`
- 适合：已经有项目方向、上游资料或当前阶段卡点，希望让 AI 按 ShipSolo 流程推进。
- 不适合：完全没有输入，又希望 AI 凭空编数据。缺信息时要让 AI 标 `[待确认]` 或 `[BLOCKED]`。

## 推荐使用方式：复制 Prompt 给 AI

1. 打开你常用的 AI 工具：ChatGPT、Claude、Gemini、Cursor、Hermes、OpenClaw 都可以。
2. 复制下面的 Prompt。
3. 把你的项目资料、上游输出、链接或截图文字粘到 Prompt 的“输入”部分。
4. 让 AI 按阶段流程输出交付物。
5. 检查最后一行状态：只有 `[DONE]` 才进入下一阶段；`[BLOCKED]` 先补资料；`[NEEDS_REVIEW]` 先人工确认。

```text
你现在执行 ShipSolo 做站流程的「落地页文案与 SEO 内容」阶段。

角色定位：墨笔脱敏版：把 PRD、定价、合规边界转成能转化、能排名、能交给设计的文案。
项目：[项目名称]
当前阶段：05-copy
上游输入：[粘贴 PRD/调研报告/设计包/代码仓库/数据截图]
目标市场：[默认 US / English，可修改]
限制条件：[时间、预算、技术栈、不能做什么]

请严格按这个 Skill 执行：
1. 先检查输入是否满足“输入契约”，不足就列 [BLOCKED] 和缺失项。
2. 如果可以推进，按阶段流程逐步产出。
3. 所有不确定信息标 [待确认]，不要编造数据、价格、法律结论、部署结果。
4. 输出“交付物 + 质量门槛自检 + 下游交接摘要”。
5. 最后一行只能是：[DONE] / [BLOCKED] / [NEEDS_REVIEW]。
```

## 最小作业模板

把这段复制给 AI，补齐空白即可：

```markdown
# 作业：落地页文案与 SEO 内容

## 我的项目
- 项目名称：
- 目标用户：
- 目标市场：
- 当前阶段：05-copy

## 我已有的资料
- 上游交付物：
- 参考链接 / 截图文字：
- 我已经确定的决策：
- 我不确定的问题：

## 请你帮我输出
- 本阶段交付物：
- 关键判断依据：
- 风险和待确认事项：
- 下一阶段交接摘要：
- 最后一行状态：[DONE] / [BLOCKED] / [NEEDS_REVIEW]
```

## 怎么判断 AI 输出能不能用

- 输入不够时，AI 有没有明确标 `[待确认]`，而不是编造。
- 每个关键结论有没有理由、证据或假设。
- 交付物是否能直接给下一阶段使用。
- 风险有没有分级：P0 / P1 / P2，或高 / 中 / 低。
- 最后一行是否明确写了 `[DONE] / [BLOCKED] / [NEEDS_REVIEW]`。

## 可选辅助材料

参考文件：
- `references/copy-quality-rules.md`
- `references/feishu-tutorial.md`

模板文件：
- `templates/landing-copy-template.md`
- `templates/stage-handoff-template.md`

脚本文件：
- `scripts/audit_copy_quality.py`：高级校验/自动化辅助，学员可先不用。
- `scripts/validate_handoff.py`：高级校验/自动化辅助，学员可先不用。

说明：脚本不是新手主路径。只有当你想做批量校验、格式检查、API 拉取或自动化处理时，再让 AI 解释这些脚本怎么用。

## 如果你要使用脚本

可以这样问 AI，而不是自己硬跑：

```text
我已经下载了这个 Skill。请先阅读 SKILL.md 和 references/USAGE.md，告诉我是否需要使用 scripts/ 里的辅助脚本。如果需要，请用新手能理解的方式解释：这个脚本解决什么、需要什么输入、怎么检查输出、失败了怎么办。不要假设我会 Python 或命令行。
```

## 交给下一阶段

当 AI 输出 `[DONE]` 后，把“交付物 + 风险 + 下一阶段交接摘要”复制给下一个 Skill。不要只复制结论，缺少依据会导致后面阶段返工。

## 更新记录

- 1.2.1：统一使用说明为“自然语言 Prompt 优先”，脚本改为可选高级辅助。
