#!/usr/bin/env python3
"""
京张智脉 — 5 张专业城市设计图生成 v3
排版 v3：标签全部移到场地外左右空白带 + 引线连接 + 垂直等距避让，
图例移到底部横排，彻底消除字与字、字与图重叠。
"""
import json, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
from shapely.geometry import shape, mapping, box, LineString, Point
from matplotlib.path import Path
from matplotlib.patches import PathPatch

SUB = "submissions/xusu-ai/jingzhang-ai-vein"
GEOM = f"{SUB}/geometry"
FIG = f"{SUB}/assets/figures"
import os
os.makedirs(FIG, exist_ok=True)

# 深色专业底色
BG = "#0E1420"
FG = "#E8EDF5"
ACCENT = "#2E5BFF"
COPPER = "#B8860B"
GREEN = "#3D9E6A"
GRID = "#2A3547"
MUT = "#8A94A6"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": FG, "axes.edgecolor": GRID, "axes.labelcolor": FG,
    "xtick.color": GRID, "ytick.color": GRID,
    "font.family": "WenQuanYi Zen Hei",
})
import matplotlib.font_manager as fm
for fp in ["/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"]:
    if os.path.exists(fp):
        fm.fontManager.addfont(fp)
plt.rcParams["font.family"] = "WenQuanYi Zen Hei"

def load(name):
    return json.load(open(f"{GEOM}/{name}.geojson"))

def shp(fc):
    return [shape(f["geometry"]) for f in fc["features"]]

site = shp(load("site_boundary"))[0]
minx, miny, maxx, maxy = site.bounds
CX = (minx + maxx) / 2
PAD = 0.0025          # 标签与场地边缘的间距
XLIM = (minx - 0.014, maxx + 0.014)   # 左右留出标签空白带

# 用地配色（MNR 码 → 颜色）
LU_COLORS = {
    "0802": "#2E5BFF",  # 科研 - 智脉蓝
    "0803": "#7B5BFF",  # 文化 - 紫
    "0701": "#E0A63C",  # 居住 - 暖金
    "05":   "#E05B6D",  # 商业 - 玫红
    "1401": "#3D9E6A",  # 公园 - 绿
}
LU_NAMES = {"0802": "科研用地", "0803": "文化用地", "0701": "居住用地", "05": "商业用地", "1401": "公园绿地"}

def draw_site_ctx(ax):
    """画场地边界 + 网格"""
    ax.add_patch(PathPatch(Path(site.exterior.coords), facecolor="none",
                           edgecolor=GRID, linewidth=1.2, zorder=1))
    for gx in range(3, 7):
        ax.axvline(minx + (maxx-minx)*gx/10, color=GRID, linewidth=0.4, alpha=0.5, zorder=0)
    for gy in range(2, 8):
        ax.axhline(miny + (maxy-miny)*gy/10, color=GRID, linewidth=0.4, alpha=0.5, zorder=0)

def plot_polys(ax, geoms, color, alpha=0.85, lw=0.4, hatch=None, ec="#0E1420"):
    for g in geoms:
        ax.add_patch(PathPatch(Path(g.exterior.coords), facecolor=color, alpha=alpha,
                               edgecolor=ec, linewidth=lw, hatch=hatch, zorder=2))

def leader_labels(ax, items, side, fs=9.5, color="#FFFFFF", lcolor="#4A5878", cw=0.7, ms=3.0):
    """items: [(geom, text), ...]
    按 centroid.y 排序后在场外垂直等距展开，细引线连接 centroid 锚点。
    side: 'left' | 'right' —— 标签靠场地左/右缘，文字向外延伸。"""
    n = len(items)
    if not n:
        return
    items = sorted(items, key=lambda it: it[0].centroid.y)
    xa = minx - PAD if side == "left" else maxx + PAD
    ha = "right" if side == "left" else "left"
    ys = [miny + (maxy - miny) * (i + 0.5) / n for i in range(n)]
    for (geom, text), ty in zip(items, ys):
        c = geom.centroid
        ax.plot([c.x, xa], [c.y, ty], color=lcolor, lw=cw, alpha=0.75,
                solid_capstyle="round", zorder=4)
        ax.plot([c.x], [c.y], marker="o", ms=ms, color=lcolor, zorder=5)
        ax.text(xa, ty, text, color=color, fontsize=fs, ha=ha, va="center", zorder=6,
                bbox=dict(boxstyle="round,pad=0.28", fc=BG, ec=lcolor, lw=0.7, alpha=0.92))

