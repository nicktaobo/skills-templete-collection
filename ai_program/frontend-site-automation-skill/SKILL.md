---
name: frontend-site-automation
description: |
  Use when turning a PRD/design handoff into a production Next.js + Cloudflare Workers site. Automates the standard flow: validate inputs, scaffold or reuse a Next.js/OpenNext Worker project, convert HTML design sections into React components, add SEO/legal pages, analytics, mobile checks, deploy, and report verification.
version: 1.0.0
author: Nextfield Labs / ShipSite
license: MIT
metadata:
  hermes:
    tags: [frontend, nextjs, cloudflare-workers, opennext, seo, automation, shipsite]
    related_skills: [nextjs-cloudflare-workers-opennext, ship-site-frontend]
---

# Frontend Site Automation

## Overview

This skill builds a real website from a design/PRD handoff.

Default target stack:

```txt
Next.js + TypeScript + Tailwind CSS
+ OpenNext Cloudflare adapter
+ Cloudflare Workers
+ Workers Assets
+ D1 / KV / R2 / Queues when needed
```

Default deployment target is **Cloudflare Workers**, not Cloudflare Pages.

Core rule:

```txt
Design HTML is reference material, not final code.
Convert it into React components. Do not use dangerouslySetInnerHTML.
```

## Required Inputs

Ask only if a required input is missing and cannot be inferred.

```yaml
domain: yourdomain.com
project_name: yourdomain
github_owner: owner-or-org
workdir: /root/projects/yourdomain
design_dir: /absolute/path/to/design-handoff
prd_path: /absolute/path/to/PRD.md
contact_email: hello@yourdomain.com
cloudflare_target: workers
analytics:
  plausible_domain: optional
  plausible_script_url: optional
  ga_id: optional
  clarity_id: optional
  ahrefs_analytics_id: optional
  gsc_verification: optional
seo_pages:
  - slug: optional-keyword-page
    title: optional title
    description: optional description
```

## Credentials / Token Requirements

Local implementation does **not** require a Cloudflare token.

Cloudflare auth is required only for Cloudflare-side actions:

| Action | Needs Cloudflare auth? | Notes |
|---|---:|---|
| Read PRD/design, generate code | No | local only |
| `npm run dev` | No | local Next.js dev server |
| `npm run build` | No | local build |
| `npm run preview` | Usually yes | Wrangler may need Cloudflare login/account context; local runtime still may work if config is complete |
| `npm run deploy` / `npx wrangler deploy` | Yes | needs `CLOUDFLARE_API_TOKEN` or `wrangler login` |
| Create D1/KV/R2/Queues | Yes | account-level Cloudflare API access |
| Bind custom domain / routes | Yes | zone + worker permissions |
| Configure Worker secrets | Yes | `wrangler secret put` or Dashboard |
| Configure Git Integration | Yes | Cloudflare Dashboard + Git provider auth |
| Configure Email Routing | Yes | Dashboard/API + zone permissions |

Recommended auth checks for student/local use:

```bash
# 1. GitHub CLI authenticated: create repo, push code, connect GitHub workflow
 gh auth status

# 2. Cloudflare Wrangler authenticated: deploy Worker, configure secrets/bindings where allowed
npx wrangler whoami
# or: wrangler whoami
```

For most student workflows, **these two logged-in CLIs are enough**. A raw Cloudflare token is not required if `wrangler whoami` passes and the account has permission to deploy the target Worker.

Environment variables are mainly for headless CI / server automation:

```bash
CLOUDFLARE_API_TOKEN=...
CLOUDFLARE_ACCOUNT_ID=...
# optional but useful for DNS/domain automation
CLOUDFLARE_ZONE_ID=...
```

Minimum Cloudflare token permissions depend on scope, but for full automation use a token with permissions covering Workers Scripts, Workers Builds, Account Settings, D1/KV/R2 if used, and Zone DNS/Workers Routes for the target zone.

If neither `wrangler whoami` nor `CLOUDFLARE_API_TOKEN` is available, continue local implementation and stop at **READY_FOR_DEPLOY** with exact commands for the user to run.

If the user gives only a domain and design folder, infer:

```txt
project_name = domain without suffix
contact_email = hello@domain
workdir = /root/projects/project_name
cloudflare_target = workers
```

## When to Use

