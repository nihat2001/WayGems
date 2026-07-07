# WayGems

AI-powered travel guide for Baku, Azerbaijan.

## Stack

- **FastAPI** (async) — backend API
- **PostgreSQL + pgvector** — database + vector search
- **Redis** — caching
- **Groq** — LLM reasoning (tool calling, few-shot, CoT)
- **Gemini** — text embeddings
- **Docker Compose** — orchestration

## Quick Start

```bash
# 1. Start all services
docker compose up -d

# 2. Seed database
docker compose exec app python -m app.seed.seed_data

# 3. API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/categories` | List all place categories |
| GET | `/places` | Filtered & paginated places |
| GET | `/places/{id}` | Place detail |
| POST | `/places` | Create a new place |
| POST | `/ai/search` | Natural language place search |
| POST | `/ai/recommend` | AI recommendation with reasoning |
| GET | `/health` | Health check |

## Local Dev (without Docker)

```bash
pip install -r requirements.txt
python -m app.seed.seed_data
uvicorn app.main:app --reload
```

## Project Structure

```
app/
├── main.py              # FastAPI app
├── config.py            # Settings from .env
├── database.py          # Engine, session, Redis
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic validation
├── routers/             # API endpoints
├── services/            # Business logic + AI pipeline
├── utils/               # Text cleaning, prompts
└── seed/                # Database seeder
```
