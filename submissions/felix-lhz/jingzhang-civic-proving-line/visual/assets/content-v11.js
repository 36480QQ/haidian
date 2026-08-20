const fs = require('fs');
const path = require('path');
const { run: runAudit } = require('./spatial-audit-v11');

const ROOT = path.resolve(__dirname, '..', '..');
const read = (rel) => JSON.parse(fs.readFileSync(path.join(ROOT, rel), 'utf8'));
const write = (rel, value) => fs.writeFileSync(path.join(ROOT, rel), JSON.stringify(value, null, 2) + '\n');

const zhBlock = `<!-- V11_DECISION_START -->
## 一次真正的空间裁决

城市采纳编译器不再把“全部通过”当作优秀。V11 对 S7 的同一任务、同一用户和同一场地生成三个空间备选，再用同一组几何硬门审计：**ALT-A 中央混合湾被淘汰，ALT-B 分散双湾退回修改，ALT-C 单侧可逆湾进入深化。** 这里的 reject_design / revise_design / advance_design 是设计备选状态，不是现场采纳结论；现场仍只允许由人类委员会作出 adopt / revise / stop。[data:visual/assets/spatial-decision.json] [metric:spatial_alternative_count]

ALT-A 的试验边界切断公共十字，并与消防、撤场和人工急停可达性同时发生冲突，因此六道硬门失败。ALT-B 保住公共路线，却把两处试验湾、两条撤场线和监督岗位分散到相距约 94.9 米的两端，形成三项软性修改要求。ALT-C 让 372 米概念公共路线在试验态保持原长，将 2,496 平方米试验范围和 3,840 平方米可逆缓冲集中于单侧，并把最远急停—人工岗位距离控制为 24.3 米的原型假设。[metric:rejected_spatial_alternative_count] [metric:advanced_spatial_alternative_count] [data:geometry/public_space.geojson#V11-ALT-C-TRIAL-1]

这些数值来自以大钟寺原型中心建立的局部等距近似画布，只能审查设计几何是否自洽，不代表现状测绘、交通表现、消防审批或安全绩效。任何正式底图、站口、权属或专业条件变化，都必须重新运行审计；若计算结果变化，图纸和文字必须服从计算。[data:geometry/roads.geojson#V11-ALT-C-BASE-NS] [depth:three_key_area_detailed_design]
<!-- V11_DECISION_END -->`;

const enBlock = `<!-- V11_DECISION_START -->
## One Real Spatial Decision

The Civic Adoption Compiler no longer treats an all-green matrix as excellence. V11 generates three spatial alternatives for the same S7 task, users and site, then audits each with identical geometry gates: **ALT-A Central Mixed Bay is rejected, ALT-B Split Bays returns for revision, and ALT-C One-sided Reversible Bay advances.** These reject_design / revise_design / advance_design labels describe design alternatives, not field adoption; only a human committee may later issue adopt / revise / stop.[data:visual/assets/spatial-decision.json] [metric:spatial_alternative_count]

ALT-A severs the public cross and conflicts with fire access, retirement and staffed E-stop reach, failing six hard gates. ALT-B preserves the public routes but splits two trial bays, two retirement paths and supervision posts across about 94.9 metres, producing three revision flags. ALT-C keeps the 372-metre concept public-route total unchanged in trial state, concentrates a 2,496-square-metre trial and 3,840-square-metre reversible buffer on one side, and limits the furthest E-stop-to-staff distance to a 24.3-metre prototype assumption.[metric:rejected_spatial_alternative_count] [metric:advanced_spatial_alternative_count] [data:geometry/public_space.geojson#V11-ALT-C-TRIAL-1]

The figures use a local equidistant approximation centred on the Dazhongsi prototype. They audit design geometry only; they do not establish surveyed conditions, transport performance, fire approval or safety performance. Any change in the official base, station entrance, ownership or professional constraints must rerun the audit, and drawings and prose must follow the calculation.[data:geometry/roads.geojson#V11-ALT-C-BASE-NS] [depth:three_key_area_detailed_design]
<!-- V11_DECISION_END -->`;

function replaceBlock(text, block) {
  const re = /<!-- V11_DECISION_START -->[\s\S]*?<!-- V11_DECISION_END -->/;
  if (re.test(text)) return text.replace(re, block);
  const anchor = text.indexOf('\n## 设计依据与资料清单') >= 0 ? '\n## 设计依据与资料清单' : '\n## Design Basis and Source List';
  return text.replace(anchor, `\n\n${block}\n${anchor}`);
}

