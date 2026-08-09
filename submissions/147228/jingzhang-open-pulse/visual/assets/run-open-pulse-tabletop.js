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
const acceptanceChecks = contract.acceptance_checks || [];
const traceRequirements = contract.trace_requirements || {};
const fixtureIds = new Set(fixtures.map((item) => item.fixture_id));
const acceptanceIds = acceptanceChecks.map((item) => item.id);
const acceptanceIdSet = new Set(acceptanceIds);
const scenarioIds = new Set([contract.scenario_id]);
const boundaryFields = new Set([
  ...Object.keys(contract),
  ...Object.keys(contract.result_boundary || {})
]);
const tracedFixtureIds = new Set();
const tracedScenarioIds = new Set();
const tracedBoundaryFields = new Set();
const rollbackStepIds = new Set(rollback.map((item) => item && item.id));
const rollbackFixtureIds = new Set();
const rollbackAcceptanceIds = new Set();
let traceReferencesResolve = true;
let everyAcceptanceCheckHasTrace = true;
for (const item of acceptanceChecks) {
  const refs = [
    ...(item.fixture_ids || []),
    ...(item.scenario_ids || []),
    ...(item.boundary_fields || [])
  ];
  everyAcceptanceCheckHasTrace = everyAcceptanceCheckHasTrace && refs.length > 0;
  for (const id of item.fixture_ids || []) {
    tracedFixtureIds.add(id);
    traceReferencesResolve = traceReferencesResolve && fixtureIds.has(id);
  }
  for (const id of item.scenario_ids || []) {
    tracedScenarioIds.add(id);
    traceReferencesResolve = traceReferencesResolve && scenarioIds.has(id);
  }
  for (const field of item.boundary_fields || []) {
    tracedBoundaryFields.add(field);
    traceReferencesResolve = traceReferencesResolve && boundaryFields.has(field);
  }
}
let rollbackReferencesResolve = true;
let everyRollbackStepHasTrace = true;
for (const item of rollback) {
  everyRollbackStepHasTrace = everyRollbackStepHasTrace &&
    Boolean(item && item.id && item.action && Array.isArray(item.fixture_ids) && item.fixture_ids.length > 0 &&
      Array.isArray(item.acceptance_ids) && item.acceptance_ids.length > 0);
  for (const id of (item && item.fixture_ids) || []) {
    rollbackFixtureIds.add(id);
    rollbackReferencesResolve = rollbackReferencesResolve && fixtureIds.has(id);
  }
  for (const id of (item && item.acceptance_ids) || []) {
    rollbackAcceptanceIds.add(id);
    rollbackReferencesResolve = rollbackReferencesResolve && acceptanceIdSet.has(id);
  }
}
function coversAll(traced, required) {
  return (required || []).every((id) => traced.has(id));
}
const rollbackTraceCoverage =
  rollbackReferencesResolve &&
  everyRollbackStepHasTrace &&
  rollback.length === 5 &&
  rollbackStepIds.size === rollback.length &&
  coversAll(rollbackStepIds, traceRequirements.rollback_step_ids);
const traceCoverage =
  traceReferencesResolve &&
  everyAcceptanceCheckHasTrace &&
  coversAll(tracedFixtureIds, traceRequirements.fixture_ids) &&
  coversAll(tracedScenarioIds, traceRequirements.scenario_ids) &&
  coversAll(tracedBoundaryFields, traceRequirements.boundary_fields);
const checks = [
  result('record_identity', contract.scenario_id === 'S02' && record.purpose.scenario_id === 'S02' && record.record_id === 'OPW-S02-SYNTHETIC-001', `${contract.scenario_id}/${record.record_id}`, 'S02/OPW-S02-SYNTHETIC-001'),
  result('ordinary_service_preserved', fixtures.length === 4 && fixtures.every((item) => item.ordinary_equivalent), fixtures.length, 4),
  result('hold_boundary_preserved', record.place_window.boundary_status === 'provisional' && record.observation.baseline_status === 'missing' && record.observation.result_status === 'not_run', 'provisional/missing/not_run', 'provisional/missing/not_run'),
  result('stop_control_preserved', record.human_control.stop_triggers.length >= 4 && record.release_decision.decision === 'hold', record.human_control.stop_triggers.length, '>=4/hold'),
  result('no_automatic_authorization', contract.operational_status === 'not_authorized_not_run' && contract.result_boundary.performance_results === null, `${contract.operational_status}/null`, 'not_authorized_not_run/null'),
  result('rollback_sequence_complete', rollback.length === 5 && rollback.every((item) => item && item.action), rollback.length, 5),
  result('acceptance_trace_references', traceCoverage, {
    acceptance_checks: acceptanceChecks.length,
    fixtures: [...tracedFixtureIds],
    scenarios: [...tracedScenarioIds],
    boundary_fields: [...tracedBoundaryFields]
  }, 'every acceptance check has resolvable trace references and required coverage'),
  result('acceptance_ids_unique', acceptanceIds.length === 6 && new Set(acceptanceIds).size === acceptanceIds.length, acceptanceIds, 'six unique acceptance-check IDs'),
  result('rollback_trace_references', rollbackTraceCoverage, {
    rollback_steps: [...rollbackStepIds],
    fixtures: [...rollbackFixtureIds],
    acceptance_checks: [...rollbackAcceptanceIds]
  }, 'five unique rollback IDs with resolvable fixture and acceptance references')
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
  trace_coverage: {
    acceptance_checks: `${acceptanceChecks.length}/${acceptanceChecks.length}`,
    fixtures: `${tracedFixtureIds.size}/${(traceRequirements.fixture_ids || []).length}`,
    scenarios: `${tracedScenarioIds.size}/${(traceRequirements.scenario_ids || []).length}`,
    boundary_fields: `${tracedBoundaryFields.size}/${(traceRequirements.boundary_fields || []).length}`,
    rollback_steps: `${rollbackStepIds.size}/${(traceRequirements.rollback_step_ids || []).length}`
  },
  rollback: {steps_declared: rollback.length, steps_replayed: pass ? rollback.length : 0, result: pass ? 'pass' : 'fail'},
  result_status: record.observation.result_status,
  performance_results: null,
  next_action: 'Confirm official geometry, accessibility baseline, named roles and professional safety review before any bounded S02 window.'
}, null, 2));
