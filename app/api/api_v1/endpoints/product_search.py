from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from app.helpers.product_fetch.description_generate import generate_product_description
from app.helpers.product_fetch.text import get_search_products_from_text
from app.helpers.product_fetch.image import get_search_products_from_image
router = APIRouter()
from app.schemas.text_search import ImageLink, ProductQuerySchema, ProductListResponse, HybridSearchRequest
from app.schemas.text_search import ProductSchema


#################################################################################################
#   search with image only
#################################################################################################
@router.post("/image-search", response_model=ProductListResponse)
async def search_products_image(image: ImageLink):
    # Extract the image link from the request body
    image_link = image.image_link
    products = get_search_products_from_image(image_link)
    return ProductListResponse(products=products)


#################################################################################################
#   search with Text only
#################################################################################################

@router.post("/text-search", response_model=ProductListResponse)
async def search_products_text(query: ProductQuerySchema):
    products = get_search_products_from_text(query.query)
    return ProductListResponse(products=products)

#################################################################################################
#   Hybrid Search
#################################################################################################
@router.post("/hybrid-search", response_model=ProductListResponse)
async def search_products_text(query: HybridSearchRequest):
    description = generate_product_description(query.image_link,query.text_query)
    products = get_search_products_from_text(description)
    return ProductListResponse(products=products)