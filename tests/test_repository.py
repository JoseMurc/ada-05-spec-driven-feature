"""Tests for CustomerRepository."""

import json
from pathlib import Path
from customer_search.models import Customer
from customer_search.repository import CustomerRepository, DEFAULT_DATA_PATH


def test_find_all_reads_seed_dataset():
    repo = CustomerRepository()
    customers = repo.find_all()

    # Must match the seed dataset count (1,000 customers)
    assert len(customers) == 1000
    assert all(isinstance(c, Customer) for c in customers)

    # Verify first and last records match raw json directly without alteration
    with open(DEFAULT_DATA_PATH, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    for i in [0, 500, 999]:
        assert customers[i].cliente_id == raw_data[i]["cliente_id"]
        assert customers[i].nombre == raw_data[i]["nombre"]
        assert customers[i].email == raw_data[i]["email"]


def test_find_all_empty_dataset(tmp_path: Path):
    empty_file = tmp_path / "empty.json"
    empty_file.write_text("[]", encoding="utf-8")

    repo = CustomerRepository(file_path=empty_file)
    results = repo.find_all()
    assert results == []


def test_find_all_does_not_filter_sort_or_normalize(tmp_path: Path):
    sample_data = [
        {"cliente_id": "Z-99", "nombre": "zeta", "email": "zeta@test.com"},
        {"cliente_id": "A-01", "nombre": "Álvaro", "email": "alvaro@test.com"},
        {"cliente_id": "M-50", "nombre": "  Marcos  ", "email": "marcos@test.com"},
    ]
    sample_file = tmp_path / "sample.json"
    sample_file.write_text(json.dumps(sample_data, ensure_ascii=False), encoding="utf-8")

    repo = CustomerRepository(file_path=sample_file)
    customers = repo.find_all()

    # Order must strictly match file order (no sorting)
    assert [c.cliente_id for c in customers] == ["Z-99", "A-01", "M-50"]
    # Content must preserve original accents, case, and whitespace (no normalization)
    assert customers[0].nombre == "zeta"
    assert customers[1].nombre == "Álvaro"
    assert customers[2].nombre == "  Marcos  "
