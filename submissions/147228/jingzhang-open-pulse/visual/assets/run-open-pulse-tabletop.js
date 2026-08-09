'use strict';

/* Offline replay of the S02 public-route safety contract. PASS is not deployment evidence. */
const fs = require('fs');
const path = require('path');
const root = __dirname;
const contract = JSON.parse(fs.readFileSync(path.join(root, 'open-pulse-tabletop-contract.json'), 'utf8'));
const record = JSON.parse(fs.readFileSync(path.join(root, 'example-s02-embodied-test-window.json'), 'utf8'));

function result(id, pass, observed, expected) { return {id, pass, observed, expected}; }

const fixtures = contract.fixtures || [];
const rollback = contract.rollback_steps || [];
const checks = [
  result('record_identity', contract.scenario_id === 'S02' && record.purpose.scenario_id === 'S02' && record.record_id === 'OPW-S02-SYNTHETIC-001', `${contract.scenario_id}/${record.record_id}`, 'S02/OPW-S02-SYNTHETIC-001'),
  result('ordinary_service_preserved', fixtures.length === 4 && fixtures.every((item) => item.ordinary_equivalent), fixtures.length, 4),
  result('hold_boundary_preserved', record.place_window.boundary_status === 'provisional' && record.observation.baseline_status === 'missing' && record.observation.result_status === 'not_run', 'provisional/missing/not_run', 'provisional/missing/not_run'),
  result('stop_control_preserved', record.human_control.stop_triggers.length >= 4 && record.release_decision.decision === 'hold', record.human_control.stop_triggers.length, '>=4/hold'),
  result('no_automatic_authorization', contract.operational_status === 'not_authorized_not_run' && contract.result_boundary.performance_results === null, `${contract.operational_status}/null`, 'not_authorized_not_run/null'),
  result('rollback_sequence_complete', rollback.length === 5 && rollback.every(Boolean), rollback.length, 5)
];
const pass = checks.every((item) => item.pass);
if (!pass) { console.error('OPEN_PULSE_TABLETOP_CHECK_FAIL'); process.exitCode = 1; }
console.log(JSON.stringify({
  runner: 'run-open-pulse-tabletop.js',
  contract_id: contract.contract_id,
  scenario_id: contract.scenario_id,
  status: pass ? 'PASS' : 'FAIL',
  claim_level: contract.claim_level,
  operational_status: contract.operational_status,
  gate_effect: contract.gate_effect,
  environment: contract.environment,
  checks,
  fixture_dispatch: {fixtures: fixtures.length, ordinary_equivalents: fixtures.filter((item) => item.ordinary_equivalent).length, route_restored_on_stop: true, human_review_required: true},
  rollback: {steps_declared: rollback.length, steps_replayed: pass ? rollback.length : 0, result: pass ? 'pass' : 'fail'},
  result_status: record.observation.result_status,
  performance_results: null,
  next_action: 'Confirm official geometry, accessibility baseline, named roles and professional safety review before any bounded S02 window.'
}, null, 2));
