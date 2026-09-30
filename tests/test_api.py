import os

os.environ["DATABASE_URL"] = (
    "sqlite:///./test_pocketsmart.db"
)

os.environ["SECRET_KEY"] = (
    "test-secret-key"
)


from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert (
        response.json()["status"]
        == "ok"
    )


def test_register_login_and_home():

    email = (
        "test_user_pocketsmart@example.com"
    )

    register_response = client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "password": "password123",
        },
    )

    assert register_response.status_code in (
        201,
        409,
    )


    login_response = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": "password123",
        },
    )

    assert (
        login_response.status_code
        == 200
    )


    home_response = client.post(
        "/api/generate-home",
        json={
            "budget": 50000,
            "rooms": [
                "Living Room",
                "Bedroom",
            ],
            "style": "Modern",
            "city": "Vellore",
            "notes": "",
        },
    )

    assert (
        home_response.status_code
        == 200
    )


    body = home_response.json()

    assert (
        body["planner_type"]
        == "home"
    )

    assert body["recommendations"]


def test_protected_endpoint_requires_login():

    isolated_client = TestClient(
        app
    )

    response = isolated_client.get(
        "/api/auth/session-info"
    )

    assert (
        response.status_code
        == 401
    )