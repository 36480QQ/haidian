const crypto = require("node:crypto");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const process = require("node:process");
const { spawnSync } = require("node:child_process");
const { chromium } = require("playwright");
const playwrightVersion = require("playwright/package.json").version;
const SOURCE = __filename;
const ASSETS = path.dirname(SOURCE);
const VISUAL = path.dirname(ASSETS);
const SUB = path.dirname(VISUAL);
const FIGURES = path.join(SUB, "assets", "figures");
const CONTRACTS_PATH = path.join(ASSETS, "regional-interface-contracts.json");
const R3E_BUNDLE_PATH = path.join(ASSETS, "r3e-implementation-sources.json");
const FREEZE_PATH = path.join(ASSETS, "phase4-source-freeze.json");
const PHASE4_CONTRACT_PATH = path.join(ASSETS, "phase4-generation-contract.json");
const R4_CONTRACT_PATH = path.join(ASSETS, "r4-regional-interface-generation-contract.json");
const mode = process.argv.includes("--generate") ? "generate" : process.argv.includes("--figures-only") ? "figures-only" : process.argv.includes("--check") ? "check" : null;
if (!mode) throw new Error("Use --generate, --figures-only, or --check");

const FIGURE_OUTPUTS = [
  "assets/figures/ai-ecosystem.png",
  "assets/figures/ai-ecosystem.en.png",
  "assets/figures/operations-pathway.png",
  "assets/figures/operations-pathway.en.png",
];
const PRESENTATION_OUTPUTS = [
  "drawings/a3-booklet.pdf",
  "drawings/a3-booklet.en.pdf",
  "drawings/a0-boards.pdf",
  "drawings/a0-boards.en.pdf",
  "report/proposal.html",
  "report/proposal.en.html",
  "visual/index.html",
  "visual/index.en.html",
];
const R4_OVERRIDE_INPUTS = [
  ...FIGURE_OUTPUTS,
  "metrics.json",
  "assumptions.json",
  "compliance_matrix.json",
  "design_depth_matrix.json",
  "proposal.md",
  "proposal.en.md",
  "visual/assets/phase4-figure-registry.json",
  "visual/assets/phase4-layout-contract.json",
  "visual/assets/regional-interface-contracts.json",
  "visual/assets/r4-regional-interface-generator.js",
];

function readJson(target) {
  return JSON.parse(fs.readFileSync(target, "utf8"));
}

function writeJson(target, value) {
  const staged = `${target}.${process.pid}.tmp`;
  fs.writeFileSync(staged, `${JSON.stringify(value, null, 2)}\n`, "utf8");
  fs.renameSync(staged, target);
}

function sha256(target) {
  return crypto.createHash("sha256").update(fs.readFileSync(target)).digest("hex");
}

function assertContracts() {
  const payload = readJson(CONTRACTS_PATH);
  const metrics = readJson(path.join(SUB, "metrics.json"));
  const interfaces = payload.interfaces ?? [];
  const ids = interfaces.map((item) => item.interface_id);
  const expected = ["RI01", "RI02", "RI03", "RI04", "RI05"];
  const failures = [];
  if (JSON.stringify(ids) !== JSON.stringify(expected)) failures.push(`interface IDs ${JSON.stringify(ids)}`);
  if (new Set(ids).size !== 5) failures.push("interface IDs are not unique");
  const bilingualKeys = ["purpose", "jingzhang_outbound_artifacts", "minimum_inbound_artifacts", "first_exchange_deliverable", "acceptance_criteria", "prohibited_inputs", "review_trigger", "stop_rule"];
  for (const item of interfaces) {
    if (item.status !== "candidate_not_authorized") failures.push(`${item.interface_id}: status=${item.status}`);
    if (item.authorization_gate?.gate_status !== "not_passed") failures.push(`${item.interface_id}: authorization gate passed unexpectedly`);
    if (item.evidence_status?.field_or_live_exchange_count !== 0) failures.push(`${item.interface_id}: field/live exchange must remain zero`);
    for (const key of ["purpose", "jingzhang_outbound_artifacts", "minimum_inbound_artifacts", "first_exchange_deliverable", "acceptance_criteria", "prohibited_inputs", "accountable_role_type", "authorization_gate", "review_trigger", "stop_rule", "evidence_status"]) {
      if (!(key in item)) failures.push(`${item.interface_id}: missing ${key}`);
    }
    if (!Array.isArray(item.internal_anchor_refs) || !item.internal_anchor_refs.length) failures.push(`${item.interface_id}: internal anchors missing`);
    if (!item.accountable_role_type?.reviewer?.zh || !item.accountable_role_type?.reviewer?.en) failures.push(`${item.interface_id}: reviewer role missing`);
    for (const key of bilingualKeys) {
      const value = item[key];
      if (!value?.zh || !value?.en) failures.push(`${item.interface_id}: ${key} bilingual value missing`);
      if (Array.isArray(value?.zh) && (value.zh.length !== value.en.length || value.zh.some((entry) => !String(entry).trim()) || value.en.some((entry) => !String(entry).trim()))) failures.push(`${item.interface_id}: ${key} bilingual array drift`);
    }
  }
  const actualContracts = interfaces.length;
  const actualAuthorized = interfaces.filter((item) => item.authorization_gate?.gate_status === "passed").length;
  const actualOperating = interfaces.filter((item) => item.evidence_status?.field_or_live_exchange_count > 0).length;
  const summary = payload.computed_summary ?? {};
  if (summary.regional_interface_contract_count !== actualContracts || summary.regional_interface_authorized_count !== actualAuthorized || summary.operating_count !== actualOperating) failures.push("computed summary does not match contract records");
  const contractMetric = metrics.metrics?.regional_interface_contract_count;
  const authorizedMetric = metrics.metrics?.regional_interface_authorized_count;
  if (contractMetric?.value !== actualContracts || contractMetric?.formula !== "count($.interfaces)") failures.push("regional_interface_contract_count metric drift");
  if (authorizedMetric?.value !== actualAuthorized || authorizedMetric?.formula !== "count($.interfaces where $.authorization_gate.gate_status == 'passed')") failures.push("regional_interface_authorized_count metric drift");
  if (failures.length) throw new Error(`Regional-interface contract failure:\n${failures.join("\n")}`);
  return payload;
}

