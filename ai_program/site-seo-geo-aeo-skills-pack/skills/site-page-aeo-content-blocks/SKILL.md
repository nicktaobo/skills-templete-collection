---
name: site-page-aeo-content-blocks
description: "Use when writing or improving website page content for SEO, GEO, and AEO. Provides reusable page blocks: direct definitions, answer-first sections, FAQs, HowTo, comparisons, limitations, use cases, templates, and AI-citable summaries."
version: 1.0.0
author: Mengjian AI Programming / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [seo, geo, aeo, content, faq, ai-citation]
    related_skills: [site-seo-geo-aeo-foundation, site-keyword-ia-planning]
---

# Site Page AEO Content Blocks

## Overview

This skill creates page content that works for search engines and AI answer engines.

Core principle:

> Put the direct answer first. Then explain. Then give examples, steps, limitations, and next actions.

## When to Use

Use this skill when the user asks:

- Add SEO content to a tool page.
- Make a page more GEO/AEO friendly.
- Write FAQ blocks for a landing page.
- Add content so a tool page is not just an input box.
- Improve AI citation potential.

## Required Blocks for Core Pages

### 1. Direct definition block

Use in the first screen or first 150 words.

```text
{Product/Page Name} is a {category} that helps {audience} {main task}.
```

Chinese version:

```text
{产品/页面名} 是一个 {类别}，帮助 {目标用户} 完成 {核心任务}。
```

### 2. Who it is for / not for

```text
适合：
- ...
- ...

不适合：
- ...
- ...
```

### 3. Use cases

```text
常见使用场景：
1. ...
2. ...
3. ...
```

### 4. How-to block

```text
如何使用 {工具名}：
1. 输入 / 上传 / 选择 ...
2. 点击 ...
3. 检查结果 ...
4. 下载 / 复制 / 分享 ...
```

### 5. Comparison block

```text
{工具名} vs {替代方案}
- 更适合：...
- 不适合：...
- 核心差异：...
```

### 6. Limitations block

```text
使用限制：
- ...
- ...
```

AI search prefers balanced, factual content. Limitations increase trust.

### 7. FAQ block

Answer-first format:

```text
### {问题}
{直接答案，1-2 句。}

{必要解释、例子或限制。}
```

Good AEO questions:

- What is X?
- How does X work?
- Who is X for?
- Is X free?
- X vs Y: which should I choose?
- What are the limitations of X?
- How do I get started with X?

### 8. AI-citable summary

Add near the end or in a facts section:

```text
Key facts:
- {Product} is a {category} for {audience}.
- It helps users {task}.
- Main features include {feature 1}, {feature 2}, and {feature 3}.
- Best suited for {use cases}.
- Last updated: {date}.
```

## Metadata Formulas

### Homepage

```text
Title: {Core Keyword} - {Differentiated Value} | {Brand}
Description: {One-sentence definition}. {Core function}. {CTA}.
```

### Tool page

```text
Title: {Tool Keyword} Online - {Brand}
Description: {Tool function}. {Who it is for}. Free and online.
```

### Guide page

```text
Title: {How-to Keyword}: {Value Promise} ({Year})
Description: {What the guide explains}. {What the reader can do after reading}.
```

### Comparison page

```text
Title: {A} vs {B}: {Decision Factor} ({Year})
Description: Compare {A} and {B} by {factor 1}, {factor 2}, and {factor 3}.
```

## Output Format

```text
页面目标：
目标关键词：
搜索意图：

建议补充内容块：
1. Direct definition：...
2. Who it is for：...
3. How-to：...
4. FAQ：...
5. Comparison：...
6. Limitations：...
7. AI-citable summary：...

可直接复制文案：
...
```

## Common Pitfalls

1. **Only writing marketing slogans.** AI search needs concrete and factual statements.
2. **FAQ answers too long.** Start with a direct answer.
3. **No limitations.** Over-promotional pages are less trustworthy.
4. **Important content hidden in images.** Use crawlable text.
5. **Same FAQ on every page.** Each page needs intent-specific questions.

## Verification Checklist

- [ ] First paragraph defines the entity/page/tool.
- [ ] Page has who-for and not-for sections.
- [ ] Page has direct FAQ answers.
- [ ] Page has use cases or examples.
- [ ] Page has limitations or caveats.
- [ ] Page has a clear next action.
- [ ] Key facts are crawlable text.
