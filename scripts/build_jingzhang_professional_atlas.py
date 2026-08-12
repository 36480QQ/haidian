from __future__ import annotations

import argparse
import importlib.util
import json
import math
import shutil
import textwrap
from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle
from PIL import Image, ImageOps
from reportlab.lib.pagesizes import A0, A3, landscape
from reportlab.pdfgen import canvas
from shapely import affinity


ROOT = Path(__file__).resolve().parents[1]
SUB = ROOT / "submissions" / "CatNebulaaaa" / "grow-with-jingzhang"
GEOM = SUB / "geometry"
FIG = SUB / "assets" / "figures"
SCENES = SUB / "assets" / "generated-scenes"
DRAWINGS = SUB / "drawings"
ASSETS = SUB / "visual" / "assets"

W, H, DPI = 2480, 1754, 200
PAGE_SIZE = (W / DPI, H / DPI)

INK = "#102A43"
GREEN = "#2F855A"
CYAN = "#2B9BB3"
ORANGE = "#F45B3F"
GOLD = "#E6B93F"
VIOLET = "#76578F"
PAPER = "#F6F2E9"
PANEL = "#FFFDFC"
MUTED = "#667788"
LINE = "#CBD4D8"
LIGHT = "#EAE5DA"
RED = "#B94135"
WHITE = "#FFFFFF"

FONT_REG_PATH = Path("C:/Windows/Fonts/msyh.ttc")
FONT_BOLD_PATH = Path("C:/Windows/Fonts/msyhbd.ttc")
FONT_REG = font_manager.FontProperties(fname=str(FONT_REG_PATH)) if FONT_REG_PATH.exists() else None
FONT_BOLD = font_manager.FontProperties(fname=str(FONT_BOLD_PATH)) if FONT_BOLD_PATH.exists() else FONT_REG
matplotlib.rcParams["font.family"] = ["Microsoft YaHei", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False


def fp(size: float, bold: bool = False):
    base = FONT_BOLD if bold else FONT_REG
    if base is None:
        return font_manager.FontProperties(size=size, weight="bold" if bold else "normal")
    prop = base.copy()
    prop.set_size(size)
    return prop


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


SPATIAL = load_json(SUB / "spatial.json")
METRICS = load_json(SUB / "metrics.json")["metrics"]
CONTRACT = load_json(ASSETS / "implementation-operation-contract.json")
RUNBOOK = load_json(ASSETS / "growth-runbook.json")
TABLETOP = load_json(ASSETS / "growth-tabletop-evidence.json")
INCLUSION = load_json(ASSETS / "inclusion-ledger.json")
REGIONAL = load_json(ASSETS / "regional-collaboration-ledger.json")
BRAND = load_json(ASSETS / "brand-system.json")
RIGHTS = load_json(ASSETS / "rights-clearance-ledger.json")


def text(ax, x, y, value, size=10, color=INK, bold=False, ha="left", va="top",
         transform=None, linespacing=1.2, zorder=10, **kwargs):
    return ax.text(
        x, y, value, fontproperties=fp(size, bold), color=color, ha=ha, va=va,
        transform=transform or ax.transAxes, linespacing=linespacing, zorder=zorder, **kwargs
    )


def page(code: str, title_zh: str, title_en: str, sub_zh: str, sub_en: str, lang: str):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=DPI, facecolor=PAPER)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    ax.add_patch(Rectangle((0, .982), 1, .018, transform=ax.transAxes, color=INK, lw=0))
    ax.add_patch(Rectangle((0, .974), 1, .006, transform=ax.transAxes, color=ORANGE, lw=0))
    text(ax, .035, .938, code, 8.2, ORANGE, True)
    text(ax, .035, .900, title_zh if lang == "zh" else title_en, 22.5, INK, True)
    text(ax, .035, .866, sub_zh if lang == "zh" else sub_en, 8.5, MUTED)
    return fig, ax


def footer(ax, source: str, note_zh: str, note_en: str, page_no: str, lang: str):
    ax.plot([.035, .965], [.043, .043], color=INK, lw=.7, transform=ax.transAxes)
    text(ax, .035, .027, source, 5.5, MUTED, va="center")
    text(ax, .86, .027, note_zh if lang == "zh" else note_en, 5.7, ORANGE, True, ha="right", va="center")
    text(ax, .965, .027, page_no, 6, INK, True, ha="right", va="center")


def panel(fig, rect, face=PANEL, edge=LINE, radius=.008, lw=.8):
    ax = fig.add_axes(rect)
    ax.set_facecolor(face)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    p = FancyBboxPatch(
        (0, 0), 1, 1, boxstyle=f"round,pad=0.004,rounding_size={radius}",
        facecolor=face, edgecolor=edge, lw=lw, transform=ax.transAxes, clip_on=False, zorder=-10
    )
    ax.add_patch(p)
    return ax


def cover_image(ax, path: Path, size=(1400, 900), focus=(.5, .5)):
    im = Image.open(path).convert("RGB")
    fitted = ImageOps.fit(im, size, method=Image.Resampling.LANCZOS, centering=focus)
    ax.imshow(fitted, aspect="auto", extent=[0, 1, 0, 1])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")


def pill(ax, x, y, label, color=INK, width=None, size=6.5):
    width = width or max(.065, .012 + len(label) * .012)
    ax.add_patch(FancyBboxPatch((x, y), width, .035, boxstyle="round,pad=.004,rounding_size=.012",
                                transform=ax.transAxes, fc=color, ec="none"))
    text(ax, x + width / 2, y + .0175, label, size, WHITE, True, ha="center", va="center")


def stat(ax, x, y, value, label, color=INK, value_size=20, label_size=7.2):
    text(ax, x, y, value, value_size, color, True)
    text(ax, x, y - .085, label, label_size, MUTED)


def rotated_layers():
    names = ["site_boundary", "land_use", "green_space", "buildings", "roads", "key_areas", "public_space", "phasing"]
    layers = {n: gpd.read_file(GEOM / f"{n}.geojson").to_crs(4548) for n in names}
    site_geom = layers["site_boundary"].geometry.iloc[0]
    coords = np.asarray(site_geom.exterior.coords)
    centred = coords - coords.mean(axis=0)
    vals, vecs = np.linalg.eigh(np.cov(centred.T))
    axis = vecs[:, np.argmax(vals)]
    angle = math.degrees(math.atan2(axis[1], axis[0]))
    origin = (site_geom.centroid.x, site_geom.centroid.y)
    rotation = -angle
    for gdf in layers.values():
        gdf["geometry"] = gdf.geometry.apply(lambda g: affinity.rotate(g, rotation, origin=origin))
    return layers, angle


LAYERS, MAP_AXIS_ANGLE = rotated_layers()
LAND_COLORS = [GREEN, GOLD, CYAN, ORANGE, VIOLET, "#6D9F76"]
LAND_NAMES_ZH = ["研发测试与安全评估", "人才居住与生活配套", "教育培训与成果转化", "铁路文化与公共服务", "数字服务与商业配套", "蓝绿空间与市政设施"]
LAND_NAMES_EN = ["R&D + safety review", "talent housing + amenities", "training + technology transfer", "rail culture + public service", "digital service + commerce", "blue-green + utilities"]


def map_extent(ax, pad=.025):
    x0, y0, x1, y1 = LAYERS["site_boundary"].total_bounds
    dx, dy = x1 - x0, y1 - y0
    ax.set_xlim(x0 - dx * pad, x1 + dx * pad)
    ax.set_ylim(y0 - dy * .30, y1 + dy * .30)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")


def plot_map(ax, mode="overview", labels=True):
    if mode in {"overview", "mobility"}:
        LAYERS["land_use"].plot(ax=ax, color=[c + "22" for c in LAND_COLORS], edgecolor="#AEB9B9", linewidth=.45, zorder=1)
    if mode == "landuse":
        LAYERS["land_use"].plot(ax=ax, color=LAND_COLORS, alpha=.78, edgecolor=PAPER, linewidth=1.7, zorder=1)
    if mode in {"overview", "mobility"}:
        LAYERS["green_space"].plot(ax=ax, color="#B9D8C3", edgecolor=GREEN, linewidth=1.0, zorder=2)
    if mode == "overview":
        LAYERS["buildings"].plot(ax=ax, color="#C6C2B8", edgecolor="#7E8A8D", linewidth=.35, zorder=3)
    LAYERS["roads"].plot(ax=ax, color=CYAN if mode != "landuse" else INK, linewidth=2.2 if mode == "mobility" else 1.35, zorder=4)
    LAYERS["site_boundary"].boundary.plot(ax=ax, color=INK, linewidth=1.4, zorder=7)
    if mode != "landuse":
        LAYERS["key_areas"].boundary.plot(ax=ax, color=ORANGE, linewidth=2.0, zorder=8)
        LAYERS["public_space"].plot(ax=ax, color=ORANGE, edgecolor=WHITE, linewidth=.65, markersize=25, zorder=9)
    else:
        LAYERS["key_areas"].boundary.plot(ax=ax, color=WHITE, linewidth=2.4, zorder=8)
    if labels:
        for i, geom in enumerate(LAYERS["key_areas"].geometry):
            p = geom.representative_point()
            ax.text(p.x, p.y, ["P-03", "P-04", "P-02"][i], fontproperties=fp(6.3, True), color=WHITE,
                    ha="center", va="center", zorder=12,
                    path_effects=[pe.withStroke(linewidth=3.2, foreground=ORANGE)])
    map_extent(ax)


def map_scale(ax, length_m=1000):
    x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
    sx = x0 + (x1 - x0) * .055; sy = y0 + (y1 - y0) * .09
    ax.plot([sx, sx + length_m], [sy, sy], color=INK, lw=2)
    ax.plot([sx, sx], [sy - (y1-y0)*.012, sy + (y1-y0)*.012], color=INK, lw=1)
    ax.plot([sx + length_m, sx + length_m], [sy - (y1-y0)*.012, sy + (y1-y0)*.012], color=INK, lw=1)
    ax.text(sx + length_m/2, sy + (y1-y0)*.025, "1 km", fontproperties=fp(5.5, True), color=INK, ha="center")


def site_overview(lang):
    fig, root = page("01 / SPATIAL FRAMEWORK", "总体空间结构与公共服务骨架", "Spatial Framework and Public-service Armature",
                     "一轴三片、多点支撑｜真实图层沿廊道长轴展开", "One spine, three districts and twelve service nodes | corridor-axis review orientation", lang)
    ax = panel(fig, [.035, .56, .675, .24], face="#ECEBE5", edge=INK, lw=.9)
    plot_map(ax, "overview")
    map_scale(ax)
    text(ax, .02, .965, "总体设计工作范围 / 11.4128 km²" if lang == "zh" else "WORKING DESIGN EXTENT / 11.4128 km²", 7.5, INK, True)
    text(ax, .985, .03, f"MAP AXIS {MAP_AXIS_ANGLE:.1f}° / EPSG:4548", 5.2, MUTED, ha="right", va="bottom")

    lower = panel(fig, [.035, .13, .675, .39], face=PANEL, edge=LINE)
    text(lower, .035, .92, "空间—服务—实施一体化摘要" if lang == "zh" else "INTEGRATED SPACE—SERVICE—DELIVERY SUMMARY", 8.2, INK, True)
    lower.plot([.335, .335], [.10, .82], color=LINE, lw=.8, transform=lower.transAxes)
    lower.plot([.665, .665], [.10, .82], color=LINE, lw=.8, transform=lower.transAxes)
    text(lower, .035, .79, "首期动作" if lang == "zh" else "FIRST MOVES", 6.8, ORANGE, True)
    first_moves = ["1 km 连续慢行示范段", "3 处公共服务节点", "3,000 m² 共享首层", "1.5 ha 受控验证场"] if lang == "zh" else ["1 km continuous mobility pilot", "3 public-service nodes", "3,000 m² shared ground floor", "1.5 ha controlled validation field"]
    for i, item in enumerate(first_moves):
        text(lower, .035, .69 - i*.12, f"{i+1:02d}  {item}", 6.0, INK, True)
    text(lower, .365, .79, "8–80 同等服务" if lang == "zh" else "8–80 EQUAL SERVICE", 6.8, GREEN, True)
    equal_rules = ["无需账户、手机或人脸", "人工或非数字路径同等可达", "故障时基本公共服务持续", "责任、接管和退出公开"] if lang == "zh" else ["no account, phone or face required", "equal human/non-digital path", "basic service continues on failure", "owner, takeover and exit disclosed"]
    for i, item in enumerate(equal_rules):
        text(lower, .365, .69 - i*.12, f"{i+1:02d}  {item}", 5.8, INK)
    text(lower, .695, .79, "实施前置" if lang == "zh" else "PRECONDITIONS", 6.8, CYAN, True)
    prerequisites = ["正式范围与权属", "交通 / 轨道 / 消防", "地下管线与水文", "运营、采购与维护责任"] if lang == "zh" else ["official scope + tenure", "traffic / rail / fire", "utilities + hydrology", "operations + procurement + maintenance"]
    for i, item in enumerate(prerequisites):
        text(lower, .695, .69 - i*.12, f"{i+1:02d}  {item}", 5.8, INK)

    right = panel(fig, [.73, .13, .235, .67], face=PANEL, edge=LINE)
    text(right, .07, .95, "核心空间账本" if lang == "zh" else "CORE SPATIAL LEDGER", 9, INK, True)
    stat(right, .07, .87, "11.41 km²", "工作底图复算" if lang == "zh" else "recalculated working extent", INK, 18)
    stat(right, .55, .87, "3", "重点片区" if lang == "zh" else "key districts", ORANGE, 18)
    stat(right, .07, .72, "12", "公共服务节点" if lang == "zh" else "service nodes", CYAN, 18)
    stat(right, .55, .72, "1 km", "首期示范段" if lang == "zh" else "first pilot", GREEN, 18)
    right.plot([.07, .93], [.61, .61], color=LINE, lw=.8, transform=right.transAxes)
    text(right, .07, .57, "图层图例" if lang == "zh" else "MAP LEGEND", 8, INK, True)
    legend = [(GREEN, "蓝绿公共空间" if lang == "zh" else "blue-green commons"),
              (CYAN, "连续慢行主线" if lang == "zh" else "walk-cycle spine"),
              (ORANGE, "片区 / 服务节点" if lang == "zh" else "districts / service nodes"),
              ("#C6C2B8", "概念建筑体量" if lang == "zh" else "concept massing")]
    for i, (c, lab) in enumerate(legend):
        y = .505 - i * .064
        right.add_patch(Rectangle((.07, y), .05, .019, transform=right.transAxes, fc=c, ec="none"))
        text(right, .15, y + .010, lab, 6.7, INK, va="center")
    text(right, .07, .235, "实施门控" if lang == "zh" else "DELIVERY GATES", 8, INK, True)
    gates = CONTRACT["gates"]
    for i, g in enumerate(gates):
        y = .16 - i * .032
        c = [GREEN, CYAN, GOLD, ORANGE, VIOLET][i]
        right.add_patch(Circle((.09 + i*.18, .145), .026, transform=right.transAxes, fc=c, ec=WHITE, lw=.6))
        text(right, .09 + i*.18, .145, g["id"], 5.2, WHITE, True, ha="center", va="center")
    gate_names = "资料—协商—审查—开放—复审" if lang == "zh" else "evidence—consult—review—open—renew"
    text(right, .07, .075, gate_names, 6.1, MUTED)
    footer(root, "geometry/*.geojson · spatial.json · EPSG:4548", "方案研究范围，正式边界以主管部门成果为准", "working design extent; official boundary follows statutory confirmation", "01", lang)
    return fig


