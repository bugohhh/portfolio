# 作品帖

郭的個人作品展示站：課程專案、個人專案與畢業專題。

- 網站：https://bugohhh.github.io/portfolio/
- AI 施工規範：[`CLAUDE.md`](./CLAUDE.md)（非 Claude 的 agent 請讀 [`AGENTS.md`](./AGENTS.md)）

## 這個專案的重點

不是「把一個網頁做出來」，而是「定一套規則，讓之後可以很快加新內容」。
新增一件作品只要兩步，不用寫 HTML：

1. 複製 `templates/work-template.md` 成 `works/<slug>.md`，填內文
2. 在 `works/works.json` 加一筆資料

改完執行 `python3 tools/check.py` 檢查是否符合規則。

也可以直接對 AI 說：

> 請依照 CLAUDE.md 新增一件作品：（貼上作品素材）

## 本機預覽

```
python3 -m http.server 8000
```

打開 http://localhost:8000（直接雙擊 `index.html` 會讀不到資料）。

## 部署到 GitHub Pages

1. 在 GitHub 建立公開 repo，名稱 `portfolio`（不要勾選新增 README）
2. 在專案資料夾執行：
   ```
   git remote add origin https://github.com/bugohhh/portfolio.git
   git branch -M main
   git push -u origin main
   ```
3. repo → **Settings → Pages** → Source 選 **Deploy from a branch**，Branch 選 `main`、資料夾 `/ (root)` → Save
4. 約一分鐘後即可在 https://bugohhh.github.io/portfolio/ 瀏覽
