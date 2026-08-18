const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const read = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));
const write = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
const bi = (zh, en) => ({ zh, en });

const permittedStates = [
  'ready_documented',
  'pending_survey',
  'pending_permit',
  'pending_quote',
  'not_built',
  'not_field_run',
];

const permits = [
  ['PERMIT-SITE', '场地使用与资产方书面同意', 'Written site-use and asset-owner consent'],
  ['PERMIT-TITLE', '权属、边界与现状测绘核验', 'Ownership, boundary and existing-condition survey'],
  ['PERMIT-FIRE', '消防车道、疏散面与临时构筑物复核', 'Fire access, egress apron and temporary-structure review'],
  ['PERMIT-ACCESS', '无障碍路线、坡道、盲道和人工服务审计', 'Audit of accessible routes, ramps, tactile guidance and staffed service'],
  ['PERMIT-POWER', '临时用电、配电保护与断电责任', 'Temporary power, protection and isolation responsibility'],
  ['PERMIT-NET', '隔离网络、数据最小化与日志保存规则', 'Isolated network, data minimisation and log-retention rule'],
  ['PERMIT-TRAFFIC', '常规接驳优先、活动时窗与交通组织审批', 'Conventional-interchange priority, operating window and traffic approval'],
  ['PERMIT-EQUIP', '设备安全、保险、急停与供应商撤场责任', 'Equipment safety, insurance, emergency stop and supplier removal duty'],
].map(([id, zh, en]) => ({ id, label: bi(zh, en), status: 'pending_permit', required_before: 'TRIAL' }));

const bill = [
  ['KIT-PAV-01', '透水铺装', 'Permeable paving', 920, 'sqm', '46m × 20m 原型公共面；待测绘复核', '46m × 20m prototype public surface; survey pending', 'site_asset_lead', 'retain_as_public_space'],
  ['KIT-ACC-01', '连续盲道', 'Continuous tactile guidance', 168, 'linear_m', '南北 92m + 东西 76m 原型路线', '92m north-south + 76m east-west prototype route', 'baseline_service_lead', 'retain_as_public_access'],
  ['KIT-ACC-02', '无障碍坡道', 'Accessible ramps', 4, 'unit', '公共十字四个路缘接口各 1 处', 'one at each of four public-cross curb interfaces', 'baseline_service_lead', 'retain_as_public_access'],
  ['KIT-BGR-01', '雨水花园', 'Rain gardens', 240, 'sqm', '两侧 6m × 20m × 2 处', 'two sides at 6m × 20m each', 'site_asset_lead', 'retain_as_blue_green_asset'],
  ['KIT-SHA-01', '遮阴单元', 'Shade bays', 6, 'bay', '两侧候车与休息面各 3 跨', 'three bays on each waiting/rest edge', 'site_asset_lead', 'retain_as_public_space'],
  ['KIT-FUR-01', '公共座椅', 'Public benches', 12, 'unit', '每个遮阴跨 2 组', 'two units per shade bay', 'baseline_service_lead', 'retain_as_public_space'],
  ['KIT-WAT-01', '饮水点', 'Drinking-water points', 2, 'unit', '公共十字两侧各 1 处', 'one on each side of the public cross', 'site_asset_lead', 'retain_as_public_service'],
  ['KIT-LGT-01', '低位照明', 'Low-level lighting', 16, 'unit', '公共路线按约 12m 原型间距布置', 'prototype spacing of about 12m along public routes', 'site_asset_lead', 'retain_as_public_safety'],
  ['KIT-SAF-01', '可拆隔离单元', 'Removable barriers', 48, 'module', '试验湾边界按 2m 模块复算', 'trial-bay perimeter calculated in 2m modules', 'safety_lead', 'supplier_return_or_storage'],
  ['KIT-SAF-02', '双急停柱', 'Dual emergency-stop posts', 2, 'unit', '试验湾相对两角各 1 处', 'one at each of two opposing trial-bay corners', 'safety_lead', 'supplier_return_or_storage'],
  ['KIT-EVD-01', '人工证据门廊', 'Staffed evidence porch', 48, 'sqm', '8m × 6m 可逆构筑物', '8m × 6m reversible pavilion', 'baseline_service_lead', 'reuse_as_staffed_service'],
  ['KIT-EVD-02', '公开回执墙', 'Public receipt wall', 12, 'linear_m', '门廊两侧各 6m 展示界面', 'two 6m display faces at the porch', 'public_representative', 'retain_as_public_information'],
  ['KIT-OPS-01', '控制亭', 'Control kiosk', 1, 'unit', '独立于人工公共服务岗位', 'separate from the staffed public-service post', 'trial_operator', 'supplier_return_or_storage'],
  ['KIT-AI-01', '可逆试验湾', 'Reversible trial bay', 420, 'sqm', '21m × 20m 单侧原型范围', '21m × 20m one-side prototype area', 'trial_operator', 'restore_as_waiting_or_event_space'],
  ['KIT-DAT-01', '端侧机柜', 'Edge cabinet', 1, 'unit', '隔离供电与网络，位于试验边界内', 'isolated power and network inside the trial boundary', 'data_lead', 'supplier_return_or_secure_storage'],
  ['KIT-RET-01', '存储与撤场门', 'Storage and removal gate', 1, 'unit', '连接试验湾与外侧服务路线', 'connects trial bay to outer service route', 'site_asset_lead', 'retain_as_service_access'],
].map(([id, zh, en, quantity, unit, qzh, qen, owner, destination]) => ({
  id,
  name: bi(zh, en),
  quantity,
  unit,
  quantity_formula: bi(qzh, qen),
  dimension_basis: 'prototype_design_assumption_pending_survey',
  quote_status: 'pending_quote',
  maintenance_owner: owner,
  retirement_destination: destination,
}));