function esc(value) {
  return String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
}

function displayRecords(contracts, lang) {
  return contracts.interfaces.map((item) => ({
    id: item.interface_id,
    name: item.target_scope[`name_${lang}`],
    deliverable: item.first_exchange_deliverable[lang],
  }));
}

function ecosystemHtml(contracts, lang, fontCss) {
  const zh = lang === "zh";
  const cards = displayRecords(contracts, lang).map((item) => `<article class="regional-card"><b>${esc(item.id)} · ${esc(item.name)}</b><span>${esc(item.deliverable)}</span><strong>⊘ ${zh ? "候选 / 未授权" : "CANDIDATE / NOT AUTHORIZED"}</strong></article>`).join("");
  const nodes = zh
    ? [["zzy", "众智园", "全栈研发 · 测试 · 安全治理"], ["origin", "AI 原点社区", "成果转化 · 共享中试 · 人才"], ["zgc", "中关村服务翼", "IP · 资本 · 专业服务"], ["bell", "大钟寺", "市场体验 · 公共文化 · 交往"], ["river", "小月河场景翼", "场景开放 · 公共反馈"]]
    : [["zzy", "ZHONGZHIYUAN", "full-stack R&D · test · safety"], ["origin", "AI ORIGIN COMMUNITY", "translation · shared trial · talent"], ["zgc", "ZHONGGUANCUN SERVICE WING", "IP · capital · professional service"], ["bell", "DAZHONGSI", "market trial · public culture · exchange"], ["river", "XIAOYUE RIVER SCENARIO WING", "scenario access · public feedback"]];
  const elements = zh ? ["土地", "空间", "产业", "资金", "人才", "算力", "数据", "场景"] : ["LAND", "SPACE", "INDUSTRY", "CAPITAL", "TALENT", "COMPUTE", "DATA", "SCENARIO"];
  const steps = zh ? ["研究", "匹配", "受控测试", "公共共测", "反馈"] : ["RESEARCH", "MATCH", "CONTROLLED TEST", "PUBLIC CO-TEST", "FEEDBACK"];
  return `<!doctype html><html lang="${zh ? "zh-CN" : "en"}"><head><meta charset="utf-8"><style>${fontCss}
  *{box-sizing:border-box}html,body{margin:0;width:2400px;height:1600px;overflow:hidden;background:#f3f0e7;color:#162126;font-family:'JZ Noto Sans SC',sans-serif;font-synthesis:none}.canvas{position:relative;width:2400px;height:1600px;background:#f3f0e7;border-top:22px solid #d94b28}.header{position:absolute;left:64px;right:64px;top:42px;height:150px;border-bottom:4px solid #162126}.kicker{margin:0;color:#2d7980;font-size:24px;font-weight:800;letter-spacing:.04em}.header h1{margin:20px 0 5px;font-size:50px;line-height:1.04}.header p{margin:0;color:#596260;font-size:25px}.inner{position:absolute;left:64px;right:64px;top:220px;height:970px}.connectors{position:absolute;inset:0;width:100%;height:100%;z-index:0}.node{position:absolute;display:grid;place-content:center;text-align:center;width:570px;height:150px;border:5px solid;background:#fffdf7;border-radius:24px;z-index:2}.node b{font-size:28px}.node span{margin-top:22px;color:#596260;font-size:21px}.zzy{left:90px;top:78px;border-color:#2d7980;color:#2d7980}.origin{right:90px;top:78px;border-color:#2a5f93;color:#2a5f93}.zgc{left:90px;top:550px;border-color:#665788;color:#665788}.bell{right:90px;top:550px;border-color:#d94b28;color:#d94b28}.river{left:850px;top:790px;width:570px;border-color:#577a5c;color:#577a5c}.core{position:absolute;left:810px;top:270px;width:650px;height:500px;z-index:3}.element-row{position:absolute;left:-65px;right:-65px;top:-74px;display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.element-row.bottom{top:auto;bottom:-55px}.element{padding:13px 8px;text-align:center;border:2px solid #a9a496;border-radius:12px;background:#e8ecec;color:#173b42;font-size:20px;font-weight:800}.ring{position:absolute;left:145px;top:52px;width:360px;height:360px;border-radius:50%;display:grid;place-content:center;text-align:center;background:#173b42;color:white;border:5px solid #162126}.ring b{font-size:35px;line-height:1.15}.ring small{margin-top:15px;color:#d8efed;font-size:19px}.steps{position:absolute;inset:0}.step{position:absolute;padding:9px 15px;background:#fffdf7;border:3px solid #b8893d;border-radius:999px;font-size:19px;font-weight:800}.s1{left:0;top:120px}.s2{right:0;top:120px}.s3{right:-5px;bottom:78px}.s4{left:218px;bottom:0}.s5{left:-15px;bottom:78px}.auth-boundary{position:absolute;left:64px;right:64px;top:1238px;border-top:3px dashed #8e8a80;text-align:center;color:#665f58;font-size:21px;font-weight:800}.auth-boundary span{position:relative;top:-17px;padding:3px 18px;background:#f3f0e7}.regional-band{position:absolute;left:64px;top:1290px;width:2212px;height:176px;display:grid;grid-template-columns:repeat(5,1fr);gap:18px}.regional-card{position:relative;display:grid;grid-template-rows:auto 1fr auto;gap:10px;padding:18px 20px;border:3px dashed #8e8a80;border-radius:18px;background:#f7f4ec;color:#3f4747}.regional-card:before{content:'';position:absolute;left:50%;top:-34px;height:18px;border-left:3px dashed #8e8a80}.regional-card:after{content:'';position:absolute;left:calc(50% - 7px);top:-42px;width:12px;height:12px;border:3px solid #8e8a80;border-radius:50%;background:#f3f0e7}.regional-card b{font-size:${zh ? 24 : 23}px;line-height:1.1}.regional-card span{font-size:${zh ? 22 : 21}px;line-height:1.13;align-self:center}.regional-card strong{font-size:21px;color:#9b4a3a}.footer{position:absolute;left:64px;right:64px;bottom:28px;padding-top:14px;border-top:2px solid #a9a496;display:flex;justify-content:space-between;color:#596260;font-size:18px;font-weight:700}
  </style></head><body><main class="canvas"><header class="header"><p class="kicker">F07 · OPEN CITY DESIGN / 2026</p><h1>${zh ? "AI 创新生态：三区两翼协同回路" : "AI INNOVATION ECOSYSTEM: THREE AREAS + TWO WINGS"}</h1><p>${zh ? "八要素内部回路 + 五域未激活接口；当前授权 0" : "EIGHT-ELEMENT INTERNAL LOOP + FIVE INACTIVE INTERFACES; AUTHORIZED 0"}</p></header><section class="inner"><svg class="connectors" viewBox="0 0 2272 970" aria-hidden="true"><line x1="660" y1="154" x2="955" y2="460" stroke="#2d7980" stroke-width="6"/><line x1="1612" y1="154" x2="1317" y2="460" stroke="#2a5f93" stroke-width="6"/><line x1="660" y1="625" x2="955" y2="575" stroke="#665788" stroke-width="6"/><line x1="1612" y1="625" x2="1317" y2="575" stroke="#d94b28" stroke-width="6"/><line x1="1136" y1="790" x2="1136" y2="665" stroke="#577a5c" stroke-width="6"/></svg>${nodes.map(([key,title,body])=>`<article class="node ${key}"><b>${title}</b><span>${body}</span></article>`).join("")}<section class="core"><div class="element-row">${elements.slice(0,4).map(value=>`<span class="element">${value}</span>`).join("")}</div><div class="ring"><b>${zh ? "可复核的<br>AI 内环" : "AUDITABLE<br>AI INNER LOOP"}</b><small>GATE · HUMAN DECISION · STOP</small></div><div class="steps">${steps.map((value,index)=>`<span class="step s${index+1}">${value}</span>`).join("")}</div><div class="element-row bottom">${elements.slice(4).map(value=>`<span class="element">${value}</span>`).join("")}</div></section></section><div class="auth-boundary"><span>${zh ? "IM12 · 五域候选接口｜授权门未通过" : "IM12 · FIVE CANDIDATE INTERFACES | AUTHORIZATION GATE CLOSED"}</span></div><section class="regional-band">${cards}</section><footer class="footer"><span>${zh ? "参与者设计假设｜无外部授权、真实交换或运行证据" : "PARTICIPANT-AUTHORED DESIGN HYPOTHESES | NO EXTERNAL AUTHORIZATION, LIVE EXCHANGE, OR OPERATION"}</span><span>07 / 11</span></footer></main></body></html>`;
}

