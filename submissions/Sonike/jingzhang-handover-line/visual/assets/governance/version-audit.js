#!/usr/bin/env node
"use strict";

/* Pure-Node integrity gate for the visible v2.0 package identity.
 * Binary figures and PDFs are bound to their independently generated stamp
 * reports by SHA-256; HTML and tactile SVG deliverables are checked directly.
 * JZ_AUDIT_OVERLAY lets audit-selftest.js inject defects without touching the
 * submission package. No network or third-party module is used.
 */

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const HERE = __dirname;
const PKG = path.resolve(HERE, "../../..");
const OVERLAY = process.env.JZ_AUDIT_OVERLAY ? path.resolve(process.env.JZ_AUDIT_OVERLAY) : null;
const LABEL = "JING-ZHANG HANDOVER LINE / PACKAGE v2.0";
const STATIC = [
  "report/proposal.html",
  "report/proposal.en.html",
  "visual/index.html",
  "visual/index.en.html",
  "assets/tactile/tactile-corridor-map.svg",
  "assets/tactile/tactile-corridor-map.en.svg",
];

function resolveIn(rel) {
  if (OVERLAY) {
    const candidate = path.join(OVERLAY, rel);
    if (fs.existsSync(candidate)) return candidate;
  }
  return path.join(PKG, rel);
}

function read(rel) { return fs.readFileSync(resolveIn(rel)); }
function json(rel) { return JSON.parse(read(rel).toString("utf8")); }
function sha256(rel) { return crypto.createHash("sha256").update(read(rel)).digest("hex"); }

const errors = [];

let figures = null;
try { figures = json("visual/assets/governance/version-stamp-report.json"); }
catch (error) { errors.push(`version-stamp-report.json 无法读取：${error.message}`); }
if (figures) {
  if (figures.package_version !== "v2.0" || figures.visible_label !== LABEL) errors.push("图件版本报告不是 v2.0");
  if (figures.legacy_visible_version_allowed !== false) errors.push("图件版本报告未禁止旧可见版本");
  if (figures.figure_count !== 26 || !Array.isArray(figures.figures) || figures.figures.length !== 26) {
    errors.push("图件版本报告必须恰含 26 张图件");
  }
  for (const item of figures.figures || []) {
    try {
      if (sha256(item.path) !== item.file_sha256) errors.push(`${item.path}: 与 v2.0 图件版本报告哈希不符`);
    } catch (error) { errors.push(`${item.path}: 缺失或不可读`); }
  }
}

let pdfs = null;
try { pdfs = json("visual/assets/governance/pdf-version-report.json"); }
catch (error) { errors.push(`pdf-version-report.json 无法读取：${error.message}`); }
if (pdfs) {
  if (pdfs.package_version !== "v2.0" || pdfs.ok !== true) errors.push("PDF 版本报告不是通过状态的 v2.0");
  if (pdfs.pdf_count !== 4 || pdfs.page_count !== 38 || !Array.isArray(pdfs.pdfs) || pdfs.pdfs.length !== 4) {
    errors.push("PDF 版本报告必须恰含 4 套、38 页");
  }
  for (const item of pdfs.pdfs || []) {
    if (item.package_v2_hits !== item.pages || item.legacy_v1_15_hits !== 0) {
      errors.push(`${item.path}: 可检索包版本命中数不是 ${item.pages}/0`);
    }
    try {
      if (sha256(item.path) !== item.sha256) errors.push(`${item.path}: 与 v2.0 PDF 版本报告哈希不符`);
    } catch (error) { errors.push(`${item.path}: 缺失或不可读`); }
  }
}

for (const rel of STATIC) {
  try {
    const text = read(rel).toString("utf8");
    if (!text.includes("PACKAGE v2.0")) errors.push(`${rel}: 缺可见 PACKAGE v2.0`);
    if (text.includes("PACKAGE v1.15")) errors.push(`${rel}: 仍含旧可见 PACKAGE v1.15`);
  } catch (error) { errors.push(`${rel}: 缺失或不可读`); }
}

const result = {
  ok: errors.length === 0,
  package_version: "v2.0",
  figure_count: figures ? figures.figure_count : null,
  pdf_count: pdfs ? pdfs.pdf_count : null,
  pdf_page_count: pdfs ? pdfs.page_count : null,
  static_deliverables_checked: STATIC.length,
  errors,
};

if (process.argv.includes("--json")) process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
else if (result.ok) process.stdout.write("PASS  26 张图件、4 套 38 页 PDF 与 6 份静态载体统一为 PACKAGE v2.0\n");
else for (const error of errors) process.stderr.write(`FAIL  ${error}\n`);
process.exit(result.ok ? 0 : 1);