def land_use_structure(lang):
    fig, root = page("02 / LAND-USE LEDGER", "用地结构与复合功能组织", "Land-use Structure and Mixed-use Logic",
                     "六类方案分区、面积平衡与实施边界", "Six concept zones, area balance and implementation boundary", lang)
    ax = panel(fig, [.035, .54, .62, .26], face="#ECEBE5", edge=INK, lw=.9)
    plot_map(ax, "landuse")
    map_scale(ax)
    for i, geom in enumerate(LAYERS["land_use"].geometry):
        p = geom.representative_point()
        ax.text(p.x, p.y, f"LU-{i+1:02d}", fontproperties=fp(6.2, True), color=WHITE, ha="center", va="center",
                path_effects=[pe.withStroke(linewidth=2.6, foreground=INK)], zorder=12)
    detail = panel(fig, [.035, .14, .62, .36], face=PANEL, edge=LINE)
    text(detail, .035, .92, "功能结构与实施提示" if lang == "zh" else "PROGRAM STRUCTURE + DELIVERY NOTES", 8.2, INK, True)
    areas = np.array([float(v) for v in LAYERS["land_use"]["area_sqm_declared"]]) / 10000
    names = LAND_NAMES_ZH if lang == "zh" else LAND_NAMES_EN
    total = areas.sum()
    notes_zh = ["受控测试优先", "照护设施协同", "存量首层微改造", "铁路文化与服务", "日常服务混合", "海绵设施连续"]
    notes_en = ["controlled testing first", "integrate care facilities", "adapt existing ground floors", "rail culture + civic service", "mix daily services", "continuous sponge systems"]
    for i, (name, value, c) in enumerate(zip(names, areas, LAND_COLORS)):
        col, row = i % 2, i // 2
        x = .035 + col*.49; y = .77 - row*.215
        detail.add_patch(Rectangle((x, y-.105), .012, .13, transform=detail.transAxes, fc=c, ec="none"))
        text(detail, x+.028, y, f"LU-{i+1:02d}  {name}", 6.2, INK, True)
        text(detail, x+.028, y-.055, f"{value:.1f} ha  /  {value/total:.1%}", 6.0, c, True)
        text(detail, x+.245, y-.055, (notes_zh if lang=="zh" else notes_en)[i], 5.3, MUTED)
    text(detail, .035, .08, f"{total:.1f} ha", 15, INK, True)
    text(detail, .18, .07, "六类方案分区完整覆盖；空白 0、重叠 0。" if lang=="zh" else "Six concept zones cover the extent; 0 gaps and 0 overlaps.", 5.7, MUTED)

    bar = panel(fig, [.68, .14, .285, .66], face=PANEL, edge=LINE)
    text(bar, .07, .95, "方案土地平衡" if lang == "zh" else "CONCEPT LAND BALANCE", 9, INK, True)
    y = np.arange(6)[::-1]
    bar.set_xlim(0, max(areas)*1.35); bar.set_ylim(-.8, 6.3)
    bar.barh(y, areas, color=LAND_COLORS, height=.52)
    for i, (yy, value, name) in enumerate(zip(y, areas, names)):
        bar.text(.6, yy, f"LU-{i+1:02d}", fontproperties=fp(5.2, True), color=WHITE, va="center")
        bar.text(value + 2.2, yy + .13, f"{value:.1f} ha", fontproperties=fp(6.3, True), color=LAND_COLORS[i], va="center")
        bar.text(value + 2.2, yy - .15, name, fontproperties=fp(5.3), color=INK, va="center")
    bar.axis("off")
    footer(root, "geometry/land_use.geojson · geometry/key_areas.geojson · metrics.json", "方案分区不替代法定用地分类", "concept zones do not replace statutory land-use classification", "02", lang)
    return fig


def key_areas(lang):
    fig, root = page("03 / KEY DISTRICTS", "重点实施片区与近期建设任务", "Key Delivery Districts and Near-term Projects",
                     "三处重点片区分别建立项目清单和前置条件清单，分类安排更新方式与实施时序", "Each district receives its own project list, prerequisites, renewal method and delivery sequence", lang)
    photo = panel(fig, [.035, .18, .51, .64], face="#DDD", edge=INK, lw=.9)
    cover_image(photo, SCENES / "generated-co-learning-commons.png", (1500, 1000), (.62, .52))
    photo.add_patch(Rectangle((0, 0), 1, .17, transform=photo.transAxes, fc=INK, alpha=.87, ec="none"))
    text(photo, .035, .135, "存量空间改造示意" if lang == "zh" else "EXISTING-SPACE RETROFIT", 9, WHITE, True)
    text(photo, .035, .075, "首层开放、无障碍通行、雨水调蓄和人工服务纳入同一改造项目。" if lang == "zh" else "Ground-floor access, barrier-free routes, stormwater and staffed service are delivered as one project.", 6.4, "#DDE7EC")
    tbl = panel(fig, [.565, .18, .40, .64], face=PANEL, edge=LINE)
    text(tbl, .04, .955, "重点片区项目台账" if lang == "zh" else "KEY-DISTRICT PROJECT REGISTER", 8.5, INK, True)
    names_en = ["Zhongzhiyuan Validation District", "AI Origin Collaborative District", "Dazhongsi Station-City District"]
    codes = ["P-03", "P-04", "P-02"]
    colors = [GREEN, CYAN, ORANGE]
    first_en = ["1.5 ha controlled validation field", "3,000 m² shared ground floor", "station-city public-hall interface"]
    for i, area in enumerate(SPATIAL["key_areas"]):
        y0 = .88 - i*.285
        tbl.add_patch(Rectangle((.035, y0-.215), .012, .225, transform=tbl.transAxes, fc=colors[i], ec="none"))
        text(tbl, .065, y0, codes[i], 7.2, colors[i], True)
        name = area["name_zh"] if lang == "zh" else names_en[i]
        text(tbl, .15, y0, name, 7.5 if lang == "zh" else 6.5, INK, True)
        ann = area["announced_area_sqm"]/10000
        calc = area["calculated_provisional_area_sqm"]/10000
        text(tbl, .065, y0-.062, f"{ann:.1f} ha", 13, INK, True)
        text(tbl, .265, y0-.055, f"/ {calc:.1f} ha", 7.1, colors[i], True)
        first = area["first_action"]["name_zh"] if lang == "zh" else first_en[i]
        text(tbl, .065, y0-.115, first, 6.6, INK, True)
        gates = [
            "权属准入 · 安全评估 · 交通消防",
            "权属租约 · 结构消防 · 分时运营",
            "客流疏散 · 轨道接口 · 产权协商",
        ][i] if lang == "zh" else [
            "tenure · safety review · traffic/fire", "lease · structure/fire · operations", "flow/evacuation · rail · tenure"][i]
        text(tbl, .065, y0-.163, gates, 5.2, MUTED)
        if i < 2:
            tbl.plot([.065, .95], [y0-.225, y0-.225], color=LINE, lw=.7, transform=tbl.transAxes)
    text(tbl, .04, .055, "公告面积与底图复算差异均小于 0.5%；正式四至仍由后续法定成果确定。" if lang == "zh" else "Published and recalculated areas differ by less than 0.5%; official extents remain subject to statutory confirmation.", 5.4, MUTED)
    footer(root, "spatial.json · geometry/key_areas.geojson · generated-co-learning-commons.png", "重点片区范围与建设条件在城市更新实施方案中衔接落实", "district extents and delivery conditions are coordinated through the renewal implementation plan", "03", lang)
    return fig


def mobility_bluegreen(lang):
    fig, root = page("04 / MOBILITY + CLIMATE", "慢行、蓝绿与气候适应一体化设计", "Integrated Mobility, Blue-green and Climate Adaptation",
                     "连续网络、典型断面、气候基线与验收方法", "Continuous network, typical section, climate baseline and acceptance method", lang)
    ax = panel(fig, [.035, .38, .64, .44], face="#E7ECE8", edge=INK, lw=.9)
    plot_map(ax, "mobility")
    map_scale(ax)
    climate = panel(fig, [.695, .38, .27, .44], face=INK, edge=INK)
    text(climate, .07, .93, "2015–2024 气候基线" if lang == "zh" else "2015–2024 CLIMATE BASELINE", 8.4, WHITE, True)
    vals = [("35.58°C", "日最高温 P95" if lang == "zh" else "daily Tmax P95", ORANGE),
            ("22.3 d/y", "≥35°C 日数" if lang == "zh" else "days ≥35°C", "#F58A72"),
            ("649.1 mm", "年均降水" if lang == "zh" else "annual precipitation", CYAN),
            ("4.05", "kWh/m²/日太阳辐射" if lang == "zh" else "kWh/m²/day solar", GOLD)]
    for i, (v, lab, c) in enumerate(vals):
        y = .78 - i*.18
        text(climate, .07, y, v, 15.5, c, True)
        text(climate, .52, y-.005, lab, 6.2, "#D7E1E8")
        climate.plot([.07, .93], [y-.085, y-.085], color="#FFFFFF24", lw=.7, transform=climate.transAxes)
    sec = panel(fig, [.035, .13, .93, .20], face=PANEL, edge=LINE)
    segs = [(3.0, "连续步行" if lang=="zh" else "continuous walk", "#D9D3C4"),
            (2.5, "雨水花园" if lang=="zh" else "rain garden", "#CFE1D2"),
            (4.0, "双向骑行" if lang=="zh" else "two-way cycling", "#D2E7EE"),
            (2.5, "服务停留" if lang=="zh" else "service lay-by", "#F5D8CF")]
    x=.04; total=12.0
    for w, lab, c in segs:
        ww=.72*w/total
        sec.add_patch(Rectangle((x,.30),ww,.45,transform=sec.transAxes,fc=c,ec=INK,lw=.8))
        text(sec,x+ww/2,.52,lab,6.4,INK,True,ha="center",va="center")
        text(sec,x+ww/2,.22,f"{w:.1f} m",6.0,INK,True,ha="center",va="center")
        x+=ww
    text(sec,.80,.76,"验收要点" if lang=="zh" else "ACCEPTANCE",7.2,INK,True)
    checks = ["连续净宽实测", "汇水—溢流—退水", "遮阴与休憩间距"] if lang=="zh" else ["clear width survey","inflow-overflow-drainage","shade + rest spacing"]
    for i, s in enumerate(checks):
        text(sec,.80,.60-i*.16,f"{i+1:02d}  {s}",5.9,[GREEN,CYAN,ORANGE][i],True)
    footer(root, "geometry/roads.geojson · geometry/green_space.geojson · NASA POWER", "工程参数在专项设计阶段复核", "engineering parameters require specialist-stage verification", "04", lang)
    return fig


