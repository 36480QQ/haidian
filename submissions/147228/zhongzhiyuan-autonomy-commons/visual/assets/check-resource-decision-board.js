#!/usr/bin/env node
/* Offline checker for the resource-and-decision board. */
const fs = require('fs');
const path = require('path');
const here = __dirname;
const root = path.resolve(here, '../..');
const data = JSON.parse(fs.readFileSync(path.join(here, 'resource-decision-board.json'), 'utf8'));
const checks = [];
function check(id, pass, detail) { checks.push({ id, status: pass ? 'PASS' : 'FAIL', detail }); }
check('STATUS', data.status === 'conceptual_resource_decision_contract' && data.not_a_score === true, data.status);
check('BOUNDARY', data.official_boundary === false && data.geometry_role === 'provisional_constraint' && data.operational_status === 'not_authorized_not_run', 'provisional and not operational');
check('PRINCIPLES', data.principles.length === 3 && data.principles.every((x) => x.name_zh && x.name_en && x.rule_zh && x.rule_en), `principles=${data.principles.length}`);
check('RESOURCES', data.resource_classes.length === 5 && data.resource_classes.every((x) => [x.name_zh, x.name_en, x.holds_zh, x.holds_en, x.resource_route_zh, x.resource_route_en, x.veto_zh, x.veto_en, x.minimum_evidence_zh, x.minimum_evidence_en].every(Boolean)), `resource_classes=${data.resource_classes.length}`);
check('STAGES', data.decision_stages.length === 4 && data.decision_stages.every((x) => [x.stage_zh, x.stage_en, x.can_propose_zh, x.can_propose_en, x.must_hold_zh, x.must_hold_en, x.decision_zh, x.decision_en, x.stop_zh, x.stop_en].every(Boolean)), `decision_stages=${data.decision_stages.length}`);
check('ANCHORS', data.coverage.key_area_refs.every((ref) => { const [file] = ref.split('#'); return fs.existsSync(path.join(root, file)); }), 'all key-area anchors resolve');
check('FIGURES', ['resource-decision-board.svg', 'resource-decision-board.en.svg'].every((name) => fs.existsSync(path.join(root, 'assets', 'figures', name))), 'bilingual SVG figures exist');
const failed = checks.filter((x) => x.status === 'FAIL');
const result = { schema_version: '0.1.0', generated_by: 'visual/assets/check-resource-decision-board.js', status: failed.length ? 'FAIL' : 'PASS', checks, not_a_score: true, boundary_zh: 'PASS 只证明资源类别、决策权和停止字段可离线复核，不产生预算、许可、主体或运营结论。', boundary_en: 'PASS proves only that resource, decision, and stop fields replay offline; it produces no budget, permit, actor, or operating conclusion.' };
fs.writeFileSync(path.join(here, 'resource-decision-board-evidence.json'), `${JSON.stringify(result, null, 2)}\n`);
console.log(JSON.stringify(result, null, 2));
if (failed.length) process.exit(1);
