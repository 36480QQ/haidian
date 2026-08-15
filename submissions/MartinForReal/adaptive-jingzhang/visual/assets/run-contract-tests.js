#!/usr/bin/env node
"use strict";

// Participant-local contract suite for the Adaptive Jing-Zhang v0.3 regeneration.
//
// Every changelog Class C checkbox is closed only by a named artifact existing plus the
// named case here passing. The suite is failing-first: cases for artifacts that are not
// built yet fail until they are, and none of them may be weakened to make a run green.
// It is read-only — each builder is spawned in --check mode, so a green run also proves
// every generated file on disk already matches its source of truth.
//
// This is not, and does not stand in for, the repository validator or the independent
// audit. It only checks what this package can check about itself.
//
// Usage: node run-contract-tests.js
// Exit 0 when every case passes, 1 when any case fails, 2 on harness error.

const crypto = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");
const { spawnSync } = require("node:child_process");

const ASSETS = __dirname;
const PACKAGE_ROOT = path.resolve(ASSETS, "..", "..");

const FROZEN_SHA256 = {
  "visual/assets/physarum-inputs.json": "5e5a9be65bb122617798bf488f12fc5838dfba46aead6d824b679b48db718d53",
  "visual/assets/physarum-runs.json": "ea93df307c30bd90024438ed1dc4704a4e7bec8f4b456a7ec323c914ea4e06fe",
};

// The approved lifecycle removes both specification artifacts before any contract test
// or build runs, so their continued presence is itself a failure.
const REMOVED_SPEC_ARTIFACTS = ["regeneration-design.md", "v0.3-implementation-plan.md"];

// Transcribed from the repository validator, which matches required sections by
// substring containment. Held here as the external contract rather than read back out
// of the package, so the package cannot satisfy the test by redefining it.
const REQUIRED_SECTIONS_ZH = [
  "设计依据与资料清单",
  "三层范围工作框架",
  "统筹研究范围产业与未来城市研究",
  "总体设计范围城市更新与控规深度城市设计",
  "重点区域详细设计",
  "AI 创新生态、人才画像与 AI+ 场景",
  "用地、建筑规模与拆改留方案",
  "交通、轨道、市政与公共服务设施",
  "蓝绿空间、公共空间与城市风貌",
  "更新项目清单、实施政策与分期计划",
  "指标体系、面积复算与合规矩阵",
  "风险、版权与合规说明",
  "参考资料",
];
const REQUIRED_SECTIONS_EN = [
  "Design Basis and Source List",
  "Three-Level Scope Framework",
  "Coordinated Research Area: Industry and Future City Research",
  "Overall Design Area: Urban Renewal and Regulatory-Plan-Level Urban Design",
  "Detailed Design of Key Areas",
  "AI Innovation Ecosystem, Personas, and AI+ Scenarios",
  "Land Use, Building Scale, and Retain-Renovate-Demolish Strategy",
  "Transport, Rail, Municipal Infrastructure, and Public Services",
  "Blue-Green Network, Public Space, and Urban Character",
  "Renewal Projects, Implementation Policy, and Phasing",
  "Metrics, Area Recalculation, and Compliance Matrix",
  "Risk, Copyright, and Compliance",
  "References",
];

// Five semantic plates per key area, each published as a Chinese raster and a separate
// English twin. The superseded architecture had ten combined bilingual infographics per
// area; that count is gone from this file so a stale row cannot pass against it.
const SEMANTIC_PLATES_PER_AREA = 5;

const results = [];

function readText(relative) {
  return fs.readFileSync(path.join(PACKAGE_ROOT, relative), "utf8");
}

function readJson(relative) {
  return JSON.parse(readText(relative));
}

function exists(relative) {
  return fs.existsSync(path.join(PACKAGE_ROOT, relative));
}

function check(id, description, run) {
  const problems = [];
  let detail = null;
  try {
    detail = run((message) => problems.push(message)) ?? null;
  } catch (error) {
    problems.push(error instanceof Error ? error.message : String(error));
  }
  results.push({
    id,
    description,
    status: problems.length === 0 ? "PASS" : "FAIL",
    problems,
    detail,
  });
}

function duplicateIdentifiers(values) {
  const counts = new Map();
  for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);
  return [...counts.entries()]
    .filter((entry) => entry[1] > 1)
    .map(([id, count]) => ({ id, count }))
    .sort((left, right) => String(left.id).localeCompare(String(right.id)));
}

function auditIdentifierNamespaces(caseIds, reservedEntries) {
  const duplicateCaseIds = duplicateIdentifiers(caseIds);
  const duplicateReservedIds = duplicateIdentifiers(reservedEntries.map((entry) => entry.id)).map((duplicate) => ({
    ...duplicate,
    namespaces: reservedEntries.filter((entry) => entry.id === duplicate.id).map((entry) => entry.namespace),
  }));
  const reservedIds = new Set(reservedEntries.map((entry) => entry.id));
  const reservedCaseCollisions = [...new Set(caseIds.filter((id) => reservedIds.has(id)))].sort();
  return {
    duplicate_case_ids: duplicateCaseIds,
    duplicate_reserved_ids: duplicateReservedIds,
    reserved_case_collisions: reservedCaseCollisions,
  };
}

function runNode(scriptRelative, args = []) {
  const result = spawnSync(process.execPath, [path.join(PACKAGE_ROOT, scriptRelative), ...args], {
    encoding: "utf8",
    cwd: PACKAGE_ROOT,
    maxBuffer: 64 * 1024 * 1024,
  });
  if (result.error) throw result.error;
  let payload = null;
  try {
    payload = JSON.parse(result.stdout);
  } catch {
    throw new Error(`${scriptRelative} did not emit JSON: ${result.stdout.slice(0, 300)}`);
  }
  return { exitCode: result.status, payload };
}

check("L01", "both specification artifacts are removed from the package root", (fail) => {
  const present = REMOVED_SPEC_ARTIFACTS.filter((name) => exists(name));
  for (const name of present) fail(`${name} is still present; no build or test may run before it is removed`);
  return { present };
});