Use this skill when the user says:

- “帮我做站”
- “把设计稿变成网站”
- “把这个 PRD/HTML 上线”
- “从设计交付包自动做站”
- “用 Next.js + Cloudflare Workers 出站”
- “ShipSite / 一键做站 / 前端自动化”

Do not use for:

- Pure content blog only
- Documentation-only site
- Legacy Cloudflare Pages static export unless explicitly requested
- Backend-first API design without a page/design handoff

## Execution Contract

The agent must continue until one of these states is reached:

1. **DONE**: site built, verified, deployed or ready for deploy, report written.
2. **BLOCKED**: missing credential, missing design, failing upstream API, or destructive action requiring user approval.

Never stop after only writing a plan if filesystem and tools are available.

## Phase 0 — Preflight

Run these checks first:

```bash
pwd -P
node -v
npm -v
git --version
npx wrangler --version
```

Discover inputs:

```bash
find "$DESIGN_DIR" -maxdepth 3 -type f | sort | sed -n '1,120p'
```

Validate handoff:

- [ ] PRD exists or equivalent user brief exists
- [ ] Design HTML exists
- [ ] Assets/images exist or absence is acceptable
- [ ] Domain known
- [ ] Project name known
- [ ] GitHub owner/repo known or repo creation is allowed
- [ ] Cloudflare token/login available if deployment/domain/secrets are requested; otherwise mark output as READY_FOR_DEPLOY

If design has multiple versions, choose the newest `design-v*` / latest modified folder unless the user explicitly selected another one.

## Phase 1 — Project Init

If the project does not exist:

```bash
mkdir -p /root/projects
cd /root/projects

gh repo create "$GITHUB_OWNER/$PROJECT_NAME" --private --clone
cd "$PROJECT_NAME"

npm create cloudflare@latest -- . --framework=next
```

During C3 prompts, choose:

```txt
Framework: Next.js
Language: TypeScript
Deploy now: No
```

If the project already exists:

```bash
cd "$WORKDIR"
pwd -P
git status --short
```

Do not add `output: "export"`. That is a Pages/static-export path and is not the default.

Remove default assets:

```bash
rm -f public/next.svg public/vercel.svg
```

Copy design handoff:

```bash
mkdir -p design-v3
cp -R "$DESIGN_DIR"/. design-v3/
```

## Phase 2 — Design Extraction

Read the PRD and design HTML. Extract:

- brand/site name
- primary keyword
- target audience
- page list
- section list
- design tokens/colors
- assets
- CTA text and destinations
- FAQ
- SEO pages

Expected output as internal implementation notes:

```txt
Site:
Pages:
Sections:
Assets:
Colors:
CTA:
Analytics:
Routes:
Risks:
```

## Phase 3 — Component Build

Create component directories:

```bash
mkdir -p src/components/layout src/components/sections src/components/ui src/lib
```

Convert design HTML by section, not as one huge blob.

Rules:

- `class` → `className`
- `for` → `htmlFor`
- Close `<img />`, `<br />`, `<input />`
- Remove `<html>`, `<head>`, `<body>`, `<script>` wrappers
- Keep presentational sections as Server Components
- Use `"use client"` only for state/events/forms/menu/FAQ/tabs
- Do not use `dangerouslySetInnerHTML`
- Do not use `document.querySelector` for normal React interactions

Recommended files:

```txt
src/components/layout/Header.tsx
src/components/layout/Footer.tsx
src/components/sections/HeroSection.tsx
src/components/sections/FeaturesSection.tsx
src/components/sections/ToolSection.tsx
src/components/sections/HowItWorksSection.tsx
src/components/sections/PricingSection.tsx
src/components/sections/FAQSection.tsx
src/components/sections/CTASection.tsx
src/components/ui/Button.tsx
src/components/ui/Card.tsx
src/lib/analytics.ts
```

Homepage composition:

```tsx
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { HeroSection } from "@/components/sections/HeroSection";
import { FeaturesSection } from "@/components/sections/FeaturesSection";
import { FAQSection } from "@/components/sections/FAQSection";

export default function HomePage() {
  return (
    <>
      <Header />
      <main>
        <HeroSection />
        <FeaturesSection />
        <FAQSection />
      </main>
      <Footer />
    </>
  );
}
```

## Phase 4 — Routes, SEO, Legal

