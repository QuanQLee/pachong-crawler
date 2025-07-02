import asyncio
import time
import sqlite3
import threading
from typing import Iterable, Callable, Awaitable, Set
from urllib.parse import urljoin

import aiohttp
from aiohttp import ClientResponseError
from bs4 import BeautifulSoup


class SQLiteStore:
    """Simple SQLite-based storage for crawled pages and queue."""

    def __init__(self, path: str = "crawl.db") -> None:
        # Allow the connection to be shared across threads
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._lock = threading.Lock()
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS pages (url TEXT PRIMARY KEY, html TEXT)"
        )
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS queue (url TEXT PRIMARY KEY)"
        )
        self.conn.commit()

    def visited(self) -> Set[str]:
        with self._lock:
            cur = self.conn.execute("SELECT url FROM pages")
            return {row[0] for row in cur.fetchall()}

    def enqueue(self, url: str) -> None:
        with self._lock:
            self.conn.execute("INSERT OR IGNORE INTO queue(url) VALUES (?)", (url,))
            self.conn.commit()

    def dequeue(self) -> str | None:
        with self._lock:
            cur = self.conn.execute("SELECT url FROM queue LIMIT 1")
            row = cur.fetchone()
            if row:
                self.conn.execute("DELETE FROM queue WHERE url=?", (row[0],))
                self.conn.commit()
                return row[0]
            return None

    def save(self, url: str, html: str) -> None:
        with self._lock:
            self.conn.execute(
                "INSERT OR REPLACE INTO pages(url, html) VALUES (?, ?)",
                (url, html),
            )
            self.conn.commit()


class AsyncFetcher:
    """Fetcher that first tries ``aiohttp`` and falls back to Playwright."""

    def __init__(self, delay: float = 1.0, proxy: str | None = None) -> None:
        self.delay = delay
        self.proxy = proxy
        self._last_request = 0.0

    async def _wait(self) -> None:
        now = time.time()
        elapsed = now - self._last_request
        if elapsed < self.delay:
            await asyncio.sleep(self.delay - elapsed)
        self._last_request = time.time()

    async def _fetch_aiohttp(self, session: aiohttp.ClientSession, url: str) -> str:
        await self._wait()
        async with session.get(url, proxy=self.proxy) as resp:
            if resp.status in (403, 429):
                raise ClientResponseError(
                    resp.request_info, resp.history, status=resp.status, message=resp.reason
                )
            text = await resp.text()
            if "<script" in text.lower():
                # Heuristic that page likely requires JS rendering
                raise RuntimeError("js-detected")
            return text

    async def _fetch_playwright(self, url: str) -> str:
        from playwright.async_api import async_playwright

        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url)
            content = await page.content()
            await browser.close()
            return content

    async def fetch(self, session: aiohttp.ClientSession, url: str) -> str:
        try:
            return await self._fetch_aiohttp(session, url)
        except (ClientResponseError, RuntimeError):
            return await self._fetch_playwright(url)


PluginFunc = Callable[[str, str], Awaitable[None]]


class AsyncCrawler:
    """Breadth-first asynchronous crawler with resumable queue."""

    def __init__(
        self,
        seeds: Iterable[str],
        store: SQLiteStore,
        *,
        delay: float = 1.0,
        plugins: Iterable[PluginFunc] | None = None,
    ) -> None:
        self._seeds = list(seeds)
        self._store = store
        self._fetcher = AsyncFetcher(delay=delay)
        self._plugins = list(plugins or [])

    async def crawl(self, *, continuous: bool = False) -> None:
        visited = self._store.visited()
        for s in self._seeds:
            if s not in visited:
                self._store.enqueue(s)

        async with aiohttp.ClientSession() as session:
            while True:
                url = self._store.dequeue()
                if not url:
                    if continuous:
                        await asyncio.sleep(1)
                        continue
                    break
                if url in visited:
                    continue
                visited.add(url)
                try:
                    html = await self._fetcher.fetch(session, url)
                except Exception:
                    continue
                self._store.save(url, html)
                for plugin in self._plugins:
                    await plugin(url, html)
                for link in self._extract_links(html, url):
                    if link not in visited:
                        self._store.enqueue(link)

    def _extract_links(self, html: str, base: str) -> Iterable[str]:
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup.find_all("a", href=True):
            yield urljoin(base, tag["href"])


async def _main() -> None:
    store = SQLiteStore("crawl.db")
    crawler = AsyncCrawler(["https://example.com"], store)
    await crawler.crawl()


if __name__ == "__main__":
    asyncio.run(_main())
