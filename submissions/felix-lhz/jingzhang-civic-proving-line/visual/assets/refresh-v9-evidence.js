const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const read = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));
const write = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);

const metricsFile = path.join(ROOT, 'metrics.json');
const metrics = read(metricsFile);
const known = (value, unit, formula) => ({ status:'known', value, unit, source_files:['visual/assets/e2-readiness.json'], formula, confidence:'high', assumptions:['ASM-V9-E2'] });
metrics.metrics.s7_prototype_kit_item_count = known(16, 'count', 'count(e2-readiness.bill_of_components)');
metrics.metrics.e2_permit_gate_count = known(8, 'count', 'count(e2-readiness.permit_checklist)');
metrics.metrics.e2_printable_form_count = known(5, 'count', 'count(e2-readiness.forms where printable=true)');
metrics.metrics.e2_procurement_package_count = known(4, 'count', 'count(e2-readiness.procurement_packages)');
metrics.metrics.e2_readiness_status = { status:'unknown', value:null, unit:'status', source_files:['visual/assets/e2-readiness.json'], formula:'field readiness becomes known only after survey and all permit gates close', confidence:'unknown', assumptions:['ASM-V9-E2'], reason:'E2 documents are prepared, but survey, permits, quotes, assembly and field operation have not occurred.' };
metrics.metrics.field_performance_status.reason = 'V9 documents E2 prototype readiness only; no survey, permit, assembly, baseline, controlled trial or adoption has occurred.';
write(metricsFile, metrics);

const index = {
  'agent.1': { section:'总体设计范围城市更新与控规深度城市设计', figure:'assets/figures/site-overview.png', data:'visual/assets/spatial-atlas.json', conclusion:'一脊三站两翼通过连续公共空间、三种地标和六条缝合形成总体城市设计。' },
  'agent.2': { section:'产业生态、人才与未来城市研究', figure:'assets/figures/ecosystem-synergy.png', data:'visual/assets/two-answers.json', conclusion:'能力必须经过复现、受控验证、人工决定和知识归档后进入城市。' },
  'agent.3': { section:'AI 创新生态、人才画像与 AI+ 场景', figure:'assets/figures/key-areas.png', data:'visual/assets/two-answers.json', conclusion:'十二场景均具有同题普通答案、AI增量、负责人、测量、停止和恢复。' },
  'agent.4': { section:'三座回执地标、文化里程与国际传播', figure:'assets/figures/key-areas.png', data:'visual/assets/spatial-atlas.json', conclusion:'验真环、共译门、回执廊关闭标题后仍由环、门、十字加单侧湾辨认。' },
  'agent.5': { section:'蓝绿空间、公共空间与城市风貌', figure:'assets/figures/mobility-bluegreen.png', data:'visual/assets/spatial-atlas.json', conclusion:'触觉、高对比、双语、无智能手机入口和城市证据里程共同形成国际公共识别。' },
  'agent.6': { section:'一带全球 AI 创新活动体系与长期运营设计', figure:'assets/figures/metrics-evidence.png', data:'visual/assets/e2-readiness.json', conclusion:'90天试点、8道许可、16项构件、5类表单和城市采纳年构成长效运营证据。' },
};

for (const name of ['compliance_matrix.json','design_depth_matrix.json']) {
  const file = path.join(ROOT, name);
  const value = read(file);
  value.v9_evidence_index = index;
  write(file, value);
}

const changelogFile = path.join(ROOT, 'changelog.md');
let changelog = fs.readFileSync(changelogFile, 'utf8');
if (!changelog.includes('## V9 · 可验证的城市样机')) {
  changelog = changelog.replace(/^# ([^\n]+)\n/, `$&\n## V9 · 可验证的城市样机\n\n- S7 升级为 E2 原型准备文件：16 项构件、8 道许可、5 类空白表单和 4 个采购包；明确未测绘、未许可、未搭建、未现场运行。\n- 五张核心图、A0 三板、A3 十六页及两个 HTML 首屏重构；三张概念体验图与 T2/S2/S7 空间关系对应并单独披露权利边界。\n- 包内 schema 升级至 1.7.0，新增 E2 状态、采购、表单、测量和恢复接口；现场绩效继续为 unknown。\n\n`);
  fs.writeFileSync(changelogFile, changelog.replace(/\r\n/g,'\n'));
}

console.log(JSON.stringify({ metrics:5, agent_evidence:Object.keys(index).length, matrices:2 }, null, 2));
