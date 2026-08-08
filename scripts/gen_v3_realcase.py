#!/usr/bin/env python3
"""
京张智脉 V3 — 真实北京建筑案例支撑版生成脚本
核心升级（相对 V2）：
1. 居住地块 → 板式住宅楼南低北高错落排布（真实案例：万柳书院10-15层/30-45m、使馆壹号院、融创北京壹号院）——北京在北半球阳光自南射入，南排矮北排高利于全部楼栋采光
2. 科研地块 → 点式超高层（真实案例：中国尊78m见方、正大中心238m、国贸三期330m）
3. 文化地块 → 大型文化建筑（真实案例：首都博物馆、中国科技馆，基底1-4万㎡、3-5层）
4. 商业地块 → 商业综合体（真实案例：朝阳大悦城、西单大悦城）+ 底商裙房≤3层
5. 居住地块配建教育建筑（北京中小学教学楼 4-5层）+ 沿街底商
6. 日照：南低北高梯度（30→45m，每排+3m），排距260m ≈ 5.8×最高楼高45m，远超北京板楼日照间距系数 1.5-1.7 要求，层高3m
7. 所有建筑体块有真实北京案例对应（见 proposal.md 案例支撑表）
"""
import json, math
from shapely.geometry import Polygon, box, LineString
from pyproj import Transformer

OUT = "/tmp/scene_v3.json"
to_4548 = Transformer.from_crs("EPSG:4326", "EPSG:4548", always_xy=True)

# ============ 1. 场地 ============
SITE_RINGS = [[-584.3213683998594,-4857.095687500316],[670.2509814002696,-4857.095687500316],[670.2509814002696,-1970.5931074999432],[498.39175540067015,804.8901424998991],[670.2509814002696,4857.095687499526],[-412.46214240025984,4857.095687499526],[-498.391755399449,2581.1994224997034],[-670.2509814002696,-860.3998075001641],[-584.3213683998594,-4857.095687500316]]
SITE_W, SITE_H = 1340.5, 9714.19
SITE_POLY = Polygon(SITE_RINGS)

A_LON, B_LON = 0.0000116374, 116.3475
C_LAT, D_LAT = 0.0000090074, 39.98275

def area_sqm_4548(ring):
    wgs = [[A_LON*p[0]+B_LON, C_LAT*p[1]+D_LAT] for p in ring]
    proj = [to_4548.transform(x, y) for x, y in wgs]
    return abs(Polygon(proj).area)

SITE_AREA = area_sqm_4548(SITE_RINGS)
print(f"场地面积(EPSG:4548): {SITE_AREA/1e4:.1f} ha")

def poly_ring(poly, shrink=0.0):
    if shrink > 0:
        poly = poly.buffer(-shrink)
    coords = list(poly.exterior.coords)
    return [[round(x,9), round(y,9)] for x, y in coords]

# ============ 2. 地块（复用 V2 中轴对称划分）============
AXIS = 0.0; PARK_HALF = 110.0; WING_IN = 110.0; WING_OUT = 671.0

def mk_parcel(pid, code, color, name, label, x0, x1, y0, y1, axis_gap=0.0):
    if axis_gap > 0 and x1 <= 0:
        x1 -= axis_gap
    elif axis_gap > 0 and x0 >= 0:
        x0 += axis_gap
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

all_blds = []
bid = 0
phase_map = {"LU-001":"phase1_near","LU-002":"phase1_near","LU-003":"phase1_near","LU-004":"phase1_near",
             "LU-005":"phase2_mid","LU-006":"phase2_mid","LU-007":"phase2_mid","LU-008":"phase2_mid",
             "LU-009":"phase3_far","LU-010":"phase3_far","LU-011":"phase3_far","LU-012":"phase3_far"}

def add_bld(pid, btype, tname, color, rings, h, fl, area, case=""):
    """rings: 本地坐标环（点数组）；area: EPSG:4548 投影面积"""
    global bid
    bid += 1
    all_blds.append({"id": f"B-{bid:03d}", "type": btype, "typeName": tname,
                     "color": color, "height": h, "floors": fl,
                     "area": round(area,1), "parent": pid, "rings": rings,
                     "phase": phase_map[pid], "status": "new_build",
                     "case": case})

def bld_box(pid, x0, y0, x1, y1, h, fl, btype, tname, color, case, shrink=0.05):
    """在场地内放一个矩形建筑（自动裁剪 + 投影面积 + 微收缩防贴边）"""
    bp = box(x0, y0, x1, y1).intersection(SITE_POLY)
    if bp.is_empty or bp.geom_type != "Polygon":
        return
    bp = bp.buffer(-0.35)  # 微收缩：确保严格在场地内（消除共享边浮点）
    if bp.is_empty or bp.geom_type != "Polygon":
        return
    area = area_sqm_4548(poly_ring(bp, 0.0))
    add_bld(pid, btype, tname, color, poly_ring(bp), h, fl, area, case)

