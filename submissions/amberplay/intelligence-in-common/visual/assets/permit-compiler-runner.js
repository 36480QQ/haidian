#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const data = JSON.parse(fs.readFileSync(path.join(__dirname, "spatiotemporal-permits.json"), "utf8"));
const actions = JSON.parse(fs.readFileSync(path.join(__dirname, "design-actions-public-context.json"), "utf8"));
const context = JSON.parse(fs.readFileSync(path.join(__dirname, "public-context.json"), "utf8"));
const validations = JSON.parse(fs.readFileSync(path.join(__dirname, "preregistered-validation-protocols.json"), "utf8"));
if (data.status !== "synthetic_tabletop_only_not_authorized_not_field_run") throw new Error("Synthetic-only status is required.");
if (data.deployment_decision !== "not_authorized_not_run" || data.field_performance !== null) throw new Error("No field or deployment claim is allowed.");
if (data.public_consent !== null || data.selection_status !== "design_team_desktop_conditional_preference_only_professional_and_public_review_pending") throw new Error("Desktop preference must not be represented as professional or public selection.");
if (data.cases.length !== 3) throw new Error(`Expected 3 cross-tie cases, got ${data.cases.length}.`);
if (!data.ai_assistance_record || !data.ai_assistance_record.hard_constraint_rule || !data.ai_assistance_record.human_override_rule) throw new Error("AI assistance needs explicit hard-constraint and human-override rules.");
if (validations.status !== "preregistered_protocol_only_not_field_run" || validations.field_performance !== null) throw new Error("Validation protocols must remain preregistered and field-null.");
if (validations.professional_signoff !== false || validations.affected_public_signoff !== false || validations.currency_quotes !== null) throw new Error("Pending sign-off and quote states must stay explicit.");
if (validations.protocols.length !== data.cases.length) throw new Error("Every spatial case needs one preregistered validation protocol.");

const requiredPermitFields = ["place_condition", "time_window", "max_footprint", "kit", "minimum_staff", "valid_until", "restore"];
const actionFeatures = actions.features.filter((feature) => feature.geometry);
const actionByOption = new Map(actions.features.filter((feature) => feature.properties.option_id).map((feature) => [feature.properties.option_id, feature]));
const actionById = new Map(actions.features.map((feature) => [feature.properties.id, feature]));
const protocolByCase = new Map(validations.protocols.map((protocol) => [protocol.case_id, protocol]));
if (actionByOption.size !== 9) throw new Error(`Expected 9 mapped spatial options, got ${actionByOption.size}.`);
if (context.processing_pad_deg !== 0) throw new Error("Public-context windows must be strict-clipped with zero processing pad.");

function walkCoordinates(value, output = []) {
  if (Array.isArray(value) && value.length >= 2 && typeof value[0] === "number" && typeof value[1] === "number") output.push(value);
  else if (Array.isArray(value)) for (const item of value) walkCoordinates(item, output);
  return output;
}

function bboxOf(feature) {
  const coordinates = walkCoordinates(feature.geometry.coordinates);
  return [
    Math.min(...coordinates.map((point) => point[0])),
    Math.min(...coordinates.map((point) => point[1])),
    Math.max(...coordinates.map((point) => point[0])),
    Math.max(...coordinates.map((point) => point[1]))
  ];
}

function intersects(a, b) {
  return !(a[2] < b[0] || b[2] < a[0] || a[3] < b[1] || b[3] < a[1]);
}

function orientation(a, b, c) {
  return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]);
}

function segmentCrosses(a, b, c, d) {
  const o1 = orientation(a, b, c), o2 = orientation(a, b, d), o3 = orientation(c, d, a), o4 = orientation(c, d, b);
  return ((o1 > 0 && o2 < 0) || (o1 < 0 && o2 > 0)) && ((o3 > 0 && o4 < 0) || (o3 < 0 && o4 > 0));
}

