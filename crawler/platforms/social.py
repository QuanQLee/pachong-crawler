from __future__ import annotations

from typing import Iterable, Any

from . import Platform


class FakeSocialPlatform(Platform):
    """Example social data source using jsonplaceholder posts."""

    API_URL = "https://jsonplaceholder.typicode.com/posts"

    def fetch_items(self) -> Iterable[dict[str, Any]]:
        data = self.fetcher.fetch(self.API_URL, json=True)
        for item in data[:10]:  # take a subset as "trending"
            yield {
                "id": item.get("id"),
                "title": item.get("title"),
                "url": f"{self.API_URL}/{item.get('id')}",
            }
