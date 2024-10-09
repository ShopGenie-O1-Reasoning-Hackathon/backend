from typing import List, Optional
from app.core.qdrant import qdrantClient as qdrantClient_ShopGenie
from app.core.config import settings
from qdrant_client.http import models
from uuid import UUID

async def get_products_by_category(
    category: str, 
    granular_categories: List[str], 
    limit: int, 
    offset: Optional[UUID]
) -> dict:

    filter_query = models.Filter(
        must=[
            models.FieldCondition(
                key="Category",
                match=models.MatchAny(any=granular_categories)
            )
        ]
    )
    
    result = qdrantClient_ShopGenie.scroll(
        collection_name=settings.QDRANT_COLLECTION_SHOPGENIE, 
        scroll_filter=filter_query,
        limit=limit,
        with_payload=True,
        with_vectors=False,
        offset=str(offset) if offset else None
    )

    points, next_offset = result
    # print(points)
    
    products = [
        {
            "product_id": str(point.id),
            "link": point.payload.get("Link"),
            "name": point.payload.get("Name"),
            "description": point.payload.get("Description"),
            "price": point.payload.get("Price", '0'),
            "specifications": point.payload.get("Specifications"),
            "image_links": point.payload.get("Image_links", []),
            "gender": point.payload.get("Gender"),
            "category": point.payload.get("Category"),
            "company": point.payload.get("Company"),
        }
        for point in points
    ]
    
    return {
        "products": products,
        "next_offset": next_offset
    }