def footer(ax, text):
    ax.text(0.5, -0.125, text, transform=ax.transAxes, ha="center",
            fontsize=8, color=MUT)

def bottom_legend(ax, handles, ncol):
    leg = ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.055),
                    ncol=ncol, fontsize=9, framealpha=0.9, facecolor=BG,
                    edgecolor=GRID, labelcolor=FG, columnspacing=1.2, handlelength=1.4)
    return leg

def check_text_overlaps(fig, name):
    """渲染层精确检测：所有 Text artist（含 title/suptitle/legend/note）的实际窗口 bbox 互相重叠。
    排除两类误报：legend 文字 vs 自身边框；suptitle 在 fig.texts 中的重复记录。"""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    items = []  # (描述, bbox, 组id)  组id相同者不互相比较
    gid = 0
    for ax in fig.axes:
        if ax.get_title().strip():
            items.append((f"title[{ax.get_title()[:16]}]", ax.title.get_window_extent(renderer), None))
        for t in ax.texts:
            if t.get_text().strip():
                items.append((f"text[{t.get_text()[:16]}]", t.get_window_extent(renderer), None))
        leg = ax.get_legend()
        if leg:
            gid += 1
            items.append((f"legend框[{leg.get_texts()[0].get_text()[:8]}…]", leg.get_window_extent(renderer), gid))
            for t in leg.get_texts():
                items.append((f"legend[{t.get_text()[:16]}]", t.get_window_extent(renderer), gid))
    suptitle_id = None
    if fig._suptitle is not None and fig._suptitle.get_text().strip():
        suptitle_id = id(fig._suptitle)
        items.append((f"suptitle[{fig._suptitle.get_text()[:16]}]", fig._suptitle.get_window_extent(renderer), None))
    for t in fig.texts:
        if t.get_text().strip() and id(t) != suptitle_id:
            items.append((f"figtext[{t.get_text()[:16]}]", t.get_window_extent(renderer), None))
    overlaps = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i][2] is not None and items[i][2] == items[j][2]:
                continue  # 同一图例组内不比较
            b1, b2 = items[i][1], items[j][1]
            ox = min(b1.x1, b2.x1) - max(b1.x0, b2.x0)
            oy = min(b1.y1, b2.y1) - max(b1.y0, b2.y0)
            if ox > 2 and oy > 2:
                overlaps.append((items[i][0], items[j][0], ox * oy))
    if overlaps:
        print(f"⚠️ {name}: {len(overlaps)} 处文字重叠")
        for t1, t2, area in sorted(overlaps, key=lambda t: -t[2])[:12]:
            print(f"    {t1} × {t2} 面积={area:.0f}")
    else:
        print(f"✅ {name}: 无文字重叠")

# ============ 1. site-overview.png ============
fig, ax = plt.subplots(figsize=(12, 9), dpi=150)
fig.subplots_adjust(left=0.01, right=0.99, top=0.90, bottom=0.17)
draw_site_ctx(ax)
lu_fc = load("land_use")
for f in lu_fc["features"]:
    g = shape(f["geometry"])
    code = f["properties"]["land_use_code"]
    c = LU_COLORS.get(code, "#555")
    ax.add_patch(PathPatch(Path(g.exterior.coords), facecolor=c, alpha=0.7,
                           edgecolor="#0E1420", linewidth=0.5, zorder=2))
# 公园带高亮
for f in lu_fc["features"]:
    if f["properties"]["land_use_code"] == "1401":
        g = shape(f["geometry"])
        ax.add_patch(PathPatch(Path(g.exterior.coords), facecolor="none",
                               edgecolor=GREEN, linewidth=2.2, zorder=4))
# 重点区虚线框
ka_fc = load("key_areas")
for f in ka_fc["features"]:
    g = shape(f["geometry"])
    ax.add_patch(PathPatch(Path(g.exterior.coords), facecolor="none", edgecolor="#FFFFFF",
                           linewidth=1.6, linestyle="--", zorder=5))
# 重点区标签 —— 全部移到场地左侧空白带，垂直等距 + 引线
ka_labels = {
    "PROV-KEY-001": "众智园AI加速区",
    "PROV-KEY-002": "AI原点社区",
    "PROV-KEY-003": "大钟寺AI集聚区",
}
ka_items = [(shape(f["geometry"]), ka_labels.get(f["id"], f["id"])) for f in ka_fc["features"]]
leader_labels(ax, ka_items, "left", fs=10.5, color="#FFFFFF", lcolor="#4A5878", cw=0.9, ms=3.6)
# 智脉纵轴 —— 竖线 + 右侧空白带旋转文字
spine_x = minx + (maxx - minx) * 0.34
ax.annotate("", xy=(spine_x, maxy), xytext=(spine_x, miny),
            arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=3, linestyle="--", zorder=6))