Required routes:

```txt
/
/privacy-policy
/terms-of-service
/sitemap.xml
/robots.txt
```

Add SEO pages from PRD if specified.

Each page needs metadata:

```tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Primary Keyword — Value Proposition | Brand",
  description: "150-160 character description with keyword and CTA.",
  openGraph: {
    title: "...",
    description: "...",
    images: ["/og-image.png"],
  },
  twitter: { card: "summary_large_image" },
};
```

Do not export `metadata` from a client component. If a page needs interactivity, keep the page server-side and import client child components.

Add `src/app/sitemap.ts`:

```tsx
export const dynamic = "force-static";

export default function sitemap() {
  const baseUrl = "https://YOUR_DOMAIN";
  return [
    { url: baseUrl, lastModified: new Date() },
    { url: `${baseUrl}/privacy-policy`, lastModified: new Date() },
    { url: `${baseUrl}/terms-of-service`, lastModified: new Date() },
  ];
}
```

Add `src/app/robots.ts`:

```tsx
export const dynamic = "force-static";

export default function robots() {
  return {
    rules: { userAgent: "*", allow: "/" },
    sitemap: "https://YOUR_DOMAIN/sitemap.xml",
  };
}
```

## Phase 5 — Links and Navigation

Replace all dead links:

```bash
rg 'href="#"|href=""|TODO|Lorem ipsum|example.com|Your Company' src app components || true
```

Required replacements:

| Link | Target |
|---|---|
| Home | `/` |
| Pricing | `/#pricing` |
| FAQ | `/#faq` |
| Privacy | `/privacy-policy` |
| Terms | `/terms-of-service` |
| Support | `mailto:hello@domain.com` |
| Primary CTA | tool section, signup, checkout, or requested destination |

Every SEO subpage should link back to related pages or a browse-all block.

## Phase 6 — Interactions

Implement required interactions:

- FAQ accordion: client component with `useState` or native `<details>`
- Mobile menu: client component
- Pricing toggle if present
- Tool form states if present: empty, loading, success, error
- CTA analytics event

Analytics event helper:

```ts
export function trackEvent(name: string, props?: Record<string, unknown>) {
  if (typeof window === "undefined") return;
  const w = window as typeof window & {
    plausible?: (event: string, options?: { props?: Record<string, unknown> }) => void;
    gtag?: (...args: unknown[]) => void;
  };
  w.plausible?.(name, { props });
  w.gtag?.("event", name, props || {});
}
```

Suggested event names:

```txt
hero_cta_click
pricing_cta_click
faq_open
tool_submit
tool_result_view
copy_result_click
outbound_click
```

## Phase 7 — Analytics

Create `src/components/Analytics.tsx` using `next/script`.

Environment variables:

```bash
NEXT_PUBLIC_PLAUSIBLE_DOMAIN=yourdomain.com
NEXT_PUBLIC_PLAUSIBLE_SCRIPT_URL=https://plausible.io/js/script.js
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
NEXT_PUBLIC_CLARITY_ID=xxxxxxxxxx
NEXT_PUBLIC_AHREFS_ANALYTICS_ID=xxxxxxxxxx
```

Rules:

- `NEXT_PUBLIC_*` is public and build-time.
- Configure `NEXT_PUBLIC_*` in Cloudflare Workers Builds variables if using Git Integration.
- Runtime secrets go to Worker Variables & Secrets or `npx wrangler secret put KEY_NAME`.
- GSC verification goes in metadata `verification.google`.

## Phase 8 — Mobile and Responsive QA

Check these widths:

```txt
320px
360px
375px
390px
768px
1024px
```

Console overflow check:

```js
document.documentElement.scrollWidth > document.documentElement.clientWidth
```

Find overflow elements:

```js
[...document.querySelectorAll("*")]
  .filter((el) => el.scrollWidth > document.documentElement.clientWidth)
  .map((el) => ({
    tag: el.tagName,
    class: el.className,
    width: el.scrollWidth,
    text: el.textContent?.slice(0, 80),
  }));
```

Common fixes:

```txt
Use px-4 sm:px-6 lg:px-8
Use max-w-full on images/cards/buttons
Use grid-cols-1 sm:grid-cols-2 lg:grid-cols-3
Use break-words for long URLs/tokens
Use text-3xl sm:text-4xl lg:text-6xl for H1
Use min-h-11 for touch targets
Use font-size: 16px for input/select/textarea on iOS
```

