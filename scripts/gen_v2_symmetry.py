#!/usr/bin/env python3
"""
京张智脉 V2 — 中轴对称重划方案生成脚本（v4，自检合规版）
关键修复：
1. 地块/建筑裁剪到场地内（SITE_POLY intersection）——消除 GEOMETRY_OUTSIDE_SITE
2. source_type = agent_generated_design（官方 schema）
3. FAR ≤ 1.0：降低建筑层数/覆盖率
4. 面积用 EPSG:4548 投影计算（DECLARED_AREA_MISMATCH 修复）
5. 对称设计矩形保留在 design_rect 字段（设计意图），几何跟随场地
"""
import json, math
from shapely.geometry import Polygon, box
from pyproj import Transformer

OUT = "/tmp/scene_v2.json"
to_4548 = Transformer.from_crs("EPSG:4326", "EPSG:4548", always_xy=True)

# ============ 1. 场地 ============
SITE_RINGS = [[-584.3213683998594,-4857.095687500316],[670.2509814002696,-4857.095687500316],[670.2509814002696,-1970.5931074999432],[498.39175540067015,804.8901424998991],[670.2509814002696,4857.095687499526],[-412.46214240025984,4857.095687499526],[-498.391755399449,2581.1994224997034],[-670.2509814002696,-860.3998075001641],[-584.3213683998594,-4857.095687500316]]
SITE_W, SITE_H = 1340.5, 9714.19
SITE_POLY = Polygon(SITE_RINGS)

# 坐标转换（本地 → WGS84）
A_LON, B_LON = 0.0000116374, 116.3475
C_LAT, D_LAT = 0.0000090074, 39.98275

def area_sqm_4548(ring):
    """本地坐标 ring → WGS84 → EPSG:4548 投影面积"""
    wgs = [[A_LON*p[0]+B_LON, C_LAT*p[1]+D_LAT] for p in ring]
    proj = [to_4548.transform(x, y) for x, y in wgs]
    return abs(Polygon(proj).area)

SITE_AREA = area_sqm_4548(SITE_RINGS)
print(f"场地面积(EPSG:4548): {SITE_AREA/1e4:.1f} ha")

def poly_ring(poly, shrink=0.0):
    if shrink > 0:
        poly = poly.buffer(-shrink)  # 微收缩消除边界贴合浮点误差
    coords = list(poly.exterior.coords)
    return [[round(x,9), round(y,9)] for x, y in coords]

# ============ 2. 地块（设计矩形 ∩ 场地，对称）============
AXIS = 0.0; PARK_HALF = 110.0; WING_IN = 110.0; WING_OUT = 671.0

def mk_parcel(pid, code, color, name, label, x0, x1, y0, y1, axis_gap=0.0):
    # axis_gap>0 时在中轴侧内缩（消除与公园共享边重叠）
    if axis_gap > 0 and x1 <= 0:
        x1 -= axis_gap   # 西翼右边界向左缩（远离中轴）
    elif axis_gap > 0 and x0 >= 0:
        x0 += axis_gap   # 东翼左边界向右缩（远离中轴）
    design = box(x0, y0, x1, y1)
    poly = design.intersection(SITE_POLY)
    if poly.is_empty or poly.geom_type != "Polygon":
        return None
    ring = poly_ring(poly, 0.0)
    area = area_sqm_4548(ring)
    return {"id": pid, "code": code, "color": color, "name": name, "label": label,
            "rings": ring, "area_sqm": round(area,1),
            "area_ratio": round(area/SITE_AREA*100, 1),
            "design_rect": [x0, x1, y0, y1]}

