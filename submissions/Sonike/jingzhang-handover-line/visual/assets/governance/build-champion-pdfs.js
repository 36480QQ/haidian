#!/usr/bin/env node
"use strict";

/*
 * Rebuilds only page 1 of the four review PDFs. Pages 2..n are copied from the
 * audited technical drawing set, so page references and technical content remain
 * stable while the AI/human review preview receives the v2.0 spatial thesis.
 */

const fs = require("fs");
const crypto = require("crypto");
const os = require("os");
const path = require("path");
const { spawnSync } = require("child_process");
const { chromium } = require("playwright");

const HERE = __dirname;
const PKG = path.resolve(HERE, "../../..");
const DRAWINGS = path.join(PKG, "drawings");
const FIGURES = path.join(PKG, "assets/figures");
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const QPDF = "/opt/homebrew/bin/qpdf";
const CJK_FONT = process.env.JZ_CJK_FONT || "/tmp/NotoSansCJKsc-Medium.otf";
const CJK_FONT_SHA256 = "ca094f6b0001fb048ca39ddd797a0cdb0179e1e55c6561e111c49c3e6a61d7b7";

function fail(message) {
  process.stderr.write(`${message}\n`);
  process.exit(1);
}

for (const needed of [CHROME, QPDF, CJK_FONT]) {
  if (!fs.existsSync(needed)) fail(`missing dependency: ${needed}`);
}
if (crypto.createHash("sha256").update(fs.readFileSync(CJK_FONT)).digest("hex") !== CJK_FONT_SHA256) {
  fail(`font checksum mismatch: ${CJK_FONT}`);
}

function fileUrl(file) {
  return `file://${encodeURI(file)}`;
}

const copy = {
  zh: {
    lang: "zh-CN",
    codeA3: "JZ / 01 · 冠军版首页",
    codeA0: "B / 01 · 冠军版展板",
    title: "京张交接线",
    thesis: "一梳三场 · 两翼八支 · 二十单元",
    lead: "把废弃铁路变成一把伸向城市两翼的公共梳：AI 生产空间与可进入、可停用、有人负责的公共服务沿线成对生长。",
    overall: "总体骨架 / 一条公共脊缝合两翼",
    sections: "重点设计 / 三座交接场形成三种城市性格",
    metrics: [
      ["9.5 km", "连续公共脊"], ["8", "东西缝合支线"], ["20", "产业／公共成对单元"],
      ["12 / 12", "离线任务通过"], ["48 / 48", "接管断言通过"], ["0 / 12", "现场任务；待授权"],
    ],
    strip: "机器空间由北向南逐段退场；人工窗口、连续步行面、轨道线索与绿荫始终存在。",
    boundary: "临时边界 / 概念尺寸 / 非道路红线、权属、批准或已建事实",
    package: "JING-ZHANG HANDOVER LINE / PACKAGE v2.0",
  },
  en: {
    lang: "en",
    codeA3: "JZ / 01 · CHAMPIONSHIP COVER",
    codeA0: "B / 01 · CHAMPIONSHIP BOARD",
    title: "JING-ZHANG HANDOVER LINE",
    thesis: "ONE COMB · THREE YARDS · EIGHT TEETH · TWENTY PAIRED CELLS",
    lead: "Turn the disused railway into a civic comb: AI production space and an enterable, stoppable, staffed public service grow in pairs along one continuous spine.",
    overall: "URBAN FRAME / ONE PUBLIC SPINE STITCHES BOTH SIDES",
    sections: "KEY DESIGN / THREE YARDS, THREE URBAN CHARACTERS",
    metrics: [
      ["9.5 km", "continuous public spine"], ["8", "east-west stitch links"], ["20", "industry / civic paired cells"],
      ["12 / 12", "offline tasks passed"], ["48 / 48", "takeover assertions passed"], ["0 / 12", "field tasks; authority pending"],
    ],
    strip: "Machine space recedes from north to south; the staffed counter, continuous path, rail trace and shade remain.",
    boundary: "PROVISIONAL EXTENT / CONCEPT DIMENSIONS / NOT A REDLINE, TITLE, APPROVAL OR AS-BUILT CLAIM",
    package: "JING-ZHANG HANDOVER LINE / PACKAGE v2.0",
  },
};

