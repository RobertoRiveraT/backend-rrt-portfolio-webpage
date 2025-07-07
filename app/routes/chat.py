# Este archivo contiene la lógica del endpoint /chat.
# Recibe un mensaje del usuario autenticado, guarda el mensaje en la base de datos,
# llama a la API de OpenAI (ChatGPT) y devuelve una respuesta.
# También guarda la respuesta del bot como mensaje con rol "assistant".

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from datetime import datetime
from pydantic import BaseModel
from typing import cast
import openai
import os

from app.routes import auth
from app.utils.chat.text_processor import TextProcessor
from app.utils.chat.short_term_memory import get_short_term_memory
# No hace falta cache aún: personalidad solo se carga una vez por request

router = APIRouter()

# Cargar clave de API desde .env
openai.api_key = os.environ["OPENIA_SECRET"]

@router.post("/chat", response_model=schemas.MessageOut)
def chat(message: schemas.MessageCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)):

    # 1. Guardar mensaje del usuario
    user_msg = models.Message(
        user_id=current_user.id,
        role="user",
        content=message.content,
        timestamp=datetime.utcnow()
    )
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    # 2. Preparar prompt para OpenAI
    try:
        system_prompt = TextProcessor.load_personality(character="arelia", mode="default")
        user_id = cast(int, current_user.id)
        history = get_short_term_memory(db, user_id, limit=10)
        user_prompt = TextProcessor.format_history(history) + f"\n\nAhora el usuario dice:\n{message.content}"

        # 3. Llamar a la API
        bot_response = call_openai(system_prompt, user_prompt)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")

    # 4. Guardar respuesta del bot
    bot_msg = models.Message(
        user_id=current_user.id,
        role="assistant",
        content=bot_response,
        timestamp=datetime.utcnow()
    )
    db.add(bot_msg)
    db.commit()
    db.refresh(bot_msg)

    return bot_msg

def call_openai(system_prompt: str, user_prompt: str) -> str:
    debug_prompt(system_prompt, user_prompt)

    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=150
    )

    raw = completion.choices[0].message.content
    return TextProcessor.clean_output(str(raw))

def debug_prompt(system_prompt: str, user_prompt: str):
    print("\n🧠 Prompt enviado a OpenAI:")
    print("──────────────────────────────────────────────")
    print("[SYSTEM] ", system_prompt.strip()[:800])
    print("──────────────────────────────────────────────")
    print("[USER]   ", user_prompt.strip()[:800])
    print("──────────────────────────────────────────────")

@router.get("/chat-history", response_model=list[schemas.MessageOut])
def get_chat_history(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    history = (
        db.query(models.Message)
        .filter(models.Message.user_id == current_user.id)
        .order_by(models.Message.timestamp.asc())
        .all()
    )
    return history