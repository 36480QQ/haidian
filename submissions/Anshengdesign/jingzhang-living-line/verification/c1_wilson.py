# -*- coding: utf-8 -*-
"""C1 · Wilson 空间交互 λ 标定（双口径：直线 + OSM 路网距离）
参照 KUN 手册 §2.1：T_ij = K·O_i·D_j / f(d_ij)，相变临界 λ_c ≈ 0.42（Crosato et al. 2018）。
实现口径（如实声明为代理）：
  - 节点 = 三区 + 两翼 + 锚点（轨道站/高校/文保）
  - 耦合 λ_ij = exp(-d_ij / d0)，d0 = 2500 m = 官方"十分钟创新圈"半径（海淀区 2026-07-29 发布会口径：
    原点社区"形成了'十分钟创新圈'"；按骑行 15 km/h × 10 min = 2.5 km）
  - λ_ij > λ_c=0.42 ⇔ 路网距离 < d0·ln(1/0.42) ≈ 2170 m
  - 输出：①全部配对超临界占比 ②三区两翼 5 核的超临界连通分量（全局协同是否达成）
  - 两口径：直线 vs OSM 路网最短路径；路网不通对回退直线×1.3 迂回系数（登记 caveat）
输出：计算/c1_wilson.json + charts/c1_wilson.png
"""
import os, json, math, pickle
import numpy as np
import networkx as nx
from kun_common import setup_chinese_fonts, build_road_graph, dist_m, snap_to_graph, registry_put

HERE = os.path.dirname(os.path.abspath(__file__))
CALC = os.path.join(HERE, "计算"); CHARTS = os.path.join(HERE, "charts")
os.makedirs(CALC, exist_ok=True); os.makedirs(CHARTS, exist_ok=True)

model = pickle.load(open(os.path.join(HERE, "site_model.pkl"), "rb"))
keys = model["key_geoms"]
layers = model["layers"]

LAMBDA_C = 0.42
D0 = 2500.0          # 十分钟创新圈（官方口径锚点）
DETOUR = 1.3         # 路网不通时的迂回系数

def centroid(g):
    return g.centroid.x, g.centroid.y

nodes = []
for fid, area_id, zh in [
    ("PROV-KEY-001", "zhongzhiyuan_ai_acceleration_area", "众智园AI自主创新加速区"),
    ("PROV-KEY-002", "beijing_ai_origin_community", "北京AI原点社区"),
    ("PROV-KEY-003", "dazhongsi_ai_industry_cluster", "大钟寺AI产业集聚区"),
]:
    g = keys[fid]
    nodes.append({"id": area_id, "zh": zh, "lon": g.centroid.x, "lat": g.centroid.y,
                  "mass": 1.0, "kind": "key_area"})
nodes += [
    {"id": "zhongguancun_tech_service_wing", "zh": "中关村科技服务翼", "lon": 116.3237, "lat": 39.9797, "mass": 1.0, "kind": "wing"},
    {"id": "xiaoyuehe_scenario_wing", "zh": "小月河场景赋能翼", "lon": 116.3569, "lat": 39.9777, "mass": 1.0, "kind": "wing"},
]
for aid, zh, lon, lat in [
    ("STA-WUDAOKOU", "五道口站", 116.3317, 39.9915),
    ("STA-DAZHONGSI", "大钟寺站", 116.3390, 39.9653),
    ("STA-ZHICHUNLU", "知春路站", 116.3344, 39.9751),
    ("STA-QHDXK", "清华东路西口站", 116.3336, 39.9993),
    ("STA-XUEYUANQIAO", "学院桥站", 116.3473, 39.9868),
    ("STA-XUEZHIYUAN", "学知园站", 116.3458, 40.0136),
    ("STA-BEIJINGBEI", "北京北站", 116.3462, 39.9459),
    ("STA-XITUCHENG", "西土城站", 116.3478, 39.9749),
    ("UNI-PKUHSC", "北京大学医学部", 116.3463, 39.9822),
    ("UNI-BUAA", "北京航空航天大学", 116.3474, 39.9789),
    ("HER-QINGHUAYUAN", "清华园车站遗址", 116.3390, 39.9850),
]:
    nodes.append({"id": aid, "zh": zh, "lon": lon, "lat": lat, "mass": 1.0, "kind": "anchor"})

N = len(nodes)
D_euc = np.zeros((N, N))
for i in range(N):
    for j in range(N):
        D_euc[i, j] = dist_m(nodes[i]["lon"], nodes[i]["lat"], nodes[j]["lon"], nodes[j]["lat"])

G = build_road_graph(layers["roads"])
node_idx = {}
for i, nd in enumerate(nodes):
    v, _ = snap_to_graph(G, nd["lon"], nd["lat"])
    node_idx[i] = v
sp = dict(nx.all_pairs_dijkstra_path_length(G, weight="w"))
D_net = np.zeros((N, N))
detour_used = 0
for i in range(N):
    for j in range(N):
        if i == j:
            continue
        d = sp.get(node_idx[i], {}).get(node_idx[j])
        if d is None:
            D_net[i, j] = D_euc[i, j] * DETOUR
            detour_used += 1
        else:
            D_net[i, j] = d