function html(lang, format) {
  const t = copy[lang];
  const isA3 = format === "a3";
  const page = isA3 ? "420mm 297mm" : "841mm 1189mm";
  const size = isA3 ? "width:420mm;height:297mm" : "width:841mm;height:1189mm";
  const overall = fileUrl(path.join(FIGURES, `site-overview${lang === "en" ? ".en" : ""}.png`));
  const sections = fileUrl(path.join(FIGURES, `key-areas${lang === "en" ? ".en" : ""}.png`));
  const cjkFont = fileUrl(CJK_FONT);
  const cards = t.metrics.map(([n, label], i) => `<div class="metric m${i}"><b>${n}</b><span>${label}</span></div>`).join("");
  return `<!doctype html>
<html lang="${t.lang}"><head><meta charset="utf-8"><style>
@font-face{font-family:JZNoto;src:url("${cjkFont}") format("opentype");font-style:normal;font-weight:100 900}@page{size:${page};margin:0}*{box-sizing:border-box}html,body{margin:0;${size};overflow:hidden}
body{--coal:#171a18;--ink:#262b28;--bone:#f2eddf;--paper:#fbf8ef;--grid:#d8d1c2;--muted:#606560;--red:#c72d1e;--redfill:#e64b3c;--cyan:#00746f;--cyanfill:#00a79f;--yellow:#83660a;--yellowfill:#f1c64a;position:relative;color:var(--ink);background:var(--bone);font-family:JZNoto,sans-serif;background-image:linear-gradient(#d8d1c288 1px,transparent 1px),linear-gradient(90deg,#d8d1c288 1px,transparent 1px)}
body.a3{padding:15mm 18mm 11mm;background-size:10mm 10mm}body.a0{padding:34mm 42mm 28mm;background-size:20mm 20mm}
.head{display:grid;grid-template-columns:1fr auto;gap:12mm;align-items:start;border-bottom:1.2mm solid var(--redfill)}
.a3 .head{height:61mm;padding-bottom:6mm}.a0 .head{height:154mm;padding-bottom:13mm}
.code{font-weight:800;letter-spacing:.16em;color:var(--red);text-transform:uppercase}.a3 .code{font-size:3.8mm}.a0 .code{font-size:8mm}
h1{margin:2.4mm 0 0;line-height:.92;letter-spacing:-.055em}.a3 h1{font-size:${lang === "zh" ? "19mm" : "13.5mm"}}.a0 h1{font-size:${lang === "zh" ? "44mm" : "30mm"}}
.thesis{align-self:end;text-align:right;font-weight:900;color:var(--red);line-height:1.12}.a3 .thesis{font-size:${lang === "zh" ? "6.7mm" : "4.5mm"};max-width:145mm}.a0 .thesis{font-size:${lang === "zh" ? "16mm" : "11mm"};max-width:360mm}
.lead{color:var(--muted);font-weight:500;line-height:1.58}.a3 .lead{margin:4mm 0 0;font-size:${lang === "zh" ? "4.2mm" : "3.5mm"};max-width:240mm}.a0 .lead{margin:9mm 0 0;font-size:${lang === "zh" ? "9.2mm" : "7.2mm"};max-width:610mm}
.plates{display:grid}.a3 .plates{grid-template-columns:1fr 1fr;gap:7mm;height:134mm;margin-top:7mm}.a0 .plates{grid-template-rows:minmax(0,1fr) minmax(0,1fr);gap:17mm;height:770mm;margin-top:18mm}
.plate{margin:0;display:flex;flex-direction:column;min-width:0;min-height:0;overflow:hidden;background:var(--paper);border:.55mm solid var(--coal);padding:3mm}.a0 .plate{padding:7mm;border-width:1.1mm}
.plate figcaption{display:flex;align-items:center;min-height:9mm;font-weight:900;color:var(--red);letter-spacing:.045em;text-transform:uppercase}.a3 .plate figcaption{font-size:${lang === "zh" ? "3.7mm" : "3.1mm"}}.a0 .plate figcaption{min-height:22mm;font-size:${lang === "zh" ? "8.5mm" : "6.8mm"}}
.plate img{display:block;width:100%;height:calc(100% - 9mm);min-height:0;object-fit:contain;background:var(--bone)}.a0 .plate img{height:calc(100% - 22mm)}
.metrics{display:grid;grid-template-columns:repeat(6,1fr)}.a3 .metrics{gap:3mm;height:33mm;margin-top:7mm}.a0 .metrics{gap:8mm;height:91mm;margin-top:18mm}
.metric{background:var(--paper);border-top:2mm solid var(--redfill);padding:3mm}.metric:nth-child(2),.metric:nth-child(5){border-color:var(--cyanfill)}.metric:nth-child(3),.metric:nth-child(6){border-color:var(--yellowfill)}.a0 .metric{border-top-width:4mm;padding:8mm}
.metric b{display:block;line-height:1;color:var(--red)}.metric:nth-child(2) b,.metric:nth-child(5) b{color:var(--cyan)}.metric:nth-child(3) b,.metric:nth-child(6) b{color:var(--yellow)}.a3 .metric b{font-size:5.4mm}.a0 .metric b{font-size:13mm}
.metric span{display:block;color:var(--muted);line-height:1.2}.a3 .metric span{font-size:${lang === "zh" ? "2.7mm" : "2.3mm"};margin-top:2mm}.a0 .metric span{font-size:${lang === "zh" ? "6.5mm" : "5.2mm"};margin-top:5mm}
.foot{display:grid;grid-template-columns:1fr auto;align-items:end;border-top:.6mm solid var(--redfill);color:var(--muted)}.a3 .foot{height:14mm;margin-top:5mm;padding-top:3mm;font-size:2.8mm}.a0 .foot{height:57mm;margin-top:17mm;padding-top:8mm;font-size:6.5mm;border-top-width:1.2mm}.foot strong{display:block;color:var(--coal);margin-bottom:1mm}.package{text-align:right;font-weight:800;letter-spacing:.06em;color:var(--coal)}
</style></head><body class="${format}">
<header class="head"><div><div class="code">${isA3 ? t.codeA3 : t.codeA0}</div><h1>${t.title}</h1><p class="lead">${t.lead}</p></div><div class="thesis">${t.thesis}</div></header>
<main class="plates"><figure class="plate"><figcaption>${t.overall}</figcaption><img src="${overall}"></figure><figure class="plate"><figcaption>${t.sections}</figcaption><img src="${sections}"></figure></main>
<section class="metrics">${cards}</section>
<footer class="foot"><div><strong>${t.strip}</strong>${t.boundary}</div><div class="package">${t.package}<br>${isA3 ? "01–13" : "01–06"}</div></footer>
</body></html>`;
}

