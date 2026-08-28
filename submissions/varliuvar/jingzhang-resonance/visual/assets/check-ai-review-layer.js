"use strict";

const fs = require("fs");
const path = require("path");

if (process.argv.length !== 3 || process.argv[2] !== "--check") {
  console.error("Usage: node visual/assets/check-ai-review-layer.js --check");
  process.exit(2);
}

const assetDir = __dirname;
const packageDir = path.resolve(assetDir, "..", "..");
const layerRelativePath = "visual/assets/ai-review-layer.json";
const layerPath = path.join(packageDir, layerRelativePath);
const manifestPath = path.join(packageDir, "manifest.json");
const errors = [];
const expectedDimensions = ["brief_alignment", "originality", "ai_planning_innovation", "implementation_feasibility", "public_interest_inclusion", "risk_compliance", "expression_completeness"];
const expectedRepairs = Array.from({ length: 13 }, (_, index) => `R${String(index + 1).padStart(2, "0")}`);
const repairStates = ["complete", "in_progress", "external_dependency", "not_started"];
const expectedScenarios = ["T-01", "T-04", "T-10"];
const expectedSamples = ["S-LOW-DISTURBANCE-SPATIAL", "S-T04-AI-TEST"];
const participantMethodCompleteStatus = "method_complete_external_evidence_pending";
const expectedReviewBaselineSha = "34aeb29893414ae9eeace69348abf21fc4addbc511abfb0b23efb1364ebb4b9a";
const expectedPreviousReviewBaselineSha = "53ae6be5a3787ab225f187d6d39342cddbd6db6343d5558eb99d7a06a12fedb0";
const expectedRepairCounts = { complete: 13, in_progress: 0, external_dependency: 2, not_started: 0 };
const repairFields = ["id", "title", "status", "repair_state", "participant_action", "evidence_paths", "claim_boundary", "external_dependency"];
const feedbackFields = ["id", "review_source", "dimension_id", "feedback_summary", "requested_action", "human_narrative_change_required", "status", "evidence_paths", "resolution_note"];
const scenarioFields = ["scenario_id", "baseline_status", "sampling_scope", "data_controller_role", "human_reviewer_role", "continue_condition", "pause_condition", "exit_condition", "public_disclosure", "measured_value", "institution_status"];
const sampleFields = ["sample_id", "sample_type", "scenario_id", "status", "participant_complete", "scope", "proposed_raci_role_types", "prerequisite_permissions", "cost_estimation_method", "cost_amount", "maintenance_cycle", "emergency_escalation", "exit_acceptance", "retest_template", "institution_status", "evidence_paths", "claim_boundary"];

function fail(message) { errors.push(message); }

function readJson(file) {
  try { return JSON.parse(fs.readFileSync(file, "utf8")); }
  catch (error) { fail(`${path.relative(packageDir, file)}: ${error.message}`); return null; }
}

function requireFields(label, value, fields) {
  if (!value || typeof value !== "object" || Array.isArray(value)) { fail(`${label} must be an object`); return; }
  for (const field of fields) if (!(field in value) || value[field] === "" || value[field] === undefined) fail(`${label}.${field} is required`);
}

function exactIds(label, actual, expected) {
  if (!Array.isArray(actual) || actual.length !== expected.length || actual.some((id, index) => id !== expected[index])) fail(`${label} must be exactly ${expected.join(", ")}`);
}

function normalizeEvidencePath(value, label) {
  if (typeof value !== "string" || value.length === 0) { fail(`${label} must be a non-empty string`); return null; }
  const normalized = value.replace(/\\/g, "/");
  if (path.isAbsolute(value) || normalized.startsWith("/") || normalized.split("/").includes("..")) { fail(`${label} must be a safe package-relative path`); return null; }
  if (normalized.startsWith("review/ai/")) fail(`${label} uses forbidden review/ai/* storage`);
  const resolved = path.resolve(packageDir, normalized);
  if (resolved !== packageDir && !resolved.startsWith(`${packageDir}${path.sep}`)) { fail(`${label} escapes the package`); return null; }
  return { normalized, resolved };
}

