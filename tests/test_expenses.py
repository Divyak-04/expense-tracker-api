"""
Test suite for the Smart Expense Tracker API.

Uses FastAPI's TestClient (backed by httpx) against the real `app`
object. The store is pointed at a temp JSON file and cleared before
every test so tests don't leak state into each other or into the
real data/expenses.json used by `uvicorn` during manual runs.
"""
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src import storage
from src.main import app

# Redirect storage to a throwaway file for the whole test session,
# then clear it before each individual test.
_tmp_dir = tempfile.TemporaryDirectory()
storage_module_file = Path(_tmp_dir.name) / "test_expenses.json"


@pytest.fixture(autouse=True)
def clean_store():
    from src.main import store

    store._data_file = storage_module_file
    store.clear()
    yield
    store.clear()


client = TestClient(app)


def _add(title="Coffee", amount=150, category="food", date="2026-07-01"):
    return client.post(
        "/expenses",
        json={"title": title, "amount": amount, "category": category, "date": date},
    )


def test_add_expense_returns_created_expense_with_id():
    resp = _add()
    assert resp.status_code == 201
    body = resp.json()
    assert body["title"] == "Coffee"
    assert body["amount"] == 150
    assert body["category"] == "food"
    assert body["date"] == "2026-07-01"
    assert isinstance(body["id"], int)


def test_add_expense_rejects_non_positive_amount():
    resp = _add(amount=0)
    assert resp.status_code == 422

    resp = _add(amount=-5)
    assert resp.status_code == 422


def test_add_expense_rejects_blank_title():
    resp = _add(title="   ")
    assert resp.status_code == 422


def test_list_expenses_returns_all_added():
    _add(title="Coffee", amount=150, category="food")
    _add(title="Bus ticket", amount=40, category="travel")

    resp = client.get("/expenses")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body) == 2
    titles = {e["title"] for e in body}
    assert titles == {"Coffee", "Bus ticket"}


def test_list_expenses_filters_by_category_case_insensitively():
    _add(title="Coffee", amount=150, category="Food")
    _add(title="Bus ticket", amount=40, category="Travel")

    resp = client.get("/expenses", params={"category": "food"})
    assert resp.status_code == 200
    body = resp.json()
    assert len(body) == 1
    assert body[0]["title"] == "Coffee"


def test_list_expenses_empty_category_filter_returns_no_matches():
    _add(title="Coffee", amount=150, category="food")
    resp = client.get("/expenses", params={"category": "utilities"})
    assert resp.status_code == 200
    assert resp.json() == []


def test_totals_overall_and_by_category():
    _add(title="Coffee", amount=150, category="food")
    _add(title="Lunch", amount=250, category="food")
    _add(title="Bus ticket", amount=40, category="travel")

    resp = client.get("/expenses/total")
    assert resp.status_code == 200
    body = resp.json()
    assert body["overall_total"] == 440
    by_cat = {c["category"]: c["total"] for c in body["by_category"]}
    assert by_cat == {"food": 400, "travel": 40}


def test_totals_scoped_to_a_single_category():
    _add(title="Coffee", amount=150, category="food")
    _add(title="Lunch", amount=250, category="food")
    _add(title="Bus ticket", amount=40, category="travel")

    resp = client.get("/expenses/total", params={"category": "food"})
    assert resp.status_code == 200
    assert resp.json()["overall_total"] == 400


def test_monthly_summary_groups_by_year_month():
    _add(title="Coffee", amount=150, category="food", date="2026-07-01")
    _add(title="Lunch", amount=250, category="food", date="2026-07-15")
    _add(title="Flight", amount=5000, category="travel", date="2026-08-02")

    resp = client.get("/expenses/summary/monthly")
    assert resp.status_code == 200
    assert resp.json() == {"2026-07": 400, "2026-08": 5000}


def test_delete_expense_removes_it():
    created = _add().json()
    expense_id = created["id"]

    resp = client.delete(f"/expenses/{expense_id}")
    assert resp.status_code == 204

    resp = client.get("/expenses")
    assert resp.json() == []


def test_delete_nonexistent_expense_returns_404():
    resp = client.delete("/expenses/9999")
    assert resp.status_code == 404
