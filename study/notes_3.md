# 🧠 Relación entre FastAPI, SQLAlchemy y PostgreSQL

Este documento explica claramente el rol de **FastAPI**, **SQLAlchemy** y **PostgreSQL** dentro del backend de la app `chatbot_arelia`, para comprender cómo trabajan juntos.

---

## ✅ 1. FastAPI  
> 🧰 "La oficina donde trabajas como desarrollador backend"

- Es el **framework** que permite construir una **aplicación web/API RESTful**.
- Define las **rutas** (`/register`, `/chat`, etc.), valida datos, maneja respuestas y errores.
- También se encarga de correr la app con `uvicorn`.

📌 **Archivo clave:** `main.py`  
📌 **FastAPI no sabe nada de bases de datos directamente.**

---

## ✅ 2. SQLAlchemy  
> 🔌 "El traductor que conecta la app con la base de datos"

- Es un **ORM** (Object Relational Mapper).
- Permite definir las **tablas como clases de Python** (`User`, `Message`).
- También proporciona una **sesión (`Session`) para interactuar con la base**:
  - Insertar usuarios
  - Leer mensajes
  - Hacer commits, updates, deletes, etc.

📌 **Archivos clave:** `models.py`, `database.py`

---

## ✅ 3. PostgreSQL (Railway)  
> 💾 "La bóveda donde se guardan los datos"

- Es el **sistema de base de datos real** que guarda la información de forma **persistente**.
- Railway lo hospeda en la nube.
- SQLAlchemy crea las tablas y ejecuta las consultas por ti (sin escribir SQL crudo).

📌 **La conexión se hace con:**  
```env
DATABASE_URL=postgresql://usuario:clave@host:puerto/nombre_basedatos
```

---

## 🔁 Flujo de trabajo entre tecnologías

```
Lógica de la app (FastAPI)
         ⬇️
  Modelos ORM (SQLAlchemy)
         ⬇️
  Consultas SQL generadas
         ⬇️
  Base de datos real (PostgreSQL)
```

---

## 🧠 Resumen de roles

| Tecnología   | Rol en el flujo                            |
|--------------|---------------------------------------------|
| FastAPI      | Define la API y recibe las peticiones       |
| SQLAlchemy   | Traduce las operaciones a consultas SQL     |
| PostgreSQL   | Ejecuta y guarda los datos en la nube       |