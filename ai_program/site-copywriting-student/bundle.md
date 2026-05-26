# 落地页文案与 SEO 内容

> ShipSolo public skill bundle. Sensitive server paths and credential-like values are redacted.



---

## CHANGELOG.md

# 落地页文案与转化结构 更新记录

## 1.2.1 - 2026-05-18

- 统一 `references/USAGE.md` 为面向学员的自然语言 Prompt 使用路径。
- 明确脚本仍保留在包内，但只作为可选高级辅助，不作为新手主流程。


## v1.2.0 — 标准包升级

- 新增 `references/`：沉淀内部 Agent 的判断标准与质量门槛。
- 新增 `templates/`：提供可复制填写的阶段交付物和下游交接模板。
- 新增 `scripts/`：提供本地最小校验/辅助脚本。
- 保持脱敏：不包含真实账号、密钥、生产路径、内部群 ID 或私有配置。

## v1.1.0 — 内部流程脱敏版

- 从简化版 `SKILL.md` 升级为完整阶段流程。
- 增加输入契约、阶段流程、验收清单、下游交接格式和学员指南。



---

## SKILL.md

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



---

## references/USAGE.md

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



---

## references/copy-quality-rules.md

# 落地页文案与转化结构 — 内部能力脱敏参考

## 阶段核心能力

Hero、价值主张、CTA、FAQ、Meta、SEO 子页、反 AI 味

## 执行顺序

1. 先读上游交接摘要，确认输入是否满足契约。
2. 缺关键输入时输出 `[BLOCKED]`，不要编造数据或替用户做高风险决策。
3. 可推进时按 `SKILL.md` 的 Phase 顺序执行，所有依据写来源或标 `[待确认]`。
4. 完成后用模板生成交付物，再运行脚本做最小校验。
5. 最后一段写下游交接摘要，状态只能是 `[DONE] / [BLOCKED] / [NEEDS_REVIEW]`。

## 质量门槛

- [ ] Headline 结果导向
- [ ] CTA 是动词+结果
- [ ] FAQ 首句直答
- [ ] 禁用空泛 AI 味词

## 脱敏边界

- 可以保留流程、字段、判断标准、模板、脚本骨架。
- 不保留真实 API Key、Cookie、Token、内部路径、生产库名、群聊 ID、真实客户数据。
- 公开示例统一用 `[PROJECT]`、`[DOMAIN]`、`[API_KEY]`、`[ACCOUNT]` 这类占位符。



---

## references/feishu-tutorial.md

## 第二部分：OpenClaw / Hermes 自动化

### 安装方式

把整个目录放到你的 skills 目录下：

```
skills/site-copywriting-student/SKILL.md
```

如果是 Hermes / OpenClaw / Claude Code 这类支持 Skill 的 Agent，放好后新开会话，让 Agent 加载或使用：

```
使用 site-copywriting-student skill，为下面产品生成英文首页文案：
[粘贴产品信息]
```

## 最短口令

```
用 site-copywriting-student skill，按 9 区块首页结构，为这个产品写英文落地页文案。框架：Hero=PAS，Use Cases=BAB，Features=FAB，Pricing=4Ps，Final CTA=SSS。不要编假数据，信息不足标 [待确认]，最后做 8 条铁律自查。
```

## 产品信息模板

```
product_name: ""
one_liner: ""
target_users:
  - ""
  - ""
  - ""
main_pain_points:
  - ""
  - ""
  - ""
core_value: ""
differentiation: ""
primary_keyword: ""
pricing:
  free: ""
  pro: ""
  lifetime: ""
proof:
  users: ""
  usage: ""
  testimonials: ""
compliance_notes:
  - ""
```

---

## 第三部分：手动实操 — 一步步教你怎么做

### Step 1：准备原材料（10 分钟）

写文案之前，这些信息必须已经有了。没有 = 先补齐再来。

把这些信息列在一个文档里：

```
产品名：[xxx]
一句话说清楚：[产品做什么]
目标用户：[3-4 个人群]
用户痛点（从 Reddit 扒的原话）：
  - "[痛点1]"
  - "[痛点2]"
  - "[痛点3]"
竞品弱点：
  - [竞品A]：[弱点]
  - [竞品B]：[弱点]
我们的差异化：[一句话]
定价：Free [限制] → Pro $[价格]/月 [额度] → Lifetime $[价格]
合规禁词：[从墨盾拿到的禁用表述列表]
```

### Step 2：写 Hero 区（10 分钟）

#### 提示词模板

