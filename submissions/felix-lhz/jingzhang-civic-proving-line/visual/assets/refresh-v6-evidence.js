const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..', '..');
const read = (name) => JSON.parse(fs.readFileSync(path.join(root, name), 'utf8'));
const write = (name, value) => fs.writeFileSync(path.join(root, name), `${JSON.stringify(value, null, 2)}\n`);

const depth = read('design_depth_matrix.json');
const depthUpdates = {
  traffic_rail_slow_parking: {
    geometry_refs: ['geometry/roads.geojson#V7-D-BASE-NS','geometry/roads.geojson#V7-D-BASE-EW','geometry/roads.geojson#V7-D-TACTILE-NS','geometry/roads.geojson#V7-D-TRANSIT','geometry/roads.geojson#V7-D-EMERGENCY'],
    metric_refs: ['s7_review_scale_count','s7_prototype_kit_item_count','s7_baseline_sample_status'],
    evidence_summary_zh: 'S7 城市采纳站把公共十字、触觉引导、常规接驳、独立试验湾、证据门廊、疏散和撤场画在同一五级尺度证据链中；方向和尺寸均为待测绘复核的原型建议。',
  },
  blue_green_public_space: {
    geometry_refs: ['geometry/public_space.geojson#V7-D-RAIN-W','geometry/public_space.geojson#V7-D-RAIN-E','geometry/public_space.geojson#V7-D-SHADE-W','geometry/public_space.geojson#V7-D-SHADE-E','geometry/public_space.geojson#V7-D-EVIDENCE'],
    evidence_summary_zh: '大钟寺前场将雨水花园、双侧遮阴休息、证据门廊和公共十字作为永久基线；AI 试验停机或撤场后仍完整。',
  },
  three_key_area_detailed_design: {
    drawing_refs: ['assets/figures/key-areas.png','assets/figures/hero-s7-detail.png','assets/figures/hero-s7-section.png','assets/figures/hero-s7-assembly.png','drawings/a0-boards.pdf#page=2','drawings/a3-booklet.pdf#page=10'],
    geometry_refs: ['geometry/roads.geojson#V7-D-BASE-NS','geometry/roads.geojson#V7-D-TACTILE-NS','geometry/public_space.geojson#V7-D-TRIAL','geometry/buildings.geojson#V7-D-PORCH','geometry/constraints.geojson#V7-D-STAFF-TRIAL'],
    metric_refs: ['s7_traceable_spatial_object_count','s7_review_scale_count','s7_prototype_kit_item_count','s7_baseline_sample_status','s7_formal_cost_status'],
    assumption_ids: ['A-SPATIAL-ATLAS-001','A-V7-S7-DIMENSIONS'],
    evidence_summary_zh: 'S7 作为旗舰样板完成城市联系、1:2000、1:500、1:200和装配轴测；公共十字、可逆试验湾、证据门廊、双急停、消防、存储与还场全部可追踪，T2/S2 保留差异化对照。',
  },
  phasing_implementation: {
    metric_refs: ['field_performance_status','s7_baseline_sample_status'],
    evidence_summary_zh: '四阶段以进入条件、输出物和失败条件控制；17 项原型包先完成数量复算与正式询价，S7 必须在 E2 建立普通基线并完成许可矩阵，才可进入 E3。',
  },
  metrics_recalculation: {
    metric_refs: ['s7_traceable_spatial_object_count','s7_review_scale_count','s7_prototype_kit_item_count','s7_baseline_sample_status','s7_formal_cost_status','field_performance_status'],
    evidence_summary_zh: '复算设计对象、审查尺度与原型包数量；100 次通行分母、7 日窗口和计时起止点已登记，正式报价、现场样本、成效与采用结论保持 unknown。',
  },
};
depth.items = depth.items.map((item) => ({ ...item, ...(depthUpdates[item.item_id] || {}) }));
delete depth.v6_evidence_index;
depth.v7_evidence_index = {
  version: 'V7',
  flagship: 'S7 Dazhongsi / A0-02 / A3 pp.9-11 / assets/figures/key-areas.png',
  five_views: '1:5000 city / 1:2000 plan / 1:500 detail / 1:200 section / assembly axonometric',
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
delete compliance.v6_evidence_index;
compliance.v7_evidence_index = depth.v7_evidence_index;
write('compliance_matrix.json', compliance);

const standards = read('standard_matrix.json');
standards.standards = standards.standards.map((item) => {
  if (!['MOHURD-URBAN-DESIGN-MEASURES','MOHURD-ARCH-DESIGN-DEPTH-2016','PROJECT-AGENT-OPEN-CALL-TASKBOOK'].includes(item.standard_id)) return item;
  return {
    ...item,
    drawing_refs: Array.from(new Set([...(item.drawing_refs || []),'assets/figures/key-areas.png','assets/figures/hero-s7-assembly.png','drawings/a3-booklet.pdf#page=10'])),
    geometry_refs: Array.from(new Set([...(item.geometry_refs || []).filter((ref) => !/V[56]-D-/.test(ref)),'geometry/roads.geojson#V7-D-BASE-NS','geometry/roads.geojson#V7-D-TACTILE-NS','geometry/public_space.geojson#V7-D-TRIAL','geometry/buildings.geojson#V7-D-PORCH'])),
    metric_refs: Array.from(new Set([...(item.metric_refs || []),'s7_review_scale_count','s7_prototype_kit_item_count','s7_baseline_sample_status','s7_formal_cost_status'])),
    evidence_summary_zh: `${(item.evidence_summary_zh || '').replace(/\s+V[67] 以 S7[^。]*。/g,'').trim()} V7 以 S7 五级视图、公共十字不可退化、17 项原型包、四态运营和回执测量补强可实施证据。`.trim(),
  };
});
delete standards.v6_evidence_index;
standards.v7_evidence_index = depth.v7_evidence_index;
write('standard_matrix.json', standards);

const risk = read('risk.json');
risk.summary = 'V7 把 S7 的公共十字、触觉引导、路缘、常规接驳、可逆试验湾、证据门廊、蓝绿边界、岗位、双急停、消防、存储和撤场写入同一组可追踪对象；正式报价、现场成效与采用决定保持 unknown。';
risk.v7_flagship_rule = 'public_cross_continuous_in_OPEN_TRIAL_PAUSE_RETIRE + reversible_trial_bay + staffed_evidence_porch + human_authority';
write('risk.json', risk);

console.log('V7 matrices and risk evidence refreshed');
