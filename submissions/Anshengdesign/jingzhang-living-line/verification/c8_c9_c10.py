# -*- coding: utf-8 -*-
"""C8+C9+C10 · 标度律偏离度 / 就业-交通平衡(LUTI式) / H健康因子
C8  偏离度 = (实际占比/均匀参考占比 - 1)×100%（淀山湖式，KUN 对标方法论）
C9  就业-交通平衡：7站 1km 写字楼/公司 POI 密度 × 地铁站数（上海式 Batty 三层模型简化）
    就业集中度：Lorenz/Gini（"多少面积承载多少就业"）
C10 H = γ_创新/β_基建 健康因子（企业标度律的城市版，临界参照 H=1.35 / H<1 消耗自己）
输出：计算/c8_c9_c10.json + charts/c8_c9_c10.png
"""
import os, json, math
import numpy as np
from shapely.geometry import Point, box
from shapely.ops import transform as sh_transform
import pyproj
from kun_common import setup_chinese_fonts, registry_put

HERE = os.path.dirname(os.path.abspath(__file__))
CALC = os.path.join(HERE, "计算"); CHARTS = os.path.join(HERE, "charts")
POI_DIR = os.path.join(HERE, "poi_wgs84")
DG = os.path.join(HERE, "design_geometry")
os.makedirs(CALC, exist_ok=True); os.makedirs(CHARTS, exist_ok=True)

TRANS = pyproj.Transformer.from_crs(pyproj.CRS.from_epsg(4326), pyproj.CRS.from_epsg(4548), always_xy=True)
def to_m(g):
    def pr(x, y, z=None):
        a, b = TRANS.transform(x, y)
        return (a, b)
    return sh_transform(pr, g)

cats_zh = {"company": "公司企业", "research": "科研机构", "finance": "金融保险", "school": "学校",
           "residential": "商务住宅", "living": "生活服务", "dining": "餐饮服务", "shopping": "购物服务",
           "sports": "体育休闲", "medical": "医疗保健", "scenic": "风景名胜", "transport": "交通设施"}
pois = {}
for slug in cats_zh:
    d = json.load(open(os.path.join(POI_DIR, f"{slug}.json")))
    pois[slug] = [Point(p["lon_wgs"], p["lat_wgs"]) for p in d]

# ---------------- C8 功能偏离度 ----------------
n_total = sum(len(v) for v in pois.values())
uniform = 1 / len(cats_zh)
c8_rows = []
for slug, zh in cats_zh.items():
    n = len(pois[slug])
    share = n / n_total
    dev = (share / uniform - 1) * 100
    diag = "偏多(量)" if dev > 15 else ("基本匹配" if dev >= -15 else "不足")
    c8_rows.append({"category": zh, "n": n, "share_pct": round(share * 100, 2),
                    "deviation_pct": round(dev, 1), "diagnosis": diag})
c8_rows.sort(key=lambda r: -r["deviation_pct"])

# ---------------- C9 就业-交通平衡 ----------------
import pickle
model = pickle.load(open(os.path.join(HERE, "site_model.pkl"), "rb"))
site_m = to_m(model["site"])
stations = [
    ("五道口站", 116.3317, 39.9915, 2), ("知春路站", 116.3344, 39.9751, 2),
    ("清华东路西口站", 116.3336, 39.9993, 1), ("大钟寺站", 116.3390, 39.9653, 1),
    ("学院桥站", 116.3473, 39.9868, 1), ("学知园站", 116.3458, 40.0136, 1),
    ("北京北站", 116.3462, 39.9459, 2),
]
work_pts = pois["company"] + pois["research"] + pois["finance"]
office_pts = pois["company"] + pois["finance"]
c9_rows = []
for nm, lon, lat, n_metro in stations:
    p = to_m(Point(lon, lat))
    r1 = p.buffer(1000)
    n_office = sum(1 for q in office_pts if r1.contains(to_m(q)))
    n_work = sum(1 for q in work_pts if r1.contains(to_m(q)))
    c9_rows.append({"station": nm, "n_office_1km": n_office, "n_work_1km": n_work,
                    "n_metro_lines": n_metro,
                    "balance_score": round(n_office / (n_metro + 1), 1)})
