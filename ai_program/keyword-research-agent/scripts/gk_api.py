#!/usr/bin/env python3
"""
Google Keywords Website API client.

Single entry point: submit expand job → poll status → get full results
(including AI filter, SERP competition, trends comparison).

All heavy lifting is server-side. This script submits the job,
polls until complete, then returns the final data.
"""
import os
import sys
import json
import time
import argparse
from pathlib import Path
import requests
from typing import List, Dict, Optional

# Website config
GK_SITE_URL = os.environ.get('GK_SITE_URL', 'https://www.discoverkeywords.co')
GK_API_KEY = os.environ.get('GK_API_KEY', '')
DEFAULT_BENCHMARK = os.environ.get('GK_BENCHMARK', 'gpts')
RECOMMENDED_COMPARE_LIMIT = int(os.environ.get('GK_RECOMMENDED_COMPARE_LIMIT', '50'))
RECOMMENDED_MIN_SCORE = int(os.environ.get('GK_RECOMMENDED_MIN_SCORE', '20'))
RECOMMENDED_HIGH_CONFIDENCE_SCORE = int(os.environ.get('GK_RECOMMENDED_HIGH_CONFIDENCE_SCORE', '60'))
RECOMMENDED_SECTION_QUOTAS = {
    'explosive': int(os.environ.get('GK_RECOMMENDED_EXPLOSIVE_QUOTA', '22')),
    'fastRising': int(os.environ.get('GK_RECOMMENDED_FAST_RISING_QUOTA', '16')),
    'steadyRising': int(os.environ.get('GK_RECOMMENDED_STEADY_RISING_QUOTA', '12')),
}
FALLBACK_DEFAULT_SEEDS = [
    "calculator", "generator", "converter", "maker", "creator",
    "editor", "builder", "designer", "simulator", "translator",
]
SHARED_DEFAULTS_PATH = Path(
    os.environ.get(
        'GK_SHARED_DEFAULTS_PATH',
        '/root/clawd/projects/google_keywords/config/shared-keyword-defaults.json'
    )
)

DEFAULT_SEEDS = FALLBACK_DEFAULT_SEEDS[:]

try:
    if SHARED_DEFAULTS_PATH.exists():
        shared_defaults = json.loads(SHARED_DEFAULTS_PATH.read_text())
        keywords = shared_defaults.get('defaultKeywords', [])
        if isinstance(keywords, list):
            parsed = [item.strip() for item in keywords if isinstance(item, str) and item.strip()]
            if parsed:
                DEFAULT_SEEDS = parsed
except Exception:
    DEFAULT_SEEDS = FALLBACK_DEFAULT_SEEDS[:]

raw_default_seeds = os.environ.get('GK_DEFAULT_SEEDS', '').strip()
if raw_default_seeds:
    DEFAULT_SEEDS = [item.strip() for item in raw_default_seeds.split(',') if item.strip()]

def _headers():
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {GK_API_KEY}',
        'Accept': 'application/json',
        'User-Agent': 'curl/8.5.0',
    }

def _api_call(method: str, path: str, body: dict = None, timeout: int = 30) -> Dict:
    url = f'{GK_SITE_URL}{path}'
    resp = requests.request(method, url, headers=_headers(), json=body, timeout=timeout)
    resp.raise_for_status()
    return resp.json()

# ── Expand (submit + poll) ──

def expand(keywords: List[str], use_cache: bool = True) -> Dict:
    """POST /api/research/expand. Returns a pending job envelope."""
    return _api_call('POST', '/api/research/expand', {
        'keywords': keywords,
        'useCache': use_cache,
    }, timeout=30)