const layer = readJson(layerPath);
const manifest = readJson(manifestPath);
const manifestFiles = new Set((manifest?.files || []).map((item) => item.path?.replace(/\\/g, "/")));
const allEvidence = [];

function checkEvidencePaths(paths, label, ownerStatus = "open") {
  if (!Array.isArray(paths) || paths.length === 0) { fail(`${label} must be a non-empty array`); return; }
  paths.forEach((value, index) => {
    const result = normalizeEvidencePath(value, `${label}[${index}]`);
    if (result) allEvidence.push({ ...result, label: `${label}[${index}]`, ownerStatus });
  });
}

if (layer) {
  requireFields("root", layer, ["schema_version", "audience", "purpose", "reviewed_baseline_sha256", "human_layer_policy", "manifest_registration", "formal_review_gate", "rubric_dimensions", "repair_register", "future_feedback_register", "regional_collaboration", "priority_scenarios", "deepened_samples", "bilingual_artifact_status", "rights_summary", "claim_boundary"]);
  if (layer.schema_version !== "1.0.0") fail("schema_version must be 1.0.0");
  if (layer.audience !== "maintainer_ai_review") fail("audience must be maintainer_ai_review");
  if (layer.reviewed_baseline_sha256 !== expectedReviewBaselineSha) fail("reviewed_baseline_sha256 must match the latest 84/100 historical review");
  if (layer.prior_reviewed_baseline?.score_total !== 89 || layer.prior_reviewed_baseline?.package_sha256 !== expectedPreviousReviewBaselineSha) fail("prior_reviewed_baseline must retain the previous 89/100 review");
  if (layer.human_layer_policy?.proposal_body_rewrite_allowed !== false || layer.human_layer_policy?.ai_review_terms_stay_in_ai_layer !== true || !Array.isArray(layer.human_layer_policy?.allowed_human_changes)) fail("human_layer_policy must match the frozen-narrative contract");
  if (layer.formal_review_gate?.review_state !== "request_changes" || layer.formal_review_gate?.formal_review !== false || layer.formal_review_gate?.score_total !== 84 || layer.formal_review_gate?.previous_reviewed_baseline_score_total !== 89 || layer.formal_review_gate?.publication_state !== "pending_visual_rights_reconciliation") fail("formal_review_gate must retain 84 latest historical score, 89 previous score, formal_review false, and pending rights state");

  if (!Array.isArray(layer.rubric_dimensions)) fail("rubric_dimensions must be an array");
  else {
    exactIds("rubric dimension IDs", layer.rubric_dimensions.map((item) => item.id), expectedDimensions);
    layer.rubric_dimensions.forEach((item, index) => {
      requireFields(`rubric_dimensions[${index}]`, item, ["id", "score", "score_max", "findings", "evidence", "boundaries"]);
      if (!Number.isInteger(item.score) || item.score < 0 || item.score > item.score_max) fail(`rubric_dimensions[${index}].score is invalid`);
      if (!Array.isArray(item.findings) || item.findings.length === 0) fail(`rubric_dimensions[${index}].findings must be non-empty`);
      if (!Array.isArray(item.boundaries) || item.boundaries.length === 0) fail(`rubric_dimensions[${index}].boundaries must be non-empty`);
      if (!Array.isArray(item.evidence) || item.evidence.length < 1 || item.evidence.length > 3) fail(`rubric_dimensions[${index}].evidence must contain 1-3 primary paths`);
      else checkEvidencePaths(item.evidence, `rubric_dimensions[${index}].evidence`);
    });
  }

  if (!Array.isArray(layer.repair_register)) fail("repair_register must be an array");
  else {
    exactIds("repair IDs", layer.repair_register.map((item) => item.id), expectedRepairs);
    layer.repair_register.forEach((item, index) => {
      requireFields(`repair_register[${index}]`, item, repairFields);
      if (item.status === "completed" || item.status === "verified_closed") fail(`repair_register[${index}] must remain open in this batch`);
      if (!repairStates.includes(item.repair_state)) fail(`repair_register[${index}].repair_state is invalid`);
      checkEvidencePaths(item.evidence_paths, `repair_register[${index}].evidence_paths`, item.status);
    });
  }

  if (!Array.isArray(layer.future_feedback_register) || layer.future_feedback_register.length === 0) fail("future_feedback_register must be non-empty");
  else {
    const feedbackIds = new Set();
    layer.future_feedback_register.forEach((item, index) => {
      requireFields(`future_feedback_register[${index}]`, item, feedbackFields);
      if (!/^F-\d{8}-\d{2}$/.test(item.id || "")) fail(`future_feedback_register[${index}].id is invalid`);
      if (feedbackIds.has(item.id)) fail(`duplicate feedback ID ${item.id}`);
      feedbackIds.add(item.id);
      if (!expectedDimensions.includes(item.dimension_id)) fail(`future_feedback_register[${index}].dimension_id is invalid`);
      if (item.human_narrative_change_required !== false) fail(`future_feedback_register[${index}] must not request a human narrative change`);
      checkEvidencePaths(item.evidence_paths, `future_feedback_register[${index}].evidence_paths`, item.status);
    });
  }

  if (!Array.isArray(layer.priority_scenarios)) fail("priority_scenarios must be an array");
  else {
    exactIds("priority scenario IDs", layer.priority_scenarios.map((item) => item.scenario_id), expectedScenarios);
    layer.priority_scenarios.forEach((item, index) => {
      requireFields(`priority_scenarios[${index}]`, item, scenarioFields);
      if (item.measured_value !== null) fail(`priority_scenarios[${index}].measured_value must be null`);
      if (item.institution_status !== "unconfirmed") fail(`priority_scenarios[${index}].institution_status must be unconfirmed`);
    });
  }

  if (!Array.isArray(layer.deepened_samples)) fail("deepened_samples must be an array");
  else {
    exactIds("deepened sample IDs", layer.deepened_samples.map((item) => item.sample_id), expectedSamples);
    layer.deepened_samples.forEach((item, index) => {
      requireFields(`deepened_samples[${index}]`, item, sampleFields);
      if (item.status !== participantMethodCompleteStatus || item.participant_complete !== true) fail(`deepened_samples[${index}] must record participant method completion while retaining external evidence pending`);
      if (item.cost_amount !== null || item.institution_status !== "unconfirmed") fail(`deepened_samples[${index}] must keep cost_amount null and institution_status unconfirmed`);
      const raci = item.proposed_raci_role_types || {};
      for (const role of ["responsible", "accountable", "consulted", "informed"]) if (!Array.isArray(raci[role]) || raci[role].length === 0) fail(`deepened_samples[${index}].proposed_raci_role_types.${role} must be non-empty`);
      if (!Array.isArray(item.prerequisite_permissions) || item.prerequisite_permissions.length === 0) fail(`deepened_samples[${index}].prerequisite_permissions must be non-empty`);
      else if (item.prerequisite_permissions.some((permission) => typeof permission !== "string" || !permission.endsWith("_unconfirmed"))) fail(`deepened_samples[${index}].prerequisite_permissions must remain explicitly unconfirmed`);
      checkEvidencePaths(item.evidence_paths, `deepened_samples[${index}].evidence_paths`, item.status);
      const sampleEvidence = item.evidence_paths?.[0] ? readJson(path.join(packageDir, item.evidence_paths[0])) : null;
      if (sampleEvidence?.sample_id !== item.sample_id || sampleEvidence?.status !== participantMethodCompleteStatus || sampleEvidence?.participant_complete !== true) fail(`deepened_samples[${index}] must match its participant-complete external-evidence-pending sample record`);
      if (sampleEvidence?.institution_status !== "unconfirmed") fail(`deepened_samples[${index}] sample record must keep institution_status unconfirmed`);
      const permissionRecords = sampleEvidence?.prerequisite_permissions;
      if (!Array.isArray(permissionRecords) || permissionRecords.length === 0 || permissionRecords.some((permission) => permission?.status !== "unconfirmed")) fail(`deepened_samples[${index}] sample record must keep every prerequisite permission unconfirmed`);
    });
  }

  if (layer.regional_collaboration?.institution_status !== "unconfirmed") fail("regional_collaboration.institution_status must be unconfirmed");
  if (!Array.isArray(layer.regional_collaboration?.suggested_relationship_names) || layer.regional_collaboration.suggested_relationship_names.length !== 5) fail("regional_collaboration must retain five existing suggested relationship names");

  const counts = { ...expectedRepairCounts };
  const repairRegisterCounts = Object.fromEntries(repairStates.map((state) => [state, 0]));
  for (const repair of layer.repair_register || []) repairRegisterCounts[repair.repair_state] += 1;
  if (repairRegisterCounts.complete !== 13 || repairRegisterCounts.in_progress !== 0 || repairRegisterCounts.not_started !== 0) fail("repair_register must contain 13 complete participant repairs");
  const countsMatch = (value) => repairStates.every((state) => value?.[state] === counts[state]);

  const statusWord = /^(committed|approved)$/i;
  function inspectStatuses(value, label = "root") {
    if (!value || typeof value !== "object") return;
    for (const [key, child] of Object.entries(value)) {
      const childLabel = `${label}.${key}`;
      if (/(institution_status|commitment_status|authorization_status)$/.test(key) && typeof child === "string" && statusWord.test(child)) fail(`${childLabel} must not be ${child}`);
      inspectStatuses(child, childLabel);
    }
  }
  inspectStatuses(layer);

  const sourceRegistry = readJson(path.join(packageDir, "sources.json"));
  const layerSource = sourceRegistry?.sources?.find((item) => item.id === "AI-REVIEW-LAYER");
  if (!layerSource || !/^participant_generated/.test(layerSource.source_type || "") || layerSource.ownership !== "participant_generated") fail("AI-REVIEW-LAYER source must be explicitly participant-generated");
  if (layerSource?.manifest_listed !== layer.manifest_registration?.manifest_listed || layerSource?.provisional_manifest_registration !== layer.manifest_registration?.provisional_manifest_registration) fail("AI-REVIEW-LAYER source registration state must match the AI review layer");
  if (layerSource?.ai_review_input_summary?.open_feedback_ids?.[0] !== "F-20260825-01") fail("sources.json must carry the latest open feedback summary into review input");
  if (layerSource?.ai_review_input_summary?.reviewed_baseline_sha256_prefix !== expectedReviewBaselineSha.slice(0, 12) || layerSource?.ai_review_input_summary?.score_total !== 84 || layerSource?.ai_review_input_summary?.previous_reviewed_baseline_score_total !== 89 || layerSource?.ai_review_input_summary?.formal_review !== false) fail("sources.json review metadata must match 84 latest and 89 previous historical baselines");
  if (!countsMatch(layerSource?.ai_review_input_summary?.repair_counts)) fail("sources.json repair counts must match the AI review layer");

  const compliance = readJson(path.join(packageDir, "compliance_matrix.json"));
  for (const requirementId of ["agent.2", "agent.3", "agent.4", "agent.6"]) {
    const requirement = compliance?.requirements?.find((item) => item.requirement_id === requirementId);
    if (!requirement?.ai_review_evidence?.includes(layerRelativePath) || !requirement.ai_review_structured_summary) fail(`compliance_matrix.${requirementId} must carry AI review evidence and a structured summary`);
    if (requirement?.current_reality_state !== "concept_complete_external_evidence_pending" || requirement?.institution_status !== "role_types_only_unconfirmed") fail(`compliance_matrix.${requirementId} must retain plan status enums`);
    if (requirement?.ai_review_evidence) checkEvidencePaths(requirement.ai_review_evidence, `compliance_matrix.${requirementId}.ai_review_evidence`);
  }
  const complianceById = Object.fromEntries((compliance?.requirements || []).map((item) => [item.requirement_id, item]));
  if (complianceById["agent.2"]?.ai_review_structured_summary?.detail_rows_complete !== true) fail("compliance_matrix.agent.2 must expose the completed regional detail rows");
  if (!complianceById["agent.3"]?.ai_review_evidence?.includes("visual/assets/t04-ai-test-sample.json")) fail("compliance_matrix.agent.3 must reference the T-04 test sample");
  if (complianceById["agent.4"]?.ai_review_structured_summary?.sample_status !== participantMethodCompleteStatus || complianceById["agent.4"]?.ai_review_structured_summary?.participant_complete !== true) fail("compliance_matrix.agent.4 must distinguish participant-complete sample methods from pending external evidence");
  for (const samplePath of ["visual/assets/low-disturbance-spatial-sample.json", "visual/assets/t04-ai-test-sample.json"]) if (!complianceById["agent.4"]?.ai_review_evidence?.includes(samplePath)) fail(`compliance_matrix.agent.4 must reference ${samplePath}`);
  if (!countsMatch(complianceById["agent.6"]?.ai_review_structured_summary?.repair_counts)) fail("compliance_matrix.agent.6 repair counts must match the AI review layer");
  if (complianceById["agent.6"]?.ai_review_structured_summary?.score_total !== 84 || complianceById["agent.6"]?.ai_review_structured_summary?.previous_reviewed_baseline_score_total !== 89 || complianceById["agent.6"]?.ai_review_structured_summary?.formal_review !== false || complianceById["agent.6"]?.ai_review_structured_summary?.publication_clearance !== false) fail("compliance_matrix.agent.6 review metadata must retain historical scores and pending publication");

  const designDepth = readJson(path.join(packageDir, "design_depth_matrix.json"));
  for (const item of (designDepth?.items || []).filter((entry) => entry.participant_complete === false)) {
    if (!Array.isArray(item.completeness_limited_by) || item.completeness_limited_by.length === 0) fail(`design_depth_matrix.${item.item_id} must disclose completeness_limited_by`);
    checkEvidencePaths(item.ai_review_evidence, `design_depth_matrix.${item.item_id}.ai_review_evidence`);
  }
  const depthSummaries = (designDepth?.items || []).map((item) => item.ai_review_structured_summary).filter(Boolean);
  if (!depthSummaries.some((summary) => summary.sample_id === "S-LOW-DISTURBANCE-SPATIAL" && summary.status === participantMethodCompleteStatus) || !depthSummaries.some((summary) => summary.sample_id === "S-T04-AI-TEST" && summary.status === participantMethodCompleteStatus)) fail("design_depth_matrix must carry both participant-complete, external-evidence-pending sample summaries");
  if (!depthSummaries.some((summary) => summary.open_feedback_ids?.includes("F-20260825-01"))) fail("design_depth_matrix must carry the latest open feedback summary");
  if (!depthSummaries.some((summary) => countsMatch(summary.repair_counts))) fail("design_depth_matrix repair counts must match the AI review layer");
  if (!depthSummaries.some((summary) => summary.score_total === 84 && summary.previous_reviewed_baseline_score_total === 89 && summary.formal_review === false && summary.publication_clearance === false && summary.publication_state === "pending_visual_rights_reconciliation")) fail("design_depth_matrix must carry synchronized historical review and rights metadata");

  const registration = layer.manifest_registration || {};
  if (registration.finalized === true) {
    if (registration.provisional_manifest_registration !== false || registration.manifest_listed !== true) fail("finalized manifest registration must disable provisional mode and assert manifest_listed true");
    for (const evidence of allEvidence) {
      if (!fs.existsSync(evidence.resolved)) fail(`${evidence.label} is missing after manifest finalization`);
      if (!manifestFiles.has(evidence.normalized)) fail(`${evidence.label} is not manifest-listed after finalization`);
    }
    if (!manifestFiles.has(layerRelativePath)) fail(`${layerRelativePath} is not manifest-listed after finalization`);
  } else {
    if (registration.provisional_manifest_registration !== true) fail("unfinished manifest registration requires provisional_manifest_registration true");
    if (registration.manifest_listed === true && !manifestFiles.has(layerRelativePath)) fail(`${layerRelativePath} asserts manifest registration but is not manifest-listed`);
    for (const evidence of allEvidence) {
      if (evidence.ownerStatus === "verified_closed" && !fs.existsSync(evidence.resolved)) fail(`${evidence.label} is missing for verified_closed evidence`);
      if (fs.existsSync(evidence.resolved) && registration.manifest_listed === true && !manifestFiles.has(evidence.normalized)) fail(`${evidence.label} exists but is not manifest-listed during provisional finalization`);
      if (!fs.existsSync(evidence.resolved) && !/^(visual\/assets\/|assets\/|drawings\/)/.test(evidence.normalized)) fail(`${evidence.label} is a missing planned path outside the allowed evidence roots`);
    }
  }

  for (const file of ["visual/index.html", "visual/index.en.html"]) {
    const absolute = path.join(packageDir, file);
    let html = "";
    try { html = fs.readFileSync(absolute, "utf8"); } catch (error) { fail(`${file}: ${error.message}`); continue; }
    const section = html.match(/<section id=["']ai-review-layer["'][\s\S]*?<\/section>/)?.[0] || "";
    if (!section) { fail(`${file} must contain the AI review section`); continue; }
    if (!/data-audience=["']participant-self-check["']/.test(section)) fail(`${file} AI section must declare participant self-check audience`);
    if (/MAINTAINER REVIEW INDEX|机器评审专用索引|request-changes|80\/100|维护者复评/.test(section)) fail(`${file} participant self-check section must not present maintainer-style scores or decisions`);
    for (const dimension of layer.rubric_dimensions || []) {
      if (!section.includes(dimension.id)) fail(`${file} evidence map must contain ${dimension.id}`);
      for (const evidence of dimension.evidence || []) if (!section.includes(evidence)) fail(`${file} evidence map must contain ${evidence}`);
    }
    for (const repairId of expectedRepairs) if (!new RegExp(`\\b${repairId}\\b`).test(section)) fail(`${file} must contain ${repairId}`);
    for (const state of repairStates) {
      // external_dependency is an aggregate gate count; the frozen indexes render participant repair states only.
      if (state === "external_dependency") continue;
      const countPattern = new RegExp(`data-repair-state=["']${state}["'][^>]*>[^<]*${counts[state]}\\b`);
      if (!countPattern.test(section)) fail(`${file} must show ${state} count ${counts[state]}`);
    }
    for (const feedback of (layer.future_feedback_register || []).filter((item) => item.status !== "verified_closed")) {
      if (!section.includes(feedback.id) || !section.includes(feedback.status)) fail(`${file} must show open feedback ${feedback.id} and status`);
      for (const evidence of feedback.evidence_paths || []) if (!section.includes(evidence)) fail(`${file} must show feedback evidence ${evidence}`);
    }
  }
}

if (errors.length) {
  errors.forEach((error) => console.error(`ERROR: ${error}`));
  console.error(`FAIL: ${errors.length} error(s)`);
  process.exit(1);
}

console.log("PASS: AI review contract, provisional manifest state, evidence map, repair counts, feedback, scenarios, samples, and index navigation are valid.");
