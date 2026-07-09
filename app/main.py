from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db, cache
from app.routers import places, ai_chat
from app.seed.seed_data import seed as run_seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await cache.aclose()


app = FastAPI(
    title="WayGems",
    description="AI-powered travel guide for Baku, Azerbaijan",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(places.router)
app.include_router(ai_chat.router)


@app.get("/health")
async def health():
    return {"status": "ok", "project": "WayGems"}


@app.post("/seed")
async def seed_database():
    await run_seed()
    return {"message": "Database seeded successfully"}
