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

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Example schemas (replace with your own):

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
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Add your own schemas here:
# --------------------------------------------------

class Lead(BaseModel):
    """Leads from demo/contact form
    Collection name: "lead"
    """
    name: str = Field(..., min_length=2, description="Full name")
    email: EmailStr = Field(..., description="Work email")
    company: Optional[str] = Field(None, description="Company name")
    role: Optional[str] = Field(None, description="Role or title")
    message: Optional[str] = Field(None, description="Additional context")
    source: Optional[str] = Field("website", description="Acquisition source")

class Module(BaseModel):
    """Training modules metadata
    Collection name: "module"
    """
    title: str = Field(..., description="Module title")
    slug: str = Field(..., description="Unique slug for the module")
    audience: str = Field(..., description="Target audience e.g. Sales, Marketing")
    level: str = Field("Débutant", description="Difficulty level")
    duration_min: int = Field(..., ge=5, le=240, description="Estimated duration in minutes")
    tags: List[str] = Field(default_factory=list, description="Keywords")
    summary: str = Field(..., description="Short description")
    cover: Optional[str] = Field(None, description="Cover image URL")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
