# 做站 SEO / GEO / AEO 学员 Skills 包

这是给学员直接使用的 Hermes Skills 包，目标不是泛泛讲 SEO，而是服务「从 0 到 1 做一个可收录、可排名、可被 AI 引用的新站」。

## 包内 Skills

- `site-seo-geo-aeo-foundation`  
  做站 SEO/GEO/AEO 总流程：从选词、IA、内容、技术验收到上线后监控。

- `site-keyword-ia-planning`  
  关键词分层、搜索意图判断、页面矩阵、URL/IA 规划。

- `site-page-aeo-content-blocks`  
  页面正文、AEO 问答块、GEO 可引用内容块、FAQ/HowTo/Comparison 写法。

- `site-technical-seo-launch-checklist`  
  robots.txt、sitemap.xml、llms.txt、canonical、schema、OG、CWV、上线验收。

- `site-seo-geo-monitoring`  
  GSC、Bing Webmaster Tools、GA4/Plausible/Umami、AI 搜索可见性监控。

## 安装

复制到 Hermes skills 目录：

```bash
mkdir -p ~/.hermes/skills/seo
cp -R ./skills/* ~/.hermes/skills/seo/
```

如果使用 profile，例如 `moyin`：

```bash
mkdir -p ~/.hermes/profiles/moyin/skills/seo
cp -R ./skills/* ~/.hermes/profiles/moyin/skills/seo/
```

刷新技能：

```text
/reload-skills
```

或新开一个 Hermes 会话。

## 推荐使用方式

### 1. 从 0 规划一个新站

```text
/skill site-seo-geo-aeo-foundation
/skill site-keyword-ia-planning
我准备做一个站：{产品/工具/主题}
目标用户：{用户}
目标市场：{国家/语言}
请输出：关键词分层、页面矩阵、URL 结构、首页/子页 SEO 约束、GEO/AEO 内容块规划。
```

### 2. 给单页补 SEO/GEO/AEO 正文

```text
/skill site-page-aeo-content-blocks
这是我的页面：{URL 或页面草稿}
目标词：{关键词}
请补：首屏定义、适合谁/不适合谁、How-to、FAQ、对比块、可被 AI 引用的摘要。
```

### 3. 上线前验收

```text
/skill site-technical-seo-launch-checklist
这是我的站点：{URL}
请按上线前 SEO/GEO/AEO 技术验收清单检查，并按 P0/P1/P2 输出问题。
```

### 4. 上线后每周巡检

```text
/skill site-seo-geo-monitoring
这是本周数据：
GSC：...
Bing Webmaster Tools：...
GA4/Plausible/Umami：...
AI 搜索测试结果：...
请输出本周 SEO/GEO/AEO 巡检报告和下周动作。
```

## 学员输入模板

```text
站点：
目标市场 / 语言：
产品一句话：
目标用户：
核心功能：
主要竞品：
候选关键词：
当前页面：
技术栈：
是否已有 GSC / BWT / Analytics：
```

## 标准交付格式

建议让 Hermes 始终按这个格式输出：

```text
结论：
风险：
P0 必做：
P1 应做：
P2 可做：
需要的数据：
可直接复制的页面/代码/文案：
```

## 核心原则

- SEO：先保证可抓取、可索引、页面意图清晰。
- GEO：让 AI 搜索知道你是谁、解决什么问题、为什么可信。
- AEO：让页面能直接回答用户问题。
- 新站不要只做首页，至少要有核心工具页、场景页、FAQ/指南页、对比/替代页。
- `/llms.txt`、`sitemap.xml`、`robots.txt` 是新站上线基础项，不是后补项。
