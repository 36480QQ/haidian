#!/usr/bin/env node
/**
 * 一键复算：从包内 GeoJSON 离线复算全部核心指标并与 metrics.json 对账。
 *
 * 用法（在提交包根目录执行）：
 *     node visual/assets/recompute_metrics.js            # 复算 + 对账 + 打印报告
 *     node visual/assets/recompute_metrics.js --json     # 仅输出机器可读 JSON
 *
 * 依赖：Node.js >= 14，仅用标准库（fs/path），全部离线、零外部依赖——
 * 与 visual/index.html 同一技术栈，评审环境无需安装任何包。
 *
 * 口径与 metrics.json 逐条对齐（面积/长度在 EPSG:4548 投影下计算）：
 *   EPSG:4548 = CGCS2000 / 3-degree Gauss-Kruger CM 117E（false easting 500000）。
 *   本脚本内联实现高斯-克吕格投影（CGCS2000 椭球 a=6378137, f=1/298.257222101，
 *   中央经线 117°E），与仓库评审脚本（pyproj EPSG:4326→4548 + shapely）口径一致；
 *   平移参数（false easting）不影响面积与长度，故不引入。
 *   ——与 metrics.json 声明值对账容差：面积类相对 1e-4，比率类绝对 1e-4，长度类相对 1e-3。
 *   任一指标超出容差即判 FAIL 并以非零码退出（对应可证伪条件第 4 条「复算主张」）。
 *
 * 证据输出：visual/assets/recompute-evidence.json（供评审与 CI 复核）。
 */
"use strict";

const fs = require("fs");
const path = require("path");

const PKG = path.resolve(__dirname, "..", ".."); // visual/assets/ -> 包根
const SPINE_ROAD_NAME = "开源步道·京张遗址慢行主线";
const UNKNOWN_METRICS = ["floor_area_ratio", "building_height_control"];

const TOLERANCES = {
  site_area_sqm: ["rel", 1e-4],
  green_space_area_sqm: ["rel", 1e-4],
  green_ratio: ["abs", 1e-4],
  public_space_area_sqm: ["rel", 1e-4],
  public_space_ratio: ["abs", 1e-4],
  building_footprint_area_sqm: ["rel", 1e-4],
  building_footprint_ratio: ["abs", 1e-4],
  spine_length_m: ["rel", 1e-3],
  key_area_count: ["abs", 0],
  key_area_zhongzhiyuan_area_sqm: ["rel", 1e-4],
  key_area_origin_community_area_sqm: ["rel", 1e-4],
  key_area_dazhongsi_area_sqm: ["rel", 1e-4],
};

// ---------------- CGCS2000 椭球 + 高斯-克吕格投影（CM 117E） ----------------
const A = 6378137.0;                    // 长半轴
const F = 1 / 298.257222101;            // 扁率（CGCS2000）
const E2 = 2 * F - F * F;               // 第一偏心率平方
const CENTRAL_MERIDIAN = 117.0;         // EPSG:4548 中央经线（3-degree GK CM 117E）
const RAD = Math.PI / 180;

/** 经纬度（度）-> 高斯-克吕格平面坐标（米，相对中央经线，无平移） */
function gkProject(lonDeg, latDeg) {
  const lon = (lonDeg - CENTRAL_MERIDIAN) * RAD;
  const lat = latDeg * RAD;
  const sinLat = Math.sin(lat);
  const cosLat = Math.cos(lat);
  const tanLat = Math.tan(lat);
  const e2 = E2;
  const ep2 = e2 / (1 - e2);            // 第二偏心率平方
  const N = A / Math.sqrt(1 - e2 * sinLat * sinLat);   // 卯酉圈曲率半径
  const T = tanLat * tanLat;
  const C = ep2 * cosLat * cosLat;
  const Aa = cosLat * lon;
  const M =
    A *
    ((1 - e2 / 4 - (3 * e2 * e2) / 64 - (5 * e2 * e2 * e2) / 256) * lat -
      ((3 * e2) / 8 + (3 * e2 * e2) / 32 + (45 * e2 * e2 * e2) / 1024) *
        Math.sin(2 * lat) +
      ((15 * e2 * e2) / 256 + (45 * e2 * e2 * e2) / 1024) * Math.sin(4 * lat) -
      ((35 * e2 * e2 * e2) / 3072) * Math.sin(6 * lat));
  const x = N * (Aa + ((1 - T + C) * Aa ** 3) / 6 + ((5 - 18 * T + T * T + 72 * C - 58 * ep2) * Aa ** 5) / 120); // 东向
  const y = M + N * tanLat * (Aa ** 2 / 2 + ((5 - T + 9 * C + 4 * C * C) * Aa ** 4) / 24 + ((61 - 58 * T + T * T + 600 * C - 330 * ep2) * Aa ** 6) / 720); // 北向
  return [x, y];
}

