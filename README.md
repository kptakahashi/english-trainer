# English Trainer

**目標**: Cambridge C1 Advanced / 英語でビジネスができる状態
**現在の課題**: アウトプットの質と速度
**構成**: 音声会話は ChatGPT アプリに任せ、お題の提示・プロンプト生成・語彙SRS・弱点集計を自作アプリが担う。

---

## ファイル

| ファイル | 用途 |
|---|---|
| [chatgpt/01-project-instructions.md](chatgpt/01-project-instructions.md) | ChatGPT の Project 指示欄に貼る（初回のみ） |
| [chatgpt/02-kickoff-prompt.md](chatgpt/02-kickoff-prompt.md) | 毎回のセッション開始プロンプト |
| [chatgpt/03-end-session-prompt.md](chatgpt/03-end-session-prompt.md) | 終了時のレポート生成プロンプト |
| [topics/topics-ladder.md](topics/topics-ladder.md) | お題48本（上から順に消化） |
| [vocab/phrasebank.md](vocab/phrasebank.md) | 機能別フレーズ（TARGET PHRASES の供給源） |
| `logs/` | 日々のレポートJSON置き場 |
| [app/index.html](app/index.html) | **アプリ本体（唯一の編集対象）** |
| [pwa/](pwa/) | Pages に出すもの。`index.html` は Actions が `app/index.html` から作る(git に入れない)。`sw.js`・manifest・アイコンは手で持つ |
| [DEPLOY.md](DEPLOY.md) | 公開の仕組み、スマホへのインストール、更新の手順 |
| [CLAUDE.md](CLAUDE.md) | 開発のルールと、完了前に通す検査 |
| `tools/` | `build_pwa.py`（PWA生成）、`make_icons.py`（アイコン生成） |

---

## 初回セットアップ（15分・1回だけ）

1. Android の ChatGPT アプリで **Projects → 新規作成**（名前: `English Trainer`）
2. Project の「指示」に `chatgpt/01-project-instructions.md` の `---` 以降を貼る
3. **動作確認**: そのProject内で新規チャット →「What are your rules for our conversations?」と聞く
   → ルールを答えれば成功。答えなければ Project指示が効いていないので、
   毎回 kickoff プロンプトをテキストで送る運用にする（下記の手順どおりなら問題なし）
4. ホーム画面に **ChatGPTウィジェット**を置く（音声ボタン付きのもの）。1タップで音声起動できる
5. `phrasebank.md` のグループ1を今日の TARGET PHRASES に設定

---

## 毎日の手順（20分）

### ① 準備 3分
- `topics-ladder.md` から今日のお題（上から順）
- `phrasebank.md` から今週のグループの3フレーズ
- `02-kickoff-prompt.md` のテンプレを埋めて **コピー**

### ② 開始
- ChatGPTアプリ → English Trainer プロジェクト → 新規チャット
- kickoff プロンプトを**テキストで送信**（まだ音声にしない）
- 返事が来たら **マイクボタンで音声モードへ**

### ③ 会話 12分
- タイマーを12分。時間が来たら途中でも切る
- **原則: 沈黙しても日本語に逃げない。** 詰まったら `Let me put that another way,` で仕切り直す
- 相手が反論してきたら、必ず一度は正面から受けて返す（話題を変えて逃げない）

### ④ レポート 1分
- 音声モードを**終了**（重要：JSONを読み上げられる）
- 同じチャットに `03-end-session-prompt.md` をテキストで貼る
- 出力JSONを `logs/2026-08-30.json` のように保存

### ⑤ 復習 4分
- `upgrades` の5件を**声に出して3回**言う（読むだけでは定着しない）
- `reached_for_but_missed` を明日の TARGET PHRASES に入れる
- `errors` の同じtypeが3日続いたら、それが今週の重点課題

---

## Phase 0 の合格ライン（2〜3週間後）

これが満たせたら Phase 1（PWA実装）に進む価値がある：

- [ ] 12分の会話を日本語ゼロで完走できる
- [ ] レポートJSONが10本以上たまっている
- [ ] `errors` の頻出typeが自分で言えるようになっている
- [ ] 手作業が面倒になっている ← **これが一番重要なシグナル**

最後の項目が「面倒じゃない」なら、アプリを作る意味はまだ薄い。まず運用が回るか試す。

---

## Phase 1 で自動化する予定のもの

- お題とフレーズの自動出題（ラダー進行 + 再走管理）
- kickoff プロンプトのワンタップ生成 → クリップボード → ChatGPT起動（Android intent）
- レポートJSON貼り付け → パース → 語彙SRSへ自動投入
- `upgrades` / `reached_for_but_missed` の口頭アウトプット型SRS（和文→英語を声で）
- errors の type 別集計グラフ、連続日数
