#!/usr/bin/env node

/*
 * Regenerate the small set of presentation-only aids used by the mobility
 * package.  The script deliberately consumes only committed package files.
 * It does not add geometry, demand, route or performance data.
 */
const fs = require('fs');
const path = require('path');

const assetDir = __dirname;
const packageDir = path.resolve(assetDir, '..', '..');
const figureDir = path.join(packageDir, 'assets', 'figures');

const groundInterfacePairs = [
  {
    id: 'zhongzhiyuan',
    zh: 'key-area-zhongzhiyuan-ground-interface.svg',
    en: 'key-area-zhongzhiyuan-ground-interface.en.svg',
    required: {
      zh: ['交通台', '人工', '无障碍', '回退', '不表达'],
      en: ['enterprise desk', 'human', 'accessible', 'fallback', 'not an existing'],
    },
  },
  {
    id: 'ai-origin-community',
    zh: 'key-area-ai-origin-community-ground-interface.svg',
    en: 'key-area-ai-origin-community-ground-interface.en.svg',
    required: {
      zh: ['服务台', '人工', '轮椅', '退出', '不表达'],
      en: ['community desk', 'human', 'wheelchair', 'exit', 'does not prove'],
    },
  },
  {
    id: 'dazhongsi',
    zh: 'key-area-dazhongsi-transfer-interface.svg',
    en: 'key-area-dazhongsi-transfer-interface.en.svg',
    required: {
      zh: ['轨道', '人工', '无障碍', '回退', '不表达'],
      en: ['rail', 'human', 'accessible', 'fallback', 'does not prove'],
    },
  },
];

function numericAttr(attrs, name, fallback = 0) {
  const match = attrs.match(new RegExp(`${name}="(-?\\d+(?:\\.\\d+)?)"`));
  return match ? Number(match[1]) : fallback;
}

function svgText(svg) {
  return [...svg.matchAll(/<text\b[^>]*>([\s\S]*?)<\/text>/g)]
    .map((match) => match[1].replace(/<[^>]+>/g, '').trim())
    .join(' ');
}

function checkGroundInterfacePair(pair) {
  const errors = [];
  const textCounts = {};
  for (const [lang, file] of [['zh', pair.zh], ['en', pair.en]]) {
    const target = path.join(figureDir, file);
    if (!fs.existsSync(target)) {
      errors.push(`${lang}: missing ${file}`);
      continue;
    }
    const svg = fs.readFileSync(target, 'utf8');
    if ((svg.match(/<svg\b/g) || []).length !== 1 || !svg.trim().endsWith('</svg>')) errors.push(`${lang}: malformed svg wrapper`);
    if (!svg.includes('viewBox="0 0 1600 1000"')) errors.push(`${lang}: unexpected viewBox`);
    const text = svgText(svg);
    textCounts[lang] = (svg.match(/<text\b/g) || []).length;
    for (const token of pair.required[lang]) {
      if (!text.toLocaleLowerCase().includes(token.toLocaleLowerCase())) errors.push(`${lang}: missing semantic token ${token}`);
    }
    for (const match of svg.matchAll(/<rect\b([^>]*)\/?>/g)) {
      const attrs = match[1];
      const x = numericAttr(attrs, 'x');
      const y = numericAttr(attrs, 'y');
      const width = numericAttr(attrs, 'width');
      const height = numericAttr(attrs, 'height');
      if (x < 0 || y < 0 || x + width > 1600 || y + height > 1000) errors.push(`${lang}: rectangle outside viewBox`);
    }
  }
  if (textCounts.zh !== textCounts.en) errors.push(`text token counts differ zh=${textCounts.zh} en=${textCounts.en}`);
  return { id: pair.id, status: errors.length ? 'FAIL' : 'PASS', errors, text_counts: textCounts };
}

const groundInterfaceAudit = groundInterfacePairs.map(checkGroundInterfacePair);
if (groundInterfaceAudit.some((result) => result.status === 'FAIL')) {
  throw new Error(JSON.stringify({ ground_interface_audit: groundInterfaceAudit }, null, 2));
}

function readJson(rel) {
  return JSON.parse(fs.readFileSync(path.join(packageDir, rel), 'utf8'));
}

