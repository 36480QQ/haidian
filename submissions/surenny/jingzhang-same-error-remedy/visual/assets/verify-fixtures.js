#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const payload = JSON.parse(
  fs.readFileSync(path.join(__dirname, "synthetic-test-fixtures.json"), "utf8"),
);
const failures = [];
const fixtures = payload.fixtures;

if (fixtures.length !== 60) failures.push("fixture count");
if (fixtures.filter((item) => item.synthetic_fields.frozen_rule_version === "ERR-V7").length !== 12) failures.push("shared-version count");
if (fixtures.filter((item) => item.synthetic_fields.complaint_present).length !== 1) failures.push("complainant count");
if (fixtures.filter((item) => !item.synthetic_fields.required_scope_field_complete).length !== 4) failures.push("ambiguity count");

for (const fixture of fixtures) {
  if (JSON.stringify(fixture.expected) !== JSON.stringify(fixture.actual) || fixture.result !== "pass") {
    failures.push(fixture.fixture_id);
  }
}
for (const suite of payload.test_suites) {
  if (JSON.stringify(suite.expected) !== JSON.stringify(suite.actual) || suite.result !== "pass" || !suite.failure_branch) {
    failures.push(suite.test_id);
  }
}

if (failures.length) {
  console.error(`FAIL: ${failures.join(", ")}`);
  process.exit(1);
}
console.log("PASS: 60 row-level fixtures and four expected/actual/failure suites verified");