check("F01", "both frozen ensemble assets are byte-identical to their recorded hashes", (fail) => {
  const observed = {};
  for (const [relative, expected] of Object.entries(FROZEN_SHA256)) {
    const actual = crypto.createHash("sha256")
      .update(fs.readFileSync(path.join(PACKAGE_ROOT, relative)))
      .digest("hex");
    observed[relative] = actual;
    if (actual !== expected) fail(`${relative} changed: ${actual}`);
  }
  return observed;
});

check("R01", "the reproducer recomputes the published record with zero mismatches", (fail) => {
  const { exitCode, payload } = runNode("visual/assets/reproduce_physarum.js");
  if (exitCode !== 0) fail(`expected exit 0, got ${exitCode}`);
  if (payload.status !== "PASS") fail(`expected PASS, got ${payload.status}`);
  if (payload.summary?.comparisons !== 633) fail(`expected 633 comparisons, got ${payload.summary?.comparisons}`);
  if (payload.comparison_counts?.derived_metrics !== 7) {
    fail(`expected 7 derived metrics, got ${payload.comparison_counts?.derived_metrics}`);
  }
  if (payload.mismatch_count !== 0) fail(`expected 0 mismatches, got ${payload.mismatch_count}`);
  if (payload.summary?.selected_edges_per_run !== 11) {
    fail(`expected 11 selected edges per run, got ${payload.summary?.selected_edges_per_run}`);
  }
  return {
    comparisons: payload.summary?.comparisons,
    derived_metrics: payload.comparison_counts?.derived_metrics,
    mismatch_count: payload.mismatch_count,
  };
});

check("R02", "the isolated tamper suite proves the reproducer detects a corrupted record", (fail) => {
  const { exitCode, payload } = runNode("visual/assets/test-reproducer-tamper.js");
  if (exitCode !== 0) fail(`expected exit 0, got ${exitCode}`);
  if (payload.status !== "PASS") fail(`expected PASS, got ${payload.status}`);
  if (!Array.isArray(payload.failures) || payload.failures.length !== 0) {
    fail(`expected zero tamper failures, got ${JSON.stringify(payload.failures)}`);
  }
  if (payload.cases_run !== 15) fail(`expected 15 cases, got ${payload.cases_run}`);
  if (payload.frozen_assets_unchanged !== true) fail("the tamper suite did not restore the frozen assets");
  return { cases_run: payload.cases_run };
});

// The canonical strings this suite defends, restated here rather than imported.
// A regression that edits the method card and the reproducer together is exactly
// the regression worth catching, and a test that reads the same file the builder
// writes cannot catch it: it would agree with whatever the drift produced. These
// literals are the independent record of what the package is allowed to claim.
const CANONICAL_METHOD_NAME_EN =
  "Seeded Kruskal minimum-spanning-tree topology and selection-instability probe "
  + "over hand-declared candidate edges.";
const CANONICAL_METHOD_NAME_ZH =
  "在人工声明的候选边上运行的带种子 Kruskal 最小生成树拓扑与选择不稳定性探针。";
const CANONICAL_GUARANTEED_BY_CONSTRUCTION =
  "connectivity of each run, and exactly 11 selected edges per run";
const CANONICAL_NOT_COMPUTED_EN = [
  "movement",
  "demand",
  "engineering feasibility",
  "accessibility",
  "biological adaptation",
  "public preference",
  "optimality for Beijing",
];
const CANONICAL_NOT_COMPUTED_ZH = [
  "出行",
  "需求",
  "工程可行性",
  "无障碍水平",
  "生物适应",
  "公众偏好",
  "对北京的最优性",
];
// The four selection-frequency thresholds, as components rather than as one blob,
// so a record that publishes three of them and drops the fourth still fails.
const CANONICAL_THRESHOLDS = {
  persistent_min_frequency: 0.7,
  highest_disagreement_frequency: 0.6875,
  mid_disagreement_frequency: 0.5,
  disagreement_min_frequency: 0.35,
};
// The coordinate scale is a declared constant of the method. The reproducer must
// keep saying so: an earlier revision described these two numbers as having been
// fitted from the published edge lengths, which the executable has never done.
const CANONICAL_X_SCALE_M = 1374.006827;
const CANONICAL_Y_SCALE_M = 9723.469847;
const RETRACTED_SCALE_PHRASES = ["solved back out", "反解"];

function pinList(fail, label, actual, expected) {
  const got = actual ?? [];
  if (got.length !== expected.length) {
    return fail(`${label} has ${got.length} entries, expected exactly ${expected.length}`);
  }
  expected.forEach((value, index) => {
    if (got[index] !== value) {
      fail(`${label}[${index}] is ${JSON.stringify(got[index])}, expected ${JSON.stringify(value)}`);
    }
  });
  return undefined;
}

