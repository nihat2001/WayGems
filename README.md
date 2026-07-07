# WayGems

AI-powered travel guide for Baku, Azerbaijan.
  
## Stack

- **FastAPI** (async) — backend API
- **PostgreSQL + pgvector** — database + vector search
- **Redis** — caching
- **Groq** — LLM reasoning (tool calling, few-shot, CoT)
- **Gemini** — text embeddings
- **React + TypeScript** — frontend UI
- **Vite** — build tool
- **Tailwind CSS** — styling
- **Nginx** — reverse proxy (proxies `/api/` to backend) 
- **Docker Compose** — orchestration
 
## Quick Start

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Start all services
docker compose up -d

# 3. Seed database
docker compose exec app python -m app.seed.seed_data

# 4. API available at http://localhost:8000
#    Docs at http://localhost:8000/docs
#    Frontend at http://localhost:8080
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

### Backend

```bash
pip install -r requirements.txt
python -m app.seed.seed_data
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend dev server (Vite) proxies `/api/` requests to the backend at `http://localhost:8000`.

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
frontend/
├── src/
│   ├── api/client.ts    # API client
│   ├── components/      # Reusable UI (Layout, PlaceCard, ChatBubble, ...)
│   ├── pages/           # Route pages (AIChatPage, PlacesPage, PlaceDetailPage)
│   ├── hooks/           # Custom hooks
│   ├── types/           # TypeScript types
│   ├── App.tsx
│   └── main.tsx
├── nginx.conf           # Reverse proxy config
└── Dockerfile
```