parcels = []
parcels.append(mk_parcel("LU-001","0802","#2E5BFF","科研用地","科研用地（AI自主创新加速·西翼）",-WING_OUT,-WING_IN,3238,4857.5,1.0))
parcels.append(mk_parcel("LU-002","0802","#2E5BFF","科研用地","科研用地（AI自主创新加速·东翼）",WING_IN,WING_OUT,3238,4857.5,1.0))
parcels.append(mk_parcel("LU-003","0803","#7B5BFF","文化用地","文化用地（AI展示与体验·西翼）",-WING_OUT,-WING_IN,1619,3238,1.0))
parcels.append(mk_parcel("LU-004","0803","#7B5BFF","文化用地","文化用地（AI展示与体验·东翼）",WING_IN,WING_OUT,1619,3238,1.0))
parcels.append(mk_parcel("LU-005","0701","#E0A63C","居住用地","城镇住宅用地（人才社区·西翼）",-WING_OUT,-WING_IN,0,1619,1.0))
parcels.append(mk_parcel("LU-006","0701","#E0A63C","居住用地","城镇住宅用地（人才社区·东翼）",WING_IN,WING_OUT,0,1619,1.0))
parcels.append(mk_parcel("LU-007","05","#E05B6D","商业用地","商业服务业用地（原点社区配套·西翼）",-WING_OUT,-WING_IN,-1619,0,1.0))
parcels.append(mk_parcel("LU-008","05","#E05B6D","商业用地","商业服务业用地（原点社区配套·东翼）",WING_IN,WING_OUT,-1619,0,1.0))
parcels.append(mk_parcel("LU-009","05","#E05B6D","商业用地","商业服务业用地（大钟寺智能消费·西翼）",-WING_OUT,-WING_IN,-3238,-1619,1.0))
parcels.append(mk_parcel("LU-010","05","#E05B6D","商业用地","商业服务业用地（大钟寺智能消费·东翼）",WING_IN,WING_OUT,-3238,-1619,1.0))
parcels.append(mk_parcel("LU-011","0802","#2E5BFF","科研用地","科研用地（AI产业集聚·西翼）",-WING_OUT,-WING_IN,-4857.5,-3238,1.0))
parcels.append(mk_parcel("LU-012","0802","#2E5BFF","科研用地","科研用地（AI产业集聚·东翼）",WING_IN,WING_OUT,-4857.5,-3238,1.0))
parcels.append(mk_parcel("LU-013","1401","#3D9E6A","公园绿地","公园绿地（京张遗址公园北段）",-110.95,110.95,1619,4857))
parcels.append(mk_parcel("LU-014","1401","#3D9E6A","公园绿地","公园绿地（京张遗址公园中段）",-110.95,110.95,-1619,1619))
parcels.append(mk_parcel("LU-015","1401","#3D9E6A","公园绿地","公园绿地（京张遗址公园南段）",-110.95,110.95,-4857,-1619))

print("=== 地块镜像对称（设计矩形）===")
for i in range(0, 12, 2):
    a, b = parcels[i], parcels[i+1]
    ax = a["design_rect"]; bx = b["design_rect"]
    assert abs(ax[0]+bx[1])<0.001 and abs(ax[1]+bx[0])<0.001 and ax[2]==bx[2] and ax[3]==bx[3]
print("  ✅ 6 对地块设计矩形镜像对称")

# ============ 3. 建筑生成（网格，FAR≤1.0）============
B_CFG = {
    "0802": {"type":"ai_r_and_d","tname":"AI研发","color":"#4F7CFF","cover":0.16,"b_area":1500,"h_lo":12,"h_hi":24,"fl_lo":3,"fl_hi":7},
    "0803": {"type":"education","tname":"教育建筑","color":"#9B7BFF","cover":0.18,"b_area":1400,"h_lo":9,"h_hi":24,"fl_lo":2,"fl_hi":7},
    "0701": {"type":"residential","tname":"居住建筑","color":"#E8B84C","cover":0.12,"b_area":1000,"h_lo":12,"h_hi":21,"fl_lo":4,"fl_hi":7},
    "05":   {"type":"mixed_use","tname":"混合功能","color":"#FF6B7A","cover":0.15,"b_area":1100,"h_lo":9,"h_hi":18,"fl_lo":2,"fl_hi":5},
}

