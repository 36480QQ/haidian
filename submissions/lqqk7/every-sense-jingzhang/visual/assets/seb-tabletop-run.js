#!/usr/bin/env node
/*
 * SEB 桌面配对推演校验器 / SEB tabletop pairing-run checker
 *
 * 方法学演示工具，不构成实测。本脚本只把服务等价基准（seb-spec.json）的四个组件
 * 施加在文本样例（seb-tabletop-fixtures.json）上，不接触任何真实参与者、现场设备
 * 或运行中的系统，不写入 metrics.json，也不产生任何绩效指标数值。它能证明的只有
 * 一件事：判据是否可以被机器逐条执行。
 *
 * Methodology demonstration tool, not a field measurement. The script applies the
 * four components of the Service Equivalence Baseline (seb-spec.json) to text
 * fixtures (seb-tabletop-fixtures.json). It touches no real participant, no site
 * equipment and no running system, writes nothing to metrics.json, and produces no
 * performance metric value. It demonstrates one thing only: whether the criteria
 * can be executed by a machine, item by item.
 *
 * 用法 / Usage: node seb-tabletop-run.js
 * 零依赖，仅使用 Node 内置模块 / Zero dependencies, Node built-ins only.
 * 退出码 0 表示全部样例的判定与 expected_verdict 一致。
 * Exit code 0 means every fixture verdict matched its expected_verdict.
 */

"use strict";

const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const SPEC_PATH = path.join(HERE, "seb-spec.json");
const FIXTURES_PATH = path.join(HERE, "seb-tabletop-fixtures.json");
const NODE_SOURCE_PATH = path.join(HERE, "..", "..", "geometry", "constraints.geojson");

// 把 node_schema 中"不得填写仍依赖同一系统的路径"这句自然语言约束实现为可执行的
// 拒绝词表。词表是本推演工具的解释，不是基准条文本身，见变更回执 CR-2026-08-12-001。
// Machine-executable deny list standing in for the natural-language constraint
// "must not name a route that still depends on the same system". The list is this
// tool's interpretation, not baseline text; see change receipt CR-2026-08-12-001.
const SAME_SYSTEM_PATTERNS = [
  "线上办理", "在线办理", "网上办理", "扫码", "二维码", "小程序",
  "下载应用", "关注公众号", "注册账户", "登录账号",
  "online service", "scan the qr", "download the app", "register an account",
];

// 把"须写明可被找到的角色，不得只写机构名称"实现为角色词表。
// Machine-executable role lexicon for "must name a findable role, not only an organisation".
const ROLE_TOKENS = [
  "人员", "值守", "岗位", "主持人", "代表", "专员", "维护者", "服务员",
  "operator", "officer", "steward", "attendant", "staff",
];

// 分母完整性规则要求与完成数一并报告的失败类别。
// Failure categories the denominator-integrity rule requires alongside completions.
const REQUIRED_DENOMINATOR_CATEGORIES = [
  "completed", "withdrawn", "technical_fault", "non_completion_other",
];

// 拒绝理由的双语解释 / Bilingual explanation of each rejection reason.
const REASON_TEXT = {
  NODE_FIELD_MISSING: ["节点缺少必填字段，不得计入服务覆盖", "node is missing a required field and may not count towards service coverage"],
  NODE_ENUM_INVALID: ["字段取值不在允许集合内", "field value falls outside the allowed set"],
  "NODE_CONSTRAINT_VIOLATION:ai_off_path": ["AI 关闭后的路径仍依赖同一系统，等价性不成立", "the AI-off route still depends on the same system, so equivalence does not hold"],
  "NODE_CONSTRAINT_VIOLATION:human_handoff": ["人工接管只写了机构，没有可被找到的角色", "human takeover names an organisation, not a findable role"],
  DENOMINATOR_SAMPLE_DROPPED: ["分母删除了失败样本，该次测量作废", "a failed sample was dropped from the denominator, voiding that measurement"],
  METRIC_ID_UNKNOWN: ["指标不在基准评分口径内", "the metric lies outside the baseline scoring definitions"],
  LEVEL_UNKNOWN: ["等级不在基准定义内", "the level is not defined by the baseline"],
  LEVEL_BINDING_MISSING: ["等级绑定字段不齐，四项缺一即不得升级", "a level binding field is missing; all four are required before any upgrade"],
  LEVEL_GATE_MISMATCH: ["申报等级与节点所处闸门不一致", "the claimed level and the node gate disagree"],
  STOP_NOT_ENFORCED: ["停止条件触发却以限期整改续跑", "a triggered stop condition was continued under a corrective-action deadline"],
  RESUME_WITHOUT_EVIDENCE: ["以承诺而非证据恢复", "work resumed on a promise rather than on evidence"],
  RISK_ID_UNKNOWN: ["风险条目不在基准判定规则内", "the risk entry lies outside the baseline decision rules"],
  SOURCE_MISMATCH: ["样例与几何文件中的节点属性不一致", "the fixture disagrees with the node attributes held in the geometry file"],
};

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function component(spec, componentId) {
  return spec.components.find((item) => item.component_id === componentId);
}