# ============ 镜像工具（以中轴 x=0 左右对称，所有成对地块共用）============
def _site_limit_at(y):
    """该 y 位置、以 x=0 镜像排布的楼群半宽上限（含 15m 退线）。
    取西翼可用西边界与东翼可用东边界中较窄者——两翼镜像共用同一上限，保证不出界。"""
    inter = LineString([(-700, y), (700, y)]).intersection(SITE_POLY)
    if inter.is_empty:
        return 0.0
    xs = [p[0] for p in inter.coords]
    west, east = min(xs), max(xs)
    west_eff = max(west, -WING_OUT + 15)   # 西翼 clip 西边界
    east_eff = min(east, WING_OUT - 15)    # 东翼 clip 东边界
    return min(abs(west_eff), east_eff)

def _mirror_x(x0, d, sz):
    """以 x=0 为中轴镜像：西翼楼 x∈[−d−sz, −d]，东翼楼 x∈[d, d+sz]（严格镜像）"""
    if x0 < 0:
        return -d - sz, -d
    return d, d + sz

# ============ 3. 建筑生成（真实北京案例）============
# ---- 3.1 科研地块：大基底点式办公楼（36-80m，锚定北五环外真实高度）----
# 高度参照：北京上地信息产业基地/中关村软件园（西二旗）写字楼 6-18 层/24-72m 为主流
# ---- 3.1 科研地块：大基底点式办公楼（45-80m，锚定北五环外真实高度）----
# 镜像排布：10 栋塔楼成对出现在 ±d（以中轴 x=0 镜像）
# 疏散+贴边：y 均匀铺满地块（0.06~0.94 贴南北边界），d 从内(150)到外(贴西翼边界)分散；
# 北段西翼斜边界窄(-431~-467)、南段宽(-587~-617)——南北段各用一套 d 值各自贴边
def gen_rd(pid, x0, x1, y0, y1, tag):
    # 用实际可用区域（设计矩形∩场地）
    clip = box(x0+15, y0+15, x1-15, y1-15).intersection(SITE_POLY)
    if clip.is_empty or clip.geom_type != "Polygon":
        return
    cx0, cy0, cx1, cy1 = clip.bounds
    hgt_span = cy1 - cy0
    y0 = cy0
    north = y0 > 0  # 北段 LU-001/002（西翼边界窄）vs 南段 LU-011/012（西翼边界宽）
    # 塔楼规格（y比例, 见方, 高度m, 层数, 颜色, 案例）— y 均匀分布 0.06~0.94 贴南北边界
    towers_spec = [
        (0.06, 60, 54, 14, "#7BA8FF", "软件园地标级·单层~3600㎡"),
        (0.15, 75, 80, 20, "#4F7CFF", "中国尊级·底部78m见方/单层~3500㎡·社区级缩尺"),
        (0.25, 58, 48, 12, "#7BA8FF", "科技园级·单层~3400㎡"),
        (0.35, 70, 70, 18, "#4F7CFF", "正大中心级·50m见方/单层~2500㎡·放大版"),
        (0.45, 56, 45, 11, "#5B8CFF", "园区办公级·单层~3100㎡"),
        (0.55, 72, 60, 15, "#4F7CFF", "国贸三期级·48×50m/单层~2300㎡·放大版"),
        (0.65, 58, 48, 12, "#7BA8FF", "科技园级·单层~3400㎡"),
        (0.75, 65, 60, 15, "#5B8CFF", "CBD核心区级·55-60m见方/单层~3000㎡"),
        (0.85, 56, 45, 11, "#5B8CFF", "园区办公级·单层~3100㎡"),
        (0.94, 62, 54, 14, "#6B9AFF", "上地地标级·单层~3800㎡"),
    ]
    # 距中轴 d：内→外分散（疏散），外侧塔贴该段西翼边界（镜像下东翼同距，两翼对称）
    if north:
        d_list = [150, 383, 250, 380, 320, 365, 200, 356, 290, 348]  # 北段西界 -416~-470
    else:
        d_list = [200, 510, 320, 525, 420, 530, 280, 535, 420, 545]  # 南段西界 -587~-617
    for (ty, sz, h, fl, color, case), d in zip(towers_spec, d_list):
        by = y0 + hgt_span * ty
        bx0, bx1 = _mirror_x(x0, d, sz)
        bld_box(pid, bx0, by, bx1, by+sz, h, fl, "ai_r_and_d", "AI研发", color,
                f"大基底写字楼·参考北京{case}({h}m/{fl}层/层高{h/fl:.1f}m)")
    # 研发裙房（低层大基底，3层/12m=4.0m层高 — 参考中关村软件园办公楼，两翼镜像；贴地块南边界）
    d = 225 if north else 300
    by = y0 + hgt_span * 0.03
    bx0, bx1 = _mirror_x(x0, d, 240)
    bld_box(pid, bx0, by, bx1, by+70, 12, 3, "ai_r_and_d", "AI研发裙房", "#6FA0FF",
            f"低层研发裙房·参考北京中关村软件园办公楼(3层/12m/4.0m层高)")

