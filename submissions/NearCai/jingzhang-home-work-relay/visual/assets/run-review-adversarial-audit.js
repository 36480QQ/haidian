"use strict";

const fs = require("fs");
const path = require("path");

const here = __dirname;
const root = path.resolve(here, "..", "..");
const outputPath = path.join(here, "review-adversarial-audit.validation.json");

function readJson(relPath) {
  return JSON.parse(fs.readFileSync(path.join(root, relPath), "utf8"));
}

function readText(relPath) {
  return fs.readFileSync(path.join(root, relPath), "utf8");
}

function unique(values) {
  return [...new Set(values)];
}

const checks = [];
function check(id, passed, details = {}) {
  checks.push({ id, passed: Boolean(passed), details });
}

const audit = readJson("visual/assets/review-adversarial-audit.json");
const scoreSprint = readJson("visual/assets/score-sprint-100-days.json");
const scenarioFixtures = readJson("visual/assets/scenario-negative-fixtures.json");
const scoreMap = readJson("visual/assets/review-score-evidence-map.json");
const relayContracts = readJson("visual/assets/relay-contracts.json");
const metrics = readJson("metrics.json").metrics;
const assumptions = readJson("assumptions.json").assumptions;
const manifest = readJson("manifest.json");
const proposalZh = readText("proposal.md");
const proposalEn = readText("proposal.en.md");
const reportZh = readText("report/proposal.html");
const reportEn = readText("report/proposal.en.html");
const visualZh = readText("visual/index.html");
const visualEn = readText("visual/index.en.html");

const expected = audit.expected_counts || {};
const measured = {
  review_score_dimension_count: Array.isArray(scoreMap.dimensions) ? scoreMap.dimensions.length : 0,
  first_100_days_action_count: Array.isArray(scoreSprint.actions) ? scoreSprint.actions.length : 0,
  commissioning_gate_count: Array.isArray(scoreSprint.gates) ? scoreSprint.gates.length : 0,
  raci_role_type_count: Array.isArray(scoreSprint.raci_role_types) ? scoreSprint.raci_role_types.length : 0,
  scene_contract_count: Array.isArray(scenarioFixtures.scene_contracts) ? scenarioFixtures.scene_contracts.length : 0,
  scenario_negative_fixture_branch_count: Array.isArray(scenarioFixtures.negative_branches) ? scenarioFixtures.negative_branches.length : 0,
  relay_contract_count: Array.isArray(relayContracts.contracts) ? relayContracts.contracts.length : 0,
  relay_state_count: Array.isArray(relayContracts.states) ? relayContracts.states.length : 0,
  relay_gate_count: Array.isArray(relayContracts.gates) ? relayContracts.gates.length : 0,
  adversarial_audit_probe_count: Array.isArray(audit.probes) ? audit.probes.length : 0,
  adversarial_negative_probe_count: Array.isArray(audit.probes) ? audit.probes.filter((probe) => probe.probe_type === "negative_guardrail").length : 0,
  authorized_field_action_count: Number(scoreSprint.coverage_summary && scoreSprint.coverage_summary.authorized_field_action_count),
  approved_budget_count: Number(scoreSprint.coverage_summary && scoreSprint.coverage_summary.approved_budget_count),
  professional_appointment_count: Number(scoreSprint.coverage_summary && scoreSprint.coverage_summary.professional_appointment_count),
  real_person_data_count: Number(scenarioFixtures.coverage_summary && scenarioFixtures.coverage_summary.real_person_data_count),
  ai_decision_authority_count: Number(scenarioFixtures.coverage_summary && scenarioFixtures.coverage_summary.ai_decision_authority_count),
};

Object.entries(expected).forEach(([metricId, expectedValue]) => {
  if (metricId === "remote_resource_violation_count") return;
  const metricValue = metrics[metricId] ? metrics[metricId].value : measured[metricId];
  const actual = measured[metricId] !== undefined ? measured[metricId] : metricValue;
  check(`count:${metricId}`, actual === expectedValue && (metricValue === undefined || metricValue === expectedValue), {
    expected: expectedValue,
    measured: actual,
    metrics_json: metricValue,
  });
});

const branchSceneIds = scenarioFixtures.negative_branches.map((branch) => branch.scene_id);
const scenesWithBranches = unique(branchSceneIds);
check("negative-branches:each-scene-has-six", scenarioFixtures.scene_contracts.every((scene) => branchSceneIds.filter((id) => id === scene.scene_id).length === 6), {
  scenes: scenarioFixtures.scene_contracts.length,
  scenes_with_branches: scenesWithBranches.length,
});