const forms = [
  ['FORM-BASELINE', '普通服务基线记录表', 'Baseline service log', ['date_time', 'weather', 'user_profile_optional', 'task_attempt', 'task_completed', 'assistance_requested', 'route_continuous', 'accessibility_issue', 'appeal_lodged']],
  ['FORM-TRIAL', '受控试验记录表', 'Controlled trial log', ['permit_gate_complete', 'four_posts_present', 'trial_start', 'trial_end', 'eligible_passages', 'human_interventions', 'near_miss_events', 'zero_tolerance_event', 'baseline_regression']],
  ['FORM-INCIDENT', '异常与停止事件表', 'Incident and stop-event form', ['event_time', 'trigger', 'stop_authority', 'equipment_isolated', 'staff_takeover', 'public_routes_open', 'notification', 'corrective_action']],
  ['FORM-RECOVERY', '停止演练与空间恢复表', 'Recovery drill and space-restoration form', ['clock_start', 'ordinary_task_completed', 'north_south_route_open', 'east_west_route_open', 'equipment_removed', 'bay_restored', 'clock_end', 'co_signatures']],
  ['FORM-RECEIPT', '城市采纳回执', 'Civic adoption receipt', ['task', 'same_users', 'ordinary_baseline', 'ai_increment', 'measurement_denominator', 'zero_tolerance_events', 'public_comment', 'appeal_status', 'decision', 'review_due', 'signatures']],
].map(([id, zh, en, fields]) => ({ id, title: bi(zh, en), fields, record_status: 'not_field_run', printable: true }));

const readiness = {
  schema_version: '1.7.0',
  dataset_id: 'jingzhang-v9-e2-readiness',
  title: bi('V9 E2 原型就绪包', 'V9 E2 Prototype Readiness Pack'),
  definition: bi('E2 表示测绘、询价、审批和搭建准备材料已形成，不表示已取得许可、完成搭建或现场运行。', 'E2 means survey, quotation, permit and assembly preparation documents exist; it does not mean permits, construction or field operation are complete.'),
  prototype_readiness: 'ready_documented',
  field_status: 'not_field_run',
  permitted_states: permittedStates,
  survey_dependency: ['official_boundary', 'topographic_survey', 'ownership', 'station_exits', 'utilities', 'fire_access', 'traffic_counts'],
  permit_checklist: permits,
  bill_of_components: bill,
  forms,
  procurement_packages: [
    { id: 'PROC-BASELINE', contents: bill.filter(x => x.id.startsWith('KIT-PAV') || x.id.startsWith('KIT-ACC') || x.id.startsWith('KIT-BGR') || x.id.startsWith('KIT-SHA') || x.id.startsWith('KIT-FUR') || x.id.startsWith('KIT-WAT') || x.id.startsWith('KIT-LGT')).map(x => x.id), status: 'pending_quote' },
    { id: 'PROC-SAFETY', contents: ['KIT-SAF-01', 'KIT-SAF-02', 'KIT-RET-01'], status: 'pending_quote' },
    { id: 'PROC-EVIDENCE', contents: ['KIT-EVD-01', 'KIT-EVD-02'], status: 'pending_quote' },
    { id: 'PROC-AI-OPTIONAL', contents: ['KIT-OPS-01', 'KIT-AI-01', 'KIT-DAT-01'], status: 'pending_quote' },
  ],
};

