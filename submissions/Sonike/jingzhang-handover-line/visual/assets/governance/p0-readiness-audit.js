#!/usr/bin/env node
/* 京张交接线 · P0 可实施性与公共利益就绪审计器（离线、只读、零第三方依赖） */
"use strict";

const fs = require("fs");
const path = require("path");

const HERE = process.env.JZ_AUDIT_HOME ? path.resolve(process.env.JZ_AUDIT_HOME) : __dirname;
const PKG = path.resolve(HERE, "../../..");
const OVERLAY = process.env.JZ_AUDIT_OVERLAY ? path.resolve(process.env.JZ_AUDIT_OVERLAY) : null;
const errors = [];

const resolveIn = (base, rel, key) => {
  if (OVERLAY) {
    const candidate = path.join(OVERLAY, key || rel);
    if (fs.existsSync(candidate)) return candidate;
  }
  return path.join(base, rel);
};
const readText = (rel) => {
  const file = resolveIn(PKG, rel);
  if (!fs.existsSync(file)) {
    errors.push(`缺少文件 ${rel}`);
    return "";
  }
  return fs.readFileSync(file, "utf8");
};
const readJSON = (rel) => {
  const text = readText(rel);
  if (!text) return null;
  try { return JSON.parse(text); }
  catch (error) {
    errors.push(`${rel} 不是有效 JSON：${error.message}`);
    return null;
  }
};
const exactSet = (actual, expected) =>
  Array.isArray(actual) && actual.length === expected.length && expected.every((item) => actual.includes(item));

const DELIVERY_PATH = "visual/assets/governance/p0-delivery-contract.json";
const PUBLIC_PATH = "visual/assets/governance/public-benefit-gate.json";
const REVIEW_PATH = "visual/assets/governance/review-3825-readiness-matrix.json";
const PROTOTYPE_PATH = "visual/index.html";
const PROTOTYPE_LINK = "visual/index.html#p0-prototype";
const EXPECTED_SCENARIOS = Array.from({ length: 12 }, (_, index) => `SCN-${String(index + 1).padStart(2, "0")}`);
const EXPECTED_GROUPS = [
  "residents", "youth_talent", "enterprises", "universities", "visitors", "marginalized_groups",
];
const EXPECTED_GATES = [
  "site_authorisation",
  "independent_roles",
  "safety_accessibility",
  "insurance_maintenance",
  "data_minimisation_deletion",
  "cost_quotes_sustained_budget",
  "fire_transport_utilities",
  "co_testing_consent_accommodation",
];
const EXPECTED_STAGES = ["PRE-D0", "D0", "D1-D30", "D31-D60", "D61-D90"];
const EXPECTED_ACCEPTANCE = [
  "same_core_outcome",
  "task_success_gap",
  "completion_time_ratio",
  "queue_and_price_parity",
  "essential_safety_information",
  "device_and_algorithm_refusal",
  "complaint_stop_receipt",
  "accessibility_essential_tasks",
];
const EXPECTED_RACI_PACKAGES = [
  "site_authorisation",
  "independent_review",
  "human_service_floor",
  "smart_layer_installation",
  "cotest_recruitment_and_consent",
  "data_and_deletion",
  "field_rehearsal",
  "complaint_and_dissent",
  "acceptance_decision",
  "same_day_rollback_and_restoration",
];
const EXPECTED_PROTECTIONS = [
  "public_life_before_technology_display",
  "non_consumption_access",
  "no_mandatory_personal_device",
  "no_mandatory_face_recognition",
  "human_responsibility_and_appeal",
  "minimum_data_and_deletion",
  "child_older_and_disability_safety",
  "shade_rest_low_light_low_noise",
];
const EXPECTED_ELIGIBILITY_CHECKS = [
  "privacy_personal_or_nonpublic_data",
  "fabricated_official_endorsement",
  "unlawful_discriminatory_malicious",
  "material_irrelevance",
  "agent_taskbook_coverage",
  "settled_government_decision",
];
const EXPECTED_REVIEW_ITEMS = [
  "R96-01", "R96-02", "R96-03", "R96-04", "R96-05", "R96-06", "R96-07",
];

