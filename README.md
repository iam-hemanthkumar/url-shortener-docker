# URL Shortener with Docker Compose

A simple URL-shortening application built with Flask, Redis, and Docker Compose.

## What it does

- Takes a long URL from a web form
- Creates a short code
- Stores the short code and original URL in Redis
- Redirects the short URL to the original URL

## Architecture

- **App:** Flask application running in Python
- **Redis:** Stores the URL mappings
- **Network:** The app and Redis communicate through a Docker network
- **Volume:** Redis data is stored in a named Docker volume

## Project structure

```text
url-shortener/
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
└── app/
    ├── Dockerfile
    ├── app.py
    └── requirements.txt
```

## Running the project

Make sure Docker and Docker Compose are installed.

From the project directory, run:

```bash
docker compose up --build
```

Then open:

```text
http://localhost:8000
```

Paste a URL and click **Shorten**. The application generates a short URL that redirects to the original URL.

## Testing persistence

To verify that Redis data is stored in the Docker named volume:

1. Create a short URL.
2. Copy or keep the generated short URL.
3. Recreate only the Redis container:

   ```bash
   docker compose up -d --force-recreate redis
   ```

4. Open the same short URL again.

The URL should still work because the Redis data is stored in the named volume, not only inside the Redis container.

## Docker concepts used

- Docker Compose
- Dockerfile
- Multi-stage build
- Docker networks
- Named volumes
- Health checks
- Service names for container communication
- Port mapping

## Notes

- The Flask app runs on port `3000` inside the container.
- Port `8000` on the host is mapped to the application.
- Redis is not exposed to the host.
- The app connects to Redis using the service name `redis`.

## License

MIT