function esc(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function allCoordinates(geometry) {
  if (geometry.type === 'LineString') return geometry.coordinates;
  if (geometry.type === 'Polygon') return geometry.coordinates.flat();
  return [];
}

function centroid(feature) {
  const points = allCoordinates(feature.geometry);
  const sum = points.reduce((acc, p) => [acc[0] + p[0], acc[1] + p[1]], [0, 0]);
  return [sum[0] / points.length, sum[1] / points.length];
}

const boundary = readJson('geometry/site_boundary.geojson');
const keyAreas = readJson('geometry/key_areas.geojson');
const roads = readJson('geometry/roads.geojson');
const publicSpace = readJson('geometry/public_space.geojson');

const all = [
  ...boundary.features,
  ...keyAreas.features,
  ...roads.features,
  ...publicSpace.features,
].flatMap((feature) => allCoordinates(feature.geometry));
const xs = all.map((p) => p[0]);
const ys = all.map((p) => p[1]);
const minX = Math.min(...xs);
const maxX = Math.max(...xs);
const minY = Math.min(...ys);
const maxY = Math.max(...ys);
const map = { x: 70, y: 160, w: 1040, h: 650 };
const padX = (maxX - minX) * 0.06;
const padY = (maxY - minY) * 0.06;
const extent = {
  minX: minX - padX,
  maxX: maxX + padX,
  minY: minY - padY,
  maxY: maxY + padY,
};

function project(p) {
  const x = map.x + ((p[0] - extent.minX) / (extent.maxX - extent.minX)) * map.w;
  const y = map.y + map.h - ((p[1] - extent.minY) / (extent.maxY - extent.minY)) * map.h;
  return [Number(x.toFixed(1)), Number(y.toFixed(1))];
}

function pathFor(feature) {
  const points = allCoordinates(feature.geometry).map(project);
  if (!points.length) return '';
  const start = `M ${points[0][0]} ${points[0][1]}`;
  const body = points.slice(1).map((p) => `L ${p[0]} ${p[1]}`).join(' ');
  return `${start} ${body}${feature.geometry.type === 'Polygon' ? ' Z' : ''}`;
}

function polygon(feature, fill, stroke, extra = '') {
  return `<path d="${pathFor(feature)}" fill="${fill}" stroke="${stroke}" ${extra}/>`;
}

function line(feature, stroke, width, extra = '') {
  return `<path d="${pathFor(feature)}" fill="none" stroke="${stroke}" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round" ${extra}/>`;
}

function pointAt(feature, fraction) {
  const points = allCoordinates(feature.geometry);
  const start = points[0];
  const end = points[points.length - 1];
  return project([
    start[0] + (end[0] - start[0]) * fraction,
    start[1] + (end[1] - start[1]) * fraction,
  ]);
}

const areaColors = ['#8B5CF6', '#0EA5A4', '#F97316'];
const curbColors = ['#2A9D8F', '#F59E0B', '#7C3AED', '#E76F51', '#DC2626'];
const curbLabelsZh = ['开放通行', '预约窗口', '维护装卸', '人工优先', '应急保留'];
const curbLabelsEn = ['open', 'booked', 'service', 'human-only', 'emergency'];

function labelPosition(feature, index) {
  const [x, y] = project(centroid(feature));
  const offsets = [[0, -10], [0, 4], [0, 18]];
  const [dx, dy] = offsets[index] || [0, 0];
  return [x + dx, y + dy];
}

function mapSvg(lang) {
  const zh = lang === 'zh';
  const title = zh ? '交通共行环：把方式、重点区和路缘状态放回同一张图' : 'Mobility commons: modes, key areas and curb states in one spatial view';
  const subtitle = zh
    ? '概念关系图 · provisional 边界与设计线位 · 不表达现状道路、站点容量或实测 OD'
    : 'Conceptual relationship map · provisional boundary and design links · not observed roads, station capacity or OD';
  const areaNames = zh
    ? ['众智园 / 企业到岗', 'AI 原点社区 / 居民日常', '大钟寺 / 轨道换乘']
    : ['Zhongzhiyuan / enterprise arrival', 'AI Origin / resident daily access', 'Dazhongsi / rail transfer'];
  const modeLegend = zh
    ? ['轨道 / 公交骨干', '步行与无障碍', '自行车接驳', '汽车与服务路缘']
    : ['rail / bus backbone', 'walking / accessible', 'bicycle connection', 'car and service curb'];
  const proof = zh
    ? ['这张图能帮读者看懂', '三处重点区如何共享一套关系图', '企业、居民、轨道、路缘如何相遇', '五种路缘状态的责任入口', '这张图暂时不能证明', '官方红线、真实站点、现状流量', '居民需求、班次容量或运行许可', '空中出行航线，当前仍为 BLOCKED']
    : ['This map helps readers see', 'how the three key areas share one network', 'where enterprise, residents, rail and curb meet', 'where the five curb states enter the contract', 'This map does not prove', 'official redlines, real stations or observed flows', 'resident demand, timetable capacity or permits', 'an air route; the candidate remains BLOCKED'];
  const areaMarkup = keyAreas.features.map((feature, index) => {
    const [x, y] = labelPosition(feature, index);
    return `${polygon(feature, `${areaColors[index]}22`, areaColors[index], 'stroke-width="3" stroke-dasharray="9 7"')}<circle cx="${x}" cy="${y}" r="9" fill="${areaColors[index]}" stroke="#fff" stroke-width="3"/><text x="${x + 16}" y="${y + 5}" class="area">${esc(areaNames[index])}</text>`;
  }).join('');
  const roadMarkup = roads.features.map((feature, index) => {
    const roadClass = feature.properties.road_class || '';
    const stroke = roadClass === 'cycleway' ? '#FBBF24' : roadClass === 'pedestrian' ? '#2A9D8F' : '#5B8DEF';
    const width = roadClass === 'transit_connection' ? 11 : 7;
    const base = line(feature, stroke, width, 'opacity=".85"');
    const curb = Array.from({ length: 5 }, (_, state) => {
      const p1 = pointAt(feature, state / 5);
      const p2 = pointAt(feature, (state + 1) / 5);
      return `<line x1="${p1[0]}" y1="${p1[1]}" x2="${p2[0]}" y2="${p2[1]}" stroke="${curbColors[state]}" stroke-width="3" stroke-linecap="round"/>`;
    }).join('');
    const [lx, ly] = pointAt(feature, 0.56);
    return `${base}${curb}<circle cx="${lx}" cy="${ly}" r="4" fill="#fff" stroke="${stroke}" stroke-width="2"/>`;
  }).join('');
  const publicMarkup = publicSpace.features.map((feature) => polygon(feature, '#34D39918', '#34D399', 'stroke-width="2" stroke-dasharray="6 8"')).join('');
  const [externalLeftX, externalLeftY] = project([extent.minX, (minY + maxY) / 2]);
  const [externalRightX, externalRightY] = project([extent.maxX, (minY + maxY) / 2]);
  const [hubX, hubY] = project([(minX + maxX) / 2, (minY + maxY) / 2]);
  const nodes = keyAreas.features.map((feature, index) => {
    const [x, y] = project(centroid(feature));
    return `<circle cx="${x}" cy="${y}" r="18" fill="#0B2337" stroke="${areaColors[index]}" stroke-width="4"/><circle cx="${x}" cy="${y}" r="5" fill="#fff"/>`;
  }).join('');
  const stateLegend = curbLabelsZh.map((label, index) => `<g transform="translate(1185 ${270 + index * 40})"><rect width="18" height="18" rx="5" fill="${curbColors[index]}"/><text x="30" y="15" class="legend">${esc(zh ? label : curbLabelsEn[index])}</text></g>`).join('');
  const modes = [
    ['#5B8DEF', modeLegend[0]], ['#2A9D8F', modeLegend[1]], ['#FBBF24', modeLegend[2]], ['#E76F51', modeLegend[3]],
  ].map(([color, label], index) => `<g transform="translate(1185 ${520 + index * 38})"><line x1="0" y1="8" x2="26" y2="8" stroke="${color}" stroke-width="${index === 0 ? 9 : 6}" stroke-linecap="round"/><text x="40" y="14" class="legend">${esc(label)}</text></g>`).join('');
  const proofMarkup = proof.map((lineText, index) => `<text x="1185" y="${690 + index * 26}" class="${index === 0 || index === 4 ? 'proofHead' : 'proof'}">${esc(lineText)}</text>`).join('');
  const air = `<g transform="translate(965 205)"><rect width="115" height="54" rx="14" fill="#3B1F3A" stroke="#F472B6" stroke-width="2"/><text x="57" y="22" text-anchor="middle" class="air">AIR</text><text x="57" y="41" text-anchor="middle" class="airSmall">BLOCKED</text></g>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000" role="img" aria-labelledby="title desc">
  <title id="title">${esc(title)}</title>
  <desc id="desc">${esc(subtitle)}</desc>
  <defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#071A2B"/><stop offset="1" stop-color="#0E3448"/></linearGradient><filter id="shadow" x="-10%" y="-10%" width="130%" height="130%"><feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#000" flood-opacity=".22"/></filter><style>.sans{font-family:PingFang SC,Microsoft YaHei,Arial,sans-serif}.title{font-size:29px;font-weight:800;fill:#F5FBFF}.sub{font-size:16px;fill:#9FC0CF}.area{font-size:18px;font-weight:800;fill:#F6FBFF}.legend{font-size:15px;font-weight:700;fill:#DCEEF5}.proofHead{font-size:16px;font-weight:800;fill:#66E3CA}.proof{font-size:14px;fill:#A9C7D4}.small{font-size:13px;fill:#91B3C2}.nodeLabel{font-size:13px;fill:#E8F5FA}.air{font-size:16px;font-weight:900;fill:#F9A8D4}.airSmall{font-size:12px;font-weight:800;fill:#FBCFE8}</style></defs>
  <rect width="1600" height="1000" fill="url(#bg)"/><circle cx="1510" cy="80" r="290" fill="#1C7771" opacity=".18"/><circle cx="80" cy="950" r="300" fill="#3C4F89" opacity=".17"/>
  <text x="70" y="58" class="sans" fill="#64E4C5" font-size="18" font-weight="900" letter-spacing="3">MOBILITY COMMONS / SPATIAL RELATIONSHIP</text>
  <text x="70" y="98" class="sans title">${esc(title)}</text><text x="70" y="126" class="sans sub">${esc(subtitle)}</text>
  <g filter="url(#shadow)"><rect x="${map.x - 20}" y="${map.y - 18}" width="${map.w + 40}" height="${map.h + 36}" rx="28" fill="#0B2738" stroke="#24556B"/><rect x="1150" y="135" width="370" height="730" rx="28" fill="#0B2738" stroke="#24556B"/></g>
  <g opacity=".14">${Array.from({ length: 8 }, (_, i) => `<line x1="${map.x + i * 145}" y1="${map.y}" x2="${map.x + i * 145}" y2="${map.y + map.h}" stroke="#8EC9D6" stroke-width="1"/><line x1="${map.x}" y1="${map.y + i * 104}" x2="${map.x + map.w}" y2="${map.y + i * 104}" stroke="#8EC9D6" stroke-width="1"/>`).join('')}</g>
  ${polygon(boundary.features[0], '#F59E0B0B', '#FBBF24', 'stroke-width="4" stroke-dasharray="16 12"')}${publicMarkup}${areaMarkup}${roadMarkup}
  <path d="M ${externalLeftX} ${externalLeftY} C ${hubX - 180} ${hubY - 110}, ${hubX - 80} ${hubY - 40}, ${hubX} ${hubY}" fill="none" stroke="#F8FAFC" stroke-width="3" stroke-dasharray="10 10" opacity=".65"/><path d="M ${externalRightX} ${externalRightY} C ${hubX + 180} ${hubY + 90}, ${hubX + 90} ${hubY + 30}, ${hubX} ${hubY}" fill="none" stroke="#F8FAFC" stroke-width="3" stroke-dasharray="10 10" opacity=".65"/>
  ${nodes}${air}<text x="${map.x + 20}" y="${map.y + map.h - 18}" class="sans small">${esc(zh ? '对外通勤：跨边界关系线，仅用于说明接口' : 'External commuting: cross-boundary relationship lines, for interface reading only')}</text>
  <g transform="translate(1185 178)"><text class="sans" y="0" fill="#66E3CA" font-size="18" font-weight="900">${esc(zh ? '路缘五态 / 责任入口' : 'Five curb states / ownership entry')}</text><text y="26" class="sans small">${esc(zh ? '颜色只表示概念状态，不代表现状占用' : 'Colors show a concept contract, not observed occupancy')}</text></g>
  ${stateLegend}<g transform="translate(1185 480)"><text class="sans" y="0" fill="#66E3CA" font-size="18" font-weight="900">${esc(zh ? '方式关系' : 'Mode relationship')}</text></g>${modes}
  ${proofMarkup}<text x="1185" y="910" class="sans small">${esc(zh ? '来源：package GeoJSON · synthetic / provisional' : 'Source: package GeoJSON · synthetic / provisional')}</text>
  <text x="70" y="925" class="sans small">${esc(zh ? '空间关系图 · 先读三处重点区，再读方式与路缘状态；所有线位均为概念建议' : 'Spatial relationship map · read the three areas first, then modes and curb states; all links are conceptual')}</text>
</svg>`;
}

fs.writeFileSync(path.join(figureDir, 'mobility-spatial-plan.svg'), mapSvg('zh'));
fs.writeFileSync(path.join(figureDir, 'mobility-spatial-plan.en.svg'), mapSvg('en'));

const chain = {
  zh: ['区域覆盖', '网络边节点', '运力缺口', '群体分布', '可达性尾部', '资源敏感性', '稳健性'],
  en: ['regional scale', 'network flow', 'capacity gap', 'group distribution', 'accessibility tail', 'resource sensitivity', 'robustness'],
};
const chainColors = ['#4DE1BF', '#6EA5FF', '#F7BF63', '#F07D9E', '#F4A261', '#B8A1FF', '#5ED6D0'];
const boardNames = [
  ['regional-scale-commute-board.svg', 'regional-scale-commute-board.en.svg'],
  ['network-flow-board.svg', 'network-flow-board.en.svg'],
  ['capacity-closure-board.svg', 'capacity-closure-board.en.svg'],
  ['distributional-equity-board.svg', 'distributional-equity-board.en.svg'],
  ['distributional-accessibility-board.svg', 'distributional-accessibility-board.en.svg'],
  ['resource-pressure-board.svg', 'resource-pressure-board.en.svg'],
  ['robustness-screen-board.svg', 'robustness-screen-board.en.svg'],
];

function addRibbon(file, lang) {
  const target = path.join(figureDir, file);
  let svg = fs.readFileSync(target, 'utf8');
  if (svg.includes('id="evidence-chain-ribbon"')) {
    svg = svg.replace(/<g id="evidence-chain-ribbon">[\s\S]*?<\/g>/, '');
  }
  const match = svg.match(/viewBox="0 0 (\d+(?:\.\d+)?) (\d+(?:\.\d+)?)"/);
  if (!match) throw new Error(`no viewBox in ${file}`);
  const width = Number(match[1]);
  const height = Number(match[2]);
  const x = 40;
  const y = height - 92;
  const gap = 8;
  const labels = chain[lang];
  const boxWidth = (width - x * 2 - gap * (labels.length - 1)) / labels.length;
  const title = lang === 'zh' ? '同一份区域 runner · 七个读出视角' : 'ONE REGIONAL RUNNER · SEVEN READOUT VIEWS';
  const note = lang === 'zh' ? '同源聚合证据，不是七组独立的现场结果' : 'one aggregate evidence chain, not seven independent field results';
  const boxes = labels.map((label, index) => {
    const bx = x + index * (boxWidth + gap);
    return `<rect x="${bx.toFixed(1)}" y="${y}" width="${boxWidth.toFixed(1)}" height="38" rx="10" fill="${chainColors[index]}22" stroke="${chainColors[index]}" stroke-width="1.5"/><text x="${(bx + 14).toFixed(1)}" y="${y + 25}" font-family="Arial,sans-serif" font-size="14" font-weight="800" fill="#E8F8FA">${esc(`${index + 1}  ${label}`)}</text>`;
  }).join('');
  const ribbon = `<g id="evidence-chain-ribbon"><rect x="0" y="${y - 18}" width="${width}" height="${height - y + 18}" fill="#071A2B" opacity=".96"/><text x="${x}" y="${y - 1}" font-family="Arial,sans-serif" font-size="14" font-weight="800" fill="#66E3CA">${esc(title)}</text><text x="${width - x}" y="${y - 1}" text-anchor="end" font-family="Arial,sans-serif" font-size="12" fill="#9FC0CF">${esc(note)}</text>${boxes}</g>`;
  svg = svg.replace('</svg>', `${ribbon}</svg>`);
  fs.writeFileSync(target, svg);
}

boardNames.forEach(([zh, en]) => {
  addRibbon(zh, 'zh');
  addRibbon(en, 'en');
});

function updateVisualIndex(file, lang) {
  const target = path.join(packageDir, 'visual', file);
  let html = fs.readFileSync(target, 'utf8');
  const zh = lang === 'zh';
  const suffix = zh ? '' : '.en';
  const oldAlt = zh ? '三处重点区，一条共行环' : 'Three areas, one operating loop';
  const newAlt = zh ? '交通共行环空间关系图' : 'Mobility commons spatial relationship map';
  const oldImage = `../assets/figures/site-overview${suffix}.png" alt="${oldAlt}`;
  const newImage = `../assets/figures/mobility-spatial-plan${suffix}.svg" alt="${newAlt}`;
  html = html.replace(oldImage, newImage);
  const regionalMarker = `<img src="../assets/figures/regional-scale-commute-board${suffix}.svg"`;
  const chainTitle = zh ? '同一份区域 runner，七个读出视角' : 'One regional runner, seven readout views';
  const chainText = zh
    ? '区域覆盖 → 网络边节点 → 运力缺口 → 群体分布 → 可达性尾部 → 资源敏感性 → 稳健性。七张图共享一份合成聚合证据，任何一张都不代表现场绩效。'
    : 'Regional scale → network flow → capacity gap → group distribution → accessibility tail → resource sensitivity → robustness. Seven boards share one synthetic aggregate evidence chain; none is field performance.';
  const chain = `<div class="evidence-chain"><strong>${chainTitle}</strong><span>${chainText}</span></div>`;
  const oldChainTitle = zh ? '同一份区域 runner，六个读出视角' : 'One regional runner, six readout views';
  const oldChainText = zh
    ? '区域覆盖 → 网络边节点 → 运力缺口 → 群体分布 → 资源敏感性 → 稳健性。六张图共享一份合成聚合证据，任何一张都不代表现场绩效。'
    : 'Regional scale → network flow → capacity gap → group distribution → resource sensitivity → robustness. Six boards share one synthetic aggregate evidence chain; none is field performance.';
  html = html.replace(oldChainTitle, chainTitle).replace(oldChainText, chainText);
  if (!html.includes('class="evidence-chain"')) html = html.replace(regionalMarker, `${chain}${regionalMarker}`);
  const css = '.evidence-chain{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;background:#0B2738;color:#E6FFFA;border:1px solid #2A9D8F;border-radius:12px;padding:12px 14px;margin:10px 0 14px;font-size:12px}.evidence-chain strong{color:#66E3CA;white-space:nowrap}.evidence-chain span{color:#B6D3DC}';
  if (!html.includes('.evidence-chain{')) html = html.replace('</style></head>', `${css}</style></head>`);

  const taskSectionStart = html.indexOf('<section id="10" class="evidence">');
  const taskSectionEnd = taskSectionStart >= 0 ? html.indexOf('</section>', taskSectionStart) : -1;
  const taskbookBoard = `assets/figures/taskbook-crosswalk-board${suffix}.svg`;
  if (taskSectionStart >= 0 && taskSectionEnd >= 0 && !html.includes(taskbookBoard)) {
    const taskbookTitle = zh ? '六项任务与本包交通交付的对照' : 'Six taskbook items and this package contribution';
    const taskbookNote = zh
      ? '把本包负责的交通交付、评审入口和未声称事项放在同一张图里；不把交通包读成整带总包。'
      : 'The board separates this package contribution, review entry points and non-claims; it is not a whole-corridor package.';
    const taskbookBlock = `<div class="evidence-chain"><strong>${taskbookTitle}</strong><span>${taskbookNote}</span></div><img src="../${taskbookBoard}" alt="${taskbookTitle}">`;
    html = `${html.slice(0, taskSectionEnd)}${taskbookBlock}${html.slice(taskSectionEnd)}`;
  }

  const areaSectionStart = html.indexOf('<section id="2" class="evidence">');
  const areaSectionEnd = areaSectionStart >= 0 ? html.indexOf('</section>', areaSectionStart) : -1;
  const areaPrefix = 'assets/figures/key-area-';
  if (zh && areaSectionStart >= 0 && areaSectionEnd >= 0 && !html.includes(`${areaPrefix}zhongzhiyuan-ground-interface.svg`)) {
    const areaBlock = '<div class="evidence-chain"><strong>三处重点区的地面界面</strong><span>入口、等待、停放、换乘和求助先画清楚；图面无尺度，不新增容量或现状主张。</span></div><img src="../assets/figures/key-area-zhongzhiyuan-ground-interface.svg" alt="众智园企业到岗地面界面概念图"><img src="../assets/figures/key-area-ai-origin-community-ground-interface.svg" alt="AI 原点社区居民日常地面界面概念图"><img src="../assets/figures/key-area-dazhongsi-transfer-interface.svg" alt="大钟寺轨道换乘与路缘界面概念剖面">';
    html = `${html.slice(0, areaSectionEnd)}${areaBlock}${html.slice(areaSectionEnd)}`;
  }

  if (!zh && !html.includes('taskbook-crosswalk-board.en.svg')) {
    const enTaskbookMarker = '<h2>Reading Labels and Evidence Boundaries</h2>';
    const enTaskbookBlock = '<h2>Taskbook Crosswalk for This Mobility Package</h2><p>The six taskbook items remain belt-wide work. This package shows only the transport contribution it can deliver, the shortest review entry and the claims it deliberately leaves open.</p><figure class="proposal-figure"><img src="../assets/figures/taskbook-crosswalk-board.en.svg" alt="Taskbook crosswalk board for the mobility package"><figcaption>Taskbook crosswalk: mobility contribution, review entry points and non-claims</figcaption></figure>';
    if (html.includes(enTaskbookMarker)) html = html.replace(enTaskbookMarker, `${enTaskbookBlock}${enTaskbookMarker}`);
  }

  if (!zh && !html.includes('key-area-zhongzhiyuan-ground-interface.en.svg')) {
    const enAreaMarker = '<h2>Detailed Design of Key Areas</h2>';
    const enAreaBlock = '<div class="evidence-chain"><strong>Three key-area ground interfaces</strong><span>Entry, waiting, parking, transfer and help are shown first; drawings are scale-free and add no capacity or existing-condition claim.</span></div><figure class="proposal-figure"><img src="../assets/figures/key-area-zhongzhiyuan-ground-interface.en.svg" alt="Zhongzhiyuan enterprise-arrival ground interface concept"><figcaption>Zhongzhiyuan enterprise-arrival ground interface</figcaption></figure><figure class="proposal-figure"><img src="../assets/figures/key-area-ai-origin-community-ground-interface.en.svg" alt="AI Origin Community resident daily ground interface concept"><figcaption>AI Origin Community resident daily ground interface</figcaption></figure><figure class="proposal-figure"><img src="../assets/figures/key-area-dazhongsi-transfer-interface.en.svg" alt="Dazhongsi rail-transfer and curb interface concept section"><figcaption>Dazhongsi rail-transfer and curb interface</figcaption></figure>';
    if (html.includes(enAreaMarker)) html = html.replace(enAreaMarker, `${enAreaMarker}${enAreaBlock}`);
  }

  const networkBoard = `../assets/figures/network-flow-board${suffix}.svg`;
  const distributionalBoard = `../assets/figures/distributional-equity-board${suffix}.svg`;
  const accessibilityBoard = `../assets/figures/distributional-accessibility-board${suffix}.svg`;
  const networkAlt = zh
    ? '全量人员动线与网络压力屏查'
    : 'Population-scale people flow and network pressure screen';
  const regionalAlt = zh ? '区域人口规模通勤综合模拟' : 'Regional population-scale commute simulation';
  const regionalImage = `<img src="../assets/figures/regional-scale-commute-board${suffix}.svg" alt="${regionalAlt}">`;
  const networkImage = `<img src="${networkBoard}" alt="${networkAlt}">`;
  const distributionalAlt = zh
    ? '六类人的群体分布与公平屏查'
    : 'Distributional and equity screen for six groups';
  const distributionalImage = `<img src="${distributionalBoard}" alt="${distributionalAlt}">`;
  const accessibilityAlt = zh
    ? '六类合成群体的可达性尾部与最低群体门槛'
    : 'Accessibility tail and lowest-group gate for six synthetic groups';
  const accessibilityImage = `<img src="${accessibilityBoard}" alt="${accessibilityAlt}">`;
  if (!html.includes(networkBoard)) html = html.replace(regionalImage, `${regionalImage}${networkImage}`);
  if (!html.includes(distributionalBoard)) html = html.replace(networkImage, `${networkImage}${distributionalImage}`);
  if (!html.includes(accessibilityBoard)) html = html.replace(distributionalImage, `${distributionalImage}${accessibilityImage}`);
  const distributionalScreen = zh
    ? '<section class="evidence multimodal-board"><div class="section-head"><span class="section-no">22</span><h2>群体分布与可达性尾部</h2><span class="tag">合成屏查</span></div><p>同一份区域 runner 按六类群体回读个体合成时间、满意度与可达性代理。O4 下物流/维护组的满意度代理 P10 为 50/100，夜班工作者的通勤时间 P90 分箱为 90 分钟，群体 P10 差距为 20 个代理分；可达性代理 P10 差距为 5 个代理点。名义可达性门槛为 20 个代理点，压力门为 30 个代理点。P10 把分布尾部留在平均值旁边；这些是合成屏查读数，不是居民体验、居民无障碍走查、服务审计或运营绩效。</p><figure class="proposal-figure"><img src="../assets/figures/distributional-equity-board.svg" alt="六类合成群体的分布与公平屏查"><figcaption>六类合成群体的分布与公平屏查</figcaption></figure><figure class="proposal-figure"><img src="../assets/figures/distributional-accessibility-board.svg" alt="六类合成群体的可达性尾部与最低群体门槛"><figcaption>六类合成群体的可达性尾部与最低群体门槛</figcaption></figure><div class="micro">distributional-equity-board.svg · distributional-accessibility-board.svg · regional-scale-commute-readout.json · 合成分箱，不是本地结果</div></section>'
    : '<section class="evidence multimodal-board"><div class="section-head"><span class="section-no">22</span><h2>Distributional equity and accessibility tail</h2><span class="tag">SYNTHETIC SCREEN</span></div><p>The same regional runner bins synthetic per-agent travel time, satisfaction and accessibility proxies by six groups. Under O4, the logistics/maintenance group has a satisfaction-proxy P10 of 50/100, night workers have a P90 travel-time bin of 90 minutes, the group P10 spread is 20 proxy points and the accessibility-proxy P10 spread is 5 proxy points. The nominal accessibility gate is 20 points and the stress gate is 30 points. P10 keeps the lower tail visible beside the overall mean; these are synthetic screen outputs, not resident experience, a resident accessibility walk-through, an accessibility audit or operating performance.</p><figure class="proposal-figure"><img src="../assets/figures/distributional-equity-board.en.svg" alt="Distributional and equity screen for six synthetic groups"><figcaption>Distributional and equity screen for six synthetic groups</figcaption></figure><figure class="proposal-figure"><img src="../assets/figures/distributional-accessibility-board.en.svg" alt="Accessibility tail and lowest-group gate for six synthetic groups"><figcaption>Accessibility tail and lowest-group gate for six synthetic groups</figcaption></figure><div class="micro">distributional-equity-board.en.svg · distributional-accessibility-board.en.svg · regional-scale-commute-readout.json · synthetic bins, not local outcomes</div></section>';
  const hasDistributionalText = zh
    ? html.includes('<span class="section-no">22</span><h2>群体分布与公平屏查</h2>')
    : html.includes('<span class="section-no">22</span><h2>Distributional equity screen</h2>');
  if (!hasDistributionalText) html = html.replace('</main>', `${distributionalScreen}</main>`);
  const accessibilityScreen = zh
    ? '<section class="evidence multimodal-board"><div class="section-head"><span class="section-no">23</span><h2>可达性尾部与最低群体门槛</h2><span class="tag">合成屏查</span></div><p>同一份 runner 按六类合成群体回读可达性代理 P10、P50 和 P90。O4 的可达性代理 P10 差距为 5 个代理点，名义使用 20 个代理点门槛；强天气压力下 O2 为 20 个代理点，压力门为 30 个代理点。这是合成充分性屏查，不是居民无障碍走查、服务可达性审计或运营承诺。</p><figure class="proposal-figure"><img src="../assets/figures/distributional-accessibility-board.svg" alt="六类合成群体的可达性尾部与最低群体门槛"><figcaption>六类合成群体的可达性尾部与最低群体门槛</figcaption></figure><div class="micro">distributional-accessibility-board.svg · regional-scale-commute-readout.json · 合成屏查，不是本地结果</div></section>'
    : '<section class="evidence multimodal-board"><div class="section-head"><span class="section-no">23</span><h2>Accessibility tail and lowest-group gate</h2><span class="tag">SYNTHETIC SCREEN</span></div><p>The same runner bins accessibility proxies for six synthetic groups at P10, P50 and P90. The nominal O4 accessibility-proxy P10 spread is 5 proxy points against a 20-point gate; under severe-weather stress O2 is 20 proxy points against a 30-point stress gate. This is a synthetic sufficiency screen, not a resident accessibility walk-through, an accessibility audit or an operating promise.</p><figure class="proposal-figure"><img src="../assets/figures/distributional-accessibility-board.en.svg" alt="Accessibility tail and lowest-group gate for six synthetic groups"><figcaption>Accessibility tail and lowest-group gate for six synthetic groups</figcaption></figure><div class="micro">distributional-accessibility-board.en.svg · regional-scale-commute-readout.json · synthetic screen, not a local outcome</div></section>';
  const hasAccessibilityText = zh
    ? html.includes('<span class="section-no">23</span><h2>可达性尾部与最低群体门槛</h2>')
    : html.includes('<span class="section-no">23</span><h2>Accessibility tail and lowest-group gate</h2>');
  if (!hasAccessibilityText) html = html.replace('</main>', `${accessibilityScreen}</main>`);
  if (zh) html = html.replace('名义门槛为 20 个代理点；强天气压力下 O2', '名义使用 20 个代理点门槛；强天气压力下 O2');
  fs.writeFileSync(target, html);
}

updateVisualIndex('index.html', 'zh');
updateVisualIndex('index.en.html', 'en');

console.log(JSON.stringify({
  ok: true,
  ground_interface_audit: groundInterfaceAudit,
  generated: ['assets/figures/mobility-spatial-plan.svg', 'assets/figures/mobility-spatial-plan.en.svg'],
  ribbon_boards: boardNames.flat(),
  source_boundary: 'geometry/site_boundary.geojson',
  source_key_areas: 'geometry/key_areas.geojson',
  source_roads: 'geometry/roads.geojson',
  visual_index: ['visual/index.html', 'visual/index.en.html'],
  note: 'presentation aids only; no demand, geometry or performance values changed'
}, null, 2));
