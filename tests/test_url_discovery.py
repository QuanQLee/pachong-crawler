from crawler.url_discovery import discover_urls


def test_discover_urls_basic():
    html = '<a href="http://example.com">Example</a>'
    assert discover_urls(html) == ["http://example.com"]


def test_discover_urls_multiple():
    html = '<a href="https://example.com/page1">One</a> <a href="http://example.com/page2">Two</a>'
    assert discover_urls(html) == [
        "https://example.com/page1",
        "http://example.com/page2",
    ]


def test_discover_urls_none():
    assert discover_urls("No links here!") == []