ax.text(maxx + PAD + 0.001, (miny + maxy) / 2, "京张智脉纵轴  Jingzhang AI Vein Spine",
        color=ACCENT, fontsize=11, fontweight="bold", rotation=90, va="center",
        ha="left", zorder=6,
        bbox=dict(boxstyle="round,pad=0.28", fc=BG, ec=ACCENT, lw=0.7, alpha=0.92))
# 图例 —— 底部横排
handles = [mpatches.Patch(color=LU_COLORS["0802"], label="科研 0802 (AI研发)"),
           mpatches.Patch(color=LU_COLORS["05"], label="商业 05"),
           mpatches.Patch(color=LU_COLORS["0701"], label="居住 0701 (人才社区)"),
           mpatches.Patch(color=LU_COLORS["0803"], label="文化 0803"),
           mpatches.Patch(color=LU_COLORS["1401"], label="公园绿地 1401"),
           mpatches.Patch(facecolor="none", edgecolor="#FFFFFF", linestyle="--", label="重点区 (provisional)")]
bottom_legend(ax, handles, 6)
ax.set_title("京张智脉 · 总体设计范围用地总览\nJingzhang AI Vein — Land Use Overview (provisional boundary)",
             fontsize=14, fontweight="bold", color=FG, pad=10)
footer(ax, "来源: geometry/land_use.geojson · 边界: provisional_constraint (非官方红线) · 场地 11.41 km²")
ax.set_xlim(*XLIM); ax.set_ylim(miny - 0.001, maxy + 0.001)
ax.set_aspect("equal"); ax.axis("off")
check_text_overlaps(fig, "site-overview")
plt.savefig(f"{FIG}/site-overview.png", dpi=150); plt.close()
print("✅ site-overview.png")

# ============ 2. land-use-structure.png ============
fig, ax = plt.subplots(figsize=(12, 9), dpi=150)
fig.subplots_adjust(left=0.01, right=0.99, top=0.90, bottom=0.17)
draw_site_ctx(ax)
for f in lu_fc["features"]:
    g = shape(f["geometry"])
    code = f["properties"]["land_use_code"]
    c = LU_COLORS.get(code, "#555")
    ax.add_patch(PathPatch(Path(g.exterior.coords), facecolor=c, alpha=0.75,
                           edgecolor="#0E1420", linewidth=0.6, zorder=2))
# 9 块标签 —— 按 x 位置分左右两侧，外部引线标注
total = site.area
for f in lu_fc["features"]:
    f["_geom"] = shape(f["geometry"])
lu_fc["features"].sort(key=lambda f: f["_geom"].centroid.x)
left_items, right_items = [], []
for f in lu_fc["features"]:
    g = f["_geom"]
    lbl = f["properties"].get("label_zh", "")
    short = lbl.split("（")[0] if "（" in lbl else lbl
    code = f["properties"]["land_use_code"]
    text = f"{short} · {f['id']}"
    (left_items if g.centroid.x < CX else right_items).append((g, text))
leader_labels(ax, left_items, "left", fs=9.5)
leader_labels(ax, right_items, "right", fs=9.5)
# 用地占比统计
for code, name in [("0802", "科研"), ("05", "商业"), ("0701", "居住"), ("0803", "文化"), ("1401", "公园")]:
    area = sum(f["_geom"].area for f in lu_fc["features"] if f["properties"]["land_use_code"] == code)
    print(f"  {name}: {area/total*100:.1f}%")
# 图例 —— 底部横排
handles = [mpatches.Patch(color=LU_COLORS["0802"], label="科研用地 0802"),
           mpatches.Patch(color=LU_COLORS["05"], label="商业用地 05"),
           mpatches.Patch(color=LU_COLORS["0701"], label="居住用地 0701"),
           mpatches.Patch(color=LU_COLORS["0803"], label="文化用地 0803"),
           mpatches.Patch(color=LU_COLORS["1401"], label="公园绿地 1401")]
bottom_legend(ax, handles, 5)
ax.set_title("京张智脉 · 用地结构分区\nLand Use Structure — 9 topological parcels, gap-free & overlap-free",
             fontsize=14, fontweight="bold", pad=10)
