# -*- coding: utf-8 -*-
"""C4b · 托莱多式空间句法全套（京张三区对照 + POI 句法落位）
严格按 Toledo 手册定义：
  整合度 = (n-1)/Σd_ij（拓扑跳数, floyd_warshall）；选择度 = betweenness；连接度 = degree
  局部整合度 R3/R5 用 (k_R-1) 局部节点数归一（★不可用全局 n-1）
  可理解度 = r(connectivity, integration) 与 r(R3, global)
  结构判别（规模无关）：交叉口密度 / 整合度Gini / 核心集聚度 / 选择度Gini
  度量可达：400m/800m 可达节点数；半径剖面 R2..Rn
对照分区（约束重定义，不搬托莱多）：
  A 走廊带 = 遗址公园主脊两侧500m（铁路线有机肌理）
  B 高校大院带 = 学院路-五道口（大院肌理）
  C 网格新区 = 学知园以北清河带（规划网格肌理）
POI 落位：清华园车站/五道口/知春路/大钟寺/北京北/三朝圣地标/北大医学部/北航 → 句法百分位剖面
输出：计算/c4b_syntax_toledo.json + charts/c4b_syntax_zones.png + charts/c4b_syntax_poi.png
"""
import os, json, math, pickle
import numpy as np
import networkx as nx
from shapely.geometry import Point, Polygon
from shapely.ops import transform as sh_transform
import pyproj
from kun_common import setup_chinese_fonts, build_road_graph, snap_to_graph, registry_put

HERE = os.path.dirname(os.path.abspath(__file__))
CALC = os.path.join(HERE, "计算"); CHARTS = os.path.join(HERE, "charts")
os.makedirs(CALC, exist_ok=True); os.makedirs(CHARTS, exist_ok=True)

TRANS = pyproj.Transformer.from_crs(pyproj.CRS.from_epsg(4326), pyproj.CRS.from_epsg(4548), always_xy=True)
def to_m(g):
    def pr(x, y, z=None):
        a, b = TRANS.transform(x, y)
        return (a, b)
    return sh_transform(pr, g)

model = pickle.load(open(os.path.join(HERE, "site_model.pkl"), "rb"))
layers = model["layers"]
corridor = model["corridor"]

# 全路网图（含步行道 = network_type 'all'）→ 压缩二度节点（continuity 简化）
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
        w = G[v][a]["w"] + G[v][b]["w"]
        G.add_edge(a, b, w=w, hw=G[v][a].get("hw"))
        G.remove_node(v)
print("contracted network: nodes=%d edges=%d" % (len(G), len(G.edges)))

# 分区（WGS84 多边形 → 米制）
zone_wsg = {
    "A_heritage_corridor": (corridor.buffer(0.005)).intersection(model["site"]) if corridor is not None else None,
    "B_campus_belt": Polygon([(116.3405, 39.9785), (116.3560, 39.9785), (116.3560, 40.0005), (116.3405, 40.0005), (116.3405, 39.9785)]),
    "C_grid_newtown": Polygon([(116.3405, 40.0045), (116.3560, 40.0045), (116.3560, 40.0260), (116.3405, 40.0260), (116.3405, 40.0045)]),
}

