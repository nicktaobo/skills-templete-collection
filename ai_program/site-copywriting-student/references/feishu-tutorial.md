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