const delivery = readJSON(DELIVERY_PATH);
const publicGate = readJSON(PUBLIC_PATH);
const reviewMatrix = readJSON(REVIEW_PATH);
const prototype = readText(PROTOTYPE_PATH);
const metricsDoc = readJSON("metrics.json");
const compliance = readJSON("compliance_matrix.json");
const roleSpec = readJSON("visual/assets/governance/role-spec.json");
const proposalZh = readText("proposal.md");
const proposalEn = readText("proposal.en.md");
const visualZh = readText("visual/index.html");
const visualEn = readText("visual/index.en.html");

let validEntryGates = 0;
let validStages = 0;
let validRaciPackages = 0;
let validBomItems = 0;
let validAcceptanceCriteria = 0;
if (delivery) {
  if (delivery.evidence_level !== "E2_preregistered_delivery_contract") {
    errors.push("P0 evidence_level 必须是 E2_preregistered_delivery_contract");
  }
  if (delivery.activation_state !== "not_started") errors.push("P0 activation_state 必须保持 not_started");
  if (!delivery.scope || delivery.scope.pilot_scenario_id !== "SCN-05" || delivery.scope.one_scenario_only !== true) {
    errors.push("P0 必须先锁定 SCN-05 单一场景，不得一次扩到十二场景");
  }
  for (const key of ["site_authorisation_received", "professional_signoff_received", "insurance_received",
    "three_quotes_received", "sustained_budget_committed", "field_rehearsal_completed"]) {
    if (!delivery.current_evidence || delivery.current_evidence[key] !== false) {
      errors.push(`current_evidence.${key} 必须如实保持 false`);
    }
  }
  if (!delivery.current_evidence || delivery.current_evidence.real_participant_observations !== 0) {
    errors.push("P0 真实参与者观察数必须保持 0");
  }

  const gates = Array.isArray(delivery.entry_gates) ? delivery.entry_gates : [];
  if (!exactSet(gates.map((item) => item.gate_id), EXPECTED_GATES)) errors.push("P0 八道进入门集合不完整");
  for (const gate of gates) {
    const local = [];
    if (gate.status !== "not_started") local.push("status 不是 not_started");
    if (gate.evidence_received_count !== 0) local.push("evidence_received_count 不是 0");
    if (!Array.isArray(gate.required_evidence) || gate.required_evidence.length < 2) local.push("required_evidence 少于 2 项");
    if (!String(gate.on_fail || "").includes("smart_layer_off")) local.push("失败动作未关闭智能层");
    if (local.length) errors.push(`${gate.gate_id || "未知进入门"}: ${local.join("；")}`);
    else validEntryGates += 1;
  }

  const stages = Array.isArray(delivery.delivery_stages) ? delivery.delivery_stages : [];
  if (!exactSet(stages.map((item) => item.stage_id), EXPECTED_STAGES)) errors.push("P0 五阶段 90 天路径不完整");
  for (const stage of stages) {
    const local = [];
    if (stage.status !== "not_started") local.push("status 不是 not_started");
    if (!Array.isArray(stage.deliverables) || stage.deliverables.length < 2) local.push("deliverables 少于 2 项");
    if (!Array.isArray(stage.exit_evidence) || stage.exit_evidence.length < 2) local.push("exit_evidence 少于 2 项");
    if (!String(stage.rollback || "").includes("基础人工服务")) local.push("rollback 未保留基础人工服务");
    if (local.length) errors.push(`${stage.stage_id || "未知阶段"}: ${local.join("；")}`);
    else validStages += 1;
  }

  const roleIds = new Set(((roleSpec && roleSpec.roles) || []).map((item) => item.role_id));
  const raci = Array.isArray(delivery.raci_work_packages) ? delivery.raci_work_packages : [];
  if (!exactSet(raci.map((item) => item.work_package_id), EXPECTED_RACI_PACKAGES)) errors.push("P0 十项 RACI 工作包不完整");
  for (const item of raci) {
    const local = [];
    if (!Array.isArray(item.responsible_role_ids) || item.responsible_role_ids.length < 1) local.push("没有 R 角色");
    if (!item.accountable_role_id) local.push("没有唯一 A 角色");
    for (const role of [...(item.responsible_role_ids || []), item.accountable_role_id].filter(Boolean)) {
      if (!roleIds.has(role)) local.push(`角色 ${role} 未登记在 role-spec`);
    }
    if (item.assignment_status !== "unassigned") local.push("assignment_status 不是 unassigned");
    if (local.length) errors.push(`${item.work_package_id || "未知工作包"}: ${local.join("；")}`);
    else validRaciPackages += 1;
  }

  const bom = Array.isArray(delivery.component_schedule) ? delivery.component_schedule : [];
  if (bom.length !== 12) errors.push(`P0 构件清单 ${bom.length} 项，应为 12 项`);
  for (const item of bom) {
    const local = [];
    if (!(Number.isFinite(item.quantity) && item.quantity > 0)) local.push("quantity 无效");
    if (!String(item.unit || "").trim()) local.push("unit 缺失");
    if (!String(item.acceptance_check_zh || "").trim()) local.push("acceptance_check_zh 缺失");
    if (item.procurement_status !== "not_quoted") local.push("procurement_status 不是 not_quoted");
    if (item.unit_price_cny !== null || item.total_price_cny !== null) local.push("未询价却填写了价格");
    if (local.length) errors.push(`${item.item_id || "未知构件"}: ${local.join("；")}`);
    else validBomItems += 1;
  }
  const quotes = delivery.procurement && delivery.procurement.quote_slots;
  if (!Array.isArray(quotes) || quotes.length !== 3 || quotes.some((item) =>
    item.vendor !== null || item.amount_cny !== null || item.received_at !== null)) {
    errors.push("三方询价槽位必须恰为 3 个且在真实询价前保持 null");
  }
  if (!delivery.procurement || delivery.procurement.cost_class !== "S" || delivery.procurement.total_budget_cny !== null) {
    errors.push("P0 只能声明 S 级成本，真实总预算在询价前必须为 null");
  }

  const acceptance = Array.isArray(delivery.preregistered_acceptance_criteria)
    ? delivery.preregistered_acceptance_criteria : [];
  if (!exactSet(acceptance.map((item) => item.criterion_id), EXPECTED_ACCEPTANCE)) {
    errors.push("P0 八项预注册验收判据不完整");
  }
  for (const item of acceptance) {
    const local = [];
    if (!String(item.measure || "").trim()) local.push("measure 缺失");
    if (!String(item.pass_rule || "").trim()) local.push("pass_rule 缺失");
    if (!String(item.stop_rule || "").includes("smart_layer_off")) local.push("stop_rule 未关闭智能层");
    if (item.observed_value !== null || item.status !== "not_observed") local.push("未实测却出现结果");
    if (local.length) errors.push(`${item.criterion_id || "未知验收项"}: ${local.join("；")}`);
    else validAcceptanceCriteria += 1;
  }
  const cotest = delivery.cotesting_protocol || {};
  if (cotest.participant_session_minimum !== 24 || cotest.current_participant_sessions !== 0) {
    errors.push("共测须预注册至少 24 个任务场次，当前真实场次保持 0");
  }
  if (!exactSet(cotest.required_rubric_groups, EXPECTED_GROUPS)) errors.push("共测未覆盖任务书六类公共群体");
  if (!Array.isArray(cotest.access_accommodations) || cotest.access_accommodations.length < 8) {
    errors.push("共测便利与合理调整少于 8 项");
  }
}

