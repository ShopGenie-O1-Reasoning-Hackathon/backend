from app.core.openai import openaiClient
from typing import List
from fastapi import HTTPException
from app.core.qdrant import qdrantClient as qdrantClient_ShopGenie
from app.core.openai import openaiClient
from app.helpers.embedding_generate import get_text_embedding
from app.schemas.product import ProductSchema
from app.core.config import settings

def get_search_products_from_text(query: str) -> List[ProductSchema]:
    embedding = get_text_embedding(query)
    
    try:
        search_result = qdrantClient_ShopGenie.search(
            collection_name=settings.QDRANT_COLLECTION_SHOPGENIE, 
            query_vector={
                "name": "summary",
                "vector": embedding
            },
            limit=15,
            with_payload=True,
            with_vectors=False
        )

        
        products = [
            ProductSchema(
                product_id=str(point.id),
                link=point.payload.get("Link", ""),
                name=point.payload.get("Name", ""),
                description=point.payload.get("Description", ""),
                price=point.payload.get("Price", "0"),
                specifications=point.payload.get("Specifications", ""),
                image_links=point.payload.get("Image_links", []),
                gender=point.payload.get("Gender", ""),
                category=point.payload.get("Category", ""),
                company=point.payload.get("Company", "")
            )
            for point in search_result
        ]
        
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching products: {str(e)}")


