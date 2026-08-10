#!/usr/bin/env python3
"""Redraw CaoChen13 stage-13 bilingual figures from submission data.

The original scaffold figures were generic placeholders.  This renderer keeps
all spatial marks tied to the submission GeoJSON and all displayed metric
values tied to metrics.json.  It intentionally uses no web map or OSM layer.
"""

from __future__ import annotations

import argparse
import json
import math
import warnings
from pathlib import Path
from typing import Any, Iterable

import matplotlib

matplotlib.use("Agg")

import matplotlib.font_manager as font_manager
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from shapely.geometry import shape


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUBMISSION = REPO_ROOT / "submissions" / "CaoChen13" / "jingzhang-probe"
FONT_PATH = Path(r"C:\Windows\Fonts\msyh.ttc")

PAPER = "#F4F2EC"
PANEL = "#FBFAF6"
INK = "#14212B"
MUTED = "#627078"
LINE = "#C9CEC9"
NAVY = "#173B4E"
GREEN = "#4F8062"
GREEN_LIGHT = "#CFE2D2"
TEAL = "#1E7B78"
CYAN = "#68A9B2"
GOLD = "#C7923E"
AMBER = "#E0B567"
CORAL = "#D56A52"
RED = "#A84A3D"
PURPLE = "#6B5A86"
BLUE = "#3F6F8C"

LANG = {
    "zh": {
        "kicker": "京张探针公带 · 数据同源图解",
        "status": "PROVISIONAL · 临时边界",
        "provisional": "PROVISIONAL · 临时边界仅供 intake 展示与可替换复算；不是官方红线、尺寸依据或专业图纸。",
        "source": "数据来源",
        "legend": "图例",
    },
    "en": {
        "kicker": "JING-ZHANG PROBE COMMONS · DATA-COHERENT DIAGRAM",
        "status": "PROVISIONAL BOUNDARY",
        "provisional": "PROVISIONAL · Boundary is for intake display and replaceable recalculation only; not an official redline, dimensional basis, or professional drawing.",
        "source": "DATA SOURCES",
        "legend": "LEGEND",
    },
}


def configure_font() -> str:
    if not FONT_PATH.is_file():
        raise FileNotFoundError(f"required CJK font is missing: {FONT_PATH}")
    font_manager.fontManager.addfont(str(FONT_PATH))
    family = font_manager.FontProperties(fname=str(FONT_PATH)).get_name()
    matplotlib.rcParams["font.family"] = "sans-serif"
    matplotlib.rcParams["font.sans-serif"] = [family, "Microsoft YaHei"]
    matplotlib.rcParams["axes.unicode_minus"] = False
    matplotlib.rcParams["svg.fonttype"] = "none"
    return family


FONT_FAMILY = configure_font()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_features(submission: Path, stem: str) -> list[dict[str, Any]]:
    return load_json(submission / "geometry" / f"{stem}.geojson")["features"]


