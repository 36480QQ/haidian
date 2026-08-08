#!/usr/bin/env python3
"""
京张智脉 — metrics.json 生成脚本 v2（符合 schema: schema_version/units/metrics 顶层结构）
全部指标从 GeoJSON 在 EPSG:4548 下复算
"""
import json
from shapely.geometry import shape, mapping, Polygon, LineString
from pyproj import Transformer

SUB = "submissions/xusu-ai/jingzhang-ai-vein"
GEOM = f"{SUB}/geometry"

to_4548 = Transformer.from_crs("EPSG:4326", "EPSG:4548", always_xy=True)

def area_sqm(poly_geom):
    if poly_geom.is_empty:
        return 0.0
    if poly_geom.geom_type == "MultiPolygon":
        return sum(area_sqm(p) for p in poly_geom.geoms)
    coords = list(poly_geom.exterior.coords)
    projected = [to_4548.transform(x, y) for x, y in coords]
    return abs(Polygon(projected).area)

def length_m(line_geom):
    if line_geom.is_empty:
        return 0.0
    if line_geom.geom_type == "MultiLineString":
        return sum(length_m(l) for l in line_geom.geoms)
    projected = [to_4548.transform(x, y) for x, y in line_geom.coords]
    return LineString(projected).length

def load(name):
    return json.load(open(f"{GEOM}/{name}.geojson"))

def polys(name):
    fc = load(name)
    return [shape(f["geometry"]) for f in fc["features"]]

site = shape(load("site_boundary")["features"][0]["geometry"])
site_area = area_sqm(site)

land_use = load("land_use")
lu_by_code = {}
for f in land_use["features"]:
    code = f["properties"]["land_use_code"]
    lu_by_code.setdefault(code, 0.0)
    lu_by_code[code] += area_sqm(shape(f["geometry"]))

buildings_area = sum(area_sqm(p) for p in polys("buildings"))
green_area = sum(area_sqm(p) for p in polys("green_space"))
public_area = sum(area_sqm(p) for p in polys("public_space"))
roads_len = sum(length_m(p) for p in polys("roads"))
key_areas = [shape(f["geometry"]) for f in load("key_areas")["features"]]

phase_areas = {}
for f in load("phasing")["features"]:
    phase_areas[f["properties"]["phase_code"]] = area_sqm(shape(f["geometry"]))

key_area_list = []
for f in load("key_areas")["features"]:
    key_area_list.append({
        "id": f["id"],
        "area_id": f["properties"].get("area_id"),
        "area_sqm": round(area_sqm(shape(f["geometry"])), 1),
    })

M = {}
M["site_area_sqm"] = {
    "status": "known", "value": round(site_area, 1), "unit": "sqm",
    "source_files": ["geometry/site_boundary.geojson"],
    "formula": "polygon_area(site_boundary) in EPSG:4548",
    "confidence": "medium",
    "assumptions": ["基于 provisional 边界（provisional_rough），官方 polygon 缺失，非正式红线"],
}
M["land_use_area_by_code"] = {
    "status": "known", "unit": "sqm",
    "source_files": ["geometry/land_use.geojson"],
    "formula": "sum polygon_area per land_use_code in EPSG:4548",
    "confidence": "medium",
    "assumptions": ["概念性分区建议，非控规结论"],
    "values": {k: round(v, 1) for k, v in sorted(lu_by_code.items())},
}
M["total_floor_area_sqm"] = {
    "status": "known", "value": round(buildings_area * 3.2, 1), "unit": "sqm",
    "source_files": ["geometry/buildings.geojson"],
    "formula": "building_footprint_area * average_floors(3.2 concept)",
    "confidence": "low",
    "assumptions": ["层数为概念假设（5-10层），非工程结论"],
}
M["floor_area_ratio"] = {
    "status": "known", "value": round(buildings_area * 3.2 / site_area, 4), "unit": "ratio",
    "source_files": ["geometry/buildings.geojson", "geometry/site_boundary.geojson"],
    "formula": "total_floor_area / site_area",
    "confidence": "low",
    "assumptions": ["概念容积率，官方控规条件缺失（planning_limits.json 标记 missing）"],
}
M["building_density"] = {
    "status": "known", "value": round(buildings_area / site_area, 4), "unit": "ratio",
    "source_files": ["geometry/buildings.geojson", "geometry/site_boundary.geojson"],
    "formula": "building_footprint_area / site_area",
    "confidence": "low",
    "assumptions": ["概念建筑密度，非控规结论"],
}
M["building_footprint_area_sqm"] = {
    "status": "known", "value": round(buildings_area, 1), "unit": "sqm",
    "source_files": ["geometry/buildings.geojson"],
    "formula": "sum polygon_area(buildings) in EPSG:4548",
    "confidence": "medium",
    "assumptions": ["概念建筑基底，非现状测绘"],
}
M["green_ratio"] = {
    "status": "known", "value": round(green_area / site_area, 4), "unit": "ratio",
    "source_files": ["geometry/green_space.geojson", "geometry/site_boundary.geojson"],
    "formula": "green_space_area / site_area",
    "confidence": "medium",
    "assumptions": ["绿地面积含京张遗址公园带概念范围"],
}
M["public_space_ratio"] = {
    "status": "known", "value": round(public_area / site_area, 4), "unit": "ratio",
    "source_files": ["geometry/public_space.geojson", "geometry/site_boundary.geojson"],
    "formula": "public_space_area / site_area",
    "confidence": "medium",
    "assumptions": ["广场与公共空间为概念范围"],
}
M["road_length_m"] = {
    "status": "known", "value": round(roads_len, 1), "unit": "m",
    "source_files": ["geometry/roads.geojson"],
    "formula": "sum linestring_length(roads) in EPSG:4548",
    "confidence": "medium",
    "assumptions": ["道路中心线为概念骨架，非道路红线"],
}
M["phasing_area_sqm"] = {
    "status": "known", "unit": "sqm",
    "source_files": ["geometry/phasing.geojson"],
    "formula": "polygon_area per phase in EPSG:4548",
    "confidence": "medium",
    "assumptions": ["分期为概念建议"],
    "values": {k: round(v, 1) for k, v in phase_areas.items()},
}
M["key_area_count"] = {
    "status": "known", "value": len(key_areas), "unit": "count",
    "source_files": ["geometry/key_areas.geojson"],
    "formula": "count(key_area features)",
    "confidence": "high",
    "assumptions": [],
}
M["key_area_details"] = {
    "status": "known", "unit": "sqm",
    "source_files": ["geometry/key_areas.geojson"],
    "formula": "polygon_area per key area in EPSG:4548",
    "confidence": "medium",
    "assumptions": ["重点区为 provisional 边界"],
    "values": key_area_list,
}

out = {
    "schema_version": "0.1.0",
    "units": {
        "length": "m",
        "area": "sqm",
        "ratio": "ratio",
        "count": "count",
    },
    "metrics": M,
}

with open(f"{SUB}/metrics.json", "w") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

print("✅ metrics.json v2 已生成（schema 合规）")
print(f"  场地: {site_area/1e6:.2f} km² | 绿地率: {green_area/site_area*100:.1f}% | 建筑基底: {buildings_area/1e4:.1f} ha")
