from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CategoryOut(BaseModel):
    id: int
    name: str
    icon: str
    description: str

    model_config = {"from_attributes": True}


class PlaceOut(BaseModel):
    id: int
    name: str
    description: str
    address: str
    category_id: int
    rating: float
    price_level: int
    image_urls: list[str]
    latitude: float | None = None
    longitude: float | None = None

    model_config = {"from_attributes": True}


class PlaceDetail(PlaceOut):
    place_metadata: dict = Field(default_factory=dict)
    category: CategoryOut | None = None

    model_config = {"from_attributes": True, "populate_by_name": True}


class PlaceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    address: str = Field(default="", max_length=500)
    latitude: float | None = None
    longitude: float | None = None
    category_id: int
    rating: float = Field(default=0.0, ge=0, le=5)
    price_level: int = Field(default=1, ge=0, le=5)
    image_urls: list[str] = Field(default_factory=list)
    place_metadata: dict = Field(default_factory=dict)


class PlaceFilter(BaseModel):
    category_id: int | None = None
    min_rating: float | None = None
    max_price: int | None = None
    search: str | None = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)
