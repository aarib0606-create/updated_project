"""SQLAlchemy database models for the hospital management system."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Patient(Base):
    """Represent a patient and their associated appointments."""

    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    appointments = relationship(
        "Appointment",
        back_populates="patient",
    )


class Doctor(Base):
    """Represent a doctor and their associated appointments."""

    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)

    appointments = relationship(
        "Appointment",
        back_populates="doctor",
    )


class Appointment(Base):
    """Represent an appointment between a patient and a doctor."""

    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False,
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id"),
        nullable=False,
    )

    date = Column(String, nullable=False)
    time = Column(String, nullable=False)

    patient = relationship(
        "Patient",
        back_populates="appointments",
    )

    doctor = relationship(
        "Doctor",
        back_populates="appointments",
    )
