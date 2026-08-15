# -*- coding: utf-8 -*-
"""投稿图件生成器：5 张中文核心图 + 5 张英文版（同一数据源）
数据源：design_geometry/*.geojson + 计算/*.json（全部本地实算）
图面要求：主叙事/图例/来源与临时性说明/设计标注；provisional 边界低对比度虚线
"""
import os, json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle
import pyproj
from shapely.geometry import shape, LineString
from shapely.ops import transform as sh_transform

HERE = os.path.dirname(os.path.abspath(__file__))
DG = os.path.join(HERE, "design_geometry")
CALC = os.path.join(HERE, "计算")
FIG = "/Users/mac/Downloads/同步空间/2026/百年京张AI创新带城市设计开源征集/haidian/submissions/Anshengdesign/jingzhang-living-line/assets/figures"
os.makedirs(FIG, exist_ok=True)

# 中文字体（KUN 手册 §3.1）
from kun_common import setup_chinese_fonts
setup_chinese_fonts()

TRANS = pyproj.Transformer.from_crs(pyproj.CRS.from_epsg(4326), pyproj.CRS.from_epsg(4548), always_xy=True)
def to_m(g):
    def pr(x, y, z=None):
        a, b = TRANS.transform(x, y)
        return (a, b)
    return sh_transform(pr, g)

def load_fc(name):
    d = json.load(open(os.path.join(DG, f"{name}.geojson")))
    return d["features"]

site = to_m(shape(load_fc("site_boundary")[0]["geometry"]))
keys = {f["properties"]["area_id"]: to_m(shape(f["geometry"])) for f in load_fc("key_areas")}
lu = [(f["properties"]["land_use_code"], to_m(shape(f["geometry"]))) for f in load_fc("land_use")]
roads = [to_m(shape(f["geometry"])) for f in load_fc("roads")]
green = [to_m(shape(f["geometry"])) for f in load_fc("green_space")]
pub = [to_m(shape(f["geometry"])) for f in load_fc("public_space")]
bldg = [to_m(shape(f["geometry"])) for f in load_fc("buildings")]

corridor = None
model = __import__("pickle").load(open(os.path.join(HERE, "site_model.pkl"), "rb"))
corridor = to_m(model["corridor"]) if model["corridor"] is not None else None
water = None
wlay = model["layers"]["water"]
wgs = [g for e, g in wlay if e.get("tags", {}).get("name")]
if wgs:
    from shapely.ops import unary_union
    water = to_m(unary_union(wgs))

c1 = json.load(open(os.path.join(CALC, "c1_wilson.json")))
c2 = json.load(open(os.path.join(CALC, "c2_percolation.json")))
c4 = json.load(open(os.path.join(CALC, "c4_syntax.json")))
c5 = json.load(open(os.path.join(CALC, "c5_counterfactual.json")))
c6 = json.load(open(os.path.join(CALC, "c6_fractal.json")))
c7 = json.load(open(os.path.join(CALC, "c7_poi_dynamics.json")))
dmet = json.load(open(os.path.join(DG, "design_metrics.json")))

LU_COLORS = {"0802": "#5b8dd9", "0804": "#7f6fd4", "05": "#e8915a", "0701": "#e8c07a",
             "1401": "#5fbf77", "0806": "#d96a6a", "16": "#cccccc"}
KEY_COLORS = {"zhongzhiyuan_ai_acceleration_area": "#c0392b",
              "beijing_ai_origin_community": "#8e44ad",
              "dazhongsi_ai_industry_cluster": "#2980b9"}

def plot_base(ax, title, LANG="zh"):
    # 底图：provisional 边界低对比度虚线
    ax.plot(*site.exterior.xy, color="#888888", lw=1.0, ls=(0, (6, 4)), alpha=0.7,
            label="临时粗略边界(provisional)" if LANG=="zh" else "Provisional boundary")
    # 用地淡色
    for code, g in lu:
        ax.fill(*g.exterior.xy, color=LU_COLORS.get(code, "#ccc"), alpha=0.28, lw=0)
    # 现状水系
    if water is not None:
        for g in ([water] if water.geom_type == "LineString" else list(water.geoms)):
            if g.geom_type == "LineString":
                ax.plot(*g.xy, color="#4aa3c2", lw=2.2, alpha=0.8)
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.set_aspect("equal"); ax.axis("off")
    return ax

