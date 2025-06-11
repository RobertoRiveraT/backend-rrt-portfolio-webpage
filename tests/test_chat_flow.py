import pytest

@pytest.fixture
def chat_user():
    # Provide test user credentials
    return {
        "email": "testUserChatFlow@example.com",
        "password": "pytestpassword123"
    }

@pytest.fixture
def chat_auth(client, chat_user):
    """
    Fixture that ensures the user is deleted before test,
    registers the user, logs in, and returns the Authorization header.
    """
    # Cleanup in case user already exists
    try:
        token = get_token(client, chat_user)
        client.delete("/delete-account", headers={
            "Authorization": f"Bearer {token}"
        })
    except AssertionError:
        pass  # user didn't exist

    # Register user
    register = client.post("/register", json=chat_user)
    assert register.status_code == 200

    # Login to get token
    token = get_token(client, chat_user)
    yield {"Authorization": f"Bearer {token}"}

    # Cleanup user after test
    client.delete("/delete-account", headers={"Authorization": f"Bearer {token}"})

def get_token(client, user_data):
    """Helper function to get JWT token for a user"""
    response = client.post("/login", data={
        "username": user_data["email"],
        "password": user_data["password"]
    }, headers={
        "Content-Type": "application/x-www-form-urlencoded"
    })
    assert response.status_code == 200
    return response.json()["access_token"]

def test_chat_flow(client, chat_auth):
    """
    Tests the complete chat flow:
    1. User sends a message to the bot
    2. Bot responds with content
    3. User retrieves chat history
    """
    # 1. Send message to /chat endpoint
    response_chat = client.post("/chat", json={
        "content": "Hola, ¿qué puedes hacer?"
    }, headers=chat_auth)
    assert response_chat.status_code == 200
    data = response_chat.json()
    assert "content" in data
    assert data["role"] == "assistant"
    assert isinstance(data["content"], str)
    assert len(data["content"]) > 0

    # 2. Fetch message history
    response_history = client.get("/chat-history", headers=chat_auth)
    assert response_history.status_code == 200
    history = response_history.json()
    assert isinstance(history, list)
    assert len(history) >= 2  # Should contain both user and assistant messages
    assert all("role" in msg and "content" in msg for msg in history)
