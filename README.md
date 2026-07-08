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

---

## 🛠️ Tech Stack & Infrastructure

| Component | Technology | Role in Project |
| :--- | :--- | :--- |
| **Backend Framework** | FastAPI | Asynchronous REST API development |
| **Database** | PostgreSQL + `pgvector` | Relational data storage and vector similarity search |
| **Caching Layer** | Redis | API response caching and session optimization |
| **LLM Reasoning** | Groq (Llama-3) | Tool calling, few-shot prompting, and CoT reasoning |
| **Embeddings Engine** | Gemini API | Generating high-dimensional text embeddings for places |
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
| `app/routers/` | Folder | API endpoint controllers routing specific domains |
| `app/services/` | Folder | Core business logic, vector search, and AI pipeline orchestration |
| `app/utils/` | Folder | Text preprocessing and system prompt engineering templates |
| `app/seed/` | Folder | Database initialization scripts and mock data seeder for Baku |
| `frontend/src/api/` | Folder | Axios/Fetch client configuration and central API layer |
| `frontend/src/components/` | Folder | Reusable UI design elements (Layout, PlaceCard, ChatBubble) |
| `frontend/src/pages/` | Folder | Application views (AIChatPage, PlacesPage, PlaceDetailPage) |
| `frontend/src/hooks/` | Folder | Custom React hooks for global state and data fetching |
| `frontend/nginx.conf` | File | Reverse proxy routing configuration inside the frontend container |

---

## 🔌 Core API Endpoints

| Method | Endpoint | Query/Body Params | Description |
| :--- | :--- | :--- | :--- |
| 🟢 **GET** | `/api/categories` | None | Retrieve all available place categories (e.g., Cafe, Museum) |
| 🟢 **GET** | `/api/places` | `page`, `limit`, `category` | Paginated & filterable list of locations in Baku |
| 🟢 **GET** | `/api/places/{id}` | `id` (Path) | Detailed view and metadata of a specific place |
| 🔵 **POST** | `/api/places` | JSON Body | Add a new location directly to the database |
| 🔵 **POST** | `/api/ai/search` | `{"query": "string"}` | Semantic, natural language search powered by vector embeddings |
| 🔵 **POST** | `/api/ai/recommend`| `{"preferences": []}` | AI recommendation engine featuring detailed contextual reasoning |
| 🟢 **GET** | `/api/health` | None | System check for Database, Redis, and API status |

---

## 🚦 Quick Start (Docker Deployment)

### 1. Environment Setup
Clone the repository and create your environment file from the template:
```bash
cp .env.example .env
