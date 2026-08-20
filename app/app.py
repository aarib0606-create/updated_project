"""Hospital management system API using FastAPI and SQLAlchemy."""

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Appointment, Doctor, Patient
from app.schemas import (
    AppointmentCreate,
    AppointmentResponse,
    DoctorCreate,
    DoctorResponse,
    PatientCreate,
    PatientResponse,
)

app = FastAPI(title="Hospital Management System API")



# ==================================================
# PATIENTS
# ==================================================


@app.get("/patients", response_model=list[PatientResponse])
async def get_patients(db: Session = Depends(get_db)):
    """Return a list of all patients."""
    patients = db.query(Patient).all()

    return patients


@app.post("/patients", response_model=PatientResponse, status_code=201)
async def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
):
    """Create a new patient and save it to the database."""

    new_patient = Patient(
        name=patient.name,
        age=patient.age,
        gender=patient.gender,
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


@app.get("/patients/{patient_id}", response_model=PatientResponse)
async def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
):
    """Return a patient by ID."""

    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    return patient


# ==================================================
# DOCTORS
# ==================================================


@app.get("/doctors", response_model=list[DoctorResponse])
async def get_doctors(db: Session = Depends(get_db)):
    """Return a list of all doctors."""

    doctors = db.query(Doctor).all()

    return doctors


@app.post("/doctors", response_model=DoctorResponse, status_code=201)
async def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
):
    """Create a new doctor and save it to the database."""

    new_doctor = Doctor(
        name=doctor.name,
        specialization=doctor.specialization,
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor


@app.get("/doctors/{doctor_id}", response_model=DoctorResponse)
async def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
):
    """Return a doctor by ID."""

    doctor = (
        db.query(Doctor)
        .filter(Doctor.id == doctor_id)
        .first()
    )

    if doctor is None:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found",
        )

    return doctor


# ==================================================
# APPOINTMENTS
# ==================================================


@app.get(
    "/appointments",
    response_model=list[AppointmentResponse],
)
async def get_appointments(db: Session = Depends(get_db)):
    """Return a list of all appointments."""

    appointments = db.query(Appointment).all()

    return appointments


@app.post(
    "/appointments",
    response_model=AppointmentResponse,
    status_code=201,
)
async def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
):
    """Create an appointment after validating patient and doctor."""

    # Check that the patient exists.
    patient = (
        db.query(Patient)
        .filter(Patient.id == appointment.patient_id)
        .first()
    )

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    # Check that the doctor exists.
    doctor = (
        db.query(Doctor)
        .filter(Doctor.id == appointment.doctor_id)
        .first()
    )

    if doctor is None:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found",
        )

    new_appointment = Appointment(
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        date=appointment.date,
        time=appointment.time,
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment


@app.get(
    "/appointments/{appointment_id}",
    response_model=AppointmentResponse,
)
async def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
):
    """Return an appointment by ID."""

    appointment = (
        db.query(Appointment)
        .filter(Appointment.id == appointment_id)
        .first()
    )

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found",
        )

    return appointment
