#!/usr/bin/env node
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const zlib = require('zlib');
const { spawnSync } = require('child_process');

const HERE = __dirname;
const ROOT = path.resolve(HERE, '../..');
const FIGURES = path.join(ROOT, 'assets/figures');
const osmEnvelope = read('visual/assets/site-context-osm.json');
const osm = JSON.parse(zlib.gunzipSync(Buffer.from(osmEnvelope.payload, 'base64')).toString('utf8'));
const results = read('visual/assets/site-context-results.json');
const keyAreas = read('geometry/key_areas.geojson');
const landUse = read('geometry/land_use.geojson');

const W = 2000;
const H = 1200;
const C = {
  ink: '#101d31', muted: '#607089', paper: '#f4f7fa', white: '#ffffff',
  cyan: '#20b7b1', blue: '#2e78d7', amber: '#e9aa27', coral: '#f06b5b',
  green: '#35aa7b', paleBlue: '#dceafa', paleGreen: '#dff3ea', paleAmber: '#fff0c7',
  paleCoral: '#fde3df', line: '#cad6e5', building: '#c7ced7', road: '#94a1b2', water: '#9dd8e4',
};
const stationColors = [C.blue, C.green, C.amber];
const stationNames = {
  zh: ['众智园', 'AI原点', '大钟寺'],
  en: ['ZHONGZHI', 'AI ORIGIN', 'DAZHONGSI'],
};

function read(relative) {
  return JSON.parse(fs.readFileSync(path.join(ROOT, relative), 'utf8'));
}

function esc(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;' }[char]));
}

function text(x, y, value, size, color = C.ink, weight = 400, anchor = 'start') {
  return `<text x="${x}" y="${y}" font-family="Noto Sans CJK SC, sans-serif" font-size="${size}" font-weight="${weight}" fill="${color}" text-anchor="${anchor}">${esc(value)}</text>`;
}

function lines(x, y, values, size, color = C.muted, weight = 400, gap = 1.45) {
  return values.map((value, index) => text(x, y + index * size * gap, value, size, color, weight)).join('');
}

function header(index, titleZh, titleEn, subtitleZh, subtitleEn, lang) {
  const title = lang === 'zh' ? titleZh : titleEn;
  const subtitle = lang === 'zh' ? subtitleZh : subtitleEn;
  return `<rect width="${W}" height="136" fill="${C.ink}"/>
    ${text(58, 48, `${String(index).padStart(2, '0')} / X JINGZHANG`, 18, C.cyan, 700)}
    ${text(58, 100, title, 38, C.white, 700)}
    ${text(1942, 96, subtitle, 18, '#c9d5e6', 400, 'end')}`;
}

function footer(lang) {
  const note = lang === 'zh'
    ? 'OSM 公开现状切片 © OpenStreetMap contributors · ODbL 1.0；临时重点区仅用于概念定位，不是法定红线、权属或工程测绘。'
    : 'Public OSM context © OpenStreetMap contributors · ODbL 1.0; provisional key-area boxes are not statutory boundaries, ownership or survey data.';
  return `<line x1="58" y1="1142" x2="1942" y2="1142" stroke="${C.line}"/>
    ${text(58, 1172, note, 15, C.muted)}
    ${text(1942, 1172, 'X JINGZHANG · PUBLIC CONTEXT / CONCEPT ACTION', 14, C.muted, 600, 'end')}`;
}

function extentForRing(ring, pad = 0.08) {
  const xs = ring.map((point) => point[0]);
  const ys = ring.map((point) => point[1]);
  const dx = Math.max(...xs) - Math.min(...xs);
  const dy = Math.max(...ys) - Math.min(...ys);
  return [Math.min(...xs) - dx * pad, Math.min(...ys) - dy * pad, Math.max(...xs) + dx * pad, Math.max(...ys) + dy * pad];
}

function project(point, extent, rect) {
  const [west, south, east, north] = extent;
  return [
    rect.x + ((point[0] - west) / (east - west)) * rect.w,
    rect.y + (1 - (point[1] - south) / (north - south)) * rect.h,
  ];
}

