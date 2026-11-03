"""Command-line interface (CLI) for customer search."""

import argparse
import sys
from typing import Optional, Sequence

from customer_search.formatting import format_output
from customer_search.search_service import SearchService
from customer_search.session import InteractiveSession

__all__ = ["build_parser", "format_output", "main"]


def build_parser() -> argparse.ArgumentParser:
    """Build argument parser for customer search CLI."""
    parser = argparse.ArgumentParser(
        description="Search customers by name or email.",
    )
    parser.add_argument(
        "query",
        nargs="?",
        default=None,
        help=(
            "Search query to match against customer name or email. "
            "If omitted, an interactive session is started."
        ),
    )
    return parser


def main(argv: Optional[Sequence[str]] = None, service: Optional[SearchService] = None) -> int:
    """CLI entry point.

    Without a query argument, starts the interactive session (FR-11, SR-10);
    with a query argument, runs a one-shot search (FR-15).

    Args:
        argv: Command-line arguments. Defaults to sys.argv[1:].
        service: Optional SearchService instance for dependency injection.

    Returns:
        Exit code (0 for completed search interaction).
    """
    parser = build_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    search_service = service or SearchService()

    if args.query is None:
        InteractiveSession(service=search_service).run()
        return 0

    result = search_service.search(args.query)

    output = format_output(result)
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
