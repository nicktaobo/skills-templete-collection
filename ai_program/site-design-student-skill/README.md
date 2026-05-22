# Site Design Student Skill 使用说明

给学员用的「站点设计 Skill」。

它做三件事：

1. 把产品信息整理成设计方案
2. 生成可复制到 Stitch / v0 / Lovable 的页面 Prompt
3. 输出给前端看的 `HANDOFF.md`

默认**不需要 API Key**。只有你想让 Agent 自动调用 Stitch 或自动生图时，才需要 Key。

---

## 1. 安装

把文件夹放进你的 skills 目录：

```bash
mkdir -p skills
cp -R site-design-student-skill skills/site-design-student
```

如果你用 Hermes，也可以放到 profile 目录：

```bash
mkdir -p ~/.hermes/profiles/default/skills
cp -R site-design-student-skill ~/.hermes/profiles/default/skills/site-design-student
```

`default` 换成你的 profile 名即可。

---

## 2. 最简单用法

直接把这段发给 Agent：

```text
请使用 site-design-student Skill，为我的产品做站点设计。

产品名：
一句话定位：
目标用户：
核心页面：首页 / Pricing / FAQ / SEO 页面
竞品：URL1 URL2 URL3

请输出：
1. 竞品视觉分析
2. 反 AI 味约束表
3. 3 个设计方向
4. 首页页面生成 Prompt
5. Logo / OG / Hero 图提示词
6. HANDOFF.md
```

---

## 3. 推荐用法

先填写：

```text
templates/input-brief.md
```

然后发给 Agent：

```text
请使用 site-design-student Skill，基于下面的 input brief 生成完整设计交付包。

[粘贴 input brief]
```

---

## 4. 有没有 Key 都能用

### 无 Key：推荐给大多数学员

Skill 会输出：

- 设计方向
- 页面生成 Prompt
- Logo / OG / Hero 图 Prompt
- HANDOFF.md
- 验收清单

然后你手动复制 Prompt 到：

- Google Stitch
- v0
- Lovable
- Claude / ChatGPT

### 有 Key：自动化用法

如果你希望 Agent 直接生成页面或图片，需要按工具配置对应 Key：

```text
STITCH_API_KEY       # 自动调用 Stitch 时需要
OPENAI_API_KEY       # 用 OpenAI 生图时需要
GEMINI_API_KEY       # 用 Gemini / 图片工具时需要
SNAPOG_API_KEY       # 可选，自动生成 OG Image 时需要
```

没有这些 Key 不影响 Skill 使用，只是不能自动出图/自动调用设计工具。

---

## 5. 学员应该拿到什么

一次完整运行后，应该得到：

```text
1. 竞品视觉分析
2. 反 AI 味约束表
3. 3 个设计方向
4. Landing Page Desktop Prompt
5. Landing Page Mobile Prompt
6. SEO 页面模板 Prompt
7. Logo / Favicon / OG / Hero 图提示词
8. HANDOFF.md
9. final-checklist.md
```

---

## 6. 重要规则

- 先定文案，再做设计
- 先定定价和合规，再做 Pricing 区
- 不用 Inter / Roboto / Arial 默认字体
- 不用紫蓝渐变 + 白背景 + 居中 Hero
- 不用 emoji 做 icon
- 不编假用户评价
- 至少做 Desktop + Mobile
- 设计定稿后不要随便改文案

---

## 7. 一句话记住

```text
看得懂 → 信得过 → 点得下去
```
