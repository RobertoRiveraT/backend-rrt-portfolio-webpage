# Este archivo contiene pruebas básicas de integración para el backend de chatbot_arelia.
# Usa TestClient de FastAPI para simular peticiones HTTP al servidor.
# Valida que el registro, login y chat funcionen correctamente.

from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.main import app

client = TestClient(app)

# Usa un email único cada vez que corras el test (o borra el user de la base)
test_email = "testuser@example.com"
test_password = "securepassword123"

def test_register_user():
    response = client.post("/register", json={
        "email": test_email,
        "password": test_password
    })

    # Puede ser 200 (creado) o 400 si ya existe
    assert response.status_code in (200, 400)
    if response.status_code == 200:
        assert "email" in response.json()
    else:
        assert response.json()["detail"] == "Email already registered"

def test_login_user():
    response = client.post("/login", data={
        "username": test_email,
        "password": test_password
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Guardar token para usarlo en la siguiente prueba
    global auth_token
    auth_token = data["access_token"]

def test_chat_with_bot():
    # Asegurarse de que auth_token está disponible
    assert auth_token is not None

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/chat", headers=headers, json={
        "content": "Hola, ¿qué puedes hacer?"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "assistant"
    assert isinstance(data["content"], str)
    assert len(data["content"]) > 0
