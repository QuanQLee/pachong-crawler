from frontend.app import app


def test_index_get():
    client = app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200
