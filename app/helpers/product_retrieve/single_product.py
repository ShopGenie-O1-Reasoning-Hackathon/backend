from typing import Dict, List
import uuid
from app.core.config import settings

from app.core.qdrant import qdrantClient as qdrantClient_ShopGenie

async def retrieve_single_product_from_qdrant(product_id: uuid.UUID) -> dict:
    items = qdrantClient_ShopGenie.retrieve(
        collection_name=settings.QDRANT_COLLECTION_SHOPGENIE,
        ids=[str(product_id)]
    )
    if not items:
        return None
    
    item = items[0]
    product_data = item.payload
    
    # Normalize the keys to match the expected field names in the Product model
    normalized_product_data = {
        'product_id': str(item.id),
        'link': product_data.get('Link', ''),
        'name': product_data.get('Name', ''),
        'description': product_data.get('Description', ''),
        'price': product_data.get('Price', '0'),
        'specifications': product_data.get('Specifications', ''),
        'image_links': product_data.get('Image_links', []),
        'gender': product_data.get('Gender', ''),
        'category': product_data.get('Category', ''),
        'company': product_data.get('Company', ''),
    }
    
    return normalized_product_data

async def retrieve_similar_products(product_id: uuid.UUID, limit: int = 5) -> List[dict]:
    recommendations = qdrantClient_ShopGenie.recommend(
        collection_name=settings.QDRANT_COLLECTION_SHOPGENIE,
        positive=[str(product_id)],
        using="summary",
        strategy="best_score",
        limit=limit,
        with_payload=True
    )
    
    similar_products = []
    for item in recommendations:
        product_data = item.payload
        normalized_product_data = {
            'product_id': str(item.id),
            'link': product_data.get('Link', ''),
            'name': product_data.get('Name', ''),
            'description': product_data.get('Description', ''),
            'price': product_data.get('Price', '0'),
            'specifications': product_data.get('Specifications', ''),
            'image_links': product_data.get('Image_links', []),
            'gender': product_data.get('Gender', ''),
            'category': product_data.get('Category', ''),
            'company': product_data.get('Company', ''),
        }
        similar_products.append(normalized_product_data)
    
    return similar_products


    