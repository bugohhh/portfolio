# AGENTS.md

本專案的完整 AI 施工規範寫在 [`CLAUDE.md`](./CLAUDE.md)，所有 agent（Codex、Cursor、Claude 等）都適用。

最重要的三件事：

1. 新增作品 = `works/<slug>.md` + `works/works.json` 加一筆，不要寫 HTML。
2. 純靜態、無建置工具、無外部 JS 套件；顏色只能用 `style.css` 的 CSS 變數。
3. 改完一定要跑 `python3 tools/check.py`。
