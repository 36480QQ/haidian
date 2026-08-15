# -*- coding: utf-8 -*-
"""C6 · 分形维数分析（街道网络盒计数 D）
参照 CASA 主文档 §3.4/§7.2：健康老城街道网络 D≈1.6–1.8（Arcaute；Batty Fractal Cities）
方法：对场地内 OSM 街道网络做盒计数 N(ε)~ε^(-D)，双对数最小二乘拟合 D
  - REAL 现状路网 D
  - GRID_NULL 规则网格 D（≈2 逼近时；对照）
输出：计算/c6_fractal.json + charts/c6_fractal.png
"""
import os, json, pickle, math
import numpy as np
import networkx as nx
from shapely.geometry import LineString
from kun_common import setup_chinese_fonts, build_road_graph, registry_put

HERE = os.path.dirname(os.path.abspath(__file__))
CALC = os.path.join(HERE, "计算"); CHARTS = os.path.join(HERE, "charts")
os.makedirs(CALC, exist_ok=True); os.makedirs(CHARTS, exist_ok=True)

model = pickle.load(open(os.path.join(HERE, "site_model.pkl"), "rb"))
layers = model["layers"]
site = model["site"]

def box_count(lines, bbox, epsilons):
    """盒计数：N(ε) = 被线段穿过的 ε 网格数"""
    x0, y0, x1, y1 = bbox
    out = []
    for eps in epsilons:
        nx_ = max(1, int((x1 - x0) / eps)); ny_ = max(1, int((y1 - y0) / eps))
        occupied = set()
        for ln in lines:
            lx0, ly0, lx1, ly1 = ln.bounds
            i0 = max(0, int((lx0 - x0) / eps)); i1 = min(nx_ - 1, int((lx1 - x0) / eps))
            j0 = max(0, int((ly0 - y0) / eps)); j1 = min(ny_ - 1, int((ly1 - y0) / eps))
            if i1 < i0 or j1 < j0:
                continue
            # 对每个线段采样点落在哪些格子
            n = max(8, int(ln.length / eps * 2))
            for k in range(n + 1):
                p = ln.interpolate(ln.length * k / n)
                i = min(nx_ - 1, max(0, int((p.x - x0) / eps)))
                j = min(ny_ - 1, max(0, int((p.y - y0) / eps)))
                occupied.add((i, j))
        out.append(len(occupied))
    return out

def fit_D(eps, counts, lo, hi):
    xs = np.log(eps[lo:hi]); ys = np.log(np.array(counts[lo:hi], dtype=float))
    A = np.vstack([xs, np.ones_like(xs)]).T
    d, _ = np.linalg.lstsq(A, ys, rcond=None)[0]
    pred = A @ np.array([d, _])
    ssr = ((ys - pred) ** 2).sum(); sst = ((ys - ys.mean()) ** 2).sum()
    return -d, 1 - ssr / sst

# 场地内道路线（WGS84 → 米制投影后盒计数；直接用经纬度做盒计数也可，保持一致用米）
import pyproj
from shapely.ops import transform as sh_transform
TRANS = pyproj.Transformer.from_crs(pyproj.CRS.from_epsg(4326), pyproj.CRS.from_epsg(4548), always_xy=True)
def to_m(g):
    def pr(x, y, z=None):
        a, b = TRANS.transform(x, y)
        return (a, b)
    return sh_transform(pr, g)

site_m = to_m(site)
lines_m = []
for e, g in layers["roads"]:
    if g.geom_type == "LineString":
        gm = to_m(g).intersection(site_m)
        if gm.geom_type == "LineString" and gm.length > 30:
            lines_m.append(gm)
        elif gm.geom_type == "MultiLineString":
            lines_m.extend([s for s in gm.geoms if s.length > 30])

eps = [1200, 900, 700, 500, 350, 250, 180, 120, 80]
counts = box_count(lines_m, site_m.bounds, eps)
# 分形维是尺度依赖量：主值取大尺度段(1200–500m，城市形态尺度)，并报告各尺度段
D_real, r2 = fit_D(eps, counts, 0, 4)
D_real_small, r2_small = fit_D(eps, counts, 5, 9)

# GRID_NULL：等长度规则网格（同总长度，400m 间距）
total_len = sum(l.length for l in lines_m)
x0, y0, x1, y1 = site_m.bounds
grid_lines = []
step = 400.0
x = x0 + step / 2
while x < x1:
    grid_lines.append(LineString([(x, y0), (x, y1)])); x += step
y = y0 + step / 2
while y < y1:
    grid_lines.append(LineString([(x0, y), (x1, y)])); y += step
counts_grid = box_count(grid_lines, site_m.bounds, eps)
D_grid, r2g = fit_D(eps, counts_grid, 1, len(eps) - 1)

result = {
    "meta": {"model": "box-counting fractal dimension of street network",
             "epsilons_m": eps, "n_lines_real": len(lines_m),
             "reference": "Arcaute/Batty: 健康老城 D≈1.6–1.8；网格 D→2 上界；D 为尺度依赖量",
             "fit_ranges": "large=1200–500m(城市形态尺度); small=350–80m(肌理尺度)"},
    "real": {"D_large": round(D_real, 3), "r2_large": round(r2, 3),
             "D_small": round(D_real_small, 3), "r2_small": round(r2_small, 3), "counts": counts},
    "grid_null": {"D": round(D_grid, 3), "r2": round(r2g, 3), "counts": counts_grid},
}
json.dump(result, open(os.path.join(CALC, "c6_fractal.json"), "w"), ensure_ascii=False, indent=2)
registry_put("C6_FRACTAL", "street_network_D_real", round(D_real, 3), "dimensionless",
             "盒计数分形维数 D（街道网络，双对数最小二乘）",
             f"现状路网 D；健康老城区间 1.6–1.8",
             caveat="盒计数对采样密度敏感；拟合区间为中间尺度(120–900m)")
registry_put("C6_FRACTAL", "street_network_D_grid", round(D_grid, 3), "dimensionless",
             "规则网格零模型盒计数 D", "强加秩序基准（趋近 2）", caveat="解析对照")

plt = setup_chinese_fonts()
fig, ax = plt.subplots(figsize=(8, 5.6))
ax.loglog(eps, counts, "o-", label=f"REAL 现状路网 D大尺度={D_real:.3f} / D小尺度={D_real_small:.3f}", color="#b08a4f")
ax.loglog(eps, counts_grid, "s--", label=f"GRID_NULL 规则网格 D={D_grid:.3f}", color="#8a97a8")
ax.axhspan(0, 0, color="#2e9e6b", alpha=0.08, label="健康老城区间 D≈1.6–1.8")
ax.set_xlabel("ε (m)"); ax.set_ylabel("N(ε) 被占用格数")
ax.set_title("图 C6 · 街道网络盒计数分形维数（REAL vs GRID_NULL）")
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "c6_fractal.png"), dpi=150, bbox_inches="tight")
print(json.dumps(result, ensure_ascii=False, indent=1))
