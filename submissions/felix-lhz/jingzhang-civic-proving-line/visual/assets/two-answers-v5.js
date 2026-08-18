(() => {
  const node = document.getElementById('geometry-data');
  const targets = [document.getElementById('atlasSvg'), document.getElementById('v7TwinSvg')].filter(Boolean);
  if (!node || !targets.length) return;
  const geo = JSON.parse(node.textContent); const NS = 'http://www.w3.org/2000/svg';
  const idOf = (f) => String(f.id || f.properties?.id || '');
  const projector = (features) => { const all = features.flatMap((f) => f.geometry?.type === 'Point' ? [f.geometry.coordinates] : f.geometry?.type === 'LineString' ? f.geometry.coordinates : f.geometry?.type === 'Polygon' ? f.geometry.coordinates.flat() : []); const xs = all.map((p) => p[0]), ys = all.map((p) => p[1]); const b = [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)]; return ([x, y]) => [120 + (x - b[0]) / (b[2] - b[0]) * 760, 100 + (b[3] - y) / (b[3] - b[1]) * 800]; };
  const family = (f) => {
    const id = idOf(f); const role = String(f.properties?.route_role || f.properties?.space_role || f.properties?.building_role || f.properties?.point_role || '');
    return /trial|buffer|control|barrier|plugin|cabinet|estop/i.test(`${id} ${role}`) ? 'ai' : /evidence|staff|emergency|egress|appeal|state|porch/i.test(`${id} ${role}`) ? 'evidence' : 'baseline';
  };
  const draw = (svg) => {
    const features = svg.id === 'v7TwinSvg' ? geo.features.filter((f) => idOf(f).startsWith('V7-D-')) : geo.features; const project = projector(features);
    const group = document.createElementNS(NS, 'g'); group.setAttribute('class', 'v5-geometry v7-live-geometry');
    for (const f of features) {
      const g = f.geometry; const cls = `v5-object layer ${family(f)}`; let el;
      if (g.type === 'Point') { const [cx, cy] = project(g.coordinates); el = document.createElementNS(NS, 'circle'); Object.entries({ cx, cy, r: 7, class: cls }).forEach(([k, v]) => el.setAttribute(k, v)); }
      else { const coords = g.type === 'LineString' ? g.coordinates : g.geometry?.coordinates?.[0] || g.coordinates[0]; el = document.createElementNS(NS, g.type === 'LineString' ? 'polyline' : 'polygon'); el.setAttribute('points', coords.map(project).map((p) => p.join(',')).join(' ')); el.setAttribute('class', cls); }
      el.dataset.geometryId = f.id || f.properties?.id; group.append(el);
    }
    svg.insertBefore(group, svg.querySelector('.station'));
    if (svg.id === 'v7TwinSvg') {
      const label = document.createElementNS(NS, 'g'); label.innerHTML = '<text x="38" y="55" class="v7-twin-title">S7 · LIVE GEOJSON</text><text x="38" y="88" class="v7-twin-note">PUBLIC CROSS / REVERSIBLE BAY / EVIDENCE PORCH</text>';
      svg.append(label);
    }
  };
  targets.forEach(draw);
  const updateMode = () => { const mode = document.body.dataset.mode; document.querySelectorAll('.v5-object.ai').forEach((x) => x.classList.toggle('mode-muted', mode === 'baseline')); document.querySelectorAll('.v5-object.baseline').forEach((x) => x.classList.toggle('mode-muted', mode === 'ai')); };
  document.querySelectorAll('[data-mode],[data-layer]').forEach((button) => button.addEventListener('click', () => requestAnimationFrame(updateMode))); updateMode();
})();

(() => {
  const dataNode = document.getElementById('scenario-data'); const controls = [...document.querySelectorAll('[data-state-view]')];
  document.body.dataset.v7Init = String(controls.length); if (!dataNode || !controls.length) return;
  const data = JSON.parse(dataNode.textContent); const s7 = data.scenarios.find((item) => item.id === 'SCN-010'); const always = new Set(s7?.state_views?.OPEN || []);
  const copy = {
    OPEN: ['公共十字、常规接驳和证据门廊独立运行', 'The public cross, conventional interchange and evidence porch operate independently'],
    TRIAL: ['独立试验湾限时开启；双急停与人工岗位激活', 'The separate bay opens by schedule; two E-stops and staff post activate'],
    PAUSE: ['AI 停机、人工接管、边界关闭；两条公共路线继续开放', 'AI stops, staff take over and the boundary closes; both public routes remain open'],
    RETIRE: ['设备经撤场路线进入存储，场地恢复普通用途', 'Equipment follows the removal route to storage and the ground returns to civic use'],
  };
  const lang = document.documentElement.lang === 'en' ? 1 : 0;
  const updateHash = (state) => { const params = new URLSearchParams(location.hash.replace(/^#/, '')); params.set('state', state.toLowerCase()); history.replaceState(null, '', `${location.href.split('#')[0]}#${params.toString()}`); };
  const apply = (state, writeHash = true) => {
    document.body.dataset.v7State = state.toLowerCase(); controls.forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.stateView === state)));
    const active = new Set([...always, ...(s7?.state_views?.[state] || [])]); document.querySelectorAll('[data-geometry-id^="V7-D-"]').forEach((element) => element.classList.toggle('state-muted', !active.has(element.dataset.geometryId)));
    const label = document.getElementById('v7StateLabel'); const detail = document.getElementById('v7StateDetail'); if (label) label.textContent = state; if (detail) detail.textContent = copy[state][lang]; if (writeHash) updateHash(state);
  };
  controls.forEach((button) => button.addEventListener('click', () => apply(button.dataset.stateView)));
  const initial = new URLSearchParams(location.hash.replace(/^#/, '')).get('state')?.toUpperCase(); apply(copy[initial] ? initial : 'OPEN', false);
})();
