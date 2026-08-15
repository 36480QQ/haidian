# -*- coding: utf-8 -*-
"""C3 · 标度律分析（Y = Y0·N^β，West/Bettencourt）
口径：以 98 个概念用地分区为单元（n=98），对数-对数拟合各功能随单元规模的标度指数 β。
  - N = 单元面积（规模代理）
  - Y_road  = 单元内道路长度（基础设施）
  - Y_ai    = 单元内 AI 创新空间（0802+0804+05，按质心所在单元计）
  - Y_resi  = 居住用地（0701）
  - Y_green = 绿地（1401）
  参照：城市基础设施典型亚线性 β≈0.85；超线性 β≈1.15 为集聚收益（手册 §2.1）
输出：计算/c3_scaling.json + charts/c3_scaling.png
"""
import os, json, math
import numpy as np
from shapely.geometry import shape
from shapely.ops import transform as sh_transform
import pyproj
from kun_common import setup_chinese_fonts, registry_put

HERE = os.path.dirname(os.path.abspath(__file__))
CALC = os.path.join(HERE, "计算"); CHARTS = os.path.join(HERE, "charts")
DG = os.path.join(HERE, "design_geometry")
os.makedirs(CALC, exist_ok=True); os.makedirs(CHARTS, exist_ok=True)

TRANS = pyproj.Transformer.from_crs(pyproj.CRS.from_epsg(4326), pyproj.CRS.from_epsg(4548), always_xy=True)
def to_m(g):
    def pr(x, y, z=None):
        a, b = TRANS.transform(x, y)
        return (a, b)
    return sh_transform(pr, g)

lu = json.load(open(os.path.join(DG, "land_use.geojson")))
roads = json.load(open(os.path.join(DG, "roads.geojson")))

cells = []
for f in lu["features"]:
    g = to_m(shape(f["geometry"]))
    cells.append({"id": f["id"], "geom": g, "code": f["properties"]["land_use_code"], "area": g.area})

road_segs = [to_m(shape(f["geometry"])) for f in roads["features"]]

# 更精细的 Y（避免与单元面积同义反复）
bldgs = json.load(open(os.path.join(DG, "buildings.geojson")))
green = json.load(open(os.path.join(DG, "green_space.geojson")))
bldg_geoms = [to_m(shape(f["geometry"])) for f in bldgs["features"]]
green_geoms = [to_m(shape(f["geometry"])) for f in green["features"]]

rows = []
for c in cells:
    road_len = sum(s.intersection(c["geom"]).length for s in road_segs)
    n_bldg = sum(1 for b in bldg_geoms if c["geom"].intersects(b))
    bldg_area = sum(b.intersection(c["geom"]).area for b in bldg_geoms)
    green_in = sum(g.intersection(c["geom"]).area for g in green_geoms)
    rows.append({
        "id": c["id"], "N_area": c["area"], "code": c["code"],
        "Y_road": road_len,
        "Y_bldg_n": float(n_bldg),
        "Y_bldg_area": bldg_area,
        "Y_green_in": green_in,
    })

def fit(xs, ys):
    xs = np.array(xs); ys = np.array(ys)
    m = ys > 0
    if m.sum() < 5:
        return {"beta": None, "r2": None, "n": int(m.sum())}
    lx, ly = np.log(xs[m]), np.log(ys[m])
    A = np.vstack([lx, np.ones_like(lx)]).T
    beta, logy0 = np.linalg.lstsq(A, ly, rcond=None)[0]
    pred = A @ np.array([beta, logy0])
    ss_res = ((ly - pred) ** 2).sum()
    ss_tot = ((ly - ly.mean()) ** 2).sum()
    r2 = 1 - ss_res / ss_tot
    return {"beta": round(float(beta), 3), "logY0": round(float(logy0), 3),
            "r2": round(float(r2), 3), "n": int(m.sum())}

X = [r["N_area"] for r in rows]
result = {"meta": {"model": "Y = Y0·N^β (allometric scaling)",
                   "units": "N=单元面积(sqm)；Y: 道路=m, 建筑数=count, 其余=sqm",
                   "reference": "基础设施亚线性 β≈0.85；集聚超线性 β≈1.15（手册 §2.1）",
                   "n_cells": len(rows)},
          "fits": {}}
for name in ("Y_road", "Y_bldg_n", "Y_bldg_area", "Y_green_in"):
    f = fit(X, [r[name] for r in rows])
    result["fits"][name] = f
    registry_put("C3_SCALING", f"beta_{name}", f["beta"], "dimensionless",
                 "log-log 最小二乘拟合 β（Y=Y0·N^β，n=98 概念分区单元）",
                 f"{name} 的标度指数；对照 β≈0.85(亚线性)/1.15(超线性)",
                 caveat="概念分区（agent_generated_design），非控规；n=98 为设计单元尺度")

json.dump(result, open(os.path.join(CALC, "c3_scaling.json"), "w"), ensure_ascii=False, indent=2)

plt = setup_chinese_fonts()
names = ["Y_road", "Y_bldg_n", "Y_bldg_area", "Y_green_in"]
labels = {"Y_road": "道路长度", "Y_bldg_n": "建筑数量", "Y_bldg_area": "建筑基底面积", "Y_green_in": "单元内绿地面积"}
fig, axes = plt.subplots(1, 4, figsize=(17, 4.2))
for ax, nm in zip(axes, names):
    xs = np.array(X); ys = np.array([r[nm] for r in rows])
    m = ys > 0
    ax.scatter(xs[m] / 1e6, ys[m] / 1e6, s=18, alpha=0.7, color="#2f6fed")
    if m.sum() >= 5:
        b = result["fits"][nm]["beta"]
        lx = np.log(xs[m]); ly = np.log(ys[m])
        A = np.vstack([lx, np.ones_like(lx)]).T
        bb = np.linalg.lstsq(A, ly, rcond=None)[0]
        xx = np.linspace(lx.min(), lx.max(), 20)
        ax.plot(np.exp(xx) / 1e6, np.exp(bb[1] + bb[0] * xx) / 1e6, "r--", lw=2)
    ax.axhline(0, color="#999", lw=0.5)
    ax.set_title(f"{labels[nm]}\nβ={result['fits'][nm]['beta']} (R²={result['fits'][nm]['r2']})", fontsize=10)
    ax.set_xlabel("单元面积 (万㎡)"); ax.set_ylabel("Y (万㎡)")
fig.suptitle("图 C3 · 标度律：功能随单元规模的标度指数（98 个概念分区单元）", fontweight="bold", fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "c3_scaling.png"), dpi=150, bbox_inches="tight")
print(json.dumps(result, ensure_ascii=False, indent=1))
