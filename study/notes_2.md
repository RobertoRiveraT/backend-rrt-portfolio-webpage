# 📘 study/notes_2.md — Conexión a Railway, despliegue backend y solución de errores

## ✅ Resumen de logros

- Se conectó correctamente el backend FastAPI a una base de datos PostgreSQL en Railway.
- Se verificó que las tablas `users` y `messages` se crearon correctamente.
- Se preparó y subió el proyecto a GitHub.
- Se desplegó el backend en Railway y se solucionaron errores relacionados con entornos virtuales y Docker.
- Se configuró `railway.json` para tener control total del build y start.

---

## ⚙️ Estructura actual del backend

- `app/models.py`: define tablas `User` y `Message`
- `app/database.py`: conexión con PostgreSQL usando SQLAlchemy
- `.env`: contiene `DATABASE_URL`, `SECRET_KEY`, etc.
- `railway.json`: archivo de configuración para el deploy

---

## ⚠️ Problemas encontrados y soluciones

### 🟥 Error: `invalid literal for int() with base 10: 'port'`

**Causa:** Se estaba usando `postgres.railway.internal` desde local, lo cual no es accesible fuera de Railway.

**Solución:** Cambiar a la **URL pública de conexión** que comienza con `shuttle.proxy.rlwy.net:PUERTO`, encontrada en la pestaña de variables o connect del servicio PostgreSQL.

---

### 🟥 Error: `Text file busy: '/opt/venv/bin/python'`  
Durante el deploy en Railway.

**Causa:** Railway intentaba crear un entorno virtual (`python -m venv`) dentro de un contenedor que ya tiene uno. Esto sucedía porque Railway estaba usando un `Dockerfile` (invisible o recordado).

**Solución:**
- Confirmamos que no había `Dockerfile` ni `.dockerignore`.
- Eliminamos el servicio backend de Railway (sin borrar el proyecto ni la base de datos).
- Creamos un **nuevo servicio limpio** conectado a GitHub.
- Usamos `railway.json` para forzar el comportamiento correcto:

```json
{
  "build": {
    "buildCommand": "pip install -r requirements.txt",
    "startCommand": "uvicorn app.main:app --host=0.0.0.0 --port=8000"
  }
}
```

---

### 🟢 Confirmación final

- La API responde correctamente desde su URL pública de Railway.
- Las tablas fueron creadas y accedidas desde local y desde el backend desplegado.
- Entorno controlado y documentación iniciada.

---

## 📌 Siguientes pasos sugeridos

- Crear `auth.py` para manejar registro, login y JWT
- Validar tokens y proteger endpoints (`/messages`, `/chat`)
- Crear pruebas automáticas (`pytest`)
- Conectar el frontend Angular