c9_rows.sort(key=lambda r: -r["balance_score"])
# 就业集中度：办公楼 POI 的 Lorenz/Gini（全场）
def gini_points(pts):
    # 以 200m 网格计数算 Gini
    CELL = 200.0
    x0, y0, x1, y1 = site_m.bounds
    nx_ = int((x1 - x0) / CELL) + 1; ny_ = int((y1 - y0) / CELL) + 1
    grid = np.zeros((ny_, nx_))
    for q in pts:
        pm = to_m(q)
        if not site_m.contains(pm):
            continue
        i = min(ny_ - 1, max(0, int((pm.y - y0) / CELL)))
        j = min(nx_ - 1, max(0, int((pm.x - x0) / CELL)))
        grid[i, j] += 1
    vals = np.sort(grid.ravel())
    csum = np.cumsum(vals)
    total = csum[-1]
    if total == 0:
        return 0.0, None, None
    lorenz = np.concatenate([[0], csum / total])
    area = np.trapz(lorenz, np.linspace(0, 1, len(lorenz)))
    g = 1 - 2 * area
    # 前 N% 网格承载的就业比例（correct: top share = 1 - prefix of smallest len-k values）
    n_top = max(1, int(np.ceil(len(vals) * 0.01)))
    top_share = (total - csum[len(vals) - 1 - n_top]) / total if len(vals) > n_top else 1.0
    n_top10 = max(1, int(np.ceil(len(vals) * 0.10)))
    top10_share = (total - csum[len(vals) - 1 - n_top10]) / total if len(vals) > n_top10 else 1.0
    return g, top_share, top10_share
g, top1, top10 = gini_points(office_pts)

# ---------------- C10 H 健康因子 ----------------
# γ_创新代理：work 类 POI 数随 200m 网格面积（建成格）的标度指数（与 C3 同法）
CELL = 200.0
x0, y0, x1, y1 = site_m.bounds
nx_ = int((x1 - x0) / CELL) + 1; ny_ = int((y1 - y0) / CELL) + 1
grid_work = np.zeros((ny_, nx_))
for q in work_pts:
    pm = to_m(q)
    if not site_m.contains(pm):
        continue
    i = min(ny_ - 1, max(0, int((pm.y - y0) / CELL)))
    j = min(nx_ - 1, max(0, int((pm.x - x0) / CELL)))
    grid_work[i, j] += 1
# 建成格 = 网格内有 POI 或建筑基底的格（用总 POI 格作代理）
grid_total = np.zeros((ny_, nx_))
for pts in pois.values():
    for q in pts:
        pm = to_m(q)
        if not site_m.contains(pm):
            continue
        i = min(ny_ - 1, max(0, int((pm.y - y0) / CELL)))
        j = min(nx_ - 1, max(0, int((pm.x - x0) / CELL)))
        grid_total[i, j] += 1
