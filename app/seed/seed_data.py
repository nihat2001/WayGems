import asyncio
import numpy as np
from sqlalchemy import select
from app.database import AsyncSessionLocal, init_db
from app.models import Category, Place
from app.config import settings


def _random_embedding(text: str) -> list[float]:
    np.random.seed(hash(text) % (2**31))
    return np.random.uniform(-0.1, 0.1, settings.vector_dimension).tolist()


def _img(seed: str) -> list[str]:
    return [f"https://picsum.photos/seed/{seed}/800/600"]


BAKU_CATEGORIES = [
    {"name": "cafe", "icon": "☕", "description": "Cafes and coffee shops"},
    {"name": "restaurant", "icon": "🍽️", "description": "Restaurants and dining"},
    {"name": "historical", "icon": "🏛️", "description": "Historical landmarks and museums"},
    {"name": "park", "icon": "🌳", "description": "Parks and nature areas"},
    {"name": "hotel", "icon": "🏨", "description": "Hotels and accommodation"},
    {"name": "nightlife", "icon": "🌙", "description": "Bars, clubs, and entertainment"},
    {"name": "shopping", "icon": "🛍️", "description": "Malls, markets, and shops"},
    {"name": "beach", "icon": "🏖️", "description": "Beaches and seaside areas"},
]

