from typing import Dict, List
import uuid
from app.core.config import settings

from app.core.qdrant import qdrantClient as qdrantClient_ShopGenie

async def retrieve_multiple_products_from_qdrant(product_ids: List[str]) -> List[dict]:
    items = qdrantClient_ShopGenie.retrieve(
        collection_name=settings.QDRANT_COLLECTION_SHOPGENIE,
        ids=product_ids
    )
    
    products = []
    for item in items:
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
        
        products.append(normalized_product_data)
    
    return products