# -*- coding: utf-8 -*-
"""C7 · 高德 POI 动力分析（"看不见的动力"体检）
- 输入：poi_wgs84/*.json（高德 API，GCJ-02→WGS84 已转换，12 类 25,476 点）
- 分析：
  1) 200m 网格 POI 密度热场（总活力 + 分维度：工作/生活/休闲/健康）
  2) 三处重点区 + 走廊带的 POI 功能体检（各类占比 vs 定位匹配度）
  3) Jacobs 活力条件：交叉口密度 + POI 多样性（熵）
  4) 热点识别：company+research 密度 Top 网格（AI 生态锚点）
  5) 缺口诊断：各区相对供应短板（供职比、餐饮/医疗/生活服务密度）
输出：计算/c7_poi_dynamics.json + charts/c7_poi.png
"""
import os, json, math
import numpy as np
from shapely.geometry import Point, Polygon, box
from shapely.ops import transform as sh_transform, unary_union
import pyproj
from kun_common import setup_chinese_fonts, registry_put

HERE = os.path.dirname(os.path.abspath(__file__))
CALC = os.path.join(HERE, "计算"); CHARTS = os.path.join(HERE, "charts")
POI_DIR = os.path.join(HERE, "poi_wgs84")
os.makedirs(CALC, exist_ok=True); os.makedirs(CHARTS, exist_ok=True)

import pickle
model = pickle.load(open(os.path.join(HERE, "site_model.pkl"), "rb"))
site = model["site"]
keys = model["key_geoms"]
corridor = model["corridor"]

TRANS = pyproj.Transformer.from_crs(pyproj.CRS.from_epsg(4326), pyproj.CRS.from_epsg(4548), always_xy=True)
def to_m(g):
    def pr(x, y, z=None):
        a, b = TRANS.transform(x, y)
        return (a, b)
    return sh_transform(pr, g)

# 加载 POI
cats = {
    "company": "工作(企业)", "research": "工作(科研)", "finance": "工作(金融)",
    "school": "教育", "residential": "居住", "living": "生活服务",
    "dining": "餐饮", "shopping": "购物", "sports": "休闲体育",
    "medical": "医疗健康", "scenic": "文旅", "transport": "交通",
}
pois = {}
pois_m = {}
total = 0
for slug in cats:
    d = json.load(open(os.path.join(POI_DIR, f"{slug}.json")))
    pts = [Point(p["lon_wgs"], p["lat_wgs"]) for p in d]
    pois[slug] = pts
    pois_m[slug] = [to_m(p) for p in pts]
    total += len(pts)

site_m = to_m(site)
corridor_m = to_m(corridor) if corridor is not None else None

def count_in(points, geom_m):
    g = unary_union([p for p in points if geom_m.contains(p) or geom_m.distance(p) < 1e-9])
    return len(g.geoms) if hasattr(g, "geoms") else (1 if not g.is_empty else 0)

def count_polygon(points, poly_m):
    n = 0
    for p in points:
        if poly_m.contains(p):
            n += 1
    return n

# 1) 200m 网格密度场
CELL = 200.0
x0, y0, x1, y1 = site_m.bounds
nx_ = int((x1 - x0) / CELL) + 1; ny_ = int((y1 - y0) / CELL) + 1
grid_total = np.zeros((ny_, nx_)); grid_work = np.zeros((ny_, nx_)); grid_life = np.zeros((ny_, nx_))
work_cats = {"company", "research", "finance"}
life_cats = {"dining", "shopping", "living", "sports"}
def cell_index(p):
    return (min(ny_ - 1, max(0, int((p.y - y0) / CELL))), min(nx_ - 1, max(0, int((p.x - x0) / CELL))))
for slug, pts in pois.items():
    for p in pts:
        pm = to_m(p)
        if not site_m.contains(pm):
            continue
        i, j = cell_index(pm)
        grid_total[i, j] += 1
        if slug in work_cats:
            grid_work[i, j] += 1
        if slug in life_cats:
            grid_life[i, j] += 1

# 热点 Top 网格（AI 生态锚点）
hot = []
for i in range(ny_):
    for j in range(nx_):
        if grid_total[i, j] >= 15:
            cx = x0 + (j + 0.5) * CELL; cy = y0 + (i + 0.5) * CELL
            hot.append({"i": int(i), "j": int(j), "total": int(grid_total[i, j]),
                        "work": int(grid_work[i, j]), "life": int(grid_life[i, j]),
                        "work_life_ratio": round(float(grid_work[i, j] / max(1, grid_life[i, j])), 2)})
hot.sort(key=lambda h: -h["total"])

