"""Command-line interface (CLI) for customer search."""

import argparse
import sys
from typing import Optional, Sequence

from customer_search.search_service import SearchService


def build_parser() -> argparse.ArgumentParser:
    """Build argument parser for customer search CLI."""
    parser = argparse.ArgumentParser(
        description="Search customers by name or email.",
    )
    parser.add_argument(
        "query",
        nargs="?",
        default="",
        help="Search query to match against customer name or email.",
    )
    return parser


def format_output(result) -> str:
    """Format SearchResult into user-facing text output.

    Translates each status (OK, EMPTY_QUERY, NO_RESULTS) into the appropriate
    channel presentation.
    """
    if result.status == "EMPTY_QUERY":
        return "Consulta vacía. Ingrese un término de búsqueda para consultar clientes."

    if result.status == "NO_RESULTS":
        return result.message or "No se encontraron clientes."

    # Status: OK
    lines = [
        f"Total de coincidencias: {result.total}",
        f"Mostrando {len(result.items)} resultados:",
        "-" * 40,
    ]
    for item in result.items:
        lines.append(f"[{item.cliente_id}] {item.nombre} <{item.email}>")
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None, service: Optional[SearchService] = None) -> int:
    """CLI entry point.

    Args:
        argv: Command-line arguments. Defaults to sys.argv[1:].
        service: Optional SearchService instance for dependency injection.

    Returns:
        Exit code (0 for completed search interaction).
    """
    parser = build_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    search_service = service or SearchService()
    result = search_service.search(args.query)

    output = format_output(result)
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