function updateNarratives() {
  const files = [
    ['proposal.md', zhBlock, 'summary: "三个空间备选，一次公开否决，一个可复核选择：几何审计淘汰会牺牲公共路径的方案；现场绩效仍未知。"'],
    ['proposal.en.md', enBlock, 'summary: "Three spatial alternatives, one public rejection and one reviewable selection: geometry audit eliminates designs that sacrifice the public route; field performance remains unknown."'],
  ];
  for (const [rel, block, summary] of files) {
    const p = path.join(ROOT, rel); let s = fs.readFileSync(p, 'utf8');
    s = s.replace(/^summary:.*$/m, summary);
    s = s.replace(/> \*\*城市采纳编译器[\s\S]*?\n\n/, '> **城市采纳编译器 / CIVIC ADOPTION COMPILER：三个空间备选，一次公开否决，一个可复核选择。** 普通服务先成立，AI 再进入同题验证；任何会切断公共路线的空间方案必须被编译器淘汰。现场决定仍只允许 `adopt / revise / stop`，并属于人类场景委员会。\n\n');
    s = s.replace(/> \*\*Civic Adoption Compiler[\s\S]*?\n\n/i, '> **Civic Adoption Compiler: three spatial alternatives, one public rejection and one reviewable selection.** Ordinary service stands first; AI enters only the same-task test. Any spatial option that severs the public route must be rejected by the compiler. Field decisions remain `adopt / revise / stop` and belong to a human scenario committee.\n\n');
    s = replaceBlock(s, block);
    s = s.replace(/V10/g, 'V11');
    s = s.replaceAll('visual/assets/v10-tabletop-results.json', 'visual/assets/tabletop-results.json');
    s = s.replaceAll('geometry/roads.geojson#V7-D-BASE-NS', 'geometry/roads.geojson#V11-ALT-C-BASE-NS');
    fs.writeFileSync(p, s);
  }
}

function updateData(decision) {
  for (const rel of ['visual/assets/two-answers.json', 'visual/assets/spatial-atlas.json']) {
    const j = read(rel); j.schema_version = '1.9.0'; j.publication_version = 'V11';
    j.spatial_decision = {
      dataset_ref: 'visual/assets/spatial-decision.json',
      advanced_alternative_id: decision.summary.advanced_alternative_id,
      decisions: { reject_design: decision.summary.reject_count, revise_design: decision.summary.revise_count, advance_design: decision.summary.advance_count },
      verification_scope: 'geometry_based_design_audit', field_status: 'not_field_run',
    };
    if (Array.isArray(j.scenarios)) {
      for (const s of j.scenarios) {
        s.field_status = 'not_field_run';
        if ((s.code || s.scenario_code) === 'S7') {
          s.spatial_decision_ref = 'visual/assets/spatial-decision.json#ALT-C';
          s.alternative_geometry_refs = decision.alternatives.flatMap(a => a.geometry_refs);
          s.design_alternative_state = 'advance_design';
        }
      }
    }
    write(rel, j);
  }
  const metrics = read('metrics.json');
  const defs = {
    spatial_alternative_count: [3, 'count', 'count(spatial-decision.alternatives)'],
    rejected_spatial_alternative_count: [1, 'count', 'count(alternative where decision=reject_design)'],
    revised_spatial_alternative_count: [1, 'count', 'count(alternative where decision=revise_design)'],
    advanced_spatial_alternative_count: [1, 'count', 'count(alternative where decision=advance_design)'],
    spatial_hard_gate_evaluation_count: [21, 'count', '3 alternatives × 7 geometry hard gates'],
    alt_c_public_route_length_m: [372, 'm', 'sum(length(ALT-C OPEN public routes) in local metre projection)'],
    alt_c_trial_area_sqm: [2496, 'sqm', 'polygon_area(ALT-C trial boundary in local metre projection)'],
    alt_c_reversible_buffer_area_sqm: [3840, 'sqm', 'polygon_area(ALT-C reversible buffer in local metre projection)'],
    alt_c_max_estop_staff_distance_m: [24.331, 'm', 'max(min(distance(E-stop, human post)))'],
  };
  for (const [id, [value, unit, formula]] of Object.entries(defs)) metrics.metrics[id] = {status:'known',value,unit,source_files:['visual/assets/spatial-decision.json'],formula,confidence:'high',assumptions:['ASM-V11-PROTOTYPE-DIMENSIONS']};
  metrics.schema_version = '1.9.0'; write('metrics.json', metrics);

  const assumptions = read('assumptions.json');
  const add = [
    {id:'ASM-V11-PROTOTYPE-DIMENSIONS',status:'concept_only',statement:'V11 alternative dimensions and distances are design-model assumptions in a local metre projection, not surveyed site dimensions.',impact:'Rerun the spatial audit after official base mapping, station entrance, fire, accessibility and utility data are confirmed.'},
    {id:'ASM-V11-PROVISIONAL-CONTEXT',status:'pending_official_data',statement:'All three alternatives use the same provisional Dazhongsi context and do not assert official ownership, redlines or station entrances.',impact:'A change in the verified context may change the reject, revise or advance result.'},
  ];
  assumptions.assumptions = assumptions.assumptions.filter(a=>!add.some(x=>x.id===a.id)).concat(add); write('assumptions.json', assumptions);
}

