const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const readJson = rel => JSON.parse(fs.readFileSync(path.join(ROOT, rel), 'utf8'));
const writeJson = (rel, value) => fs.writeFileSync(path.join(ROOT, rel), JSON.stringify(value, null, 2) + '\n');
const readText = rel => fs.readFileSync(path.join(ROOT, rel), 'utf8');
const writeText = (rel, value) => fs.writeFileSync(path.join(ROOT, rel), value.replace(/\r\n/g, '\n'));

const zhIntro = `

> **不断线的公共十字 / THE UNBROKEN PUBLIC CROSS。** 普通服务先成立，AI 只进入一侧可逆试验湾；任何会切断公共路线、侵占消防或撤场路径的备选都必须被公开淘汰。后台几何审计仍称“城市采纳编译器”，但首屏只展示一个可进入、可暂停、可恢复的城市空间。[data:visual/assets/v14-spatial-model.json] [data:visual/assets/spatial-decision.json]

公开资料能够确认京张铁路遗址公园、轨道、道路、水系与公园的方向性关系，却不能确认大钟寺现状建筑界面：2026-08-13 的 OSM 裁切在该范围仅含 1 个建筑要素。因此 V14 不虚构站口或沿街建筑，而以“公开数据缺测”作为设计前置条件；所有尺寸仍是待测绘复核的原型假设。[data:visual/assets/context-open-map.json] [source:OPENSTREETMAP-CONTEXT-20260813]

同一任务、同一用户、同一场地接受同一组硬门后，ALT-A 中央混合湾因切断公共十字被 **REJECT**，ALT-B 因监督与撤场碎片化被 **REVISE**，ALT-C 单侧可逆湾进入深化。ALT-C 将全天公共十字、东南试验湾、西南人工回执廊和双侧蓝绿边界画进同一张 1:500 平面与 1:200 剖面。[metric:rejected_spatial_alternative_count] [metric:revised_spatial_alternative_count] [metric:advanced_spatial_alternative_count]

**当前实施决定是 G0 NO-GO。** 设计文件已形成，但精确测绘、权属、八类许可、四个独立岗位和连续 7 日普通服务基线均未完成；当前关闭许可为 0/8、已记录基线为 0/7 日，因此 AI 试验不得开始。这个 no-go 是可实施性的诚实起点，不是失败。[data:visual/assets/e2-readiness.json] [metric:current_trial_open_gate_count] [metric:pending_trial_permit_count]

六项任务各有独立入口：Agent 1 见区域能力交换；Agent 2 见首层界面和公共基线；Agent 3 见十二场景与三份英雄契约；Agent 4 见验真环、共译门、回执廊；Agent 5 见京张文化里程与双语触觉识别；Agent 6 见一天运行、90 天试点和城市采纳年。现场决定仍只允许人类委员会作出 \`adopt / revise / stop\`。[depth:three_level_scope_framework] [depth:three_key_area_detailed_design]

![总体双答结构](assets/figures/site-overview.png)

`;

const enIntro = `

> **THE UNBROKEN PUBLIC CROSS.** Ordinary service stands first. AI may enter one reversible bay only; any option that cuts the public route or occupies fire and removal access must be rejected in public. The geometry audit remains the back-stage “Civic Adoption Compiler”, while the first screen shows one enterable, pausable and recoverable civic space.[data:visual/assets/v14-spatial-model.json] [data:visual/assets/spatial-decision.json]

Public sources establish only directional relations among the Jing-Zhang heritage park, rail, roads, water and parks. They do not establish the existing frontage at Dazhongsi: the 2026-08-13 OSM crop contains one building feature in this context. V14 therefore does not invent station exits or buildings; the data gap is a precondition, and all dimensions remain prototype assumptions pending survey.[data:visual/assets/context-open-map.json] [source:OPENSTREETMAP-CONTEXT-20260813]

Under the same task, users, site and hard gates, ALT-A is **REJECTED** for cutting the public cross; ALT-B is **REVISED** because supervision and removal are fragmented; ALT-C advances. ALT-C draws the all-day public cross, south-east trial bay, south-west staffed receipt porch and two blue-green edges into the same 1:500 plan and 1:200 section.[metric:rejected_spatial_alternative_count] [metric:revised_spatial_alternative_count] [metric:advanced_spatial_alternative_count]

**The present implementation decision is G0 NO-GO.** Design documents exist, but precise survey, title, eight permits, four independent duty posts and seven consecutive baseline days do not. Closed permits are 0/8 and recorded baseline days are 0/7, so no AI trial may begin. This honest no-go is the starting point of feasibility, not a failure.[data:visual/assets/e2-readiness.json] [metric:current_trial_open_gate_count] [metric:pending_trial_permit_count]

The six tasks have separate entrances: Agent 1 regional capability exchange; Agent 2 ground interfaces and public baseline; Agent 3 twelve scenes and three hero contracts; Agent 4 the Ring, Gate and Porch; Agent 5 the Jing-Zhang evidence mile and bilingual tactile identity; Agent 6 one-day operation, the 90-day pilot and civic year. Field decisions remain \`adopt / revise / stop\`, made by a human scene committee.[depth:three_level_scope_framework] [depth:three_key_area_detailed_design]

![Overall Two Answers structure](assets/figures/site-overview.en.png)

`;

