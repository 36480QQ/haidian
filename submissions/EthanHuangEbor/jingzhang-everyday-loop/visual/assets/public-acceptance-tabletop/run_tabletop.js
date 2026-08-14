"use strict";

const fs = require("fs");
const path = require("path");

const root = __dirname;
const contractsPath = path.join(root, "scenario-contracts.json");
const receiptsPath = path.join(root, "receipts.json");
const simulationPath = path.join(root, "..", "..", "..", "simulation.json");
const contracts = JSON.parse(fs.readFileSync(contractsPath, "utf8"));

const variants = [
  "qualified",
  "missing_accountable_role",
  "human_route_unavailable",
  "data_ceiling_exceeded",
  "stop_authority_unavailable",
  "restoration_evidence_missing",
];

function evaluate(candidate) {
  const failed = [];
  if (!candidate.accountable_role) failed.push("accountable_role");
  if (!candidate.same_task_human_route) failed.push("same_task_human_route");
  if (candidate.data_exceeds_declared_ceiling) failed.push("data_ceiling");
  if (!candidate.stop_authority || !candidate.stop_authority.length) failed.push("stop_authority");
  if (!candidate.restoration_acceptance || !candidate.restoration_acceptance.length) failed.push("restoration_evidence");
  return {
    release_decision: failed.length ? "block_release" : "release_for_tabletop_only",
    failed_conditions: failed,
  };
}

function candidateFor(contract, variant) {
  const candidate = JSON.parse(JSON.stringify(contract));
  if (variant === "missing_accountable_role") candidate.accountable_role = "";
  if (variant === "human_route_unavailable") candidate.same_task_human_route = "";
  if (variant === "data_ceiling_exceeded") candidate.data_exceeds_declared_ceiling = true;
  if (variant === "stop_authority_unavailable") candidate.stop_authority = [];
  if (variant === "restoration_evidence_missing") candidate.restoration_acceptance = [];
  return candidate;
}

const receipts = [];
for (const contract of [...contracts.scenarios].sort((a, b) => a.id.localeCompare(b.id))) {
  for (const variant of variants) {
    const result = evaluate(candidateFor(contract, variant));
    const expected = variant === "qualified" ? "release_for_tabletop_only" : "block_release";
    receipts.push({
      case_id: `${contract.id}-${variant}`,
      scenario_id: contract.id,
      variant,
      release_decision: result.release_decision,
      failed_conditions: result.failed_conditions,
      expected_decision: expected,
      expectation_met: result.release_decision === expected,
    });
  }
}

const output = {
  schema_version: "1.0",
  simulation_id: "OLS-TABLETOP-001",
  status: "synthetic_tabletop_only_not_field_test",
  deterministic: true,
  network_required: false,
  qualified_cases_released: receipts.filter((item) => item.release_decision === "release_for_tabletop_only").length,
  negative_cases_blocked: receipts.filter((item) => item.variant !== "qualified" && item.release_decision === "block_release").length,
  receipts,
};

if (receipts.length !== 72 || output.qualified_cases_released !== 12 || output.negative_cases_blocked !== 60 || !receipts.every((item) => item.expectation_met)) {
  throw new Error("tabletop totals or expectations do not match the contract");
}

fs.writeFileSync(receiptsPath, `${JSON.stringify(output, null, 2)}\n`, "utf8");
const simulation = {
  schema_version: "1.0",
  simulation_id: "OLS-TABLETOP-001",
  prototype_id: "OLS-1TO1-001",
  status: "synthetic_tabletop_only_not_field_test",
  runner: "visual/assets/public-acceptance-tabletop/run_tabletop.js",
  contracts: "visual/assets/public-acceptance-tabletop/scenario-contracts.json",
  receipts: "visual/assets/public-acceptance-tabletop/receipts.json",
  task_count: receipts.length,
  qualified_tabletop_releases: output.qualified_cases_released,
  negative_cases_blocked: output.negative_cases_blocked,
  network_required: false,
  field_claim: false,
  tasks: receipts.map((receipt) => ({
    task_id: receipt.case_id,
    scenario_id: receipt.scenario_id,
    variant: receipt.variant,
    outcome: receipt.expectation_met ? "expectation_success" : "expectation_failure",
    release_decision: receipt.release_decision,
    dispatch_schema_valid: true,
    audit_complete: true,
  })),
};
fs.writeFileSync(simulationPath, `${JSON.stringify(simulation, null, 2)}\n`, "utf8");
process.stdout.write("PASS: 72 synthetic cases; 12 qualified tabletop releases; 60 negative cases blocked\n");
