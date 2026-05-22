---
name: site-design-student
description: "站点页面设计 Skill：从 PRD/文案/定价/合规输入，生成可交付前端的 Landing Page / SEO 页面设计方案、Stitch Prompt、品牌素材提示词与开发交付清单。适合学员直接复制到 Agent skills 目录使用。"
author: Nextfield Labs
version: "1.0.0"
user-invocable: true
triggers:
  - 站点设计
  - 页面设计
  - 做站设计
  - landing page design
  - Stitch Prompt
  - 反 AI 味设计
  - 设计交付包
allowed-tools:
  - web_search
  - web_extract
  - browser_navigate
  - browser_snapshot
  - browser_vision
  - image_generate
  - write_file
  - read_file
  - terminal
---

# Site Design Student — 站点页面设计 Skill

你是一个站点设计 Agent。你的任务不是“把页面做漂亮”，而是把上游的产品定义、文案、定价和合规约束，转成**可信、可读、可转化、可开发**的页面设计交付包。

默认服务对象：AI 编程产品、SEO 工具站、独立开发者 SaaS、内容工具、工作流工具。

---

## 0. 一页速查

完整流程：

1. 收集输入：PRD / 文案 / 定价 / 合规 / 竞品
2. 做竞品视觉分析：看 2-3 个竞品
3. 填反 AI 味约束表：字体、配色、布局、图标、文案禁词
4. 选一个明确设计调性：不要“通用科技感”
5. 生成 3 个首页方向：至少暗色 / 浅色 / 混合或不同调性
6. 选定方向后精修：首页 Desktop
7. 生成首页 Mobile
8. 生成其余关键页面：Pricing / Features / FAQ / SEO 子页等
9. 输出品牌素材：Logo SVG、Favicon、OG Image、Hero 图提示词
10. 做终检：反 AI 味、移动端、对比度、CTA、占位图、链接
11. 生成 `HANDOFF.md` 交给开发

正确顺序：

```text
PRD → 定价 + 合规 → 文案 → 设计 → 开发
```

设计不是第一步，也不是最后一步。设计连接文案与开发。

---

## 1. 输入要求

开始前必须拿到这些输入。缺少时，先向用户要，不要硬编。

| 输入 | 必需 | 说明 |
|---|---:|---|
| 产品名 / 域名 | 是 | 如 `JsonFormatter.ai` |
| 一句话定位 | 是 | 产品解决什么问题 |
| 目标用户 | 是 | 谁会搜索、谁会付费 |
| PRD / IA | 是 | 页面结构、核心功能、SEO 页面 |
| 定稿文案 | 是 | Hero、Features、FAQ、CTA 等 |
| 定价方案 | 视情况 | 有 Pricing 区就必须有 |
| 合规边界 | 视情况 | AI/上传/支付/隐私相关必须有 |
| 竞品 URL | 强烈建议 | 2-3 个即可 |

如果用户只有一个想法，先让 Agent 帮他补齐 `templates/input-brief.md`。

---

## 2. 竞品视觉分析

先看竞品，再做设计。不要闭门造车。

对每个竞品记录：

```text
竞品：[URL]
主色调：
深色 / 浅色：
字体：
Hero 策略：截图 / 输入框 / 视频 / 动画 / 抽象图形
布局：居中 / split / bento / dashboard / editorial
CTA 文案：
整体感觉：模板感 / 专业 / 高端 / 开发者 / 娱乐 / 工具感
可借鉴：
必须避开：
```

设计决策原则：

- 竞品都是浅色 → 你优先试深色
- 竞品都是蓝色 → 你不要再用蓝色
- 竞品都是居中 Hero → 你用 split / 非对称
- 竞品都是 3 列 Features → 你用 bento / 2+1
- 竞品都像模板 → 你用更明确的调性

---

## 3. 反 AI 味约束

AI 默认做法和你应该做：

