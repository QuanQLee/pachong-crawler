"""Run AsyncCrawler and broadcast discovered URLs over WebSocket."""

import asyncio
from crawler import AsyncCrawler, SQLiteStore
from .live_ws import LiveWebSocket
from .discovery import discover_urls


async def ws_plugin(ws: LiveWebSocket, url: str, html: str) -> None:
    for link in discover_urls(html, url):
        await ws.broadcast(link)


async def main() -> None:
    ws = LiveWebSocket()
    store = SQLiteStore("crawl.db")
    crawler = AsyncCrawler(["https://example.com"], store, plugins=[lambda u, h: ws_plugin(ws, u, h)])
    await asyncio.gather(ws.start(), crawler.crawl(continuous=True))


if __name__ == "__main__":
    asyncio.run(main())
