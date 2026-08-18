const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const GEO = path.join(ROOT, 'geometry');
const read = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));
const write = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
const bilingual = (zh, en) => ({ zh, en });
const centre = [116.3490, 39.9570];
const lngPerMetre = 1 / (111320 * Math.cos(centre[1] * Math.PI / 180));
const latPerMetre = 1 / 110540;
const wgs = ([x, y]) => [
  Number((centre[0] + x * lngPerMetre).toFixed(7)),
  Number((centre[1] + y * latPerMetre).toFixed(7)),
];
const close = (points) => [...points, points[0]];

const common = (id, layer, extra = {}) => ({
  id,
  layer,
  source_type: 'agent_generated_design',
  confidence: 'low',
  geometry_role: 'design_proposal',
  status: 'concept_proposal',
  station: 'dazhongsi',
  evidence_level: 'E1_concept_design',
  dimension_basis: 'prototype_design_assumption_pending_survey',
  ...extra,
});
const line = (id, points, extra = {}) => ({
  type: 'Feature', id,
  properties: common(id, 'ROAD_CENTERLINE', extra),
  geometry: { type: 'LineString', coordinates: points.map(wgs) },
});
const polygon = (id, points, extra = {}) => ({
  type: 'Feature', id,
  properties: common(id, 'PUBLIC_SPACE', extra),
  geometry: { type: 'Polygon', coordinates: [close(points).map(wgs)] },
});
const building = (id, points, extra = {}) => ({
  type: 'Feature', id,
  properties: common(id, 'BUILDING_FOOTPRINT', {
    retain_renovate_demolish_status: 'concept_adaptive_reuse_or_reversible_structure',
    ...extra,
  }),
  geometry: { type: 'Polygon', coordinates: [close(points).map(wgs)] },
});
const point = (id, xy, extra = {}) => ({
  type: 'Feature', id,
  properties: common(id, 'REGULATORY_CONTROL', extra),
  geometry: { type: 'Point', coordinates: wgs(xy) },
});

