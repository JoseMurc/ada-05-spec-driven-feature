"""Unit tests for InteractiveSession controller."""

from typing import List
import pytest

from customer_search.messages import NO_RESULTS_MESSAGE
from customer_search.models import Customer
from customer_search.repository import CustomerRepository
from customer_search.search_service import SearchService
from customer_search.session import (
    EXIT_COMMANDS,
    PROMPT,
    WELCOME_BANNER,
    InteractiveSession,
)


class MockRepository(CustomerRepository):
    """In-memory mock repository for session tests."""

    def __init__(self, customers: list[Customer]) -> None:
        self._customers = customers

    def find_all(self) -> list[Customer]:
        return list(self._customers)


@pytest.fixture
def mock_service() -> SearchService:
    customers = [
        Customer("C-1", "Carlos Gómez", "carlos.gomez@example.com"),
        Customer("C-2", "Ana Martínez", "ana@example.com"),
        Customer("C-3", "Elena Salir", "exit.user@domain.com"),
        Customer("C-4", "Cliente Exit", "cliente:exit@domain.com"),
    ]
    return SearchService(repository=MockRepository(customers))


def test_ac15_welcome_banner_content():
    """Verify welcome banner contains expected text and exit command instructions."""
    assert "Bienvenido a buscador de clientes" in WELCOME_BANNER
    assert ":salir" in WELCOME_BANNER
    assert ":exit" in WELCOME_BANNER


def test_ac15_banner_printed_on_run(mock_service):
    """Verify welcome banner is printed first upon session start (AC-15, SR-11)."""
    outputs: List[str] = []
    inputs = iter([":salir"])

    session = InteractiveSession(
        service=mock_service,
        input_fn=lambda prompt: next(inputs),
        output_fn=outputs.append,
    )
    session.run()

    assert len(outputs) >= 1
    assert outputs[0] == WELCOME_BANNER


def test_ac16_prompt_and_single_search(mock_service):
    """Verify prompt text and single search result output (AC-16, SR-12)."""
    prompts_received: List[str] = []
    outputs: List[str] = []
    inputs = iter(["carlos", ":salir"])

    def fake_input(prompt: str) -> str:
        prompts_received.append(prompt)
        return next(inputs)

    session = InteractiveSession(
        service=mock_service,
        input_fn=fake_input,
        output_fn=outputs.append,
    )
    session.run()

    # Prompts shown
    assert prompts_received == [PROMPT, PROMPT]
    assert PROMPT == "Buscar cliente: "

    # Outputs: banner, then carlos results
    assert outputs[0] == WELCOME_BANNER
    assert "Total de coincidencias: 1" in outputs[1]
    assert "[C-1] Carlos Gómez" in outputs[1]


def test_ac16_multiple_consecutive_searches(mock_service):
    """Verify session processes multiple consecutive queries in the same loop (AC-16, SR-12)."""
    outputs: List[str] = []
    inputs = iter(["carlos", "ana", ":exit"])

    session = InteractiveSession(
        service=mock_service,
        input_fn=lambda prompt: next(inputs),
        output_fn=outputs.append,
    )
    session.run()

    assert len(outputs) == 3  # Banner + 2 search outputs
    assert "[C-1] Carlos Gómez" in outputs[1]
    assert "[C-2] Ana Martínez" in outputs[2]


def test_ac17_empty_query_keeps_session_active(mock_service):
    """Verify empty query displays message and keeps session active for next query (AC-17, SR-13)."""
    outputs: List[str] = []
    inputs = iter(["   ", "carlos", ":salir"])

    session = InteractiveSession(
        service=mock_service,
        input_fn=lambda prompt: next(inputs),
        output_fn=outputs.append,
    )
    session.run()

    assert len(outputs) == 3
    assert "vacía" in outputs[1].lower()
    assert "[C-1] Carlos Gómez" in outputs[2]


