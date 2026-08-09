#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const root = __dirname;
const readJson = (name) => JSON.parse(fs.readFileSync(path.join(root, name), 'utf8'));
const contract = readJson('autonomy-curbside-tabletop-contract.json');
const evidence = readJson('autonomy-curbside-tabletop-evidence.json');
const gates = readJson('curbside-test-gates.json');
const checks = [];

function check(id, pass, observed, expected) {
  checks.push({ id, pass, observed, expected });
}

const gateIds = new Set((gates.gates || []).map((gate) => gate.id));
check(
  'gate-linkage',
  contract.gate_ids.every((id) => gateIds.has(id)),
  contract.gate_ids,
  ['AV-T01', 'AV-T02', 'AV-T03']
);
check(
  'unknown-boundary',
  gates.gates.every((gate) => gate.baseline === 'unknown') &&
    String(gates.decision_rule).includes('unknown'),
  gates.gates.map((gate) => ({ id: gate.id, baseline: gate.baseline })),
  'all gate baselines stay unknown'
);
check(
  'ordinary-route-continuity',
  contract.fixtures.some((fixture) =>
    fixture.id === 'ordinary_curb_audit' &&
    fixture.expected_action === 'preserve_manual_patrol_and_paper_signage'
  ),
  contract.fixtures.find((fixture) => fixture.id === 'ordinary_curb_audit')?.expected_action,
  'preserve_manual_patrol_and_paper_signage'
);
check(
  'accessible-stop',
  contract.fixtures.some((fixture) =>
    fixture.id === 'accessible_route_obstruction' &&
    fixture.expected_action === 'stop_automation_and_switch_to_human_only' &&
    fixture.fallback === 'manual_service_route_preserved'
  ),
  contract.fixtures.find((fixture) => fixture.id === 'accessible_route_obstruction')?.expected_action,
  'stop automation and preserve manual route'
);
check(
  'equivalent-service-stop',
  contract.fixtures.some((fixture) =>
    fixture.id === 'equivalent_service_worse' &&
    fixture.expected_action === 'hold_trial_and_keep_human_paper_phone_route' &&
    fixture.fallback === 'human_service_and_redress_preserved'
  ),
  contract.fixtures.find((fixture) => fixture.id === 'equivalent_service_worse')?.expected_action,
  'hold trial and keep human paper/phone route'
);
check(
  'network-weather-rollback',
  contract.fixtures.some((fixture) =>
    fixture.id === 'network_weather_rollback' &&
    fixture.expected_action === 'freeze_new_trials_broadcast_and_restore_ordinary_service' &&
    fixture.fallback.includes('recovery')
  ),
  contract.fixtures.find((fixture) => fixture.id === 'network_weather_rollback')?.expected_action,
  'freeze, broadcast, restore and recover'
);
check(
  'no-authorization',
  contract.operational_status === 'not_authorized_not_run' &&
    contract.boundary.authorization === 'not_authorized' &&
    evidence.operational_status === 'not_authorized_not_run',
  { contract: contract.operational_status, evidence: evidence.operational_status },
  'not_authorized_not_run'
);
check(
  'no-performance-inference',
  contract.boundary.performance_results === null &&
    evidence.performance_results === null &&
    evidence.baselines === 'unknown',
  { performance_results: evidence.performance_results, baselines: evidence.baselines },
  'null performance results and unknown baselines'
);

const ok = checks.every((item) => item.pass);
const output = {
  runner: 'run-autonomy-curbside-tabletop.js',
  contract_id: contract.contract_id,
  ok,
  mode: 'offline_synthetic_tabletop',
  fixtures: contract.fixtures.length,
  acceptance_checks_defined: contract.acceptance_checks.length,
  checks_executed: checks.length,
  rollback_steps: contract.rollback_steps.length,
  result_status: contract.boundary.result_status,
  operational_status: contract.operational_status,
  performance_results: contract.boundary.performance_results,
  checks
};

console.log(JSON.stringify(output, null, 2));
process.exitCode = ok ? 0 : 1;
