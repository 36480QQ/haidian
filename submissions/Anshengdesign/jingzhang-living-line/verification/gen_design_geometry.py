# -*- coding: utf-8 -*-
"""设计几何生成器（KUN-SAL 京张参赛）
方法：网格裁剪分区（拓扑安全：共享边、无缝隙、无重叠，全在边界内）
- 用地分区 = 400m 网格 × 站点边界裁剪，按（重点区/走廊距离/水系距离/站点锚点）规则赋类
- 设计道路 = 网格线（次干/支路）+ 走廊绿道 + 断点缝合 + 站点接驳
- 建筑 = 可建设单元格内规则布局基底（概念体量，低置信度）
- 绿地 = 走廊缓冲 + 水系缓冲 + 公园单元格 + OSM 现状公园
- 公共空间 = 轨道站/关键节点广场 + 荣誉展示节点
- 分期 = 三期（走廊缝合+大钟寺 / 原点社区 / 众智园）
- 约束 = 现状主干路 + 水系 + 遗址走廊（locked，仅作 constraint 表达）
输出：design_geometry/*.geojson（EPSG:4326；area_sqm_declared 用 EPSG:4548 复算）
"""
import os, json, math, pickle
import numpy as np
import pyproj
from shapely.geometry import (Polygon, LineString, Point, MultiLineString, mapping,
                              box, MultiPolygon)
from shapely.ops import unary_union, transform as sh_transform, linemerge
from shapely.affinity import translate

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "design_geometry")
os.makedirs(OUT, exist_ok=True)

TRANS = pyproj.Transformer.from_crs(pyproj.CRS.from_epsg(4326), pyproj.CRS.from_epsg(4548), always_xy=True)
INV = pyproj.Transformer.from_crs(pyproj.CRS.from_epsg(4548), pyproj.CRS.from_epsg(4326), always_xy=True)

def to_m(g):
    def pr(x, y, z=None):
        a, b = TRANS.transform(x, y)
        return (a, b)
    return sh_transform(pr, g)

def to_ll(g):
    def pr(x, y, z=None):
        a, b = INV.transform(x, y)
        return (a, b)
    return sh_transform(pr, g)

def area_m2(g):
    return round(to_m(g).area, 1)

model = pickle.load(open(os.path.join(HERE, "site_model.pkl"), "rb"))
site = model["site"]
keys = model["key_geoms"]
corridor = model["corridor"]
layers = model["layers"]

# ---------- 约束提取 ----------
major_roads = []
for e, g in layers["roads"]:
    hw = e.get("tags", {}).get("highway")
    if hw in ("motorway", "trunk", "primary") and g.geom_type == "LineString":
        major_roads.append((e.get("tags", {}).get("name", ""), g))
water_lines = [g for e, g in layers["water"] if e.get("tags", {}).get("name") and g.geom_type == "LineString"]
water_polys = [g for e, g in layers["water"] if e.get("tags", {}).get("name") and g.geom_type in ("Polygon", "MultiPolygon")]

# ---------- 用地分区（400m 网格裁剪）----------
CELL = 400.0
bounds = to_m(site).bounds
cols = int((bounds[2] - bounds[0]) / CELL) + 2
rows = int((bounds[3] - bounds[1]) / CELL) + 2
cells = []
grid_lines_v = []; grid_lines_h = []
for i in range(cols + 1):
    x = bounds[0] + i * CELL
    grid_lines_v.append(LineString([(x, bounds[1]), (x, bounds[3])]))
for j in range(rows + 1):
    y = bounds[1] + j * CELL
    grid_lines_h.append(LineString([(bounds[0], y), (bounds[2], y)]))

site_m = to_m(site)
for i in range(cols):
    for j in range(rows):
        x0 = bounds[0] + i * CELL; x1 = x0 + CELL
        y0 = bounds[1] + j * CELL; y1 = y0 + CELL
        c = box(x0, y0, x1, y1).intersection(site_m)
        if c.is_empty:
            continue
        if c.geom_type == "Polygon":
            cells.append(c)
        elif c.geom_type == "MultiPolygon":
            cells.extend(list(c.geoms))
        else:
            cells.append(c)

