from pathlib import Path

import crawler.main as main

class DummyFetcher:
    def __init__(self, delay=1.0):
        pass
    def fetch(self, url):
        return "<html>dummy</html>"

def test_main_stores_file(tmp_path, monkeypatch):
    monkeypatch.setattr("crawler.fetcher.Fetcher", DummyFetcher)
    import crawler
    monkeypatch.setattr(crawler, "Fetcher", DummyFetcher, raising=False)
    # Use real ObjectStore
    output = tmp_path
    main.main(["--seed", "http://example.com", "--output-dir", str(output)])
    files = list(output.glob("*.html"))
    assert len(files) == 1
    assert files[0].read_text() == "<html>dummy</html>"
