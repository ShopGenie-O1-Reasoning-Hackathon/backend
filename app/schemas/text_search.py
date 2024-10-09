from pydantic import BaseModel
from typing import List, Optional
from .product import ProductSchema

class ProductQuerySchema(BaseModel):
    query: str

class ImageLink(BaseModel):
    image_link: str

class ProductListResponse(BaseModel):
    products: List[ProductSchema]

class HybridSearchRequest(BaseModel):
    text_query: str
    image_link: str