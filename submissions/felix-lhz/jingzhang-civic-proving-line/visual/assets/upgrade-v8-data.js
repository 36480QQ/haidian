const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const read = (rel) => JSON.parse(fs.readFileSync(path.join(ROOT, rel), 'utf8'));
const write = (rel, value) => fs.writeFileSync(path.join(ROOT, rel), `${JSON.stringify(value, null, 2)}\n`);
const bi = (zh, en) => ({ zh, en });
const unique = (items) => Array.from(new Set(items));
const upsertBy = (items, key, value) => {
  const next = items.filter((item) => item[key] !== value[key]);
  next.push(value);
  return next;
};

const landmarks = [
  {
    id: 'LMK-01',
    station_ref: 'zhongzhiyuan',
    title: bi('众智园·验真环', 'Zhongzhiyuan Verification Ring'),
    spatial_archetype: 'complete_public_bypass_around_controlled_verification_ring',
    public_baseline_refs: ['B01', 'B02', 'B03'],
    ai_plugin_refs: ['A01', 'A02'],
    evidence_interface_refs: ['E01', 'E02', 'E03'],
    heritage_story_ref: 'MILE-02-EXPERIMENT',
    honor_display_rule: bi('只登记任务、复现条件、许可、失败原因、证据等级和人工决定；不设置企业广告排行榜。', 'Record task, reproducibility conditions, licence, failure reason, evidence level and human decision only; no promotional ranking.'),
    state_views: ['OPEN', 'TRIAL', 'PAUSE', 'RETIRE'],
    scene_refs: ['SCN-001', 'SCN-002', 'SCN-003'],
    status: 'concept_proposal',
  },
  {
    id: 'LMK-02',
    station_ref: 'ai_origin',
    title: bi('AI 原点·共译门', 'AI Origin Translation Gate'),
    spatial_archetype: 'three_no_account_public_passages_through_staffed_translation_interface',
    public_baseline_refs: ['B01', 'B02', 'B03'],
    ai_plugin_refs: ['A03'],
    evidence_interface_refs: ['E01', 'E03'],
    heritage_story_ref: 'MILE-03-OPEN_KNOWLEDGE',
    honor_display_rule: bi('公开问题、人工复核和可复用知识包，不展示未经复核的模型自评分。', 'Display public questions, human review and reusable knowledge packs, never unreviewed model self-scores.'),
    state_views: ['OPEN', 'TRIAL', 'PAUSE', 'RETIRE'],
    scene_refs: ['SCN-004', 'SCN-005', 'SCN-006'],
    status: 'concept_proposal',
  },
  {
    id: 'LMK-03',
    station_ref: 'dazhongsi',
    title: bi('大钟寺·回执廊', 'Dazhongsi Receipt Porch'),
    spatial_archetype: 'continuous_public_cross_one_side_reversible_trial_bay_and_staffed_receipt_porch',
    public_baseline_refs: ['B01', 'B02', 'B03'],
    ai_plugin_refs: ['A01', 'A03'],
    evidence_interface_refs: ['E01', 'E02', 'E03'],
    heritage_story_ref: 'MILE-04-CIVIC_DECISION',
    honor_display_rule: bi('回执只允许 adopt、revise、stop，并记录复核日期、申诉入口和退出资产。', 'Receipts allow adopt, revise or stop only and record review date, appeal access and exit assets.'),
    state_views: ['OPEN', 'TRIAL', 'PAUSE', 'RETIRE'],
    scene_refs: ['SCN-010', 'SCN-011', 'SCN-012'],
    status: 'concept_proposal',
  },
];