const readinessFile = path.join(__dirname, 'e2-readiness.json');
write(readinessFile, readiness);

const answersFile = path.join(__dirname, 'two-answers.json');
const answers = read(answersFile);
answers.schema_version = '1.7.0';
answers.publication_version = 'V9';
answers.subtitle = bi('可验证的城市样机', 'Verifiable Civic Prototype');
answers.status_note = bi('S7 已形成 E2 原型准备文件；仍未测绘、许可、搭建或现场运行。', 'S7 has an E2 prototype-preparation dossier; survey, permits, assembly and field operation remain incomplete.');
answers.prototype_readiness = {
  status: 'ready_documented',
  scope: 'S7_DAZHONGSI_FLAGSHIP',
  field_status: 'not_field_run',
  readiness_pack_ref: 'visual/assets/e2-readiness.json',
};
answers.permit_checklist = permits;
answers.bill_of_components = bill;
answers.form_templates = forms;
answers.scenarios.forEach((scene) => {
  const isS7 = scene.code === 'S7';
  const isHero = ['T2', 'S2', 'S7'].includes(scene.code);
  Object.assign(scene, {
    prototype_readiness: isS7 ? 'ready_documented' : isHero ? 'pending_survey' : 'not_built',
    readiness_gate: isS7 ? 'all_eight_permits_and_four_independent_posts_before_TRIAL' : 'replicate_after_S7_review',
    survey_dependency: readiness.survey_dependency,
    permit_checklist: isS7 ? permits.map(x => x.id) : permits.slice(0, 4).map(x => x.id),
    bill_of_components: isS7 ? bill.map(x => x.id) : scene.prototype_kit_refs || [],
    quantity_formula: isS7 ? 'see_visual_assets_e2_readiness_json' : 'adapt_after_site_survey',
    procurement_package_ref: isS7 ? ['PROC-BASELINE', 'PROC-SAFETY', 'PROC-EVIDENCE', 'PROC-AI-OPTIONAL'] : [],
    baseline_form_ref: 'FORM-BASELINE',
    trial_form_ref: 'FORM-TRIAL',
    incident_form_ref: 'FORM-INCIDENT',
    recovery_drill_ref: 'FORM-RECOVERY',
    receipt_template_ref: 'FORM-RECEIPT',
    e2_status: isS7 ? 'ready_documented' : 'not_built',
  });
  scene.evidence_level = isS7 ? 'E2_READINESS_DOCUMENTED_NOT_BUILT' : scene.evidence_level;
  scene.evidence_status = 'not_field_run';
  scene.receipt_state = 'pending_field_evidence';
});
write(answersFile, answers);

const atlasFile = path.join(__dirname, 'spatial-atlas.json');
const atlas = read(atlasFile);
atlas.schema_version = '1.7.0';
atlas.publication_version = 'V9';
atlas.subtitle = bi('可验证的城市样机', 'Verifiable Civic Prototype');
atlas.prototype_readiness = answers.prototype_readiness;
atlas.readiness_gate = 'ordinary_baseline_survey_permits_independent_posts_forms_complete_before_TRIAL';
atlas.survey_dependency = readiness.survey_dependency;
atlas.permit_checklist = permits.map(x => x.id);
atlas.bill_of_components = bill.map(x => x.id);
atlas.form_refs = forms.map(x => x.id);
atlas.landmarks.forEach((landmark) => {
  landmark.prototype_readiness = landmark.station_ref === 'dazhongsi' ? 'ready_documented' : 'pending_survey';
  landmark.experience_view = `assets/figures/concept-${landmark.station_ref === 'zhongzhiyuan' ? 't2' : landmark.station_ref === 'ai_origin' ? 's2' : 's7'}-v9.webp`;
  landmark.experience_view_status = 'concept_generated_not_site_evidence';
});
write(atlasFile, atlas);