let validGroups = 0;
let validScenarioGates = 0;
let validProtections = 0;
if (publicGate) {
  if (publicGate.evidence_level !== "E2_preregistered_public_value_contract") {
    errors.push("公共利益 evidence_level 必须是 E2_preregistered_public_value_contract");
  }
  if (publicGate.activation_state !== "specified_not_observed") errors.push("公共利益 gate 必须保持 specified_not_observed");
  const decision = publicGate.decision_rule || {};
  for (const key of ["public_benefit_is_entry_condition", "public_life_precedes_technology_display",
    "smart_layer_closes_when_public_floor_fails", "basic_service_continues_after_closure"]) {
    if (decision[key] !== true) errors.push(`公共利益 decision_rule.${key} 必须为 true`);
  }

  const groups = Array.isArray(publicGate.beneficiary_groups) ? publicGate.beneficiary_groups : [];
  if (!exactSet(groups.map((item) => item.group_id), EXPECTED_GROUPS)) errors.push("任务书六类公共群体集合不完整");
  for (const group of groups) {
    const local = [];
    if (!String(group.public_value_zh || "").trim()) local.push("public_value_zh 缺失");
    if (!String(group.no_ai_access_zh || "").trim()) local.push("no_ai_access_zh 缺失");
    if (!Array.isArray(group.evidence_to_collect) || group.evidence_to_collect.length < 2) local.push("待采证据少于 2 项");
    if (group.status !== "specified_not_observed" || group.observed_participant_count !== 0) local.push("被写成已观察");
    if (local.length) errors.push(`${group.group_id || "未知群体"}: ${local.join("；")}`);
    else validGroups += 1;
  }

  const protections = Array.isArray(publicGate.cross_cutting_protections)
    ? publicGate.cross_cutting_protections : [];
  if (!exactSet(protections.map((item) => item.protection_id), EXPECTED_PROTECTIONS)) {
    errors.push("八项跨场景公共保护集合不完整");
  }
  for (const item of protections) {
    if (!String(item.requirement_zh || "").trim() || !String(item.failure_action || "").includes("smart_layer_off")) {
      errors.push(`${item.protection_id || "未知保护"}: 要求或关闭动作缺失`);
    } else validProtections += 1;
  }

  const scenarioGates = Array.isArray(publicGate.scenario_public_value_gates)
    ? publicGate.scenario_public_value_gates : [];
  if (!exactSet(scenarioGates.map((item) => item.scenario_id), EXPECTED_SCENARIOS)) {
    errors.push("十二场景公共利益硬门槛集合不完整");
  }
  for (const item of scenarioGates) {
    const local = [];
    if (!Array.isArray(item.primary_group_ids) || item.primary_group_ids.length < 2 ||
        item.primary_group_ids.some((group) => !EXPECTED_GROUPS.includes(group))) local.push("受益群体无效或少于 2 类");
    if (!String(item.public_benefit_zh || "").trim()) local.push("公共收益缺失");
    if (!String(item.harm_to_avoid_zh || "").trim()) local.push("要避免的伤害缺失");
    if (!Array.isArray(item.safeguards) || item.safeguards.length < 3) local.push("保障少于 3 项");
    if (!String(item.stop_condition_zh || "").includes("关闭智能层")) local.push("停止条件未关闭智能层");
    if (!String(item.non_tech_remainder_zh || "").trim()) local.push("关闭后公共遗产缺失");
    if (item.status !== "specified_not_observed") local.push("被写成已观察");
    if (local.length) errors.push(`${item.scenario_id || "未知场景"}: ${local.join("；")}`);
    else validScenarioGates += 1;
  }
}