def syntax_zone(G_full, poly_ll):
    """裁剪分区子图 → 取最大连通分量 → Toledo 全套指标"""
    # 判定用 WGS84 多边形 × WGS84 节点坐标（同空间比较）；面积另用米制
    nodes_in = [v for v in G_full.nodes if poly_ll.contains(Point(G_full.graph["coords"][v][0], G_full.graph["coords"][v][1]))]
    if len(nodes_in) < 30:
        return None
    pm = to_m(poly_ll)
    Gz = G_full.subgraph(nodes_in).copy()
    if not nx.is_connected(Gz):
        Gz = Gz.subgraph(max(nx.connected_components(Gz), key=len)).copy()
    nodes = list(Gz.nodes()); n = len(nodes)
    # 拓扑距离矩阵（跳数）
    D = nx.floyd_warshall_numpy(Gz, nodelist=nodes)
    rowsum = D.sum(axis=1)
    glob_int = (n - 1) / rowsum
    def local_int(R):
        li = np.zeros(n)
        for i in range(n):
            mask = D[i] <= R
            k = int(mask.sum())
            if k <= 1:
                continue
            li[i] = (k - 1) / D[i][mask].sum()
        return li
    li3 = local_int(3); li5 = local_int(5)
    bet = nx.betweenness_centrality(Gz, k=min(500, n), seed=42) if n > 1500 else nx.betweenness_centrality(Gz)
    bet_arr = np.array([bet[v] for v in nodes])
    conn = np.array([Gz.degree(v) for v in nodes])
    # 度量可达
    def metric_reach(limit):
        return np.array([sum(1 for vv, dd in nx.single_source_dijkstra_path_length(Gz, nd, weight="w").items()
                             if 0 < dd <= limit) for nd in nodes])
    r400 = metric_reach(400); r800 = metric_reach(800)
    # 结构判别指标
    def gini(x):
        x = np.sort(x[x > 0])
        if len(x) == 0:
            return 0.0
        return float((2 * np.arange(1, len(x) + 1) - len(x) - 1) @ x / (len(x) * x.sum()))
    int_gini = gini(glob_int); bet_gini = gini(bet_arr)
    int_count = sum(1 for v in nodes if Gz.degree(v) >= 3)
    area_km2 = to_m(poly_ll).area / 1e6
    # 核心集聚度：top10% 高整合度节点凸包面积 / 全区面积
    from shapely.geometry import MultiPoint
    top10 = np.argsort(-glob_int)[:max(3, n // 10)]
    pts = [Point(Gz.graph["coords"][nodes[i]][0], Gz.graph["coords"][nodes[i]][1]) for i in top10]
    hull_area = to_m(MultiPoint(pts).convex_hull).area if len(pts) >= 3 else 0.0
    core_conc = hull_area / pm.area if pm.area else 0.0
    # 可理解度
    r_c_i = float(np.corrcoef(conn, glob_int)[0, 1]) if n > 2 else 0.0
    r_r3_g = float(np.corrcoef(li3, glob_int)[0, 1]) if n > 2 else 0.0
    # 半径剖面
    profile = {}
    for R in (2, 3, 5, 7, 10):
        profile[f"R{R}"] = round(float(local_int(R).mean()), 5)
    # 平均路段长（米）
    seg_lens = [d["w"] for _, _, d in Gz.edges(data=True)]
    return {
        "n_nodes": n,
        "area_km2": round(area_km2, 2),
        "intersection_density_per_km2": round(int_count / area_km2, 1),
        "integration_mean": round(float(glob_int.mean()), 5),
        "integration_gini": round(int_gini, 4),
        "choice_gini": round(bet_gini, 4),
        "connectivity_mean": round(float(conn.mean()), 3),
        "intelligibility_r_conn_int": round(r_c_i, 3),
        "intelligibility_r_R3_global": round(r_r3_g, 3),
        "core_concentration": round(core_conc, 4),
        "reach_400m_mean": round(float(r400.mean()), 1),
        "reach_800m_mean": round(float(r800.mean()), 1),
        "mean_segment_length_m": round(float(np.mean(seg_lens)), 1) if seg_lens else 0,
        "radius_profile": profile,
        "zone_graph": Gz, "nodes": nodes, "glob_int": glob_int, "bet": bet_arr,
    }

zones = {}
for zid, poly in zone_wsg.items():
    if poly is None or poly.is_empty:
        continue
    r = syntax_zone(G, poly)
    if r:
        zones[zid] = r

# POI 句法落位（在全网 G 上，百分位 = 该节点整合度/选择度在全网的位置）
all_nodes = list(G.nodes())
D_full = nx.floyd_warshall_numpy(G, nodelist=all_nodes)
rowsum_full = D_full.sum(axis=1)
glob_int_full = (len(all_nodes) - 1) / rowsum_full
bet_full = nx.betweenness_centrality(G, k=600, seed=42)
bet_full_arr = np.array([bet_full[v] for v in all_nodes])

pois = [
    ("HER-QINGHUAYUAN", "清华园车站遗址", 116.3390, 39.9850, "heritage"),
    ("STA-WUDAOKOU", "五道口站", 116.3317, 39.9915, "transit"),
    ("STA-ZHICHUNLU", "知春路站", 116.3344, 39.9751, "transit"),
    ("STA-DAZHONGSI", "大钟寺站", 116.3390, 39.9653, "transit"),
    ("STA-BEIJINGBEI", "北京北站", 116.3462, 39.9459, "transit"),
    ("STA-QHDXK", "清华东路西口站", 116.3336, 39.9993, "transit"),
    ("STA-XUEYUANQIAO", "学院桥站", 116.3473, 39.9868, "transit"),
    ("STA-XUEZHIYUAN", "学知园站", 116.3458, 40.0136, "transit"),
    ("UNI-PKUHSC", "北京大学医学部", 116.3463, 39.9822, "campus"),
    ("UNI-BUAA", "北京航空航天大学", 116.3474, 39.9789, "campus"),
    ("UNI-CUPL", "中国政法大学研究生院", 116.3435, 39.9654, "campus"),
    ("LM-ORIGIN", "原点广场(概念)", 116.3430, 39.9850, "landmark"),
    ("LM-PHASE", "相变广场(概念)", 116.3330, 39.9915, "landmark"),
    ("LM-FRONT", "界面广场(概念)", 116.3402, 39.9646, "landmark"),
]
poi_rows = []
for pid, name, lon, lat, kind in pois:
    v, dist = snap_to_graph(G, lon, lat)
    if dist > 600:
        continue
    i = all_nodes.index(v)
    gi = float(glob_int_full[i]); bc = float(bet_full_arr[i])
    pct_i = float((glob_int_full <= gi).mean() * 100)
    pct_c = float((bet_full_arr <= bc).mean() * 100)
    poi_rows.append({"id": pid, "name": name, "kind": kind,
                     "integration": round(gi, 5), "integration_pct": round(pct_i, 1),
                     "choice": round(bc, 5), "choice_pct": round(pct_c, 1),
                     "dist_to_network_m": round(dist, 0)})

result = {
    "meta": {
        "model": "Toledo-style space syntax (segment-node graph, unweighted topological distance)",
        "notes": [
            "局部整合度用 (k_R-1) 局部节点数归一（Toledo手册§3.3纪律）",
            "路段节点图上可理解度弱/负相关为有机织物正常特征（§5.1），不下'更可读/更混乱'结论",
            "跨区比较用规模无关指标（交叉口密度/Gini/核心集聚度），整合度均值受规模混淆",
        ],
        "n_nodes_full": len(G),
    },
    "zones": {k: {kk: vv for kk, vv in v.items() if kk not in ("zone_graph", "nodes", "glob_int", "bet")} for k, v in zones.items()},
    "poi_syntax": poi_rows,
}
json.dump(result, open(os.path.join(CALC, "c4b_syntax_toledo.json"), "w"), ensure_ascii=False, indent=2)

# 登记关键指标
for zid, z in zones.items():
    registry_put("C4B_SYNTAX", f"{zid}_intersection_density", z["intersection_density_per_km2"], "1/km2",
                 "托莱多式交叉口密度（三岔以上）", f"{zid} 步行网格细密度",
                 caveat="OSM 路网口径；分区为分析对照定义（非官方分区）")
    registry_put("C4B_SYNTAX", f"{zid}_reach400", z["reach_400m_mean"], "count",
                 "400m 步行可达节点数均值", f"{zid} 人尺度步行可达性",
                 caveat="度量口径(米制最短路径)")
for p in poi_rows:
    registry_put("C4B_SYNTAX", f"poi_{p['id']}_int_pct", p["integration_pct"], "percentile",
                 "POI 句法落位：全网整合度百分位", f"{p['name']} 整合度百分位（类似托莱多城门98.3%的读法）",
                 caveat="segment-node 图口径；POI 坐标精度为公开口径")

# ---- 图 ----
plt = setup_chinese_fonts()
fig, axes = plt.subplots(1, 2, figsize=(14, 5.6))
zlabels = {"A_heritage_corridor": "A 走廊带(铁路肌理)", "B_campus_belt": "B 高校大院带(大院肌理)", "C_grid_newtown": "C 网格新区(规划肌理)"}
xs = np.arange(len(zones))
dens = [zones[z]["intersection_density_per_km2"] for z in zones]
r400 = [zones[z]["reach_400m_mean"] for z in zones]
ax = axes[0]
ax.bar(xs - 0.18, dens, 0.36, label="交叉口密度/km²", color="#5b8dd9")
ax2b = ax.twinx()
ax2b.bar(xs + 0.18, r400, 0.36, label="400m可达节点数", color="#5fbf77")
ax.set_xticks(xs); ax.set_xticklabels([zlabels[z] for z in zones], fontsize=9)
ax.set_title("图 C4b-1 · 三区步行粒度对照（人尺度）")
ax.set_ylabel("交叉口密度/km²"); ax2b.set_ylabel("400m可达节点数")
ax.axhline(200, color="#c0392b", ls="--", lw=1, label="老城基准>200")
ax.axhline(80, color="#e67e22", ls="--", lw=1, label="车本新城<80")
ax.legend(loc="upper left", fontsize=8)
ax2 = axes[1]
names = [p["name"] for p in poi_rows]
pcts = [p["integration_pct"] for p in poi_rows]
colors = ["#c0392b" if p >= 80 else ("#f39c12" if p >= 50 else "#7f8c8d") for p in pcts]
ax2.barh(range(len(names))[::-1], pcts[::-1], color=colors[::-1])
ax2.axvline(50, color="#999", ls=":", lw=1)
ax2.set_yticks(range(len(names))[::-1]); ax2.set_yticklabels(names[::-1], fontsize=8.5)
ax2.set_xlabel("全网整合度百分位(%)")
ax2.set_title("图 C4b-2 · POI 句法落位：谁是京张的『比萨格拉门』？")
fig.suptitle("图 C4b · 托莱多式空间句法：配置如何塑造运动（京张实证）", fontweight="bold", fontsize=13.5)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "c4b_syntax.png"), dpi=150, bbox_inches="tight")
print(json.dumps(result["zones"], ensure_ascii=False, indent=1))
print("POI syntax:")
for p in poi_rows:
    print(f"  {p['name']}: int_pct={p['integration_pct']}% choice_pct={p['choice_pct']}%")