function containsAny(value, patterns) {
  const text = String(value).toLowerCase();
  return patterns.some((pattern) => text.includes(pattern.toLowerCase()));
}

function explain(code) {
  return REASON_TEXT[code] || REASON_TEXT[code.split(":")[0]] || ["", ""];
}

// 组件一：节点 schema 五个必填字段与两条取值约束。
// Component 1: the five required node fields and the two value constraints.
function checkNodeSchema(node, schema) {
  const reasons = [];
  for (const field of schema.required_fields) {
    const value = node ? node[field.field] : undefined;
    if (typeof value !== "string" || value.trim() === "") {
      reasons.push(`NODE_FIELD_MISSING:${field.field}`);
      continue;
    }
    if (field.type === "enum" && !field.allowed_values.includes(value)) {
      reasons.push(`NODE_ENUM_INVALID:${field.field}`);
    }
    if (field.field === "ai_off_path" && containsAny(value, SAME_SYSTEM_PATTERNS)) {
      reasons.push("NODE_CONSTRAINT_VIOLATION:ai_off_path");
    }
    if (field.field === "human_handoff" && !containsAny(value, ROLE_TOKENS)) {
      reasons.push("NODE_CONSTRAINT_VIOLATION:human_handoff");
    }
  }
  return reasons;
}

// 组件二：评分口径的分母完整性。适用范围由分母文字推导——凡分母写明"有效"样本或
// "成对测试样本"的指标，都属于参与者任务型测量，必须保留失败样本。
// Component 2: denominator integrity. Scope is derived from the denominator wording:
// any metric whose denominator names "valid" samples or paired-test samples is a
// participant-task measurement and must keep its failed samples.
function checkDenominator(declaration, scoring) {
  if (!declaration) return [];
  const reasons = [];
  const metric = scoring.metrics.find((item) => item.metric_id === declaration.metric_id);
  if (!metric) return [`METRIC_ID_UNKNOWN:${declaration.metric_id}`];
  const denominator = metric.denominator_zh || "";
  if (!denominator.includes("有效") && !denominator.includes("成对测试样本")) return reasons;
  const declared = new Set(declaration.denominator_categories_declared || []);
  for (const category of REQUIRED_DENOMINATOR_CATEGORIES) {
    if (!declared.has(category)) reasons.push(`DENOMINATOR_SAMPLE_DROPPED:${category}`);
  }
  for (const category of declaration.denominator_categories_excluded || []) {
    reasons.push(`DENOMINATOR_SAMPLE_DROPPED:${category}`);
  }
  return reasons;
}

// 组件三：等级定义。四项绑定字段缺一不可，且申报等级须与节点所处闸门一致。
// Component 3: level definitions. All four binding fields are required, and the
// claimed level must agree with the gate the node sits at.
function checkLevel(claim, levels, node) {
  const level = levels.levels.find((item) => item.level_id === (claim && claim.level_id));
  if (!level) return [`LEVEL_UNKNOWN:${claim ? claim.level_id : "none"}`];
  const reasons = [];
  for (const field of levels.level_binding_fields) {
    const value = claim[field];
    if (typeof value !== "string" || value.trim() === "") {
      reasons.push(`LEVEL_BINDING_MISSING:${field}`);
    }
  }
  const expectedGate = (String(level.gate).match(/G[0-3]/) || [])[0];
  if (expectedGate && node && node.gate_id && node.gate_id !== expectedGate) {
    reasons.push("LEVEL_GATE_MISMATCH");
  }
  return reasons;
}

// 组件四：判定规则。停止条件触发即停止，恢复须提交证据而不是承诺。
// Component 4: decision rules. A triggered stop condition stops the work, and
// resumption requires submitted evidence rather than a promise.
function checkDecision(decision, rules) {
  const reasons = [];
  const known = new Set(rules.risk_entries.map((item) => item.risk_id));
  for (const riskId of decision.risk_ids || []) {
    if (!known.has(riskId)) reasons.push(`RISK_ID_UNKNOWN:${riskId}`);
  }
  if (decision.stop_condition_triggered) {
    if (decision.action_taken !== "stopped") {
      reasons.push("STOP_NOT_ENFORCED");
    } else if (decision.resumed === true && decision.resumption_basis !== "evidence_submitted") {
      reasons.push("RESUME_WITHOUT_EVIDENCE");
    }
  }
  return reasons;
}

