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
    title: '京张双答 V7｜大钟寺城市采纳站', kicker: 'JING-ZHANG TWO ANSWERS · V7',
    claim: '公共十字不断线，AI 只进入一侧可逆试验湾，城市决定留在证据门廊。',
    overallAlt: '一脊三站两翼总体城市设计', stateDetail: '公共十字、常规接驳和证据门廊独立运行',
    stateCaption: 'S7 运行孪生｜真实 V7 设计几何', baseline: '两条公共路线', bay: '一侧可逆试验湾', porch: '人工证据门廊',
    reportTitle: '结论先行：把回执画进城市', reportClaim: '一条路、一个湾、一座门廊、一圈蓝绿边界。',
    reportPoints: ['普通服务先成立，AI 关闭后城市仍完整。', '试验、急停、岗位和撤场全部留在公共十字一侧。', '数量可复算，价格待询价，采用决定待现场。'],
  },
  en: {
    title: 'Jing-Zhang Two Answers V7 | Dazhongsi Civic Adoption Station', kicker: 'JING-ZHANG TWO ANSWERS · V7',
    claim: 'The public cross stays open; AI enters one reversible bay; the civic decision remains at the evidence porch.',
    overallAlt: 'One spine, three stations and two wings', stateDetail: 'The public cross, conventional interchange and evidence porch operate independently',
    stateCaption: 'S7 OPERATING TWIN · LIVE V7 DESIGN GEOMETRY', baseline: 'two public routes', bay: 'one reversible trial bay', porch: 'staffed evidence porch',
    reportTitle: 'Conclusion first: draw the receipt into the city', reportClaim: 'A route, a bay, a porch and a blue-green edge.',
    reportPoints: ['The baseline stands first; the city remains complete with AI off.', 'Trial, E-stops, staff and removal stay on one side of the public cross.', 'Quantities are reproducible; prices and adoption await field evidence.'],
  },
};

for (const lang of ['zh', 'en']) {
  const file = path.join(ROOT, 'visual', `index${lang === 'en' ? '.en' : ''}.html`);
  const c = copy[lang]; const suffix = lang === 'en' ? '.en' : '';
  const firstLook = `<div class="first-look v7"><div class="v7-review-grid"><figure><img src="../assets/figures/site-overview${suffix}.png" alt="${c.overallAlt}"><figcaption>${lang === 'zh' ? '总体判断｜一脊 · 三站 · 两翼' : 'OVERALL · SPINE · STATIONS · WINGS'}</figcaption></figure><section class="v7-state-panel"><div class="v7-twin"><svg id="v7TwinSvg" viewBox="0 0 1000 1000" role="img" aria-label="${c.stateCaption}"></svg><b>${c.stateCaption}</b></div><div class="v7-state-controls" aria-label="S7 operating states"><button type="button" data-state-view="OPEN" aria-pressed="true">OPEN</button><button type="button" data-state-view="TRIAL" aria-pressed="false">TRIAL</button><button type="button" data-state-view="PAUSE" aria-pressed="false">PAUSE</button><button type="button" data-state-view="RETIRE" aria-pressed="false">RETIRE</button></div><div class="v7-state-copy"><b id="v7StateLabel">OPEN</b><span id="v7StateDetail">${c.stateDetail}</span></div></section></div><div class="v7-evidence-strip"><b>${c.baseline}</b><b>${c.bay}</b><b>${c.porch}</b></div><strong>NOT FIELD-RUN · E1 CONCEPT DESIGN · FORMAL QUOTE PENDING</strong></div>`;
  let html = fs.readFileSync(file, 'utf8');
  html = html
    .replace(/<title>[^<]*<\/title>/, `<title>${c.title}</title>`)
    .replace(/<p class="kicker">[^<]*<\/p>/, `<p class="kicker">${c.kicker}</p>`)
    .replace(/<p class="claim">[^<]*<\/p>/, `<p class="claim">${c.claim}</p>`)
    .replace(/<div class="first-look[^>]*>[\s\S]*?<\/div><nav class="review-nav"/, '<nav class="review-nav"')
    .replace('</div><nav class="review-nav"', `</div>${firstLook}<nav class="review-nav"`)
    .replace(/<script id="scenario-data"[\s\S]*?<\/script>/, `<script id="scenario-data" type="application/json">${data}</script>`)
    .replace(/<script id="atlas-data"[\s\S]*?<\/script>/, `<script id="atlas-data" type="application/json">${atlas}</script>`)
    .replace(/<script id="context-data"[\s\S]*?<\/script>/, `<script id="context-data" type="application/json">${context}</script>`);
  if (!html.includes('two-answers-v5.css')) html = html.replace('</head>', '<link rel="stylesheet" href="assets/two-answers-v5.css"></head>');
  if (html.includes('id="geometry-data"')) html = html.replace(/<script id="geometry-data"[\s\S]*?<\/script>/, `<script id="geometry-data" type="application/json">${JSON.stringify(geometry)}</script>`);
  else html = html.replace('<script src="assets/two-answers.js"></script>', `<script id="geometry-data" type="application/json">${JSON.stringify(geometry)}</script><script src="assets/two-answers.js"></script><script src="assets/two-answers-v5.js"></script>`);
  fs.writeFileSync(file, html.replace(/\r\n/g, '\n'));

  const report = path.join(ROOT, 'report', `proposal${lang === 'en' ? '.en' : ''}.html`);
  if (!fs.existsSync(report)) continue;
  let reportHtml = fs.readFileSync(report, 'utf8').replace(/<!-- V7_EXEC_START -->[\s\S]*?<!-- V7_EXEC_END -->/, '');
  const block = `<!-- V7_EXEC_START --><style>.v7-exec{margin:-42px -24px 36px;padding:44px 36px 34px;background:#0d2019;color:white}.v7-exec h1{font-size:46px;max-width:980px}.v7-exec>p{font-size:24px;color:#f7e2b7}.v7-exec-grid{display:grid;grid-template-columns:.7fr 1.3fr;gap:18px}.v7-exec-points{display:grid;gap:10px;align-content:start}.v7-exec-points b{padding:18px;background:#ffffff12;border-left:6px solid #176b55;font-size:18px}.v7-exec-points b:nth-child(2){border-color:#dc8b12}.v7-exec-points b:nth-child(3){border-color:#126d9b}.v7-exec figure{margin:0;background:#f3efe5;padding:10px;align-self:start}.v7-exec img{display:block;width:100%;height:auto;object-fit:contain}.v7-exec .v7-section img{height:185px}.v7-exec small{display:block;margin-top:12px;letter-spacing:.12em;color:#d8ebf4}@media(max-width:800px){.v7-exec-grid{grid-template-columns:1fr}.v7-exec .v7-section img{height:auto}}</style><section class="v7-exec"><h1>${c.reportTitle}</h1><p>${c.reportClaim}</p><div class="v7-exec-grid"><div class="v7-exec-points">${c.reportPoints.map(x => `<b>${x}</b>`).join('')}<figure class="v7-section"><img src="../assets/figures/hero-s7-section${suffix}.png" alt="S7 section"></figure></div><figure><img src="../assets/figures/site-overview${suffix}.png" alt="${c.overallAlt}"></figure></div><small>NOT FIELD-RUN · E1 CONCEPT DESIGN · FORMAL QUOTE PENDING</small></section><!-- V7_EXEC_END -->`;
  reportHtml = reportHtml.replace('<main>', `<main>${block}`);
  fs.writeFileSync(report, reportHtml.replace(/\r\n/g, '\n'));
}
console.log(`embedded V7 data and ${geometry.features.length} traceable GeoJSON objects`);