# ---------- 图1 site-overview ----------
def fig_site_overview(LANG="zh"):
    T = lambda zh, en: zh if LANG == "zh" else en
    fig, ax = plt.subplots(figsize=(11, 13.5))
    plot_base(ax, T("图1 · 一带总览：一线三折两翼七节点", "Fig.1 · Belt overview: one line, three folds, two wings, seven nodes"), LANG)
    if corridor is not None:
        ax.plot(*corridor.xy, color="#1f4e2d", lw=5.0, alpha=0.9,
                label=T("京张 Hyper Line 主脊", "Jing-Zhang Hyper Line spine"))
    for aid, g in keys.items():
        ax.fill(*g.exterior.xy, color=KEY_COLORS[aid], alpha=0.30, lw=0)
        c = g.centroid
        names = {"zhongzhiyuan_ai_acceleration_area": T("众智园·HYPER STACK 全栈段","Zhongzhiyuan · HYPER STACK"),
                 "beijing_ai_origin_community": T("北京AI原点社区·HYPER ORIGIN 策源段","AI Origin Community · HYPER ORIGIN"),
                 "dazhongsi_ai_industry_cluster": T("大钟寺·HYPER FRONT 界面段","Dazhongsi · HYPER FRONT")}
        ax.annotate(names[aid], (c.x, c.y), ha="center", fontsize=10, fontweight="bold",
                    color=KEY_COLORS[aid], bbox=dict(fc="white", ec=KEY_COLORS[aid], alpha=0.85, boxstyle="round,pad=0.3"))
    # 七节点
    nodes = [(116.3315,39.9992),(116.3318,39.9915),(116.3324,39.9849),(116.3341,39.9750),
             (116.3391,39.9662),(116.3419,39.9568),(116.3429,39.9432)]
    nlabels = ["清华东路","五道口","北四环","知春路","北三环","学院南路","高梁桥斜街"] if LANG=="zh" else \
              ["Qinghuadonglu","Wudaokou","N.4th Ring","Zhichunlu","N.3rd Ring","Xueyuannanlu","Gaoliangqiao"]
    for (lon, lat), nl in zip(nodes, nlabels):
        x, y = TRANS.transform(lon, lat)
        ax.scatter(x, y, s=90, color="#e74c3c", zorder=5, edgecolor="white", linewidth=1.2)
        ax.annotate(nl, (x, y), xytext=(6, 6), textcoords="offset points", fontsize=8, color="#a93226")
    # 两翼
    wing_l = TRANS.transform(116.3237, 39.9797); wing_r = TRANS.transform(116.3569, 39.9777)
    ax.scatter(*wing_l, s=110, marker="s", color="#7f8c8d", zorder=5)
    ax.scatter(*wing_r, s=110, marker="s", color="#7f8c8d", zorder=5)
    ax.annotate(T("中关村·要素翼 CAPITAL WING","Zhongguancun · CAPITAL WING"), wing_l, xytext=(10,-14), textcoords="offset points", fontsize=9, color="#2c3e50")
    ax.annotate(T("小月河·场景翼 SCENARIO WING","Xiaoyuehe · SCENARIO WING"), wing_r, xytext=(10,-14), textcoords="offset points", fontsize=9, color="#2c3e50")
    # 朝圣地标
    marks = [(116.3430,39.9850,T("清华园车站·原点","Tsinghuayuan Stn · ORIGIN")),
             (116.3330,39.9915,T("五道口·相变广场","Wudaokou · Phase Plaza")),
             (116.3402,39.9646,T("大钟寺·界面广场","Dazhongsi · Interface Plaza"))]
    for lon, lat, nm in marks:
        x, y = TRANS.transform(lon, lat)
        ax.scatter(x, y, s=160, marker="*", color="#f39c12", zorder=6, edgecolor="white")
        ax.annotate(nm, (x, y), xytext=(8, 8), textcoords="offset points", fontsize=8.5, color="#b9770e", fontweight="bold")
    ax.legend(loc="upper left", fontsize=8)
    # 来源与状态说明
    ax.text(0.5, -0.045, T(
        "来源：官方公告+OSM现状+高德POI（2026-08-15）；临时边界仅虚线表达，非官方红线；全部为概念建议",
        "Sources: official announcement + OSM + Amap POI (2026-08-15); provisional boundary dashed only, not an official redline; all conceptual"),
        transform=ax.transAxes, ha="center", fontsize=7.5, color="#666666")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "site-overview.png" if LANG == "zh" else "site-overview.en.png"),
                dpi=150, bbox_inches="tight"); plt.close()