def gen_in_parcel(parcel):
    pid = parcel["id"]; code = parcel["code"]
    if code == "1401":
        return []
    cfg = B_CFG[code]
    x0, x1, y0, y1 = parcel["design_rect"]
    m = 25
    clip = box(x0+m, y0+m, x1-m, y1-m).intersection(SITE_POLY)
    if clip.is_empty:
        return []
    cx0, cy0, cx1, cy1 = clip.bounds
    w = cx1-cx0; h = cy1-cy0
    if w <= 0 or h <= 0:
        return []
    parcel_area = parcel["area_sqm"]
    n_target = max(8, int(parcel_area * cfg["cover"] / cfg["b_area"]))
    blds = []
    best = None
    for n_cols in (3,4,5):
        rows = max(3, math.ceil(n_target/n_cols))
        cw = w/n_cols; rh = h/rows
        bw = cw*0.38; bh = rh*0.42
        if bw < 15 or bh < 12:
            continue
        score = abs(n_cols*rows - n_target)
        if best is None or score < best[0]:
            best = (score, n_cols, rows, cw, rh, bw, bh)
    if best is None:
        n_cols, rows = 3, max(3, math.ceil(n_target/3))
        cw, rh = w/3, h/max(3,math.ceil(n_target/3))
        bw, bh = cw*0.38, rh*0.42
    else:
        _, n_cols, rows, cw, rh, bw, bh = best
    for i in range(n_cols):
        for j in range(rows):
            bx0 = cx0 + cw*i + (cw-bw)/2
            by0 = cy0 + rh*j + (rh-bh)/2
            bpoly = box(bx0, by0, bx0+bw, by0+bh).intersection(SITE_POLY)
            if bpoly.is_empty or bpoly.geom_type != "Polygon":
                continue
            bpoly = bpoly.buffer(-0.05)
            if bpoly.is_empty or bpoly.geom_type != "Polygon":
                continue
            ba = area_sqm_4548(poly_ring(bpoly, 0.0))
            if ba < bw*bh*0.35:
                continue
            t = j/(rows-1) if rows > 1 else 0.5
            hgt = round(cfg["h_lo"] + t*(cfg["h_hi"]-cfg["h_lo"]))
            fl = round(cfg["fl_lo"] + t*(cfg["fl_hi"]-cfg["fl_lo"]))
            blds.append({"type":cfg["type"],"tname":cfg["tname"],"color":cfg["color"],
                         "h":hgt,"f":fl,"ring":poly_ring(bpoly),"area":round(ba,1)})
    return blds

all_blds = []
bid = 0
phase_map = {"LU-001":"phase1_near","LU-002":"phase1_near","LU-003":"phase1_near","LU-004":"phase1_near",
             "LU-005":"phase2_mid","LU-006":"phase2_mid","LU-007":"phase2_mid","LU-008":"phase2_mid",
             "LU-009":"phase3_far","LU-010":"phase3_far","LU-011":"phase3_far","LU-012":"phase3_far"}
for p in parcels:
    if p["code"] == "1401":
        continue
    for b in gen_in_parcel(p):
        bid += 1
        all_blds.append({"id":f"B-{bid:03d}","type":b["type"],"typeName":b["tname"],
                         "color":b["color"],"height":b["h"],"floors":b["f"],
                         "area":b["area"],"parent":p["id"],"rings":b["ring"],
                         "phase":phase_map[p["id"]],"status":"new_build"})

def add_landmark(pid_parent, x0, x1, y0, y1, phase, h=36, fl=10):
    global bid
    bpoly = box(x0, y0, x1, y1).intersection(SITE_POLY)
    if bpoly.is_empty or bpoly.geom_type != "Polygon":
        return
    bid += 1
    all_blds.append({"id":f"B-{bid:03d}","type":"ai_r_and_d","typeName":"AI研发","color":"#4F7CFF",
                     "height":h,"floors":fl,"area":round(area_sqm_4548(poly_ring(bpoly.buffer(-0.05), 0.0)),1),
                     "parent":pid_parent,"rings":poly_ring(bpoly),
                     "phase":phase,"status":"new_build"})
