import asyncio
import requests
from app.config import settings


N8N_TIMEOUT = 10


async def get_n8n_context(query: str, places_text: str) -> str:
    url = settings.n8n_webhook_url
    if not url:
        return ""

    def _sync_call() -> str:
        try:
            resp = requests.post(
                url,
                json={"query": query, "places": places_text},
                timeout=N8N_TIMEOUT,
            )
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    if isinstance(data, dict):
                        return next(iter(data.values()), resp.text)
                except Exception:
                    pass
                return resp.text
            else:
                print(f"n8n webhook error: {resp.status_code} {resp.text}")
        except requests.RequestException as e:
            print(f"n8n webhook call failed: {e}")
        return ""

    return await asyncio.to_thread(_sync_call)
