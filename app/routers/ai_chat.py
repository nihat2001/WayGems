from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_service import vector_search
from app.services.llm_service import search_places_ai, recommend_places_ai
from app.schemas.place import PlaceOut

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/search", response_model=ChatResponse)
async def ai_search(req: ChatRequest, db: AsyncSession = Depends(get_session)):
    try:
        places = await vector_search(db, req.query, top_k=req.top_k)
        place_outs = [
            PlaceOut.model_validate(p) for p in places
        ]
        return await search_places_ai(req.query, place_outs, top_k=req.top_k)
    except Exception as e:
        print(f"AI search endpoint error: {e}")
        return ChatResponse(
            answer="Sorry, something went wrong with the search. Please try again in a moment.",
            matches=[],
        )


@router.post("/recommend", response_model=ChatResponse)
async def ai_recommend(req: ChatRequest, db: AsyncSession = Depends(get_session)):
    try:
        places = await vector_search(db, req.query, top_k=req.top_k)
        place_outs = [
            PlaceOut.model_validate(p) for p in places
        ]
        return await recommend_places_ai(req.query, place_outs, top_k=req.top_k)
    except Exception as e:
        print(f"AI recommend endpoint error: {e}")
        return ChatResponse(
            answer="Sorry, something went wrong with the recommendation. Please try again in a moment.",
            matches=[],
        )