const zhContracts = `<!-- V12_MEASUREMENT_START -->
## 入选之后再测量：三份英雄契约与十二项目录

空间裁决回答“为什么选 ALT-C”，测量契约回答“建成后如何知道 AI 是否值得保留”。完整 12/12 契约继续登记在结构化数据中，但不再用十二行小字表格占据评审首屏；本节只展示三类可复制的英雄契约。[data:visual/assets/two-answers.json] [metric:measurement_contract_count]

- **T2 机器人通行**：普通与试验模式各 100 次同路线通行，按轮椅、视障、步行和昼夜分层；碰撞、公共旁路中断或急停失效立即停止。
- **S2 国际人才抵达**：人工与 AI 辅助各 100 个同题请求，按语言、辅助需求和复杂度分层；无账户入口、人工双语台和复核后台始终开放。
- **S7 轨道接驳**：先记录连续 7 个普通运行日，再在 8 类许可和 4 个独立岗位齐全后进行 100 次限时试验；公共路线中断、无人工接管或基础服务退化均为零容忍事件。

当前仍为 **12 份契约 / 0 项现场结果**。缺失样本不得填补为成功，非安全阈值由现场基线建立后的场景委员会登记。[metric:field_verification_result_count]
<!-- V12_MEASUREMENT_END -->`;

const enContracts = `<!-- V12_MEASUREMENT_START -->
## Measure after selection: three hero contracts and a twelve-scene directory

The spatial decision answers why ALT-C is selected; measurement contracts answer how the city will know whether AI deserves to remain. All 12/12 contracts stay in structured data, while this review entrance shows only three transferable hero contracts.[data:visual/assets/two-answers.json] [metric:measurement_contract_count]

- **T2 robot passage:** 100 same-route passages per ordinary and trial mode, stratified by wheelchair, visual impairment, walking and day/night; collision, bypass interruption or E-stop failure triggers an immediate stop.
- **S2 international arrival:** 100 same-task requests per staffed and AI-assisted mode, stratified by language, assistance need and complexity; account-free entry, bilingual staff and review backstage remain open.
- **S7 transit feeder:** record seven ordinary operating days first, then 100 timed trials only after eight permits and four independent posts close; a broken public route, absent takeover or degraded baseline is zero-tolerance.

The status remains **12 contracts / 0 field results**. Missing samples cannot be imputed as success; non-safety thresholds are registered by the scene committee after a field baseline exists.[metric:field_verification_result_count]
<!-- V12_MEASUREMENT_END -->`;

