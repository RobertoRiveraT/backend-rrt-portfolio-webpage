from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_user_account_crud():
    # Registro de usuario
    email = "pytestuser@example.com"
    password = "pytestpassword123"
    register = client.post("/register", json={"email": email, "password": password})
    assert register.status_code == 200

    # Login para obtener token
    login = client.post(
        "/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Cambiar email
    new_email = "newemail@example.com"
    response_email = client.put(
        "/update-email",
        headers=headers,
        json={"new_email": new_email}  # ✅ JSON en el body
    )
    assert response_email.status_code == 200
    assert "Correo actualizado correctamente" in response_email.json()["message"]

    # Cambiar contraseña
    new_password = "newpass456"
    response_password = client.put(
        "/update-password",
        headers=headers,
        json={"new_password": new_password}
    )
    assert response_password.status_code == 200
    assert "Contraseña actualizada correctamente" in response_password.json()["message"]

    # Eliminar cuenta
    response_delete = client.delete("/delete-account", headers=headers)
    assert response_delete.status_code == 200
    assert "Cuenta eliminada correctamente" in response_delete.json()["message"]