// ---------------- GeoJSON 几何计算 ----------------
function ringArea(ring) {
  // 平面 shoelace；GeoJSON 面与内部环反号，直接累加即得带孔面积
  let s = 0;
  const pts = ring.map(([lon, lat]) => gkProject(lon, lat));
  for (let i = 0; i < pts.length - 1; i++) {
    s += pts[i][0] * pts[i + 1][1] - pts[i + 1][0] * pts[i][1];
  }
  return Math.abs(s) / 2;
}

function geomArea(geom) {
  if (geom.type === "Polygon") return geom.coordinates.reduce((a, r) => a + ringArea(r), 0);
  if (geom.type === "MultiPolygon")
    return geom.coordinates.reduce((a, p) => a + p.reduce((b, r) => b + ringArea(r), 0), 0);
  if (geom.type === "GeometryCollection")
    return geom.geometries.reduce((a, g) => a + geomArea(g), 0);
  return 0;
}

function geomLength(geom) {
  let total = 0;
  const lines = geom.type === "LineString" ? [geom.coordinates]
    : geom.type === "MultiLineString" ? geom.coordinates : [];
  for (const line of lines) {
    for (let i = 0; i < line.length - 1; i++) {
      const [x1, y1] = gkProject(line[i][0], line[i][1]);
      const [x2, y2] = gkProject(line[i + 1][0], line[i + 1][1]);
      total += Math.hypot(x2 - x1, y2 - y1);
    }
  }
  return total;
}

function loadFeatures(name) {
  return JSON.parse(fs.readFileSync(path.join(PKG, "geometry", name), "utf8")).features;
}

