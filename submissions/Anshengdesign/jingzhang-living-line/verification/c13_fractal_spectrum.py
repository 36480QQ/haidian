# -*- coding: utf-8 -*-
"""C13 · 分形谱系完整化（Batty/Arcaute 全谱）
① 面积-周长标度 P ∝ A^(D/2)（建成斑块与用地斑块）
② 密度衰减 ρ(d) ∝ d^(-γ)（就业 POI 距主脊/站点的衰减）
③ Lacunarity 空隙度（绿地斑块纹理）
④ 建成斑块盒计数 D（补充路网 D）
输出：计算/c13_fractal_spectrum.json + charts/c13_fractal.png
"""
import os, json, pickle, math
import numpy as np
from shapely.geometry import Point, shape
from shapely.ops import transform as sh_transform, unary_union
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

model = pickle.load(open(os.path.join(HERE, "site_model.pkl"), "rb"))
site_m = to_m(model["site"])
corridor_m = to_m(model["corridor"]) if model["corridor"] is not None else None

# ---------- ① 面积-周长标度 ----------
def area_perimeter_D(geoms, min_area=500):
    A = []; P = []
    for g in geoms:
        gm = to_m(g) if g.geom_type not in ("Polygon", "MultiPolygon") or True else g
        if gm.area < min_area:
            continue
        A.append(gm.area); P.append(gm.length)
    if len(A) < 8:
        return None, len(A)
    lx = np.log(A); ly = np.log(P)
    A_m = np.vstack([lx, np.ones_like(lx)]).T
    slope, _ = np.linalg.lstsq(A_m, ly, rcond=None)[0]
    pred = A_m @ np.array([slope, _])
    r2 = 1 - ((ly - pred) ** 2).sum() / ((ly - ly.mean()) ** 2).sum()
    D_ap = 2 * slope   # P ∝ A^(D/2)
    return D_ap, len(A), r2

bldg_feats = json.load(open(os.path.join(DG, "buildings.geojson")))["features"]
lu_feats = json.load(open(os.path.join(DG, "land_use.geojson")))["features"]
D_bldg, n_bldg, r2_bldg = area_perimeter_D([shape(f["geometry"]) for f in bldg_feats])
D_lu, n_lu, r2_lu = area_perimeter_D([shape(f["geometry"]) for f in lu_feats])

# ---------- ② 密度衰减 ----------
work_pts = []
for s in ("company", "research", "finance"):
    d = json.load(open(os.path.join(POI_DIR, f"{s}.json")))
    work_pts += [to_m(Point(p["lon_wgs"], p["lat_wgs"])) for p in d]
def density_decay(ref_line):
    dists = [ref_line.distance(p) for p in work_pts if site_m.contains(p)]
    dists = [d for d in dists if 0 < d < 4000]
    if len(dists) < 50:
        return None
    # 对数分箱密度
    bins = np.logspace(math.log10(200), math.log10(4000), 8)
    dens = []; mids = []
    for k in range(len(bins) - 1):
        cnt = sum(1 for d in dists if bins[k] <= d < bins[k + 1])
        ring = math.pi * (bins[k + 1] ** 2 - bins[k] ** 2) if corridor_m is None else (bins[k+1]-bins[k])*bins[k]*2
        dens.append(cnt / ring if ring > 0 else 0)
        mids.append(math.sqrt(bins[k] * bins[k + 1]))
    ok = [i for i, v in enumerate(dens) if v > 0]
    if len(ok) < 4:
        return None
    lx = np.log([mids[i] for i in ok]); ly = np.log([dens[i] for i in ok])
    A = np.vstack([lx, np.ones_like(lx)]).T
    g, _ = np.linalg.lstsq(A, ly, rcond=None)[0]
    pred = A @ np.array([g, _])
    r2 = 1 - ((ly - pred) ** 2).sum() / ((ly - ly.mean()) ** 2).sum()
    return float(-g), round(float(r2), 3)
gamma_sta, r2_sta = density_decay(unary_union([to_m(Point(a, b)) for a, b in
    [(116.3317,39.9915),(116.3344,39.9751),(116.3336,39.9993),(116.3390,39.9653),(116.3473,39.9868),(116.3458,40.0136),(116.3462,39.9459)]]))
gamma_cor = None
if corridor_m is not None:
    gamma_cor, r2_cor = density_decay(corridor_m)

