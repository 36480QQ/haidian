#!/usr/bin/env node

/*
 * Render the ten mobility scenario contracts as a bilingual, presentation-
 * ready board.  The board only exposes declared design fields; it does not
 * create partners, demand, permits or field results.
 */
const fs = require('fs');
const path = require('path');

const assetDir = __dirname;
const packageDir = path.resolve(assetDir, '..', '..');
const figureDir = path.join(packageDir, 'assets', 'figures');
const data = JSON.parse(fs.readFileSync(path.join(assetDir, 'scenario-cards.json'), 'utf8'));

const required = [
  'space', 'users', 'trigger', 'inputs', 'service_action', 'readout',
  'accountable_role', 'fallback', 'stop_condition', 'evidence_status', 'run_status'
];
if (!Array.isArray(data.cards) || data.cards.length !== 10) {
  throw new Error(`scenario card count must be 10, got ${data.cards?.length}`);
}
for (const card of data.cards) {
  for (const key of required) {
    const field = key === 'evidence_status' ? data.evidence_status : key === 'run_status' ? data.run_status : `${key}_zh`;
    if (!card[field] && !(key === 'evidence_status' || key === 'run_status')) {
      throw new Error(`${card.id} missing ${field}`);
    }
  }
}

function esc(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function wrap(text, max = 54) {
  const value = String(text);
  const chars = [...value];
  const lines = [];
  let line = '';
  for (const char of chars) {
    if (line.length >= max && char === ' ') {
      lines.push(line.trim());
      line = '';
    } else if (line.length >= max) {
      lines.push(line.trim());
      line = char;
    } else {
      line += char;
    }
  }
  if (line.trim()) lines.push(line.trim());
  return lines.slice(0, 2);
}

function fieldMarkup(x, y, label, value, color, maxChars = 52) {
  const lines = wrap(value, maxChars);
  const text = lines.map((line, index) => `<text x="${x + 82}" y="${y + 14 + index * 14}" class="field">${esc(line)}</text>`).join('');
  return `<text x="${x}" y="${y + 14}" class="label" fill="${color}">${esc(label)}</text>${text}`;
}

const accents = ['#55E4C1', '#7DA8FF', '#F7BF63', '#F082A7', '#B7A4FF', '#5ED6D0', '#FF9F68', '#8CB6FF', '#E5C25D', '#D99CF7'];

function board(lang) {
  const zh = lang === 'zh';
  const title = zh ? '十张交通场景卡：从需求登记到停止条件' : 'TEN MOBILITY SCENARIO CARDS: FROM REQUEST TO STOP';
  const subtitle = zh
    ? '每张卡都回答空间、对象、触发、输入、动作、读数、责任、回退与停止；当前均未授权、未运行'
    : 'Each card states place, people, trigger, inputs, action, readout, owner, fallback and stop; all remain unauthorised and unrun';
  const labels = zh
    ? {space: '空间', users: '对象', trigger: '触发', inputs: '输入', service_action: '动作', readout: '读数', accountable_role: '责任', fallback: '回退', stop_condition: '停止'}
    : {space: 'SPACE', users: 'PEOPLE', trigger: 'TRIGGER', inputs: 'INPUT', service_action: 'ACTION', readout: 'READOUT', accountable_role: 'OWNER', fallback: 'FALLBACK', stop_condition: 'STOP'};
  const cardWidth = 730;
  const cardHeight = 218;
  const left = 60;
  const top = 142;
  const gapX = 20;
  const gapY = 14;
  const cards = data.cards.map((card, index) => {
    const col = index % 2;
    const row = Math.floor(index / 2);
    const x = left + col * (cardWidth + gapX);
    const y = top + row * (cardHeight + gapY);
    const accent = accents[index];
    const titleText = zh ? card.title_zh : card.title_en;
    const values = {
      space: zh ? card.space_zh : card.space_en,
      users: zh ? card.users_zh : card.users_en,
      trigger: zh ? card.trigger_zh : card.trigger_en,
      inputs: zh ? card.inputs_zh : card.inputs_en,
      service_action: zh ? card.service_action_zh : card.service_action_en,
      readout: zh ? card.readout_zh : card.readout_en,
      accountable_role: zh ? card.accountable_role_zh : card.accountable_role_en,
      fallback: zh ? card.fallback_zh : card.fallback_en,
      stop_condition: zh ? card.stop_condition_zh : card.stop_condition_en,
    };
    const rowMarkup = [
      ['space', 42, 50],
      ['users', 64, 50],
      ['trigger', 86, 50],
      ['inputs', 108, 50],
      ['service_action', 130, 50],
      ['readout', 152, 50],
      ['accountable_role', 174, 44],
    ].map(([key, yy, max]) => fieldMarkup(x + 18, y + yy, labels[key], values[key], accent, max)).join('');
    return `<g class="card"><rect x="${x}" y="${y}" width="${cardWidth}" height="${cardHeight}" rx="18" fill="#102A3A" stroke="#2D5366" stroke-width="1.5"/><rect x="${x}" y="${y}" width="8" height="${cardHeight}" rx="4" fill="${accent}"/><text x="${x + 24}" y="${y + 29}" class="cardId" fill="${accent}">${esc(card.id)}</text><text x="${x + 78}" y="${y + 29}" class="cardTitle">${esc(titleText)}</text><rect x="${x + cardWidth - 220}" y="${y + 12}" width="196" height="24" rx="12" fill="#173E4C" stroke="#2A9D8F"/><text x="${x + cardWidth - 122}" y="${y + 28}" text-anchor="middle" class="status">${esc(zh ? '设计合同 · 未运行' : 'DESIGN CONTRACT · UNRUN')}</text>${rowMarkup}<text x="${x + 18}" y="${y + 210}" class="stopLabel" fill="#F39BAE">${esc(labels.stop_condition)}</text><text x="${x + 100}" y="${y + 210}" class="stopText">${esc(zh ? card.stop_condition_zh : card.stop_condition_en)}</text></g>`;
  }).join('');
  const footer = zh
    ? '证据状态：unknown_until_authorized · 运行状态：not_authorized_not_run · 场景卡是设计清单，不是合作、许可、居民验证或现场绩效'
    : 'Evidence: unknown_until_authorized · Run: not_authorized_not_run · These are design registers, not partners, permits, resident validation or field performance';
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1400" viewBox="0 0 1600 1400" role="img" aria-labelledby="title desc"><title id="title">${esc(title)}</title><desc id="desc">${esc(subtitle)}</desc><defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#071A2B"/><stop offset="1" stop-color="#123E4A"/></linearGradient><style>.sans{font-family:PingFang SC,Microsoft YaHei,Arial,sans-serif}.title{font-size:30px;font-weight:850;fill:#F5FBFF}.sub{font-size:15px;fill:#A9C7D4}.cardId{font:800 16px Arial,sans-serif;letter-spacing:1px}.cardTitle{font:800 18px PingFang SC,Microsoft YaHei,Arial,sans-serif;fill:#F6FBFF}.label{font:800 10px Arial,PingFang SC,sans-serif;letter-spacing:.6px}.field{font:500 11px PingFang SC,Microsoft YaHei,Arial,sans-serif;fill:#D8EAF0}.status{font:800 10px Arial,PingFang SC,sans-serif;fill:#9CF2DE;letter-spacing:.3px}.stopLabel{font:800 10px Arial,PingFang SC,sans-serif;letter-spacing:.5px}.stopText{font:500 11px PingFang SC,Microsoft YaHei,Arial,sans-serif;fill:#F5C4CB}</style></defs><rect width="1600" height="1400" fill="url(#bg)"/><circle cx="1500" cy="40" r="300" fill="#2A9D8F" opacity=".12"/><circle cx="70" cy="1320" r="260" fill="#5B8DEF" opacity=".12"/><text x="60" y="54" class="sans" fill="#66E3CA" font-size="17" font-weight="900" letter-spacing="3">MOBILITY COMMONS / SCENARIO CONTRACTS</text><text x="60" y="94" class="sans title">${esc(title)}</text><text x="60" y="120" class="sans sub">${esc(subtitle)}</text>${cards}<rect x="60" y="1345" width="1480" height="34" rx="10" fill="#0B2738" stroke="#2A9D8F"/><text x="80" y="1367" class="sans sub" font-size="12">${esc(footer)}</text></svg>`;
}

fs.writeFileSync(path.join(figureDir, 'scenario-cards-board.svg'), board('zh'));
fs.writeFileSync(path.join(figureDir, 'scenario-cards-board.en.svg'), board('en'));

function updateVisualIndex(file, lang) {
  const target = path.join(packageDir, 'visual', file);
  let html = fs.readFileSync(target, 'utf8');
  const zh = lang === 'zh';
  const nav = zh ? '<a href="#17">场景卡</a>' : '<a href="#17">Scenario cards</a>';
  if (!html.includes('href="#17"')) {
    const metricLink = zh ? '<a href="#9">核心指标</a>' : '<a href="#9">Core metrics</a>';
    html = html.replace(metricLink, `${nav}${metricLink}`);
  }
  const section = zh
    ? '<section id="17" class="evidence scenario-card-board"><div class="section-head"><span class="section-no">18</span><h2>十张场景卡：从需求到停止</h2><span class="tag">未授权</span></div><p>每张卡都把空间、对象、触发、输入、动作、读数、责任、回退和停止条件放在一起。它们是设计合同，不是合作、许可或现场结果。</p><img src="../assets/figures/scenario-cards-board.svg" alt="十张交通场景卡"><div class="micro">scenario-cards.json · design_register_not_operational · unknown_until_authorized · not_authorized_not_run</div></section>'
    : '<section id="17" class="evidence scenario-card-board"><div class="section-head"><span class="section-no">18</span><h2>Ten scenario cards: from request to stop</h2><span class="tag">UNAUTHORISED</span></div><p>Each card keeps place, people, trigger, inputs, action, readout, owner, fallback and stop condition together. These are design contracts, not partners, permits or field results.</p><img src="../assets/figures/scenario-cards-board.en.svg" alt="Ten mobility scenario cards"><div class="micro">scenario-cards.json · design_register_not_operational · unknown_until_authorized · not_authorized_not_run</div></section>';
  if (!html.includes('class="scenario-card-board"')) {
    html = html.replace('<section id="14" class="evidence multimodal-board">', `${section}<section id="14" class="evidence multimodal-board">`);
  }
  if (!html.includes('.scenario-card-board')) {
    html = html.replace('</head>', '<style>.scenario-card-board{background:#eef7f5}.scenario-card-board img{background:#071A2B;border-color:#2A9D8F}.scenario-card-board .micro{color:#5E7D88}</style></head>');
  }
  fs.writeFileSync(target, html);
}

updateVisualIndex('index.html', 'zh');
updateVisualIndex('index.en.html', 'en');

console.log(JSON.stringify({
  ok: true,
  card_count: data.cards.length,
  generated: ['assets/figures/scenario-cards-board.svg', 'assets/figures/scenario-cards-board.en.svg'],
  visual_index: ['visual/index.html', 'visual/index.en.html'],
  status: data.status,
  evidence_status: data.evidence_status,
  run_status: data.run_status,
}, null, 2));
