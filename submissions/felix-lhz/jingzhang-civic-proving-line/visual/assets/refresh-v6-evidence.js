const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..', '..');
const read = (name) => JSON.parse(fs.readFileSync(path.join(root, name), 'utf8'));
const write = (name, value) => fs.writeFileSync(path.join(root, name), `${JSON.stringify(value, null, 2)}\n`);

const depth = read('design_depth_matrix.json');
const depthUpdates = {
  traffic_rail_slow_parking: {
    geometry_refs: ['geometry/roads.geojson#V6-D-BASE-NS','geometry/roads.geojson#V6-D-BASE-EW','geometry/roads.geojson#V6-D-TRANSIT','geometry/roads.geojson#V6-D-EMERGENCY'],
    metric_refs: ['s7_review_scale_count','s7_baseline_sample_status'],
    evidence_summary_zh: 'S7 旗舰样板把两条连续公共路线、两处过街、常规接驳、独立低速湾、疏散和撤场画在同一四级尺度证据链中；方向和尺寸均为待测绘复核的概念建议。',
  },
  blue_green_public_space: {
    geometry_refs: ['geometry/public_space.geojson#V6-D-RAIN-W','geometry/public_space.geojson#V6-D-RAIN-E','geometry/public_space.geojson#V6-D-SHADE-NW','geometry/public_space.geojson#V6-D-EVIDENCE'],
    evidence_summary_zh: '大钟寺前场将雨水花园、遮阴休息、证据广场和四象限公共路线作为永久基线；AI 试验停机或撤场后仍完整。',
  },
  three_key_area_detailed_design: {
    drawing_refs: ['assets/figures/key-areas.png','assets/figures/hero-s7-detail.png','assets/figures/hero-s7-section.png','drawings/a0-boards.pdf#page=2','drawings/a3-booklet.pdf#page=13'],
    geometry_refs: ['geometry/roads.geojson#V6-D-BASE-NS','geometry/public_space.geojson#V6-D-TRIAL','geometry/buildings.geojson#V6-D-SERVICE','geometry/constraints.geojson#V6-D-STAFF-TRIAL'],
    metric_refs: ['s7_traceable_spatial_object_count','s7_review_scale_count','s7_baseline_sample_status'],
    assumption_ids: ['A-SPATIAL-ATLAS-001','A-V6-S7-DIMENSIONS'],
    evidence_summary_zh: 'S7 作为 60% 深化资源的旗舰样板完成 1:5000/1:2000/1:500/1:200、四态运行、RACI、双急停、消防与还场；T2/S2 保留差异化安全和公共服务对照。',
  },
  phasing_implementation: {
    metric_refs: ['field_performance_status','s7_baseline_sample_status'],
    evidence_summary_zh: '四阶段以进入条件、输出物和失败条件控制；S7 必须在 E2 建立普通基线并完成许可矩阵，才可进入 E3 受控试验。',
  },
  metrics_recalculation: {
    metric_refs: ['s7_traceable_spatial_object_count','s7_review_scale_count','s7_baseline_sample_status','field_performance_status'],
    evidence_summary_zh: '仅复算设计对象与审查尺度；100 次通行分母、7 日窗口和分层方法已登记，但现场样本、成效与采用结论保持 unknown。',
  },
};
depth.items = depth.items.map((item) => ({ ...item, ...(depthUpdates[item.item_id] || {}) }));
depth.v6_evidence_index = {
  version: 'V6',
  flagship: 'S7 Dazhongsi / A0-02 / A3 pp.13-14 / assets/figures/key-areas.png',
  four_scales: '1:5000 city / 1:2000 plan / 1:500 detail / 1:200 section',
  state_trace: 'OPEN / TRIAL / PAUSE / RETIRE',
  field_status: 'not_field_run; no outcome or adoption claim',
};
write('design_depth_matrix.json', depth);

const compliance = read('compliance_matrix.json');
const cUpdates = {
  '1.5.2.3': 'S7 以常规交通优先、两条公共路线、独立试验湾、消防/疏散/撤场和四态运营回应交通、轨道与新型设施组织；尺寸与站口方向待专业复核。',
  '1.5.3.required': '三处均保留详细设计证据，S7 作为旗舰完成四级尺度、可见城市界面、RACI、许可、测量分母和恢复程序。',
  '1.5.3.3': '大钟寺以常规接驳前场、四象限公共路线、独立低速湾、雨水花园、证据广场和可恢复普通用途形成旗舰城市采用样板。',
  'agent.3': '十二项场景保持可复制契约；S7 将同题比较、100 次通行分母、7 日基线窗口、零容忍停止与人工决定落实到真实空间对象。',
  'agent.4': '公共路线、遮阴休息、服务亭和证据广场先成立；AI 试验湾独立、限时、可停、可拆，并有明确还场用途。',
  'agent.6': '场地资产、普通服务、AI、安全、数据和公众代表的 RACI 与四态运营相连，许可未齐不得从 OPEN 进入 TRIAL。',
};
compliance.requirements = compliance.requirements.map((item) => {
  if (!cUpdates[item.requirement_id]) return item;
  const next = { ...item, evidence_summary_zh: cUpdates[item.requirement_id] };
  next.drawings = Array.from(new Set([...(item.drawings || []),'assets/figures/key-areas.png','assets/figures/metrics-evidence.png']));
  next.metrics = Array.from(new Set([...(item.metrics || []),'s7_review_scale_count','s7_baseline_sample_status']));
  return next;
});
compliance.v6_evidence_index = depth.v6_evidence_index;
write('compliance_matrix.json', compliance);

const standards = read('standard_matrix.json');
standards.standards = standards.standards.map((item) => {
  if (!['MOHURD-URBAN-DESIGN-MEASURES','MOHURD-ARCH-DESIGN-DEPTH-2016','PROJECT-AGENT-OPEN-CALL-TASKBOOK'].includes(item.standard_id)) return item;
  return {
    ...item,
    drawing_refs: Array.from(new Set([...(item.drawing_refs || []),'assets/figures/key-areas.png','drawings/a3-booklet.pdf#page=13'])),
    geometry_refs: Array.from(new Set([...(item.geometry_refs || []),'geometry/roads.geojson#V6-D-BASE-NS','geometry/public_space.geojson#V6-D-TRIAL'])),
    metric_refs: Array.from(new Set([...(item.metric_refs || []),'s7_review_scale_count','s7_baseline_sample_status'])),
    evidence_summary_zh: `${item.evidence_summary_zh || ''} V6 以 S7 四级尺度、公共路线不可退化、四态运营和回执测量补强可实施空间证据。`.trim(),
  };
});
standards.v6_evidence_index = depth.v6_evidence_index;
write('standard_matrix.json', standards);

const risk = read('risk.json');
risk.summary = 'V6 把 S7 的公共路线、路缘、常规接驳、AI 试验边界、雨水花园、人工岗位、双急停、消防和撤场写入同一组可追踪概念对象；空间深度 major 在盲审前保持开放，现场成效与采用决定保持 unknown。';
risk.v6_flagship_rule = 'baseline_route_continuous_in_OPEN_TRIAL_PAUSE_RETIRE + zero_tolerance_safety + human_authority';
write('risk.json', risk);

console.log('V6 matrices and risk evidence refreshed');
