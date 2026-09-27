"""Tests for Customer domain model."""

import pytest
from customer_search.models import Customer


def test_customer_creation():
    customer = Customer(
        cliente_id="CUST-0001",
        nombre="José García",
        email="jose.garcia@example.com",
    )
    assert customer.cliente_id == "CUST-0001"
    assert customer.nombre == "José García"
    assert customer.email == "jose.garcia@example.com"


def test_customer_equality():
    c1 = Customer("CUST-0001", "Ana Martínez", "ana@example.com")
    c2 = Customer("CUST-0001", "Ana Martínez", "ana@example.com")
    c3 = Customer("CUST-0002", "Ana Martínez", "ana@example.com")
    assert c1 == c2
    assert c1 != c3


def test_customer_missing_fields():
    with pytest.raises(TypeError):
        Customer(cliente_id="CUST-0001")  # missing required fields
