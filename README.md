# Backend Architecture

## Get Started

```bash
poetry install
cp .env.example .env
poetry run uvicorn app.main:app --reload
```

Available at <http://localhost:8000>

Run checks with:

```bash
poetry run pytest
poetry run ruff check .
poetry run ruff format --check .
```

## Project structure

```text
app/
├── api/          # Routers and endpoints
├── core/         # Settings and shared infrastructure
└── main.py       # Application factory and ASGI entry point
tests/
```
