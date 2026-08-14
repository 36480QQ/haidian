/* Jingzhang Rising AI Examination validator. No network or external dependency. */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.JZExam = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";
  const FIELDS = ["F1", "F2", "F3", "F4", "F5", "F6"];
  const HUMAN = ["H1", "H2", "H3", "H4", "H5"];
  const GATES = ["G0", "G1", "G2", "G3", "G4", "G5"];
  function text(value) { return typeof value === "string" && value.trim().length > 0; }
  function validateContract(contract) {
    const failures = [];
    if (!contract || typeof contract !== "object") return {classification:"blocked", failures:["contract_missing"]};
    if (!text(contract.scenario_id)) failures.push("scenario_id_missing");
    if (contract.current_status !== "concept_not_authorized_not_operating") failures.push("status_must_remain_unapproved");
    if (!Array.isArray(contract.responsible_roles_zh) || contract.responsible_roles_zh.length < 2) failures.push("responsibility_missing");
    for (const id of FIELDS) {
      if (!contract.report_card || !contract.report_card[id] || !text(contract.report_card[id].value_zh)) failures.push(id + "_missing");
    }
    for (const id of HUMAN) {
      if (!contract.human_lane || !contract.human_lane[id] || !text(contract.human_lane[id].value_zh)) failures.push(id + "_missing");
    }
    for (const id of GATES) {
      if (!contract.evidence_gates || !text(contract.evidence_gates[id])) failures.push(id + "_missing");
    }
    return {
      classification: failures.length ? "blocked" : "protocol_ready_not_authorized",
      failures
    };
  }
  function removePath(target, path) {
    const parts = path.split(".");
    let cursor = target;
    for (let i = 0; i < parts.length - 1; i++) {
      if (!cursor || typeof cursor !== "object") return;
      cursor = cursor[parts[i]];
    }
    if (cursor && typeof cursor === "object") delete cursor[parts[parts.length - 1]];
  }
  function clone(value) { return JSON.parse(JSON.stringify(value)); }
  function runCases(contracts, cases) {
    const byId = Object.fromEntries(contracts.map(item => [item.scenario_id, item]));
    const receipts = [];
    for (const test of cases) {
      const candidate = clone(byId[test.scenario_id]);
      if (test.remove_path) removePath(candidate, test.remove_path);
      const actual = validateContract(candidate);
      receipts.push({
        case_id: test.case_id,
        scenario_id: test.scenario_id,
        expected: test.expected,
        actual: actual.classification,
        pass: test.expected === actual.classification,
        failures: actual.failures
      });
    }
    return receipts;
  }
  return {FIELDS, HUMAN, GATES, validateContract, removePath, clone, runCases};
});

if (typeof require === "function" && require.main === module) {
  const fs = require("fs");
  const contracts = JSON.parse(fs.readFileSync(process.argv[2], "utf8")).contracts;
  const cases = JSON.parse(fs.readFileSync(process.argv[3], "utf8")).cases;
  const receipts = module.exports.runCases(contracts, cases);
  const summary = {
    total_cases: receipts.length,
    passed_cases: receipts.filter(item => item.pass).length,
    protocol_ready_cases: receipts.filter(item => item.actual === "protocol_ready_not_authorized").length,
    blocked_negative_cases: receipts.filter(item => item.expected === "blocked" && item.actual === "blocked").length,
    unexpected_cases: receipts.filter(item => !item.pass).length,
    receipts
  };
  process.stdout.write(JSON.stringify(summary, null, 2) + "\n");
}
