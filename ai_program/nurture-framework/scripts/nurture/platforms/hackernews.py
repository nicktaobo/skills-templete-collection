"""
Hacker News (HN) nurturing implementation.

Actions: browse_frontpage, upvote, comment
Style: Thoughtful, slightly informal, no markdown, no numbered lists
Pitfalls: New accounts heavily rate-limited (1 comment/day for first week)
          Comments easily flagged as AI if too polished or too long
"""

import json
import random
import time
from typing import List, Optional

from core.base import PlatformNurturer, ActionResult
from core.executor import register_platform


class HackerNewsNurturer(PlatformNurturer):
    """Nurturing logic for Hacker News."""

    @property
    def platform_name(self) -> str:
        return "hackernews"

    def login_check(self) -> bool:
        """Check if logged into HN."""
        try:
            self.cdp.navigate("https://news.ycombinator.com/")
            self.human_pause(2, 4)
            result = self.cdp.evaluate("""
                document.querySelector('a[href*="logout"]') !== null
            """)
            return bool(result)
        except Exception as e:
            print(f"[{self.platform_name}] Login check error: {e}")
            return False

    def preflight_check(self) -> bool:
        """
        HN-specific pre-flight: check karma, account age, and recent comment history.
        New accounts (karma <= 1, age < 48h) are limited to ~1 comment/day.
        """
        print(f"[{self.platform_name}] Running pre-flight check...")

        username = self.config.get("username")
        if not username:
            print(f"[{self.platform_name}] No username configured, skipping pre-flight")
            return True

        try:
            # Check profile for karma and age
            self.cdp.navigate(f"https://news.ycombinator.com/user?id={username}")
            self.human_pause(2, 4)

            info = self.cdp.evaluate("""
                (function() {
                    var rows = document.querySelectorAll('table tr');
                    var info = {};
                    rows.forEach(function(tr) {
                        var tds = tr.querySelectorAll('td');
                        if (tds.length >= 2) {
                            info[tds[0].innerText.trim()] = tds[1].innerText.trim();
                        }
                    });
                    return info;
                })()
            """)

            karma_str = str(info.get("karma", "0")).replace(",", "")
            karma = int(karma_str) if karma_str.isdigit() else 0
            created = info.get("created", "")

            # Store for later use by _is_new_account
            self._karma = karma
            self._account_created = created

            print(f"[{self.platform_name}] Karma: {karma}, Created: {created}")

            # Check if commented recently
            self.cdp.navigate(f"https://news.ycombinator.com/threads?id={username}")
            self.human_pause(2, 4)

            has_recent = self.cdp.evaluate("""
                (function() {
                    var times = document.querySelectorAll('.age');
                    if (times.length === 0) return false;
                    var latest = times[0].innerText;
                    return latest.includes('minute') || latest.includes('hour');
                })()
            """)

            # New account restrictions
            special_rules = self.config.get("special_rules", [])
            new_account_rule = None
            for rule in special_rules:
                if isinstance(rule, dict) and "new_account_limit" in rule:
                    new_account_rule = rule["new_account_limit"]
                    break

            # Store threshold for _is_new_account
            self._new_account_threshold = new_account_rule.get("karma_threshold", 1) if new_account_rule else 1

            if new_account_rule and karma <= new_account_rule.get("karma_threshold", 1):
                if "day" in created or "hour" in created:
                    if has_recent:
                        msg = f"HN new account limit: karma={karma}, commented recently. Skipping."
                        print(f"[{self.platform_name}] {msg}")
                        self.record_observation(msg, tags=["hn", "limit", "new-account"])
                        return False
                    else:
                        print(f"[{self.platform_name}] New account, but no recent comments. Proceeding with caution.")

            return True

        except Exception as e:
            print(f"[{self.platform_name}] Pre-flight error: {e}")
            return True  # Fail open - let session proceed

    def _is_new_account(self) -> bool:
        """
        Determine if this is a new/restricted account.
        New accounts (low karma, recently created) have stricter limits.
        """
        karma = getattr(self, "_karma", None)
        created = getattr(self, "_account_created", "")
        threshold = getattr(self, "_new_account_threshold", 1)

        if karma is None:
            # Preflight didn't run or failed; assume new to be safe
            return True

        # Check karma threshold
        if karma > threshold:
            return False

        # Check account age (recently created)
        if created and ("day" in created or "hour" in created):
            return True

        # Low karma but older account - still somewhat restricted
        return karma <= 5

    def browse(self, duration_minutes: int) -> ActionResult:
        """Browse HN frontpage, observing trending topics."""
        print(f"[{self.platform_name}] Browsing frontpage for {duration_minutes}min...")

        self.cdp.navigate("https://news.ycombinator.com/")
        self.human_pause(2, 4)

        # Extract posts for observations
        try:
            posts = self.cdp.evaluate("""
                Array.from(document.querySelectorAll('.athing')).slice(0, 15).map(row => {
                    var title = row.querySelector('.titleline > a');
                    var subtext = row.nextElementSibling;
                    var score = subtext ? subtext.querySelector('.score') : null;
                    var comments = subtext ? subtext.querySelector('a[href^="item?id="]') : null;
                    return title ? {
                        title: title.innerText,
                        url: title.href,
                        id: row.id,
                        score: score ? score.innerText : '0',
                        comments_link: comments ? comments.href : null,
                        comments_count: comments ? comments.innerText : '0'
                    } : null;
                }).filter(Boolean)
            """)

            for p in posts[:5]:
                self.record_observation(
                    f"HN frontpage: {p['title']} ({p['score']})",
                    tags=["hn", "frontpage", "trending"],
                    source_url=f"https://news.ycombinator.com/item?id={p['id']}",
                )

            # Cache posts for actions
            self._posts_cache = posts

        except Exception as e:
            print(f"[{self.platform_name}] Failed to extract posts: {e}")
            self._posts_cache = []

        # Simulate browsing
        start = time.time()
        while time.time() - start < duration_minutes * 60:
            self.cdp.scroll_by(int(200 + 500 * (time.time() - start) / (duration_minutes * 60)))
            self.human_pause(4, 10)

        return ActionResult(
            "browse",
            True,
            f"Browsed HN frontpage for {duration_minutes}min, scanned {len(self._posts_cache)} posts",
        )

    def execute_action(self, action_name: str) -> ActionResult:
        """Execute a specific interaction on HN."""
        print(f"[{self.platform_name}] Executing: {action_name}")

        if action_name == "upvote":
            return self._action_upvote()
        elif action_name == "comment":
            return self._action_comment()
        else:
            return ActionResult(action_name, False, f"Unknown action: {action_name}")

    # ------------------------------------------------------------------
    #  Upvote
    # ------------------------------------------------------------------

    def _action_upvote(self) -> ActionResult:
        """Upvote a post on HN."""
        if not getattr(self, "_posts_cache", None):
            return ActionResult("upvote", False, "No posts cached from browse")

        # Pick a post that we haven't upvoted yet
        target = random.choice(self._posts_cache[:8])
        post_id = target["id"]

        try:
            self.cdp.navigate(f"https://news.ycombinator.com/item?id={post_id}")
            self.human_pause(2, 3)

            # Click the upvote arrow
            result = self.cdp.evaluate("""
                (function() {
                    var arrow = document.querySelector('.votearrow[title="upvote"]');
                    if (arrow) {
                        arrow.click();
                        return 'UPVOTED';
                    }
                    // Fallback: any votearrow
                    arrow = document.querySelector('.votearrow');
                    if (arrow) {
                        arrow.click();
                        return 'UPVOTED_FALLBACK';
                    }
                    return 'NO_ARROW';
                })()
            """)

            if result in ("UPVOTED", "UPVOTED_FALLBACK"):
                self.actions_done["upvote"] += 1
                self.record_observation(
                    f"Upvoted HN post: {target['title'][:60]}",
                    tags=["hn", "upvote"],
                    source_url=f"https://news.ycombinator.com/item?id={post_id}",
                )
                return ActionResult("upvote", True, f"Upvoted post {post_id}")
            else:
                return ActionResult("upvote", False, "No upvote arrow found")

        except Exception as e:
            return ActionResult("upvote", False, f"Error: {e}")

    # ------------------------------------------------------------------
    #  Comment
    # ------------------------------------------------------------------

    def _action_comment(self) -> ActionResult:
        """
        Comment on an HN post.
        Strategy for maximizing karma:
        - Pick posts with high score (100+) and active discussion
        - Read existing comments thoroughly to avoid repetition
        - Reference specific article details, express real opinion
        - New accounts: 80-150 words max, 1 comment per session
        """
        username = self.config.get("username")
        if not getattr(self, "_posts_cache", None):
            return ActionResult("comment", False, "No posts cached from browse")

        # Sort candidates by engagement: prefer high-score posts with active discussion
        def _score_post(p):
            try:
                score_str = p.get("score", "0").replace(" points", "").replace(" point", "")
                score = int(score_str) if score_str.isdigit() else 0
            except (ValueError, AttributeError):
                score = 0
            try:
                comments_str = p.get("comments_count", "0").replace(" comments", "").replace(" comment", "").replace("discuss", "0")
                comments = int(comments_str) if comments_str.isdigit() else 0
            except (ValueError, AttributeError):
                comments = 0
            # Weight: score * 2 + comments, favor posts with both high score and discussion
            return score * 2 + comments

        # Filter out posts with no discussion link
        candidates = [p for p in self._posts_cache
                      if p.get("comments_link") and "discuss" not in p.get("comments_count", "").lower()]
        if not candidates:
            candidates = self._posts_cache[:5]

        # Sort by engagement score, pick from top 5 (not purely random)
        candidates.sort(key=_score_post, reverse=True)
        target = random.choice(candidates[:5]) if len(candidates) >= 5 else candidates[0]
        post_id = target["id"]

        try:
            # Navigate to post
            self.cdp.navigate(f"https://news.ycombinator.com/item?id={post_id}")
            self.human_pause(2, 3)

            # Check if already commented
            if username:
                already_commented = self.cdp.evaluate(f"""
                    (function() {{
                        var found = false;
                        document.querySelectorAll('.hnuser').forEach(function(el) {{
                            if (el.innerText === '{username}') found = true;
                        }});
                        return found;
                    }})()
                """)
                if already_commented:
                    return ActionResult("comment", False, "Already commented on this post")

            # Read existing top comments with their authors for context
            top_comments_raw = self.cdp.evaluate("""
                Array.from(document.querySelectorAll('.comment')).slice(0, 8).map(c => {
                    var userEl = c.closest('.comtr')?.querySelector('.hnuser');
                    var user = userEl ? userEl.innerText : 'unknown';
                    return user + ': ' + c.innerText.slice(0, 250);
                })
            """) or []

            # Try to extract article text from the post or external link
            article_text = ""
            article_link = self.cdp.evaluate("""
                (function() {
                    var titleLink = document.querySelector('.titleline > a');
                    return titleLink ? titleLink.href : '';
                })()
            """)

            # If it's a text post (Ask HN, Show HN), extract the body
            if "news.ycombinator.com" in (article_link or ""):
                article_text = self.cdp.evaluate("""
                    (function() {
                        var fatitem = document.querySelector('.fatitem');
                        if (fatitem) {
                            var subtext = fatitem.querySelector('.subtext');
                            var text = fatitem.innerText;
                            if (subtext) text = text.replace(subtext.innerText, '');
                            return text.slice(0, 1500).trim();
                        }
                        return '';
                    })()
                """) or ""

            article_title = target.get("title", "")

            # Generate comment with richer context
            comment_text = self._generate_comment(
                article_title=article_title,
                article_text=article_text,
                top_comments=top_comments_raw,
            )

            if not comment_text:
                return ActionResult("comment", False, "Failed to generate comment")

            # Set comment text in textarea
            set_result = self.cdp.evaluate(f"""
                (function() {{
                    var box = document.querySelector('textarea[name="text"]');
                    if (box) {{
                        box.value = {json.dumps(comment_text)};
                        box.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        return 'SET_OK';
                    }}
                    return 'NO_BOX';
                }})()
            """)

            if set_result != "SET_OK":
                return ActionResult("comment", False, "No comment textarea found")

            self.human_pause(1, 2)

            # Submit
            submit_result = self.cdp.evaluate("""
                (function() {
                    var btn = document.querySelector('input[type="submit"]');
                    if (btn) { btn.click(); return 'SUBMITTED'; }
                    return 'NO_BUTTON';
                })()
            """)

            if submit_result != "SUBMITTED":
                return ActionResult("comment", False, "Submit button not found")

            self.human_pause(3, 5)

            # Verify comment appeared
            if username:
                verified = self.cdp.evaluate(f"""
                    (function() {{
                        var found = false;
                        document.querySelectorAll('.hnuser').forEach(function(el) {{
                            if (el.innerText === '{username}') found = true;
                        }});
                        return found ? 'SUCCESS' : 'FAILED';
                    }})()
                """)
                success = verified == "SUCCESS"
            else:
                success = True  # Can't verify without username

            if success:
                self.actions_done["comment"] += 1
                self.record_observation(
                    f"Commented on HN: {target['title'][:60]}",
                    tags=["hn", "comment"],
                    source_url=f"https://news.ycombinator.com/item?id={post_id}",
                )
                return ActionResult("comment", True, f"Commented on post {post_id}")
            else:
                return ActionResult("comment", False, "Comment verification failed")

        except Exception as e:
            return ActionResult("comment", False, f"Error: {e}")

    def _generate_comment(
        self,
        article_title: str,
        article_text: str = "",
        top_comments: List[str] = None,
    ) -> str:
        """
        Generate a human-sounding HN comment using AI.
        Passes article text and existing comments for richer context.
        """
        from core.text_generator import generate_comment
        max_chars = 150 if self._is_new_account() else 500
        return generate_comment(
            platform="hackernews",
            post_title=article_title,
            post_text=article_text,
            existing_comments=top_comments[:5] if top_comments else None,
            max_length=max_chars,
        )

    # ------------------------------------------------------------------
    #  Session orchestration
    # ------------------------------------------------------------------

    def run_session(self, duration_minutes: int) -> List[ActionResult]:
        """Run a complete HN nurturing session."""
        results = []
        results.append(self.browse(duration_minutes))

        # For new accounts (low karma), commenting is the primary karma growth path.
        # If preflight passed (meaning we haven't commented today), prioritize comment.
        is_new = self._is_new_account()

        if is_new:
            # New account: try comment first (most important for karma), then upvote
            if self.random_decision("comment") or self.actions_done["comment"] == 0:
                self.human_pause(2, 5)
                results.append(self.execute_action("comment"))
            # Only upvote if we have remaining capacity and didn't just comment
            if self.random_decision("upvote"):
                self.human_pause(2, 5)
                results.append(self.execute_action("upvote"))
        else:
            # Established account: normal weighted random
            if self.random_decision("upvote"):
                self.human_pause(2, 5)
                results.append(self.execute_action("upvote"))
            if self.random_decision("comment"):
                self.human_pause(2, 5)
                results.append(self.execute_action("comment"))

        return results


# Register with executor
register_platform("hackernews", HackerNewsNurturer)
