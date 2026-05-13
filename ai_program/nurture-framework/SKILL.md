---
name: nurture-framework
description: Social media account nurturing system for X/Twitter, Reddit, HN, Product Hunt. CDP-based automation with AI-generated comments, YAML-driven scheduling, and structured observation tracking.
---

# Social Media Nurture Framework

## Trigger
Use when the user asks to:
- Deploy/run/migrate the social media nurture framework
- Set up account nurturing for X/Twitter, Reddit, HN, or Product Hunt
- Execute `run.py`, check nurture status/logs, or fix platform-specific failures
- Configure cron jobs for automated daily nurturing sessions

## Quick Start

### 1. Activate the framework (copy code to working directory)

The framework code is bundled inside this skill. To activate:

```bash
# Copy framework from skill to working directory
mkdir -p ~/nurture
cp -r ~/.hermes/skills/social-media/nurture-framework/scripts/nurture/* ~/nurture/
cd ~/nurture
```

### 2. Install dependencies

```bash
pip3 install playwright pyyaml openai
playwright install chromium
```

### 3. Configure

Edit `.env` for AI comment generation:
```bash
OPENAI_API_KEY=AIzaSy...
OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
LLM_MODEL=gemini-3.1-pro-preview
```

Edit `config/account_profiles.yaml` for usernames:
```yaml
accounts:
  x_twitter: {username: "nicktaobo"}
  reddit:    {username: "Antique_Prune_4869"}
  hackernews:{username: "nicktaobo"}
  product_hunt:{username: "timyao1987"}
```

### 4. Start Chrome with CDP and log into all platforms

```bash
# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 > /dev/null 2>&1 &
```

Then manually log into: **Twitter/X, Reddit, HN, Product Hunt** in Chrome.

### 5. Run

```bash
# Dry run
python3 run.py --dry-run

# Single platform test
python3 run.py --platform reddit --duration 2

# Scheduled execution (reads config/schedule.yaml)
python3 run.py
```

## Architecture

```
nurture/
├── config/
│   ├── platforms.yaml          # Weights, durations, action limits per platform
│   ├── schedule.yaml           # Time windows, probabilities
│   └── account_profiles.yaml   # Usernames only (login via Chrome cookies)
├── core/
│   ├── base.py                 # PlatformNurturer abstract base
│   ├── cdp_manager.py          # Playwright CDP wrapper
│   ├── executor.py             # Task execution, logging
│   ├── scheduler.py            # TimeWindow + task generation
│   ├── notifier.py             # Notification wrapper
│   ├── randomizer.py           # Human-like delays
│   └── text_generator.py       # AI comment generation (OpenAI-compatible API)
├── platforms/
│   ├── x_twitter.py            # Retweet, like, reply, follow, bookmark
│   ├── reddit.py               # Upvote, comment, save (shadow DOM aware)
│   ├── hackernews.py           # Upvote, comment (new-account limits)
│   └── product_hunt.py         # Browse, comment, upvote
├── run.py                      # Unified entry point
└── .env                        # API keys (optional, fallback templates work without)
```

## Core Concepts

### CDP-Based (Real Browser)
- Connects to Chrome DevTools Protocol on port 9222
- Reuses real Chrome session (cookies, login state, Cloudflare bypass)
- **You must manually log into each platform in Chrome first**

### Config-Driven
- `config/platforms.yaml`: Enable/disable platforms, set weights, action probabilities, durations
- `config/schedule.yaml`: Define time windows (morning/noon/evening), execution probability
- Changing behavior = edit YAML, no code changes needed

### AI Comment Generation
- Uses OpenAI-compatible API (Gemini, OpenAI, etc.) to generate platform-specific comments
- Fallback templates when API unavailable
- Platform-tuned prompts: HN (thoughtful), Reddit (casual slang), X (short/sarcastic), PH (product-specific)

### Registry Pattern
- Platforms self-register via `register_platform("name", Class)` at import time
- Adding new platform = write one file in `platforms/` + add config entry

