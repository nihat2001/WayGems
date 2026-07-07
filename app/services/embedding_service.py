import numpy as np
from app.config import settings


def _random_embedding(text: str) -> list[float]:
    np.random.seed(hash(text) % (2**31))
    return np.random.uniform(-0.1, 0.1, settings.vector_dimension).tolist()


async def generate_embedding(text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> list[float]:
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
        return _random_embedding(text)
