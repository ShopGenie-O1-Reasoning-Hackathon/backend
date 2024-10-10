import uuid
from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Cart(Base):
    __tablename__ = 'cartinfo'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    product_id = Column(UUID(as_uuid=True), nullable=True)

    uploader = relationship('User', back_populates='favourites')
