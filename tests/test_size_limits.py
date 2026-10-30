"""File size limit: 400 lines per file; ruff has no such rule, so the test is the machine check.

No file is over the limit today, so there is no ratchet list. Split a file instead of adding one.
"""

from pathlib import Path

MAX_LINES = 400
ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRS = [ROOT / "tools", ROOT / "tests"]


def _line_counts() -> dict[str, int]:
    return {p.relative_to(ROOT).as_posix(): len(p.read_text(encoding="utf-8").splitlines()) for d in SOURCE_DIRS for p in d.rglob("*.py")}


def test_no_file_over_the_limit():
    over = {name: n for name, n in _line_counts().items() if n > MAX_LINES}
    assert not over, f"split these files (limit {MAX_LINES} lines): {over}"


def test_counts_the_checks_themselves():
    assert "tools/build_pwa.py" in _line_counts()
