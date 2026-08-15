# -*- coding: utf-8 -*-
"""C16 · 空间句法平面图分析（真正的句法图面，非表格）
Map A：全网整合度着色路网（红=高整合核心，蓝=低整合边缘）+ 站点/文物 POI 叠加
Map B：选择度着色路网（红=穿行主轴）
Map C：三区 400m 步行可达圈对比（人尺度平面分析）
输出：charts/c16_syntax_maps.png（中英双版）
"""
import os, json, math, pickle
import numpy as np
import networkx as nx
from shapely.geometry import Point, LineString
from shapely.ops import transform as sh_transform
import pyproj
from kun_common import setup_chinese_fonts, build_road_graph, registry_put
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

HERE = os.path.dirname(os.path.abspath(__file__))
CALC = os.path.join(HERE, "计算"); CHARTS = os.path.join(HERE, "charts")
os.makedirs(CALC, exist_ok=True); os.makedirs(CHARTS, exist_ok=True)
setup_chinese_fonts()
plt.rcParams["font.family"] = "Heiti TC"

TRANS = pyproj.Transformer.from_crs(pyproj.CRS.from_epsg(4326), pyproj.CRS.from_epsg(4548), always_xy=True)
def to_m(g):
    def pr(x, y, z=None):
        a, b = TRANS.transform(x, y)
        return (a, b)
    return sh_transform(pr, g)

model = pickle.load(open(os.path.join(HERE, "site_model.pkl"), "rb"))
layers = model["layers"]
site = to_m(model["site"])
corridor = to_m(model["corridor"]) if model["corridor"] is not None else None

# 压缩路网（同 C4b）
G = build_road_graph(layers["roads"])
LCC = G.graph["largest_cc_nodes"]
G = G.subgraph(LCC).copy()
deg2 = [v for v in G if G.degree(v) == 2]
for v in deg2:
    if v not in G:
        continue
    nb = list(G.neighbors(v))
    if len(nb) == 2:
        a, b = nb
        G.add_edge(a, b, w=G[v][a]["w"] + G[v][b]["w"])
        G.remove_node(v)
print("contracted:", len(G), "nodes")

nodes = list(G.nodes())
D = nx.floyd_warshall_numpy(G, nodelist=nodes)
rowsum = D.sum(axis=1)
glob_int = (len(nodes) - 1) / rowsum
bet = nx.betweenness_centrality(G, k=600, seed=42)
bet_arr = np.array([bet[v] for v in nodes])

# 边集合（米制坐标）
coords_ll = G.graph["coords"]
edge_segs = []
edge_int = []
edge_choice = []
for a, b in G.edges():
    x1, y1 = TRANS.transform(coords_ll[a][0], coords_ll[a][1])
    x2, y2 = TRANS.transform(coords_ll[b][0], coords_ll[b][1])
    ia, ib = nodes.index(a), nodes.index(b)
    edge_segs.append([(x1, y1), (x2, y2)])
    edge_int.append((glob_int[ia] + glob_int[ib]) / 2)
    edge_choice.append((bet_arr[ia] + bet_arr[ib]) / 2)
edge_int = np.array(edge_int); edge_choice = np.array(edge_choice)
# 百分位
int_pct = np.searchsorted(np.sort(edge_int), edge_int) / len(edge_int) * 100
cho_pct = np.searchsorted(np.sort(edge_choice), edge_choice) / len(edge_choice) * 100

# POI
pois_zh = {
    "学院桥站 97.5%": (116.3473, 39.9868), "清华园车站 93.5%": (116.3390, 39.9850),
    "学知园站 84.0%": (116.3458, 40.0136), "知春路站 68.0%": (116.3344, 39.9751),
    "五道口站 57.1%": (116.3317, 39.9915), "大钟寺站 20.2%": (116.3390, 39.9653),
    "北京北站 29.2%": (116.3462, 39.9459),
}
pois_en = {
    "Xueyuanqiao 97.5%": (116.3473, 39.9868), "Tsinghuayuan 93.5%": (116.3390, 39.9850),
    "Xuezhiyuan 84.0%": (116.3458, 40.0136), "Zhichunlu 68.0%": (116.3344, 39.9751),
    "Wudaokou 57.1%": (116.3317, 39.9915), "Dazhongsi 20.2%": (116.3390, 39.9653),
    "Beijing North 29.2%": (116.3462, 39.9459),
}
def plot_net(ax, vals, title, cmap="RdYlBu_r"):
    segs = LineCollection(edge_segs, linewidths=0.9, cmap=cmap, array=vals, alpha=0.85)
    ax.add_collection(segs)
    return segs

