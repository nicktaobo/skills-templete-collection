---
name: site-seo-geo-monitoring
description: "Use when monitoring post-launch SEO, GEO, and AEO performance for a new site. Covers Google Search Console, Bing Webmaster Tools, GA4/Plausible/Umami, AI search mention/citation checks, and weekly action reports."
version: 1.0.0
author: Mengjian AI Programming / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [seo, geo, aeo, monitoring, gsc, bing-webmaster-tools, analytics]
    related_skills: [site-seo-geo-aeo-foundation, site-technical-seo-launch-checklist]
---

# Site SEO / GEO Monitoring

## Overview

This skill creates a weekly monitoring loop after a site launches.

Core principle:

> GSC, BWT, and analytics are not reports. They are debugging inputs.

Monitor search visibility, indexation, traffic quality, conversion, and AI citation together.

## When to Use

Use this skill when the user asks:

- What should I check after launching a site?
- Interpret GSC/BWT/Analytics data.
- Why do I have impressions but no clicks?
- Why is Bing important for ChatGPT Search?
- How do I monitor AI search visibility?
- Generate a weekly SEO/GEO report.

## Google Search Console Checks

Daily/weekly:

1. **Pages**  
   Which pages are indexed and not indexed?

2. **Sitemaps**  
   Was sitemap successfully read?

3. **Search results**  
   Check queries / pages / clicks / impressions / CTR / position.

4. **URL Inspection**  
   Are core pages indexable?

Diagnosis:

- **Impressions but no clicks** → improve title / meta description.
- **Indexed but no impressions** → keyword intent or page content mismatch.
- **Crawled - currently not indexed** → quality / duplicate / thin content issue.
- **Discovered - currently not indexed** → low authority, weak internal links, low crawl priority.

## Bing Webmaster Tools Checks

Check:

- Sitemap submitted.
- URL indexed.
- Site Explorer crawl status.
- Bing visibility for ChatGPT Search-related goals.

Reminder:

> If ChatGPT Search matters, Bing cannot be ignored.

## Analytics Checks: GA4 / Plausible / Umami

At least check:

- Traffic sources: organic, referral, direct, social.
- Landing pages.
- Conversion events: button clicks, signups, generation, downloads, payments.
- Country / device.
- Time on page and bounce/engagement.

Diagnosis:

- Organic grows but no conversions → wrong intent or weak CTA.
- Referral converts well → double down on similar sources.
- High bounce on mobile → first screen, speed, or layout problem.
- Important landing pages get no visits → check indexation and internal links.

## AI Search Visibility Checks

Test query groups:

- Brand query: `{brand}`
- Category query: `best {category} tool`
- Task query: `how to {task}`
- Alternative query: `{competitor} alternative`
- Comparison query: `{brand} vs {competitor}`
- Definition query: `what is {category}`

Track:

- Mention rate: how often the brand appears.
- Citation rate: how often the site is linked/cited.
- Competitors recommended instead.
- Source URLs AI systems cite.
- Missing content categories.

## Weekly Report Format

```text
## SEO/GEO/AEO 周报 - {站点} - {日期}

结论：
- 本周最大问题：
- 本周最大机会：

1. 索引状态
- GSC Pages：
- URL Inspection：
- Bing indexed：

2. 搜索表现
- clicks：
- impressions：
- CTR：
- position：
- 有曝光没点击页面：
- 有收录没曝光页面：

3. 流量质量
- organic：
- referral：
- direct：
- social：
- top landing pages：
- conversion events：

4. AI 搜索可见性
- ChatGPT Search：
- Perplexity：
- Google AI Overview：
- Gemini：
- 竞品替代：

5. 下周动作
P0：
P1：
P2：
```

## Common Pitfalls

1. **Only watching traffic.** New sites should watch impressions and indexation first.
2. **Ignoring Bing.** Bing matters for ChatGPT Search scenarios.
3. **No conversion events.** Without events, you cannot judge traffic quality.
4. **Not separating page types.** Homepage, tool pages, guides, and comparisons behave differently.
5. **No AI visibility baseline.** You need a starting point before optimizing GEO.

## Verification Checklist

- [ ] GSC sitemap and Pages are checked.
- [ ] BWT sitemap/indexed/Site Explorer are checked.
- [ ] Analytics sources and landing pages are checked.
- [ ] Conversion events are checked.
- [ ] AI search mention/citation tests are recorded.
- [ ] Next actions are split into P0/P1/P2.
