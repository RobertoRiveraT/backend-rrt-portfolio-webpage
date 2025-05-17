# 📘 study/notes_5.md — Error 400 al registrar usuario en pruebas con pytest

---

## 🧪 Problema

Al ejecutar la prueba `test_user_account_crud()` en `pytest`, se produjo este error:

```
assert 400 == 200
```

La línea fallida fue:

```python
assert register.status_code == 200
```

---

## 🔍 Causa

El endpoint `/register` devolvía `400 Bad Request` porque el correo electrónico usado (`testuser@example.com`) ya existía previamente en la base de datos remota de PostgreSQL en Railway.

Como las pruebas estaban apuntando a una base de datos real (remota), no se podía volver a registrar al mismo usuario.

---

## ✅ Solución aplicada

Para garantizar que el correo sea único en cada prueba, se usó el módulo `uuid` para generar direcciones de email aleatorias:

```python
import uuid
email = f"testuser_{uuid.uuid4()}@example.com"
```

Esto garantiza que cada ejecución de `pytest` use un nuevo usuario, evitando colisiones en la base de datos.

---

## 🧪 Resultado

- Las pruebas pasaron correctamente al usar correos únicos
- Se mantuvo el uso de la base de datos real (Railway) para efectos prácticos del proyecto
- Se entendió que `pytest` se ejecuta localmente, pero puede modificar datos en remoto si así se configura en `.env`

---

## 📌 Observaciones

- Este tipo de errores son comunes cuando se realizan pruebas sobre bases compartidas o persistentes
- Para entornos profesionales, es recomendable:
  - Usar una base de datos temporal (SQLite o Docker)
  - O tener una base de Railway exclusiva para pruebas

---