const annualProgram = [
  {
    program_id: 'YEAR-SPRING', season: 'spring', station_ref: 'belt_wide',
    title: bi('公共基线审计季', 'Public Baseline Audit Season'),
    users: ['wheelchair_user', 'blind_pedestrian', 'older_adult_without_smartphone', 'night_operator'],
    ordinary_baseline: bi('人工无障碍审计、静态导视核验、遮阴饮水和常规接驳台账。', 'Staff-led accessibility audit, static-sign check, shade/water and conventional interchange ledger.'),
    ai_optional: bi('可选工具只整理公开问题，不替代现场判断。', 'Optional tools organise public issues only and do not replace field judgement.'),
    entry_gate: 'named_baseline_operator_and_accessibility_review_method',
    evidence_output: 'baseline_issue_register',
    stop_condition: 'ordinary_service_or_accessibility_route_unavailable',
    knowledge_asset: 'public_baseline_audit_pack',
  },
  {
    program_id: 'YEAR-SUMMER', season: 'summer', station_ref: 'zhongzhiyuan',
    title: bi('能力验真与开发者开放测试', 'Capability Verification and Developer Open Test'),
    users: ['developer_team', 'safety_reviewer', 'accessibility_observer'],
    ordinary_baseline: bi('隔离场地、人工安全员、手工复现清单和完整公共旁路。', 'Isolated site, human safety staff, manual reproducibility checklist and complete public bypass.'),
    ai_optional: bi('模型、机器人和端侧设备在受控边界内接受复现与降级测试。', 'Models, robots and edge devices undergo reproducibility and degradation tests in a controlled boundary.'),
    entry_gate: 'licence_safety_data_and_shutdown_checks_complete',
    evidence_output: 'verification_dossier',
    stop_condition: 'safety_data_or_degradation_gate_failure',
    knowledge_asset: 'open_verification_recipe',
  },
  {
    program_id: 'YEAR-AUTUMN', season: 'autumn', station_ref: 'dazhongsi',
    title: bi('城市场景试用与公众采纳周', 'Urban Trial and Civic Adoption Week'),
    users: ['resident_and_carer', 'visitor', 'international_team', 'transport_operator'],
    ordinary_baseline: bi('普通路线、人工服务、常规接驳和纸质回执先独立运行。', 'Ordinary routes, staffed service, conventional interchange and paper receipt operate first.'),
    ai_optional: bi('AI 只在许可时窗和一侧试验湾比较同题增量。', 'AI compares same-task increment only in a permitted window and one-side trial bay.'),
    entry_gate: 'E2_baseline_complete_and_all_trial_permits_valid',
    evidence_output: 'civic_adoption_receipt',
    stop_condition: 'zero_tolerance_event_or_baseline_regression',
    knowledge_asset: 'adopt_revise_stop_case_record',
  },
  {
    program_id: 'YEAR-WINTER', season: 'winter', station_ref: 'ai_origin',
    title: bi('年度回执与退出复盘', 'Annual Receipt and Exit Review'),
    users: ['public_representative', 'asset_owner', 'service_operator', 'data_reviewer'],
    ordinary_baseline: bi('公开会议、纸质摘要、人工申诉和资产盘点。', 'Public meeting, paper summary, staffed appeal and asset inventory.'),
    ai_optional: bi('可选助手仅生成可追溯摘要，最终决定由人类委员会签署。', 'Optional assistant produces traceable summaries only; the human committee signs the final decision.'),
    entry_gate: 'conflict_disclosure_and_evidence_quality_review_complete',
    evidence_output: 'annual_public_ledger',
    stop_condition: 'evidence_not_reproducible_or_conflict_not_disclosed',
    knowledge_asset: 'annual_civic_proof_archive',
  },
];

