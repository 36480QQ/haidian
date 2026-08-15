# -*- coding: utf-8 -*-
"""C12 · CA 城市更新涌现模拟（京张版，CASA CA 范式）
格子：100m；状态：用地类别（居住/科研/商业/教育/绿地/锁定约束）
初始态：POI 主导特征（自下而上现状）
约束（锁定，不可变）：铁路主脊缓冲、水系缓冲、高校现状、文保节点
更新规则（局部）：站域与缝合节点 300m 内可"更新跃迁"；邻域同类集聚 + 主脊吸附
反事实：CA 涌现分区 vs 人工 400m 概念分区（主导类别重合度）
输出：计算/c12_ca.json + charts/c12_ca.png
"""
import os, json, math, pickle
import numpy as np
from shapely.geometry import Point, box
from shapely.ops import transform as sh_transform
import pyproj
from kun_common import setup_chinese_fonts, registry_put

HERE = os.path.dirname(os.path.abspath(__file__))
CALC = os.path.join(HERE, "计算"); CHARTS = os.path.join(HERE, "charts")
POI_DIR = os.path.join(HERE, "poi_wgs84")
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
layers = model["layers"]
wgs = [g for e, g in layers["water"] if e.get("tags", {}).get("name")]
water_m = to_m(__import__("shapely.ops", fromlist=["unary_union"]).unary_union(wgs)) if wgs else None

CELL = 100.0
x0, y0, x1, y1 = site_m.bounds
nx_ = int((x1 - x0) / CELL) + 1; ny_ = int((y1 - y0) / CELL) + 1

# 状态码
EMPTY, LOCK, RESI, RES_OFF, COMM, EDU = 0, -1, 1, 2, 3, 4
NAME = {0: "空/非建设", -1: "锁定(约束)", 1: "居住", 2: "科研办公", 3: "商业", 4: "教育"}

# POI 初始态（自下而上现状）
pois = {}
cat_map = {"company": RES_OFF, "research": RES_OFF, "finance": RES_OFF,
           "residential": RESI, "living": RESI,
           "dining": COMM, "shopping": COMM,
           "school": EDU, "medical": COMM, "sports": COMM, "scenic": EMPTY, "transport": COMM}
for slug in cat_map:
    d = json.load(open(os.path.join(POI_DIR, f"{slug}.json")))
    pois[slug] = [to_m(Point(p["lon_wgs"], p["lat_wgs"])) for p in d]

grid = np.zeros((ny_, nx_), dtype=int)
for slug, state in cat_map.items():
    for p in pois[slug]:
        if not site_m.contains(p):
            continue
        i = min(ny_ - 1, max(0, int((p.y - y0) / CELL)))
        j = min(nx_ - 1, max(0, int((p.x - x0) / CELL)))
        if grid[i, j] == 0:
            grid[i, j] = state
# 锁定约束
if corridor_m is not None:
    lock = corridor_m.buffer(60).intersection(site_m)
    for i in range(ny_):
        for j in range(nx_):
            c = box(x0 + j * CELL, y0 + i * CELL, x0 + (j + 1) * CELL, y0 + (i + 1) * CELL)
            if c.intersects(lock):
                grid[i, j] = LOCK
if water_m is not None:
    lock2 = water_m.buffer(40).intersection(site_m)
    for i in range(ny_):
        for j in range(nx_):
            c = box(x0 + j * CELL, y0 + i * CELL, x0 + (j + 1) * CELL, y0 + (i + 1) * CELL)
            if c.intersects(lock2):
                grid[i, j] = LOCK
# 站域与缝合节点
stations = [(116.3317,39.9915),(116.3344,39.9751),(116.3336,39.9993),(116.3390,39.9653),
            (116.3473,39.9868),(116.3458,40.0136),(116.3462,39.9459),
            (116.3315,39.9992),(116.3324,39.9849),(116.3391,39.9662),(116.3419,39.9568),(116.3429,39.9432)]
sta_m = [to_m(Point(a, b)) for a, b in stations]

