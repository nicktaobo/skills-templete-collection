"""
AI Text Generator for social media comments/replies.
Uses OpenAI-compatible API (Kimi/Moonshot/etc) to generate platform-specific comments.
Falls back to template-based generation if API is unavailable.
"""

import os
import random
from typing import Optional, Dict, List

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


# ---------------------------------------------------------------------------
#  Fallback template library (used when LLM API is unavailable)
# ---------------------------------------------------------------------------
FALLBACK_TEMPLATES = {
    "hackernews": [
        "Interesting approach. I wonder how it handles edge cases with concurrent writes?",
        "The performance numbers look solid, but I'd be curious to see how it behaves under real load.",
        "This reminds me of a similar project from a few years back. The key difference seems to be the handling of failure cases.",
        "Nice writeup. The trade-off between simplicity and features is well explained, though I think the complexity might grow quickly.",
        "I'd be curious to see benchmarks against the existing solutions in this space. The approach seems promising but hard to evaluate without numbers.",
        "The architecture makes sense for small-scale deployments. I'd need more detail on how it handles scaling before I'd consider using it.",
        "Clever use of existing tools rather than reinventing the wheel. That's usually the right call, though I'm not sure about the dependency choices.",
        "I've run into similar issues before. The solution seems reasonable, but I'm skeptical about the claimed performance improvements.",
    ],
    "reddit": [
        "lol this is actually pretty cool ngl",
        "ngl i'd use this. fr.",
        "wait this actually solves a real problem tho",
        "tbh i was skeptical but this looks legit",
        "how long did this take to build? looks solid",
        "damn, didn't expect this to be that good",
        "anyone else tried this yet? looks promising",
        "this is the kind of content i come here for",
    ],
    "x_twitter": [
        "Finally someone built this properly.",
        "The UI alone is worth it. Clean work.",
        "How's the latency on real workloads?",
        "This solves a pain point I didn't know I had.",
        "Shipped faster than most teams I know. Respect.",
        "The real question: can it handle Monday morning traffic?",
        "Been waiting for something like this. Installed.",
    ],
    "product_hunt": [
        "The onboarding flow looks smooth. How long did you spend iterating on that?",
        "Love that you focused on one core feature instead of trying to do everything.",
        "The integration with existing tools is what sold me. Nice work.",
        "Would love to see a dark mode option in the next update.",
        "This fills a gap I've been looking for. The pricing is reasonable too.",
        "How does this compare to the existing players in the space?",
        "The demo video clearly shows the value prop. Well done.",
    ],
}


def _fallback_comment(platform: str, post_title: str = "") -> str:
    """Generate a fallback comment from templates, optionally incorporating post title."""
    templates = FALLBACK_TEMPLATES.get(platform, FALLBACK_TEMPLATES["reddit"])
    base = random.choice(templates)
    # 30% chance to reference the post title briefly
    if post_title and random.random() < 0.3:
        words = post_title.split()[:4]
        short_title = " ".join(words)
        base = f"Re: {short_title}—{base}"
    return base


# ---------------------------------------------------------------------------
#  Platform-specific system prompts
# ---------------------------------------------------------------------------
PLATFORM_PROMPTS = {
    "hackernews": {
        "system": (
            "You are writing a comment on Hacker News. Your goal is to write something that gets upvoted by the HN community.\n\n"
            "CRITICAL RULES:\n"
            "- Plain text ONLY. No markdown (**bold**, *italic*, `code`, links, bullet points, numbered lists). HN strips markdown.\n"
            "- NO structural devices: no 'First... Second... Third...', no 'In summary', no 'Finally'. Write natural flowing paragraphs.\n"
            "- 2-4 short paragraphs, 1-3 sentences each. Total 80-150 words for new accounts, up to 200 for established ones.\n"
            "- NO AI clichés: never say 'Thanks for sharing', 'Great discussion', 'This is fascinating', 'What do you think?', 'I appreciate the insights'.\n\n"
            "WRITING STRATEGY (read this carefully):\n"
            "1. FIRST, analyze the existing comments. Identify what angles have ALREADY been covered. Your comment must add something NEW—don't repeat.\n"
            "2. Reference SPECIFIC details from the article or post. Generic reactions get ignored. Pick one concrete point and expand on it.\n"
            "3. Express a REAL opinion or insight. Disagree respectfully, raise a technical concern, share relevant experience, or ask a pointed follow-up question. Summaries get downvoted.\n"
            "4. Use uncertain language naturally: 'I think', 'maybe', 'not sure but', 'could be wrong', 'my understanding is'. This is very HN-appropriate and signals genuine thought.\n"
            "5. Be slightly skeptical or critical when warranted. HN upvotes honest technical analysis more than praise.\n"
            "6. Tone: thoughtful, direct, slightly informal but NOT casual. No 'lol', 'ngl', 'fr', 'tbh', 'based'. It's okay to be blunt but keep it respectful.\n"
            "7. Occasional minor imperfections are fine—a slightly run-on sentence, a missing comma, lowercase 'i'. But don't overdo it.\n\n"
            "If you can't think of a genuinely valuable angle that hasn't been covered, write a concise technical question about the implementation instead."
        ),
        "max_tokens": 1024,
        "temperature": 0.7,
    },
    "reddit": {
        "system": (
            "You are a casual Reddit commenter. Use occasional slang like lol, ngl, fr, tbh. "
            "Keep it very short—1-2 sentences. Sound like a real person, not a bot. "
            "No AI clichés like 'Thanks for sharing' or 'This is a great question'. "
            "Sometimes ask a follow-up question, sometimes share a quick opinion. "
            "Occasionally use lowercase or skip punctuation for casualness."
        ),
        "max_tokens": 1024,
        "temperature": 0.85,
    },
    "x_twitter": {
        "system": (
            "You are replying on X/Twitter. Keep replies EXTREMELY short: 1 sentence, max 2 short sentences. "
            "Be specific, add value, optionally sarcastic or roasty. "
            "No AI-sounding explanations. No 'Great post!' or 'I love this'. "
            "Use natural internet slang sparingly. Be opinionated."
        ),
        "max_tokens": 1024,
        "temperature": 0.9,
    },
    "product_hunt": {
        "system": (
            "You are commenting on Product Hunt. Comments MUST be specific to the product described. "
            "NO generic praise like 'Great product!' or 'Love this!' or 'Amazing work!'. "
            "Reference actual features, use cases, or give constructive feedback. "
            "Mention a specific thing you find useful or a question about functionality. "
            "Keep under 250 characters. Sound like a potential user evaluating the product."
        ),
        "max_tokens": 1024,
        "temperature": 0.8,
    },
}


