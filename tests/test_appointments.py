"""Tests for the appointments API."""

from fastapi.testclient import TestClient

from app.app import app

client = TestClient(app)


def test_get_appointments():
    """Verify that all appointments can be retrieved."""

    response = client.get("/appointments")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_create_appointment():
    """Verify that an appointment can be created."""

    patient_response = client.post(
        "/patients",
        json={
            "name": "Appointment Patient",
            "age": 35,
            "gender": "male",
        },
    )

    assert patient_response.status_code == 201

    patient_id = patient_response.json()["id"]

    doctor_response = client.post(
        "/doctors",
        json={
            "name": "Appointment Doctor",
            "specialization": "cardiologist",
        },
    )

    assert doctor_response.status_code == 201

    doctor_id = doctor_response.json()["id"]

    response = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "date": "2026-08-20",
            "time": "10:30",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["patient_id"] == patient_id
    assert data["doctor_id"] == doctor_id
    assert data["date"] == "2026-08-20"
    assert data["time"] == "10:30"


def test_create_appointment_patient_not_found():
    """Verify that an invalid patient returns 404."""

    doctor_response = client.post(
        "/doctors",
        json={
            "name": "Test Doctor",
            "specialization": "neurologist",
        },
    )

    assert doctor_response.status_code == 201

    doctor_id = doctor_response.json()["id"]

    response = client.post(
        "/appointments",
        json={
            "patient_id": 999999,
            "doctor_id": doctor_id,
            "date": "2026-08-20",
            "time": "10:30",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Patient not found"


def test_create_appointment_doctor_not_found():
    """Verify that an invalid doctor returns 404."""

    patient_response = client.post(
        "/patients",
        json={
            "name": "Test Patient",
            "age": 40,
            "gender": "female",
        },
    )

    assert patient_response.status_code == 201

    patient_id = patient_response.json()["id"]

    response = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": 999999,
            "date": "2026-08-20",
            "time": "10:30",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Doctor not found"


def test_get_appointment():
    """Verify that a created appointment can be retrieved by ID."""

    patient_response = client.post(
        "/patients",
        json={
            "name": "Get Appointment Patient",
            "age": 50,
            "gender": "male",
        },
    )

    assert patient_response.status_code == 201

    patient_id = patient_response.json()["id"]

    doctor_response = client.post(
        "/doctors",
        json={
            "name": "Get Appointment Doctor",
            "specialization": "surgeon",
        },
    )

    assert doctor_response.status_code == 201

    doctor_id = doctor_response.json()["id"]

    create_response = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "date": "2026-08-20",
            "time": "14:00",
        },
    )

    assert create_response.status_code == 201

    appointment_id = create_response.json()["id"]

    response = client.get(f"/appointments/{appointment_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == appointment_id
    assert data["patient_id"] == patient_id
    assert data["doctor_id"] == doctor_id


def test_get_appointment_not_found():
    """Verify that a missing appointment returns 404."""

    response = client.get("/appointments/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Appointment not found"