def metrics_evidence(lang):
    fig, root = page("05 / PLANNING INDICATORS", "规划指标分级管理与验收要求", "Planning Indicator Management and Acceptance",
                     "将九项指标分为基础复算、设计控制和运营考核，逐项明确测量阶段、责任类型和复核周期", "Nine indicators are assigned to base-map checks, design control and operating assessment with methods, owners and review cycles", lang)
    ax = panel(fig, [.035, .14, .93, .68], face=PANEL, edge=LINE)
    labels_zh = ["工作范围", "绿地比例", "公共空间", "示范段", "步行净宽", "骑行净宽", "休憩间距", "遮阴目标", "人工服务"]
    labels_en = ["working extent", "green ratio", "public space", "pilot length", "walk width", "cycle width", "rest spacing", "shade target", "human service"]
    values = [11.41, 18.95, 2.19, 1.0, 3.0, 4.0, 150, 70, 100]
    displays = ["11.41 km²", "18.95%", "2.19%", "1 km", "3.0 m", "4.0 m", "≤150 m", "70%", "100%"]
    roles = ["复算值", "复算值", "复算值", "建议目标", "建议目标", "建议目标", "建议目标", "建议目标", "运营目标"] if lang=="zh" else ["recalculated"]*3+["proposed target"]*5+["service target"]
    colors = [INK, GREEN, CYAN, ORANGE, ORANGE, ORANGE, GOLD, GREEN, CYAN]
    y = np.arange(9)[::-1]
    normalized = np.array([.92,.78,.48,.72,.62,.82,.70,.70,1.0])
    ax.set_xlim(0, 1); ax.set_ylim(-.8, 9.1)
    for i, yy in enumerate(y):
        ax.barh(yy, .82, left=.12, height=.52, color="#E8ECEB", zorder=1)
        ax.barh(yy, normalized[i]*.82, left=.12, height=.52, color=colors[i], alpha=.90, zorder=2)
        ax.text(.02, yy, (labels_zh if lang=="zh" else labels_en)[i], fontproperties=fp(6.4, True), color=INK, va="center")
        ax.text(.135, yy, displays[i], fontproperties=fp(7.4, True), color=WHITE, va="center", zorder=3)
        ax.text(.96, yy, roles[i], fontproperties=fp(5.5, True), color=colors[i], ha="right", va="center")
    ax.axis("off")
    text(ax,.02,.975,"数值 / 类型" if lang=="zh" else "VALUE / EVIDENCE CLASS",7.5,INK,True)
    text(ax,.98,.975,"测量方法、责任类型和复核周期已逐项登记" if lang=="zh" else "METHOD, OWNER TYPE AND REVIEW CYCLE RECORDED",6.0,MUTED,True,ha="right")
    footer(root, "metrics.json · spatial.json · implementation-operation-contract.json", "指标按现状调查、方案设计、工程验收和运营评估分阶段管理", "indicators are managed through survey, design, acceptance and operating evaluation", "05", lang)
    return fig


def implementation_protocol(lang):
    fig, root = page("06 / PROTOCOL TABLETOP", "实施协议、负向测试与退出条件", "Implementation Protocol, Negative Tests and Exit Conditions",
                     "十二项服务通过八条准入规则；八类缺陷由对应规则拦截", "Twelve services pass eight admission rules; eight injected defects are rejected", lang)
    graph = panel(fig, [.035, .48, .93, .34], face=INK, edge=INK)
    G = nx.DiGraph()
    gates = [g["id"] for g in CONTRACT["gates"]]
    for g in gates: G.add_node(g, subset=0)
    for a,b in zip(gates[:-1],gates[1:]): G.add_edge(a,b)
    pos = {g:(i,0) for i,g in enumerate(gates)}
    colors=[GREEN,CYAN,GOLD,ORANGE,VIOLET]
    nx.draw_networkx_edges(G,pos,ax=graph,edge_color="#BFD0DB",width=2.2,arrows=True,arrowsize=14,min_source_margin=18,min_target_margin=18)
    nx.draw_networkx_nodes(G,pos,ax=graph,node_color=colors,node_size=1200,edgecolors=WHITE,linewidths=1.2)
    nx.draw_networkx_labels(G,pos,ax=graph,font_family="Microsoft YaHei",font_size=8,font_color=WHITE,font_weight="bold")
    graph.set_xlim(-.6,4.6);graph.set_ylim(-.9,.7);graph.axis("off")
    gate_names_zh=["资料归集","可行协商","专项审查","验收开放","年度复审"]
    gate_names_en=["evidence lock","feasibility","specialist review","accept + open","annual review"]
    for i,n in enumerate(gate_names_zh if lang=="zh" else gate_names_en):
        graph.text(i,-.48,n,fontproperties=fp(6.2,True),color=WHITE,ha="center")
    text(graph,.02,.95,"五级决策关口" if lang=="zh" else "FIVE DECISION GATES",8,WHITE,True)
    rule_names = ["R1 责任", "R2 同等", "R3 最小数据", "R4 禁生物识别", "R5 人工接管", "R6 叫停权", "R7 公示", "R8 回执"] if lang=="zh" else ["R1 owner", "R2 equal", "R3 minimum data", "R4 no biometric", "R5 takeover", "R6 stop", "R7 notice", "R8 receipt"]
    for i, label in enumerate(rule_names):
        pill(graph, .025+i*.121, .055, label, [GREEN,CYAN,GOLD,ORANGE,GREEN,CYAN,GOLD,ORANGE][i], .105, 4.6)
    matrix = panel(fig, [.035, .14, .62, .29], face=PANEL, edge=LINE)
    rules=["R1","R2","R3","R4","R5","R6","R7","R8"]
    data=np.ones((12,8))
    matrix.imshow(data,cmap=matplotlib.colors.ListedColormap(["#DCECE3",GREEN]),vmin=0,vmax=1,aspect="auto",extent=[0,8,0,12])
    matrix.set_xticks(np.arange(0, 9, 1), minor=True)
    matrix.set_yticks(np.arange(0, 13, 1), minor=True)
    matrix.grid(which="minor", color=WHITE, linewidth=1.0, alpha=.78)
    matrix.tick_params(which="minor", length=0)
    for row in range(12):
        for col in range(8):
            matrix.add_patch(Circle((col+.5, row+.5), .095, fc=WHITE, ec="none", alpha=.92))
    matrix.set_xticks(np.arange(.5,8,.999));matrix.set_xticklabels(rules,fontproperties=fp(5.5,True),color=INK)
    matrix.set_yticks(np.arange(.5,12,.999));matrix.set_yticklabels([f"S{i:02d}" for i in range(12,0,-1)],fontproperties=fp(4.8),color=MUTED)
    matrix.tick_params(length=0);matrix.set_xlim(0,8);matrix.set_ylim(0,12)
    matrix.set_title("12 项服务 × 8 条规则：全部通过" if lang=="zh" else "12 SERVICES × 8 RULES: ALL PASS",fontproperties=fp(7.2,True),color=INK,loc="left",pad=8)
    result = panel(fig, [.675, .14, .29, .29], face=PANEL, edge=LINE)
    stat(result,.08,.83,"12/12","有效服务通过" if lang=="zh" else "valid services pass",GREEN,18)
    stat(result,.55,.83,"8/8","缺陷被拦截" if lang=="zh" else "defects rejected",ORANGE,18)
    stat(result,.08,.51,"0","失效规则" if lang=="zh" else "dead rules",CYAN,18)
    text(result,.08,.24,"负向测试 X01–X08 分别触发 R1–R8；结果来自可复算桌面协议，不代表项目授权或建成表现。" if lang=="zh" else "Negative cases X01–X08 trigger R1–R8 respectively. Results prove protocol logic only, not authorization or built performance.",5.7,MUTED,linespacing=1.45)
    footer(root, "growth-runbook.json · growth-tabletop-evidence.json · growth-protocol.schema.json", "协议验证结果，不替代专项审批", "protocol evidence; not a substitute for specialist approval", "06", lang)
    return fig


def inclusion_incidence(lang):
    fig, root = page("07 / INCLUSIVE SERVICES", "重点人群服务需求与项目整改清单", "Priority-user Needs and Project Rectification List",
                     "项目立项前开展重点人群走查，形成问题清单、整改责任表和意见反馈记录", "Complete priority-user walk-throughs before initiation and record issues, rectification duties and responses", lang)
    ax = panel(fig,[.035,.16,.68,.66],face=PANEL,edge=LINE)
    groups=INCLUSION["groups"]
    topics = [
        (["路径","步行","骑行","换乘","通行","客流"], "通行" if lang=="zh" else "mobility"),
        (["休憩","照护","座椅","家庭"], "停留照护" if lang=="zh" else "rest + care"),
        (["人工","服务","窗口"], "人工服务" if lang=="zh" else "human service"),
        (["学习","就业","经营","课程","工作"], "学习就业" if lang=="zh" else "learning + work"),
        (["施工","噪声","租金","成本","绕行"], "施工负担" if lang=="zh" else "delivery burden"),
        (["数据","数字","设备","画像","轨迹"], "数据数字" if lang=="zh" else "data + digital"),
        (["维护","故障","接管","培训","人员不足"], "维护接管" if lang=="zh" else "maintenance + takeover"),
    ]
    mat=[]
    for g in groups:
        corpus=" ".join(sum([g["benefits"],g["burdens"],g["blind_spots"],g["required_inputs"],g["procedural_standing"]["rights"]],[]))
        mat.append([min(3,sum(corpus.count(k) for k in keys)) for keys,_ in topics])
    mat=np.array(mat)
    cmap=matplotlib.colors.ListedColormap(["#EEF0EC","#B9D8D8",CYAN,INK])
    ax.imshow(mat,cmap=cmap,vmin=0,vmax=3,aspect="auto")
    labels=[g["label_zh"] if lang=="zh" else g["label_en"] for g in groups]
    ax.set_yticks([])
    heads=[name for _,name in topics]
    ax.set_xticks(range(7));ax.set_xticklabels(heads,fontproperties=fp(6.4 if lang=="zh" else 5.2,True),color=INK)
    ax.tick_params(length=0,pad=7)
    ax.set_xlim(-1.65, 6.5)
    for i, label in enumerate(labels):
        ax.text(-1.55, i, label, fontproperties=fp(5.8 if lang=="zh" else 4.9), color=INK, ha="left", va="center")
    for i in range(9):
        for j in range(7):
            if mat[i,j] > 0:
                ax.text(j,i,str(mat[i,j]),fontproperties=fp(6.5,True),color=WHITE if mat[i,j]>=2 else INK,ha="center",va="center")
    ax.set_title("重点人群问题登记频次 0—3" if lang=="zh" else "REGISTERED USER ISSUES 0–3",fontproperties=fp(8,True),loc="left",pad=12,color=INK)
    side=panel(fig,[.735,.16,.23,.66],face=INK,edge=INK)
    text(side,.08,.93,"调查与处置安排" if lang=="zh" else "SURVEY + ACTION ARRANGEMENT",9,WHITE,True)
    items=[("9类","重点人群调查" if lang=="zh" else "priority-user groups",GREEN),
           ("6项","参与和反馈环节" if lang=="zh" else "participation steps",CYAN),
           ("1套","问题整改责任表" if lang=="zh" else "rectification register",ORANGE)]
    for i,(v,l,c) in enumerate(items):stat(side,.08,.80-i*.18,v,l,c,18,6.2)
    note = "覆盖率在分时客流、常住与就业\n人口底数补齐后核算；当前按分组\n需求和问题清单推进整改。" if lang=="zh" else "Coverage is calculated after population,\nemployment and time-of-day flow baselines;\ncurrent action follows group issue lists."
    text(side,.08,.25,note,5.6,"#D7E1E8",linespacing=1.45)
    footer(root,"inclusion-ledger.json · user-cotest-plan.json","全龄使用需求纳入项目协商、设计审查和运营评估全过程", "all-age needs are integrated into consultation, design review and operating evaluation", "07",lang)
    return fig


