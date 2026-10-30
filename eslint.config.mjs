// The machine says no before a human has to. Run: npm run lint
// Same rules as brain-app. Focus: XSS. HTML built from data must go through esc() (app/index.html).
// The app's JS lives inside app/index.html, so eslint-plugin-html reads the <script> block.
import comments from "@eslint-community/eslint-plugin-eslint-comments";
import js from "@eslint/js";
import html from "eslint-plugin-html";
import nounsanitized from "eslint-plugin-no-unsanitized";
import globals from "globals";

export default [
  // pwa/index.html is generated from app/index.html; lint the source only.
  { ignores: ["node_modules/", "pwa/index.html", ".venv/"] },
  js.configs.recommended,
  // 例外は 1 行ずつ、規則名と理由(-- の後)を書く。要らなくなった例外は止める
  { linterOptions: { reportUnusedDisableDirectives: "error" } },
  {
    files: ["**/*.js", "**/*.html"],
    plugins: { html, "no-unsanitized": nounsanitized, "@eslint-community/eslint-comments": comments },
    languageOptions: { ecmaVersion: "latest", sourceType: "script", globals: { ...globals.browser } },
    rules: {
      // esc() turns < > & " into entities. Anything else put into HTML is reported.
      "no-unsanitized/method": ["error", { escape: { methods: ["esc"] } }],
      "no-unsanitized/property": ["error", { escape: { methods: ["esc"] } }],
      // 保存・取得に失敗したら(容量・プライベートモード)既定値のまま続ける、がこの画面の決まり。空の catch はその印
      "no-empty": ["error", { allowEmptyCatch: true }],
      "no-eval": "error",
      "no-implied-eval": "error",
      "no-new-func": "error",
      "no-script-url": "error",
      "@eslint-community/eslint-comments/require-description": "error",
      "@eslint-community/eslint-comments/no-unlimited-disable": "error",
      "@eslint-community/eslint-comments/disable-enable-pair": "error",
    },
  },
  {
    files: ["app/index.html"],
    // claude は Claude の Artifact として開いたときだけある実行環境(バックアップの書き出しに使う)。無ければ使わない
    languageOptions: { globals: { claude: "readonly" } },
  },
  {
    files: ["pwa/sw.js"],
    languageOptions: { globals: { ...globals.serviceworker } },
  },
  {
    files: ["eslint.config.mjs"],
    languageOptions: { sourceType: "module" },
  },
];
