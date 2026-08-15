# -*- coding: utf-8 -*-
"""C4 · 空间句法整合度/选择度（REAL vs DESIGN 公园主脊贯通）
口径（如实声明为代理）：
  - OSM 路网 → 压缩二度节点为"路链图"（continuity 简化，米制边长）
  - 整合度代理 = (N-1)/Σd（多源 Dijkstra 精确计算，仅对关键锚点）
  - 选择度代理 = sampled betweenness (k=400)（全图排名用）
  - DESIGN = 遗址公园走廊作为概念慢行主脊接入（断点缝合节点，60m 等价阻抗）
输出：计算/c4_syntax.json + charts/c4_syntax.png
"""
import os, json, pickle
import numpy as np
import networkx as nx
from kun_common import setup_chinese_fonts, build_road_graph, snap_to_graph, registry_put

HERE = os.path.dirname(os.path.abspath(__file__))
CALC = os.path.join(HERE, "计算"); CHARTS = os.path.join(HERE, "charts")
os.makedirs(CALC, exist_ok=True); os.makedirs(CHARTS, exist_ok=True)

model = pickle.load(open(os.path.join(HERE, "site_model.pkl"), "rb"))
layers = model["layers"]
corridor = model["corridor"]

G = build_road_graph(layers["roads"])
LCC = G.graph["largest_cc_nodes"]
G = G.subgraph(LCC).copy()

# 压缩二度节点
deg2 = [v for v in G if G.degree(v) == 2]
for v in deg2:
    if v not in G:
        continue
    nb = list(G.neighbors(v))
    if len(nb) == 2:
        a, b = nb
        w = G[v][a]["w"] + G[v][b]["w"]
        G.add_edge(a, b, w=w, hw=G[v][a].get("hw"))
        G.remove_node(v)
print("contracted graph: nodes=%d edges=%d" % (len(G), len(G.edges)))

def integration_of(Gx, node_v):
    """精确整合度代理：(N-1)/Σd(v,u)"""
    lens = nx.single_source_dijkstra_path_length(Gx, node_v, weight="w")
    n = len(Gx)
    total = sum(lens.values())
    return (n - 1) / total if total > 0 else 0.0

anchors = {
    "五道口站": (116.3317, 39.9915),
    "知春路站": (116.3344, 39.9751),
    "清华东路西口站": (116.3336, 39.9993),
    "大钟寺站": (116.3390, 39.9653),
    "学院桥站": (116.3473, 39.9868),
    "学知园站": (116.3458, 40.0136),
    "北京北站": (116.3462, 39.9459),
}

def anchor_integrations(Gx):
    out = {}
    for nm, (lon, lat) in anchors.items():
        v, _ = snap_to_graph(Gx, lon, lat)
        out[nm] = integration_of(Gx, v)
    return out

real_int = anchor_integrations(G)
bc = nx.betweenness_centrality(G, weight="w", normalized=True, k=400, seed=42)
top_bc = sorted(bc.items(), key=lambda kv: -kv[1])[:8]
top_bc_named = []
for v, b in top_bc:
    x, y = G.graph["coords"].get(v, (0, 0))
    top_bc_named.append({"node": v, "betweenness": round(b, 6), "lon": x, "lat": y})

# DESIGN：公园主脊接入
Gd = G.copy()
spine_pts = []
if corridor is not None and not corridor.is_empty:
    lines = [corridor] if corridor.geom_type == "LineString" else list(corridor.geoms)
    for ln in lines:
        total = ln.length
        n = max(3, int(total / 0.0012))
        for k in range(n + 1):
            p = ln.interpolate(total * k / n)
            spine_pts.append(p)
snapped = []
for p in spine_pts:
    v, _ = snap_to_graph(Gd, p.x, p.y)
    snapped.append(v)
# 沿脊顺序连边（断点处自然跨过道路——概念缝合）
prev = None
spine_edges = 0
for v in snapped:
    if prev is not None and v != prev:
        if not Gd.has_edge(prev, v):
            Gd.add_edge(prev, v, w=60.0, spine=True)
            spine_edges += 1
    prev = v
design_int = anchor_integrations(Gd)

result = {
    "meta": {
        "model": "continuity-contracted segment graph (OSM, EPSG:4548 weights)",
        "proxy_note": "整合度=(N-1)/Σd（锚点精确）；选择度=sampled betweenness k=400；设计脊=概念缝合(60m等价阻抗)",
        "n_nodes_contracted_real": len(G),
        "n_nodes_design": len(Gd),
        "spine_edges_added": spine_edges,
    },
    "real": {"anchor_integration": {k: round(v, 6) for k, v in real_int.items()},
             "top_betweenness_nodes": top_bc_named,
             "anchor_rank": sorted(real_int.items(), key=lambda kv: -kv[1])},
    "design": {"anchor_integration": {k: round(v, 6) for k, v in design_int.items()},
               "delta_vs_real": {k: round(design_int[k] - real_int[k], 6) for k in anchors}},
}
json.dump(result, open(os.path.join(CALC, "c4_syntax.json"), "w"), ensure_ascii=False, indent=2)

for nm in anchors:
    registry_put("C4_SYNTAX", f"integration_real_{nm}", round(real_int[nm], 6), "1/m",
                 "整合度代理 (N-1)/Σd（continuity 压缩图，多源Dijkstra精确）",
                 f"{nm} 现状整合度",
                 caveat="代理口径（节点整合度，非完整轴向分析）")
    registry_put("C4_SYNTAX", f"integration_design_{nm}", round(design_int[nm], 6), "1/m",
                 "整合度代理（DESIGN 公园主脊贯通后）",
                 f"{nm} 设计后整合度",
                 caveat="设计脊为概念接入")

plt = setup_chinese_fonts()
names = list(anchors.keys())
x = np.arange(len(names))
w = 0.36
fig, ax = plt.subplots(figsize=(11.5, 5.2))
ax.bar(x - w / 2, [real_int[n] for n in names], w, label="REAL 现状", color="#b08a4f")
ax.bar(x + w / 2, [design_int[n] for n in names], w, label="DESIGN 公园主脊贯通后", color="#2e9e6b")
ax.set_xticks(x); ax.set_xticklabels(names, rotation=15)
ax.set_ylabel("整合度 (N-1)/Σd  [1/m]")
ax.set_title("图 C4 · 空间句法：一带关键节点整合度变化（概念口径）")
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "c4_syntax.png"), dpi=150, bbox_inches="tight")
print("anchor integration REAL:", json.dumps({k: round(v, 6) for k, v in real_int.items()}, ensure_ascii=False))
print("anchor integration DESIGN:", json.dumps({k: round(v, 6) for k, v in design_int.items()}, ensure_ascii=False))
print("delta:", json.dumps({k: round(design_int[k] - real_int[k], 6) for k in anchors}, ensure_ascii=False))
print("anchor rank REAL:", [k for k, v in sorted(real_int.items(), key=lambda kv: -kv[1])])