footer(ax, "来源: geometry/land_use.geojson · 联合面积=场地面积(拓扑闭合) · 概念分区非控规")
ax.set_xlim(*XLIM); ax.set_ylim(miny - 0.001, maxy + 0.001)
ax.set_aspect("equal"); ax.axis("off")
check_text_overlaps(fig, "land-use-structure")
plt.savefig(f"{FIG}/land-use-structure.png", dpi=150); plt.close()
print("✅ land-use-structure.png")

# ============ 3. key-areas.png ============
# 统一显示窗口（同高宽比 → 三个子图 axes 形状一致、顶部对齐，消除扁条错位）
WW, WH = 0.013, 0.0286
ka_data = [
    ("PROV-KEY-001", "众智园AI自主创新加速区", "ZHI Source · 全栈自主+治理", "科研核心 · 清河界面 · 安全治理沙盒"),
    ("PROV-KEY-002", "北京AI原点社区", "ZHI Origin · 近校转化+人才特区", "改造更新 · 开源发布 · 成果转化街"),
    ("PROV-KEY-003", "大钟寺AI产业聚集区", "ZHI Market · 智能经济+国际交往", "商业核心 · 轨道一体化 · 路演客厅"),
]
ka_geoms = {f["id"]: shape(f["geometry"]) for f in load("key_areas")["features"]}
fig, axes = plt.subplots(1, 3, figsize=(16, 6.2), dpi=150)
fig.subplots_adjust(top=0.78, bottom=0.14, left=0.02, right=0.98, wspace=0.10)
for ax, (kid, name_zh, name_en, note) in zip(axes, ka_data):
    ax.set_facecolor(BG)
    kg = ka_geoms[kid]
    c = kg.centroid
    win = box(c.x - WW / 2, c.y - WH / 2, c.x + WW / 2, c.y + WH / 2)
    for f in lu_fc["features"]:
        g = f["_geom"]
        if g.intersects(win):
            code = f["properties"]["land_use_code"]
            ax.add_patch(PathPatch(Path(g.exterior.coords), facecolor=LU_COLORS.get(code, "#555"),
                                   alpha=0.7, edgecolor="#0E1420", linewidth=0.5, zorder=2))
    ax.add_patch(PathPatch(Path(kg.exterior.coords), facecolor="none", edgecolor="#FFFFFF",
                           linewidth=2, linestyle="--", zorder=5))
    ax.set_xlim(c.x - WW / 2, c.x + WW / 2)
    ax.set_ylim(c.y - WH / 2, c.y + WH / 2)
    ax.set_title(f"{name_zh}\n{name_en}", fontsize=11.5, fontweight="bold", color=FG, pad=10)
    ax.text(0.5, -0.08, note, transform=ax.transAxes, ha="center", fontsize=9, color="#B8C2D4")
    ax.set_aspect("equal"); ax.axis("off")
fig.suptitle("京张智脉 · 三处重点区域详细设计索引\nThree Key Areas — Detailed Design Index (provisional polygons)",
             fontsize=14, fontweight="bold", y=0.96)
check_text_overlaps(fig, "key-areas")
plt.savefig(f"{FIG}/key-areas.png", dpi=150); plt.close()
print("✅ key-areas.png")

# ============ 4. mobility-bluegreen.png ============
fig, ax = plt.subplots(figsize=(12, 9), dpi=150)
fig.subplots_adjust(left=0.01, right=0.99, top=0.90, bottom=0.17)
draw_site_ctx(ax)
# 绿地
for f in load("green_space")["features"]:
    g = shape(f["geometry"])
    ax.add_patch(PathPatch(Path(g.exterior.coords), facecolor=GREEN, alpha=0.55,
                           edgecolor=GREEN, linewidth=1.0, zorder=2))
# 公共空间
for f in load("public_space")["features"]:
    g = shape(f["geometry"])
    ax.add_patch(PathPatch(Path(g.exterior.coords), facecolor=COPPER, alpha=0.8,
                           edgecolor=COPPER, linewidth=0.8, zorder=4))
# 道路
for f in load("roads")["features"]:
    g = shape(f["geometry"])
    xs, ys = g.xy
    cls = f["properties"].get("road_class", "local")
    color = "#FFFFFF" if cls == "arterial" else "#9AA7BD"
    lw = 3.2 if cls == "arterial" else 1.8
    ax.plot(xs, ys, color=color, linewidth=lw, zorder=5,
            solid_capstyle="round", alpha=0.95)
# 重点区
for f in load("key_areas")["features"]:
    g = shape(f["geometry"])
    ax.add_patch(PathPatch(Path(g.exterior.coords), facecolor="none", edgecolor="#FFFFFF",
                           linewidth=1.4, linestyle="--", zorder=6))
