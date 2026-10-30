## 何を

<!-- 1 つの意図を 1〜2 行で。関連: Closes #N / plans/YYYY-MM-DD-名前.md -->

## なぜ

<!-- 課題のどの事実に対する対策か -->

## リスク・トレードオフ

<!-- この変更で失うもの、気をつけること -->

## どう検証したか

- [ ] `npm run lint` / `ruff check` / `ruff format --check` / `pyright` / `pytest` が通る(CI 緑)
- [ ] 画面を変えたら `pwa/sw.js` の CACHE の版を上げた
- [ ] 手元で `python tools/build_pwa.py` を回して画面を開いた(何を見たか 1 行)

## やらなかったこと

<!-- 意図的に含めなかったもの。次の PR か、やらない -->
