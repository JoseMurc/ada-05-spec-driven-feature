"""Integration tests for customer search CLI."""

from io import StringIO
import pytest
from customer_search.cli import format_output, main
from customer_search.messages import NO_RESULTS_MESSAGE
from customer_search.search_service import CustomerView, SearchResult, SearchService


def test_format_output_ok():
    result = SearchResult(
        items=[
            CustomerView("CUST-0001", "José García", "jose@example.com"),
            CustomerView("CUST-0002", "Ana Martínez", "ana@example.com"),
        ],
        total=2,
        status="OK",
    )
    output = format_output(result)
    assert "Total de coincidencias: 2" in output
    assert "Mostrando 2 resultados:" in output
    assert "[CUST-0001] José García <jose@example.com>" in output
    assert "[CUST-0002] Ana Martínez <ana@example.com>" in output


def test_format_output_empty_query():
    result = SearchResult(items=[], total=0, status="EMPTY_QUERY", message=None)
    output = format_output(result)
    assert "vacía" in output.lower()


def test_format_output_no_results():
    result = SearchResult(items=[], total=0, status="NO_RESULTS", message=NO_RESULTS_MESSAGE)
    output = format_output(result)
    assert output == NO_RESULTS_MESSAGE


def test_cli_main_ok(monkeypatch):
    captured = StringIO()
    monkeypatch.setattr("sys.stdout", captured)

    exit_code = main(["carlos"])
    assert exit_code == 0
    stdout = captured.getvalue()
    assert "Total de coincidencias:" in stdout
    assert "carlos" in stdout.lower()


def test_cli_main_empty_query(monkeypatch):
    captured = StringIO()
    monkeypatch.setattr("sys.stdout", captured)

    exit_code = main(["   "])
    assert exit_code == 0
    stdout = captured.getvalue()
    assert "vacía" in stdout.lower()


def test_cli_main_no_results(monkeypatch):
    captured = StringIO()
    monkeypatch.setattr("sys.stdout", captured)

    exit_code = main(["nonexistent_query_xyz_12345"])
    assert exit_code == 0
    stdout = captured.getvalue()
    assert NO_RESULTS_MESSAGE in stdout