def area_action_plan(lang):
    fig, root = page("08 / ACTION PROGRAM", "近期建设项目库与实施条件", "Near-term Project Register and Delivery Conditions",
                     "六个近期项目包逐项落实建设内容、前置手续、资金安排、实施周期、验收要求和运营责任", "Six near-term projects record scope, prerequisites, funding, schedule, acceptance and operating responsibility", lang)
    packages=CONTRACT["packages"]
    class_color={"S":GREEN,"M":CYAN,"L":ORANGE}
    labels_en=["Jingzhang mobility pilot","Dazhongsi station connection","Zhongzhiyuan R&D test field","AI Origin shared ground floor","public-service node prototype","public-AI management system"]
    scope_zh=["1公里步行骑行、雨水及休憩设施","四向步行、导向、服务点和停车整治","1.5公顷研发测试、安全缓冲及运维培训","3000平方米学习、人才服务和共享工作","320平方米人工服务、便民和雨水设施","项目申报、联合审查、工单和年度评估"]
    scope_en=["1 km walking, cycling, stormwater and rest","four-way access, wayfinding, service and parking","1.5 ha R&D test, safety buffer and training","3,000 m² learning, talent and shared work","320 m² staffed service, amenities and stormwater","applications, joint review, work orders and evaluation"]
    owner_en=["district · subdistrict · rightsholder","subdistrict · station · transport · rightsholder","park · test bodies · safety evaluator","rightsholder · subdistrict · campus/community · operator","subdistrict · community · facility operator","district · service operators · evaluator"]

    register=panel(fig,[.035,.16,.66,.66],face=PANEL,edge=LINE)
    text(register,.025,.95,"六个近期项目管理卡" if lang=="zh" else "SIX NEAR-TERM PROJECT CARDS",8.4,INK,True)
    text(register,.025,.905,"建设内容｜建议责任类型｜实施窗口｜前置手续｜交付成果" if lang=="zh" else "SCOPE | OWNER TYPE | WINDOW | PREREQUISITES | OUTPUT",4.9,MUTED)
    for i,p in enumerate(packages):
        col,row=i%2,i//2
        x=.025+col*.49;y=.81-row*.265
        color=class_color[p["class"]]
        register.add_patch(FancyBboxPatch((x,y-.185),.465,.205,boxstyle="round,pad=.004,rounding_size=.009",transform=register.transAxes,fc=color+"0D",ec=LINE,lw=.65))
        register.add_patch(Rectangle((x,y-.185),.010,.205,transform=register.transAxes,fc=color,ec="none"))
        text(register,x+.025,y-.005,p["id"],5.5,color,True)
        text(register,x+.095,y-.005,p["name_zh"] if lang=="zh" else labels_en[i],5.6 if lang=="zh" else 4.8,INK,True)
        text(register,x+.025,y-.050,("建设：" if lang=="zh" else "SCOPE  ")+scope_zh[i] if lang=="zh" else "SCOPE  "+scope_en[i],4.45,INK)
        owners=" · ".join(p["owner_types"][:3]) if lang=="zh" else owner_en[i]
        text(register,x+.025,y-.090,("责任：" if lang=="zh" else "OWNERS  ")+owners,4.2,MUTED)
        text(register,x+.025,y-.130,("工期：" if lang=="zh" else "WINDOW  ")+p["duration_months"]+("个月" if lang=="zh" else " months")+f"  |  {p['class']}",4.35,color,True)
        start=p["start"][0]+"、"+p["start"][1] if lang=="zh" else f"{len(p['start'])} prerequisites"
        text(register,x+.025,y-.163,("先办：" if lang=="zh" else "START  ")+start,4.05,MUTED)

    funding=panel(fig,[.715,.16,.25,.66],face=INK,edge=INK)
    text(funding,.07,.95,"资金与运营安排" if lang=="zh" else "FUNDING + OPERATIONS",8.6,WHITE,True)
    items_zh=[
        ("01","公共空间和基本设施","纳入项目建设投资，明确资产接收和日常维护单位",GREEN),
        ("02","经营及共享空间","产权单位与运营单位核算改造、租赁和人员费用",CYAN),
        ("03","研发测试和数字服务","实施主体落实设备、保险、安全评估和系统维护费用",GOLD),
        ("04","开工前资金条件","建设资金、年度运维经费和人员安排同步形成书面方案",ORANGE),
    ]
    items_en=[
        ("01","PUBLIC SPACE + AMENITIES","capital plan names asset recipient and maintenance body",GREEN),
        ("02","REVENUE + SHARED SPACE","rightsholder and operator cost retrofit, lease and staff",CYAN),
        ("03","R&D TEST + DIGITAL SERVICE","implementer funds equipment, insurance, safety and upkeep",GOLD),
        ("04","PRE-START FUNDING GATE","capital, annual O&M and staffing documented together",ORANGE),
    ]
    for i,(num,heading,body,color) in enumerate(items_zh if lang=="zh" else items_en):
        y=.82-i*.185
        funding.add_patch(Circle((.105,y),.030,transform=funding.transAxes,fc=color,ec=WHITE,lw=.5))
        text(funding,.105,y,num,4.6,WHITE,True,ha="center",va="center")
        text(funding,.18,y+.022,heading,5.6 if lang=="zh" else 4.5,color,True)
        text(funding,.18,y-.040,"\n".join(textwrap.wrap(body,width=18 if lang=="zh" else 28)),4.4,"#D7E1E8",linespacing=1.35)
    funding.plot([.07,.93],[.11,.11],color="#FFFFFF30",lw=.7,transform=funding.transAxes)
    text(funding,.07,.07,"投资级别：S＜500万｜M 500—2000万｜L 2000—5000万" if lang=="zh" else "COST CLASS: S <5m | M 5–20m | L 20–50m CNY",4.5,"#AFC2CE")
    footer(root,"implementation-operation-contract.json · spatial.json","概念成本级用于项目排序，投资测算在可研和概算阶段编制", "concept cost classes support prioritization; investment is developed at feasibility and estimate stages", "08",lang)
    return fig


def implementation_section(lang):
    fig, root = page("09 / TYPICAL SECTION", "京张沿线慢行示范段断面控制", "Typical-section Controls for the Jingzhang Pilot",
                     "针对步行断点、骑行混行、休憩不足和雨水排放问题，提出12米典型断面及验收要求", "A 12-m typical section addresses walking gaps, mixed traffic, limited rest and stormwater drainage", lang)
    photo=panel(fig,[.035,.20,.64,.62],face="#DDD",edge=INK,lw=.9)
    cover_image(photo,SCENES/"generated-corridor-section.jpg",(1600,1000),(.48,.52))
    photo.add_patch(Rectangle((0,0),1,.11,transform=photo.transAxes,fc=INK,alpha=.85,ec="none"))
    text(photo,.025,.075,"示范段建成效果｜无障碍步行 + 雨水花园 + 双向骑行 + 人工服务" if lang=="zh" else "PILOT DELIVERY VIEW | accessible walk + rain garden + two-way cycling + human service",6.6,WHITE,True)
    side=panel(fig,[.695,.20,.27,.62],face=PANEL,edge=LINE)
    text(side,.065,.955,"断面控制与验收要点" if lang=="zh" else "SECTION CONTROLS + ACCEPTANCE",8.5,INK,True)
    text(side,.065,.910,"总宽12.0 m｜四类功能带连续衔接" if lang=="zh" else "12.0 m total | four continuous functional bands",4.8,MUTED)
    section_rows_zh = [
        ("01", "步行通行", "≥3.0 m", "净宽连续，盲道与缘石坡道顺接", "沿线净宽实测", GREEN),
        ("02", "雨洪调蓄", "≥2.5 m", "汇水、溢流和退水路径完整", "专项计算＋通水检查", CYAN),
        ("03", "骑行通行", "≥4.0 m", "双向组织，交叉口落实减速提示", "标线净宽＋冲突点复核", GOLD),
        ("04", "服务停留", "≥2.5 m", "配置座椅、遮阴和人工导向", "设施清单＋无障碍核验", ORANGE),
    ]
    section_rows_en = [
        ("01", "WALKING", "≥3.0 m", "continuous clear width, tactile and kerb-ramp links", "field width survey", GREEN),
        ("02", "STORMWATER", "≥2.5 m", "complete inflow, overflow and drainage route", "hydraulic check + flow test", CYAN),
        ("03", "CYCLING", "≥4.0 m", "two-way operation with speed control at crossings", "marking width + conflict review", GOLD),
        ("04", "SERVICE EDGE", "≥2.5 m", "seating, shade and staffed wayfinding", "facility list + access audit", ORANGE),
    ]
    for i, (num, heading, value, requirement, acceptance, color) in enumerate(section_rows_zh if lang=="zh" else section_rows_en):
        y = .835 - i*.155
        side.add_patch(FancyBboxPatch((.055,y-.112),.89,.125,
            boxstyle="round,pad=.004,rounding_size=.010",transform=side.transAxes,
            fc=color+"10",ec=LINE,lw=.55))
        side.add_patch(Rectangle((.055,y-.112),.010,.125,transform=side.transAxes,fc=color,ec="none"))
        text(side,.082,y-.010,num,4.6,color,True)
        text(side,.145,y-.010,heading,5.7,INK,True)
        text(side,.91,y-.010,value,8.3,color,True,ha="right")
        text(side,.082,y-.055,requirement,4.35,MUTED)
        text(side,.082,y-.088,("验收：" if lang=="zh" else "ACCEPT  ")+acceptance,4.25,INK,True)
    side.plot([.065,.935],[.205,.205],color=LINE,lw=.7,transform=side.transAxes)
    text(side,.065,.170,"建设衔接" if lang=="zh" else "DELIVERY INTERFACES",6.3,INK,True)
    delivery_zh=["轨道保护范围与检修通道同步校核","道路红线、地下管线和现状树木一图统筹","停电断网期间保留实体导向和人工服务"]
    delivery_en=["coordinate rail protection and maintenance access","integrate street limits, utilities and existing trees","retain physical wayfinding and human service during outages"]
    for i,s in enumerate(delivery_zh if lang=="zh" else delivery_en):
        side.add_patch(Circle((.078,.128-i*.040),.006,transform=side.transAxes,fc=[GREEN,CYAN,ORANGE][i],ec="none"))
        text(side,.098,.128-i*.040,s,4.25,INK,va="center")
    footer(root,"spatial.json · generated-corridor-section.jpg · Beijing walk/cycle standards","断面宽度结合轨道安全、道路红线、市政管线和现状树木条件深化", "section dimensions are developed with rail safety, street limits, utilities and existing trees", "09",lang)
    return fig


def service_node_kit(lang):
    fig, root = page("10 / SERVICE NODE GUIDE", "公共服务节点建设与运营指引", "Public-service Node Delivery and Operations Guide",
                     "以320平方米样板节点为例，明确用地、功能、人员、管线、验收和退出管理要求", "A 320 m² prototype defines site, program, staffing, utilities, acceptance and exit requirements", lang)
    photo=panel(fig,[.035,.20,.61,.62],face="#DDD",edge=INK,lw=.9)
    cover_image(photo,SCENES/"generated-service-node-axonometric.jpg",(1500,1000),(.50,.55))
    photo.add_patch(Rectangle((0,0),1,.105,transform=photo.transAxes,fc=INK,alpha=.86,ec="none"))
    text(photo,.025,.072,"节点轴测意向｜20 m × 16 m｜连续无障碍闭环" if lang=="zh" else "NODE AXONOMETRIC INTENT | 20 m × 16 m | continuous accessible loop",6.6,WHITE,True)
    side=panel(fig,[.665,.20,.30,.62],face=PANEL,edge=LINE)
    text(side,.06,.955,"节点建设与运营控制表" if lang=="zh" else "NODE DELIVERY + OPERATIONS",8.5,INK,True)
    text(side,.06,.910,"规划面积250—400 m²｜样板节点320 m²" if lang=="zh" else "250–400 m² program range | 320 m² prototype",4.8,MUTED)
    node_rows_zh = [
        ("01", "空间规模", "320 m²", "20 m×16 m样板；采用可拆装构件", "用地与建成面积复核", INK),
        ("02", "人工服务", "24—36 m²", "配置窗口、等候、储物及值守席位", "开放时段与人员排班", ORANGE),
        ("03", "环境品质", "≥70%", "主要停留空间形成连续遮阴", "夏季日照分析与现场抽测", GREEN),
        ("04", "运行响应", "60 s / 24 h", "人工接管及时响应；常规故障建单", "月度响应和工单台账", CYAN),
    ]
    node_rows_en = [
        ("01", "FOOTPRINT", "320 m²", "20 m × 16 m prototype with demountable components", "site and built-area check", INK),
        ("02", "HUMAN SERVICE", "24–36 m²", "counter, waiting, storage and staffed position", "hours and staffing roster", ORANGE),
        ("03", "MICROCLIMATE", "≥70%", "continuous shade across principal stay areas", "summer solar study + field audit", GREEN),
        ("04", "RESPONSE", "60 s / 24 h", "human acknowledgement and routine fault logging", "monthly response + work-order log", CYAN),
    ]
    for i, (num, heading, value, requirement, acceptance, color) in enumerate(node_rows_zh if lang=="zh" else node_rows_en):
        y = .835 - i*.155
        side.add_patch(FancyBboxPatch((.05,y-.112),.90,.125,
            boxstyle="round,pad=.004,rounding_size=.010",transform=side.transAxes,
            fc=color+"10",ec=LINE,lw=.55))
        side.add_patch(Rectangle((.05,y-.112),.010,.125,transform=side.transAxes,fc=color,ec="none"))
        text(side,.076,y-.010,num,4.6,color,True)
        text(side,.137,y-.010,heading,5.6 if lang=="zh" else 5.0,INK,True)
        text(side,.92,y-.010,value,8.2 if i!=3 else 7.2,color,True,ha="right")
        text(side,.076,y-.055,requirement,4.35,MUTED)
        text(side,.076,y-.088,("验收：" if lang=="zh" else "ACCEPT  ")+acceptance,4.2,INK,True)
    side.plot([.06,.94],[.205,.205],color=LINE,lw=.7,transform=side.transAxes)
    text(side,.06,.170,"交付与退出管理" if lang=="zh" else "HANDOVER + EXIT MANAGEMENT",6.3,INK,True)
    handover_zh=["管线综合、消防、无障碍和场地许可同步审查","形成设施清单、运维责任表和月度巡检记录","运营条件未落实时撤除设备，保留基本便民设施"]
    handover_en=["joint utilities, fire, access and site-permit review","facility list, duty register and monthly inspection record","remove equipment if operations lapse; retain basic civic amenities"]
    for i,s in enumerate(handover_zh if lang=="zh" else handover_en):
        side.add_patch(Circle((.074,.128-i*.040),.006,transform=side.transAxes,fc=[GREEN,CYAN,ORANGE][i],ec="none"))
        text(side,.094,.128-i*.040,s,4.2,INK,va="center")
    footer(root,"spatial.json · implementation-operation-contract.json · generated-service-node-axonometric.jpg","节点建设纳入管线综合、消防审查、无障碍设计和运营维护方案", "node delivery integrates utilities, fire review, accessibility and operating maintenance", "10",lang)
    return fig