def poll_expand_status(job_id: str, max_wait: int = 300) -> Dict:
    """Poll /api/research/expand/status until complete."""
    for i in range(max_wait // 10):
        data = _api_call('GET', f'/api/research/expand/status?jobId={job_id}', timeout=15)
        status = data.get('status', '')
        if status == 'complete':
            return data
        elif status == 'failed':
            raise Exception(f"Job failed: {data.get('error')}")
        if i % 3 == 0:
            print(f"  ⏳ Job {job_id}: {status}... ({i*10}s)", file=sys.stderr)
        time.sleep(10)
    raise Exception(f"Job {job_id} timed out after {max_wait}s")

def compare(keywords: List[str], date_from: str, date_to: str, benchmark: str = DEFAULT_BENCHMARK) -> Dict:
    """POST /api/research/compare. Ordinary API-key users should hit shared cache."""
    return _api_call('POST', '/api/research/compare', {
        'keywords': keywords,
        'dateFrom': date_from,
        'dateTo': date_to,
        'benchmark': benchmark,
        'minRuleScore': RECOMMENDED_MIN_SCORE,
    }, timeout=60)

def poll_compare_status(job_id: str, max_wait: int = 600) -> Dict:
    """Poll /api/research/compare/status until complete."""
    for i in range(max_wait // 10):
        data = _api_call('GET', f'/api/research/compare/status?jobId={job_id}', timeout=30)
        status = data.get('status', '')
        if status == 'complete':
            return data
        elif status == 'failed':
            raise Exception(f"Compare job failed: {data.get('error')}")
        if i % 3 == 0:
            ready = data.get('ready')
            total = data.get('total')
            print(f"  ⏳ Compare job {job_id}: {status} {ready}/{total}... ({i*10}s)", file=sys.stderr)
        time.sleep(10)
    raise Exception(f"Compare job {job_id} timed out after {max_wait}s")

def get_expanded_keywords(keywords: List[str], use_cache: bool = True) -> Dict:
    """
    Full flow: submit expand job → poll status → return complete results.
    Server-side pipeline: DataForSEO → rule engine → AI filter → SERP → trends.
    """
    if not GK_API_KEY:
        raise Exception("GK_API_KEY env var required.")

    print(f"📡 Calling expand API with {len(keywords)} seed keywords...", file=sys.stderr)
    result = expand(keywords, use_cache)

    job_id = result.get('jobId')
    if job_id:
        if result.get('fromCache'):
            print(f"  ♻️  Reusing cached job: {job_id}, polling...", file=sys.stderr)
        else:
            print(f"  📋 Job submitted: {job_id}, polling...", file=sys.stderr)
        data = poll_expand_status(job_id)
        flat = data.get('flatList', [])
        print(f"  ✅ Got {len(flat)} expanded keywords", file=sys.stderr)
        return data

    if result.get('status') == 'complete':
        flat = result.get('flatList', [])
        print(f"  ✅ Got {len(flat)} expanded keywords", file=sys.stderr)
        return result

    return result

# ── Helpers ──

def extract_keyword_names(results: List[Dict]) -> List[str]:
    return [item.get('keyword', '') for item in results if item.get('keyword')]

def _freshness_label(item: Dict) -> str:
    freshness = item.get('freshness') or {}
    label = freshness.get('label') or freshness.get('status') or '-'
    window = freshness.get('window')
    return f"{label}({window})" if window and window != 'none' else label

def _intent_summary(item: Dict) -> str:
    intent = item.get('intent') or {}
    demand = intent.get('demand') or ''
    label = intent.get('label') or ''
    if demand and label:
        return f"{label}: {demand}"
    return demand or label or '-'

def _why_item(item: Dict) -> str:
    freshness = item.get('freshness') or {}
    parts = []
    if freshness.get('reason'):
        parts.append(str(freshness['reason']))
    if item.get('ratio') is not None:
        parts.append(f"趋势强度 {item.get('ratio')}x")
    if item.get('verdict'):
        parts.append(f"判定 {item.get('verdict')}")
    return '；'.join(parts) or '-'

def _entry_direction(item: Dict) -> str:
    keyword = (item.get('keyword') or '').lower()
    intent = item.get('intent') or {}
    demand = intent.get('demand') or ''
    if any(token in keyword for token in ['generator', 'creator', 'maker']):
        return '做轻量生成器，突出模板、批量生成、可下载结果。'
    if any(token in keyword for token in ['editor', 'enhancer', 'upscaler', 'remover']):
        return '做在线编辑/增强工具，突出上传即用、前后对比、无需注册。'
    if any(token in keyword for token in ['checker', 'detector', 'verifier']):
        return '做检测/校验工具，突出快速判断、解释原因、给修复建议。'
    if any(token in keyword for token in ['calculator', 'planner', 'tracker']):
        return '做交互式计算/规划工具，突出表单输入、结果解释、可保存分享。'
    if demand:
        return f"围绕用户需求切入：{demand}"
    return '先做单页工具 MVP，验证搜索意图和转化。'

def render_report(result: Dict, max_items: int = 10) -> str:
    opportunities = result.get('opportunities') or []
    stable_old = result.get('stableOld') or []
    compare_results = (result.get('compare') or {}).get('results') or []
    watch_items = [
        item for item in compare_results
        if item not in opportunities
        and item.get('verdict') in ('close', 'watch')
        and (item.get('freshness') or {}).get('status') != 'stable_old'
    ]
    rejected = [
        item for item in compare_results
        if item.get('verdict') == 'fail'
        or (item.get('freshness') or {}).get('status') == 'stable_old'
    ]

    verdict = (
        f"本轮发现 {len(opportunities)} 个近期可做机会词。"
        if opportunities
        else "本轮没有发现足够明确的近期可做新词，建议等待下一轮缓存或扩大词根。"
    )
    lines = [
        "# 一句话总判断",
        verdict,
        "",
        "## 值得继续",
        "| 关键词 | 趋势 | 新鲜度 | 用户意图 | 为什么 | 切入方向 |",
        "|---|---:|---|---|---|---|",
    ]

    if opportunities:
        for item in opportunities[:max_items]:
            lines.append(
                "| {keyword} | {ratio}x / {verdict} | {freshness} | {intent} | {why} | {direction} |".format(
                    keyword=item.get('keyword', '-'),
                    ratio=item.get('ratio', '-'),
                    verdict=item.get('verdict', '-'),
                    freshness=_freshness_label(item),
                    intent=_intent_summary(item).replace('|', '/'),
                    why=_why_item(item).replace('|', '/'),
                    direction=_entry_direction(item).replace('|', '/'),
                )
            )
    else:
        lines.append("| - | - | - | - | 暂无 | - |")

    lines.extend([
        "",
        "## 可观察",
        "| 关键词 | 趋势 | 新鲜度 | 为什么观察 | 跟踪什么 |",
        "|---|---:|---|---|---|",
    ])
    observable = watch_items[:max_items]
    if observable:
        for item in observable:
            lines.append(
                "| {keyword} | {ratio}x / {verdict} | {freshness} | {why} | 观察下一轮是否进入 new/old_hot，且 verdict 是否提升。 |".format(
                    keyword=item.get('keyword', '-'),
                    ratio=item.get('ratio', '-'),
                    verdict=item.get('verdict', '-'),
                    freshness=_freshness_label(item),
                    why=_why_item(item).replace('|', '/'),
                )
            )
    else:
        lines.append("| - | - | - | 暂无 | - |")

    lines.extend([
        "",
        "## 不值得做",
        "| 关键词 | 为什么 |",
        "|---|---|",
    ])
    if rejected:
        for item in rejected[:max_items]:
            reason = '稳定老词，不作为近期新词机会。' if (item.get('freshness') or {}).get('status') == 'stable_old' else '趋势判定 fail。'
            lines.append(f"| {item.get('keyword', '-')} | {reason} |")
    else:
        lines.append("| - | 暂无 |")

    lines.extend([
        "",
        "## 下一步建议",
        "1. 优先人工复核“值得继续”里的关键词搜索意图和落地页形态。",
        "2. 不要把 stable_old 当作新词机会，除非有明确差异化产品方案。",
        "3. 下一轮每日缓存更新后，重点观察 old_hot/new 是否持续出现。",
    ])
    return '\n'.join(lines)

def sanitize_for_learner(value):
    """Remove platform/internal transport details from learner-facing output."""
    hidden_keys = {
        'fromCache',
        'cacheFallback',
        'jobId',
        'strategy',
        'sessionId',
        'comparisonId',
        'intentRefreshed',
    }
    if isinstance(value, dict):
        return {
            key: sanitize_for_learner(item)
            for key, item in value.items()
            if key not in hidden_keys
        }
    if isinstance(value, list):
        return [sanitize_for_learner(item) for item in value]
    return value

def _candidate_score(item: Dict) -> float:
    try:
        return float(item.get('score') or 0)
    except (TypeError, ValueError):
        return 0

def build_recommended_selection(expand_data: Dict, limit: int = RECOMMENDED_COMPARE_LIMIT) -> List[str]:
    """Mirror the web app recommended compare selection."""
    organized = expand_data.get('organized') or {}
    flat_list = expand_data.get('flatList') or expand_data.get('candidates') or []
    picked: List[str] = []
    picked_set = set()

    def add_keyword(item: Dict) -> bool:
        keyword = item.get('keyword') if isinstance(item, dict) else None
        if not keyword or keyword in picked_set:
            return False
        if _candidate_score(item) < RECOMMENDED_MIN_SCORE:
            return False
        picked.append(keyword)
        picked_set.add(keyword)
        return True

    def add_candidates(items: List[Dict], max_count: int) -> None:
        added = 0
        for item in items or []:
            if len(picked) >= limit or added >= max_count:
                break
            if add_keyword(item):
                added += 1

    strong = [
        item for item in flat_list
        if isinstance(item, dict) and _candidate_score(item) >= RECOMMENDED_HIGH_CONFIDENCE_SCORE
    ]
    for item in strong:
        if len(picked) >= limit:
            break
        add_keyword(item)

    add_candidates(organized.get('explosive') or [], RECOMMENDED_SECTION_QUOTAS['explosive'])
    add_candidates(organized.get('fastRising') or [], RECOMMENDED_SECTION_QUOTAS['fastRising'])
    add_candidates(organized.get('steadyRising') or [], RECOMMENDED_SECTION_QUOTAS['steadyRising'])

    if len(picked) < limit:
        slow_ids = {
            id(item) for item in organized.get('slowRising') or []
            if isinstance(item, dict)
        }
        non_slow = [item for item in flat_list if id(item) not in slow_ids]
        add_candidates(non_slow, limit)

    return picked[:limit]

def get_complete_keyword_research(
    keywords: List[str],
    use_cache: bool = True,
    benchmark: str = DEFAULT_BENCHMARK,
) -> Dict:
    """Expand from shared cache, then compare against benchmark from shared cache."""
    expand_data = get_expanded_keywords(keywords, use_cache=use_cache)
    selected = build_recommended_selection(expand_data)
    if not selected:
        return {
            'status': 'complete',
            'expand': expand_data,
            'compare': None,
            'selectedKeywords': [],
            'opportunities': [],
        }

    print(f"📊 Calling compare API with {len(selected)} recommended keywords...", file=sys.stderr)
    compare_data = compare(
        selected,
        expand_data.get('dateFrom', ''),
        expand_data.get('dateTo', ''),
        benchmark=benchmark,
    )
    job_id = compare_data.get('jobId')
    if job_id:
        print(f"  📋 Compare job: {job_id}, polling...", file=sys.stderr)
        compare_data = poll_compare_status(job_id)

    results = compare_data.get('results') or []
    opportunities = [
        item for item in results
        if item.get('verdict') in ('strong', 'pass', 'close', 'watch')
        and (item.get('freshness') or {}).get('status') in ('new', 'old_hot')
    ]
    stable_old = [
        item for item in results
        if (item.get('freshness') or {}).get('status') == 'stable_old'
    ]

    print(
        f"  ✅ Compare results={len(results)} opportunities={len(opportunities)} stable_old={len(stable_old)}",
        file=sys.stderr,
    )
    return {
        'status': 'complete',
        'benchmark': benchmark,
        'dateFrom': expand_data.get('dateFrom'),
        'dateTo': expand_data.get('dateTo'),
        'selectedKeywords': selected,
        'opportunities': opportunities,
        'stableOld': stable_old,
        'expand': expand_data,
        'compare': compare_data,
    }

def main():
    parser = argparse.ArgumentParser(description='Google Keywords Website API client')
    sub = parser.add_subparsers(dest='command', required=True)

    # research (recommended): expand cache + compare cache, returns opportunity keywords
    p_research = sub.add_parser('research', help='Complete keyword research from shared cache')
    p_research.add_argument('seeds', nargs='*', help='Seed keywords (optional; defaults to shared seeds)')
    p_research.add_argument('--no-cache', action='store_true')
    p_research.add_argument('--benchmark', default=DEFAULT_BENCHMARK)
    p_research.add_argument('--names-only', action='store_true')
    p_research.add_argument('--report', action='store_true', help='Output a learner-friendly Markdown report')
    p_research.add_argument('--raw', action='store_true', help='Output raw API-shaped data including internal fields')

    # expand (candidate discovery only)
    p_expand = sub.add_parser('expand', help='Expand seed keywords (candidate discovery only)')
    p_expand.add_argument('seeds', nargs='*', help='Seed keywords (optional; defaults to built-in seeds)')
    p_expand.add_argument('--no-cache', action='store_true')
    p_expand.add_argument('--names-only', action='store_true')

    # serp (kept for backward compat, but now part of expand pipeline)
    p_serp = sub.add_parser('serp', help='[DEPRECATED] Use expand instead')
    p_serp.add_argument('keywords', nargs='+')

    # trends (kept for backward compat, but now part of expand pipeline)
    p_trends = sub.add_parser('trends', help='[DEPRECATED] Use expand instead')
    p_trends.add_argument('keywords', nargs='+')

    # full (kept for backward compat, same as expand now)
    p_full = sub.add_parser('full', help='Expand + SERP + Trends (same as expand)')
    p_full.add_argument('seeds', nargs='*')

    args = parser.parse_args()

    if args.command == 'research':
        seeds = args.seeds or DEFAULT_SEEDS
        if not args.seeds:
            print(f"ℹ️  No seeds provided. Using {len(seeds)} default seeds.", file=sys.stderr)
        results = get_complete_keyword_research(
            seeds,
            use_cache=not getattr(args, 'no_cache', False),
            benchmark=getattr(args, 'benchmark', DEFAULT_BENCHMARK),
        )
        if getattr(args, 'names_only', False):
            for kw in extract_keyword_names(results.get('opportunities', [])):
                print(kw)
        elif getattr(args, 'report', False):
            print(render_report(results))
        else:
            output = results if getattr(args, 'raw', False) else sanitize_for_learner(results)
            print(json.dumps(output, indent=2, ensure_ascii=False))

    elif args.command in ('expand', 'full'):
        seeds = args.seeds or DEFAULT_SEEDS
        if not args.seeds:
            print(f"ℹ️  No seeds provided. Using {len(seeds)} default seeds.", file=sys.stderr)
        results = get_expanded_keywords(seeds, use_cache=not getattr(args, 'no_cache', False))
        if args.command == 'expand' and getattr(args, 'names_only', False):
            for kw in extract_keyword_names(results.get('flatList', [])):
                print(kw)
        else:
            print(json.dumps(results, indent=2, ensure_ascii=False))

    elif args.command == 'serp':
        print("⚠️  SERP is now part of the expand pipeline. Use: expand <keywords>", file=sys.stderr)
        print("SERP competition data is included in each candidate's result.", file=sys.stderr)
        sys.exit(1)

    elif args.command == 'trends':
        print("⚠️  Trends comparison is now part of the expand pipeline. Use: expand <keywords>", file=sys.stderr)
        print("Trend data (ratio, verdict, etc.) is included in each candidate's 'trends' field.", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
