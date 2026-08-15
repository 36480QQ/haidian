# -*- coding: utf-8 -*-
"""C2 · 京张公园走廊断点 + 蓝绿网络渗流分析（REAL vs DESIGN）
修正口径（回应公告任务『聚焦公园慢行系统断点』）：
  C2a 走廊断点：遗址公园走廊(废弃铁路/京包线)与主干路以上道路的交点 = 慢行断点候选
  C2b 蓝绿渗流：仅绿地+公园走廊斑块（不含普通步行道）100m 缓冲邻接，
      巨分量面积占比 vs p_c≈59.27%；DESIGN 在真实断点处缝合后重算
输出：计算/c2_percolation.json + charts/c2_percolation.png
"""
import os, json, pickle, math
import numpy as np
import networkx as nx
from shapely.geometry import LineString, Point
from shapely.ops import transform as sh_transform
import pyproj
from kun_common import setup_chinese_fonts, registry_put

HERE = os.path.dirname(os.path.abspath(__file__))
CALC = os.path.join(HERE, "计算"); CHARTS = os.path.join(HERE, "charts")
os.makedirs(CALC, exist_ok=True); os.makedirs(CHARTS, exist_ok=True)

TRANS = pyproj.Transformer.from_crs(pyproj.CRS.from_epsg(4326), pyproj.CRS.from_epsg(4548), always_xy=True)
P_C = 0.5927
BUFFER_M = 100.0

def to_m(g):
    def pr(x, y, z=None):
        a, b = TRANS.transform(x, y)
        return (a, b)
    return sh_transform(pr, g)

model = pickle.load(open(os.path.join(HERE, "site_model.pkl"), "rb"))
layers = model["layers"]
corridor = model["corridor"]

# ---- C2a 走廊断点 ----
major_hw = {"motorway", "trunk", "primary", "secondary"}
major_roads = []
for e, g in layers["roads"]:
    if e.get("tags", {}).get("highway") in major_hw and g.geom_type == "LineString":
        t = e.get("tags", {})
        major_roads.append((t.get("name", "") or t.get("ref", "") or "主干路", g))

crossings = []
if corridor is not None and not corridor.is_empty:
    lines = [corridor] if corridor.geom_type == "LineString" else list(corridor.geoms)
    for nm, rg in major_roads:
        for ln in lines:
            x = ln.intersection(rg)
            pts = []
            if x.geom_type == "Point":
                pts = [x]
            elif x.geom_type == "MultiPoint":
                pts = list(x.geoms)
            for p in pts:
                crossings.append({"road": str(nm)[:20], "lon": round(p.x, 5), "lat": round(p.y, 5)})

# 去重（20m 内合并）
uniq = []
for c in crossings:
    dup = False
    for u in uniq:
        if abs(u["lon"] - c["lon"]) < 0.00025 and abs(u["lat"] - c["lat"]) < 0.00025:
            u["roads"] = u.get("roads", [u["road"]]) + [c["road"]]
            dup = True
            break
    if not dup:
        uniq.append(dict(c))
uniq.sort(key=lambda c: -c["lat"])
for u in uniq:
    u.pop("road", None)

# 走廊分段（被断点切开后各段长度）
corridor_len_m = 0.0
seg_lens = []
if corridor is not None and not corridor.is_empty:
    lines = [corridor] if corridor.geom_type == "LineString" else list(corridor.geoms)
    for ln in lines:
        corridor_len_m += to_m(ln).length
        # 按断点切段
        coords = list(ln.coords)
        cut = [0.0] + [ln.project(Point(c["lon"], c["lat"])) for c in uniq
                       if ln.distance(Point(c["lon"], c["lat"])) < 0.001] + [ln.length]
        cut = sorted(set(round(v, 6) for v in cut))
        for i in range(len(cut) - 1):
            seg = ln.interpolate(cut[i]).distance(ln.interpolate(cut[i + 1]))
            deg = abs(cut[i + 1] - cut[i])
            seg_lens.append(to_m(LineString([ln.interpolate(cut[i]), ln.interpolate(cut[i + 1])])).length)

# ---- C2b 蓝绿渗流（绿地+公园走廊，不含普通步行道）----
patches = []
if corridor is not None and not corridor.is_empty:
    lines = [corridor] if corridor.geom_type == "LineString" else list(corridor.geoms)
    for i, ln in enumerate(lines):
        coords = list(ln.coords)
        for k in range(len(coords) - 1):
            patches.append((f"PARK-{i:02d}-{k:03d}", "遗址公园走廊段",
                            to_m(LineString([coords[k], coords[k + 1]])).buffer(15.0), "park"))
for i, (e, g) in enumerate(layers["green"]):
    if g.geom_type not in ("Polygon", "MultiPolygon"):
        continue
    gm = to_m(g)
    if gm.area < 200:
        continue
    t = e.get("tags", {})
    patches.append((f"GRN-{i:03d}", str(t.get("name", "") or "绿地")[:14], gm, "green"))

