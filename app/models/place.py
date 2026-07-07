from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.database import Base
from app.config import settings


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(String(2000), default="")
    address = Column(String(500), default="")
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    rating = Column(Float, default=0.0)
    price_level = Column(Integer, default=1)
    image_urls = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)
    place_metadata = Column(JSON, default=dict)
    embedding = Column(Vector(settings.vector_dimension), nullable=True)

    category = relationship("Category", backref="places", lazy="selectin")
