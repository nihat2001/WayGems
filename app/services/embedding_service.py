from app.config import settings


async def generate_embedding(text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> list[float] | None:
    try:
        import asyncio
        from google import genai

        client = genai.Client(api_key=settings.gemini_api_key)
        result = await asyncio.to_thread(
            client.models.embed_content,
            model="models/text-embedding-004",
            contents=[text],
            config={"task_type": task_type},
        )
        return result.embeddings[0].values
    except Exception:
        return None
