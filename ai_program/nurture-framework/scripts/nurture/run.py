#!/usr/bin/env python3
"""
Nurture - Social Media Account Nurturing System

Usage:
    python run.py [--dry-run] [--platform PLATFORM]

Examples:
    python run.py              # Normal execution based on schedule
    python run.py --dry-run    # Test without executing actions
    python run.py --platform hackernews  # Run specific platform only
"""

import argparse
import os
import sys
import yaml
from datetime import datetime

# Ensure core/platform modules are importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.cdp_manager import CDPManager
from core.scheduler import Scheduler
from core.executor import Executor
from core.notifier import Notifier
from core.randomizer import Randomizer

# Import platforms to trigger registration
import platforms


def load_config(path: str) -> dict:
    """Load a YAML config file."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="Social media account nurturing")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be done without executing")
    parser.add_argument("--platform", type=str, help="Run a specific platform (bypass schedule)")
    parser.add_argument("--duration", type=int, default=10, help="Session duration in minutes (for --platform)")
    parser.add_argument("--cdp-url", type=str, default="http://localhost:9222", help="CDP endpoint")
    args = parser.parse_args()

    # ------------------------------------------------------------------
    #  Load configs
    # ------------------------------------------------------------------
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(base_dir, "config")

    try:
        platforms_cfg = load_config(os.path.join(config_dir, "platforms.yaml"))
        schedule_cfg = load_config(os.path.join(config_dir, "schedule.yaml"))
        accounts_cfg = load_config(os.path.join(config_dir, "account_profiles.yaml"))
    except FileNotFoundError as e:
        print(f"[Error] Config file not found: {e}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"[Error] Invalid YAML in config: {e}")
        sys.exit(1)

    # Merge account usernames into platform configs
    for platform, account in accounts_cfg.get("accounts", {}).items():
        if platform in platforms_cfg.get("platforms", {}):
            platforms_cfg["platforms"][platform]["username"] = account.get("username", "")

    # ------------------------------------------------------------------
    #  Initialize components
    # ------------------------------------------------------------------
    scheduler = Scheduler(schedule_cfg, platforms_cfg)
    notifier = Notifier()

    # ------------------------------------------------------------------
    #  Mode: specific platform (bypass schedule)
    # ------------------------------------------------------------------
    if args.platform:
        if args.platform not in platforms_cfg.get("platforms", {}):
            print(f"[Error] Unknown platform: {args.platform}")
            print(f"Available: {list(platforms_cfg['platforms'].keys())}")
            sys.exit(1)

        print(f"[Run] Platform mode: {args.platform} ({args.duration}min)")

        if args.dry_run:
            print("[Dry Run] Would connect to CDP and execute session")
            sys.exit(0)

        cdp = CDPManager(cdp_url=args.cdp_url)
        if not cdp.connect():
            print("[Error] Failed to connect to Chrome CDP. Is Chrome running with --remote-debugging-port=9222?")
            sys.exit(1)

        try:
            accounts = accounts_cfg.get("accounts", {})
            executor = Executor(cdp, platforms_cfg, notifier=notifier, accounts=accounts)
            results = executor.run_platform(args.platform, args.duration)

            success = sum(1 for r in results if r.success)
            print(f"\n[Done] {success}/{len(results)} actions succeeded")
        finally:
            cdp.disconnect()

        sys.exit(0)

    # ------------------------------------------------------------------
    #  Mode: scheduled execution
    # ------------------------------------------------------------------
    should_run, window = scheduler.should_run_now()

    if not should_run:
        if window:
            print(f"[Skip] Window '{window.name}' did not hit probability threshold or is outside hours")
        else:
            print("[Skip] Current time is not within any scheduled window")
        sys.exit(0)

    # Generate tasks
    tasks = scheduler.generate_tasks(window)
    if not tasks:
        print("[Skip] No tasks generated for this window")
        sys.exit(0)

    print(f"\n{'='*60}")
    print(f"[Run] Window: {window.name} ({window.start.strftime('%H:%M')}-{window.end.strftime('%H:%M')})")
    print(f"[Run] Tasks: {len(tasks)} platform(s)")
    for t in tasks:
        print(f"       - {t['platform']}: {t['duration_minutes']}min")
    print(f"{'='*60}\n")

    if args.dry_run:
        print("[Dry Run] Would execute the above tasks")
        sys.exit(0)

    # Check CDP before starting
    if not CDPManager.check_port():
        print("[Error] Chrome CDP not available on port 9222")
        print("[Hint] Start Chrome with: --remote-debugging-port=9222")
        notifier.send("Nurture failed: Chrome CDP not available")
        sys.exit(1)

    # Execute
    cdp = CDPManager(cdp_url=args.cdp_url)
    if not cdp.connect():
        print("[Error] Failed to connect to Chrome CDP")
        notifier.send("Nurture failed: CDP connection error")
        sys.exit(1)

    all_results = {}
    try:
        accounts = accounts_cfg.get("accounts", {})
        executor = Executor(cdp, platforms_cfg, notifier=notifier, accounts=accounts)
        all_results = executor.run_tasks(tasks)
    except Exception as e:
        print(f"[Error] Execution failed: {e}")
        notifier.send(f"Nurture error: {e}")
    finally:
        cdp.disconnect()

    # Summary
    total_actions = 0
    total_success = 0
    platforms_ran = []
    errors = []

    for platform, results in all_results.items():
        platforms_ran.append(platform)
        for r in results:
            total_actions += 1
            if r.success:
                total_success += 1
            else:
                errors.append(f"{platform}/{r.action}: {r.detail}")

    print(f"\n{'='*60}")
    print(f"[Summary] Platforms: {', '.join(platforms_ran)}")
    print(f"[Summary] Actions: {total_success}/{total_actions} succeeded")
    if errors:
        print(f"[Summary] Errors: {len(errors)}")
        for e in errors[:5]:
            print(f"          - {e}")
    print(f"{'='*60}")

    notifier.send_digest(
        observations_count=sum(len(r) for r in all_results.values()),
        platforms_ran=platforms_ran,
        errors=errors,
    )


if __name__ == "__main__":
    main()