function pathData(points, extent, rect, close = false) {
  const projected = points.map((point) => project(point, extent, rect));
  return projected.map((point, index) => `${index ? 'L' : 'M'}${point[0].toFixed(1)},${point[1].toFixed(1)}`).join(' ') + (close ? ' Z' : '');
}

function intersects(feature, extent) {
  return feature.coordinates.some(([lon, lat]) => lon >= extent[0] && lon <= extent[2] && lat >= extent[1] && lat <= extent[3]);
}

function mapLayer(extent, rect, clipId, options = {}) {
  const features = osm.features.filter((feature) => intersects(feature, extent));
  const order = ['park', 'water', 'building', 'waterway', 'highway', 'railway'];
  let body = `<defs><clipPath id="${clipId}"><rect x="${rect.x}" y="${rect.y}" width="${rect.w}" height="${rect.h}" rx="4"/></clipPath></defs>`;
  body += `<g clip-path="url(#${clipId})"><rect x="${rect.x}" y="${rect.y}" width="${rect.w}" height="${rect.h}" fill="#eef2f5"/>`;
  for (const klass of order) {
    for (const feature of features.filter((item) => item.class === klass)) {
      const close = ['park', 'water', 'building'].includes(klass);
      let fill = 'none';
      let stroke = C.road;
      let width = 0.8;
      let opacity = 0.7;
      if (klass === 'park') { fill = C.paleGreen; stroke = '#9bcbb5'; opacity = 0.9; }
      if (klass === 'water') { fill = '#d7f0f4'; stroke = C.water; opacity = 1; }
      if (klass === 'building') { fill = C.building; stroke = '#b4bdc9'; opacity = options.lightBuildings ? 0.36 : 0.62; }
      if (klass === 'waterway') { stroke = C.water; width = 2.2; opacity = 0.95; }
      if (klass === 'highway') {
        const type = feature.tags.highway;
        const major = ['motorway', 'trunk', 'primary', 'secondary'].includes(type);
        const walk = ['footway', 'path', 'pedestrian', 'steps', 'cycleway'].includes(type);
        stroke = walk ? '#6ea9a3' : major ? '#73859b' : '#aeb8c5';
        width = walk ? 1.05 : major ? 2.1 : 0.8;
        opacity = walk ? 0.78 : 0.62;
      }
      if (klass === 'railway') { stroke = C.ink; width = 2.1; opacity = 0.8; }
      body += `<path d="${pathData(feature.coordinates, extent, rect, close)}" fill="${fill}" stroke="${stroke}" stroke-width="${width}" opacity="${opacity}"/>`;
    }
  }
  body += '</g>';
  return body;
}

function ringOverlay(ring, extent, rect, color, label) {
  const center = ring.slice(0, -1).reduce((acc, point) => [acc[0] + point[0] / (ring.length - 1), acc[1] + point[1] / (ring.length - 1)], [0, 0]);
  const [cx, cy] = project(center, extent, rect);
  return `<path d="${pathData(ring, extent, rect, true)}" fill="${color}" fill-opacity="0.08" stroke="${color}" stroke-width="3" stroke-dasharray="10 7"/>
    <circle cx="${cx}" cy="${cy}" r="12" fill="${color}" stroke="white" stroke-width="4"/>
    ${text(cx + 18, cy + 7, label, 17, C.ink, 700)}`;
}

