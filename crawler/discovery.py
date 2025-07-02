"""Utilities for discovering URLs from HTML content."""

from typing import Iterable, Set
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup


def discover_urls(html: str, base_url: str) -> Set[str]:
    """Parse *html* and return absolute URLs discovered on the page."""
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()
        if not href:
            continue
        parsed = urlparse(href)
        if parsed.scheme and parsed.netloc:
            links.add(href)
        else:
            links.add(urljoin(base_url, href))
    return links