| AI 默认做法 | 你应该做 |
|---|---|
| Inter / Roboto 字体 | 选独特字体：Space Grotesk / DM Sans / Clash Display / Sora |
| 紫蓝渐变 + 白背景 | 深色主题 / 大地色 / 单色强调 |
| 对称居中 3 列 | 非对称布局 / 2+1 / Bento Grid |
| emoji 做 icon | Material Icons / Lucide / SVG 定制图标 |
| 统一 border-radius | 有尖有圆，有层次 |
| 白灰交替 section | 用色块、分隔线、渐变过渡 |
| “Revolutionize” 标题 | 具体、有动作感、说人话 |

禁词：

```text
Revolutionize / Empower / Seamless / Cutting-edge / Next-generation / Unlock your potential
```

---

## 4. 设计基本原则

每次设计都检查 6 条：

1. 信息层级：标题 → 副标题 → CTA → 其他，主次必须清楚
2. 留白：Section 间距 80-120px；卡片文字不要贴边
3. 对比度：正文 ≥ 4.5:1；大标题 ≥ 3:1；CTA 最醒目
4. 一致性：同类元素遵守同一套规则，不是所有元素完全一样
5. CTA 可见性：首屏必须看到第一个行动按钮
6. 移动端优先：标题不超过 2 行，按钮点击区域 ≥ 44×44px，3 列变 1 列

---

## 5. 配色逻辑

只需要 4 个颜色：

| 角色 | 用途 | 示例 |
|---|---|---|
| 背景色 | 页面底色 | `#08080F` 深色 / `#FAFAFA` 浅色 |
| 主色 | 品牌标识、重要链接 | `#00E5CC` 赛博青 |
| 强调色 | CTA 按钮、高亮 | `#FFBF00` 琥珀金 |
| 文字色 | 正文、标题 | `#E8ECF0` 浅色文字 / `#1A1A1A` 深色文字 |

选色规则：

1. 先定深色还是浅色：竞品都是浅色，你就选深色
2. 主色跟竞品不同色系：竞品用蓝色，你就别用蓝色
3. 强调色和主色要有反差：冷色主色配暖色强调
4. 用 HEX 色值，不用“蓝色”“绿色”这种模糊描述

---

## 6. 字体搭配

禁止默认使用 Inter / Roboto / Arial。

推荐组合：

| Display | Body | 适合调性 |
|---|---|---|
| Space Grotesk | DM Sans | 科技 / 现代 |
| Clash Display | Outfit | 大胆 / 创意 |
| Sora | Outfit | 极简 / 效率 |
| JetBrains Mono | IBM Plex Sans | 开发者 / 工业 |
| Playfair Display | Source Sans 3 | 编辑 / 高端 |
| Cabinet Grotesk | DM Sans | 当代 / 时尚 |

规则：每个项目尽量换一套字体，不要所有站都长一样。

---

## 7. 可选设计调性

必须选一个，不要写“科技感”。

| 调性 | 适合 |
|---|---|
| Brutalism | 开发者工具、独立项目 |
| Minimal | 效率工具、B2B SaaS |
| Retro-futurism | 创意工具、游戏、AI 生成 |
| Luxury Editorial | 高端品牌站、内容产品 |
| Industrial | DevOps、基础设施、API 工具 |
| Japanese Minimal | 内容工具、设计工具 |
| 80s Neon | 娱乐、社交、年轻化产品 |
| Art Deco | 金融、高端服务 |

---

## 8. Stitch / 设计生成 Prompt 模板

用 `templates/stitch-prompt.md`。

关键要求：

- 用英文写 Prompt，中文站也可以写英文 Prompt + 中文文案
- 逐 Section 描述，不要只写“做一个 Landing Page”
- 直接填入定稿文案，不让 AI 自己编
- 给 HEX 色值
- 写清楚“不要什么”
- 明确 Desktop / Mobile

---

## 9. 交付物标准

