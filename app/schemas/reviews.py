from pydantic import BaseModel
from datetime import datetime
import uuid

class ReviewResponseSchema(BaseModel):
    id: uuid.UUID
    user_name: str
    user_comment: str
    review_sentiment: str
    created_at: datetime

class ReviewCreateRequestSchema(BaseModel):
    user_id: uuid.UUID
    product_id: uuid.UUID
    user_comment: str
    review_sentiment: str