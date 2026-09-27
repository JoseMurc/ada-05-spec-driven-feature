"""Unit tests for text and query normalization."""

from customer_search.normalization import (
    normalize_query,
    normalize_text,
    remove_diacritics,
)


def test_remove_diacritics():
    # Acute, grave, circumflex, diaeresis, tilde
    assert remove_diacritics("José") == "Jose"
    assert remove_diacritics("Hélène") == "Helene"
    assert remove_diacritics("Benoît") == "Benoit"
    assert remove_diacritics("Günther") == "Gunther"
    assert remove_diacritics("Jürgen") == "Jurgen"
    assert remove_diacritics("Iñigo") == "Inigo"


def test_normalize_text():
    assert normalize_text("JOSÉ") == "jose"
    assert normalize_text("José") == "jose"
    assert normalize_text("jose") == "jose"
    assert normalize_text("GÜNTHER") == "gunther"
    assert normalize_text("Hélène Dubois") == "helene dubois"


def test_normalize_query_trim_and_internal_whitespace():
    # Leading and trailing spaces stripped, internal spaces preserved
    assert normalize_query("   ana   ") == "ana"
    assert normalize_query("  Ana   María  ") == "ana   maria"
    assert normalize_query("jose") == "jose"
    assert normalize_query("  ") == ""
