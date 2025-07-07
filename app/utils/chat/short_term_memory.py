# shot_term_memory.py
from sqlalchemy.orm import Session
from app import models

def get_short_term_memory(db: Session, user_id: int, limit: int = 5) -> list[dict]:
    """
    Devuelve el historial reciente de mensajes del usuario como lista para usar con OpenAI.
    """
    history = (
        db.query(models.Message)
        .filter(models.Message.user_id == user_id)
        .order_by(models.Message.timestamp.desc())
        .limit(limit)
        .all()
    )
    history.reverse()
    return [{"role": msg.role, "content": msg.content} for msg in history]
