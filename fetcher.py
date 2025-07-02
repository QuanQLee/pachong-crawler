import time
from urllib.parse import urlparse
from urllib import robotparser
import requests


class Fetcher:
    """Simple HTTP fetcher that respects robots.txt and rate-limits requests."""

    def __init__(self, user_agent: str = "pachong-crawler", delay: float = 1.0):
        self.user_agent = user_agent
        self.delay = delay
        self._robots = {}
        self._last_request = {}

    def _get_parser(self, url: str) -> robotparser.RobotFileParser:
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        if base not in self._robots:
            rp = robotparser.RobotFileParser()
            rp.set_url(f"{base}/robots.txt")
            try:
                rp.read()
            except Exception:
                # If robots.txt cannot be read, default to allowing all
                rp = robotparser.RobotFileParser()
                rp.parse([])
            self._robots[base] = rp
        return self._robots[base]

    def can_fetch(self, url: str) -> bool:
        rp = self._get_parser(url)
        return rp.can_fetch(self.user_agent, url)

    def _sleep_if_needed(self, url: str):
        parsed = urlparse(url)
        netloc = parsed.netloc
        now = time.monotonic()
        last = self._last_request.get(netloc)
        if last is not None and now - last < self.delay:
            time.sleep(self.delay - (now - last))
        self._last_request[netloc] = time.monotonic()

    def fetch(self, url: str, **kwargs) -> requests.Response:
        if not self.can_fetch(url):
            raise PermissionError(f"Fetching disallowed by robots.txt: {url}")
        self._sleep_if_needed(url)
        headers = kwargs.pop("headers", {})
        headers.setdefault("User-Agent", self.user_agent)
        response = requests.get(url, headers=headers, **kwargs)
        response.raise_for_status()
        return response
