import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED = [
    "AGENTS.md",
    "README.md",
    "REQUIREMENTS.md",
    "SPEC.md",
    "ARCHITECTURE.md",
    "TASKS.md",
    "docs/REPO_MAP.md",
    "results",
]

CORE_DOCS = [
    "README.md", 
    "REQUIREMENTS.md",
    "SPEC.md",
    "ARCHITECTURE.md",
    "TASKS.md",
    "docs/REPO_MAP.md",
]

PATH_EXTENSIONS = {
    "py", "md", "json", "toml", "cfg", "ini", "txt", "sh", "yml", "yaml", "ps1",
}

PATH_PATTERN = re.compile(r"`([^`\s]+)`|\]\(([^)\s]+)\)")


def extract_referenced_paths(text: str) -> set[str]:
    paths = set()
    for backtick_path, link_path in PATH_PATTERN.findall(text):
        candidate = backtick_path or link_path
        if not candidate or "/" not in candidate:
            continue
        candidate = candidate.split("#", 1)[0]
        if candidate.startswith(("http://", "https://", "file:")):
            continue
        extension = candidate.rsplit(".", 1)[-1].lower() if "." in candidate else ""
        if extension not in PATH_EXTENSIONS:
            continue
        paths.add(candidate.rstrip("/"))
    return paths


def main() -> int:
    errors = []

    missing = [path for path in REQUIRED if not (REPO_ROOT / path).exists()]
    for path in missing:
        errors.append(f"Missing required path: {path}")

    for doc in CORE_DOCS:
        doc_path = REPO_ROOT / doc
        if not doc_path.exists():
            continue
        text = doc_path.read_text(encoding="utf-8")
        for referenced in sorted(extract_referenced_paths(text)):
            if not (REPO_ROOT / referenced).exists():
                errors.append(f"{doc} references nonexistent path: {referenced}")

    if errors:
        print("REPO_CONTRACT: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("REPO_CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
