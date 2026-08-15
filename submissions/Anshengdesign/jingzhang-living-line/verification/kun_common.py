# -*- coding: utf-8 -*-
"""KUN-SAL 京张参赛 · 计算公共模块
- 中文字体修复（手册 §3.1，已验证）
- EPSG:4326→4548 度量变换
- OSM 道路网络图构建（空间句法/λ/渗流共用）
- 指标登记册（metrics_registry，单源真相）
"""
import os, json, math
import numpy as np
from shapely.geometry import LineString, Point
from shapely.ops import unary_union, linemerge
from shapely import get_coordinates
import networkx as nx
import pyproj

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------- 字体 ----------
def setup_chinese_fonts():
    import matplotlib
    from matplotlib import font_manager
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _FONT_FILES = [
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    names = []
    for p in _FONT_FILES:
        if os.path.exists(p):
            try:
                font_manager.fontManager.addfont(p)
                names.append(font_manager.FontProperties(fname=p).get_name())
            except Exception:
                pass
    uniq = []
    for n in names:
        if n not in uniq:
            uniq.append(n)
    fallback = [n for n in ["STHeiti", "Heiti TC", "Arial Unicode MS", "Hiragino Sans GB", "PingFang HK", "Songti SC"] if n not in uniq]
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = uniq + fallback + ["DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    return plt

# ---------- 坐标 ----------
WGS84 = pyproj.CRS.from_epsg(4326)
P4548 = pyproj.CRS.from_epsg(4548)
_TRANS = pyproj.Transformer.from_crs(WGS84, P4548, always_xy=True)

def xy(lon, lat):
    return _TRANS.transform(lon, lat)

def dist_m(lon1, lat1, lon2, lat2):
    (x1, y1), (x2, y2) = xy(lon1, lat1), xy(lon2, lat2)
    return math.hypot(x2 - x1, y2 - y1)

# ---------- OSM 路网图 ----------
def build_road_graph(elements, include=("motorway", "trunk", "primary", "secondary", "tertiary",
                                        "unclassified", "residential", "living_street",
                                        "pedestrian", "cycleway", "path", "footway")):
    """把 OSM way 元素转为 networkx 无向图（节点=交点/端点, 边=路段米制长度）。
    返回 G（节点坐标为 lon/lat 元组）+ 每条边的道路等级。"""
    G = nx.Graph()
    ways = []
    for item in elements:
        e = item[0] if isinstance(item, tuple) else item
        if e.get("type") != "way":
            continue
        t = e.get("tags", {})
        hw = t.get("highway")
        if hw not in include:
            continue
        geom = e.get("geometry") or []
        pts = [(c["lon"], c["lat"]) for c in geom]
        if len(pts) >= 2:
            ways.append((pts, hw))
    node_ids = {}
    def nid(p):
        key = (round(p[0], 7), round(p[1], 7))
        if key not in node_ids:
            node_ids[key] = len(node_ids)
        return node_ids[key]
    for pts, hw in ways:
        a = nid(pts[0])
        for i in range(1, len(pts)):
            b = nid(pts[i])
            d = dist_m(pts[i - 1][0], pts[i - 1][1], pts[i][0], pts[i][1])
            if d <= 0:
                continue
            if G.has_edge(a, b):
                if G[a][b].get("w", 1e9) > d:
                    G[a][b]["w"] = d
            else:
                G.add_edge(a, b, w=d, hw=hw)
            a = b
    # 记录 id→坐标
    G.graph["coords"] = {v: k for k, v in node_ids.items()}
    # 去除孤立节点（保留最大连通分量图做分析, 但返回全图）
    G.graph["largest_cc_nodes"] = max(nx.connected_components(G), key=len) if len(G) else set()
    return G

def snap_to_graph(G, lon, lat, k=1):
    """最近节点（只考虑当前图中存在的节点）"""
    best, bd = None, 1e18
    coords = G.graph.get("coords", {})
    for v, (x, y) in coords.items():
        if v not in G:
            continue
        d = dist_m(lon, lat, x, y)
        if d < bd:
            bd, best = d, v
    if best is None:
        # 图无坐标缓存时暴力找最近
        import math as _m
        for v in G.nodes:
            pass
        raise RuntimeError("graph has no coordinate registry")
    return best, bd

# ---------- 指标登记册 ----------
REGISTRY_PATH = os.path.join(HERE, "metrics_registry.json")

def registry_load():
    if os.path.exists(REGISTRY_PATH):
        return json.load(open(REGISTRY_PATH))
    return {"meta": {"title": "百年京张AI创新带 · KUN-SAL 指标登记册",
                     "purpose": "投稿中出现的每个数字必须在此登记", "generated": "2026-08-15"},
            "metrics": {}}

def registry_put(section, key, value, unit, method, interpretation, caveat="", sd=None, n=None):
    reg = registry_load()
    reg["metrics"][f"{section}.{key}"] = {
        "value": value, "unit": unit, "method": method,
        "interpretation": interpretation, "caveat": caveat,
    }
    if sd is not None:
        reg["metrics"][f"{section}.{key}"]["sd"] = sd
    if n is not None:
        reg["metrics"][f"{section}.{key}"]["n"] = n
    json.dump(reg, open(REGISTRY_PATH, "w"), ensure_ascii=False, indent=2)

def registry_report(section=None):
    reg = registry_load()
    m = reg["metrics"]
    if section:
        m = {k: v for k, v in m.items() if k.startswith(section + ".")}
    return m