BAKU_PLACES = [
    {"name": "İçərişəhər (Old City)", "description": "UNESCO World Heritage site, the ancient historic core of Baku with 12th-century walls, palaces, mosques, and caravanserais.", "address": "Old City, Baku", "latitude": 40.3666, "longitude": 49.8353, "category": "historical", "rating": 4.8, "price_level": 1, "image_urls": ["https://media-cdn.tripadvisor.com/media/photo-s/1a/a7/8e/8a/old-city-or-inner-city.jpg"]},
    {"name": "Maiden Tower (Qız Qalası)", "description": "Iconic 12th-century tower in Old City, symbol of Baku with panoramic views of the Caspian Sea.", "address": "Old City, Baku", "latitude": 40.3683, "longitude": 49.8372, "category": "historical", "rating": 4.7, "price_level": 2, "image_urls": ["https://media-cdn.tripadvisor.com/media/photo-s/14/9f/31/42/1-1a01b6fdcaad5afa679cb11142a3.jpg"]},
    {"name": "Palace of the Shirvanshahs", "description": "15th-century palace complex in Old City, a masterpiece of Azerbaijani architecture.", "address": "Old City, Baku", "latitude": 40.3661, "longitude": 49.8336, "category": "historical", "rating": 4.6, "price_level": 2, "image_urls": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTRdRJM-Fe3WV0PkoR3ZasKPk48aoqHNQa1iN_ECuJ0Eg&s=10"]},
    {"name": "Heydar Aliyev Center", "description": "Stunning modern architectural masterpiece designed by Zaha Hadid, hosting cultural exhibitions and events.", "address": "1 Heydar Aliyev Avenue, Baku", "latitude": 40.3953, "longitude": 49.8666, "category": "historical", "rating": 4.9, "price_level": 3, "image_urls": ["http://azerbaijan.travel/resize3000/center/pages/714/57fb3b7b-f01d-4184-9128-ac673f5f4aad.jpg"]},
    {"name": "Baku Boulevard (Dənizkənarı Bulvar)", "description": "Beautiful seaside promenade stretching along the Caspian Sea, perfect for walks and relaxation.", "address": "Neftchilar Avenue, Baku", "latitude": 40.3700, "longitude": 49.8450, "category": "park", "rating": 4.7, "price_level": 1, "image_urls": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ1Rt75gME7y0BNlyzvSGLZZ9FxytX58EShecFqpCPfsCUNiZ9jE7cobOkX&s=10"]},
    {"name": "Şirvanşah Müsəlləsi", "description": "Upscale restaurant serving traditional Azerbaijani cuisine in a historic setting with live music.", "address": "Old City, Baku", "latitude": 40.3670, "longitude": 49.8340, "category": "restaurant", "rating": 4.6, "price_level": 4, "image_urls": ["https://bakuguide.com/images/places/855/sirvanshah4.png"]},
    {"name": "Firuze Restaurant", "description": "Cozy restaurant in Old City with traditional Azerbaijani decor and excellent local cuisine.", "address": "Old City, Baku", "latitude": 40.3660, "longitude": 49.8360, "category": "restaurant", "rating": 4.5, "price_level": 3, "image_urls": ["https://dynamic-media-cdn.tripadvisor.com/media/photo-o/33/27/f1/1d/caption.jpg?w=1200&h=1200&s=1"]},
    {"name": "Pasifico Café", "description": "Beachfront café on Baku Boulevard with sea views, smoothies, and light bites.", "address": "Baku Boulevard, Baku", "latitude": 40.3690, "longitude": 49.8430, "category": "cafe", "rating": 4.5, "price_level": 2, "image_urls": ["https://media-cdn.tripadvisor.com/media/photo-m/1280/1a/50/db/fa/caption.jpg"]},
    {"name": "Four Seasons Hotel Baku", "description": "Luxury 5-star hotel located in the city center with sea views, spa, and fine dining.", "address": "1 Neftchilar Avenue, Baku", "latitude": 40.3695, "longitude": 49.8420, "category": "hotel", "rating": 4.9, "price_level": 5, "image_urls": ["https://content.r9cdn.net/rimg/himg/17/2f/96/leonardo-438421-516455-438427.jpg?width=1200&height=630&crop=true"]},
    {"name": "JW Marriott Absheron Baku", "description": "Premium business hotel with modern amenities, rooftop pool, and panoramic city views.", "address": "674 Azadliq Square, Baku", "latitude": 40.3730, "longitude": 49.8500, "category": "hotel", "rating": 4.7, "price_level": 5, "image_urls": ["https://www.cfmedia.vfmleonardo.com/imageRepo/7/0/160/883/681/gydjw-exterior-0022-ver-clsc_S.jpg"]},
    {"name": "Baku Palace Hotel", "description": "Boutique hotel in a restored historic building near the Old City gates.", "address": "Old City, Baku", "latitude": 40.3665, "longitude": 49.8365, "category": "hotel", "rating": 4.3, "price_level": 3, "image_urls": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTRcxw4Opn6S72OF0HCvN3K-2dv0TW0YnuVNlxd-gzZAVRk0wNiD_Naane1&s=10"]},
    {"name": "Upland Park (Dağüstü Parkı)", "description": "Hilltop park with panoramic views of Baku and the Caspian Sea, featuring the Flame Towers backdrop.", "address": "Baku", "latitude": 40.3675, "longitude": 49.8330, "category": "park", "rating": 4.8, "price_level": 1, "image_urls": ["https://itinari-images.s3.eu-west-1.amazonaws.com/activity/images/original/f01f2983-e26c-4390-81e1-08ecf0d503f5-istock-900392626.jpg"]},
    {"name": "Philharmonic Fountain Park", "description": "Elegant park with fountains, sculptures, and flower gardens next to the Philharmonic Hall.", "address": "Rashid Behbudov Street, Baku", "latitude": 40.3745, "longitude": 49.8390, "category": "park", "rating": 4.5, "price_level": 1, "image_urls": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdtUwxRxsZFBvQYKxyLhI6noKvfxUty7z6FA5Jcy48uOMxj-RMLj0rBJA&s=10"]},
    {"name": "Nizami Street (Torgovaya)", "description": "Main pedestrian shopping street with international brands, boutiques, cafes, and entertainment.", "address": "Nizami Street, Baku", "latitude": 40.3750, "longitude": 49.8450, "category": "shopping", "rating": 4.5, "price_level": 3, "image_urls": ["https://eurasia.travel/wp-content/uploads/2025/03/9.-Nizami-street-Baku.jpg"]},
    {"name": "Port Baku Mall", "description": "Modern shopping mall with luxury brands, cinema, food court, and entertainment zone.", "address": "Neftchilar Avenue, Baku", "latitude": 40.3710, "longitude": 49.8400, "category": "shopping", "rating": 4.4, "price_level": 4, "image_urls": ["https://pashamalls.az/resized/resize1000/center/pages/12/af9a1689-1.jpg"]},
    {"name": "Mardakan Beach", "description": "Clean beach with resort facilities, a popular weekend destination for Baku residents.", "address": "Mardakan, Baku", "latitude": 40.4920, "longitude": 50.1310, "category": "beach", "rating": 4.1, "price_level": 3, "image_urls": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTs9sF6SdFoyF9ayWvoqHd_Fe1eM5YsBjMDoUtUAKCS2HnZBzApYcNDbC63&s=10"]},
]


async def seed():
    await init_db()
    async with AsyncSessionLocal() as db:
        existing = await db.execute(select(Category).limit(1))
        if existing.scalar_one_or_none():
            print("Database already seeded.")
            return

        cat_map = {}
        for cat in BAKU_CATEGORIES:
            category = Category(**cat)
            db.add(category)
            await db.flush()
            cat_map[cat["name"]] = category.id

        for p in BAKU_PLACES:
            cat_name = p.pop("category")
            p["category_id"] = cat_map[cat_name]
            place = Place(**p)
            text_for_embedding = f"{place.name} {place.description} {place.address}"
            place.embedding = _random_embedding(text_for_embedding)
            db.add(place)

        await db.commit()
        print(f"Seeded {len(BAKU_CATEGORIES)} categories and {len(BAKU_PLACES)} places.")


if __name__ == "__main__":
    asyncio.run(seed())