// All coordinates below are local-metre prototype assumptions. They are not surveyed site facts.
const localDesign = {
  extent_m: [-96, -86, 96, 94],
  scale_note: bilingual('原型设计假设，待测绘、站口、道路红线和交通组织复核', 'Prototype design assumption pending survey, station-exit, road-line and traffic verification'),
  routes: [
    { id: 'V6-D-BASE-NS', role: 'baseline', width_m: 4.0, points: [[0,-86],[0,-14],[-4,-4],[0,14],[0,94]] },
    { id: 'V6-D-BASE-EW', role: 'baseline', width_m: 4.0, points: [[-96,0],[-16,0],[-4,4],[16,0],[96,0]] },
    { id: 'V6-D-CROSS-N', role: 'crossing', width_m: 4.0, points: [[-12,14],[12,14]] },
    { id: 'V6-D-CROSS-S', role: 'crossing', width_m: 4.0, points: [[-12,-14],[12,-14]] },
    { id: 'V6-D-TRANSIT', role: 'conventional_transit', width_m: 6.0, points: [[-82,56],[-18,56],[18,56],[82,56]] },
    { id: 'V6-D-EMERGENCY', role: 'emergency', width_m: 4.0, points: [[24,-30],[73,-30],[91,-8]] },
    { id: 'V6-D-REMOVAL', role: 'removal', width_m: 4.0, points: [[48,-68],[96,-68]] },
    { id: 'V6-D-FIRE', role: 'fire_access', width_m: 4.0, points: [[-92,76],[-42,76],[-20,56]] },
    { id: 'V6-D-CURB-N', role: 'curb_edge', width_m: 0.15, points: [[-82,48],[82,48]] },
    { id: 'V6-D-CURB-S', role: 'curb_edge', width_m: 0.15, points: [[-82,64],[82,64]] },
  ],
  spaces: [
    { id: 'V6-D-FORECOURT', role: 'conventional_forecourt', points: [[-82,14],[82,14],[82,76],[-82,76]] },
    { id: 'V6-D-PLATFORM', role: 'conventional_platform', points: [[-76,46],[76,46],[76,66],[-76,66]] },
    { id: 'V6-D-TRIAL', role: 'ai_trial', points: [[26,-70],[78,-70],[78,-24],[26,-24]] },
    { id: 'V6-D-BUFFER', role: 'safety_buffer', points: [[20,-76],[84,-76],[84,-18],[20,-18]] },
    { id: 'V6-D-EVIDENCE', role: 'evidence_square', points: [[-78,-70],[-22,-70],[-22,-20],[-78,-20]] },
    { id: 'V6-D-EGRESS', role: 'evacuation_apron', points: [[-18,-18],[18,-18],[18,18],[-18,18]] },
    { id: 'V6-D-RAIN-W', role: 'rain_garden', points: [[-88,20],[-80,20],[-80,72],[-88,72]] },
    { id: 'V6-D-RAIN-E', role: 'rain_garden', points: [[80,20],[88,20],[88,72],[80,72]] },
    { id: 'V6-D-SHADE-NW', role: 'shade_rest', points: [[-72,22],[-28,22],[-28,42],[-72,42]] },
    { id: 'V6-D-RESTORE', role: 'retired_public_use', points: [[26,-70],[78,-70],[78,-24],[26,-24]] },
  ],
  buildings: [
    { id: 'V6-D-SERVICE', role: 'staffed_public_service', points: [[-70,24],[-42,24],[-42,40],[-70,40]] },
    { id: 'V6-D-CONTROL', role: 'trial_control', points: [[58,-16],[76,-16],[76,-2],[58,-2]] },
    { id: 'V6-D-EVIDENCE-WALL', role: 'public_evidence_interface', points: [[-74,-64],[-26,-64],[-26,-59],[-74,-59]] },
  ],
  points: [
    ['V6-D-ENT-N',[0,94],'directional_entrance'], ['V6-D-ENT-E',[96,0],'directional_entrance'],
    ['V6-D-ENT-S',[0,-86],'directional_entrance'], ['V6-D-ENT-W',[-96,0],'directional_entrance'],
    ['V6-D-STAFF-BASE',[-48,32],'baseline_staff_position'], ['V6-D-STAFF-TRIAL',[25,-30],'trial_staff_position'],
    ['V6-D-ESTOP-01',[29,-28],'emergency_stop'], ['V6-D-ESTOP-02',[75,-28],'emergency_stop'],
    ['V6-D-UTILITY',[76,-68],'isolated_utility_interface'], ['V6-D-FIRE-GATE',[-92,76],'fire_access_gate'],
    ['V6-D-APPEAL',[-72,-62],'appeal_and_exit_notice'], ['V6-D-WATER',[-32,32],'drinking_water'],
    ['V6-D-LIGHT-01',[-74,18],'lighting'], ['V6-D-LIGHT-02',[-24,18],'lighting'],
    ['V6-D-LIGHT-03',[24,18],'lighting'], ['V6-D-LIGHT-04',[74,18],'lighting'],
    ['V6-D-LIGHT-05',[-18,-70],'lighting'], ['V6-D-LIGHT-06',[84,-70],'lighting'],
  ].map(([id, xy, role]) => ({ id, xy, role })),
  states: {
    OPEN: ['V6-D-BASE-NS','V6-D-BASE-EW','V6-D-CROSS-N','V6-D-CROSS-S','V6-D-TRANSIT','V6-D-FORECOURT','V6-D-PLATFORM','V6-D-SERVICE'],
    TRIAL: ['V6-D-TRIAL','V6-D-BUFFER','V6-D-CONTROL','V6-D-STAFF-TRIAL','V6-D-ESTOP-01','V6-D-ESTOP-02'],
    PAUSE: ['V6-D-EMERGENCY','V6-D-EGRESS','V6-D-STAFF-BASE','V6-D-APPEAL'],
    RETIRE: ['V6-D-REMOVAL','V6-D-RESTORE','V6-D-EVIDENCE','V6-D-EVIDENCE-WALL'],
  },
};

const roads = read(path.join(GEO, 'roads.geojson'));
const spaces = read(path.join(GEO, 'public_space.geojson'));
const buildings = read(path.join(GEO, 'buildings.geojson'));
const constraints = read(path.join(GEO, 'constraints.geojson'));
[roads, spaces, buildings, constraints].forEach((collection) => {
  collection.features = collection.features.filter((feature) => !String(feature.id || feature.properties?.id).startsWith('V6-D-'));
});
roads.features.push(...localDesign.routes.map((r) => line(r.id, r.points, {
  route_role: r.role, design_width_m: r.width_m,
  name_zh: r.role, name_en: r.role.replaceAll('_', ' '),
})));
spaces.features.push(...localDesign.spaces.map((s) => polygon(s.id, s.points, {
  space_role: s.role, name_zh: s.role, name_en: s.role.replaceAll('_', ' '),
})));
buildings.features.push(...localDesign.buildings.map((b) => building(b.id, b.points, {
  building_type: b.role === 'trial_control' ? 'mobility_hub' : 'community_service',
  building_role: b.role, name_zh: b.role, name_en: b.role.replaceAll('_', ' '),
})));
constraints.features.push(...localDesign.points.map((p) => point(p.id, p.xy, {
  point_role: p.role, name_zh: p.role, name_en: p.role.replaceAll('_', ' '),
})));
write(path.join(GEO, 'roads.geojson'), roads);
write(path.join(GEO, 'public_space.geojson'), spaces);
write(path.join(GEO, 'buildings.geojson'), buildings);
write(path.join(GEO, 'constraints.geojson'), constraints);

