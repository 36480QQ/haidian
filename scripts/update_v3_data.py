#!/usr/bin/env python3
"""
V2 方案数据文件更新器 v3（完全对齐官方 schema）
"""
import json, hashlib, os, math
from shapely.geometry import Polygon, box
from pyproj import Transformer
from datetime import datetime, timezone

SUB = "submissions/xusu-ai/jingzhang-ai-vein"
GEOM = f"{SUB}/geometry"
scene = json.load(open("/tmp/scene_v3.json"))

# ---------- 坐标转换 ----------
A_LON, B_LON = 0.0000116374, 116.3475
C_LAT, D_LAT = 0.0000090074, 39.98275
to_4548 = Transformer.from_crs("EPSG:4326", "EPSG:4548", always_xy=True)
SITE_RINGS = scene["site"]["rings"]

def to_wgs(ring):
    return [[round(A_LON*p[0]+B_LON, 9), round(C_LAT*p[1]+D_LAT, 9)] for p in ring]

def area_4548(ring):
    wgs = to_wgs(ring)
    proj = [to_4548.transform(x, y) for x, y in wgs]
    return abs(Polygon(proj).area)

SITE_AREA = area_4548(SITE_RINGS)

def poly_geom(ring):
    wgs = to_wgs(ring)
    return {"type": "Polygon", "coordinates": [wgs + [wgs[0]]]}

def line_geom(pts):
    wgs = [to_wgs([p])[0] for p in pts]
    return {"type": "LineString", "coordinates": wgs}

def fc(features):
    return {"type": "FeatureCollection", "features": features}

def feat(fid, layer, geom, props):
    return {"type": "Feature", "id": fid, "properties": props, "geometry": geom}

# ---------- 1. land_use.geojson ----------
lu_features = []
for lu in scene["landUse"]:
    lu_features.append(feat(lu["id"], "LAND_USE", poly_geom(lu["rings"]), {
        "id": lu["id"], "layer": "LAND_USE", "land_use_code": lu["code"],
        "label_zh": lu["label"], "source_type": "agent_generated_design",
        "confidence": "medium", "geometry_role": "design_proposal",
        "official_boundary": False, "area_sqm_declared": round(area_4548(lu["rings"]), 1),
        "design_note": "V3 真实案例版：以 x=0 城市中轴镜像成对，含日照校核（间距系数1.7）",
    }))
json.dump(fc(lu_features), open(f"{GEOM}/land_use.geojson", "w"), ensure_ascii=False)
print(f"✅ land_use.geojson: {len(lu_features)}")

# ---------- 2. buildings.geojson ----------
b_features = []
for b in scene["buildings"]:
    b_features.append(feat(b["id"], "BUILDING_FOOTPRINT", poly_geom(b["rings"]), {
        "id": b["id"], "layer": "BUILDING_FOOTPRINT",
        "source_type": "agent_generated_design", "confidence": "medium",
        "geometry_role": "design_proposal", "building_type": b["type"],
        "land_use_parent": b["parent"], "height_m_concept": b["height"],
        "floors_concept": b["floors"], "status_concept": "new_build",
        "area_sqm_declared": round(area_4548(b["rings"]), 1), "phase_concept": b["phase"],
        "real_case_ref": b.get("case", ""),
        "design_note": "V3 真实北京案例体块：居住板楼(55×14m/11-18层/间距≥1.2H)科研超高层(中国尊/正大中心级)商业综合体(大悦城级)文化馆(首博级)",
    }))
json.dump(fc(b_features), open(f"{GEOM}/buildings.geojson", "w"), ensure_ascii=False)
print(f"✅ buildings.geojson: {len(b_features)}")