let validEligibilityChecks = 0;
let validReviewItems = 0;
if (reviewMatrix) {
  if (reviewMatrix.package_result !== "CLOSED_FOR_FORMAL_REVIEW") {
    errors.push("投稿包自评结果必须为 CLOSED_FOR_FORMAL_REVIEW");
  }
  if (reviewMatrix.participant_controlled_open_repair_count !== 0) {
    errors.push("当前参与者可控制的开放修复项必须为 0");
  }
  if (reviewMatrix.field_pilot_result !== "BLOCKED_EXTERNAL_PRE_PILOT") {
    errors.push("真实现场试点必须保持 BLOCKED_EXTERNAL_PRE_PILOT");
  }
  if (reviewMatrix.public_performance_claim_result !== "BLOCKED_UNTIL_24_REAL_TASKS") {
    errors.push("公众绩效主张必须保持 BLOCKED_UNTIL_24_REAL_TASKS");
  }
  if (reviewMatrix.official_geometry_result !== "WAITING_ORGANIZER_INPUT") {
    errors.push("正式几何必须保持 WAITING_ORGANIZER_INPUT");
  }
  const eligibility = Array.isArray(reviewMatrix.eligibility_evidence)
    ? reviewMatrix.eligibility_evidence : [];
  if (!exactSet(eligibility.map((item) => item.check_id), EXPECTED_ELIGIBILITY_CHECKS)) {
    errors.push("正式评审资格六项事实核对不完整");
  }
  for (const item of eligibility) {
    const local = [];
    if (item.rejection_condition_observed !== false) local.push("拒绝条件未保持 false");
    if (!Array.isArray(item.evidence_refs) || item.evidence_refs.length < 2) local.push("证据少于 2 项");
    if (!String(item.finding_zh || "").trim() || !String(item.finding_en || "").trim()) local.push("双语事实结论缺失");
    if (local.length) errors.push(`${item.check_id || "未知资格核对"}: ${local.join("；")}`);
    else validEligibilityChecks += 1;
  }
  const issues = Array.isArray(reviewMatrix.issues) ? reviewMatrix.issues : [];
  if (!exactSet(issues.map((item) => item.review_item_id), EXPECTED_REVIEW_ITEMS)) {
    errors.push("96 分评审七项后续动作映射不完整");
  }
  for (const item of issues) {
    const local = [];
    if (item.participant_controlled_current_repair !== false) local.push("被误标为当前参与者修复");
    if (!String(item.classification || "").trim() || !String(item.status || "").trim()) local.push("分类或状态缺失");
    if (!Array.isArray(item.evidence_refs) || item.evidence_refs.length < 1) local.push("证据引用缺失");
    if (String(item.status || "").startsWith("OPEN_PARTICIPANT")) local.push("仍有开放参与者修复");
    if (local.length) errors.push(`${item.review_item_id || "未知评审项"}: ${local.join("；")}`);
    else validReviewItems += 1;
  }
}