function updateMatrices() {
  const compliance = read('compliance_matrix.json');
  for (const k of Object.keys(compliance)) if (/^v\d+_evidence_index$/.test(k)) delete compliance[k];
  const agent = {
    'agent.1':['总体设计范围城市更新与控规深度城市设计','assets/figures/site-overview.png','一脊三站两翼和三个S7备选共同说明总体空间结构与选择。'],
    'agent.2':['统筹研究范围产业与未来城市研究','assets/figures/land-use-structure.png','能力必须经过空间硬门、公开证据与人工决定才能进入城市。'],
    'agent.3':['AI 创新生态、人才画像与 AI+ 场景','assets/figures/metrics-evidence.png','十二场景保留84项状态契约，S7进一步接受三个空间备选的几何裁决。'],
    'agent.4':['重点区域详细设计','assets/figures/key-areas.png','验真环、共译门和回执廊具备不同平面、剖面、状态和退出路径。'],
    'agent.5':['蓝绿空间、公共空间与城市风貌','assets/figures/mobility-bluegreen.png','公共路线、触觉引导、蓝绿边界和失败回退共同构成公共识别。'],
    'agent.6':['更新项目清单、实施政策与分期计划','assets/figures/metrics-evidence.png','90天试点、许可门、责任、退役和长期复盘形成运行链。'],
  };
  for (const r of compliance.requirements) if (agent[r.requirement_id]) {
    const [section,figure,summary]=agent[r.requirement_id];r.report_sections=[section,'一次真正的空间裁决'];r.geojson_layers=['geometry/roads.geojson','geometry/public_space.geojson','geometry/constraints.geojson'];r.metrics=['spatial_alternative_count','rejected_spatial_alternative_count','advanced_spatial_alternative_count'];r.visual_sections=[figure,'visual/assets/spatial-decision.json'];r.evidence_summary_zh=summary;
  }
  compliance.v11_evidence_index={version:'V11',decision:'visual/assets/spatial-decision.json',figures:'five bilingual canonical core figures',drawings:'A0 3 boards / A3 16 pages',interaction:'report and visual use different first-screen compositions',field_boundary:'geometry audit only; not field-run'}; write('compliance_matrix.json', compliance);

  const depth = read('design_depth_matrix.json'); for(const k of Object.keys(depth))if(/^v\d+_evidence_index$/.test(k))delete depth[k];
  for(const item of depth.items){
    if(['three_key_area_detailed_design','traffic_rail_slow_parking','metrics_recalculation','phasing_implementation'].includes(item.item_id)){
      item.proposal_sections=[...new Set([...(item.proposal_sections||[]).filter(x=>x!=='决策摘要与设计依据'&&x!=='一次真正的空间裁决'),'一次真正的空间裁决'])];
      item.geometry_refs=[...new Set([...(item.geometry_refs||[]),'geometry/roads.geojson','geometry/public_space.geojson','geometry/constraints.geojson'])];
      item.metric_refs=[...new Set([...(item.metric_refs||[]),'spatial_alternative_count','rejected_spatial_alternative_count','advanced_spatial_alternative_count'])];
      item.evidence_summary_zh='V11以三个同题空间备选、21道几何硬门和一项公开否决补强空间选择、交通连续、指标复算与实施退出证据。';
    }
  }
  depth.v11_evidence_index={decision:'visual/assets/spatial-decision.json',spatial_scales:'1:5000 / 1:2000 / 1:500 / 1:200 / 1:50',audit:'reject / revise / advance results computed from geometry',limitation:'prototype dimensions pending official survey'};write('design_depth_matrix.json',depth);

  const standards=read('standard_matrix.json');for(const k of Object.keys(standards))if(/^v\d+_evidence_index$/.test(k))delete standards[k];
  standards.v11_evidence_index={decision:'geometry hard gates and public-route invariants',public_interest:'ordinary service remains independent',professional_followup:'survey, accessibility, fire, utilities and transport confirmation remain required'};write('standard_matrix.json',standards);
}

function updateChangelog() {
  const p=path.join(ROOT,'changelog.md');let s=fs.readFileSync(p,'utf8');
  if(!s.includes('V11 一次真正的空间裁决'))s=s.replace(/^(#.*\n)/,`$1\n## 2026-08-19 · V11 一次真正的空间裁决\n\n- 对 S7 三个同题备选执行可复跑几何审计：ALT-A 淘汰、ALT-B 修改、ALT-C 推进。\n- 将84项状态契约降为附录证据，新增公共路线、消防、撤场、岗位与可逆占地的计算结果。\n- 现场绩效、许可、测绘和报价继续保持未知；设计状态不冒充城市采纳决定。\n\n`);
  fs.writeFileSync(p,s);
}

function run() { const decision=runAudit();updateData(decision);updateNarratives();updateMatrices();updateChangelog();console.log('V11 content and structured evidence updated');return decision; }
module.exports={run};
if(require.main===module)run();
