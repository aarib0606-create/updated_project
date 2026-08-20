# Hospital Management System API

FastAPI + SQLAlchemy API for managing patients, doctors, and appointments.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
alembic -c alembic.ini upgrade head
uvicorn app.app:app --reload
```

API documentation is available at `/docs` while the server is running.

## Tests

```bash
pytest tests --cov=app --cov-report=term-missing
```

Tests use a separate SQLite database (`tests/hospital_test.db`) so they do not modify the development database.