const pilotProtocol = {
  pilot_id: 'S7-90D',
  scene_ref: 'SCN-010',
  status: 'concept_schedule_pending_site_and_operator_confirmation',
  minimum_role_coverage: ['site_lead', 'ordinary_service_staff', 'safety_lead', 'data_recorder'],
  role_separation_rule: 'safety_lead_and_ordinary_service_staff_must_not_be_the_same_person_during_TRIAL',
  phases: [
    { phase_id: 'P90-01', day_range: '0-15', entry_gate: 'site_access_for_survey', owner_roles: ['site_lead'], evidence_output: 'survey_and_permission_gap_register', stop_condition: 'boundary_ownership_exit_fire_utility_or_traffic_unknown_blocks_layout', receipt_state: 'E1' },
    { phase_id: 'P90-02', day_range: '16-30', entry_gate: 'baseline_layout_reviewed', owner_roles: ['site_lead', 'ordinary_service_staff'], evidence_output: 'ordinary_baseline_prototype', stop_condition: 'public_cross_or_accessibility_route_incomplete', receipt_state: 'E2_pending' },
    { phase_id: 'P90-03', day_range: '31-45', entry_gate: 'ordinary_baseline_operational', owner_roles: ['ordinary_service_staff', 'data_recorder'], evidence_output: 'seven_operating_day_baseline', stop_condition: 'sample_definition_or_manual_service_not_stable', receipt_state: 'E2' },
    { phase_id: 'P90-04', day_range: '46-75', entry_gate: 'all_permits_RACI_and_zero_tolerance_controls_active', owner_roles: ['site_lead', 'ordinary_service_staff', 'safety_lead', 'data_recorder'], evidence_output: 'controlled_same_task_trial_log', stop_condition: 'any_zero_tolerance_event_or_baseline_regression', receipt_state: 'E3' },
    { phase_id: 'P90-05', day_range: '76-90', entry_gate: 'trial_closed_or_completed', owner_roles: ['site_lead', 'ordinary_service_staff', 'safety_lead', 'data_recorder', 'public_representative'], evidence_output: 'recovery_verification_and_public_receipt', stop_condition: 'public_space_not_restored_or_evidence_not_reproducible', receipt_state: 'E4_pending' },
  ],
};

const atlasPath = 'visual/assets/spatial-atlas.json';
const atlas = read(atlasPath);
atlas.schema_version = '1.6.0';
atlas.publication_version = 'V8';
atlas.subtitle = bi('三站一历：三座回执地标与一个城市年度', 'Three Stations, One Civic Year: three receipt landmarks and one operating calendar');
atlas.landmarks = landmarks;
atlas.annual_program_refs = annualProgram.map((item) => item.program_id);
atlas.heritage_mile_system = {
  status: 'concept_proposal',
  graphic_language: 'heritage_graphite_rail + public_green_baseline + candidate_amber_joint + evidence_blue_receipt',
  milestones: [
    { id: 'MILE-01-RAIL', title: bi('京张铁路记忆', 'Jing-Zhang Railway Memory'), evidence_source: 'JINGZHANG-PARK-PLANNING-INTERPRETATION' },
    { id: 'MILE-02-EXPERIMENT', title: bi('公开实验', 'Open Experiment'), evidence_source: 'ZHONGGUANCUN-CULTURE-HISTORY' },
    { id: 'MILE-03-OPEN_KNOWLEDGE', title: bi('开源转译', 'Open Knowledge Translation'), evidence_source: 'AGENT-TASKBOOK' },
    { id: 'MILE-04-CIVIC_DECISION', title: bi('城市采纳回执', 'Civic Adoption Receipt'), evidence_source: 'agent_generated_design' },
  ],
};
write(atlasPath, atlas);

const answersPath = 'visual/assets/two-answers.json';
const answers = read(answersPath);
answers.schema_version = '1.6.0';
answers.publication_version = 'V8';
answers.title = bi('京张双答：三站一历', 'Jing-Zhang Two Answers: Three Stations, One Civic Year');
answers.subtitle = bi('一条不断线的公共基线，三座会留下回执的城市地标，一年四季的公开采纳程序。', 'One uninterrupted public baseline, three civic landmarks that leave receipts, and a year-round public adoption process.');
answers.annual_program = annualProgram;
answers.pilot_protocol = pilotProtocol;
answers.public_ledger_schema = {
  status: 'schema_only_no_field_records',
  allowed_decisions: ['adopt', 'revise', 'stop'],
  required_fields: ['event_id', 'task', 'user_group', 'ordinary_baseline', 'ai_increment', 'evidence_level', 'measurement_definition', 'human_decision', 'review_due', 'appeal_route', 'exit_asset_destination'],
  records: [],
};
answers.scenarios = answers.scenarios.map((scenario) => ({
  ...scenario,
  review_due: scenario.review_due || 'after_E2_or_next_annual_review',
  receipt_state: scenario.receipt_state && !String(scenario.receipt_state).includes('V7') ? scenario.receipt_state : 'pending_field_evidence',
}));
write(answersPath, answers);

