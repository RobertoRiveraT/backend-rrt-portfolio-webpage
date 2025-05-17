# Este archivo define los esquemas de validación de datos (Pydantic models)
# utilizados por FastAPI para validar las solicitudes entrantes y estructurar las respuestas.
# Aquí se declaran los modelos de usuario y mensaje tanto para crear, recibir, y retornar datos.

from pydantic import BaseModel, EmailStr
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

    class Config:
        orm_mode = True

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

    class Config:
        orm_mode = True