# ---------- ③ Lacunarity（绿地斑块） ----------
green_feats = json.load(open(os.path.join(DG, "green_space.geojson")))["features"]
def lacunarity(geoms, eps=200):
    """空隙度 = Var(ε格内建成占比)/Mean² + 1 的滑移盒算法（简化：固定网格）"""
    x0, y0, x1, y1 = site_m.bounds
    nx_ = int((x1 - x0) / eps) + 1; ny_ = int((y1 - y0) / eps) + 1
    occ = np.zeros((ny_, nx_))
    for f in geoms:
        g = to_m(shape(f["geometry"])).intersection(site_m)
        if g.is_empty:
            continue
        bx0, by0, bx1, by1 = g.bounds
        for i in range(max(0, int((by0 - y0) / eps)), min(ny_, int((by1 - y0) / eps) + 1)):
            for j in range(max(0, int((bx0 - x0) / eps)), min(nx_, int((bx1 - x0) / eps) + 1)):
                c = __import__("shapely.geometry", fromlist=["box"]).box(x0 + j * eps, y0 + i * eps,
                                                                         x0 + (j + 1) * eps, y0 + (i + 1) * eps)
                occ[i, j] = max(occ[i, j], c.intersection(g).area / c.area)
    m = occ.mean(); v = occ.var()
    return float(v / (m * m) + 1) if m > 0 else None
lac = lacunarity(green_feats)

result = {
    "meta": {"model": "Fractal spectrum (Batty/Arcaute): area-perimeter / density decay / lacunarity",
             "reference": "P∝A^(D/2)：紧凑斑块 D≈2；城市建成 D≈1.2-1.5；密度衰减 γ≈1-2；Lacunarity 高=纹理粗糙"},
    "area_perimeter": {
        "buildings_D": round(D_bldg, 2) if D_bldg else None, "n_buildings": n_bldg, "r2": round(r2_bldg, 2) if D_bldg else None,
        "land_use_D": round(D_lu, 2) if D_lu else None, "n_land_use": n_lu, "r2_lu": round(r2_lu, 2) if D_lu else None,
    },
    "density_decay": {
        "gamma_station": gamma_sta, "r2_station": r2_sta,
        "gamma_corridor": gamma_cor, "r2_corridor": r2_cor if gamma_cor else None,
        "reference": "城市就业密度衰减 γ≈1-2；γ 越小越扁平（多中心）",
    },
    "lacunarity_green": lac,
}
json.dump(result, open(os.path.join(CALC, "c13_fractal_spectrum.json"), "w"), ensure_ascii=False, indent=2)
for k, v in {"building_AP_D": D_bldg, "landuse_AP_D": D_lu,
             "employment_decay_gamma_station": gamma_sta, "employment_decay_gamma_corridor": gamma_cor,
             "green_lacunarity": lac}.items():
    registry_put("C13_FRAC", k, (round(float(v), 3) if v is not None else None), "dimensionless",
                 "分形谱系（面积-周长/密度衰减/空隙度）", "形态谱系诊断",
                 caveat="代理口径：斑块=设计图层/POI点；Lacunarity 为固定网格近似")

plt = setup_chinese_fonts()
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
ax = axes[0]
for label, feats, color in [("建筑斑块", [shape(f["geometry"]) for f in bldg_feats], "#5b8dd9"),
                            ("用地斑块", [shape(f["geometry"]) for f in lu_feats], "#5fbf77")]:
    A = []; P = []
    for g in feats:
        gm = to_m(g)
        if gm.area < 500:
            continue
        A.append(gm.area); P.append(gm.length)
    ax.scatter(np.log(A), np.log(P), s=12, alpha=0.5, label=label, color=color)
ax.set_xlabel("ln 面积"); ax.set_ylabel("ln 周长")
ax.set_title(f"面积-周长标度 P∝A^(D/2)\n建筑D={D_bldg:.2f} 用地D={D_lu:.2f}")
ax.legend(fontsize=8)
ax2 = axes[1]
for label, g, color in ([("距轨道站", gamma_sta, "#5b8dd9"), ("距主脊", gamma_cor, "#5fbf77")]):
    if g:
        ax2.axhline(g, color=color, ls="--", lw=2, label=f"{label} γ={g:.2f}")
ax2.set_title("就业密度衰减 γ（对数环带）")
ax2.set_ylabel("γ"); ax2.set_xticks([]); ax2.legend(fontsize=8)
ax3 = axes[2]
ax3.bar([0], [lac], color="#e8915a")
ax3.set_xticks([0]); ax3.set_xticklabels(["绿地 Lacunarity"])
ax3.set_title(f"绿地纹理空隙度 = {lac:.3f}" if lac else "空隙度未计算")
fig.suptitle("图 C13 · 分形谱系：面积-周长 / 密度衰减 / 空隙度（京张实算）", fontweight="bold", fontsize=13)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "c13_fractal.png"), dpi=150, bbox_inches="tight")
print(json.dumps(result, ensure_ascii=False, indent=1))
