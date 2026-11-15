// 共用工具：讀取作品清單、編號、標籤與狀態名稱
const TAG_LABELS = {
  backend: "後端",
  frontend: "前端",
  database: "資料庫",
  optimization: "最佳化",
  "ai-agent": "AI Agent",
  mobile: "行動 App",
  education: "教學工具",
  meta: "本站",
};

const STATUS_LABELS = { done: "已完成", wip: "進行中", plan: "規劃中" };

const NUMERALS = ["零", "壹", "貳", "參", "肆", "伍", "陸", "柒", "捌", "玖", "拾"];

function toNumeral(n) {
  if (n <= 10) return NUMERALS[n];
  if (n < 20) return "拾" + NUMERALS[n - 10];
  const t = Math.floor(n / 10), o = n % 10;
  return NUMERALS[t] + "拾" + (o ? NUMERALS[o] : "");
}

async function loadWorks() {
  const res = await fetch("works/works.json", { cache: "no-cache" });
  if (!res.ok) throw new Error("無法讀取 works.json");
  const data = await res.json();
  return data.works.map((w, i) => ({ ...w, no: toNumeral(i + 1), index: i }));
}

function escapeHTML(s) {
  return String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}
