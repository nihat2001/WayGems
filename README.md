# 🗺️ WayGems: AI-Powered Travel Guide for Baku

An intelligent, AI-driven travel companion designed to help travelers explore *Baku, Azerbaijan*. By combining modern semantic search with advanced LLM reasoning, WayGems offers personalized recommendations, contextual city insights, and natural language search tailored to every user's preferences.

## 🚀 Key Features

| *Feature* | *Description* | *Technology Used* |
| ----- | ----- | ----- |
| *🤖 AI Recommendations* | Delivers deep, contextual travel suggestions using Chain-of-Thought (CoT) reasoning instead of generic lists. | Groq LLM |
| *🔍 Semantic Search* | Understands user intent behind complex queries like *"cozy places to drink traditional tea near Old City"*. | Gemini Text Embeddings & pgvector |
| *📄 PDF Document Processing* | Extracts and parses local travel brochures, historical guides, and itineraries to enrich the knowledge base. | PyMuPDF (fitz) |
| *⚡ High Performance* | Fully asynchronous API architecture cached with Redis for lightning-fast response times. | FastAPI & Redis |
| *💻 Modern UI/UX* | Responsive, clean, and intuitive dashboard built for smooth user navigation. | React, TypeScript & Tailwind CSS |
| *🐳 Containerized* | Production-ready environment setup for easy and consistent deployment. | Docker Compose & Nginx |
| *🌤️ Live Weather* | Real-time weather data fetched via n8n workflow and injected into AI responses. | n8n & Open-Meteo API |

## 🛠️ Tech Stack & Infrastructure

| *Component* | *Technology* | *Role in Project* |
| ----- | ----- | ----- |
| *Backend Framework* | FastAPI | Asynchronous REST API development |
| *Database* | PostgreSQL + pgvector | Relational data storage and vector similarity search |
| *Caching Layer* | Redis | API response caching and session optimization |
| *PDF Extraction Engine* | PyMuPDF (fitz) | High-performance PDF text parsing and document processing |
| *LLM Reasoning* | Groq (Llama-3) | Tool calling, few-shot prompting, and CoT reasoning |
| *Embeddings Engine* | Gemini API | Generating high-dimensional text embeddings for places |
| *Workflow Automation* | n8n | Live weather data pipeline (webhook → Open-Meteo → formatted response) |
| *Frontend Core* | React + TypeScript | Robust, type-safe user interface development |
| *Build Tool* | Vite | Ultra-fast frontend bundling and hot reloading |
| *Styling* | Tailwind CSS | Modern utility-first responsive styling |
| *Reverse Proxy* | Nginx | Routing client traffic efficiently to the backend API |
| *Orchestration* | Docker Compose | Managing multi-container application lifecycle |

## 📂 Project Structure

| *Directory* | *Type* | *Description* |
| ----- | ----- | ----- |
| app/main.py | File | FastAPI application initialization and entry point |
| app/config.py | File | Environment variables and global configuration management |
| app/database.py | File | Database engines, SQLAlchemy session lifecycle, and Redis client |
| app/models/ | Folder | SQLAlchemy database models defining the schema |
| app/schemas/ | Folder | Pydantic validation schemas for request/response serialization |
| app/routers/ | Folder | API endpoint controllers (places CRUD, AI chat) |
| app/services/ | Folder | Core business logic, vector search, LLM pipeline, and n8n integration |
| app/utils/ | Folder | System prompt templates with embedded Baku knowledge |
| app/seed/ | Folder | Database seeder with 16 original Baku places |
| frontend/src/api/ | Folder | Axios/Fetch client configuration and central API layer |
| frontend/src/components/ | Folder | Reusable UI design elements (Layout, PlaceCard, ChatBubble) |
| frontend/src/pages/ | Folder | Application views (AIChatPage, PlacesPage, PlaceDetailPage) |
| frontend/src/hooks/ | Folder | Custom React hooks for global state and data fetching |
| frontend/nginx.conf | File | Reverse proxy routing configuration inside the frontend container |

## 💬 AI Chat Features

The AI chat supports natural language queries about places in Baku, enhanced with:
- *Baku knowledge* — LLM prompts include metro lines/stations, all 12 districts, Bayil neighborhood, and key landmarks
- *Conversation memory* — chat history persisted in localStorage, sent to the backend for context-aware responses
- *Clear chat* — one-click reset button in the chat header

## 🌤️ Live Weather (via n8n)

Queries about current weather fetch real-time data through an n8n workflow:
1. *Backend* sends the user query to the n8n webhook
2. *n8n HTTP Request node* fetches weather from Open-Meteo API (`latitude=40.3776&longitude=49.8924`)
3. *n8n Code node* parses the response (temperature, humidity, wind, weather code)
4. *Formatted text* is returned and injected into the LLM prompt alongside Baku knowledge
