#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const packageRoot = path.resolve(__dirname, "..", "..");
const entrypoints = ["report/proposal.html", "visual/index.html"];
const fontStylesheetPath = "visual/assets/cjk-font.css";
const expectedLinks = {
  "report/proposal.html": "../visual/assets/cjk-font.css",
  "visual/index.html": "assets/cjk-font.css"
};
const criticalStrings = ["京张验真公地", "公众判据", "临时边界", "概念建议", "待授权实测"];
const dataUriPattern = /data:font\/woff2;base64,([A-Za-z0-9+/=]+)/;

function fail(message) {
  console.error(JSON.stringify({ ok: false, error: message }, null, 2));
  process.exit(1);
}

const fontCss = fs.readFileSync(path.join(packageRoot, fontStylesheetPath), "utf8");
const fontMatch = fontCss.match(dataUriPattern);
if (!fontMatch) fail(`${fontStylesheetPath}: missing inline WOFF2 data URI`);

const results = entrypoints.map((relativePath) => {
  const html = fs.readFileSync(path.join(packageRoot, relativePath), "utf8");
  if (!html.includes(`href="${expectedLinks[relativePath]}"`)) fail(`${relativePath}: missing local CJK stylesheet link`);
  const missingText = criticalStrings.filter((text) => !html.includes(text));
  if (missingText.length) fail(`${relativePath}: missing smoke text ${missingText.join(", ")}`);
  if (!html.includes('font-family: "JZAC Noto Sans SC"') && !html.includes('font-family:"JZAC Noto Sans SC"')) {
    fail(`${relativePath}: packaged font is not the first declared family`);
  }
  if (/(?:src|href)\s*=\s*["'](?:https?:)?\/\//i.test(html) || /@import\s+(?:url\()?\s*["']?(?:https?:)?\/\//i.test(html)) {
    fail(`${relativePath}: remote runtime dependency detected`);
  }
  return { relativePath, html };
});

if (/(?:src|href)\s*=\s*["'](?:https?:)?\/\//i.test(fontCss) || /@import\s+(?:url\()?\s*["']?(?:https?:)?\/\//i.test(fontCss)) {
  fail(`${fontStylesheetPath}: remote runtime dependency detected`);
}
const fontBytes = Buffer.from(fontMatch[1], "base64");
if (fontBytes.subarray(0, 4).toString("ascii") !== "wOF2") fail("inline font has an invalid WOFF2 signature");
if (fontBytes.length < 100000) fail("inline font payload is unexpectedly small");
if (/<script\b/i.test(results[0].html)) fail("report/proposal.html must remain script-free");
if (!results[1].html.includes("font-smoke-test.js?v=1.4.1")) fail("visual/index.html is missing the runtime font check");

console.log(JSON.stringify({
  ok: true,
  entrypoints,
  fontStylesheetPath,
  criticalStrings,
  fontBytes: fontBytes.length,
  reportScriptFree: true,
  sharedLocalStylesheet: true,
  remoteRuntimeDependency: false
}, null, 2));
