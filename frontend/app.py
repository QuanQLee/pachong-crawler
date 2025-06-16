from flask import Flask, render_template_string, request
from crawler import Fetcher, discovery

app = Flask(__name__)
_fetcher = Fetcher()

HTML_TEMPLATE = """
<!doctype html>
<title>Pachong Crawler</title>
<h1>Pachong Crawler</h1>
<form method=post>
  URL: <input type=text name=url size=60>
  <input type=submit value=Fetch>
</form>
{% if error %}<p style='color:red'>{{ error }}</p>{% endif %}
{% if urls %}
<h2>Discovered URLs</h2>
<ul>
{% for u in urls %}<li><a href='{{ u }}'>{{ u }}</a></li>{% endfor %}
</ul>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    urls = []
    error = None
    if request.method == 'POST':
        url = request.form.get('url', '')
        if url:
            try:
                html = _fetcher.fetch(url)
                urls = list(discovery.discover_urls(html, url))
            except Exception as exc:
                error = str(exc)
    return render_template_string(HTML_TEMPLATE, urls=urls, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