// 第 0 步：凡声明了来源的样例，其五个必填字段须与 constraints.geojson 中的同名点位逐字一致。
// Step 0: any fixture naming a source of record must match the five required fields
// of the same node in constraints.geojson, verbatim.
function checkSourceAlignment(fixture, schema, nodeSource) {
  const record = fixture.source_of_record;
  if (!record || !nodeSource) return { reasons: [], line: null };
  const feature = nodeSource.features.find((item) => item.properties.id === record.feature_id);
  if (!feature) return { reasons: [`SOURCE_MISMATCH:${record.feature_id}`], line: null };
  const reasons = [];
  for (const field of schema.required_fields) {
    if (feature.properties[field.field] !== fixture.node[field.field]) {
      reasons.push(`SOURCE_MISMATCH:${field.field}`);
    }
  }
  const line = reasons.length === 0
    ? `    ${fixture.fixture_id} ← ${record.file}#${record.feature_id} : `
      + `${schema.required_fields.length} 个必填字段逐字一致 / ${schema.required_fields.length} required fields match verbatim`
    : `    ${fixture.fixture_id} ← ${record.file}#${record.feature_id} : 不一致 / mismatch`;
  return { reasons, line };
}

function evaluate(fixture, parts, nodeSource) {
  const alignment = checkSourceAlignment(fixture, parts.schema, nodeSource);
  const reasons = [
    ...alignment.reasons,
    ...checkNodeSchema(fixture.node, parts.schema),
    ...checkDenominator(fixture.measurement_declaration, parts.scoring),
    ...checkLevel(fixture.level_claim, parts.levels, fixture.node),
    ...checkDecision(fixture.decision, parts.rules),
  ];
  const unique = [...new Set(reasons)];
  return {
    verdict: unique.length === 0 ? "accept" : "reject",
    reasons: unique,
    alignmentLine: alignment.line,
  };
}

function main() {
  const spec = readJson(SPEC_PATH);
  const fixtureFile = readJson(FIXTURES_PATH);
  const parts = {
    schema: component(spec, "node_schema"),
    scoring: component(spec, "scoring_definitions"),
    levels: component(spec, "level_definitions"),
    rules: component(spec, "decision_rules"),
  };

  let nodeSource = null;
  try {
    nodeSource = readJson(NODE_SOURCE_PATH);
  } catch (error) {
    nodeSource = null;
  }

  const out = [];
  out.push("SEB 桌面配对推演 / SEB tabletop pairing run");
  out.push(`基准 / Baseline : ${spec.spec_id} v${spec.version} (${spec.status})`);
  out.push(`样例 / Fixtures : ${fixtureFile.fixtures_id} v${fixtureFile.version} · ${fixtureFile.fixtures.length} 条 / items`);
  out.push("性质 / Nature   : 方法学演示，无真实参与者，不产生任何绩效指标数值");
  out.push("                  methodology demonstration, no real participant, no performance metric value");
  out.push("");
  out.push("[0] 节点数据对齐 / Node-data alignment");

  const results = [];
  const alignmentLines = [];
  for (const fixture of fixtureFile.fixtures) {
    const result = evaluate(fixture, parts, nodeSource);
    results.push({ fixture, result });
    if (result.alignmentLine) alignmentLines.push(result.alignmentLine);
  }
  if (alignmentLines.length === 0) {
    out.push("    未找到可对齐的来源声明 / no source-of-record declaration found");
  } else {
    alignmentLines.forEach((line) => out.push(line));
  }
  out.push("");

  let index = 0;
  let matched = 0;
  for (const { fixture, result } of results) {
    index += 1;
    const agree = result.verdict === fixture.expected_verdict
      && JSON.stringify([...result.reasons].sort()) === JSON.stringify([...(fixture.expected_reasons || [])].sort());
    if (agree) matched += 1;
    out.push(`[${index}] ${fixture.fixture_id}  ${fixture.title_zh} / ${fixture.title_en}`);
    out.push(`    判定 / verdict : ${result.verdict.toUpperCase()}   期望 / expected : ${fixture.expected_verdict.toUpperCase()}   ${agree ? "一致 / match" : "不一致 / MISMATCH"}`);
    for (const code of result.reasons) {
      const [zh, en] = explain(code);
      out.push(`    理由 / reason  : ${code}`);
      out.push(`                     ${zh} / ${en}`);
    }
    if (!agree) {
      out.push(`    期望理由 / expected reasons : ${(fixture.expected_reasons || []).join(", ") || "(none)"}`);
    }
    out.push("");
  }

  const accepted = results.filter((item) => item.result.verdict === "accept").length;
  out.push("汇总 / Summary");
  out.push(`    通过 / accepted : ${accepted}`);
  out.push(`    拒绝 / rejected : ${results.length - accepted}`);
  out.push(`    与期望一致 / matching expectation : ${matched} / ${results.length}`);
  out.push("    本次运行不写入 metrics.json，七项包容性指标保持 unknown");
  out.push("    this run writes nothing to metrics.json; the seven inclusion metrics stay unknown");

  process.stdout.write(out.join("\n") + "\n");
  return matched === results.length ? 0 : 1;
}

process.exitCode = main();
