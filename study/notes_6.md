# 📝 notes_6.md – Manejo de mensajes y borrado de cuenta

## ✅ Contexto

Al implementar la función para eliminar una cuenta con `/delete-account`, notamos que los mensajes asociados al usuario **no se estaban eliminando**, lo que generaba registros huérfanos en la base de datos.

## ❌ Problema

```python
db.delete(user)
db.commit()
```

Esto eliminaba al usuario, pero **no eliminaba sus mensajes** porque SQLAlchemy no aplica `CASCADE` por defecto a menos que se configure explícitamente en los modelos.

## ✅ Solución rápida aplicada (versión manual)

Optamos por **eliminar los mensajes explícitamente** antes de eliminar al usuario. La función final quedó así:

```python
@router.delete("/delete-account")
def delete_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Eliminar mensajes del usuario
    from app import models  # Asegurarse de importar el modelo
    db.query(models.Message).filter(models.Message.user_id == current_user.id).delete()

    # Eliminar usuario
    db.delete(user)
    db.commit()

    return {"message": "Cuenta eliminada correctamente."}
```

## 📌 Notas técnicas

- Usamos `models.Message` en lugar de `Message` para evitar errores de referencia no definida.
- `models` debe estar importado desde `app`, así:  
  `from app import models`
- Esto se considera una solución segura en producción cuando no quieres alterar las migraciones de la base de datos.

## 🛠 Alternativa más elegante (no usada aquí)

Configurar relaciones con `cascade="all, delete-orphan"` y `ForeignKey(..., ondelete="CASCADE")` para que la base de datos lo maneje automáticamente. Requiere recrear tablas o usar Alembic.

---

## ✅ Resultado

Al eliminar una cuenta, sus mensajes se eliminan correctamente también, asegurando integridad en la base de datos.