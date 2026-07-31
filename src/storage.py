"""
Simple JSON-file-backed storage for expenses.

Kept deliberately small and dependency-free (just the stdlib `json`
module) so the persistence logic is easy to read and to unit test in
isolation from the API layer.
"""
import json
from pathlib import Path
from threading import Lock
from typing import Optional

from .models import Expense, ExpenseCreate

DEFAULT_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "expenses.json"


class ExpenseStore:
    """
    In-memory list of expenses, mirrored to a JSON file on every write so
    data survives a server restart. A lock guards read-modify-write
    sequences (add/delete) since FastAPI can serve requests concurrently.
    """

    def __init__(self, data_file: Optional[Path] = None):
        self._data_file = data_file or DEFAULT_DATA_FILE
        self._lock = Lock()
        self._expenses: list[Expense] = []
        self._next_id = 1
        self._load()

    def _load(self) -> None:
        if self._data_file.exists():
            raw = json.loads(self._data_file.read_text() or "[]")
            self._expenses = [Expense(**item) for item in raw]
            if self._expenses:
                self._next_id = max(e.id for e in self._expenses) + 1

    def _persist(self) -> None:
        self._data_file.parent.mkdir(parents=True, exist_ok=True)
        payload = [json.loads(e.model_dump_json()) for e in self._expenses]
        self._data_file.write_text(json.dumps(payload, indent=2, default=str))

    def add(self, payload: ExpenseCreate) -> Expense:
        with self._lock:
            expense = Expense(id=self._next_id, **payload.model_dump())
            self._expenses.append(expense)
            self._next_id += 1
            self._persist()
            return expense

    def list_all(self, category: Optional[str] = None) -> list[Expense]:
        if category is None:
            return list(self._expenses)
        return [e for e in self._expenses if e.category.lower() == category.lower()]

    def delete(self, expense_id: int) -> bool:
        with self._lock:
            before = len(self._expenses)
            self._expenses = [e for e in self._expenses if e.id != expense_id]
            deleted = len(self._expenses) != before
            if deleted:
                self._persist()
            return deleted

    def clear(self) -> None:
        """Used by tests to reset state between runs."""
        with self._lock:
            self._expenses = []
            self._next_id = 1
            self._persist()
