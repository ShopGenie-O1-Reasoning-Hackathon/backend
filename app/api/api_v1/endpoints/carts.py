from typing import List
import uuid
from sqlalchemy.orm import Session, joinedload
from fastapi import APIRouter, Depends, HTTPException
from app.helpers.product_retrieve.multiple_product import retrieve_multiple_products_from_qdrant
from app.schemas.product import ProductSchema, CategoryRequestSchema, CategoryResponseSchema, ProductRetrieveResponseSchema, ProductRetrieveMultipleRequestSchema, ProductRetrieveMultipleResponseSchema, ProductSimilarMultipleResponseSchema
from app.helpers.product_retrieve.single_product import retrieve_single_product_from_qdrant, retrieve_similar_products
from app.helpers.product_retrieve.category import get_products_by_category
from app.db.models.cart import Cart as CartModel
from app.db.models.users import User as UserModel
from app.api import deps
from app.schemas.product import cart as retCart
router = APIRouter()
import random

####################################################
#  GET cartProducts with user_id
####################################################
@router.get("/{user_id}", response_model=retCart)
async def get_cart_products(user_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    try:
        db_cart = (
            db.query(UserModel)
            .options(joinedload(UserModel.favourites))
            .filter(UserModel.id == user_id)
            .first()
        )
        if not db_cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        cart = db_cart.favourites

        product_ids = [str(item.product_id) for item in cart]
        
        products = await retrieve_multiple_products_from_qdrant(product_ids)
        # return product_ids

        # print("Products: ", products)

        similar_products_set = set()  # To ensure no duplication

        for product_id in product_ids:
            similar_products = await retrieve_similar_products(product_id, limit=5)
            for product in similar_products:
                product_tuple = tuple((key, tuple(value) if isinstance(value, list) else value) for key, value in product.items())
                similar_products_set.add(product_tuple)  

        unique_similar_products = [dict(product) for product in similar_products_set]
        
        # Shuffle the list of unique similar products
        random.shuffle(unique_similar_products)
        
        return retCart(
            similars=[ProductSchema(**product) for product in unique_similar_products],
            products=products
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))