def regional_collaboration(lang):
    fig, root = page(
        "11 / REGIONAL COORDINATION",
        "区域协同事项与实施责任清单",
        "Regional Coordination Tasks and Delivery Responsibilities",
        "围绕创新测试、人才培养、成果转化、站城服务和蓝绿运维，明确牵头类型、配合单位、年度任务和归档成果",
        "Define lead types, supporting bodies, annual tasks and filed outputs for testing, talent, transfer, station services and blue-green operations",
        lang,
    )

    hero = panel(fig, [.035, .275, .575, .545], face="#E9E6DE", edge=INK, lw=.9)
    cover_image(hero, ASSETS / "image2-regional-corridor-planning.jpg", (1700, 1030), (.42, .52))
    hero.add_patch(Rectangle((0, 0), 1, .16, transform=hero.transAxes, fc=INK, alpha=.90, ec="none"))
    text(hero, .03, .122, "区域协同事项分布示意" if lang == "zh" else "REGIONAL COORDINATION TASK MAP", 8.6, WHITE, True)
    text(hero, .03, .061,
         "铁路遗产主轴串联科研园区、社区学习、成果转化、站城服务与蓝绿基础设施。" if lang == "zh" else
         "The historic rail spine connects research, community learning, transfer, station services and blue-green infrastructure.",
         5.5, "#D7E1E8")
    pill(hero, .025, .91, "1条区域主轴" if lang == "zh" else "1 REGIONAL SPINE", INK, .145, 5.2)
    pill(hero, .18, .91, "5项协同任务" if lang == "zh" else "5 TASKS", GREEN, .145, 5.2)

    ledger = panel(fig, [.63, .275, .335, .545], face=PANEL, edge=LINE)
    text(ledger, .055, .955, "年度协同任务" if lang == "zh" else "ANNUAL COORDINATION TASKS", 8.2, INK, True)
    text(ledger, .055, .905,
         "按事项明确牵头类型、前置条件和归档成果" if lang == "zh" else
         "Each task records lead type, prerequisites and filed outputs",
         5.3, MUTED)
    names_en = [
        "AI safety evaluation", "campus-community learning", "technology transfer",
        "station-city public service", "blue-green operations",
    ]
    owners_en = [
        "park operator · university lab · evaluator", "university · community · operator",
        "technology service · park operator · rightsholder", "station operator · subdistrict · transport",
        "landscape · municipal · local operator",
    ]
    outputs_en = [
        "versioned report and failure cases", "course edition and review record",
        "referral register and rights statement", "task test and site-inspection record",
        "as-built file, inspection and work orders",
    ]
    task_colors = [GREEN, CYAN, GOLD, ORANGE, VIOLET]
    for i, item in enumerate(REGIONAL["interfaces"]):
        y = .82 - i * .154
        color = task_colors[i]
        ledger.add_patch(FancyBboxPatch((.045, y - .105), .91, .125,
            boxstyle="round,pad=.005,rounding_size=.012", transform=ledger.transAxes,
            fc=color + "12", ec=LINE, lw=.6))
        ledger.add_patch(Rectangle((.045, y - .105), .012, .125, transform=ledger.transAxes, fc=color, ec="none"))
        text(ledger, .075, y, item["id"], 5.7, color, True)
        text(ledger, .195, y,
             item["name_zh"].replace("接口", "协同") if lang == "zh" else names_en[i],
             6.0 if lang == "zh" else 5.3, INK, True)
        owner = " · ".join(item["owner_types"]) if lang == "zh" else owners_en[i]
        proof = item["proof"] if lang == "zh" else outputs_en[i]
        text(ledger, .075, y - .046,
             ("责任建议：" + owner) if lang == "zh" else ("LEAD TYPES  " + owner),
             4.45, MUTED)
        text(ledger, .075, y - .078,
             ("成果要求：" + proof) if lang == "zh" else ("OUTPUT  " + proof),
             4.45, INK, True)

    mechanism = panel(fig, [.035, .125, .93, .105], face=INK, edge=INK)
    text(mechanism, .025, .72, "推进机制" if lang == "zh" else "DELIVERY MECHANISM", 7.2, WHITE, True, va="center")
    steps_zh = ["协同事项建库", "责任主体确认", "专业联合审查", "先行项目实施", "年度评估入库"]
    steps_en = ["TASK REGISTER", "OWNER CONFIRMATION", "JOINT REVIEW", "PILOT DELIVERY", "ANNUAL EVALUATION"]
    for i, label in enumerate(steps_zh if lang == "zh" else steps_en):
        x = .19 + i * .155
        color = task_colors[i]
        mechanism.add_patch(Circle((x, .58), .030, transform=mechanism.transAxes, fc=color, ec=WHITE, lw=.6))
        text(mechanism, x, .58, f"{i+1:02d}", 4.7, WHITE, True, ha="center", va="center")
        text(mechanism, x, .22, label, 5.25 if lang == "zh" else 4.5, WHITE, True, ha="center", va="center")
        if i < 4:
            mechanism.add_patch(FancyArrowPatch((x + .038, .58), (x + .117, .58), transform=mechanism.transAxes,
                                                arrowstyle="-|>", mutation_scale=7, color="#8FB2C3", lw=1.0))
    footer(root, "regional-collaboration-ledger.json · image2-regional-corridor-planning.jpg · sources.json",
           "协同事项纳入年度任务清单前完成职责确认和工作衔接",
           "responsibilities are confirmed before tasks enter the annual delivery list", "11", lang)
    return fig


def ai_governance(lang):
    fig, root = page(
        "12 / AI SERVICE GOVERNANCE",
        "公共人工智能服务建设运营管理",
        "Delivery and Operating Management for Public AI Services",
        "按立项、审查、测试、开放、评估五个环节明确责任单位、工作要求和成果文件",
        "Define accountable bodies, tasks and filed outputs across initiation, review, testing, opening and evaluation",
        lang,
    )

    stats_panel = panel(fig, [.035, .705, .93, .115], face=INK, edge=INK)
    stats_data = [
        ("12", "拟建公共服务" if lang == "zh" else "PROPOSED SERVICES", GREEN),
        ("8", "申报审查条件" if lang == "zh" else "REVIEW CONDITIONS", CYAN),
        ("60 s", "人工响应目标" if lang == "zh" else "HUMAN ACKNOWLEDGEMENT", ORANGE),
        ("5个工作日" if lang == "zh" else "5 days", "公众意见答复" if lang == "zh" else "PUBLIC RESPONSE", GOLD),
    ]
    for i, (value, label, color) in enumerate(stats_data):
        x = .035 + i * .245
        if i:
            stats_panel.plot([x - .025, x - .025], [.20, .80], color="#FFFFFF30", lw=.7, transform=stats_panel.transAxes)
        text(stats_panel, x, .67, value, 14.5 if i != 3 or lang != "zh" else 12.5, color, True, va="center")
        text(stats_panel, x, .27, label, 5.5, "#D7E1E8", True, va="center")

    process = panel(fig, [.035, .275, .93, .395], face=PANEL, edge=LINE)
    text(process, .025, .94, "全过程管理流程" if lang == "zh" else "FULL-CYCLE MANAGEMENT", 7.8, INK, True)
    text(process, .975, .94,
         "前一节点材料、责任和整改未落实，不转入下一节点" if lang == "zh" else
         "NO TRANSFER UNTIL DOCUMENTS, OWNERSHIP AND RECTIFICATION ARE COMPLETE",
         5.0, ORANGE, True, ha="right")
    stages_zh = [
        ("项目申报", "建设前", "实施单位", "场地、经费、数据和人工服务方案", "明确服务对象、建设位置和责任单位", "任务书及经费来源完整", "项目任务书"),
        ("联合审查", "开放前", "统筹及专业单位", "项目任务书、风险清单和应急预案", "审查安全、数据、无障碍和运营条件", "审查意见逐项落实", "联合审查意见"),
        ("试运行评估", "试运行期", "运营、使用者及评估方", "公示文本、测试方案和人工接管流程", "组织重点人群试用、走查和故障演练", "问题整改完成并复核", "问题清单与整改表"),
        ("运行监管", "每月", "运营及人工服务", "设施清单、人员排班和服务工单", "落实人工接管、故障处置和信息公开", "月度记录完整可查", "运行月报与工单"),
        ("年度评估", "每年", "统筹及独立评估", "绩效、公众意见和维护成本", "提出延续、整改、缩减或终止意见", "形成下一年度项目清单", "年度调整清单"),
    ]
    stages_en = [
        ("APPLICATION", "PRE-BUILD", "implementer", "site, funding, data and staffed-service plan", "define users, location and accountable body", "brief and funding source complete", "project brief"),
        ("JOINT REVIEW", "PRE-OPEN", "lead + specialists", "project brief, risk list and emergency plan", "review safety, data, access and operations", "all review actions closed", "joint review opinion"),
        ("TRIAL REVIEW", "TRIAL", "operator + users + evaluator", "notice, test plan and takeover procedure", "co-test with priority users and run fault drills", "actions closed and rechecked", "issue + action register"),
        ("OPERATIONS", "MONTHLY", "operator + human service", "asset list, staff roster and work orders", "deliver takeover, fault response and disclosure", "monthly evidence complete", "monthly report + orders"),
        ("ANNUAL REVIEW", "ANNUAL", "lead + evaluator", "performance, comments and maintenance cost", "continue, rectify, reduce or terminate", "next-year list agreed", "annual adjustment list"),
    ]
    stage_colors = [INK, CYAN, ORANGE, GREEN, VIOLET]
    for i, (title_s, timing, owner, inputs, action, transfer, output) in enumerate(stages_zh if lang == "zh" else stages_en):
        x = .025 + i * .194
        process.add_patch(FancyBboxPatch((x, .09), .175, .75,
            boxstyle="round,pad=.005,rounding_size=.012", transform=process.transAxes,
            fc=stage_colors[i] + "10", ec=stage_colors[i], lw=.8))
        process.add_patch(Rectangle((x, .75), .175, .09, transform=process.transAxes, fc=stage_colors[i], ec="none"))
        text(process, x + .015, .795, f"{i+1:02d}", 4.8, WHITE, True, va="center")
        text(process, x + .050, .795, title_s, 5.7 if lang == "zh" else 4.55, WHITE, True, va="center")
        pill(process, x + .105, .683, timing, stage_colors[i], .056, 4.0)
        text(process, x + .015, .675, "责任" if lang == "zh" else "OWNER", 4.25, stage_colors[i], True)
        text(process, x + .015, .615, owner, 4.7, INK, True)
        text(process, x + .015, .535, "前置材料" if lang == "zh" else "INPUT", 4.25, stage_colors[i], True)
        text(process, x + .015, .492, "\n".join(textwrap.wrap(inputs, width=15 if lang == "zh" else 27)), 4.2, MUTED, linespacing=1.25)
        text(process, x + .015, .385, "主要工作" if lang == "zh" else "ACTION", 4.25, stage_colors[i], True)
        text(process, x + .015, .342, "\n".join(textwrap.wrap(action, width=15 if lang == "zh" else 27)), 4.2, INK, linespacing=1.25)
        text(process, x + .015, .235, "转序条件" if lang == "zh" else "TRANSFER GATE", 4.25, stage_colors[i], True)
        text(process, x + .015, .192, "\n".join(textwrap.wrap(transfer, width=15 if lang == "zh" else 27)), 4.15, MUTED, linespacing=1.2)
        text(process, x + .015, .115, ("归档：" if lang == "zh" else "FILE  ") + output, 4.15, INK, True)
        if i < 4:
            process.add_patch(FancyArrowPatch((x + .176, .46), (x + .192, .46), transform=process.transAxes,
                                              arrowstyle="-|>", mutation_scale=7, color=INK, lw=.8, zorder=8))

    controls = panel(fig, [.035, .105, .93, .135], face="#EEF1ED", edge=LINE)
    control_data = [
        ("服务保障" if lang == "zh" else "SERVICE ACCESS", GREEN,
         "人工或非数字服务同步设置｜断网停电保留实体导向｜公众意见5个工作日答复" if lang == "zh" else "Staffed/non-digital route | physical wayfinding during outages | public reply within 5 days"),
        ("数据管理" if lang == "zh" else "DATA MANAGEMENT", CYAN,
         "仅采集办理所需信息｜公开用途和保存期限｜年度更新数据清单" if lang == "zh" else "Necessary data only | disclose use and retention | update annual data inventory"),
        ("安全运行" if lang == "zh" else "SAFE OPERATIONS", ORANGE,
         "重大故障立即隔离｜60秒人工响应｜常规故障24小时内建单" if lang == "zh" else "Isolate critical faults | 60 s human acknowledgement | routine work order within 24 h"),
        ("监督评估" if lang == "zh" else "PUBLIC OVERSIGHT", VIOLET,
         "每月汇总故障工单｜每季度复核服务规则｜每年形成调整清单" if lang == "zh" else "Monthly fault summary | quarterly rule review | annual adjustment list"),
    ]
    for i, (heading, color, body) in enumerate(control_data):
        x = .025 + i * .242
        controls.add_patch(Rectangle((x, .18), .009, .64, transform=controls.transAxes, fc=color, ec="none"))
        text(controls, x + .025, .76, heading, 5.8, color, True)
        lines = body.split("｜") if lang == "zh" else body.split(" | ")
        for j, line in enumerate(lines):
            text(controls, x + .025, .50 - j*.19, f"{j+1:02d}  {line}", 4.35, INK, linespacing=1.2)
    footer(root, "growth-runbook.json · implementation-operation-contract.json · inclusion-ledger.json",
           "公共人工智能服务实行场景清单管理、人工服务保障和年度评估",
           "public AI services follow scenario-list management, human-service safeguards and annual evaluation", "12", lang)
    return fig