const metrics = read('metrics.json');
metrics.metrics.receipt_landmark_count = { status: 'known', value: 3, unit: 'count', source_files: [atlasPath], formula: 'count(landmarks)', confidence: 'high', assumptions: ['A-V8-LANDMARKS'] };
metrics.metrics.annual_program_cycle_count = { status: 'known', value: 4, unit: 'count', source_files: [answersPath], formula: 'count(annual_program)', confidence: 'high', assumptions: ['A-V8-OPERATIONS'] };
metrics.metrics.s7_pilot_phase_count = { status: 'known', value: 5, unit: 'count', source_files: [answersPath], formula: 'count(pilot_protocol.phases)', confidence: 'high', assumptions: ['A-V8-OPERATIONS'] };
metrics.metrics.agent_task_unique_evidence_count = { status: 'known', value: 6, unit: 'count', source_files: ['compliance_matrix.json'], formula: 'count(agent.1..agent.6 with distinct evidence summary, report section and drawing set)', confidence: 'high', assumptions: [] };
metrics.metrics.public_ledger_record_status = { status: 'unknown', value: null, unit: 'field_records', source_files: [answersPath], formula: 'count(public_ledger_schema.records after E2/E3)', confidence: 'unknown', assumptions: ['A-METRICS-001', 'A-V8-OPERATIONS'], reason: 'The ledger contract exists, but no field prototype, trial or civic decision has occurred.' };
write('metrics.json', metrics);

const assumptions = read('assumptions.json');
assumptions.assumptions = upsertBy(assumptions.assumptions, 'id', { id: 'A-V8-LANDMARKS', status: 'concept_only', statement: 'Verification Ring, Translation Gate and Receipt Porch are conceptual civic landmark prototypes under provisional boundaries, not approved buildings or installed public art.', impact: 'Location, structure, heritage review, fire access, utilities, ownership and accessibility require professional verification before E2.' });
assumptions.assumptions = upsertBy(assumptions.assumptions, 'id', { id: 'A-V8-OPERATIONS', status: 'requires_stakeholder_agreement', statement: 'The four-season civic year and 90-day S7 pilot are proposed operating protocols, not confirmed calendars, staffing commitments or permits.', impact: 'Phase dates, duty rosters, insurance, procurement, data governance and public representation must be agreed before field use.' });
write('assumptions.json', assumptions);

