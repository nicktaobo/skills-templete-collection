"""
Platform implementations for social media nurturing.
Import each platform to auto-register it with the executor.
"""

# Auto-import to trigger registration
from .x_twitter import XTwitterNurturer
from .reddit import RedditNurturer
from .hackernews import HackerNewsNurturer
from .product_hunt import ProductHuntNurturer

__all__ = [
    "XTwitterNurturer",
    "RedditNurturer",
    "HackerNewsNurturer",
    "ProductHuntNurturer",
]
