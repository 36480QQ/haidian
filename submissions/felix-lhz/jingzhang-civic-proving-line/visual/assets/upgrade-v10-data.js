const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const read = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));
const write = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);

const twoPath = path.join(__dirname, 'two-answers.json');
const atlasPath = path.join(__dirname, 'spatial-atlas.json');
const metricsPath = path.join(ROOT, 'metrics.json');
const assumptionsPath = path.join(ROOT, 'assumptions.json');
const changelogPath = path.join(ROOT, 'changelog.md');
const compliancePath = path.join(ROOT, 'compliance_matrix.json');
const readinessPath = path.join(__dirname, 'e2-readiness.json');

const two = read(twoPath);
two.schema_version = '1.8.0';
two.publication_version = 'V10';
two.subtitle = {
  zh: '城市采纳编译器：把每项 AI 空间方案编译为完整公共路线、可触发停止机制和可复核回执。',
  en: 'Civic Adoption Compiler: compile every AI spatial proposal into a complete public route, triggerable stop mechanism and reviewable receipt.',
};
two.verification_scope = {
  status: 'T0_synthetic_contract_verified',
  result_ref: 'visual/assets/v10-tabletop-results.json',
  rule_ref: 'visual/assets/run-v10-tabletop.js',
  case_count: 84,
  field_status: 'not_field_run',
};
two.scenarios = two.scenarios.map((scene) => {
  const isS7 = scene.code === 'S7';
  const isHeroConcept = scene.code === 'T2' || scene.code === 'S2';
  return {
    ...scene,
    verification_scope: 'synthetic_design_contract_only',
    test_case_ids: Array.from({ length: 7 }, (_, index) => `${scene.id}-T${String(index + 1).padStart(2, '0')}`),
    initial_state: 'OPEN',
    injected_event: 'see_v10_tabletop_results',
    expected_state: 'see_v10_tabletop_results',
    observed_state: 'see_v10_tabletop_results',
    invariants_checked: [
      'baseline_route_continuous',
      'permit_gate_before_trial',
      'accountable_human_before_trial',
      'zero_tolerance_stops_trial',
      'recovery_before_reopen',
      'retirement_restores_public_use',
    ],
    synthetic_result: 'pass',
    input_hash: 'resolved_per_test_case',
    recovery_exit: scene.exit_and_restore,
    field_status: 'not_field_run',
    prototype_readiness: isS7 ? 'E2_documented_prototype_ready' : (isHeroConcept ? 'E1_concept_design' : 'E1_catalogue_trace_complete'),
    e2_status: isS7 ? 'E2_documented_prototype_ready' : 'not_built',
  };
});
write(twoPath, two);

const atlas = read(atlasPath);
atlas.schema_version = '1.8.0';
atlas.publication_version = 'V10';
atlas.subtitle = two.subtitle;
atlas.verification_scope = two.verification_scope;
atlas.prototype_status = {
  S7: 'E2_documented_prototype_ready',
  T2: 'E1_concept_design',
  S2: 'E1_concept_design',
  tabletop: 'T0_synthetic_contract_verified',
  field: 'not_field_run',
};
atlas.s7_detail_scales = [
  { id: 'S7-CITY-5000', scale: '1:5000', purpose: 'city_interface' },
  { id: 'S7-PLAN-2000', scale: '1:2000', purpose: 'public_route_and_trial_occupancy' },
  { id: 'S7-DETAIL-500', scale: '1:500', purpose: 'curb_tactile_tree_rainwater_stop_fire_removal' },
  { id: 'S7-SECTION-200', scale: '1:200', purpose: 'route_buffer_trial_edge_section' },
  { id: 'S7-NODE-050', scale: '1:50', purpose: 'ramp_tactile_barrier_evidence_power_rainwater_node' },
];
write(atlasPath, atlas);

const readiness = read(readinessPath);
readiness.schema_version = '1.8.0';
readiness.dataset_id = 'jingzhang-v10-e2-readiness';
readiness.title = { zh: 'V10 S7 E2 文件就绪包', en: 'V10 S7 E2 Documented Prototype Pack' };
readiness.prototype_readiness = 'E2_documented_prototype_ready';
readiness.synthetic_verification = {
  status: 'T0_synthetic_contract_verified',
  case_count: 84,
  result_ref: 'visual/assets/v10-tabletop-results.json',
  field_status: 'not_field_run',
};
write(readinessPath, readiness);

