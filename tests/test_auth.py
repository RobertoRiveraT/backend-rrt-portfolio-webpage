import pytest

@pytest.fixture
def test_user():
    """
    Fixture that provides a consistent user payload for registration and login tests.
    """
    return {
        "email": "testuserAuth@example.com",
        "password": "securepassword123"
    }

def get_token(client, user_data):
    response = client.post("/login", data={
        "username": user_data["email"],
        "password": user_data["password"]
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
    return response.json()["access_token"]

def delete_user_via_force_route(client, email):
    """
    Uses the /force-delete-user test-only endpoint to remove a user by email,
    regardless of their current password or state.
    """
    response = client.post("/force-delete-user", json={"email": email})
    assert response.status_code == 200

def test_register_user(client, test_user):
    """
    Tests the registration endpoint by:
    - Deleting the user beforehand to ensure a clean state
    - Registering the user
    - Validating the returned response
    """
    # Ensure user doesn't exist
    delete_user_via_force_route(client, test_user["email"])

    # Attempt to register user
    response = client.post("/register", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert "email" in data

    # Cleanup
    delete_user_via_force_route(client, test_user["email"])

def test_login_user(client, test_user):
    """
    Tests the login endpoint by:
    - Deleting and recreating the user
    - Logging in to retrieve a JWT token
    - Validating token structure and response
    """
    # Ensure clean slate
    delete_user_via_force_route(client, test_user["email"])

    # Register user for login
    register = client.post("/register", json=test_user)
    assert register.status_code == 200

    # Login to get token
    response = client.post("/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Cleanup
    delete_user_via_force_route(client, test_user["email"])