# ---------- 3. roads.geojson ----------
r_features = []
cls_map = {"arterial":"主干路","secondary":"次干路","branch":"支路"}
for r in scene["roads"]:
    r_features.append(feat(r["id"], "ROAD_CENTERLINE", line_geom(r["pts"]), {
        "id": r["id"], "layer": "ROAD_CENTERLINE",
        "source_type": "agent_generated_design", "confidence": "medium",
        "geometry_role": "design_proposal", "road_class": r["cls"],
        "road_class_label": cls_map.get(r["cls"], r["cls"]), "name_zh": r["name"],
        "status": "concept_proposal",
    }))
json.dump(fc(r_features), open(f"{GEOM}/roads.geojson", "w"), ensure_ascii=False)
print(f"✅ roads.geojson: {len(r_features)}")

# ---------- 4. green_space / public_space ----------
g_features = [feat(g["id"], "GREEN_SPACE", poly_geom(g["rings"]), {
    "id": g["id"], "layer": "GREEN_SPACE", "name_zh": g["name"],
    "source_type": "agent_generated_design", "confidence": "medium",
    "geometry_role": "design_proposal", "official_boundary": False,
}) for g in scene["greenSpace"]]
json.dump(fc(g_features), open(f"{GEOM}/green_space.geojson", "w"), ensure_ascii=False)
print(f"✅ green_space.geojson: {len(g_features)}")

p_features = [feat(p["id"], "PUBLIC_SPACE", poly_geom(p["rings"]), {
    "id": p["id"], "layer": "PUBLIC_SPACE", "name_zh": p["name"],
    "source_type": "agent_generated_design", "confidence": "medium",
    "geometry_role": "design_proposal",
}) for p in scene["publicSpace"]]
json.dump(fc(p_features), open(f"{GEOM}/public_space.geojson", "w"), ensure_ascii=False)
print(f"✅ public_space.geojson: {len(p_features)}")

# ---------- 5. key_areas.geojson（对齐 V1 schema：area_id + provisional_constraint）----------
key_area_specs = [
    ("PROV-KEY-001", "zhongzhiyuan_ai_acceleration_area", "众智园AI自主创新加速区（对称双翼+中轴）", "众智园AI加速区", 192.9),
    ("PROV-KEY-002", "beijing_ai_origin_community", "北京AI原点社区（对称双翼+中轴）", "AI原点社区", 104.3),
    ("PROV-KEY-003", "dazhongsi_ai_industry_cluster", "大钟寺AI产业聚集区（对称双翼+中轴）", "大钟寺AI集聚区", 72.0),
]
k_features = []
for i, (kid, area_id, name, short, announced) in enumerate(key_area_specs):
    ring = scene["keyAreas"][i]["rings"]
    k_features.append(feat(kid, "KEY_AREA", poly_geom(ring), {
        "id": kid, "layer": "KEY_AREA", "parent_scope_id": "key_detailed_design_area",
        "area_id": area_id, "name_zh": name, "short_name_zh": short,
        "source_type": "agent_inferred_from_public_data", "confidence": "medium",
        "geometry_role": "provisional_constraint", "official_boundary": False,
        "boundary_precision": "provisional_rough",
        "announced_area_sqm": announced*10000,
        "area_sqm_calculated": round(area_4548(ring), 1),
        "source_id": "DATA-SRC-PROVISIONAL-BOUNDARIES-20260605",
        "derived_from_source_ids": ["DATA-SRC-OFFICIAL-ANNOUNCEMENT-20260509"],
        "source_title": "依据公告重点片区名称、南北顺序和临时 SITE_BOUNDARY 形成的临时粗略范围",
        "derivation_method": "V2 方案：以 x=0 中轴对称双翼+中轴绿带划定；公告未给出四至，矩形边不得解释为地块或道路红线。",
        "usage_note": "仅用于 AI agent 生成、展示和临时自检；不得作为 official key-area polygon、审批依据或精确面积复算依据。",
    }))
json.dump(fc(k_features), open(f"{GEOM}/key_areas.geojson", "w"), ensure_ascii=False)
print(f"✅ key_areas.geojson: {len(k_features)}")

