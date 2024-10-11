import uuid
from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, UUID, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Click(Base):
    __tablename__ = 'click_info'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)

    click_records = relationship('Product', back_populates='clicks')
