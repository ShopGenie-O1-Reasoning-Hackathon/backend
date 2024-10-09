from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID

class CategoryRequestSchema(BaseModel):
    category: str
    sub_category: str
    limit: int = Field(gt=0, description="Number of items to return")
    offset: Optional[UUID] = Field(None, description="Offset for pagination (optional, UUID)")

class ProductSchema(BaseModel):
    product_id: str
    link: str
    name: str
    description: str
    price: str
    specifications: str
    image_links: List[str]
    gender: str
    category: str
    company: str

class ProductRetrieveResponseSchema(BaseModel):
    product: ProductSchema
    similar_products: List[ProductSchema]

class CategoryResponseSchema(BaseModel):
    products: List[ProductSchema]
    next_offset: str

class ProductRetrieveMultipleRequestSchema(BaseModel):
    product_ids: List[str] 

class ProductRetrieveMultipleResponseSchema(BaseModel):
    products: List[ProductSchema]

class ProductSimilarMultipleResponseSchema(BaseModel):
    products: List[ProductSchema]
