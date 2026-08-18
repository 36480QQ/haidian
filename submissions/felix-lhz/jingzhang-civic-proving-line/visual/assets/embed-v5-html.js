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
      return id.startsWith('V6-') || (id.startsWith('V5-') && !id.startsWith('V5-D-'));
    }),
};
const copy = {
  zh: {
    title: '京张双答 V6｜大钟寺城市采纳样板',
    kicker: 'JING-ZHANG TWO ANSWERS · V6',
    claim: '每一次 AI 试验，都必须在真实城市空间中保留一条不被牺牲的公共路径，并留下可审计的城市采纳回执。',
    overallAlt: '一脊三站两翼总体城市设计',
    s7Alt: '大钟寺城市采纳样板 1:500 详图',
    stateDetail: '普通交通与公共空间独立运行',
  },
  en: {
    title: 'Jing-Zhang Two Answers V6 | Dazhongsi Civic Adoption Sample',
    kicker: 'JING-ZHANG TWO ANSWERS · V6',
    claim: 'Every AI trial must preserve a non-negotiable public route in real urban space and leave an auditable civic adoption receipt.',
    overallAlt: 'One spine, three stations and two wings',
    s7Alt: 'Dazhongsi civic adoption sample at 1:500',
    stateDetail: 'Conventional transit and public space operate independently',
  },
};

for (const lang of ['zh', 'en']) {
  const file = path.join(ROOT, 'visual', `index${lang === 'en' ? '.en' : ''}.html`);
  const c = copy[lang];
  const suffix = lang === 'en' ? '.en' : '';
  const firstLook = `<div class="first-look v6"><div class="v6-review-grid"><figure><img src="../assets/figures/site-overview${suffix}.png" alt="${c.overallAlt}"><figcaption>${lang === 'zh' ? '总体：一脊 · 三站 · 两翼' : 'OVERALL: SPINE · STATIONS · WINGS'}</figcaption></figure><section class="v6-state-panel"><img src="../assets/figures/hero-s7-detail${suffix}.png" alt="${c.s7Alt}"><div class="v6-state-controls" aria-label="S7 operating states"><button type="button" data-state-view="OPEN" aria-pressed="true">OPEN</button><button type="button" data-state-view="TRIAL" aria-pressed="false">TRIAL</button><button type="button" data-state-view="PAUSE" aria-pressed="false">PAUSE</button><button type="button" data-state-view="RETIRE" aria-pressed="false">RETIRE</button></div><div class="v6-state-copy"><b id="v6StateLabel">OPEN</b><span id="v6StateDetail">${c.stateDetail}</span></div></section></div><strong>NOT FIELD-RUN · E1 CONCEPT DESIGN · S7 FLAGSHIP</strong></div>`;
  let html = fs.readFileSync(file, 'utf8');
  html = html
    .replace(/<title>[^<]*<\/title>/, `<title>${c.title}</title>`)
    .replace(/<p class="kicker">[^<]*<\/p>/, `<p class="kicker">${c.kicker}</p>`)
    .replace(/<p class="claim">[^<]*<\/p>/, `<p class="claim">${c.claim}</p>`)
    .replace(/<div class="first-look(?: v6)?">[\s\S]*?<\/div><nav class="review-nav"/, '<nav class="review-nav"')
    .replace('</div><nav class="review-nav"', `</div>${firstLook}<nav class="review-nav"`)
    .replace(/<script id="scenario-data"[\s\S]*?<\/script>/, `<script id="scenario-data" type="application/json">${data}</script>`)
    .replace(/<script id="atlas-data"[\s\S]*?<\/script>/, `<script id="atlas-data" type="application/json">${atlas}</script>`)
    .replace(/<script id="context-data"[\s\S]*?<\/script>/, `<script id="context-data" type="application/json">${context}</script>`);
  if (!html.includes('two-answers-v5.css')) html = html.replace('</head>', '<link rel="stylesheet" href="assets/two-answers-v5.css"></head>');
  if (html.includes('id="geometry-data"')) html = html.replace(/<script id="geometry-data"[\s\S]*?<\/script>/, `<script id="geometry-data" type="application/json">${JSON.stringify(geometry)}</script>`);
  else html = html.replace('<script src="assets/two-answers.js"></script>', `<script id="geometry-data" type="application/json">${JSON.stringify(geometry)}</script><script src="assets/two-answers.js"></script><script src="assets/two-answers-v5.js"></script>`);
  fs.writeFileSync(file, html.replace(/\r\n/g, '\n'));
}
console.log(`embedded V6 data and ${geometry.features.length} traceable GeoJSON objects`);