const work = fs.mkdtempSync(path.join(os.tmpdir(), "jingzhang-champion-pdfs-"));

function run(command, args) {
  const result = spawnSync(command, args, { encoding: "utf8" });
  if (result.status !== 0) fail(`${command} failed:\n${result.stdout}\n${result.stderr}`);
}

async function rebuild(format, lang) {
  const suffix = lang === "en" ? ".en" : "";
  const basename = format === "a3" ? `a3-booklet${suffix}.pdf` : `a0-boards${suffix}.pdf`;
  const source = path.join(DRAWINGS, basename);
  const htmlPath = path.join(work, `${format}-${lang}.html`);
  const cover = path.join(work, `${format}-${lang}.pdf`);
  const output = path.join(DRAWINGS, `.${basename}.champion.tmp.pdf`);
  fs.writeFileSync(htmlPath, html(lang, format));
  const browser = await chromium.launch({ executablePath: CHROME, headless: true });
  try {
    const page = await browser.newPage();
    await page.goto(fileUrl(htmlPath), { waitUntil: "load" });
    await page.emulateMedia({ media: "print" });
    await page.pdf({ path: cover, printBackground: true, preferCSSPageSize: true, tagged: true });
  } finally {
    await browser.close();
  }
  run(QPDF, ["--empty", "--pages", cover, "1", source, "2-z", "--", output]);
  fs.renameSync(output, source);
  process.stdout.write(`${source}\n`);
}

async function main() {
  for (const format of ["a3", "a0"]) {
    for (const lang of ["zh", "en"]) await rebuild(format, lang);
  }
}

main().catch((error) => fail(error && error.stack ? error.stack : String(error)));
