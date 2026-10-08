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


# --- AC-14 / TS-14: dispatcher between interactive session and one-shot ---


class _SpySession:
    """Test double recording how InteractiveSession is constructed and run."""

    instances = []

    def __init__(self, service=None, **kwargs):
        self.service = service
        self.ran = False
        _SpySession.instances.append(self)

    def run(self):
        self.ran = True


class _SpyService:
    """Test double recording queries passed to SearchService.search."""

    def __init__(self):
        self.queries = []

    def search(self, query):
        self.queries.append(query)
        return SearchResult(items=[], total=0, status="NO_RESULTS", message=NO_RESULTS_MESSAGE)


@pytest.fixture
def spy_session(monkeypatch):
    _SpySession.instances = []
    monkeypatch.setattr("customer_search.session.InteractiveSession", _SpySession)
    return _SpySession


def test_build_parser_query_defaults_to_none():
    from customer_search.cli import build_parser

    args = build_parser().parse_args([])
    assert args.query is None


def test_ac14_main_without_args_starts_interactive_session(spy_session):
    service = _SpyService()

    exit_code = main([], service=service)

    assert exit_code == 0
    assert len(spy_session.instances) == 1
    session = spy_session.instances[0]
    assert session.service is service
    assert session.ran is True
    # The dispatcher itself does not run a search; the session does.
    assert service.queries == []


def test_ac14_main_with_args_runs_one_shot_without_session(spy_session, monkeypatch):
    captured = StringIO()
    monkeypatch.setattr("sys.stdout", captured)
    service = _SpyService()

    exit_code = main(["carlos"], service=service)

    assert exit_code == 0
    assert spy_session.instances == []
    assert service.queries == ["carlos"]
    assert NO_RESULTS_MESSAGE in captured.getvalue()


def test_ac14_main_with_whitespace_arg_stays_one_shot(spy_session, monkeypatch):
    captured = StringIO()
    monkeypatch.setattr("sys.stdout", captured)

    exit_code = main(["   "])

    assert exit_code == 0
    assert spy_session.instances == []
    assert "vacía" in captured.getvalue().lower()


def test_ac14_main_without_args_runs_real_session_until_eof(monkeypatch):
    captured = StringIO()
    monkeypatch.setattr("sys.stdout", captured)

    # Empty stdin makes the real input() raise EOFError (EH-05).
    monkeypatch.setattr("sys.stdin", StringIO(""))

    exit_code = main([])

    assert exit_code == 0
    assert "Bienvenido a buscador de clientes" in captured.getvalue()
