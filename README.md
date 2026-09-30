# URL Shortener with Docker Compose

A small URL-shortening service that demonstrates how to run a multi-container application with Docker Compose. The app uses Flask (Python) and Redis, and it stores short-code mappings persistently in a Docker volume.

## What it does

- Accepts a long URL through a web form
- Generates a short code (e.g., `aB3_x7`)
- Stores `code → long URL` in Redis
- Redirects users who open the short URL to the original link

## Architecture

- **App service:** Flask web application (Python)
- **Redis service:** In-memory key-value store for mappings
- **Networking:** Private Docker network; app reaches Redis via service name
- **Persistence:** Named Docker volume attached to Redis `/data`

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

Prerequisites: Docker and Docker Compose installed.

1. Clone or copy this repository.
2. From the project root, start the stack:

   ```bash
   docker compose up --build
   ```

3. Open in your browser:

   ```text
   http://localhost:8000
   ```

4. Paste a long URL, click **Shorten**, then open the generated short URL to verify redirection.

## Testing persistence

1. Create a short URL.
2. Recreate only the Redis container:

   ```bash
   docker compose up -d --force-recreate redis
   ```

3. Open the same short URL again. It should still redirect, proving that data is stored in the named volume.

## Key Docker concepts demonstrated

- Multi-stage Docker build for the Flask app
- Docker Compose services, networks, and named volumes
- Service health checks and dependency ordering
- Internal service discovery (`redis` hostname)
- Publishing only the application port to the host

## Notes

- The app listens on port 3000 inside the container.
- The host port (8000) can be changed in `docker-compose.yml` if needed.
- Redis is not exposed to the host; it is reachable only by the app service.

## License

MIT
