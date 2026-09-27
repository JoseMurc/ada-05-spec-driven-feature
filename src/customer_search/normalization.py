"""Text normalization utilities for customer search."""

import unicodedata


def remove_diacritics(text: str) -> str:
    """Remove diacritics (accents, umlauts, circumflexes, etc.) from text.

    Uses NFKD decomposition to separate characters from their combining
    diacritical marks, and filters out combining marks (category 'Mn').
    """
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")


def normalize_text(text: str) -> str:
    """Normalize text by removing diacritics and converting to lowercase.

    Args:
        text: Input string.

    Returns:
        Normalized string in lowercase without diacritics.
    """
    return remove_diacritics(text).lower()


def normalize_query(query: str) -> str:
    """Normalize search query.

    Strips leading and trailing whitespace while preserving internal
    whitespace (SR-04), then removes diacritics and converts to lowercase (SR-03).

    Args:
        query: Raw search query string.

    Returns:
        Normalized query string.
    """
    return normalize_text(query.strip())
