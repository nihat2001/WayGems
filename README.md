# WayGems

AI-powered travel guide for Baku, Azerbaijan.
  
## Stack

- **FastAPI** (async) — backend API
- **PostgreSQL + pgvector** — database + vector search
- **Redis** — caching
- **Groq** — LLM reasoning (few-shot, CoT, general knowledge)
- **Gemini** — text embeddings
- **n8n** — workflow automation (live weather data)
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
| GET | `/places` | Filtered & paginated places |
| GET | `/places/{id}` | Place detail |
| POST | `/places` | Create a new place |
| POST | `/ai/search` | Natural language place search |
| POST | `/ai/recommend` | AI recommendation with reasoning |
| GET | `/health` | Health check |

## AI Chat Features

- **Baku knowledge** — LLM prompts include metro lines/stations, all 12 districts, neighborhoods, and landmarks
- **Conversation memory** — chat history is persisted in `localStorage` and sent to the backend with each request
- **Live weather** — queries about current weather fetch real-time data via an n8n workflow (Open-Meteo API)

### n8n Weather Workflow

A separate n8n Docker service exposes a webhook that:
1. Receives the user query from the backend
2. Fetches current weather from Open-Meteo API
3. Parses & formats the response (temperature, humidity, wind, description)
4. Returns structured text injected into the LLM prompt

Enable by setting `N8N_WEBHOOK_URL` in `.env` and activating the workflow in n8n.

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
├── main.py                 # FastAPI app
├── config.py               # Settings from .env
├── database.py             # Engine, session, Redis
├── models/                 # SQLAlchemy models
├── schemas/                # Pydantic validation
├── routers/                # API endpoints
│   ├── ai_chat.py          # AI search & recommend
│   └── places.py           # Places CRUD
├── services/               # Business logic + AI pipeline
│   ├── llm_service.py      # LLM calls, prompt routing
│   ├── rag_service.py      # Vector search + fallback
│   ├── embedding_service.py
│   └── n8n_service.py      # Live data via n8n webhook
├── utils/
│   └── prompts.py          # System prompts + Baku knowledge
└── seed/
    └── seed_data.py        # 16 original Baku places
frontend/
├── src/
│   ├── api/
│   │   └── client.ts       # API client (+ ai.search/ai.recommend)
│   ├── components/         # Layout, PlaceCard, ChatBubble, ...
│   ├── pages/
│   │   ├── AIChatPage.tsx  # Chat UI + localStorage + Clear chat
│   │   ├── PlacesPage.tsx
│   │   └── PlaceDetailPage.tsx
│   ├── hooks/
│   ├── types/
│   ├── App.tsx
│   └── main.tsx
├── nginx.conf
└── Dockerfile
```
