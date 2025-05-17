# 📃 chatbot\_arelia - Estudio Backend (FastAPI + PostgreSQL)

Este documento resume todo el proceso de desarrollo backend del proyecto **chatbot\_arelia**, con el objetivo de servir como referencia futura para entrevistas, estudio y mantenimiento del proyecto.

---

## 🌐 Stack elegido

* **Framework backend:** FastAPI (Python)
* **Base de datos:** PostgreSQL (Railway)
* **ORM:** SQLAlchemy
* **Autenticación:** JWT (via python-jose)
* **Variables de entorno:** python-dotenv
* **Testing:** pytest (local), Postman (externo)

---

## 🚀 Proceso de configuración

### 1. Estructura del proyecto

```
chatbot_arelia-backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── auth.py
│   ├── chat.py
├── tests/
│   ├── test_auth.py
│   ├── test_chat.py
├── .env
├── requirements.txt
└── README.md
```

### 2. Instalación de dependencias

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose[cryptography] passlib[bcrypt] pydantic python-dotenv pytest
```

Contenido de `requirements.txt`:

```
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-jose[cryptography]
passlib[bcrypt]
pydantic
python-dotenv
pytest
```

### 3. Configuración de `.env`

```env
DATABASE_URL=postgresql://<user>:<password>@shuttle.proxy.rlwy.net:<puerto>/railway
SECRET_KEY=<clave secreta generada>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> NOTA: En desarrollo local, se debe usar la URL con `shuttle.proxy.rlwy.net`. La URL con `postgres.railway.internal` solo funciona dentro de Railway.

### 4. Conexión a PostgreSQL (`database.py`)

* Se utiliza SQLAlchemy para crear el motor de conexión.
* Se define `Base`, `SessionLocal`, y `get_db()` como dependencia para rutas.

### 5. Creación de modelos (`models.py`)

* `User`: id, email, hashed\_password, created\_at
* `Message`: id, user\_id, role, content, timestamp
* Relación uno a muchos entre `User` y `Message`

### 6. Creación de esquemas (`schemas.py`)

* `UserCreate`, `UserOut` para usuarios
* `Token`, `TokenData` para autenticación JWT
* `MessageCreate`, `MessageOut` para mensajes

### 7. Creación de tablas

* Se incluye temporalmente esta línea en `main.py`:

```python
models.Base.metadata.create_all(bind=database.engine)
```

* Luego se elimina para evitar conflictos futuros.

---

## 🔧 Infraestructura

* **Base de datos PostgreSQL** creada y alojada en Railway
* **Conexión local** desde FastAPI usando `shuttle.proxy.rlwy.net` y el puerto asignado (no 5432)
* **Railway manejará automáticamente la URL interna (`postgres.railway.internal`) al hacer deploy**

---

## 🌟 Decisiones importantes

* Separación de frontend y backend en **repositorios distintos**
* **Backend en Railway**, **Frontend en Vercel** (Angular)
* El proyecto debe servir tanto para entrevistas como para estudio personal
* Cada archivo del backend incluye comentario explicativo sobre su propósito
* La carpeta `/study` se usará para documentar todo el flujo y servir como referencia viva

---

Próximos pasos:

* Implementar autenticación JWT en `auth.py`
* Crear endpoints `/register`, `/login`, `/chat`, `/messages`
* Agregar integración con la API de OpenAI
* Agregar pruebas unitarias con `pytest`
* Preparar despliegue en Railway (backend) y Vercel (frontend)
