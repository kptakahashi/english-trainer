"""Lint etiquette that ruff cannot check itself. Copied from Brain (tests/test_lint_hygiene.py).

- A suppression comment (ruff `noqa`, `pyright: ignore`, `type: ignore`) names its rule and carries a reason, so the next
  reader can judge whether the exception still holds. File-wide `# ruff: noqa` is never allowed.
- Every test asserts something (or expects an exception). A test that only runs code is a test that cannot fail.
"""

from __future__ import annotations

import ast
import io
import re
import tokenize
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRS = [ROOT / "tools", ROOT / "tests"]
# A rule list, then " - " and at least one word of reason.
NOQA_WITH_REASON = re.compile(r"noqa: [A-Z]+[0-9]+(, [A-Z]+[0-9]+)* - \S")
TYPE_IGNORE_WITH_REASON = re.compile(r"(pyright|type): ignore\[[A-Za-z_, -]+\] - \S")
FILE_WIDE_NOQA = re.compile(r"(ruff|flake8)\s*:\s*noqa")


def _comments(path: Path) -> list[tuple[int, str]]:
    tokens = tokenize.generate_tokens(io.StringIO(path.read_text(encoding="utf-8")).readline)
    return [(tok.start[0], tok.string) for tok in tokens if tok.type == tokenize.COMMENT]


def _is_bad_noqa(comment: str) -> bool:
    text = comment.lower()
    if "noqa" in text:
        return bool(FILE_WIDE_NOQA.search(text)) or not NOQA_WITH_REASON.search(comment)
    if ": ignore" in text:
        return not TYPE_IGNORE_WITH_REASON.search(comment)
    return False


def _bare_noqa_comments(path: Path) -> list[str]:
    return [f"{path.relative_to(ROOT).as_posix()}:{lineno}" for lineno, text in _comments(path) if _is_bad_noqa(text)]


def _expects_something(fn: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    for node in ast.walk(fn):
        if isinstance(node, ast.Assert):
            return True
        if isinstance(node, ast.withitem) and "raises" in ast.unparse(node.context_expr):
            return True
    return False


def _tests_without_assertion(path: Path) -> list[str]:
    nodes = ast.walk(ast.parse(path.read_text(encoding="utf-8")))
    tests = [n for n in nodes if isinstance(n, ast.FunctionDef | ast.AsyncFunctionDef) and n.name.startswith("test_")]
    return [f"{path.name}:{fn.lineno} {fn.name}" for fn in tests if not _expects_something(fn)]


def test_every_noqa_names_its_rule_and_reason():
    bare = [line for d in SOURCE_DIRS for p in d.rglob("*.py") for line in _bare_noqa_comments(p)]
    assert not bare, f"write `noqa: RULE - why` on these lines: {bare}"


def test_every_test_asserts_or_expects_an_exception():
    silent = [name for p in (ROOT / "tests").rglob("test_*.py") for name in _tests_without_assertion(p)]
    assert not silent, f"these tests cannot fail; add an assert or pytest.raises: {silent}"


def test_detects_a_bare_noqa():
    assert _is_bad_noqa("# noqa: E501")
    assert _is_bad_noqa("# noqa")
    assert _is_bad_noqa("# NOQA: E501")
    assert _is_bad_noqa("# ruff: noqa: F401 - even with a reason, a whole file is too much")
    assert _is_bad_noqa("# noqa: F401  (register tables)")
    assert _is_bad_noqa("# pyright: ignore[reportAssignmentType]")
    assert _is_bad_noqa("# type: ignore[attr-defined]")
    assert not _is_bad_noqa("# noqa: E501 - long URL")
    assert not _is_bad_noqa("# noqa: BLE001, S112 - skipped on purpose")
    assert not _is_bad_noqa("# pyright: ignore[reportAssignmentType] - library typing")
    assert not _is_bad_noqa("# type: ignore[assignment] - SDK types it as object")
    assert not _is_bad_noqa("# plain comment")


def test_detects_a_test_without_assertion():
    src = "def test_runs():\n    f()\n\ndef test_raises():\n    with pytest.raises(ValueError):\n        f()\n"
    fns = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef)]
    assert [_expects_something(fn) for fn in fns] == [False, True]
