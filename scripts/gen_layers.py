#!/usr/bin/env python3
"""
京张智脉 — 图层生成脚本 Part 2：buildings / roads / green_space / public_space / phasing / constraints
"""
import json
from shapely.geometry import shape, mapping, Polygon, LineString, Point, box
from shapely.ops import unary_union, split
from pyproj import Transformer

SUB = "submissions/xusu-ai/jingzhang-ai-vein"
GEOM = f"{SUB}/geometry"

to_4548 = Transformer.from_crs("EPSG:4326", "EPSG:4548", always_xy=True)

def area_sqm(poly_geom):
    coords = list(poly_geom.exterior.coords)
    projected = [to_4548.transform(x, y) for x, y in coords]
    return abs(Polygon(projected).area)

def feat(fid, layer, geom, extra=None, source_type="agent_design_proposal", confidence="medium", role="design_proposal"):
    props = {
        "id": fid, "layer": layer, "source_type": source_type,
        "confidence": confidence, "geometry_role": role,
    }
    if extra:
        props.update(extra)
    if geom.geom_type in ("Polygon",):
        props["area_sqm_declared"] = round(area_sqm(geom), 1)
    return {"type": "Feature", "id": fid, "properties": props, "geometry": mapping(geom)}

site = shape(json.load(open(f"{GEOM}/site_boundary.geojson"))["features"][0]["geometry"])
minx, miny, maxx, maxy = site.bounds
lu_fc = json.load(open(f"{GEOM}/land_use.geojson"))
lu_polys = {f["id"]: shape(f["geometry"]) for f in lu_fc["features"]}

# 找出非公园用地的可建设用地（科研/商业/文化/居住）
buildable = [k for k, v in lu_polys.items() if "1401" not in json.dumps(
    [p["properties"] for p in lu_fc["features"] if p["id"] == k][0].get("land_use_code", ""))]
buildable_ids = [k for k, v in lu_polys.items()]
land_use_by_id = {f["id"]: f["properties"]["land_use_code"] for f in lu_fc["features"]}

# ============ BUILDINGS ============
# 在可建设地块内生成建筑轮廓（用网格剖分，保证在用地内、不重叠）
buildings = []
b_id = 0
for fid, poly in lu_polys.items():
    code = land_use_by_id[fid]
    if code == "1401":  # 公园绿地不放建筑
        continue
    b_minx, b_miny, b_maxx, b_maxy = poly.bounds
    # 依据用地类型决定建筑密度
    if code in ("0802", "0803"):  # 科研/文化 — 中等密度
        n_cells = 6
        cell_w = (b_maxx - b_minx) / 3
        cell_h = (b_maxy - b_miny) / 2
        btype = "ai_r_and_d" if code == "0802" else "education"
    elif code == "05":  # 商业 — 较高密度
        n_cells = 9
        cell_w = (b_maxx - b_minx) / 3
        cell_h = (b_maxy - b_miny) / 3
        btype = "mixed_use"
    else:  # 居住
        n_cells = 6
        cell_w = (b_maxx - b_minx) / 3
        cell_h = (b_maxy - b_miny) / 2
        btype = "residential"
    for i in range(3):
        for j in range(2 if code in ("0802", "0803", "0701") else 3):
            cx = b_minx + cell_w * (i + 0.5)
            cy = b_miny + cell_h * (j + 0.5)
            w = cell_w * 0.55
            h = cell_h * 0.55
            b = box(cx - w/2, cy - h/2, cx + w/2, cy + h/2)
            b = b.intersection(poly)
            if b.is_empty or b.geom_type != "Polygon":
                continue
            if b.area < (cell_w * cell_h) * 0.15:
                continue
            b_id += 1
            buildings.append(feat(f"B-{b_id:03d}", "BUILDING_FOOTPRINT", b, extra={
                "building_type": btype,
                "land_use_parent": fid,
                "height_m_concept": 24 if code in ("0802",) else (36 if code == "05" else 18),
                "floors_concept": 6 if code in ("0802",) else (10 if code == "05" else 5),
                "status_concept": "retain_renovate" if code == "0701" else "new_build",
            }))
print(f"✅ buildings: {len(buildings)}")

# ============ ROADS ============
# 南北主干道（沿公园带西缘）+ 东西向连接路（每段中心）
roads = []
# 纵向骨架：沿 park 带西缘
road_west_x = minx + (maxx - minx) * 0.34
road_east_x = minx + (maxx - minx) * 0.64
# 南北贯通慢行主廊（京张遗址公园内）
spine_pts = [(road_west_x + (maxx - minx)*0.02, miny + 0.0005),
             (road_west_x + (maxx - minx)*0.01, (miny+maxy)/2),
             (road_west_x + (maxx - minx)*0.015, maxy - 0.0005)]
spine = LineString([(road_west_x, miny), (road_west_x, maxy)])
roads.append(feat("RD-001", "ROAD_CENTERLINE", spine, extra={
    "road_class": "arterial", "road_class_label": "主干路", "name_zh": "智脉纵轴",
    "status": "concept_proposal"}))

