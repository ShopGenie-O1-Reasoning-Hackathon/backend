import uuid
from sqlalchemy import Column, String, ARRAY, TIMESTAMP, UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = 'products'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    link = Column(String, nullable=False)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    category = Column(String, nullable=False)
    company = Column(String, nullable=False)

    reviews = relationship('Review', back_populates='for_product')
