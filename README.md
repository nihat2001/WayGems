# 🗺️ WayGems: AI-Powered Travel Guide for Baku

An intelligent, AI-driven travel companion designed to help travelers explore **Baku, Azerbaijan**. By combining modern semantic search with advanced LLM reasoning, WayGems offers personalized recommendations, contextual city insights, and natural language search tailored to every user's preferences.

---

## 🚀 Key Features

| Feature | Description | Technology Used |
| :--- | :--- | :--- |
| **🤖 AI Recommendations** | Delivers deep, contextual travel suggestions using Chain-of-Thought (CoT) reasoning instead of generic lists. | Groq LLM |
| **🔍 Semantic Search** | Understands user intent behind complex queries like *"cozy places to drink traditional tea near Old City"*. | Gemini Text Embeddings & `pgvector` |
| **⚡ High Performance** | Fully asynchronous API architecture cached with Redis for lightning-fast response times. | FastAPI & Redis |
| **💻 Modern UI/UX** | Responsive, clean, and intuitive dashboard built for smooth user navigation. | React, TypeScript & Tailwind CSS |
| **🐳 Containerized** | Production-ready environment setup for easy and consistent deployment. | Docker Compose & Nginx |
| **🌤️ Live Weather** | Real-time weather data fetched via n8n workflow and injected into AI responses. | n8n & Open-Meteo API |

---

## 🛠️ Tech Stack & Infrastructure

| Component | Technology | Role in Project |
| :--- | :--- | :--- |
| **Backend Framework** | FastAPI | Asynchronous REST API development |
| **Database** | PostgreSQL + `pgvector` | Relational data storage and vector similarity search |
| **Caching Layer** | Redis | API response caching and session optimization |
| **LLM Reasoning** | Groq (Llama-3) | Tool calling, few-shot prompting, and CoT reasoning |
| **Embeddings Engine** | Gemini API | Generating high-dimensional text embeddings for places |
| **Workflow Automation** | n8n | Live weather data pipeline (webhook → Open-Meteo → formatted response) |
| **Frontend Core** | React + TypeScript | Robust, type-safe user interface development |
| **Build Tool** | Vite | Ultra-fast frontend bundling and hot reloading |
| **Styling** | Tailwind CSS | Modern utility-first responsive styling |
| **Reverse Proxy** | Nginx | Routing client traffic efficiently to the backend API |
| **Orchestration** | Docker Compose | Managing multi-container application lifecycle |

---

## 📂 Project Structure

| Directory | Type | Description |
| :--- | :--- | :--- |
| `app/main.py` | File | FastAPI application initialization and entry point |
| `app/config.py` | File | Environment variables and global configuration management |
| `app/database.py` | File | Database engines, SQLAlchemy session lifecycle, and Redis client |
| `app/models/` | Folder | SQLAlchemy database models defining the schema |
| `app/schemas/` | Folder | Pydantic validation schemas for request/response serialization |
| `app/routers/` | Folder | API endpoint controllers (places CRUD, AI chat) |
| `app/services/` | Folder | Core business logic, vector search, LLM pipeline, and n8n integration |
| `app/utils/` | Folder | System prompt templates with embedded Baku knowledge |
| `app/seed/` | Folder | Database seeder with 16 original Baku places |
| `frontend/src/api/` | Folder | Axios/Fetch client configuration and central API layer |
| `frontend/src/components/` | Folder | Reusable UI design elements (Layout, PlaceCard, ChatBubble) |
| `frontend/src/pages/` | Folder | Application views (AIChatPage, PlacesPage, PlaceDetailPage) |
| `frontend/src/hooks/` | Folder | Custom React hooks for global state and data fetching |
| `frontend/nginx.conf` | File | Reverse proxy routing configuration inside the frontend container |

---

## 🔌 Core API Endpoints

| Method | Endpoint | Query/Body Params | Description |
| :--- | :--- | :--- | :--- |
| 🟢 **GET** | `/api/places` | `page`, `limit`, `category` | Paginated & filterable list of locations in Baku |
| 🟢 **GET** | `/api/places/{id}` | `id` (Path) | Detailed view and metadata of a specific place |
| 🔵 **POST** | `/api/places` | JSON Body | Add a new location directly to the database |
| 🔵 **POST** | `/api/ai/search` | `{"query", "history"}` | Natural language place search with conversation memory |
| 🔵 **POST** | `/api/ai/recommend` | `{"query", "history"}` | AI recommendation engine with detailed contextual reasoning |
| 🟢 **GET** | `/api/health` | None | System check for Database, Redis, and API status |

---

## 🚦 Quick Start (Docker Deployment)

### 1. Environment Setup
Clone the repository and create your environment file from the template:
```bash
cp .env.example .env
```

### 2. Start All Services
```bash
docker compose up -d
```

### 3. Seed the Database
```bash
docker compose exec app python -m app.seed.seed_data
```

### 4. Access the Application
- **API** — [http://localhost:8000](http://localhost:8000)
- **API Docs** — [http://localhost:8000/docs](http://localhost:8000/docs)
- **Frontend** — [http://localhost:8080](http://localhost:8080)

---

## 💬 AI Chat Features

The AI chat supports natural language queries about places in Baku, enhanced with:

- **Baku knowledge** — LLM prompts include metro lines/stations, all 12 districts, Bayil neighborhood, and key landmarks
- **Conversation memory** — chat history persisted in `localStorage`, sent to the backend for context-aware responses
- **Clear chat** — one-click reset button in the chat header

### 🌤️ Live Weather (via n8n)

Queries about current weather fetch real-time data through an n8n workflow:

1. **Backend** sends the user query to the n8n webhook
2. **n8n HTTP Request node** fetches weather from Open-Meteo API (`latitude=40.3776&longitude=49.8924`)
3. **n8n Code node** parses the response (temperature, humidity, wind, weather code)
4. **Formatted text** is returned and injected into the LLM prompt alongside Baku knowledge

To enable, add to `.env`:
```
N8N_WEBHOOK_URL=http://host.docker.internal:5678/webhook/your-webhook-id
```
Then activate the workflow in the n8n editor (`http://localhost:5678`).

---

## 🛠️ Local Dev (without Docker)

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

The Vite dev server proxies `/api/` requests to the backend at `http://localhost:8000`.
