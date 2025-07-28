from __future__ import annotations

from typing import Iterable, Any

from . import Platform


class FakeStorePlatform(Platform):
    """Example e-commerce data source using the fakestoreapi."""

    API_URL = "https://fakestoreapi.com/products"

    def fetch_items(self) -> Iterable[dict[str, Any]]:
        data = self.fetcher.fetch(self.API_URL, json=True)
        for item in data:
            yield {
                "id": item.get("id"),
                "title": item.get("title"),
                "price": item.get("price"),
            }
