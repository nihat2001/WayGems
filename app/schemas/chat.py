from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.place import PlaceOut


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    top_k: int = Field(default=5, ge=1, le=20)


class AIPlaceResult(BaseModel):
    place: PlaceOut | None = None
    confidence: float = Field(default=0.0, ge=0, le=1)
    reasoning: str = ""


class ChatResponse(BaseModel):
    answer: str = ""
    matches: list[AIPlaceResult] = Field(default_factory=list)
