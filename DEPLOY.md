# English Trainer — 公開とインストール

## 公開済み

| | |
|---|---|
| アプリURL | **https://kptakahashi.github.io/english-trainer/** |
| リポジトリ | https://github.com/kptakahashi/english-trainer (Public) |
| Pages | GitHub Actions(`.github/workflows/pages.yml`)。main に入ると `pwa/` を作って公開 |

公開は GitHub Actions が行う(`decisions/0001`)。手でファイルをアップロードしない。

---

## スマホにインストールする

1. AndroidのChromeで上のURLを開く
2. 右上の **⋮** メニュー
3. **「アプリをインストール」**（または「インストール」）を選ぶ
   - ここが **「ホーム画面に追加」としか出ない場合**は、まだPWAとして
     認識されていません。URL末尾の `/` の有無を確認し、再読み込みしてください
4. **前に作ったChromeバッジ付きのショートカットは削除**する

これで、独自アイコン・バッジなし・アドレスバーなし・オフライン起動可、になります。

---

---

## アプリを更新するとき

編集するのは **`app/index.html` だけ**です。`pwa/index.html` は作られるもの(git に入れない)なので直接触らないこと。

1. ブランチを切って `app/index.html` を直す。手元で見るときは `python tools/build_pwa.py` で `pwa/index.html` を作る
2. `pwa/sw.js` の `var CACHE = "english-trainer-v1"` の版番号を 1 つ上げる(上げないと古い画面がキャッシュから出続けます)
3. PR を出し、CI(ESLint・ruff・pyright・pytest)が通って diff を読んだらマージする。main に入ると Actions が `pwa/` を作って Pages に出す
4. スマホでアプリを一度閉じて開き直す

アイコンのデザインを変えたときは `python tools/make_icons.py` を先に流します。
