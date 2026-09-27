"""Tests for SearchService search logic and acceptance criteria."""

import dataclasses
from customer_search.messages import NO_RESULTS_MESSAGE
from customer_search.models import Customer
from customer_search.repository import CustomerRepository
from customer_search.search_service import CustomerView, SearchResult, SearchService


class MockRepository(CustomerRepository):
    """In-memory mock repository for isolated search logic tests."""

    def __init__(self, customers: list[Customer]) -> None:
        self._customers = customers

    def find_all(self) -> list[Customer]:
        return list(self._customers)


def test_ac01_name_and_email_match():
    customers = [
        Customer("C-1", "Beatriz Solano", "bsolano@domain.com"),
        Customer("C-2", "Marcos Vélez", "mvelez_special@domain.com"),
        Customer("C-3", "Carlos López", "clopez@domain.com"),
    ]
    service = SearchService(repository=MockRepository(customers))

    # Match by name only
    res_name = service.search("Solano")
    assert res_name.status == "OK"
    assert len(res_name.items) == 1
    assert res_name.items[0].cliente_id == "C-1"

    # Match by email only
    res_email = service.search("special")
    assert res_email.status == "OK"
    assert len(res_email.items) == 1
    assert res_email.items[0].cliente_id == "C-2"


def test_ac02_deduplication():
    # Carlos appears in both name and email
    customers = [
        Customer("C-1", "Carlos Gómez", "carlos.gomez@domain.com"),
        Customer("C-2", "Ana Martínez", "ana@domain.com"),
    ]
    service = SearchService(repository=MockRepository(customers))

    res = service.search("carlos")
    assert res.status == "OK"
    assert res.total == 1
    assert len(res.items) == 1
    assert res.items[0].cliente_id == "C-1"


def test_ac03_substring_match():
    customers = [
        Customer("C-1", "Isabel Torres", "itorres@domain.com"),
        Customer("C-2", "Benoît Laurent", "laurent@domain.com"),
    ]
    service = SearchService(repository=MockRepository(customers))

    # "bel" is inside Isabel (not at prefix)
    res = service.search("bel")
    assert res.status == "OK"
    assert any(c.cliente_id == "C-1" for c in res.items)

    # "torres" in email
    res2 = service.search("torres")
    assert res2.status == "OK"
    assert any(c.cliente_id == "C-1" for c in res2.items)


def test_ac04_case_and_diacritics_equivalence():
    service = SearchService()  # Uses real 1,000 customers seed dataset

    res_upper = service.search("JOSÉ")
    res_lower = service.search("jose")
    res_title = service.search("José")

    assert res_upper.status == "OK"
    assert res_lower.status == "OK"
    assert res_title.status == "OK"

    assert res_upper.total == res_lower.total == res_title.total
    assert res_upper.items == res_lower.items == res_title.items


def test_ac05_whitespace_equivalence():
    service = SearchService()

    res1 = service.search("ana")
    res2 = service.search(" ana ")
    res3 = service.search("   ana   ")

    assert res1.status == "OK"
    assert res1.total == res2.total == res3.total
    assert res1.items == res2.items == res3.items


def test_ac09_truncation_to_50_with_real_total():
    service = SearchService()  # Real dataset has >50 records matching example.com

    res = service.search("example.com")
    assert res.status == "OK"
    assert res.total > 50
    assert len(res.items) == 50


def test_ac10_deterministic_order():
    service = SearchService()

    run1 = service.search("García")
    run2 = service.search("García")
    run3 = service.search("García")

    assert [c.cliente_id for c in run1.items] == [c.cliente_id for c in run2.items] == [c.cliente_id for c in run3.items]


def test_ac12_field_projection_whitelist():
    customers = [
        Customer("C-1", "Carlos Gómez", "carlos@example.com"),
    ]
    service = SearchService(repository=MockRepository(customers))

    res = service.search("Carlos")
    assert len(res.items) == 1
    item = res.items[0]
    assert isinstance(item, CustomerView)
    item_dict = dataclasses.asdict(item)
    assert set(item_dict.keys()) == {"cliente_id", "nombre", "email"}


def test_ac13_ranking_and_tie_breaking():
    customers = [
        Customer("C-30", "Valeria Galeote", "valeria.g@example.com"),       # Tier 3 (internal substring "leo")
        Customer("C-21", "Leonor Cruz", "leonor.cruz@example.com"),         # Tier 2 (prefix "leo")
        Customer("C-20", "Leonardo Paz", "leonardo.paz@example.com"),       # Tier 2 (prefix "leo")
        Customer("C-10", "Leo", "leo.solo@example.com"),                    # Tier 1 (exact match "leo")
        Customer("C-22", "Leonardo Paz", "leonardo.alt@example.com"),       # Tier 2 (same name as C-20, ID tie-breaker)
    ]
    service = SearchService(repository=MockRepository(customers))

    res = service.search("Leo")
    assert res.status == "OK"
    ids = [c.cliente_id for c in res.items]

    # Priority order:
    # 1. C-10: Exact match ("Leo")
    # 2. C-20: Prefix match ("Leonardo Paz", ID C-20 before C-22)
    # 3. C-22: Prefix match ("Leonardo Paz", ID C-22)
    # 4. C-21: Prefix match ("Leonor Cruz", alphabetical after "Leonardo Paz")
    # 5. C-30: Substring match ("Valeria Galeote")
    assert ids == ["C-10", "C-20", "C-22", "C-21", "C-30"]


class SpyRepository(CustomerRepository):
    """Repository that tracks whether find_all was invoked."""

    def __init__(self) -> None:
        self.called = False

    def find_all(self) -> list[Customer]:
        self.called = True
        return []


def test_ac06_empty_query_does_not_call_repository():
    spy_repo = SpyRepository()
    service = SearchService(repository=spy_repo)

    for empty_input in ["", "   ", "\t  \n  "]:
        res = service.search(empty_input)
        assert res.status == "EMPTY_QUERY"
        assert res.items == []
        assert res.total == 0
        assert res.message is None
        assert spy_repo.called is False


def test_ac07_no_results_returns_empty_list_and_fixed_message():
    service = SearchService()  # Uses full dataset

    res = service.search("nonexistent_customer_query_xyz_999")
    assert res.status == "NO_RESULTS"
    assert res.items == []
    assert res.total == 0
    assert res.message == NO_RESULTS_MESSAGE


def test_ac11_user_scope_unrestricted():
    # FR-09 / AC-11: Data scope is the entire catalog for every user.
    # Simulated queries executed by different callers receive identical results.
    service = SearchService()

    user_a_result = service.search("Carlos")
    user_b_result = service.search("Carlos")

    assert user_a_result.status == user_b_result.status == "OK"
    assert user_a_result.total == user_b_result.total
    assert [c.cliente_id for c in user_a_result.items] == [c.cliente_id for c in user_b_result.items]


