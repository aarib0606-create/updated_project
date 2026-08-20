"""Tests for the patients API."""

from fastapi.testclient import TestClient

from app.app import app

client = TestClient(app)


def test_create_patient():
    """Verify that a patient can be created."""

    response = client.post(
        "/patients",
        json={
            "name": "John Doe",
            "age": 30,
            "gender": "male",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["name"] == "John Doe"
    assert data["age"] == 30
    assert data["gender"] == "male"


def test_get_patients():
    """Verify that all patients can be retrieved."""

    response = client.get("/patients")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_patient():
    """Verify that a created patient can be retrieved by ID."""

    create_response = client.post(
        "/patients",
        json={
            "name": "Jane Smith",
            "age": 45,
            "gender": "female",
        },
    )

    assert create_response.status_code == 201

    patient_id = create_response.json()["id"]

    response = client.get(f"/patients/{patient_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == patient_id
    assert data["name"] == "Jane Smith"
    assert data["age"] == 45
    assert data["gender"] == "female"


def test_get_patient_not_found():
    """Verify that a missing patient returns a 404 response."""

    response = client.get("/patients/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Patient not found"


def test_create_patient_invalid_data():
    """Verify that invalid patient data returns a validation error."""

    response = client.post(
        "/patients",
        json={
            "name": "John Doe",
            "age": "invalid",
            "gender": "male",
        },
    )

    assert response.status_code == 422