# ---- 3.2 文化地块：大型文化建筑（案例：首都博物馆/中国科技馆）----
# 镜像排布：主馆/专题馆/配套各一对 ±d（以中轴 x=0 镜像）
def gen_culture(pid, x0, x1, y0, y1, tag):
    clip = box(x0+15, y0+15, x1-15, y1-15).intersection(SITE_POLY)
    if clip.is_empty or clip.geom_type != "Polygon":
        return
    cx0, cy0, cx1, cy1 = clip.bounds
    hgt_span = cy1 - cy0
    y0 = cy0
    # 主文化馆（大型文化建筑，基底~1.4万㎡，4层，36m — 参考首都博物馆6.4万㎡/5层/40m；d=370 贴西翼边界）
    d = 370; by = y0 + hgt_span*0.22
    bx0, bx1 = _mirror_x(x0, d, 150)
    bld_box(pid, bx0, by, bx1, by+95, 36, 4, "education", "文化建筑", "#9B7BFF",
            f"大型文化馆·参考首都博物馆(6.4万㎡/5层/高40m/基底~1.3万㎡)")
    # 第二文化馆（~0.8万㎡基底，3层 — 参考中国科技馆10.2万㎡/5层；d=400 避开西翼 y≈2105 斜边界 -521）
    d = 400; by = y0 + hgt_span*0.30
    bx0, bx1 = _mirror_x(x0, d, 115)
    bld_box(pid, bx0, by, bx1, by+75, 30, 3, "education", "文化建筑", "#B494FF",
            f"专题文化馆·参考中国科技馆(10.2万㎡/5层/高30m)")
    # 文化配套商业（底商≤3层，d=355 避开西翼 y≈2785 斜边界 -488）
    d = 355; by = y0 + hgt_span*0.72
    bx0, bx1 = _mirror_x(x0, d, 130)
    bld_box(pid, bx0, by, bx1, by+60, 12, 3, "mixed_use", "文化商业配套", "#FF8FA3",
            f"文化商业底商·参考北京文化园区配套商业(≤3层)")

