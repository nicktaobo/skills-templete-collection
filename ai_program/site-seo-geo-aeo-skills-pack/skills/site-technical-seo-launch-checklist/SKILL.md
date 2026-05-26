---
name: site-technical-seo-launch-checklist
description: "Use when checking whether a new website is technically ready for SEO/GEO/AEO launch. Covers robots.txt, sitemap.xml, llms.txt, canonical, noindex, schema, metadata, OG/Twitter, internal links, 404, performance, and indexing blockers."
version: 1.0.0
author: Mengjian AI Programming / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [technical-seo, launch, sitemap, robots, llms-txt, schema, cwv]
    related_skills: [site-seo-geo-aeo-foundation, site-seo-geo-monitoring]
---

# Site Technical SEO Launch Checklist

## Overview

This skill checks whether a new site is ready to be crawled, indexed, shared, and cited.

Core principle:

> If technical SEO is broken, content optimization is wasted.

## When to Use

Use this skill when the user asks:

- Is this site ready to launch?
- Check technical SEO before publishing.
- What files do I need for SEO/GEO?
- Review robots/sitemap/canonical/schema.
- Why is my site not indexed?

## P0 Launch Requirements

A site should not be considered SEO-ready until these exist:

- `/robots.txt` returns 200.
- `/sitemap.xml` returns 200 and lists canonical URLs.
- `/llms.txt` returns 200 and describes the site for AI systems.
- Core pages return 200.
- Core pages are not `noindex`.
- Canonical is correct.
- Each indexable page has title, meta description, H1.
- Homepage links to core pages.
- Legal pages exist where needed.
- 404 page exists.

## robots.txt Minimum

```text
User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
```

Avoid accidentally blocking assets needed for rendering.

## sitemap.xml Requirements

- Contains canonical URLs only.
- Excludes noindex pages.
- Excludes duplicate parameter URLs.
- Includes homepage and P0 pages.
- Updates when new pages are published.

## llms.txt Requirements

`/llms.txt` is a launch requirement for GEO sites.

Minimum structure:

```text
# {Site Name}

> {One-sentence definition}

## Core Pages

- [Homepage](https://example.com/): {description}
- [{Core Page}](https://example.com/{slug}): {description}

## Key Facts

- {Fact 1}
- {Fact 2}
- {Fact 3}

## Contact

- Website: https://example.com
- Contact: {email or contact page}

Last updated: {date}
```

Rules:

- Only include true facts.
- Link to pages that return 200.
- Keep it concise and maintained.

## Page-Level Checks

For every indexable page:

- Unique title, ideally ≤ 60 chars.
- Unique meta description, ideally ≤ 155 chars.
- Exactly one H1.
- Logical H2/H3 hierarchy.
- Self-referencing canonical unless intentionally canonicalized.
- OG title, description, image.
- Twitter card.
- Image alt where images matter.
- Internal links to related pages.
- No `href="#"` dead links.

## Schema Checks

Minimum:

- Organization
- WebSite
- WebPage

Optional by page:

- FAQPage
- SoftwareApplication
- BreadcrumbList
- HowTo
- Product

Rules:

- Schema must match visible page content.
- Validate rendered DOM, not just raw HTML.
- Do not invent ratings, reviews, or prices.

## Performance / Rendering Checks

Targets:

- LCP < 2.5s
- CLS < 0.1
- INP < 200ms

Check:

- Main content visible without complex JS dependency.
- Hero image compressed.
- Lazy load non-critical images.
- Fonts do not cause severe layout shift.
- Mobile layout is readable.

## Output Format

```text
结论：可上线 / 暂不建议上线

P0 阻塞：
- ...

P1 应修：
- ...

P2 可优化：
- ...

逐项检查：
- robots.txt：通过 / 失败
- sitemap.xml：通过 / 失败
- llms.txt：通过 / 失败
- canonical：通过 / 失败
- metadata：通过 / 失败
- schema：通过 / 失败
- internal links：通过 / 失败
- performance：通过 / 风险
```

## Common Pitfalls

1. **Missing llms.txt.** For AI-search-oriented sites, this is not optional.
2. **Canonical points to the wrong page.** This can suppress indexing.
3. **Schema only exists in raw code but not rendered DOM.** Always verify rendered output.
4. **Noindex accidentally left from staging.** Common launch blocker.
5. **Only homepage in sitemap.** P0 pages need discovery.

## Verification Checklist

- [ ] robots.txt exists and allows crawling.
- [ ] sitemap.xml exists and lists canonical P0 pages.
- [ ] llms.txt exists and is factual.
- [ ] No accidental noindex on core pages.
- [ ] Canonical is correct.
- [ ] Metadata exists and is unique.
- [ ] Schema matches visible content.
- [ ] Internal links expose P0 pages.
- [ ] Mobile performance is acceptable.
