"""Shared pytest configuration for isolated test databases."""

import os

# Set this before importing the application so tests never modify the project DB.
os.environ.setdefault("DATABASE_URL", "sqlite:///./tests/hospital_test.db")

from app.database import Base, engine  # noqa: E402
from app import models  # noqa: F401,E402


def pytest_sessionstart(session):
    """Create the isolated test schema before test collection runs."""
    del session
    Base.metadata.create_all(bind=engine)