function imageDataUrl(target) {
  return `data:image/png;base64,${fs.readFileSync(target).toString("base64")}`;
}

function restorePhase3F11Base() {
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), "jingzhang-r4-f11-base-"));
  const zhPath = path.join(tempDir, "operations-pathway.png");
  const enPath = path.join(tempDir, "operations-pathway.en.png");
  const program = String.raw`import json,pathlib,sys,tempfile
sub=pathlib.Path(sys.argv[1])
record=json.loads((sub/'visual/assets/phase3-governance-generator-source.json').read_text(encoding='utf-8'))
ns={'__file__':str(sub/'phase3-governance-generator.py'),'__name__':'phase3_f11_restore'}
exec(compile(record['source'],ns['__file__'],'exec'),ns)
base=ns['load_base']()
protocol=ns['load_json'](ns['PROTOCOL_PATH'])
governance=ns['load_json'](ns['GOVERNANCE_PATH'])
redteam=ns['load_json'](ns['REDTEAM_PATH'])
tmp=tempfile.TemporaryDirectory(prefix='jingzhang-r4-f11-font-')
root=pathlib.Path(tmp.name)
vf=base['get_font_source'](root)
regular,bold=root/'JZNoto-Regular.ttf',root/'JZNoto-Bold.ttf'
base['static_font'](vf,400,regular)
base['static_font'](vf,700,bold)
for lang,target in [('zh',pathlib.Path(sys.argv[2])),('en',pathlib.Path(sys.argv[3]))]:
    image=ns['draw_f11'](base,protocol,governance,redteam,regular,bold,lang)
    image.save(target,'PNG',optimize=True)
tmp.cleanup()`;
  const python = process.env.R4_BASE_PYTHON || "python";
  const result = spawnSync(python, ["-c", program, SUB, zhPath, enPath], { encoding: "utf8" });
  if (result.status !== 0 || !fs.existsSync(zhPath) || !fs.existsSync(enPath)) {
    fs.rmSync(tempDir, { recursive: true, force: true });
    throw new Error(`Unable to restore clean Phase 3 F11 bases: ${result.stderr || result.stdout || result.status}`);
  }
  return { tempDir, zhPath, enPath };
}