# 关键锚点（米制）
def anchor_m(lon, lat):
    x, y = TRANS.transform(lon, lat)
    return Point(x, y)

corridor_m = to_m(corridor)
key_m = {k: to_m(v) for k, v in keys.items()}
water_union_m = to_m(unary_union(water_lines + water_polys)) if (water_lines or water_polys) else None

station_anchors = {
    "STA-WUDAOKOU": anchor_m(116.3317, 39.9915),
    "STA-DAZHONGSI": anchor_m(116.3390, 39.9653),
    "STA-ZHICHUNLU": anchor_m(116.3344, 39.9751),
    "STA-QHDXK": anchor_m(116.3336, 39.9993),
    "STA-XUEYUANQIAO": anchor_m(116.3473, 39.9868),
    "STA-XUEZHIYUAN": anchor_m(116.3458, 40.0136),
    "STA-BEIJINGBEI": anchor_m(116.3462, 39.9459),
}

# ---------- POI 证据（高德 12 类，WGS84；用于自下而上的用地特征识别） ----------
POI_DIR = os.path.join(HERE, "poi_wgs84")
poi_cat_map = {
    "company": "work", "research": "work", "finance": "work",
    "dining": "life", "shopping": "life", "living": "life", "sports": "life",
    "medical": "medical", "school": "education", "residential": "residential",
    "scenic": "scenic", "transport": "transport",
}
poi_pts_m = {}
for slug in poi_cat_map:
    fp = os.path.join(POI_DIR, f"{slug}.json")
    if os.path.exists(fp):
        d = json.load(open(fp))
        poi_pts_m[slug] = [to_m(Point(p["lon_wgs"], p["lat_wgs"])) for p in d]
def cell_poi_signature(cell):
    """单元格内 POI 主导特征（现状特征，自下而上）"""
    sig = {}
    for slug, kind in poi_cat_map.items():
        n = sum(1 for p in poi_pts_m.get(slug, []) if cell.contains(p))
        sig[kind] = sig.get(kind, 0) + n
    total = sum(sig.values())
    if total < 5:
        return None, total
    dom = max(sig.items(), key=lambda kv: kv[1])
    return dom[0], total
POI_TO_LU = {"work": ("0802", "科研用地(现状企业特征)"),
             "life": ("05", "商业服务业用地(现状生活特征)"),
             "medical": ("0806", "医疗卫生用地(现状特征)"),
             "education": ("0804", "教育科研用地(现状特征)"),
             "residential": ("0701", "城镇住宅用地(现状特征)"),
             "scenic": ("1401", "公园绿地(现状特征)"),
             "transport": ("05", "商业服务业用地(枢纽特征)")}


def classify(cell):
    """按位置/关系赋用地代码（概念分区，非控规）；绿地判定用质心距离避免整格变绿"""
    c = cell.centroid
    d_corr = c.distance(corridor_m) if corridor_m else 1e9
    d_water = c.distance(water_union_m) if water_union_m else 1e9
    d_sta = min(p.distance(c) for p in station_anchors.values())
    in_key = [k for k, g in key_m.items() if cell.intersects(g)]
    # 绿地优先（窄带：遗址公园主脊 ≈ 真实公园宽度 + 滨水窄带）
    if d_water < 40 or (corridor_m and d_corr < 50):
        return "1401", "公园绿地"
    # 站域 300m → 商业/公共服务
    if d_sta < 300:
        return "05", "商业服务业用地"
    if in_key:
        k = in_key[0]
        if k == "PROV-KEY-001":   # 众智园
            return "0802", "科研用地(AI研发)"
        if k == "PROV-KEY-002":   # 原点社区
            if d_corr < 420 and d_sta < 700:
                return "0802", "科研用地(成果转化)"
            return "0804", "教育科研用地"
        if k == "PROV-KEY-003":   # 大钟寺
            if d_sta < 700:
                return "05", "商业服务业用地"
            return "0802", "科研用地(AI原生)"
    # 带内其余：优先保留 POI 现状特征（自下而上涌现），仅走廊/站域做更新干预
    if d_corr < 500:
        return "0802", "科研用地(创新廊)"
    if d_sta < 900:
        return "0701", "城镇住宅用地(职住平衡)"
    sig, npoi = cell_poi_signature(cell)
    if sig is not None:
        code, zh = POI_TO_LU[sig]
        return code, zh + f"(POI主导,{npoi}点)"
    return "0701", "城镇住宅用地"

