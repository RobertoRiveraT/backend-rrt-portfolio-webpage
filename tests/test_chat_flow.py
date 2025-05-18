from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_flow_reusable():
    email = "pytestuserchat@example.com"
    password = "pytestpassword123"

    # 1. Verificar si el usuario ya existe tratando de loguear
    login = client.post(
        "/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    if login.status_code == 200:
        token = login.json()["access_token"]
    else:
        # 2. Registrar usuario si no existe
        register = client.post("/register", json={"email": email, "password": password})
        assert register.status_code == 200

        # 3. Login ahora que fue creado
        login = client.post(
            "/login",
            data={"username": email, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert login.status_code == 200
        token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # 4. Enviar mensaje al bot
    response_chat = client.post("/chat", json={"content": "Hola, ¿qué puedes hacer?"}, headers=headers)
    assert response_chat.status_code == 200
    data = response_chat.json()
    assert "content" in data
    assert data["role"] == "assistant"
    assert isinstance(data["content"], str)
    assert len(data["content"]) > 0

    # 5. Obtener historial
    response_history = client.get("/chat-history", headers=headers)
    assert response_history.status_code == 200
    history = response_history.json()
    assert isinstance(history, list)
    if history:
        assert "content" in history[0]
        assert "role" in history[0]
        assert history[0]["role"] in ["user", "assistant"]