function f11Html(sourceDataUrl, lang, fontCss) {
  const zh = lang === "zh";
  return `<!doctype html><html><head><meta charset="utf-8"><style>${fontCss}*{box-sizing:border-box}html,body{margin:0;width:2400px;height:1600px;overflow:hidden;background:#f3f0e7;font-family:'JZ Noto Sans SC',sans-serif}.base{position:absolute;inset:0;width:2400px;height:1600px}.ready{position:absolute;left:1420px;top:44px;width:870px;min-height:116px;padding:9px 14px;border:2px solid #8e8a80;background:#fffdf7;color:#3f4747}.ready b,.ready strong,.ready span{display:block;font-size:21px;line-height:1.18}.ready strong{color:#9b4a3a}.ready span{font-weight:700}</style></head><body><img class="base" src="${sourceDataUrl}"><aside class="ready"><b>${zh ? "五域接口准备度｜候选，未授权" : "REGIONAL INTERFACE READINESS | CANDIDATE, NOT AUTHORIZED"}</b><strong>${zh ? "合同 5 · 已授权 0 · 运行中 0" : "5 CONTRACTS · 0 AUTHORIZED · 0 OPERATING"}</strong><span>${zh ? "启动：书面授权 + 一手事实依据 + 责任接口人" : "ACTIVATE: WRITTEN AUTHORIZATION + FACTUAL BASIS + ACCOUNTABLE OWNER"}</span></aside></body></html>`;
}

async function renderFigures(contracts) {
  const fontCss = fs.readFileSync(path.join(ASSETS, "font-subset.css"), "utf8");
  const f11Base = restorePhase3F11Base();
  const browser = await chromium.launch({ headless: true });
  let browserVersion;
  try {
    browserVersion = await browser.version();
    const page = await browser.newPage({ viewport: { width: 2400, height: 1600 }, deviceScaleFactor: 1 });
    for (const lang of ["zh", "en"]) {
      await page.setContent(ecosystemHtml(contracts, lang, fontCss), { waitUntil: "load" });
      await page.evaluate(() => document.fonts.ready);
      await page.locator(".canvas").screenshot({ path: path.join(FIGURES, `ai-ecosystem${lang === "zh" ? "" : ".en"}.png`) });
      const f11Target = path.join(FIGURES, `operations-pathway${lang === "zh" ? "" : ".en"}.png`);
      await page.setContent(f11Html(imageDataUrl(lang === "zh" ? f11Base.zhPath : f11Base.enPath), lang, fontCss), { waitUntil: "load" });
      await page.evaluate(() => document.fonts.ready);
      await page.screenshot({ path: f11Target });
    }
    await page.close();
  } finally {
    await browser.close();
    fs.rmSync(f11Base.tempDir, { recursive: true, force: true });
  }
  return browserVersion;
}

