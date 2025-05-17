# Este archivo configura la conexión entre la aplicación FastAPI y la base de datos PostgreSQL
# usando SQLAlchemy. Define un motor, una sesión de base de datos y una función para inicializar
# las tablas al arrancar el proyecto. Esta conexión es reutilizada por todos los módulos del backend.

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

print("URL from .env:", os.getenv("DATABASE_URL"))

# Carga las variables del archivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Motor de conexión con PostgreSQL
engine = create_engine(DATABASE_URL) # type: ignore

# Sesión para interactuar con la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Dependencia para usar en rutas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
