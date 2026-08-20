"""Tests for the doctors API."""

from fastapi.testclient import TestClient

from app.app import app

client = TestClient(app)


def test_create_doctor():
    """Verify that a doctor can be created."""

    response = client.post(
        "/doctors",
        json={
            "name": "John Doe",
            "specialization": "neurologist",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["name"] == "John Doe"
    assert data["specialization"] == "neurologist"


def test_get_doctors():
    """Verify that all doctors can be retrieved."""

    response = client.get("/doctors")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_doctor():
    """Verify that a created doctor can be retrieved by ID."""

    create_response = client.post(
        "/doctors",
        json={
            "name": "Jane Smith",
            "specialization": "cardiologist",
        },
    )

    assert create_response.status_code == 201

    doctor_id = create_response.json()["id"]

    response = client.get(f"/doctors/{doctor_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == doctor_id
    assert data["name"] == "Jane Smith"
    assert data["specialization"] == "cardiologist"


def test_get_doctor_not_found():
    """Verify that a missing doctor returns a 404 response."""

    response = client.get("/doctors/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Doctor not found"


def test_create_doctor_invalid_data():
    """Verify that invalid doctor data returns a validation error."""

    response = client.post(
        "/doctors",
        json={
            "name": "John Doe",
        },
    )

    assert response.status_code == 422