const metrics = read(metricsPath);
metrics.metrics.synthetic_design_verification_case_count = {
  status: 'known', value: 84, unit: 'count',
  source_files: ['visual/assets/v10-tabletop-results.json'],
  formula: 'count(12 scenarios × 7 deterministic design-contract cases)',
  confidence: 'high', assumptions: ['ASM-V10-SYNTHETIC'],
};
metrics.metrics.synthetic_design_verification_pass_count = {
  status: 'known', value: 84, unit: 'count',
  source_files: ['visual/assets/v10-tabletop-results.json'],
  formula: 'count(test where synthetic_result=pass)',
  confidence: 'high', assumptions: ['ASM-V10-SYNTHETIC'],
};
metrics.metrics.synthetic_design_verification_scenario_count = {
  status: 'known', value: 12, unit: 'count',
  source_files: ['visual/assets/v10-tabletop-results.json'],
  formula: 'count(distinct scene_id)',
  confidence: 'high', assumptions: ['ASM-V10-SYNTHETIC'],
};
metrics.metrics.field_verification_result_count = {
  status: 'known', value: 0, unit: 'count',
  source_files: ['visual/assets/v10-tabletop-results.json'],
  formula: 'count(records where field_status is a completed field result)',
  confidence: 'high', assumptions: ['ASM-V10-SYNTHETIC'],
};
write(metricsPath, metrics);

const assumptions = read(assumptionsPath);
assumptions.assumptions = assumptions.assumptions.filter((item) => item.id !== 'ASM-V10-SYNTHETIC');
assumptions.assumptions.push({
  id: 'ASM-V10-SYNTHETIC',
  status: 'synthetic_design_verification_only',
  statement: {
    zh: '84 项确定性桌面演练只验证规则、状态跃迁、准入、停止、恢复和退役契约自洽，不是现场仿真、公众测试或安全认证。',
    en: 'The 84 deterministic tabletop cases verify only rule, transition, admission, stop, recovery and retirement consistency; they are not field simulation, public testing or safety certification.',
  },
  impact: {
    zh: '客流、效率、安全表现、满意度、能耗、成本和恢复时长继续保持现场未知。',
    en: 'Flow, efficiency, safety performance, satisfaction, energy, cost and recovery duration remain field unknowns.',
  },
});
write(assumptionsPath, assumptions);

const compliance = read(compliancePath);
const agentEvidence = {
  'agent.1': {
    geojson_layers: ['geometry/site_boundary.geojson', 'geometry/key_areas.geojson', 'geometry/roads.geojson', 'geometry/public_space.geojson'],
    metrics: ['receipt_landmark_count', 'east_west_stitch_count'],
  },
  'agent.2': {
    geojson_layers: ['geometry/land_use.geojson', 'geometry/buildings.geojson', 'geometry/constraints.geojson'],
    metrics: ['industry_test_count', 'annual_program_cycle_count'],
  },
  'agent.3': {
    geojson_layers: ['geometry/constraints.geojson', 'geometry/roads.geojson', 'geometry/public_space.geojson'],
    metrics: ['paired_scenario_count', 'industry_test_count', 'stress_profile_count', 'synthetic_design_verification_case_count', 'synthetic_design_verification_pass_count'],
    evidence_summary_zh: '12 个双答场景、3 项产业测试和 6 类压力画像保持稳定 ID；84 项确定性桌面演练逐场景验证普通基线、准入、停止、人工恢复和设备退役，结果明确为合成设计验证而非现场绩效。',
  },
  'agent.4': {
    geojson_layers: ['geometry/key_areas.geojson', 'geometry/buildings.geojson', 'geometry/roads.geojson', 'geometry/public_space.geojson'],
    metrics: ['receipt_landmark_count', 'east_west_stitch_count'],
  },
  'agent.5': {
    geojson_layers: ['geometry/roads.geojson', 'geometry/green_space.geojson', 'geometry/public_space.geojson'],
    metrics: ['receipt_landmark_count'],
  },
  'agent.6': {
    geojson_layers: ['geometry/phasing.geojson', 'geometry/public_space.geojson', 'geometry/constraints.geojson'],
    metrics: ['annual_program_cycle_count', 's7_pilot_phase_count', 'public_ledger_record_status', 'field_verification_result_count'],
  },
};
for (const item of compliance.requirements) {
  if (!agentEvidence[item.requirement_id]) continue;
  Object.assign(item, agentEvidence[item.requirement_id]);
}
if (compliance.metadata) compliance.metadata.version = 'V10';
write(compliancePath, compliance);

let changelog = fs.readFileSync(changelogPath, 'utf8');
if (!changelog.includes('## V10 · 城市采纳编译器')) {
  changelog = changelog.replace('# 方案迭代记录\n', `# 方案迭代记录\n\n## V10 · 城市采纳编译器\n\n- 对 12 个场景各运行 7 类规则驱动用例，共 84 项确定性桌面演练；非法跃迁、许可/岗位缺失、公共服务退化、零容忍事件和现场未知冒充已知都会阻断构建。\n- 统一状态为 S7 \`E2_documented_prototype_ready\`、T2/S2 \`E1_concept_design\`、桌面演练 \`T0_synthetic_contract_verified\`、现场 \`not_field_run\`。\n- 新增 S7 1:50 装配节点接口，并把“已知设计 / 合成验证 / 现场未知”写入 Review Agent 可直接读取的正文与指标。\n\n`);
  fs.writeFileSync(changelogPath, changelog);
}

console.log('V10 data interfaces upgraded to schema 1.8.0');