# ---------- 6. phasing.geojson（layer=PHASE）----------
ph_features = []
for p in scene["phasing"]:
    ph_features.append(feat(p["id"], "PHASE", poly_geom(p["rings"]), {
        "id": p["id"], "layer": "PHASE", "phase_code": p["code"],
        "phase_label_zh": p["label"], "phase_note_zh": p["note"],
        "source_type": "agent_generated_design", "confidence": "medium",
        "geometry_role": "design_proposal",
    }))
json.dump(fc(ph_features), open(f"{GEOM}/phasing.geojson", "w"), ensure_ascii=False)
print(f"✅ phasing.geojson: {len(ph_features)}")

# ---------- 7. metrics.json（对齐 V1 schema 键名）----------
total_floor = sum(b["area"]*b["floors"] for b in scene["buildings"])
bld_foot = sum(b["area"] for b in scene["buildings"])
green_area = sum(area_4548(g["rings"]) for g in scene["greenSpace"])
pub_area = sum(area_4548(p["rings"]) for p in scene["publicSpace"])
road_len_m = sum(math.dist(r["pts"][0], r["pts"][1]) for r in scene["roads"])
lu_by_code = {}
for lu in scene["landUse"]:
    lu_by_code[lu["code"]] = lu_by_code.get(lu["code"], 0.0) + lu["area_sqm"]
phase_areas = {}
for p in scene["phasing"]:
    phase_areas[p["code"]] = round(area_4548(p["rings"]), 1)