# 标注 —— 移到左右空白带，引线指向，bbox 隔离
bg_mid = (minx + (maxx - minx) * 0.38, (miny + maxy) / 2)
ax.annotate("京张遗址公园活力带\n(Blue-Green Spine)", xy=bg_mid,
            xytext=(minx - PAD - 0.001, maxy - 0.006),
            color=GREEN, fontsize=10.5, fontweight="bold", zorder=7,
            ha="right", va="top",
            bbox=dict(boxstyle="round,pad=0.28", fc=BG, ec=GREEN, lw=0.8, alpha=0.92),
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5))
spine_pt = (minx + (maxx - minx) * 0.34, (miny + maxy) * 0.45)
ax.annotate("智脉纵轴\n(AI Vein Spine)", xy=spine_pt,
            xytext=(maxx + PAD + 0.001, miny + 0.010),
            color="#FFFFFF", fontsize=10, zorder=7, ha="left", va="bottom",
            bbox=dict(boxstyle="round,pad=0.28", fc=BG, ec="#FFFFFF", lw=0.7, alpha=0.92),
            arrowprops=dict(arrowstyle="->", color="#FFFFFF", lw=1.2))
# 图例 —— 底部横排
handles = [mpatches.Patch(color=GREEN, label="绿地/公园带"),
           mpatches.Patch(color=COPPER, label="公共空间/广场"),
           mpatches.Patch(color="#FFFFFF", label="智脉纵轴(主干)"),
           mpatches.Patch(color="#9AA7BD", label="横向连接路"),
           mpatches.Patch(facecolor="none", edgecolor="#FFFFFF", linestyle="--", label="重点区")]
bottom_legend(ax, handles, 5)
ax.set_title("京张智脉 · 交通慢行与蓝绿公共空间复合系统\nMobility & Blue-Green Network — spine, loops, plazas",
             fontsize=14, fontweight="bold", pad=10)
footer(ax, "来源: geometry/roads|green_space|public_space.geojson · 道路为概念骨架非红线 · 绿地率25%")
ax.set_xlim(*XLIM); ax.set_ylim(miny - 0.001, maxy + 0.001)
ax.set_aspect("equal"); ax.axis("off")
check_text_overlaps(fig, "mobility-bluegreen")
plt.savefig(f"{FIG}/mobility-bluegreen.png", dpi=150); plt.close()
print("✅ mobility-bluegreen.png")

# ============ 5. metrics-evidence.png ============
fig, axes = plt.subplots(2, 3, figsize=(15, 9.5), dpi=150)
fig.subplots_adjust(top=0.88, bottom=0.06, left=0.03, right=0.99, hspace=0.75, wspace=0.18)
metrics = json.load(open(f"{SUB}/metrics.json"))
mm = metrics.get("metrics", metrics)  # v2: 顶层 metrics 键
data = [
    ("场地面积 site_area", mm["site_area_sqm"]["value"]/1e6, "km²", ACCENT),
    ("绿地率 green_ratio", mm["green_ratio"]["value"]*100, "%", GREEN),
    ("公共空间比例 public_space", mm["public_space_ratio"]["value"]*100, "%", COPPER),
    ("建筑密度 building_density", mm["building_density"]["value"]*100, "%", "#E05B6D"),
    ("道路总长 road_length", mm["road_length_m"]["value"]/1000, "km", "#FFFFFF"),
    ("重点区合计 key areas", sum(k["area_sqm"] for k in mm["key_area_details"]["values"])/1e4, "ha", "#7B5BFF"),
]
for ax, (name, val, unit, color) in zip(axes.flat, data):
    ax.set_facecolor("#141D2E")
    ax.barh([0], [val], color=color, height=0.5, alpha=0.9, edgecolor="#FFFFFF", linewidth=0.5)
    ax.set_xlim(0, max(v*1.15 for _, v, _, _ in data))
    ax.set_yticks([])
    ax.set_title(f"{name}\n{val:.2f} {unit}", fontsize=11, fontweight="bold", color=FG, pad=6)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=GRID)
fig.suptitle("京张智脉 · 核心指标复算证据链\nMetrics Evidence — recalculated from GeoJSON in EPSG:4548",
             fontsize=15, fontweight="bold", y=0.97)
check_text_overlaps(fig, "metrics-evidence")
plt.savefig(f"{FIG}/metrics-evidence.png", dpi=150); plt.close()
print("✅ metrics-evidence.png")
print("\n全部 5 图完成")
