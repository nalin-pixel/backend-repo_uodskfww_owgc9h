"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# Example schemas (you can keep these and add your own below)

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category, e.g. clothing or coffee")
    in_stock: bool = Field(True, description="Whether product is in stock")
    image: Optional[HttpUrl] = Field(None, description="Primary image URL")
    images: Optional[List[HttpUrl]] = Field(default=None, description="Additional image URLs")
    tags: Optional[List[str]] = Field(default=None, description="Searchable tags")
    brand: Optional[str] = Field(default=None, description="Brand name")
    size: Optional[str] = Field(default=None, description="Size for apparel")
    color: Optional[str] = Field(default=None, description="Color for apparel")
    weight_grams: Optional[int] = Field(default=None, description="Weight for coffee bags")
    roast_level: Optional[str] = Field(default=None, description="Roast level for coffee")

class Track(BaseModel):
    """
    Music tracks collection schema
    Collection name: "track"
    """
    title: str = Field(..., description="Track title")
    artist: str = Field(..., description="Artist name")
    cover: Optional[HttpUrl] = Field(None, description="Album art URL")
    audio_url: Optional[HttpUrl] = Field(None, description="Public streaming URL (mp3/wav)")
    external_url: Optional[HttpUrl] = Field(None, description="Link to Spotify/Apple/etc")
    genre: Optional[str] = Field(None, description="Genre")
    bpm: Optional[int] = Field(None, ge=0, description="Beats per minute")
    key: Optional[str] = Field(None, description="Musical key")
    description: Optional[str] = Field(None, description="Short description")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
