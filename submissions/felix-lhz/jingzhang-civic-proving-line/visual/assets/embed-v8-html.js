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
    title: '京张双答 V8｜三站一历', kicker: 'JING-ZHANG TWO ANSWERS · V8 · THREE STATIONS, ONE CIVIC YEAR',
    claim: '一条不断线的公共基线，三座会留下回执的城市地标，一年四季的公开采纳程序。',
    overall: '总体城市关系｜一脊 · 三站 · 两翼', ring: ['众智园·验真环', '公共旁路包围受控验证'], gate: ['AI 原点·共译门', '三条无账户路径穿越人工服务'], porch: ['大钟寺·回执廊', '公共十字不断线，试验只进一侧'],
    twin: 'S7 四态空间孪生', open: '公共十字、常规接驳和人工门廊独立运行',
    seasons: ['春｜基线审计', '夏｜开放验证', '秋｜公众采纳', '冬｜回执复盘'], evidence: ['公共路线可定位', '试验边界在一侧', '人工决定留在门廊'],
    stationTabs: [['众智园·验真环','连续旁路 + 受控内环'],['AI 原点·共译门','三路穿行 + 人工复核'],['大钟寺·回执廊','公共十字 + 可逆试验湾']],
    reportTitle: '六项任务，一条可核验的城市证据链', reportClaim: '空间不是协议的背景：环、门、廊分别承载验真、共译与城市采纳。',
    tasks: [['Agent 1','空间底图与三层范围'],['Agent 2','三站两翼产业协同'],['Agent 3','十二组双答场景'],['Agent 4','三座地标与公共缝合'],['Agent 5','文化里程与国际标识'],['Agent 6','四季运营与知识归档']],
    status: '当前证据：E1 概念设计｜E2–E4 待原型、受控试验与城市决定', nav: '五段评审路径',
  },
  en: {
    title: 'Jing-Zhang Two Answers V8 | Three Stations, One Civic Year', kicker: 'JING-ZHANG TWO ANSWERS · V8 · THREE STATIONS, ONE CIVIC YEAR',
    claim: 'One unbroken public baseline, three civic landmarks that leave receipts, and a year-round public adoption procedure.',
    overall: 'URBAN RELATION · SPINE · STATIONS · WINGS', ring: ['Verification Ring', 'A public bypass encloses controlled verification'], gate: ['Translation Gate', 'Three account-free routes cross staffed service'], porch: ['Receipt Porch', 'The public cross stays open; trial stays on one side'],
    twin: 'S7 FOUR-STATE SPATIAL TWIN', open: 'The public cross, conventional interchange and staffed porch operate independently',
    seasons: ['SPRING · audit', 'SUMMER · verify', 'AUTUMN · adopt', 'WINTER · review'], evidence: ['public route located', 'trial boundary on one side', 'human decision at porch'],
    stationTabs: [['Verification Ring','continuous bypass + controlled inner ring'],['Translation Gate','three crossings + human review'],['Receipt Porch','public cross + reversible trial bay']],
    reportTitle: 'Six tasks, one auditable civic evidence chain', reportClaim: 'Space is not a backdrop to the protocol: ring, gate and porch host verification, translation and civic adoption.',
    tasks: [['Agent 1','base map and three scopes'],['Agent 2','three stations and two wings'],['Agent 3','twelve paired-answer scenes'],['Agent 4','landmarks and public seams'],['Agent 5','culture mile and bilingual identity'],['Agent 6','seasonal operation and archive']],
    status: 'CURRENT EVIDENCE: E1 CONCEPT DESIGN · E2–E4 AWAIT PROTOTYPE, TRIAL AND CIVIC DECISION', nav: 'Five-part review route',
  },
};

function landmarkSvg(kind) {
  if (kind === 'ring') return '<svg viewBox="0 0 120 90" aria-hidden="true"><ellipse cx="60" cy="45" rx="43" ry="31" fill="none" stroke="#176b55" stroke-width="10"/><ellipse cx="60" cy="45" rx="23" ry="15" fill="#dc8b1233" stroke="#dc8b12" stroke-width="3"/><path d="M8 45h28M84 45h28" stroke="#176b55" stroke-width="5"/></svg>';
  if (kind === 'gate') return '<svg viewBox="0 0 120 90" aria-hidden="true"><path d="M18 77V18h84v59M18 40h84M18 60h84" fill="none" stroke="#dc8b12" stroke-width="8"/><path d="M8 30h104M8 50h104M8 70h104" stroke="#176b55" stroke-width="4"/></svg>';
  return '<svg viewBox="0 0 120 90" aria-hidden="true"><path d="M8 45h104M60 8v74" stroke="#176b55" stroke-width="8"/><path d="M72 22h38v48H72" fill="#dc8b1233" stroke="#dc8b12" stroke-width="4"/><path d="M17 17h35v18H17z" fill="#126d9b"/></svg>';
}