def by_id(features: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {feature["properties"]["id"]: feature for feature in features}


def geom(feature: dict[str, Any]):
    return shape(feature["geometry"])


def polygons(geometry):
    if geometry.geom_type == "Polygon":
        yield geometry
    elif geometry.geom_type == "MultiPolygon":
        yield from geometry.geoms
    else:
        raise TypeError(f"expected Polygon or MultiPolygon, received {geometry.geom_type}")


def lines(geometry):
    if geometry.geom_type == "LineString":
        yield geometry
    elif geometry.geom_type == "MultiLineString":
        yield from geometry.geoms
    else:
        raise TypeError(f"expected LineString or MultiLineString, received {geometry.geom_type}")


def plot_polygon(
    ax,
    geometry,
    *,
    facecolor: str,
    edgecolor: str,
    linewidth: float = 1.2,
    alpha: float = 1.0,
    hatch: str | None = None,
    linestyle: str = "-",
    zorder: float = 1,
):
    artists = []
    for polygon in polygons(geometry):
        artist = patches.Polygon(
            list(polygon.exterior.coords),
            closed=True,
            facecolor=facecolor,
            edgecolor=edgecolor,
            linewidth=linewidth,
            alpha=alpha,
            hatch=hatch,
            linestyle=linestyle,
            joinstyle="round",
            zorder=zorder,
        )
        ax.add_patch(artist)
        artists.append(artist)
    return artists


def plot_line(
    ax,
    geometry,
    *,
    color: str,
    linewidth: float = 1.5,
    linestyle: str = "-",
    alpha: float = 1.0,
    zorder: float = 3,
):
    artists = []
    for line in lines(geometry):
        xs, ys = line.xy
        artists.extend(
            ax.plot(
                xs,
                ys,
                color=color,
                linewidth=linewidth,
                linestyle=linestyle,
                alpha=alpha,
                solid_capstyle="round",
                zorder=zorder,
            )
        )
    return artists


def style_map(ax, boundary, *, x_padding: float, y_padding: float) -> None:
    minx, miny, maxx, maxy = boundary.bounds
    ax.set_xlim(minx - x_padding, maxx + x_padding)
    ax.set_ylim(miny - y_padding, maxy + y_padding)
    ax.set_aspect(1 / math.cos(math.radians((miny + maxy) / 2)))
    ax.set_facecolor(PANEL)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color(LINE)
        spine.set_linewidth(0.9)


def north_arrow(ax, x: float = 0.94, y: float = 0.93) -> None:
    ax.annotate(
        "N",
        xy=(x, y),
        xytext=(x, y - 0.09),
        xycoords="axes fraction",
        textcoords="axes fraction",
        ha="center",
        va="center",
        fontsize=8,
        color=INK,
        arrowprops={"arrowstyle": "-|>", "color": INK, "linewidth": 1.0},
        zorder=20,
    )


def add_shell(fig, lang: str, title: str, subtitle: str, accent: str, source: str) -> None:
    text = LANG[lang]
    fig.patch.set_facecolor(PAPER)
    fig.add_artist(
        patches.Rectangle((0.047, 0.895), 0.006, 0.075, transform=fig.transFigure, facecolor=accent, edgecolor="none")
    )
    fig.text(0.061, 0.965, text["kicker"], ha="left", va="top", fontsize=7.5, color=accent, weight="bold")
    fig.text(0.061, 0.935, title, ha="left", va="top", fontsize=23, color=INK, weight="bold")
    fig.text(0.061, 0.893, subtitle, ha="left", va="top", fontsize=9.2, color=MUTED)
    fig.text(
        0.945,
        0.944,
        text["status"],
        ha="right",
        va="center",
        fontsize=7.4,
        color=RED,
        weight="bold",
        bbox={"boxstyle": "round,pad=0.55", "facecolor": "#F4E3DF", "edgecolor": "#D8A69B", "linewidth": 0.8},
    )
    fig.add_artist(patches.Rectangle((0.047, 0.018), 0.898, 0.075, transform=fig.transFigure, facecolor=INK, edgecolor="none"))
    fig.text(0.061, 0.070, f"{text['source']}  /  {source}", ha="left", va="center", fontsize=6.9, color="#DDE5E5")
    fig.text(0.061, 0.040, text["provisional"], ha="left", va="center", fontsize=7.2, color="#F0C9BE", weight="bold")


def add_card(ax, y: float, h: float, title: str, body: str, accent: str, *, icon: str | None = None, face: str = PANEL) -> None:
    ax.add_patch(
        patches.FancyBboxPatch(
            (0.015, y),
            0.97,
            h,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            transform=ax.transAxes,
            facecolor=face,
            edgecolor=LINE,
            linewidth=0.8,
        )
    )
    ax.add_patch(patches.Rectangle((0.015, y), 0.012, h, transform=ax.transAxes, facecolor=accent, edgecolor="none"))
    title_x = 0.055
    if icon:
        ax.text(0.064, y + h - 0.052, icon, transform=ax.transAxes, ha="center", va="center", fontsize=13, color=accent, weight="bold")
        title_x = 0.105
    ax.text(title_x, y + h - 0.034, title, transform=ax.transAxes, ha="left", va="top", fontsize=8.8, color=accent, weight="bold")
    ax.text(0.055, y + h - 0.079, body, transform=ax.transAxes, ha="left", va="top", fontsize=7.4, color=INK, linespacing=1.5)


def add_legend(ax, lang: str, items: list[tuple[str, str]], *, y: float = 0.02, columns: int = 2) -> None:
    ax.text(0.02, y + 0.145, LANG[lang]["legend"], transform=ax.transAxes, ha="left", va="bottom", fontsize=7.5, color=MUTED, weight="bold")
    rows = math.ceil(len(items) / columns)
    for index, (label, color) in enumerate(items):
        column = index // rows
        row = index % rows
        x = 0.02 + column * (0.96 / columns)
        yy = y + 0.108 - row * 0.042
        ax.add_patch(patches.Rectangle((x, yy), 0.028, 0.016, transform=ax.transAxes, facecolor=color, edgecolor="none"))
        ax.text(x + 0.04, yy + 0.008, label, transform=ax.transAxes, ha="left", va="center", fontsize=6.6, color=INK)


def save_figure(fig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        fig.savefig(path, dpi=150, facecolor=fig.get_facecolor(), metadata={"Software": "Matplotlib + Microsoft YaHei"})
    plt.close(fig)
    missing = [str(item.message) for item in caught if "Glyph" in str(item.message) and "missing" in str(item.message)]
    if missing:
        raise RuntimeError(f"missing font glyphs while rendering {path.name}: {missing}")


def data_bundle(submission: Path) -> dict[str, Any]:
    return {
        "boundary": load_features(submission, "site_boundary"),
        "key": load_features(submission, "key_areas"),
        "land": load_features(submission, "land_use"),
        "roads": load_features(submission, "roads"),
        "green": load_features(submission, "green_space"),
        "public": load_features(submission, "public_space"),
        "metrics": load_json(submission / "metrics.json")["metrics"],
    }


def render_site_overview(submission: Path, data: dict[str, Any], lang: str) -> Path:
    zh = lang == "zh"
    fig = plt.figure(figsize=(16, 9), dpi=150)
    add_shell(
        fig,
        lang,
        "总体空间结构" if zh else "Overall Spatial Structure",
        "公共创新带、差异化核心、协同翼与证据回路落在同一组真实几何上" if zh else "Public innovation band, differentiated cores, service wings, and an evidence loop on one geometry base",
        NAVY,
        "geometry/site_boundary.geojson · roads.geojson · green_space.geojson · key_areas.geojson",
    )
    ax = fig.add_axes((0.055, 0.12, 0.56, 0.73))
    side = fig.add_axes((0.645, 0.12, 0.30, 0.73))
    side.axis("off")
    boundary = geom(data["boundary"][0])
    style_map(ax, boundary, x_padding=0.0105, y_padding=0.0035)
    plot_polygon(ax, boundary, facecolor="#ECEBE5", edgecolor=MUTED, linewidth=1.1, linestyle="--", zorder=1)
    for feature in data["green"]:
        plot_polygon(ax, geom(feature), facecolor=GREEN_LIGHT, edgecolor=GREEN, linewidth=0.5, alpha=0.9, zorder=2)
    road_styles = {
        "greenway": (NAVY, 2.7, "-"),
        "cycleway": (CYAN, 1.25, "-"),
        "pedestrian": (TEAL, 0.85, "--"),
        "transit_connection": (GOLD, 0.85, (0, (3, 3))),
    }
    for feature in data["roads"]:
        style = road_styles[feature["properties"]["road_class"]]
        plot_line(ax, geom(feature), color=style[0], linewidth=style[1], linestyle=style[2], alpha=0.9, zorder=4)

    area_colors = [PURPLE, TEAL, CORAL]
    area_markers = ["^", "s", "o"]
    centroids = []
    for feature, color, marker in zip(data["key"], area_colors, area_markers):
        geometry = geom(feature)
        centroids.append(geometry.centroid)
        plot_polygon(ax, geometry, facecolor=color, edgecolor=color, linewidth=1.5, alpha=0.17, zorder=3)
        ax.scatter(geometry.centroid.x, geometry.centroid.y, marker=marker, s=52, facecolor=color, edgecolor="white", linewidth=0.8, zorder=8)

    minx, miny, maxx, maxy = boundary.bounds
    wing_y = (miny + maxy) / 2
    left_label = "科技服务翼\n知识与专业服务" if zh else "TECH SERVICE WING\nKnowledge interfaces"
    right_label = "场景赋能翼\n观察、试用、反馈" if zh else "SCENARIO WING\nObserve · trial · feedback"
    wing_offset = 0.0065 if zh else 0.0082
    wing_font = 7.2 if zh else 6.5
    ax.text(minx - wing_offset, wing_y, left_label, ha="center", va="center", fontsize=wing_font, color=BLUE, weight="bold", bbox={"boxstyle": "round,pad=0.55", "facecolor": "#E4EDF1", "edgecolor": BLUE, "linewidth": 0.8})
    ax.text(maxx + wing_offset, wing_y, right_label, ha="center", va="center", fontsize=wing_font, color=GOLD, weight="bold", bbox={"boxstyle": "round,pad=0.55", "facecolor": "#F4EBD8", "edgecolor": GOLD, "linewidth": 0.8})
    ax.plot((minx - 0.0037, minx + 0.003), (wing_y, wing_y), color=BLUE, linewidth=0.9, linestyle="--", zorder=2)
    ax.plot((maxx - 0.003, maxx + 0.0037), (wing_y, wing_y), color=GOLD, linewidth=0.9, linestyle="--", zorder=2)

    for start, end in zip(centroids, centroids[1:]):
        ax.add_patch(FancyArrowPatch((start.x, start.y), (end.x, end.y), arrowstyle="-|>", mutation_scale=8, linewidth=1.0, color=PURPLE, alpha=0.72, connectionstyle="arc3,rad=0.16", zorder=7))
    ax.add_patch(FancyArrowPatch((centroids[-1].x, centroids[-1].y), (centroids[0].x, centroids[0].y), arrowstyle="-|>", mutation_scale=8, linewidth=0.95, color=PURPLE, alpha=0.6, linestyle="--", connectionstyle="arc3,rad=-0.32", zorder=6))
    ax.text(0.045, 0.955, "真实几何底图" if zh else "GEOMETRY BASE", transform=ax.transAxes, ha="left", va="top", fontsize=7.4, color=MUTED, weight="bold")
    ax.text(0.045, 0.917, "公共创新带" if zh else "PUBLIC INNOVATION BAND", transform=ax.transAxes, ha="left", va="top", fontsize=10.5, color=NAVY, weight="bold")
    north_arrow(ax)

    side.text(0.02, 0.99, "结构释义" if zh else "STRUCTURE READING", transform=side.transAxes, ha="left", va="top", fontsize=8, color=MUTED, weight="bold")
    add_card(side, 0.77, 0.16, "公共创新带" if zh else "PUBLIC INNOVATION BAND", "绿脊承载连续慢行与日常公共界面；\n主脊与横向联系均来自 roads 图层。" if zh else "Green spine carries continuous slow mobility and\ndaily public interfaces; alignments come from roads.", NAVY)
    add_card(side, 0.57, 0.16, "研发核 · 转化核 · 应用核" if zh else "RESEARCH · TRANSFER · APPLICATION CORES", "众智园：开放问题与受控验证\nAI 原点：开源转化与人才服务\n大钟寺：智能业态与日常服务" if zh else "Zhongzhiyuan: open briefs + governed tests\nAI Origin: open transfer + talent services\nDazhongsi: AI-native commerce + daily services", TEAL)
    add_card(side, 0.37, 0.16, "东西协同翼" if zh else "COMPLEMENTARY SERVICE WINGS", "科技服务翼提供知识与专业接口；\n场景赋能翼组织观察、试用与公共反馈。" if zh else "Tech-service wing supplies knowledge interfaces;\nscenario wing organizes observation, trials, feedback.", GOLD)
    add_card(side, 0.17, 0.16, "证据回路" if zh else "EVIDENCE LOOP", "问题 → 空间建议 → 受控试用 → 人工复核 → 维护；\n失败可返回上游，不把演示当成实施。" if zh else "Question → spatial proposal → governed trial →\nhuman review → maintenance; failure loops upstream.", PURPLE)
    add_legend(side, lang, [("临时范围" if zh else "Provisional scope", MUTED), ("公共带" if zh else "Public band", NAVY), ("重点核心" if zh else "Key cores", TEAL), ("证据回路" if zh else "Evidence loop", PURPLE)], y=0.005)
    out = submission / "assets" / "figures" / ("site-overview.png" if zh else "site-overview.en.png")
    save_figure(fig, out)
    return out


def render_key_areas(submission: Path, data: dict[str, Any], lang: str) -> Path:
    zh = lang == "zh"
    fig = plt.figure(figsize=(16, 9), dpi=150)
    add_shell(
        fig,
        lang,
        "重点片区：三种城市接口" if zh else "Key Areas: Three Urban Interfaces",
        "同一任务走廊内，三处临时范围以不同符号、空间角色与策略抓手表达" if zh else "Within one task corridor, each provisional area has a distinct symbol, spatial role, and strategy",
        PURPLE,
        "geometry/key_areas.geojson · site_boundary.geojson  /  metrics.json: key_area_count",
    )
    ax = fig.add_axes((0.055, 0.12, 0.49, 0.73))
    side = fig.add_axes((0.575, 0.12, 0.37, 0.73))
    side.axis("off")
    boundary = geom(data["boundary"][0])
    style_map(ax, boundary, x_padding=0.0055, y_padding=0.0035)
    plot_polygon(ax, boundary, facecolor="#ECEBE5", edgecolor=MUTED, linewidth=1.1, linestyle="--", zorder=1)
    spine = by_id(data["roads"])["ROAD-001"]
    plot_line(ax, geom(spine), color=NAVY, linewidth=2.2, alpha=0.72, zorder=2)

    styles = [
        {"color": PURPLE, "hatch": "////", "marker": "^"},
        {"color": TEAL, "hatch": None, "marker": "s"},
        {"color": CORAL, "hatch": "..", "marker": "o"},
    ]
    for feature, style in zip(data["key"], styles):
        geometry = geom(feature)
        plot_polygon(ax, geometry, facecolor=style["color"], edgecolor=style["color"], linewidth=1.7, alpha=0.22, hatch=style["hatch"], zorder=3)
        ax.scatter(geometry.centroid.x, geometry.centroid.y, marker=style["marker"], s=86, facecolor=style["color"], edgecolor="white", linewidth=1.2, zorder=7)
    ax.text(0.045, 0.955, f"key_area_count = {metric_value(data['metrics'], 'key_area_count')}", transform=ax.transAxes, ha="left", va="top", fontsize=8.5, color=PURPLE, family="monospace", weight="bold")
    ax.text(0.045, 0.915, "形状仅为临时定位，非地块或道路红线" if zh else "Shapes are provisional locators, not parcel or road redlines", transform=ax.transAxes, ha="left", va="top", fontsize=7.2, color=MUTED)
    north_arrow(ax)

    side.text(0.02, 0.99, "差异化策略" if zh else "DIFFERENTIATED STRATEGIES", transform=side.transAxes, ha="left", va="top", fontsize=8, color=MUTED, weight="bold")
    add_card(side, 0.70, 0.23, "众智园 · 研发验证接口" if zh else "ZHONGZHIYUAN · R&D VALIDATION", "开放问题客厅\n受控室内测试与版本化交接\n低风险公共展示、失败即退回沙盒" if zh else "Open-problem commons\nGoverned indoor tests + versioned handoff\nLow-risk display; failed gates return to sandbox", PURPLE, icon="▲", face="#F3EFF7")
    add_card(side, 0.43, 0.23, "AI 原点社区 · 开源转化接口" if zh else "AI ORIGIN · OPEN TRANSFER", "近校共享街与人才服务\n模型红队、人工复核与申诉\n存量空间优先，可撤组件补位" if zh else "Campus-adjacent shared street + talent services\nModel red-team, human review, appeal route\nExisting space first; reversible components", TEAL, icon="■", face="#EAF3F0")
    add_card(side, 0.16, 0.23, "大钟寺 · 日常应用接口" if zh else "DAZHONGSI · DAILY APPLICATION", "多语公共解释与商户自愿辅导\n共享桌、可锁设备柜、可撤展示轨\n消防或运营资料不足时保留基础服务" if zh else "Multilingual interpretation + opt-in merchant help\nShared tables, lockable cabinets, demountable rail\nIf fire/operations evidence is absent, keep basics", CORAL, icon="●", face="#F7ECE8")
    add_legend(side, lang, [("研发验证" if zh else "R&D validation", PURPLE), ("开源转化" if zh else "Open transfer", TEAL), ("日常应用" if zh else "Daily application", CORAL), ("临时范围" if zh else "Provisional scope", MUTED)], y=0.005)
    out = submission / "assets" / "figures" / ("key-areas.png" if zh else "key-areas.en.png")
    save_figure(fig, out)
    return out


def render_land_use(submission: Path, data: dict[str, Any], lang: str) -> Path:
    zh = lang == "zh"
    fig = plt.figure(figsize=(16, 9), dpi=150)
    add_shell(
        fig,
        lang,
        "用地结构：关系型概念分区" if zh else "Land-use Structure: Relational Concept Zoning",
        "分区回答方案希望发生什么关系；不回答土地今天是什么，也不替代法定用途" if zh else "Zones express intended relationships; they do not claim present use or replace statutory planning",
        GREEN,
        "geometry/land_use.geojson · site_boundary.geojson",
    )
    ax = fig.add_axes((0.055, 0.12, 0.52, 0.73))
    side = fig.add_axes((0.605, 0.12, 0.34, 0.73))
    side.axis("off")
    boundary = geom(data["boundary"][0])
    style_map(ax, boundary, x_padding=0.0046, y_padding=0.0035)
    palette = {
        "LU-001": "#6FA178",
        "LU-002": "#A7C9B1",
        "LU-003": "#D9CDB5",
        "LU-004": "#D98B67",
        "LU-005": "#7AA3B5",
        "LU-006": "#9B91B4",
    }
    for feature in data["land"]:
        identifier = feature["properties"]["id"]
        plot_polygon(ax, geom(feature), facecolor=palette[identifier], edgecolor=PANEL, linewidth=0.95, alpha=0.92, zorder=2)
    plot_polygon(ax, boundary, facecolor="none", edgecolor=MUTED, linewidth=1.1, linestyle="--", zorder=5)
    ax.text(0.045, 0.955, "CONCEPT ONLY" if zh else "CONCEPT ONLY", transform=ax.transAxes, ha="left", va="top", fontsize=8.5, color=RED, weight="bold")
    ax.text(0.045, 0.915, "概念分区 ≠ 现状用地" if zh else "CONCEPT ZONING ≠ EXISTING LAND USE", transform=ax.transAxes, ha="left", va="top", fontsize=10.2, color=RED, weight="bold")
    north_arrow(ax)

    side.add_patch(patches.FancyBboxPatch((0.015, 0.82), 0.97, 0.13, boxstyle="round,pad=0.012,rounding_size=0.018", transform=side.transAxes, facecolor="#F4E3DF", edgecolor="#D8A69B", linewidth=0.9))
    side.text(0.05, 0.92, "证据边界" if zh else "EVIDENCE BOUNDARY", transform=side.transAxes, ha="left", va="top", fontsize=8.2, color=RED, weight="bold")
    side.text(0.05, 0.875, "现状用途、权属、法定规划用途与容量控制均待官方资料和现场核验。" if zh else "Present use, tenure, statutory designation, and capacity controls require official data and field verification.", transform=side.transAxes, ha="left", va="top", fontsize=7.3, color=INK, linespacing=1.45)

    side.text(0.02, 0.77, "空间关系" if zh else "SPATIAL RELATIONSHIP", transform=side.transAxes, ha="left", va="top", fontsize=8, color=MUTED, weight="bold")
    bands = [
        ("居住兼容更新" if zh else "RESIDENTIAL\nCOMPATIBLE", palette["LU-003"], 0.06, 0.20),
        ("社区服务界面" if zh else "SERVICE\nINTERFACE", palette["LU-002"], 0.27, 0.18),
        ("绿地核心" if zh else "GREEN\nCORE", palette["LU-001"], 0.46, 0.12),
        ("东侧复合界面" if zh else "EAST MIXED\nINTERFACE", palette["LU-005"], 0.59, 0.35),
    ]
    for label, color, x, width in bands:
        side.add_patch(patches.FancyBboxPatch((x, 0.66), width, 0.07, boxstyle="round,pad=0.005,rounding_size=0.01", transform=side.transAxes, facecolor=color, edgecolor=PANEL, linewidth=0.8))
        side.text(x + width / 2, 0.695, label, transform=side.transAxes, ha="center", va="center", fontsize=5.9 if zh else 5.3, color=INK, weight="bold", linespacing=1.05)
    side.text(0.06, 0.62, "西侧兼容更新" if zh else "WEST: COMPATIBLE RENEWAL", transform=side.transAxes, ha="left", va="top", fontsize=6.8, color=MUTED)
    side.text(0.94, 0.62, "东侧教育 / 科研 / 商业兼容" if zh else "EAST: EDUCATION / RESEARCH / COMMERCE", transform=side.transAxes, ha="right", va="top", fontsize=6.8, color=MUTED)

    add_card(side, 0.43, 0.13, "公共带优先" if zh else "PUBLIC BAND FIRST", "绿地核心与社区服务界面共同保障连续、可见、可进入的日常路径。" if zh else "Green core and service interface protect a continuous, visible, accessible daily route.", GREEN)
    add_card(side, 0.26, 0.13, "兼容而非替换" if zh else "COMPATIBILITY, NOT REPLACEMENT", "外围分区是深化比较层；没有官方地块就不生成地块容量或调整结论。" if zh else "Outer zones are comparison layers; no parcel capacity or land-change claim without official parcels.", GOLD)
    legend_items = [
        ("绿地核心" if zh else "Green core", palette["LU-001"]),
        ("社区服务界面" if zh else "Service interface", palette["LU-002"]),
        ("居住兼容更新" if zh else "Residential-compatible", palette["LU-003"]),
        ("商业服务兼容" if zh else "Commercial-compatible", palette["LU-004"]),
        ("科研开放兼容" if zh else "Research-compatible", palette["LU-005"]),
        ("教育共享兼容" if zh else "Education-compatible", palette["LU-006"]),
    ]
    add_legend(side, lang, legend_items, y=0.005, columns=2)
    out = submission / "assets" / "figures" / ("land-use-structure.png" if zh else "land-use-structure.en.png")
    save_figure(fig, out)
    return out


def render_mobility(submission: Path, data: dict[str, Any], lang: str) -> Path:
    zh = lang == "zh"
    fig = plt.figure(figsize=(16, 9), dpi=150)
    add_shell(
        fig,
        lang,
        "交通慢行与蓝绿连续网络" if zh else "Slow Mobility and Blue-green Continuity",
        "慢行先连续，轨道先核真；绿脊、公共节点与横向联系共用同一临时空间基底" if zh else "Continuity first for walking and cycling; verify rail first; green spine, public nodes, and cross-links share one provisional base",
        TEAL,
        "geometry/roads.geojson · green_space.geojson · public_space.geojson · site_boundary.geojson",
    )
    ax = fig.add_axes((0.055, 0.12, 0.56, 0.73))
    side = fig.add_axes((0.645, 0.12, 0.30, 0.73))
    side.axis("off")
    boundary = geom(data["boundary"][0])
    style_map(ax, boundary, x_padding=0.0055, y_padding=0.0035)
    plot_polygon(ax, boundary, facecolor="#ECEBE5", edgecolor=MUTED, linewidth=1.1, linestyle="--", zorder=1)
    for feature in data["green"]:
        plot_polygon(ax, geom(feature), facecolor=GREEN_LIGHT, edgecolor=GREEN, linewidth=0.55, alpha=0.95, zorder=2)
    for feature in data["public"]:
        plot_polygon(ax, geom(feature), facecolor=CYAN, edgecolor=TEAL, linewidth=0.6, alpha=0.85, zorder=3)
    for feature in data["roads"]:
        road_class = feature["properties"]["road_class"]
        if road_class == "greenway":
            plot_line(ax, geom(feature), color=NAVY, linewidth=2.7, zorder=6)
        elif road_class == "cycleway":
            plot_line(ax, geom(feature), color=BLUE, linewidth=1.5, zorder=7)
        elif road_class == "pedestrian":
            plot_line(ax, geom(feature), color=TEAL, linewidth=1.05, linestyle="--", zorder=7)
        else:
            plot_line(ax, geom(feature), color=GOLD, linewidth=1.1, linestyle=(0, (3, 3)), zorder=5)
    for feature in data["public"][1:]:
        point = geom(feature).centroid
        ax.scatter(point.x, point.y, s=22, facecolor=PANEL, edgecolor=TEAL, linewidth=1.0, zorder=9)
    ax.text(0.045, 0.955, "连续性目标 / 非工程线位" if zh else "CONTINUITY TARGET / NOT ENGINEERED ALIGNMENTS", transform=ax.transAxes, ha="left", va="top", fontsize=8.2, color=TEAL, weight="bold")
    ax.text(0.045, 0.915, "未绘制既定轨道或站口" if zh else "NO CONFIRMED RAIL OR STATION ALIGNMENT IS DRAWN", transform=ax.transAxes, ha="left", va="top", fontsize=7.2, color=RED, weight="bold")
    north_arrow(ax)

    side.add_patch(patches.FancyBboxPatch((0.015, 0.82), 0.97, 0.13, boxstyle="round,pad=0.012,rounding_size=0.018", transform=side.transAxes, facecolor="#F4EBD8", edgecolor="#D9B66F", linewidth=0.9))
    side.text(0.05, 0.92, "轨道相关：先核真" if zh else "RAIL: VERIFY FIRST", transform=side.transAxes, ha="left", va="top", fontsize=9, color=RED, weight="bold")
    side.text(0.05, 0.875, "站口、铁路状态、净空与接驳须用运营方、交通管理和测绘资料核验；OSM 不作为线位、尺寸或面积依据。" if zh else "Entrances, rail status, clearance, and interchange require operator, traffic, and survey evidence;\nOSM is not an alignment, dimension, or area basis.", transform=side.transAxes, ha="left", va="top", fontsize=7.1, color=INK, linespacing=1.45)

    side.text(0.02, 0.77, "连续性验证链" if zh else "CONTINUITY VERIFICATION", transform=side.transAxes, ha="left", va="top", fontsize=8, color=MUTED, weight="bold")
    flow = [
        ("记录断点" if zh else "RECORD GAPS", "通行、坡坎、过街、遮荫" if zh else "access, grades, crossings, shade", NAVY),
        ("人工与使用者复核" if zh else "HUMAN + USER REVIEW", "无障碍、安全、安静界面" if zh else "accessibility, safety, quiet edge", TEAL),
        ("选择可逆动作" if zh else "SELECT REVERSIBLE ACTION", "绕行、标线、轻量修复" if zh else "detour, markings, light repair", GOLD),
        ("验收并回写" if zh else "ACCEPT + WRITE BACK", "证据进入维护台账" if zh else "evidence enters maintenance ledger", PURPLE),
    ]
    y_positions = [0.66, 0.53, 0.40, 0.27]
    for (title, body, color), y in zip(flow, y_positions):
        side.add_patch(patches.FancyBboxPatch((0.08, y), 0.84, 0.09, boxstyle="round,pad=0.01,rounding_size=0.018", transform=side.transAxes, facecolor=PANEL, edgecolor=color, linewidth=0.9))
        side.add_patch(patches.Circle((0.13, y + 0.045), 0.018, transform=side.transAxes, facecolor=color, edgecolor="none"))
        side.text(0.18, y + 0.061, title, transform=side.transAxes, ha="left", va="center", fontsize=7.8, color=color, weight="bold")
        side.text(0.18, y + 0.030, body, transform=side.transAxes, ha="left", va="center", fontsize=6.8, color=INK)
    for y in [0.64, 0.51, 0.38]:
        side.annotate("", xy=(0.50, y - 0.008), xytext=(0.50, y + 0.016), xycoords=side.transAxes, textcoords=side.transAxes, arrowprops={"arrowstyle": "-|>", "color": MUTED, "linewidth": 0.8})
    add_legend(side, lang, [("绿脊与口袋" if zh else "Green spine + pockets", GREEN), ("公共空间" if zh else "Public space", CYAN), ("慢行主脊" if zh else "Slow-mobility spine", NAVY), ("待核横向联系" if zh else "Cross-links to verify", GOLD)], y=0.005)
    out = submission / "assets" / "figures" / ("mobility-bluegreen.png" if zh else "mobility-bluegreen.en.png")
    save_figure(fig, out)
    return out


def metric_value(metrics: dict[str, Any], field: str) -> Any:
    item = metrics[field]
    if item["status"] != "known":
        raise ValueError(f"{field} must be known")
    return item["value"]


def render_metrics(submission: Path, data: dict[str, Any], lang: str) -> Path:
    zh = lang == "zh"
    metrics = data["metrics"]
    known_fields = [
        "site_area_sqm",
        "building_footprint_area_sqm",
        "green_ratio",
        "public_space_ratio",
        "key_area_count",
    ]
    unknown_fields = [
        "affected_household_count",
        "mitigation_budget_cny",
        "floor_area_ratio",
        "building_height_m",
        "statutory_green_ratio",
    ]
    for field in unknown_fields:
        if metrics[field]["status"] != "unknown" or metrics[field]["value"] is not None:
            raise ValueError(f"{field} must remain unknown/null")

    fig = plt.figure(figsize=(16, 9), dpi=150)
    add_shell(
        fig,
        lang,
        "指标证据链：从几何到正文" if zh else "Metric Evidence Chain: Geometry to Narrative",
        "同名字段、固定公式与 unknown 状态让每一条正文判断可以回到输入层复算" if zh else "Named fields, fixed formulas, and explicit unknown states make narrative claims traceable to inputs",
        CORAL,
        "geometry/*.geojson · metrics.json · proposal.md / proposal.en.md",
    )
    ax = fig.add_axes((0.055, 0.12, 0.89, 0.73))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def panel(x: float, y: float, w: float, h: float, title: str, color: str, face: str = PANEL):
        ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.018", facecolor=face, edgecolor=LINE, linewidth=0.9))
        ax.add_patch(patches.Rectangle((x, y + h - 0.055), w, 0.055, facecolor=color, edgecolor="none"))
        ax.text(x + 0.02, y + h - 0.027, title, ha="left", va="center", fontsize=8.4, color="white", weight="bold")

    panel(0.00, 0.12, 0.20, 0.82, "几何输入" if zh else "GEOMETRY INPUTS", NAVY)
    input_rows = [
        ("site_boundary.geojson", "临时分母几何" if zh else "provisional denominator"),
        ("buildings.geojson", "概念建筑基底" if zh else "concept footprints"),
        ("green_space.geojson", "绿地方案并集" if zh else "proposal green union"),
        ("public_space.geojson", "公共空间并集" if zh else "public-space union"),
        ("key_areas.geojson", "重点片区要素" if zh else "key-area features"),
    ]
    for idx, (name, note) in enumerate(input_rows):
        y = 0.79 - idx * 0.135
        ax.add_patch(patches.FancyBboxPatch((0.025, y), 0.15, 0.085, boxstyle="round,pad=0.008,rounding_size=0.012", facecolor="#E7EEF1", edgecolor="#B8C8CF", linewidth=0.7))
        ax.text(0.038, y + 0.056, name, ha="left", va="center", fontsize=6.8, color=NAVY, family="monospace", weight="bold")
        ax.text(0.038, y + 0.026, note, ha="left", va="center", fontsize=6.4, color=MUTED)
    ax.text(0.025, 0.16, "仅使用投稿包内几何；\n不从 OSM 推导尺寸、面积或红线。" if zh else "Submission geometry only;\nOSM derives no dimension, area, or redline.", ha="left", va="bottom", fontsize=7, color=RED, linespacing=1.5, weight="bold")

    panel(0.29, 0.49, 0.42, 0.45, "metrics.json · known" if zh else "metrics.json · KNOWN", TEAL, face="#F3F8F6")
    known_labels = {
        "site_area_sqm": f"{metric_value(metrics, 'site_area_sqm')} sqm",
        "building_footprint_area_sqm": f"{metric_value(metrics, 'building_footprint_area_sqm')} sqm",
        "green_ratio": f"{metric_value(metrics, 'green_ratio')}",
        "public_space_ratio": f"{metric_value(metrics, 'public_space_ratio')}",
        "key_area_count": f"{metric_value(metrics, 'key_area_count')}",
    }
    for idx, field in enumerate(known_fields):
        y = 0.815 - idx * 0.066
        ax.text(0.315, y, field, ha="left", va="center", fontsize=7.0, color=INK, family="monospace")
        ax.text(0.685, y, known_labels[field], ha="right", va="center", fontsize=7.4, color=TEAL, family="monospace", weight="bold")
        if idx < len(known_fields) - 1:
            ax.plot((0.315, 0.685), (y - 0.033, y - 0.033), color="#D8E3DE", linewidth=0.6)
    ax.text(0.315, 0.535, "值按 metrics.json 原精度显示；图面不另行换算。" if zh else "Values use metrics.json precision; no display-only conversion.", ha="left", va="center", fontsize=6.5, color=MUTED)

    panel(0.29, 0.12, 0.42, 0.31, "metrics.json · unknown", RED, face="#FAF3F1")
    for idx, field in enumerate(unknown_fields):
        y = 0.348 - idx * 0.047
        ax.text(0.315, y, field, ha="left", va="center", fontsize=6.75, color=INK, family="monospace")
        ax.text(0.685, y, "unknown", ha="right", va="center", fontsize=7.2, color=RED, family="monospace", weight="bold")
    ax.text(0.315, 0.132, "不填美化值；补齐官方控制、调查、工程量与审核单价后再算。" if zh else "No cosmetic fill-ins; calculate only after controls, surveys, quantities, and reviewed rates exist.", ha="left", va="bottom", fontsize=6.4, color=MUTED)

    panel(0.80, 0.12, 0.20, 0.82, "正文证据" if zh else "NARRATIVE EVIDENCE", PURPLE)
    narrative_rows = [
        ("分母口径" if zh else "DENOMINATOR", "总体设计临时范围；\n研究范围不进入比率分母。" if zh else "Provisional overall-design scope;\nresearch context is not a ratio denominator."),
        ("方案比例" if zh else "PROPOSAL RATIOS", "绿地与公共空间分别复算；\n不冒充法定绿地率。" if zh else "Green and public-space unions recalculate\nseparately; neither is a statutory ratio."),
        ("缺口披露" if zh else "GAP DISCLOSURE", "住户、缓解预算、容积率、\n高度与法定绿地率保持 unknown。" if zh else "Households, mitigation budget, FAR,\nheight, and statutory green ratio stay unknown."),
        ("替换复算" if zh else "REPLACE + RERUN", "官方边界或控规到位后，\n替换输入并沿同一公式链重跑。" if zh else "When official boundaries or controls arrive,\nreplace inputs and rerun the same formulas."),
    ]
    for idx, (title, body) in enumerate(narrative_rows):
        y = 0.78 - idx * 0.165
        ax.text(0.825, y + 0.06, title, ha="left", va="center", fontsize=7.2, color=PURPLE, weight="bold")
        ax.text(0.825, y, body, ha="left", va="center", fontsize=6.6, color=INK, linespacing=1.5)
        if idx < len(narrative_rows) - 1:
            ax.plot((0.825, 0.975), (y - 0.066, y - 0.066), color="#DDD7E5", linewidth=0.6)

    for y in (0.70, 0.30):
        ax.add_patch(FancyArrowPatch((0.215, y), (0.282, y), arrowstyle="-|>", mutation_scale=11, linewidth=1.2, color=NAVY, connectionstyle="arc3,rad=0"))
        ax.add_patch(FancyArrowPatch((0.718, y), (0.792, y), arrowstyle="-|>", mutation_scale=11, linewidth=1.2, color=PURPLE, connectionstyle="arc3,rad=0"))
    ax.text(0.248, 0.735, "复算" if zh else "RECALCULATE", ha="center", va="bottom", fontsize=6.3, color=NAVY, weight="bold")
    ax.text(0.755, 0.735, "引用" if zh else "CITE", ha="center", va="bottom", fontsize=6.3, color=PURPLE, weight="bold")

    legend = [("几何输入" if zh else "Geometry input", NAVY), ("已知指标" if zh else "Known metric", TEAL), ("未知指标" if zh else "Unknown metric", RED), ("正文解释" if zh else "Narrative evidence", PURPLE)]
    ax.text(0.00, 0.06, LANG[lang]["legend"], ha="left", va="center", fontsize=7.2, color=MUTED, weight="bold")
    for idx, (label, color) in enumerate(legend):
        x = 0.08 + idx * 0.16
        ax.add_patch(patches.Rectangle((x, 0.049), 0.018, 0.022, facecolor=color, edgecolor="none"))
        ax.text(x + 0.026, 0.06, label, ha="left", va="center", fontsize=6.5, color=INK)

    out = submission / "assets" / "figures" / ("metrics-evidence.png" if zh else "metrics-evidence.en.png")
    save_figure(fig, out)
    return out


def render_all(submission: Path) -> list[Path]:
    data = data_bundle(submission)
    renderers = [render_site_overview, render_key_areas, render_land_use, render_mobility, render_metrics]
    outputs: list[Path] = []
    for lang in ("zh", "en"):
        for renderer in renderers:
            outputs.append(renderer(submission, data, lang))
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--submission", type=Path, default=DEFAULT_SUBMISSION)
    args = parser.parse_args()
    submission = args.submission.resolve()
    outputs = render_all(submission)
    print(f"font={FONT_FAMILY} path={FONT_PATH}")
    for path in outputs:
        print(path.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
