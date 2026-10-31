# English の開発環境を Wellness app と同じ型にそろえる

状態: 完了(english-trainer#1、2026-10-31)
課題: なし(hub#0002「5 つとも Wellness app と同じ開発環境に揃える」の実施)
期限: 2026-11-06

## 目的

English を git と PR で管理し、JS と Python を機械で止める状態にする。完成品は手でアップロードせず、GitHub Actions で作って Pages に出す(`decisions/0001`)。

## いまの差

| | Wellness app | English |
|---|---|---|
| git・PR | ある | **無い**(完成品だけを手でアップロード) |
| 記録の 5 か所(issue・plans・PR・結果・decisions)と CLAUDE.md | ある | **無い** |
| lint・型・テスト | ある(Python) | **無い**(JS は `app/index.html` の中、Python は `tools/` の 2 本) |
| commit 前の hook と CI | ある | **無い** |

## やること

| # | 何を | なぜ |
|---|---|---|
| 1 | `C:\English` を git にし、`english-trainer` の今の履歴の上に、コード一式を足す。`pwa/index.html`(作られるもの)と `logs/` は `.gitignore` | 履歴を残したまま、手でのアップロードをやめる |
| 2 | `.github/workflows/pages.yml`: main に入ったら `tools/build_pwa.py` で `pwa/index.html` を作り、`pwa/` を Pages に出す | 出したものと、元のコードが必ず一致するようにする |
| 3 | Pages の公開元を「main の直下」から「GitHub Actions」に切り替える(PR のマージの直前) | 切り替えないと、マージ後に Pages が README などを出してしまう |
| 4 | Wellness app と同じ記録の型: CLAUDE.md、AGENTS.md、`docs/workflow.md`、`decisions/`、`plans/`、issue と PR のテンプレート | どのプロジェクトでも同じ場所を見れば分かるようにする |
| 5 | JS: brain-app と同じ ESLint の規則(`esc()` を通さない HTML、`eval` を止める)。HTML の中の JS は `eslint-plugin-html` で検査 | `innerHTML` の付け忘れを、人ではなく機械が止める |
| 6 | Python: `tools/` に ruff・pyright・pytest。`build_pwa.py` の組み立てを純粋な関数に分けてテストを書く | 完成品を作る道具が壊れたら、出す前に止める |
| 7 | 同じ検査を `.githooks/pre-commit` と CI で回す。pre-commit は `logs/` と秘密らしき文字列も止める | 学習の記録が公開リポジトリに入るのを止める |

## やらないこと

| 何を | なぜやらないか | リスク・トレードオフ |
|---|---|---|
| アプリの機能を変える | 1 plan = 1 意図。開発環境だけ | なし |
| `app/index.html` の JS を別ファイルに切り出す | 作り直しになる。`eslint-plugin-html` で今の形のまま検査できる | 800 行の HTML の中に JS がある形のまま |
| CSP を足す | 振る舞いが変わりうる(インラインの JS が止まる)。別の plan で | XSS の 2 枚目の壁がまだ無い。外部への通信も鍵も無いので、漏れるものは小さい |
| `.claude/settings.json` に hook を足す | Claude の自己設定の変更になる | 止めるのは pre-commit と CI だけ |
| アイコンを作り直す(`tools/make_icons.py`) | 変わらないので、今の PNG をそのまま commit する | なし |

## 検証方法

- 指標:
  - 手元で ESLint・ruff・pyright・pytest が全部通る。CI も緑
  - わざと違反(`esc()` の無い `innerHTML`、未使用の import)を入れた commit が止まる
  - `logs/` にファイルを置いて commit しようとすると止まる
  - 切り替え後の Pages(`https://kptakahashi.github.io/english-trainer/`)の `index.html` が、手元で作ったものと一致し、スマホのアプリが今までどおり開く
- 期間: 実装の当日
- 効いたと言える線: 上の 4 つが全部そろう

## 作り直しが高いもの(先に決める)

- 公開する URL とパス: 今と同じ `/english-trainer/`。変えるとスマホに入れたアプリ(サービスワーカー)が迷子になる

## 本人がやること

- この plan の「やらないこと」と「検証方法」を確認する
- 切り替え後、スマホのアプリを開いて今までどおり動くかを見る

## メモ
- 2026-10-30: plan から変えたところ
  - `tools/build-pwa.py`・`make-icons.py` を `build_pwa.py`・`make_icons.py` に改名(テストから import するため)。出力は改名前と 1 バイトも変わらない
  - 画面のコードを lint のために少し直した(使わない `catch (e)` の `e` を消す、エラーに元の原因を付ける、innerHTML の例外 4 か所に理由)。振る舞いは変わらないが、規則どおり `pwa/sw.js` の CACHE を v2 に上げた
  - `.github/dependabot.yml` を足した(npm・pip・Actions の更新を PR で知らせる。CI が通れば読んでマージ)
- 2026-10-30: 公開リポジトリは無料プランでもブランチ保護が使える。main を「PR 必須・CI 必須」にするのは、リポジトリの設定の変更なので本人が決める
- 2026-10-30: 試しの commit で、pre-commit の秘密の検査がすり抜けた。`set -o pipefail` の下で `echo … | grep -q` を使うと、grep が早く抜けたときに echo が SIGPIPE で失敗し、「見つからなかった」扱いになる(大きな diff で起きる)。here-string(`<<<`)で渡す形に直し、止まることを確かめた。同じ書き方が wellness-app の `.githooks/pre-commit` にもあるので、別の PR で直す
- 2026-10-30: `pwa/` の中に、手でアップロードしていた頃の git リポジトリ(`pwa/.git`)があった。公開リポジトリと同じ commit を指すだけの重複なので、`C:\old\english-pwa-git-backup` に移した(消していない)
- 2026-10-31: 完了。Pages の公開元を GitHub Actions に切り替えてから #1 をマージした。公開中の `index.html` が手元で作ったものと 1 バイトも違わず、スマホのアプリも今までどおり開いた(本人確認)
- 2026-10-31: main を GitHub のルールで保護した(PR 必須・CI の check 必須・強制 push と削除の禁止)。直接 push が拒否されることを確かめた