// ---------------- 主流程 ----------------
function main() {
  const jsonOnly = process.argv.includes("--json");
  const metrics = JSON.parse(fs.readFileSync(path.join(PKG, "metrics.json"), "utf8")).metrics;

  const siteArea = geomArea(loadFeatures("site_boundary.geojson")[0].geometry);
  const layerArea = (f) => loadFeatures(f).reduce((a, x) => a + geomArea(x.geometry), 0);
  const green = layerArea("green_space.geojson");
  const pub = layerArea("public_space.geojson");
  const bldg = layerArea("buildings.geojson");

  let spineLen = 0;
  for (const f of loadFeatures("roads.geojson")) {
    if (f.properties && f.properties.name_zh === SPINE_ROAD_NAME) spineLen += geomLength(f.geometry);
  }

  const keyFeats = {};
  for (const f of loadFeatures("key_areas.geojson")) keyFeats[f.properties.area_id] = geomArea(f.geometry);

  const computed = {
    site_area_sqm: siteArea,
    green_space_area_sqm: green,
    green_ratio: green / siteArea,
    public_space_area_sqm: pub,
    public_space_ratio: pub / siteArea,
    building_footprint_area_sqm: bldg,
    building_footprint_ratio: bldg / siteArea,
    spine_length_m: spineLen,
    key_area_count: Object.keys(keyFeats).length,
    key_area_zhongzhiyuan_area_sqm: keyFeats.zhongzhiyuan_ai_acceleration_area,
    key_area_origin_community_area_sqm: keyFeats.beijing_ai_origin_community,
    key_area_dazhongsi_area_sqm: keyFeats.dazhongsi_ai_industry_cluster,
  };

  const rows = [];
  const failures = [];
  for (const [name, value] of Object.entries(computed)) {
    const claimed = metrics[name] && metrics[name].value;
    if (claimed == null) { failures.push(`${name}: metrics.json 缺少该指标`); continue; }
    const [kind, tol] = TOLERANCES[name];
    const diff = Math.abs(value - claimed);
    const dev = kind === "rel" && claimed ? diff / Math.abs(claimed) : diff;
    const ok = dev <= tol;
    rows.push({
      metric: name, recomputed: +value.toFixed(3), claimed,
      abs_diff: +diff.toFixed(6), tolerance: `${kind} <= ${tol}`,
      result: ok ? "PASS" : "FAIL",
    });
    if (!ok) failures.push(`${name}: 偏差 ${dev.toExponential(3)} 超出容差 ${kind}<=${tol}`);
  }

  const unknownOk = UNKNOWN_METRICS.every((m) => metrics[m].status === "unknown" && metrics[m].value == null);
  if (!unknownOk) failures.push("floor_area_ratio / building_height_control 应保持 unknown（官方控规未发布）");

  const allPass = failures.length === 0;
  const evidence = {
    schema_version: "1.0.0",
    generated_at: new Date().toISOString().replace(/\.\d{3}Z$/, "Z"),
    crs: "EPSG:4548",
    script: "visual/assets/recompute_metrics.js",
    runtime: "Node.js（仅标准库，零外部依赖，全离线）",
    inputs: [
      "geometry/site_boundary.geojson", "geometry/green_space.geojson",
      "geometry/public_space.geojson", "geometry/buildings.geojson",
      "geometry/roads.geojson", "geometry/key_areas.geojson", "metrics.json",
    ],
    tolerances: Object.fromEntries(Object.entries(TOLERANCES).map(([k, v]) => [k, `${v[0]}<=${v[1]}`])),
    unknown_metrics_kept: UNKNOWN_METRICS,
    metrics_checked: rows.length,
    all_pass: allPass,
    failures,
    results: rows,
    note: "一键复算证据：全部 known 状态指标由包内 GeoJSON 在 EPSG:4548（CGCS2000 / 3-degree Gauss-Kruger CM 117E，脚本内联投影实现）下独立复算并与 metrics.json 对账；floor_area_ratio 与 building_height_control 因官方控规未发布保持 unknown，不以推测值冒充。复算口径与仓库评审脚本一致（EPSG:4326→4548 投影面积/长度）。",
  };
  fs.writeFileSync(
    path.join(__dirname, "recompute-evidence.json"),
    JSON.stringify(evidence, null, 2) + "\n", "utf8");

  if (jsonOnly) { console.log(JSON.stringify(evidence, null, 2)); process.exit(allPass ? 0 : 1); }

  const line = "=".repeat(78);
  console.log(line);
  console.log("一键复算报告（recompute_metrics.js，Node.js 零依赖，全离线，EPSG:4548）");
  console.log(line);
  for (const r of rows) {
    console.log(
      `  [${r.result}] ${r.metric.padEnd(40)} 复算 ${r.recomputed.toLocaleString("en-US", { minimumFractionDigits: 3 })}` +
      `  声明 ${r.claimed.toLocaleString("en-US", { minimumFractionDigits: 3 })}  偏差 ${r.abs_diff}（${r.tolerance}）`);
  }
  console.log("  [INFO] floor_area_ratio / building_height_control 保持 unknown（官方控规未发布）");
  console.log("-".repeat(78));
  console.log(allPass ? `结论: 全部 PASS（${rows.length} 项指标复算一致）` : `结论: FAIL: ${failures.join("; ")}`);
  console.log("证据已写入: visual/assets/recompute-evidence.json");
  process.exit(allPass ? 0 : 1);
}

main();
