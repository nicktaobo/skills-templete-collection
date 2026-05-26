---
name: site-copywriting-student
title: 落地页文案与 SEO 内容
description: 基于 PRD 输出 9 区块落地页文案、Meta Tags、FAQ、SEO 内容结构，并用 PAS/BAB/FAB/AIDA/4Ps/SSS 和 CORE-EEAT 做自检。
version: 1.2.1
owner: ShipSolo
agent: mobi
category: 做站全流程
stage: 05-copy
updated: 2026-05-18
student_level: intermediate
source: internal-site-building-flow-publicized
---

# 落地页文案与 SEO 内容

基于 PRD 输出 9 区块落地页文案、Meta Tags、FAQ、SEO 内容结构，并用 PAS/BAB/FAB/AIDA/4Ps/SSS 和 CORE-EEAT 做自检。

> 这是内部做站流程的脱敏学员版：保留流程、判断标准、交接格式和质量门槛；移除真实路径、密钥、内部群、账号和生产配置。

## 流水线位置

- 当前阶段：`05-copy`
- 角色：墨笔脱敏版：把 PRD、定价、合规边界转成能转化、能排名、能交给设计的文案。
- 上游：product-definition-prd + pricing + compliance
- 下游：site-design-student

## 什么时候使用

- 要写首页文案
- PRD 已完成准备设计
- 要写 SEO 子页 / 博客 / 对比页
- 要生成 Meta Title/Description

## 输入契约

开始前尽量准备：

- PRD
- 定价口径
- 合规禁词和免责声明
- 主关键词和次级关键词
- 竞品弱点和 ICP

如果缺信息，不要停死；按下面规则：

- 影响结论或上线安全：标 `[BLOCKED]`，列缺失项。
- 不影响当前阶段推进：标 `[待确认]`，继续产出 v0。
- 涉及密钥、Cookie、Token、支付后台、生产数据库：只写变量名或 `[REDACTED]`。

## 一键启动 Prompt

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


## 阶段流程

### Step 1：提取文案字段

product_name、one_liner、target_users、pain_points、competitors、differentiation、pricing、compliance、primary_keyword。

### Step 2：Hero — PAS

Problem 指痛点，Agitate 算成本，Solve 给解决方案。Headline ≤10 词，CTA 用动词 + 结果。

### Step 3：How It Works

永远 3 步，每步动词开头，3-5 词标题 + 20 词以内描述。

### Step 4：Use Cases — BAB

每个目标用户一张卡：Before / After / Bridge。After 尽量有具体结果。

### Step 5：Features — FAB

每个功能写 Feature / Advantage / Benefit，不能只列功能。

### Step 6：Pricing — 4Ps

先价值后价格；免费层正面表述；Pro 明确额度；CTA 带价格锚点。

### Step 7：FAQ + Final CTA

FAQ 回答购买异议，首句直答；Final CTA 用 Star-Story-Solution。

### Step 8：SEO/AEO

Title 50-60 字符，Description 150-160 字符；H2 首句可被 AI 引用；FAQ 覆盖 PAA。

### Step 9：铁律自查

you/your ≥ 2x we/our；无假评价；无模糊大词；合规禁词全部避开。

## 交付物

- 9 区块首页文案
- Hero 3 个变体
- FAQ 6-10 条
- Meta/OG/Twitter Tags
- SEO 子页写作 brief
- 文案自查报告

## 验收清单 / 质量门槛

- [ ] 文案定稿后尽量不改，改文案会影响设计和前端
- [ ] 不编用户数、评价、收入、案例
- [ ] 不使用 Revolutionize/Empower/Seamless/Cutting-edge 等 AI 味词
- [ ] CTA 必须具体
- [ ] 输出必须按 section 给设计使用

## 下游交接格式

```markdown
# 落地页文案与 SEO 内容交接摘要

## 当前结论
- 结论：
- 状态：[DONE] / [BLOCKED] / [NEEDS_REVIEW]

## 关键输入
- 项目：
- 当前阶段：05-copy
- 上游资料：

## 本阶段交付物
- 文件/内容：
- 核心判断：
- 已确认项：
- 待确认项：

## 给下游的最小必要信息
最终文案按 section 输出，含 Hero、CTA、FAQ、Pricing、Meta、禁词，交给设计直接粘贴。

## 风险
- P0：
- P1：
- P2：

## 建议下一步
- 下一阶段：site-design-student
- 启动 Prompt：
```


## 学员怎么用

你可以把这个 Skill 用在 Hermes、OpenClaw、Claude Code、Cursor、ChatGPT、Gemini 等任意 AI 工具里。

### 方式 A：安装到 Hermes / OpenClaw

```bash
mkdir -p ~/.hermes/skills/shipsolo/site-copywriting-student
cp SKILL.md ~/.hermes/skills/shipsolo/site-copywriting-student/SKILL.md
```

### 方式 B：不安装，直接复制

打开 `SKILL.md`，复制“一键启动 Prompt”，把项目资料填进方括号，发给 AI。

### 建议节奏

- 每个阶段单独开一个会话或清晰分隔上下文。
- 每阶段结束时保存交付物，再进入下一阶段。
- 不要让 AI 一口气从调研做到上线；中间必须验收。


## 常见坑

- 把“AI 看起来很完整”的输出当成真实事实。
- 没有输入契约就直接进入下游，导致后面返工。
- 没有 `[DONE] / [BLOCKED] / [NEEDS_REVIEW]` 状态，团队不知道能不能接。
- 公开材料里残留服务器路径、密钥名之外的真实 secret、内部群 ID、个人账号。
- 跳过质量门槛，只看交付物篇幅。


## 标准包内容

这个 Skill 不是单个提示词，而是一个可安装/可复制的标准包：

- `SKILL.md`：阶段入口、输入契约、一键启动 Prompt、流程与验收清单。
- `references/USAGE.md`：学员使用说明。
- `CHANGELOG.md`：本 Skill 独立版本说明。
- `references/copy-quality-rules.md`：从内部 Agent 流程脱敏出的判断标准。
- `templates/landing-copy-template.md`：本阶段标准交付物模板。
- `templates/stage-handoff-template.md`：交给下游的统一摘要模板。
- `scripts/audit_copy_quality.py`：本阶段最小校验/辅助脚本，可本地运行。
- `scripts/validate_handoff.py`：通用交接完整性检查。

## 更新记录

### 1.1.0 — 2026-05-18
- 升级为内部做站流程脱敏版。
- 补齐输入契约、阶段流程、质量门槛、下游交接格式和学员使用方式。
- 强化 `[DONE] / [BLOCKED] / [NEEDS_REVIEW]` 状态约定。

### 1.0.0 — 2026-05-18
- 发布学员版基础结构。


## 更新记录

- v1.2.0：补齐标准包结构，新增 references、templates、scripts、CHANGELOG，贴近内部做站 Agent 能力并完成脱敏。
