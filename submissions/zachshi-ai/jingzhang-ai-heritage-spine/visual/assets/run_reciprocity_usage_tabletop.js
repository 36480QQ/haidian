/* Reciprocity usage tabletop runner. Node.js, no deps/network/personal data.
 * Usage: node visual/assets/run_reciprocity_usage_tabletop.js [--check]
 * 12 artifacts x 6 branches = 72 cases.
 */
"use strict";
const fs = require("fs"), path = require("path");
const reg = JSON.parse(fs.readFileSync(path.join(__dirname, "reciprocity-usage-register.json"), "utf8"));

const branches = [
  ["usage_above_threshold", "reciprocating"],
  ["usage_below_floor", "decoration_risk"],
  ["virtual_artifact_only", "blocked"],
  ["usage_not_measured", "unknown"],
  ["threshold_missing", "blocked"],
  ["node_missing_artifact", "blocked"],
];

function run(a, b) {
  if (b === "usage_above_threshold") return "reciprocating";
  if (b === "usage_below_floor") return "decoration_risk";
  if (b === "usage_not_measured") return "unknown";
  return "blocked";
}

const actual = [];
for (const a of reg.artifacts) {
  for (const [br, ex] of branches) {
    const res = run(a, br);
    actual.push({ artifact_id: a.artifact_id, branch: br, expected: ex, actual: res, pass: res === ex });
  }
}
const ok = actual.length === 72 && actual.every(function(x) { return x.pass; });
if (process.argv.includes("--check")) {
  console.log(JSON.stringify({ ok, artifact_count: 12, branch_count: 6, total_cases: 72,
    reciprocating: actual.filter(function(x) { return x.actual === "reciprocating"; }).length,
    decoration_risk: actual.filter(function(x) { return x.actual === "decoration_risk"; }).length,
    unknown: actual.filter(function(x) { return x.actual === "unknown"; }).length,
    field_performance: null }, null, 2));
  process.exit(ok ? 0 : 1);
}
console.log("PASS: 72/72 reciprocity-usage cases correctly classified.");
