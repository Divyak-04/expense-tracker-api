# Smart Expense Tracker API

A small REST API for tracking personal expenses, built with FastAPI.

## What it does

- Add an expense (title, amount, category, date)
- View all expenses, optionally filtered by category
- Calculate totals (overall, and broken down by category)
- Delete an expense
- **Bonus:** a monthly summary endpoint (`/expenses/summary/monthly`) that
  groups totals by `YYYY-MM`
- Interactive API docs are auto-generated at `/docs` (Swagger UI) and
  `/redoc`, courtesy of FastAPI

Data is stored in a local JSON file (`data/expenses.json`), created
automatically on first write, so expenses survive a server restart.

## Project structure

```
.
├── README.md
├── AI_NOTES.md
├── requirements.txt
├── src/
│   ├── main.py       # FastAPI app and route handlers
│   ├── models.py      # Pydantic request/response models
│   └── storage.py     # JSON-file-backed storage layer
└── tests/
    └── test_expenses.py
```

## Install

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run the server

```bash
uvicorn src.main:app --reload
```

The API is then available at `http://127.0.0.1:8000`, with interactive
docs at `http://127.0.0.1:8000/docs`.

## Run the tests

```bash
pytest tests/ -v
```

Tests use FastAPI's `TestClient` and point the storage layer at a
temporary file, so they never touch (or depend on) `data/expenses.json`.

## API reference

| Method | Path                          | Description                                   |
|--------|-------------------------------|------------------------------------------------|
| POST   | `/expenses`                   | Add an expense                                |
| GET    | `/expenses`                   | List expenses (optional `?category=`)         |
| GET    | `/expenses/total`             | Overall total + breakdown by category (optional `?category=` to scope the overall total) |
| GET    | `/expenses/summary/monthly`   | Totals grouped by month (bonus)               |
| DELETE | `/expenses/{id}`              | Delete an expense by id                       |

### Example: add an expense

```bash
curl -X POST http://127.0.0.1:8000/expenses \
  -H "Content-Type: application/json" \
  -d '{"title": "Coffee", "amount": 150, "category": "food", "date": "2026-07-01"}'
```

## Design notes

- **Storage:** a single `ExpenseStore` class wraps a JSON file. It's not
  a database, but the read/write logic is isolated behind a small
  interface so it could be swapped for one without touching the route
  handlers.
- **IDs:** integers assigned in-memory, continuing from the highest id
  already in the file on startup.
- **Validation:** Pydantic enforces a positive amount and non-blank
  title/category at the request boundary, so bad data returns a 422
  before it reaches the storage layer.
- **Concurrency:** a lock guards add/delete so two requests can't
  interleave a read-modify-write on the JSON file.
