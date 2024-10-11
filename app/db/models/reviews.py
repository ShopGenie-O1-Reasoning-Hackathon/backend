import uuid
from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, UUID, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    user_comment = Column(String, nullable=True)
    review_sentiment = Column(String, nullable=True)

    created_at = Column(DateTime, server_default=func.now())

    for_product = relationship('Product', back_populates='reviews')
