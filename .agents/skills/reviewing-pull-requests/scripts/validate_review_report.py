"""Deterministic structural validator for a PR readiness review report.

Checks presence of required sections only; never judges content quality.
"""

import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    ("Review Context", r"^##\s*Review Context\s*$"),
    (
        "Requirements / Acceptance Criteria Reviewed",
        r"^##\s*Requirements\s*/\s*Acceptance Criteria Reviewed\s*$",
    ),
    ("Test Evidence", r"^##\s*Test Evidence\s*$"),
    ("MUST FIX", r"^##\s*MUST FIX\s*$"),
    ("SHOULD FIX", r"^##\s*SHOULD FIX\s*$"),
    ("OPTIONAL", r"^##\s*OPTIONAL\s*$"),
    ("Final Review Summary", r"^##\s*Final Review Summary\s*$"),
]

HUMAN_DECISION_PATTERN = r"^Human decision required\s*:"


def find_missing_sections(text: str) -> list[str]:
    """Return the labels of required sections absent from the report text."""
    missing = [
        label
        for label, pattern in REQUIRED_SECTIONS
        if not re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
    ]
    if not re.search(HUMAN_DECISION_PATTERN, text, re.MULTILINE | re.IGNORECASE):
        missing.append("Human decision required")
    return missing


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv

    if len(argv) != 1:
        print("Usage: validate_review_report.py <path-to-report.md>")
        return 2

    report_path = Path(argv[0])
    if not report_path.is_file():
        print(f"INVALID: file not found: {report_path}")
        return 1

    text = report_path.read_text(encoding="utf-8")
    missing = find_missing_sections(text)

    if missing:
        for section in missing:
            print(f"MISSING: {section}")
        print(f"INVALID: PR readiness review is missing {len(missing)} required section(s).")
        return 1

    print("VALID: PR readiness review structure is complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
