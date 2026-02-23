# Deribit Price Tracker

A service that tracks cryptocurrency index prices (BTC/USD, ETH/USD) from the [Deribit](https://docs.deribit.com/) exchange and exposes them through a REST API.

## Architecture

The project consists of two independent services sharing a common codebase (`src/share`):

```text
├── src/
│   ├── share/          # Shared domain: entities, repositories, config
│   ├── web/            # FastAPI REST API service
│   └── worker/         # Celery background worker
```

**Worker** — polls Deribit every 60 seconds via Celery Beat, saves prices to PostgreSQL.
**Web** — FastAPI application that serves the stored data.

## Tech Stack

| Layer | Technology |
| --- | --- |
| Language | Python 3.12+ |
| Web framework | FastAPI + Uvicorn / Gunicorn |
| Background tasks | Celery + Redis (broker) |
| Database | PostgreSQL 16 |
| ORM / Migrations | SQLAlchemy 2 (async) + Alembic |
| HTTP client | aiohttp + tenacity (retries) |
| Logging | structlog |
| Config | pydantic-settings |
| Containers | Docker Compose |
| Monitoring | Prometheus, Loki, Promtail, Grafana |
| Dev tools | pytest, mypy, ruff, black, isort |

## API Endpoints

All endpoints require the `ticker` query parameter (`btc_usd` or `eth_usd`).

| Method | Path | Description |
| --- | --- | --- |
| GET | `/prices` | All saved prices for a ticker (paginated) |
| GET | `/prices/last` | Latest saved price for a ticker |
| GET | `/prices/filtered` | Price for a ticker filtered by exact date |

### Query Parameters

**`GET /prices`**

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `ticker` | `btc_usd` \| `eth_usd` | required | Currency ticker |
| `start_date` | datetime / UNIX timestamp | now (UTC) | Pagination cursor |
| `limit` | int | 50 | Max records returned |

**`GET /prices/last`**

| Parameter | Type | Description |
| --- | --- | --- |
| `ticker` | `btc_usd` \| `eth_usd` | Currency ticker |

**`GET /prices/filtered`**

| Parameter | Type | Description |
| --- | --- | --- |
| `ticker` | `btc_usd` \| `eth_usd` | Currency ticker |
| `date` | datetime | Target datetime |

### Response Schema

```json
{
  "id": 1,
  "ticker": "btc_usd",
  "price": "68241.50",
  "created_at": "2024-01-15T12:00:00Z"
}
```

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Make (optional, for convenience commands)

### 1. Configure environment

```bash
cp .env.example .env
```

Edit `.env` if needed (defaults work out of the box with Docker Compose).

### 2. Start infrastructure (PostgreSQL + Redis)

```bash
make infra
# or: docker-compose -f docker-compose.infra.yml up -d --build
```

### 3. Run database migrations

```bash
make upgrade
# or: docker-compose run --rm web alembic upgrade head
```

### 4. Start services

```bash
# Web API (port 8000)
make dev-web

# Worker (in a separate terminal)
make dev-worker
```

The API will be available at `http://localhost:8000`.
Interactive docs: `http://localhost:8000/docs`

## Make Commands

```text
make infra          Start infrastructure (PostgreSQL, Redis)
make upgrade        Apply database migrations
make migrate msg=   Generate a new Alembic migration
make downgrade rev= Rollback to a specific revision

make dev-web        Run the FastAPI web service (dev mode)
make dev-worker     Run the Celery worker (dev mode)
make debug-web      Run the web service with debugpy on port 5678

make monitoring     Start the monitoring stack (Loki, Promtail, Grafana)

make test           Run tests
make lint           Run ruff linter
make type-check     Run mypy
make format         Format code with black + isort
make check          Run lint + type-check + tests

make down           Stop development services
make down-infra     Stop infrastructure
make down-monitoring Stop monitoring stack
```

## Monitoring

Start the full observability stack:

```bash
make monitoring
```

| Service | URL |
| --- | --- |
| Grafana | <http://localhost:3001> |
| Loki | <http://localhost:3100> |

Grafana is pre-configured with Loki as a datasource (no login required in dev mode).

## Environment Variables

| Variable | Description | Example |
| --- | --- | --- |
| `API_VERSION` | API version prefix | `v1` |
| `DEBUG` | Debug mode | `true` |
| `LOG_LEVEL` | Log level | `DEBUG` |
| `REDIS_HOST` | Redis hostname | `redis` |
| `REDIS_PORT` | Redis port | `6379` |
| `REDIS_DB` | Redis DB index for app | `0` |
| `REDIS_CELERY_BROKER_DB` | Redis DB index for Celery | `1` |
| `POSTGRES_HOST` | PostgreSQL hostname | `postgres` |
| `POSTGRES_PORT` | PostgreSQL port | `5432` |
| `POSTGRES_DB` | Database name | `simple_decition` |
| `POSTGRES_USER` | Database user | `postgres` |
| `POSTGRES_PASSWORD` | Database password | `postgres` |
| `CLIENT_BASE_URL` | Deribit API base URL | `https://deribit.com/api/v2` |

## Development

Install dependencies locally (requires [Poetry](https://python-poetry.org/)):

```bash
poetry install --extras all
```

Run the full quality check suite:

```bash
make check
```

The worker fetches prices via `GET /public/get_index_price` with up to 3 retries using exponential backoff (powered by `tenacity`).
