# セッション終了プロンプト（音声を切ってから、テキストで送る）

**重要**: 音声モードのまま送るとJSONを読み上げられて地獄です。必ず音声を終了し、
同じチャットにテキストで貼ってください。

---

```
END SESSION.

Now review the whole conversation and output a report. Be harsh. I want the things I got
wrong, not encouragement. Output ONLY the JSON, in a code block, nothing before or after.

{
  "date": "YYYY-MM-DD",
  "session_type": "",
  "topic": "",
  "fluency": {
    "verdict": "one blunt paragraph: was I fluent, or was I assembling sentences word by word?",
    "filler_habits": ["fillers and stalling patterns I actually used"],
    "self_repair_count": 0,
    "estimated_level": "B1 / B2 / B2+ / C1"
  },
  "errors": [
    { "said": "what I actually said", "fix": "the correct version", "why": "one short line", "type": "grammar|word choice|collocation|preposition|tense|article" }
  ],
  "upgrades": [
    { "plain": "the flat/simple thing I said", "refined": "how a C1 speaker would say it", "register": "neutral|formal|business|conversational", "note": "why it lands better" }
  ],
  "reached_for_but_missed": [
    { "meaning_ja_or_en": "the idea I was clearly struggling to express", "english": "the phrase I needed" }
  ],
  "new_lexis": [
    { "item": "word or chunk", "meaning_en": "short definition", "example": "a sentence using it about ME, from this conversation" }
  ],
  "target_phrase_usage": [
    { "phrase": "", "used": true, "naturally": true }
  ],
  "next_session": { "type": "", "topic": "", "reason": "which weakness this attacks" }
}

Rules for the report:
- "errors": every real error, up to 12. Do not soften them. Skip pure pronunciation.
- "upgrades": exactly 5. This is the most important section. Take things I said that were
  correct but flat, and show me the version that sounds like someone who works in English.
- "reached_for_but_missed": moments where I stalled, circled, or gave up on an idea.
- "new_lexis": 5-8 items, drawn from THIS conversation, not a generic word list.
```

---

出力されたJSONは `C:\English\logs\YYYY-MM-DD.json` に保存する（Phase 1 のアプリがこれを食う）。