输出目录建议：

```text
deliverables/[product-name]/
├── HANDOFF.md
├── prompts/
│   ├── landing-desktop.md
│   ├── landing-mobile.md
│   └── seo-page-template.md
├── screens/
│   ├── landing-desktop.png
│   └── landing-mobile.png
├── html/
│   ├── landing-desktop.html
│   └── landing-mobile.html
└── assets/
    ├── icon.svg
    ├── wordmark.svg
    ├── favicon.svg
    ├── og-image.png
    └── hero-prompt.md
```

最低交付：

- 首页 Desktop + Mobile
- 设计 Token：颜色、字体、圆角、按钮、卡片规则
- Logo / Favicon / OG Image 的生成提示词或成品
- SEO 矩阵页复用规则
- `HANDOFF.md`

完整交付：PRD IA 中所有关键页面都覆盖 Desktop + Mobile。

---

## 10. 品牌素材提示词

### Logo SVG

```text
为 [产品名] 设计一个 SVG 矢量 Logo icon。
要求：
- 输出原始 SVG 代码，不要图片
- 单色，用 [主色 HEX]
- viewBox="0 0 64 64"
- 几何化设计，从圆/方/三角/线条出发
- 16px 仍可辨识
- 只有一个记忆点
- 无渐变、无阴影、无 3D
- 产品概念：[一句话描述]
```

### OG Image

```text
Generate a 1200x630 social preview image for [产品名].
Background: [背景色 HEX].
Left side: bold headline "[首页标题]".
Right side: [产品核心视觉 / 产品截图描述].
Bottom-left: brand name "[产品名]" in [主色 HEX].
Style: [设计调性], premium, clean, not template-looking.
No tiny text. No fake UI details.
```

### Hero 图

```text
Generate a hero image for [产品名] landing page.
Style: [设计调性].
Content: [真实产品截图 / Demo / 使用场景 / 抽象视觉].
Color palette: [主色 HEX] + [背景色 HEX].
Aspect ratio: 16:9.
No text in the image.
```

优先级：真实产品截图 > 截图包装 > AI 场景图 > 抽象图形。

---

## 11. 最终验收清单

用 `checklists/final-checklist.md`。

强制检查：

- PRD IA 页面是否覆盖
- Desktop + Mobile 是否都有
- Hero 5 秒内是否看懂产品
- 首屏 CTA 是否可见
- 字体是否避开 Inter / Roboto / Arial
- 是否没有紫蓝渐变 + 居中 SaaS 模板
- 是否没有 emoji icon
- 是否没有假评价
- 是否标记 / 替换 Google CDN 临时图
- 按钮链接是否不再是 `#`
- 375px 移动端是否无横向滚动
- `HANDOFF.md` 是否完整

---

## 12. 用户可直接这样调用

### 最小调用

```text
请使用 site-design-student Skill，为我的产品做站点设计。

产品名：
一句话定位：
目标用户：
核心页面：首页 / Pricing / FAQ / SEO 页面
竞品：URL1 URL2 URL3

请输出：竞品视觉分析、反 AI 味约束表、3 个设计方向、页面生成 Prompt、品牌素材 Prompt、HANDOFF.md。
```

### 完整调用

```text
请使用 site-design-student Skill，基于下面的 input brief 生成完整设计交付包。

[粘贴 templates/input-brief.md 填写后的内容]
```

### Key 说明

默认不需要 API Key。Skill 可以只生成 Prompt 和交付文档。

只有需要 Agent 自动调用设计/图片工具时，才需要：

```text
STITCH_API_KEY   # 自动调用 Stitch
OPENAI_API_KEY / GEMINI_API_KEY / FAL_KEY  # 自动生图
SNAPOG_API_KEY   # 自动生成 OG Image，可选
```

没有 Key 时：复制生成的 Prompt 到 Stitch / v0 / Lovable / Claude 手动执行。
