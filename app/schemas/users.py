import uuid
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class UserCreate(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    
class UserUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    occupation: Optional[str] = None

    
class User(BaseModel):
    id: uuid.UUID
    name: str
    address: str
    country: str
    occupation: str
    email: str