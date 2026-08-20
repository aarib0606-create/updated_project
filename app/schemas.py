"""Pydantic schemas for the hospital management system API."""

from pydantic import BaseModel, ConfigDict


# ==================================================
# PATIENTS
# ==================================================


class PatientCreate(BaseModel):
    """Define the data required to create a patient."""

    name: str
    age: int
    gender: str


class PatientResponse(PatientCreate):
    """Define the data returned for a patient."""

    id: int

    model_config = ConfigDict(from_attributes=True)


# ==================================================
# DOCTORS
# ==================================================


class DoctorCreate(BaseModel):
    """Define the data required to create a doctor."""

    name: str
    specialization: str


class DoctorResponse(DoctorCreate):
    """Define the data returned for a doctor."""

    id: int

    model_config = ConfigDict(from_attributes=True)


# ==================================================
# APPOINTMENTS
# ==================================================


class AppointmentCreate(BaseModel):
    """Define the data required to create an appointment."""

    patient_id: int
    doctor_id: int
    date: str
    time: str


class AppointmentResponse(AppointmentCreate):
    """Define the data returned for an appointment."""

    id: int

    model_config = ConfigDict(from_attributes=True)
