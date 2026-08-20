#!/usr/bin/env node
/**
 * verify_spine.js — 智脊·京张AI创新带 提交包一致性验证器
 *
 * 用途：离线验证 risk.json / spatial.json / simulation.json / metrics.json
 * 与 proposal.md 之间的结构一致性，以及变异测试是否全部拦截。
 * 不调用外部 API，不联网，仅读取提交包内文件。
 *
 * 运行：node verify_spine.js   （在 visual/assets/ 目录下，或任意位置）
 *
 * 边界声明：本脚本是离线概念验证，证明提交包内判定逻辑可复现、
 * 结构一致、变异违规可被文档机制识别；不证明实地数据、真实复核
 * 主体介入、服务绩效或官方审批结论。
 */
'use strict';

const fs = require('fs');
const path = require('path');

// 提交包根目录 = 本脚本所在目录的上一级上级（visual/assets -> visual -> 提交包根）
const ROOT = path.resolve(__dirname, '..', '..');

function readJSON(relPath) {
  const p = path.join(ROOT, relPath);
  if (!fs.existsSync(p)) {
    return null;
  }
  try {
    return JSON.parse(fs.readFileSync(p, 'utf8'));
  } catch (e) {
    return { __parse_error: e.message };
  }
}

const results = [];
function check(id, passed, detail) {
  results.push({ id, passed, detail });
}

const risk = readJSON('risk.json');
const spatial = readJSON('spatial.json');
const sim = readJSON('simulation.json');
const metrics = readJSON('metrics.json');

// ---- 1. risk.json 校验 ----
if (!risk) {
  check('risk.present', false, 'risk.json 缺失');
} else if (risk.__parse_error) {
  check('risk.present', false, 'risk.json 解析失败: ' + risk.__parse_error);
} else {
  const dims = risk.dimensions || [];
  check('risk.dimension_count', dims.length === 8, `风险维度=${dims.length}，期望 8`);
  const badScores = dims.filter(d => !(d.score >= 1 && d.score <= 5));
  check('risk.score_range', badScores.length === 0, `越界评分维度=${badScores.length}`);
  const highRisk = dims.filter(d => d.score >= 4);
  const highNoReview = highRisk.filter(d => !d.human_review);
  check('risk.high_risk_human_review', highNoReview.length === 0, `高风险缺人工复核=${highNoReview.map(d => d.id).join(',') || '无'}`);
  const noMitigation = dims.filter(d => !d.mitigation);
  check('risk.mitigation_all', noMitigation.length === 0, `缺缓解措施=${noMitigation.length}`);
}

// ---- 2. spatial.json 校验 ----
if (!spatial) {
  check('spatial.present', false, 'spatial.json 缺失');
} else if (spatial.__parse_error) {
  check('spatial.present', false, 'spatial.json 解析失败');
} else {
  const items = spatial.items || [];
  const nodes = items.filter(i => i.type === 'node');
  const corridors = items.filter(i => i.type === 'corridor');
  const areas = items.filter(i => i.type === 'area');
  check('spatial.node_count', nodes.length === 6, `节点=${nodes.length}，期望 6`);
  check('spatial.corridor_count', corridors.length === 4, `廊道=${corridors.length}，期望 4`);
  check('spatial.area_count', areas.length === 3, `区域=${areas.length}，期望 3`);
  const nonConcept = items.filter(i => !(i.geometry && i.geometry.mode === 'concept'));
  check('spatial.concept_only', nonConcept.length === 0, `非 concept 项=${nonConcept.length}`);
  const withCoords = items.filter(i => i.geometry && (i.geometry.coordinates || i.geometry.bbox));
  check('spatial.no_coordinates', withCoords.length === 0, `含坐标/bbox 项=${withCoords.length}`);
  const badLevel = items.filter(i => !['cleared', 'provisional', 'public'].includes(i.public_level));
  check('spatial.public_level_enum', badLevel.length === 0, `非法 public_level=${badLevel.length}`);
}

// ---- 3. simulation.json 校验 ----
if (!sim) {
  check('sim.present', false, 'simulation.json 缺失');
} else if (sim.__parse_error) {
  check('sim.present', false, 'simulation.json 解析失败');
} else {
  const tasks = sim.tasks || [];
  const mutations = sim.mutation_tests || [];
  check('sim.task_count_match', sim.task_count === tasks.length, `task_count=${sim.task_count}，实际=${tasks.length}`);
  let totalAssertions = 0;
  let failingAssertions = 0;
  for (const t of tasks) {
    const as = t.assertions || [];
    totalAssertions += as.length;
    for (const a of as) {
      if (JSON.stringify(a.expected) !== JSON.stringify(a.actual)) failingAssertions++;
    }
    if (t.result !== 'pass') failingAssertions++;
  }
  check('sim.assertion_count_match', sim.assertion_count === totalAssertions, `assertion_count=${sim.assertion_count}，实际=${totalAssertions}`);
  check('sim.all_assertions_pass', failingAssertions === 0, `未通过断言=${failingAssertions}`);
  const notIntercepted = mutations.filter(m => m.expected_detection !== 'intercepted' || m.result !== 'pass');
  check('sim.mutation_all_intercepted', notIntercepted.length === 0, `变异未拦截=${notIntercepted.length}`);
  check('sim.mutation_count_match', sim.mutation_test_count === mutations.length, `mutation_test_count=${sim.mutation_test_count}，实际=${mutations.length}`);
  const boundary = sim.boundary_statement || '';
  check('sim.boundary_stated', boundary.length > 0, '缺少 boundary_statement 边界声明');
}

// ---- 4. metrics.json 校验 ----
if (!metrics) {
  check('metrics.present', false, 'metrics.json 缺失');
} else if (metrics.__parse_error) {
  check('metrics.present', false, 'metrics.json 解析失败');
} else {
  const m = metrics.metrics || {};
  const known = Object.values(m).filter(v => v && v.status === 'known');
  check('metrics.known_count', known.length >= 10, `known 指标=${known.length}，期望 ≥10`);
}

// ---- 汇总 ----
const failed = results.filter(r => !r.passed);
const passed = results.filter(r => r.passed);
console.log('\n=== 智脊·京张AI创新带 提交包验证 ===');
console.log(`通过: ${passed.length}/${results.length}`);
for (const r of results) {
  const mark = r.passed ? '  PASS' : '  FAIL';
  console.log(`${mark}  ${r.id}  ${r.passed ? '' : '— ' + r.detail}`);
}
if (failed.length > 0) {
  console.log(`\nRESULT: FAIL (${failed.length} 项未通过)`);
  process.exit(1);
} else {
  console.log('\nRESULT: PASS');
  console.log('边界声明：离线概念验证，不证明实地数据/真实复核主体介入/服务绩效/官方审批结论。');
  process.exit(0);
}