check("R03", "the reproducer names the method it performs and what it does not compute", (fail) => {
  const { payload } = runNode("visual/assets/reproduce_physarum.js");
  const contract = payload.runtime_contract ?? {};
  if (!/seeded Kruskal/i.test(contract.method_name ?? "")) {
    fail(`runtime_contract.method_name does not name a seeded Kruskal method: ${contract.method_name}`);
  }
  if (contract.method_name !== CANONICAL_METHOD_NAME_EN) {
    fail(`runtime_contract.method_name is not the canonical English method name: ${contract.method_name}`);
  }
  if (contract.method_name_zh !== CANONICAL_METHOD_NAME_ZH) {
    fail(`runtime_contract.method_name_zh is not the canonical Chinese method name: ${contract.method_name_zh}`);
  }
  if (!/11 selected edges/.test(contract.guaranteed_by_construction ?? "")) {
    fail("runtime_contract does not state that 11 selected edges are guaranteed by construction");
  }
  if (contract.guaranteed_by_construction !== CANONICAL_GUARANTEED_BY_CONSTRUCTION) {
    fail("runtime_contract.guaranteed_by_construction is not the canonical sentence: "
      + `${contract.guaranteed_by_construction}`);
  }
  const notComputed = contract.not_computed ?? [];
  if (notComputed.length !== 7) fail(`expected 7 not_computed entries, got ${notComputed.length}`);
  pinList(fail, "runtime_contract.not_computed", notComputed, CANONICAL_NOT_COMPUTED_EN);

  // The scale constants are executable and fixed. Pinning the numbers and the
  // sentence together is what stops the package drifting back to describing them
  // as a fit while the code keeps not fitting them.
  const basis = contract.coordinate_basis ?? {};
  if (basis.x_scale_m !== CANONICAL_X_SCALE_M) {
    fail(`coordinate_basis.x_scale_m is ${basis.x_scale_m}, expected ${CANONICAL_X_SCALE_M}`);
  }
  if (basis.y_scale_m !== CANONICAL_Y_SCALE_M) {
    fail(`coordinate_basis.y_scale_m is ${basis.y_scale_m}, expected ${CANONICAL_Y_SCALE_M}`);
  }
  if (!/never re-fits/.test(basis.declared_as ?? "")) {
    fail(`coordinate_basis.declared_as does not state that the reproducer never re-fits: ${basis.declared_as}`);
  }
  for (const phrase of RETRACTED_SCALE_PHRASES) {
    if (JSON.stringify(basis).includes(phrase)) {
      fail(`coordinate_basis repeats the retracted claim ${JSON.stringify(phrase)}`);
    }
  }

  const card = readJson("visual/assets/regeneration-source.json").method_card;
  for (const [language, list] of [["en", card.does_not_compute_en], ["zh", card.does_not_compute_zh]]) {
    if (list.length !== 7) fail(`method_card does_not_compute_${language} has ${list.length} entries, expected 7`);
  }
  pinList(fail, "method_card.does_not_compute_en", card.does_not_compute_en, CANONICAL_NOT_COMPUTED_EN);
  pinList(fail, "method_card.does_not_compute_zh", card.does_not_compute_zh, CANONICAL_NOT_COMPUTED_ZH);
  if (card.name_en !== CANONICAL_METHOD_NAME_EN) {
    fail(`method_card.name_en is not the canonical English method name: ${card.name_en}`);
  }
  if (card.name_zh !== CANONICAL_METHOD_NAME_ZH) {
    fail(`method_card.name_zh is not the canonical Chinese method name: ${card.name_zh}`);
  }

  const thresholds = card.thresholds;
  const expected = CANONICAL_THRESHOLDS;
  for (const [key, value] of Object.entries(expected)) {
    if (thresholds[key] !== value) fail(`threshold ${key} is ${thresholds[key]}, expected ${value}`);
  }
  return { method_name: contract.method_name, thresholds };
});

check("Z01", "the zero-jitter comparison is published for every candidate edge", (fail) => {
  const relative = "visual/assets/physarum-zero-jitter-ablation.json";
  if (!exists(relative)) return fail(`${relative} does not exist`);
  const record = readJson(relative);
  const rows = record.edges ?? [];
  if (rows.length !== 24) fail(`expected 24 candidate edges, found ${rows.length}`);
  for (const row of rows) {
    for (const field of ["edge_id", "primary_frequency", "zero_jitter_frequency", "delta"]) {
      if (row[field] === undefined || row[field] === null) fail(`${row.edge_id ?? "?"} is missing ${field}`);
    }
    const delta = Number((row.zero_jitter_frequency - row.primary_frequency).toFixed(6));
    if (Math.abs(delta - row.delta) > 1e-9) fail(`${row.edge_id} delta ${row.delta} does not equal the difference ${delta}`);
  }
  if (record.thresholds?.highest_disagreement_frequency !== 0.6875) {
    fail("the ablation record does not publish the 0.6875 threshold");
  }
  if (record.thresholds?.mid_disagreement_frequency !== 0.5) {
    fail("the ablation record does not publish the 0.50 threshold");
  }
  // Every threshold component, not only the two the band chart happens to draw.
  for (const [key, value] of Object.entries(CANONICAL_THRESHOLDS)) {
    if (record.thresholds?.[key] !== value) {
      fail(`ablation threshold ${key} is ${record.thresholds?.[key]}, expected ${value}`);
    }
  }
  if (!record.limitations_en || !record.limitations_zh) fail("the ablation record states no bilingual limitations");

  // The record calls its zero-jitter persistence graph connected. That claim is
  // checked here against the frozen edge list rather than believed: the eleven
  // persistent edges are unioned over their own endpoints and the components are
  // counted. A record that keeps the word and loses the property fails.
  const persistent = rows
    .filter((row) => row.zero_jitter_frequency >= CANONICAL_THRESHOLDS.persistent_min_frequency)
    .map((row) => row.edge_id);
  if (persistent.length !== record.summary?.zero_jitter_persistent_edges) {
    fail(`summary.zero_jitter_persistent_edges is ${record.summary?.zero_jitter_persistent_edges}, `
      + `but ${persistent.length} rows reach the ${CANONICAL_THRESHOLDS.persistent_min_frequency} threshold`);
  }
  if (persistent.length !== 11) {
    fail(`expected 11 zero-jitter persistent edges, found ${persistent.length}`);
  }
  const inputs = readJson("visual/assets/physarum-inputs.json");
  const byId = new Map((inputs.edges ?? []).map((edge) => [edge.id, edge]));
  const parent = new Map((inputs.nodes ?? []).map((node) => [node.id, node.id]));
  const find = (node) => {
    let root = node;
    while (parent.get(root) !== root) root = parent.get(root);
    return root;
  };
  for (const edgeId of persistent) {
    const edge = byId.get(edgeId);
    if (!edge) {
      fail(`persistent edge ${edgeId} is not present in the frozen candidate edge list`);
      continue;
    }
    parent.set(find(edge.a), find(edge.b));
  }
  const components = new Set([...parent.keys()].map(find));
  const connected = components.size === 1;
  if (record.summary?.zero_jitter_persistence_graph !== (connected ? "connected" : "disconnected")) {
    fail(`summary.zero_jitter_persistence_graph says ${record.summary?.zero_jitter_persistence_graph}, `
      + `but the persistent edges span ${components.size} component(s) over ${parent.size} nodes`);
  }
  if (!connected) {
    fail(`the zero-jitter persistent edges do not connect all ${parent.size} nodes: `
      + `${components.size} components`);
  }

  // The anisotropy limitation must name both fixed constants and must not carry
  // the retracted description of them as a fit.
  for (const [language, list] of [["en", record.limitations_en], ["zh", record.limitations_zh]]) {
    if (list.length !== 4) fail(`limitations_${language} has ${list.length} entries, expected 4`);
    const joined = list.join(" ");
    for (const phrase of RETRACTED_SCALE_PHRASES) {
      if (joined.includes(phrase)) {
        fail(`limitations_${language} repeats the retracted claim ${JSON.stringify(phrase)}`);
      }
    }
    for (const constant of [CANONICAL_X_SCALE_M, CANONICAL_Y_SCALE_M]) {
      if (!joined.includes(String(constant))) {
        fail(`limitations_${language} does not state the fixed scale constant ${constant}`);
      }
    }
  }
  return { edges: rows.length, persistent_edges: persistent.length, components: components.size };
});

