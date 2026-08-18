(() => {
  const node = document.getElementById('geometry-data'); const svg = document.getElementById('atlasSvg');
  if (!node || !svg) return;
  const geo = JSON.parse(node.textContent); const NS = 'http://www.w3.org/2000/svg';
  const all = geo.features.flatMap((f) => f.geometry?.type === 'Point' ? [f.geometry.coordinates] : f.geometry?.type === 'LineString' ? f.geometry.coordinates : f.geometry?.type === 'Polygon' ? f.geometry.coordinates.flat() : []);
  const xs = all.map((p) => p[0]), ys = all.map((p) => p[1]); const b = [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)];
  const project = ([x, y]) => [150 + (x - b[0]) / (b[2] - b[0]) * 700, 90 + (b[3] - y) / (b[3] - b[1]) * 820];
  const family = (f) => { const id = String(f.id || f.properties?.id || ''); return /TRIAL|BUFFER|PLUGIN|CABINET|CONTROL/.test(id) ? 'ai' : /EVIDENCE|STAFF|ESTOP|EMERGENCY|UTILITY|APPEAL/.test(id) ? 'evidence' : 'baseline'; };
  const group = document.createElementNS(NS, 'g'); group.setAttribute('class', 'v5-geometry');
  for (const f of geo.features) { const g = f.geometry; const cls = `v5-object layer ${family(f)}`; let el;
    if (g.type === 'Point') { const [cx, cy] = project(g.coordinates); el = document.createElementNS(NS, 'circle'); Object.entries({ cx, cy, r: 7, class: cls }).forEach(([k, v]) => el.setAttribute(k, v)); }
    else { const coords = g.type === 'LineString' ? g.coordinates : g.coordinates[0]; el = document.createElementNS(NS, g.type === 'LineString' ? 'polyline' : 'polygon'); el.setAttribute('points', coords.map(project).map((p) => p.join(',')).join(' ')); el.setAttribute('class', cls); }
    el.dataset.geometryId = f.id || f.properties?.id; group.append(el);
  }
  svg.insertBefore(group, svg.querySelector('.station'));
  const updateMode = () => { const mode = document.body.dataset.mode; svg.querySelectorAll('.v5-object.ai').forEach((x) => x.classList.toggle('mode-muted', mode === 'baseline')); svg.querySelectorAll('.v5-object.baseline').forEach((x) => x.classList.toggle('mode-muted', mode === 'ai')); };
  document.querySelectorAll('[data-mode],[data-layer]').forEach((button) => button.addEventListener('click', () => requestAnimationFrame(updateMode))); updateMode();
})();

(() => {
  const dataNode = document.getElementById('scenario-data');
  const controls = [...document.querySelectorAll('[data-state-view]')];
  document.body.dataset.v6Init = String(controls.length);
  if (!dataNode || !controls.length) return;
  const data = JSON.parse(dataNode.textContent);
  const s7 = data.scenarios.find((item) => item.id === 'SCN-010');
  const always = new Set(s7?.state_views?.OPEN || []);
  const copy = {
    OPEN: ['普通交通与公共空间独立运行', 'Conventional transit and public space operate independently'],
    TRIAL: ['独立试验湾限时开启；两条公共路径保持完整', 'The separate trial bay opens by schedule; both public routes remain whole'],
    PAUSE: ['AI 停机，人工接管；试验边界关闭', 'AI stops, staff take over, and the trial boundary closes'],
    RETIRE: ['设备撤出，恢复候车、短停或公共活动', 'Equipment leaves; waiting, short stay or civic activity returns'],
  };
  const lang = document.documentElement.lang === 'en' ? 1 : 0;
  const updateHash = (state) => {
    const params = new URLSearchParams(location.hash.replace(/^#/, ''));
    params.set('state', state.toLowerCase());
    history.replaceState(null, '', `${location.href.split('#')[0]}#${params.toString()}`);
  };
  const apply = (state, writeHash = true) => {
    document.body.dataset.v6State = state.toLowerCase();
    controls.forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.stateView === state)));
    const active = new Set([...always, ...(s7?.state_views?.[state] || [])]);
    document.querySelectorAll('[data-geometry-id^="V6-D-"]').forEach((element) => element.classList.toggle('state-muted', !active.has(element.dataset.geometryId)));
    const label = document.getElementById('v6StateLabel');
    const detail = document.getElementById('v6StateDetail');
    if (label) label.textContent = state;
    if (detail) detail.textContent = copy[state][lang];
    if (writeHash) updateHash(state);
  };
  controls.forEach((button) => button.addEventListener('click', () => apply(button.dataset.stateView)));
  const initial = new URLSearchParams(location.hash.replace(/^#/, '')).get('state')?.toUpperCase();
  apply(copy[initial] ? initial : 'OPEN', false);
})();