land_use_feats = []
for i, c in enumerate(cells):
    code, zh = classify(c)
    poly = to_ll(c)
    land_use_feats.append({
        "type": "Feature", "id": f"LU-{i+1:03d}",
        "properties": {
            "id": f"LU-{i+1:03d}", "layer": "LAND_USE", "land_use_code": code,
            "name_zh": zh, "source_type": "agent_generated_design",
            "confidence": "medium", "geometry_role": "design_proposal",
            "area_sqm_declared": area_m2(poly),
        },
        "geometry": mapping(poly),
    })

# ---------- 设计道路 ----------
road_feats = []
rid = 0
def add_road(g, cls, name, role="design_proposal", src="agent_generated_design"):
    global rid
    rid += 1
    if g.is_empty:
        return
    road_feats.append({
        "type": "Feature", "id": f"ROAD-{rid:03d}",
        "properties": {
            "id": f"ROAD-{rid:03d}", "layer": "ROAD_CENTERLINE", "road_class": cls,
            "name_zh": name, "source_type": src, "confidence": "medium",
            "geometry_role": role,
        },
        "geometry": mapping(g),
    })

# 网格线 → 次干/支路（裁剪到场地内）
for idx, l in enumerate(grid_lines_v + grid_lines_h):
    seg = l.intersection(site_m)
    if seg.is_empty:
        continue
    if seg.geom_type == "Point":
        continue
    if seg.geom_type == "GeometryCollection":
        parts = [g for g in seg.geoms if g.geom_type == "LineString"]
    elif seg.geom_type == "LineString":
        parts = [seg]
    else:
        parts = list(seg.geoms)
    for p in parts:
        if p.geom_type == "LineString" and p.length > 60:
            add_road(to_ll(p), "secondary" if idx < len(grid_lines_v) else "branch",
                     "设计次干路" if idx < len(grid_lines_v) else "设计支路")
# 走廊绿道（主脊）
if corridor_m is not None:
    add_road(to_ll(corridor_m), "greenway", "京张遗址公园慢行主脊", src="agent_inferred_from_public_data", role="design_proposal")
# 断点缝合（7 处道路交叉点 E-W 连接）
for sx, sy in [(116.33151, 39.99924), (116.3318, 39.99151), (116.33241, 39.98487),
               (116.33409, 39.97504), (116.3391, 39.9662), (116.3419, 39.95682), (116.34291, 39.94318)]:
    mx, my = TRANS.transform(sx, sy)
    add_road(to_ll(LineString([(mx - 160, my), (mx + 160, my)])), "pedestrian", "断点缝合步道（概念）")
# 站点接驳（站到走廊/最近网格线）
for sid, p in station_anchors.items():
    d = corridor_m.distance(p)
    if d < 900:
        pp = corridor_m.interpolate(corridor_m.project(p))
        add_road(to_ll(LineString([p, pp])), "transit_connection", f"{sid} 接驳支路（概念）")

# ---------- 建筑基底（概念体量，规则布局）----------
bldg_feats = []
bid = 0
def add_bldg(poly, btype, zh):
    global bid
    bid += 1
    bldg_feats.append({
        "type": "Feature", "id": f"BLDG-{bid:03d}",
        "properties": {
            "id": f"BLDG-{bid:03d}", "layer": "BUILDING_FOOTPRINT", "building_type": btype,
            "name_zh": zh, "source_type": "agent_generated_design",
            "confidence": "low", "geometry_role": "design_proposal",
            "area_sqm_declared": area_m2(poly),
            "note_zh": "概念体量示意，非建筑方案或拆改留结论",
        },
        "geometry": mapping(poly),
    })

