from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
import redis.asyncio as redis

from app.config import settings

DATABASE_URL = f"postgresql+asyncpg://postgres:{settings.db_password}@{settings.db_host}:5432/{settings.db_name}"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

cache = redis.Redis(host=settings.redis_host, port=6379, decode_responses=True)
Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
