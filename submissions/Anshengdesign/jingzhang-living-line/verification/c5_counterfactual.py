# -*- coding: utf-8 -*-
"""C5 · 反事实零模型（REAL vs GRID_NULL vs RANDOM_NULL vs DESIGN）
参照 KUN 手册（阿尔罕布拉范式 §1.6）：不检验『约束产生了什么』，研究就只是描述。
  C5a 走廊线：遗址公园走廊(REAL) vs 同长度正北直线(GRID_NULL) vs 同长度随机游走(RANDOM_NULL)
       vs 走廊+6处缝合(DESIGN)；指标=朝向熵(12箱/ln12)、迂回系数、顺轴占比
  C5b 绿地斑块：REAL vs 同数量同面积正交网格 vs 随机散布；指标=斑块长轴朝向熵
输出：计算/c5_counterfactual.json + charts/c5_counterfactual.png
"""
import os, json, pickle, math
import numpy as np
import pyproj
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import transform as sh_transform
from shapely import get_coordinates
from kun_common import setup_chinese_fonts, registry_put

HERE = os.path.dirname(os.path.abspath(__file__))
CALC = os.path.join(HERE, "计算"); CHARTS = os.path.join(HERE, "charts")
os.makedirs(CALC, exist_ok=True); os.makedirs(CHARTS, exist_ok=True)

model = pickle.load(open(os.path.join(HERE, "site_model.pkl"), "rb"))
layers = model["layers"]
corridor = model["corridor"]

TRANS = pyproj.Transformer.from_crs(pyproj.CRS.from_epsg(4326), pyproj.CRS.from_epsg(4548), always_xy=True)
def to_m(g):
    def pr(x, y, z=None):
        a, b = TRANS.transform(x, y)
        return (a, b)
    return sh_transform(pr, g)

def bearing_entropy(lines, bins=12):
    """线段朝向香农熵/ln(bins)；北=0，逆时针角度 mod 180"""
    angs = []
    for ln in lines:
        coords = list(ln.coords)
        for i in range(len(coords) - 1):
            dx = coords[i + 1][0] - coords[i][0]
            dy = coords[i + 1][1] - coords[i][1]
            if abs(dx) + abs(dy) < 1e-9:
                continue
            a = math.degrees(math.atan2(dx, dy)) % 180.0   # 0=北
            angs.append(a)
    if not angs:
        return 0.0, 0
    hist, _ = np.histogram(angs, bins=bins, range=(0, 180))
    p = hist / hist.sum()
    H = -sum(x * math.log(x) for x in p if x > 0)
    return H / math.log(bins), len(angs)

def corridor_lines(c):
    if c is None or c.is_empty:
        return []
    return [c] if c.geom_type == "LineString" else list(c.geoms)

# ---- C5a 走廊线反事实（全部在投影米制坐标下构建与计算）----
real_lines = corridor_lines(corridor)
if real_lines:
    real_lines_m = [to_m(l) for l in real_lines]
    real_len = sum(l.length for l in real_lines_m)
    pts_m = [p for l in real_lines_m for p in l.coords]
    south = min(pts_m, key=lambda p: p[1])
    north = max(pts_m, key=lambda p: p[1])
    end_dist = math.hypot(north[0] - south[0], north[1] - south[1])
    # GRID_NULL：正北直线（同端到端）
    grid_line_m = LineString([south, (south[0], north[1])])
    # RANDOM_NULL：随机游走（米制；步长=真实平均段长，步数=真实段数，seed=42）
    seg_counts = sum(max(1, len(l.coords) - 1) for l in real_lines_m)
    step = real_len / seg_counts if seg_counts else 100
    rng = np.random.default_rng(42)
    x, y = south[0], south[1]
    walk = [(x, y)]
    target = math.atan2(0.0, north[1] - south[1])   # 正北
    for i in range(seg_counts):
        a = target + rng.normal(0, 0.55)
        x += step * math.sin(a)
        y += step * math.cos(a)
        walk.append((x, y))
    rand_line_m = LineString(walk)
    # DESIGN：REAL + 6 处东西缝合短线（每处 120m，米制）
    design_lines_m = list(real_lines_m)
    for sx, sy in [(116.33152, 39.99924), (116.33182, 39.99151), (116.33237, 39.98487),
                   (116.33414, 39.97504), (116.33909, 39.9662), (116.34191, 39.95681)]:
        mx, my = TRANS.transform(sx, sy)
        design_lines_m.append(LineString([(mx - 60, my), (mx + 60, my)]))
    models = {
        "REAL_走廊": real_lines_m,
        "GRID_NULL_正北直线": [grid_line_m],
        "RANDOM_NULL_随机游走": [rand_line_m],
        "DESIGN_走廊+缝合": design_lines_m,
    }
    c5a = {}
    for nm, lns in models.items():
        H, n = bearing_entropy(lns)
        tot = sum(l.length for l in lns)
        sinu = tot / end_dist if end_dist else None
        angs = []
        for ln in lns:
            coords = list(ln.coords)
            for i in range(len(coords) - 1):
                dx = coords[i + 1][0] - coords[i][0]; dy = coords[i + 1][1] - coords[i][1]
                if abs(dx) + abs(dy) < 1e-9:
                    continue
                angs.append(math.degrees(math.atan2(dx, dy)) % 180.0)
        aligned = sum(1 for a in angs if a < 20 or a > 160) / len(angs) if angs else 0.0
        c5a[nm] = {"bearing_entropy_norm": round(H, 3), "n_segments": n,
                   "sinuosity": round(sinu, 3) if sinu else None,
                   "n_s_aligned_ratio": round(aligned, 3),
                   "total_length_m": round(tot, 0)}
    for nm in c5a:
        registry_put("C5_CF", f"corridor_{nm}_bearing_entropy", c5a[nm]["bearing_entropy_norm"], "ratio",
                     "线段朝向熵（12箱香农熵/ln12，米制投影坐标）",
                     f"{nm} 朝向熵（走廊线反事实）",
                     caveat="随机游走 seed=42；缝合长度 120m 假设；走廊轴线为推导参考线")