def delivery_program(lang):
    fig, root = page("13 / PHASED DELIVERY", "分期实施计划与年度评估安排", "Phased Delivery Plan and Annual Evaluation",
                     "先完成90日准备工作，再按项目成熟度推进六个项目包，并建立月度调度和年度评估制度", "Complete 90-day preparation, then advance six projects by readiness with monthly scheduling and annual evaluation", lang)
    ax=panel(fig,[.035,.16,.93,.66],face=PANEL,edge=LINE)
    packages=CONTRACT["packages"]
    starts=[6,12,12,9,6,3]; ends=[18,24,24,18,12,9]
    y=np.arange(6)[::-1]
    colors=[CYAN,ORANGE,ORANGE,CYAN,GREEN,GOLD]
    for i,(p,yy,s,e,c) in enumerate(zip(packages,y,starts,ends,colors)):
        ax.barh(yy,e-s,left=s,height=.48,color=c,alpha=.88)
        name=p["name_zh"] if lang=="zh" else ["spine pilot","station-city pilot","validation field","shared ground floor","service-node prototype","governance system"][i]
        ax.text(-.35,yy,f"{p['id']}  {name}",fontproperties=fp(6.3,True),color=INK,ha="right",va="center")
        ax.text((s+e)/2,yy,f"{s}–{e}m",fontproperties=fp(5.5,True),color=WHITE,ha="center",va="center")
    gate_months=[0,3,9,18,24]
    for gm,g,c in zip(gate_months,CONTRACT["gates"],[GREEN,CYAN,GOLD,ORANGE,VIOLET]):
        ax.axvline(gm,color=c,lw=1.4,ls="--",alpha=.9)
        ax.text(gm,6.05,g["id"],fontproperties=fp(6.0,True),color=c,ha="center")
    ax.set_xlim(-5.8,24);ax.set_ylim(-.8,6.4);ax.set_yticks([]);ax.set_xticks(range(0,25,3));ax.set_xticklabels(range(0,25,3),fontproperties=fp(5.5),color=MUTED)
    ax.grid(axis="x",color=LINE,lw=.55);ax.spines[:].set_visible(False)
    ax.set_title("0–24 月建议实施窗口" if lang=="zh" else "PROPOSED 0–24 MONTH DELIVERY WINDOW",fontproperties=fp(8,True),loc="left",color=INK,pad=12)
    text(ax,.58,.03,"0—15日底图权属｜16—45日踏勘测算｜46—75日流程演练｜76—90日整改决策" if lang=="zh" else "D0–15 base map/tenure | D16–45 survey/costing | D46–75 drills | D76–90 action decision",5.6,MUTED)
    footer(root,"implementation-operation-contract.json · user-cotest-plan.json","实施时序结合边界、权属、专项审查和资金安排滚动更新", "delivery sequencing is updated with boundaries, tenure, specialist review and funding", "13",lang)
    return fig


def brand_system(lang):
    fig, root = page("14 / PUBLIC IDENTITY", "公共识别系统与信息使用规则", "Public Identity System and Information Rules",
                     "轨线、年轮与人工服务缺口构成统一识别", "Rail lines, growth rings and the human-service opening form one identity", lang)
    mark=panel(fig,[.035,.20,.44,.62],face=INK,edge=INK)
    for y in [.43,.57]:mark.plot([.14,.86],[y,y],color=WHITE,lw=4,solid_capstyle="round",transform=mark.transAxes)
    for r,c in [(0.22,GREEN),(0.15,CYAN),(0.08,ORANGE)]:
        mark.add_patch(matplotlib.patches.Arc((.50,.50),2*r,2*r,theta1=25,theta2=325,color=c,lw=5,transform=mark.transAxes))
    mark.add_patch(Rectangle((.76,.43),.10,.14,transform=mark.transAxes,fc=INK,ec="none",zorder=4))
    text(mark,.50,.18,"京张共长线" if lang=="zh" else "GROW WITH JINGZHANG",18,WHITE,True,ha="center")
    text(mark,.50,.105,"8–80 同等服务" if lang=="zh" else "8–80 EQUAL SERVICE",7,CYAN,True,ha="center")
    spec=panel(fig,[.50,.20,.465,.62],face=PANEL,edge=LINE)
    text(spec,.05,.94,"颜色与职责" if lang=="zh" else "COLOR + RESPONSIBILITY",8.5,INK,True)
    palette=[(INK,"轨道墨蓝" if lang=="zh" else "rail ink"),(GREEN,"叶绿 / 公共空间" if lang=="zh" else "leaf / commons"),(CYAN,"市民青 / 信息流" if lang=="zh" else "civic cyan / information"),(ORANGE,"公共橙 / 责任与停止" if lang=="zh" else "public orange / duty + stop"),(GOLD,"审查金 / 门控" if lang=="zh" else "review gold / gates")]
    for i,(c,n) in enumerate(palette):
        y=.84-i*.115
        spec.add_patch(Rectangle((.05,y-.035),.14,.07,transform=spec.transAxes,fc=c,ec="none"))
        text(spec,.23,y,n,6.4,INK,True,va="center")
        text(spec,.78,y,c,5.7,MUTED,ha="right",va="center")
    spec.plot([.05,.95],[.24,.24],color=LINE,lw=.8,transform=spec.transAxes)
    rules=BRAND["usage_rules"] if lang=="zh" else ["Do not combine with government emblems.","Use orange only for duty, stop and service prompts.","Every AI point also displays the human-service symbol."]
    text(spec,.05,.20,"使用规则" if lang=="zh" else "USAGE RULES",7.2,INK,True)
    for i,r in enumerate(rules):text(spec,.05,.145-i*.05,f"{i+1:02d}  {r}",5.5,MUTED)
    footer(root,"brand-system.json · rights-clearance-ledger.json","公共识别不得形成政府背书暗示", "public identity must not imply government endorsement", "14",lang)
    return fig


def rights_evidence(lang):
    fig, root = page(
        "15 / BASIS + MATERIALS",
        "成果编制依据与资料使用说明",
        "Planning Basis and Material-use Statement",
        "实行资料分类、来源登记、用途管理和成果复核，形成可持续更新的编制档案",
        "Materials are classified, sourced, managed by use and reviewed as an updatable planning record",
        lang,
    )
    rows = RIGHTS["assets"]

    summary_panel = panel(fig, [.035, .715, .93, .105], face=INK, edge=INK)
    summary_stats = [
        ("8类" if lang == "zh" else "8", "编制资料" if lang == "zh" else "MATERIAL CLASSES", GREEN),
        ("30张" if lang == "zh" else "30", "规划图件" if lang == "zh" else "PLANNING FIGURES", CYAN),
        ("4份" if lang == "zh" else "4", "PDF成果" if lang == "zh" else "PDF DELIVERABLES", ORANGE),
        ("2套" if lang == "zh" else "2", "中英文本" if lang == "zh" else "LANGUAGE SETS", GOLD),
    ]
    for i, (value, label, color) in enumerate(summary_stats):
        x = .05 + i * .235
        if i:
            summary_panel.plot([x - .028, x - .028], [.20, .80], color="#FFFFFF30", lw=.7, transform=summary_panel.transAxes)
        text(summary_panel, x, .65, value, 14, color, True, va="center")
        text(summary_panel, x, .25, label, 5.5, "#D7E1E8", True, va="center")

    ax = panel(fig, [.035, .245, .93, .435], face=PANEL, edge=LINE)
    names_zh = ["方案文本及译稿", "规划技术图件", "开放地图底图", "区域气候资料", "走廊空间模型", "概念场景图像", "离线三维展示", "成果排版字体"]
    names_en = [r["asset"] for r in rows]
    origins_zh = ["本方案编制", "结构化数据本地生成", "OpenStreetMap / ODbL", "NASA POWER 公开数据", "Blender 本地建模", "OpenAI 图像生成", "Three.js / MIT", "系统许可字体"]
    uses_zh = ["规划说明和双语成果", "空间分析、指标复算和项目表达", "区域联系与城市肌理参照", "2015—2024 气候基线分析", "城市设计意向和空间推演", "公共空间氛围与使用场景表达", "方案空间关系交互浏览", "PDF、网页和图件排版"]
    controls_zh = [
        "重要政策、标准和事实保留来源编号", "同步保存生成脚本、数据口径和坐标系统",
        "图面标注贡献者及许可信息", "保留数据集、时间范围和计算口径",
        "纳入概念方案档案，工程深化结合测绘校核", "登记生成工具和用途，实施图纸采用专业设计成果",
        "随成果保留许可声明和版本信息", "以嵌入方式用于成果排版",
    ]
    statuses_zh = ["来源已登记", "过程可复核", "许可已登记", "口径已登记", "概念成果", "意向表达", "许可已登记", "嵌入使用"]
    statuses_en = ["REGISTERED", "REPRODUCIBLE", "LICENSED", "REGISTERED", "CONCEPT", "ILLUSTRATIVE", "LICENSED", "EMBEDDED"]
    heads = ["资料类别", "来源与授权", "规划用途", "使用管理要求", "核验状态"] if lang == "zh" else ["MATERIAL", "SOURCE / RIGHT", "PLANNING USE", "MANAGEMENT REQUIREMENT", "STATUS"]
    xcols = [.025, .185, .395, .625, .895]
    status_width = .08
    for x, h in zip(xcols, heads):
        text(ax, x, .94, h, 5.9, INK, True)
    ax.plot([.025, .975], [.895, .895], color=INK, lw=1.0, transform=ax.transAxes)
    for i, row in enumerate(rows):
        y = .84 - i * .097
        if i % 2 == 0:
            ax.add_patch(Rectangle((.02, y - .053), .96, .086, transform=ax.transAxes, fc="#F0F1ED", ec="none"))
        values = [
            names_zh[i] if lang == "zh" else names_en[i],
            origins_zh[i] if lang == "zh" else row["origin"],
            uses_zh[i] if lang == "zh" else row["right"],
            controls_zh[i] if lang == "zh" else row["limits"],
        ]
        wrap_widths = [11, 18, 20, 24] if lang == "zh" else [18, 28, 30, 38]
        for j, value in enumerate(values):
            wrapped = "\n".join(textwrap.wrap(value, width=wrap_widths[j]))
            text(ax, xcols[j], y, wrapped, 4.55 if j else 4.9, INK if j in {0, 2} else MUTED,
                 bold=(j == 0), va="center", linespacing=1.2)
        status = statuses_zh[i] if lang == "zh" else statuses_en[i]
        color = [GREEN, CYAN, GREEN, CYAN, GOLD, ORANGE, GREEN, CYAN][i]
        ax.add_patch(FancyBboxPatch((xcols[4], y - .021), status_width, .041,
            boxstyle="round,pad=.003,rounding_size=.009", transform=ax.transAxes,
            fc=color + "18", ec=color, lw=.6))
        text(ax, xcols[4] + status_width / 2, y, status, 4.1, color, True, ha="center", va="center")

    notes = panel(fig, [.035, .125, .93, .085], face="#EEF1ED", edge=LINE)
    note_data = [
        ("法定依据" if lang == "zh" else "STATUTORY BASIS", GREEN,
         "政策、标准和任务依据逐项编号并纳入来源目录" if lang == "zh" else "Policies, standards and task sources are indexed in the source register"),
        ("技术底图" if lang == "zh" else "TECHNICAL BASE", CYAN,
         "工作底图随正式边界、测绘和现状调查动态更新" if lang == "zh" else "The working base is updated with official boundaries, survey and current-condition records"),
        ("成果使用" if lang == "zh" else "DELIVERABLE USE", ORANGE,
         "概念图像用于表达规划意图，建设实施衔接专项设计成果" if lang == "zh" else "Concept visuals convey planning intent; delivery proceeds through specialist design outputs"),
    ]
    for i, (heading, color, body) in enumerate(note_data):
        x = .025 + i * .325
        notes.add_patch(Rectangle((x, .18), .010, .64, transform=notes.transAxes, fc=color, ec="none"))
        text(notes, x + .027, .67, heading, 5.4, color, True)
        text(notes, x + .027, .35, body, 4.5, INK)
    footer(root, "sources.json · rights-clearance-ledger.json · report/copyright_statement.md",
           "各类资料实行来源登记、用途管理和成果复核",
           "all materials follow source registration, use management and deliverable review", "15", lang)
    return fig