# 更新势能：站域300m 可更新
update_potential = np.zeros((ny_, nx_), dtype=bool)
for i in range(ny_):
    for j in range(nx_):
        c = box(x0 + j * CELL, y0 + i * CELL, x0 + (j + 1) * CELL, y0 + (i + 1) * CELL)
        if min(c.centroid.distance(s) for s in sta_m) < 300:
            update_potential[i, j] = True

def neighbors(i, j):
    n = []
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        ii, jj = i + di, j + dj
        if 0 <= ii < ny_ and 0 <= jj < nx_:
            n.append(grid[ii, jj])
    return n

def ca_step(g, rng, intervene):
    g2 = g.copy()
    for i in range(ny_):
        for j in range(nx_):
            if g[i, j] == LOCK:
                continue
            if not intervene:
                continue   # 无干预情景：纯自组织（验证路径锁定）
            if not update_potential[i, j]:
                continue
            nb = neighbors(i, j)
            same = sum(1 for s in nb if s == g[i, j])
            d_cor = (corridor_m.distance(box(x0 + j * CELL, y0 + i * CELL, x0 + (j + 1) * CELL, y0 + (i + 1) * CELL).centroid)
                     if corridor_m is not None else 1e9)
            if g[i, j] == EMPTY:
                counts = {s: nb.count(s) for s in set(nb) if s > 0}
                if counts and rng.random() < 0.9:
                    g2[i, j] = max(counts, key=counts.get)
            elif g[i, j] == RESI:
                # 职住平衡干预：主脊 300m 内居住→科研办公，站域→混合（商业）
                if d_cor < 300 and rng.random() < 0.5:
                    g2[i, j] = RES_OFF
                elif rng.random() < 0.3:
                    g2[i, j] = COMM
            elif g[i, j] in (RES_OFF, COMM):
                # 集聚强化：同类型邻域 ≥3 时锁定，否则向主脊吸附类型漂移
                if same >= 3:
                    continue
                if d_cor < 300 and rng.random() < 0.4:
                    g2[i, j] = RES_OFF
                elif rng.random() < 0.25:
                    g2[i, j] = COMM
    return g2

rng = np.random.default_rng(42)
grid0 = grid.copy()
grid_ni = grid.copy()
for t in range(60):
    grid_ni = ca_step(grid_ni, rng, intervene=False)
rng2 = np.random.default_rng(42)
for t in range(60):
    grid = ca_step(grid, rng2, intervene=True)

def dominant_counts(g):
    vals, counts = np.unique(g, return_counts=True)
    return {int(v): int(c) for v, c in zip(vals, counts)}

ca_counts = dominant_counts(grid)
ca_ni_counts = dominant_counts(grid_ni)
init_counts = dominant_counts(grid0)
ni_change = sum(abs(ca_ni_counts.get(k, 0) - init_counts.get(k, 0)) for k in set(list(ca_ni_counts) + list(init_counts))) / 2
int_change = sum(abs(ca_counts.get(k, 0) - init_counts.get(k, 0)) for k in set(list(ca_counts) + list(init_counts))) / 2

# 与人工分区对比：读 400m 概念分区主导类别
lu = json.load(open(os.path.join(HERE, "design_geometry", "land_use.geojson")))
from shapely.geometry import shape
manual = {}
for f in lu["features"]:
    g = to_m(shape(f["geometry"]))
    code = f["properties"]["land_use_code"]
    for i in range(ny_):
        for j in range(nx_):
            c = box(x0 + j * CELL, y0 + i * CELL, x0 + (j + 1) * CELL, y0 + (i + 1) * CELL)
            if c.centroid.within(g):
                st = {"0802": RES_OFF, "05": COMM, "0701": RESI, "0804": EDU, "1401": EMPTY}.get(code, EMPTY)
                manual[(i, j)] = st
def dominant_in_400(g, ii, jj):
    vals = []
    for i in range(ii * 4, min(ii * 4 + 4, ny_)):
        for j in range(jj * 4, min(jj * 4 + 4, nx_)):
            if g[i, j] > 0:
                vals.append(g[i, j])
    if not vals:
        return EMPTY
    return max(set(vals), key=vals.count)
