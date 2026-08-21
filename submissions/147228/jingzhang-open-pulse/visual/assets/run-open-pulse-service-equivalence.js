#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '../..');
const read = (rel) => JSON.parse(fs.readFileSync(path.join(root, rel), 'utf8'));
const atlas = read('visual/assets/open-pulse-service-equivalence-atlas.json');
const scenarios = read('visual/assets/scenario-operation-matrix.json');
const operations = read('visual/assets/operations-matrix.json');
const nodes = read('visual/assets/key-area-node-plans.json');
const personas = read('visual/assets/persona-and-inclusion-matrix.json');
const gate = read('visual/assets/gates/29-non-ai-equivalence.json');
const tabletop = read('visual/assets/open-pulse-tabletop-contract.json');

const errors = [];
const same = (actual, expected, label) => {
  if (actual !== expected) errors.push(`${label}: expected ${expected}, got ${actual}`);
};
const has = (set, value, label) => {
  if (!set.has(value)) errors.push(`${label}: missing ${value}`);
};

same(atlas.schema_version, 'open-pulse-service-equivalence-atlas-v1', 'atlas schema');
same(atlas.operational_status, 'not_authorized_not_run', 'operational status');
same(atlas.baseline, 'unknown', 'baseline');
same(atlas.result_status, 'not_run', 'result status');
same(atlas.decision, 'HOLD', 'decision');
same(atlas.authorizations, 0, 'authorizations');
same(atlas.field_data, false, 'field data');
same(atlas.performance_results, null, 'performance results');
same(atlas.network_calls, 0, 'network calls');
same(gate.gate_id, 'GATE-29', 'equivalence gate');
same(tabletop.contract_id, 'OP-S02-TABLETOP-001', 'tabletop contract');

const scenarioRows = new Map(scenarios.rows.map((row) => [row.scenario_id, row]));
const operationRows = new Map(operations.packages.map((row) => [row.action_id, row]));
const nodeRows = new Map(nodes.nodes.map((row) => [row.id, row]));
const personaIds = new Set(personas.personas.map((row) => row.id));
same(scenarioRows.size, 14, 'scenario row count');
same(operationRows.size, 8, 'operation row count');
same(nodeRows.size, 3, 'node count');
same(personas.personas.length, 8, 'persona count');
same(atlas.route_cards.length, 3, 'route card count');
same(atlas.receipt_steps.length, 5, 'receipt step count');
same(atlas.negative_replay.length, 4, 'negative fixture count');

for (const route of atlas.route_cards) {
  has(nodeRows, route.node_id, `${route.id} node`);
  has(scenarioRows, route.scenario_id, `${route.id} scenario`);
  has(operationRows, route.operation_id, `${route.id} operation`);
  const node = nodeRows.get(route.node_id);
  if (node && node.site_ref !== route.site_ref) errors.push(`${route.id}: site ref does not match node`);
  for (const persona of route.persona_ids) has(personaIds, persona, `${route.id} persona`);
  for (const field of ['ordinary_route', 'ai_gain', 'stop_rule', 'restore_rule']) {
    if (!route[field]) errors.push(`${route.id}: missing ${field}`);
  }
}

const expectedSteps = ['EQ-01', 'EQ-02', 'EQ-03', 'EQ-04', 'EQ-05'];
if (JSON.stringify(atlas.receipt_steps.map((step) => step.id)) !== JSON.stringify(expectedSteps)) {
  errors.push('receipt step order is not deterministic');
}
if (JSON.stringify(atlas.positive_control) !== JSON.stringify(['R-01', 'R-02', 'R-03'])) {
  errors.push('positive control set changed');
}
if (new Set(atlas.negative_replay.map((fixture) => fixture.fixture_id)).size !== 4) {
  errors.push('negative fixtures are not unique');
}

const result = {
  ok: errors.length === 0,
  atlas_id: atlas.atlas_id,
  route_cards: atlas.route_cards.length,
  source_scenarios: scenarioRows.size,
  source_operations: operationRows.size,
  source_nodes: nodeRows.size,
  source_personas: personas.personas.length,
  receipt_steps: atlas.receipt_steps.length,
  negative_replay: `${atlas.negative_replay.length}/${atlas.negative_replay.length}`,
  positive_control: atlas.positive_control.length,
  authorizations: atlas.authorizations,
  field_data: atlas.field_data,
  baseline: atlas.baseline,
  result_status: atlas.result_status,
  decision: atlas.decision,
  errors
};
process.stdout.write(JSON.stringify(result, null, 2) + '\n');
process.exitCode = errors.length ? 1 : 0;
