# Este archivo contiene la lógica del endpoint /chat.
# Recibe un mensaje del usuario autenticado, guarda el mensaje en la base de datos,
# llama a la API de OpenAI (ChatGPT) y devuelve una respuesta.
# También guarda la respuesta del bot como mensaje con rol "assistant".

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from datetime import datetime
import openai
import os

from app.routes import auth

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

    # 2. Llamar a la API de OpenAI (GPT-3.5)
    try:
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message.content}
            ]
        )
        raw_response = completion.choices[0].message.content
        if raw_response is None:
            raise HTTPException(status_code=500, detail="OpenAI returned an empty response.")

        bot_response = raw_response.strip()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")

    # 3. Guardar respuesta del bot
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
