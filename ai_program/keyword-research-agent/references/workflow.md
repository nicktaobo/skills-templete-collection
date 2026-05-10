# Keyword Research Workflow - discoverkeywords.co API

## Prerequisites

- `GK_API_KEY` environment variable — API key from discoverkeywords.co dashboard (Settings → API Keys)
- `python3` + `requests` (`pip install requests`)
- `whois` for domain age checks (optional, Step 4)

## Environment Setup

```bash
export GK_API_KEY="your_api_key_from_discoverkeywords_co"
# Optional: override website URL
export GK_SITE_URL="https://discoverkeywords.co"
```

## How to Use

### Option 1: Complete Workflow (Recommended)

```bash
# Navigate to skill directory first
cd /path/to/keyword-research-agent

# Use default seed keywords (127 built-in)
python3 scripts/gk_api.py research --report

# Use custom seed keywords
python3 gk_api.py research "ai tattoo generator" "ai portrait generator" --report

# Output options
python3 gk_api.py research --names-only      # Only keyword names
python3 gk_api.py research --report          # Markdown report (recommended)
python3 gk_api.py research --raw            # Full API response (debug)
```

### Option 2: Expand Only (Without Comparison)

```bash
# Get expanded keywords, no trend comparison
python3 gk_api.py expand "ai generator" --names-only
```

## Understanding Results

### Response Structure

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
| `intent.label` | User intent category | Utility Tools, Image Generation, etc. |
| `intent.demand` | What user wants | "Find an online tool to..." |
| `ratio` | Trend strength vs benchmark | 1.0x = baseline, >1.0x = stronger |

### Verdict Guide

| Verdict | Action | Description |
|---|---|---|
| `strong` | ✅ Pursue | Trending strongly above benchmark |
| `pass` | ✅ Pursue | Good opportunity, steady or rising |
| `close` | ⚠️ Watch | Close to pass, verify manually |
| `watch` | ⏸️ Observe | Monitor for trend changes |
| `fail` | ❌ Skip | Declining, no opportunity |

### Freshness Guide

| Status | Action | Description |
|---|---|---|
| `new` | ✅ Pursue | Recently emerged (7d/30d/90d window) |
| `old_hot` | ✅ Pursue | Old word with recent surge |
| `stable_old` | ❌ Skip | Stable for years, not a new opportunity |
| `unclear` | ⚠️ Verify | Not enough data, manual check needed |

## Step-by-Step Analysis

### Step 1: Get Results

```bash
python3 gk_api.py research --report > results.md
```

This runs server-side pipeline:
- ✅ Keyword expansion (DataForSEO + Google Trends)
- ✅ AI-powered filtering (removes junk, keeps utility tools)
- ✅ Trend comparison vs benchmark (`gpts`)
- ✅ SERP competition analysis
- ✅ Final opportunity classification

### Step 2: Review Opportunities

From the report's "值得继续" table:

1. **Check user intent** - Does `intent.demand` match a tool/saaS need?
   - ✅ "Find an online tool to..." → Good
   - ❌ "What is...", "How to..." → Informational, skip

2. **Check trend strength** - Is `verdict` strong or pass?
   - ✅ `strong` or `pass` → Pursue
   - ⚠️ `close` → Verify manually
   - ❌ `watch` or `fail` → Skip

3. **Check freshness** - Is it new or old_hot?
   - ✅ `new` (7d/30d/90d) → Fresh opportunity
   - ✅ `old_hot` → Old word with recent surge
   - ❌ `stable_old` → Not a new opportunity

### Step 3: Manual SERP Verification (Optional but Recommended)

For each "值得继续" keyword, verify manually:

1. **Google search** - Open incognito window, search the keyword
2. **Check intent** - Are top 10 mostly tool pages or blog posts?
3. **Check competition** - Are there small niche sites or only big brands?
4. **Check features** - What are competitors doing? Can we differentiate?

**Red flags**:
- Top 10 are mostly blog posts / tutorials / Wikipedia → Informational intent, skip
- AI Overview present → Google already answering, skip
- Featured Snippet present → Hard to rank, skip
- Only big brands (Adobe, Canva, Grammarly) → Authority-heavy, skip

**Green flags**:
- Multiple niche tool sites (.ai, .app, .io) → Niche-friendly
- Mix of authority + niche → Mixed, can compete
- Few or no AI Overview / Featured Snippet → SERP not locked

### Step 4: Competitor Domain Age (Optional)

If manual SERP check passes, check competitor ages:

```bash
# Extract niche domains from Google results, then:
python3 scripts/domain_age.py tattoogen.ai blackink.ai coloringpage.ai
```

**Age guide**:
- < 2 years → ✅ Strong opportunity (new, beatable)
- 2-5 years → ⚠️ Moderate (established, but can compete)
- > 5 years → ❌ Deep moat (skip unless major differentiation)

### Step 5: Product Direction

From the report's "切入方向" column, pick a direction:

| Keyword Type | Suggested Product |
|---|---|
| `generator` | Template-based generation, batch export, customizable parameters |
| `editor` / `enhancer` | Upload-based editor, before/after comparison, no signup required |
| `checker` / `detector` | Quick validation, explain why, give fix suggestions |
| `converter` | Drag-and-drop, instant result, download options |

## Decision Boundaries

**Stop** when:
- Found 2-3 "strong" or "pass" opportunities → Move to project planning
- All remaining `stable_old` or `fail` → Change seed keywords
- Quota exceeded → Wait for next day or increase quota

**Pause** when:
- Have 1 strong + 3-5 close/watch → Pursue strong, observe rest
- No clear winners but several close → Expand seed keywords and retry

## Common Pitfalls

1. **Don't chase volume alone** — High volume + declining trend = bad opportunity
2. **Don't ignore SERP** — Good keyword + authority-heavy SERP = can't rank
3. **Don't assume age** — "Looks small" ≠ actually small (check domain age!)
4. **Don't trust only verdict** — Manual SERP verification is critical
5. **Don't skip intent check** — Informational queries don't convert to tool users

## Output Format

Always use this three-table format:

```
# 一句话总判断
[one sentence summary]

## 值得继续
| 关键词 | 趋势 | 新鲜度 | 用户意图 | 为什么 | 切入方向 |

## 可观察
| 关键词 | 趋势 | 新鲜度 | 为什么观察 | 跟踪什么 |

## 不值得做
| 关键词 | 为什么 |

## 下一步建议
1. ...
```

This matches the `--report` output format and is learner-friendly.