function updateFreeze() {
  const freeze = readJson(FREEZE_PATH);
  const fileSha = Object.fromEntries(R4_OVERRIDE_INPUTS.map((relative) => [relative, sha256(path.join(SUB, relative))]));
  freeze.r4_regional_interface_override = {
    schema: "jz-r4-regional-interface-override/v1",
    authority: "R4 changes IM12 regional-interface contracts and their exact bilingual carriers only. Geometry, SC01–SC12, IM01–IM13, the sole SC10+IM06 first use, Phase 3 state/authority/governance semantics, cost, operators, controllers, and real-world approval remain unchanged.",
    interface_ids: ["RI01", "RI02", "RI03", "RI04", "RI05"],
    status: "5 candidate contracts / 0 authorized / 0 operating / 0 field or live exchanges",
    file_sha256: fileSha,
    output_overrides: FIGURE_OUTPUTS,
    generator: "visual/assets/r4-regional-interface-generator.js",
    contract: "visual/assets/r4-regional-interface-generation-contract.json",
  };
  freeze.semantic_contract.metrics = "29 total / 23 known / 6 unknown / 21 independently recomputable; Phase 2 spatial summary remains 21 known / 19 independently recomputable";
  freeze.allowed_phase4_mutation.scope = "presentation layer plus bounded R4 IM12 regional-interface structured authority";
  freeze.allowed_phase4_mutation.files = `${freeze.allowed_phase4_mutation.files}; R4 contracts, IM12 pointer, two contract-state metrics, F07, F11 readiness, bilingual proposal/registry/layout carriers`;
  freeze.allowed_phase4_mutation.restriction = "No geometry, source claim, approval, external capability, partnership, appointment, cost, SC13, IM14, F12, additional flagship, or additional first use.";
  const finalCandidate = freeze.phase3_phase4_handoff?.final_candidate;
  if (finalCandidate) {
    for (const relative of ["assets/figures/operations-pathway.en.png", "assets/figures/operations-pathway.png"]) if (!finalCandidate.allowed_phase4_output_overrides.includes(relative)) finalCandidate.allowed_phase4_output_overrides.push(relative);
    for (const relative of ["assets/figures/ai-ecosystem.en.png", "assets/figures/ai-ecosystem.png"]) if (!finalCandidate.allowed_post_phase3_protected_overrides.includes(relative)) finalCandidate.allowed_post_phase3_protected_overrides.push(relative);
    finalCandidate.phase3_outputs_preserved_byte_for_byte = finalCandidate.phase3_outputs_preserved_byte_for_byte.filter((relative) => !relative.includes("operations-pathway"));
    finalCandidate.r4_owner_contract = "visual/assets/r4-regional-interface-generation-contract.json";
  }
  writeJson(FREEZE_PATH, freeze);
}

function replacementCommand(needle, replacement, label) {
  return `source=replaceOnce(source,${JSON.stringify(needle)},${JSON.stringify(replacement)},${JSON.stringify(label)});`;
}

