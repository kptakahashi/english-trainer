# English Trainer

英語のアウトプット訓練アプリ(目標と使い方は README)。音声会話は ChatGPT アプリに任せ、お題・プロンプト生成・語彙 SRS・弱点集計をこのアプリが担う。画面は `app/index.html` 1 枚(HTML の中に JS)、`tools/build_pwa.py` で `pwa/` を作り、GitHub Actions が Pages に出す(`decisions/0001`)。

## コマンド

```bash
npm run lint && .venv/Scripts/python -m ruff check . && .venv/Scripts/python -m ruff format --check . && .venv/Scripts/python -m pyright && .venv/Scripts/python -m pytest
```

**IMPORTANT**: コードを変えたら、完了と言う前に必ず上を全部通す。同じ列が `git commit` 前の hook(`.githooks/pre-commit`)と CI でも走る

- 初回だけ: `npm ci && py -3.14 -m venv .venv && .venv/Scripts/python -m pip install -r requirements-dev.txt && git config core.hooksPath .githooks`
- 画面を手元で見る: `python tools/build_pwa.py` のあと `.claude/launch.json` の `pwa`

## 機械が止めること(ここには書かない)

- JS: `eslint.config.mjs`。いちばんの狙いは XSS。データから作る HTML は必ず `esc()` を通す。例外は 1 行ずつ `// eslint-disable-next-line 規則 -- 理由`(理由が無い・要らない例外も止まる)
- Python: `pyproject.toml`(ruff, pyright strict)と `tests/test_size_limits.py`(ファイル 400 行)・`tests/test_lint_hygiene.py`(noqa の理由、assert の無いテスト)
- 公開してはいけないもの: `.githooks/pre-commit` が `logs/`(学習の記録)・`.env`・秘密らしき文字列を止める
- 上限はラチェット。緩めるときは理由を書いた単独の PR で
- 新しい関数には必ずテスト。判定や組み立ては純粋な関数に分ける

## 絶対ルール

- NEVER: キー付きの有料 API を使わない。課金が要る提案もしない(出典: wellness-app#0002)
- NEVER: このリポジトリは公開(`decisions/0001`)。学習の記録(`logs/` の JSON、会話の中身、弱点の数字)と本人の生活の具体を、コード・文書・issue・PR・commit に書かない
- 開発は手元の PC と Remote Control でだけ行う(出典: hub#0001)
- 編集するのは `app/index.html`。`pwa/index.html` は作られるもので、git に入れない。画面を変えたら `pwa/sw.js` の CACHE の版を上げる
- 公開する URL とパス(`/english-trainer/`)を変えない。スマホに入れたアプリが迷子になる
- 機能は足す前に消す。YAGNI。使っていない自分の不便から出た要望だけ実装する
- 小さく刻む。1 PR = 1 意図。ゼロから書き直さない
- 「動く」と「正しい・安全」は別。diff を読み、裏を取り、未読でマージしない
- 仕様・コマンド・手順を変えたら、この CLAUDE.md と README・DEPLOY.md を同じ PR で直す
- 同じ指摘が 2 回出たらここか lint に落とす

## 記録の流儀(詳細は docs/workflow.md)

チャットは消える。課題 → Issue、対策 → `plans/`、実装 → PR(`Closes #N`、検証結果を本文に)、結果 → issue を閉じるコメント、判断 → `decisions/`。

- 本人が決める欄: plan の「やらないこと」「検証方法」、issue を閉じるか、decision の「決定」。Claude は下書きしてよいが、本人が承認するまで「下書き」のまま
- 提案・plan は、項目ごとに「何を/なぜ/リスク・トレードオフ」を書き、推す案を 1 つ示す
- main は PR でだけ変える。小さな直しも PR(issue と plan は要らない)
- 決定や plan に無いことはやらず、plan の「メモ」に書いて止まる
