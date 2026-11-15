#!/usr/bin/env python3
"""依 CLAUDE.md 規則檢查作品資料。用法：python3 tools/check.py"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKS_DIR = ROOT / "works"

ALLOWED_TAGS = {"backend", "frontend", "database", "optimization",
                "ai-agent", "mobile", "education", "meta"}
ALLOWED_STATUS = {"done", "wip", "plan"}
REQUIRED = ["slug", "title", "summary", "period", "role", "status", "tags", "stack"]
SECTIONS = ["## 背景", "## 我做了什麼", "## 技術重點", "## 反思"]
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+){1,3}$")
PERIOD_RE = re.compile(r"^\d{4} [春夏秋冬]( – (至今|\d{4} [春夏秋冬]))?$")
HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")

errors = []


def err(where, msg):
    errors.append(f"[{where}] {msg}")


def check_works():
    try:
        data = json.loads((WORKS_DIR / "works.json").read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        err("works.json", f"無法解析：{e}")
        return
    works = data.get("works", [])
    if not works:
        err("works.json", "works 陣列是空的")
    seen = set()
    for i, w in enumerate(works):
        where = f"works.json #{i + 1} {w.get('slug', '?')}"
        for key in REQUIRED:
            if key not in w or w[key] in ("", None, []):
                err(where, f"缺少必填欄位 {key}")
        slug = w.get("slug", "")
        if slug in seen:
            err(where, "slug 重複")
        seen.add(slug)
        if slug and not SLUG_RE.match(slug):
            err(where, "slug 必須是 2～4 個英文小寫單字的 kebab-case")
        if len(w.get("title", "")) > 20:
            err(where, "title 超過 20 字")
        n = len(w.get("summary", ""))
        if n and not 30 <= n <= 60:
            err(where, f"summary 應為 30～60 字，目前 {n} 字")
        if w.get("period") and not PERIOD_RE.match(w["period"]):
            err(where, f"period 格式錯誤：{w['period']}")
        if w.get("status") not in ALLOWED_STATUS:
            err(where, f"status 只能是 {sorted(ALLOWED_STATUS)}")
        tags = w.get("tags", [])
        if not 1 <= len(tags) <= 3:
            err(where, "tags 需 1～3 個")
        for t in tags:
            if t not in ALLOWED_TAGS:
                err(where, f"tag「{t}」不在詞彙表")
        for link in w.get("links", []):
            if not str(link.get("url", "")).startswith(("https://", "./", "../")):
                err(where, f"連結格式可疑：{link}")
        md = WORKS_DIR / f"{slug}.md"
        if not md.exists():
            err(where, f"找不到 works/{slug}.md")
            continue
        check_markdown(md)
    for md in WORKS_DIR.glob("*.md"):
        if md.stem not in seen:
            err(md.name, "這個檔案沒有登記在 works.json")


def check_markdown(md):
    text = md.read_text(encoding="utf-8")
    where = f"works/{md.name}"
    lines = text.splitlines()
    heads = [ln.strip() for ln in lines if ln.startswith("## ")]
    if heads != SECTIONS:
        err(where, f"## 段落須依序為 {SECTIONS}，目前為 {heads}")
    in_code = False
    for n, ln in enumerate(lines, 1):
        if ln.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if re.match(r"^# ", ln):
            err(where, f"第 {n} 行：內文不可使用 # 一級標題")
        if re.search(r"<[a-zA-Z/][^>]*>", re.sub(r"`[^`]*`", "", ln)):
            err(where, f"第 {n} 行：不可使用 HTML 標籤")
        if ln.lstrip().startswith("|"):
            err(where, f"第 {n} 行：不支援表格語法")
        if re.search(r"!\[", ln):
            err(where, f"第 {n} 行：不支援圖片語法")


def check_css():
    css = (ROOT / "assets/css/style.css").read_text(encoding="utf-8")
    root_block = re.search(r":root\s*{([^}]*)}", css)
    rest = css.replace(root_block.group(0), "") if root_block else css
    for m in HEX_RE.finditer(rest):
        err("style.css", f"在 :root 以外寫死顏色 {m.group(0)}，請改用 CSS 變數")


def check_static():
    if not (ROOT / ".nojekyll").exists():
        err("root", "缺少 .nojekyll")
    for page in ["index.html", "work.html"]:
        html = (ROOT / page).read_text(encoding="utf-8")
        for src in re.findall(r'<script[^>]+src="([^"]+)"', html):
            if src.startswith("http"):
                err(page, f"不可引用外部 JS：{src}")
        for href in re.findall(r'(?:href|src)="(/[^"]*)"', html):
            err(page, f"請使用相對路徑：{href}")


check_works()
check_css()
check_static()

if errors:
    print(f"✗ 發現 {len(errors)} 個問題：")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("✓ 全部通過")