const sources = read('sources.json');
const sourceRecords = [
  { id: 'JINGZHANG-PARK-PHASE-1', publisher: '北京市园林绿化局（首都绿化委员会办公室）', date: '2023-06-26', source_type: 'official_public', url: 'https://yllhj.beijing.gov.cn/zwgk/zwxx/202306/t20230626_3145467.shtml', retrieved_at: '2026-08-18', license: 'Government public information; factual citation and attribution only', usage: 'Background for heritage protection, public-space stitching and the opened first phase.', limitations: 'Does not establish this proposal boundary, detailed station layout, ownership, controls or current performance.' },
  { id: 'JINGZHANG-PARK-PHASE-2', publisher: '北京市人民政府门户网站 / 海淀区人民政府', date: '2024-09-20', source_type: 'official_public', url: 'https://www.beijing.gov.cn/ywdt/gqrd/202409/t20240920_3902264.html', retrieved_at: '2026-08-18', license: 'Government public information; factual citation and attribution only', usage: 'Background for north-south continuity, east-west stitching, all-age public space and phased implementation.', limitations: 'Published planning and construction background only; no precise redline, station exit or implementation commitment for this concept.' },
  { id: 'ZHONGGUANCUN-CULTURE-HISTORY', publisher: '北京市人民政府门户网站 / 北京市海淀区委宣传部', date: '2020-12-11', source_type: 'official_public', url: 'https://www.beijing.gov.cn/renwen/sy/whkb/202012/t20201211_2162664.html', retrieved_at: '2026-08-18', license: 'Government public information; factual citation and attribution only', usage: 'Background for the memory-science-experiment-world narrative of Zhongguancun culture.', limitations: 'Does not authorise reuse of exhibition media, trademarks or imply collaboration with the museum.' },
  { id: 'DAZHONGSI-RAIL-CONTEXT', publisher: '北京市人民政府门户网站 / 北京市海淀区人民政府', date: '2022-10', source_type: 'official_public', url: 'https://www.beijing.gov.cn/hudong/gfxwjzj/qjzjxx/202210/P020221020368951317382.pdf', retrieved_at: '2026-08-18', license: 'Government public information; factual citation and attribution only', usage: 'Background evidence that the surface segment of Metro Line 13 includes Dazhongsi; used only for directional rail context.', limitations: 'Does not locate entrances, platforms, public-space boundaries, traffic demand or engineering conditions.' },
];
for (const record of sourceRecords) sources.sources = upsertBy(sources.sources, 'id', record);
write('sources.json', sources);

const compliance = read('compliance_matrix.json');
const agentEvidence = {
  'agent.1': { sections: ['三层范围工作框架', '总体设计范围城市更新与控规深度城市设计', '三座回执地标、文化里程与国际传播'], figures: ['assets/figures/site-overview.png', 'assets/figures/culture-brand.png'], metrics: ['receipt_landmark_count', 'east_west_stitch_count'], summary: 'V8 以“京张双答 / 三站一历”统一名称、四色情报、三座不同轮廓的回执地标和一脊三站两翼总图响应总体概念、视觉识别与功能统筹。' },
  'agent.2': { sections: ['统筹研究范围产业与未来城市研究', 'AI创新生态、人才画像与AI+场景'], figures: ['assets/figures/land-use-structure.png', 'assets/figures/ecosystem-synergy.png'], metrics: ['industry_test_count', 'annual_program_cycle_count'], summary: '七个国际案例各转译一种机制；问题、复现、转译、受控试验、城市回执和开放知识包把土地、人才、算力、数据、场景与服务翼连成可追踪生态。' },
  'agent.3': { sections: ['AI创新生态、人才画像与AI+场景'], figures: ['assets/figures/key-areas.png', 'assets/figures/persona-journeys.png'], metrics: ['paired_scenario_count', 'industry_test_count', 'stress_profile_count'], summary: '12 张双答场景、3 项产业测试和6类压力画像保持稳定ID；三项英雄场景落到平面、剖面、运营、人工责任、停止与恢复。' },
  'agent.4': { sections: ['重点区域详细设计', '三座回执地标、文化里程与国际传播'], figures: ['assets/figures/key-areas.png', 'assets/figures/culture-brand.png', 'assets/figures/mobility-bluegreen.png'], metrics: ['receipt_landmark_count', 'east_west_stitch_count'], summary: '验真环、共译门、回执廊是三座可辨认的AI公共地标；公共旁路、穿行大厅和公共十字先成立，公开荣誉只登记证据、贡献和人工决定。' },
  'agent.5': { sections: ['三座回执地标、文化里程与国际传播', '蓝绿空间、公共空间与城市风貌'], figures: ['assets/figures/culture-brand.png', 'assets/figures/site-overview.png'], metrics: ['receipt_landmark_count'], summary: '城市证据里程以京张铁路记忆、中关村公开实验、开源转译和城市回执形成文化序列，并提供双语、触觉、高对比和无智能手机入口。' },
  'agent.6': { sections: ['一带全球AI创新活动体系与长期运营设计', '更新项目清单、实施政策与分期计划'], figures: ['assets/figures/implementation-roadmap.png', 'assets/figures/metrics-evidence.png'], metrics: ['annual_program_cycle_count', 's7_pilot_phase_count', 'public_ledger_record_status'], summary: '春季基线审计、夏季开发者验真、秋季公众采纳、冬季退出复盘形成城市采纳年；S7另设90天试点、角色分离、许可门和知识归档。' },
};
compliance.requirements = compliance.requirements.map((item) => {
  const update = agentEvidence[item.requirement_id];
  if (!update) return item;
  return {
    ...item,
    report_sections: update.sections,
    drawings: unique(['drawings/a3-booklet.pdf', 'drawings/a0-boards.pdf', ...update.figures]),
    visual_sections: update.sections,
    metrics: unique(update.metrics),
    source_ids: unique([...(item.source_ids || []), 'AGENT-TASKBOOK', ...(item.requirement_id === 'agent.5' ? ['JINGZHANG-PARK-PHASE-1', 'JINGZHANG-PARK-PHASE-2', 'ZHONGGUANCUN-CULTURE-HISTORY'] : [])]),
    assumption_ids: unique([...(item.assumption_ids || []), 'A-V8-LANDMARKS', 'A-V8-OPERATIONS']),
    evidence_summary_zh: update.summary,
  };
});
delete compliance.v7_evidence_index;
compliance.v8_evidence_index = { version: 'V8', concept: 'Three Stations, One Civic Year', landmarks: 'LMK-01..03', annual_program: 'YEAR-SPRING..WINTER', pilot: 'S7-90D / P90-01..05', field_status: 'not_field_run' };
write('compliance_matrix.json', compliance);