for (const [id, script] of [
  ["B01", "visual/assets/build-proposals.js"],
  ["B02", "visual/assets/build-sources.js"],
  ["B03", "visual/assets/build-standards.js"],
]) {
  check(id, `${path.basename(script)} reports the package already matches its source of truth`, (fail) => {
    const { exitCode, payload } = runNode(script, ["--check"]);
    if (payload.status !== "PASS") fail(`expected PASS, got ${payload.status}: ${JSON.stringify(payload.failures)}`);
    if (exitCode !== 0) fail(`expected exit 0 (nothing left to regenerate), got ${exitCode}`);
    return { changed: payload.changed ?? payload.changed_files };
  });
}

check("S01", "sources.json holds exactly 41 unique records with the bibliographic field shape", (fail) => {
  const bibliography = readJson("visual/assets/source-bibliography.json");
  const records = readJson("sources.json").sources;
  const expected = bibliography.count_contract.closed_final_total;
  if (expected !== 41) fail(`the count contract is ${expected}, but the closed inventory is 41`);
  if (records.length !== expected) fail(`expected ${expected} records, found ${records.length}`);
  const ids = records.map((record) => record.id);
  const duplicates = ids.filter((id, index) => ids.indexOf(id) !== index);
  if (duplicates.length > 0) fail(`duplicate source ids: ${duplicates.join(", ")}`);
  const missingShape = records
    .filter((record) => !("title" in record) || !("author_or_issuer" in record) || !("year" in record))
    .map((record) => record.id);
  if (missingShape.length > 0) fail(`records missing the bibliographic field shape: ${missingShape.join(", ")}`);
  const unresolved = records.filter((record) => record.bibliographic_status === "not_transcribed_from_source");
  return { records: records.length, preserved_unknown_bibliographies: unresolved.length };
});

check("S02", "the meteorological record stays registered but unselected, so nothing derives from it", (fail) => {
  const record = readJson("sources.json").sources
    .find((item) => item.id === "BEIJING-METEOROLOGICAL-SEASONAL-QUALIFICATION");
  if (!record) return fail("the frozen meteorological identifier is not registered");
  if (record.selection_status !== "not_selected") {
    fail(`selection_status must remain not_selected, found ${record.selection_status}`);
  }
  for (const field of ["url", "title", "author_or_issuer", "year"]) {
    if (record[field] !== null) {
      fail(`${field} must stay null while no source is selected, found ${JSON.stringify(record[field])}`);
    }
  }
  if (record.task_state !== "open") fail("C06 must remain open while no source is selected");
  return { selection_status: record.selection_status, task_state: record.task_state };
});