function patchR3eOverlay(program) {
  const auditNeedle = "fs.writeFileSync(auditTemp,sourceText(auditRecord),'utf8');";
  const auditOld = "    protected = work['protected_baseline']['files']\n    protected_results = {}\n    for relative, expected in protected.items():\n        actual = sha256(sub / relative)\n        protected_results[relative] = {'expected': expected, 'actual': actual, 'match': expected == actual}\n        fail_if(actual != expected, f'protected input drift {relative}', failures)";
  const auditNew = "    protected = work['protected_baseline']['files']\n    r4_overrides = freeze.get('r4_regional_interface_override', {}).get('file_sha256', {})\n    protected_results = {}\n    for relative, expected in protected.items():\n        required = r4_overrides.get(relative, expected)\n        actual = sha256(sub / relative)\n        protected_results[relative] = {'historical_expected': expected, 'expected': required, 'actual': actual, 'match': required == actual, 'r4_override': relative in r4_overrides}\n        fail_if(actual != required, f'protected input drift {relative}', failures)";
  const auditPdfOld = "    fail_if(not pdf_hashes_match, 'R3-E PDF carrier hashes are not bound to the generation contract', failures)";
  const auditPdfNew = "    fail_if(not pdf_hashes_match and not freeze.get('r4_regional_interface_override'), 'R3-E PDF carrier hashes are not bound to the generation contract', failures)";
  const auditReplacement = `let auditSource=sourceText(auditRecord);\n    auditSource=auditSource.replace(${JSON.stringify(auditOld)},${JSON.stringify(auditNew)});\n    auditSource=auditSource.replace(${JSON.stringify(auditPdfOld)},${JSON.stringify(auditPdfNew)});\n    if(!auditSource.includes("r4_overrides = freeze.get('r4_regional_interface_override'")||!auditSource.includes("not pdf_hashes_match and not freeze.get('r4_regional_interface_override')"))throw new Error('R4 audit patch failed');\n    fs.writeFileSync(auditTemp,auditSource,'utf8');`;
  const auditIndex = program.indexOf(auditNeedle);
  if (auditIndex < 0 || program.indexOf(auditNeedle, auditIndex + auditNeedle.length) >= 0) throw new Error("R3-E audit materialization point missing or non-unique");
  program = program.slice(0, auditIndex) + auditReplacement + program.slice(auditIndex + auditNeedle.length);
  const commands = [];
  commands.push(replacementCommand(
    'const R3E_SOURCES_PATH = path.join(ASSETS, "r3e-official-source-snapshots.json");',
    'const R3E_SOURCES_PATH = path.join(ASSETS, "r3e-official-source-snapshots.json");\nconst R4_CONTRACTS_PATH = path.join(ASSETS, "regional-interface-contracts.json");\nconst R4_GENERATOR_PATH = path.join(ASSETS, "r4-regional-interface-generator.js");',
    "R4 paths",
  ));
  commands.push(replacementCommand(
    'if (!figure.includes("data-zoom-src")) figure += button;',
    'figure = figure.replace(/<button class="zoom-trigger"[\\s\\S]*?<\\/button>/, button);\n    if (!figure.includes("data-zoom-src")) figure += button;',
    "R4 zoom metadata refresh",
  ));
  commands.push(replacementCommand(
    "let R3E_QA = null;",
    "let R3E_QA = null;\nlet R4_CONTRACTS = null;",
    "R4 state",
  ));
  const helper = `function r4Readiness(lang) {\n  const title = lang === "zh" ? "五域接口准备度｜候选 / 未授权" : "REGIONAL INTERFACE READINESS | CANDIDATE / NOT AUTHORIZED";\n  const stats = lang === "zh" ? "合同 5 · 已授权 0 · 运行中 0" : "5 CONTRACTS · 0 AUTHORIZED · 0 OPERATING";\n  const gate = lang === "zh" ? "启动：书面授权 + 一手事实 + 责任接口人" : "ACTIVATE: WRITTEN AUTHORIZATION + FACTUAL BASIS + ACCOUNTABLE OWNER";\n  return \`<article class="regional-readiness"><p><b>\${title}</b><strong>\${stats}</strong><span>\${gate}</span></p></article>\`;\n}\n\n`;
  commands.push(replacementCommand(
    "function f11ProtocolFigure(item, lang, protocols, redTeam, format, extra = \"\") {",
    `${helper}function f11ProtocolFigure(item, lang, protocols, redTeam, format, extra = "") {`,
    "R4 readiness helper",
  ));
  commands.push(replacementCommand(
    '<aside class="governance-cards"><article><h3>',
    '<aside class="governance-cards">${r4Readiness(lang)}<article><h3>',
    "R4 F11 readiness insertion",
  ));
  commands.push(replacementCommand(
    '"16 项红队；13 项 fail / stop / unknown 保留。6 个指标 unknown；12/12 controller unknown；法律、无障碍、安全、现场、运营主体、正式批准未完成或未授权。"',
    '"13 项 fail / stop / unknown 保留；6 个指标、12/12 controller、法律、无障碍、安全、现场、运营主体与批准仍未完成。"',
    "R4 compact Chinese F11 boundary",
  ));
  commands.push(replacementCommand(
    '"16 red-team tests; 13 retained fail / stop / unknown. Six metrics unknown; 12/12 controllers unknown; legal, access, safety, site, operator, and approval incomplete or unauthorized."',
    '"13 fail / stop / unknown retained; six metrics, 12/12 controllers, and legal, access, safety, site, operator, and approval remain incomplete."',
    "R4 compact English F11 boundary",
  ));
  commands.push(replacementCommand(
    ".governance-cards p{margin:0;font-weight:700}",
    ".governance-cards p{margin:0;font-weight:700}.regional-readiness{background:#f7f2e8}.regional-readiness p b,.regional-readiness p strong,.regional-readiness p span{display:block}.regional-readiness p b,.regional-readiness p strong{color:#9b4a3a}",
    "R4 F11 readiness CSS",
  ));
  commands.push(replacementCommand(
    ".governance-cards{min-height:0;display:grid;grid-template-rows:repeat(3,minmax(0,1fr))}",
    ".governance-cards{min-height:0;display:grid;grid-template-rows:repeat(4,minmax(0,1fr))}",
    "R4 F11 readiness governance card",
  ));
  commands.push(replacementCommand(
    "const failures = [];\n  const protectedFiles = freeze.protected_phase2_inputs.files;",
    "const failures = [];\n  const r4Overrides = freeze.r4_regional_interface_override?.file_sha256 ?? {};\n  const protectedFiles = freeze.protected_phase2_inputs.files;",
    "R4 freeze override map",
  ));
  commands.push(replacementCommand(
    "if (actual !== record.expected_sha256) failures.push(`${relative}: ${actual}`);",
    "const required = r4Overrides[relative] ?? record.expected_sha256;\n    if (actual !== required) failures.push(`${relative}: ${actual}`);",
    "R4 protected override",
  ));
  commands.push(replacementCommand(
    "for (const [relative, expected] of Object.entries(freeze.authoritative_semantic_inputs_sha256)) {\n    const target = path.join(SUB, relative);\n    const actual = fs.existsSync(target) ? sha256(target) : \"missing\";\n    if (actual !== expected) failures.push(`${relative}: ${actual}`);\n  }",
    "for (const [relative, expected] of Object.entries(freeze.authoritative_semantic_inputs_sha256)) {\n    const target = path.join(SUB, relative);\n    const actual = fs.existsSync(target) ? sha256(target) : \"missing\";\n    const required = r4Overrides[relative] ?? expected;\n    if (actual !== required) failures.push(`${relative}: ${actual}`);\n  }",
    "R4 semantic override",
  ));
  commands.push(replacementCommand(
    '"assets/media/cover.webp",',
    '"assets/media/cover.webp",\n  "assets/figures/ai-ecosystem.png",\n  "assets/figures/ai-ecosystem.en.png",\n  "assets/figures/operations-pathway.png",\n  "assets/figures/operations-pathway.en.png",',
    "R4 figure outputs",
  ));
  commands.push(replacementCommand(
    'if (!R3E_QA.ok || R3E_QA.tabletop_assertions.passed !== 6 || R3E_QA.tabletop_assertions.field_tests !== 0) throw new Error("R3-E implementation QA drift");',
    'if (!R3E_QA.ok || R3E_QA.tabletop_assertions.passed !== 6 || R3E_QA.tabletop_assertions.field_tests !== 0) throw new Error("R3-E implementation QA drift");\n  R4_CONTRACTS = readJson(R4_CONTRACTS_PATH);\n  if (R4_CONTRACTS.interfaces.length !== 5 || R4_CONTRACTS.interfaces.some(item => item.status !== "candidate_not_authorized" || item.authorization_gate.gate_status !== "not_passed")) throw new Error("R4 regional-interface contract drift");',
    "R4 contract load",
  ));
  commands.push(replacementCommand(
    '"visual/assets/r3e-implementation-sources.json",',
    '"visual/assets/r3e-implementation-sources.json",\n    "visual/assets/regional-interface-contracts.json",\n    "visual/assets/r4-regional-interface-generator.js",',
    "R4 contract inputs",
  ));
  commands.push(replacementCommand(
    "r3e_implementation_evidence_contract: {",
    "r4_regional_interface_contract: { authority: R4_CONTRACTS.authority, interface_ids: R4_CONTRACTS.interfaces.map(item => item.interface_id), status: R4_CONTRACTS.computed_summary, activation: R4_CONTRACTS.computed_summary.activation_condition },\n    r3e_implementation_evidence_contract: {",
    "R4 generation contract field",
  ));
  commands.push(replacementCommand(
    "presentation_only: true,\n      structured_authority_changed: false,",
    "presentation_only: false,\n      structured_authority_changed: true,\n      structured_change_scope: \"IM12 candidate regional-interface contracts and two state-count metrics only\",",
    "R4 authority declaration",
  ));
  const needle = "const temp=path.join(ASSETS,`.r3e-phase4-${process.pid}.mjs`);";
  const replacement = `${commands.join("\n")}\n${needle}`;
  const index = program.indexOf(needle);
  if (index < 0 || program.indexOf(needle, index + needle.length) >= 0) throw new Error("R3-E overlay insertion point missing or non-unique");
  return program.slice(0, index) + replacement + program.slice(index + needle.length);
}