# 2) 三区 + 走廊带功能体检
areas = {
    "zhongzhiyuan_ai_acceleration_area": ("众智园", keys["PROV-KEY-001"]),
    "beijing_ai_origin_community": ("北京AI原点社区", keys["PROV-KEY-002"]),
    "dazhongsi_ai_industry_cluster": ("大钟寺", keys["PROV-KEY-003"]),
    "corridor_band": ("走廊带(主脊两侧500m)", (corridor.buffer(0.0045).intersection(site)) if corridor is not None else None),
}
health_report = {}
for aid, (zh, g) in areas.items():
    if g is None or g.is_empty:
        continue
    gm = to_m(g) if aid != "corridor_band" else to_m(g)
    counts = {slug: count_polygon(pois_m[slug], gm) for slug in pois_m}
    n = sum(counts.values())
    if n == 0:
        continue
    mix = {slug: round(v / n, 4) for slug, v in counts.items()}
    # 多样性熵
    p = np.array([v / n for v in counts.values()])
    H = -sum(x * math.log(x) for x in p if x > 0) / math.log(len(cats))
    # 供职比 = 工作类/生活类
    w = counts["company"] + counts["research"] + counts["finance"]
    l = counts["dining"] + counts["shopping"] + counts["living"] + counts["sports"]
    health_report[aid] = {"name_zh": zh, "n_pois": n, "mix": mix,
                          "diversity_entropy_norm": round(float(H), 3),
                          "work_life_ratio": round(w / max(1, l), 3),
                          "medical_density": round(counts["medical"] / (gm.area / 1e6), 2),
                          "area_km2": round(gm.area / 1e6, 3)}

# 3) Jacobs 活力：交叉口密度（用 C4 的压缩图节点？直接用 OSM 原图）
from kun_common import build_road_graph
G = build_road_graph(model["layers"]["roads"])
int_nodes = [v for v in G if G.degree(v) >= 3]
int_pts = [Point(G.graph["coords"][v][0], G.graph["coords"][v][1]) for v in int_nodes]
int_count = sum(1 for p in int_pts if site_m.contains(to_m(p)))
intersection_density = round(int_count / (site_m.area / 1e6), 1)

# 4) 缺口诊断：三区相对短板
gap_notes = []
for aid, hr in health_report.items():
    if aid == "corridor_band":
        continue
    short = sorted(hr["mix"].items(), key=lambda kv: kv[1])[:3]
    gap_notes.append({"area": hr["name_zh"], "weakest_categories": [(s, round(v, 4)) for s, v in short]})

result = {
    "meta": {"source": "高德地图 Web Service POI API (key=WebService)",
             "n_pois": total, "categories": cats,
             "crs": "GCJ-02 已转 WGS84（标准算法，非手工偏移）",
             "fetched": "2026-08-15"},
    "grid": {"cell_m": CELL, "n_hotspots": len(hot), "top_hotspots": hot[:20]},
    "jacobs": {"intersection_density_per_km2": intersection_density,
               "reference": "Porta/Jacobs: 老城常 >200/km²；车本新城常 <80/km²"},
    "area_health": health_report,
    "gap_notes": gap_notes,
}
json.dump(result, open(os.path.join(CALC, "c7_poi_dynamics.json"), "w"), ensure_ascii=False, indent=2)

registry_put("C7_POI", "n_pois_total", total, "count",
             "高德 POI 抓取（12类，GCJ-02→WGS84）",
             "一带高频活力数据底座",
             caveat="POI 为高德口径快照(2026-08-15)，非普查；类别归属按高德 typecode")
registry_put("C7_POI", "intersection_density_per_km2", intersection_density, "1/km2",
             "OSM 路网三岔以上交叉口密度",
             f"Jacobs/Porta 活力指标；对照老城>200、车本新城<80",
             caveat="OSM 路网完整性口径")
for aid, hr in health_report.items():
    registry_put("C7_POI", f"poi_diversity_{aid}", hr["diversity_entropy_norm"], "ratio",
                 "POI 类别香农熵/ln(12)（功能混合度）",
                 f"{hr['name_zh']} 功能多样性",
                 caveat="高德 POI 快照口径")

plt = setup_chinese_fonts()
fig, axes = plt.subplots(1, 2, figsize=(14, 5.6))
ax = axes[0]
im = ax.imshow(grid_total, origin="lower", cmap="YlOrRd", aspect="auto",
               extent=[x0, x1, y0, y1])
ax.set_title(f"图 C7a · 200m 网格 POI 总密度场（{total} 点，12 类）")
ax.set_xlabel("E (m)"); ax.set_ylabel("N (m)")
fig.colorbar(im, ax=ax, label="POI 数量/格")
ax2 = axes[1]
names = [hr["name_zh"] for hr in health_report.values()]
w_l = [hr["work_life_ratio"] for hr in health_report.values()]
H = [hr["diversity_entropy_norm"] for hr in health_report.values()]
x = np.arange(len(names))
ax2.bar(x - 0.18, w_l, 0.36, label="供职比(工作/生活类)", color="#b08a4f")
ax2.bar(x + 0.18, H, 0.36, label="功能多样性熵", color="#2e9e6b")
ax2.set_xticks(x); ax2.set_xticklabels(names, rotation=12)
ax2.set_title("图 C7b · 三区+走廊带功能体检")
ax2.legend()
fig.suptitle("图 C7 · 高德 POI 动力分析：看不见的城市动力", fontweight="bold", fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "c7_poi.png"), dpi=150, bbox_inches="tight")
print("total POIs:", total, "| hotspots:", len(hot), "| intersection density:", intersection_density, "/km2")
for aid, hr in health_report.items():
    print(f"  {hr['name_zh']}: n={hr['n_pois']} mix_H={hr['diversity_entropy_norm']} W/L={hr['work_life_ratio']} med={hr['medical_density']}/km2")
for g_ in gap_notes:
    print("  gap:", g_)
