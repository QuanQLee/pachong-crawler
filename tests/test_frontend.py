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