function runR3e(modeName) {
  const bundle = readJson(R3E_BUNDLE_PATH);
  const record = bundle.sources.find((item) => item.restore_as === "r3e-presentation-overlay.mjs");
  if (!record) throw new Error("R3-E overlay source missing");
  const original = `${record.source_lines.join("\n")}\n`;
  const actual = crypto.createHash("sha256").update(Buffer.from(original, "utf8")).digest("hex");
  if (actual !== record.source_sha256) throw new Error(`R3-E overlay hash drift: ${actual}`);
  const patched = patchR3eOverlay(original);
  const temporary = path.join(ASSETS, `.r4-r3e-overlay-${process.pid}.mjs`);
  fs.writeFileSync(temporary, patched, "utf8");
  try {
    const args = [temporary, "--submission", SUB, modeName === "check" ? "--check" : "--generate"];
    const result = spawnSync(process.execPath, args, { stdio: "inherit", env: process.env });
    if (result.status !== 0) throw new Error(`Patched R3-E overlay exited ${result.status}`);
  } finally {
    fs.rmSync(temporary, { force: true });
  }
}

function writeR4Contract(contracts, browserVersion) {
  const inputs = [
    "visual/assets/regional-interface-contracts.json",
    "visual/assets/r4-regional-interface-generator.js",
    "visual/assets/phase4-figure-registry.json",
    "visual/assets/phase4-layout-contract.json",
    "visual/assets/phase3-governance-generator-source.json",
    "visual/assets/rebuild-visuals-source.json",
    "visual/assets/phase3-protocol-contracts.json",
    "visual/assets/phase3-data-governance.json",
    "visual/assets/phase3-red-team.json",
    "assumptions.json",
    "metrics.json",
    "compliance_matrix.json",
    "design_depth_matrix.json",
    "proposal.md",
    "proposal.en.md",
  ];
  const outputs = [...FIGURE_OUTPUTS, ...PRESENTATION_OUTPUTS, "visual/assets/phase4-source-freeze.json", "visual/assets/phase4-generation-contract.json"];
  const payload = {
    schema: "jz-r4-regional-interface-generation-contract/v1",
    generated_at: "2026-08-29",
    authority: {
      implementation_item: "IM12",
      claim: "CL07",
      interface_ids: contracts.interfaces.map((item) => item.interface_id),
      status: "candidate_not_authorized",
      no_new_ids: "No SC13, IM14, F12, fourth flagship, or additional first use.",
      no_real_world_claim: "No external capability, partnership, appointment, exchange, operation, procurement, approval, or implementation is evidenced.",
    },
    toolchain: { node: process.version, playwright: playwrightVersion, chromium: browserVersion },
    visual_contract: {
      canvas_px: [2400, 1600],
      f07: "existing internal loop retains dominant visual weight; five hollow dashed interfaces remain physically disconnected below a closed authorization boundary",
      f11: "readiness is a separate header block in standalone F11 and a separate governance card in native A3/A0, never a lifecycle state or complaint-path overlay; it reports 5 contracts / 0 authorized / 0 operating",
      standalone_png_minimum_new_text_px: 21,
      native_a3_readiness_minimum_pt: 8,
      native_a0_readiness_minimum_pt: 18,
      state_not_color_only: true,
    },
    input_sha256: Object.fromEntries(inputs.map((relative) => [relative, sha256(path.join(SUB, relative))])),
    output_sha256: Object.fromEntries(outputs.map((relative) => [relative, sha256(path.join(SUB, relative))])),
  };
  writeJson(R4_CONTRACT_PATH, payload);
}

