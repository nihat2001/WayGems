from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas.place import PlaceOut, PlaceDetail, PlaceCreate, PlaceFilter
from app.services.place_service import list_places, get_place, create_place

router = APIRouter(prefix="/places", tags=["places"])


@router.get("", response_model=list[PlaceOut])
async def get_places(
    category_id: int | None = Query(None),
    min_rating: float | None = Query(None),
    max_price: int | None = Query(None),
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_session),
):
    filters = PlaceFilter(
        category_id=category_id,
        min_rating=min_rating,
        max_price=max_price,
        search=search,
        page=page,
        limit=limit,
    )
    places, _ = await list_places(db, filters)
    return places


@router.get("/{place_id}", response_model=PlaceDetail)
async def get_place_detail(place_id: int, db: AsyncSession = Depends(get_session)):
    place = await get_place(db, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return place


@router.post("", response_model=PlaceOut, status_code=201)
async def create_new_place(data: PlaceCreate, db: AsyncSession = Depends(get_session)):
    return await create_place(db, data)
