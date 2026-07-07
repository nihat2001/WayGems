from sqlalchemy import Column, String, Integer, Text
from pgvector.sqlalchemy import Vector
from pydantic import BaseModel, Field
from typing import Optional
from database import Base

class FreewareApp(Base):
    __tablename__ = "freeware_apps"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)          
    category = Column(String, nullable=False, index=True)      
    replaces = Column(String, nullable=False, index=True)      
    description = Column(Text, nullable=False)                 
    github_url = Column(String, nullable=True)                 
    description_vector = Column(Vector(768), nullable=True)

class AppCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, description="Name of the open-source alternative")
    category: str = Field(..., description="Software category or domain")
    replaces: str = Field(..., description="The paid software it replaces")
    description: str = Field(..., min_length=10, description="Brief description of features")
    github_url: Optional[str] = Field(None, description="URL to the source code repository")

class AppResponseSchema(AppCreateSchema):
    id: int

    class Config:
        from_attributes = True