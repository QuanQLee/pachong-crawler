from flask import Flask, render_template_string, request, jsonify
import asyncio
import threading

from pathlib import Path

from crawler import AsyncCrawler, SQLiteStore, ObjectStore, discover_urls
from crawler.live_ws import LiveWebSocket

app = Flask(__name__)

store = SQLiteStore("crawl.db")
file_store = ObjectStore(Path("data"))
ws = LiveWebSocket()

async def ws_plugin(url: str, html: str) -> None:
    for link in discover_urls(html, url):
        await ws.broadcast(link)

async def save_plugin(url: str, html: str) -> None:
    """Persist crawled pages to the ``data`` directory."""
    from hashlib import md5
    name = md5(url.encode("utf-8")).hexdigest() + ".html"
    file_store.put(name, html.encode("utf-8"))

crawler = AsyncCrawler([], store, plugins=[ws_plugin, save_plugin])
loop = asyncio.new_event_loop()


def _run_background() -> None:
    asyncio.set_event_loop(loop)
    loop.create_task(ws.start())
    loop.create_task(crawler.crawl(continuous=True))
    loop.run_forever()

threading.Thread(target=_run_background, daemon=True).start()

HTML_TEMPLATE = """
<!doctype html>
<title>Pachong Crawler</title>
<h1>Pachong Crawler</h1>
<form id="form">
  URL: <input type=text id="url" size=60>
  <input type=submit value="Enqueue">
</form>
<ul id="results"></ul>
<script>
const ws = new WebSocket("ws://" + location.hostname + ":8765");
ws.onmessage = ev => {
  const li = document.createElement('li');
  li.textContent = ev.data;
  document.getElementById('results').appendChild(li);
};

document.getElementById('form').onsubmit = async ev => {
  ev.preventDefault();
  const url = document.getElementById('url').value;
  await fetch('/enqueue', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({url})
  });
  document.getElementById('url').value = '';
};
</script>
"""


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/enqueue', methods=['POST'])
def enqueue():
    data = request.get_json() or request.form
    url = data.get('url') if data else None
    if not url:
        return jsonify({'error': 'missing url'}), 400
    store.enqueue(url)
    return jsonify({'status': 'enqueued', 'url': url})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