n_p = len(patches)
areas = np.array([p[2].area for p in patches])
total = areas.sum()

def build_graph(patches):
    Gx = nx.Graph()
    Gx.add_nodes_from(range(len(patches)))
    for i in range(len(patches)):
        bi = patches[i][2].buffer(BUFFER_M)
        for j in range(i + 1, len(patches)):
            if bi.intersects(patches[j][2]):
                Gx.add_edge(i, j)
    return Gx

def analyze(Gx, label):
    comps = sorted(nx.connected_components(Gx), key=len, reverse=True)
    giant = comps[0] if comps else set()
    frac = sum(areas[i] for i in giant) / total if total else 0.0
    return {"label": label, "n_patches": n_p, "n_components": len(comps),
            "giant_fraction_area": round(float(frac), 4),
            "above_threshold": bool(frac > P_C), "p_c": P_C,
            "components_sizes_top8": [len(c) for c in comps[:8]]}

G = build_graph(patches)
real = analyze(G, "REAL_蓝绿现状")
# 断点（分量间最近距离，<800m）
comps = sorted(nx.connected_components(G), key=len, reverse=True)[:8]
gaps = []
for a in range(len(comps)):
    for b in range(a + 1, len(comps)):
        best = 1e18; bp = None
        for i in comps[a]:
            for j in comps[b]:
                d = patches[i][2].distance(patches[j][2])
                if d < best:
                    best = d; bp = (i, j)
        if best < 800:
            gaps.append((best, bp))
gaps.sort()
# DESIGN：缝合前 N 处断点
Gd = G.copy()
for best, (i, j) in gaps[:8]:
    Gd.add_edge(i, j, stitch=True)
design = analyze(Gd, "DESIGN_缝合后")

result = {
    "meta": {
        "model": "C2a 走廊断点识别 + C2b 蓝绿网络渗流（Batty 式代理）",
        "p_c": P_C, "adjacency_buffer_m": BUFFER_M,
        "corridor_total_length_m": round(corridor_len_m, 1),
        "note": "断点仅按几何与道路等级识别；标高/权属/交通管制约束待正式数据补齐",
    },
    "c2a_corridor": {
        "n_crossings_with_major_roads": len(uniq),
        "crossings": uniq,
        "segment_lengths_m": [round(v, 1) for v in sorted(seg_lens, reverse=True)],
        "max_gap_segment_m": round(max(seg_lens), 1) if seg_lens else None,
    },
    "c2b_real": real,
    "c2b_design": design,
    "stitch_targets": [{"dist_m": round(g[0], 1), "from": patches[g[1][0]][0], "to": patches[g[1][1]][0],
                        "kind_from": patches[g[1][0]][1], "kind_to": patches[g[1][1]][1]} for g in gaps[:8]],
}
json.dump(result, open(os.path.join(CALC, "c2_percolation.json"), "w"), ensure_ascii=False, indent=2)

registry_put("C2_PERC", "corridor_n_road_crossings", len(uniq), "count",
             "遗址公园走廊与主干路以上道路的交叉断点数",
             "对应公告『聚焦公园慢行系统断点』；断点即设计缝合靶点",
             caveat="几何口径，未含标高/交通管制")
registry_put("C2_PERC", "bluegreen_real_giant_fraction", real["giant_fraction_area"], "ratio",
             "蓝绿网络（绿地+公园走廊）巨分量面积占比 REAL",
             f"现状{'超' if real['above_threshold'] else '亚'}临界({P_C})",
             caveat="斑块网络非规则格点，p_c 为启发代理")
registry_put("C2_PERC", "bluegreen_design_giant_fraction", design["giant_fraction_area"], "ratio",
             "蓝绿网络巨分量面积占比 DESIGN（缝合8处断点后）",
             "设计缝合的量化效果",
             caveat="缝合为概念连接")

plt = setup_chinese_fonts()
fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
for ax, d in zip(axes, [real, design]):
    sizes = d["components_sizes_top8"]
    ax.bar(range(len(sizes)), sizes, color="#2e9e6b" if d["label"].startswith("DESIGN") else "#b08a4f")
    ax.set_title(f"{d['label']}\n分量数={d['n_components']}  巨分量面积占比={d['giant_fraction_area']*100:.1f}%  (临界 59.3%)")
    ax.set_xlabel("连通分量（按大小排序）"); ax.set_ylabel("分量内斑块数")
fig.suptitle("图 C2 · 蓝绿网络渗流：现状 vs 设计缝合", fontweight="bold", fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "c2_percolation.png"), dpi=150, bbox_inches="tight")
print("corridor crossings:", len(uniq))
for u in uniq:
    print("  ", u)
print(json.dumps(real, ensure_ascii=False))
print(json.dumps(design, ensure_ascii=False))
print("stitch targets:")
for s in result["stitch_targets"]:
    print("  ", s)