function lineCrossesFeature(lineFeature, contextFeature) {
  const line = walkCoordinates(lineFeature.geometry.coordinates);
  const contextLine = walkCoordinates(contextFeature.geometry.coordinates);
  for (let i = 0; i < line.length - 1; i += 1) {
    for (let j = 0; j < contextLine.length - 1; j += 1) {
      if (segmentCrosses(line[i], line[i + 1], contextLine[j], contextLine[j + 1])) return true;
    }
  }
  return false;
}

for (const feature of actionFeatures) {
  const window = context.windows[feature.properties.window];
  if (!window) throw new Error(`${feature.properties.id}: missing public-context window.`);
  const [minX, minY, maxX, maxY] = bboxOf(feature);
  const [west, south, east, north] = window.bbox;
  if (minX < west || maxX > east || minY < south || maxY > north) throw new Error(`${feature.properties.id}: geometry leaves declared study window.`);
}

const exclusions = actionFeatures.filter((feature) => feature.properties.role === "desktop_exclusion_zone");
const buildings = context.features.filter((feature) => feature.properties.context_kind === "building" && feature.geometry);
const publicRoadRail = context.features.filter((feature) => ["road", "railway"].includes(feature.properties.context_kind) && feature.geometry);
let options = 0;
let selectedSpatialChoices = 0;
let selectedBuildingCollisions = 0;
let selectedExclusionCollisions = 0;
let selectedPublicRoadRailIntersections = 0;
let selectedNonDazhongsiRoadRailRelations = 0;
let selectedSpatialBands = 0;
let selectedBandWidthTotalM = 0;
let aiRankOneOverriddenByHardConstraint = 0;
let preregisteredValidationProtocols = 0;
let protocolsWithCompleteMeasurementChain = 0;
for (const item of data.cases) {
  if (item.options.length !== 3) throw new Error(`${item.case_id}: exactly 3 options required.`);
  options += item.options.length;
  if (item.options.filter((option) => option.human_decision === "select_conditionally").length !== 1) {
    throw new Error(`${item.case_id}: exactly one conditionally selected human decision required.`);
  }
  const selectedOption = item.options.find((option) => option.human_decision === "select_conditionally");
  const aiFirst = item.options.find((option) => option.ai_rank === 1);
  if (!aiFirst) throw new Error(`${item.case_id}: exactly one AI rank-one option is required.`);
  if (selectedOption.option_id !== aiFirst.option_id) aiRankOneOverriddenByHardConstraint += 1;
  if (!selectedOption.hard_gate || selectedOption.hard_gate !== "DESKTOP_PASS_FIELD_PENDING") throw new Error(`${item.case_id}: selected option must retain a field-pending desktop pass.`);
  if (!aiFirst.hard_gate) throw new Error(`${item.case_id}: AI rank-one option needs an auditable hard-gate result.`);
  for (const option of item.options) {
    const action = actionByOption.get(option.option_id);
    if (!action) throw new Error(`${option.option_id}: no spatial action geometry.`);
    if (action.properties.human_decision !== option.human_decision) throw new Error(`${option.option_id}: human decision mismatch.`);
    if (option.human_decision === "select_conditionally") {
      selectedSpatialChoices += 1;
      if (!action.properties.section_id || !actionById.has(action.properties.section_id)) throw new Error(`${option.option_id}: selected action needs a mapped section line.`);
      if ((action.properties.rights_status || "unknown") === "unknown") throw new Error(`${option.option_id}: selected action cannot hide unknown rights.`);
      if (action.properties.engineering_status === "missing") throw new Error(`${option.option_id}: missing engineering evidence cannot be selected.`);
      const actionBox = bboxOf(action);
      const localBuildings = buildings.filter((feature) => feature.properties.window === action.properties.window && intersects(actionBox, bboxOf(feature)));
      const localExclusions = exclusions.filter((feature) => feature.properties.window === action.properties.window && intersects(actionBox, bboxOf(feature)));
      const localPublicRoadRail = publicRoadRail.filter((feature) => feature.properties.window === action.properties.window && lineCrossesFeature(action, feature));
      selectedBuildingCollisions += localBuildings.length;
      selectedExclusionCollisions += localExclusions.length;
      if (action.properties.window === "dazhongsi") selectedPublicRoadRailIntersections += localPublicRoadRail.length;
      else selectedNonDazhongsiRoadRailRelations += localPublicRoadRail.length;
      if (localBuildings.length || localExclusions.length || (action.properties.window === "dazhongsi" && localPublicRoadRail.length)) throw new Error(`${option.option_id}: selected desktop geometry collides with ${localBuildings.length} building(s), ${localExclusions.length} exclusion zone(s), and ${localPublicRoadRail.length} blocking Dazhongsi road/rail feature(s).`);
      const band = action.properties.spatial_band;
      if (!band || action.properties.cross_tie_type === undefined) throw new Error(`${option.option_id}: selected action needs one site-specific spatial band.`);
      const parts = [band.ordinary_clear_route_target_m, band.heritage_memory_seam_target_m, band.removable_ai_sideband_target_m, band.permanent_edge_target_m];
      if (parts.some((value) => typeof value !== "number" || value <= 0)) throw new Error(`${option.option_id}: every spatial-band component needs a positive conditional target.`);
      const componentTotal = parts.reduce((sum, value) => sum + value, 0);
      if (Math.abs(componentTotal - band.width_target_m) > 1e-9) throw new Error(`${option.option_id}: spatial-band components do not equal the stated width target.`);
      if (band.width_status !== "conditional_design_target_field_width_pending") throw new Error(`${option.option_id}: width target must remain explicitly conditional.`);
      if (!band.heritage_trigger || !band.ordinary_city_after_expiry) throw new Error(`${option.option_id}: heritage trigger and post-expiry ordinary-city state are required.`);
      selectedSpatialBands += 1;
      selectedBandWidthTotalM += band.width_target_m;
    }
  }
  for (const field of requiredPermitFields) if (!item.permit[field]) throw new Error(`${item.case_id}: missing permit.${field}`);
  const protocol = protocolByCase.get(item.case_id);
  if (!protocol || item.validation_protocol_ref !== `visual/assets/preregistered-validation-protocols.json#${item.case_id}`) throw new Error(`${item.case_id}: validation protocol reference does not resolve.`);
  if (protocol.selected_option_id !== selectedOption.option_id || protocol.project_id === undefined) throw new Error(`${item.case_id}: validation protocol must bind the selected option and project.`);
  if (protocol.baseline.status !== "pending_field_measurement" || !protocol.baseline.ordinary_no_ai_condition || !protocol.baseline.observation_location_rule || !protocol.baseline.comparison) throw new Error(`${item.case_id}: incomplete no-AI baseline and comparison design.`);
  if (!protocol.sample_plan.unit || !protocol.sample_plan.minimum || !protocol.sample_plan.frequency) throw new Error(`${item.case_id}: incomplete sample plan.`);
  const measurement = protocol.measurement;
  if (!Array.isArray(measurement.methods) || measurement.methods.length < 2 || !Array.isArray(measurement.preregistered_pass) || measurement.preregistered_pass.length < 3 || !Array.isArray(measurement.hold) || measurement.hold.length < 2 || !measurement.missing_or_anomalous_data) throw new Error(`${item.case_id}: incomplete measurement/pass/hold/missing-data chain.`);
  if (!protocol.roles.collector || !protocol.roles.reviewer || !protocol.roles.signatory || !Array.isArray(protocol.evidence_outputs) || protocol.evidence_outputs.length < 3 || !protocol.restore) throw new Error(`${item.case_id}: incomplete responsibility/evidence/restore chain.`);
  if (item.case_id === "CT-03") {
    const unit = protocol.inquiry_ready_validation_unit;
    if (!unit || unit.status !== "conditional_inquiry_performance_brief_not_purchase_order_not_construction_design" || unit.length_target_m !== 12 || unit.sideband_width_target_m !== 2.4) throw new Error("CT-03: the 12 m inquiry-ready validation brief is missing or overclaimed.");
    const interval = unit.desktop_reference_interval;
    if (!interval || interval.status !== "provisional_centered_reference_not_final_setout" || interval.candidate_chainage_start_target_m !== 43.3 || interval.candidate_chainage_end_target_m !== 55.3 || Math.abs(interval.candidate_chainage_end_target_m - interval.candidate_chainage_start_target_m - unit.length_target_m) > 1e-9 || !interval.relocation_or_cancel_rule) throw new Error("CT-03: the provisional 12 m chainage and relocate-or-cancel rule are incomplete.");
    if (!unit.dimensional_rule || !unit.dimensional_rule.includes("exact component dimensions and heights remain null")) throw new Error("CT-03: dimensional nulls must remain explicit.");
    if (!Array.isArray(unit.components) || unit.components.length !== 6 || unit.components.some((component) => !component.id || !component.item || !component.quantity || !component.requirement)) throw new Error("CT-03: six countable performance-specified components are required.");
    if (unit.removal_target_hours !== 4 || !unit.quotation_rule.includes("no purchase order is authorized") || !unit.quotation_rule.includes("currency values remain null") || !Array.isArray(unit.acceptance_documents) || unit.acceptance_documents.length < 5) throw new Error("CT-03: removal, inquiry, and acceptance-document requirements are incomplete.");
  }
  preregisteredValidationProtocols += 1;
  protocolsWithCompleteMeasurementChain += 1;
}

