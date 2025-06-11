# Este es el punto de entrada principal de la aplicación FastAPI.
# Aquí se inicializa la app, se incluyen los routers de autenticación y chat,
# y se realiza la conexión inicial con la base de datos si es necesario.

from fastapi import FastAPI
from app import models, database
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router
from app.routes.chat import router as chat_router
from app.routes.user import router as user_router

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Chatbot Arelia API",
    description="Backend API for chatbot with authentication and OpenAI integration.",
    version="1.0"
)

origins = [
    "http://localhost:4200",
    "https://chatbot-arelia-frontend.vercel.app",
    "https://github.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 👈 aquí defines qué frontend(s) están permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas de diferentes módulos
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "Chatbot Arelia API is up and running!"}

# 👇 Esta línea crea las tablas en la base de datos (solo la necesitas una vez).
## models.Base.metadata.create_all(bind=database.engine)