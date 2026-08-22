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
const roads = read('geometry/roads.geojson');

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

function wrapWords(value, maxChars) {
  const words = String(value).split(/\s+/);
  const output = [];
  let line = '';
  for (const word of words) {
    const next = line ? `${line} ${word}` : word;
    if (line && next.length > maxChars) {
      output.push(line);
      line = word;
    } else {
      line = next;
    }
  }
  if (line) output.push(line);
  return output;
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

function drawDesignNetwork(extent, rect) {
  let body = '';
  for (const feature of roads.features) {
    const role = feature.properties.design_role;
    if (!['heritage_slow_mobility_spine', 'east_west_stitch'].includes(role)) continue;
    const color = role === 'heritage_slow_mobility_spine' ? C.cyan : C.amber;
    const width = role === 'heritage_slow_mobility_spine' ? 8 : 3;
    const dash = role === 'east_west_stitch' ? ' stroke-dasharray="10 7"' : '';
    body += `<path d="${pathData(feature.geometry.coordinates, extent, rect)}" fill="none" stroke="white" stroke-width="${width + 4}" opacity="0.86"/>`;
    body += `<path d="${pathData(feature.geometry.coordinates, extent, rect)}" fill="none" stroke="${color}" stroke-width="${width}"${dash}/>`;
  }
  return body;
}

function cityProblemFigure(lang) {
  const zh = lang === 'zh';
  const extent = [116.337, 39.937, 116.359, 40.029];
  const rect = { x: 58, y: 160, w: 1240, h: 940 };
  let body = header(1,
    '城市问题：一条纵向公共线，三类横向技术进入',
    'ONE PUBLIC LINE, THREE LATERAL AI ENTRIES',
    '先看已经存在的公共生活，再决定技术如何进入',
    'START WITH EXISTING PUBLIC LIFE, THEN DECIDE HOW TECHNOLOGY MAY ENTER', lang);
  body += `<rect x="58" y="160" width="1240" height="940" rx="5" fill="white" stroke="${C.line}"/>`;
  body += mapLayer(extent, rect, `problem-${lang}`, { lightBuildings: true });
  body += drawDesignNetwork(extent, rect);
  keyAreas.features.forEach((area, index) => {
    body += ringOverlay(area.geometry.coordinates[0], extent, rect, stationColors[index], stationNames[lang][index]);
  });
  body += `<rect x="1330" y="160" width="612" height="940" rx="5" fill="white" stroke="${C.line}"/>`;
  body += text(1366, 218, zh ? '现状 → 问题 → 空间原则' : 'EXISTING → CONFLICT → SPATIAL RULE', 24, C.ink, 700);
  const cards = zh ? [
    ['01 已经拥有', ['约9公里开放遗址走廊', '铁路记忆与日常慢行共存', '两侧是园区、校园、社区与站点']],
    ['02 真正缺少', ['AI活动需要横向进入', '试验、发布和服务可能争夺公共界面', '普通人不应为技术绕路']],
    ['03 X京张动作', ['公众正线连续', 'AI只占可关闭侧袋', '唯一交叉有人值守；失败沿侧路撤出']],
  ] : [
    ['01 ALREADY HERE', ['roughly 9 km of open heritage corridor', 'rail memory and everyday movement coexist', 'campuses, homes and stations sit on both sides']],
    ['02 MISSING RULE', ['AI activity needs lateral entry', 'tests, launches and service compete for one interface', 'ordinary users must not detour for technology']],
    ['03 X JINGZHANG MOVE', ['keep the civic main line continuous', 'AI occupies a closable pocket only', 'staff the sole crossing; failure exits sideways']],
  ];
  cards.forEach((card, index) => {
    const y = 270 + index * 248;
    const color = [C.cyan, C.coral, C.green][index];
    body += `<rect x="1366" y="${y}" width="540" height="210" rx="5" fill="${[C.paleBlue, C.paleCoral, C.paleGreen][index]}" stroke="${color}"/>`;
    body += text(1394, y + 42, card[0], 17, color, 700);
    body += lines(1394, y + 88, card[1], zh ? 17 : 15, C.ink, 600, 1.65);
  });
  body += `<rect x="1366" y="1014" width="540" height="58" rx="4" fill="${C.ink}"/>`;
  body += text(1392, 1050, zh ? '青色：既有纵向公共线　金色：概念横向缝合' : 'CYAN: PUBLIC LINE   GOLD: CONCEPT LATERAL LINKS', zh ? 14 : 12, C.white, 650);
  return svgWrap(body + footer(lang));
}

function operatingFigure(lang) {
  const zh = lang === 'zh';
  const extent = [116.337, 39.937, 116.359, 40.029];
  const rect = { x: 58, y: 160, w: 940, h: 940 };
  let body = header(2,
    '一件产品沿城市线前进，也必须在空间里折返',
    'ONE PRODUCT ADVANCES ALONG THE CITY LINE AND RETURNS IN SPACE',
    '0.8 FAIL → 0.9 LIMITED → PUBLIC RETURN → 0.10 RETEST',
    '0.8 FAIL → 0.9 LIMITED → PUBLIC RETURN → 0.10 RETEST', lang);
  body += `<rect x="58" y="160" width="940" height="940" rx="5" fill="white" stroke="${C.line}"/>`;
  body += mapLayer(extent, rect, `operating-${lang}`, { lightBuildings: true });
  body += drawDesignNetwork(extent, rect);
  const centers = keyAreas.features.map((area) => {
    const ring = area.geometry.coordinates[0].slice(0, -1);
    const center = ring.reduce((acc, point) => [acc[0] + point[0] / ring.length, acc[1] + point[1] / ring.length], [0, 0]);
    return project(center, extent, rect);
  });
  const ordered = [centers[0], centers[1], centers[2]];
  body += `<path d="M${ordered[0][0]},${ordered[0][1]} L${ordered[1][0]},${ordered[1][1]} L${ordered[2][0]},${ordered[2][1]}" fill="none" stroke="white" stroke-width="16" opacity="0.9"/>`;
  body += `<path d="M${ordered[0][0]},${ordered[0][1]} L${ordered[1][0]},${ordered[1][1]} L${ordered[2][0]},${ordered[2][1]}" fill="none" stroke="${C.ink}" stroke-width="8" marker-end="url(#arrow-dark)"/>`;
  body += `<defs><marker id="arrow-dark" markerWidth="12" markerHeight="12" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="${C.ink}"/></marker><marker id="arrow-return" markerWidth="12" markerHeight="12" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="${C.coral}"/></marker></defs>`;
  body += `<path d="M${ordered[2][0] + 45},${ordered[2][1]} C${ordered[2][0] + 180},${ordered[2][1] - 40} ${ordered[0][0] + 180},${ordered[0][1] + 40} ${ordered[0][0] + 45},${ordered[0][1]}" fill="none" stroke="white" stroke-width="14" opacity="0.9"/>`;
  body += `<path d="M${ordered[2][0] + 45},${ordered[2][1]} C${ordered[2][0] + 180},${ordered[2][1] - 40} ${ordered[0][0] + 180},${ordered[0][1] + 40} ${ordered[0][0] + 45},${ordered[0][1]}" fill="none" stroke="${C.coral}" stroke-width="7" marker-end="url(#arrow-return)"/>`;
  centers.forEach((point, index) => {
    body += `<circle cx="${point[0]}" cy="${point[1]}" r="19" fill="${stationColors[index]}" stroke="white" stroke-width="6"/>`;
  });
  body += `<rect x="1030" y="160" width="912" height="940" rx="5" fill="white" stroke="${C.line}"/>`;
  const stages = zh ? [
    ['01 众智园', '0.8 / FAIL', ['意外穿越触发急停', '机器从测试侧袋撤出', '公众路径不改线']],
    ['02 AI原点', '0.9 / LIMITED', ['复测版本公开方法与许可', '责任人与撤回同场可见', '仅允许有限进入下一段']],
    ['03 大钟寺', 'PUBLIC / RETURN', ['周阿姨线下提出异议', '试用侧袋关闭，人工服务继续', '新工况随0.10返回众智园']],
  ] : [
    ['01 ZHONGZHI', '0.8 / FAIL', ['unexpected crossing triggers human stop', 'device leaves through test pocket', 'public path does not move']],
    ['02 AI ORIGIN', '0.9 / LIMITED', ['retested version exposes method and licence', 'owner and withdrawal share one interface', 'limited entry to the next section only']],
    ['03 DAZHONGSI', 'PUBLIC / RETURN', ['Ms Zhou objects offline', 'trial pocket closes; staffed service stays', 'new fixture returns with version 0.10']],
  ];
  stages.forEach((stage, index) => {
    const y = 208 + index * 260;
    const color = stationColors[index];
    body += `<rect x="1068" y="${y}" width="836" height="222" rx="5" fill="${[C.paleBlue, C.paleGreen, C.paleAmber][index]}" stroke="${color}"/>`;
    body += text(1098, y + 42, stage[0], 18, color, 700);
    body += text(1868, y + 42, stage[1], 16, index === 2 ? C.coral : C.ink, 700, 'end');
    body += lines(1098, y + 92, stage[2], zh ? 17 : 15, C.ink, 600, 1.62);
  });
  body += `<rect x="1068" y="994" width="836" height="78" rx="4" fill="${C.ink}"/>`;
  body += text(1094, 1025, zh ? '折返不是后台状态：断能 → 撤出 → 恢复普通用途 → 带新问题返回' : 'RETURN IS PHYSICAL: ISOLATE → REMOVE → RESTORE ORDINARY USE → RETEST', zh ? 15 : 13, C.white, 650);
  return svgWrap(body + footer(lang));
}

function stationSpatialFigure(lang) {
  const zh = lang === 'zh';
  let body = header(5,
    '三站相对平面：同一原则，三种不可互换的空间',
    'THREE STATIONS, THREE SPATIAL RELATIONS',
    '公开地图语境 + 相对关系；不虚构工程尺寸',
    'PUBLIC MAP CONTEXT + RELATIVE RELATIONS; NO INVENTED FIELD DIMENSIONS', lang);
  body += `<defs><marker id="arrow-return" markerWidth="12" markerHeight="12" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="${C.coral}"/></marker></defs>`;
  const titles = zh ? ['众智园｜研发与河岸', 'AI原点｜校园与社区', '大钟寺｜轨道与商业'] : ['ZHONGZHI | RESEARCH + RIVER', 'AI ORIGIN | CAMPUS + COMMUNITY', 'DAZHONGSI | TRANSIT + COMMERCE'];
  const labels = zh ? [
    ['连续公众路径', '观察缓冲', '测试侧袋', '值守 + 急停', '后勤撤出'],
    ['贯通公共首层', '开放实验室', '发布台 + 公众阶梯', '责任 + 撤回', '协作庭院'],
    ['轨道到达主链', '人工等价服务', '投诉节点', '有限试用侧袋', '设备退出'],
  ] : [
    ['continuous civic path', 'observation buffer', 'test pocket', 'staff + physical stop', 'service exit'],
    ['public ground floor', 'open lab', 'release table + steps', 'owner + withdrawal', 'collaboration court'],
    ['transit arrival chain', 'staffed equivalent', 'complaint point', 'limited trial pocket', 'equipment exit'],
  ];
  const after = zh ? ['机器撤出，院落与绿地恢复', '产品撤下，学习协作继续', '试用关闭，交通、商业与人工服务继续'] : ['device leaves; court and green recover', 'product leaves; learning and collaboration stay', 'trial closes; transit, commerce and staff stay'];
  keyAreas.features.forEach((area, index) => {
    const x = 58 + index * 636;
    const ring = area.geometry.coordinates[0];
    const mapRect = { x: x + 20, y: 212, w: 566, h: 300 };
    const extent = extentForRing(ring, 0.14);
    const color = stationColors[index];
    body += `<rect x="${x}" y="160" width="606" height="930" rx="5" fill="white" stroke="${C.line}"/><rect x="${x}" y="160" width="606" height="10" fill="${color}"/>`;
    body += text(x + 24, 202, titles[index], 20, C.ink, 700);
    body += mapLayer(extent, mapRect, `atlas-${lang}-${index}`, { lightBuildings: true });
    body += ringOverlay(ring, extent, mapRect, color, stationNames[lang][index]);
    const y = 620;
    body += text(x + 24, 558, zh ? '相对平面关系' : 'RELATIVE PLAN', 14, color, 700);
    body += `<line x1="${x + 42}" y1="${y}" x2="${x + 564}" y2="${y}" stroke="${C.cyan}" stroke-width="11"/>`;
    if (index === 0) {
      body += `<rect x="${x + 208}" y="${y - 170}" width="210" height="112" rx="5" fill="${C.paleBlue}" stroke="${color}" stroke-width="3"/><rect x="${x + 182}" y="${y - 44}" width="262" height="20" fill="${C.paleGreen}"/><line x1="${x + 313}" y1="${y - 58}" x2="${x + 313}" y2="${y}" stroke="${C.coral}" stroke-width="7"/><path d="M${x+418},${y-115} L${x+540},${y-180}" stroke="${C.coral}" stroke-width="4" marker-end="url(#arrow-return)"/>`;
    } else if (index === 1) {
      body += `<rect x="${x + 80}" y="${y - 174}" width="150" height="108" fill="${C.paleBlue}" stroke="${color}"/><rect x="${x + 238}" y="${y - 174}" width="150" height="108" fill="${C.paleAmber}" stroke="${color}"/><rect x="${x + 396}" y="${y - 174}" width="130" height="108" fill="${C.paleCoral}" stroke="${color}"/><rect x="${x + 128}" y="${y + 36}" width="350" height="74" rx="36" fill="${C.paleGreen}" stroke="${color}"/>`;
    } else {
      body += `<line x1="${x + 304}" y1="${y - 190}" x2="${x + 304}" y2="${y + 115}" stroke="${C.blue}" stroke-width="9"/><rect x="${x + 62}" y="${y - 168}" width="170" height="92" fill="${C.paleGreen}" stroke="${color}"/><circle cx="${x + 414}" cy="${y - 120}" r="72" fill="${C.paleAmber}" stroke="${color}" stroke-width="3"/><circle cx="${x + 304}" cy="${y}" r="15" fill="${C.coral}" stroke="white" stroke-width="4"/><path d="M${x+486},${y-120} L${x+560},${y-120}" stroke="${C.coral}" stroke-width="4" marker-end="url(#arrow-return)"/>`;
    }
    labels[index].forEach((label, itemIndex) => {
      const ly = 780 + itemIndex * 38;
      body += `<circle cx="${x + 34}" cy="${ly - 5}" r="5" fill="${itemIndex === 0 ? C.cyan : color}"/>${text(x + 50, ly, label, zh ? 14 : 12, C.ink, 600)}`;
    });
    body += `<rect x="${x + 24}" y="990" width="558" height="62" rx="4" fill="${[C.paleBlue, C.paleGreen, C.paleAmber][index]}"/>`;
    body += text(x + 44, 1028, zh ? `设备退出后：${after[index]}` : `AFTER EXIT: ${after[index]}`, zh ? 14 : 12, C.ink, 650);
  });
  return svgWrap(body + footer(lang));
}

function mobilityFigure(lang) {
  const zh = lang === 'zh';
  const extent = [116.332, 39.937, 116.363, 40.029];
  const rect = { x: 58, y: 170, w: 780, h: 930 };
  let body = header(4, '有限试用 / 折返 / 普通使用', 'LIMITED TRIAL / RETURN / ORDINARY USE', '技术状态可变，公众正线、无障碍与人工服务不断', 'TECH STATE CHANGES; CIVIC MOVEMENT, ACCESS AND STAFFED SERVICE CONTINUE', lang);
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
  const stateHeads = zh ? ['有限试用', 'RETURN / 撤出恢复', '普通使用'] : ['LIMITED TRIAL', 'RETURN / WITHDRAW', 'ORDINARY USE'];
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

function innovationLineFigure(lang) {
  const zh = lang === 'zh';
  const extent = [116.337, 39.937, 116.359, 40.029];
  const rect = { x: 58, y: 160, w: 1160, h: 930 };
  let body = header(1,
    '让城市的问题进入研发，让AI的答案回到生活',
    'CITY QUESTIONS IN. AI ANSWERS BACK TO LIFE.',
    '一条京张公共创新线 × 三个不可互换的城市站点',
    'ONE PUBLIC INNOVATION LINE × THREE URBAN STATIONS', lang);
  body += `<defs>
    <marker id="innov-arrow-${lang}" markerWidth="12" markerHeight="12" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="${C.cyan}"/></marker>
    <marker id="question-arrow-${lang}" markerWidth="12" markerHeight="12" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="${C.coral}"/></marker>
  </defs>`;
  body += `<rect x="58" y="160" width="1160" height="930" rx="5" fill="white" stroke="${C.line}"/>`;
  body += mapLayer(extent, rect, `innovation-${lang}`, { lightBuildings: true });
  body += drawDesignNetwork(extent, rect);
  const centers = keyAreas.features.map((area) => {
    const ring = area.geometry.coordinates[0].slice(0, -1);
    const center = ring.reduce((acc, point) => [acc[0] + point[0] / ring.length, acc[1] + point[1] / ring.length], [0, 0]);
    return project(center, extent, rect);
  });
  const [z, a, d] = centers;
  body += `<path d="M${d[0]-42},${d[1]} C${d[0]-190},${d[1]-80} ${z[0]-190},${z[1]+80} ${z[0]-42},${z[1]}" fill="none" stroke="white" stroke-width="18" opacity=".92"/>`;
  body += `<path d="M${d[0]-42},${d[1]} C${d[0]-190},${d[1]-80} ${z[0]-190},${z[1]+80} ${z[0]-42},${z[1]}" fill="none" stroke="${C.coral}" stroke-width="8" stroke-dasharray="15 10" marker-end="url(#question-arrow-${lang})"/>`;
  body += `<path d="M${z[0]+38},${z[1]} L${a[0]+38},${a[1]} L${d[0]+38},${d[1]}" fill="none" stroke="white" stroke-width="20" opacity=".92"/>`;
  body += `<path d="M${z[0]+38},${z[1]} L${a[0]+38},${a[1]} L${d[0]+38},${d[1]}" fill="none" stroke="${C.cyan}" stroke-width="10" marker-end="url(#innov-arrow-${lang})"/>`;
  const stationRole = zh ? ['共研 / BUILD', '开放 / OPEN', '使用 / LIVE'] : ['CO-DEVELOP / BUILD', 'OPEN / OPEN', 'USE / LIVE'];
  centers.forEach((point, index) => {
    body += `<circle cx="${point[0]}" cy="${point[1]}" r="24" fill="${stationColors[index]}" stroke="white" stroke-width="7"/>`;
    body += `<rect x="${point[0]+34}" y="${point[1]-38}" width="${zh ? 212 : 250}" height="76" rx="4" fill="white" stroke="${stationColors[index]}"/>`;
    body += text(point[0]+50, point[1]-8, stationNames[lang][index], zh ? 18 : 15, C.ink, 700);
    body += text(point[0]+50, point[1]+20, stationRole[index], 13, stationColors[index], 700);
  });
  const lateral = zh ? [
    ['高校 / 科研园区', 120, 300, z[0]-18, z[1]],
    ['社区 / 小月河', 940, 390, a[0]+18, a[1]],
    ['轨道 / 商业 / 日常服务', 870, 930, d[0]+18, d[1]],
  ] : [
    ['UNIVERSITIES / R&D', 105, 300, z[0]-18, z[1]],
    ['COMMUNITIES / XIAOYUE', 915, 390, a[0]+18, a[1]],
    ['TRANSIT / COMMERCE / DAILY LIFE', 805, 930, d[0]+18, d[1]],
  ];
  lateral.forEach((item, index) => {
    body += `<rect x="${item[1]}" y="${item[2]-30}" width="${index === 2 ? 300 : 230}" height="54" rx="4" fill="${C.ink}"/>`;
    body += text(item[1]+14, item[2]+5, item[0], zh ? 14 : 12, C.white, 650);
  });
  body += `<rect x="1248" y="160" width="694" height="930" rx="5" fill="white" stroke="${C.line}"/>`;
  body += text(1284, 218, zh ? '一条创新链，不是一套门禁' : 'AN INNOVATION LINE, NOT AN ACCESS GATE', zh ? 24 : 21, C.ink, 700);
  const steps = zh ? [
    ['01 城市出题', '居民、服务人员、园区与河岸把困难写成可工作的任务', C.coral],
    ['02 众智园共研', '开发者把任务做成工况、原型与开放测试方法', C.blue],
    ['03 AI原点开放', '高校、企业与公众复现、解释、修改并形成公共能力', C.green],
    ['04 大钟寺使用', '成果进入通勤、商业和社区服务，判断是否真正改善生活', C.amber],
    ['05 带题返回', '现场反馈成为下一版研发输入，而不是停在投诉端', C.coral],
  ] : [
    ['01 FRAME THE QUESTION', 'Residents, staff, campuses and the river edge turn difficulty into a workable brief.', C.coral],
    ['02 CO-DEVELOP AT ZHONGZHI', 'Developers turn the brief into conditions, prototypes and open test methods.', C.blue],
    ['03 OPEN AT AI ORIGIN', 'Universities, enterprises and the public reproduce, explain and improve it.', C.green],
    ['04 USE AT DAZHONGSI', 'The answer meets transit, commerce and community life to prove real value.', C.amber],
    ['05 RETURN WITH A QUESTION', 'Field feedback becomes the next research input instead of ending as a complaint.', C.coral],
  ];
  steps.forEach((step, index) => {
    const y = 278 + index * 145;
    body += `<circle cx="1299" cy="${y+29}" r="18" fill="${step[2]}"/>`;
    if (index < steps.length-1) body += `<line x1="1299" y1="${y+50}" x2="1299" y2="${y+132}" stroke="${C.line}" stroke-width="4"/>`;
    body += text(1333, y+21, step[0], zh ? 18 : 15, step[2], 700);
    body += lines(1333, y+57, zh ? [step[1]] : wrapWords(step[1], 48), zh ? 16 : 13, C.ink, 500, 1.45);
  });
  body += `<rect x="1284" y="1010" width="622" height="54" rx="4" fill="${C.ink}"/>`;
  body += text(1595, 1044, zh ? 'X = 城市问题 × AI能力' : 'X = CITY QUESTION × AI CAPABILITY', zh ? 18 : 16, C.white, 700, 'middle');
  return svgWrap(body + footer(lang));
}

function stationInnovationFigure(lang) {
  const zh = lang === 'zh';
  let body = header(3,
    '三站城市空间：做东西、开放东西、真正使用东西',
    'THREE URBAN STATIONS: MAKE, OPEN, USE',
    '创新活动是空间主体；治理合同是安全底盘',
    'INNOVATION IS THE SPATIAL PROGRAMME; GOVERNANCE IS THE FOUNDATION', lang);
  const titles = zh ? ['众智园｜把问题做成原型', 'AI原点｜把原型变成公共能力', '大钟寺｜让公共能力进入生活'] : ['ZHONGZHI | TURN QUESTIONS INTO PROTOTYPES', 'AI ORIGIN | TURN PROTOTYPES INTO PUBLIC CAPABILITY', 'DAZHONGSI | PUT CAPABILITY INTO DAILY LIFE'];
  const users = zh ? ['开发者 · 企业 · 居民 · 孩子', '高校 · 开发者 · 创业者 · 社区', '通勤者 · 老人 · 儿童 · 商户'] : ['DEVELOPERS · ENTERPRISES · RESIDENTS · CHILDREN', 'UNIVERSITIES · DEVELOPERS · START-UPS · COMMUNITY', 'COMMUTERS · OLDER PEOPLE · CHILDREN · SHOPS'];
  const spaces = zh ? [
    ['城市问题厅', '开发者工作台', '开放实验庭院', '观察廊', '机器人测试街', '清河生态工况'],
    ['城市问题墙', '开放实验大厅', '原型工坊', '开源剧场', '开发者阶梯', '人才生活庭院'],
    ['轨道到达厅', '城市服务街', '人工服务岛', '社区问题桌', '终端工坊', '公共活动客厅'],
  ] : [
    ['QUESTION HALL', 'DEVELOPER BENCHES', 'OPEN LAB COURT', 'OBSERVATION', 'ROBOT TEST STREET', 'QINGHE ECO FIXTURES'],
    ['QUESTION WALL', 'OPEN LAB HALL', 'PROTOTYPE WORKSHOP', 'OPEN-SOURCE THEATRE', 'DEVELOPER STEPS', 'TALENT-LIFE COURT'],
    ['TRANSIT ARRIVAL', 'CITY SERVICE STREET', 'STAFFED ISLAND', 'COMMUNITY QUESTION DESK', 'TERMINAL WORKSHOP', 'PUBLIC ACTIVITY ROOM'],
  ];
  const foundations = zh ? ['TEST：边界、急停、撤出', 'RELEASE：方法、权利、责任', 'USE：人工服务、无障碍、返回'] : ['TEST: LIMIT · STOP · EXIT', 'RELEASE: METHOD · RIGHTS · OWNER', 'USE: STAFF · ACCESS · RETURN'];
  keyAreas.features.forEach((area, index) => {
    const x = 58 + index * 636;
    const color = stationColors[index];
    const mapRect = { x: x+20, y: 214, w: 566, h: 250 };
    const ring = area.geometry.coordinates[0];
    const extent = extentForRing(ring, 0.14);
    body += `<rect x="${x}" y="160" width="606" height="930" rx="5" fill="white" stroke="${C.line}"/><rect x="${x}" y="160" width="606" height="10" fill="${color}"/>`;
    body += text(x+24, 203, titles[index], zh ? 20 : 15, C.ink, 700);
    body += mapLayer(extent, mapRect, `station-innovation-${lang}-${index}`, { lightBuildings: true });
    body += ringOverlay(ring, extent, mapRect, color, stationNames[lang][index]);
    body += text(x+24, 500, users[index], zh ? 14 : 11, color, 700);
    const px = x+24, py = 542, pw = 558, ph = 354;
    body += `<rect x="${px}" y="${py}" width="${pw}" height="${ph}" rx="5" fill="${[C.paleBlue,C.paleGreen,C.paleAmber][index]}" stroke="${color}"/>`;
    if (index === 0) {
      body += `<rect x="${px+26}" y="${py+26}" width="188" height="92" fill="white" stroke="${color}"/><rect x="${px+232}" y="${py+26}" width="296" height="92" fill="white" stroke="${color}"/>`;
      body += `<rect x="${px+26}" y="${py+140}" width="502" height="58" fill="white" stroke="${C.green}"/><rect x="${px+26}" y="${py+218}" width="96" height="108" fill="white" stroke="${C.green}"/><rect x="${px+140}" y="${py+218}" width="388" height="108" fill="white" stroke="${C.coral}" stroke-width="3"/>`;
      body += text(px+40,py+64,spaces[index][0],13,C.ink,700)+text(px+246,py+64,spaces[index][1],13,C.ink,700)+text(px+40,py+176,spaces[index][2],13,C.ink,700)+text(px+40,py+256,spaces[index][3],zh?12:10,C.ink,700)+text(px+154,py+256,spaces[index][4],zh?13:11,C.ink,700)+text(px+154,py+294,spaces[index][5],zh?12:10,C.green,700);
    } else if (index === 1) {
      body += `<rect x="${px+26}" y="${py+26}" width="80" height="302" fill="${C.ink}"/><rect x="${px+124}" y="${py+26}" width="184" height="138" fill="white" stroke="${color}"/><rect x="${px+326}" y="${py+26}" width="202" height="138" fill="white" stroke="${color}"/>`;
      body += `<path d="M${px+142},${py+242} L${px+278},${py+180} L${px+414},${py+242}" fill="none" stroke="${color}" stroke-width="14"/><rect x="${px+124}" y="${py+262}" width="404" height="66" rx="30" fill="white" stroke="${C.green}"/>`;
      body += text(px+66,py+178,spaces[index][0],zh?12:9,C.white,700,'middle')+text(px+140,py+67,spaces[index][1],zh?12:10,C.ink,700)+text(px+342,py+67,spaces[index][2],zh?12:10,C.ink,700)+text(px+250,py+224,spaces[index][3],zh?12:10,C.ink,700,'middle')+text(px+430,py+224,spaces[index][4],zh?12:10,C.ink,700,'middle')+text(px+326,py+302,spaces[index][5],zh?12:10,C.green,700,'middle');
    } else {
      body += `<rect x="${px+26}" y="${py+26}" width="502" height="74" fill="white" stroke="${C.blue}" stroke-width="3"/><rect x="${px+26}" y="${py+122}" width="502" height="64" fill="white" stroke="${color}"/>`;
      body += `<circle cx="${px+120}" cy="${py+256}" r="55" fill="white" stroke="${C.green}" stroke-width="3"/><rect x="${px+196}" y="${py+210}" width="142" height="94" fill="white" stroke="${C.coral}"/><rect x="${px+356}" y="${py+210}" width="172" height="94" fill="white" stroke="${color}"/>`;
      body += text(px+277,py+70,spaces[index][0],13,C.ink,700,'middle')+text(px+277,py+162,spaces[index][1],13,C.ink,700,'middle')+text(px+120,py+260,spaces[index][2],zh?11:9,C.green,700,'middle')+text(px+267,py+250,spaces[index][3],zh?11:9,C.coral,700,'middle')+text(px+442,py+250,spaces[index][4],zh?11:9,C.ink,700,'middle')+text(px+442,py+280,spaces[index][5],zh?11:9,C.ink,700,'middle');
    }
    for (let i=0; i<7; i++) {
      const cx=px+54+i*74, cy=py+ph-18-(i%2)*9;
      body += `<circle cx="${cx}" cy="${cy-10}" r="6" fill="${color}"/><line x1="${cx}" y1="${cy-2}" x2="${cx}" y2="${cy+13}" stroke="${color}" stroke-width="3"/>`;
    }
    body += `<rect x="${x+24}" y="934" width="558" height="74" rx="4" fill="${C.ink}"/>`;
    body += text(x+44, 966, zh ? '安全底盘' : 'SAFETY FOUNDATION', 12, '#a9bed1', 700);
    body += text(x+44, 992, foundations[index], zh ? 15 : 12, C.white, 650);
    body += text(x+24, 1052, zh ? ['看见问题怎样变成原型','加入方法怎样被共同改进','让日常使用产生下一道题'][index] : ['SEE A QUESTION BECOME A PROTOTYPE','JOIN THE OPEN IMPROVEMENT','TURN DAILY USE INTO THE NEXT QUESTION'][index], zh ? 15 : 12, color, 700);
  });
  return svgWrap(body + footer(lang));
}

function cityQuestionJourneyFigure(lang) {
  const zh = lang === 'zh';
  const extent = [116.337, 39.937, 116.359, 40.029];
  const rect = { x: 58, y: 160, w: 850, h: 930 };
  let body = header(2,
    '一个城市问题，如何变成AI能力，又如何回来继续改变它',
    'ONE CITY QUESTION CHANGES AN AI ANSWER',
    '概念演练：大钟寺无障碍到达 × 72岁非数字用户',
    'DAZHONGSI ACCESS × A 72-YEAR-OLD NON-DIGITAL USER', lang);
  body += `<defs><marker id="journey-arrow-${lang}" markerWidth="12" markerHeight="12" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="${C.coral}"/></marker></defs>`;
  body += `<rect x="58" y="160" width="850" height="930" rx="5" fill="white" stroke="${C.line}"/>` + mapLayer(extent, rect, `question-journey-${lang}`, { lightBuildings: true }) + drawDesignNetwork(extent, rect);
  const centers = keyAreas.features.map((area) => {
    const ring = area.geometry.coordinates[0].slice(0,-1);
    return project(ring.reduce((acc,p)=>[acc[0]+p[0]/ring.length,acc[1]+p[1]/ring.length],[0,0]), extent, rect);
  });
  const [z,a,d]=centers;
  body += `<path d="M${d[0]-20},${d[1]} C${d[0]-160},${d[1]-110} ${z[0]-160},${z[1]+110} ${z[0]-20},${z[1]} L${a[0]+28},${a[1]} L${d[0]+28},${d[1]}" fill="none" stroke="white" stroke-width="18" opacity=".9"/>`;
  body += `<path d="M${d[0]-20},${d[1]} C${d[0]-160},${d[1]-110} ${z[0]-160},${z[1]+110} ${z[0]-20},${z[1]} L${a[0]+28},${a[1]} L${d[0]+28},${d[1]}" fill="none" stroke="${C.coral}" stroke-width="8" stroke-dasharray="13 9" marker-end="url(#journey-arrow-${lang})"/>`;
  centers.forEach((point,index)=>body += `<circle cx="${point[0]}" cy="${point[1]}" r="20" fill="${stationColors[index]}" stroke="white" stroke-width="6"/>`);
  body += `<rect x="940" y="160" width="1002" height="930" rx="5" fill="white" stroke="${C.line}"/>`;
  body += text(980,214,zh?'问题主角：不是机器人，而是一次真实到达':'THE PROTAGONIST IS AN ARRIVAL PROBLEM, NOT A ROBOT',zh?23:19,C.ink,700);
  const stages = zh ? [
    ['01 大钟寺提出问题','72岁的周阿姨不用手机，能否在复杂到达环境中获得连续、有人支持的无障碍服务？',C.amber],
    ['02 众智园把问题做成工况','拥挤、设备停靠、围观、轮椅优先和人工接管被组合成可重复任务；SC-03只是候选工具。',C.blue],
    ['03 0.8失败也产生知识','意外穿越触发急停；失败没有被抹掉，而是改进测试边界和下一版原型。',C.coral],
    ['04 AI原点开放共同改进','开发者和无障碍专业人员复现方法、检查边界并修改接口，0.9才进入有限使用。',C.green],
    ['05 大钟寺真实使用','设备无碰撞，但停靠与围观仍侵入优先路线；人工服务继续，周阿姨线下提出问题。',C.amber],
    ['06 带着新问题返回','0.10携带“停靠 + 围观 + 轮椅优先”新工况返回众智园，城市生活改变下一轮研发。',C.coral],
  ] : [
    ['01 DAZHONGSI FRAMES THE QUESTION','Can 72-year-old Ms Zhou complete accessible arrival without a phone, with clear and staffed support?',C.amber],
    ['02 ZHONGZHI MAKES CONDITIONS','Crowding, parking, spectators, wheelchair priority and takeover become a repeatable task; SC-03 is one tool.',C.blue],
    ['03 VERSION 0.8 FAILS USEFULLY','An unexpected crossing triggers a stop. Failure changes the boundary and next prototype instead of disappearing.',C.coral],
    ['04 AI ORIGIN OPENS IMPROVEMENT','Developers and access specialists reproduce the method, inspect limits and revise the interface before 0.9 use.',C.green],
    ['05 DAZHONGSI USES IT','No collision occurs, yet parking and spectators invade the priority route. Staff remain; Ms Zhou reports offline.',C.amber],
    ['06 RETURN WITH A NEW QUESTION','Version 0.10 carries parking + spectators + wheelchair priority back to Zhongzhi for the next research cycle.',C.coral],
  ];
  stages.forEach((stage,index)=>{
    const y=258+index*126;
    body += `<circle cx="992" cy="${y+17}" r="15" fill="${stage[2]}"/>`;
    if(index<stages.length-1) body += `<line x1="992" y1="${y+35}" x2="992" y2="${y+116}" stroke="${C.line}" stroke-width="4"/>`;
    body += text(1024,y+12,stage[0],zh?17:14,stage[2],700);
    const desc=stage[1];
    const chunks=zh?[desc]:wrapWords(desc, 72);
    body += lines(1024,y+48,chunks,zh?15:12,C.ink,500,1.42);
  });
  body += `<rect x="980" y="1014" width="926" height="54" rx="4" fill="${C.ink}"/>`;
  body += text(1443,1048,zh?'RETURN = 真实生活为下一轮研发重新出题':'RETURN = DAILY LIFE WRITES THE NEXT RESEARCH BRIEF',zh?17:15,C.white,700,'middle');
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
  ['mobility-bluegreen.png', innovationLineFigure('zh')],
  ['mobility-bluegreen.en.png', innovationLineFigure('en')],
  ['key-areas.png', stationInnovationFigure('zh')],
  ['key-areas.en.png', stationInnovationFigure('en')],
  ['x-operating-proof.png', cityQuestionJourneyFigure('zh')],
  ['x-operating-proof.en.png', cityQuestionJourneyFigure('en')],
  ['station-design-atlas.png', stationSpatialFigure('zh')],
  ['station-design-atlas.en.png', stationSpatialFigure('en')],
  ['land-use-structure.png', landUseFigure('zh')],
  ['land-use-structure.en.png', landUseFigure('en')],
];

for (const [name, svg] of jobs) {
  render(svg, path.join(FIGURES, name));
  console.log(`rendered assets/figures/${name}`);
}