const depth = read('design_depth_matrix.json');
depth.items = depth.items.map((item) => {
  const summaries = {
    overall_spatial_structure: '一脊、三站、两翼和六条缝合由三座回执地标及城市采纳年共同组织；总体图只表达概念结构，临时边界保持低对比披露。',
    three_key_area_detailed_design: '验真环、共译门和回执廊分别以旁路环、三路穿行厅和公共十字形成独立空间母题；S7继续提供四级尺度、四态运行和撤场恢复。',
    phasing_implementation: '0-36个月长期分期与S7九十天最小试点并行，分别登记进入门、输出、失败条件、主责角色和公共知识资产。',
    blue_green_public_space: '蓝绿永久基线与京张城市证据里程叠合，遮阴、饮水、雨水、照明、无障碍和文化标识不依赖AI运行。',
    metrics_recalculation: '新增3座地标、4季运营、5段试点和6项独立任务证据的可复算覆盖数；现场绩效和公共回执记录继续待现场建立。',
  };
  if (!summaries[item.item_id]) return item;
  return { ...item, evidence_summary_zh: summaries[item.item_id], metric_refs: unique([...(item.metric_refs || []), 'receipt_landmark_count', 'annual_program_cycle_count', 's7_pilot_phase_count']), assumption_ids: unique([...(item.assumption_ids || []), 'A-V8-LANDMARKS', 'A-V8-OPERATIONS']) };
});
delete depth.v7_evidence_index;
depth.v8_evidence_index = compliance.v8_evidence_index;
write('design_depth_matrix.json', depth);