lam_euc = np.exp(-D_euc / D0)
lam_net = np.exp(-D_net / D0)
np.fill_diagonal(lam_euc, 0); np.fill_diagonal(lam_net, 0)
n_pairs = N * (N - 1)
f_euc = float((lam_euc > LAMBDA_C).sum() / n_pairs)
f_net = float((lam_net > LAMBDA_C).sum() / n_pairs)

# 5 核（三区+两翼）超临界连通分量（路网口径）
core_idx = [i for i, nd in enumerate(nodes) if nd["kind"] in ("key_area", "wing")]
Gc = nx.Graph()
for i in core_idx:
    Gc.add_node(i)
for i in core_idx:
    for j in core_idx:
        if i < j and lam_net[i, j] > LAMBDA_C:
            Gc.add_edge(i, j)
core_comps = sorted(nx.connected_components(Gc), key=len, reverse=True)
giant = core_comps[0] if core_comps else set()
core_span = len(giant) / len(core_idx) if core_idx else 0.0
core_connected = (len(giant) == len(core_idx))
core_names = {i: nodes[i]["zh"] for i in core_idx}

pairs = []
for i in core_idx:
    for j in core_idx:
        if i < j:
            pairs.append({
                "pair": f"{nodes[i]['zh']}×{nodes[j]['zh']}",
                "d_net_m": round(float(D_net[i, j]), 0),
                "lambda_net": round(float(lam_net[i, j]), 4),
                "above_critical": bool(lam_net[i, j] > LAMBDA_C),
            })

result = {
    "meta": {
        "model": "Wilson spatial interaction (entropy-maximizing)",
        "formula": "λ_ij = exp(-d_ij/d0), d0=2500m（官方『十分钟创新圈』，海淀区2026-07-29发布会）",
        "critical_coupling": LAMBDA_C,
        "critical_distance_m": round(D0 * math.log(1 / LAMBDA_C), 0),
        "proxy_note": "代理口径；λ>0.42 等价于路网距离<≈2170m。路网不通对回退直线×1.3（迂回系数）",
        "nodes_n": N,
        "detour_pairs": detour_used,
    },
    "supercritical_fraction": {
        "euc": {"value_pct": round(f_euc * 100, 3)},
        "net": {"value_pct": round(f_net * 100, 3)},
        "scale_caveat": "本组节点为带内尺度(2–9km)；长三角四城 0.19%–0.49% 窄带为区域尺度，仅作量级参照不作直接对比",
    },
    "core_5_network": {
        "giant_component_size": len(giant),
        "core_nodes": len(core_idx),
        "core_span_ratio": round(core_span, 3),
        "globally_connected": core_connected,
        "components": [{"members": sorted(core_names[i] for i in c)} for c in core_comps],
    },
    "core_pairs": pairs,
    "nodes": [{"id": nd["id"], "zh": nd["zh"], "kind": nd["kind"]} for nd in nodes],
}
json.dump(result, open(os.path.join(CALC, "c1_wilson.json"), "w"), ensure_ascii=False, indent=2)

registry_put("C1_WILSON", "supercritical_fraction_net_pct", round(f_net * 100, 3), "%",
             "λ_ij=exp(-d_ij/2500m)>0.42 配对占比（OSM路网最短路径口径）",
             "现状超临界配对占比；核心判据为三区两翼是否构成全局连通",
             caveat="代理口径；区域尺度窄带仅量级参照")
registry_put("C1_WILSON", "core_span_ratio", round(core_span, 3), "ratio",
             "三区两翼5核超临界连通分量的最大分量占比（路网口径）",
             "5核全局协同度：=1 表示三区两翼在十分钟创新圈耦合下全部连通",
             caveat="λ_c=0.42 引自 Crosato et al. 2018；耦合定义为距离指数衰减代理")

# ---- 图 ----
plt = setup_chinese_fonts()
fig, axes = plt.subplots(1, 2, figsize=(13, 5.4))
for ax, (lam, title) in zip(axes, [(lam_euc, "直线口径"), (lam_net, "OSM路网口径")]):
    vals = lam[lam > 0].ravel()
    ax.hist(vals, bins=30, color="#2f6fed", alpha=0.85)
    ax.axvline(LAMBDA_C, color="#c0392b", lw=2, ls="--", label=f"相变临界 λc={LAMBDA_C}")
    ax.set_title(f"配对耦合分布 · {title}\n超临界占比 {round(float((vals > LAMBDA_C).mean() * 100), 2)}%")
    ax.set_xlabel("λ_ij = exp(-d_ij/2500m)"); ax.set_ylabel("配对数量")
    ax.legend()
fig.suptitle("图 C1 · 空间交互 λ 标定（现状）：5核全局连通=%s" % ("是" if core_connected else "否"),
             fontweight="bold", fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "c1_wilson.png"), dpi=150, bbox_inches="tight")
print(json.dumps(result["core_5_network"], ensure_ascii=False))
print("supercritical fraction: euc=%.2f%% net=%.2f%%" % (f_euc * 100, f_net * 100))
for c in pairs:
    print("  %-40s d=%6.0fm λ=%.3f %s" % (c["pair"], c["d_net_m"], c["lambda_net"], "超临界" if c["above_critical"] else ""))