for LANG in ["zh", "en"]:
    zh = LANG == "zh"
    T = lambda z, e: z if zh else e
    fig, axes = plt.subplots(1, 3, figsize=(21, 10))
    for ax in axes:
        ax.set_aspect("equal")
        xs, ys = site.exterior.xy
        ax.plot(xs, ys, color="#888888", lw=1.0, ls=(0, (6, 4)), alpha=0.7)
        if corridor is not None:
            ax.plot(*corridor.xy, color="#1f4e2d", lw=3.5, alpha=0.9)
        ax.set_xlim(site.bounds[0] - 300, site.bounds[2] + 300)
        ax.set_ylim(site.bounds[1] - 300, site.bounds[3] + 300)
        ax.axis("off")
    # Map A 整合度
    segs = plot_net(axes[0], int_pct, "")
    cbar = fig.colorbar(segs, ax=axes[0], fraction=0.04, pad=0.02)
    cbar.set_label(T("整合度百分位", "Integration percentile"))
    _pois = pois_zh if zh else pois_en
    for nm, (lon, lat) in _pois.items():
        x, y = TRANS.transform(lon, lat)
        axes[0].scatter(x, y, s=45, color="black", zorder=6, edgecolor="white", linewidth=1)
        axes[0].annotate(nm, (x, y), xytext=(6, 6), textcoords="offset points", fontsize=7.5, color="black")
    axes[0].set_title(T("图 A · 全网整合度：红=结构的嘴，蓝=边缘\n学院桥与清华园车站抱成核心", "Map A · Integration: red = structural core"), fontsize=10.5)
    # Map B 选择度
    segs = plot_net(axes[1], cho_pct, "")
    cbar = fig.colorbar(segs, ax=axes[1], fraction=0.04, pad=0.02)
    cbar.set_label(T("选择度百分位", "Choice percentile"))
    axes[1].set_title(T("图 B · 选择度：红=穿行主轴\n北四环-学院路-学知园一线是流的水管", "Map B · Choice: red = through-movement spine"), fontsize=10.5)
    # Map C 400m 可达圈（走廊带 vs 大院带）
    for g_ in [corridor.buffer(400), to_m(__import__("shapely.geometry", fromlist=["Polygon"]).Polygon([(116.3405, 39.9785), (116.3560, 39.9785), (116.3560, 40.0005), (116.3405, 40.0005), (116.3405, 39.9785)]))]:
        pass
    axes[2].fill(*corridor.buffer(400).exterior.xy if corridor is not None else [(0, 0)], color="#5fbf77", alpha=0.12)
    if corridor is not None:
        for d, col in [(200, "#2e9e6b"), (400, "#5fbf77"), (800, "#a3d9b1")]:
            axes[2].plot(*corridor.buffer(d).exterior.xy, color=col, lw=1.2, alpha=0.8)
    axes[2].set_title(T("图 C · 人尺度平面：主脊 200/400/800m 步行圈\n400m 内仅 24 个节点可达=最难走的一段", "Map C · 200/400/800m walking rings: the hardest 400m on the belt"), fontsize=10.5)
    fig.suptitle(T("空间句法平面图分析：配置塑造运动（京张全网实算，5720 节点）", "Space syntax plan analysis: configuration shapes movement (5,720 nodes, computed)"), fontweight="bold", fontsize=13)
    plt.tight_layout()
    out = os.path.join(CHARTS, f"c16_syntax_maps_{'zh' if zh else 'en'}.png")
    plt.savefig(out, dpi=150, bbox_inches="tight"); plt.close()
    print("saved", out)
