# 📦 study/notes_freeze.md — Cómo congelar dependencias en `requirements.txt`

---

## ✅ ¿Qué es `pip freeze > requirements.txt`?

Este comando guarda todas las dependencias instaladas actualmente en tu entorno virtual en un archivo de texto llamado `requirements.txt`.

Este archivo es usado para que otras personas (o servicios como Railway) puedan instalar exactamente las mismas librerías y versiones que se usaron.

---

## 📋 ¿Cuándo usarlo?

- Después de instalar nuevas librerías (`pip install openai`, `pip install pytest`, etc.)
- Antes de hacer deploy en Railway
- Cuando finalizas una sección funcional de tu proyecto
- Cuando vayas a compartir tu repositorio

---

## 🧪 Comando a ejecutar

```bash
pip freeze > requirements.txt
```

Esto sobrescribe (o crea) el archivo `requirements.txt` con una lista como:

```
fastapi==0.115.1
openai==1.30.5
psycopg2-binary==2.9.10
python-dotenv==1.0.1
sqlalchemy==2.0.41
pytest==8.3.5
uvicorn==0.34.2
```

---

## 📦 ¿Para qué sirve `requirements.txt`?

- Railway o cualquier servidor puede correr:

```bash
pip install -r requirements.txt
```

Y tener el mismo entorno que el de development, sin errores por versiones incompatibles.

---

## 📌 Buen hábito

Después de instalar una nueva dependencia, haz:

```bash
pip install nueva_libreria
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
```

Así aseguras consistencia y despliegues confiables.