# 以 400m 聚合单元做标度拟合（避免 200m 网格过噪）
CELL2 = 400
nx2 = int((x1 - x0) / CELL2) + 1; ny2 = int((y1 - y0) / CELL2) + 1
unit_work = np.zeros((ny2, nx2)); unit_all = np.zeros((ny2, nx2))
for i in range(ny_):
    for j in range(nx_):
        unit_work[i // 2, j // 2] += grid_work[i, j]
        unit_all[i // 2, j // 2] += grid_total[i, j]
mass = unit_all  # 规模代理 N = 单元总POI数
y = unit_work
mask = (mass >= 5) & (y >= 1)
if mask.sum() >= 8:
    lx = np.log(mass[mask]); ly = np.log(y[mask])
    A = np.vstack([lx, np.ones_like(lx)]).T
    gamma, _ = np.linalg.lstsq(A, ly, rcond=None)[0]
    pred = A @ np.array([gamma, _])
    r2 = 1 - ((ly - pred) ** 2).sum() / ((ly - ly.mean()) ** 2).sum()
else:
    gamma, r2 = None, None
beta_road = 0.915   # C3 实算
beta_bldg = 0.60    # C3 实算
beta_infra = (beta_road + beta_bldg) / 2
H = (gamma / beta_infra) if gamma else None
c10 = {
    "gamma_innovation_estimated": round(float(gamma), 3) if gamma else None,
    "r2": round(float(r2), 3) if r2 is not None else None,
    "n_units": int(mask.sum()),
    "beta_road": beta_road, "beta_bldg": beta_bldg,
    "beta_infra_mean": round(beta_infra, 3),
    "H_estimated": round(H, 3) if H else None,
    "reference": "H基准≈1.35（γ1.15/β0.85）；H<1=系统在消耗自己（扩张不可持续）",
    "interpretation": ("现状 γ 可拟合，H 可计算" if H else "γ 无法稳健拟合——创新产出的标度指数未被度量，这本身就是诊断结论：'是否成功'的判据缺失，方案以年度发布机制补上度量"),
}

result = {"meta": {"generated": "2026-08-15",
                   "c8_model": "功能偏离度=(实际占比/均匀参考占比-1)×100%（KUN 对标方法论）",
                   "c9_model": "Batty 三层模型简化：就业密度×站点可达性；Lorenz/Gini 就业集中度",
                   "c10_model": "H=γ/β 健康因子（企业标度律城市版）；临界参照 H=1.35"},
          "c8_deviation": c8_rows,
          "c9_station_balance": c9_rows,
          "c9_employment_concentration": {"gini": round(float(g), 3) if g else None,
                                          "top1pct_grid_share": round(float(top1), 3) if top1 else None,
                                          "top10pct_grid_share": round(float(top10), 3) if top10 else None,
                                          "london_reference": "伦敦：11.6%面积承载50%就业、0.4%面积承载10%就业"},
          "c10_health_factor": c10}
json.dump(result, open(os.path.join(CALC, "c8_c9_c10.json"), "w"), ensure_ascii=False, indent=2)

registry_put("C8_DEV", "top_surplus_category", c8_rows[0]["category"], "name",
             "功能偏离度诊断（12类POI，均匀参考）", f"偏离度最高：{c8_rows[0]['category']} +{c8_rows[0]['deviation_pct']}%",
             caveat="高德POI快照口径；均匀参考为诊断基准非目标")
registry_put("C8_DEV", "top_deficit_category", c8_rows[-1]["category"], "name",
             "功能偏离度诊断", f"偏离度最低：{c8_rows[-1]['category']} {c8_rows[-1]['deviation_pct']}%",
             caveat="同上")
registry_put("C9_EMP", "best_balance_station", c9_rows[0]["station"], "name",
             "就业-交通平衡点（1km写字楼POI×轨道线数）", f"京张的最佳就业-交通平衡点：{c9_rows[0]['station']}",
             caveat="POI口径；轨道线数按公开运营信息")
registry_put("C9_EMP", "employment_gini", round(float(g), 3) if g else None, "ratio",
             "办公楼POI空间分布Gini（200m网格）", "就业集中度；对照伦敦 0.4%面积承载10%就业",
             caveat="POI快照口径")
registry_put("C10_H", "H_health_factor", round(H, 3) if H else None, "dimensionless",
             "H=γ_创新/β_基建（城市版健康因子）", f"临界参照 H=1.35；H<1=消耗自己" + ("；现状可计算" if H else "；现状不可稳健拟合（γ缺度量）"),
             caveat="γ 为 400m 单元 POI 标度拟合代理；β 取自 C3 实算")

# ---- 图 ----
plt = setup_chinese_fonts()
fig, axes = plt.subplots(1, 3, figsize=(17, 5.4))
ax = axes[0]
names = [r["category"] for r in c8_rows]
devs = [r["deviation_pct"] for r in c8_rows]
colors = ["#e74c3c" if d < -15 else ("#5fbf77" if d > 15 else "#8a97a8") for d in devs]
ax.barh(range(len(names))[::-1], devs[::-1], color=colors[::-1])
ax.axvline(0, color="#333", lw=1)
ax.set_yticks(range(len(names))[::-1]); ax.set_yticklabels(names[::-1], fontsize=8)
ax.set_xlabel("偏离度(%)"); ax.set_title("图 C8 · 功能偏离度诊断（均匀参考）")
ax2 = axes[1]
sn = [r["station"] for r in c9_rows]
so = [r["n_office_1km"] for r in c9_rows]
ax2.barh(range(len(sn))[::-1], so[::-1], color="#5b8dd9")
ax2.set_yticks(range(len(sn))[::-1]); ax2.set_yticklabels(sn[::-1], fontsize=8)
ax2.set_xlabel("1km 写字楼POI"); ax2.set_title("图 C9 · 就业-交通平衡（1km圈）")
ax3 = axes[2]
ax3.bar([0], [H if H else 0], color="#5fbf77" if (H and H >= 1) else "#e74c3c")
ax3.axhline(1.35, color="#c0392b", ls="--", lw=2, label="H基准≈1.35")
ax3.axhline(1.0, color="#e67e22", ls="--", lw=1.5, label="H=1 临界（<1=消耗自己）")
ax3.set_xticks([0]); ax3.set_xticklabels([("现状H" if H else "现状H=不可度量")], fontsize=9)
ax3.set_ylabel("H=γ/β"); ax3.set_title("图 C10 · H 健康因子（临界值参照）")
ax3.legend(fontsize=8)
fig.suptitle("图 C8-C10 · 标度律偏离 / 就业-交通平衡 / H健康因子（临界值体系）", fontweight="bold", fontsize=13.5)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "c8_c9_c10.png"), dpi=150, bbox_inches="tight")
print("C8 deviation top3:", [(r['category'], r['deviation_pct']) for r in c8_rows[:3]])
print("C8 deficit top3:", [(r['category'], r['deviation_pct']) for r in c8_rows[-3:]])
print("C9 balance:", [(r['station'], r['n_office_1km'], r['balance_score']) for r in c9_rows[:3]])
print("C9 gini:", g, "top1%:", top1, "top10%:", top10)
print("C10:", c10)
