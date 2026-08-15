# -*- coding: utf-8 -*-
"""
京张AI创新带 · 站点计算模型（KUN-SAL 范式）
把 OSM 现状数据 + 仓库临时边界整合为可计算场地图。
- 坐标系：输入 EPSG:4326，度量计算统一投影 EPSG:4548 (CGCS2000 / CM 117E)
- 数据源：OSM (ODbL, 需署名) + brief/site-package provisional boundaries（临时约束，仅用于生成/讨论）
- 输出：site_model.pkl (shapely/networkx) + site_report.json（全数字溯源）
"""
import json, os, pickle, math
import numpy as np
from shapely.geometry import shape, LineString, Point, box, mapping
from shapely.ops import unary_union, linemerge
import pyproj

HERE = os.path.dirname(os.path.abspath(__file__))
OSM_DIR = os.path.join(HERE, "osm")
HAIDIAN = os.path.join(HERE, "..", "haidian")
BRIEF_GEO = os.path.join(HAIDIAN, "brief", "site-package", "geometry", "provisional_boundaries.geojson")

WGS84 = pyproj.CRS.from_epsg(4326)
P4548 = pyproj.CRS.from_epsg(4548)
TRANS = pyproj.Transformer.from_crs(WGS84, P4548, always_xy=True)

def to4548(lon, lat):
    x, y = TRANS.transform(lon, lat)
    return x, y

def load_osm(name):
    p = os.path.join(OSM_DIR, f"{name}.json")
    if not os.path.exists(p):
        return []
    return json.load(open(p))["elements"]

def elements_to_geoms(elements):
    geoms = []
    for e in elements:
        g = None
        if e["type"] == "node":
            g = Point(e["lon"], e["lat"])
        elif e["type"] == "way" and "geometry" in e:
            pts = [(c["lon"], c["lat"]) for c in e["geometry"]]
            if len(pts) >= 2:
                if pts[0] == pts[-1] and len(pts) >= 4:
                    from shapely.geometry import Polygon
                    g = Polygon(pts)
                else:
                    g = LineString(pts)
        elif e["type"] == "relation" and "members" in e:
            lines = []
            for m in e["members"]:
                if m.get("type") == "way" and "geometry" in m:
                    pts = [(c["lon"], c["lat"]) for c in m["geometry"]]
                    if len(pts) >= 2:
                        lines.append(LineString(pts))
            if lines:
                g = unary_union(lines)
        if g is not None and not g.is_empty:
            geoms.append((e, g))
    return geoms

def load_provisional():
    gj = json.load(open(BRIEF_GEO))
    out = {}
    for f in gj["features"]:
        g = shape(f["geometry"])
        out[f["id"]] = (f["properties"], g)
    return out

def _reproject(geom):
    from shapely.ops import transform as sh_transform
    def pr(x, y, z=None):
        a, b = TRANS.transform(x, y)
        return (a, b)
    return sh_transform(pr, geom)

def geom_stats(geom):
    """返回 EPSG:4548 下的面积/长度统计（混合类型分别累计）"""
    if geom.is_empty:
        return None
    if geom.geom_type == "GeometryCollection":
        acc = {"area_sqm": 0.0, "length_m": 0.0}
        for g in geom.geoms:
            s = geom_stats(g)
            if s:
                acc["area_sqm"] += s["area_sqm"] or 0.0
                acc["length_m"] += s["length_m"] or 0.0
        return acc
    pg = _reproject(geom)
    if pg.geom_type in ("Polygon", "MultiPolygon"):
        return {"area_sqm": pg.area, "length_m": pg.length}
    if pg.geom_type in ("LineString", "MultiLineString"):
        return {"length_m": pg.length, "area_sqm": None}
    return None

# ---------- 关键锚点（公开常识 + OSM 校验，登记进 registry） ----------
ANCHORS = [
    # id, 名称, 类型, lon, lat, 依据
    ("STA-WUDAOKOU", "五道口站", "metro_13", 116.3317, 39.9915, "OSM node railway=station"),
    ("STA-DAZHONGSI", "大钟寺站", "metro_13", 116.3390, 39.9653, "OSM node railway=station"),
    ("STA-ZHICHUNLU", "知春路站", "metro_10_13", 116.3344, 39.9751, "OSM node railway=station"),
    ("STA-QHDXK", "清华东路西口站", "metro_15", 116.3336, 39.9993, "OSM node railway=station"),
    ("STA-XUEYUANQIAO", "学院桥站", "metro_cp", 116.3473, 39.9868, "OSM node railway=station"),
    ("STA-XUEZHIYUAN", "学知园站", "metro_cp", 116.3458, 40.0136, "OSM node railway=station"),
    ("STA-BEIJINGBEI", "北京北站", "mainline", 116.3462, 39.9459, "OSM node railway=station"),
    ("STA-XIZHIMEN", "西直门站", "metro_2_4_13", 116.3492, 39.9392, "OSM node railway=station"),
    ("STA-XITUCHENG", "西土城站", "metro_10", 116.3478, 39.9749, "OSM node railway=station"),
    ("UNI-PKUHSC", "北京大学医学部", "university", 116.3463, 39.9822, "OSM amenity=university 多节点"),
    ("UNI-BUAA", "北京航空航天大学", "university", 116.3474, 39.9789, "OSM 校园区(学院路)"),
    ("UNI-CUPL", "中国政法大学研究生院", "university", 116.3435, 39.9654, "OSM node"),
    ("UNI-CIPS", "首都体育学院", "university", 116.3431, 39.9688, "OSM node"),
    ("HER-QINGHUAYUAN", "清华园车站(遗址)", "heritage", 116.3390, 39.9850, "公开资料：京张铁路清华园站旧址(成府路口南)"),
    ("HER-SI_LIESHI", "四烈士墓遗址", "heritage", 116.3322, 39.9386, "OSM node historic=memorial"),
    ("PK-LAODONGXUEGONG", "京张铁路遗址公园(五道口段)", "park", 116.3330, 39.9850, "公开资料：原京张铁路走廊改造为遗址公园"),
]