const atlasPath = path.join(__dirname, 'spatial-atlas.json');
const atlas = read(atlasPath);
atlas.schema_version = '1.4.0';
atlas.publication_version = 'V6';
atlas.subtitle = bilingual('大钟寺城市采纳样板：公共路线不可牺牲', 'Dazhongsi Civic Adoption Sample: the public route is non-negotiable');
atlas.dimension_basis = 'prototype_design_assumption_pending_survey';
atlas.stations = atlas.stations.map((item) => item.id === 'dazhongsi' ? {
  ...item,
  flagship_weight: 0.6,
  local_design: localDesign,
  city_scale: '1:5000', plan_scale: '1:2000', detail_scale: '1:500', section_scale: '1:200',
  dimension_basis: localDesign.scale_note,
  interface_geometry_refs: localDesign.routes.filter((x) => ['curb_edge','crossing','conventional_transit'].includes(x.role)).map((x) => x.id),
  baseline_route_geometry: ['V6-D-BASE-NS','V6-D-BASE-EW','V6-D-CROSS-N','V6-D-CROSS-S'],
  trial_boundary_geometry: ['V6-D-TRIAL','V6-D-BUFFER'],
  human_post_geometry: ['V6-D-STAFF-BASE','V6-D-STAFF-TRIAL','V6-D-ESTOP-01','V6-D-ESTOP-02'],
  emergency_route_geometry: ['V6-D-EMERGENCY','V6-D-FIRE','V6-D-EGRESS'],
  state_views: localDesign.states,
  geometry_refs: [
    ...localDesign.routes.map((x) => x.id), ...localDesign.spaces.map((x) => x.id),
    ...localDesign.buildings.map((x) => x.id), ...localDesign.points.map((x) => x.id),
  ],
} : { ...item, flagship_weight: 0.2 });
write(atlasPath, atlas);

const scenariosPath = path.join(__dirname, 'two-answers.json');
const scenarios = read(scenariosPath);
scenarios.schema_version = '1.4.0';
scenarios.publication_version = 'V6';
scenarios.title = bilingual('京张双答：大钟寺城市采纳样板', 'Jing-Zhang Two Answers: Dazhongsi Civic Adoption Sample');
scenarios.status_note = bilingual('当前为 E1 概念设计，S7 未现场运行，回执结论保持待定。', 'Current status is E1 concept design; S7 is not field-run and the receipt decision remains pending.');
scenarios.scenarios = scenarios.scenarios.map((item) => {
  const isS7 = item.id === 'SCN-010';
  const defaultRoute = Array.isArray(item.baseline_route_geometry) ? item.baseline_route_geometry : [item.baseline_route_ref].filter(Boolean);
  return {
    ...item,
    dimension_basis: 'prototype_design_assumption_pending_survey',
    interface_geometry_refs: isS7 ? ['V6-D-CURB-N','V6-D-CURB-S','V6-D-CROSS-N','V6-D-CROSS-S','V6-D-TRANSIT'] : (item.interface_geometry_refs || []),
    baseline_route_geometry: isS7 ? ['V6-D-BASE-NS','V6-D-BASE-EW','V6-D-CROSS-N','V6-D-CROSS-S'] : defaultRoute,
    trial_boundary_geometry: isS7 ? ['V6-D-TRIAL','V6-D-BUFFER'] : (item.trial_boundary_geometry || []),
    human_post_geometry: isS7 ? ['V6-D-STAFF-BASE','V6-D-STAFF-TRIAL','V6-D-ESTOP-01','V6-D-ESTOP-02'] : (item.human_post_geometry || []),
    emergency_route_geometry: isS7 ? ['V6-D-EMERGENCY','V6-D-FIRE','V6-D-EGRESS'] : [item.emergency_route_ref].filter(Boolean),
    state_views: isS7 ? localDesign.states : (item.state_views || {}),
    measurement_denominator: isS7 ? bilingual('每种模式下连续记录 100 次符合准入条件的接驳通行；同时保留全部严重事件记录', 'Record 100 eligible interchange passages in each mode; retain every severe-event record') : bilingual('E2 前由场景运营者登记同题分母', 'Operator registers the same-task denominator before E2'),
    baseline_window: isS7 ? bilingual('E2 原型后连续 7 个运行日，分层记录高峰/平峰、昼/夜、天气和辅助需求', 'Seven consecutive operating days after the E2 prototype, stratified by peak/off-peak, day/night, weather and assistance needs') : bilingual('E2 原型后建立', 'Established after the E2 prototype'),
    zero_tolerance_events: isS7 ? [
      'collision_or_person_in_safety_buffer', 'emergency_stop_failure',
      'baseline_route_blocked_or_accessibility_regressed', 'human_takeover_timeout',
    ] : [item.stop_conditions],
    recovery_protocol: isS7 ? bilingual('立即停机并关闭试验边界；人工完成当前任务；开放两条普通路线；记录事件；设备经撤场线移出；委员会复核后方可重新申请 TRIAL。', 'Stop and close the trial boundary; staff complete the current task; reopen both baseline routes; log the event; remove equipment via the removal route; only the committee may authorise a new TRIAL application.') : item.exit_and_restore,
    receipt_state: isS7 ? 'E1_FLAGSHIP_READY_E2_PENDING' : item.receipt_state,
  };
});
write(scenariosPath, scenarios);

