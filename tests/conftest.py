"""Shared pytest fixtures for customer search test suite."""

import json
from pathlib import Path
import pytest

from customer_search.models import Customer
from customer_search.repository import CustomerRepository, DEFAULT_DATA_PATH
from customer_search.search_service import SearchService


@pytest.fixture
def seed_dataset_path() -> Path:
    """Fixture returning the path to the seed customers.json file."""
    return DEFAULT_DATA_PATH


@pytest.fixture
def seed_customers(seed_dataset_path: Path) -> list[Customer]:
    """Fixture returning the full list of Customer objects from seed dataset."""
    repo = CustomerRepository(file_path=seed_dataset_path)
    return repo.find_all()


@pytest.fixture
def search_service() -> SearchService:
    """Fixture providing a default SearchService configured with seed repository."""
    return SearchService()


@pytest.fixture
def sample_customers() -> list[Customer]:
    """Fixture providing a controlled small list of customers."""
    return [
        Customer("C-01", "José García", "jose.garcia@example.com"),
        Customer("C-02", "Ana Martínez", "ana.martinez@example.com"),
        Customer("C-03", "Carlos Gómez", "carlos.gomez@example.com"),
        Customer("C-04", "Beatriz Solano", "bsolano98@mail.com"),
        Customer("C-05", "Marcos Vélez", "mvelez_special@test.org"),
        Customer("C-06", "Isabel Torres", "isabel.torres@empresa.es"),
    ]