# 门户地标（36m 控制 FAR）
add_landmark("LU-001", -650, -585, 4550, 4780, "phase1_near")
add_landmark("LU-002",  585,  650, 4550, 4780, "phase1_near")
add_landmark("LU-011", -650, -585, -4780, -4550, "phase3_far")
add_landmark("LU-012",  585,  650, -4780, -4550, "phase3_far")

print(f"\n🏗 建筑总数: {len(all_blds)}")

# ============ 4. 道路/绿地/公共空间/重点区/分期 ============
roads = [
    {"id":"RD-001","cls":"arterial","name":"智脉纵轴（中轴大道）","color":"#FFFFFF","radius":9,"pts":[[AXIS,-4857.10],[AXIS,4857.10]]},
    {"id":"RD-002","cls":"secondary","name":"西翼纵路","color":"#9AA7BD","radius":6.5,"pts":[[-WING_IN-20,-4857.10],[-WING_IN-20,4857.10]]},
    {"id":"RD-003","cls":"secondary","name":"东翼纵路","color":"#9AA7BD","radius":6.5,"pts":[[WING_IN+20,-4857.10],[WING_IN+20,4857.10]]},
    {"id":"RD-004","cls":"branch","name":"智脉横轴1（北）","color":"#C7D2E3","radius":4.5,"pts":[[-670.25,4040],[670.25,4040]]},
    {"id":"RD-005","cls":"branch","name":"智脉横轴2","color":"#C7D2E3","radius":4.5,"pts":[[-670.25,2420],[670.25,2420]]},
    {"id":"RD-006","cls":"branch","name":"智脉横轴3（中）","color":"#C7D2E3","radius":4.5,"pts":[[-670.25,810],[670.25,810]]},
    {"id":"RD-007","cls":"branch","name":"智脉横轴4","color":"#C7D2E3","radius":4.5,"pts":[[-670.25,-810],[670.25,-810]]},
    {"id":"RD-008","cls":"branch","name":"智脉横轴5（南）","color":"#C7D2E3","radius":4.5,"pts":[[-670.25,-2420],[670.25,-2420]]},
    {"id":"RD-009","cls":"branch","name":"智脉横轴6","color":"#C7D2E3","radius":4.5,"pts":[[-670.25,-4040],[670.25,-4040]]},
]

def ring_of(x0,y0,x1,y1):
    return poly_ring(box(x0,y0,x1,y1).intersection(SITE_POLY).buffer(-0.3), 0.0)

def park_ring(y0, y1):
    """中轴公园：扩展到双翼收缩缝隙（±110.5）"""
    return poly_ring(box(-110.95, y0, 110.95, y1).intersection(SITE_POLY).buffer(-0.3), 0.0)