function svgWrap(content) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><rect width="${W}" height="${H}" fill="${C.paper}"/>${content}</svg>`;
}

function keyAreasFigure(lang) {
  const zh = lang === 'zh';
  const title = ['三站现场合同', 'THREE STATIONS AS SITE CONTRACTS'];
  const subtitle = ['真实公开底图 × 三种不可互换的城市决定', 'PUBLIC MAP CONTEXT × THREE NON-INTERCHANGEABLE DECISIONS'];
  const roles = zh ? ['TEST / 技术边界', 'RELEASE / 权利边界', 'USE / 公众边界'] : ['TEST / TECHNICAL LIMIT', 'RELEASE / RIGHTS LIMIT', 'USE / PUBLIC LIMIT'];
  const questions = zh ? ['它能否在边界内工作？', '它是否有权被有限发布？', '城市是否愿意继续使用？'] : ['Can it work inside the limit?', 'May it be released for limited use?', 'Will the city continue using it?'];
  const systems = zh ? [
    ['电子围栏 + 最小风险停车', '实体急停 + 版本事件日志'],
    ['组件清单 + 许可核对', '期限、责任人 + 公开撤回'],
    ['人工服务 + 无AI等价路径', '投诉直达 + Public Verdict'],
  ] : [
    ['geofence + minimum-risk stop', 'physical E-stop + versioned log'],
    ['component inventory + licence check', 'expiry, owner + visible withdrawal'],
    ['staffed service + non-AI equivalent', 'direct complaint + Public Verdict'],
  ];
  const fail = zh ? ['机器口袋关闭；公众院落继续', '发布界面撤下；教学协作继续', '试用口袋关闭；人工服务继续'] : ['close machine pocket; keep public court', 'withdraw release; keep learning/collaboration', 'close trial pocket; keep staffed service'];
  let body = header(3, title[0], title[1], subtitle[0], subtitle[1], lang);
  const panelW = 606;
  keyAreas.features.forEach((area, index) => {
    const x = 58 + index * 636;
    const ring = area.geometry.coordinates[0];
    const extent = extentForRing(ring, 0.14);
    const rect = { x, y: 177, w: panelW, h: 420 };
    const metric = results.key_area_metrics[index];
    body += `<rect x="${x}" y="160" width="${panelW}" height="920" rx="5" fill="${C.white}" stroke="${C.line}"/>
      <rect x="${x}" y="160" width="${panelW}" height="10" fill="${stationColors[index]}"/>`;
    body += mapLayer(extent, rect, `key-${lang}-${index}`);
    body += ringOverlay(ring, extent, rect, stationColors[index], stationNames[lang][index]);
    body += text(x + 24, 635, `${String(index + 1).padStart(2, '0')}  ${stationNames[lang][index]}`, 26, C.ink, 700);
    body += text(x + 24, 674, roles[index], 18, stationColors[index], 700);
    body += text(x + 24, 719, questions[index], 24, C.ink, 700);
    body += lines(x + 24, 765, systems[index], 17, C.muted, 400, 1.55);
    body += `<line x1="${x + 24}" y1="836" x2="${x + panelW - 24}" y2="836" stroke="${C.line}"/>`;
    const metricLabel = zh
      ? [`OSM建筑基底 ${metric.mapped_building_footprints}`, `步行/骑行线 ${Math.round(metric.mapped_walk_or_cycle_length_m / 100) / 10} km`, `路网连接点 ${metric.mapped_highway_junctions}`]
      : [`OSM footprints ${metric.mapped_building_footprints}`, `walk/cycle lines ${Math.round(metric.mapped_walk_or_cycle_length_m / 100) / 10} km`, `mapped junctions ${metric.mapped_highway_junctions}`];
    body += text(x + 24, 874, zh ? '公开现状读数' : 'PUBLIC CONTEXT READOUT', 15, C.muted, 700);
    body += metricLabel.map((item, i) => text(x + 24 + i * 184, 912, item, zh ? 15 : 13, C.ink, 600)).join('');
    body += `<rect x="${x + 24}" y="950" width="${panelW - 48}" height="88" rx="4" fill="${[C.paleBlue, C.paleGreen, C.paleAmber][index]}"/>`;
    body += text(x + 42, 980, zh ? 'FAIL 后保留' : 'AFTER FAIL', 14, stationColors[index], 700);
    body += text(x + 42, 1014, fail[index], 17, C.ink, 650);
  });
  return svgWrap(body + footer(lang));
}

function mobilityFigure(lang) {
  const zh = lang === 'zh';
  const extent = [116.332, 39.937, 116.363, 40.029];
  const rect = { x: 58, y: 170, w: 780, h: 930 };
  let body = header(4, 'AI ON / RETURN / AI OFF', 'AI ON / RETURN / AI OFF', '技术状态可变，公众正线、无障碍与人工服务不断', 'TECH STATE CHANGES; CIVIC MOVEMENT, ACCESS AND STAFFED SERVICE CONTINUE', lang);
  body += `<rect x="58" y="160" width="780" height="950" rx="5" fill="white" stroke="${C.line}"/>`;
  body += mapLayer(extent, rect, `mobility-${lang}`, { lightBuildings: true });
  const spine = [[116.3482, 39.944], [116.3485, 39.985], [116.349, 40.018]];
  body += `<path d="${pathData(spine, extent, rect)}" fill="none" stroke="${C.coral}" stroke-width="7" opacity="0.9"/>`;
  keyAreas.features.forEach((area, index) => {
    const ring = area.geometry.coordinates[0];
    body += ringOverlay(ring, extent, rect, stationColors[index], stationNames[lang][index]);
  });
  body += `<rect x="872" y="160" width="1070" height="950" rx="5" fill="white" stroke="${C.line}"/>`;
  body += text(914, 214, zh ? '城市连续性不是备用方案，而是空间骨架' : 'CIVIC CONTINUITY IS THE SPATIAL FRAME, NOT A BACKUP', 25, C.ink, 700);
  const stateHeads = zh ? ['AI ON / 有限开放', 'RETURN / 撤出恢复', 'AI OFF / 普通城市'] : ['AI ON / LIMITED', 'RETURN / WITHDRAW', 'AI OFF / ORDINARY CITY'];
  const stateNotes = zh ? [
    ['AI只占侧袋', '有人值守和物理停止', '公众正线保持优先'],
    ['设备沿撤出路径离场', '围界和发布界面撤下', '投诉进入新复测任务'],
    ['步行与无障碍不断', '人工服务和商业继续', '遗产解释无需模型'],
  ] : [
    ['AI occupies a siding only', 'staffed and physically stoppable', 'civic main line keeps priority'],
    ['equipment leaves by exit route', 'edge and release front withdraw', 'complaint becomes a retest task'],
    ['walking and access continue', 'staffed service and commerce stay', 'heritage works without a model'],
  ];
  stateHeads.forEach((head, index) => {
    const x = 914 + index * 328;
    const color = [C.blue, C.coral, C.green][index];
    body += `<rect x="${x}" y="270" width="302" height="360" rx="5" fill="${C.white}" stroke="${color}" stroke-width="3"/>
      <rect x="${x}" y="270" width="302" height="10" fill="${color}"/>
      ${text(x + 22, 326, head, 18, color, 700)}`;
    // Main line remains continuous in every state; only the siding changes.
    body += `<line x1="${x + 25}" y1="405" x2="${x + 277}" y2="405" stroke="${C.ink}" stroke-width="9"/>
      <line x1="${x + 25}" y1="405" x2="${x + 277}" y2="405" stroke="${C.cyan}" stroke-width="3"/>`;
    if (index === 0) body += `<path d="M${x+75},405 L${x+115},350 L${x+215},350 L${x+255},405" fill="none" stroke="${C.blue}" stroke-width="7"/>`;
    if (index === 1) body += `<path d="M${x+75},405 L${x+115},350 L${x+180},350" fill="none" stroke="${C.coral}" stroke-width="7" stroke-dasharray="9 7"/><path d="M${x+180},350 L${x+145},330 L${x+145},370 Z" fill="${C.coral}"/>`;
    if (index === 2) body += `<path d="M${x+75},405 L${x+105},375" fill="none" stroke="${C.line}" stroke-width="7" stroke-dasharray="8 8"/>`;
    body += lines(x + 22, 480, stateNotes[index], 15, C.muted, 500, 1.65);
  });
  const continuity = zh ? [
    ['普通步行', '连续'], ['无障碍主链', '连续'], ['人工服务', '连续'], ['商业与休息', '连续'], ['铁路遗产解释', '连续'],
  ] : [
    ['ordinary walking', 'continuous'], ['accessible main line', 'continuous'], ['staffed service', 'continuous'], ['commerce + rest', 'continuous'], ['railway interpretation', 'continuous'],
  ];
  body += text(914, 694, zh ? '五项不断线验收' : 'FIVE CONTINUITY ACCEPTANCE ITEMS', 20, C.ink, 700);
  continuity.forEach((item, index) => {
    const y = 740 + index * 58;
    body += `<circle cx="932" cy="${y-6}" r="8" fill="${C.green}"/>${text(954, y, item[0], 16, C.ink, 600)}${text(1880, y, item[1], 15, C.green, 700, 'end')}`;
  });
  body += `<rect x="914" y="1040" width="986" height="42" rx="4" fill="${C.ink}"/>${text(938, 1068, zh ? '关闭技术功能，只改变侧线状态；任何AI空间都不得成为公众必经路。' : 'CLOSING TECH CHANGES THE SIDING ONLY; NO AI SPACE MAY BECOME A REQUIRED CIVIC ROUTE.', 14, C.white, 650)}`;
  return svgWrap(body + footer(lang));
}

function landUseFigure(lang) {
  const zh = lang === 'zh';
  const extent = [116.337, 39.937, 116.359, 40.029];
  const rect = { x: 58, y: 170, w: 760, h: 930 };
  let body = header(2, '七段双翼：把概念用地放回真实城市肌理', 'SEVEN SEGMENTS, TWO WINGS: CONCEPT USE IN REAL FABRIC', '14个决策单元，不是法定分区', '14 DECISION UNITS, NOT STATUTORY ZONING', lang);
  body += `<rect x="58" y="160" width="760" height="950" rx="5" fill="white" stroke="${C.line}"/>`;
  body += mapLayer(extent, rect, `land-${lang}`, { lightBuildings: true });
  const codeColor = { '0802': C.blue, '0804': '#5b78c9', '1401': C.green, '0701': '#83bd77', '0702': C.cyan, '05': C.amber, '0803': '#8a6dcc', '16': '#aeb6c2' };
  for (const feature of landUse.features) {
    const ring = feature.geometry.coordinates[0];
    const color = codeColor[feature.properties.land_use_code] || C.coral;
    body += `<path d="${pathData(ring, extent, rect, true)}" fill="${color}" fill-opacity="0.31" stroke="white" stroke-width="1.5"/>`;
  }
  keyAreas.features.forEach((area, index) => { body += ringOverlay(area.geometry.coordinates[0], extent, rect, stationColors[index], stationNames[lang][index]); });
  body += `<rect x="852" y="160" width="1090" height="950" rx="5" fill="white" stroke="${C.line}"/>`;
  body += text(894, 218, zh ? '从北到南：每一段都有两种责任' : 'NORTH TO SOUTH: TWO DUTIES IN EVERY SEGMENT', 25, C.ink, 700);
  const bandsZh = ['众智园', '北段', 'AI原点', '近校', '蓟门', '大钟寺', '南门户'];
  const westZh = ['模型安全与算力验证', '端侧算力与低碳设施', '开源发布与互操作', '高校成果到原型', '技术服务与合规支持', '智能终端与企业服务', '国际到达与铁路文化核证'];
  const eastZh = ['具身测试与清河复原', '小月河生态与慢行服务', '人才庭院与公共问题桌', '人才生活与公共学习', '社区问题定义与反馈', '轨道到达与城市消费', '访客服务与社区到达'];
  const westEn = ['model safety + compute validation', 'edge compute + low-carbon service', 'open release + interoperability', 'campus result to prototype', 'technical service + compliance', 'terminal trial + enterprise service', 'arrival + railway-source verification'];
  const eastEn = ['embodied test + river restoration', 'river ecology + slow mobility', 'talent court + public issue desk', 'daily life + public learning', 'community issue definition + feedback', 'rail arrival + urban consumption', 'visitor service + community arrival'];
  const bandsEn = ['ZHONGZHI', 'NORTH', 'AI ORIGIN', 'CAMPUS', 'JIMEN', 'DAZHONGSI', 'SOUTH GATE'];
  for (let index = 0; index < 7; index += 1) {
    const y = 275 + index * 102;
    body += `<line x1="894" y1="${y + 52}" x2="1900" y2="${y + 52}" stroke="${C.line}"/>
      ${text(894, y, zh ? bandsZh[index] : bandsEn[index], 18, C.coral, 700)}
      ${text(1115, y, zh ? westZh[index] : westEn[index], 16, C.blue, 600)}
      ${text(1510, y, zh ? eastZh[index] : eastEn[index], 16, C.green, 600)}`;
  }
  body += text(1115, 250, zh ? '西翼 / 能力与验证' : 'WEST / CAPABILITY + VALIDATION', 14, C.blue, 700);
  body += text(1510, 250, zh ? '东翼 / 问题与反馈' : 'EAST / QUESTIONS + FEEDBACK', 14, C.green, 700);
  body += `<rect x="894" y="1002" width="1006" height="72" rx="4" fill="${C.paleCoral}"/>`;
  body += zh
    ? text(916, 1045, '判定边界：功能与比例只在临时范围内复算；official polygon / 控规 / 权属到位后整链重建。', 16, C.coral, 650)
    : lines(916, 1032, ['Evidence limit: functions and ratios are recomputed only inside the provisional extent;', 'official polygons, zoning and ownership trigger a full rebuild.'], 14, C.coral, 650, 1.5);
  return svgWrap(body + footer(lang));
}

function metricsFigure(lang) {
  const zh = lang === 'zh';
  let body = header(10, '一页证据合同：观测、方案、验证与未知分开', 'ONE-PAGE EVIDENCE CONTRACT', '只有可追溯的东西进入下一站', 'OBSERVATION, PROPOSAL, CHECK AND UNKNOWN STAY SEPARATE', lang);
  const columns = [58, 540, 1022, 1504];
  const labels = zh ? ['公开观测', '概念方案', '仓库验证', '必须保持未知'] : ['PUBLIC OBSERVATION', 'CONCEPT PROPOSAL', 'REPOSITORY CHECK', 'MUST REMAIN UNKNOWN'];
  const colors = [C.cyan, C.blue, C.green, C.coral];
  const values = zh ? [
    ['6,266 条 OSM要素', '3处重点区现状切片', '450个建筑基底落入临时框', '时间戳随包保存'],
    ['3站 / 3张票', '12场景 / 4产业验证', '90天最小试点', '14单元 / 10缝合'],
    ['生命周期 24 / 24', '站点拓扑 29 / 29', '旗舰合同 37 / 37', 'OSM复算 5 / 5'],
    ['official polygon', '权属 / 道路红线 / 管线', '现场尺寸 / 人流 / 无障碍', '预算 / 保险 / 许可 / 主体'],
  ] : [
    ['6,266 OSM features', 'three key-area context slices', '450 mapped footprints in rough boxes', 'source timestamp shipped'],
    ['3 stations / 3 tickets', '12 scenarios / 4 industry tests', '90-day minimum pilots', '14 units / 10 stitches'],
    ['lifecycle 24 / 24', 'station topology 29 / 29', 'flagship contracts 37 / 37', 'OSM recomputation 5 / 5'],
    ['official polygons', 'ownership / redlines / utilities', 'site dimensions / flows / access', 'budget / insurance / permits / actors'],
  ];
  columns.forEach((x, index) => {
    body += `<rect x="${x}" y="170" width="438" height="540" rx="5" fill="white" stroke="${C.line}"/>
      <rect x="${x}" y="170" width="438" height="10" fill="${colors[index]}"/>
      ${text(x + 28, 230, labels[index], 18, colors[index], 700)}`;
    values[index].forEach((value, itemIndex) => {
      const y = 310 + itemIndex * 90;
      body += text(x + 28, y, value, itemIndex === 0 ? 25 : 18, itemIndex === 0 ? C.ink : C.muted, itemIndex === 0 ? 700 : 500);
      if (itemIndex < 3) body += `<line x1="${x + 28}" y1="${y + 28}" x2="${x + 410}" y2="${y + 28}" stroke="${C.line}"/>`;
    });
  });
  body += `<rect x="58" y="750" width="1884" height="330" rx="5" fill="white" stroke="${C.line}"/>`;
  body += text(90, 810, zh ? '证据怎样进入城市决定' : 'HOW EVIDENCE ENTERS A CITY DECISION', 24, C.ink, 700);
  const chain = zh ? [
    ['01', '公开现状', ['OSM切片只说明', '“地图上有什么”']],
    ['02', '概念动作', ['临时范围内提出可关闭、', '可恢复的空间关系']],
    ['03', '人工签注', ['TEST / RELEASE / USE', '各自承担不同责任']],
    ['04', '现场证据门', ['90/180日只补资料、复现、', '投诉与复原证据']],
    ['05', '继续或RETURN', ['缺一项就停止，不把仓库PASS', '写成现场批准']],
  ] : [
    ['01', 'PUBLIC CONTEXT', ['OSM slice says only', 'what is mapped']],
    ['02', 'CONCEPT ACTION', ['closable, restorable relations', 'inside the rough extent']],
    ['03', 'HUMAN SIGN-OFF', ['TEST / RELEASE / USE hold', 'different duties']],
    ['04', 'FIELD EVIDENCE GATE', ['90/180-day records, reproduction,', 'complaints and restoration']],
    ['05', 'CONTINUE OR RETURN', ['one missing item stops;', 'repository PASS is not field approval']],
  ];
  chain.forEach((item, index) => {
    const x = 90 + index * 365;
    body += `<circle cx="${x + 23}" cy="880" r="23" fill="${index === 4 ? C.coral : C.ink}"/>
      ${text(x + 23, 887, item[0], 13, C.white, 700, 'middle')}
      ${text(x + 58, 874, item[1], 16, index === 4 ? C.coral : C.ink, 700)}
      ${lines(x + 58, 910, item[2], 14, C.muted, 400, 1.45)}`;
    if (index < 4) body += `<line x1="${x + 300}" y1="880" x2="${x + 350}" y2="880" stroke="${C.cyan}" stroke-width="3"/>`;
  });
  return svgWrap(body + footer(lang));
}

function pilotFigure(lang) {
  const zh = lang === 'zh';
  let body = header(5, '90天试点：失败也留下城市资产', '90-DAY PILOTS: FAILURE STILL LEAVES CITY ASSETS', '面积、构件、主体、停止、撤出与保留均按城市设计量级判断', 'PLANNING-SCALE AREA, KIT, ACTORS, STOP, EXIT AND RETAINED VALUE', lang);
  const pilots = zh ? [
    ['众智园 / TEST', '800–1,500 m²', '轻建造级 · 数百万元级', '可拆围界 / 观察台 / 急停 / 撤机路', '场地运营 / 产品 / 安全 / 独立观察', '越界、急停失效或公众线冲突', '公众院落 / 安全模块 / 失败档案'],
    ['AI原点 / RELEASE', '300–800 m²', '家具+轻改造 · 百万元级', '发布双台 / 权利墙 / 撤回台 / 旁观阶梯', '场地运营 / 权利复核 / 发布 / 社区代表', '许可HOLD、撤回失灵或普通使用受阻', '公共长桌 / 教学空间 / 开放方法档案'],
    ['大钟寺 / USE', '500–1,000 m²', '家具+轻建造 · 百万至数百万元级', '人工窗口 / 触觉导引 / 投诉台 / 储位', '公共服务 / 无障碍 / 维护 / 用户代表', '无AI服务中断、无障碍受阻或异议未闭环', '人工窗口 / 触觉地图 / 座椅与普通商业'],
  ] : [
    ['ZHONGZHI / TEST', '800–1,500 m²', 'LIGHT BUILD · MULTI-MILLION CNY BAND', 'REMOVABLE EDGE / VIEWING / E-STOP / EXIT ROUTE', 'SITE OPS / PRODUCT / SAFETY / INDEPENDENT OBSERVER', 'BOUNDARY BREACH, STOP FAILURE OR CIVIC CONFLICT', 'CIVIC COURT / SAFETY KIT / FAILURE ARCHIVE'],
    ['AI ORIGIN / RELEASE', '300–800 m²', 'FURNITURE + LIGHT RETROFIT · MILLION CNY BAND', 'DUAL TABLE / RIGHTS WALL / WITHDRAWAL / STEPS', 'SITE OPS / RIGHTS / RELEASE / COMMUNITY', 'LICENCE HOLD, WITHDRAWAL FAILURE OR CIVIC USE BLOCKED', 'PUBLIC TABLE / LEARNING / OPEN METHOD ARCHIVE'],
    ['DAZHONGSI / USE', '500–1,000 m²', 'FURNITURE + LIGHT BUILD · LOW–MULTI MILLION CNY', 'STAFFED WINDOW / TACTILE WAY / COMPLAINT / STORAGE', 'PUBLIC SERVICE / ACCESS / MAINTENANCE / USERS', 'NON-AI OUT, ACCESS BLOCKED OR OPEN COMPLAINT', 'STAFFED WINDOW / TACTILE MAP / SEATING + COMMERCE'],
  ];
  const phaseLabels = zh ? ['01–14 基线', '15–45 建造', '46–75 开放', '76–90 退出'] : ['01–14 BASE', '15–45 BUILD', '46–75 OPEN', '76–90 EXIT'];
  pilots.forEach((pilot, index) => {
    const x = 58 + index * 636;
    const color = stationColors[index];
    body += `<rect x="${x}" y="160" width="606" height="930" rx="5" fill="white" stroke="${C.line}"/><rect x="${x}" y="160" width="606" height="10" fill="${color}"/>
      ${text(x+26, 218, pilot[0], 24, C.ink, 700)}${text(x+26, 270, pilot[1], 30, color, 700)}${text(x+26, 307, pilot[2], 13, C.muted, 700)}`;
    phaseLabels.forEach((phase, phaseIndex) => {
      const px = x + 26 + phaseIndex * 139;
      body += `<rect x="${px}" y="350" width="128" height="58" rx="5" fill="${phaseIndex === 3 ? C.paleCoral : [C.paleBlue,C.paleGreen,C.paleAmber][index]}" stroke="${phaseIndex === 3 ? C.coral : color}"/>${text(px+64, 384, phase, zh ? 13 : 11, phaseIndex === 3 ? C.coral : C.ink, 700, 'middle')}`;
    });
    const rows = zh ? [['构件',pilot[3]],['所需主体类型',pilot[4]],['立即停止',pilot[5]]] : [['KIT',pilot[3]],['REQUIRED ACTORS',pilot[4]],['STOP NOW',pilot[5]]];
    rows.forEach((row, rowIndex) => {
      const y = 472 + rowIndex * 150;
      body += text(x+26, y, row[0], 13, C.muted, 700) + lines(x+26, y+38, [row[1]], zh ? 16 : 13, C.ink, 600, 1.5) + `<line x1="${x+26}" y1="${y+104}" x2="${x+580}" y2="${y+104}" stroke="${C.line}"/>`;
    });
    body += `<rect x="${x+26}" y="920" width="554" height="126" rx="5" fill="${C.paleGreen}" stroke="${C.green}"/>${text(x+48, 957, zh ? '90天后留下' : 'LEFT AFTER DAY 90', 14, C.green, 700)}${lines(x+48, 992, [pilot[6]], zh ? 16 : 13, C.ink, 650, 1.5)}`;
  });
  body += text(58, 1128, zh ? '量级声明：面积、实施强度与投资不是测绘、概算、招标预算或实施承诺；正式条件到位后由专业团队重建。' : 'BAND NOTE: AREA, BUILD INTENSITY AND COST ARE NOT SURVEY, COST PLAN, TENDER OR DELIVERY COMMITMENT; PROFESSIONAL TEAMS REBUILD AFTER FORMAL EVIDENCE.', 14, C.muted, 500);
  return svgWrap(body + footer(lang));
}

function render(svg, output) {
  const temp = path.join(os.tmpdir(), `xjz-${process.pid}-${path.basename(output)}.svg`);
  fs.writeFileSync(temp, svg);
  const result = spawnSync('python3.13', ['-m', 'cairosvg', temp, '-o', output, '-s', '1'], { encoding: 'utf8' });
  fs.unlinkSync(temp);
  if (result.status !== 0) throw new Error(result.stderr || `cairosvg failed for ${output}`);
}

const jobs = [
  ['land-use-structure.png', landUseFigure('zh')],
  ['land-use-structure.en.png', landUseFigure('en')],
  ['mobility-bluegreen.png', mobilityFigure('zh')],
  ['mobility-bluegreen.en.png', mobilityFigure('en')],
  ['metrics-evidence.png', pilotFigure('zh')],
  ['metrics-evidence.en.png', pilotFigure('en')],
];

for (const [name, svg] of jobs) {
  render(svg, path.join(FIGURES, name));
  console.log(`rendered assets/figures/${name}`);
}
