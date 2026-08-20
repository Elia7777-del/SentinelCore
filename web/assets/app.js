const $ = id => document.getElementById(id);

const demo = {
  metrics: {critical:3, high:17, assets:1284, agents:96},
  incidents: [
    {severity:"CRITICAL", title:"Repeated privileged authentication anomaly", source:"Endpoint SC-042", age:"2 min ago", status:"Investigating"},
    {severity:"HIGH", title:"Suspicious outbound connection", source:"Server SC-117", age:"8 min ago", status:"Contained"},
    {severity:"HIGH", title:"Malware indicator detected", source:"Endpoint SC-083", age:"14 min ago", status:"Investigating"}
  ],
  events: [
    {time:"19:43:04",severity:"HIGH",source:"Endpoint",event:"Suspicious process execution",status:"Investigating"},
    {time:"19:42:49",severity:"MEDIUM",source:"Identity",event:"Unusual authentication context",status:"Triaged"},
    {time:"19:42:18",severity:"CRITICAL",source:"Endpoint",event:"Privilege escalation pattern",status:"Investigating"}
  ]
};

function renderMetrics(m) {
  if (!m) return;
  $("critical").textContent = m.critical ?? 0;
  $("high").textContent = m.high ?? 0;
  $("assetsCount").textContent = Number(m.assets ?? 0).toLocaleString();
  $("agentsCount").textContent = Number(m.agents ?? 0).toLocaleString();
}
function renderIncidents(list) {
  const box = document.querySelector("#incidents");
  if (!box || !Array.isArray(list)) return;
  box.innerHTML = `<div class="panel-head"><h2>Priority Incidents</h2><span>${list.length} ACTIVE</span></div>`;
  list.slice(0,6).forEach(x => {
    const el = document.createElement("div");
    el.className = "incident";
    el.innerHTML = `<b>${x.severity || "INFO"}</b><p>${escapeHtml(x.title || x.name || "Security incident")}</p><small>${escapeHtml(x.source || x.asset || "")} · ${escapeHtml(x.age || x.status || "")}</small>`;
    box.appendChild(el);
  });
}
function renderEvents(list) {
  const table = $("eventsTable");
  if (!table || !Array.isArray(list)) return;
  table.innerHTML = "";
  list.slice(0,20).forEach(x => {
    const row = document.createElement("tr");
    const sev = String(x.severity || "INFO").toLowerCase();
    row.innerHTML = `<td>${escapeHtml(x.time || x.timestamp || "")}</td>
      <td><b class="${sev}">${escapeHtml(x.severity || "INFO")}</b></td>
      <td>${escapeHtml(x.source || x.device || "")}</td>
      <td>${escapeHtml(x.event || x.message || "")}</td>
      <td>${escapeHtml(x.status || "New")}</td>`;
    table.appendChild(row);
  });
}
function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
}
async function refresh() {
  try {
    const m = await SentinelAPI.metrics();
    renderMetrics(m);
    try { renderIncidents(await SentinelAPI.incidents()); } catch {}
    try { renderEvents(await SentinelAPI.events()); } catch {}
    document.body.dataset.api = "online"; if ($("apiStatus")) $("apiStatus").textContent = "ONLINE";
  } catch (err) {
    // Presentation fallback is intentionally retained for first-run/local demos.
    renderMetrics(demo.metrics);
    renderIncidents(demo.incidents);
    renderEvents(demo.events);
    document.body.dataset.api = "offline"; if ($("apiStatus")) $("apiStatus").textContent = "DEMO/OFFLINE";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const themeBtn = $("themeBtn");
  themeBtn?.addEventListener("click", () => document.body.classList.toggle("light"));

  refresh();
  setInterval(refresh, 10000);
});

function openAPISettings() {
  const current = SentinelAPI.base;
  const url = prompt("SentinelCore API base URL", current);
  if (url) {
    SentinelAPI.setBase(url);
    alert("API base saved. Refreshing dashboard.");
    location.reload();
  }
}
