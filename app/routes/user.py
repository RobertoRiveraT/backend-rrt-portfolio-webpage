from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models
from app.database import get_db
from app.models import User
from app.routes.auth import get_current_user
from passlib.context import CryptContext
from pydantic import BaseModel

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class EmailUpdate(BaseModel):
    new_email: str

@router.put("/update-email")
def update_email(
    payload: EmailUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_email = payload.new_email

    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.email = new_email  # type: ignore
    db.commit()
    return {"message": "Correo actualizado correctamente."}

class PasswordUpdate(BaseModel):
    new_password: str

@router.put("/update-password")
def update_password(
    payload: PasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_password = payload.new_password

    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.hashed_password = pwd_context.hash(new_password)  # type: ignore
    db.commit()
    return {"message": "Contraseña actualizada correctamente."}


@router.delete("/delete-account")
def delete_account(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Eliminar mensajes del usuario
    db.query(models.Message).filter(models.Message.user_id == current_user.id).delete()

    # Luego eliminar usuario
    db.delete(user)
    db.commit()

    return {"message": "The account was successfully deleted."}