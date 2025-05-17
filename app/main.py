# Este es el punto de entrada principal de la aplicación FastAPI.
# Aquí se inicializa la app, se incluyen los routers de autenticación y chat,
# y se realiza la conexión inicial con la base de datos si es necesario.

from fastapi import FastAPI
from app import models, database
from app.auth import router as auth_router
from app.chat import router as chat_router

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Chatbot Arelia API",
    description="Backend API for chatbot with authentication and OpenAI integration.",
    version="1.0"
)

# Incluir rutas de diferentes módulos
app.include_router(auth_router)
app.include_router(chat_router)

@app.get("/")
def root():
    return {"message": "Chatbot Arelia API is up and running!"}

# 👇 Esta línea crea las tablas en la base de datos (solo la necesitas una vez).
## models.Base.metadata.create_all(bind=database.engine)