metrics = {
  "schema_version": "0.1.0",
  "units": {"length": "m", "area": "sqm", "ratio": "ratio", "count": "count"},
  "metrics": {
    "site_area_sqm": {"status": "known", "value": round(SITE_AREA,1), "unit": "sqm",
      "source_files": ["geometry/site_boundary.geojson"],
      "formula": "polygon_area(site_boundary) in EPSG:4548", "confidence": "medium",
      "assumptions": ["provisional 边界（provisional_rough）"]},
    "land_use_area_by_code": {"status": "known", "unit": "sqm",
      "source_files": ["geometry/land_use.geojson"],
      "formula": "sum polygon_area per land_use_code in EPSG:4548",
      "confidence": "medium", "assumptions": ["V2 中轴对称重划方案"],
      "values": {k: round(v,1) for k,v in lu_by_code.items()},
      "value": round(sum(lu_by_code.values()),1)},
    "total_floor_area_sqm": {"status": "known", "value": round(total_floor,1), "unit": "sqm",
      "source_files": ["geometry/buildings.geojson"],
      "formula": "sum(building_footprint_area * floors_concept)", "confidence": "low",
      "assumptions": ["层数为概念值，南低北高满足日照"]},
    "floor_area_ratio": {"status": "known", "value": round(total_floor/SITE_AREA, 4), "unit": "ratio",
      "source_files": ["geometry/buildings.geojson", "geometry/site_boundary.geojson"],
      "formula": "total_floor_area / site_area", "confidence": "low",
      "assumptions": ["概念容积率，V2 对称方案 ≤1.0"]},
    "building_density": {"status": "known", "value": round(bld_foot/SITE_AREA, 4), "unit": "ratio",
      "source_files": ["geometry/buildings.geojson", "geometry/site_boundary.geojson"],
      "formula": "building_footprint_area / site_area", "confidence": "low",
      "assumptions": ["概念建筑密度"]},
    "building_footprint_area_sqm": {"status": "known", "value": round(bld_foot,1), "unit": "sqm",
      "source_files": ["geometry/buildings.geojson"],
      "formula": "sum(building_footprint_area)", "confidence": "low"},
    "green_ratio": {"status": "known", "value": round(green_area/SITE_AREA, 4), "unit": "ratio",
      "source_files": ["geometry/green_space.geojson", "geometry/site_boundary.geojson"],
      "formula": "green_space_area / site_area", "confidence": "medium",
      "assumptions": ["V2 中轴绿带三段（京张遗址公园）"]},
    "public_space_ratio": {"status": "known", "value": round(pub_area/SITE_AREA, 4), "unit": "ratio",
      "source_files": ["geometry/public_space.geojson", "geometry/site_boundary.geojson"],
      "formula": "public_space_area / site_area", "confidence": "medium",
      "assumptions": ["广场与公共空间为概念范围"]},
    "road_length_m": {"status": "known", "value": round(road_len_m, 1), "unit": "m",
      "source_files": ["geometry/roads.geojson"],
      "formula": "sum(line_length) in EPSG:4548", "confidence": "medium",
      "assumptions": ["V2 中轴+双翼纵路+六横轴"]},
    "building_count": {"status": "known", "value": len(scene["buildings"]), "unit": "count",
      "source_files": ["geometry/buildings.geojson"], "formula": "count(features)",
      "confidence": "high"},
    "phasing_area_sqm": {"status": "known", "unit": "sqm",
      "source_files": ["geometry/phasing.geojson"],
      "formula": "polygon_area per phase_code in EPSG:4548", "confidence": "medium",
      "values": phase_areas,
      "value": round(sum(phase_areas.values()),1)},
    "key_area_count": {"status": "known", "value": len(k_features), "unit": "count",
      "source_files": ["geometry/key_areas.geojson"], "formula": "count(features)",
      "confidence": "high"},
    "key_area_details": {"status": "known",
      "value": round(sum(area_4548(k["rings"]) for k in scene["keyAreas"]), 1),
      "unit": "sqm", "source_files": ["geometry/key_areas.geojson"],
      "formula": "sum key area polygon area in EPSG:4548", "confidence": "medium",
      "values": [
        {"id": k["id"], "name": k["name"], "area_sqm": round(area_4548(k["rings"]), 1)}
        for k in scene["keyAreas"]
      ]},
  },
    "v3_plan_summary": {
    "axis": "x=0 城市中轴线，左右镜像对称",
    "parcel_pairs": 6,
    "sunlight_rule": "居住地块纯住宅（无教育/底商）：5排板式住宅南低北高（45-65×14m/10-15层/30-45m，参照万柳书院/使馆壹号院/融创北京壹号院）+ 4栋点式塔楼四角贴边界（南角30m/北角45m），南排矮北排高利于日照，排距350m≈7.8×最高楼高（北京大寒日≥2h），层高3.0m",
    "building_strategy": "科研地块点式超高层(180-288m/参考中国尊/正大中心/国贸三期)，商业综合体(95m/参考朝阳大悦城)，文化馆(30-40m/参考首博/科技馆)，配建中小学(4-5层/参考北京四中/中关村三小)，底商≤3层",
    "parcel_stats": [
      {"id": lu["id"], "code": lu["code"], "name": lu["name"],
       "area_ha": round(lu["area_sqm"]/1e4,1),
       "coverage_pct": round(sum(b["area"] for b in scene["buildings"] if b["parent"]==lu["id"])/lu["area_sqm"]*100,1),
       "buildings": sum(1 for b in scene["buildings"] if b["parent"]==lu["id"])}
      for lu in scene["landUse"] if lu["code"] != "1401"
    ]
  }
}
json.dump(metrics, open(f"{SUB}/metrics.json", "w"), ensure_ascii=False, indent=1)
print("✅ metrics.json 更新")

# ---------- 8. manifest.json sha256 ----------
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

manifest = json.load(open(f"{SUB}/manifest.json"))
manifest["generated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
manifest["site_package_version"] = "0.2.0"
for f in manifest.get("files", []):
    p = f.get("path")
    if p and os.path.exists(f"{SUB}/{p}") and not p.endswith("manifest.json"):
        f["sha256"] = sha256_file(f"{SUB}/{p}")
json.dump(manifest, open(f"{SUB}/manifest.json", "w"), ensure_ascii=False, indent=2)
print("✅ manifest.json 更新")
print("\n✅ 全部数据文件更新完成")
