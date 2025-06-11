# This file defines the data validation schemas (Pydantic models)
# used by FastAPI to validate incoming requests and structure responses.
# It declares user and message models for creating, receiving, and returning data.

from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

# -------- USERS --------

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # Enables compatibility with ORM objects (Pydantic v2+)
    model_config = ConfigDict(from_attributes=True)

# -------- AUTH --------

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

# -------- MESSAGES --------

class MessageCreate(BaseModel):
    content: str

class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    timestamp: datetime

    # Enables compatibility with ORM objects (Pydantic v2+)
    model_config = ConfigDict(from_attributes=True)
