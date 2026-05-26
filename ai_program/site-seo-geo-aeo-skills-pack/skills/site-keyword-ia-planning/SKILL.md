---
name: site-keyword-ia-planning
description: "Use when turning a site idea into keyword layers, search intent mapping, page matrix, URL structure, internal linking, and programmatic SEO boundaries for SEO/GEO/AEO-ready websites."
version: 1.0.0
author: Mengjian AI Programming / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [seo, keyword-research, ia, programmatic-seo, site-structure]
    related_skills: [site-seo-geo-aeo-foundation, site-page-aeo-content-blocks]
---

# Site Keyword and IA Planning

## Overview

This skill turns a site idea into an SEO/GEO/AEO page plan.

Goal:

> One search intent = one strong page. One page = one clear job.

## When to Use

Use this skill when the user asks:

- What pages should this site have?
- Which keyword goes to homepage vs subpage?
- How should I design URL structure?
- Can this idea support programmatic SEO?
- Which pages should be P0/P1/P2?

## Keyword Layers

### Homepage keyword

Choose the broadest high-value term that describes the whole product/site.

Criteria:

- Represents the category.
- Matches the main user task.
- Can support brand positioning.
- Not too narrow.

### Core tool/product pages

Use for feature-level or task-level intent.

Examples:

```text
/json-formatter
/yaml-validator
/hash-generator
```

### Use-case pages

Use for audience, scenario, or job-to-be-done intent.

Examples:

```text
/for-developers
/use-cases/api-debugging
/use-cases/linkedin-headshots
```

### Comparison / alternative pages

Use for commercial investigation intent.

Examples:

```text
/compare/a-vs-b
/alternatives/product-name
/best-ai-tools-for-x
```

### Templates / examples pages

Use for users who want something reusable.

Examples:

```text
/templates
/templates/resume
/examples
/examples/github-readme
```

### Guides / FAQ pages

Use for informational and AEO intent.

Examples:

```text
/guides/how-to-format-json
/faq
```

## Search Intent Classification

Classify every keyword:

- **Do**: user wants to perform a task.
- **Know**: user wants explanation.
- **Compare**: user wants A vs B / alternatives.
- **Buy**: user wants pricing or vendor choice.
- **Navigate**: user wants a specific brand or tool.

Do not mix too many intents on one page.

## Page Matrix Output

Use this format:

```text
页面：
URL：
主关键词：
次关键词：
搜索意图：Do / Know / Compare / Buy / Navigate
页面角色：首页 / 工具页 / 场景页 / 对比页 / 模板页 / 指南页
GEO 内容块：定义 / 对比 / FAQ / 步骤 / 限制 / 模板
AEO 问题：
内链入口：
优先级：P0 / P1 / P2
```

## IA Rules

- Homepage links to all P0 pages.
- P0 pages appear in header or footer.
- Related pages cross-link to each other.
- Blog/guides link back to core tool pages.
- Programmatic pages have hub pages.
- Avoid orphan pages.
- Avoid many URLs serving the same intent.

## Programmatic SEO Boundaries

Only create programmatic pages when each page has at least one unique element:

- Unique scenario
- Unique example
- Unique FAQ
- Unique template
- Unique data point
- Unique comparison
- Unique output/sample

Bad pattern:

```text
{keyword} + same paragraph + same FAQ + same CTA
```

Good pattern:

```text
Different intent + different example + different FAQ + different internal links
```

## Output Format

```text
关键词分层：
- 首页主词：
- P0 页面：
- P1 页面：
- P2 页面：
- 暂不做：

页面矩阵：
1. URL：...
   Intent：...
   主词：...
   GEO/AEO 内容块：...
   内链：...

风险：
- 重复意图：...
- 薄内容：...
- 大平台垄断：...
```

## Common Pitfalls

1. **Homepage keyword too narrow.** It limits the whole site.
2. **Subpages cannibalize homepage.** Different pages must target different intent.
3. **Programmatic pages are too thin.** Unique value is mandatory.
4. **No hub pages.** Large page sets need category/hub pages.
5. **No internal links.** Discovery and crawl priority suffer.

## Verification Checklist

- [ ] Homepage keyword is broad enough.
- [ ] Each P0 page has unique intent.
- [ ] URL slugs are short, lowercase, and semantic.
- [ ] P0 pages are linked from homepage/header/footer.
- [ ] Programmatic pages have unique value.
- [ ] Comparison/alternative pages are separated from guides.
