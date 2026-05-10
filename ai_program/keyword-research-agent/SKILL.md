---
name: keyword-research-agent
description: >
  Find and validate AI tool site keyword opportunities using discoverkeywords.co API.
  Complete workflow: keyword expansion → trend comparison → SERP analysis → final opportunity keywords.
  Use when user asks to: find keywords for an AI tool site, research niche opportunities,
  validate whether a keyword is worth pursuing, run keyword research, analyze SERP competition,
  find AI tool site directions, or check if a market is worth entering.
  Trigger phrases: "find keywords", "keyword research", "AI tool site", "which direction to build",
  "validate keyword", "SERP analysis", "market opportunity", "找词", "需求挖掘", "竞品验证".
---

# Keyword Research Agent

Automated AI tool site keyword research using discoverkeywords.co API.

## Architecture

```
Skill (gk_api.py) → discoverkeywords.co API
                  ↓
         Server-side processing (DataForSEO + LLM + SERP + Trends)
                  ↓
         Returns final opportunity keywords (new/old-hot)
```

**All computation happens server-side.** The skill simply calls the API and polls for results.

## Prerequisites

- `GK_API_KEY` environment variable — API key from discoverkeywords.co dashboard (Settings → API Keys)
- `python3` + `requests` (`pip install requests`)
- `whois` for domain age checks (optional)

## How to Use

### Complete Workflow (Recommended)

```bash
# Navigate to skill directory first
cd /path/to/keyword-research-agent

# Use default seed keywords (127 built-in)
python3 scripts/gk_api.py research --report

# Use custom seed keywords
python3 scripts/gk_api.py research "ai tattoo generator" "ai portrait generator" --report

# Output options
python3 scripts/gk_api.py research --names-only      # Only keyword names
python3 scripts/gk_api.py research --report          # Markdown report (recommended)
python3 scripts/gk_api.py research --raw            # Full API response (debug)
```

### Expand Only (Without Comparison)

```bash
# Get expanded keywords, no trend comparison
python3 gk_api.py expand "ai generator" --names-only
```

## Response Structure

```json
{
  "status": "complete",
  "opportunities": [
    {
      "keyword": "square face generator",
      "verdict": "close",
      "ratio": 1.48,
      "freshness": {
        "status": "new",
        "label": "新词",
        "window": "90d"
      },
      "intent": {
        "label": "Utility Tools",
        "demand": "Find an online tool to generate and customize a square face icon and download it."
      }
    }
  ],
  "stableOld": [...],
  "expand": { "...": "full expand result" },
  "compare": { "...": "full compare result" }
}
```

### Key Fields

| Field | Description | Values |
|---|---|---|
| `verdict` | Trend comparison vs benchmark | `strong` > `pass` > `close` > `watch` > `fail` |
| `freshness.status` | Keyword age/type | `new`, `old_hot`, `stable_old`, `unclear` |
| `freshness.window` | Recent rise window | `7d`, `30d`, `90d`, `none` |
| `ratio` | Trend strength vs benchmark | 1.0x = baseline, >1.0x = stronger |

## Decision Guide

### Verdict

| Verdict | Action | Description |
|---|---|---|
| `strong` | ✅ Pursue | Trending strongly above benchmark |
| `pass` | ✅ Pursue | Good opportunity, steady or rising |
| `close` | ⚠️ Verify manually | Close to pass, manual check needed |
| `watch` | ⏸️ Observe | Monitor for trend changes |
| `fail` | ❌ Skip | Declining, no opportunity |

### Freshness

| Status | Action | Description |
|---|---|---|
| `new` | ✅ Pursue | Recently emerged (7d/30d/90d window) |
| `old_hot` | ✅ Pursue | Old word with recent surge |
| `stable_old` | ❌ Skip | Stable for years, not a new opportunity |

## 5-Step Workflow

### Step 1: Run Research

```bash
python3 gk_api.py research --report > results.md
```

Server-side pipeline:
- ✅ Keyword expansion (DataForSEO + Google Trends)
- ✅ AI-powered filtering (removes junk)
- ✅ Trend comparison vs benchmark
- ✅ SERP competition analysis
- ✅ Final opportunity classification

### Step 2: Review Opportunities

From "值得继续" table:
1. Check `intent.demand` — Is it a tool/saaS need?
2. Check `verdict` — Is it strong or pass?
3. Check `freshness.status` — Is it new or old_hot?

### Step 3: Manual SERP Verification (Optional but Recommended)

1. Google search the keyword (incognito)
2. Check intent — Tool pages or blog posts?
3. Check competition — Niche sites or big brands?
4. Check features — Can we differentiate?

**Red flags**:
- AI Overview present
- Featured Snippet present
- Only big brands (Adobe, Canva, Grammarly)

**Green flags**:
- Multiple niche tool sites (.ai, .app, .io)
- Mix of authority + niche

### Step 4: Competitor Domain Age (Optional)

```bash
python3 scripts/domain_age.py tattoogen.ai blackink.ai coloringpage.ai
```

- < 2 years → ✅ Strong opportunity
- 2-5 years → ⚠️ Moderate
- > 5 years → ❌ Deep moat

### Step 5: Product Direction

From "切入方向" column:
- `generator` → Template-based, batch export
- `editor` / `enhancer` → Upload-based, before/after comparison
- `checker` / `detector` → Quick validation, explain why

## Scripts

| Script | Purpose | Usage |
|---|---|---|
| `gk_api.py research` | Complete workflow | `python3 gk_api.py research --report` |
| `gk_api.py expand` | Expand only | `python3 gk_api.py expand --names-only` |
| `domain_age.py` | Check domain age | `python3 scripts/domain_age.py domain.com` |

## Options

| Flag | Description |
|---|---|
| `--names-only` | Output only keyword names, one per line |
| `--report` | Output Markdown report (recommended) |
| `--raw` | Output full API response (debug) |

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GK_API_KEY` | **Yes** | API key from discoverkeywords.co dashboard |
| `GK_SITE_URL` | No | Override website URL (default: https://discoverkeywords.co) |
| `GK_BENCHMARK` | No | Override trend benchmark (default: gpts) |

## Decision Boundaries

**Stop** when:
- Found 2-3 strong/pass opportunities
- All remaining stable_old or fail
- Quota exceeded

**Pause** when:
- 1 strong + 3-5 close/watch → Pursue strong, observe rest
- No clear winners but several close → Expand seeds and retry
