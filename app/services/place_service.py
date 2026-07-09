from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Place
from app.schemas.place import PlaceCreate, PlaceFilter


async def list_places(db: AsyncSession, filters: PlaceFilter) -> tuple[list[Place], int]:
    query = select(Place).where(Place.is_active == True)

    if filters.category_id is not None:
        query = query.where(Place.category_id == filters.category_id)
    if filters.min_rating is not None:
        query = query.where(Place.rating >= filters.min_rating)
    if filters.max_price is not None:
        query = query.where(Place.price_level <= filters.max_price)
    if filters.search:
        query = query.where(
            Place.name.ilike(f"%{filters.search}%")
            | Place.description.ilike(f"%{filters.search}%")
        )

    count_query = select(Place.id).where(Place.is_active == True)
    if filters.category_id is not None:
        count_query = count_query.where(Place.category_id == filters.category_id)

    total = len((await db.execute(count_query)).scalars().all())

    offset = (filters.page - 1) * filters.limit
    query = query.offset(offset).limit(filters.limit).order_by(Place.rating.desc())

    result = await db.execute(query)
    return result.scalars().all(), total


async def get_place(db: AsyncSession, place_id: int) -> Place | None:
    stmt = (
        select(Place)
        .options(selectinload(Place.category))
        .where(Place.id == place_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_place(db: AsyncSession, data: PlaceCreate) -> Place:
    place = Place(**data.model_dump())
    db.add(place)
    await db.commit()
    await db.refresh(place)
    return place