const remotePattern = /((src|href)=["']https?:\/\/|(src|href)=["']\/\/[A-Za-z0-9_.-]+|@import\s+url\(["']?https?:\/\/|<iframe\b|<form\b|fetch\s*\(|XMLHttpRequest|navigator\.sendBeacon|gtag\s*\(|analytics\.js|cdn\.[A-Za-z0-9_.-]+)/i;
const remoteViolations = [];
[
  ["visual/index.html", visualZh],
  ["visual/index.en.html", visualEn],
].forEach(([relPath, text]) => {
  text.split(/\r?\n/).forEach((line, index) => {
    if (remotePattern.test(line)) remoteViolations.push(`${relPath}:${index + 1}`);
  });
});
measured.remote_resource_violation_count = remoteViolations.length;
check("offline-html:no-remote-resource-or-tracking", remoteViolations.length === expected.remote_resource_violation_count, {
  expected: expected.remote_resource_violation_count,
  violations: remoteViolations,
});

const requiredAuditMarkersZh = [
  "[metric:adversarial_audit_probe_count]",
  "[metric:adversarial_negative_probe_count]",
  "[data:visual/assets/review-adversarial-audit.validation.json#checks]",
];
const requiredAuditMarkersEn = [
  "[metric:adversarial_audit_probe_count]",
  "[metric:adversarial_negative_probe_count]",
  "[data:visual/assets/review-adversarial-audit.validation.json#checks]",
];
check("proposal:bilingual-audit-markers", requiredAuditMarkersZh.every((marker) => proposalZh.includes(marker)) && requiredAuditMarkersEn.every((marker) => proposalEn.includes(marker)), {
  zh_missing: requiredAuditMarkersZh.filter((marker) => !proposalZh.includes(marker)),
  en_missing: requiredAuditMarkersEn.filter((marker) => !proposalEn.includes(marker)),
});

check("rendered-html:audit-markers-present", reportZh.includes('data-evidence-value="adversarial_audit_probe_count"') && reportEn.includes('data-evidence-value="adversarial_audit_probe_count"') && reportZh.includes('review-adversarial-audit.validation.json#checks') && reportEn.includes('review-adversarial-audit.validation.json#checks'), {});
check("proposal:visible-governance-boundaries", proposalZh.includes("unknown 不是 pass") && proposalEn.includes("unknown is not pass") && proposalZh.includes("AI 不决定") && proposalEn.includes("AI does not decide"), {});
check("visual:display-audit-metrics", visualZh.includes('data-metric="adversarial_audit_probe_count"') && visualEn.includes('data-metric="adversarial_audit_probe_count"'), {});
check("assumptions:audit-limitation-present", assumptions.some((item) => item.id === "A-ADVERSARIAL-AUDIT-001"), {});
check("manifest:ready-with-cover", manifest.package_state === "ready_for_review" && manifest.package_type === "professional_design_package" && manifest.cover_image === "assets/media/cover.webp", {
  package_state: manifest.package_state,
  package_type: manifest.package_type,
  cover_image: manifest.cover_image,
});
check("prohibited-claim-controls:zero-current-count", (audit.prohibited_claim_controls || []).every((item) => item.current_count === 0), {
  non_zero: (audit.prohibited_claim_controls || []).filter((item) => item.current_count !== 0).map((item) => item.control_id),
});

const passed = checks.every((item) => item.passed);
const output = {
  schema_version: "1.0.0",
  package_version: audit.package_version,
  validation_scope: "offline adversarial audit of package counts, negative denominator, visible bilingual anchors, offline HTML, and non-authorization boundaries",
  field_pilot_status: "not_authorized_not_run",
  result: passed ? "pass" : "fail",
  measured_counts: measured,
  checks,
  limitation: "A passing result means the submitted package keeps its desktop audit contract internally consistent. It does not establish official geometry, professional approval, legal authority, field performance, capacity, affordability, safety, equity or implementation feasibility.",
};

fs.writeFileSync(outputPath, `${JSON.stringify(output, null, 2)}\n`, "utf8");
if (!passed) {
  process.stderr.write(`${JSON.stringify(output, null, 2)}\n`);
  process.exit(1);
}
process.stdout.write(`${JSON.stringify(output, null, 2)}\n`);
