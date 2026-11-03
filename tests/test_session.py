"""Unit tests for InteractiveSession controller."""

from typing import Callable, Iterable, List
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


class SpyRepository(MockRepository):
    """Mock repository that counts how many times the catalog is read."""

    def __init__(self, customers: list[Customer]) -> None:
        super().__init__(customers)
        self.find_all_calls = 0

    def find_all(self) -> list[Customer]:
        self.find_all_calls += 1
        return super().find_all()


class SpySearchService(SearchService):
    """SearchService that records every query it receives."""

    def __init__(self, repository: SpyRepository) -> None:
        super().__init__(repository=repository)
        self.queries: list[str] = []

    def search(self, query: str):
        self.queries.append(query)
        return super().search(query)


def scripted_input(lines: Iterable[str]) -> Callable[[str], str]:
    """Return an input_fn that yields the given lines, then raises EOFError.

    Raising EOFError once the script is exhausted ends the session, so a
    regression that ignores an exit command fails the test instead of hanging.
    """
    remaining = iter(lines)

    def fake_input(prompt: str) -> str:
        try:
            return next(remaining)
        except StopIteration:
            raise EOFError() from None

    return fake_input


CUSTOMERS = [
    Customer("C-1", "Carlos Gómez", "carlos.gomez@example.com"),
    Customer("C-2", "Ana Martínez", "ana@example.com"),
    Customer("C-3", "Elena Salir", "exit.user@domain.com"),
    Customer("C-4", "Cliente Exit", "cliente:exit@domain.com"),
]


@pytest.fixture
def mock_service() -> SearchService:
    return SearchService(repository=MockRepository(CUSTOMERS))


@pytest.fixture
def spy_service() -> SpySearchService:
    return SpySearchService(repository=SpyRepository(CUSTOMERS))


def test_ac15_welcome_banner_content():
    """Verify welcome banner contains expected text and exit command instructions."""
    assert "Bienvenido a buscador de clientes" in WELCOME_BANNER
    assert ":salir" in WELCOME_BANNER
    assert ":exit" in WELCOME_BANNER


def test_ac15_banner_printed_on_run(mock_service):
    """Verify welcome banner is printed first upon session start (AC-15, SR-11)."""
    outputs: List[str] = []
    inputs = scripted_input([":salir"])

    session = InteractiveSession(
        service=mock_service,
        input_fn=inputs,
        output_fn=outputs.append,
    )
    session.run()

    assert len(outputs) >= 1
    assert outputs[0] == WELCOME_BANNER


def test_ac16_prompt_and_single_search(mock_service):
    """Verify prompt text and single search result output (AC-16, SR-12)."""
    prompts_received: List[str] = []
    outputs: List[str] = []
    inputs = scripted_input(["carlos", ":salir"])

    def fake_input(prompt: str) -> str:
        prompts_received.append(prompt)
        return inputs(prompt)

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
    inputs = scripted_input(["carlos", "ana", ":exit"])

    session = InteractiveSession(
        service=mock_service,
        input_fn=inputs,
        output_fn=outputs.append,
    )
    session.run()

    assert len(outputs) == 3  # Banner + 2 search outputs
    assert "[C-1] Carlos Gómez" in outputs[1]
    assert "[C-2] Ana Martínez" in outputs[2]


def test_ac17_empty_query_keeps_session_active(mock_service):
    """Verify empty query displays message and keeps session active for next query (AC-17, SR-13)."""
    outputs: List[str] = []
    inputs = scripted_input(["   ", "carlos", ":salir"])

    session = InteractiveSession(
        service=mock_service,
        input_fn=inputs,
        output_fn=outputs.append,
    )
    session.run()

    assert len(outputs) == 3
    assert "vacía" in outputs[1].lower()
    assert "[C-1] Carlos Gómez" in outputs[2]


def test_ac17_no_results_keeps_session_active(mock_service):
    """Verify no-results query displays fixed message and keeps session active (AC-17, SR-13)."""
    outputs: List[str] = []
    inputs = scripted_input(["termino_inexistente_xyz", "carlos", ":exit"])

    session = InteractiveSession(
        service=mock_service,
        input_fn=inputs,
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
def test_ac18_exit_commands_terminate_session(spy_service, exit_cmd):
    """Verify exit commands terminate the session without querying service or repository (AC-18, SR-14, VR-04, A-12)."""
    outputs: List[str] = []
    # The extra query after the exit command must never be read or searched.
    session = InteractiveSession(
        service=spy_service,
        input_fn=scripted_input([exit_cmd, "carlos"]),
        output_fn=outputs.append,
    )
    assert session.is_exit_command(exit_cmd) is True

    session.run()

    assert outputs == [WELCOME_BANNER]
    assert spy_service.queries == []
    assert spy_service.repository.find_all_calls == 0


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
def test_ac18_legitimate_queries_containing_exit_or_salir_are_searched(spy_service, legitimate_query):
    """Verify queries containing exit words without colon command syntax are treated as queries (AC-18, A-12)."""
    outputs: List[str] = []
    session = InteractiveSession(
        service=spy_service,
        input_fn=scripted_input([legitimate_query, ":salir"]),
        output_fn=outputs.append,
    )
    assert session.is_exit_command(legitimate_query) is False

    session.run()

    # Banner + 1 search result output
    assert len(outputs) == 2
    assert outputs[0] == WELCOME_BANNER
    assert "Total de coincidencias:" in outputs[1]
    assert spy_service.queries == [legitimate_query]


@pytest.mark.parametrize(
    "not_a_command",
    [
        ":salir ahora",
        "::exit",
        ":exit:",
        ": salir",
        ":sa lir",
        "salir:",
        ":salir\t:exit",
        ":exit\nmás",
    ],
)
def test_ac18_text_containing_exit_commands_is_searched_literally(spy_service, not_a_command):
    """Verify text that contains but is not exactly an exit command is a literal search term (VR-04, A-12)."""
    outputs: List[str] = []
    session = InteractiveSession(
        service=spy_service,
        input_fn=scripted_input([not_a_command, ":exit"]),
        output_fn=outputs.append,
    )
    assert session.is_exit_command(not_a_command) is False

    session.run()

    # The term was searched verbatim and the session stayed active until ":exit".
    assert spy_service.queries == [not_a_command]
    assert len(outputs) == 2
    assert outputs[0] == WELCOME_BANNER


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
    inputs = scripted_input(["carlos", ":salir"])

    def fake_input(prompt: str) -> str:
        prompts.append(prompt)
        return inputs(prompt)

    monkeypatch.setattr("builtins.input", fake_input)

    session = InteractiveSession()
    session.run()

    assert prompts == [PROMPT, PROMPT]
    stdout = capsys.readouterr().out
    assert WELCOME_BANNER in stdout
    assert "Total de coincidencias:" in stdout