## Commands

| Command | Purpose |
|---------|---------|
| `python3 run.py` | Scheduled execution (checks time window) |
| `python3 run.py --dry-run` | Show what would run without executing |
| `python3 run.py --platform reddit --duration 10` | Run single platform, bypass schedule |
| `python3 test_framework.py` | Run 35-unit test suite |

## Critical Implementation Details

### Reddit: Shadow DOM Everywhere
- Upvote buttons inside `shreddit-post` → `shadowRoot` → SVG arrows
- Save button inside `shreddit-post-overflow-menu` → `shadowRoot` → `#post-overflow-save`
- Comment box: click `faceplate-textarea-input` trigger first, then find `[contenteditable]`
- **Never rely on a single selector** — always implement multi-strategy fallback

### X/Twitter: React State
- `element.fill()` does NOT work — use `page.keyboard.type()` after `click(force=True)`
- Follow buttons need 4-strategy fallback (aria-label → data-testid → sidebar scope → global text)
- UI may be localized (Chinese: "关注" instead of "Follow")

### Hacker News: New-Account Limits
- Karma ≤1 + age <48h → max **1 comment per 24h**
- Plain text only — no Markdown, no numbered lists, no structured sections
- Long comments (>200 words) from new accounts flagged as AI

### Product Hunt: Dynamic Hydration
- Product cards hydrate via React/Vue — DOM extraction often returns 0 results
- Use screenshot + vision as fallback to identify products
- URL slugs may NOT match visual text — always extract `href` from live DOM
- Filter out "THE PITCH" / "Promoted" products

### CDPManager.check_port() Bug (Fixed)
```python
# WRONG
return "Browser" in data.get("Browser", "")
# CORRECT
return bool(data.get("Browser", ""))
```

### login_check() Must Navigate First
When running multiple platforms sequentially, the browser stays on the previous platform's page. Always:
```python
def login_check(self) -> bool:
    self.cdp.navigate("https://platform.com/")
    self.human_pause(2, 4)
    # THEN check login indicators
```

### Account Parameter in Platform Constructor
```python
# WRONG — login_check() reads from self.account, not self.config
RedditNurturer(config={"username": "..."}, cdp_manager=cdp)

# CORRECT
RedditNurturer(
    config={"search_fallback_topics": [...]},
    cdp_manager=cdp,
    account={"username": "Antique_Prune_4869"},
)
```

## Cron / Background Execution

```bash
# Morning 8:30
30 8 * * * cd ~/nurture && PYTHONUNBUFFERED=1 python3 run.py >> logs/cron.log 2>&1

# Noon 12:30
30 12 * * * cd ~/nurture && PYTHONUNBUFFERED=1 python3 run.py >> logs/cron.log 2>&1

# Evening 20:00
0 20 * * * cd ~/nurture && PYTHONUNBUFFERED=1 python3 run.py >> logs/cron.log 2>&1
```

**Mandatory**: `PYTHONUNBUFFERED=1` or output is silently buffered in background.

**Timeout**: Max session duration is 20m (reddit), so cron timeout must exceed this.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Chrome CDP not available` | Chrome not running with CDP port 9222 | Start Chrome with `--remote-debugging-port=9222` |
| `Login check failed` | Not logged in / session expired | Manually log into platform in Chrome |
| `No upvote button found` | Shadow DOM / not visible | Multi-strategy detection with scrollIntoView |
| Comments truncated | Gemini max_tokens < 200 | Set max_tokens ≥ 200 in text_generator.py |
| Empty logs mid-run | Normal — logs written at completion | Poll process stdout instead |

## Platform-Specific Account Status (As of 2026-05-13)

| Platform | Username | Status |
|----------|----------|--------|
| X/Twitter | nicktaobo | Active |
| Reddit | Antique_Prune_4869 | Active |
| HN | nicktaobo | karma=0, age<48h → comment limited to 1/day |
| Product Hunt | timyao1987 | Active |