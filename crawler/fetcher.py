"""Simple HTTP fetcher with rudimentary rate limiting."""

import time
from typing import Any, Optional

import requests


class Fetcher:
    """Fetch HTML or JSON content from the web respecting a delay."""

    def __init__(self, delay: float = 1.0, session: Optional[requests.Session] = None) -> None:
        self.delay = delay
        self.session = session or requests.Session()
        self._last_request = 0.0

    def _wait(self) -> None:
        """Wait for ``delay`` seconds since the previous request."""
        now = time.time()
        elapsed = now - self._last_request
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self._last_request = time.time()

    def fetch(self, url: str, *, json: bool = False, **kwargs: Any) -> Any:
        """Fetch ``url`` and return text or JSON depending on ``json`` flag."""
        self._wait()
        resp = self.session.get(url, **kwargs)
        resp.raise_for_status()
        return resp.json() if json else resp.text