```
你是一个专注 SaaS/工具站的转化文案专家。请用 PAS（Problem-Agitate-Solve）框架
帮我写首页 Hero 区。

产品信息：
- 产品名：[你的产品名]
- 一句话描述：[产品做什么]
- 目标用户：[给谁用]
- 用户最大痛点：[从 Reddit/G2 扒的用户原话]
- 竞品弱点：[竞品做不好的地方]
- 我们的差异化：[我们比竞品强在哪]

输出要求：
1. Headline：≤10 个英文词，包含核心卖点
2. Subhead：1-2 句话，补充说明 how 或 for whom
3. CTA 按钮文案：用「动词 + 结果 + 降低摩擦」公式
4. CTA 按钮下方小字：降低门槛（如 "No signup required"）
5. 给 3 个 Headline 变体（Action-Outcome / Benefit-First / Problem-Solution 各一个）

注意：
- "you/your" 出现频率必须高于 "we/our"
- 不用模糊形容词（如 powerful、ultimate、innovative），用具体数字
- 第一句话必须是用户的痛点，不是你的产品介绍
```

#### 生成后检查 5 个点

### Step 3：写 How It Works（5 分钟）

#### 铁律：永远 3 步

#### 提示词模板

```
我的产品是 [产品名]，[一句话描述]。

请帮我写 "How It Works" 区块，要求：
1. 只能有 3 步（Step 1 / Step 2 / Step 3）
2. 每步标题 3-5 词，用动词开头
3. 每步描述 1 句话，≤20 词
4. 从用户视角写（"You upload..." 不是 "Our system processes..."）
```

### Step 4：写场景卡片（15 分钟）

#### 提示词模板

```
我的产品是 [产品名]，目标用户包括：
1. [用户群 A]
2. [用户群 B]
3. [用户群 C]

请用 BAB（Before-After-Bridge）框架，为每个用户群写一张场景卡片。

每张卡片格式：
- 场景名：[面向哪个用户群]
- Before：1-2 句话描述没有这个产品时用户怎么受苦（用用户的语言）
- After：1-2 句话描述用了产品之后的理想状态（描述结果，不描述过程）
- Bridge：1 句话说怎么做到的（越短越好）

注意：
- Before 部分尽量用 Reddit/G2 上的用户原话
- After 部分包含具体数字或时间对比
- Bridge 部分不超过 15 个词
```

### Step 5：写功能区（10 分钟）

#### 提示词模板

```
我的产品核心功能：
1. [功能 A]
2. [功能 B]
3. [功能 C]
4. [功能 D]

请用 FAB（Feature-Advantage-Benefit）框架，为每个功能写一条文案。

每条格式：
- Feature Title：3-5 词
- Feature Description：1-2 句话
  - 第 1 句：这个功能是什么 + 比竞品强在哪（Advantage）
  - 第 2 句：用户得到什么好处（Benefit，必须从用户视角写）

注意：
- 选 4-6 个最核心的功能，不要列 10 个
- 每个 Benefit 回答"所以用户能......"
- 不用 "powerful" / "advanced" / "state-of-the-art" 这些空词
```

### Step 6：写定价区（10 分钟）

#### 提示词模板

```
我的定价方案：
- Free：[限制和权益]
- Pro：$[价格]/月，[权益]
- Lifetime（可选）：$[价格]，[权益]

竞品定价参考：
- [竞品 A]：[价格和模式]
- [竞品 B]：[价格和模式]

请帮我写定价区文案，用 4Ps（Promise-Picture-Proof-Push）框架：
1. 每个 Plan 的名称和一行 tagline
2. 权益列表（正面表述："5 free images daily" 不是 "Limited to 5"）
3. 帮我算单价（$X/月 ÷ 次数 = $X/次），用来做价格锚定
4. CTA 按钮文案 + 下方小字
5. 如果有 Lifetime，加稀缺性文案

注意：
- 免费层叫 "Free" 或 "Starter"，不叫 "Basic"（暗示低质量）
- 先展示价值再展示价格
- "No credit card required" / "Cancel anytime" 这类信任文案必须有
- 如有合规要求的自动续费说明，写在小字里
```

### Step 7：写 FAQ（10 分钟）

#### 核心逻辑

FAQ 不是"回答问题"，是处理购买异议。用户不买，无非这几个原因：

#### 提示词模板

```
我的产品是 [产品名]，[一句话描述]。
定价：[Free/Pro/Lifetime 方案]

请帮我写 6-10 条 FAQ，要求：
1. 每条 FAQ 对应一个购买异议
2. 答案第一句必须直接回答 Yes/No 或给出结论
3. 答案总长不超过 3 句话
4. 每条 FAQ 的答案控制在 40-60 词（为 Google Featured Snippet 优化）
5. 语气友好直接，不要法律腔

❌ 不要写成这样：
"Our platform offers a generous free tier that allows users to explore..."

✅ 写成这样：
"Yes. 3 free per day. No sign-up, no credit card."
```

