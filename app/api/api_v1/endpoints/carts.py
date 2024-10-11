from typing import List
import uuid
from sqlalchemy.orm import Session, joinedload
from fastapi import APIRouter, Depends, HTTPException,status
from app.helpers.product_retrieve.multiple_product import retrieve_multiple_products_from_qdrant
from app.schemas.product import CartRemoveRequestSchema, ProductSchema, CategoryRequestSchema, CategoryResponseSchema, ProductRetrieveResponseSchema, ProductRetrieveMultipleRequestSchema, ProductRetrieveMultipleResponseSchema, ProductSimilarMultipleResponseSchema
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
            similar_products = await retrieve_similar_products(product_id, limit=10)
            for product in similar_products:
                if product["product_id"] in product_ids:
                    continue
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
    

####################################################
#  REMOVE cartProducts with user_id, Cart_id
####################################################
@router.post("/remove", status_code=status.HTTP_204_NO_CONTENT)
async def remove_cart_product(cart_remove_data: CartRemoveRequestSchema, db: Session = Depends(deps.get_db)):
    try:
       
        db_cart = (
            db.query(CartModel)
            .filter(CartModel.user_id == uuid.UUID(cart_remove_data.userId))
            .filter(CartModel.product_id == uuid.UUID(cart_remove_data.productId))
            .first()
        )

        if not db_cart:
            raise HTTPException(status_code=404, detail="Cart entry not found")

        # Delete the cart entry
        db.delete(db_cart)
        db.commit()

        return {"detail": "Cart entry successfully removed"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    
@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_cart_product(cart_add_data: CartRemoveRequestSchema, db: Session = Depends(deps.get_db)):
    try:
        
        existing_cart = (
            db.query(CartModel)
            .filter(CartModel.user_id == uuid.UUID(cart_add_data.userId))
            .filter(CartModel.product_id == uuid.UUID(cart_add_data.productId))
            .first()
        )

        if existing_cart:
            raise HTTPException(status_code=400, detail="Product already in cart")

        # Create a new Cart entry
        new_cart = CartModel(
            user_id=uuid.UUID(cart_add_data.userId),
            product_id=uuid.UUID(cart_add_data.productId)
        )

        # Add the new cart entry to the session and commit
        db.add(new_cart)
        db.commit()
        db.refresh(new_cart)

        return {"detail": "Product successfully added to cart", "cart_id": str(new_cart.id)}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))


@router.post("/check", status_code=status.HTTP_200_OK)
async def check_cart_product(cart_check_data: CartRemoveRequestSchema, db: Session = Depends(deps.get_db)):
    try:
        # Check if the Cart entry exists for the user and product
        existing_cart = (
            db.query(CartModel)
            .filter(CartModel.user_id == uuid.UUID(cart_check_data.userId))
            .filter(CartModel.product_id == uuid.UUID(cart_check_data.productId))
            .first()
        )

        return {"isInCart": bool(existing_cart)}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))