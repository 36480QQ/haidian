const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const data = fs.readFileSync(path.join(__dirname, 'two-answers.json'), 'utf8').trim();
const atlas = fs.readFileSync(path.join(__dirname, 'spatial-atlas.json'), 'utf8').trim();
const context = fs.readFileSync(path.join(__dirname, 'context-open-map.json'), 'utf8').trim();
const geometry = {
  type: 'FeatureCollection',
  features: ['roads.geojson', 'public_space.geojson', 'buildings.geojson', 'constraints.geojson']
    .flatMap((name) => JSON.parse(fs.readFileSync(path.join(ROOT, 'geometry', name), 'utf8')).features)
    .filter((feature) => {
      const id = String(feature.id || feature.properties?.id || '');
      return id.startsWith('V7-D-') || (id.startsWith('V5-') && !id.startsWith('V5-D-'));
    }),
};

const copy = {
  zh: {
    title: '京张双答 V9｜可验证的城市样机',
    kicker: 'JING-ZHANG TWO ANSWERS · V9 · VERIFIABLE CIVIC PROTOTYPE',
    claim: '普通服务先成立，AI 再进入同题验证；通过公开回执后，才获得城市采用资格。',
    concept: 'S7 概念生成图 / 非现场证据 · 与公共十字、单侧试验湾和回执廊对应',
    twin: 'S7 四态空间孪生', open: '公共十字、常规接驳和人工门廊独立运行',
    proof: [['空间证据','五级尺度','公共路线、试验湾、岗位与撤场可定位'],['实施证据','16项构件','数量可复算，正式价格待询'],['许可门','8项待关闭','任何缺口都不得进入 TRIAL'],['空白表单','5类可打印','当前没有现场记录或采用决定']],
    map: '总体城市设计 · 一脊三站两翼',
    status: 'E2 原型准备文件已形成', status2: '未测绘 · 未许可 · 未搭建 · 未现场运行',
    reportTitle: '六项任务，一套可审计的 E2 原型准备文件',
    reportClaim: '总图、三座地标、S7 构件、许可门、空白表单和失败回退均可定位；现场绩效仍为空。',
    tasks: [['Agent 1','总体城市设计与三层范围'],['Agent 2','产业能力进入城市的验收链'],['Agent 3','十二个同题双答场景'],['Agent 4','验真环、共译门、回执廊'],['Agent 5','城市证据里程与双语传播'],['Agent 6','90天试点与城市采纳年']],
  },
  en: {
    title: 'Jing-Zhang Two Answers V9 | Verifiable Civic Prototype',
    kicker: 'JING-ZHANG TWO ANSWERS · V9 · VERIFIABLE CIVIC PROTOTYPE',
    claim: 'Baseline first. AI then enters paired proof and earns civic adoption only through a public receipt.',
    concept: 'S7 CONCEPT IMAGE / NOT SITE EVIDENCE · matched to public cross, one-side bay and receipt porch',
    twin: 'S7 FOUR-STATE SPATIAL TWIN', open: 'The public cross, conventional interchange and staffed porch operate independently',
    proof: [['SPATIAL PROOF','five scales','routes, bay, posts and removal are locatable'],['DELIVERY PROOF','16 components','reproducible quantities; quotes pending'],['PERMIT GATES','8 pending','any gap blocks TRIAL'],['BLANK FORMS','5 printable','no field record or adoption decision exists']],
    map: 'OVERALL URBAN DESIGN · SPINE, STATIONS + WINGS',
    status: 'E2 PROTOTYPE-PREPARATION DOCUMENTS EXIST', status2: 'NOT SURVEYED · NOT PERMITTED · NOT BUILT · NOT FIELD-RUN',
    reportTitle: 'Six tasks, one auditable E2 prototype-preparation dossier',
    reportClaim: 'The plan, three landmarks, S7 kit, permit gates, blank forms and failure fallback are locatable; field performance remains empty.',
    tasks: [['Agent 1','urban design and three scopes'],['Agent 2','capability-to-adoption chain'],['Agent 3','twelve paired-answer scenes'],['Agent 4','ring, gate and receipt porch'],['Agent 5','evidence mile and bilingual reach'],['Agent 6','90-day pilot and civic year']],
  },
};

function firstLook(c, suffix) {
  return `<div class="v9-first-look"><div class="v9-flagship"><figure><img src="../assets/figures/concept-s7-v9.webp" alt="${c.concept}"><figcaption>${c.concept}</figcaption></figure><div class="v9-state-panel"><div class="v9-twin"><svg id="v7TwinSvg" viewBox="0 0 1000 1000" role="img" aria-label="${c.twin}"></svg><b>${c.twin}</b></div><div class="v9-state-side"><div class="v7-state-controls" aria-label="S7 operating states"><button type="button" data-state-view="OPEN" aria-pressed="true">OPEN</button><button type="button" data-state-view="TRIAL" aria-pressed="false">TRIAL</button><button type="button" data-state-view="PAUSE" aria-pressed="false">PAUSE</button><button type="button" data-state-view="RETIRE" aria-pressed="false">RETIRE</button></div><div class="v9-state-copy"><b id="v7StateLabel">OPEN</b><span id="v7StateDetail">${c.open}</span></div></div></div></div><div class="v9-evidence"><div><h2>${c.status}</h2><p>${c.status2}</p></div><div class="v9-proof-grid">${c.proof.map((p)=>`<article><b>${p[0]}</b><strong>${p[1]}</strong><span>${p[2]}</span></article>`).join('')}<div class="v9-mini-map"><img src="../assets/figures/site-overview${suffix}.png" alt="${c.map}"></div><div class="v9-mini-map"><img src="../assets/figures/metrics-evidence${suffix}.png" alt="E2 evidence pack"></div></div><div class="v9-status"><strong>${c.status}</strong><span>${c.status2}</span><span>ADOPT · REVISE · STOP</span></div></div></div>`;
}

