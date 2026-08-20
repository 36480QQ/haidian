#!/usr/bin/env node
/*
 * 京张交接线 · 协议自检重跑器（离线、只读）
 *
 * 用途：把本包两个招牌数字——96 条规则检查与 48 项接管断言——从原始夹具当场重算一遍，
 * 并与随包发布的结果逐条比对。包内其余数值（面积、长度、比率、断面合计、更新单元落点）
 * 都能由 geojson 与 metrics.json 直接复算；这两个数此前是唯一的例外，本文件补上。
 *
 * 用法：
 *   node protocol-check-runner.js            # 人读摘要，全部一致时退出码 0
 *   node protocol-check-runner.js --json     # 机器可读结果
 *
 * 只读三个随包文件，不写任何东西，不联网，不依赖任何第三方包：
 *   shift-ledger-suite.json   输入夹具：12 条合成交接账
 *   rule-check-report.json    随包发布的 96 条规则检查结果
 *   ../../../simulation.json  随包发布的 12 任务 / 48 断言结果
 *
 * 规则谓词与缺陷注入按 rule-check-report.json 的 rules[].statement_zh 独立实现，
 * 不是原生成脚本的搬运；因此本文件与那两份结果一致，构成一次独立复现。
 *
 * 它不证明现场绩效、安全、合规或获批：现场演练仍为 0/12。
 */
"use strict";
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const read = (p) => JSON.parse(fs.readFileSync(path.join(HERE, p), "utf8"));

const suite = read("shift-ledger-suite.json");
const report = read("rule-check-report.json");
const sim = read("../../../simulation.json");

const RULES = [
  "R1_DUAL_CONTROL_SEPARATION",
  "R2_HUMAN_FLOOR_FIRST",
  "R3_BLOCKING_ITEM_HOLDS_SMART_LAYER_OFF",
  "R4_NO_TRIAL_WITHOUT_OBSERVED_ROLLBACK",
  "R5_SYNTHETIC_MUST_NOT_TOUCH_LIVE",
  "R6_REFUSAL_NEEDS_REASONS",
  "R7_NO_ATTESTATION_WITHOUT_APPOINTMENT",
];
// 「智能层关闭时该渠道仍可用」的两种合法取值
const FLOOR_OFF_OK = [
  "available_while_smart_layer_is_off",
  "available_before_during_and_after_smart_layer",
];
const ATTESTED = ["attested", "co_signed", "signed"];

const hasBlockingOpen = (L) =>
  (L.unresolved_register || []).some((i) => i.blocking === true && i.state === "open");

/* 七条规则的谓词。返回被违反的规则，按 R1…R7 次序。 */
function violations(L) {
  const v = [];
  const cp = L.control_pair, ta = L.transfer_attempt;
  const hf = L.human_service_floor, oe = L.operating_envelope, rb = L.rollback_rehearsal;

  // R1 交出与接入必须由不同角色判断，同一人不得两侧签字
  if (cp.same_person_permitted !== false ||
      cp.release_role.role_code === cp.receive_role.role_code) v.push(RULES[0]);

  // R2 人工等价服务须先于智能层存在，且至少一条渠道在智能层关闭时仍可用
  if (hf.must_exist_before_smart_layer !== true ||
      !(hf.channels || []).some((c) => FLOOR_OFF_OK.includes(c.continuity_rule))) v.push(RULES[1]);

  // R3 存在未闭合的阻塞性未决项时，智能层必须保持关闭
  if (hasBlockingOpen(L) && ta.smart_layer_state_after_decision !== "off") v.push(RULES[2]);

  // R4 回滚演练未被观察到通过前，不得进入限定试用
  if (rb.pass !== true && ta.smart_layer_state_after_decision === "limited_trial") v.push(RULES[3]);

  // R5 合成记录不得触碰真实服务，也不得含个人数据
  if (oe.record_origin === "synthetic" &&
      (oe.touches_live_service !== false || oe.contains_personal_data !== false)) v.push(RULES[4]);

  // R6 拒收必须给出可复核的理由
  if (ta.receiver_disposition === "refused" &&
      !(ta.refusal_reasons || []).length) v.push(RULES[5]);

  // R7 角色未指派时，双联状态不得标记为已共同签认
  const roles = ["release_role", "receive_role"];
  const unassigned = roles.filter((k) => cp[k].assignment_state === "unassigned_concept_role");
  if (unassigned.some((k) => ATTESTED.includes(cp[k].attestation_state)) ||
      (unassigned.length && ATTESTED.includes(cp.pair_state))) v.push(RULES[6]);

  return v;
}

/* 七类缺陷注入：每类只动一处字段，使对应规则必然被触发。
   注意 R4 的注入同时会触发 R3——阻塞项仍开着而智能层被推到限定试用，
   这与随包结果里那 12 条 violations 为两元素的记录一致。 */