const readiness = compliance && compliance.formal_review_readiness_boundary;
if (!readiness) {
  errors.push("compliance_matrix.json 缺 formal_review_readiness_boundary");
} else {
  if (readiness.source !== REVIEW_PATH) errors.push("正式评审边界未指向唯一修复矩阵");
  if (readiness.assessment_owner !== "participant_self_audit") errors.push("正式评审边界必须声明为参与者自审");
  if (readiness.package_result !== "CLOSED_FOR_FORMAL_REVIEW" ||
      readiness.participant_controlled_open_repair_count !== 0) {
    errors.push("合规矩阵未把当前投稿闭合与开放修复数锁定为 CLOSED / 0");
  }
  if (readiness.eligibility_rejection_condition_observed_count !== 0 ||
      readiness.eligibility_evidence_check_count !== EXPECTED_ELIGIBILITY_CHECKS.length) {
    errors.push("合规矩阵资格事实核对计数必须为 6 项／0 命中");
  }
  if (readiness.field_pilot_result !== "BLOCKED_EXTERNAL_PRE_PILOT" ||
      readiness.public_performance_claim_result !== "BLOCKED_UNTIL_24_REAL_TASKS") {
    errors.push("合规矩阵未保持现场与公众绩效主张双重阻断");
  }
}

const deliveryBoundary = delivery && delivery.formal_review_boundary;
if (!deliveryBoundary || deliveryBoundary.package_result !== "CLOSED_FOR_FORMAL_REVIEW" ||
    deliveryBoundary.field_pilot_result !== "BLOCKED_EXTERNAL_PRE_PILOT" ||
    deliveryBoundary.participant_controlled_open_repair_count !== 0) {
  errors.push("P0 交付合同未分离投稿包闭合与现场试点阻断");
}

const readinessPhrases = [
  ["proposal.md", proposalZh, "CLOSED_FOR_FORMAL_REVIEW", "BLOCKED_EXTERNAL_PRE_PILOT"],
  ["proposal.en.md", proposalEn, "CLOSED_FOR_FORMAL_REVIEW", "BLOCKED_EXTERNAL_PRE_PILOT"],
];
for (const [name, text, packageStatus, fieldStatus] of readinessPhrases) {
  if (!text.includes(packageStatus) || !text.includes(fieldStatus)) {
    errors.push(`${name} 未明确分离投稿包闭合与现场阻断`);
  }
}

