# decisions/ — 決めたことの記録

結果を見て方針を固定した・変えたとき、1 件 1 ファイル。番号は連番、消さない。覆すときは新しい番号で書き、古い方の先頭に「→ NNNN で置き換え」と足す。
`CLAUDE.md` の絶対ルールは、ここで決まったことの要約。decision を書いたら CLAUDE.md を見直す。
プロジェクトをまたぐ判断は、元の decision を「出典: hub#NNNN」「出典: wellness-app#NNNN」で参照する。本文はコピーしない。

## 一覧

| 番号 | 決定 | 日付 | 状態 |
|---|---|---|---|
| [0001](0001-one-public-repo.md) | コードは公開リポジトリ english-trainer 1 つに置き、画面は GitHub Actions で作って Pages に出す | 2026-10-30 | 有効 |

## ほかのリポジトリにある、この English に効く判断

| 判断 | 置き場 |
|---|---|
| 有料のキー付き API を持たない | wellness-app#0002 |
| Claude Code は手元の PC でだけ動かす。スマホからは Remote Control | hub#0001 |
| 開発するのは 5 つ。English は英語力 | hub#0002 |

## 書き方

```markdown
# NNNN: (決定を 1 行で)

日付: YYYY-MM-DD
状態: 下書き | 有効 | → NNNN で置き換え
出典: #issue / PR / plans/...

## 文脈
## 決定
## 理由
## 捨てた案
## 影響
```
