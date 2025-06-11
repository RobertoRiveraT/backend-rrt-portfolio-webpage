import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Fixed test user data
TEST_EMAIL = "pytestuserCRUD@example.com"
NEW_EMAIL = "newemailCRUD@example.com"
TEST_PASSWORD = "pytestpassword123"
NEW_PASSWORD = "newpass456"

def get_token(email, password):
    """
    Logs in and retrieves an access token for the given credentials.
    """
    response = client.post("/login", data={
        "username": email,
        "password": password
    }, headers={
        "Content-Type": "application/x-www-form-urlencoded"
    })
    assert response.status_code == 200
    return response.json()["access_token"]

def delete_if_exists(email):
    """
    Attempts to delete the user by email using the test-only endpoint.
    This avoids test collisions due to duplicate emails.
    """
    client.post("/force-delete-user", json={"email": email})  # No assert needed in case it doesn't exist

@pytest.fixture(scope="module")
def setup_user():
    """
    Fixture to create a test user, handle cleanup, and provide original credentials.
    """
    # Clean both emails just in case
    delete_if_exists(TEST_EMAIL)
    delete_if_exists(NEW_EMAIL)

    # Register new user
    register = client.post("/register", json={
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    })
    assert register.status_code == 200

    yield {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }

    # Final cleanup
    delete_if_exists(TEST_EMAIL)
    delete_if_exists(NEW_EMAIL)

@pytest.fixture
def auth_headers(setup_user):
    """
    Fixture that returns an Authorization header for the test user.
    """
    token = get_token(setup_user["email"], setup_user["password"])
    return {"Authorization": f"Bearer {token}"}

def test_update_email(auth_headers):
    """
    Tests updating the user's email using /update-email endpoint.
    """
    response = client.put("/update-email", headers=auth_headers, json={
        "new_email": NEW_EMAIL
    })
    assert response.status_code == 200
    assert "Correo actualizado correctamente" in response.json()["message"]

def test_update_password():
    """
    Tests updating the password for the newly updated email user.
    We login with the new email and change password.
    """
    token = get_token(NEW_EMAIL, TEST_PASSWORD)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.put("/update-password", headers=headers, json={
        "new_password": NEW_PASSWORD
    })
    assert response.status_code == 200
    assert "Contraseña actualizada correctamente" in response.json()["message"]

def test_final_deletion():
    """
    Tests final deletion of the updated user account using /delete-account.
    """
    token = get_token(NEW_EMAIL, NEW_PASSWORD)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete("/delete-account", headers=headers)
    assert response.status_code == 200
    assert "The account was successfully deleted." in response.json()["message"]

