import uuid
from sqlalchemy import Column, String, ARRAY, TIMESTAMP, UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=True, default='N/A')
    city = Column(String, nullable=True, default='N/A')
    occupation = Column(String, nullable=True, default='N/A')
    email = Column(String, nullable=False, unique=True)

    favourites = relationship('Cart', back_populates='uploader')