function replaceIntro(text, intro) {
  const marker = '<!-- V11_DECISION_START -->';
  const idx = text.indexOf(marker);
  if (idx < 0) throw new Error('Decision marker missing');
  const h1 = text.match(/^# .+$/m);
  if (!h1) throw new Error('H1 missing');
  const headEnd = h1.index + h1[0].length;
  return text.slice(0, headEnd + 1) + intro + text.slice(idx);
}

function updateProposal(rel, lang) {
  let text = readText(rel);
  if (!/^# .+$/m.test(text)) {
    const h1 = lang === 'zh' ? '# 京张双答 / JING-ZHANG TWO ANSWERS' : '# JING-ZHANG TWO ANSWERS / 京张双答';
    text = text.replace(/^(---\n[\s\S]*?\n---)\n+/, `$1\n\n${h1}\n`);
  }
  text = text.replace(/^summary: ".*"$/m, lang === 'zh'
    ? 'summary: "公共十字永远不断线，AI只进入一侧可逆试验湾；越线方案公开淘汰，当前实施门为G0 NO-GO。"'
    : 'summary: "The public cross never breaks; AI enters one reversible bay only, crossing options are rejected, and the current implementation gate is G0 NO-GO."');
  text = replaceIntro(text, lang === 'zh' ? zhIntro : enIntro);
  text = text.replace(/<!-- V12_MEASUREMENT_START -->[\s\S]*?<!-- V12_MEASUREMENT_END -->/, lang === 'zh' ? zhContracts : enContracts);
  const replacements = lang === 'zh' ? [
    ['S7 为 `E2_documented_prototype_ready`，T2/S2 为 `E1_concept_design`', 'S7 当前为 `G0_no_go_pending_survey_and_permits`，T2/S2 为 `E1_concept_design`'],
    ['S7 的 **E2 原型准备文件**', 'S7 的 **设计完整 / 试验未准入文件包**'],
    ['E2 同时登记 8 类许可、4 个采购包和 5 类空白表单；它**不表示**测绘、许可、采购、搭建或现场运行已经发生。', '文件包登记 8 类许可、4 个采购包和 5 类空白表单；当前 8 类许可全部待办，结论明确为 **G0 NO-GO**，不表示测绘、采购、搭建或现场运行已经发生。']
  ] : [
    ['S7 is `E2_documented_prototype_ready` while T2/S2 are `E1_concept_design`', 'S7 is `G0_no_go_pending_survey_and_permits` while T2/S2 are `E1_concept_design`'],
    ['S7 **E2 prototype-preparation documents**', 'S7 **design-complete / trial-not-admitted document pack**']
  ];
  for (const [a, b] of replacements) text = text.replace(a, b);
  writeText(rel, text);
}

function updateReadiness() {
  const data = readJson('visual/assets/e2-readiness.json');
  data.dataset_id = 'jingzhang-v14-pretrial-g0-gate';
  data.title = {zh: 'V14 S7 G0 试验准入门', en: 'V14 S7 G0 Pre-trial Gate'};
  data.definition = {
    zh: '设计原型和准备表单已经形成，但测绘、权属、八类许可、独立岗位和普通服务基线未完成；当前结论为NO-GO。',
    en: 'The design prototype and preparation forms exist, but survey, title, eight permits, independent posts and the ordinary-service baseline are incomplete; the current decision is NO-GO.'
  };
  data.prototype_readiness = 'G0_no_go_pending_survey_and_permits';
  data.readiness_gate = {
    gate_id: 'G0-S7-PRETRIAL',
    decision: 'no_go',
    closed_permit_count: data.permit_checklist.filter(x => x.status === 'ready_documented').length,
    required_permit_count: data.permit_checklist.length,
    recorded_baseline_days: 0,
    required_baseline_days: 7,
    contracted_independent_role_count: 0,
    required_independent_role_count: 4,
    next_decision: 'repeat_gate_after_survey_permits_roles_and_baseline'
  };
  writeJson('visual/assets/e2-readiness.json', data);
}

function updateMetrics() {
  const data = readJson('metrics.json');
  data.metrics.current_trial_open_gate_count = {
    status: 'known', value: 0, unit: 'count',
    source_files: ['visual/assets/e2-readiness.json'],
    formula: 'count(readiness gates whose current decision permits TRIAL)',
    confidence: 'high', assumptions: []
  };
  data.metrics.pending_trial_permit_count = {
    status: 'known', value: 8, unit: 'count',
    source_files: ['visual/assets/e2-readiness.json'],
    formula: 'count(permit_checklist where status=pending_permit)',
    confidence: 'high', assumptions: []
  };
  writeJson('metrics.json', data);
}

function updateAtlasAndScenes() {
  const atlas = readJson('visual/assets/spatial-atlas.json');
  atlas.v14_spatial_model_ref = 'visual/assets/v14-spatial-model.json';
  atlas.current_implementation_gate = 'G0_no_go_pending_survey_and_permits';
  writeJson('visual/assets/spatial-atlas.json', atlas);
  const scenes = readJson('visual/assets/two-answers.json');
  scenes.v14_spatial_model_ref = 'visual/assets/v14-spatial-model.json';
  scenes.current_implementation_gate = 'G0_no_go_pending_survey_and_permits';
  writeJson('visual/assets/two-answers.json', scenes);
}

function updateChangelog() {
  const rel = 'changelog.md';
  let text = readText(rel);
  if (!text.includes('## V14 - 不断线的公共十字')) {
    text = text.replace(/^(# .*\n)/, `$1\n## V14 - 不断线的公共十字\n\n- 将“城市采纳编译器”降为后台审计方法，首屏改为公共十字、单侧试验湾和人工回执廊。\n- S7 当前准入结论改为 G0 NO-GO：0/8 许可、0/7 基线日、0/4 已落实独立岗位。\n- 十二场景测量契约保留在结构化目录，首屏只显示 T2、S2、S7 三份英雄契约。\n- 新增统一米制空间模型，驱动 V14 平面、剖面、轴测、出版物和交互入口。\n\n`);
  }
  writeText(rel, text);
}

function run() {
  updateReadiness();
  updateMetrics();
  updateAtlasAndScenes();
  updateProposal('proposal.md', 'zh');
  updateProposal('proposal.en.md', 'en');
  updateChangelog();
  console.log('V14 public-cross content and G0 NO-GO gate written');
}

module.exports = {run};
if (require.main === module) run();
