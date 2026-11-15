// 作品內頁：依 ?id=<slug> 讀取 works.json 與 works/<slug>.md
(async function () {
  const main = document.getElementById("work");
  const id = new URLSearchParams(location.search).get("id");

  function notFound(msg) {
    document.title = "找不到作品｜作品帖";
    main.innerHTML = `<header class="work-head"><h1>找不到這件作品</h1>
      <p class="lede">${escapeHTML(msg)}</p></header>
      <p><a href="./">← 回到作品帖</a></p>`;
  }

  let works;
  try {
    works = await loadWorks();
  } catch (e) {
    return notFound("作品清單載入失敗。");
  }
  const w = works.find((x) => x.slug === id);
  if (!w) return notFound(id ? `沒有 id 為「${id}」的作品。` : "網址缺少 id 參數。");

  let body = "";
  try {
    const res = await fetch(`works/${encodeURIComponent(w.slug)}.md`, { cache: "no-cache" });
    if (!res.ok) throw new Error();
    body = MD.render(await res.text());
  } catch (e) {
    body = `<p class="empty">內文載入失敗。</p>`;
  }

  document.title = `${w.title}｜作品帖`;
  const links = (w.links || []).length
    ? w.links.map((l) => `<a href="${escapeHTML(l.url)}" target="_blank" rel="noopener">${escapeHTML(l.label)}</a>`).join("、")
    : "—";
  const prev = works[w.index - 1];
  const next = works[w.index + 1];

  main.innerHTML = `
    <header class="work-head">
      <span class="card-no">${w.no}</span>
      <h1>${escapeHTML(w.title)}</h1>
      <p class="lede">${escapeHTML(w.summary)}</p>
      <dl class="facts">
        <dt>期間</dt><dd>${escapeHTML(w.period)}</dd>
        <dt>角色</dt><dd>${escapeHTML(w.role)}</dd>
        <dt>技術</dt><dd>${w.stack.map((s) => `<code>${escapeHTML(s)}</code>`).join("　")}</dd>
        <dt>狀態</dt><dd><span class="status status-${w.status}">${STATUS_LABELS[w.status]}</span></dd>
        <dt>連結</dt><dd>${links}</dd>
      </dl>
    </header>
    <article class="prose">${body}</article>
    <nav class="pager">
      ${prev ? `<a class="prev" href="work.html?id=${prev.slug}">← ${prev.no}・${escapeHTML(prev.title)}</a>` : ""}
      ${next ? `<a class="next" href="work.html?id=${next.slug}">${next.no}・${escapeHTML(next.title)} →</a>` : ""}
    </nav>`;
})();
