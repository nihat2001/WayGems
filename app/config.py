from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_password: str = ""
    db_host: str = "localhost"
    db_name: str = "postgres"
    redis_host: str = "localhost"
    groq_api_key: str = ""
    gemini_api_key: str = ""
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "llama-3.3-70b-versatile"
    vector_dimension: int = 768
    n8n_webhook_url: str = ""

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