def test_ac17_no_results_keeps_session_active(mock_service):
    """Verify no-results query displays fixed message and keeps session active (AC-17, SR-13)."""
    outputs: List[str] = []
    inputs = iter(["termino_inexistente_xyz", "carlos", ":exit"])

    session = InteractiveSession(
        service=mock_service,
        input_fn=lambda prompt: next(inputs),
        output_fn=outputs.append,
    )
    session.run()

    assert len(outputs) == 3
    assert outputs[1] == NO_RESULTS_MESSAGE
    assert "[C-1] Carlos Gómez" in outputs[2]


@pytest.mark.parametrize(
    "exit_cmd",
    [
        ":salir",
        ":exit",
        "  :salir  ",
        "  :exit  ",
        ":SALIR",
        ":EXIT",
        "  :Salir  ",
        "  :Exit  ",
    ],
)
def test_ac18_exit_commands_terminate_session(mock_service, exit_cmd):
    """Verify exit commands terminate the session without querying service (AC-18, VR-04, A-12)."""
    outputs: List[str] = []
    session = InteractiveSession(
        service=mock_service,
        input_fn=lambda prompt: exit_cmd,
        output_fn=outputs.append,
    )
    assert session.is_exit_command(exit_cmd) is True

    session.run()
    # Only banner was printed; no search was performed
    assert outputs == [WELCOME_BANNER]


@pytest.mark.parametrize(
    "legitimate_query",
    [
        "exit.user@domain.com",
        "Elena Salir",
        "salir",
        "exit",
        "cliente:exit",
    ],
)
def test_ac18_legitimate_queries_containing_exit_or_salir_are_searched(mock_service, legitimate_query):
    """Verify queries containing exit words without colon command syntax are treated as queries (AC-18, A-12)."""
    session = InteractiveSession(service=mock_service)
    assert session.is_exit_command(legitimate_query) is False

    outputs: List[str] = []
    inputs = iter([legitimate_query, ":salir"])

    session.input_fn = lambda prompt: next(inputs)
    session.output_fn = outputs.append
    session.run()

    # Banner + 1 search result output
    assert len(outputs) == 2
    assert outputs[0] == WELCOME_BANNER
    assert "Total de coincidencias:" in outputs[1]


def test_ac19_eof_error_terminates_gracefully(mock_service):
    """Verify EOFError (Ctrl+D) terminates session without exception (AC-19, EH-05)."""
    outputs: List[str] = []

    def raise_eof(prompt: str) -> str:
        raise EOFError()

    session = InteractiveSession(
        service=mock_service,
        input_fn=raise_eof,
        output_fn=outputs.append,
    )
    # Must not raise EOFError
    session.run()
    assert outputs == [WELCOME_BANNER]


def test_ac19_keyboard_interrupt_terminates_gracefully(mock_service):
    """Verify KeyboardInterrupt (Ctrl+C) terminates session without exception (AC-19, EH-05)."""
    outputs: List[str] = []

    def raise_sigint(prompt: str) -> str:
        raise KeyboardInterrupt()

    session = InteractiveSession(
        service=mock_service,
        input_fn=raise_sigint,
        output_fn=outputs.append,
    )
    # Must not raise KeyboardInterrupt
    session.run()
    assert outputs == [WELCOME_BANNER]


def test_default_session_initialization():
    """Verify InteractiveSession initializes with default dependencies."""
    session = InteractiveSession()
    assert isinstance(session.service, SearchService)
    assert session.input_fn is input
    assert session.output_fn is print


def test_default_session_uses_real_builtin_input(monkeypatch, capsys):
    """Verify the default session reads from builtins.input at runtime (AC-16, AC-18)."""
    prompts: List[str] = []
    inputs = iter(["carlos", ":salir"])

    def fake_input(prompt: str) -> str:
        prompts.append(prompt)
        return next(inputs)

    monkeypatch.setattr("builtins.input", fake_input)

    session = InteractiveSession()
    session.run()

    assert prompts == [PROMPT, PROMPT]
    stdout = capsys.readouterr().out
    assert WELCOME_BANNER in stdout
    assert "Total de coincidencias:" in stdout