rng = np.random.default_rng(11)
for i, c in enumerate(cells):
    code = classify(c)[0]
    if code in ("1401", "16"):
        continue   # 绿地/留白不放基底
    # 单元内 10-12 栋概念体量（基底密度约 15-20%）
    n = 10 if c.area < 120000 else 12
    placed = 0
    bx0, by0, bx1, by1 = c.bounds
    if (bx1 - bx0) < 120 or (by1 - by0) < 100:
        continue
    placed_polys = []
    for _ in range(n * 4):
        if placed >= n:
            break
        w = rng.uniform(45, 90); h = rng.uniform(28, 50)
        cx = rng.uniform(bx0 + 35, bx1 - 35)
        cy = rng.uniform(by0 + 30, by1 - 30)
        p = box(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
        if not c.contains(p):
            continue
        # 拒绝重叠（空间审查用 union 计面积，重叠会被并掉）
        if any(p.intersects(q) for q in placed_polys):
            continue
        # 避开公园主脊/滨水绿带（概念退让）
        if (corridor_m is not None and p.intersects(corridor_m.buffer(75))) or \
           (water_union_m is not None and p.intersects(water_union_m.buffer(45))):
            continue
        placed_polys.append(p)
        # 类型按用地
        btype = {"0802": "ai_r_and_d", "0804": "education", "0701": "residential",
                 "05": "mixed_use"}.get(code, "mixed_use")
        add_bldg(to_ll(p), btype, {"0802": "AI研发概念体量", "0804": "教育科研概念体量",
                                   "0701": "职住社区概念体量"}.get(btype, "混合功能概念体量"))
        placed += 1

# ---------- 绿地 ----------
green_feats = []
gid = 0
def add_green(poly, zh, role="design_proposal", src="agent_generated_design", code="1401"):
    global gid
    gid += 1
    if poly.is_empty:
        return
    if poly.geom_type not in ("Polygon", "MultiPolygon"):
        return
    green_feats.append({
        "type": "Feature", "id": f"GREEN-{gid:03d}",
        "properties": {
            "id": f"GREEN-{gid:03d}", "layer": "GREEN_SPACE", "land_use_code": code,
            "name_zh": zh, "source_type": src, "confidence": "medium",
            "geometry_role": role, "area_sqm_declared": area_m2(poly),
        },
        "geometry": mapping(poly),
    })

# 走廊缓冲 60m 主脊绿地
if corridor_m is not None:
    add_green(to_ll(corridor_m.buffer(60).intersection(site_m)), "京张遗址公园活力带绿地（概念）")
# 水系缓冲 30m（清河/小月河等有名称河流）
if water_union_m is not None:
    for wg in ([water_union_m] if water_union_m.geom_type in ("Polygon", "MultiPolygon") else list(water_union_m.geoms)):
        add_green(to_ll(wg.buffer(30).intersection(site_m)), "滨水绿带（概念）", src="agent_inferred_from_public_data")
# 用地分区中的公园绿地块（质心远离主脊的绿地单元）
for i, c in enumerate(cells):
    if classify(c)[0] == "1401" and c.centroid.distance(corridor_m) > 50:
        add_green(to_ll(c), "社区公园（概念）")
# OSM 现状公园（现有条件）
for e, g in layers["green"]:
    if g.geom_type in ("Polygon", "MultiPolygon"):
        t = e.get("tags", {})
        nm = t.get("name", "")
        if nm:
            gi = g.intersection(site)
            if not gi.is_empty:
                add_green(gi, f"{nm}（现状）", role="existing_condition", src="osm")

# ---------- 公共空间 ----------
pub_feats = []
pid = 0
# 广场节点沿走廊交叉点（东移 20-40m 保持在临时边界内）+ 重点区中心 + 主脊沿线
pub_nodes = [
    ("清华东路·北门户广场（概念）", 116.3326, 39.9992, "station_plaza"),
    ("五道口·相变广场（概念）", 116.3330, 39.9915, "station_plaza"),
    ("北四环·上跨缝合广场（概念）", 116.3335, 39.9849, "station_plaza"),
    ("知春路·换乘广场（概念）", 116.3352, 39.9750, "station_plaza"),
    ("北三环·上跨缝合广场（概念）", 116.3402, 39.9662, "station_plaza"),
    ("大钟寺·涌现界面广场（概念）", 116.3402, 39.9646, "station_plaza"),
    ("学院南路·南门户广场（概念）", 116.3430, 39.9568, "station_plaza"),
    ("众智园·花园交往广场（概念）", 116.3485, 40.0167, "district_center"),
    ("原点社区·策源广场（概念）", 116.3475, 39.9885, "district_center"),
    ("清华园车站遗址·原点广场（概念）", 116.3430, 39.9850, "heritage_node"),
    ("主脊中段·开发者步道广场（概念）", 116.3368, 39.9928, "linear_node"),
    ("主脊南段·开源成果展示广场（概念）", 116.3416, 39.9615, "linear_node"),
]
for zh, lon, lat, kind in pub_nodes:
    x, y = TRANS.transform(lon, lat)
    size = 200 if kind in ("station_plaza", "linear_node") else 160
    p = box(x - size / 2, y - size / 2, x + size / 2, y + size / 2).intersection(site_m)
    if p.is_empty:
        continue
    a = p.area
    if not math.isfinite(a) or a < 2000:
        continue
    pid += 1
    pub_feats.append({
        "type": "Feature", "id": f"PUBLIC-{pid:03d}",
        "properties": {
            "id": f"PUBLIC-{pid:03d}", "layer": "PUBLIC_SPACE", "name_zh": zh,
            "kind": kind, "source_type": "agent_generated_design",
            "confidence": "medium", "geometry_role": "design_proposal",
            "area_sqm_declared": round(p.area, 1),
        },
        "geometry": mapping(to_ll(p)),
    })

# ---------- 分期 ----------
phase_defs = [
    ("PHASE-1", "近期：主脊缝合与大钟寺界面（概念）", ["PROV-KEY-003"], 0),
    ("PHASE-2", "中期：原点社区更新（概念）", ["PROV-KEY-002"], 1),
    ("PHASE-3", "远期：众智园花园街区（概念）", ["PROV-KEY-001"], 2),
]
phase_feats = []
for ph_id, zh, kset, idx in phase_defs:
    area = unary_union([key_m[k] for k in kset])
    # 主脊缝合带并入一期
    if idx == 0 and corridor_m is not None:
        area = unary_union([area, corridor_m.buffer(150)])
    clipped = area.intersection(site_m)
    if clipped.is_empty:
        continue
    phase_feats.append({
        "type": "Feature", "id": ph_id,
        "properties": {
            "id": ph_id, "layer": "PHASE", "phase": f"phase_{idx+1}",
            "name_zh": zh, "source_type": "agent_generated_design",
            "confidence": "medium", "geometry_role": "design_proposal",
            "area_sqm_declared": round(clipped.area, 1),
            "note_zh": "分期为概念建议，非开发时序或审批结论",
        },
        "geometry": mapping(to_ll(clipped)),
    })

# ---------- 约束（locked 表达）----------
constraint_feats = []
cid = 0
def add_constraint(g, layer, name, src, cls=None):
    global cid
    cid += 1
    if g.is_empty:
        return
    props = {
        "id": f"CON-{cid:03d}", "layer": layer, "name_zh": name,
        "source_type": src, "confidence": "medium",
        "geometry_role": "existing_condition",
    }
    if cls:
        props["road_class"] = cls
    constraint_feats.append({"type": "Feature", "id": f"CON-{cid:03d}",
                             "properties": props, "geometry": mapping(g)})

for nm, g in major_roads:
    gi = g.intersection(site)
    if not gi.is_empty:
        add_constraint(gi, "EXISTING_PRIMARY_ROAD", f"{nm or '主干路'}（现状，OSM）", "osm")
if water_union_m is not None:
    add_constraint(to_ll(water_union_m.intersection(site_m)), "EXISTING_WATER", "清河/小月河等现状水系（OSM）", "osm")
if corridor_m is not None:
    add_constraint(to_ll(corridor_m), "EXISTING_RAIL", "京张铁路遗址走廊（推导参考轴线）", "agent_inferred_from_public_data")

# ---------- site_boundary / key_areas（provisional 复制）----------
def wf(fid, props, geom):
    return {"type": "Feature", "id": fid, "properties": props, "geometry": mapping(geom)}

site_feat = wf("SITE-001", {
    "id": "SITE-001", "layer": "SITE_BOUNDARY", "scope_id": "overall_design_area",
    "name_zh": "总体设计范围（临时粗略替代边界）",
    "source_type": "agent_inferred_from_public_data", "confidence": "medium",
    "geometry_role": "provisional_constraint", "official_boundary": False,
    "boundary_precision": "provisional_rough",
    "area_sqm_declared": 11400000, "area_sqm_calculated": round(to_m(site).area, 1),
    "source_id": "DATA-SRC-PROVISIONAL-BOUNDARIES-20260605",
    "usage_note": "临时粗略边界，仅用于生成、展示与自检；非官方红线、非精确面积依据",
}, site)

key_area_info = {
    "PROV-KEY-001": ("KEY-001", "zhongzhiyuan_ai_acceleration_area", "众智园AI自主创新加速区（临时粗略范围）", 1921000),
    "PROV-KEY-002": ("KEY-002", "beijing_ai_origin_community", "北京AI原点社区（临时粗略范围）", 1043000),
    "PROV-KEY-003": ("KEY-003", "dazhongsi_ai_industry_cluster", "大钟寺AI产业集聚区（临时粗略范围）", 720000),
}
key_feats = []
for src_id, (fid, area_id, zh, ann) in key_area_info.items():
    g = keys[src_id]
    key_feats.append(wf(fid, {
        "id": fid, "layer": "KEY_AREA", "area_id": area_id, "name_zh": zh,
        "parent_scope_id": "key_detailed_design_area",
        "source_type": "agent_inferred_from_public_data", "confidence": "medium",
        "geometry_role": "provisional_constraint", "official_boundary": False,
        "boundary_precision": "provisional_rough",
        "announced_area_sqm": ann, "area_sqm_calculated": round(to_m(g).area, 1),
        "source_id": "DATA-SRC-PROVISIONAL-BOUNDARIES-20260605",
        "usage_note": "临时粗略范围，仅用于生成、展示与自检",
    }, g))

def write_fc(name, feats):
    path = os.path.join(OUT, f"{name}.geojson")
    json.dump({"type": "FeatureCollection", "name": name, "features": feats},
              open(path, "w"), ensure_ascii=False, indent=1)
    print(f"{name}: {len(feats)} features")

write_fc("site_boundary", [site_feat])
write_fc("key_areas", key_feats)
write_fc("land_use", land_use_feats)
write_fc("roads", road_feats)
write_fc("buildings", bldg_feats)
write_fc("green_space", green_feats)
write_fc("public_space", pub_feats)
write_fc("phasing", phase_feats)
write_fc("constraints", constraint_feats)

# ---------- 指标复算（union 口径，与官方 spatial_review 一致） ----------
from shapely.geometry import shape as _shape
def union_area(feats):
    geoms = [to_m(_shape(f["geometry"])) for f in feats]
    u = unary_union(geoms)
    return float(u.area) if u is not None and not u.is_empty else 0.0
lu_areas = {}
for f in land_use_feats:
    code = f["properties"]["land_use_code"]
    lu_areas[code] = lu_areas.get(code, 0) + f["properties"]["area_sqm_declared"]
green_area = union_area(green_feats)
pub_area = union_area(pub_feats)
bldg_area = union_area(bldg_feats)
road_len = 0.0
for f in road_feats:
    g = to_m(_shape(f["geometry"]))
    road_len += g.length
site_area = round(to_m(site).area, 1)
metrics = {
    "site_area_sqm": site_area,
    "land_use_area_by_code_sqm": lu_areas,
    "green_area_sqm": green_area,
    "green_ratio": round(green_area / site_area, 4),
    "public_space_area_sqm": pub_area,
    "public_space_ratio": round(pub_area / site_area, 4),
    "building_footprint_area_sqm": bldg_area,
    "building_density": round(bldg_area / site_area, 4),
    "road_centerline_length_m": round(road_len, 0),
    "n_buildings": len(bldg_feats),
    "n_land_use_polygons": len(land_use_feats),
}
json.dump(metrics, open(os.path.join(OUT, "design_metrics.json"), "w"), ensure_ascii=False, indent=2)
print(json.dumps(metrics, ensure_ascii=False, indent=1))
