#!/usr/bin/env python3
"""建立新作品的骨架。用法：python3 tools/new_work.py <slug>

會做兩件事：
1. 從 templates/work-template.md 複製出 works/<slug>.md
2. 在 works/works.json 最前面插入一筆待填資料

插入的資料故意不符合規則（例如 summary 是空的），
所以在填完之前 tools/check.py 一定會失敗，避免半成品被 commit。
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if len(sys.argv) != 2:
    sys.exit("用法：python3 tools/new_work.py <slug>")
slug = sys.argv[1]
if not re.match(r"^[a-z0-9]+(-[a-z0-9]+){1,3}$", slug):
    sys.exit("slug 必須是 2～4 個英文小寫單字的 kebab-case，例如 smart-vending-machine")

md = ROOT / "works" / f"{slug}.md"
if md.exists():
    sys.exit(f"works/{slug}.md 已經存在")

manifest = ROOT / "works" / "works.json"
data = json.loads(manifest.read_text(encoding="utf-8"))
if any(w["slug"] == slug for w in data["works"]):
    sys.exit(f"works.json 已經有 {slug}")

shutil.copy(ROOT / "templates" / "work-template.md", md)
data["works"].insert(0, {
    "slug": slug,
    "title": "",
    "summary": "",
    "period": "",
    "role": "",
    "status": "done",
    "tags": [],
    "stack": [],
    "links": [],
})
manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(f"✓ 已建立 works/{slug}.md，並在 works.json 最前面加入一筆待填資料")
print("  接下來：填好兩個檔案 → python3 tools/check.py → 本機預覽")