function inject(L, rule) {
  const x = JSON.parse(JSON.stringify(L));
  const cp = x.control_pair, ta = x.transfer_attempt;
  switch (rule) {
    case RULES[0]: cp.receive_role.role_code = cp.release_role.role_code; break;
    case RULES[1]: x.human_service_floor.must_exist_before_smart_layer = false; break;
    case RULES[2]: ta.smart_layer_state_after_decision = "sandbox_preview"; break;
    case RULES[3]: ta.smart_layer_state_after_decision = "limited_trial"; break;
    case RULES[4]: x.operating_envelope.touches_live_service = true; break;
    case RULES[5]: ta.refusal_reasons = []; break;
    case RULES[6]: cp.release_role.attestation_state = "attested"; cp.pair_state = "attested"; break;
  }
  return x;
}

/* 四项接管断言，逐条由夹具字段判定。 */
const ASSERTS = ["smart_layer_off_baseline", "human_takeover_route",
                 "synthetic_record_disposal", "rollback_to_human_service"];
function assertions(L) {
  const ta = L.transfer_attempt, hf = L.human_service_floor;
  const oe = L.operating_envelope, rb = L.rollback_rehearsal;
  const d = oe.synthetic_record_disposal || {};
  const floorMethods = (hf.channels || []).map((c) => c.method_zh);
  return {
    smart_layer_off_baseline: ta.smart_layer_state_after_decision === "off" ? "pass" : "fail",
    human_takeover_route:
      hf.must_exist_before_smart_layer === true && hf.device_free_access === true &&
      (hf.channels || []).some((c) => FLOOR_OFF_OK.includes(c.continuity_rule)) ? "pass" : "fail",
    synthetic_record_disposal:
      oe.record_origin === "synthetic" && !!d.trigger && !!d.verification_method &&
      (d.retained_material || []).length > 0 ? "pass" : "fail",
    rollback_to_human_service:
      floorMethods.includes(rb.target_state_zh) &&
      (rb.expected_sequence || []).length >= 1 ? "pass" : "fail",
  };
}

/* ---------------- 重算并比对 ---------------- */
const recomputed = new Map();
for (const L of suite.ledgers) {
  const sid = L.scenario_anchor.scenario_id;
  recomputed.set(`${sid}::baseline`, violations(L));
  for (const r of RULES) recomputed.set(`${sid}::${r}`, violations(inject(L, r)));
}

const ruleMismatches = [];
for (const c of report.checks) {
  const got = recomputed.get(c.check_id);
  const same = got && JSON.stringify(got) === JSON.stringify(c.violations);
  const resultOk = c.variant === "baseline"
    ? (got || []).length === 0
    : (got || []).includes(c.injected_defect);
  if (!same || (c.result === "pass") !== resultOk) {
    ruleMismatches.push({ check_id: c.check_id, published: c.violations, recomputed: got });
  }
}

const byScenario = new Map(suite.ledgers.map((L) => [L.scenario_anchor.scenario_id, L]));
let assertRun = 0;
const assertMismatches = [];
for (const t of sim.tasks) {
  const a = assertions(byScenario.get(t.scenario_id));
  for (const [k, published] of Object.entries(t.checks)) {
    assertRun += 1;
    if (a[k] !== published) {
      assertMismatches.push({ scenario_id: t.scenario_id, check: k, published, recomputed: a[k] });
    }
  }
}

const out = {
  runner: "protocol-check-runner.js",
  reads_only: ["shift-ledger-suite.json", "rule-check-report.json", "simulation.json"],
  ledgers: suite.ledgers.length,
  rule_checks_recomputed: report.checks.length,
  rule_checks_matching_published: report.checks.length - ruleMismatches.length,
  assertions_recomputed: assertRun,
  assertions_matching_published: assertRun - assertMismatches.length,
  rule_mismatches: ruleMismatches,
  assertion_mismatches: assertMismatches,
  all_match: ruleMismatches.length === 0 && assertMismatches.length === 0,
  field_rehearsal_tasks_completed: sim.summary.field_rehearsal_tasks_completed,
  scope_note_zh: "只重算协议逻辑，不证明现场绩效、安全、合规或获批；现场演练仍为 0/12。",
};

if (process.argv.includes("--json")) {
  console.log(JSON.stringify(out, null, 2));
} else {
  console.log(`交接账 ${out.ledgers} 条`);
  console.log(`规则检查 ${out.rule_checks_matching_published}/${out.rule_checks_recomputed} 与随包结果一致`);
  console.log(`接管断言 ${out.assertions_matching_published}/${out.assertions_recomputed} 与随包结果一致`);
  console.log(`现场演练 ${out.field_rehearsal_tasks_completed}/12（未授权，未执行）`);
  for (const m of out.rule_mismatches) console.log("  规则不一致:", JSON.stringify(m));
  for (const m of out.assertion_mismatches) console.log("  断言不一致:", JSON.stringify(m));
  console.log(out.all_match ? "全部一致" : "存在不一致");
}
process.exit(out.all_match ? 0 : 1);