else:
    c5a = {}

# ---- C5b 绿地斑块长轴朝向反事实 ----
def patch_axes(patches):
    angs = []
    for _, g in patches:
        gm = to_m(g)
        if gm.area < 500:
            continue
        coords = get_coordinates(gm)
        if len(coords) < 3:
            continue
        c = coords - coords.mean(axis=0)
        try:
            _, _, v = np.linalg.svd(c)
            ax = v[0]
            a = math.degrees(math.atan2(ax[0], ax[1])) % 180.0
            angs.append(a)
        except Exception:
            continue
    return angs

green_geoms = [(e, g) for e, g in layers["green"] if g.geom_type in ("Polygon", "MultiPolygon")]
real_angs = patch_axes(green_geoms)

def entropy(angs, bins=12):
    if not angs:
        return 0.0, 0
    hist, _ = np.histogram(angs, bins=bins, range=(0, 180))
    p = hist / hist.sum()
    H = -sum(x * math.log(x) for x in p if x > 0)
    return H / math.log(bins), len(angs)

real_H, real_n = entropy(real_angs)
# GRID_NULL：同数量正交矩形（长轴全为 0°）→ 熵=0
grid_angs = [0.0] * max(real_n, 1)
grid_H, _ = entropy(grid_angs)
# RANDOM_NULL：均匀随机朝向
rng = np.random.default_rng(7)
rand_angs = list(rng.uniform(0, 180, max(real_n, 1)))
rand_H, _ = entropy(rand_angs)

c5b = {
    "REAL_绿地斑块": {"n_patches_measured": real_n, "orientation_entropy_norm": round(real_H, 3)},
    "GRID_NULL_正交网格": {"n_patches_measured": len(grid_angs), "orientation_entropy_norm": round(grid_H, 3)},
    "RANDOM_NULL_随机散布": {"n_patches_measured": len(rand_angs), "orientation_entropy_norm": round(rand_H, 3)},
    "interpretation": "REAL 应远高于 GRID(0)：约束（铁路/河流/存量地块）释放的是『去网格化』的相干形态而非强加秩序（阿尔罕布拉范式同构判据）",
}
registry_put("C5_CF", "green_real_orientation_entropy", round(real_H, 3), "ratio",
             "绿地斑块长轴朝向熵（12箱/ln12）",
             "现状绿地朝向熵：对比 GRID=0 / RANDOM≈1 判断约束指纹",
             caveat="长轴=形状点集SVD第一主轴；网格/随机为解析对照（同数量）")
registry_put("C5_CF", "green_grid_orientation_entropy", round(grid_H, 3), "ratio",
             "正交网格零模型长轴朝向熵", "强加秩序基准=0", caveat="解析对照")
registry_put("C5_CF", "green_random_orientation_entropy", round(rand_H, 3), "ratio",
             "随机散布零模型长轴朝向熵", "无约束基准≈1", caveat="seed=7 解析对照")

result = {"meta": {"model": "counterfactual null models (REAL/GRID/RANDOM/DESIGN)",
                   "note": "指标定义在四模型间保持一致；坐标已投影 EPSG:4548"},
          "c5a_corridor": c5a,
          "c5b_green_patches": c5b}
json.dump(result, open(os.path.join(CALC, "c5_counterfactual.json"), "w"), ensure_ascii=False, indent=2)

# ---- 图 ----
plt = setup_chinese_fonts()
fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
if c5a:
    names = list(c5a.keys())
    x = np.arange(len(names))
    ax = axes[0]
    ax.bar(x, [c5a[n]["bearing_entropy_norm"] for n in names], color=["#b08a4f", "#8a97a8", "#8a97a8", "#2e9e6b"])
    ax.set_xticks(x); ax.set_xticklabels(names, rotation=12)
    ax.set_ylim(0, 1.05)
    ax.set_title("C5a · 走廊线朝向熵（12箱/ln12）\n约束指纹=REAL 显著高于 GRID_NULL(0)")
    ax.set_ylabel("朝向熵")
names2 = list(c5b.keys())[:3]
ax2 = axes[1]
ax2.bar(names2, [c5b[n]["orientation_entropy_norm"] for n in names2], color=["#b08a4f", "#8a97a8", "#8a97a8"])
ax2.set_title("C5b · 绿地斑块长轴朝向熵\nREAL 接近 RANDOM、远离 GRID = 去网格化约束形态")
ax2.set_ylabel("朝向熵")
fig.suptitle("图 C5 · 反事实零模型：约束释放的涌现（不是强加的网格）", fontweight="bold", fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "c5_counterfactual.png"), dpi=150, bbox_inches="tight")
print(json.dumps(c5a, ensure_ascii=False, indent=1))
print(json.dumps(c5b, ensure_ascii=False, indent=1))