process.stdout.write(JSON.stringify({
  result: "PASS",
  mode: "read_only_zero_network_synthetic_permit_tabletop",
  cross_tie_cases: data.cases.length,
  compared_options: options,
  options_with_public_coordinate_geometry: actionByOption.size,
  selected_spatial_choices: selectedSpatialChoices,
  selected_building_collisions: selectedBuildingCollisions,
  selected_exclusion_collisions: selectedExclusionCollisions,
  selected_dazhongsi_public_map_road_rail_intersections: selectedPublicRoadRailIntersections,
  selected_other_site_public_map_road_rail_relations_pending_field_design: selectedNonDazhongsiRoadRailRelations,
  selected_site_specific_spatial_bands: selectedSpatialBands,
  selected_spatial_band_width_target_total_m: Number(selectedBandWidthTotalM.toFixed(1)),
  ordinary_clear_route_target_m_each: 3.0,
  spatial_band_width_status: "conditional_design_target_field_width_pending",
  mapped_section_lines: actions.features.filter((feature) => feature.properties.role === "section_line").length,
  public_context_processing_pad_deg: context.processing_pad_deg,
  permits_with_all_fields: data.cases.length,
  design_team_desktop_conditionally_preferred_options: data.cases.length,
  ai_rank_one_overridden_by_city_hard_constraint: aiRankOneOverriddenByHardConstraint,
  preregistered_validation_protocols: preregisteredValidationProtocols,
  protocols_with_complete_baseline_sample_method_threshold_role_evidence_restore_chain: protocolsWithCompleteMeasurementChain,
  professional_signoff_completed: false,
  affected_public_signoff_completed: false,
  currency_quotes: null,
  dazhongsi_inquiry_ready_validation_unit_length_target_m: protocolByCase.get("CT-03").inquiry_ready_validation_unit.length_target_m,
  dazhongsi_inquiry_ready_component_types: protocolByCase.get("CT-03").inquiry_ready_validation_unit.components.length,
  dazhongsi_desktop_reference_chainage_start_target_m: protocolByCase.get("CT-03").inquiry_ready_validation_unit.desktop_reference_interval.candidate_chainage_start_target_m,
  dazhongsi_desktop_reference_chainage_end_target_m: protocolByCase.get("CT-03").inquiry_ready_validation_unit.desktop_reference_interval.candidate_chainage_end_target_m,
  named_professional_and_affected_public_selection_completed: false,
  field_performance: null,
  deployment_decision: "not_authorized_not_run"
}, null, 2) + "\n");