const zhInsert = `\n### V9 可验证城市样机：E2 原型就绪而非现场完成\n\nV9 将大钟寺 S7 从单纯 E1 概念图推进为 **E2 原型准备文件完整**：同一套几何同时生成 1:5000 城市联系、1:2000 重点区、1:500 构件详图、1:200 剖面和分层剖切轴测。E2 在本方案中的严格含义是：构件数量、八类许可、采购分包、普通基线表、受控试验表、异常停止表、恢复演练表和城市采纳回执均已形成可复核模板；它**不表示**测绘、许可、采购、搭建或现场运行已经发生。\n\nS7 的普通公共十字和人工服务必须先完成测绘与 7 个连续运行日的基线记录。只有场地、权属、消防、无障碍、临电、网络、交通组织和设备安全八道许可门全部关闭，且场地负责人、普通服务人员、安全负责人和数据记录人员独立在岗，东南侧试验湾才可进入 \`TRIAL\`。碰撞、缓冲侵入、急停失效、公共路线中断或人工接管失败均触发零容忍停止；计时从停止指令开始，到人工完成同题任务且两条公共路线恢复开放为止。当前恢复时间仍为 \`unknown / not_field_run\`。\n\n三座地标继续采用不同空间原型：众智园验真环以完整公共旁路包围受控内环；AI 原点共译门以三条无账户路线穿过人工服务与复核后台；大钟寺回执廊以公共十字、单侧试验湾和人工证据门廊构成旗舰样机。三张体验图均为严格对应构件关系的概念生成图，不承担现状、尺度或绩效证明。\n`;
const enInsert = `\n### V9 Verifiable Civic Prototype: E2 readiness, not field completion\n\nV9 advances Dazhongsi S7 from an E1 concept drawing to an **E2 prototype-preparation dossier**. One geometry model now drives the 1:5000 link, 1:2000 key-area plan, 1:500 component detail, 1:200 section and layered cutaway axonometric. E2 has a strict meaning here: reproducible quantities, eight permit gates, procurement packages, a baseline log, controlled-trial log, incident form, recovery-drill form and civic-adoption receipt exist as reviewable templates. It **does not mean** survey, permits, procurement, assembly or field operation have occurred.\n\nThe ordinary public cross and staffed service must be surveyed and logged for seven consecutive operating days first. The southeast trial bay may enter \`TRIAL\` only after site, title, fire, accessibility, temporary power, network, traffic-management and equipment-safety gates are closed and four independent posts are staffed. Collision, buffer intrusion, emergency-stop failure, interruption of a public route or failed human takeover triggers a zero-tolerance stop. The recovery clock runs from the stop command until staff complete the same task and both public routes reopen. Recovery time remains \`unknown / not_field_run\`.\n\nThe three landmarks retain different spatial archetypes: the Verification Ring wraps a controlled inner ring with a complete public bypass; the Translation Gate carries three account-free paths past staffed service and professional review; the Receipt Porch combines a public cross, one-side trial bay and staffed evidence interface. All three experiential views are geometry-matched concept images, not evidence of existing conditions, dimensions or performance.\n`;

function insertSection(file, marker, content) {
  let text = fs.readFileSync(file, 'utf8');
  text = text.replace(/\n### V9 [\s\S]*?(?=\n## )/, '\n');
  const index = text.indexOf(marker);
  if (index < 0) throw new Error(`marker not found in ${file}`);
  text = text.slice(0, index) + content + text.slice(index);
  fs.writeFileSync(file, text.replace(/\r\n/g, '\n'));
}
insertSection(path.join(ROOT, 'proposal.md'), '\n## 总体设计：', zhInsert);
insertSection(path.join(ROOT, 'proposal.en.md'), '\n## Overall design:', enInsert);

const assumptionsFile = path.join(ROOT, 'assumptions.json');
const assumptions = read(assumptionsFile);
assumptions.assumptions = assumptions.assumptions || [];
if (!assumptions.assumptions.some(x => x.id === 'ASM-V9-E2')) assumptions.assumptions.push({
  id: 'ASM-V9-E2',
  statement: bi('E2 仅表示原型准备文件完整；测绘、许可、报价、搭建和现场运行仍待完成。', 'E2 means prototype-preparation documents are complete; survey, permits, quotes, assembly and field operation remain pending.'),
  status: 'active',
  consequence: bi('不得把空白表单、构件数量或数字样机解读为现场绩效。', 'Blank forms, quantities and the digital prototype must not be read as field performance.'),
});
write(assumptionsFile, assumptions);

console.log(JSON.stringify({ schema: '1.7.0', scenarios: answers.scenarios.length, permits: permits.length, components: bill.length, forms: forms.length, s7_e2: 'ready_documented' }, null, 2));