## Phase 9 — Build and Preview

Run:

```bash
npm run build
npm run preview
```

`npm run preview` is mandatory because production runs in Cloudflare Workers/workerd, not the normal Next.js dev server.

If preview starts a long-running server, verify with browser or curl, then stop it before finalizing.

## Phase 10 — Deploy

Deployment discipline:

```bash
git status
git add -A
git commit -m "feat: launch <domain> on cloudflare workers"
git push origin main
```

Before running Cloudflare-side commands, check auth:

```bash
npx wrangler whoami
# or ensure CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID are set
```

If Cloudflare auth is missing, do **not** fake deployment. Stop as **READY_FOR_DEPLOY** and report:

```txt
Local build complete.
Cloudflare deploy blocked: missing CLOUDFLARE_API_TOKEN / wrangler login.
Run: npx wrangler login
Then: npm run deploy
```

If Cloudflare Git Integration is connected, `git push` triggers Workers Builds.

If not connected and auth is available:

```bash
npm run deploy
# or
npx wrangler deploy
```

Bind custom domain:

```txt
Cloudflare Dashboard
→ Workers & Pages
→ Select Worker
→ Settings
→ Domains & Routes
→ Add
→ Custom domain
```

Add:

```txt
yourdomain.com
www.yourdomain.com
```

## Phase 11 — Post-Deploy Verification

Verify:

```txt
[ ] https://yourdomain.com works
[ ] https://www.yourdomain.com works
[ ] HTTP redirects to HTTPS
[ ] Homepage visual is correct
[ ] Mobile layout works
[ ] All CTAs clickable
[ ] Footer links correct
[ ] /privacy-policy works
[ ] /terms-of-service works
[ ] /sitemap.xml works
[ ] /robots.txt works
[ ] Analytics scripts load
[ ] GSC verification passes if configured
[ ] Email Routing test email received if configured
```

If API/data exists:

```txt
[ ] /api/health works
[ ] Forms submit correctly
[ ] D1/KV/R2 bindings work
[ ] Runtime secrets work
```

## Final Report Format

Write a report at:

```txt
deliverables/frontend/implementation-report-YYYYMMDD.md
```

Report must include:

```md
# Frontend Implementation Report

## Inputs
- Domain:
- Project:
- Design directory:
- PRD:

## Changes
- Files/components created:
- Routes created:
- Analytics added:
- SEO/legal files:

## Verification
- npm run build:
- npm run preview:
- Mobile checks:
- Dead link scan:
- SEO files:

## Deployment
- Git commit:
- Worker URL:
- Custom domain:
- Cloudflare Git Integration:

## Blockers / Follow-ups
- ...
```

## Common Pitfalls

1. **Using Cloudflare Pages by habit**: default is Workers + OpenNext.
2. **Adding `output: "export"`**: breaks dynamic Next.js capabilities and is not the default path.
3. **Skipping `npm run preview`**: dev server does not match Workers runtime.
4. **Using `dangerouslySetInnerHTML` for design HTML**: convert to React components instead.
5. **Putting secrets in `NEXT_PUBLIC_*`**: public env vars are visible in browser bundles.
6. **Putting metadata in client components**: page-level metadata must stay in server components.
7. **Leaving `href="#"` dead links**: replace before build.
8. **Forgetting legal pages**: Privacy and Terms are P0 for launch.
9. **Not checking mobile 320/375/390**: desktop-only sites fail conversion.
10. **Deploying dirty working tree**: commit first, then deploy or push.

## Verification Checklist

- [ ] Inputs resolved or blockers reported
- [ ] Project initialized or existing project inspected
- [ ] Design copied into repo
- [ ] HTML converted to React components
- [ ] No `dangerouslySetInnerHTML` except unavoidable third-party analytics script blocks
- [ ] No `output: "export"`
- [ ] All required routes exist
- [ ] Metadata, sitemap, robots exist
- [ ] Analytics configured when IDs are provided
- [ ] Mobile overflow checked
- [ ] `npm run build` passes
- [ ] `npm run preview` passes or blocker documented
- [ ] Git commit created
- [ ] Deployed or deployment blocker documented
- [ ] Final report written
