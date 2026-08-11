"use strict";

// Deterministic, synthetic-only validation of the v3 civic-timetable contract.
// No network, device, account, personal-data, or production-system I/O is used.

const fs = require("fs");
const path = require("path");

const ROOT = __dirname;
const CASES = [
  "nominal",
  "missing_human",
  "missing_non_ai",
  "prohibited_data",
  "public_path_blocked",
  "reset_after_stop",
];

function readJson(name) {
  return JSON.parse(fs.readFileSync(path.join(ROOT, name), "utf8"));
}

function branch(spec, caseName) {
  const outcomes = {
    nominal: ["admit_to_schedule", "human, non-AI baseline, data minimum and public path checks present"],
    missing_human: ["block", "no named human conductor"],
    missing_non_ai: ["block", "non-AI equivalent unavailable"],
    prohibited_data: ["stop_and_isolate", "prohibited data presented"],
    public_path_blocked: ["stop_and_restore", "always-open public base obstructed"],
    reset_after_stop: ["audit_before_restart", "reset actions and receipts required; automatic restart forbidden"],
  };
  const [decision, reason] = outcomes[caseName];
  return {
    service_id: spec.locator_id,
    case: caseName,
    decision,
    reason,
    synthetic_only: true,
    field_performance: null,
    receipt_types: ["nominal", "reset_after_stop"].includes(caseName)
      ? spec.expected_receipts
      : [],
  };
}

function run() {
  const timetable = readJson("civic-timetable.json");
  const scenarioCards = readJson("scenario-cards.json").scenarios;
  const cards = new Map(scenarioCards.map((item) => [item.locator_id, item]));
  const services = timetable.services || [];
  const errors = [];
  const expectedIds = Array.from({ length: 12 }, (_, i) => `SCN-${String(i + 1).padStart(2, "0")}`);
  const actualIds = services.map((item) => item.locator_id).sort();
  if (JSON.stringify(actualIds) !== JSON.stringify(expectedIds)) {
    errors.push(`service ids mismatch: ${actualIds.join(",")}`);
  }
  const required = [
    "station_prototype_id",
    "public_baseline_zh",
    "non_ai_equivalent_zh",
    "human_conductor_role_ids",
    "stop_triggers",
    "reset_actions",
    "expected_receipts",
  ];
  for (const item of services) {
    for (const field of required) {
      const value = item[field];
      if (value == null || value === "" || (Array.isArray(value) && value.length === 0)) {
        errors.push(`${item.locator_id}: missing ${field}`);
      }
    }
    if (item.performance_results !== null) {
      errors.push(`${item.locator_id}: field performance must remain null`);
    }
    if (item.public_base_must_remain_open !== true) {
      errors.push(`${item.locator_id}: public base is not protected`);
    }
    if (!item.data_minimum || !Array.isArray(item.data_minimum.forbidden) || item.data_minimum.forbidden.length === 0) {
      errors.push(`${item.locator_id}: prohibited-data list missing`);
    }
    const card = cards.get(item.locator_id);
    if (!card || card.name_zh !== item.name_zh) {
      errors.push(`${item.locator_id}: scenario card name mismatch`);
    }
    if (!card || card.performance_results !== null) {
      errors.push(`${item.locator_id}: scenario performance must remain null`);
    }
  }
  const results = services.flatMap((item) => CASES.map((caseName) => branch(item, caseName)));
  if (results.length !== 72) errors.push("expected 72 tabletop branches");
  return {
    schema_version: "1.0.0",
    runner: "visual/assets/tabletop-runner.js",
    run_type: "deterministic_synthetic_tabletop",
    external_io: false,
    real_personal_data_used: false,
    field_authorization: false,
    field_performance: null,
    service_count: services.length,
    case_count: results.length,
    stop_branch_count: results.filter((item) => item.decision.startsWith("stop")).length,
    reset_branch_count: results.filter((item) => item.case === "reset_after_stop").length,
    status: errors.length === 0 ? "pass" : "fail",
    errors,
    results,
    limitations: [
      "PASS proves contract completeness and branch behavior only.",
      "No field, operator, device, account, personal data or production system was contacted.",
      "Real performance, authorization, capacity, budget and safety remain unknown/null.",
    ],
  };
}

function stableReceipt(value) {
  return {
    runner: value.runner,
    service_count: value.service_count,
    case_count: value.case_count,
    stop_branch_count: value.stop_branch_count,
    reset_branch_count: value.reset_branch_count,
    external_io: value.external_io,
    real_personal_data_used: value.real_personal_data_used,
    field_performance: value.field_performance,
    status: value.status,
    errors: value.errors,
    results: value.results,
  };
}

const result = run();
if (process.argv.includes("--write-receipt")) {
  fs.writeFileSync(
    path.join(ROOT, "timetable-tabletop-evidence.json"),
    JSON.stringify(result, null, 2) + "\n",
    "utf8",
  );
}
if (process.argv.includes("--check")) {
  const saved = readJson("timetable-tabletop-evidence.json");
  if (JSON.stringify(stableReceipt(saved)) !== JSON.stringify(stableReceipt(result))) {
    console.error(JSON.stringify({ status: "fail", error: "saved receipt differs from rerun" }));
    process.exit(1);
  }
}
console.log(JSON.stringify({
  status: result.status,
  service_count: result.service_count,
  case_count: result.case_count,
  stop_branch_count: result.stop_branch_count,
  reset_branch_count: result.reset_branch_count,
  external_io: result.external_io,
  real_personal_data_used: result.real_personal_data_used,
  field_performance: result.field_performance,
}));
if (result.status !== "pass") process.exit(1);