greenSpace = [
    {"id":"GS-001","name":"京张遗址公园（北段）","rings":park_ring(1619,4857)},
    {"id":"GS-002","name":"京张遗址公园（中段）","rings":park_ring(-1619,1619)},
    {"id":"GS-003","name":"京张遗址公园（南段）","rings":park_ring(-4857,-1619)},
]
publicSpace = [
    {"id":"PS-001","name":"众智园核心广场（中轴北端）","rings":ring_of(-80,3200,80,3400)},
    {"id":"PS-002","name":"AI原点社区核心广场（中轴中央）","rings":ring_of(-80,-120,80,80)},
    {"id":"PS-003","name":"大钟寺核心广场（中轴南端）","rings":ring_of(-80,-3400,80,-3200)},
    {"id":"PS-004","name":"文化双翼活力广场（西）","rings":ring_of(-330,1900,-150,2100)},
    {"id":"PS-005","name":"文化双翼活力广场（东）","rings":ring_of(150,1900,330,2100)},
]
keyAreas = [
    {"id":"PROV-KEY-001","name":"众智园AI自主创新加速区（对称双翼+中轴）","short":"众智园AI加速区","area":round(1340*3238/1e4,1),
     "rings":ring_of(-670,1619,670,4857)},
    {"id":"PROV-KEY-002","name":"北京AI原点社区（对称双翼+中轴）","short":"AI原点社区","area":round(1340*3238/1e4,1),
     "rings":ring_of(-670,-1619,670,1619)},
    {"id":"PROV-KEY-003","name":"大钟寺AI产业聚集区（对称双翼+中轴）","short":"大钟寺AI集聚区","area":round(1340*3238/1e4,1),
     "rings":ring_of(-670,-4857,670,-1619)},
]
phasing = [
    {"id":"PH-001","code":"phase1_near","label":"近期（2026-2028）","note":"北段众智园对称双翼先行",
     "rings":ring_of(-670,1619,670,4857)},
    {"id":"PH-002","code":"phase2_mid","label":"中期（2029-2031）","note":"中段AI原点社区+低层商业",
     "rings":ring_of(-670,-1619,670,1619)},
    {"id":"PH-003","code":"phase3_far","label":"远期（2032-2035）","note":"南段大钟寺+科研双翼",
     "rings":ring_of(-670,-4857,670,-1619)},
]

# ============ 5. 指标复算（EPSG:4548）============
bld_foot = sum(b["area"] for b in all_blds)
total_floor = sum(b["area"]*b["floors"] for b in all_blds)
green_area = sum(area_sqm_4548(g["rings"]) for g in greenSpace)
pub_area = sum(area_sqm_4548(p["rings"]) for p in publicSpace)
road_len_km = sum(math.dist(r["pts"][0], r["pts"][1]) for r in roads) / 1000
metrics = {
    "siteArea": round(SITE_AREA/1e6, 2),
    "greenRatio": round(green_area/SITE_AREA*100, 1),
    "density": round(bld_foot/SITE_AREA*100, 1),
    "far": round(total_floor/SITE_AREA, 2),
    "roadLen": round(road_len_km, 1),
    "bldCount": len(all_blds),
}

# ============ 6. 组装 ============
scene = {
    "site": {"rings": SITE_RINGS, "w": SITE_W, "h": SITE_H},
    "landUse": parcels,
    "buildings": all_blds,
    "roads": roads,
    "greenSpace": greenSpace,
    "publicSpace": publicSpace,
    "keyAreas": keyAreas,
    "phasing": phasing,
    "metrics": metrics,
}
with open(OUT, "w") as f:
    json.dump(scene, f, ensure_ascii=False, separators=(",", ":"))

# ============ 7. 输出验证 ============
print("\n=== 指标 ===")
for k, v in metrics.items():
    print(f"  {k}: {v}")
# 几何越界检查
from shapely.geometry import shape as shp
out_cnt = 0
for lu in parcels:
    g = Polygon(lu["rings"])
    if not SITE_POLY.covers(g):
        out_cnt += 1
for b in all_blds:
    g = Polygon(b["rings"])
    if not SITE_POLY.covers(g):
        out_cnt += 1
print(f"\n=== 几何越界检查: {out_cnt} 个越界 ===")
parcel_stats = []
for p in parcels:
    if p["code"] == "1401":
        continue
    cnt = sum(1 for b in all_blds if b["parent"] == p["id"])
    cover = sum(b["area"] for b in all_blds if b["parent"] == p["id"]) / p["area_sqm"] * 100
    parcel_stats.append({"id":p["id"],"code":p["code"],"name":p["name"],
                         "area_ha":round(p["area_sqm"]/1e4,1),"coverage":round(cover,1),"blds":cnt})
print("\n=== 每地块参数 ===")
for s in parcel_stats:
    print(f"  {s['id']} {s['name']:12s} {s['area_ha']:6.1f}ha 覆盖率{s['coverage']:5.1f}% {s['blds']:4d}栋")
print(f"\n✅ SCENE_DATA → {OUT} ({len(json.dumps(scene))/1024:.0f} KB)")