def image2_site_overview(lang):
    fig, root = page(
        "01 / DELIVERY FRAMEWORK",
        "总体空间结构与近期实施安排",
        "Overall Spatial Structure and Near-term Delivery",
        "组织近期项目和公共设施布局，形成一轴三片、两翼协同、十二节点的空间结构",
        "Use the rail heritage corridor as the framework, define three key districts and prioritise mobility continuity, service gaps and retrofit",
        lang,
    )
    hero = panel(fig, [.035, .405, .675, .415], face="#DAD8D0", edge=INK, lw=.9)
    cover_image(hero, SCENES / "image2-corridor-masterplan.jpg", (1700, 980), (.55, .52))
    hero.add_patch(Rectangle((0, 0), 1, .19, transform=hero.transAxes, fc=INK, alpha=.88, ec="none"))
    text(hero, .035, .145, "近期建设重点：慢行示范、节点补缺、首层改造、站城衔接" if lang == "zh" else "NEAR-TERM PRIORITIES: MOBILITY PILOT, SERVICE NODES, GROUND-FLOOR RETROFIT, STATION LINKS", 8.8, WHITE, True)
    text(hero, .035, .073, "以1公里慢行示范段、3处首期节点和3个重点片区项目为抓手，分期形成连续公共空间和便民服务网络。" if lang == "zh" else "A 1 km mobility pilot, three first-stage nodes and three district projects establish a continuous public-space and service network.", 6.1, "#D9E5EA")

    story = panel(fig, [.035, .13, .675, .235], face="#DAD8D0", edge=INK, lw=.8)
    cover_image(story, SCENES / "image2-three-layer-story.jpg", (1700, 560), (.50, .53))
    story.add_patch(Rectangle((0, 0), 1, .22, transform=story.transAxes, fc=INK, alpha=.87, ec="none"))
    labels = ["0—1月：底图与权属", "1—3月：项目准备与立项", "4—24月：示范先行、滚动实施"] if lang == "zh" else ["0–1M: BASE MAP + TENURE", "1–3M: PROJECT PREPARATION", "4–24M: PILOT + ROLL-OUT"]
    colors = [ORANGE, GREEN, CYAN]
    for i, (label, color) in enumerate(zip(labels, colors)):
        x = .055 + i * .315
        story.add_patch(Circle((x, .11), .018, transform=story.transAxes, fc=color, ec=WHITE, lw=.6))
        text(story, x + .032, .11, label, 6.4, WHITE, True, va="center")

    right = panel(fig, [.73, .13, .235, .69], face=INK, edge=INK)
    text(right, .07, .95, "总体工作台账" if lang == "zh" else "PROGRAM REGISTER", 9.0, WHITE, True)
    stats = [
        ("11.41 km²", "总体设计工作底图" if lang == "zh" else "overall working base", WHITE),
        ("3", "重点实施片区" if lang == "zh" else "key delivery districts", ORANGE),
        ("6", "近期建设项目包" if lang == "zh" else "near-term projects", CYAN),
        ("0—24月", "建议实施周期" if lang == "zh" else "proposed delivery window", GREEN),
    ]
    for i, (value, label, color) in enumerate(stats):
        y = .83 - i * .145
        text(right, .07, y, value, 18, color, True)
        text(right, .07, y - .060, label, 6.2, "#BFD0DB")
    right.plot([.07, .93], [.29, .29], color="#FFFFFF35", lw=.8, transform=right.transAxes)
    text(right, .07, .25, "近期管控要求" if lang == "zh" else "NEAR-TERM CONTROLS", 7.4, WHITE, True)
    principles = ["正式边界和权属先核", "轨道安全和地下管线先审", "公益设施与经营项目统筹", "建设、运营和维护责任同步落实"] if lang == "zh" else ["verify formal boundaries and tenure", "review rail safety and utilities first", "coordinate public and revenue uses", "assign delivery, operations and maintenance"]
    for i, item in enumerate(principles):
        text(right, .07, .195 - i * .047, f"{i+1:02d}  {item}", 5.5, "#D7E1E8")
    footer(root, "image2-corridor-masterplan.jpg · image2-three-layer-story.jpg · spatial.json", "工作底图用于方案编制；正式实施以边界权属、规划条件、专项审查和项目立项为准", "the working base supports design; delivery follows confirmed boundaries, planning conditions, specialist review and project initiation", "01", lang)
    return fig


def image2_land_use_structure(lang):
    fig, root = page(
        "02 / PROGRAM ROOMS",
        "功能分区、规模平衡与更新方式",
        "Functional Zoning, Area Balance and Renewal Method",
        "按六类更新单元核算用地规模，分别明确保留改造、功能导入、设施补建和实施条件",
        "Six renewal-unit types record area balance, retrofit, new uses, facility additions and delivery conditions",
        lang,
    )
    hero = panel(fig, [.035, .18, .69, .64], face="#DDD9CF", edge=INK, lw=.9)
    cover_image(hero, SCENES / "image2-program-rooms.jpg", (1700, 1100), (.50, .52))
    hero.add_patch(Rectangle((0, 0), 1, .155, transform=hero.transAxes, fc=INK, alpha=.88, ec="none"))
    text(hero, .03, .112, "六类更新单元，分别确定建设任务和实施条件" if lang == "zh" else "SIX RENEWAL UNITS WITH DEFINED TASKS AND DELIVERY CONDITIONS", 8.6, WHITE, True)
    text(hero, .03, .055, "分区用于项目统筹；法定用地性质、开发强度和兼容关系在实施方案中核定。" if lang == "zh" else "The zones support project coordination; statutory use, intensity and compatibility are confirmed through implementation planning.", 6.0, "#DCE7EB")

    ledger = panel(fig, [.745, .18, .22, .64], face=PANEL, edge=LINE)
    text(ledger, .07, .94, "用地与任务台账" if lang == "zh" else "LAND + TASK REGISTER", 8.8, INK, True)
    areas = np.array([float(v) for v in LAYERS["land_use"]["area_sqm_declared"]]) / 10000
    names = LAND_NAMES_ZH if lang == "zh" else LAND_NAMES_EN
    total = areas.sum()
    for i, (name, value, color) in enumerate(zip(names, areas, LAND_COLORS)):
        y = .835 - i * .112
        ledger.add_patch(Rectangle((.07, y - .044), .018, .074, transform=ledger.transAxes, fc=color, ec="none"))
        text(ledger, .11, y, f"LU-{i+1:02d}", 5.8, color, True)
        text(ledger, .25, y, name, 5.55 if lang == "zh" else 4.55, INK, True)
        text(ledger, .11, y - .039, f"{value:.1f} ha  ·  {value/total:.1%}", 5.4, MUTED)
        if i < 5:
            ledger.plot([.07, .93], [y - .064, y - .064], color=LINE, lw=.6, transform=ledger.transAxes)
    ledger.plot([.07, .93], [.13, .13], color=INK, lw=.8, transform=ledger.transAxes)
    text(ledger, .07, .09, f"{total:.1f} ha", 13.5, INK, True)
    text(ledger, .07, .045, "工作底图分区合计" if lang == "zh" else "working-base zone total", 5.6, MUTED)
    footer(root, "image2-program-rooms.jpg · geometry/land_use.geojson · metrics.json", "功能分区与法定用地分类衔接，具体兼容关系在实施方案中落实", "functional zones are coordinated with statutory land-use classes through the implementation plan", "02", lang)
    return fig


def image2_mobility_bluegreen(lang):
    fig, root = page(
        "04 / MOBILITY + CLIMATE",
        "慢行交通与雨洪设施近期建设要求",
        "Near-term Mobility and Stormwater Delivery Requirements",
        "针对慢行断点、休憩不足和雨洪设施分散问题，统筹步行骑行、遮阴休憩、雨水调蓄和服务停留",
        "Address mobility gaps, limited rest and fragmented drainage through coordinated walking, cycling, shade, stormwater and service stops",
        lang,
    )
    hero = panel(fig, [.035, .18, .67, .64], face="#D8DDD7", edge=INK, lw=.9)
    cover_image(hero, SCENES / "image2-climate-promenade.jpg", (1700, 1100), (.50, .50))
    hero.add_patch(Rectangle((0, 0), 1, .15, transform=hero.transAxes, fc=INK, alpha=.86, ec="none"))
    text(hero, .03, .105, "慢行示范段建成效果示意" if lang == "zh" else "ILLUSTRATIVE COMPLETED VIEW OF THE MOBILITY PILOT", 8.4, WHITE, True)
    text(hero, .03, .050, "步行、骑行、雨水设施和服务停留按12米典型断面统筹布置。" if lang == "zh" else "Walking, cycling, stormwater and service stops are coordinated within a 12 m typical section.", 6.0, "#DCE7EB")

    side = panel(fig, [.725, .18, .24, .64], face=INK, edge=INK)
    text(side, .07, .94, "气候基线与空间响应" if lang == "zh" else "CLIMATE + SPATIAL RESPONSE", 8.4, WHITE, True)
    vals = [("35.58°C", "日最高温 P95" if lang == "zh" else "daily Tmax P95", ORANGE), ("22.3 d/y", "≥35°C 日数" if lang == "zh" else "days ≥35°C", "#F58A72"), ("649.1 mm", "年均降水" if lang == "zh" else "annual rain", CYAN), ("4.05", "日太阳辐射" if lang == "zh" else "daily solar", GOLD)]
    for i, (value, label, color) in enumerate(vals):
        y = .82 - i * .115
        text(side, .07, y, value, 13.5, color, True)
        text(side, .55, y - .005, label, 5.3, "#C8D7DF")
    side.plot([.07, .93], [.35, .35], color="#FFFFFF35", lw=.8, transform=side.transAxes)
    text(side, .07, .31, "12 m 弹性界面" if lang == "zh" else "12 m FLEXIBLE EDGE", 7.1, WHITE, True)
    segs = [(3.0, GREEN), (2.5, CYAN), (4.0, GOLD), (2.5, ORANGE)]
    labels = ["步行", "雨水", "骑行", "服务"] if lang == "zh" else ["walk", "rain", "cycle", "service"]
    x = .07
    for (width, color), label in zip(segs, labels):
        ww = .86 * width / 12
        side.add_patch(Rectangle((x, .225), ww, .055, transform=side.transAxes, fc=color, ec="none"))
        text(side, x + ww / 2, .19, label, 4.8, "#D7E1E8", True, ha="center")
        text(side, x + ww / 2, .145, f"{width:.1f} m", 5.2, WHITE, True, ha="center")
        x += ww
    text(side, .07, .075, "连续净宽 · 汇水退水 · 遮阴休憩" if lang == "zh" else "clear width · drainage · shade + rest", 5.5, "#BFD0DB")
    footer(root, "image2-climate-promenade.jpg · metrics.json · NASA POWER", "慢行与蓝绿设施参数在交通、市政和景观专项设计中协同深化", "mobility and blue-green parameters are developed through transport, utilities and landscape design", "04", lang)
    return fig