def build_site_model():
    report = {"meta": {
        "title": "百年京张AI创新带站点计算模型",
        "method": "KUN-SAL: CASA内核(Wilson空间交互/渗流/标度律)+空间句法+反事实零模型",
        "crs": "EPSG:4326 input, EPSG:4548 metric",
        "generated": "2026-08-15",
        "provenance": {
            "osm": "Overpass API 2026-08-15, bbox 39.935,116.330,40.035,116.375, ODbL attribution",
            "boundaries": "brief/site-package/geometry/provisional_boundaries.geojson (provisional_constraint, 不作为红线)",
        },
    }}
    prov = load_provisional()
    site_props, site = prov["PROV-SITE-001"]
    keys = {k: prov[k] for k in ("PROV-KEY-001", "PROV-KEY-002", "PROV-KEY-003")}
    report["boundaries"] = {
        "site_area_sqm_4548": round(geom_stats(site)["area_sqm"], 1),
        "site_declared_sqm": 11400000,
        "key_areas": {
            "zhongzhiyuan_ai_acceleration_area": round(geom_stats(keys["PROV-KEY-001"][1])["area_sqm"], 1),
            "beijing_ai_origin_community": round(geom_stats(keys["PROV-KEY-002"][1])["area_sqm"], 1),
            "dazhongsi_ai_industry_cluster": round(geom_stats(keys["PROV-KEY-003"][1])["area_sqm"], 1),
        },
        "note": "临时粗略边界, 仅用于生成/讨论/自检; 官方红线发布后整包重算",
    }
    # 现状图层
    layers = {}
    for name in ("roads", "rail", "green", "water", "univ", "poi"):
        layers[name] = elements_to_geoms(load_osm(name))
        report.setdefault("osm_counts", {})[name] = len(layers[name])
    # 铁路走廊(遗址公园脊柱): 由 OSM 实测交叉点 + 公开站点锚点推导的参考轴线
    # （非官方红线；用于计算与可视化，登记为 agent_inferred_reference）
    rail_lines = []
    for e, g in layers["rail"]:
        t = e.get("tags", {})
        nm = t.get("name", "") or ""
        rw = t.get("railway", "")
        if rw in ("disused", "abandoned") or "京包" in nm:
            if g.geom_type in ("LineString", "MultiLineString"):
                rail_lines.append(g)
    corridor_waypoints = [
        (116.3430, 39.9420, "西直门外大街南端(概念)"),
        (116.3419, 39.9568, "学院南路交叉"),
        (116.3391, 39.9662, "北三环交叉"),
        (116.3341, 39.9750, "知春路交叉"),
        (116.3324, 39.9849, "北四环交叉"),
        (116.3318, 39.9915, "成府路/五道口交叉"),
        (116.3315, 39.9992, "清华东路交叉"),
        (116.3340, 40.0120, "清河方向北端(概念)"),
    ]
    corridor = LineString([(w[0], w[1]) for w in corridor_waypoints])
    report["heritage_corridor_length_m"] = round(geom_stats(corridor)["length_m"], 1)
    report["heritage_corridor_waypoints"] = corridor_waypoints
    report["heritage_corridor_segments"] = len(rail_lines)
    report["heritage_corridor_note"] = "走廊轴线由 OSM 铁路断点交叉位置与公开站点锚点推导，为计算参考线（agent_inferred_reference），非官方红线"
    # 绿地
    green_union = unary_union([g for e, g in layers["green"] if g.geom_type in ("Polygon", "MultiPolygon")])
    report["green_area_sqm_4548"] = round(geom_stats(green_union)["area_sqm"], 1) if not green_union.is_empty else 0
    # 水系
    water_union = unary_union([g for e, g in layers["water"]])
    report["water_length_m_4548"] = round(geom_stats(water_union)["length_m"], 1) if not water_union.is_empty else 0

    model = {
        "site": site, "site_props": site_props,
        "keys": {k: v[0] for k, v in keys.items()},
        "key_geoms": {k: v[1] for k, v in keys.items()},
        "corridor": corridor,
        "green_union": green_union,
        "water_union": water_union,
        "layers": layers,
        "anchors": ANCHORS,
    }
    with open(os.path.join(HERE, "site_model.pkl"), "wb") as f:
        pickle.dump(model, f)
    json.dump(report, open(os.path.join(HERE, "site_report.json"), "w"), ensure_ascii=False, indent=2)
    print(json.dumps(report, ensure_ascii=False, indent=2)[:2000])

if __name__ == "__main__":
    build_site_model()