function makeFirstLook(c, suffix) {
  const lm = [['ring',c.ring],['gate',c.gate],['porch',c.porch]].map(([kind,item]) => `<div class="v8-landmark">${landmarkSvg(kind)}<div><b>${item[0]}</b><small>${item[1]}</small></div></div>`).join('');
  return `<div class="v8-first-look"><div class="v8-overview"><figure><img src="../assets/figures/site-overview${suffix}.png" alt="${c.overall}"><figcaption>${c.overall}</figcaption></figure><div class="v8-landmarks">${lm}</div></div><div class="v8-twin-row"><section class="v8-state-panel"><div class="v8-twin"><svg id="v7TwinSvg" viewBox="0 0 1000 1000" role="img" aria-label="${c.twin}"></svg><b>${c.twin}</b></div><div class="v8-state-side"><div class="v7-state-controls" aria-label="S7 operating states"><button type="button" data-state-view="OPEN" aria-pressed="true">OPEN</button><button type="button" data-state-view="TRIAL" aria-pressed="false">TRIAL</button><button type="button" data-state-view="PAUSE" aria-pressed="false">PAUSE</button><button type="button" data-state-view="RETIRE" aria-pressed="false">RETIRE</button></div><div class="v7-state-copy"><b id="v7StateLabel">OPEN</b><span id="v7StateDetail">${c.open}</span></div></div></section><div class="v8-season">${c.seasons.map(x=>`<b>${x}</b>`).join('')}</div></div><div class="v8-evidence-strip">${c.evidence.map(x=>`<b>${x}</b>`).join('')}</div><strong>NOT FIELD-RUN · E1 CONCEPT DESIGN · E2–E4 PENDING</strong></div>`;
}

function replaceFirstLook(html, replacement) {
  const start = html.search(/<div class="(?:first-look v7|v8-first-look)"/);
  const end = html.indexOf('<nav class="review-nav"', start);
  if (start < 0 || end < 0) throw new Error('first-look boundary not found');
  return html.slice(0, start) + replacement + html.slice(end);
}

for (const lang of ['zh','en']) {
  const suffix = lang === 'en' ? '.en' : '';
  const c = copy[lang];
  const visual = path.join(ROOT, 'visual', `index${suffix}.html`);
  let html = fs.readFileSync(visual, 'utf8');
  html = html.replace(/<title>[^<]*<\/title>/, `<title>${c.title}</title>`)
    .replace(/<p class="kicker">[^<]*<\/p>/, `<p class="kicker">${c.kicker}</p>`)
    .replace(/<p class="claim">[^<]*<\/p>/, `<p class="claim">${c.claim}</p>`);
  html = replaceFirstLook(html, makeFirstLook(c, suffix));
  html = html.replace(/<link rel="stylesheet" href="assets\/two-answers-v8\.css">/g, '');
  html = html.replace('</head>', '<link rel="stylesheet" href="assets/two-answers-v8.css"></head>');
  html = html.replace(/<div class="station-tabs">[\s\S]*?<\/div><div class="station-stage">/, `<div class="station-tabs">${['zhongzhiyuan','ai_origin','dazhongsi'].map((id,i)=>`<button class="station-tab" data-station="${id}"><b>${c.stationTabs[i][0]}</b><span>${c.stationTabs[i][1]}</span></button>`).join('')}</div><div class="station-stage">`);
  html = html.replace(/<script id="scenario-data"[\s\S]*?<\/script>/, `<script id="scenario-data" type="application/json">${data}</script>`)
    .replace(/<script id="atlas-data"[\s\S]*?<\/script>/, `<script id="atlas-data" type="application/json">${atlas}</script>`)
    .replace(/<script id="context-data"[\s\S]*?<\/script>/, `<script id="context-data" type="application/json">${context}</script>`)
    .replace(/<script id="geometry-data"[\s\S]*?<\/script>/, `<script id="geometry-data" type="application/json">${JSON.stringify(geometry)}</script>`);
  fs.writeFileSync(visual, html.replace(/\r\n/g,'\n'));

  const report = path.join(ROOT, 'report', `proposal${suffix}.html`);
  if (!fs.existsSync(report)) continue;
  let reportHtml = fs.readFileSync(report,'utf8')
    .replace(/<!-- V7_EXEC_START -->[\s\S]*?<!-- V7_EXEC_END -->/g,'')
    .replace(/<!-- V8_EXEC_START -->[\s\S]*?<!-- V8_EXEC_END -->/g,'');
  const tasks = c.tasks.map(([n,t])=>`<div><b>${n}</b><span>${t}</span></div>`).join('');
  const block = `<!-- V8_EXEC_START --><style>.v8-exec{margin:-42px -24px 36px;padding:38px 34px 30px;background:#10201b;color:#fff}.v8-exec h1{font-size:43px;max-width:1050px;margin:0 0 8px}.v8-exec>p{font-size:21px;color:#f7e2b7;margin:0 0 18px}.v8-report-grid{display:grid;grid-template-columns:.9fr 1.1fr;gap:16px}.v8-agent-index{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}.v8-agent-index div{display:flex;flex-direction:column;gap:4px;padding:13px;background:#ffffff12;border-left:5px solid #176b55}.v8-agent-index div:nth-child(3n+2){border-color:#dc8b12}.v8-agent-index div:nth-child(3n){border-color:#126d9b}.v8-agent-index b{font-size:12px;letter-spacing:.08em}.v8-agent-index span{font-size:15px;font-weight:700}.v8-exec figure{margin:0;background:#f3efe5;padding:9px}.v8-exec img{display:block;width:100%;height:auto}.v8-evidence-status{margin-top:12px;padding:10px;background:#0b6b8f;color:#fff;font-weight:800;font-size:12px;letter-spacing:.04em}@media(max-width:800px){.v8-report-grid{grid-template-columns:1fr}.v8-agent-index{grid-template-columns:1fr 1fr}}</style><section class="v8-exec"><h1>${c.reportTitle}</h1><p>${c.reportClaim}</p><div class="v8-report-grid"><div class="v8-agent-index">${tasks}</div><figure><img src="../assets/figures/site-overview${suffix}.png" alt="${c.overall}"></figure></div><div class="v8-evidence-status">${c.status}</div></section><!-- V8_EXEC_END -->`;
  reportHtml = reportHtml.replace('<main>', `<main>${block}`);
  fs.writeFileSync(report, reportHtml.replace(/\r\n/g,'\n'));
}
console.log(`embedded V8 data, three landmarks, civic year and ${geometry.features.length} traceable geometry objects`);
