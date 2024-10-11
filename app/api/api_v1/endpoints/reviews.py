from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
import uuid

from app.db.models.reviews import Review as ReviewModel
from app.db.models.users import User as UserModel
from app.db.models.products import Product as ProductModel
from app.api import deps
from app.schemas.reviews import ReviewCreateRequestSchema, ReviewResponseSchema

router = APIRouter()

@router.get("/get-reviews/{product_id}", response_model=List[ReviewResponseSchema])
async def get_reviews_by_product(product_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    try:
        # Fetch the product to ensure it exists
        product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Fetch all reviews for the given product_id
        reviews = (
            db.query(ReviewModel)
            .filter(ReviewModel.product_id == product_id)
            .all()
        )

        if not reviews:
            return []  

        response = []
        for review in reviews:
            # Get the user details for each review
            user = db.query(UserModel).filter(UserModel.id == review.user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found for review")

            # Append each review with user_name to the response
            response.append(ReviewResponseSchema(
                id=review.id,
                user_name=user.name,
                user_comment=review.user_comment,
                review_sentiment=review.review_sentiment,
                created_at=review.created_at
            ))

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    

@router.post("/add", response_model=ReviewResponseSchema, status_code=status.HTTP_201_CREATED)
async def add_review(review_data: ReviewCreateRequestSchema, db: Session = Depends(deps.get_db)):
    try:
        # Check if the user exists
        user = db.query(UserModel).filter(UserModel.id == review_data.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if the product exists
        product = db.query(ProductModel).filter(ProductModel.id == review_data.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Create the new review entry
        new_review = ReviewModel(
            user_id=review_data.user_id,
            product_id=review_data.product_id,
            user_comment=review_data.user_comment,
            review_sentiment=review_data.review_sentiment,
        )

        # Add the review to the database
        db.add(new_review)
        db.commit()
        db.refresh(new_review)

        # Return the newly added review in the expected format
        return ReviewResponseSchema(
            id=new_review.id,
            user_name=user.name,
            user_comment=new_review.user_comment,
            review_sentiment=new_review.review_sentiment,
            created_at=new_review.created_at
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