function replaceFirstLook(html, replacement) {
  const start = html.search(/<div class="(?:first-look v7|v8-first-look|v9-first-look)"/);
  const end = html.indexOf('<nav class="review-nav"', start);
  if (start < 0 || end < 0) throw new Error('first-look boundary not found');
  return html.slice(0, start) + replacement + html.slice(end);
}

for (const lang of ['zh','en']) {
  const suffix = lang === 'en' ? '.en' : '';
  const c = copy[lang];
  const visual = path.join(ROOT, 'visual', `index${suffix}.html`);
  let html = fs.readFileSync(visual, 'utf8')
    .replace(/<title>[^<]*<\/title>/, `<title>${c.title}</title>`)
    .replace(/<p class="kicker">[^<]*<\/p>/, `<p class="kicker">${c.kicker}</p>`)
    .replace(/<p class="claim">[^<]*<\/p>/, `<p class="claim">${c.claim}</p>`);
  html = replaceFirstLook(html, firstLook(c, suffix));
  html = html.replace(/<link rel="stylesheet" href="assets\/two-answers-v9\.css">/g, '');
  html = html.replace('</head>', '<link rel="stylesheet" href="assets/two-answers-v9.css"></head>');
  html = html.replace(/<script id="scenario-data"[\s\S]*?<\/script>/, `<script id="scenario-data" type="application/json">${data}</script>`)
    .replace(/<script id="atlas-data"[\s\S]*?<\/script>/, `<script id="atlas-data" type="application/json">${atlas}</script>`)
    .replace(/<script id="context-data"[\s\S]*?<\/script>/, `<script id="context-data" type="application/json">${context}</script>`)
    .replace(/<script id="geometry-data"[\s\S]*?<\/script>/, `<script id="geometry-data" type="application/json">${JSON.stringify(geometry)}</script>`)
    .replaceAll('E1 CONCEPT DESIGN · E2–E4 PENDING', 'E2 DOCUMENTED · NOT BUILT · E3–E4 PENDING')
    .replaceAll('E1 概念设计；正式报价、E2 基线', 'E2 原型准备文件；正式报价、现场基线');
  fs.writeFileSync(visual, html.replace(/\r\n/g,'\n'));

  const report = path.join(ROOT, 'report', `proposal${suffix}.html`);
  if (!fs.existsSync(report)) continue;
  let reportHtml = fs.readFileSync(report,'utf8')
    .replace(/<!-- V8_EXEC_START -->[\s\S]*?<!-- V8_EXEC_END -->/g,'')
    .replace(/<!-- V9_EXEC_START -->[\s\S]*?<!-- V9_EXEC_END -->/g,'');
  const tasks = c.tasks.map(([n,t])=>`<div><b>${n}</b><span>${t}</span></div>`).join('');
  const block = `<!-- V9_EXEC_START --><style>.v9-report{margin:-42px -24px 36px;padding:36px 34px 28px;background:#10201b;color:#fff}.v9-report h1{font-size:42px;max-width:1100px;margin:0 0 8px}.v9-report>p{font-size:19px;color:#f7e2b7;margin:0 0 18px}.v9-report-grid{display:grid;grid-template-columns:.8fr 1.2fr;gap:14px}.v9-task-index{display:grid;grid-template-columns:1fr 1fr;gap:8px}.v9-task-index div{padding:12px;background:#ffffff10;border-left:5px solid #176b55;display:grid;gap:4px}.v9-task-index div:nth-child(3n+2){border-color:#d98a12}.v9-task-index div:nth-child(3n){border-color:#126d9b}.v9-task-index b{font-size:12px}.v9-task-index span{font-size:15px;font-weight:700}.v9-report-proof{display:grid;grid-template-columns:1fr .72fr;gap:8px}.v9-report-proof figure{margin:0;background:#f3efe5;padding:7px}.v9-report-proof img{display:block;width:100%;height:100%;object-fit:contain}.v9-report-status{margin-top:12px;padding:10px;background:#126d9b;font-weight:850;font-size:12px;letter-spacing:.04em}@media(max-width:800px){.v9-report-grid,.v9-report-proof{grid-template-columns:1fr}.v9-task-index{grid-template-columns:1fr 1fr}}</style><section class="v9-report"><h1>${c.reportTitle}</h1><p>${c.reportClaim}</p><div class="v9-report-grid"><div class="v9-task-index">${tasks}</div><div class="v9-report-proof"><figure><img src="../assets/figures/site-overview${suffix}.png" alt="${c.map}"></figure><figure><img src="../assets/figures/metrics-evidence${suffix}.png" alt="E2 readiness"></figure></div></div><div class="v9-report-status">${c.status} · ${c.status2}</div></section><!-- V9_EXEC_END -->`;
  reportHtml = reportHtml.replace('<main>', `<main>${block}`);
  fs.writeFileSync(report, reportHtml.replace(/\r\n/g,'\n'));
}

console.log(`embedded V9 schema, E2 readiness and ${geometry.features.length} traceable geometry objects`);
