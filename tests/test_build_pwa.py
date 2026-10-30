"""tools/build_pwa.py: app/index.html の断片を、Pages に置ける完全な HTML 文書に包む。"""

from pathlib import Path

import pytest
from build_pwa import SRC, build_document

FRAGMENT = "<style>body{}</style>\n<main>本文</main>\n<script>var x = 1;</script>\n"


def test_wraps_the_fragment_into_a_document():
    doc = build_document(FRAGMENT)
    assert doc.startswith('<!doctype html>\n<html lang="ja">\n<head>\n')
    assert doc.endswith("</body>\n</html>\n")
    head, body = doc.split("</head>")
    assert "<style>body{}</style>" in head
    assert "<main>本文</main>" in body


def test_adds_the_manifest_and_service_worker():
    doc = build_document(FRAGMENT)
    assert '<link rel="manifest" href="./manifest.webmanifest">' in doc
    assert 'navigator.serviceWorker.register("./sw.js")' in doc


def test_stops_when_the_fragment_has_no_style():
    with pytest.raises(ValueError, match="</style>"):
        build_document("<main>本文</main>")


def test_the_real_app_builds():
    doc = build_document(Path(SRC).read_text(encoding="utf-8"))
    assert doc.count("<html") == 1
    assert "function esc(" in doc
