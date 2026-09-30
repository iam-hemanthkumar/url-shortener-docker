import os
import secrets
from urllib.parse import urlparse

import redis
from flask import Flask, abort, redirect, render_template_string, request, url_for

app = Flask(__name__)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
)

HOME_PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>URL Shortener</title>
</head>
<body>
  <main>
    <h1>URL Shortener</h1>

    <form action="{{ url_for('shorten') }}" method="post">
      <label for="url">Paste a long URL</label><br>
      <input
        id="url"
        name="url"
        type="url"
        placeholder="https://example.com"
        required
        size="60"
      >
      <button type="submit">Shorten</button>
    </form>

    {% if error %}
      <p style="color: red;">{{ error }}</p>
    {% endif %}

    {% if short_url %}
      <h2>Your short URL</h2>
      <p>
        <a href="{{ short_url }}">{{ short_url }}</a>
      </p>
    {% endif %}
  </main>
</body>
</html>
"""


def is_valid_url(value):
    parsed = urlparse(value)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def create_short_code():
    return secrets.token_urlsafe(5)


@app.get("/")
def home():
    return render_template_string(HOME_PAGE)


@app.post("/shorten")
def shorten():
    long_url = request.form.get("url", "").strip()

    if not is_valid_url(long_url):
        return render_template_string(
            HOME_PAGE,
            error="Please enter a valid URL starting with http:// or https://",
        ), 400

    while True:
        code = create_short_code()
        key = f"url:{code}"

        if redis_client.set(key, long_url, nx=True):
            break

    short_url = url_for("follow_short_url", code=code, _external=True)
    return render_template_string(HOME_PAGE, short_url=short_url)


@app.get("/health")
def health():
    try:
        redis_client.ping()
        return {"status": "healthy", "redis": "connected"}, 200
    except redis.RedisError:
        return {"status": "unhealthy", "redis": "unavailable"}, 503


@app.get("/<code>")
def follow_short_url(code):
    long_url = redis_client.get(f"url:{code}")

    if long_url is None:
        abort(404, description="Short URL not found")

    return redirect(long_url, code=302)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("APP_PORT", "3000")),
    )
