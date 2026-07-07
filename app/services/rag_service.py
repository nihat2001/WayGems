from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Place
from app.services.embedding_service import generate_embedding


async def vector_search(
    db: AsyncSession, query: str, top_k: int = 5
) -> list[Place]:
    try:
        embedding = await generate_embedding(query, task_type="RETRIEVAL_QUERY")
    except Exception as e:
        print(f"Failed to generate query embedding: {e}")
        return []

    if not embedding:
        return []

    embedding_str = "[" + ",".join(str(v) for v in embedding) + "]"

    sql = text(
        "SELECT id, name, description, address, category_id, rating, price_level, image_urls, "
        "latitude, longitude "
        "FROM places "
        "WHERE embedding IS NOT NULL AND is_active = TRUE "
        "ORDER BY embedding <=> :embedding::vector "
        "LIMIT :top_k"
    )
    try:
        result = await db.execute(
            sql, {"embedding": embedding_str, "top_k": top_k}
        )
        rows = result.fetchall()
    except Exception as e:
        print(f"Vector search query failed: {e}")
        return []

    places = []
    for row in rows:
        place = Place(
            id=row[0],
            name=row[1],
            description=row[2],
            address=row[3],
            category_id=row[4],
            rating=row[5],
            price_level=row[6],
            image_urls=row[7],
            latitude=row[8],
            longitude=row[9],
        )
        places.append(place)
    return places
