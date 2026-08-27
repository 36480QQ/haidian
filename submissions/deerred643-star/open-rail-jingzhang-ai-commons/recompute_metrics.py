#!/usr/bin/env python3
"""一键复算：从包内 GeoJSON 离线复算全部核心指标并与 metrics.json 对账。

用法（在提交包根目录执行）：
    python recompute_metrics.py            # 复算 + 对账 + 打印报告
    python recompute_metrics.py --json     # 仅输出机器可读 JSON

依赖：shapely、pyproj（与仓库评审脚本 requirements-review.txt 相同依赖，全部离线）。

口径与 metrics.json 逐条对齐：
  - 面积/长度均在 EPSG:4548 投影下计算（与 metrics.area_calculation_crs 一致）
  - site_area_sqm           = site_boundary 单要素投影面积
  - green_space_area_sqm    = green_space 全要素面积之和
  - public_space_area_sqm   = public_space 全要素面积之和
  - building_footprint_sqm  = buildings 全要素面积之和
  - 三条 ratio              = 对应面积 / site_area_sqm
  - spine_length_m          = roads 中「开源步道·京张遗址慢行主线」中心线长度
  - key_area_*              = key_areas 按 area_id 对应要素面积
  - floor_area_ratio / building_height_control 保持 unknown（官方控规未发布，不复算）

对账容差（即「披露精度」，对应可证伪条件第 4 条）：
  面积类相对偏差 <= 1e-4（0.01%），比率类绝对偏差 <= 1e-4，长度类相对偏差 <= 1e-3。
  任一指标超出容差即判 FAIL 并以非零码退出。

证据输出：visual/assets/recompute-evidence.json（供评审与 CI 复核）。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from pyproj import Transformer
    from shapely.geometry import shape
    from shapely.ops import transform
except ImportError as exc:  # pragma: no cover
    sys.exit(f"缺少依赖 {exc.name}；请先 pip install -r requirements-review.txt")

PKG = Path(__file__).resolve().parent
TRANSFORMER = Transformer.from_crs("EPSG:4326", "EPSG:4548", always_xy=True)

# 指标名 -> (容差类型, 容差)  rel=相对偏差, abs=绝对偏差
TOLERANCES = {
    "site_area_sqm": ("rel", 1e-4),
    "green_space_area_sqm": ("rel", 1e-4),
    "green_ratio": ("abs", 1e-4),
    "public_space_area_sqm": ("rel", 1e-4),
    "public_space_ratio": ("abs", 1e-4),
    "building_footprint_area_sqm": ("rel", 1e-4),
    "building_footprint_ratio": ("abs", 1e-4),
    "spine_length_m": ("rel", 1e-3),
    "key_area_count": ("abs", 0),
    "key_area_zhongzhiyuan_area_sqm": ("rel", 1e-4),
    "key_area_origin_community_area_sqm": ("rel", 1e-4),
    "key_area_dazhongsi_area_sqm": ("rel", 1e-4),
}
KEY_AREA_ID_MAP = {
    "key_area_zhongzhiyuan_area_sqm": "zhongzhiyuan_ai_acceleration_area",
    "key_area_origin_community_area_sqm": "beijing_ai_origin_community",
    "key_area_dazhongsi_area_sqm": "dazhongsi_ai_industry_cluster",
}
SPINE_ROAD_NAME = "开源步道·京张遗址慢行主线"
UNKNOWN_METRICS = ("floor_area_ratio", "building_height_control")  # 官方控规未发布，保持 unknown


def load_features(rel: str):
    path = PKG / "geometry" / rel
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["features"]


def projected(geom):
    return transform(TRANSFORMER.transform, geom)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="仅输出机器可读 JSON")
    args = ap.parse_args()

    metrics = json.loads((PKG / "metrics.json").read_text(encoding="utf-8"))["metrics"]

    site = projected(shape(load_features("site_boundary.geojson")[0]["geometry"]))
    site_area = site.area

    def layer_area(fname: str) -> float:
        return sum(projected(shape(f["geometry"])).area for f in load_features(fname))

    green = layer_area("green_space.geojson")
    pub = layer_area("public_space.geojson")
    bldg = layer_area("buildings.geojson")

    spine_len = 0.0
    for f in load_features("roads.geojson"):
        if f["properties"].get("name_zh") == SPINE_ROAD_NAME:
            spine_len += projected(shape(f["geometry"])).length

    key_feats = {f["properties"]["area_id"]: projected(shape(f["geometry"])).area
                 for f in load_features("key_areas.geojson")}
    key_count = len(key_feats)

    computed = {
        "site_area_sqm": site_area,
        "green_space_area_sqm": green,
        "green_ratio": green / site_area,
        "public_space_area_sqm": pub,
        "public_space_ratio": pub / site_area,
        "building_footprint_area_sqm": bldg,
        "building_footprint_ratio": bldg / site_area,
        "spine_length_m": spine_len,
        "key_area_count": key_count,
        "key_area_zhongzhiyuan_area_sqm": key_feats["zhongzhiyuan_ai_acceleration_area"],
        "key_area_origin_community_area_sqm": key_feats["beijing_ai_origin_community"],
        "key_area_dazhongsi_area_sqm": key_feats["dazhongsi_ai_industry_cluster"],
    }

    rows, failures = [], []
    for name, value in computed.items():
        claimed = metrics.get(name, {}).get("value")
        if claimed is None:
            failures.append(f"{name}: metrics.json 缺少该指标")
            continue
        kind, tol = TOLERANCES[name]
        diff = abs(value - claimed)
        dev = diff / abs(claimed) if kind == "rel" and claimed else diff
        ok = dev <= tol
        rows.append({
            "metric": name, "recomputed": round(value, 3),
            "claimed": claimed, "abs_diff": round(diff, 6),
            "tolerance": f"{kind} <= {tol}", "result": "PASS" if ok else "FAIL",
        })
        if not ok:
            failures.append(f"{name}: 偏差 {dev:.3e} 超出容差 {kind}<={tol}")

    unknown_ok = all(metrics[m]["status"] == "unknown" and metrics[m]["value"] is None
                     for m in UNKNOWN_METRICS)
    if not unknown_ok:
        failures.append("floor_area_ratio / building_height_control 应保持 unknown（官方控规未发布）")

    all_pass = not failures
    evidence = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "crs": "EPSG:4548",
        "script": "recompute_metrics.py",
        "inputs": ["geometry/site_boundary.geojson", "geometry/green_space.geojson",
                   "geometry/public_space.geojson", "geometry/buildings.geojson",
                   "geometry/roads.geojson", "geometry/key_areas.geojson", "metrics.json"],
        "tolerances": {k: f"{v[0]}<={v[1]}" for k, v in TOLERANCES.items()},
        "unknown_metrics_kept": list(UNKNOWN_METRICS),
        "metrics_checked": len(rows),
        "all_pass": all_pass,
        "failures": failures,
        "results": rows,
        "note": "一键复算证据：全部 known 状态指标由包内 GeoJSON 在 EPSG:4548 下独立复算并与 metrics.json 对账；"
                "floor_area_ratio 与 building_height_control 因官方控规未发布保持 unknown，不以推测值冒充。"
                "复算方法与仓库评审脚本一致（pyproj EPSG:4326->4548 投影 + shapely 面积/长度）。",
    }
    out = PKG / "visual" / "assets" / "recompute-evidence.json"
    out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8", newline="")

    if args.json:
        print(json.dumps(evidence, ensure_ascii=False, indent=2))
        return 0 if all_pass else 1

    print("=" * 78)
    print("一键复算报告（recompute_metrics.py，全部离线，EPSG:4548）")
    print("=" * 78)
    for r in rows:
        print(f"  [{r['result']}] {r['metric']:<40} 复算 {r['recomputed']:>15,.3f}"
              f"  声明 {r['claimed']:>15,.3f}  偏差 {r['abs_diff']:.6f}（{r['tolerance']}）")
    print(f"  [INFO] floor_area_ratio / building_height_control 保持 unknown（官方控规未发布）")
    print("-" * 78)
    print(f"结论: {'全部 PASS（%d 项指标复算一致）' % len(rows) if all_pass else 'FAIL: ' + '; '.join(failures)}")
    print(f"证据已写入: visual/assets/recompute-evidence.json")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