### Step 8：写社会证明区（5 分钟）

#### 已有用户数据

- 用具体结果："I generated 5 NPCs in 10 minutes"
- 带来源标注："— Reddit r/DnD user"
- 数字牌："X，XXX characters generated"
#### MVP 刚上线（冷启动）

- ✅ 用活动指标替代用户数："10,000+ images extended this week"
- ✅ 用产品特性做信任信号："5 free daily， no watermark， no signup"
- ✅ 用 Product Hunt badge（如果有）
- ❌ 不要编假评价
- ❌ 不要用假 testimonial
### Step 9：通读 + 砍 30%（10 分钟）

1. 把整篇文案从头到尾读出声
1. 读到卡壳的句子 → 重写
1. 读到"正确但不惊艳"的段落 → 删掉
1. 数 "you/your" vs "we/our" → you 要是 we 的 2 倍
1. 检查每个 CTA → 是不是"动词+结果"格式
1. 检查每个数字 → 具体吗？能更具体吗？
---



---

## scripts/audit_copy_quality.py

#!/usr/bin/env python3
"""落地页文案与转化结构 最小校验脚本。用法：python scripts/audit_copy_quality.py <report.md>"""
import sys, pathlib
path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('report.md')
text = path.read_text(encoding='utf-8') if path.exists() else ''
checks = ['Headline 结果导向', 'CTA 是动词+结果', 'FAQ 首句直答', '禁用空泛 AI 味词']
missing = [c for c in checks if c.split()[0] not in text and c not in text]
base = [x for x in ['交付物','验收清单','下游交接'] if x not in text]
if base:
    print('FAIL missing sections: ' + ', '.join(base)); sys.exit(1)
print('OK 落地页文案与转化结构 report basic structure passed')
if missing:
    print('WARN review checklist manually: ' + '; '.join(missing))



---

## scripts/validate_handoff.py

#!/usr/bin/env python3
import sys, pathlib, re
path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('HANDOFF.md')
text = path.read_text(encoding='utf-8') if path.exists() else ''
required = ['[DONE]', '交付物', '质量门槛', '下游交接']
missing = [x for x in required if x not in text]
if missing:
    print('FAIL missing: ' + ', '.join(missing))
    sys.exit(1)
print('OK handoff looks complete')



---

## templates/landing-copy-template.md

# 落地页文案与转化结构 — 标准交付物模板

## 1. 基本信息

- 项目：`[PROJECT]`
- 域名/候选域名：`[DOMAIN]`
- 当前阶段：`05-copy`
- 执行人/Agent：`mobi`
- 日期：`YYYY-MM-DD`
- 状态：`[DONE] / [BLOCKED] / [NEEDS_REVIEW]`

## 2. 上游输入

- 输入文件/链接：`[LINK_OR_PATH]`
- 关键假设：
  - `[ASSUMPTION_1]`
- 缺失信息：
  - `[MISSING_OR_NONE]`

## 3. 本阶段结论

- 结论一句话：`[...]`
- 证据：
  - `[...]`
- 风险：
  - `[...]`

## 4. 交付物

- `[DELIVERABLE_1]`
- `[DELIVERABLE_2]`
- `[DELIVERABLE_3]`

## 5. 验收清单

- [ ] Headline 结果导向
- [ ] CTA 是动词+结果
- [ ] FAQ 首句直答
- [ ] 禁用空泛 AI 味词

## 6. 下游交接

- 给下游 Skill：`[NEXT_SKILL]`
- 下游必须读取：`[...]`
- 下游不能改动：`[...]`
- 下游启动 Prompt：见 `templates/stage-handoff-template.md`



---

## templates/stage-handoff-template.md

# 阶段交接摘要

- 项目：`[PROJECT]`
- 已完成阶段：`05-copy — 落地页文案与转化结构`
- 状态：`[DONE] / [BLOCKED] / [NEEDS_REVIEW]`
- 本阶段交付物：
  - `[...]`
- 核心结论：
  - `[...]`
- 风险/待确认：
  - `[...]`
- 下游输入：
  - `[...]`

## 下一阶段一键 Prompt

```text
你现在接手 ShipSolo 做站流程的下一阶段。
上游阶段：05-copy — 落地页文案与转化结构
上游结论：[粘贴本摘要]
请先检查输入契约，再执行对应 Skill。缺关键输入就输出 [BLOCKED]，不要编造。
```