def image2_implementation_protocol(lang):
    fig, root = page(
        "06 / SERVICE MANAGEMENT",
        "公共人工智能服务项目审查要点",
        "Project Review Requirements for Public AI Services",
        "对十二项拟建服务逐项核对责任主体、人工办理、数据使用、停止权限、投诉处置和年度评估",
        "Review accountable owner, human service, data use, stop authority, complaints and annual evaluation for twelve proposed services",
        lang,
    )
    services = RUNBOOK["services"]
    stats_panel = panel(fig, [.035, .715, .93, .105], face=INK, edge=INK)
    stats = [
        ("12", "拟建服务项目" if lang == "zh" else "PROPOSED SERVICES", GREEN),
        ("8", "申报审查条件" if lang == "zh" else "REVIEW CONDITIONS", CYAN),
        ("4", "近期试运行项目" if lang == "zh" else "EARLY TRIAL SERVICES", ORANGE),
        ("5", "办理管理节点" if lang == "zh" else "MANAGEMENT STAGES", GOLD),
    ]
    for i, (value, label, color) in enumerate(stats):
        x = .05 + i * .235
        if i:
            stats_panel.plot([x - .028, x - .028], [.20, .80], color="#FFFFFF30", lw=.7, transform=stats_panel.transAxes)
        text(stats_panel, x, .64, value, 14, color, True, va="center")
        text(stats_panel, x, .23, label, 5.4, "#D7E1E8", True, va="center")

    service_panel = panel(fig, [.035, .25, .62, .425], face=PANEL, edge=LINE)
    text(service_panel, .025, .945, "十二项拟建服务清单" if lang == "zh" else "TWELVE PROPOSED SERVICES", 8.0, INK, True)
    text(service_panel, .025, .895, "项目名称｜建设位置｜责任类型｜人工办理" if lang == "zh" else "SERVICE | LOCATION | OWNER TYPE | STAFFED ROUTE", 4.8, MUTED)
    areas_zh = {"dazhongsi":"大钟寺", "corridor":"京张沿线", "ai_origin":"AI原点", "service_nodes":"服务节点", "zhongzhiyuan":"众智园", "three_key_areas":"三处片区"}
    areas_en = {"dazhongsi":"Dazhongsi", "corridor":"corridor", "ai_origin":"AI Origin", "service_nodes":"service nodes", "zhongzhiyuan":"Zhongzhiyuan", "three_key_areas":"3 districts"}
    for i, service in enumerate(services):
        col, row = i % 2, i // 2
        x = .025 + col * .49
        y = .82 - row * .125
        color = [GREEN, CYAN, ORANGE, GOLD][i % 4]
        service_panel.add_patch(FancyBboxPatch((x, y - .078), .465, .092, boxstyle="round,pad=.003,rounding_size=.008", transform=service_panel.transAxes, fc=color+"0D", ec=LINE, lw=.55))
        text(service_panel, x + .014, y - .006, service["id"], 5.0, color, True)
        name = service["name_zh"] if lang == "zh" else service["name_en"]
        text(service_panel, x + .075, y - .006, name, 5.25 if lang == "zh" else 4.6, INK, True)
        area = (areas_zh if lang == "zh" else areas_en).get(service["area"], service["area"])
        owner = service["owner"] if lang == "zh" else "named operating body"
        text(service_panel, x + .075, y - .046, f"{area} · {owner}", 4.0, MUTED)

    review_panel = panel(fig, [.675, .25, .29, .425], face=PANEL, edge=LINE)
    text(review_panel, .06, .945, "申报审查条件" if lang == "zh" else "APPLICATION REVIEW", 8.0, INK, True)
    rules_zh = ["责任单位和经费", "人工或实体办理", "必要数据及保存期限", "个人信息保护", "故障切换和应急处置", "暂停和终止权限", "收费、状态和投诉公示", "运行记录和年度评估"]
    rules_en = ["owner + funding", "staffed or physical route", "necessary data + retention", "personal-data protection", "fault switching + emergency", "stop + termination authority", "fees, status + complaint notice", "records + annual review"]
    for i, rule in enumerate(rules_zh if lang == "zh" else rules_en):
        y = .855 - i * .088
        color = [GREEN, CYAN, GOLD, ORANGE][i % 4]
        review_panel.add_patch(Circle((.085, y), .022, transform=review_panel.transAxes, fc=color, ec="none"))
        text(review_panel, .085, y, f"{i+1:02d}", 4.1, WHITE, True, ha="center", va="center")
        text(review_panel, .14, y, rule, 5.0 if lang == "zh" else 4.4, INK, True, va="center")

    process = panel(fig, [.035, .105, .93, .105], face="#EEF1ED", edge=LINE)
    stages_zh = ["项目申报", "联合审查", "试运行评估", "验收移交", "年度复核"]
    stages_en = ["APPLICATION", "JOINT REVIEW", "TRIAL OPERATION", "HANDOVER", "ANNUAL REVIEW"]
    outputs_zh = ["项目任务书", "部门意见", "整改清单", "移交记录", "调整清单"]
    outputs_en = ["project brief", "review opinions", "action list", "handover record", "adjustment list"]
    for i, (stage, output) in enumerate(zip(stages_zh if lang == "zh" else stages_en, outputs_zh if lang == "zh" else outputs_en)):
        x = .035 + i * .19
        color = [INK, CYAN, ORANGE, GREEN, VIOLET][i]
        process.add_patch(Circle((x, .62), .025, transform=process.transAxes, fc=color, ec=WHITE, lw=.5))
        text(process, x + .04, .66, stage, 5.3 if lang == "zh" else 4.4, INK, True, va="center")
        text(process, x + .04, .35, output, 4.5, MUTED, va="center")
        if i < 4:
            process.add_patch(FancyArrowPatch((x + .14, .61), (x + .18, .61), transform=process.transAxes, arrowstyle="-|>", mutation_scale=7, color=INK, lw=.8))
    footer(root, "growth-runbook.json · implementation-operation-contract.json", "审查记录纳入项目立项、试运行评估、验收移交和年度复核", "review records feed project initiation, trial operation, handover and annual review", "06", lang)
    return fig


def image2_brand_system(lang):
    fig, root = page(
        "14 / PUBLIC IDENTITY",
        "公共空间标识与导视系统指引",
        "Public-space Identity and Wayfinding Guidelines",
        "建立轨道门户、方向导引和服务确认三级信息体系，统一设置、使用和维护要求",
        "A three-level system coordinates corridor gateways, direction signs and service confirmation",
        lang,
    )
    hero = panel(fig, [.035, .18, .565, .64], face="#D8D3CA", edge=INK, lw=.9)
    cover_image(hero, SCENES / "image2-public-identity.jpg", (1750, 1100), (.51, .50))
    hero.add_patch(Rectangle((0, 0), 1, .135, transform=hero.transAxes, fc=INK, alpha=.88, ec="none"))
    text(hero, .03, .095, "京张共长线" if lang == "zh" else "GROW WITH JINGZHANG", 11, WHITE, True)
    text(hero, .03, .045, "轨道门户 · 空间导引 · 人工服务 · 夜间识别" if lang == "zh" else "RAIL GATEWAY · WAYFINDING · HUMAN SERVICE · NIGHT IDENTITY", 5.6, CYAN, True)

    spec = panel(fig, [.62, .18, .345, .64], face=PANEL, edge=LINE)
    text(spec, .055, .955, "分级设置与使用要求" if lang == "zh" else "HIERARCHY + APPLICATION", 8.4, INK, True)
    text(spec, .055, .908, "形成连续、清晰、全年龄可识别的公共信息系统" if lang == "zh" else "A continuous, legible and all-age public-information system", 5.1, MUTED)

    hierarchy_zh = [
        ("一级｜轨道门户", "设置于重点片区入口和站城界面，标明项目名称与总体方向"),
        ("二级｜方向导引", "设置于路径转换点，标明目的地、距离、无障碍路线和换乘信息"),
        ("三级｜服务确认", "设置于服务节点，标明开放时段、人工窗口、服务状态和反馈渠道"),
    ]
    hierarchy_en = [
        ("L1 | CORRIDOR GATEWAY", "At district entrances and station-city interfaces; show identity and overall direction"),
        ("L2 | DIRECTION SIGN", "At route decisions; show destination, distance, accessible route and interchange"),
        ("L3 | SERVICE CONFIRMATION", "At service nodes; show hours, human desk, status and feedback route"),
    ]
    colors = [INK, CYAN, ORANGE]
    for i, (heading, body) in enumerate(hierarchy_zh if lang == "zh" else hierarchy_en):
        y = .82 - i * .17
        color = colors[i]
        spec.add_patch(FancyBboxPatch((.05, y - .11), .90, .135,
            boxstyle="round,pad=.004,rounding_size=.010", transform=spec.transAxes,
            fc=color + "0E", ec=LINE, lw=.6))
        spec.add_patch(Rectangle((.05, y - .11), .010, .135, transform=spec.transAxes, fc=color, ec="none"))
        text(spec, .08, y, heading, 5.8, color, True)
        text(spec, .08, y - .045, "\n".join(textwrap.wrap(body, width=24 if lang == "zh" else 45)), 4.55, INK, linespacing=1.25)

    spec.plot([.05, .95], [.335, .335], color=LINE, lw=.8, transform=spec.transAxes)
    text(spec, .055, .30, "信息与运维要求" if lang == "zh" else "INFORMATION + MAINTENANCE", 6.7, INK, True)
    requirements_zh = [
        "项目标识与政府机关标志分区设置，保持信息边界清晰",
        "人工智能服务点同步设置人工服务标识和非数字办理说明",
        "公共橙用于责任提示、服务状态和停止信息，常态导引采用墨蓝与市民青",
        "每月开展设施巡检；常规故障24小时内建立工单并公开状态",
    ]
    requirements_en = [
        "Separate project identity from government emblems and maintain a clear information boundary",
        "Every AI service point includes a human-service sign and non-digital access instructions",
        "Coral marks duty, service status and stop information; navy and cyan support routine navigation",
        "Inspect monthly; create and publish a routine-fault work order within 24 hours",
    ]
    for i, item in enumerate(requirements_zh if lang == "zh" else requirements_en):
        y = .255 - i * .052
        color = [GREEN, CYAN, ORANGE, GOLD][i]
        spec.add_patch(Circle((.071, y), .009, transform=spec.transAxes, fc=color, ec="none"))
        text(spec, .095, y + .012, "\n".join(textwrap.wrap(item, width=28 if lang == "zh" else 58)), 4.4, INK, va="top", linespacing=1.2)

    palette = [INK, GREEN, CYAN, ORANGE, GOLD]
    for i, color in enumerate(palette):
        spec.add_patch(Rectangle((.055 + i * .177, .025), .165, .025, transform=spec.transAxes, fc=color, ec="none"))
    footer(root, "image2-public-identity.jpg · brand-system.json · implementation-operation-contract.json",
           "公共标识纳入建设项目统一设计、设置和维护",
           "public identity is designed, installed and maintained through the delivery program", "14", lang)
    return fig


BUILDERS = {
    "site-overview": image2_site_overview,
    "land-use-structure": image2_land_use_structure,
    "key-areas": key_areas,
    "mobility-bluegreen": image2_mobility_bluegreen,
    "metrics-evidence": metrics_evidence,
    "implementation-protocol": image2_implementation_protocol,
    "inclusion-incidence": inclusion_incidence,
    "area-action-plan": area_action_plan,
    "implementation-section": implementation_section,
    "service-node-kit": service_node_kit,
    "regional-collaboration": regional_collaboration,
    "ai-governance": ai_governance,
    "delivery-program": delivery_program,
    "brand-system": image2_brand_system,
    "rights-evidence": rights_evidence,
}

BOOKLET_ORDER = [
    "site-overview", "land-use-structure", "key-areas", "mobility-bluegreen",
    "metrics-evidence", "implementation-protocol", "inclusion-incidence", "area-action-plan",
    "implementation-section", "service-node-kit", "regional-collaboration", "ai-governance",
    "delivery-program", "brand-system", "rights-evidence",
]

A0_ORDER = [
    "site-overview", "key-areas", "implementation-protocol", "metrics-evidence",
    "land-use-structure", "mobility-bluegreen", "inclusion-incidence", "area-action-plan",
    "implementation-section", "service-node-kit", "regional-collaboration", "rights-evidence",
]


def save_fig(name, lang, fig):
    FIG.mkdir(parents=True, exist_ok=True)
    path = FIG / f"{name}{'.en' if lang == 'en' else ''}.png"
    build_dir = ROOT / "tmp" / "jingzhang-figure-build"
    build_dir.mkdir(parents=True, exist_ok=True)
    raw = build_dir / f"{name}{'.en' if lang == 'en' else ''}.raw.png"
    optimized = build_dir / f"{name}{'.en' if lang == 'en' else ''}.optimized.png"
    fig.savefig(raw, dpi=DPI, facecolor=PAPER, bbox_inches=None, pad_inches=0)
    plt.close(fig)
    with Image.open(raw) as source:
        rendered = source.convert("RGB")
    indexed = rendered.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
    indexed.save(optimized, format="PNG", optimize=True, compress_level=9)
    # On Windows the atlas preview may briefly keep the existing PNG open.
    # copyfile overwrites the bytes without requiring an atomic rename over that handle.
    shutil.copyfile(optimized, path)
    optimized.unlink()
    raw.unlink()


def make_pdf(path: Path, figure_names: list[str], lang="zh", a0=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    cache = ROOT / "tmp" / "jingzhang-pdf-cache" / ("en" if lang == "en" else "zh")
    cache.mkdir(parents=True, exist_ok=True)
    jpeg_pages = {}
    for name in figure_names:
        src = FIG / f"{name}{'.en' if lang == 'en' else ''}.png"
        dst = cache / f"{name}.jpg"
        Image.open(src).convert("RGB").save(dst, format="JPEG", quality=52, subsampling=2, optimize=True)
        jpeg_pages[name] = dst
    size = landscape(A0 if a0 else A3)
    c = canvas.Canvas(str(path), pagesize=size, pageCompression=1)
    pw, ph = size
    if not a0:
        for name in figure_names:
            c.drawImage(str(jpeg_pages[name]), 0, 0, width=pw, height=ph, preserveAspectRatio=False, mask="auto")
            c.showPage()
    else:
        groups = [figure_names[i:i+4] for i in range(0, len(figure_names), 4)]
        margin, gap = 22, 12
        cell_w = (pw - 2*margin - gap) / 2
        cell_h = (ph - 2*margin - gap) / 2
        for group in groups:
            c.setFillColorRGB(.949, .937, .906)
            c.rect(0, 0, pw, ph, fill=1, stroke=0)
            for j, name in enumerate(group):
                col, row = j % 2, j // 2
                x = margin + col*(cell_w+gap)
                y = ph-margin-(row+1)*cell_h-row*gap
                c.drawImage(str(jpeg_pages[name]), x, y, width=cell_w, height=cell_h, preserveAspectRatio=False, mask="auto")
            c.showPage()
    c.save()


def load_legacy_builder():
    path = ROOT / "scripts" / "build_jingzhang_package_v3.py"
    spec = importlib.util.spec_from_file_location("jingzhang_v3", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def build_all():
    for lang in ("zh", "en"):
        for name in BOOKLET_ORDER:
            print(f"render {lang} {name}", flush=True)
            save_fig(name, lang, BUILDERS[name](lang))
    legacy = load_legacy_builder()
    for lang in ("zh", "en"):
        make_pdf(DRAWINGS / ("a3-booklet.en.pdf" if lang == "en" else "a3-booklet.pdf"), BOOKLET_ORDER, lang, a0=False)
        make_pdf(DRAWINGS / ("a0-boards.en.pdf" if lang == "en" else "a0-boards.pdf"), A0_ORDER, lang, a0=True)
        legacy.build_visual_html(lang)
    legacy.build_equivalence_audit()
    legacy.refresh_manifest()
    print("built 30 professional figures, four PDFs and two HTML atlases", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--figure", choices=sorted(BUILDERS))
    parser.add_argument("--lang", choices=["zh", "en"], default="zh")
    args = parser.parse_args()
    if args.figure:
        save_fig(args.figure, args.lang, BUILDERS[args.figure](args.lang))
    else:
        build_all()


if __name__ == "__main__":
    main()
