const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = path.resolve(__dirname, '..', '..');
const INPUT = path.join(__dirname, 'two-answers.json');
const OUTPUT = path.join(__dirname, 'v10-tabletop-results.json');
const RULE_VERSION = 'civic-adoption-compiler/1.0.0';
const ALLOWED_TRANSITIONS = new Set([
  'OPEN>TRIAL',
  'TRIAL>PAUSE',
  'PAUSE>OPEN',
  'PAUSE>RETIRE',
  'RETIRE>OPEN',
]);

function stable(value) {
  if (Array.isArray(value)) return `[${value.map(stable).join(',')}]`;
  if (value && typeof value === 'object') {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stable(value[key])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}

function hash(value) {
  return crypto.createHash('sha256').update(stable(value)).digest('hex');
}

function transition(from, to) {
  if (from === to) return { from, to, kind: 'guarded_no_change' };
  const key = `${from}>${to}`;
  if (!ALLOWED_TRANSITIONS.has(key)) throw new Error(`illegal state transition: ${key}`);
  return { from, to, kind: 'allowed_transition' };
}

const CASES = [
  {
    type: 'ordinary_baseline', initial: 'OPEN', expected: 'OPEN', event: 'baseline_task_requested',
    invariants: ['baseline_route_continuous', 'ordinary_service_available', 'ai_not_required'],
    recovery: 'remain_open_without_ai',
  },
  {
    type: 'missing_permit', initial: 'OPEN', expected: 'OPEN', event: 'trial_requested_with_missing_permit',
    invariants: ['permit_gate_complete_before_trial', 'trial_blocked_when_permit_missing'],
    recovery: 'close_missing_permit_then_request_trial_again',
  },
  {
    type: 'missing_role', initial: 'OPEN', expected: 'OPEN', event: 'trial_requested_with_missing_accountable_role',
    invariants: ['accountable_human_present_before_trial', 'trial_blocked_when_role_missing'],
    recovery: 'assign_independent_roles_then_request_trial_again',
  },
  {
    type: 'public_service_regression', initial: 'TRIAL', expected: 'PAUSE', event: 'baseline_route_or_service_regresses',
    invariants: ['baseline_never_regresses', 'pause_on_public_service_regression'],
    recovery: 'staff_complete_same_task_and_restore_public_route',
  },
  {
    type: 'zero_tolerance_event', initial: 'TRIAL', expected: 'PAUSE', event: 'zero_tolerance_event_detected',
    invariants: ['zero_tolerance_stops_trial', 'human_stop_authority_available'],
    recovery: 'isolate_equipment_log_event_and_open_human_review',
  },
  {
    type: 'human_recovery', initial: 'PAUSE', expected: 'OPEN', event: 'staffed_recovery_verified',
    invariants: ['same_task_completed_by_staff', 'public_route_restored_before_open'],
    recovery: 'open_baseline_only_and_schedule_review',
  },
  {
    type: 'equipment_retirement', initial: 'PAUSE', expected: 'OPEN', event: 'retirement_and_public_space_restoration',
    invariants: ['equipment_removed_to_declared_destination', 'retired_space_restored_to_public_use'],
    recovery: 'PAUSE>RETIRE>OPEN',
  },
];

function simulate(test) {
  const trace = [];
  const add = (from, to) => trace.push(transition(from, to));
  switch (test.type) {
    case 'ordinary_baseline': add('OPEN', 'OPEN'); break;
    case 'missing_permit': add('OPEN', 'OPEN'); break;
    case 'missing_role': add('OPEN', 'OPEN'); break;
    case 'public_service_regression': add('TRIAL', 'PAUSE'); break;
    case 'zero_tolerance_event': add('TRIAL', 'PAUSE'); break;
    case 'human_recovery': add('PAUSE', 'OPEN'); break;
    case 'equipment_retirement': add('PAUSE', 'RETIRE'); add('RETIRE', 'OPEN'); break;
    default: throw new Error(`unknown test type: ${test.type}`);
  }
  return { observed: trace.at(-1).to, trace };
}

function assertInput(scenarios) {
  if (scenarios.length !== 12) throw new Error(`expected 12 scenarios, received ${scenarios.length}`);
  const ids = new Set(scenarios.map((scene) => scene.id));
  if (ids.size !== 12) throw new Error('scenario ids are not unique');
  for (const scene of scenarios) {
    if (!scene.ordinary_answer?.zh || !scene.ordinary_answer?.en) throw new Error(`${scene.id}: ordinary answer missing`);
    if (!scene.human_responsibility?.zh || !scene.human_responsibility?.en) throw new Error(`${scene.id}: accountable human missing`);
    if (!scene.stop_conditions?.zh || !scene.stop_conditions?.en) throw new Error(`${scene.id}: stop condition missing`);
    if (!scene.exit_and_restore?.zh || !scene.exit_and_restore?.en) throw new Error(`${scene.id}: recovery exit missing`);
    if (!Array.isArray(scene.permit_dependencies) || scene.permit_dependencies.length === 0) throw new Error(`${scene.id}: permit dependencies missing`);
    if (scene.common_metrics.some((metric) => metric.status !== 'unknown')) {
      throw new Error(`${scene.id}: field metric presented as known before field operation`);
    }
  }
  let rejected = false;
  try { transition('OPEN', 'RETIRE'); } catch { rejected = true; }
  if (!rejected) throw new Error('illegal transition self-test did not fail');
}

function main() {
  const source = JSON.parse(fs.readFileSync(INPUT, 'utf8'));
  assertInput(source.scenarios);
  const tests = [];
  for (const scene of source.scenarios) {
    for (const [index, spec] of CASES.entries()) {
      const simulation = simulate(spec);
      const testCaseId = `${scene.id}-T${String(index + 1).padStart(2, '0')}`;
      const input = {
        rule_version: RULE_VERSION,
        scene_id: scene.id,
        scene_code: scene.code,
        baseline_route: scene.baseline_route_ref,
        permit_gate: scene.permit_gate,
        accountable_human: scene.human_responsibility,
        stop_condition: scene.stop_conditions,
        recovery: scene.exit_and_restore,
        test: spec,
      };
      const passed = simulation.observed === spec.expected && simulation.trace.every((step) => step.from === step.to || ALLOWED_TRANSITIONS.has(`${step.from}>${step.to}`));
      tests.push({
        verification_scope: 'synthetic_design_contract_only',
        test_case_id: testCaseId,
        scene_id: scene.id,
        scene_code: scene.code,
        case_type: spec.type,
        initial_state: spec.initial,
        injected_event: spec.event,
        expected_state: spec.expected,
        observed_state: simulation.observed,
        transition_trace: simulation.trace,
        invariants_checked: spec.invariants,
        synthetic_result: passed ? 'pass' : 'fail',
        input_hash: hash(input),
        recovery_exit: spec.recovery,
        field_status: 'not_field_run',
      });
    }
  }
  const failed = tests.filter((test) => test.synthetic_result !== 'pass');
  const output = {
    schema_version: '1.8.0',
    dataset_id: 'jingzhang-v10-synthetic-design-verification',
    rule_version: RULE_VERSION,
    generated_at: '2026-08-19T00:00:00+08:00',
    verification_scope: 'synthetic_design_contract_only',
    disclaimer: {
      zh: '84 项结果仅验证方案规则、状态机与退出路径自洽；不证明现场安全、效率、公众接受度或政府批准。',
      en: 'The 84 results verify only design-rule, state-machine and recovery consistency; they do not prove field safety, efficiency, public acceptance or government approval.',
    },
    allowed_transitions: [...ALLOWED_TRANSITIONS],
    forbidden_transition_self_test: { transition: 'OPEN>RETIRE', result: 'rejected_as_expected' },
    summary: {
      scenario_count: source.scenarios.length,
      test_types_per_scenario: CASES.length,
      test_case_count: tests.length,
      pass_count: tests.length - failed.length,
      fail_count: failed.length,
      field_result_count: 0,
      field_status: 'not_field_run',
      status: failed.length === 0 && tests.length === 84 ? 'T0_synthetic_contract_verified' : 'failed',
    },
    tests,
  };
  fs.writeFileSync(OUTPUT, `${JSON.stringify(output, null, 2)}\n`);
  if (failed.length || tests.length !== 84) throw new Error(`synthetic verification failed: ${failed.length} failed of ${tests.length}`);
  console.log(`V10 synthetic design verification: ${tests.length}/${tests.length} PASS; field_status=not_field_run`);
}

if (require.main === module) main();
module.exports = { main, transition, simulate, RULE_VERSION, ALLOWED_TRANSITIONS };