let validPrototypeChecks = 0;
const prototypeChecks = [
  ["离线证据标记", /data-evidence-state="synthetic-offline-prototype"/],
  ["跳转到主内容", /class="skip-link"[^>]*href="#main"/],
  ["状态播报", /aria-live="polite"/],
  ["智能路线", /data-service-route="smart-assist"/],
  ["无 AI 路线", /data-service-route="no-ai-human"/],
  ["相同核心结果", (text) => (text.match(/data-core-result-id="SCN-05-CORE-001"/g) || []).length >= 2],
  ["关闭智能层控件", /id="smart-off"/],
  ["拒绝数据控件", /id="refuse-data"/],
  ["投诉与停用回执", /id="issue-receipt"/],
  ["大字模式", /id="large-text"/],
  ["高对比模式", /id="high-contrast"/],
  ["中英核心信息切换", (text) => /id="language-toggle"/.test(text) &&
    /id="p0-prototype"[^>]*lang="zh-CN"/.test(text) &&
    (text.match(/data-zh="[^"]+" data-en="[^"]+"/g) || []).length >= 18 &&
    /function p0English\(\)/.test(text) &&
    /prototype\.lang\s*=\s*english\s*\?\s*'en'\s*:\s*'zh-CN'/.test(text) &&
    text.includes("Synthetic smart suggestion") && text.includes("Staffed and paper route")],
  ["打印纸本", /id="print-card"/],
  ["真实现场边界", /真实参与者观察[^0]*0/],
];
for (const [name, test] of prototypeChecks) {
  const ok = typeof test === "function" ? test(prototype) : test.test(prototype);
  if (!ok) errors.push(`P0 原型缺少：${name}`); else validPrototypeChecks += 1;
}
const prohibitedPrototypePatterns = [
  [/https?:\/\//i, "远程 URL"],
  [/\bfetch\s*\(/, "fetch 网络请求"],
  [/XMLHttpRequest|WebSocket|EventSource/, "主动网络 API"],
  [/localStorage|sessionStorage|document\.cookie/, "持久化浏览器存储"],
  [/<input[^>]+(?:name|id)=["'](?:name|phone|email|id_card)/i, "个人信息输入字段"],
];
for (const [pattern, label] of prohibitedPrototypePatterns) {
  if (pattern.test(prototype)) errors.push(`P0 原型不得包含 ${label}`);
}

const requiredPageLinks = [
  ["proposal.md", proposalZh, PROTOTYPE_LINK],
  ["proposal.en.md", proposalEn, PROTOTYPE_LINK],
  ["visual/index.html", visualZh, "id=\"p0-prototype\""],
  ["visual/index.en.html", visualEn, "index.html#p0-prototype"],
];
for (const [name, text, needle] of requiredPageLinks) {
  if (!text.includes(needle)) errors.push(`${name} 未链接 P0 可操作原型`);
}

const metrics = (metricsDoc && metricsDoc.metrics) || {};
const expectedMetrics = {
  p0_entry_gate_count: 8,
  p0_delivery_stage_count: 5,
  p0_raci_work_package_count: 10,
  p0_component_line_item_count: 12,
  p0_preregistered_acceptance_criterion_count: 8,
  public_benefit_group_count: 6,
  scenario_public_benefit_gate_count: 12,
  offline_service_prototype_route_count: 2,
  planned_equity_cotest_session_min_count: 24,
};
for (const [id, expected] of Object.entries(expectedMetrics)) {
  const value = metrics[id] && metrics[id].value;
  if (value !== expected) errors.push(`metrics.${id} 应为 ${expected}，实为 ${JSON.stringify(value)}`);
}

const result = {
  ok: errors.length === 0,
  pilot_scenario_id: delivery && delivery.scope && delivery.scope.pilot_scenario_id,
  entry_gates_valid: validEntryGates,
  delivery_stages_valid: validStages,
  raci_work_packages_valid: validRaciPackages,
  component_line_items_valid: validBomItems,
  acceptance_criteria_valid: validAcceptanceCriteria,
  public_benefit_groups_valid: validGroups,
  scenario_public_value_gates_valid: validScenarioGates,
  cross_cutting_protections_valid: validProtections,
  eligibility_evidence_checks_valid: validEligibilityChecks,
  review_items_classified_valid: validReviewItems,
  prototype_checks_valid: validPrototypeChecks,
  prototype_checks_expected: prototypeChecks.length,
  real_participant_observations: delivery && delivery.current_evidence && delivery.current_evidence.real_participant_observations,
  errors,
};

if (process.argv.includes("--json")) console.log(JSON.stringify(result, null, 2));
else if (result.ok) {
  console.log("PASS  SCN-05 单场景 P0：8 门／5 阶段／10 RACI／12 构件／8 验收；6 类公共群体／12 场景硬门槛；资格证据 6/6／评审归类 7/7；离线原型 14/14；真实观察 0");
} else {
  console.error("FAIL  P0 可实施性与公共利益就绪包不完整");
  for (const error of errors) console.error(`- ${error}`);
}
process.exit(result.ok ? 0 : 1);
