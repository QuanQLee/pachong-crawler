import re
from typing import List


def discover_urls(html: str) -> List[str]:
    """Return a list of URLs found in the provided HTML string."""
    if not html:
        return []
    pattern = re.compile(r'href=[\'\"]?(https?://[^\'\"\s>]+)')
    return pattern.findall(html)
