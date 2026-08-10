#!/usr/bin/env node
const fs = require("fs");
const path = require("path");
const source = process.argv[2] || path.join(__dirname, "..", "..", "simulation.json");
const simulation = JSON.parse(fs.readFileSync(source, "utf8"));
function evaluate(x) {
  const gates = [
    ["G0", x.authorized_for_tabletop && !x.real_world_run],
    ["G1", x.site_interface_recorded && x.access_egress_check_recorded],
    ["G2", x.synthetic_data && !x.personal_data],
    ["G3", x.rights_recorded],
    ["G4", x.steward_role_assigned && x.manual_takeover_rehearsed],
    ["G5", x.public_notice_complete && x.non_ai_route_available],
    ["G6", x.receipt_complete && x.exit_available && x.rollback_steps >= 5]
  ];
  for (const [gate, ok] of gates) if (!ok) return {decision:"stop", failed_gate:gate};
  return {decision:"pass", failed_gate:null};
}
const cases = simulation.tasks.map(task => {
  const actual = evaluate(task.inputs);
  return {task_id:task.task_id, expected:task.expected, actual,
    match:JSON.stringify(actual) === JSON.stringify(task.expected)};
});
const output = {
  runner:"visual/assets/run-veranda-receipt.js", generated_from:"simulation.json",
  tabletop_only:true, case_count:cases.length,
  expected_outcome_matches:cases.filter(x=>x.match).length,
  expected_outcome_match_rate:cases.filter(x=>x.match).length / cases.length,
  negative_stop_branches:cases.filter(x=>x.actual.decision === "stop").length,
  rollback_step_count:simulation.pilot_contract.rollback.length, cases,
  claim_limit:"Structure and stop/exit logic only; no real-world authorization, performance or safety claim."
};
console.log(JSON.stringify(output, null, 2));
if (output.expected_outcome_matches !== output.case_count) process.exitCode = 1;