const standards = read('standard_matrix.json');
standards.standards = standards.standards.map((item) => item.standard_id === 'PROJECT-AGENT-OPEN-CALL-TASKBOOK' ? {
  ...item,
  drawing_refs: unique([...(item.drawing_refs || []), 'assets/figures/culture-brand.png', 'assets/figures/ecosystem-synergy.png', 'assets/figures/implementation-roadmap.png']),
  metric_refs: unique([...(item.metric_refs || []), 'receipt_landmark_count', 'annual_program_cycle_count', 's7_pilot_phase_count', 'agent_task_unique_evidence_count']),
  assumption_ids: unique([...(item.assumption_ids || []), 'A-V8-LANDMARKS', 'A-V8-OPERATIONS']),
  evidence_summary_zh: 'V8 为Agent 1-6建立六条独立正文、图件、指标与数据证据链，并以三座回执地标、文化里程、四季运营和90天试点补齐公共空间、文化与长期运营要求。',
} : item);
delete standards.v7_evidence_index;
standards.v8_evidence_index = compliance.v8_evidence_index;
write('standard_matrix.json', standards);

const risk = read('risk.json');
risk.version = 'V8';
risk.summary = 'V8 保持公共基线、人工决定和可逆退出，同时把三座回执地标、四季活动和90天试点标为概念协议；公开资料不支持的站口、建筑、机构承诺、报价和现场绩效继续待补。';
risk.v8_operating_rule = 'baseline_first + landmark_as_public_interface + seasonal_entry_gate + role_separation + public_ledger + adopt_revise_stop';
write('risk.json', risk);

const redPath = 'visual/assets/red-team-review.json';
const red = read(redPath);
red.schema_version = '1.6.0';
red.review_date = '2026-08-18';
red.version = 'V8';
red.calibration_baseline = 'PR #3225 Review Agent 86/100';
red.status = 'v8_implementation_in_progress';
red.findings = red.findings.filter((item) => !String(item.id).startsWith('V8-'));
red.findings.push(
  { id: 'V8-BRIEF-01', round: 'brief_alignment', severity: 'major', finding: 'V7 agent.4-agent.6 reused generic evidence and did not independently establish landmarks, culture, developer activity or annual operation.', evidence: ['proposal keyword audit', 'compliance_matrix agent.1-agent.6 comparison'], remediation: 'Create three receipt landmarks, civic evidence mile, four-season program and unique task evidence.', verification: 'Pending rendered and bilingual review.', status: 'open' },
  { id: 'V8-VIS-01', round: 'entry_evidence', severity: 'major', finding: 'V7 core figures repeated the same cross plan and two optional figures had identical hashes.', evidence: ['18-image V7 comparison', 'culture-brand/ecosystem-synergy SHA-256 equality'], remediation: 'Assign one unique question to each core figure and prohibit semantic duplicates.', verification: 'Pending V8 figure hash and visual review.', status: 'open' },
  { id: 'V8-IMP-01', round: 'implementation_feasibility', severity: 'major', finding: 'V7 had quantities but no compact pilot sequence connecting site verification, baseline, trial, recovery and public receipt.', evidence: ['V7 proposal and implementation figure'], remediation: 'Publish five-gate 90-day S7 protocol with role separation.', verification: 'Pending publication and reference-integrity QA.', status: 'open' },
  { id: 'V8-DATA-01', round: 'external_context', severity: 'minor', finding: 'Official station exits, surveyed buildings, ownership, utilities and field performance remain unavailable.', evidence: ['site package missing-data list', 'OSM context completeness note'], remediation: 'Keep directional context and concept assumptions explicit; verify before E2.', verification: 'External dependency remains open.', status: 'open_external_dependency' },
);
red.summary = { blocking_open: 0, major_open: red.findings.filter((item) => item.severity === 'major' && item.status === 'open').length, major_closed: red.findings.filter((item) => item.severity === 'major' && item.status === 'closed').length, minor_open: red.findings.filter((item) => item.severity === 'minor' && String(item.status).startsWith('open')).length };
red.note = 'V8 major findings remain open until bilingual figures, PDFs, HTML and reference checks are rendered and independently inspected.';
write(redPath, red);

console.log(JSON.stringify({ schema: '1.6.0', landmarks: landmarks.length, annual_cycles: annualProgram.length, pilot_phases: pilotProtocol.phases.length, task_evidence: Object.keys(agentEvidence).length }, null, 2));
