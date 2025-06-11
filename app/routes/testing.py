from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Message
import os
from pydantic import BaseModel

router = APIRouter()

class DeleteRequest(BaseModel):
    email: str

@router.post("/force-delete-user")
def force_delete_user(payload: DeleteRequest, db: Session = Depends(get_db)):
    """
    Deletes a user and all associated messages by email.
    Only allowed when ENV=test to protect production data.
    """
    if os.getenv("ENV") != "test":
        raise HTTPException(status_code=403, detail="Access denied in non-test environments.")

    user = db.query(User).filter(User.email == payload.email).first()
    if user:
        db.query(Message).filter(Message.user_id == user.id).delete()
        db.delete(user)
        db.commit()
        return {"message": f"User '{payload.email}' deleted."}
    else:
        return {"message": "User not found."}