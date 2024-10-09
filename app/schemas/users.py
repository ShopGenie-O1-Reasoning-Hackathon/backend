import uuid
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class UserCreate(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    gender: str
    
class UserUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    city: Optional[str] = None
    occupation: Optional[str] = None

    
class User(BaseModel):
    id: uuid.UUID
    name: str
    gender: str
    city: str
    occupation: str
    email: str