const metricsPath = path.join(ROOT, 'metrics.json');
const metrics = read(metricsPath);
const v6Count = localDesign.routes.length + localDesign.spaces.length + localDesign.buildings.length + localDesign.points.length;
metrics.metrics.s7_traceable_spatial_object_count = {
  status: 'known', value: v6Count, unit: 'count',
  source_files: ['geometry/roads.geojson','geometry/public_space.geojson','geometry/buildings.geojson','geometry/constraints.geojson'],
  formula: 'count(features where id starts with V6-D-)', confidence: 'high', assumptions: ['A-SPATIAL-ATLAS-001'],
};
metrics.metrics.s7_review_scale_count = {
  status: 'known', value: 4, unit: 'count', source_files: ['visual/assets/spatial-atlas.json'],
  formula: 'count(1:5000, 1:2000, 1:500, 1:200 review scales)', confidence: 'high', assumptions: ['A-SPATIAL-ATLAS-001'],
};
metrics.metrics.s7_baseline_sample_status = {
  status: 'unknown', value: null, unit: 'eligible_passages', source_files: ['visual/assets/two-answers.json'],
  formula: '100 eligible passages per mode after E2 baseline prototype', confidence: 'unknown', assumptions: ['A-METRICS-001'],
  reason: 'S7 has not been field-run; the denominator and stratification protocol are designed but no observations exist.',
};
write(metricsPath, metrics);

const assumptionsPath = path.join(ROOT, 'assumptions.json');
const assumptions = read(assumptionsPath);
if (!assumptions.assumptions.some((x) => x.id === 'A-V6-S7-DIMENSIONS')) assumptions.assumptions.push({
  id: 'A-V6-S7-DIMENSIONS',
  statement: 'S7 local-metre dimensions, entrance directions, curb lines, transit interface and operating zones are prototype design assumptions, not surveyed existing conditions.',
  impact: 'All four scales and any engineering dimension require survey, official station-exit information, road-line, utility, fire and traffic verification before E2.',
  verification_method: 'Licensed survey plus asset-owner, transit, accessibility, fire and traffic-management review.',
  status: 'open',
});
write(assumptionsPath, assumptions);

const redPath = path.join(__dirname, 'red-team-review.json');
const red = read(redPath);
red.schema_version = '1.3.0';
red.review_date = '2026-08-17';
red.version = 'V6';
red.calibration_baseline = 'PR #3071 Review Agent 81/100';
red.status = 'major_open_pending_blind_visual_review';
red.findings = red.findings.map((finding) => finding.id === 'V5-UD-01' ? {
  ...finding,
  id: 'V6-UD-01',
  severity: 'major',
  finding: 'V5 used geometry count and legends as a proxy for visible urban-design specificity; a blind reviewer could not locate curbs, crossings, staffed posts, fire access and restoration without reading the legend.',
  evidence: ['PR #3071 Review Agent remained 81/100', 'V5 canonical key-areas and PDF first-page review'],
  remediation: 'Rebuild S7 as the flagship four-scale sample from shared local-metre objects and surface it in every Review Agent entry point.',
  verification: 'Pending: label-off blind review of canonical figures, A0 first board, A3 cover and visual first screen.',
  status: 'open',
} : finding);
red.summary = {
  blocking_open: 0,
  major_open: red.findings.filter((x) => x.severity === 'major' && x.status === 'open').length,
  major_closed: red.findings.filter((x) => x.severity === 'major' && x.status === 'closed').length,
  minor_open: red.findings.filter((x) => x.severity === 'minor' && String(x.status).startsWith('open')).length,
};
red.note = 'V6 does not close spatial depth by counting objects. Closure requires blind visual identification plus four-scale traceability.';
write(redPath, red);

console.log(`V6 data enriched: ${v6Count} S7 objects, schema 1.4.0, spatial major reopened`);