# ---------- 图2 land-use-structure ----------
def fig_landuse(LANG="zh"):
    T = lambda zh, en: zh if LANG == "zh" else en
    fig, axes = plt.subplots(1, 2, figsize=(16, 9), gridspec_kw={"width_ratios": [1.9, 1]})
    ax = axes[0]
    plot_base(ax, T("图2a · 用地结构与 POI 动力分区（概念）", "Fig.2a · Land-use structure & POI-driven zoning (concept)"), LANG)
    legend_done = set()
    for code, g in lu:
        ax.fill(*g.exterior.xy, color=LU_COLORS.get(code, "#ccc"), alpha=0.55, lw=0.4, edgecolor="white")
    if corridor is not None:
        ax.plot(*corridor.xy, color="#1f4e2d", lw=4.5, alpha=0.95)
    # 图例
    names = {"0802": T("科研(AI研发)","Research (AI R&D)"), "0804": T("教育科研","Education/Research"),
             "05": T("商业服务","Commercial"), "0701": T("居住(职住)","Residential"),
             "1401": T("绿地","Green"), "0806": T("医疗","Medical")}
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=LU_COLORS[k], label=names[k]) for k in names],
              loc="lower left", fontsize=8, ncol=2)
    ax2 = axes[1]
    share = {"0802": dmet["land_use_area_by_code_sqm"].get("0802",0),
             "0804": dmet["land_use_area_by_code_sqm"].get("0804",0),
             "05": dmet["land_use_area_by_code_sqm"].get("05",0),
             "0701": dmet["land_use_area_by_code_sqm"].get("0701",0),
             "1401": dmet["land_use_area_by_code_sqm"].get("1401",0)}
    ax2.bar(list(names.keys()), [share.get(k,0)/1e6 for k in names],
            color=[LU_COLORS[k] for k in names])
    ax2.set_title(T("图2b · 用地构成（万㎡，概念分区）","Fig.2b · Land-use mix (10k m², conceptual)"), fontsize=11)
    ax2.set_xticks(range(len(names))); ax2.set_xticklabels([names[k] for k in names], rotation=12, fontsize=8)
    ax2.set_ylabel(T("面积(万㎡)","Area (10k m²)"))
    ax2.text(0.98, 0.95, T("职住失衡：居住仅16.5%\n→ 站域补人才公寓(概念)",
                           "Jobs-housing gap: residential 16.5%\n→ talent apartments at stations (concept)"),
             transform=ax2.transAxes, ha="right", va="top", fontsize=9,
             bbox=dict(fc="#fef9e7", ec="#f0b429", alpha=0.9))
    fig.suptitle(T("图2 · 三层范围传导与用地结构（provisional 边界为虚线约束，重点在分区逻辑与职住判断）",
                   "Fig.2 · Three-level scope and land-use structure"), fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "land-use-structure.png" if LANG == "zh" else "land-use-structure.en.png"),
                dpi=150, bbox_inches="tight"); plt.close()

