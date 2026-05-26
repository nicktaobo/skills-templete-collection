---
name: site-seo-geo-aeo-foundation
description: "Use when planning or reviewing a new website for SEO, GEO, and AEO from strategy to launch. Covers keyword intent, page matrix, metadata, content blocks, technical SEO, llms.txt, and post-launch monitoring."
version: 1.0.0
author: Mengjian AI Programming / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [seo, geo, aeo, site-building, launch, ai-search]
    related_skills: [site-keyword-ia-planning, site-page-aeo-content-blocks, site-technical-seo-launch-checklist, site-seo-geo-monitoring]
---

# Site SEO / GEO / AEO Foundation

## Overview

This is the umbrella skill for building a new site that can be crawled, indexed, ranked, and cited by AI search engines.

Definitions:

- **SEO**: make pages discoverable, indexable, relevant, and competitive in search engines.
- **GEO**: make the site/entity parseable, quotable, and citable by ChatGPT Search, Perplexity, Gemini, and Google AI Overviews.
- **AEO**: make pages answer user questions directly with clear answer blocks, FAQ, HowTo, checklists, and summaries.

Core principle:

> Technical SEO first. Then page intent. Then GEO/AEO content blocks. Then distribution and monitoring.

## When to Use

Use this skill when the user asks:

- Plan SEO/GEO/AEO for a new site.
- Review whether a site is ready to launch.
- Turn a product idea into an SEO page matrix.
- Build a site for AI search visibility.
- Create a student-friendly website SEO workflow.

## End-to-End Workflow

### Step 1: Clarify the site entity

Capture:

- Site name
- One-sentence definition
- Category
- Target user
- Main task solved
- Target country/language
- Competitors / alternatives

GEO definition formula:

```text
{Site Name} is a {category} that helps {audience} {main task}.
```

### Step 2: Keyword and intent planning

Separate:

- Homepage core keyword
- Core tool/product pages
- Use-case pages
- Comparison / alternative pages
- Templates / examples pages
- Guides / FAQ pages
- Programmatic SEO pages

Do not create pages only by swapping variables. Every indexable page needs unique intent and unique value.

### Step 3: IA and URL structure

Recommended new-site structure:

```text
/
/features or /tools/[tool]
/use-cases/[scenario]
/templates/[template]
/examples/[example]
/compare/[competitor]
/alternatives
/guides/[topic]
/faq
/pricing
/about
/contact
/privacy
/terms
/llms.txt
/sitemap.xml
/robots.txt
```

### Step 4: Page-level SEO baseline

Every indexable page needs:

- Unique title
- Unique meta description
- Unique H1
- Clear H2 structure
- Canonical
- Internal links
- OG / Twitter card
- Visible text content, not only UI controls
- Schema if applicable

### Step 5: GEO/AEO content baseline

Every core page should answer:

1. What is this page/tool?
2. Who is it for?
3. What task does it solve?
4. How does it work?
5. How is it different from alternatives?
6. What are its limitations?
7. What should the user do next?

### Step 6: Technical launch baseline

Must exist before launch:

- `/robots.txt`
- `/sitemap.xml`
- `/llms.txt`
- Valid canonical
- Basic schema
- 404 page
- Legal pages
- GSC / Bing Webmaster Tools ready
- Analytics installed

### Step 7: Post-launch monitoring

Monitor:

- GSC Pages / Sitemaps / Search results / URL Inspection
- Bing sitemap / indexed / Site Explorer
- GA4 / Plausible / Umami sources and conversions
- AI search mention rate and citation rate

## Output Format

```text
结论：
当前阶段：策略 / 内容 / 技术验收 / 上线后监控

P0：必须做，否则影响收录/上线
- ...

P1：应做，影响排名/GEO/AEO
- ...

P2：可做，影响长期增长
- ...

可直接复制执行：
- URL 结构：...
- Metadata 模板：...
- 内容块：...
- 技术清单：...
```

## Common Pitfalls

1. **Only building a homepage.** New sites need supporting pages for intent coverage.
2. **Skipping technical SEO.** Content cannot compensate for blocked crawling or missing canonical.
3. **Writing slogan-only pages.** AI search needs concrete definitions, facts, comparisons, and FAQs.
4. **Programmatic thin content.** Variable-swapped pages without unique value are a risk.
5. **Ignoring Bing.** ChatGPT Search makes Bing Webmaster Tools relevant.

## Verification Checklist

- [ ] Site entity definition is clear.
- [ ] Keyword and intent map exists.
- [ ] Page matrix has unique intent per page.
- [ ] Core pages have metadata, H1, canonical, internal links.
- [ ] Core pages have AEO answer blocks.
- [ ] `/robots.txt`, `/sitemap.xml`, `/llms.txt` exist.
- [ ] GSC, BWT, and analytics are planned or installed.
