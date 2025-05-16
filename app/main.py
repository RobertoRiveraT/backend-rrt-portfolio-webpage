# app/main.py

from fastapi import FastAPI
from app import models, database

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Chatbot Arelia API is up and running!"}

# 👇 Esta línea crea las tablas en la base de datos (solo la necesitas una vez).
models.Base.metadata.create_all(bind=database.engine)