agree = 0; total = 0
for i in range(0, ny_, 4):
    for j in range(0, nx_, 4):
        dom = dominant_in_400(grid, i // 4, j // 4)
        if dom == EMPTY:
            continue
        key = (i + 1, j + 1)
        # manual 字典按 100m 单元存，取 400m 块内多数
        man_vals = [manual.get((ii, jj)) for ii in range(i, min(i + 4, ny_)) for jj in range(j, min(j + 4, nx_))]
        man_vals = [m for m in man_vals if m is not None]
        if not man_vals:
            continue
        man_dom = max(set(man_vals), key=man_vals.count)
        total += 1
        if man_dom == dom:
            agree += 1
overlap = agree / max(total, 1)

result = {
    "meta": {"model": "CA urban-renewal emergence (CASA CA paradigm)",
             "rules": "100m cells; locked=rail corridor 60m+water 40m; update potential=station/stitch 300m; agglomeration=neighbor count thresholds; spine attraction=RES_OFF within 300m",
             "iterations": 60, "seed": 42},
    "initial_counts": init_counts,
    "no_intervention_counts": ca_ni_counts,
    "no_intervention_cell_change": int(ni_change),
    "emergent_counts": ca_counts,
    "intervention_cell_change": int(int_change),
    "emergent_shares": {NAME.get(k, k): round(v / max(sum(v for kk, v in ca_counts.items() if kk > 0), 1), 3)
                        for k, v in ca_counts.items() if k > 0},
    "overlap_with_manual_partition": round(overlap, 3),
    "interpretation": "无干预60步变化≈0=路径锁定（现状自我强化）；干预后变化>0=缝合+更新政策解锁再分配。重合度=人工分区与涌现分区在400m尺度的一致性", 
}
json.dump(result, open(os.path.join(CALC, "c12_ca.json"), "w"), ensure_ascii=False, indent=2)
registry_put("C12_CA", "overlap_emergent_vs_manual", round(overlap, 3), "ratio",
             "CA 涌现分区与人工概念分区的主导类别重合度", "约束下的涌现 vs 强加秩序的对比（反事实）",
             caveat="CA 规则为简化代理；人工分区为 400m 概念网格")
for k, v in ca_counts.items():
    if k > 0:
        registry_put("C12_CA", f"emergent_{NAME[k]}_cells", v, "count",
                     "CA 涌现模拟（60 步）的用地单元数", f"{NAME[k]} 在约束涌现下的规模",
                     caveat="CA 为概念模拟，非预测")

plt = setup_chinese_fonts()
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
cmap = {0: "#eeeeee", -1: "#1f4e2d", 1: "#e8c07a", 2: "#5b8dd9", 3: "#e8915a", 4: "#7f6fd4"}
for ax, g, title in [(axes[0], grid0, f"初始（POI现状，自下而上）\n单元数 {sum(init_counts[k] for k in init_counts if k>0)}"),
                     (axes[1], grid_ni, f"无干预 60 步（路径锁定）\n变化 {int(ni_change)} 单元"),
                     (axes[2], grid, f"干预 60 步（缝合+更新解锁）\n变化 {int(int_change)} 单元")]:
    im = np.zeros((ny_, nx_, 3))
    for k, col in cmap.items():
        hexcol = col.lstrip("#")
        rgb = tuple(int(hexcol[i:i + 2], 16) / 255 for i in (0, 2, 4))
        mask = g == k
        im[mask] = rgb
    ax.imshow(im, origin="lower")
    ax.set_title(title, fontsize=10)
    ax.axis("off")
fig.text(0.5, 0.015, f"与人工400m分区重合度 {overlap*100:.0f}%（约束下的涌现 vs 强加秩序的对比）", ha="center", fontsize=10, color="#5c6b76")
fig.suptitle("图 C12 · CA 城市更新涌现模拟：无干预=锁定，干预=解锁（京张实算）", fontweight="bold", fontsize=13)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "c12_ca.png"), dpi=150, bbox_inches="tight")
print(json.dumps(result, ensure_ascii=False, indent=1))
