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
from app.db.models.products import Product as ProductModel
from app.db.models.clicks import Click as ClickModel
from app.api import deps
from app.schemas.product import cart as retCart, insertClick
router = APIRouter()
import random

####################################################
#  Insert Click for a product
####################################################
def insert_click(click: insertClick, db: Session = Depends(deps.get_db)):
    """
    Insert a click record for a product by a user.
    Ensures that each (product_id, user_id) pair is unique.
    If the pair already exists, the function does nothing and returns a success message.
    """

    # Validate and convert UUIDs
    try:
        product_uuid = uuid.UUID(click.productId)
        user_uuid = uuid.UUID(click.userId)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format for productId or userId."
        )
    
    # Optional: Verify that the product exists
    product = db.query(ProductModel).filter(ProductModel.id == product_uuid).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )
    
    # Check if the (product_id, user_id) pair already exists
    existing_click = db.query(ClickModel).filter(
        ClickModel.product_id == product_uuid,
        ClickModel.user_id == user_uuid
    ).first()
    
    if existing_click:
        # Pair already exists; do not insert a duplicate
        return {"message": "Click already recorded."}
    
    # Create a new Click record
    new_click = ClickModel(
        product_id=product_uuid,
        user_id=user_uuid
    )
    
    db.add(new_click)
    try:
        db.commit()
        db.refresh(new_click)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while recording the click."
        )
    
    return {"message": "Click recorded successfully."}