# ---------- 图3 key-areas ----------
def fig_keyareas(LANG="zh"):
    T = lambda zh, en: zh if LANG == "zh" else en
    fig, axes = plt.subplots(1, 3, figsize=(16, 6.5))
    info = [
        ("zhongzhiyuan_ai_acceleration_area", T("众智园·HYPER STACK","Zhongzhiyuan · HYPER STACK"),
         T("全栈测试带+花园街区\n补:文旅/教育/金融(概念)","Full-stack test band + garden district\nFill: tourism/edu/finance (concept)"),
         T("POI短板: scenic 0.4% school 0.7%","POI gaps: scenic 0.4% school 0.7%")),
        ("beijing_ai_origin_community", T("原点社区·HYPER ORIGIN","Origin Community · HYPER ORIGIN"),
         T("策源转化+原点广场+名墙\n补:医疗/人才公寓(概念)","Origination + Origin Plaza + name wall\nFill: medical/talent (concept)"),
         T("POI短板: medical 2.9/km²","POI gap: medical 2.9/km²")),
        ("dazhongsi_ai_industry_cluster", T("大钟寺·HYPER FRONT","Dazhongsi · HYPER FRONT"),
         T("四象限缝合+智能原生界面\n轻干预重界面(概念)","4-quadrant stitch + AI-native interface\nLight intervention (concept)"),
         T("三区最均衡: W/L 0.92","Most balanced: W/L 0.92")),
    ]
    for ax, (aid, title, strat, gap) in zip(axes, info):
        g = keys[aid]
        ax.fill(*g.exterior.xy, color=KEY_COLORS[aid], alpha=0.35)
        ax.plot(*g.exterior.xy, color=KEY_COLORS[aid], lw=2.2, ls=(0, (5, 3)))
        if corridor is not None:
            ax.plot(*corridor.xy, color="#1f4e2d", lw=3.5, alpha=0.75)
        ax.set_title(title, fontsize=11, fontweight="bold")
        ax.text(0.5, 0.12, strat, transform=ax.transAxes, ha="center", fontsize=9,
                bbox=dict(fc="white", ec="#cccccc", alpha=0.9))
        ax.text(0.5, 0.02, gap, transform=ax.transAxes, ha="center", fontsize=8, color="#a93226")
        ax.set_aspect("equal"); ax.axis("off")
    fig.suptitle(T("图3 · 三处重点区详细设计定位（临时粗略范围为虚线，定位差异与POI缺口为设计抓手）",
                   "Fig.3 · Key-area detailed design positions"), fontsize=12.5, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "key-areas.png" if LANG == "zh" else "key-areas.en.png"),
                dpi=150, bbox_inches="tight"); plt.close()

# ---------- 图4 mobility-bluegreen ----------
def fig_mobility(LANG="zh"):
    T = lambda zh, en: zh if LANG == "zh" else en
    fig, ax = plt.subplots(figsize=(11, 13.5))
    plot_base(ax, T("图4 · 交通慢行与蓝绿系统：七节点缝合","Fig.4 · Mobility & blue-green: seven-node stitching"), LANG)
    # 绿地
    for g in green:
        ax.fill(*g.exterior.xy, color="#5fbf77", alpha=0.30, lw=0)
    # 道路（概念线）
    for g in roads:
        ax.plot(*g.xy, color="#8d6e63", lw=1.1, alpha=0.6)
    if corridor is not None:
        ax.plot(*corridor.xy, color="#1f4e2d", lw=5.0, alpha=0.95,
                label=T("主脊绿道(概念)","Spine greenway (concept)"))
    # 断点缝合（E-W 短线）
    for (lon, lat) in [(116.3315,39.9992),(116.3318,39.9915),(116.3324,39.9849),(116.3341,39.9750),(116.3391,39.9662),(116.3419,39.9568),(116.3429,39.9432)]:
        x, y = TRANS.transform(lon, lat)
        ax.plot([x-160, x+160], [y, y], color="#e74c3c", lw=3.5, alpha=0.95, zorder=5)
        ax.scatter(x, y, s=70, color="#e74c3c", zorder=6, edgecolor="white")
    # 公共空间
    for g in pub:
        ax.fill(*g.exterior.xy, color="#f39c12", alpha=0.45, lw=0)
    ax.legend(loc="upper left", fontsize=9)
    # 图例文字
    ax.text(0.5, -0.045, T(
        "7处主干路断点→缝合步道(红线)；整合度提升：北京北+132% 大钟寺+102% 五道口+65%（空间句法实算）",
        "7 arterial gaps → stitch paths (red); integration gains: Beijing North +132% Dazhongsi +102% Wudaokou +65% (computed)"),
        transform=ax.transAxes, ha="center", fontsize=8, color="#666666")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "mobility-bluegreen.png" if LANG == "zh" else "mobility-bluegreen.en.png"),
                dpi=150, bbox_inches="tight"); plt.close()

