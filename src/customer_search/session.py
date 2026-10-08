"""Interactive terminal session controller for customer search."""

from typing import Callable, Optional

from customer_search.cli import format_output
from customer_search.search_service import SearchService

WELCOME_BANNER: str = (
    "Bienvenido a buscador de clientes\n"
    "Comandos de salida disponibles: :salir, :exit (o Ctrl+C / Ctrl+D)"
)

EXIT_COMMANDS: set[str] = {":salir", ":exit"}

PROMPT: str = "Buscar cliente: "


class InteractiveSession:
    """Controller managing the interactive search session (REPL)."""

    def __init__(
        self,
        service: Optional[SearchService] = None,
        input_fn: Callable[[str], str] = input,
        output_fn: Callable[[str], None] = print,
    ) -> None:
        """Initialize InteractiveSession with injectable service and I/O callables.

        Args:
            service: Optional SearchService instance. Defaults to new SearchService.
            input_fn: Callable prompting user for input. Defaults to builtins.input.
            output_fn: Callable writing output string. Defaults to builtins.print.
        """
        self.service = service or SearchService()
        self.input_fn = input_fn
        self.output_fn = output_fn

    def is_exit_command(self, text: str) -> bool:
        """Check if text is an explicit exit command (VR-04, A-12).

        Args:
            text: Raw input string.

        Returns:
            True if text (after stripping whitespace and case-folding) is ':salir' or ':exit'.
        """
        return text.strip().lower() in EXIT_COMMANDS

    def handle_input(self, raw_input: str) -> bool:
        """Process a single input line.

        Args:
            raw_input: Raw query or command entered by the user.

        Returns:
            True to continue the interactive session, False to terminate it.
        """
        if self.is_exit_command(raw_input):
            return False

        result = self.service.search(raw_input)
        output = format_output(result)
        self.output_fn(output)
        return True

    def run(self) -> None:
        """Run the interactive session loop (SR-10, SR-11, SR-12, SR-14)."""
        self.output_fn(WELCOME_BANNER)

        while True:
            try:
                raw_input = self.input_fn(PROMPT)
            except (EOFError, KeyboardInterrupt):
                # EH-05, AC-19: Graceful termination on interrupt or EOF
                break

            if not self.handle_input(raw_input):
                break