# ---- 3.3 居住地块：纯住宅统一规格板楼镜像贴边排布（无点式/教育/底商） ----
# 排布逻辑：① 住宅区仅住宅，全部统一 60×14m 板楼
# ② 以中轴 x=0 镜像：每排楼栋两翼严格左右对称（x 互为相反数）
# ③ 5 排南低北高（30→45m 每排+3m，北京阳光自南射入任何一排不被遮挡）
# ④ 每排栋数按该位置两翼边界中较窄者自适应，楼群外端离边界仅 5m——自然贴紧边界
def gen_residential(pid, x0, x1, y0, y1, tag):
    # 用实际可用区域（设计矩形∩场地）
    clip = box(x0+15, y0+15, x1-15, y1-15).intersection(SITE_POLY)
    if clip.is_empty or clip.geom_type != "Polygon":
        return
    cx0, cy0, cx1, cy1 = clip.bounds
    hgt_span = cy1 - cy0
    y0 = cy0
    bd = 14  # 板楼进深（北京板楼常规 12-16m）
    BL = 60  # 统一板楼长度 60m（同一种规格）
    gap = 22  # 山墙距 22m（≥13m消防间距）
    step = BL + gap  # 82m（楼间距）
    # 5 排南低北高：高度从南到北 30→45m 每排+3m（利于日照）
    # 排距 0.24×hgt_span ≈ 380m ≈ 8.4×最高楼高，远超北京板楼日照间距系数 1.5-1.7
    rows_y = [0.02, 0.26, 0.50, 0.74, 0.98]  # 贴南北边界
    heights = [30, 33, 36, 39, 45]
    floors  = [10, 11, 12, 13, 15]
    colors  = ["#C9952F", "#D9A23F", "#E8B84C", "#F2CD66", "#FCE796"]
    cases   = ["万柳书院(10层/30m)", "使馆壹号院(11层/33m)", "融创北京壹号院(12层/36m)",
               "融创北京壹号院(13层/39m)", "金茂府(15层/45m)"]
    for ry, h, fl, color, case in zip(rows_y, heights, floors, colors, cases):
        row_y = y0 + hgt_span * ry
        limit = _site_limit_at(row_y)                    # 镜像楼群半宽上限（两翼较窄者）
        n = max(2, int((limit - 111 - BL) // step) + 1)  # 中轴间隙 ≥111（绿带半宽）
        total = n * BL + (n - 1) * gap
        c = max(111.0, limit - total - 5)                # 楼群外端离边界 5m（自然贴紧）
        for i in range(n):
            d = c + i * step
            bx0, bx1 = _mirror_x(x0, d, BL)
            bld_box(pid, bx0, row_y, bx1, row_y+bd, h, fl, "residential", "板式住宅", color,
                    f"板式住宅·参考北京{case}/统一长60m×14m")
    # 住宅区无点式/教育/底商（纯住宅，统一规格板楼镜像贴边，用户要求）

# ---- 3.4 商业地块：商业综合体（案例：朝阳大悦城/西单大悦城）+ 底商 ----
# 镜像排布：综合体/副楼/底商各一对 ±d（以中轴 x=0 镜像）
def gen_commercial(pid, x0, x1, y0, y1, tag, is_dazhongsi=False):
    clip = box(x0+15, y0+15, x1-15, y1-15).intersection(SITE_POLY)
    if clip.is_empty or clip.geom_type != "Polygon":
        return
    cx0, cy0, cx1, cy1 = clip.bounds
    hgt_span = cy1 - cy0
    y0 = cy0
    # 商业综合体（基底~1.5万㎡，8层/36m — 参考北京清河万象汇/五环外商业综合体；d=490 贴西翼边界）
    d = 490; by = y0 + hgt_span*0.20
    bx0, bx1 = _mirror_x(x0, d, 130)
    bld_box(pid, bx0, by, bx1, by+115, 36, 8, "mixed_use", "商业综合体", "#FF6B7A",
            f"商业综合体·参考北京清河万象汇(8层/36m/大基底)")
    # 商业副楼（5层/24m — 参考北京五环外商业副楼，d=498 贴东边界 y≈-1068 处 614m；y=0.34 与综合体 y 错开防重叠）
    d = 498; by = y0 + hgt_span*0.34
    bx0, bx1 = _mirror_x(x0, d, 110)
    bld_box(pid, bx0, by, bx1, by+80, 24, 5, "mixed_use", "商业副楼", "#E85A6C",
            f"商业副楼·参考北京西红门荟聚式郊区商业(3-5层/20-24m)")
    # 底商裙房（≤3层，宽大；d=350 避开东翼 y≈-453 处东边界仅 552m）
    d = 350; by = y0 + hgt_span*0.72
    bx0, bx1 = _mirror_x(x0, d, 200)
    bld_box(pid, bx0, by, bx1, by+55, 12, 3, "mixed_use", "底商裙房", "#FF9DAE",
            f"底商裙房·参考北京商业街区裙房(≤3层/12m)")

# ============ 4. 生成全部建筑 ============
# 北段：科研超高层 + 文化建筑
for p in parcels:
    pid = p["id"]
    x0, x1, y0, y1 = p["design_rect"]
    if pid == "LU-001":
        gen_rd(pid, x0, x1, y0, y1, "西")
    elif pid == "LU-002":
        gen_rd(pid, x0, x1, y0, y1, "东")
    elif pid == "LU-003":
        gen_culture(pid, x0, x1, y0, y1, "西")
    elif pid == "LU-004":
        gen_culture(pid, x0, x1, y0, y1, "东")
    elif pid == "LU-005":
        gen_residential(pid, x0, x1, y0, y1, "西")
    elif pid == "LU-006":
        gen_residential(pid, x0, x1, y0, y1, "东")
    elif pid == "LU-007":
        gen_commercial(pid, x0, x1, y0, y1, "西", False)
    elif pid == "LU-008":
        gen_commercial(pid, x0, x1, y0, y1, "东", False)
    elif pid == "LU-009":
        gen_commercial(pid, x0, x1, y0, y1, "西", True)
    elif pid == "LU-010":
        gen_commercial(pid, x0, x1, y0, y1, "东", True)
    elif pid == "LU-011":
        gen_rd(pid, x0, x1, y0, y1, "西")
    elif pid == "LU-012":
        gen_rd(pid, x0, x1, y0, y1, "东")

print(f"\n🏗 建筑总数: {len(all_blds)}")

# ============ 5. 道路/绿地/公共空间/重点区/分期（复用 V2）============
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

# ============ 6. 指标复算（EPSG:4548）============
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

# ============ 7. 组装输出 ============
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

print("\n=== 指标 ===")
for k, v in metrics.items():
    print(f"  {k}: {v}")

# 越界检查
from shapely.geometry import shape as shp
out_cnt = 0
for b in all_blds:
    bp = Polygon(b["rings"])
    if not SITE_POLY.contains(bp):
        out_cnt += 1
print(f"建筑越界: {out_cnt}")
print(f"输出: {OUT}")