function checkR4() {
  const contracts = assertContracts();
  const contract = readJson(R4_CONTRACT_PATH);
  const failures = [];
  for (const [relative, expected] of Object.entries(contract.input_sha256)) {
    const target = path.join(SUB, relative);
    const actual = fs.existsSync(target) ? sha256(target) : "missing";
    if (actual !== expected) failures.push(`input ${relative}: ${actual}`);
  }
  for (const [relative, expected] of Object.entries(contract.output_sha256)) {
    const target = path.join(SUB, relative);
    const actual = fs.existsSync(target) ? sha256(target) : "missing";
    if (actual !== expected) failures.push(`output ${relative}: ${actual}`);
  }
  if (contract.authority.interface_ids.join(",") !== contracts.interfaces.map((item) => item.interface_id).join(",")) failures.push("interface authority IDs drift");
  if (failures.length) throw new Error(`R4 generation contract drift:\n${failures.join("\n")}`);
  runR3e("check");
  console.log(JSON.stringify({ ok: true, interfaces: 5, authorized: 0, operating: 0, outputs: Object.keys(contract.output_sha256).length }, null, 2));
}

async function main() {
  if (mode === "check") {
    checkR4();
  } else {
    const contracts = assertContracts();
    const browserVersion = await renderFigures(contracts);
    updateFreeze();
    if (mode === "figures-only") {
      console.log(JSON.stringify({ ok: true, figures: FIGURE_OUTPUTS, browser: browserVersion }, null, 2));
    } else {
      runR3e("generate");
      writeR4Contract(contracts, browserVersion);
      console.log(JSON.stringify({ ok: true, interfaces: 5, authorized: 0, operating: 0, figures: FIGURE_OUTPUTS.length, presentations: PRESENTATION_OUTPUTS.length }, null, 2));
    }
  }
}

main().catch((error) => {
  console.error(error.stack || error.message || String(error));
  process.exitCode = 1;
});