check("M01", "no unsupported evidence marker survives into any authored or rendered document", (fail) => {
  const counts = {};
  for (const file of ["proposal.md", "proposal.en.md", "report/proposal.html", "report/proposal.en.html"]) {
    const occurrences = (readText(file).match(/\[assumption:/g) || []).length;
    counts[file] = occurrences;
    if (occurrences !== 0) fail(`${file} still exposes ${occurrences} literal [assumption: markers`);
  }
  return counts;
});

check("M02", "both proposals name the computation and state what it does not compute", (fail) => {
  const expectations = [
    ["proposal.md", ["Kruskal", "由算法构造保证", "不计算出行"]],
    ["proposal.en.md", ["seeded Kruskal", "guaranteed by construction", "does not compute movement"]],
  ];
  const found = {};
  for (const [file, phrases] of expectations) {
    const body = readText(file);
    found[file] = phrases.filter((phrase) => body.includes(phrase));
    for (const phrase of phrases) {
      if (!body.includes(phrase)) fail(`${file} does not contain "${phrase}"`);
    }
  }
  return found;
});

check("E01", "every validator-required section heading is present in the matching language", (fail) => {
  const counts = {};
  for (const [file, required] of [["proposal.md", REQUIRED_SECTIONS_ZH], ["proposal.en.md", REQUIRED_SECTIONS_EN]]) {
    const headings = readText(file).split("\n").filter((line) => line.startsWith("## ")).map((line) => line.slice(3));
    const missing = required.filter((section) => !headings.some((heading) => heading.includes(section)));
    counts[file] = { headings: headings.length, missing };
    for (const section of missing) fail(`${file} is missing required section \`## ${section}\``);
  }
  return counts;
});

check("L02", "the three labs couple through exactly three declared channels", (fail) => {
  const coupling = readJson("visual/assets/regeneration-source.json").lab_coupling;
  if (coupling.channel_count !== 3) fail(`channel_count must be 3, found ${coupling.channel_count}`);
  if (coupling.channels.length !== 3) fail(`expected 3 channel records, found ${coupling.channels.length}`);
  for (const channel of coupling.channels) {
    for (const field of ["name_zh", "name_en", "definition_zh", "definition_en"]) {
      if (!channel[field]) fail(`${channel.id} is missing ${field}`);
    }
  }
  return { ids: coupling.channels.map((channel) => channel.id) };
});

check("A01", "Dazhongsi stays non-station and non-georeferenced in the record and the geometry", (fail) => {
  const area = readJson("visual/assets/regeneration-source.json").areas.find((item) => item.id === "PROV-KEY-003");
  if (!area) return fail("PROV-KEY-003 is not declared in the bilingual record");
  if (area.georeferenced !== false) fail("PROV-KEY-003 must remain non-georeferenced");
  for (const field of ["non_station_note_zh", "non_station_note_en", "source_id"]) {
    if (!area[field]) fail(`PROV-KEY-003 is missing ${field}`);
  }
  for (const term of ["entrance", "road", "crossing", "parcel", "distance", "station relationship"]) {
    if (!area.non_station_note_en.includes(term)) fail(`the disclaimer does not explicitly cover "${term}"`);
  }

  // The same position claim has to appear on the geometry a reviewer opens directly.
  const features = readJson("geometry/key_areas.geojson").features;
  const stamped = {};
  for (const feature of features) {
    const properties = feature.properties;
    const declared = readJson("visual/assets/regeneration-source.json").areas
      .find((item) => item.id === properties.id);
    if (!declared) {
      fail(`${properties.id} has geometry but no bilingual record`);
      continue;
    }
    stamped[properties.id] = properties.georeferenced;
    if (properties.georeferenced !== declared.georeferenced) {
      fail(`${properties.id} geometry declares georeferenced ${properties.georeferenced}, record says ${declared.georeferenced}`);
    }
    if (declared.georeferenced === false && properties.positional_claim !== "void") {
      fail(`${properties.id} must carry positional_claim "void", found ${properties.positional_claim}`);
    }
    if (declared.georeferenced === false && !properties.non_station_note_en) {
      fail(`${properties.id} geometry carries no non-station note`);
    }
  }
  return { stamped };
});

check("A02", "twelve actions P00-P11 are declared with a phase each", (fail) => {
  const projects = readJson("visual/assets/regeneration-source.json").projects;
  const ids = projects.map((project) => project.id);
  for (let index = 0; index < 12; index += 1) {
    const id = `P${String(index).padStart(2, "0")}`;
    if (!ids.includes(id)) fail(`${id} is not declared`);
  }
  if (projects.length !== 12) fail(`expected 12 actions, found ${projects.length}`);
  for (const project of projects) {
    for (const field of ["name_zh", "name_en", "phase"]) {
      if (!project[field]) fail(`${project.id} is missing ${field}`);
    }
  }
  return { count: projects.length };
});

check("A03", "each key area carries distinct detailed-design content with stable ids", (fail) => {
  const areas = readJson("visual/assets/regeneration-source.json").areas;
  if (areas.length !== 3) fail(`expected 3 key areas, found ${areas.length}`);
  const componentIds = new Set();
  const routeIds = new Set();
  const detail = {};
  for (const area of areas) {
    const label = area.id;
    const components = area.components ?? [];
    const routes = area.routes ?? [];
    if (components.length === 0) fail(`${label} declares no components`);
    if (routes.length === 0) fail(`${label} declares no routes`);
    for (const component of components) {
      for (const field of ["id", "name_zh", "name_en", "evidence_ref"]) {
        if (!component[field]) fail(`${label} component ${component.id ?? "?"} is missing ${field}`);
      }
      if (componentIds.has(component.id)) fail(`component id ${component.id} is reused across areas`);
      componentIds.add(component.id);
    }
    for (const route of routes) {
      for (const field of ["id", "name_zh", "name_en", "step_free", "evidence_ref"]) {
        if (route[field] === undefined || route[field] === null || route[field] === "") {
          fail(`${label} route ${route.id ?? "?"} is missing ${field}`);
        }
      }
      if (routeIds.has(route.id)) fail(`route id ${route.id} is reused across areas`);
      routeIds.add(route.id);
    }
    // A step-free chain is only continuous if every leg of it is step-free.
    if (routes.length > 0 && !routes.every((route) => route.step_free === true)) {
      fail(`${label} declares a route that breaks the continuous step-free chain`);
    }
    for (const field of ["winter_zh", "winter_en", "maintenance_zh", "maintenance_en", "phase1_envelope"]) {
      if (!area[field]) fail(`${label} is missing ${field}`);
    }
    const envelope = area.phase1_envelope ?? {};
    for (const field of ["id", "description_zh", "description_en", "reversible", "authorization_state"]) {
      if (envelope[field] === undefined || envelope[field] === null || envelope[field] === "") {
        fail(`${label} phase1_envelope is missing ${field}`);
      }
    }
    detail[label] = { components: components.length, routes: routes.length };
  }
  // Distinct content, not one description repeated three times.
  const roles = new Set(areas.map((area) => area.role_en));
  if (roles.size !== areas.length) fail("two key areas share the same role, so they are not distinct labs");
  return detail;
});

// The plate architecture itself is checked by the nine key-area tests wired in below, which
// read the shared contract module rather than restating counts here. This case only holds
// the line that the registry is the new thirty-artifact shape and not the old plate list.
check("V01", "the plate registry is the thirty-artifact bilingual-pair shape", (fail) => {
  const relative = "visual/assets/area-plates.json";
  if (!exists(relative)) return fail(`${relative} does not exist`);
  const registry = readJson(relative);
  if (registry.plates !== undefined) {
    fail("area-plates.json still carries a `plates` list; the combined-infographic architecture is rejected");
  }
  const artifacts = registry.artifacts ?? [];
  if (artifacts.length !== 30) fail(`expected 30 artifact records, found ${artifacts.length}`);
  const perArea = {};
  const plateIds = new Set();
  for (const record of artifacts) {
    perArea[record.area_feature_id] = (perArea[record.area_feature_id] ?? 0) + 1;
    if (record.plate_id) plateIds.add(record.plate_id);
  }
  for (const [areaId, count] of Object.entries(perArea)) {
    if (count !== SEMANTIC_PLATES_PER_AREA * 2) {
      fail(`${areaId} has ${count} artifacts, expected ${SEMANTIC_PLATES_PER_AREA * 2}`);
    }
  }
  if (Object.keys(perArea).length !== 3) fail(`artifacts cover ${Object.keys(perArea).length} areas, expected 3`);
  if (plateIds.size !== SEMANTIC_PLATES_PER_AREA * 3) {
    fail(`the registry names ${plateIds.size} semantic plates, expected ${SEMANTIC_PLATES_PER_AREA * 3}`);
  }
  return { artifacts: artifacts.length, semantic_plates: plateIds.size, per_area: perArea };
});

check("G01", "every P00-P11 action carries the full governance contract in both bodies", (fail) => {
  const relative = "visual/assets/action-governance.json";
  if (!exists(relative)) return fail(`${relative} does not exist`);
  const governance = readJson(relative);
  const projects = readJson("visual/assets/regeneration-source.json").projects;

  const registryIds = projects.map((project) => project.id).sort();
  const governanceIds = governance.actions.map((action) => action.id).sort();
  if (registryIds.join(",") !== governanceIds.join(",")) {
    fail(`governance covers [${governanceIds.join(" ")}] but the action registry declares [${registryIds.join(" ")}]`);
  }

  // Every field the brief requires per action, in both languages. A field that is present
  // but empty is the same defect as a missing one.
  const bilingual = [
    "operator_role", "maintainer", "beneficiary", "worst_affected", "metric",
    "proposed_target", "stop_trigger", "stop_authority", "rollback",
    "physical_restoration", "residual_liability", "non_digital_fallback",
  ];
  for (const action of governance.actions) {
    for (const field of bilingual) {
      for (const language of ["zh", "en"]) {
        const value = action[`${field}_${language}`];
        if (typeof value !== "string" || value.trim() === "") {
          fail(`${action.id} is missing ${field}_${language}`);
        }
      }
    }
    // An action that claimed an authorized target, a funding source, or no blocking gate
    // would be asserting an external approval nobody in this package can give.
    if (action.authorized_target !== null) fail(`${action.id} declares an authorized target`);
    if (action.authorization_state !== "not_authorized") fail(`${action.id} is not marked not_authorized`);
    if (action.funding_state !== "unfunded") fail(`${action.id} is not marked unfunded`);
    if (!Array.isArray(action.blocked_by) || action.blocked_by.length === 0) {
      fail(`${action.id} declares no unresolved D gate`);
    }
    for (const gate of action.blocked_by ?? []) {
      if (!/^D(0[1-9]|1[0-7])$/.test(gate)) fail(`${action.id} references ${gate}, which is not a D01-D17 gate`);
    }
  }

  // The register has to be readable in the documents, not only in this JSON.
  const detail = {};
  for (const [file, language] of [["proposal.md", "zh"], ["proposal.en.md", "en"]]) {
    const body = readText(file);
    const missing = [];
    for (const action of governance.actions) {
      if (!body.includes(action.id)) missing.push(`${action.id}:id`);
      for (const field of bilingual) {
        if (!body.includes(action[`${field}_${language}`])) missing.push(`${action.id}:${field}`);
      }
    }
    detail[file] = { missing: missing.length };
    for (const item of missing) fail(`${file} does not carry ${item}`);
  }
  return { actions: governance.actions.length, ...detail };
});

check("V02", "both viewers list all twelve actions under the canonical registry titles", (fail) => {
  const projects = readJson("visual/assets/regeneration-source.json").projects;
  const areas = readJson("visual/assets/regeneration-source.json").areas;
  const detail = {};
  for (const [file, language] of [["visual/index.html", "zh"], ["visual/index.en.html", "en"]]) {
    const body = readText(file);
    const missingProjects = projects.filter((project) => !body.includes(project[`name_${language}`]));
    const missingIds = projects.filter((project) => !body.includes(project.id));
    // The English viewer previously carried a different role for each area than the
    // Chinese one; both must now read back the single registry wording.
    const missingRoles = areas.filter((area) => !body.includes(area[`role_${language}`]));
    detail[file] = {
      missing_project_ids: missingIds.map((project) => project.id),
      missing_project_titles: missingProjects.map((project) => project.id),
      missing_area_roles: missingRoles.map((area) => area.id),
    };
    for (const project of missingIds) fail(`${file} does not list action ${project.id}`);
    for (const project of missingProjects) fail(`${file} does not use the registry title for ${project.id}`);
    for (const area of missingRoles) fail(`${file} does not use the registry role for ${area.id}`);
  }
  return detail;
});

check("HTML-H1", "each rendered report has exactly one top-level heading", (fail) => {
  const counts = {};
  for (const file of ["report/proposal.html", "report/proposal.en.html"]) {
    const found = (readText(file).match(/<h1[\s>]/g) || []).length;
    counts[file] = found;
    if (found !== 1) fail(`${file} has ${found} <h1> elements, expected exactly 1`);
  }
  return counts;
});

check("SP01", "both official spellings survive with provenance and an explicit bilingual note", (fail) => {
  const provenance = readJson("visual/assets/regeneration-source.json").spelling_provenance;
  const spellings = provenance.variants.map((variant) => variant.spelling);
  for (const spelling of ["集聚", "聚集"]) {
    if (!spellings.includes(spelling)) fail(`spelling ${spelling} is not preserved`);
  }
  for (const variant of provenance.variants) {
    if (!variant.source_id) fail(`spelling ${variant.spelling} carries no provenance`);
  }
  if (!provenance.note_zh || !provenance.note_en) fail("the bilingual note is incomplete");
  return { spellings };
});

check("C01", "the changelog still carries 14 Class C tasks and all 17 Class D gates", (fail) => {
  const changelog = readText("changelog.md");
  const classC = (changelog.match(/\*\*C\d\d\s/g) || []).length;
  if (classC !== 14) fail(`expected 14 Class C tasks, found ${classC}`);
  const missing = [];
  for (let index = 1; index <= 17; index += 1) {
    const gate = `D${String(index).padStart(2, "0")}`;
    if (!changelog.includes(gate)) missing.push(gate);
  }
  if (missing.length > 0) fail(`missing Class D gates: ${missing.join(", ")}`);
  // A Class D gate is external evidence and must stay non-checkable, so it may not
  // appear as a checkbox row at all — ticked or not.
  const checkboxIds = Array.from(changelog.matchAll(/^- \[[ x]\]\s*\*{0,2}`?([A-Z]\d\d)`?/gm), (match) => match[1]);
  const checkableD = checkboxIds.filter((id) => id.startsWith("D"));
  for (const id of checkableD) fail(`Class D gate ${id} is written as a checkbox row; D gates are non-checkable`);
  const tickedC = Array.from(changelog.matchAll(/^- \[x\]\s*\*{0,2}`?(C\d\d)`?/gm), (match) => match[1]);
  return { class_c: classC, class_d: 17 - missing.length, closed_class_c: tickedC };
});

check("EM01", "every reference in both evidence matrices resolves to the artifact it names", (fail) => {
  const { exitCode, payload } = runNode("visual/assets/build-matrices.js", ["--check"]);
  if (payload.status !== "PASS") fail(`build-matrices reported ${payload.status}`);
  for (const problem of payload.failures ?? []) fail(problem);
  if (payload.references_unresolved !== 0) {
    fail(`${payload.references_unresolved} references do not resolve`);
  }
  // A non-zero exit here means the published matrices differ from what the map produces,
  // which is the same defect as an unresolved reference: the file on disk is not the file
  // the evidence says it is.
  if (exitCode !== 0) fail(`the published matrices are out of date with the evidence map (exit ${exitCode})`);
  return {
    references_checked: payload.references_checked,
    references_resolved: payload.references_resolved,
    requirements: payload.requirements,
    design_depth_items: payload.design_depth_items,
  };
});

check("EM02", "neither evidence matrix cites the same set on every row", (fail) => {
  const matrices = [
    {
      label: "compliance_matrix.json",
      rows: readJson("compliance_matrix.json").requirements,
      idKey: "requirement_id",
      arrays: ["report_sections", "geojson_layers", "metrics", "drawings", "visual_sections", "source_ids", "assumption_ids", "self_check_ids"],
    },
    {
      label: "design_depth_matrix.json",
      rows: readJson("design_depth_matrix.json").items,
      idKey: "item_id",
      arrays: ["proposal_sections", "drawing_refs", "geometry_refs", "metric_refs", "source_ids", "assumption_ids", "self_check_ids"],
    },
  ];
  const detail = {};
  for (const matrix of matrices) {
    for (const key of matrix.arrays) {
      const missing = matrix.rows.filter((row) => !Array.isArray(row[key]) || row[key].length === 0);
      for (const row of missing) fail(`${matrix.label}: ${row[matrix.idKey]} has an empty ${key}`);
      if (missing.length > 0) continue;
      // The defect this replaced: one citation set repeated on every row, which says the
      // same thing about every requirement and so lets a reader check none of them.
      const universal = matrix.rows[0][key].filter((value) => matrix.rows.every((row) => row[key].includes(value)));
      for (const value of universal) {
        fail(`${matrix.label}: every row cites ${value} in ${key}`);
      }
    }
    // Sources are the reference kind that had collapsed hardest, so they carry the stricter
    // rule: no two rows may rest on exactly the same set of sources.
    const sourceSets = matrix.rows.map((row) => JSON.stringify(row.source_ids ?? []));
    const distinct = new Set(sourceSets).size;
    if (distinct !== matrix.rows.length) {
      fail(`${matrix.label}: only ${distinct} distinct source sets across ${matrix.rows.length} rows`);
    }
    detail[matrix.label] = { rows: matrix.rows.length, distinct_source_sets: distinct };
  }
  return detail;
});

check("EM03", "each key-area requirement cites its own area's plates, components, and routes only", (fail) => {
  const areas = [
    { requirement: "1.5.3.1", plate: "ZZY-", component: "Z-C", route: "Z-R", envelope: "ENV-ZY-01" },
    { requirement: "1.5.3.2", plate: "AIO-", component: "O-C", route: "O-R", envelope: "ENV-AO-01" },
    { requirement: "1.5.3.3", plate: "DZS-", component: "D-C", route: "D-R", envelope: "ENV-DZ-01" },
  ];
  const rows = new Map(readJson("compliance_matrix.json").requirements.map((row) => [row.requirement_id, row]));
  // How many step-free chains an area publishes is a fact about its design, not a quota.
  // Zhongzhiyuan has two pedestrian chains and the AI Origin Community has four; demanding
  // three everywhere would force one of them to invent a chain or drop a real one. Reading
  // the count from the register makes this the stronger check: the matrix has to cite every
  // chain the area actually publishes, so an omitted chain and an invented one both fail.
  const registerRoutes = new Map();
  for (const area of readJson("visual/assets/regeneration-source.json").areas ?? []) {
    for (const route of area.routes ?? []) {
      const prefix = route.id.slice(0, 3);
      registerRoutes.set(prefix, (registerRoutes.get(prefix) ?? 0) + 1);
    }
  }
  const detail = {};
  for (const area of areas) {
    const row = rows.get(area.requirement);
    if (!row) {
      fail(`compliance_matrix.json has no requirement ${area.requirement}`);
      continue;
    }
    const expect = (key, prefix, count) => {
      const values = row[key] ?? [];
      if (values.length !== count) fail(`${area.requirement}: expected ${count} entries in ${key}, found ${values.length}`);
      // Citing another area's component would mean the three areas are not actually
      // carrying different content, which is the claim these rows exist to support.
      const foreign = values.filter((value) => !value.startsWith(prefix));
      for (const value of foreign) fail(`${area.requirement}: ${key} cites ${value}, which is not a ${prefix}* reference`);
    };
    expect("plate_refs", area.plate, SEMANTIC_PLATES_PER_AREA);
    expect("component_refs", area.component, 5);
    const publishedRoutes = registerRoutes.get(area.route) ?? 0;
    if (publishedRoutes === 0) {
      fail(`${area.requirement}: regeneration-source.json publishes no ${area.route}* step-free chain`);
    }
    expect("route_refs", area.route, publishedRoutes);
    if (JSON.stringify(row.envelope_refs ?? []) !== JSON.stringify([area.envelope])) {
      fail(`${area.requirement}: envelope_refs must be exactly [${area.envelope}]`);
    }
    detail[area.requirement] = {
      plates: (row.plate_refs ?? []).length,
      components: (row.component_refs ?? []).length,
      routes: (row.route_refs ?? []).length,
    };
  }
  return detail;
});

// The fourteen key-area tests. Each is a standalone executable that reads the shared contract
// module, so a failure can be reproduced with one command; this file only registers their
// results. Requiring rather than spawning keeps a suite run to a single process and means a
// contract change cannot be seen by one test and missed by another.
for (const script of [
  "./test-key-area-inventory.js",
  "./test-key-area-registry.js",
  "./test-key-area-spatial-content.js",
  "./test-step-free-chain.js",
  "./test-winter-maintenance.js",
  "./test-dazhongsi-claim-limits.js",
  "./test-phase-accountability.js",
  "./test-evidence-resolution.js",
  "./test-source-normalization.js",
  "./test-publication-parity.js",
  "./test-english-language-integrity.js",
  "./test-gate-namespace.js",
  "./test-denominator-discipline.js",
  "./test-threshold-quantization.js",
]) {
  const outcome = require(script).run();
  check(outcome.id, outcome.description, (fail) => {
    for (const failure of outcome.failures) fail(failure);
    return outcome.detail;
  });
}

check("N01", "every JavaScript asset parses", (fail) => {
  const scripts = fs.readdirSync(ASSETS).filter((name) => name.endsWith(".js")).sort();
  for (const name of scripts) {
    const result = spawnSync(process.execPath, ["--check", path.join(ASSETS, name)], { encoding: "utf8" });
    if (result.status !== 0) fail(`${name}: ${(result.stderr || "").split("\n")[0]}`);
  }
  return { scripts };
});

const CASE_NAMESPACE_AUDIT_ID = "NS01";
check(CASE_NAMESPACE_AUDIT_ID, "aggregate case IDs are unique and never reuse a reserved gate or self-check ID", (fail) => {
  const registry = readJson("visual/assets/gate-registry.json");
  const caseIds = [...results.map((result) => result.id), CASE_NAMESPACE_AUDIT_ID];
  const reservedEntries = [
    ...(registry.human_design_gate?.gates ?? []).map((gate) => ({ namespace: "G", id: gate.id })),
    ...(registry.machine_self_check_gate?.ids ?? []).map((id) => ({ namespace: "self_check", id })),
    ...(registry.human_authorization_gate?.gates ?? []).map((gate) => ({ namespace: "H", id: gate.id })),
    ...(registry.external_evidence_gate?.gates ?? []).map((gate) => ({ namespace: "D", id: gate.id })),
  ];
  const audit = auditIdentifierNamespaces(caseIds, reservedEntries);

  for (const duplicate of audit.duplicate_case_ids) {
    fail(`aggregate case ID ${JSON.stringify(duplicate.id)} occurs ${duplicate.count} times`);
  }
  for (const duplicate of audit.duplicate_reserved_ids) {
    fail(`reserved ID ${JSON.stringify(duplicate.id)} occurs ${duplicate.count} times across ${duplicate.namespaces.join(",")}`);
  }
  for (const id of audit.reserved_case_collisions) {
    fail(`aggregate case ID ${JSON.stringify(id)} collides with a reserved gate or self-check ID`);
  }

  const mutationProbes = [
    {
      name: "duplicate aggregate case ID",
      caught: auditIdentifierNamespaces(["MUT-CASE", "MUT-CASE"], []).duplicate_case_ids.some((item) => item.id === "MUT-CASE"),
    },
    {
      name: "case ID reusing a reserved ID",
      caught: auditIdentifierNamespaces(["MUT-RESERVED"], [{ namespace: "G", id: "MUT-RESERVED" }])
        .reserved_case_collisions.includes("MUT-RESERVED"),
    },
    {
      name: "reserved ID reused across namespaces",
      caught: auditIdentifierNamespaces([], [
        { namespace: "G", id: "MUT-CROSS" },
        { namespace: "D", id: "MUT-CROSS" },
      ]).duplicate_reserved_ids.some((item) => item.id === "MUT-CROSS"),
    },
  ];
  for (const probe of mutationProbes) {
    if (!probe.caught) fail(`namespace audit did not catch mutation: ${probe.name}`);
  }

  return {
    case_ids: caseIds.length,
    reserved_ids: reservedEntries.length,
    mutation_probes_caught: mutationProbes.map((probe) => probe.name),
  };
});

const failed = results.filter((result) => result.status === "FAIL");
const report = {
  status: failed.length === 0 ? "PASS" : "FAIL",
  exit_code: failed.length === 0 ? 0 : 1,
  cases_run: results.length,
  cases_failed: failed.length,
  failed_ids: failed.map((result) => result.id),
  results,
};
process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
process.exitCode = report.exit_code;