# 横向连接路（每段中心线）
seg_y = [(miny+39.955)/2, (39.955+39.9775)/2, (39.9775+40.005)/2, (40.005+maxy)/2]
for i, yy in enumerate(seg_y):
    y = miny + (maxy - miny) * (i + 1) / 5
    line = LineString([(minx, y), (maxx, y)])
    roads.append(feat(f"RD-{i+2:03d}", "ROAD_CENTERLINE", line, extra={
        "road_class": "collector" if i % 2 else "local", "name_zh": f"智脉横轴{i+1}",
        "status": "concept_proposal"}))
# 东侧次级纵路
roads.append(feat("RD-006", "ROAD_CENTERLINE", LineString([(road_east_x, miny), (road_east_x, maxy)]), extra={
    "road_class": "collector", "name_zh": "小月河翼纵路", "status": "concept_proposal"}))
print(f"✅ roads: {len(roads)}")

# ============ GREEN_SPACE ============
# 公园带内部绿地多边形（从 land_use 1401 提取，再细分出广场）
green = []
for fid, poly in lu_polys.items():
    if land_use_by_id[fid] == "1401":
        green.append(feat(f"GS-{len(green)+1:03d}", "GREEN_SPACE", poly, extra={
            "green_type": "park", "label_zh": "京张遗址公园", "parent_land_use": fid}))
print(f"✅ green_space: {len(green)}")

# ============ PUBLIC_SPACE ============
# 每段中心放一个广场节点（在三区核心）
public = []
key_areas = json.load(open(f"{GEOM}/key_areas.geojson"))
for ka in key_areas["features"]:
    kp = shape(ka["geometry"])
    c = kp.centroid
    ps = box(c.x - 0.0008, c.y - 0.0008, c.x + 0.0008, c.y + 0.0008).intersection(site)
    public.append(feat(f"PS-{len(public)+1:03d}", "PUBLIC_SPACE", ps, extra={
        "space_type": "civic_plaza", "label_zh": f"{ka['properties'].get('name_zh','重点区')}核心广场"}))
# 公园带内再加 2 个线型广场
for i, yy in enumerate([0.4, 0.75]):
    y = miny + (maxy - miny) * yy
    ps = box(park_lo := minx+(maxx-minx)*0.36, y-0.0006, park_hi := minx+(maxx-minx)*0.36+(maxx-minx)*0.22, y+0.0006).intersection(site)
    if not ps.is_empty:
        public.append(feat(f"PS-{len(public)+1:03d}", "PUBLIC_SPACE", ps, extra={
            "space_type": "linear_plaza", "label_zh": "遗址公园活力广场"}))
print(f"✅ public_space: {len(public)}")

# ============ PHASING ============
# 分期：近期(北段众智园) / 中期(中段原点社区) / 远期(南段大钟寺+东翼)
phases = [
    ("PH-001", "phase1_near", "近期（2026-2028）", 39.995, maxy, "北段众智园先行启动"),
    ("PH-002", "phase2_mid", "中期（2029-2031）", 39.960, 39.995, "中段AI原点社区更新"),
    ("PH-003", "phase3_far", "远期（2032-2035）", miny, 39.960, "南段大钟寺+东翼联动"),
]
phasing = []
for fid, pcode, plabel, lo, hi, note in phases:
    poly = site.intersection(box(minx, lo, maxx, hi))
    if poly.is_empty or poly.geom_type != "Polygon":
        # 取最大部件
        if poly.geom_type == "MultiPolygon":
            poly = max(poly.geoms, key=lambda g: g.area)
        else:
            continue
    phasing.append(feat(fid, "PHASE", poly, extra={
        "phase_code": pcode, "label_zh": plabel, "phase_note": note}))
print(f"✅ phasing: {len(phasing)}")

# ============ CONSTRAINTS ============
# 京张铁路遗址带作为文化保护廊道约束（概念标注，非官方红线）
constraints = []
rail_y = [miny + (maxy - miny) * 0.5]
rail_line = LineString([(minx+(maxx-minx)*0.36, miny), (minx+(maxx-minx)*0.38, maxy)])
constraints.append(feat("CS-001", "HERITAGE_PROTECTION", rail_line.buffer((maxx-minx)*0.06), extra={
    "constraint_type": "heritage_corridor_concept", "label_zh": "京张铁路遗址文化廊道（概念示意）",
    "official": False, "note": "非官方文保范围，仅概念性表达"}))
print(f"✅ constraints: {len(constraints)}")

# ============ 写文件 ============
for name, feats in [("buildings", buildings), ("roads", roads), ("green_space", green),
                    ("public_space", public), ("phasing", phasing), ("constraints", constraints)]:
    fc = {"type": "FeatureCollection", "features": feats}
    with open(f"{GEOM}/{name}.geojson", "w") as f:
        json.dump(fc, f, ensure_ascii=False)
    print(f"✅ {name}.geojson: {len(feats)} features")