# ---------- 图5 metrics-evidence ----------
def fig_metrics(LANG="zh"):
    T = lambda zh, en: zh if LANG == "zh" else en
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    # a) λ vs λc
    ax = axes[0, 0]
    pairs = [("众智园×原点","Zhongzhiyuan×Origin",0.205),("众智园×大钟寺","Zhongzhiyuan×Dazhongsi",0.015),
             ("原点×中关村翼","Origin×ZGC Wing",0.374),("原点×小月河翼","Origin×XYH Wing",0.455),
             ("大钟寺×中关村翼","Dazhongsi×ZGC Wing",0.068)]
    y = [p[2] for p in pairs]
    ax.barh(range(len(pairs)), y, color=["#b03a2e" if v > 0.42 else "#7f8c8d" for v in y])
    ax.axvline(0.42, color="#c0392b", ls="--", lw=2, label=T("相变临界 λc=0.42","Critical λc=0.42"))
    ax.set_yticks(range(len(pairs))); ax.set_yticklabels([p[1 if LANG=="en" else 0] for p in pairs], fontsize=9)
    ax.set_title(T("图5a · Wilson λ：5核断裂(2/5连通)","Fig.5a · Wilson λ: core fragmented (2/5)"), fontsize=11)
    ax.legend(fontsize=8)
    # b) 整合度提升
    ax = axes[0, 1]
    names = ["北京北","大钟寺","五道口","知春路","清华东路西口","学院桥","学知园"]
    deltas = [0.000216,0.000192,0.000164,0.000150,0.000134,0.000062,0.000063]
    pct = [132,102,65,61,54,21,28]
    ax.bar(range(len(names)), pct, color="#2e9e6b")
    ax.set_xticks(range(len(names))); ax.set_xticklabels(names, rotation=12, fontsize=9)
    ax.set_title(T("图5b · 主脊贯通后锚点整合度提升(%)","Fig.5b · Integration gains after spine (%)"), fontsize=11)
    # c) 渗流
    ax = axes[1, 0]
    ax.bar([0, 1], [83.9, 86.5], color=["#b08a4f", "#2e9e6b"])
    ax.axhline(59.27, color="#c0392b", ls="--", lw=2, label=T("渗流临界 59.27%","Percolation 59.27%"))
    ax.set_xticks([0, 1]); ax.set_xticklabels([T("现状蓝绿","Existing blue-green"), T("七节点缝合后","After 7-node stitch")], fontsize=10)
    ax.set_ylabel(T("巨分量面积占比(%)","Giant component (%)"))
    ax.set_title(T("图5c · 蓝绿网络渗流：问题在主脊断点","Fig.5c · Percolation: spine gaps are the disease"), fontsize=11)
    ax.legend(fontsize=8)
    # d) 指标卡
    ax = axes[1, 1]
    ax.axis("off")
    cards = [
        (T("分形维 D(大尺度)","Fractal D (large)"), "1.746", T("健康区间1.6-1.8","healthy 1.6-1.8")),
        (T("POI 底座","POI base"), "25,476", T("12类·2026-08-15","12 cat · 2026-08-15")),
        (T("交叉口密度","Intersection density"), "132.9/km²", T("老城>200 车本<80","old>200 car<80")),
        (T("绿地朝向熵","Green orientation entropy"), "0.911", T("≈随机 >> 网格=0","≈random >> grid=0")),
        (T("基底密度(概念)","Footprint density (concept)"), "17.4%", T("低置信度","low confidence")),
        (T("待确认","Pending"), "FAR/高度/红线", T("官方数据补齐后重算","recalc on official data")),
    ]
    for i, (k, v, note) in enumerate(cards):
        x = 0.5 if i % 2 == 0 else 1.5
        y = 2.2 - (i // 2) * 0.75
        ax.add_patch(Rectangle((x - 0.42, y - 0.3), 0.84, 0.6, fc="#f4f6f7", ec="#bdc3c7"))
        ax.text(x, y + 0.15, k, ha="center", fontsize=9, color="#2c3e50")
        ax.text(x, y - 0.05, v, ha="center", fontsize=15, fontweight="bold", color="#1f4e2d")
        ax.text(x, y - 0.22, note, ha="center", fontsize=7.5, color="#7f8c8d")
    ax.set_title(T("图5d · 证据卡（全部可复算）","Fig.5d · Evidence cards (all reproducible)"), fontsize=11)
    fig.suptitle(T("图5 · 核心指标复算与证据链（数据源：7项本地实算 + 高德POI + OSM）",
                   "Fig.5 · Core metrics & evidence chain"), fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "metrics-evidence.png" if LANG == "zh" else "metrics-evidence.en.png"),
                dpi=150, bbox_inches="tight"); plt.close()

for L in ["zh", "en"]:
    fig_site_overview(L); fig_landuse(L); fig_keyareas(L); fig_mobility(L); fig_metrics(L)
    print(L, "figures done")