class TextGenerator:
    """
    Generates platform-specific comments using an LLM API.
    Falls back to templates if API fails.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        self.model = model or os.getenv("LLM_MODEL", "kimi-for-coding")
        self._client: Optional[OpenAI] = None
        self._api_available: Optional[bool] = None  # None = not tested yet

        if OpenAI is None:
            self._api_available = False

    def _ensure_client(self) -> Optional[OpenAI]:
        if self._api_available is False:
            return None
        if self._client is None:
            if not self.api_key:
                self._api_available = False
                return None
            self._client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        return self._client

    def _test_api(self) -> bool:
        """Quick API health check. Cached after first call."""
        if self._api_available is not None:
            return self._api_available
        client = self._ensure_client()
        if client is None:
            self._api_available = False
            return False
        try:
            client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "hi"}],
                max_tokens=5,
            )
            self._api_available = True
            return True
        except Exception:
            self._api_available = False
            return False

    def generate_comment(
        self,
        platform: str,
        post_title: str,
        post_text: str = "",
        existing_comments: Optional[List[str]] = None,
        max_length: Optional[int] = None,
    ) -> str:
        """
        Generate a comment. Tries LLM first, falls back to templates.
        """
        # Try LLM first
        if self._test_api():
            try:
                text = self._generate_llm(platform, post_title, post_text, existing_comments, max_length)
                if text:
                    return text
            except Exception as e:
                print(f"[TextGenerator] LLM failed, using fallback: {e}")

        # Fallback to templates
        return _fallback_comment(platform, post_title)

    def _generate_llm(
        self,
        platform: str,
        post_title: str,
        post_text: str = "",
        existing_comments: Optional[List[str]] = None,
        max_length: Optional[int] = None,
    ) -> Optional[str]:
        cfg = PLATFORM_PROMPTS.get(platform, PLATFORM_PROMPTS["reddit"])

        parts = [f"Post title: {post_title}"]
        if post_text:
            snippet = post_text[:800]
            parts.append(f"Content: {snippet}")
        if existing_comments:
            comments_text = "\n".join(f"- {c[:200]}" for c in existing_comments[:3])
            parts.append(f"Existing comments:\n{comments_text}")

        user_prompt = "\n\n".join(parts)
        user_prompt += "\n\nWrite a comment. Do not include quotes around your response."
        if max_length:
            user_prompt += f" Max {max_length} characters."

        client = self._ensure_client()
        if client is None:
            return None

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": cfg["system"]},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=cfg["max_tokens"],
            temperature=cfg["temperature"],
        )

        text = response.choices[0].message.content
        if text is None:
            return None
        text = text.strip()
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        if text.startswith("'") and text.endswith("'"):
            text = text[1:-1]
        if max_length and len(text) > max_length:
            text = text[:max_length].rsplit(" ", 1)[0]
        return text


# ---------------------------------------------------------------------------
#  Factory / convenience
# ---------------------------------------------------------------------------
_DEFAULT_GENERATOR: Optional[TextGenerator] = None


def get_generator() -> TextGenerator:
    """Get or create the default text generator."""
    global _DEFAULT_GENERATOR
    if _DEFAULT_GENERATOR is None:
        # Load .env file if exists
        try:
            from dotenv import load_dotenv
            env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
            if os.path.exists(env_path):
                load_dotenv(env_path)
        except ImportError:
            pass

        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        model = os.getenv("LLM_MODEL")

        # Try loading from Hermes config as fallback
        if not api_key:
            try:
                import yaml
                config_path = os.path.expanduser("~/.hermes/config.yaml")
                if os.path.exists(config_path):
                    with open(config_path, "r") as f:
                        cfg = yaml.safe_load(f)
                    model_cfg = cfg.get("model", {})
                    api_key = model_cfg.get("api_key", "")
                    base_url = model_cfg.get("base_url", base_url)
                    model = model_cfg.get("default", model)
            except Exception:
                pass

        _DEFAULT_GENERATOR = TextGenerator(api_key=api_key, base_url=base_url, model=model)
    return _DEFAULT_GENERATOR


def generate_comment(
    platform: str,
    post_title: str,
    post_text: str = "",
    existing_comments: Optional[List[str]] = None,
    max_length: Optional[int] = None,
) -> str:
    """Convenience function using the default generator."""
    return get_generator().generate_comment(platform, post_title, post_text, existing_comments, max_length)
