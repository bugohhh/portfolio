// 首頁：標籤篩選 + 作品卡片牆
(async function () {
  const grid = document.getElementById("grid");
  const filters = document.getElementById("filters");
  let works;
  try {
    works = await loadWorks();
  } catch (e) {
    grid.innerHTML = `<li class="empty">作品清單載入失敗。若是在本機直接開檔，請改用 <code>python3 -m http.server</code>。</li>`;
    return;
  }

  const tagsInUse = Object.keys(TAG_LABELS).filter((t) => works.some((w) => w.tags.includes(t)));
  let active = new URLSearchParams(location.search).get("tag") || "all";
  if (active !== "all" && !tagsInUse.includes(active)) active = "all";

  function card(w) {
    return `<li><a class="card" href="work.html?id=${encodeURIComponent(w.slug)}">
      <span class="card-no">${w.no}</span>
      <h2>${escapeHTML(w.title)}</h2>
      <p>${escapeHTML(w.summary)}</p>
      <div class="card-meta">
        <span>${escapeHTML(w.period)}</span>
        <span class="status status-${w.status}">${STATUS_LABELS[w.status]}</span>
      </div>
      <ul class="tags">${w.tags.map((t) => `<li>${TAG_LABELS[t]}</li>`).join("")}</ul>
    </a></li>`;
  }

  function draw() {
    filters.innerHTML = ["all", ...tagsInUse]
      .map((t) => `<button class="chip" data-tag="${t}" aria-pressed="${t === active}">${t === "all" ? "全部" : TAG_LABELS[t]}</button>`)
      .join("");
    const list = active === "all" ? works : works.filter((w) => w.tags.includes(active));
    grid.innerHTML = list.length ? list.map(card).join("") : `<li class="empty">這個分類還沒有作品。</li>`;
  }

  filters.addEventListener("click", (e) => {
    const btn = e.target.closest(".chip");
    if (!btn) return;
    active = btn.dataset.tag;
    const url = active === "all" ? location.pathname : `?tag=${active}`;
    history.replaceState(null, "", url);
    draw();
  });

  draw();
})();
