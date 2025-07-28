from crawler.platforms.ecommerce import FakeStorePlatform
from crawler.platforms.social import FakeSocialPlatform


class DummyFetcher:
    def fetch(self, url: str, json: bool = False):
        if "fakestoreapi" in url:
            return [{"id": 1, "title": "Item", "price": 9.99}]
        if "jsonplaceholder" in url:
            return [{"id": 1, "title": "Post"}]
        return []


def test_ecommerce_fetch(monkeypatch):
    platform = FakeStorePlatform()
    monkeypatch.setattr(platform, "fetcher", DummyFetcher())
    items = list(platform.fetch_items())
    assert items == [{"id": 1, "title": "Item", "price": 9.99}]


def test_social_fetch(monkeypatch):
    platform = FakeSocialPlatform()
    monkeypatch.setattr(platform, "fetcher", DummyFetcher())
    items = list(platform.fetch_items())
    assert items == [
        {"id": 1, "title": "Post", "url": "https://jsonplaceholder.typicode.com/posts/1"}
    ]
