from frontend.app import app


def test_index_get():
    client = app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200


def test_enqueue_post():
    client = app.test_client()
    resp = client.post('/enqueue', json={'url': 'http://example.com'})
    assert resp.status_code == 200
    assert resp.get_json()['status'] == 'enqueued'


def test_platform_endpoints(monkeypatch):
    client = app.test_client()

    class DummyFetcher:
        def fetch(self, url: str, json: bool = False):
            if 'fakestoreapi' in url:
                return [{'id': 1, 'title': 'Item', 'price': 9.99}]
            if 'jsonplaceholder' in url:
                return [{'id': 1, 'title': 'Post'}]
            return []

    import crawler.platforms as cp
    monkeypatch.setattr(cp, 'Fetcher', DummyFetcher)

    resp = client.get('/platform/ecommerce')
    assert resp.status_code == 200
    assert resp.get_json() == [{'id': 1, 'title': 'Item', 'price': 9.99}]

    resp = client.get('/platform/social')
    assert resp.status_code == 200
    assert resp.get_json() == [
        {'id': 1, 'title': 'Post', 'url': 'https://jsonplaceholder.typicode.com/posts/1'}
    ]
