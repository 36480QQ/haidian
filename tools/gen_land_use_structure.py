#!/usr/bin/env python3
"""Regenerate land-use-structure.{png,en.png,svg,en.svg} from geometry/land_use.geojson.

Root cause of the previously blank figure: the original gen_figures_boards.py
script was lost and the prior rendered file contained no patches. This script
re-draws the figure using the same visual style as its sibling key-areas.png
(black site-boundary outline + translucent fills + Chinese label + legend).

Writes both Chinese and English versions (PNG + SVG with font-as-path).
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "path"  # embed glyphs as paths to avoid missing-font risk
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon, Patch
from matplotlib.collections import PatchCollection
import matplotlib.font_manager as fm

PKG = Path("/Users/jiang/WorkBuddy/2026-08-18-19-29-41/haidian/submissions/kati-99/jingzhang-intelligence-loop")
HEITI = "/System/Library/Fonts/STHeiti Medium.ttc"
HEITI_FP = fm.FontProperties(fname=HEITI)
HEITI_NAME = HEITI_FP.get_name()
print("Heiti font:", HEITI_NAME)

# Land-use code -> (Chinese name, English name, fill color)
LU_MAP = {
    "0802": ("AI研发创新用地", "AI R&D Innovation", "#4F81BD"),
    "1401": ("公园绿地与开敞空间", "Park & Open Space", "#9BBB59"),
    "05":   ("产业服务与商业服务用地", "Industrial Services & Commercial", "#F79646"),
    "0702": ("社区服务与配套用地", "Community Services", "#8064A2"),
}
LEGEND_ORDER = ["0802", "1401", "05", "0702"]


def load_geojson(p):
    return json.load(open(p, encoding="utf-8"))


def ring_to_xy(ring):
    return [(c[0], c[1]) for c in ring]


def draw_figure(lang: str, out_png: Path, out_svg: Path):
    sb = load_geojson(PKG / "geometry/site_boundary.geojson")
    lu = load_geojson(PKG / "geometry/land_use.geojson")

    fig, ax = plt.subplots(figsize=(10, 10), dpi=100)

    # ---- 1) Site boundary as black outline ----
    boundary_patches = []
    boundary_coords = []
    for f in sb["features"]:
        g = f["geometry"]
        polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
        for poly in polys:
            for ring in poly:
                xy = ring_to_xy(ring)
                boundary_patches.append(MplPolygon(xy, closed=True))
                boundary_coords.extend(xy)
    ax.add_collection(
        PatchCollection(boundary_patches, facecolor="none",
                        edgecolor="#1F1F1F", linewidth=2.0)
    )

    # ---- 2) Land-use fills + centroid labels ----
    lu_patches = []
    lu_facecolors = []
    lu_labels = []
    for f in lu["features"]:
        props = f["properties"]
        code = props["land_use_code"]
        fill = LU_MAP.get(code, ("?", "?", "#CCCCCC"))[2]
        g = f["geometry"]
        polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
        for poly in polys:
            for ring in poly:
                xy = ring_to_xy(ring)
                lu_patches.append(MplPolygon(xy, closed=True))
                lu_facecolors.append(fill)
                cx = sum(p[0] for p in xy) / len(xy)
                cy = sum(p[1] for p in xy) / len(yy := xy)
                # area_ha
                area_sqm = props.get("area_sqm_declared", 0)
                area_ha = area_sqm / 10000.0
                label_name = LU_MAP.get(code, (props["name_zh"], props["name_zh"]))[0 if lang == "zh" else 1]
                lu_labels.append((cx, cy, code, label_name, area_ha))

    pc = PatchCollection(lu_patches, alpha=0.55,
                         edgecolor="#1F1F1F", linewidth=1.2)
    pc.set_facecolor(lu_facecolors)
    ax.add_collection(pc)

    # ---- 3) Per-feature labels (name + code + area) ----
    for cx, cy, code, name, area_ha in lu_labels:
        if lang == "zh":
            label = f"{name}\n{code}  {area_ha:.1f} ha"
            fontproperties = HEITI_FP
        else:
            label = f"{name}\n{code}  {area_ha:.1f} ha"
            fontproperties = None  # DejaVu default for English
        ax.text(cx, cy, label, ha="center", va="center", fontsize=9,
                fontproperties=fontproperties, color="#1F1F1F",
                bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                          edgecolor="none", alpha=0.78))

    # ---- 4) Extent & aspect ----
    xs = [c[0] for c in boundary_coords]
    ys = [c[1] for c in boundary_coords]
    xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)
    # NOTE: site_boundary extent is narrow in lon (0.0156°) and tall in lat
    # (0.0875°); with set_aspect("equal") the X axis would collapse, so we let
    # matplotlib render at true data aspect (each data unit maps 1:1 to axes).
    pad_x = (xmax - xmin) * 0.04
    pad_y = (ymax - ymin) * 0.04
    ax.set_xlim(xmin - pad_x, xmax + pad_x)
    ax.set_ylim(ymin - pad_y, ymax + pad_y)
    ax.set_aspect("auto")
    ax.set_xticks([]); ax.set_yticks([])

    # ---- 5) Title (top-left) & provisional tag (top-right) ----
    if lang == "zh":
        title_main = "用地结构 · Land Use Structure"
    else:
        # English version: bilingual title, but font unified to Heiti TC (which
        # supports both CJK and Latin) so no glyph fallback warning.
        title_main = "Land Use Structure · 用地结构"
    # Always render with Heiti TC to avoid any CJK glyph fallback to DejaVu.
    fig_title_font = HEITI_FP
    fig.text(0.06, 0.955, title_main, ha="left", va="top",
             fontsize=20, color="#1F1F1F", fontproperties=fig_title_font)
    fig.text(0.94, 0.955, "provisional · intake only",
             ha="right", va="top", fontsize=11, color="#888888")

    # ---- 6) Legend (bottom-left) ----
    handles = [
        Patch(facecolor=LU_MAP[c][2], alpha=0.55, edgecolor="#1F1F1F",
              label=f"{c} {LU_MAP[c][0 if lang=='zh' else 1]}")
        for c in LEGEND_ORDER
    ]
    ax.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.02, 0.02),
              fontsize=9, framealpha=0.88, prop=fig_title_font)

    # ---- 7) Bottom note ----
    note = "三层范围与空间工作框架图" if lang == "zh" else "Three-Layer Scope & Spatial Framework"
    fig.text(0.5, 0.025, note, ha="center", va="bottom",
             fontsize=9, color="#888888", fontproperties=fig_title_font)

    plt.subplots_adjust(left=0.04, right=0.96, top=0.92, bottom=0.08)
    fig.savefig(out_png, dpi=100, bbox_inches="tight", facecolor="white")
    fig.savefig(out_svg, dpi=100, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  written {out_png.name} ({out_png.stat().st_size} B) and {out_svg.name} ({out_svg.stat().st_size} B)")


if __name__ == "__main__":
    targets = [
        ("zh", PKG / "assets/figures/land-use-structure.png",
                PKG / "assets/figures/land-use-structure.svg"),
        ("en", PKG / "assets/figures/land-use-structure.en.png",
                PKG / "assets/figures/land-use-structure.en.svg"),
    ]
    for lang, png, svg in targets:
        draw_figure(lang, png, svg)
    print("done.")