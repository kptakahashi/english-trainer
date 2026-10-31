"""app/index.html から、GitHub Pages に置ける PWA 版を生成する。

app/index.html は Artifact 用（<html>/<head>/<body> を持たない断片）なので、
完全な HTML 文書に包み直し、manifest・アイコン・Service Worker の登録を差し込む。

    python tools/build_pwa.py

アプリを直すときは app/index.html だけを直し、これを流し直すこと。
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "app" / "index.html"
OUT = ROOT / "pwa" / "index.html"

HEAD_EXTRA = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#E8E7E2">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#15161A">
<meta name="description" content="ChatGPTの音声会話とつなぐ英語アウトプット訓練アプリ">
<link rel="manifest" href="./manifest.webmanifest">
<link rel="icon" href="./favicon-64.png" sizes="64x64" type="image/png">
<link rel="apple-touch-icon" href="./icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
"""

SW_REG = """
<script>
if("serviceWorker" in navigator){
  window.addEventListener("load", function(){
    navigator.serviceWorker.register("./sw.js").catch(function(){});
  });
}
</script>
"""


def build_document(src: str) -> str:
    """app/index.html の中身(断片)を、PWA として置ける完全な HTML 文書に包み直す。"""
    # <style>...</style> までが head、それ以降が body。
    m = re.search(r"</style>", src)
    if not m:
        raise ValueError("app/index.html に </style> が見つからない。想定と構造が違う。")  # noqa: TRY003 - 直す人への案内をその場で出す
    head, body = src[: m.end()], src[m.end() :]
    return (
        '<!doctype html>\n<html lang="ja">\n<head>\n'
        + HEAD_EXTRA
        + head.strip()
        + "\n</head>\n<body>\n"
        + body.strip()
        + "\n"
        + SW_REG.strip()
        + "\n</body>\n</html>\n"
    )


def main() -> int:
    try:
        doc = build_document(SRC.read_text(encoding="utf-8"))
    except ValueError as e:
        print(e, file=sys.stderr)
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc, encoding="utf-8", newline="\n")
    print(f"{OUT}  ({OUT.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
