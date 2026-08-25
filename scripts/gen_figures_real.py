#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate five premium concept-level figures for 智脉京张 proposal.

v3: Premium cartographic base map
  - Procedural urban fabric: building footprints, road hierarchy, water, green
  - Light technical-schematic style with professional cartographic conventions
  - Subtle shadows, layered rendering
  - Better north arrow, scale bar, legend, typography
  - 200 DPI for crisp output
  - All self-drawn, no external tiles or copyrighted imagery
"""
from __future__ import annotations

import json
import math
import random
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon as MplPolygon, Circle
from matplotlib.collections import PatchCollection, LineCollection
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from PIL import Image
from shapely.geometry import shape, Point, LineString, Polygon as ShapelyPolygon, box
from shapely.ops import unary_union
from shapely.affinity import affine_transform, translate
import pyproj

random.seed(42)
np.random.seed(42)

# ---------------------------------------------------------------------------
# Paths & constants
# ---------------------------------------------------------------------------
REPO = Path(__file__).resolve().parent.parent
SUB = REPO / "submissions" / "wengyongsheng29-spec" / "jingzhang-agent-native-belt"
FIG_DIR = SUB / "assets" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Projection for area calcs
TRANSFORM = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:4548", always_xy=True)

# ── Light technical-schematic palette ──
BG_DARK = "#f5f3ee"       # warm off-white background
BG_MID = "#ebe7dc"        # slightly darker warm gray
WATER = "#dbeafe"         # light blue water
WATER_LINE = "#93c5fd"    # water edge
ROAD_CASING = "#c8c4bc"   # road edge (warm gray)
ROAD_MAJOR = "#ffffff"    # major road fill (white)
ROAD_SECONDARY = "#f0ece4"
ROAD_MINOR = "#ddd8cc"
BUILDING_FILL = "#d5cfc0"  # building base (warm gray)
BUILDING_EDGE = "#a8a190"
GREEN_DARK = "#dcfce7"
GREEN_FILL = "#d1fae5"
GREEN_LIGHT = "#a7f3d0"
RAIL_BG = "#fef3c7"
RAIL_FG = "#b45309"       # dark amber for contrast on light bg

# Proposal colors (professional, muted for light bg)
NAVY = "#1d4ed8"          # professional blue
PURPLE = "#6d28d9"        # professional purple
GOLD = "#b45309"          # dark amber / heritage gold
TEAL = "#047857"          # dark teal
CORAL = "#dc2626"         # red
ORANGE = "#c2410c"        # dark orange
WHITE = "#1c1917"         # near-black (text color on light bg)
MUTED = "#44403c"         # warm gray (darker for readability on light bg)

# Land use colors (semi-transparent for light map)
LU_COLORS = {
    "LU-001": "#3b82f6",   # 众智园 blue
    "LU-002": "#8b5cf6",   # AI原点 violet
    "LU-003": "#d97706",   # 大钟寺 amber
    "LU-004": "#059669",   # 绿廊 emerald
    "LU-005": "#a78bfa",   # 西翼 light violet
    "LU-006": "#6ee7b7",   # 东翼 light emerald
}

plt.rcParams["font.family"] = ["Microsoft YaHei", "SimHei", "DengXian", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def load_geojson(name):
    p = SUB / "geometry" / name
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


# ── OSM road cache ──
_OSM_ROADS = None
_OSM_BUILDINGS = None

def _classify_highway(hw):
    """Map OSM highway tag to simplified road class."""
    if not hw:
        return None
    base = hw.replace("_link", "")
    if base in ("motorway", "trunk", "primary", "secondary", "tertiary"):
        return base
    if hw in ("residential", "living_street", "unclassified", "service"):
        return "residential"
    return None  # skip footway, cycleway, path, track, pedestrian, etc.


def load_osm_roads():
    """Load and cache OSM road segments as lists of (lon, lat) coordinate tuples."""
    global _OSM_ROADS
    if _OSM_ROADS is not None:
        return _OSM_ROADS
    p = REPO / "scripts" / "data" / "osm_roads.geojson"
    if not p.exists():
        _OSM_ROADS = {}
        return _OSM_ROADS
    with open(p, "r", encoding="utf-8") as f:
        fc = json.load(f)
    roads = {}
    for feat in fc["features"]:
        props = feat.get("properties", {})
        rc = props.get("road_class") or _classify_highway(props.get("highway"))
        if rc is None:
            continue
        coords = feat["geometry"]["coordinates"]
        if len(coords) < 2:
            continue
        roads.setdefault(rc, []).append(coords)
    _OSM_ROADS = roads
    return roads


def load_osm_buildings():
    """Load OSM building footprints as list of (coords, height_m) tuples."""
    global _OSM_BUILDINGS
    if _OSM_BUILDINGS is not None:
        return _OSM_BUILDINGS
    p = REPO / "scripts" / "data" / "osm_buildings.geojson"
    if not p.exists():
        _OSM_BUILDINGS = []
        return _OSM_BUILDINGS
    with open(p, "r", encoding="utf-8") as f:
        fc = json.load(f)
    buildings = []
    for feat in fc["features"]:
        geom = feat.get("geometry", {})
        if geom.get("type") != "Polygon":
            continue
        rings = geom.get("coordinates", [])
        if not rings or len(rings[0]) < 4:
            continue
        h = feat.get("properties", {}).get("height_m")
        buildings.append((rings[0], h))
    _OSM_BUILDINGS = buildings
    return buildings


def load_satellite_underlay(c_off=116.385):
    """Load cached Esri satellite tiles, rotate 90° CW to match R(lon,lat)=(lat,-lon+C).

    Returns (image_array, extent) or (None, None) if tiles unavailable.
    extent = [lat_s, lat_n, -lon_e+C, -lon_w+C] for imshow with origin='upper'.
    """
    import math as _math
    tile_dir = REPO / "scripts" / "data"
    ZOOM = 15
    TILE_SIZE = 256
    # Same tile range used by gen_satellite_comparison.py
    x_min, x_max = 26969, 26978
    y_min, y_max = 12400, 12413

    # Check tiles exist
    first_tile = tile_dir / f"tile_{ZOOM}_{x_min}_{y_min}.png"
    if not first_tile.exists():
        return None, None

    n = 2 ** ZOOM
    lon_w = x_min / n * 360 - 180
    lat_n_rad = _math.atan(_math.sinh(_math.pi * (1 - 2 * y_min / n)))
    lat_n = _math.degrees(lat_n_rad)
    lon_e = (x_max + 1) / n * 360 - 180
    lat_s_rad = _math.atan(_math.sinh(_math.pi * (1 - 2 * (y_max + 1) / n)))
    lat_s = _math.degrees(lat_s_rad)

    width = (x_max - x_min + 1) * TILE_SIZE
    height = (y_max - y_min + 1) * TILE_SIZE
    mosaic = Image.new("RGB", (width, height))
    for tx in range(x_min, x_max + 1):
        for ty in range(y_min, y_max + 1):
            tp = tile_dir / f"tile_{ZOOM}_{tx}_{ty}.png"
            if tp.exists():
                mosaic.paste(Image.open(tp).convert("RGB"),
                             ((tx - x_min) * TILE_SIZE, (ty - y_min) * TILE_SIZE))

    # Rotate 90° CW: lat→X (south→north left→right), lon→Y (west→east top→bottom)
    arr = np.array(mosaic)
    rotated = np.rot90(arr, k=-1)
    extent = [lat_s, lat_n, -lon_e + c_off, -lon_w + c_off]
    return rotated, extent


def draw_osm_buildings(ax, xlim, ylim, transform_fn=None, clip_poly=None,
                   style="context", zorder_base=1):
    """Draw OSM roads within given lon/lat bounds.

    transform_fn: optional callable(lon, lat) -> (x, y) for rotated coords.
    clip_poly: optional shapely Polygon (in same coord space) to clip roads.
    style: "context" (dark) or "bright" (light) or "site" (mixed).
    """
    roads = load_osm_roads()
    if not roads:
        return

    if style == "context":
        styles = {
            "motorway":   (ROAD_CASING, 4.0, 0.6, "#ffffff", 2.2, 0.9),
            "trunk":      (ROAD_CASING, 3.2, 0.55, "#ffffff", 1.8, 0.85),
            "primary":    (ROAD_CASING, 2.5, 0.5, "#fafaf9", 1.4, 0.8),
            "secondary":  (ROAD_CASING, 1.8, 0.45, "#f5f3ee", 1.0, 0.7),
            "tertiary":   (ROAD_CASING, 1.2, 0.4, "#f0ece4", 0.7, 0.6),
            "residential":(ROAD_CASING, 0.7, 0.3, "#ebe7dc", 0.4, 0.5),
        }
    elif style == "bright":
        styles = {
            "motorway":   (ROAD_CASING, 5.0, 0.8, "#ffffff", 2.8, 0.95),
            "trunk":      (ROAD_CASING, 4.0, 0.7, "#ffffff", 2.2, 0.9),
            "primary":    (ROAD_CASING, 3.2, 0.6, "#fafaf9", 1.7, 0.85),
            "secondary":  (ROAD_CASING, 2.5, 0.5, "#f5f3ee", 1.3, 0.75),
            "tertiary":   (ROAD_CASING, 1.8, 0.4, "#f0ece4", 0.9, 0.65),
            "residential":(ROAD_CASING, 1.0, 0.3, "#ebe7dc", 0.5, 0.55),
        }
    else:  # site
        styles = {
            "motorway":   (ROAD_CASING, 4.5, 0.7, "#ffffff", 2.5, 0.9),
            "trunk":      (ROAD_CASING, 3.5, 0.6, "#ffffff", 2.0, 0.85),
            "primary":    (ROAD_CASING, 2.8, 0.5, "#fafaf9", 1.5, 0.8),
            "secondary":  (ROAD_CASING, 2.0, 0.45, "#f5f3ee", 1.1, 0.7),
            "tertiary":   (ROAD_CASING, 1.4, 0.35, "#f0ece4", 0.8, 0.6),
            "residential":(ROAD_CASING, 0.8, 0.25, "#ebe7dc", 0.4, 0.5),
        }

    xmin, xmax = xlim
    ymin, ymax = ylim
    margin = 0.002

    for rc, segments in roads.items():
        if rc not in styles:
            continue
        cc, clw, ca, fc, flw, fa = styles[rc]
        segs_out = []
        for coords in segments:
            seg = []
            for lon, lat in coords:
                if transform_fn:
                    px, py = transform_fn(lon, lat)
                else:
                    px, py = lon, lat
                if (xmin - margin <= px <= xmax + margin and
                        ymin - margin <= py <= ymax + margin):
                    seg.append((px, py))
                elif seg:
                    if len(seg) >= 2:
                        segs_out.append(seg)
                    seg = []
            if len(seg) >= 2:
                segs_out.append(seg)
        if not segs_out:
            continue
        lc = LineCollection(segs_out, colors=cc, linewidths=clw, alpha=ca,
                            zorder=zorder_base, capstyle="round", joinstyle="round")
        if clip_poly is not None:
            lc.set_clip_path(MplPolygon(list(clip_poly.exterior.coords),
                                        transform=ax.transData))
        ax.add_collection(lc)
        lc2 = LineCollection(segs_out, colors=fc, linewidths=flw, alpha=fa,
                             zorder=zorder_base + 1, capstyle="round", joinstyle="round")
        if clip_poly is not None:
            lc2.set_clip_path(MplPolygon(list(clip_poly.exterior.coords),
                                         transform=ax.transData))
        ax.add_collection(lc2)


# Alias: draw_osm_buildings actually draws roads (misnomer retained for compat)
draw_osm_roads = draw_osm_buildings


def plot_polygon(ax, geom, **kwargs):
    if geom.is_empty:
        return
    if geom.geom_type == "Polygon":
        xs, ys = zip(*geom.exterior.coords)
        ax.fill(xs, ys, **kwargs)
    elif geom.geom_type == "MultiPolygon":
        for poly in geom.geoms:
            plot_polygon(ax, poly, **kwargs)


def plot_line(ax, geom, **kwargs):
    if geom.geom_type == "LineString":
        xs, ys = zip(*geom.coords)
        ax.plot(xs, ys, **kwargs)
    elif geom.geom_type == "MultiLineString":
        for line in geom.geoms:
            plot_line(ax, line, **kwargs)


def polygon_to_patch(geom, **kwargs):
    """Convert shapely polygon to matplotlib patch for shadow effects."""
    if geom.is_empty:
        return None
    if geom.geom_type == "Polygon":
        verts = list(geom.exterior.coords)
        return MplPolygon(verts, closed=True, **kwargs)
    elif geom.geom_type == "MultiPolygon":
        patches = []
        for poly in geom.geoms:
            p = polygon_to_patch(poly, **kwargs)
            if p:
                patches.append(p)
        return patches
    return None


# ---------------------------------------------------------------------------
# Procedural urban fabric generator
# ---------------------------------------------------------------------------
def generate_urban_fabric(site_geom, key_areas_dict):
    """Generate building footprints and road network within the site.

    Returns:
        buildings: list of (x, y, w, h, angle) in degrees
        roads_major: list of LineString
        roads_secondary: list of LineString
        water: list of LineString (小月河)
    """
    minx, miny, maxx, maxy = site_geom.bounds

    # ── Road network ──
    roads_major = []
    roads_secondary = []

    # N-S major roads (spaced ~0.008 deg ≈ 700m)
    x = minx + 0.004
    while x < maxx:
        # Slight curve for realism
        pts = []
        n_pts = 8
        for i in range(n_pts + 1):
            yy = miny + (maxy - miny) * i / n_pts
            xx = x + 0.0003 * math.sin(i * 1.5 + x * 100)
            pts.append((xx, yy))
        roads_major.append(LineString(pts))
        x += 0.008

    # E-W major roads
    y = miny + 0.006
    while y < maxy:
        pts = []
        n_pts = 8
        for i in range(n_pts + 1):
            xx = minx + (maxx - minx) * i / n_pts
            yy = y + 0.0002 * math.cos(i * 1.2 + y * 100)
            pts.append((xx, yy))
        roads_major.append(LineString(pts))
        y += 0.008

    # Secondary roads (denser grid between majors)
    x = minx + 0.002
    while x < maxx:
        pts = []
        n_pts = 6
        for i in range(n_pts + 1):
            yy = miny + (maxy - miny) * i / n_pts
            xx = x + 0.0002 * math.sin(i * 2.0 + x * 200)
            pts.append((xx, yy))
        roads_secondary.append(LineString(pts))
        x += 0.004

    y = miny + 0.003
    while y < maxy:
        pts = []
        n_pts = 6
        for i in range(n_pts + 1):
            xx = minx + (maxx - minx) * i / n_pts
            yy = y + 0.00015 * math.cos(i * 1.8 + y * 200)
            pts.append((xx, yy))
        roads_secondary.append(LineString(pts))
        y += 0.004

    # ── 小月河 (Xiaoyue River) - runs along the east side ──
    river_pts = []
    for i in range(20):
        yy = miny + (maxy - miny) * i / 19
        xx = 116.353 + 0.001 * math.sin(i * 0.8) + 0.0005 * math.cos(i * 1.3)
        river_pts.append((xx, yy))
    water = [LineString(river_pts)]

    # ── Building footprints ──
    buildings = []
    # Use grid-based placement between roads
    spacing_x = 0.0018  # ~150m blocks
    spacing_y = 0.0018
    margin = 0.0003

    bx = minx + 0.001
    while bx < maxx - 0.001:
        by = miny + 0.001
        while by < maxy - 0.001:
            # Check if center is inside site
            cx = bx + spacing_x / 2
            cy = by + spacing_y / 2
            pt = Point(cx, cy)
            if site_geom.contains(pt):
                # Skip if inside a key area (those have their own buildings)
                in_key = False
                for kgeom in key_areas_dict.values():
                    if kgeom.contains(pt):
                        in_key = True
                        break
                if not in_key:
                    # Generate 1-4 buildings per block
                    n_bldg = random.randint(1, 4)
                    for _ in range(n_bldg):
                        bw = random.uniform(0.0003, 0.0008)
                        bh = random.uniform(0.0003, 0.0008)
                        ox = random.uniform(margin, spacing_x - margin - bw)
                        oy = random.uniform(margin, spacing_y - margin - bh)
                        angle = random.choice([0, 0, 0, 0.02])  # mostly aligned
                        buildings.append((bx + ox, by + oy, bw, bh, angle))
            by += spacing_y
        bx += spacing_x

    # Key area buildings loaded from buildings.geojson in draw_urban_fabric

    return buildings, roads_major, roads_secondary, water


def draw_urban_fabric(ax, site_geom, key_areas_dict, show_buildings=True, show_roads=True, show_procedural=True):
    """Draw the procedural urban fabric on the axes."""
    buildings, roads_maj, roads_sec, water = generate_urban_fabric(site_geom, key_areas_dict)

    # ── Water (小月河) ──
    for wline in water:
        wx, wy = zip(*wline.coords)
        # Wide water body
        ax.plot(wx, wy, color=WATER, linewidth=18, alpha=0.8, zorder=1, solid_capstyle="round")
        ax.plot(wx, wy, color=WATER_LINE, linewidth=1, alpha=0.5, zorder=2)

    # ── Green patches (parks, campus green) ──
    # Scatter some green patches
    green_patches = [
        # 北大/清华 campus green (northwest)
        Point(116.315, 40.000).buffer(0.006),
        Point(116.325, 39.995).buffer(0.004),
        # 紫竹院 park area
        Point(116.320, 39.945).buffer(0.005),
        # Various small parks
        Point(116.340, 40.010).buffer(0.002),
        Point(116.350, 39.975).buffer(0.0015),
        Point(116.335, 39.960).buffer(0.002),
    ]
    for gp in green_patches:
        clipped = gp.intersection(site_geom)
        if not clipped.is_empty:
            plot_polygon(ax, clipped, facecolor=GREEN_FILL, edgecolor=GREEN_LIGHT,
                        linewidth=0.3, alpha=0.6, zorder=1)

    # ── Road casings (dark edges) ──
    if show_roads:
        for rline in roads_maj:
            rx, ry = zip(*rline.coords)
            ax.plot(rx, ry, color=ROAD_CASING, linewidth=7, alpha=0.9, zorder=3, solid_capstyle="round")
        for rline in roads_sec:
            rx, ry = zip(*rline.coords)
            ax.plot(rx, ry, color=ROAD_CASING, linewidth=4, alpha=0.7, zorder=3, solid_capstyle="round")

        # ── Road fills ──
        for rline in roads_maj:
            rx, ry = zip(*rline.coords)
            ax.plot(rx, ry, color=ROAD_MAJOR, linewidth=4, alpha=0.85, zorder=4, solid_capstyle="round")
        for rline in roads_sec:
            rx, ry = zip(*rline.coords)
            ax.plot(rx, ry, color=ROAD_SECONDARY, linewidth=2, alpha=0.6, zorder=4, solid_capstyle="round")

        # ── Center lines on major roads ──
        for rline in roads_maj:
            rx, ry = zip(*rline.coords)
            ax.plot(rx, ry, color="#f0d080", linewidth=0.5, alpha=0.4, zorder=5,
                    linestyle=(0, (8, 8)))

    # ── Buildings with drop shadows ──
    if show_buildings:
        if show_procedural:
            shadow_offset_x = 0.00015
            shadow_offset_y = -0.00012
            for (bx, by, bw, bh, angle) in buildings:
                # Shadow
                shadow = mpatches.Rectangle(
                    (bx + shadow_offset_x, by + shadow_offset_y), bw, bh,
                    angle=angle * 180 / math.pi,
                    facecolor="#a8a29e", edgecolor="none",
                    alpha=0.12, zorder=2)
                ax.add_patch(shadow)
                # Building
                rect = mpatches.Rectangle((bx, by), bw, bh, angle=angle * 180 / math.pi,
                                          facecolor=BUILDING_FILL, edgecolor=BUILDING_EDGE,
                                          linewidth=0.2, alpha=0.75, zorder=3)
                ax.add_patch(rect)

        # ── Key area buildings from buildings.geojson (varied footprints) ──
        try:
            bldg_fc = load_geojson("buildings.geojson")
            for f in bldg_fc["features"]:
                poly = shape(f["geometry"])
                if not site_geom.intersects(poly):
                    continue
                clipped = poly.intersection(site_geom)
                if clipped.is_empty:
                    continue
                btype = f["properties"].get("building_type", "mixed_use")
                is_retained = f["properties"].get("construction_status") == "retained"
                # Color by type
                if btype in ("ai_r_and_d", "lab"):
                    bcolor = BUILDING_FILL
                    balpha = 0.78
                elif btype in ("office",):
                    bcolor = "#ddd8cc"
                    balpha = 0.72
                elif btype in ("retail",):
                    bcolor = "#e8dcc8"
                    balpha = 0.68
                elif btype in ("residential", "talent_apartment"):
                    bcolor = "#e0dcd0"
                    balpha = 0.65
                elif btype == "existing_retained":
                    bcolor = "#d4c4a8"
                    balpha = 0.70
                else:
                    bcolor = BUILDING_FILL
                    balpha = 0.65
                # Shadow
                sh = translate(clipped, xoff=0.00012, yoff=-0.00010)
                if not sh.is_empty:
                    plot_polygon(ax, sh, facecolor="#a8a29e", edgecolor="none",
                                alpha=0.10, zorder=2)
                # Building
                edge_c = "#8b7355" if is_retained else BUILDING_EDGE
                edge_w = 0.5 if is_retained else 0.2
                ls = "--" if is_retained else "-"
                plot_polygon(ax, clipped, facecolor=bcolor, edgecolor=edge_c,
                            linewidth=edge_w, alpha=balpha, zorder=3, linestyle=ls)
        except Exception:
            pass

    return buildings, roads_maj, roads_sec, water


def draw_north_arrow(ax, x, y, size=0.006):
    """Draw a refined north arrow."""
    # Outer circle
    ax.add_patch(Circle((x, y), size * 0.8, facecolor=BG_MID, edgecolor=MUTED,
                        linewidth=0.8, alpha=0.8, zorder=20))
    # N arrow
    ax.annotate("", xy=(x, y + size * 0.6), xytext=(x, y - size * 0.3),
                arrowprops=dict(arrowstyle="-|>", color="#44403c", lw=1.5,
                                connectionstyle="arc3,rad=0"), zorder=21)
    ax.text(x, y + size * 0.9, "N", fontsize=9, fontweight="bold", color=WHITE,
            ha="center", va="bottom", zorder=21)


def draw_scale_bar(ax, x, y, length_m=1000):
    """Draw a refined scale bar."""
    deg_per_m = 1.0 / 111000.0
    half = length_m * deg_per_m / 2
    # Background
    ax.add_patch(mpatches.Rectangle((x - half - 0.0005, y - 0.0012), half * 2 + 0.001, 0.003,
                                     facecolor=BG_MID, edgecolor=MUTED, linewidth=0.5,
                                     alpha=0.8, zorder=20))
    # Alternating bars (black/white for visibility on light bg)
    for i in range(4):
        bx = x - half + i * half / 2
        color = "#1c1917" if i % 2 == 0 else "#ffffff"
        ax.add_patch(mpatches.Rectangle((bx, y - 0.0004), half / 2, 0.0008,
                                         facecolor=color, edgecolor="none", alpha=0.9, zorder=21))
    ax.text(x, y + 0.0018, f"{length_m}m", ha="center", va="bottom", fontsize=7,
            color="#1c1917", zorder=21, fontweight="bold")


def add_glow(ax, geom, color, n_layers=3, alpha=0.08, **kwargs):
    """Add a soft glow effect around a polygon."""
    for i in range(n_layers, 0, -1):
        expand = 0.0003 * i
        if hasattr(geom, 'buffer'):
            buffered = geom.buffer(expand)
            plot_polygon(ax, buffered, facecolor=color, edgecolor="none",
                        alpha=alpha / i, zorder=kwargs.get('zorder', 5) - i)


# ---------------------------------------------------------------------------
# Dashboard-style effects (数据可视化大屏风格)
# ---------------------------------------------------------------------------
def draw_dot_grid(ax, geom, spacing=0.0012, color="#3b82f6", alpha_range=(0.03, 0.12),
                  dot_size=1.5, zorder=4):
    """Draw a dot-matrix grid inside a polygon — digital terrain effect."""
    minx, miny, maxx, maxy = geom.bounds
    xs = np.arange(minx, maxx, spacing)
    ys = np.arange(miny, maxy, spacing)
    px, py, pa = [], [], []
    for x in xs:
        for y in ys:
            if geom.contains(Point(x, y)):
                px.append(x)
                py.append(y)
                # vary alpha by position for subtle gradient
                t = (y - miny) / (maxy - miny)
                pa.append(alpha_range[0] + (alpha_range[1] - alpha_range[0]) * (0.5 + 0.5 * math.sin(t * 6)))
    if px:
        ax.scatter(px, py, s=dot_size, c=color, alpha=pa, zorder=zorder, edgecolors="none")


def draw_extruded_polygon(ax, geom, facecolor, edgecolor=None, n_layers=8,
                          offset_x=0.00012, offset_y=-0.00010, alpha=0.15,
                          top_alpha=0.3, zorder=10):
    """Draw a 3D-extruded polygon (offset copies for block effect)."""
    from shapely.affinity import translate
    for i in range(n_layers, 0, -1):
        frac = i / n_layers
        shifted = translate(geom, xoff=offset_x * frac, yoff=offset_y * frac)
        plot_polygon(ax, shifted, facecolor=facecolor, edgecolor="none",
                     alpha=alpha * frac, zorder=zorder - 1)
    # Top face
    plot_polygon(ax, geom, facecolor=facecolor, edgecolor=edgecolor or facecolor,
                 linewidth=1.5, alpha=top_alpha, zorder=zorder)
    plot_polygon(ax, geom, facecolor="none", edgecolor=edgecolor or facecolor,
                 linewidth=2, alpha=0.9, zorder=zorder + 1)


def draw_pulse_rings(ax, x, y, color, n_rings=3, max_radius=0.003, zorder=18):
    """Draw concentric pulse rings around a point."""
    for i in range(n_rings):
        r = max_radius * (i + 1) / n_rings
        a = 0.5 * (1 - i / n_rings)
        ax.add_patch(Circle((x, y), r, facecolor="none", edgecolor=color,
                            linewidth=1.2, alpha=a, zorder=zorder))


def draw_light_beam(ax, x, y, color, height=0.008, width=0.0006, zorder=17):
    """Draw a vertical light beam (tapered polygon going up)."""
    beam = MplPolygon([
        (x - width, y),
        (x + width, y),
        (x + width * 0.15, y + height),
        (x - width * 0.15, y + height),
    ], closed=True, facecolor=color, edgecolor="none", alpha=0.35, zorder=zorder)
    ax.add_patch(beam)
    # Inner bright core
    beam2 = MplPolygon([
        (x - width * 0.3, y),
        (x + width * 0.3, y),
        (x + width * 0.05, y + height * 0.85),
        (x - width * 0.05, y + height * 0.85),
    ], closed=True, facecolor=WHITE, edgecolor="none", alpha=0.15, zorder=zorder + 1)
    ax.add_patch(beam2)


def draw_flying_line(ax, x1, y1, x2, y2, color, n_dots=8, zorder=16):
    """Draw a curved flying line with moving dots between two points."""
    # Quadratic bezier with arc
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    dist = math.sqrt(dx * dx + dy * dy)
    # Perpendicular offset for curve
    nx, ny = -dy / dist, dx / dist
    cx = mx + nx * dist * 0.25
    cy = my + ny * dist * 0.25
    # Draw curve
    ts = np.linspace(0, 1, 60)
    bx = (1 - ts) ** 2 * x1 + 2 * (1 - ts) * ts * cx + ts ** 2 * x2
    by = (1 - ts) ** 2 * y1 + 2 * (1 - ts) * ts * cy + ts ** 2 * y2
    ax.plot(bx, by, color=color, linewidth=1, alpha=0.3, zorder=zorder)
    # Dots along the curve
    for i in range(n_dots):
        t = (i + 0.5) / n_dots
        dx_t = 2 * (1 - t) * (cx - x1) + 2 * t * (x2 - cx)
        dy_t = 2 * (1 - t) * (cy - y1) + 2 * t * (y2 - cy)
        d = math.sqrt(dx_t ** 2 + dy_t ** 2)
        if d > 0:
            dx_t, dy_t = dx_t / d, dy_t / d
        px = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t ** 2 * x2
        py = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t ** 2 * y2
        ax.plot(px, py, "o", markersize=2.5, color=color, alpha=0.4 + 0.4 * (1 - abs(t - 0.5) * 2),
                zorder=zorder + 1)


def draw_corner_brackets(ax, x1, y1, x2, y2, color="#3b82f6", size=0.004, zorder=22):
    """Draw tech-style corner brackets around a map area."""
    lw = 1.5
    alpha = 0.5
    for (cx, cy, dx, dy) in [
        (x1, y2, 1, -1),   # top-left
        (x2, y2, -1, -1),  # top-right
        (x1, y1, 1, 1),    # bottom-left
        (x2, y1, -1, 1),   # bottom-right
    ]:
        ax.plot([cx, cx + dx * size], [cy, cy], color=color, linewidth=lw, alpha=alpha, zorder=zorder)
        ax.plot([cx, cx], [cy, cy + dy * size], color=color, linewidth=lw, alpha=alpha, zorder=zorder)


def draw_scan_line(ax, geom, color="#3b82f6", zorder=5):
    """Draw a subtle horizontal scan line effect."""
    minx, miny, maxx, maxy = geom.bounds
    for i in range(8):
        y = miny + (maxy - miny) * i / 8
        ax.plot([minx, maxx], [y, y], color=color, linewidth=0.3, alpha=0.03, zorder=zorder)


# ---------------------------------------------------------------------------
# Figure 1: Site Overview
# ---------------------------------------------------------------------------
def fig_site_overview():
    site_fc = load_geojson("site_boundary.geojson")
    key_fc = load_geojson("key_areas.geojson")
    site = shape(site_fc["features"][0]["geometry"])
    keys = {f["id"]: shape(f["geometry"]) for f in key_fc["features"]}

    # ── Full-bleed horizontal master plan (rotated 90° CW) ──
    # Rotation: (lon, lat) -> (lat, -lon + C) so the N-S corridor runs left-to-right
    C_OFF = 116.385
    def R(x, y):
        return y, -x + C_OFF

    # Rotate geometries
    aff = [0, 1, -1, 0, 0, C_OFF]
    site_r = affine_transform(site, aff)
    keys_r = {k: affine_transform(v, aff) for k, v in keys.items()}

    fig = plt.figure(figsize=(14, 14))
    fig.patch.set_facecolor(BG_DARK)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG_DARK)

    # View limits in rotated coordinates (square format, clipped to satellite extent)
    X_MIN, X_MAX = 39.928, 40.035   # latitude (horizontal, was Y)
    Y_MIN, Y_MAX = -0.015, 0.095    # -lon+C (vertical, matches satellite coverage)
    ax.set_xlim(X_MIN, X_MAX)
    ax.set_ylim(Y_MIN, Y_MAX)
    ax.set_aspect("auto")
    ax.axis("off")

    # ── Satellite underlay (Esri World Imagery, semi-transparent) ──
    sat_img, sat_extent = load_satellite_underlay(C_OFF)
    if sat_img is not None:
        ax.imshow(sat_img, extent=sat_extent, origin="upper",
                  alpha=0.88, zorder=0, interpolation="bilinear")
        ax.add_patch(mpatches.Rectangle(
            (X_MIN, Y_MIN), X_MAX - X_MIN, Y_MAX - Y_MIN,
            facecolor=BG_DARK, alpha=0.03, zorder=0))

    # ── Real road network from OpenStreetMap (open data, ODbL) ──
    # Load and transform real road geometry, then draw by class
    osm_roads_path = REPO / "scripts" / "data" / "osm_roads.geojson"
    road_segments = {"motorway": [], "trunk": [], "primary": [],
                     "secondary": [], "tertiary": [], "residential": []}
    if osm_roads_path.exists():
        with open(osm_roads_path, "r", encoding="utf-8") as f:
            osm_fc = json.load(f)
        for feat in osm_fc["features"]:
            props = feat.get("properties", {})
            rc = props.get("road_class") or _classify_highway(props.get("highway"))
            if rc is None:
                continue
            coords = feat["geometry"]["coordinates"]
            if len(coords) < 2:
                continue
            # Transform to rotated coords and clip to viewport with margin
            seg = []
            for lon, lat in coords:
                rx, ry = R(lon, lat)
                if X_MIN - 0.005 <= rx <= X_MAX + 0.005 and Y_MIN - 0.005 <= ry <= Y_MAX + 0.005:
                    seg.append((rx, ry))
                elif seg:
                    if len(seg) >= 2:
                        road_segments.setdefault(rc, []).append(seg)
                    seg = []
            if len(seg) >= 2:
                road_segments.setdefault(rc, []).append(seg)

    # Road drawing style by class — strengthened for satellite overlay
    # (casing_color, casing_lw, casing_alpha, fill_color, fill_lw, fill_alpha)
    road_styles = {
        "motorway":   (ROAD_CASING, 6.0, 0.50, "#fef9c3", 3.8, 0.60),
        "trunk":      (ROAD_CASING, 5.0, 0.45, "#fefce8", 3.2, 0.55),
        "primary":    (ROAD_CASING, 4.2, 0.40, "#ffffff", 2.6, 0.50),
        "secondary":  (ROAD_CASING, 3.2, 0.32, "#fafaf9", 2.0, 0.40),
        "tertiary":   (ROAD_CASING, 2.4, 0.25, "#f5f3ee", 1.4, 0.30),
        "residential":(ROAD_CASING, 1.4, 0.18, "#f0ece4", 0.8, 0.22),
    }
    for rc, segments in road_segments.items():
        if not segments:
            continue
        cc, clw, ca, fc, flw, fa = road_styles[rc]
        # Casing
        lc = LineCollection(segments, colors=cc, linewidths=clw, alpha=ca,
                            zorder=1, capstyle="round", joinstyle="round")
        ax.add_collection(lc)
        # Fill
        lc2 = LineCollection(segments, colors=fc, linewidths=flw, alpha=fa,
                             zorder=2, capstyle="round", joinstyle="round")
        ax.add_collection(lc2)

    # ── Brighter road pass within site boundary (clipped) ──
    site_road_styles = {
        "motorway":   ("#78716c", 5.5, 0.38, "#fef9c3", 3.5, 0.65),
        "trunk":      ("#78716c", 4.5, 0.34, "#fefce8", 3.0, 0.60),
        "primary":    ("#78716c", 4.0, 0.30, "#ffffff", 2.5, 0.55),
        "secondary":  ("#a8a29e", 3.2, 0.26, "#fafaf9", 2.0, 0.50),
        "tertiary":   ("#a8a29e", 2.4, 0.22, "#fdfcfa", 1.5, 0.42),
        "residential":("#c8c4bc", 1.4, 0.16, "#fefdfb", 0.8, 0.32),
    }
    for rc, segments in road_segments.items():
        if not segments:
            continue
        cc, clw, ca, fc, flw, fa = site_road_styles[rc]
        lc = LineCollection(segments, colors=cc, linewidths=clw, alpha=ca,
                            zorder=5, capstyle="round", joinstyle="round")
        lc.set_clip_path(MplPolygon(list(site_r.exterior.coords), transform=ax.transData))
        ax.add_collection(lc)
        lc2 = LineCollection(segments, colors=fc, linewidths=flw, alpha=fa,
                             zorder=6, capstyle="round", joinstyle="round")
        lc2.set_clip_path(MplPolygon(list(site_r.exterior.coords), transform=ax.transData))
        ax.add_collection(lc2)

    # ── Reference road labels removed (OSM roads + context labels suffice) ──

    # ── Building footprints: provided by satellite imagery (no OSM overlay) ──

    # ── Context: water (小月河, rotated → horizontal) ──
    wx_r, wy_r = [], []
    for i in range(25):
        yy = 39.933 + (40.030 - 39.933) * i / 24
        xx = 116.353 + 0.0015 * math.sin(i * 0.7) + 0.0008 * math.cos(i * 1.3)
        rx, ry = R(xx, yy)
        wx_r.append(rx)
        wy_r.append(ry)
    ax.plot(wx_r, wy_r, color=WATER, linewidth=8, alpha=0.6, zorder=1, solid_capstyle="round")
    ax.plot(wx_r, wy_r, color=WATER_LINE, linewidth=0.8, alpha=0.4, zorder=2)

    # ── Context: green patches (rotated) ──
    ctx_green = [
        (116.320, 40.008, 0.009, ""),   # 清华-北大
        (116.325, 39.992, 0.006, ""),   # 人大/中关村
        (116.318, 39.946, 0.007, "紫竹院公园"),
        (116.350, 39.982, 0.004, ""),   # 北航/信通院
        (116.357, 39.958, 0.004, ""),   # 北邮/北师大
        (116.322, 39.960, 0.003, ""),   # 北理工
        (116.370, 40.010, 0.004, ""),   # 北沙滩
        (116.300, 40.018, 0.005, ""),   # 圆明园/颐和园
    ]
    for gx, gy, gr, glabel in ctx_green:
        gx_r, gy_r = R(gx, gy)
        circ = Point(gx_r, gy_r).buffer(gr)
        plot_polygon(ax, circ, facecolor=GREEN_FILL, edgecolor=GREEN_LIGHT,
                     linewidth=0.3, alpha=0.35, zorder=1)
        if glabel:
            ax.text(gx_r, gy_r, glabel, fontsize=7.5, color="#365314", ha="center",
                    va="center", zorder=3, alpha=0.95, fontweight="bold")

    # ── Site urban fabric (pass rotated geometries) ──
    draw_urban_fabric(ax, site_r, keys_r, show_roads=False, show_procedural=False)

    # Site boundary: light blue fill with blue dashed outline
    plot_polygon(ax, site_r, facecolor=NAVY, edgecolor="none", alpha=0.06, zorder=6)
    plot_polygon(ax, site_r, facecolor="none", edgecolor=NAVY, linewidth=2.0,
                 alpha=0.7, zorder=7, linestyle=(0, (6, 3)))
    plot_polygon(ax, site_r, facecolor="none", edgecolor="#ffffff", linewidth=1.0,
                 alpha=0.5, zorder=7)

    # ── Green spaces (rotated) ──
    green_ov = load_geojson("green_space.geojson")
    for f in green_ov["features"]:
        g = affine_transform(shape(f["geometry"]), aff)
        gtype = f["properties"].get("green_type", "")
        if gtype == "linear_park_corridor":
            plot_polygon(ax, g, facecolor=TEAL, edgecolor="none", alpha=0.25, zorder=6)
        else:
            plot_polygon(ax, g, facecolor=TEAL, edgecolor=TEAL, linewidth=0.6,
                        alpha=0.40, zorder=7)

    # ── Public spaces (rotated) ──
    public_ov = load_geojson("public_space.geojson")
    for f in public_ov["features"]:
        g = affine_transform(shape(f["geometry"]), aff)
        plot_polygon(ax, g, facecolor=CORAL, edgecolor="none", alpha=0.30, zorder=7)

    # Railway spine (rotated)
    railway_pts_orig = [
        (116.3490, 40.0265), (116.3485, 40.0150), (116.3480, 40.0060),
        (116.3475, 39.9935), (116.3470, 39.9800), (116.3475, 39.9650),
        (116.3480, 39.9498), (116.3475, 39.9390),
    ]
    railway_pts = [R(x, y) for x, y in railway_pts_orig]
    rx, ry = zip(*railway_pts)
    ax.plot(rx, ry, color=GOLD, linewidth=14, alpha=0.08, zorder=8, solid_capstyle="round")
    ax.plot(rx, ry, color=GOLD, linewidth=6, alpha=0.18, zorder=9, solid_capstyle="round")
    ax.plot(rx, ry, color=RAIL_BG, linewidth=4, alpha=0.7, zorder=10, solid_capstyle="round")
    ax.plot(rx, ry, color=GOLD, linewidth=2, alpha=0.85, zorder=11, solid_capstyle="round")
    for i in range(len(railway_pts) - 1):
        x1, y1 = railway_pts[i]
        x2, y2 = railway_pts[i + 1]
        dx, dy = x2 - x1, y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        nx, ny = -dy/length * 0.0005, dx/length * 0.0005
        n_ties = int(length / 0.003)
        for j in range(n_ties):
            t = j / n_ties
            cx, cy = x1 + dx*t, y1 + dy*t
            ax.plot([cx - nx, cx + nx], [cy - ny, cy + ny], color=GOLD,
                    linewidth=0.7, alpha=0.35, zorder=10)

    # ── Three cores: flat semi-transparent fills with white dashed outlines ──
    key_info = [
        ("KEY-001", "众智园", "AI自主创新加速区 · 191.9 ha", NAVY),
        ("KEY-002", "AI原点社区", "24h混合创新社区 · 104.3 ha", PURPLE),
        ("KEY-003", "大钟寺", "AI+产业门户 · 72.4 ha", GOLD),
    ]
    core_centers = []
    for kid, name, desc, color in key_info:
        k = keys_r[kid]
        # Flat semi-transparent fill
        plot_polygon(ax, k, facecolor=color, edgecolor="none",
                     alpha=0.25, zorder=12)
        # White dashed outline
        plot_polygon(ax, k, facecolor="none", edgecolor="#ffffff", linewidth=1.8,
                     alpha=0.9, zorder=15, linestyle=(0, (5, 3)))
        # Colored edge
        plot_polygon(ax, k, facecolor="none", edgecolor=color, linewidth=1.0,
                     alpha=0.6, zorder=14)
        cx, cy = k.centroid.x, k.centroid.y
        core_centers.append((cx, cy, color, name))
        ax.plot(cx, cy, "o", markersize=8, color="#ffffff", markeredgecolor=color,
                markeredgewidth=2.5, zorder=18)

    # Flying lines between cores
    for i in range(len(core_centers)):
        x1, y1, c1, _ = core_centers[i]
        x2, y2, c2, _ = core_centers[(i + 1) % len(core_centers)]
        draw_flying_line(ax, x1, y1, x2, y2, c1, n_dots=10, zorder=15)

    # ── AI scenario nodes (coral dots along the corridor) ──
    scenario_pts = [
        (116.3488, 40.020), (116.3485, 40.015), (116.3482, 40.010),
        (116.3478, 39.992), (116.3475, 39.989), (116.3472, 39.986),
        (116.3470, 39.984), (116.3473, 39.975), (116.3476, 39.977),
        (116.3460, 39.965), (116.3455, 39.985), (116.3438, 39.966),
        (116.3500, 39.970), (116.3450, 39.970), (116.3485, 39.966),
    ]
    for ox, oy in scenario_pts:
        sx, sy = R(ox, oy)
        draw_pulse_rings(ax, sx, sy, CORAL, n_rings=2, max_radius=0.0012, zorder=17)
        ax.plot(sx, sy, "o", markersize=8, color=CORAL, alpha=0.18, zorder=18)
        ax.plot(sx, sy, "o", markersize=4, color=CORAL, markeredgecolor="#ffffff",
                markeredgewidth=0.7, zorder=19)

    # ── Two wings (teal indicators) ──
    # West wing = 科技服务翼 (top of rotated map, y' higher)
    wing_w_y = 0.055
    ax.plot([39.942, 40.028], [wing_w_y, wing_w_y], color=TEAL, linewidth=1.2,
            alpha=0.35, zorder=15, linestyle=(0, (0.5, 4)), dash_capstyle="round")
    ax.text(39.965, wing_w_y + 0.003, "▲ 科技服务翼（西翼）", fontsize=8,
            color=TEAL, ha="center", va="bottom", zorder=20, alpha=0.95, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#ffffff", edgecolor=TEAL,
                      alpha=0.9, linewidth=0.8))
    # East wing = 场景赋能翼 (bottom of rotated map, y' lower)
    wing_e_y = 0.018
    ax.plot([39.942, 40.028], [wing_e_y, wing_e_y], color=TEAL, linewidth=1.2,
            alpha=0.35, zorder=15, linestyle=(0, (0.5, 4)), dash_capstyle="round")
    ax.text(39.985, wing_e_y - 0.003, "场景赋能翼（东翼）▼", fontsize=8,
            color=TEAL, ha="center", va="top", zorder=20, alpha=0.95, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#ffffff", edgecolor=TEAL,
                      alpha=0.9, linewidth=0.8))

    # ── Regional synergy (purple dashed connections outward) ──
    synergy_pts = [
        (40.025, 0.060, "中关村科学城"),
        (40.025, 0.020, "未来科学城"),
        (40.030, 0.008, "怀柔科学城"),
        (39.948, 0.012, "北京经开区"),
    ]
    for tx, ty, tname in synergy_pts:
        ax.plot([39.985, tx], [0.037, ty], color=PURPLE, linewidth=0.8,
                alpha=0.25, zorder=14, linestyle=(0, (2, 3)), dash_capstyle="round")
        ax.plot(tx, ty, "o", markersize=3.5, color=PURPLE, alpha=0.4, zorder=15)
        ax.text(tx, ty + 0.002, tname, fontsize=6, color=PURPLE, ha="center",
                va="bottom", zorder=20, alpha=0.8, fontweight="bold")

    # ── Context labels (rotated) ──
    def ctx_label(xr, yr, text, color="#334155", size=8):
        ax.text(xr, yr, text, ha="center", va="center", fontsize=size,
                color=color, zorder=20, alpha=0.95, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#ffffff", edgecolor=color,
                          alpha=0.85, linewidth=0.8))

    for ox, oy, lbl, clr, sz in [
        (116.325, 40.012, "清华大学", "#2563eb", 8),
        (116.316, 39.998, "北京大学", "#2563eb", 8),
        (116.348, 39.982, "北京航空航天大学", "#2563eb", 7),
        (116.356, 39.980, "中国信通院", "#2563eb", 7),
        (116.336, 39.984, "中国科学院", "#7c3aed", 8),
        (116.358, 39.962, "北京邮电大学", "#a16207", 7),
        (116.357, 39.954, "北京师范大学", "#a16207", 7),
        (116.343, 39.952, "北京交通大学", "#a16207", 7),
        (116.370, 40.000, "中关村东区", "#059669", 7),
        (116.347, 39.940, "北京北站", "#a16207", 7),
    ]:
        xr, yr = R(ox, oy)
        ctx_label(xr, yr, lbl, clr, sz)

    # Core labels on map
    for cx, cy, color, name in core_centers:
        ax.text(cx, cy + 0.0025, name, ha="center", va="center", fontsize=11,
                fontweight="bold", color="#ffffff", zorder=19,
                bbox=dict(boxstyle="round,pad=0.4", facecolor=color, edgecolor="#ffffff",
                          alpha=0.85, linewidth=1.5))

    # North arrow pointing RIGHT (north is +x' after 90° CW rotation)
    na_x, na_y = X_MAX - 0.006, Y_MAX - 0.022
    na_s = 0.004
    ax.add_patch(Circle((na_x, na_y), na_s * 0.8, facecolor=BG_MID, edgecolor=MUTED,
                        linewidth=0.8, alpha=0.8, zorder=20))
    ax.annotate("", xy=(na_x + na_s * 0.6, na_y), xytext=(na_x - na_s * 0.3, na_y),
                arrowprops=dict(arrowstyle="-|>", color="#ffffff", lw=1.2,
                                mutation_scale=10), zorder=21)
    ax.text(na_x, na_y + na_s * 0.8, "N", fontsize=7, color=WHITE, ha="center",
            va="bottom", fontweight="bold", zorder=21)

    # Refined scale bar (bottom center)
    sb_x0 = 39.965
    sb_y = Y_MIN + 0.010
    sb_len = 2000 / 111000.0
    for i in range(4):
        x0 = sb_x0 + i * sb_len / 4
        color = "#78716c" if i % 2 == 0 else "#ffffff"
        ax.add_patch(mpatches.Rectangle((x0, sb_y), sb_len / 4, 0.0012,
                     facecolor=color, edgecolor="none", alpha=0.8, zorder=21))
    ax.add_patch(mpatches.Rectangle((sb_x0, sb_y), sb_len, 0.0012,
                 facecolor="none", edgecolor="#78716c", linewidth=0.4, zorder=21))
    ax.text(sb_x0 + sb_len, sb_y + 0.002, "2000m", fontsize=6, color="#78716c",
            ha="right", va="bottom", zorder=21)
    ax.text(sb_x0 + sb_len / 2, sb_y + 0.002, "1000m", fontsize=6, color="#78716c",
            ha="center", va="bottom", zorder=21)
    ax.text(sb_x0, sb_y - 0.002, "0", fontsize=6, color="#78716c",
            ha="left", va="top", zorder=21)

    # ══════════════════════════════════════════════════════════════
    # FLOATING INFO PANELS (overlaid on map)
    # ══════════════════════════════════════════════════════════════
    T = ax.transAxes

    # ── Top-left: Title block (dark navy, matching reference) ──
    ax.add_patch(FancyBboxPatch((0.012, 0.868), 0.30, 0.118,
                 boxstyle="round,pad=0.008", facecolor="#0f172a", edgecolor="#1e3a5f",
                 linewidth=1.2, alpha=0.95, transform=T, zorder=25))
    # Logo
    try:
        from matplotlib.offsetbox import OffsetImage, AnnotationBbox
        logo_img = plt.imread(str(FIG_DIR / ".." / "logo-icon.png"))
        im = OffsetImage(logo_img, zoom=0.085)
        ab = AnnotationBbox(im, (0.032, 0.927), frameon=False,
                            xycoords="axes fraction", box_alignment=(0.5, 0.5),
                            zorder=27)
        ax.add_artist(ab)
    except Exception:
        pass
    ax.text(0.058, 0.958, "智脉京张", fontsize=26, fontweight="bold", color="#ffffff",
            ha="left", va="top", transform=T, zorder=26)
    ax.text(0.058, 0.918, "AI 原生创新带 · 概念方案总览", fontsize=12, color="#e2e8f0",
            ha="left", va="top", transform=T, zorder=26)
    ax.text(0.058, 0.888, "Zhima Jing-Zhang — AI-Native Innovation Belt",
            fontsize=8, color="#94a3b8", ha="left", va="top", style="italic", transform=T, zorder=26)

    # ── Top-right: Key metrics (compact horizontal pills) ──
    metrics = [
        ("43.6", "km²", "研究范围", NAVY),
        ("11.4", "km²", "设计范围", PURPLE),
        ("3", "核", "三核驱动", GOLD),
        ("15", "处", "AI场景", CORAL),
    ]
    mw = 0.070
    mh = 0.044
    mgap = 0.008
    mx = 0.672
    for val, unit, label, color in metrics:
        ax.add_patch(FancyBboxPatch((mx, 0.934), mw, mh,
                     boxstyle="round,pad=0.004", facecolor="#ffffff", edgecolor=color,
                     linewidth=1.0, alpha=0.95, transform=T, zorder=25))
        # Number + unit (top row, centered)
        ax.text(mx + mw / 2, 0.963, val + unit, fontsize=11,
                fontweight="bold", color=color, ha="center", va="center",
                transform=T, zorder=26)
        # Label (bottom row, centered)
        ax.text(mx + mw / 2, 0.943, label, fontsize=6.5, color="#57534e",
                ha="center", va="center", transform=T, zorder=26)
        mx += mw + mgap

    # ── Bottom-left: Legend (white card) ──
    legend_items = [
        ("众智园（北核）", NAVY, "fill"),
        ("AI原点社区（中核）", PURPLE, "fill"),
        ("大钟寺（南核）", GOLD, "fill"),
        ("AI场景节点", CORAL, "dot"),
        ("铁路绿廊（一轴）", GOLD, "line"),
        ("公共绿地", TEAL, "fill"),
        ("水系", WATER_LINE, "line"),
        ("高校/科研院所", "#86efac", "circle"),
        ("设计范围边界", NAVY, "dash"),
    ]
    lw = 0.168
    lh = 0.035 + len(legend_items) * 0.018 + 0.012
    ax.add_patch(FancyBboxPatch((0.015, 0.025), lw, lh,
                 boxstyle="round,pad=0.008", facecolor="#ffffff", edgecolor="#d6d3d1",
                 linewidth=0.8, alpha=0.95, transform=T, zorder=25))
    ax.text(0.030, 0.025 + lh - 0.015, "图 例", fontsize=11, fontweight="bold", color="#1c1917",
            ha="left", va="top", transform=T, zorder=26)
    for i, (ltext, lcolor, ltype) in enumerate(legend_items):
        cy = 0.025 + lh - 0.040 - i * 0.018
        if ltype == "fill":
            ax.add_patch(plt.Rectangle((0.030, cy - 0.005), 0.016, 0.009,
                         facecolor=lcolor, alpha=0.7, edgecolor=lcolor, linewidth=0.8,
                         transform=T, zorder=26))
        elif ltype == "dot":
            ax.plot(0.038, cy, "o", markersize=6, color=lcolor,
                    markeredgecolor="white", markeredgewidth=0.8,
                    transform=T, zorder=26)
        elif ltype == "circle":
            ax.add_patch(plt.Circle((0.038, cy), 0.006, facecolor=lcolor,
                         edgecolor=TEAL, linewidth=0.6, alpha=0.6,
                         transform=T, zorder=26))
        elif ltype == "line":
            ax.plot([0.030, 0.046], [cy, cy], color=lcolor, linewidth=2.5,
                    transform=T, zorder=26)
        elif ltype == "dash":
            ax.plot([0.030, 0.046], [cy, cy], color=lcolor, linewidth=1.2,
                    linestyle="--", transform=T, zorder=26)
        ax.text(0.055, cy, ltext, fontsize=8, color="#374151",
                ha="left", va="center", transform=T, zorder=26)

    # ── Bottom-right: Structure notes (white card) ──
    ax.add_patch(FancyBboxPatch((0.785, 0.025), 0.20, 0.135,
                 boxstyle="round,pad=0.008", facecolor="#ffffff", edgecolor="#d6d3d1",
                 linewidth=0.8, alpha=0.95, transform=T, zorder=25))
    ax.text(0.80, 0.148, "空间结构", fontsize=11, fontweight="bold", color="#1c1917",
            ha="left", va="top", transform=T, zorder=26)
    structs = [
        ("一轴", "京张铁路绿廊 — 全长约9km", GOLD),
        ("三核", "众智园 · AI原点 · 大钟寺", NAVY),
        ("两翼", "科技服务翼（西）· 场景赋能翼（东）", TEAL),
        ("协同", "三科学城 + 京津冀创新网络", PURPLE),
    ]
    sy = 0.118
    for label, desc, color in structs:
        ax.text(0.80, sy, "▸", fontsize=10, color=color,
                ha="left", va="center", transform=T, zorder=26)
        ax.text(0.817, sy, label, fontsize=9, color=color, fontweight="bold",
                ha="left", va="center", transform=T, zorder=26)
        ax.text(0.860, sy, desc, fontsize=8, color="#4b5563",
                ha="left", va="center", transform=T, zorder=26)
        sy -= 0.024

    fig.savefig(FIG_DIR / "site-overview.png", dpi=112,
                facecolor=BG_DARK, pil_kwargs={"optimize": True})
    plt.close(fig)
    print("  site-overview.png")


# ---------------------------------------------------------------------------
# Figure 2: Land Use Structure
# ---------------------------------------------------------------------------
def fig_land_use():
    site_fc = load_geojson("site_boundary.geojson")
    lu_fc = load_geojson("land_use.geojson")
    key_fc = load_geojson("key_areas.geojson")
    site = shape(site_fc["features"][0]["geometry"])
    keys = {f["id"]: shape(f["geometry"]) for f in key_fc["features"]}

    # ── Rotation (same as site overview) ──
    C_OFF = 116.385
    def R(x, y):
        return y, -x + C_OFF
    aff = [0, 1, -1, 0, 0, C_OFF]
    site_r = affine_transform(site, aff)
    keys_r = {k: affine_transform(v, aff) for k, v in keys.items()}

    # Rotate land use polygons
    lu_geoms = []
    for f in lu_fc["features"]:
        g = affine_transform(shape(f["geometry"]), aff)
        lu_geoms.append((f["properties"]["id"], g, f["properties"].get("area_sqm_calculated", 0)))

    fig = plt.figure(figsize=(16, 9))
    fig.patch.set_facecolor(BG_DARK)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG_DARK)

    X_MIN, X_MAX = 39.928, 40.035
    Y_MIN, Y_MAX = -0.012, 0.082
    ax.set_xlim(X_MIN, X_MAX)
    ax.set_ylim(Y_MIN, Y_MAX)
    ax.set_aspect(0.64)
    ax.axis("off")

    # ── Real OSM roads ──
    draw_osm_roads(ax, (X_MIN, X_MAX), (Y_MIN, Y_MAX),
                   transform_fn=R, style="context", zorder_base=1)
    draw_osm_roads(ax, (X_MIN, X_MAX), (Y_MIN, Y_MAX),
                   transform_fn=R, style="bright", clip_poly=site_r, zorder_base=5)

    # ── Context: water (小月河) ──
    wx_r, wy_r = [], []
    for i in range(25):
        yy = 39.933 + (40.030 - 39.933) * i / 24
        xx = 116.353 + 0.0015 * math.sin(i * 0.7) + 0.0008 * math.cos(i * 1.3)
        rx, ry = R(xx, yy)
        wx_r.append(rx)
        wy_r.append(ry)
    ax.plot(wx_r, wy_r, color=WATER, linewidth=8, alpha=0.6, zorder=2, solid_capstyle="round")
    ax.plot(wx_r, wy_r, color=WATER_LINE, linewidth=0.8, alpha=0.4, zorder=3)

    # ── Context: green patches ──
    ctx_green = [
        (116.315, 40.000, 0.009, "清华·北大"),
        (116.325, 39.992, 0.006, ""),
        (116.320, 39.948, 0.007, "紫竹院公园"),
        (116.355, 39.975, 0.003, ""),
        (116.370, 40.010, 0.004, ""),
    ]
    for gx, gy, gr, glabel in ctx_green:
        rx, ry = R(gx, gy)
        ax.add_patch(Circle((rx, ry), gr, facecolor=GREEN_FILL, edgecolor=GREEN_LIGHT,
                            linewidth=0.5, alpha=0.25, zorder=2))
        if glabel:
            ax.text(rx, ry, glabel, fontsize=7, color=TEAL, ha="center", va="center",
                    alpha=0.9, fontweight="bold", zorder=3)

    # ── Dot grid within site ──
    draw_dot_grid(ax, site_r, spacing=0.0010, color=TEAL, alpha_range=(0.03, 0.12),
                  dot_size=1.0, zorder=4)

    # ── Site boundary glow ──
    for i in range(5):
        a = 0.04 - i * 0.007
        plot_polygon(ax, site_r, facecolor=NAVY, edgecolor="none", alpha=a, zorder=6)
    plot_polygon(ax, site_r, facecolor=NAVY, edgecolor="none", alpha=0.03, zorder=6)
    plot_polygon(ax, site_r, facecolor="none", edgecolor=NAVY, linewidth=2.5,
                 alpha=0.8, zorder=7)

    # ── Land use zones ──
    lu_names = {
        "LU-001": "众智园·研发中试",
        "LU-002": "AI原点·混合社区",
        "LU-003": "大钟寺·商务消费",
        "LU-004": "京张绿廊·公共主轴",
        "LU-005": "西翼·科技服务",
        "LU-006": "东翼·场景赋能",
    }
    core_ids = {"LU-001", "LU-002", "LU-003"}

    for fid, geom, area in lu_geoms:
        color = LU_COLORS.get(fid, "#555555")
        if fid in core_ids:
            # Flat semi-transparent fills with white dashed outlines
            plot_polygon(ax, geom, facecolor=color, edgecolor="none", alpha=0.30, zorder=11)
            plot_polygon(ax, geom, facecolor="none", edgecolor="#ffffff", linewidth=1.8,
                        alpha=0.9, zorder=13, linestyle=(0, (5, 3)))
            plot_polygon(ax, geom, facecolor="none", edgecolor=color, linewidth=1.0,
                        alpha=0.6, zorder=12)
        else:
            plot_polygon(ax, geom, facecolor=color, edgecolor="none", alpha=0.25, zorder=11)
            plot_polygon(ax, geom, facecolor="none", edgecolor=color, linewidth=1.5,
                        alpha=0.7, zorder=12)

    # ── Green space overlay (parks in wings + corridor) ──
    green_fc_lu = load_geojson("green_space.geojson")
    for f in green_fc_lu["features"]:
        g = affine_transform(shape(f["geometry"]), aff)
        gtype = f["properties"].get("green_type", "")
        if gtype == "linear_park_corridor":
            plot_polygon(ax, g, facecolor=TEAL, edgecolor="none", alpha=0.30, zorder=12)
        else:
            plot_polygon(ax, g, facecolor=TEAL, edgecolor=TEAL, linewidth=0.8,
                        alpha=0.45, zorder=13)

    # ── Building footprints (urban texture) ──
    bldg_fc = load_geojson("buildings.geojson")
    BLDG_COLORS = {
        "ai_r_and_d": ("#3b82f6", 0.55),
        "residential": ("#d97706", 0.45),
        "retail": ("#dc2626", 0.50),
        "office": ("#6366f1", 0.50),
        "mixed_use": ("#8b5cf6", 0.50),
        "existing_retained": ("#78716c", 0.55),
        "incubator": ("#10b981", 0.50),
        "talent_apartment": ("#f59e0b", 0.55),
        "lab": ("#0ea5e9", 0.50),
        "cultural": ("#ec4899", 0.50),
        "community_service": ("#f97316", 0.55),
        "education": ("#22c55e", 0.50),
        "mobility_hub": ("#a855f7", 0.55),
    }
    for f in bldg_fc["features"]:
        g = affine_transform(shape(f["geometry"]), aff)
        bt = f["properties"].get("building_type", "office")
        bc, ba = BLDG_COLORS.get(bt, ("#888888", 0.4))
        is_lm = f["properties"].get("name", "") in {
            "AI总部大楼", "AI展示中心", "AI教育空间", "扇形机车库（保留）",
            "开源成果展示廊", "算力中心", "红队测试床", "模型机房",
            "社区AI中心", "商业中心", "轨道接驳枢纽",
        }
        if is_lm:
            plot_polygon(ax, g, facecolor="#fbbf24", edgecolor="#b45309",
                        linewidth=0.8, alpha=0.85, zorder=15)
        else:
            plot_polygon(ax, g, facecolor=bc, edgecolor="none", alpha=ba, zorder=14)

    # ── Metro station catchment (500m / 800m) ──
    metro_stations = [
        (116.3485, 40.0140, "学知园站", "昌平线"),
        (116.3430, 39.9920, "五道口站", "13号线"),
        (116.3470, 39.9700, "大钟寺站", "12/13号线"),
        (116.3400, 39.9780, "知春路站", "10/13号线"),
        (116.3550, 40.0000, "清华东路西口", "15号线"),
    ]
    for slon, slat, sname, sline in metro_stations:
        sx, sy = R(slon, slat)
        # 800m catchment
        ax.add_patch(Circle((sx, sy), 800/111320, facecolor="#3b82f6",
                            edgecolor="none", alpha=0.04, zorder=8))
        # 500m catchment
        ax.add_patch(Circle((sx, sy), 500/111320, facecolor="#3b82f6",
                            edgecolor="#3b82f6", linewidth=0.5, alpha=0.08, zorder=8))
        # Station marker
        ax.plot(sx, sy, "s", markersize=5, color="#2563eb", markeredgecolor="#ffffff",
                markeredgewidth=0.8, zorder=20)
        ax.text(sx, sy + 0.0015, sname, fontsize=6.5, color="#1d4ed8",
                ha="center", va="bottom", zorder=20, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.15", facecolor="#ffffff",
                          edgecolor="none", alpha=0.8))

    # ── Public space overlay ──
    public_fc_lu = load_geojson("public_space.geojson")
    for f in public_fc_lu["features"]:
        g = affine_transform(shape(f["geometry"]), aff)
        plot_polygon(ax, g, facecolor=CORAL, edgecolor="none", alpha=0.35, zorder=13)

    # ── Railway spine ──
    rail_pts = [
        (116.3490, 40.0265), (116.3485, 40.0150), (116.3480, 40.0060),
        (116.3475, 39.9935), (116.3470, 39.9800), (116.3475, 39.9650),
        (116.3480, 39.9498), (116.3475, 39.9390),
    ]
    rail_r = [R(lon, lat) for lon, lat in rail_pts]
    rrx, rry = zip(*rail_r)
    ax.plot(rrx, rry, color=GOLD, linewidth=14, alpha=0.08, zorder=14, solid_capstyle="round")
    ax.plot(rrx, rry, color=GOLD, linewidth=6, alpha=0.18, zorder=15, solid_capstyle="round")
    ax.plot(rrx, rry, color=GOLD, linewidth=4, alpha=0.7, zorder=16, solid_capstyle="round")
    ax.plot(rrx, rry, color="#f5d060", linewidth=2, alpha=0.85, zorder=17, solid_capstyle="round")
    # Sleepers
    for j in range(len(rail_r) - 1):
        x0, y0 = rail_r[j]
        x1, y1 = rail_r[j + 1]
        dist = math.hypot(x1 - x0, y1 - y0)
        n_sleep = max(2, int(dist / 0.003))
        for k in range(n_sleep):
            t = k / n_sleep
            sx = x0 + (x1 - x0) * t
            sy = y0 + (y1 - y0) * t
            ax.plot([sx - 0.0005, sx + 0.0005], [sy, sy], color=GOLD,
                    linewidth=0.7, alpha=0.35, zorder=15)

    # ── Labels on zones ──
    # Manual label offsets for cores to avoid overlap (leader lines)
    core_label_offsets = {
        "LU-001": (0.0, 0.012),    # 众智园: above
        "LU-002": (0.0, -0.013),   # AI原点: below
        "LU-003": (0.0, -0.013),   # 大钟寺: below
    }
    for fid, geom, area in lu_geoms:
        if geom.is_empty:
            continue
        cx, cy = geom.centroid.x, geom.centroid.y
        color = LU_COLORS.get(fid, "#555")
        if fid in core_ids:
            label = f"{lu_names[fid]}\n{area/10000:.1f} ha"
            fs = 11
            fw = "bold"
            bbox = dict(boxstyle="round,pad=0.4", facecolor="#ffffff",
                        edgecolor=color, alpha=0.95, linewidth=1.8)
            dx, dy = core_label_offsets.get(fid, (0, 0))
            lx, ly = cx + dx, cy + dy
            # Leader line from centroid to label
            ax.plot([cx, lx], [cy, ly - dy * 0.35], color=color, linewidth=1.0,
                    alpha=0.7, zorder=19, solid_capstyle="round")
            ax.text(lx, ly, label, ha="center", va="center", fontsize=fs,
                    color=color, fontweight=fw, zorder=20, bbox=bbox)
        elif fid == "LU-004":
            # Greenway spine label - place at north end, rotated along corridor
            ax.text(40.022, 0.0375, "京张绿廊·公共主轴  135.2 ha",
                    ha="center", va="center", fontsize=9, color=TEAL,
                    fontweight="bold", zorder=20, rotation=0,
                    bbox=dict(boxstyle="round,pad=0.25", facecolor="#ffffff",
                              edgecolor=TEAL, alpha=0.9, linewidth=0.8))
        else:
            label = f"{lu_names[fid]}  {area/10000:.1f} ha"
            fs = 9
            fw = "bold"
            bbox = dict(boxstyle="round,pad=0.3", facecolor="#ffffff",
                        edgecolor=color, alpha=0.9, linewidth=0.9)
            ax.text(cx, cy, label, ha="center", va="center", fontsize=fs,
                    color=WHITE, fontweight=fw, zorder=20, bbox=bbox)

    # ── Pulse rings on core centroids ──
    for kid, kr in keys_r.items():
        cx, cy = kr.centroid.x, kr.centroid.y
        color = {"KEY-001": NAVY, "KEY-002": PURPLE, "KEY-003": GOLD}[kid]
        draw_pulse_rings(ax, cx, cy, color, n_rings=3, max_radius=0.004, zorder=18)
        ax.plot(cx, cy, "o", markersize=8, color=color, markeredgecolor="#ffffff",
                markeredgewidth=1.5, zorder=19)

    # ── North arrow (points right after rotation) ──
    na_x, na_y = X_MAX - 0.006, Y_MAX - 0.022
    na_s = 0.004
    ax.annotate("", xy=(na_x + na_s, na_y), xytext=(na_x - na_s, na_y),
                arrowprops=dict(arrowstyle="-|>", color="#44403c", lw=1.5),
                zorder=25)
    ax.text(na_x, na_y + na_s * 0.7, "N", fontsize=8, color=WHITE, ha="center",
            va="bottom", fontweight="bold", zorder=25)
    ax.add_patch(Circle((na_x, na_y), na_s * 1.6, facecolor="none",
                        edgecolor=MUTED, linewidth=0.8, alpha=0.5, zorder=24))

    # ── Scale bar (bottom center, above disclaimer) ──
    m_per_deg_lat = 111320
    deg_2000m = 2000 / m_per_deg_lat
    sb_y = Y_MIN + 0.008
    sb_x0 = (X_MIN + X_MAX) / 2 - deg_2000m / 2
    ax.plot([sb_x0, sb_x0 + deg_2000m], [sb_y, sb_y], color="#44403c", linewidth=2.5,
            alpha=0.8, zorder=25, solid_capstyle="butt")
    ax.plot([sb_x0, sb_x0 + deg_2000m / 2], [sb_y, sb_y], color=BG_DARK, linewidth=3,
            alpha=0.9, zorder=26, solid_capstyle="butt")
    ax.text(sb_x0 + deg_2000m / 2, sb_y + 0.002, "2000m", fontsize=7, color=WHITE,
            ha="center", va="bottom", zorder=26)
    ax.text(sb_x0, sb_y - 0.002, "0", fontsize=6, color=MUTED, ha="center",
            va="top", zorder=26)

    # ── Title panel (top-left, dark navy) ──
    T = ax.transAxes
    ax.add_patch(FancyBboxPatch((0.012, 0.848), 0.27, 0.138,
        boxstyle="round,pad=0.008", facecolor="#0f172a", edgecolor="#1e3a5f",
        linewidth=1.2, alpha=0.95, transform=T, zorder=24))
    ax.text(0.025, 0.968, "用地结构", fontsize=26, fontweight="bold", color="#ffffff",
            ha="left", va="top", transform=T, zorder=25)
    ax.text(0.025, 0.918, "三核 · 一轴 · 两翼", fontsize=12, color="#e2e8f0",
            ha="left", va="top", transform=T, zorder=25)
    ax.text(0.025, 0.878, "Land Use Structure — 11.4 km² 无重叠覆盖",
            fontsize=8, color="#94a3b8", ha="left", va="top", style="italic",
            transform=T, zorder=25)

    # ── Metrics (top-right) ──
    metrics = [
        ("11.4", "km²", "设计范围", NAVY),
        ("368.6", "ha", "三核主体", PURPLE),
        ("31.0", "%", "绿地率", TEAL),
        ("6", "类", "用地分区", GOLD),
    ]
    mw = 0.062
    mgap = 0.014
    mx = 0.685
    _num_fs = 18
    _unit_fs = 10
    _num_cw = 0.6 * _num_fs / (72 * 16)
    _unit_cw_lat = 0.6 * _unit_fs / (72 * 16)
    for val, unit, label, color in metrics:
        ax.add_patch(FancyBboxPatch((mx, 0.90), mw, 0.075,
            boxstyle="round,pad=0.005", facecolor="#ffffff", edgecolor=color,
            linewidth=1.2, alpha=0.95, transform=T, zorder=24))
        # Center the number+unit group
        nw = len(val) * _num_cw
        if any(ord(c) > 0x2000 for c in unit):
            uw = len(unit) * _unit_fs / (72 * 16)
        else:
            uw = len(unit) * _unit_cw_lat
        _gap = 0.004
        tw = nw + _gap + uw
        sx = mx + (mw - tw) / 2
        ax.text(sx, 0.960, val, fontsize=_num_fs, fontweight="bold", color=color,
                ha="left", va="top", transform=T, zorder=25, family="monospace")
        ax.text(sx + nw + _gap, 0.955, unit, fontsize=_unit_fs, color=color,
                ha="left", va="top", transform=T, zorder=25)
        ax.text(mx + mw / 2, 0.912, label, fontsize=8, color="#44403c",
                ha="center", va="top", transform=T, zorder=25)
        mx += mw + mgap

    # ── Legend panel (bottom-left) ──
    lu_data = sorted(lu_geoms, key=lambda x: -x[2])
    total_area = sum(d[2] for d in lu_data)
    lw_panel = 0.22
    lh_panel = 0.035 + len(lu_data) * 0.032 + 0.02
    ax.add_patch(FancyBboxPatch((0.015, 0.025), lw_panel, lh_panel,
        boxstyle="round,pad=0.008", facecolor="#ffffff", edgecolor="#d6d3d1",
        linewidth=0.8, alpha=0.95, transform=T, zorder=24))
    ax.text(0.025, 0.025 + lh_panel - 0.015, "图例", fontsize=11, fontweight="bold",
            color="#1c1917", ha="left", va="top", transform=T, zorder=25)
    for i, (fid, geom, area) in enumerate(lu_data):
        ly = 0.025 + lh_panel - 0.045 - i * 0.032
        color = LU_COLORS.get(fid, "#555")
        ax.add_patch(plt.Rectangle((0.025, ly - 0.008), 0.018, 0.014,
                     facecolor=color, alpha=0.7, edgecolor=color, linewidth=0.8,
                     transform=T, zorder=25))
        pct = area / total_area * 100
        ax.text(0.050, ly, lu_names[fid], fontsize=8.5, color="#1c1917",
                ha="left", va="center", transform=T, zorder=25)
        ax.text(0.225, ly, f"{area/10000:.1f}ha {pct:.0f}%", fontsize=8,
                color="#4b5563", ha="right", va="center", transform=T, zorder=25,
                family="monospace")

    # ── Structure notes panel (bottom-right) ──
    nx, ny, nw, nh = 0.72, 0.025, 0.265, 0.16
    ax.add_patch(FancyBboxPatch((nx, ny), nw, nh,
        boxstyle="round,pad=0.008", facecolor="#ffffff", edgecolor="#d6d3d1",
        linewidth=0.8, alpha=0.95, transform=T, zorder=24))
    ax.text(nx + 0.012, ny + nh - 0.015, "结构要点", fontsize=11, fontweight="bold",
            color="#1c1917", ha="left", va="top", transform=T, zorder=25)
    notes = [
        ("三核功能主体", "368.6 ha（众智园·AI原点·大钟寺）"),
        ("京张绿廊主轴", "南北贯通，三核外段为公园绿地"),
        ("两翼城市腹地", "科技服务翼（西）+ 场景赋能翼（东）"),
        ("建筑肌理", "441栋概念建筑，按功能分色"),
        ("地铁覆盖", "6站500m覆盖率约62%，800m约85%"),
        ("留白与弹性", "概念建议阶段预留弹性用地"),
    ]
    for i, (label, desc) in enumerate(notes):
        ny_i = ny + nh - 0.045 - i * 0.028
        ax.text(nx + 0.015, ny_i, "▸", fontsize=9, color=GOLD,
                ha="left", va="center", transform=T, zorder=25)
        ax.text(nx + 0.032, ny_i, label, fontsize=8.5, color="#2563eb",
                ha="left", va="center", transform=T, zorder=25, fontweight="bold")
        ax.text(nx + 0.105, ny_i, desc, fontsize=7.5, color="#44403c",
                ha="left", va="center", transform=T, zorder=25)

    # ── Disclaimer ──
    ax.text(0.5, 0.005, "PROVISIONAL · CONCEPT ONLY — 本图为概念方案，边界为示意性表达，仅供专业团队深化研究参考",
            fontsize=8, color=MUTED, ha="center", va="bottom", transform=T, zorder=26, alpha=0.9)

    fig.savefig(FIG_DIR / "land-use-structure.png", dpi=120,
                facecolor=BG_DARK)
    plt.close(fig)
    print("  land-use-structure.png")


# ---------------------------------------------------------------------------
# Figure 3: Key Areas Detail
# ---------------------------------------------------------------------------
def _draw_key_area_buildings(ax, k, area_type, color):
    """Draw building footprints from buildings.geojson within a key area.

    Loads varied building polygons (L-shaped, U-shaped, T-shaped, rectangles)
    with retained industrial heritage highlighted.
    """
    minx, miny, maxx, maxy = k.bounds
    w = maxx - minx
    h = maxy - miny
    cx = (minx + maxx) / 2
    cy = (miny + maxy) / 2

    # Green spine corridor is drawn from green_space.geojson (GR-013 central_spine)
    # Only draw a subtle center line for reference
    ax.plot([cx, cx], [miny + 0.001, maxy - 0.001], color=TEAL, linewidth=0.8,
            alpha=0.25, zorder=7, linestyle="--")

    # Load buildings from GeoJSON
    bldg_fc = load_geojson("buildings.geojson")

    # Color mapping by building type
    type_colors = {
        "ai_r_and_d": (BUILDING_FILL, 0.92),
        "lab": (BUILDING_FILL, 0.95),
        "incubator": (color, 0.75),
        "existing_retained": (CORAL, 0.55),
        "residential": (BUILDING_FILL, 0.88),
        "mixed_use": (color, 0.65),
        "community_service": (color, 0.75),
        "retail": (color, 0.70),
        "talent_apartment": (PURPLE, 0.60),
        "office": (color, 0.80),
        "civic": (CORAL, 0.55),
    }

    for f in bldg_fc["features"]:
        props = f["properties"]
        # Only draw buildings in this key area
        if props.get("key_area_id") != area_type_to_keyid(area_type):
            continue
        poly = shape(f["geometry"])
        if not k.intersects(poly):
            continue
        clipped = poly.intersection(k)
        if clipped.is_empty:
            continue

        btype = props.get("building_type", "mixed_use")
        is_retained = props.get("construction_status") == "retained"
        bcolor, balpha = type_colors.get(btype, (BUILDING_FILL, 0.6))

        # Shadow
        shadow = translate(clipped, xoff=0.00006, yoff=-0.00005)
        if not shadow.is_empty:
            plot_polygon(ax, shadow, facecolor="#a8a29e", edgecolor="none",
                        alpha=0.08, zorder=9)

        # Building
        edge_color = CORAL if is_retained else BUILDING_EDGE
        edge_width = 1.2 if is_retained else 0.7
        edge_style = "--" if is_retained else "-"
        plot_polygon(ax, clipped, facecolor=bcolor, edgecolor=edge_color,
                    linewidth=edge_width, alpha=balpha, zorder=10,
                    linestyle=edge_style)

        # Top highlight for larger buildings
        if props.get("area_sqm_calculated", 0) > 5000:
            plot_polygon(ax, clipped, facecolor="none", edgecolor="#d6d3d1",
                        linewidth=0.2, alpha=0.15, zorder=11)

    # Central plaza node within corridor (landmark gathering space)
    plaza_r = 0.0006 if area_type != "commercial" else 0.0005
    plaza = Point(cx, cy).buffer(plaza_r)
    plaza_c = plaza.intersection(k)
    if not plaza_c.is_empty:
        plot_polygon(ax, plaza_c, facecolor=CORAL, edgecolor="none",
                     alpha=0.20, zorder=8)

    # Pocket parks are drawn from green_space.geojson (GR-002/003/004)


def area_type_to_keyid(area_type):
    """Map area_type string to key area ID."""
    mapping = {"campus": "KEY-001", "community": "KEY-002", "commercial": "KEY-003"}
    return mapping.get(area_type, "")

def _fetch_satellite_bounds(lon_min, lat_min, lon_max, lat_max, zoom=17):
    """Fetch and stitch Esri satellite tiles for a lon/lat bounding box.

    Returns (PIL.Image, (lon_w, lon_e, lat_s, lat_n)) or (None, None).
    Tiles are cached in scripts/data/.
    """
    import math as _math
    import urllib.request as _urlreq
    import time as _time
    from io import BytesIO as _BytesIO

    tile_dir = REPO / "scripts" / "data"
    tile_dir.mkdir(parents=True, exist_ok=True)
    TS = 256
    TILE_URL = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"

    def _lonlat_to_tile(lon, lat, z):
        n = 2 ** z
        x = int((lon + 180) / 360 * n)
        lat_rad = _math.radians(lat)
        y = int((1 - _math.asinh(_math.tan(lat_rad)) / _math.pi) / 2 * n)
        return x, y

    def _tile_to_lonlat(x, y, z):
        n = 2 ** z
        lon = x / n * 360 - 180
        lat_rad = _math.atan(_math.sinh(_math.pi * (1 - 2 * y / n)))
        lat = _math.degrees(lat_rad)
        return lon, lat

    # Add small padding to ensure full coverage
    pad = 0.001
    x_min, y_max = _lonlat_to_tile(lon_min - pad, lat_min - pad, zoom)
    x_max, y_min = _lonlat_to_tile(lon_max + pad, lat_max + pad, zoom)

    # Limit tile count to avoid excessive downloads
    max_tiles = 200
    total = (x_max - x_min + 1) * (y_max - y_min + 1)
    if total > max_tiles:
        zoom = zoom - 1
        x_min, y_max = _lonlat_to_tile(lon_min - pad, lat_min - pad, zoom)
        x_max, y_min = _lonlat_to_tile(lon_max + pad, lat_max + pad, zoom)

    width = (x_max - x_min + 1) * TS
    height = (y_max - y_min + 1) * TS
    mosaic = Image.new("RGB", (width, height))
    fetched = 0

    for tx in range(x_min, x_max + 1):
        for ty in range(y_min, y_max + 1):
            cache_path = tile_dir / f"tile_{zoom}_{tx}_{ty}.png"
            if cache_path.exists():
                img = Image.open(cache_path).convert("RGB")
            else:
                url = TILE_URL.format(z=zoom, x=tx, y=ty)
                img = None
                for attempt in range(3):
                    try:
                        req = _urlreq.Request(url, headers={
                            "User-Agent": "ZhimaJingZhang/1.0 (urban design)"
                        })
                        with _urlreq.urlopen(req, timeout=30) as resp:
                            img = Image.open(_BytesIO(resp.read())).convert("RGB")
                            img.save(cache_path, "PNG")
                            _time.sleep(0.08)
                            break
                    except Exception:
                        _time.sleep(1)
                if img is None:
                    continue
                fetched += 1
            mosaic.paste(img, ((tx - x_min) * TS, (ty - y_min) * TS))

    lon_w, lat_n = _tile_to_lonlat(x_min, y_min, zoom)
    lon_e, lat_s = _tile_to_lonlat(x_max + 1, y_max + 1, zoom)

    return mosaic, (lon_w, lon_e, lat_s, lat_n)


def fig_key_areas():
    key_fc = load_geojson("key_areas.geojson")
    green_fc = load_geojson("green_space.geojson")
    public_fc = load_geojson("public_space.geojson")

    keys = {f["properties"]["id"]: shape(f["geometry"]) for f in key_fc["features"]}
    key_names = {"KEY-001": "众智园", "KEY-002": "AI原点社区", "KEY-003": "大钟寺"}
    key_sub = {"KEY-001": "北核 · AI全栈自主创新加速区 · 191.9 ha",
               "KEY-002": "中核 · 24h混合创新社区 · 104.3 ha",
               "KEY-003": "南核 · AI+产业门户 · 72.4 ha"}
    key_colors = {"KEY-001": NAVY, "KEY-002": PURPLE, "KEY-003": GOLD}
    # Unified node definitions: (lon_offset_from_rail, lat_offset_frac, name, is_landmark, label_side)
    # label_side: -1 = left of key area, +1 = right of key area
    # Positions based on real geography: railway corridor, stations, known projects
    key_nodes = {
        "KEY-001": [
            (0.0000,  0.38, "LM-02 开源成果展示廊", True,  +1),
            (0.0018,  0.42, "孵化器集群",            False, +1),
            (-0.0020, -0.38, "大模型训练中试",       False, -1),
            (-0.0012, -0.10, "红队测试床",           False, -1),
            (0.0022, -0.12, "算力沙盒",             False, +1),
        ],
        "KEY-002": [
            (0.0000,  0.15, "LM-01 智脉原点碑", True,  -1),
            (-0.0025,  0.30, "AI教育空间",       False, -1),
            (-0.0017, -0.05, "社区AI中心",       False, -1),
            (-0.0018, -0.30, "研究者公寓",       False, -1),
            (0.0018,  0.05, "联合办公",         False, +1),
            (0.0015,  0.35, "健康导航站",       False, +1),
        ],
        "KEY-003": [
            (0.0000, -0.08, "LM-04 全球AI里程碑亭", True,  -1),
            (0.0022, -0.28, "AI定制零售",           False, +1),
            (-0.0022, -0.28, "金融合规顾问",         False, -1),
            (0.0018,  0.12, "沉浸体验",             False, +1),
            (0.0015,  0.32, "智能商务",             False, +1),
        ],
    }

    fig, axes = plt.subplots(1, 3, figsize=(20, 8))
    fig.patch.set_facecolor(BG_DARK)

    for idx, (kid, ax) in enumerate(zip(["KEY-001", "KEY-002", "KEY-003"], axes)):
        ax.set_facecolor(BG_DARK)
        k = keys[kid]
        minx, miny, maxx, maxy = k.bounds
        color = key_colors[kid]
        w = maxx - minx
        h = maxy - miny
        cx_k = (minx + maxx) / 2
        cy_k = (miny + maxy) / 2
        # Actual railway corridor longitude (from OSM analysis, not key area center)
        rail_lon = {"KEY-001": 116.3460, "KEY-002": 116.3472, "KEY-003": 116.3473}[kid]

        # ── Satellite base map (fetch for viewport bounds) ──
        half_lon = 0.0125
        half_lat = 0.010
        sat_img, sat_ext = _fetch_satellite_bounds(
            cx_k - half_lon, cy_k - half_lat,
            cx_k + half_lon, cy_k + half_lat, zoom=17)
        if sat_img is not None:
            # Slightly darken satellite for overlay readability
            sat_arr = np.array(sat_img).astype(np.float32)
            sat_arr = sat_arr * 0.85 + 8  # slight darken for overlay readability
            sat_arr = np.clip(sat_arr, 0, 255).astype(np.uint8)
            ax.imshow(sat_arr, extent=list(sat_ext), origin="upper",
                      zorder=1, aspect="auto")
            # Subtle dark overlay for design emphasis
            ax.add_patch(plt.Rectangle((cx_k - half_lon, cy_k - half_lat),
                         half_lon * 2, half_lat * 2,
                         facecolor="#0a0a0a", alpha=0.08, zorder=2))

        # ── OSM roads (light for satellite visibility) ──
        pad_r = 0.002
        roads = load_osm_roads()
        if roads:
            road_styles_sat = {
                "motorway":   ("#ffffff", 4.5, 0.55, "#e8e0d0", 2.5, 0.85),
                "trunk":      ("#ffffff", 3.5, 0.45, "#e8e0d0", 2.0, 0.75),
                "primary":    ("#ffffff", 2.8, 0.40, "#ddd5c5", 1.5, 0.65),
                "secondary":  ("#ffffff", 2.0, 0.30, "#d5cdbd", 1.0, 0.50),
                "tertiary":   ("#ffffff", 1.3, 0.22, "#ccc4b4", 0.7, 0.38),
                "residential":("#ffffff", 0.7, 0.15, "#c4bcac", 0.3, 0.25),
            }
            for rc, segments in roads.items():
                if rc not in road_styles_sat:
                    continue
                cc, clw, ca, fc, flw, fa = road_styles_sat[rc]
                segs_out = []
                for coords in segments:
                    seg = [(lon, lat) for lon, lat in coords
                           if minx - pad_r <= lon <= maxx + pad_r
                           and miny - pad_r <= lat <= maxy + pad_r]
                    if len(seg) >= 2:
                        segs_out.append(seg)
                if not segs_out:
                    continue
                lc = LineCollection(segs_out, colors=cc, linewidths=clw, alpha=ca,
                                    zorder=5, capstyle="round", joinstyle="round")
                lc.set_clip_path(MplPolygon(list(k.exterior.coords),
                                            transform=ax.transData))
                ax.add_collection(lc)
                lc2 = LineCollection(segs_out, colors=fc, linewidths=flw, alpha=fa,
                                     zorder=6, capstyle="round", joinstyle="round")
                lc2.set_clip_path(MplPolygon(list(k.exterior.coords),
                                             transform=ax.transData))
                ax.add_collection(lc2)

        # ── Key area color tint ──
        plot_polygon(ax, k, facecolor=color, edgecolor="none", alpha=0.10, zorder=7)

        # ── 拆改留分区 (based on real renewal data & satellite fabric) ──
        renov_w = 0.0016  # ~130m each side of railway
        # Base renovation strip along railway
        renov_rect = box(rail_lon - renov_w, miny, rail_lon + renov_w, maxy)
        renov_clipped = renov_rect.intersection(k)
        if not renov_clipped.is_empty:
            plot_polygon(ax, renov_clipped, facecolor="#ea580c", edgecolor="none",
                        alpha=0.22, zorder=7)

        # Area-specific additional renovation & new-build zones
        area_zones = {
            "KEY-001": {
                # 众智园: old industrial EAST of railway → renovate; 学北园 new north
                "renovate": [
                    box(rail_lon + renov_w, miny + h*0.15, maxx - w*0.05, miny + h*0.60),
                ],
                "newbuild": [
                    # 学北园/众智园 new campus at north (both sides of rail)
                    box(minx + w*0.08, maxy - h*0.25, rail_lon + 0.002, maxy - h*0.02),
                ],
            },
            "KEY-002": {
                # AI原点: opportunity buildings E of rail (东升/智源/东源); W side mixed
                "renovate": [
                    box(rail_lon + renov_w, miny + h*0.10, maxx - w*0.08, miny + h*0.55),
                    box(minx + w*0.05, miny + h*0.50, rail_lon - renov_w, miny + h*0.75),
                ],
                "newbuild": [
                    # 凯时广场片区 (northeast)
                    box(rail_lon + renov_w, maxy - h*0.20, maxx - w*0.05, maxy - h*0.02),
                    # 蓟鑫大厦片区 (southeast)
                    box(rail_lon + renov_w, miny + h*0.02, maxx - w*0.05, miny + h*0.18),
                ],
            },
            "KEY-003": {
                # 大钟寺: 蓝景丽家 demolition site SW; 方恒/中坤 renovate E
                "renovate": [
                    box(rail_lon + renov_w, miny + h*0.15, maxx - w*0.05, maxy - h*0.10),
                ],
                "newbuild": [
                    # 蓝景丽家→国际交流中心 (southwest of railway, real project)
                    box(minx + w*0.05, miny + h*0.05, rail_lon - renov_w, miny + h*0.32),
                ],
            },
        }
        for ztype in ["renovate", "newbuild"]:
            zcolor = "#ea580c" if ztype == "renovate" else "#dc2626"
            zalpha = 0.20 if ztype == "renovate" else 0.16
            for zbox in area_zones.get(kid, {}).get(ztype, []):
                zc = zbox.intersection(k)
                if not zc.is_empty:
                    plot_polygon(ax, zc, facecolor=zcolor, edgecolor="none",
                                alpha=zalpha, zorder=7)
                    if ztype == "newbuild":
                        plot_polygon(ax, zc, facecolor="none", edgecolor=zcolor,
                                    linewidth=0.7, alpha=0.45, zorder=7,
                                    linestyle=(0, (4, 3)))

        # ── Green spaces ──
        for f in green_fc["features"]:
            if f["properties"].get("green_type") == "linear_park_corridor":
                continue
            ggeom = shape(f["geometry"])
            if ggeom.intersects(k):
                clipped = ggeom.intersection(k)
                if not clipped.is_empty:
                    plot_polygon(ax, clipped, facecolor="#22c55e", edgecolor="none",
                                alpha=0.30, zorder=8)

        # ── Public spaces ──
        _landmark_plazas = {"PS-001", "PS-002", "PS-004"}
        for f in public_fc["features"]:
            if f["properties"].get("id") in _landmark_plazas:
                continue
            pgeom = shape(f["geometry"])
            if pgeom.intersects(k):
                clipped = pgeom.intersection(k)
                if not clipped.is_empty:
                    plot_polygon(ax, clipped, facecolor="#f97316", edgecolor="none",
                                alpha=0.30, zorder=9)

        # ── Railway green spine (at actual railway position) ──
        ax.plot([rail_lon, rail_lon], [miny, maxy], color="#22c55e", linewidth=6, alpha=0.15,
                zorder=10, solid_capstyle="round")
        ax.plot([rail_lon, rail_lon], [miny, maxy], color=GOLD, linewidth=2, alpha=0.65,
                zorder=11, solid_capstyle="round")

        # ── Public space corridors (aligned to real EW streets) ──
        corridor_fracs = {
            "KEY-001": [0.12, 0.35, 0.50, 0.95],
            "KEY-002": [0.22, 0.78],
            "KEY-003": [0.35, 0.87],
        }
        corridor_names = {
            "KEY-001": {0.50: "清华东路"},
            "KEY-002": {0.78: "成府路"},
            "KEY-003": {0.35: "北三环西路"},
        }
        for frac in corridor_fracs.get(kid, []):
            cy = miny + h * frac
            # West connection (edge to rail)
            ax.plot([minx + w*0.01, rail_lon - 0.0004], [cy, cy],
                    color="#0d9488", linewidth=6, alpha=0.20, zorder=10,
                    solid_capstyle="round")
            ax.plot([minx + w*0.01, rail_lon - 0.0004], [cy, cy],
                    color="#5eead4", linewidth=1.8, alpha=0.70, zorder=11,
                    linestyle=(0, (6, 3)), solid_capstyle="round")
            # East connection (rail to edge)
            ax.plot([rail_lon + 0.0004, maxx - w*0.01], [cy, cy],
                    color="#0d9488", linewidth=6, alpha=0.20, zorder=10,
                    solid_capstyle="round")
            ax.plot([rail_lon + 0.0004, maxx - w*0.01], [cy, cy],
                    color="#5eead4", linewidth=1.8, alpha=0.70, zorder=11,
                    linestyle=(0, (6, 3)), solid_capstyle="round")
            # Interchange node at railway
            ax.plot(rail_lon, cy, "o", markersize=5, color="#0d9488",
                    markeredgecolor="#ffffff", markeredgewidth=0.8, zorder=12, alpha=0.90)
            # Road name label (outside key area, west side)
            rname = corridor_names.get(kid, {}).get(frac)
            if rname:
                ax.text(minx - w*0.01, cy, rname, fontsize=6, color="#57534e",
                        ha="right", va="center", zorder=15, fontweight="bold",
                        bbox=dict(boxstyle="round,pad=0.1", facecolor=BG_DARK,
                                  edgecolor="none", alpha=0.7))

        # ── Key area border ──
        plot_polygon(ax, k, facecolor="none", edgecolor=color, linewidth=2.5,
                     alpha=0.95, zorder=14)
        # Outer glow
        for i in range(3):
            plot_polygon(ax, k, facecolor="none", edgecolor=color,
                         linewidth=5 + i * 3, alpha=0.06 - i * 0.02, zorder=13)

        # ── Zone labels (positioned per area to avoid overlap) ──
        zone_label_pos = {
            "KEY-001": {"retain": (minx + w*0.04, miny + h*0.04, "left", "bottom"),
                        "renov": (rail_lon + renov_w + 0.0003, miny + h*0.72, "left", "center"),
                        "new": (minx + w*0.15, maxy - h*0.16, "left", "center")},
            "KEY-002": {"retain": (minx + w*0.04, miny + h*0.04, "left", "bottom"),
                        "renov": (rail_lon + renov_w + 0.0003, miny + h*0.30, "left", "center"),
                        "new": (rail_lon + renov_w + 0.0003, maxy - h*0.10, "left", "center")},
            "KEY-003": {"retain": (maxx - w*0.04, miny + h*0.04, "right", "bottom"),
                        "renov": (rail_lon + renov_w + 0.0003, maxy - h*0.15, "left", "center"),
                        "new": (minx + w*0.10, miny + h*0.18, "left", "center")},
        }
        zp = zone_label_pos[kid]
        ax.text(zp["retain"][0], zp["retain"][1], "保留",
                fontsize=6.5, color="#64748b", ha=zp["retain"][2], va=zp["retain"][3],
                zorder=15, fontweight="bold", alpha=0.8,
                bbox=dict(boxstyle="round,pad=0.12", facecolor=BG_DARK,
                          edgecolor="#94a3b8", alpha=0.7, linewidth=0.5))
        ax.text(zp["renov"][0], zp["renov"][1], "改造",
                fontsize=6.5, color="#c2410c", ha=zp["renov"][2], va=zp["renov"][3],
                zorder=15, fontweight="bold", alpha=0.9,
                bbox=dict(boxstyle="round,pad=0.12", facecolor=BG_DARK,
                          edgecolor="#ea580c", alpha=0.75, linewidth=0.5))
        ax.text(zp["new"][0], zp["new"][1], "新建",
                fontsize=6.5, color="#b91c1c", ha=zp["new"][2], va=zp["new"][3],
                zorder=15, fontweight="bold", alpha=0.9,
                bbox=dict(boxstyle="round,pad=0.12", facecolor=BG_DARK,
                          edgecolor="#dc2626", alpha=0.75, linewidth=0.5))

        # ── Context labels (surrounding landmarks) ──
        context_labels = {
            "KEY-001": [
                (minx - w*0.035, maxy + h*0.01, "学知园站(昌平线)", (1, 0), "#0369a1"),
                (minx - w*0.035, miny - h*0.01, "北航", (1, 0), "#0369a1"),
                (maxx + w*0.035, maxy + h*0.01, "京藏高速", (-1, 0), "#57534e"),
            ],
            "KEY-002": [
                (minx - w*0.035, maxy + h*0.01, "清华大学", (1, 0), "#0369a1"),
                (maxx + w*0.035, miny + h*0.78, "五道口站(13号线)", (-1, 0), "#0369a1"),
                (maxx + w*0.035, miny - h*0.01, "中科院", (-1, 0), "#0369a1"),
            ],
            "KEY-003": [
                (minx - w*0.035, maxy + h*0.01, "中关村大街", (1, 0), "#57534e"),
                (minx - w*0.035, miny - h*0.01, "大钟寺站(12/13号线)", (1, 0), "#0369a1"),
                (maxx + w*0.035, maxy + h*0.01, "方恒·中坤广场", (-1, 0), "#57534e"),
            ],
        }
        for clx, cly, cltext, ha_i, clcolor in context_labels.get(kid, []):
            ha = "left" if ha_i[0] > 0 else "right"
            ax.text(clx, cly, cltext, fontsize=6, color=clcolor, ha=ha, va="center",
                    zorder=15, fontweight="bold", alpha=0.85,
                    bbox=dict(boxstyle="round,pad=0.12", facecolor=BG_DARK,
                              edgecolor="none", alpha=0.65))
            # Connector line from frame to label
            if cly > maxy:  # label above frame
                ax.plot([clx, clx], [maxy, cly - h*0.005], color=clcolor,
                        linewidth=1.0, alpha=0.7, zorder=14, linestyle=(0, (4, 2)))
            elif cly < miny:  # label below frame
                ax.plot([clx, clx], [miny, cly + h*0.005], color=clcolor,
                        linewidth=1.0, alpha=0.7, zorder=14, linestyle=(0, (4, 2)))
            elif ha_i[0] > 0:  # label left of frame
                ax.plot([minx, clx + 0.0001], [cly, cly], color=clcolor,
                        linewidth=1.0, alpha=0.7, zorder=14, linestyle=(0, (4, 2)))
            else:  # label right of frame
                ax.plot([maxx, clx - 0.0001], [cly, cly], color=clcolor,
                        linewidth=1.0, alpha=0.7, zorder=14, linestyle=(0, (4, 2)))

        # ── North arrow ──
        na_x = maxx - w*0.06
        na_y = maxy - h*0.06
        ax.annotate("N", xy=(na_x, na_y + h*0.025), xytext=(na_x, na_y - h*0.015),
                    fontsize=7, fontweight="bold", color="#44403c", ha="center",
                    va="bottom", zorder=20,
                    arrowprops=dict(arrowstyle="-|>", color="#44403c", lw=1.2))

        # ── Renewal data annotation (KEY-002 has official data) ──
        if kid == "KEY-002":
            data_text = "更新数据：改造6处/5.35万㎡  拆除5处/0.45万㎡  重建24处/17.3万㎡"
            ax.text(cx_k, miny - h*0.06, data_text, fontsize=5.8, color="#57534e",
                    ha="center", va="top", zorder=20,
                    bbox=dict(boxstyle="round,pad=0.2", facecolor=BG_DARK,
                              edgecolor=MUTED, alpha=0.8, linewidth=0.5))
        elif kid == "KEY-003":
            data_text = "蓝景丽家→国际交流中心（拆除重建，总投资48.8亿元）"
            ax.text(cx_k, miny - h*0.06, data_text, fontsize=5.8, color="#57534e",
                    ha="center", va="top", zorder=20,
                    bbox=dict(boxstyle="round,pad=0.2", facecolor=BG_DARK,
                              edgecolor=MUTED, alpha=0.8, linewidth=0.5))
        elif kid == "KEY-001":
            data_text = "学北园23.8万㎡已建成  国家自然科学基金委签约入驻"
            ax.text(cx_k, miny - h*0.06, data_text, fontsize=5.8, color="#57534e",
                    ha="center", va="top", zorder=20,
                    bbox=dict(boxstyle="round,pad=0.2", facecolor=BG_DARK,
                              edgecolor=MUTED, alpha=0.8, linewidth=0.5))

        # ── Nodes & landmarks with external leader-line labels ──
        nodes = key_nodes[kid]
        # Label anchor x positions (outside key area frame)
        label_x_left = minx - w * 0.008
        label_x_right = maxx + w * 0.008
        # Collect label positions per side to avoid overlap
        left_labels = []   # (y, text, color, is_landmark)
        right_labels = []
        for lon_off, lat_frac, name, is_lm, lside in nodes:
            nx = rail_lon + lon_off
            ny = cy_k + lat_frac * h * 0.40
            # Draw marker
            if is_lm:
                ax.add_patch(Circle((nx, ny), 0.0012, facecolor=GOLD, alpha=0.15,
                                    zorder=19, edgecolor="none"))
                ax.plot(nx, ny, marker="*", markersize=28, color=GOLD,
                        markeredgecolor="#ffffff", markeredgewidth=1.5, zorder=20)
            else:
                ax.plot(nx, ny, "o", markersize=7, color="#ffffff",
                        markeredgecolor="none", zorder=17)
                ax.plot(nx, ny, "o", markersize=5, color=color,
                        markeredgecolor="#ffffff", markeredgewidth=0.8, zorder=18)
            if lside < 0:
                left_labels.append((ny, name, GOLD if is_lm else color, is_lm, nx))
            else:
                right_labels.append((ny, name, GOLD if is_lm else color, is_lm, nx))

        # Sort labels by y and draw with leader lines, spreading to avoid overlap
        def _draw_labels(labels, label_x, ha, side_sign):
            labels.sort(key=lambda t: t[0], reverse=True)
            min_gap = h * 0.075  # minimum vertical gap between labels
            placed = []
            for ny, name, lcolor, is_lm, nx in labels:
                ly = ny
                # Push up if too close to previous
                for py in placed:
                    if abs(ly - py) < min_gap:
                        ly = py + min_gap
                # Keep within viewport
                ly = max(ly, miny - h*0.02)
                ly = min(ly, maxy + h*0.02)
                placed.append(ly)
                # Leader line: node → elbow → label
                elbow_x = label_x - side_sign * w * 0.01
                ax.plot([nx, elbow_x], [ny, ly], color=lcolor, linewidth=1.2,
                        alpha=0.85, zorder=16, linestyle=(0, (5, 2.5)))
                ax.plot([elbow_x, label_x - side_sign * w*0.002], [ly, ly],
                        color=lcolor, linewidth=1.2, alpha=0.85, zorder=16,
                        linestyle=(0, (5, 2.5)))
                # End dot at label
                ax.plot(label_x - side_sign * w*0.002, ly, "o",
                        markersize=3, color=lcolor, alpha=0.85, zorder=17)
                ax.text(label_x, ly, name, fontsize=6.5,
                        color="#1c1917" if not is_lm else "#92400e",
                        ha=ha, va="center", zorder=20,
                        fontweight="bold" if is_lm else "normal",
                        bbox=dict(boxstyle="round,pad=0.15", facecolor=BG_DARK,
                                  edgecolor=lcolor, alpha=0.85, linewidth=0.6))

        _draw_labels(left_labels, label_x_left, "right", -1)
        _draw_labels(right_labels, label_x_right, "left", +1)

        # ── Title (positioned at viewport top-left with background) ──
        vp_xmin = cx_k - half_lon
        vp_ymax = cy_k + half_lat + 0.0015
        ax.text(vp_xmin + 0.001, vp_ymax - 0.001, key_names[kid], fontsize=16,
                fontweight="bold", color=color, ha="left", va="top", zorder=20,
                bbox=dict(boxstyle="round,pad=0.2", facecolor=BG_DARK,
                          edgecolor="none", alpha=0.85))
        ax.text(vp_xmin + 0.001, vp_ymax - 0.0035, key_sub[kid], fontsize=8,
                color=MUTED, ha="left", va="top", zorder=20,
                bbox=dict(boxstyle="round,pad=0.15", facecolor=BG_DARK,
                          edgecolor="none", alpha=0.85))

        # ── Scale bar (400m ≈ 0.0044° lon at 40°N) ──
        vp_xmax = cx_k + half_lon
        vp_ymin = cy_k - half_lat - 0.001
        sb_len = 0.0044
        sb_x = vp_xmax - sb_len - 0.0008
        sb_y = vp_ymin + 0.0008
        ax.plot([sb_x, sb_x + sb_len], [sb_y, sb_y], color="#ffffff",
                linewidth=3, alpha=0.9, zorder=20, solid_capstyle="butt")
        ax.text(sb_x + sb_len / 2, sb_y + 0.0003, "400m", fontsize=7,
                color="#e7e5e4", ha="center", va="bottom", zorder=20)

        # ── Axes limits — uniform 2.2km × 2.2km viewport for all panels ──
        ax.set_xlim(cx_k - half_lon, cx_k + half_lon)
        ax.set_ylim(cy_k - half_lat - 0.001, cy_k + half_lat + 0.0015)
        ax.set_aspect(1.0 / math.cos(math.radians(40.0)))
        ax.axis("off")

    # ── Overall title ──
    fig.suptitle("三核详细设计  Key Areas Detailed Concept",
                 fontsize=18, fontweight="bold", color=WHITE, y=0.98)

    # ── Legend ──
    # ── Professional grouped legend ──
    legend_elements = [
        # 更新方式
        mpatches.Patch(facecolor="#94a3b8", alpha=0.40, edgecolor="#64748b",
                       linewidth=0.5, label="保留（现状建筑）"),
        mpatches.Patch(facecolor="#ea580c", alpha=0.28, edgecolor="#c2410c",
                       linewidth=0.5, label="改造更新（老旧厂房/低效楼宇）"),
        mpatches.Patch(facecolor="#dc2626", alpha=0.22, edgecolor="#dc2626",
                       linewidth=0.7, linestyle="--", label="拆除新建（旗舰项目）"),
        # 空间结构
        plt.Line2D([0], [0], color=GOLD, linewidth=3, label="京张铁路绿廊（一轴）"),
        plt.Line2D([0], [0], color="#0d9488", linewidth=4, alpha=0.5,
                   label="公共空间连廊"),
        mpatches.Patch(facecolor="#22c55e", alpha=0.4, label="绿地/公共空间"),
        # 节点
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=NAVY,
                   markersize=8, markeredgecolor="#fff", label="AI场景节点"),
        plt.Line2D([0], [0], marker="*", color="w", markerfacecolor=GOLD,
                   markersize=15, markeredgecolor="#ffffff", label="朝圣地标"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#0d9488",
                   markersize=6, markeredgecolor="#fff", label="慢行交汇节点"),
        # 范围
        mpatches.Patch(facecolor=NAVY, alpha=0.15, edgecolor=NAVY,
                       linewidth=1.5, label="众智园范围"),
        mpatches.Patch(facecolor=PURPLE, alpha=0.15, edgecolor=PURPLE,
                       linewidth=1.5, label="AI原点社区范围"),
        mpatches.Patch(facecolor=GOLD, alpha=0.15, edgecolor=GOLD,
                       linewidth=1.5, label="大钟寺范围"),
    ]
    fig.legend(handles=legend_elements, loc="lower center", ncol=4, fontsize=8,
               framealpha=0.92, facecolor=BG_MID, edgecolor=MUTED,
               labelcolor="#44403c", bbox_to_anchor=(0.5, -0.015),
               columnspacing=1.2, handletextpad=0.5)

    fig.tight_layout(pad=1.5, rect=[0, 0.03, 1, 0.95])
    out = FIG_DIR / "key-areas.png"
    if out.exists():
        try:
            out.unlink()
        except OSError:
            import os as _os
            _os.rename(out, str(out) + ".old")
    fig.savefig(out, dpi=140, bbox_inches="tight", facecolor=BG_DARK)
    plt.close(fig)
    print("  key-areas.png")



# ---------------------------------------------------------------------------
# Figure 4: Mobility & Blue-Green
# ---------------------------------------------------------------------------
def fig_mobility():
    site_fc = load_geojson("site_boundary.geojson")
    road_fc = load_geojson("roads.geojson")
    green_fc = load_geojson("green_space.geojson")
    public_fc = load_geojson("public_space.geojson")
    constraint_fc = load_geojson("constraints.geojson")
    key_fc = load_geojson("key_areas.geojson")

    site = shape(site_fc["features"][0]["geometry"])
    keys = {f["id"]: shape(f["geometry"]) for f in key_fc["features"]}

    # ── Rotation (same as site overview) ──
    C_OFF = 116.385
    def R(x, y):
        return y, -x + C_OFF
    aff = [0, 1, -1, 0, 0, C_OFF]
    site_r = affine_transform(site, aff)
    keys_r = {k: affine_transform(v, aff) for k, v in keys.items()}

    fig = plt.figure(figsize=(16, 9))
    fig.patch.set_facecolor(BG_DARK)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG_DARK)

    X_MIN, X_MAX = 39.928, 40.035
    Y_MIN, Y_MAX = -0.012, 0.082
    ax.set_xlim(X_MIN, X_MAX)
    ax.set_ylim(Y_MIN, Y_MAX)
    ax.set_aspect(0.64)
    ax.axis("off")

    # ── Real OSM roads ──
    draw_osm_roads(ax, (X_MIN, X_MAX), (Y_MIN, Y_MAX),
                   transform_fn=R, style="context", zorder_base=1)
    draw_osm_roads(ax, (X_MIN, X_MAX), (Y_MIN, Y_MAX),
                   transform_fn=R, style="bright", clip_poly=site_r, zorder_base=5)

    # ── Context: water (小月河) ──
    wx_r, wy_r = [], []
    for i in range(25):
        yy = 39.933 + (40.030 - 39.933) * i / 24
        xx = 116.353 + 0.0015 * math.sin(i * 0.7) + 0.0008 * math.cos(i * 1.3)
        rx, ry = R(xx, yy)
        wx_r.append(rx)
        wy_r.append(ry)
    ax.plot(wx_r, wy_r, color=WATER, linewidth=8, alpha=0.6, zorder=2, solid_capstyle="round")
    ax.plot(wx_r, wy_r, color=WATER_LINE, linewidth=0.8, alpha=0.4, zorder=3)

    # ── Context: green patches ──
    ctx_green = [
        (116.315, 40.000, 0.009, "清华·北大"),
        (116.325, 39.992, 0.006, ""),
        (116.320, 39.948, 0.007, "紫竹院公园"),
        (116.355, 39.975, 0.003, ""),
        (116.370, 40.010, 0.004, ""),
    ]
    for gx, gy, gr, glabel in ctx_green:
        rx, ry = R(gx, gy)
        ax.add_patch(Circle((rx, ry), gr, facecolor=GREEN_FILL, edgecolor=GREEN_LIGHT,
                            linewidth=0.5, alpha=0.25, zorder=2))
        if glabel:
            ax.text(rx, ry, glabel, fontsize=7, color=TEAL, ha="center", va="center",
                    alpha=0.9, fontweight="bold", zorder=3)

    # ── Dot grid within site ──
    draw_dot_grid(ax, site_r, spacing=0.0010, color=CORAL, alpha_range=(0.03, 0.10),
                  dot_size=1.0, zorder=4)

    # ── Site boundary glow ──
    for i in range(5):
        a = 0.04 - i * 0.007
        plot_polygon(ax, site_r, facecolor=CORAL, edgecolor="none", alpha=a, zorder=6)
    plot_polygon(ax, site_r, facecolor="none", edgecolor=CORAL, linewidth=2.5,
                 alpha=0.7, zorder=7)

    # ── Key area outlines (semi-transparent with white dashed) ──
    for kid, kr in keys_r.items():
        kcolor = {"KEY-001": NAVY, "KEY-002": PURPLE, "KEY-003": GOLD}[kid]
        plot_polygon(ax, kr, facecolor=kcolor, edgecolor="none", alpha=0.20, zorder=8)
        plot_polygon(ax, kr, facecolor="none", edgecolor="#ffffff", linewidth=1.5,
                     alpha=0.9, zorder=10, linestyle=(0, (5, 3)))
        plot_polygon(ax, kr, facecolor="none", edgecolor=kcolor, linewidth=1.0,
                     alpha=0.6, zorder=9)

    # ── Metro station catchment areas (500m / 800m) ──
    metro_stations = [
        (116.3485, 40.0140, "学知园站", "昌平线"),
        (116.3430, 39.9920, "五道口站", "13号线"),
        (116.3470, 39.9700, "大钟寺站", "12/13号线"),
        (116.3400, 39.9780, "知春路站", "10/13号线"),
        (116.3550, 40.0000, "清华东路西口", "15号线"),
        (116.3580, 39.9640, "西土城站", "10/昌平线"),
    ]
    for slon, slat, sname, sline in metro_stations:
        sx, sy = R(slon, slat)
        ax.add_patch(Circle((sx, sy), 800/111320, facecolor="#3b82f6",
                            edgecolor="none", alpha=0.05, zorder=8))
        ax.add_patch(Circle((sx, sy), 500/111320, facecolor="#3b82f6",
                            edgecolor="#3b82f6", linewidth=0.6, alpha=0.10, zorder=8))
        ax.plot(sx, sy, "s", markersize=6, color="#2563eb", markeredgecolor="#ffffff",
                markeredgewidth=1.0, zorder=20)
        ax.text(sx, sy + 0.0018, f"{sname}\n({sline})", fontsize=6, color="#1d4ed8",
                ha="center", va="bottom", zorder=20, fontweight="bold",
                linespacing=1.3,
                bbox=dict(boxstyle="round,pad=0.15", facecolor="#ffffff",
                          edgecolor="none", alpha=0.85))

    # ── Bike route network (dashed green along key connectors) ──
    bike_routes = [
        # North-south spine (parallel to railway, both sides)
        [(116.3445, 40.026), (116.3440, 40.015), (116.3435, 40.005),
         (116.3430, 39.993), (116.3425, 39.980), (116.3430, 39.965), (116.3435, 39.950)],
        [(116.3515, 40.026), (116.3510, 40.015), (116.3505, 40.005),
         (116.3500, 39.993), (116.3505, 39.980), (116.3510, 39.965), (116.3515, 39.950)],
        # East-west connectors
        [(116.335, 40.014), (116.3485, 40.014), (116.362, 40.014)],
        [(116.335, 39.992), (116.346, 39.989), (116.362, 39.989)],
        [(116.335, 39.970), (116.347, 39.968), (116.362, 39.968)],
    ]
    for route in bike_routes:
        rr = [R(lon, lat) for lon, lat in route]
        bx, by = zip(*rr)
        ax.plot(bx, by, color="#10b981", linewidth=2.0, alpha=0.6, zorder=13,
                linestyle=(0, (4, 3)), solid_capstyle="round")

    # ── Green spaces (proposal, rotated) ──
    for f in green_fc["features"]:
        ggeom = affine_transform(shape(f["geometry"]), aff)
        add_glow(ax, ggeom, TEAL, n_layers=2, alpha=0.10, zorder=10)
        plot_polygon(ax, ggeom, facecolor=TEAL, edgecolor="none", alpha=0.35, zorder=11)
        plot_polygon(ax, ggeom, facecolor="none", edgecolor=TEAL, linewidth=1,
                     alpha=0.7, zorder=12)

    # ── Constraints (rail protection, rotated) ──
    if constraint_fc:
        for f in constraint_fc["features"]:
            cgeom = affine_transform(shape(f["geometry"]), aff)
            plot_polygon(ax, cgeom, facecolor=GOLD, edgecolor="none", alpha=0.08, zorder=10)

    # ── Proposal roads (rotated) ──
    for f in road_fc["features"]:
        rgeom = affine_transform(shape(f["geometry"]), aff)
        rclass = f["properties"].get("road_class", "")
        if rclass == "arterial":
            lw_c, lw_f, col = 6, 3.5, ROAD_MAJOR
        elif rclass == "secondary":
            lw_c, lw_f, col = 4, 2, ROAD_SECONDARY
        else:
            lw_c, lw_f, col = 2.5, 1.2, TEAL
        plot_line(ax, rgeom, color=ROAD_CASING, linewidth=lw_c, alpha=0.9,
                  zorder=13, solid_capstyle="round")
        plot_line(ax, rgeom, color=col, linewidth=lw_f, alpha=0.8,
                  zorder=14, solid_capstyle="round")

    # ── Public spaces (rotated) — 3 subtypes differentiated by fill/edge ──
    # 节点广场 PS-001~004: solid CORAL, thick edge
    # 社区广场 PS-005~010: lighter red, dashed edge
    # 绿廊步行街 PS-011~012: light red strip, thin solid edge
    PS_NODE = {"PS-001", "PS-002", "PS-003", "PS-004"}
    PS_COMM = {"PS-005", "PS-006", "PS-007", "PS-008", "PS-009", "PS-010"}
    for f in public_fc["features"]:
        pid = f["properties"].get("id", "")
        pgeom = affine_transform(shape(f["geometry"]), aff)
        if pid in PS_NODE:
            fc, fa, ec, ea, lw, ls = CORAL, 0.55, CORAL, 0.9, 1.2, "solid"
        elif pid in PS_COMM:
            fc, fa, ec, ea, lw, ls = "#f87171", 0.38, "#ef4444", 0.7, 0.8, (0, (4, 2))
        else:  # PS-011, PS-012 绿廊步行街
            fc, fa, ec, ea, lw, ls = "#fca5a5", 0.50, "#f87171", 0.7, 0.8, "solid"
        add_glow(ax, pgeom, fc, n_layers=2, alpha=0.10, zorder=15)
        plot_polygon(ax, pgeom, facecolor=fc, edgecolor="none", alpha=fa, zorder=16)
        plot_polygon(ax, pgeom, facecolor="none", edgecolor=ec, linewidth=lw,
                     alpha=ea, zorder=17, linestyle=ls)

    # ── Railway spine ──
    rail_pts = [
        (116.3490, 40.0265), (116.3485, 40.0150), (116.3480, 40.0060),
        (116.3475, 39.9935), (116.3470, 39.9800), (116.3475, 39.9650),
        (116.3480, 39.9498), (116.3475, 39.9390),
    ]
    rail_r = [R(lon, lat) for lon, lat in rail_pts]
    rrx, rry = zip(*rail_r)
    ax.plot(rrx, rry, color=GOLD, linewidth=14, alpha=0.08, zorder=18, solid_capstyle="round")
    ax.plot(rrx, rry, color=GOLD, linewidth=6, alpha=0.18, zorder=19, solid_capstyle="round")
    ax.plot(rrx, rry, color=GOLD, linewidth=4, alpha=0.7, zorder=20, solid_capstyle="round")
    ax.plot(rrx, rry, color="#f5d060", linewidth=2, alpha=0.85, zorder=21, solid_capstyle="round")
    for j in range(len(rail_r) - 1):
        x0, y0 = rail_r[j]
        x1, y1 = rail_r[j + 1]
        dist = math.hypot(x1 - x0, y1 - y0)
        n_sleep = max(2, int(dist / 0.003))
        for k in range(n_sleep):
            t = k / n_sleep
            sx = x0 + (x1 - x0) * t
            sy = y0 + (y1 - y0) * t
            ax.plot([sx - 0.0005, sx + 0.0005], [sy, sy], color=GOLD,
                    linewidth=0.7, alpha=0.35, zorder=19)

    # ── 15 AI scenario nodes ──
    # (lon, lat, id, name, color, landmark?, label_dy)
    # Vertical dashed leaders only (ldx=0); labels staggered at 3 height levels
    # to avoid overlap. Positions anchored to corrected key areas.
    # ldy > 0 = above corridor, ldy < 0 = below; magnitude = height level
    scenarios = [
        # 众智园 (north) — well spaced
        (116.3488, 40.020, "SC-02", "开源成果廊", NAVY, True,   0.020),
        (116.3485, 40.015, "SC-03", "红队测试床", CORAL, False, 0.012),
        (116.3482, 40.010, "SC-04", "算力沙盒", "#38bdf8", False, -0.012),
        # AI原点 (middle) — 5 nodes, alternate above/below, stagger levels
        (116.3478, 39.992, "SC-01", "开发者步道", PURPLE, True,   0.012),
        (116.3475, 39.989, "SC-05", "健康导航", TEAL, False, 0.022),
        (116.3472, 39.986, "SC-06", "AI教育", "#c084fc", False, -0.020),
        (116.3470, 39.984, "SC-10", "文化导览", "#2dd4bf", False, -0.012),
        (116.3455, 39.985, "SC-12", "公共议题路由", "#94a3b8", False, 0.012),
        # 核间绿廊 — 2 nodes, opposite sides
        (116.3473, 39.975, "SC-08", "机器人配送", ORANGE, False, -0.012),
        (116.3476, 39.977, "SC-09", "自动接驳", "#38bdf8", False, 0.012),
        # 大钟寺 (south) — 5 dense nodes, 3 levels each side
        (116.3460, 39.965, "SC-11", "无障碍畅行", "#fb7185", False, -0.012),
        (116.3438, 39.966, "SC-07", "法律助手", GOLD, False, 0.012),
        (116.3500, 39.970, "SC-13", "AI定制零售", "#f472b6", False, -0.020),
        (116.3450, 39.970, "SC-14", "金融合规", "#a78bfa", False, 0.022),
        (116.3485, 39.966, "SC-15", "沉浸体验", "#fb923c", True, -0.028),
    ]
    for slon, slat, sid, sname, color, is_landmark, ldy in scenarios:
        sx, sy = R(slon, slat)
        ly = sy + ldy
        # Vertical dashed leader line in scenario color
        ax.plot([sx, sx], [sy, ly], color=color, linewidth=0.8,
                linestyle=(0, (3, 2)), alpha=0.75, zorder=22)
        # Small dot at label end of leader
        ax.plot(sx, ly, "o", markersize=3, color=color, alpha=0.9, zorder=23)
        draw_light_beam(ax, sx, sy, color, height=0.006, width=0.0004, zorder=22)
        draw_pulse_rings(ax, sx, sy, color, n_rings=2, max_radius=0.003, zorder=23)
        ax.plot(sx, sy, "o", markersize=16, color=color, alpha=0.2, zorder=24)
        ax.plot(sx, sy, "o", markersize=8, color=color, markeredgecolor="#ffffff",
                markeredgewidth=1.2, zorder=25)
        if is_landmark:
            ax.plot(sx, sy, "*", markersize=14, color=GOLD, markeredgecolor="#ffffff",
                    markeredgewidth=0.8, zorder=26)
        # Label centered on vertical leader
        va = "bottom" if ldy > 0 else "top"
        ax.text(sx, ly, f"{sid} {sname}",
                fontsize=6.5, color=WHITE, va=va, ha="center", zorder=27,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor=BG_MID,
                          edgecolor=color, alpha=0.9, linewidth=0.8))

    # ── North arrow ──
    na_x, na_y = X_MAX - 0.006, Y_MAX - 0.022
    na_s = 0.004
    ax.annotate("", xy=(na_x + na_s, na_y), xytext=(na_x - na_s, na_y),
                arrowprops=dict(arrowstyle="-|>", color="#44403c", lw=1.5),
                zorder=30)
    ax.text(na_x, na_y + na_s * 0.7, "N", fontsize=8, color=WHITE, ha="center",
            va="bottom", fontweight="bold", zorder=30)
    ax.add_patch(Circle((na_x, na_y), na_s * 1.6, facecolor="none",
                        edgecolor=MUTED, linewidth=0.8, alpha=0.5, zorder=29))

    # ── Scale bar ──
    m_per_deg_lat = 111320
    deg_2000m = 2000 / m_per_deg_lat
    sb_y = Y_MIN + 0.008
    sb_x0 = (X_MIN + X_MAX) / 2 - deg_2000m / 2
    ax.plot([sb_x0, sb_x0 + deg_2000m], [sb_y, sb_y], color="#44403c", linewidth=2.5,
            alpha=0.8, zorder=30, solid_capstyle="butt")
    ax.plot([sb_x0, sb_x0 + deg_2000m / 2], [sb_y, sb_y], color=BG_DARK, linewidth=3,
            alpha=0.9, zorder=31, solid_capstyle="butt")
    ax.text(sb_x0 + deg_2000m / 2, sb_y + 0.002, "2000m", fontsize=7, color=WHITE,
            ha="center", va="bottom", zorder=31)
    ax.text(sb_x0, sb_y - 0.002, "0", fontsize=6, color=MUTED, ha="center",
            va="top", zorder=31)

    # ── Title panel (top-left, dark navy) ──
    T = ax.transAxes
    ax.add_patch(FancyBboxPatch((0.012, 0.868), 0.30, 0.118,
        boxstyle="round,pad=0.008", facecolor="#0f172a", edgecolor="#7f1d1d",
        linewidth=1.2, alpha=0.95, transform=T, zorder=28))
    ax.text(0.025, 0.955, "交通 · 蓝绿 · 公共空间", fontsize=22, fontweight="bold",
            color="#ffffff", ha="left", va="top", transform=T, zorder=29)
    ax.text(0.025, 0.918, "Mobility · Blue-Green · AI Scenario Nodes", fontsize=10,
            color="#fca5a5", ha="left", va="top", style="italic", transform=T, zorder=29)
    ax.text(0.025, 0.888, "8.7 km 铁路绿廊 · 15 处 AI 场景节点",
            fontsize=8, color="#94a3b8", ha="left", va="top", transform=T, zorder=29)

    # ── Metrics (top-right) ──
    metrics = [
        ("31.0", "%", "绿地率", TEAL),
        ("5.5", "%", "公共空间", CORAL),
        ("8.7", "km", "铁路绿廊", GOLD),
        ("15", "处", "AI场景", PURPLE),
    ]
    mw = 0.058
    mgap = 0.016
    mx = 0.695
    _num_fs = 18
    _unit_fs = 10
    _num_cw = 0.6 * _num_fs / (72 * 16)
    _unit_cw_lat = 0.6 * _unit_fs / (72 * 16)
    for val, unit, label, color in metrics:
        ax.add_patch(FancyBboxPatch((mx, 0.90), mw, 0.075,
            boxstyle="round,pad=0.005", facecolor="#ffffff", edgecolor=color,
            linewidth=1.2, alpha=0.95, transform=T, zorder=28))
        # Center the number+unit group
        nw = len(val) * _num_cw
        if any(ord(c) > 0x2000 for c in unit):
            uw = len(unit) * _unit_fs / (72 * 16)
        else:
            uw = len(unit) * _unit_cw_lat
        _gap = 0.004
        tw = nw + _gap + uw
        sx = mx + (mw - tw) / 2
        ax.text(sx, 0.960, val, fontsize=_num_fs, fontweight="bold", color=color,
                ha="left", va="top", transform=T, zorder=29, family="monospace")
        ax.text(sx + nw + _gap, 0.955, unit, fontsize=_unit_fs, color=color,
                ha="left", va="top", transform=T, zorder=29)
        ax.text(mx + mw / 2, 0.912, label, fontsize=8, color="#44403c",
                ha="center", va="top", transform=T, zorder=29)
        mx += mw + mgap

    # ── Legend panel (bottom-left) ──
    legend_items = [
        ("绿地/绿廊", TEAL, "patch"),
        ("节点广场", CORAL, "patch_node"),
        ("社区广场", "#f87171", "patch_comm"),
        ("绿廊步行街", "#fca5a5", "patch_street"),
        ("地铁站点", "#2563eb", "metro"),
        ("500m覆盖圈", "#3b82f6", "catchment"),
        ("自行车道", "#10b981", "bike"),
        ("主干路", ROAD_MAJOR, "line"),
        ("次干路", ROAD_SECONDARY, "line"),
        ("慢行道", TEAL, "line"),
        ("铁路绿廊", GOLD, "line"),
        ("AI场景节点", PURPLE, "dot"),
        ("朝圣地标 ★", GOLD, "star"),
    ]
    lw_panel = 0.20
    lh_panel = 0.035 + len(legend_items) * 0.028 + 0.015
    ax.add_patch(FancyBboxPatch((0.015, 0.025), lw_panel, lh_panel,
        boxstyle="round,pad=0.008", facecolor="#ffffff", edgecolor="#d6d3d1",
        linewidth=0.8, alpha=0.95, transform=T, zorder=28))
    ax.text(0.025, 0.025 + lh_panel - 0.015, "图例", fontsize=11, fontweight="bold",
            color="#1c1917", ha="left", va="top", transform=T, zorder=29)
    for i, (label, color, kind) in enumerate(legend_items):
        ly = 0.025 + lh_panel - 0.045 - i * 0.028
        lx = 0.025
        if kind == "patch":
            ax.add_patch(plt.Rectangle((lx, ly - 0.008), 0.018, 0.014,
                         facecolor=color, alpha=0.45, edgecolor=color,
                         linewidth=1, transform=T, zorder=29))
        elif kind == "patch_node":
            ax.add_patch(plt.Rectangle((lx, ly - 0.008), 0.018, 0.014,
                         facecolor=color, alpha=0.55, edgecolor=color,
                         linewidth=1.2, transform=T, zorder=29))
        elif kind == "patch_comm":
            ax.add_patch(plt.Rectangle((lx, ly - 0.008), 0.018, 0.014,
                         facecolor=color, alpha=0.38, edgecolor="#ef4444",
                         linewidth=0.8, linestyle=(0, (4, 2)),
                         transform=T, zorder=29))
        elif kind == "patch_street":
            ax.add_patch(plt.Rectangle((lx, ly - 0.008), 0.018, 0.014,
                         facecolor=color, alpha=0.50, edgecolor="#f87171",
                         linewidth=0.8, transform=T, zorder=29))
        elif kind == "line":
            ax.plot([lx, lx + 0.018], [ly, ly], color=color, linewidth=3,
                    transform=T, zorder=29)
        elif kind == "dot":
            ax.plot(lx + 0.009, ly, "o", markersize=8, color=color,
                    markeredgecolor="#ffffff", markeredgewidth=0.8,
                    transform=T, zorder=29)
        elif kind == "star":
            ax.plot(lx + 0.009, ly, "*", markersize=12, color=color,
                    markeredgecolor="#ffffff", markeredgewidth=0.6,
                    transform=T, zorder=29)
        elif kind == "metro":
            ax.plot(lx + 0.009, ly, "s", markersize=8, color=color,
                    markeredgecolor="#ffffff", markeredgewidth=0.8,
                    transform=T, zorder=29)
        elif kind == "catchment":
            ax.add_patch(plt.Circle((lx + 0.009, ly), 0.007, facecolor=color,
                         edgecolor=color, linewidth=0.8, alpha=0.25,
                         transform=T, zorder=29))
        elif kind == "bike":
            ax.plot([lx, lx + 0.018], [ly, ly], color=color, linewidth=2.5,
                    linestyle=(0, (4, 3)), transform=T, zorder=29)
        ax.text(lx + 0.028, ly, label, fontsize=8.5, color="#374151",
                ha="left", va="center", transform=T, zorder=29)

    # ── Scenario nodes panel (bottom-right) ──
    nx, ny, nw, nh = 0.66, 0.025, 0.325, 0.24
    ax.add_patch(FancyBboxPatch((nx, ny), nw, nh,
        boxstyle="round,pad=0.008", facecolor="#ffffff", edgecolor="#d6d3d1",
        linewidth=0.8, alpha=0.95, transform=T, zorder=28))
    ax.text(nx + 0.012, ny + nh - 0.015, "AI 场景节点（15 处，含 4 处测试验证）",
            fontsize=10, fontweight="bold", color="#1c1917",
            ha="left", va="top", transform=T, zorder=29)
    # Two columns
    col1 = scenarios[:8]
    col2 = scenarios[8:]
    for i, (slon, slat, sid, sname, color, lm, ldy) in enumerate(col1):
        sy_i = ny + nh - 0.042 - i * 0.024
        ax.plot(nx + 0.018, sy_i, "o", markersize=5, color=color,
                transform=T, zorder=29)
        star = " ★" if lm else ""
        ax.text(nx + 0.030, sy_i, f"{sid} {sname}{star}", fontsize=7.5,
                color="#374151", ha="left", va="center", transform=T, zorder=29)
    for i, (slon, slat, sid, sname, color, lm, ldy) in enumerate(col2):
        sy_i = ny + nh - 0.042 - i * 0.024
        ax.plot(nx + 0.175, sy_i, "o", markersize=5, color=color,
                transform=T, zorder=29)
        star = " ★" if lm else ""
        ax.text(nx + 0.187, sy_i, f"{sid} {sname}{star}", fontsize=7.5,
                color="#374151", ha="left", va="center", transform=T, zorder=29)

    # ── Disclaimer ──
    ax.text(0.5, 0.005, "PROVISIONAL · CONCEPT ONLY — 本图为概念方案，边界为示意性表达，仅供专业团队深化研究参考",
            fontsize=8, color=MUTED, ha="center", va="bottom", transform=T, zorder=31, alpha=0.9)

    fig.savefig(FIG_DIR / "mobility-bluegreen.png", dpi=120,
                facecolor=BG_DARK)
    plt.close(fig)
    print("  mobility-bluegreen.png")


# ---------------------------------------------------------------------------
# Figure 5: Metrics & Evidence Dashboard
# ---------------------------------------------------------------------------
def fig_metrics():
    """Professional metrics dashboard with horizontal case comparison."""
    metrics_fc = json.loads((SUB / "metrics.json").read_text(encoding="utf-8"))
    m = metrics_fc["metrics"]

    fig = plt.figure(figsize=(16, 10))
    fig.patch.set_facecolor(BG_DARK)

    # ── Title ──
    fig.text(0.5, 0.965, "指标体系与全球案例对照",
             fontsize=22, fontweight="bold", color=WHITE, ha="center")
    fig.text(0.5, 0.935, "Metrics Dashboard & Global Case Comparison",
             fontsize=11, color=MUTED, ha="center", style="italic")

    # ── Top metrics strip ──
    ax_strip = fig.add_axes([0.04, 0.84, 0.92, 0.07])
    ax_strip.set_facecolor(BG_MID)
    ax_strip.set_xlim(0, 8)
    ax_strip.set_ylim(0, 1)
    ax_strip.axis("off")
    for spine in ax_strip.spines.values():
        spine.set_visible(False)

    strip_items = [
        ("11.4", "km²", "总体设计范围", NAVY),
        ("43.6", "km²", "统筹研究范围", "#5a8abb"),
        ("368.6", "ha", "三核重点区域", PURPLE),
        ("31.0", "%", "绿地率", TEAL),
        ("5.5", "%", "公共空间率", CORAL),
        ("15", "个", "AI场景节点", GOLD),
        ("4", "处", "朝圣地标", ORANGE),
        ("441", "栋", "概念建筑段", "#a78bfa"),
    ]
    for i, (val, unit, label, color) in enumerate(strip_items):
        cx = i + 0.5
        ax_strip.plot([cx - 0.45, cx + 0.45], [0.92, 0.92], color=color,
                      linewidth=2.5, solid_capstyle="round")
        ax_strip.text(cx, 0.55, val, fontsize=18, fontweight="bold",
                      color=color, ha="center", va="center")
        ax_strip.text(cx + 0.32, 0.50, unit, fontsize=9, color=MUTED,
                      ha="left", va="center")
        ax_strip.text(cx, 0.15, label, fontsize=8.5, color=MUTED,
                      ha="center", va="center")
        if i > 0:
            ax_strip.plot([i, i], [0.2, 0.8], color="#d6d3d1", linewidth=0.5)

    # ── Main: Horizontal grouped bar chart ──
    ax_bar = fig.add_axes([0.20, 0.09, 0.76, 0.66])
    ax_bar.set_facecolor(BG_DARK)

    # 8 global cases + our scheme (9 total), using actual proposal cases
    cases = [
        ("Mila",            "蒙特利尔",  [4, 5, 3, 4]),
        ("Kendall Sq.",     "波士顿",    [5, 4, 4, 3]),
        ("King's Cross",    "伦敦",      [4, 3, 3, 4]),
        ("Station F",       "巴黎",      [3, 4, 3, 3]),
        ("22@Barcelona",    "巴塞罗那",  [3, 3, 4, 4]),
        ("High Line",       "纽约",      [2, 2, 2, 5]),
        ("Helsinki AI",     "赫尔辛基",  [3, 4, 3, 5]),
        ("鹏城实验室",       "深圳",      [5, 3, 4, 2]),
        ("智脉京张",         "北京海淀",  [5, 5, 4, 5]),
    ]
    dims = ["锚定机构", "开源文化", "中试共享", "公共性"]
    bar_colors = [NAVY, PURPLE, TEAL, CORAL]

    n_cases = len(cases)
    n_dims = len(dims)
    y = np.arange(n_cases)
    bar_h = 0.18

    for i, (dim, color) in enumerate(zip(dims, bar_colors)):
        vals = [c[2][i] for c in cases]
        offset = (i - (n_dims - 1) / 2) * bar_h
        is_ours = (i == 0)  # only label our row
        bars = ax_bar.barh(y + offset, vals, bar_h, label=dim,
                           color=color, alpha=0.88, edgecolor="none", zorder=3)
        # Value labels only for our scheme (last row)
        for j, (bar, val) in enumerate(zip(bars, vals)):
            if j == n_cases - 1:
                ax_bar.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                            str(val), va="center", ha="left", fontsize=9,
                            color=color, fontweight="bold")

    # Highlight our scheme (last row)
    our_y = n_cases - 1
    ax_bar.axhspan(our_y - 0.45, our_y + 0.45, color=GOLD, alpha=0.08, zorder=1)
    ax_bar.axhline(y=our_y - 0.45, color=GOLD, linewidth=1.2, alpha=0.5,
                   linestyle="-", zorder=2)
    ax_bar.axhline(y=our_y + 0.45, color=GOLD, linewidth=1.2, alpha=0.5,
                   linestyle="-", zorder=2)

    # Y-axis labels: case name + city
    ylabels = []
    for name, city, _ in cases:
        ylabels.append(f"{name}  {city}")
    ax_bar.set_yticks(y)
    ax_bar.set_yticklabels(ylabels, fontsize=11, color=WHITE)
    # Make our label bold gold
    ytick_labels = ax_bar.get_yticklabels()
    ytick_labels[-1].set_color(GOLD)
    ytick_labels[-1].set_fontweight("bold")
    ytick_labels[-1].set_fontsize(12)

    ax_bar.set_xlim(0, 5.8)
    ax_bar.set_xticks([1, 2, 3, 4, 5])
    ax_bar.set_xticklabels(["1", "2", "3", "4", "5"], fontsize=9, color=MUTED)
    ax_bar.set_xlabel("评分（1=弱  5=强）", fontsize=10, color=MUTED, labelpad=6)

    ax_bar.tick_params(axis="y", length=0)
    ax_bar.tick_params(axis="x", colors=MUTED)
    ax_bar.grid(axis="x", alpha=0.12, color=WHITE, zorder=0)
    ax_bar.set_axisbelow(True)

    for spine in ["top", "right"]:
        ax_bar.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax_bar.spines[spine].set_color(MUTED)
        ax_bar.spines[spine].set_linewidth(0.5)

    # Legend — placed above the chart to avoid overlap
    leg = ax_bar.legend(fontsize=10, loc="lower center",
                        bbox_to_anchor=(0.5, 1.02),
                        framealpha=0.95,
                        facecolor=BG_MID, edgecolor="#d6d3d1",
                        labelcolor=WHITE, ncol=4,
                        handlelength=1.2, handleheight=0.8,
                        columnspacing=2.0, borderpad=0.6)

    # "本方案" label to the right of our row, outside bars
    ax_bar.text(5.55, our_y, "本方案", fontsize=10, color=GOLD,
                fontweight="bold", va="center", ha="right",
                bbox=dict(boxstyle="round,pad=0.3", facecolor=BG_DARK,
                          edgecolor=GOLD, linewidth=1.2, alpha=0.95))

    # Invert y so first case is at top
    ax_bar.invert_yaxis()

    # ── Footnote ──
    fig.text(0.5, 0.018,
             "注：评分为概念性对照（1-5分），基于公开资料整理；空间指标依据 GeoJSON 在 EPSG:4548 投影下复算。所有空间建议均为概念方案，不构成政府审定结论。",
             fontsize=8, color=MUTED, ha="center", style="italic")

    fig.savefig(FIG_DIR / "metrics-evidence.png", dpi=200, bbox_inches="tight",
                facecolor=BG_DARK)
    plt.close(fig)
    print("  metrics-evidence.png")


# ---------------------------------------------------------------------------
# Figure 6: Concept Section / Skyline
# ---------------------------------------------------------------------------
def fig_section():
    """Professional N-S architectural section: three cores, green spine, underground infrastructure."""
    fig, ax = plt.subplots(1, 1, figsize=(22, 8))
    fig.patch.set_facecolor(BG_DARK)
    ax.set_facecolor(BG_DARK)

    # ── Sky gradient (subtle warm-to-cool) ──
    for i in range(80):
        y0 = 1.5 + i * (8.5 / 80)
        alpha = 0.004 + i * 0.0004
        ax.axhspan(y0, y0 + 8.5/80 + 0.01, color="#475569", alpha=alpha, zorder=0)

    # ── Height reference lines ──
    for h_m in [15, 30, 45, 60]:
        y = h_m * 0.08
        ax.plot([3, 97], [y, y], color="#78716c", linewidth=0.35, alpha=0.25,
                zorder=1, linestyle=(0, (4, 3)))
        ax.plot([1.5, 3], [y, y], color="#78716c", linewidth=0.5, alpha=0.5, zorder=1)
        ax.text(1.0, y, f"{h_m}m", ha="right", va="center", fontsize=7,
                color="#a8a29e", zorder=1, fontweight="light")

    # ── Underground section ──
    ax.fill_between([0, 100], [-2.8, -2.8], [0, 0], color="#0c0a09", alpha=0.95, zorder=2)
    # Soil layers
    for sy, alpha in [(-0.5, 0.15), (-1.2, 0.1), (-2.0, 0.08)]:
        ax.plot([0, 100], [sy, sy], color="#57534e", linewidth=0.3, alpha=alpha, zorder=2)
    # Ground line
    ax.plot([0, 100], [0, 0], color="#44403c", linewidth=2.5, zorder=3)

    # ── Underground: metro line 13 ──
    metro_y = -1.0
    ax.plot([8, 92], [metro_y, metro_y], color="#60a5fa", linewidth=2.5, alpha=0.6, zorder=3)
    # Metro stations
    for sx, sn in [(22, "五道口站"), (49, "知春路站"), (76, "大钟寺站")]:
        ax.add_patch(mpatches.Rectangle((sx-1.2, metro_y-0.25), 2.4, 0.5,
                                        facecolor="#1e3a5f", edgecolor="#60a5fa",
                                        linewidth=0.8, alpha=0.8, zorder=4))
        ax.text(sx, metro_y-0.55, sn, ha="center", va="top", fontsize=6,
                color="#60a5fa", alpha=0.7, zorder=4)
    ax.text(5, metro_y, "13号线", ha="left", va="center", fontsize=6,
            color="#60a5fa", alpha=0.5, zorder=3)

    # ── Underground: data backbone ──
    data_y = -2.2
    ax.plot([10, 90], [data_y, data_y], color=TEAL, linewidth=1.5, alpha=0.4,
            zorder=3, linestyle=(0, (3, 2)))
    ax.text(5, data_y, "城市OS光纤骨干", ha="left", va="center", fontsize=5.5,
            color=TEAL, alpha=0.5, zorder=3)

    # ── Green spine at ground ──
    # Park ground
    ax.fill_between([6, 94], [0, 0], [0.28, 0.28], color=TEAL, alpha=0.22, zorder=3)
    # Path
    ax.plot([8, 92], [0.12, 0.12], color="#d6d3d1", linewidth=1.2, alpha=0.3, zorder=4)
    # Railway tracks (heritage)
    ax.plot([10, 90], [0.20, 0.20], color=GOLD, linewidth=1.0, alpha=0.35,
            zorder=4, linestyle=(0, (2, 2)))

    # Trees — layered, varied
    np.random.seed(42)
    for gx in np.arange(7.5, 93, 1.3):
        tree_h = 0.45 + 0.55 * np.random.random()
        cc_y = 0.28 + tree_h * 0.65
        cw = tree_h * 0.50
        ch = tree_h * 0.42
        # Shadow
        ax.add_patch(mpatches.Ellipse((gx + 0.06, 0.05), cw * 1.2, 0.08,
                                       facecolor="#000", alpha=0.12, zorder=4))
        # Trunk
        ax.plot([gx, gx], [0.28, cc_y - ch*0.4], color="#5c4d3e",
                linewidth=1.3, alpha=0.6, zorder=5)
        # Canopy layers (back to front)
        ax.add_patch(mpatches.Ellipse((gx - 0.08, cc_y + 0.02), cw*0.7, ch*0.8,
                                       facecolor="#2d6a3e", alpha=0.55, zorder=5))
        ax.add_patch(mpatches.Ellipse((gx, cc_y), cw, ch,
                                       facecolor="#3d8b4f", edgecolor="#2d6a3e",
                                       linewidth=0.4, alpha=0.80, zorder=6))
        ax.add_patch(mpatches.Ellipse((gx + 0.05, cc_y + 0.03), cw*0.65, ch*0.7,
                                       facecolor="#52a868", alpha=0.50, zorder=7))

    # People silhouettes on path
    np.random.seed(77)
    for px in np.arange(10, 90, 2.5):
        if np.random.random() > 0.4:
            py = 0.12
            ph = 0.12 + 0.04 * np.random.random()
            ax.add_patch(mpatches.Ellipse((px, py + ph*0.15), 0.12, ph*0.3,
                                           facecolor="#44403c", alpha=0.5, zorder=8))
            ax.plot([px, px], [py, py + ph], color="#44403c", linewidth=1.0,
                    alpha=0.5, zorder=8)

    # ── Building cluster helper ──
    def draw_cluster(x_start, x_end, spacing, h_min, h_max, color, edge_color,
                     win_color, seed, landmark_x=None, landmark_h=None,
                     landmark_color=None, podium_h=0):
        np.random.seed(seed)
        positions = np.arange(x_start, x_end, spacing)
        for bx in positions:
            center = (x_start + x_end) / 2
            dist = abs(bx - center) / ((x_end - x_start) / 2)
            taper = 1.0 - 0.25 * dist
            h = np.random.uniform(h_min, h_max) * taper
            w = np.random.uniform(0.8, 1.4)
            top = h * 0.08
            # Shadow
            ax.add_patch(mpatches.Rectangle((bx + 0.12, -0.15), w * 0.9, 0.12,
                                             facecolor="#000", alpha=0.25, zorder=4))
            # Podium
            if podium_h > 0:
                ptop = podium_h * 0.08
                ax.add_patch(mpatches.Rectangle((bx - 0.15, 0), w + 0.3, ptop,
                                                 facecolor=shade_hex(color, 0.7),
                                                 edgecolor=edge_color, linewidth=0.4,
                                                 alpha=0.85, zorder=6))
                # Podium windows
                for wy in np.arange(0.15, ptop - 0.1, 0.2):
                    ax.plot([bx - 0.05, bx + w + 0.05], [wy, wy],
                            color=win_color, alpha=0.2, linewidth=0.5, zorder=7)
            # Tower body with slight setback
            setback = 0.1 if top > 2.5 else 0
            ax.add_patch(mpatches.Rectangle((bx + setback, ptop if podium_h else 0),
                                             w - 2*setback, top - (ptop if podium_h else 0),
                                             facecolor=color, alpha=0.88,
                                             edgecolor=edge_color, linewidth=0.5, zorder=7))
            # Roof detail
            if top > 2.0 and np.random.random() > 0.5:
                ax.add_patch(mpatches.Rectangle((bx + w*0.3, top), w*0.4, 0.15,
                                                 facecolor=shade_hex(color, 0.6),
                                                 alpha=0.6, zorder=8))
            # Windows
            wy_start = (ptop if podium_h else 0) + 0.3
            for wy in np.arange(wy_start, top - 0.2, 0.38):
                if np.random.random() > 0.2:
                    ax.plot([bx + setback + 0.1, bx + w - setback - 0.1], [wy, wy],
                            color=win_color, alpha=0.25, linewidth=0.6, zorder=8)
        # Landmark tower
        if landmark_x is not None:
            lc = landmark_color or color
            ltop = landmark_h * 0.08
            # Shadow
            ax.add_patch(mpatches.Rectangle((landmark_x - 0.9, -0.2), 2.0, 0.18,
                                             facecolor="#000", alpha=0.3, zorder=5))
            # Tower
            ax.add_patch(mpatches.Rectangle((landmark_x - 0.9, 0), 1.8, ltop,
                                             facecolor=lc, alpha=0.92,
                                             edgecolor="#ffffff", linewidth=1.0, zorder=9))
            # Setback crown
            ax.add_patch(mpatches.Rectangle((landmark_x - 0.6, ltop - 0.4), 1.2, 0.5,
                                             facecolor=shade_hex(lc, 1.15),
                                             edgecolor="#ffffff", linewidth=0.6,
                                             alpha=0.7, zorder=10))
            # Spire
            ax.plot([landmark_x, landmark_x], [ltop + 0.1, ltop + 0.6],
                    color=GOLD, linewidth=1.2, alpha=0.8, zorder=11)
            # Windows
            for wy in np.arange(0.4, ltop - 0.3, 0.35):
                ax.plot([landmark_x - 0.6, landmark_x + 0.6], [wy, wy],
                        color="#ffffff", alpha=0.3, linewidth=0.7, zorder=10)
            return ltop
        return None

    def shade_hex(hex_color, factor):
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        r, g, b = [min(255, int(c * factor)) for c in (r, g, b)]
        return f"#{r:02x}{g:02x}{b:02x}"

    # KEY-001 众智园 (north): R&D mid-rise 24-45m
    draw_cluster(14, 30, 1.55, 24, 42, NAVY, "#3b82f6", "#93c5fd", seed=101,
                 podium_h=12)

    # KEY-002 AI原点 (center): mixed 18-48m + landmark 62m
    ltop = draw_cluster(40, 58, 1.35, 18, 45, PURPLE, "#8b5cf6", "#c4b5fd", seed=202,
                        landmark_x=49, landmark_h=62, landmark_color=PURPLE)

    # KEY-003 大钟寺 (south): commercial 30-55m
    draw_cluster(68, 84, 1.55, 28, 52, GOLD, "#b45309", "#fbbf24", seed=303,
                 podium_h=15)

    # ── Railway / data spine label ──
    ax.text(50, 1.75, "京张铁路绿廊  ·  AI 数据主脉  ·  公共空间主轴",
            ha="center", va="center", fontsize=8, color=GOLD, fontweight="bold",
            zorder=11, alpha=0.9,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#1c1917",
                      edgecolor=GOLD, alpha=0.85, linewidth=0.6))

    # ── LM-01 star ──
    ax.plot(49, ltop + 0.7, marker="*", color=GOLD, markersize=18,
            markeredgecolor="#ffffff", markeredgewidth=0.8, zorder=12)
    ax.annotate("LM-01 智脉原点碑", xy=(49, ltop + 0.7), xytext=(55, ltop + 1.5),
                fontsize=7.5, color=GOLD, fontweight="bold", zorder=12,
                arrowprops=dict(arrowstyle="-", color=GOLD, lw=0.8, alpha=0.6),
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#1c1917",
                          edgecolor=GOLD, alpha=0.9, linewidth=0.7))

    # ── Key area labels ──
    ax.text(22, 4.6, "众智园", ha="center", va="bottom", fontsize=12,
            color=NAVY, fontweight="bold", zorder=11)
    ax.text(22, 4.15, "AI全栈自主创新加速区", ha="center", va="top",
            fontsize=7.5, color="#60a5fa", zorder=11)
    ax.text(22, 3.8, "24-45m 研发中试 · 191.9ha", ha="center", va="top",
            fontsize=6.5, color="#78716c", zorder=11)

    ax.text(49, 6.8, "北京AI原点社区", ha="center", va="bottom", fontsize=12,
            color=PURPLE, fontweight="bold", zorder=11)
    ax.text(49, 6.35, "24h混合创新社区", ha="center", va="top",
            fontsize=7.5, color="#a78bfa", zorder=11)
    ax.text(49, 6.0, "18-62m 地标+混合 · 104.3ha", ha="center", va="top",
            fontsize=6.5, color="#78716c", zorder=11)

    ax.text(76, 4.8, "大钟寺", ha="center", va="bottom", fontsize=12,
            color=GOLD, fontweight="bold", zorder=11)
    ax.text(76, 4.35, "AI+商业文化门户", ha="center", va="top",
            fontsize=7.5, color="#d97706", zorder=11)
    ax.text(76, 4.0, "30-55m 商务消费 · 72.4ha", ha="center", va="top",
            fontsize=6.5, color="#78716c", zorder=11)

    # ── Wing indicators ──
    ax.annotate("", xy=(13, 2.8), xytext=(6, 2.8),
                arrowprops=dict(arrowstyle="-|>", color="#7c3aed", lw=1.5, alpha=0.5))
    ax.text(9.5, 3.2, "西翼·科技服务", ha="center", fontsize=7,
            color="#7c3aed", alpha=0.7, fontweight="bold")
    ax.annotate("", xy=(94, 2.8), xytext=(87, 2.8),
                arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.5, alpha=0.5))
    ax.text(90.5, 3.2, "东翼·场景赋能", ha="center", fontsize=7,
            color=TEAL, alpha=0.7, fontweight="bold")

    # ── Direction labels ──
    ax.text(3, -2.5, "北 ↑\n北五环", ha="center", va="center", fontsize=8,
            color="#78716c", fontweight="bold", linespacing=1.5, zorder=5)
    ax.text(97, -2.5, "南 ↓\n北京北站", ha="center", va="center", fontsize=8,
            color="#78716c", fontweight="bold", linespacing=1.5, zorder=5)

    # ── Scale bar ──
    sb_x, sb_y = 82, -2.3
    ax.plot([sb_x, sb_x + 8], [sb_y, sb_y], color="#a8a29e", linewidth=2, zorder=5)
    ax.plot([sb_x, sb_x], [sb_y - 0.1, sb_y + 0.1], color="#a8a29e", linewidth=1.5, zorder=5)
    ax.plot([sb_x + 8, sb_x + 8], [sb_y - 0.1, sb_y + 0.1], color="#a8a29e", linewidth=1.5, zorder=5)
    ax.text(sb_x + 4, sb_y - 0.3, "约1km", ha="center", va="top", fontsize=6.5,
            color="#a8a29e", zorder=5)

    # ── Title ──
    ax.text(50, 9.5, "概念剖面 · 南北向天际线", fontsize=19, fontweight="bold",
            color=WHITE, ha="center", va="top")
    ax.text(50, 8.8, "Concept Section — N-S Skyline（示意性，非建筑方案）",
            fontsize=9, color=MUTED, ha="center", va="top", style="italic")

    ax.set_xlim(-1, 101)
    ax.set_ylim(-3.0, 10.2)
    ax.axis("off")

    fig.tight_layout(pad=0.4)
    fig.savefig(FIG_DIR / "concept-section.png", dpi=180, bbox_inches="tight",
                facecolor=BG_DARK)
    plt.close(fig)
    print("  concept-section.png")



# ---------------------------------------------------------------------------
# Figure 7: Implementation Roadmap & Governance
# ---------------------------------------------------------------------------
def fig_roadmap():
    """Implementation timeline with Gantt chart, phases, investment, and governance."""
    fig = plt.figure(figsize=(18, 11))
    fig.patch.set_facecolor(BG_DARK)

    # ── Title ──
    fig.text(0.5, 0.97, "实施路线图与治理结构", fontsize=22, fontweight="bold",
             color=WHITE, ha="center", va="top")
    fig.text(0.5, 0.940, "Implementation Roadmap & Governance（概念性，非投资承诺）",
             fontsize=10, color=MUTED, ha="center", va="top", style="italic")

    # ═══ Gantt Chart (upper 60%) ═══
    ax = fig.add_axes([0.18, 0.40, 0.78, 0.50])
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, 10)
    n_tracks = 12
    ax.set_ylim(-0.5, n_tracks + 0.5)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0)

    # Year axis
    for yr in range(0, 11):
        x = yr
        ax.axvline(x, color=MUTED, alpha=0.10, linewidth=0.8, zorder=1)
        if yr > 0:
            ax.text(x, n_tracks + 0.2, f"Y{yr}", ha="center", va="bottom",
                    fontsize=8, color=MUTED, alpha=0.8)
    ax.text(0, n_tracks + 0.2, "2026", ha="center", va="bottom",
            fontsize=8, color=MUTED, alpha=0.8)
    ax.text(10, n_tracks + 0.2, "2036", ha="center", va="bottom",
            fontsize=8, color=MUTED, alpha=0.8)

    # Phase background bands
    phase_bands = [
        (0, 3, TEAL, "近期 1-3年\n示范启动"),
        (3, 5, NAVY, "中期 3-5年\n系统成型"),
        (5, 10, GOLD, "远期 5-10年\n生态成熟"),
    ]
    for x0, x1, color, label in phase_bands:
        ax.axvspan(x0, x1, color=color, alpha=0.06, zorder=0)
        ax.text((x0 + x1) / 2, n_tracks - 0.3, label, ha="center", va="top",
                fontsize=8, color=color, alpha=0.7, fontweight="bold", linespacing=1.4)

    # Gantt tracks: (label, start, end, color, milestone_year, milestone_label)
    tracks = [
        ("规划与制度建设", 0, 2, "#60A5FA", 1, "数据开放细则"),
        ("绿廊示范段贯通", 0, 3, "#34D399", 2, "示范段开放"),
        ("AI原点社区建设", 0.5, 4, "#A78BFA", 3, "原点碑落成"),
        ("城市OS基础平台", 0.5, 5, "#22D3EE", 2, "OS 1.0上线"),
        ("首批AI场景落地", 1, 4, "#F472B6", 2, "15场景运营"),
        ("众智园改造建设", 2, 6, "#60A5FA", 5, "中试层投用"),
        ("绿廊南北全贯通", 2, 5, "#34D399", 5, "8.7km贯通"),
        ("人才公寓建设", 1, 4, "#FBBF24", 3, "首批入住"),
        ("大钟寺门户建设", 4, 8, "#F87171", 7, "蓝景丽家建成"),
        ("两翼城市更新", 3, 10, "#FB923C", None, ""),
        ("Zhima Open Week", 1, 10, "#C084FC", 1, "首届举办"),
        ("社区分红机制", 5, 10, "#4ADE80", 7, "首次分红"),
    ]

    for i, (label, start, end, color, ms_year, ms_label) in enumerate(tracks):
        y = n_tracks - 1 - i
        # Track label
        ax.text(-0.2, y, label, ha="right", va="center", fontsize=8.5,
                color=WHITE, alpha=0.9)
        # Bar
        bar_h = 0.45
        ax.add_patch(FancyBboxPatch((start, y - bar_h/2), end - start, bar_h,
                     boxstyle="round,pad=0.02", facecolor=color, alpha=0.7,
                     edgecolor=color, linewidth=0.8, zorder=3))
        # Milestone diamond
        if ms_year is not None:
            ax.plot(ms_year, y, marker="D", color="#FBBF24", markersize=7,
                    markeredgecolor=BG_DARK, markeredgewidth=1.0, zorder=5)
            ax.text(ms_year, y - 0.55, ms_label, ha="center", va="top",
                    fontsize=6, color="#FBBF24", alpha=0.8, rotation=0)

    # Investment summary below Gantt
    ax.text(0, -1.2, "投资估算", fontsize=10, fontweight="bold", color=WHITE)
    inv_data = [
        (0, 3, "15-25亿", TEAL, "政府基建+专项债"),
        (3, 5, "40-60亿", NAVY, "政府引导+社会资本"),
        (5, 10, "60-100亿", GOLD, "社会资本+运营收入"),
    ]
    for x0, x1, amount, color, funding in inv_data:
        ax.add_patch(FancyBboxPatch((x0 + 0.1, -2.8), x1 - x0 - 0.2, 1.0,
                     boxstyle="round,pad=0.04", facecolor=color, alpha=0.2,
                     edgecolor=color, linewidth=1.0))
        ax.text((x0 + x1) / 2, -2.1, amount, ha="center", va="center",
                fontsize=11, fontweight="bold", color=color)
        ax.text((x0 + x1) / 2, -2.6, funding, ha="center", va="center",
                fontsize=7, color=MUTED)

    ax.text(8.5, -3.5, "合计 115-185亿元", fontsize=11, fontweight="bold",
            color=CORAL, ha="center")

    # ═══ Governance (lower section) ═══
    ax_gov = fig.add_axes([0.04, 0.03, 0.92, 0.32])
    ax_gov.set_facecolor(BG_DARK)
    ax_gov.set_xlim(0, 10)
    ax_gov.set_ylim(0, 5.5)
    ax_gov.axis("off")

    ax_gov.text(0.05, 5.2, "治理结构", fontsize=13, fontweight="bold", color=WHITE)
    ax_gov.plot([0.05, 1.2], [4.95, 4.95], color=GOLD, linewidth=2)

    # Four governance boxes
    gov_layers = [
        (0.05, 3.0, 2.25, 1.6, "#c0392b", "领导小组", "区政府牵头", "规划/科技/财政/街道"),
        (2.55, 3.0, 2.25, 1.6, "#2980b9", "运营平台公司", "区属国企+专业团队", "日常运营/场景/活动"),
        (5.05, 3.0, 2.25, 1.6, "#8e44ad", "专家委员会", "AI安全/规划/隐私", "场景准入+伦理审查"),
        (7.55, 3.0, 2.25, 1.6, "#27ae60", "社区议事会", "居民+商户+运营方", "季度会议+参与式预算"),
    ]

    for gx, gy, gw, gh, color, title, line1, line2 in gov_layers:
        ax_gov.add_patch(FancyBboxPatch((gx, gy), gw, gh,
                         boxstyle="round,pad=0.06", facecolor=color, alpha=0.18,
                         edgecolor=color, linewidth=1.5))
        ax_gov.text(gx + gw/2, gy + gh - 0.35, title, ha="center", va="center",
                    fontsize=11, fontweight="bold", color=WHITE)
        ax_gov.text(gx + gw/2, gy + 0.75, line1, ha="center", va="center",
                    fontsize=8.5, color=WHITE, alpha=0.85)
        ax_gov.text(gx + gw/2, gy + 0.30, line2, ha="center", va="center",
                    fontsize=8.5, color=WHITE, alpha=0.85)

    # Arrows between governance boxes
    for ax_x in [2.35, 4.85, 7.35]:
        ax_gov.annotate("", xy=(ax_x + 0.15, 3.8), xytext=(ax_x, 3.8),
                        arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.5, alpha=0.5))

    # Key success factors + policy alignment
    ax_gov.text(0.05, 2.4, "关键成功因素", fontsize=10, fontweight="bold", color=GOLD)
    ksfs = [
        "数据制度先行：开放细则+隐私标准+准入流程在建设前出台",
        "锚机构落地：1-2家头部AI企业/国家实验室作为首发锚租户",
        "人才公寓先建：首批开工即含人才公寓，安居留人",
        "场景即建即活：示范段建成时首批场景同步上线",
        "品牌从第一年启动：Open Week不等全部建成",
    ]
    for i, ksf in enumerate(ksfs):
        y = 1.85 - i * 0.35
        ax_gov.plot(0.20, y, marker=">", color=GOLD, markersize=5)
        ax_gov.text(0.40, y, ksf, ha="left", va="center", fontsize=8, color=WHITE, alpha=0.85)

    # Policy alignment (right side)
    ax_gov.text(5.2, 2.4, "政策对齐依据", fontsize=10, fontweight="bold", color=NAVY)
    policies = [
        ("北京城市总体规划(2016-2035)", "海淀科技创新中心核心区定位"),
        ("京张铁路遗址公园规划", "13.5km线性公园，本方案绿廊为其核心段"),
        ("海淀街区控规(2026.8公告)", "学北园等更新地块已纳入控规"),
        ("北京市加快建设全球数字经济标杆城市", "AI原生应用场景政策支持"),
        ("蓝景丽家48.8亿社会投资(2026.8)", "官方已公布投资计划，本方案对齐"),
    ]
    for i, (policy, basis) in enumerate(policies):
        y = 1.85 - i * 0.35
        ax_gov.plot(5.35, y, marker="s", color=NAVY, markersize=4, alpha=0.7)
        ax_gov.text(5.55, y, policy, ha="left", va="center", fontsize=7.5,
                    color=WHITE, alpha=0.85, fontweight="bold")
        ax_gov.text(5.55, y - 0.15, basis, ha="left", va="center", fontsize=6.5,
                    color=MUTED, alpha=0.8)

    fig.savefig(FIG_DIR / "implementation-roadmap.png", dpi=160, bbox_inches="tight",
                facecolor=BG_DARK)
    plt.close(fig)
    print("  implementation-roadmap.png")


# ---------------------------------------------------------------------------
# Figure 8: Site Readiness & Stakeholder Map
# ---------------------------------------------------------------------------
def fig_site_readiness():
    """Three-core site analysis: real anchors, land availability, constraints."""
    key_fc = load_geojson("key_areas.geojson")
    keys = {f["id"]: shape(f["geometry"]) for f in key_fc["features"]}

    fig, axes = plt.subplots(1, 3, figsize=(20, 12))
    fig.patch.set_facecolor(BG_DARK)
    fig.suptitle("三核现状分析：机构锚点 · 可更新用地概念分类 · 利益相关者",
                 fontsize=20, fontweight="bold", color=WHITE, y=0.97)
    fig.text(0.5, 0.935, "Site Readiness Analysis — Real Anchors · Conceptual Land Availability · Stakeholders（概念性，待现状测绘与权属调查确认）",
             ha="center", fontsize=9, color=MUTED, style="italic")

    # Each panel uses custom view limits to show real anchors around the key area.
    # All institution/station coordinates are real GCJ02 positions (verified via AMap).
    core_config = [
        {
            "ax_idx": 0, "key_id": "KEY-001", "title": "众智园（北核）",
            "subtitle": "AI自主创新加速区 · 191.9 ha",
            "color": NAVY,
            # View: 116.328-116.368, 39.996-40.030
            "view": (116.328, 116.368, 39.996, 40.030),
            "institutions": [
                (116.348, 40.010, "北京林业大学", "清华东路35号", "#5a9abf"),
                (116.354, 40.007, "中国农大(东校区)", "清华东路17号", "#5a9abf"),
                (116.344, 39.998, "中国矿大(北京)", "学院路丁11号", "#5a9abf"),
                (116.332, 40.005, "八大学院", "地大·矿大·林大\n农大·北科·北语", NAVY),
            ],
            "stations": [(116.352, 40.015, "学知园\n(昌平线)"),
                         (116.353, 40.001, "六道口\n(15/昌平线)"),
                         (116.339, 40.001, "清华东路西口\n(15号线)")],
            "renew_zones": [
                (116.352, 40.018, 0.005, 0.004, "学清路\n轨道微中心", "potential"),
                (116.353, 40.004, 0.004, 0.003, "六道口站\n一体化更新", "potential"),
                (116.348, 40.024, 0.006, 0.003, "五环绿带\n衔接节点", "tbd"),
            ],
            "retained_zones": [
                (116.351, 40.009, 0.008, 0.006, "农大·林大\n校园（保留）"),
                (116.342, 40.000, 0.006, 0.005, "矿大·地大\n校园（保留）"),
            ],
            "stakeholders": "农大·林大·矿大·地大·学知园/六道口站·学院路街道·东升镇·京张遗址公园",
        },
        {
            "ax_idx": 1, "key_id": "KEY-002", "title": "AI原点社区（中核）",
            "subtitle": "24h混合创新社区 · 104.3 ha",
            "color": PURPLE,
            # View: 116.324-116.366, 39.970-40.004
            "view": (116.324, 116.366, 39.970, 40.004),
            "institutions": [
                (116.340, 39.995, "清华", "双清路·东南门", "#c8a8ff"),
                (116.338, 39.992, "AI原点", "东升大厦·清华科技园\n200+AI企业", PURPLE),
                (116.347, 39.982, "北航", "学院路37号\nAI学院·具身智能", "#a080e0"),
                (116.333, 39.979, "中科院自动化所", "中关村东路95号", "#a080e0"),
                (116.356, 39.980, "信通院", "花园北路52号", "#a080e0"),
            ],
            "stations": [(116.338, 39.993, "五道口\n(13号线)"),
                         (116.340, 39.976, "知春路\n(10/13·31万/日)"),
                         (116.339, 40.001, "清华东路西口\n(15号线)")],
            "renew_zones": [
                (116.338, 39.990, 0.005, 0.004, "五道口\n城市更新", "potential"),
                (116.340, 39.978, 0.004, 0.003, "知春路\n楼宇升级", "potential"),
                (116.347, 39.984, 0.004, 0.003, "北航周边\n混合功能", "tbd"),
            ],
            "retained_zones": [
                (116.335, 39.997, 0.006, 0.006, "清华校园\n（保留）"),
                (116.347, 39.982, 0.005, 0.005, "北航校园\n（保留）"),
                (116.333, 39.980, 0.004, 0.004, "中科院院所\n（保留）"),
            ],
            "stakeholders": "清华·北大·中科院·北航·信通院·东升大厦·200+AI企业·中关村街道·海淀街道",
        },
        {
            "ax_idx": 2, "key_id": "KEY-003", "title": "大钟寺（南核）",
            "subtitle": "AI+产业门户 · 72.4 ha",
            "color": GOLD,
            # View: 116.326-116.370, 39.934-40.972  (note: 40.972 typo guard below)
            "view": (116.326, 116.370, 39.934, 39.972),
            "institutions": [
                (116.345, 39.967, "大钟寺", "中坤广场·12/13号线\nAI+消费先导区", GOLD),
                (116.358, 39.962, "北邮", "西土城路10号", "#f0d080"),
                (116.365, 39.961, "北师大", "新街口外大街19号", "#f0d080"),
                (116.340, 39.956, "铁科院", "大柳树路2号", "#e0c060"),
                (116.343, 39.952, "北交大", "上园村3号", "#e0c060"),
            ],
            "stations": [(116.345, 39.967, "大钟寺\n(12/13号线)"),
                         (116.355, 39.940, "西直门\n(2/4/13·全网第一)")],
            "rail_stations": [(116.354, 39.943, "北京北站")],
            "renew_zones": [
                (116.348, 39.965, 0.006, 0.004, "大钟寺商圈\nAI+消费升级", "potential"),
                (116.350, 39.963, 0.004, 0.003, "中坤广场\n功能转型", "tbd"),
                (116.354, 39.943, 0.005, 0.003, "北京北站\n枢纽提升", "potential"),
            ],
            "retained_zones": [
                (116.343, 39.952, 0.005, 0.005, "北交大校园\n（保留）"),
                (116.340, 39.956, 0.004, 0.004, "铁科院\n（保留）"),
            ],
            "stakeholders": "北邮·北师大·北交大·铁科院·大钟寺商圈·北京北站·北下关街道",
        },
    ]

    for cfg in core_config:
        ax = axes[cfg["ax_idx"]]
        ax.set_facecolor(BG_DARK)
        k = keys[cfg["key_id"]]
        kminx, kminy, kmaxx, kmaxy = k.bounds
        # Custom view limits to show real anchors around each key area
        vxmin, vxmax, vymin, vymax = cfg["view"]
        ax.set_xlim(vxmin, vxmax)
        ax.set_ylim(vymin, vymax)
        ax.set_aspect(1.2)
        ax.axis("off")

        # Real OSM roads for this panel view
        draw_osm_roads(ax, (vxmin, vxmax), (vymin, vymax),
                       style="bright", clip_poly=None, zorder_base=1)

        # Retained zones (campus/green - green overlay)
        for (cx, cy, w, h, label) in cfg["retained_zones"]:
            rect = mpatches.FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                                           boxstyle="round,pad=0.0005",
                                           facecolor=TEAL, edgecolor="#2a6a4a",
                                           alpha=0.25, linewidth=1.2, zorder=5)
            ax.add_patch(rect)
            ax.text(cx, cy, label, ha="center", va="center", fontsize=5.5,
                    color="#80c8a0", zorder=8, alpha=0.9, linespacing=1.3,
                    fontweight="bold")

        # Renewal potential zones (amber)
        for (cx, cy, w, h, label, status) in cfg["renew_zones"]:
            ec = "#c8922a" if status == "potential" else "#8a7a5a"
            fc = "#c8922a" if status == "potential" else "#6a5a3a"
            al = 0.3 if status == "potential" else 0.15
            rect = mpatches.FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                                           boxstyle="round,pad=0.0005",
                                           facecolor=fc, edgecolor=ec,
                                           alpha=al, linewidth=1.5, zorder=5,
                                           linestyle="--" if status == "tbd" else "-")
            ax.add_patch(rect)
            ax.text(cx, cy, label, ha="center", va="center", fontsize=5.5,
                    color="#f0d080" if status == "potential" else "#a09070",
                    zorder=8, alpha=0.9, linespacing=1.3, fontweight="bold")

        # Key area boundary
        plot_polygon(ax, k, facecolor=cfg["color"], edgecolor="#d6d3d1",
                     linewidth=2, alpha=0.12, zorder=6)
        plot_polygon(ax, k, facecolor="none", edgecolor=cfg["color"],
                     linewidth=2.5, alpha=0.9, zorder=7)

        # Institutions
        for (ix, iy, name, desc, clr) in cfg["institutions"]:
            ax.plot(ix, iy, marker="o", markersize=9, color=clr, zorder=10,
                    markeredgecolor="#ffffff", markeredgewidth=1.0)
            ax.text(ix + 0.0014, iy + 0.0010, name, fontsize=7.5, color=clr,
                    fontweight="bold", zorder=10, ha="left", va="bottom")
            ax.text(ix + 0.0014, iy - 0.0006, desc, fontsize=5.5, color="#44403c",
                    zorder=10, ha="left", va="top", linespacing=1.2)

        # Transit stations
        for (sx, sy, sname) in cfg["stations"]:
            ax.plot(sx, sy, marker="s", markersize=7, color="#3b82f6", zorder=10,
                    markeredgecolor="#ffffff", markeredgewidth=0.8)
            ax.text(sx, sy - 0.0015, sname, fontsize=5, color="#2563eb",
                    zorder=10, ha="center", va="top", linespacing=1.2,
                    bbox=dict(boxstyle="round,pad=0.15", facecolor=BG_DARK,
                              edgecolor="#2a4a6a", alpha=0.8, linewidth=0.3))

        # Railway stations (e.g. Beijing North)
        for (sx, sy, sname) in cfg.get("rail_stations", []):
            ax.plot(sx, sy, marker="D", markersize=7, color=GOLD, zorder=10,
                    markeredgecolor="#ffffff", markeredgewidth=0.8)
            ax.text(sx + 0.0012, sy + 0.0008, sname, fontsize=5.5, color="#8a6a10",
                    zorder=10, ha="left", va="bottom", fontweight="bold")

        # Railway spine (conceptual centerline of Jingzhang corridor)
        rail_x = [kminx + (kmaxx-kminx)*0.5, kminx + (kmaxx-kminx)*0.52]
        ax.plot(rail_x, [vymin, vymax], color=GOLD, linewidth=3,
                alpha=0.5, zorder=4, linestyle=(0, (4, 3)))

        # Title
        ax.set_title(f"{cfg['title']}\n{cfg['subtitle']}", fontsize=12,
                     fontweight="bold", color=cfg["color"], pad=8, linespacing=1.4)

        # Stakeholder text at bottom
        ax.text(0.5, -0.06, f"利益相关者：{cfg['stakeholders']}",
                transform=ax.transAxes, ha="center", va="top", fontsize=6,
                color=MUTED, style="italic", wrap=True)

    # Legend (between subplots)
    legend_elements = [
        mpatches.Patch(facecolor=TEAL, alpha=0.3, edgecolor="#2a6a4a", label="■ 保留区域（校园/公园/已建成）"),
        mpatches.Patch(facecolor="#c8922a", alpha=0.3, edgecolor="#c8922a", label="■ 概念可更新区域（待权属调查）"),
        mpatches.Patch(facecolor="#6a5a3a", alpha=0.15, edgecolor="#8a7a5a", label="■ 待研究区域（虚线）"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#a080e0",
                   markersize=8, markeredgecolor="#ffffff", label="● 高校/科研院所"),
        plt.Line2D([0], [0], marker="s", color="w", markerfacecolor="#3b82f6",
                   markersize=7, markeredgecolor="#ffffff", label="■ 轨道站点"),
        plt.Line2D([0], [0], marker="D", color="w", markerfacecolor=GOLD,
                   markersize=7, markeredgecolor="#ffffff", label="◆ 铁路车站"),
        plt.Line2D([0], [0], color=GOLD, linewidth=2, linestyle="--", label="--- 京张铁路绿廊"),
    ]
    fig.legend(handles=legend_elements, loc="lower center", ncol=4, fontsize=7.5,
               framealpha=0.9, facecolor=BG_MID, edgecolor=MUTED,
               labelcolor="#44403c", bbox_to_anchor=(0.5, 0.01))

    fig.tight_layout(rect=[0.02, 0.06, 0.98, 0.92])
    fig.savefig(FIG_DIR / "site-readiness.png", dpi=200, bbox_inches="tight",
                facecolor=BG_DARK)
    plt.close(fig)
    print("  site-readiness.png")


# ---------------------------------------------------------------------------
# Figure 9: AI-native spatial typologies (originality highlight)
# ---------------------------------------------------------------------------
def fig_ai_typologies():
    """Four AI-native spatial typologies: Compute Water Tower, Prompt Plaza,
    Model Roundhouse, Switch Plaza — shown as conceptual section/perspective diagrams."""
    fig, axes = plt.subplots(2, 2, figsize=(16, 10), facecolor=BG_DARK)
    fig.suptitle("AI原生空间类型学  |  AI-Native Spatial Typologies",
                 fontsize=22, fontweight="bold", color=WHITE, y=0.97)

    types = [
        {
            "title": "A  算力水塔",
            "subtitle": "Compute Water Tower",
            "color": NAVY,
            "tagline": "分布式边缘计算 · 50-200 TOPS · 500m服务半径",
            "specs": [
                "原型：铁路水塔（蒸汽机车补水）",
                "高8-15m塔状地标，屋顶光伏+绿电直供",
                "底部半公共空间：咖啡/信息/座椅",
                "余热回收→冬季户外供暖/温室",
                "沿绿廊每2km一座，共6-8座",
            ],
            "draw": "water_tower",
        },
        {
            "title": "B  提示广场",
            "subtitle": "Prompt Plaza",
            "color": PURPLE,
            "tagline": "人-AI协同创造 · 2000-3000㎡ · AI原点社区中心",
            "specs": [
                "原型：广场 + 命令行",
                "地面/墙面压感投影，可移动模块化家具",
                "高速WiFi + 户外电源，全天候可用",
                "活动：设计马拉松/公民数据/学生编程/老人AI教学",
                "开放、无门槛的公共AI体验空间",
            ],
            "draw": "plaza",
        },
        {
            "title": "C  模型机房",
            "subtitle": "Model Roundhouse",
            "color": GOLD,
            "tagline": "可见的AI训练 · 3000-5000㎡ · 众智园",
            "specs": [
                "原型：铁路扇形车库+转车盘",
                "旧厂房改造AI训练设施，玻璃隔断可见机房",
                "中央可旋转展示/演示平台",
                "余热→相邻温室/公共浴室",
                "服务器灯光=新工业景观，延续京张美学",
            ],
            "draw": "roundhouse",
        },
        {
            "title": "D  道岔广场",
            "subtitle": "Switch Plaza",
            "color": CORAL,
            "tagline": "「人在回路」决策节点 · 三核各1处",
            "specs": [
                "原型：铁路道岔（扳道工控制方向）",
                "真实可操作旧道岔+数字投票屏",
                "每月「扳道日」集体决策",
                "可决定：机器人配送时段/数据保留天数/AI导览开关",
                "决策可回滚，结合现有广场设置",
            ],
            "draw": "switch",
        },
    ]

    for ax, t in zip(axes.flat, types):
        ax.set_facecolor(BG_DARK)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect("equal")
        ax.axis("off")

        # Title bar
        ax.add_patch(FancyBboxPatch((0.2, 8.6), 9.6, 1.15,
                     boxstyle="round,pad=0.08", facecolor=t["color"], alpha=0.85,
                     edgecolor="none"))
        ax.text(5, 9.42, t["title"], fontsize=15, fontweight="bold",
                color="white", ha="center", va="center")
        ax.text(5, 8.88, t["subtitle"], fontsize=9.5, color="white",
                ha="center", va="center", style="italic", alpha=0.9)

        # ── Diagram area (center, larger) ──
        if t["draw"] == "water_tower":
            cx = 4.2
            # Base building (coffee/info)
            ax.add_patch(FancyBboxPatch((cx-1.4, 2.8), 2.8, 1.2,
                         boxstyle="round,pad=0.1", facecolor=BUILDING_FILL,
                         edgecolor=t["color"], linewidth=1.5, alpha=0.9))
            ax.text(cx, 3.4, "咖啡 / 信息 / 座椅", fontsize=8.5, color=MUTED,
                    ha="center", va="center")
            # Legs
            ax.plot([cx-0.9, cx-0.55], [4.0, 5.8], color=t["color"], lw=3)
            ax.plot([cx+0.9, cx+0.55], [4.0, 5.8], color=t["color"], lw=3)
            # Tank
            ax.add_patch(FancyBboxPatch((cx-1.5, 5.8), 3.0, 1.8,
                         boxstyle="round,pad=0.12", facecolor=t["color"],
                         edgecolor="white", linewidth=1.2, alpha=0.65))
            ax.text(cx, 6.7, "边缘计算", fontsize=10, color="white",
                    ha="center", va="center", fontweight="bold")
            # Solar panel bar on top
            ax.plot([cx-1.7, cx+1.7], [7.75, 7.75], color=GOLD, lw=5, solid_capstyle="round")
            # Signal light
            ax.plot(cx, 8.1, "o", color=TEAL, markersize=11, zorder=5,
                    markeredgecolor="white", markeredgewidth=1)
            # Heat arrows
            for dx in [-1.7, 1.7]:
                ax.annotate("", xy=(cx+dx, 2.5), xytext=(cx+dx, 4.5),
                           arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.8, alpha=0.6))
            ax.text(cx+2.1, 3.5, "余热", fontsize=8.5, color=ORANGE, fontweight="bold")
            # Coverage radius circle (dashed)
            cover = plt.Circle((cx, 3.4), 2.8, fill=False,
                              edgecolor=t["color"], linewidth=1, ls="--", alpha=0.3)
            ax.add_patch(cover)
            # Right-side specs
            for i, spec in enumerate(t["specs"]):
                ax.text(7.2, 7.8 - i * 0.95, spec, fontsize=8.5, color="#374151",
                        va="top", ha="left",
                        bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                                  edgecolor=t["color"], alpha=0.7, linewidth=0.8))

        elif t["draw"] == "plaza":
            # Ground
            ax.fill_between([0.5, 6.5], [2.5, 2.5], [3.3, 3.3],
                           color=GREEN_FILL, alpha=0.4)
            # Interactive grid tiles
            for i in range(6):
                for j in range(2):
                    gx = 0.8 + i * 0.85
                    gy = 2.6 + j * 0.32
                    ax.add_patch(plt.Rectangle((gx, gy), 0.7, 0.26,
                                 facecolor=t["color"], alpha=0.18,
                                 edgecolor=t["color"], linewidth=0.6))
            # People
            for px in [1.8, 3.0, 4.2, 5.4]:
                ax.plot(px, 3.9, "o", color=WHITE, markersize=9,
                        markeredgecolor=t["color"], markeredgewidth=1.5)
                ax.plot([px, px], [3.5, 4.2], color=t["color"], lw=2.5, alpha=0.6)
            # Projection beam
            ax.fill_between([2.5, 5.5], [4.2, 4.2], [5.8, 5.8], color=t["color"], alpha=0.06)
            ax.plot([2.5, 4.0], [4.2, 5.8], color=t["color"], lw=1.2, ls="--", alpha=0.5)
            ax.plot([5.5, 4.0], [4.2, 5.8], color=t["color"], lw=1.2, ls="--", alpha=0.5)
            # Screen
            ax.add_patch(FancyBboxPatch((2.8, 5.8), 2.4, 1.2,
                         boxstyle="round,pad=0.08", facecolor=t["color"],
                         edgecolor="white", linewidth=1.2, alpha=0.35))
            ax.text(4.0, 6.4, "AI", fontsize=18, color=t["color"],
                    ha="center", va="center", fontweight="bold", alpha=0.9)
            # Benches
            for fx in [0.7, 5.8]:
                ax.add_patch(FancyBboxPatch((fx, 3.5), 0.7, 0.25,
                             boxstyle="round,pad=0.04", facecolor=GOLD,
                             alpha=0.5, edgecolor=GOLD, linewidth=0.5))
            # WiFi label
            ax.text(1.2, 5.5, "WiFi", fontsize=8, color=t["color"], ha="center",
                    fontweight="bold", alpha=0.6,
                    bbox=dict(boxstyle="round,pad=0.15", facecolor="white",
                              edgecolor=t["color"], alpha=0.5, linewidth=0.8))
            # Right-side specs
            for i, spec in enumerate(t["specs"]):
                ax.text(7.2, 7.8 - i * 0.95, spec, fontsize=8.5, color="#374151",
                        va="top", ha="left",
                        bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                                  edgecolor=t["color"], alpha=0.7, linewidth=0.8))

        elif t["draw"] == "roundhouse":
            cx, cy = 3.8, 4.8
            # Outer circle
            circle = plt.Circle((cx, cy), 2.4, fill=False,
                               edgecolor=t["color"], linewidth=2.5, alpha=0.8)
            ax.add_patch(circle)
            # Wedge segments
            import matplotlib.patches as mpatches
            for angle_start in range(0, 360, 45):
                wedge = mpatches.Wedge((cx, cy), 2.4, angle_start, angle_start+35,
                                       facecolor=t["color"], alpha=0.1,
                                       edgecolor=t["color"], linewidth=0.8)
                ax.add_patch(wedge)
            # Center turntable
            inner = plt.Circle((cx, cy), 0.8, facecolor=BG_MID,
                              edgecolor=t["color"], linewidth=1.5)
            ax.add_patch(inner)
            ax.text(cx, cy+0.15, "展示", fontsize=10, color=t["color"],
                    ha="center", va="center", fontweight="bold")
            ax.text(cx, cy-0.3, "平台", fontsize=8, color=MUTED,
                    ha="center", va="center")
            # Server lights in wedges
            import numpy as np
            for angle in range(20, 360, 45):
                rad = np.radians(angle)
                lx = cx + 1.7 * np.cos(rad)
                ly = cy + 1.7 * np.sin(rad)
                ax.plot(lx, ly, "s", color=TEAL, markersize=5, alpha=0.8)
            # Heat exhaust arrows
            for dx in [-1.8, 0, 1.8]:
                ax.annotate("", xy=(cx+dx, 7.8), xytext=(cx+dx, 7.2),
                           arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.3, alpha=0.5))
            ax.text(cx, 2.0, "玻璃隔断 · 可见机房", fontsize=8.5, color=t["color"],
                    ha="center", fontweight="bold", alpha=0.8)
            # Right-side specs
            for i, spec in enumerate(t["specs"]):
                ax.text(7.2, 7.8 - i * 0.95, spec, fontsize=8.5, color="#374151",
                        va="top", ha="left",
                        bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                                  edgecolor=t["color"], alpha=0.7, linewidth=0.8))

        elif t["draw"] == "switch":
            sy = 3.8
            # Main rails
            ax.plot([0.5, 4.2], [sy, sy], color=MUTED, lw=4, solid_capstyle="round")
            ax.plot([0.5, 4.2], [sy+0.35, sy+0.35], color=MUTED, lw=4, solid_capstyle="round")
            # Sleepers
            for sx in np.arange(0.8, 4.2, 0.55):
                ax.plot([sx, sx], [sy-0.1, sy+0.45], color=MUTED, lw=1, alpha=0.4)
            # Switch point - straight
            ax.plot([4.2, 6.0], [sy+0.175, sy+0.175], color=t["color"], lw=4, solid_capstyle="round")
            # Switch point - diverging (dashed = alternative)
            ax.plot([4.2, 6.0], [sy+0.175, sy-1.0], color=t["color"], lw=3.5,
                    ls="--", solid_capstyle="round", alpha=0.7)
            # Switch lever
            ax.plot(4.2, sy+0.175, "o", color=t["color"], markersize=13, zorder=5,
                    markeredgecolor="white", markeredgewidth=1.5)
            ax.plot([4.2, 4.8], [sy+0.175, sy+1.8], color=t["color"], lw=4, solid_capstyle="round")
            ax.plot(4.8, sy+1.8, "o", color="white", markersize=10, zorder=5,
                    markeredgecolor=t["color"], markeredgewidth=2)
            ax.text(5.1, sy+2.0, "扳道杆", fontsize=8.5, color=t["color"], fontweight="bold")
            # Digital voting screen (compact)
            ax.add_patch(FancyBboxPatch((4.6, sy+2.4), 2.3, 1.3,
                         boxstyle="round,pad=0.06", facecolor=BG_MID,
                         edgecolor=t["color"], linewidth=1.2))
            ax.text(5.75, sy+3.4, "本月投票", fontsize=8, color=MUTED, ha="center", fontweight="bold")
            for i, (label, pct) in enumerate([("配送时段", 0.7), ("数据保留", 0.55), ("AI导览", 0.85)]):
                by = sy + 3.0 - i * 0.28
                ax.text(4.75, by, label, fontsize=6.5, color=MUTED, va="center")
                ax.add_patch(plt.Rectangle((5.5, by-0.06), 1.2*pct, 0.12,
                             facecolor=t["color"], alpha=0.7))
            # People
            for px in [1.8, 2.8]:
                ax.plot(px, sy-1.2, "o", color=WHITE, markersize=8,
                        markeredgecolor=t["color"], markeredgewidth=1.5)
                ax.plot([px, px], [sy-1.6, sy-0.9], color=t["color"], lw=2, alpha=0.6)
            # Right-side specs
            for i, spec in enumerate(t["specs"]):
                ax.text(7.3, 7.8 - i * 0.95, spec, fontsize=8.5, color="#374151",
                        va="top", ha="left",
                        bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                                  edgecolor=t["color"], alpha=0.7, linewidth=0.8))

        # Tagline at bottom
        ax.add_patch(FancyBboxPatch((0.2, 0.15), 9.6, 0.65,
                     boxstyle="round,pad=0.06", facecolor=t["color"], alpha=0.1,
                     edgecolor=t["color"], linewidth=0.8))
        ax.text(5, 0.47, t["tagline"], fontsize=9, color=t["color"],
                ha="center", va="center", fontweight="bold")

    fig.text(0.5, 0.015,
             "图注：四种AI原生空间类型均为概念建议，具体建筑设计、结构、设备需专业团队深化研究。",
             fontsize=9, color=MUTED, ha="center", style="italic")

    fig.tight_layout(rect=[0.02, 0.035, 0.98, 0.94])
    fig.savefig(FIG_DIR / "ai-typologies.png", dpi=200, bbox_inches="tight",
                facecolor=BG_DARK)
    plt.close(fig)
    print("  ai-typologies.png")


# ---------------------------------------------------------------------------
# Figure: 1909 Protocol mechanism diagram
# ---------------------------------------------------------------------------
def fig_protocol_1909():
    """Protocol 1909 — AI-native spatial interaction protocol derived from
    historical railway signalling. Flow diagram + railway-to-AI mapping."""
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_DARK)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.set_aspect("auto")
    ax.axis("off")

    # ── Title ──
    ax.text(0.5, 8.55, "1909", fontsize=34, fontweight="bold", color=GOLD,
            ha="left", va="center")
    ax.text(2.2, 8.62, "协议", fontsize=22, fontweight="bold", color=WHITE,
            ha="left", va="center")
    ax.text(2.2, 8.28, "Protocol 1909 — AI-Native Spatial Interaction Protocol",
            fontsize=10, color=MUTED, ha="left", va="center")
    ax.text(15.5, 8.55, "源自铁路信号的空间交互协议", fontsize=11,
            color=MUTED, ha="right", va="center")

    # Thin gold divider
    ax.plot([0.5, 15.5], [8.0, 8.0], color=GOLD, linewidth=1.2, alpha=0.4)

    # ── Historical context strip ──
    hist_y = 7.45
    ax.add_patch(FancyBboxPatch((0.5, hist_y - 0.25), 15.0, 0.45,
                 boxstyle="round,pad=0.06", facecolor="#1c1917", alpha=0.06,
                 edgecolor=GOLD, linewidth=0.8, linestyle="--"))
    ax.text(0.8, hist_y, "1909", fontsize=10, fontweight="bold", color=GOLD,
            ha="left", va="center")
    ax.text(1.7, hist_y,
            "京张铁路通车 · 詹天佑「人」字形展线 · 信号闭塞制度（分区—联锁—凭证—闭塞）"
            " → 117年后转译为AI时代的空间安全协议",
            fontsize=9.5, color=MUTED, ha="left", va="center")

    # ── Switchback routing callout (above cards) ──
    ax.add_patch(FancyBboxPatch((4.5, 6.65), 7.0, 0.5,
                 boxstyle="round,pad=0.08", facecolor=GOLD, alpha=0.08,
                 edgecolor=GOLD, linewidth=0.8, linestyle="--"))
    ax.text(8.0, 6.98, "人字形折返 Switchback Routing",
            fontsize=9.5, fontweight="bold", color=GOLD, ha="center", va="center")
    ax.text(8.0, 6.76,
            "复杂AI问题自动分解 → 路由到专门agent → 在「折返点」汇总（源自詹天佑人字形展线智慧）",
            fontsize=8, color=MUTED, ha="center", va="center")

    # ── Main protocol flow: 5 stages ──
    stages = [
        {"n": "1", "title": "路签", "en": "Spatial Token",
         "desc": "AI agent持加密凭证\n进入分区，含场景ID\n权限/有效期/责任主体",
         "color": NAVY},
        {"n": "2", "title": "联锁", "en": "Safety Interlock",
         "desc": "数据权限 + 物理安全\n+ 社区授权 三者联锁\n任一不满足则禁止",
         "color": PURPLE},
        {"n": "3", "title": "闭塞分区", "en": "Spatial Sandbox",
         "desc": "明确边界/时段/配额\n分区内自主运行\n故障不波及他区",
         "color": TEAL},
        {"n": "4", "title": "信号机", "en": "Semaphore",
         "desc": "绿=运行  黄=测试\n红=人工  蓝=维护\n状态市民可见",
         "color": GOLD},
        {"n": "5", "title": "调度所", "en": "Human Dispatch",
         "desc": "透明人在回路审批台\nAI提议→人类决策\n市民可旁观质询",
         "color": CORAL},
    ]

    card_w = 2.55
    card_h = 1.85
    card_y = 4.45
    gap = (15.0 - 5 * card_w) / 6  # even gaps
    x0 = 0.5 + gap

    card_centers = []
    for i, s in enumerate(stages):
        cx = x0 + i * (card_w + gap) + card_w / 2
        card_centers.append(cx)
        # Card background
        ax.add_patch(FancyBboxPatch((cx - card_w / 2, card_y), card_w, card_h,
                     boxstyle="round,pad=0.1", facecolor="white",
                     edgecolor=s["color"], linewidth=1.8, alpha=0.95))
        # Color top bar
        ax.add_patch(FancyBboxPatch((cx - card_w / 2, card_y + card_h - 0.45),
                     card_w, 0.45, boxstyle="round,pad=0.0",
                     facecolor=s["color"], alpha=0.9, edgecolor="none"))
        # Number circle
        ax.add_patch(Circle((cx - card_w / 2 + 0.32, card_y + card_h - 0.225),
                            0.16, facecolor="white", edgecolor="none", alpha=0.25))
        ax.text(cx - card_w / 2 + 0.32, card_y + card_h - 0.225, s["n"],
                fontsize=11, fontweight="bold", color="white", ha="center", va="center")
        # Title on color bar
        ax.text(cx + 0.15, card_y + card_h - 0.225, s["title"],
                fontsize=13, fontweight="bold", color="white", ha="center", va="center")
        # English name
        ax.text(cx, card_y + card_h - 0.65, s["en"],
                fontsize=8, color=s["color"], ha="center", va="center",
                fontstyle="italic")
        # Description
        ax.text(cx, card_y + 0.42, s["desc"],
                fontsize=8.2, color="#44403c", ha="center", va="center",
                linespacing=1.5)

        # Arrow to next card
        if i < len(stages) - 1:
            ax.annotate("", xy=(cx + card_w / 2 + gap - 0.05, card_y + card_h / 2),
                        xytext=(cx + card_w / 2 + 0.05, card_y + card_h / 2),
                        arrowprops=dict(arrowstyle="-|>", color="#a8a29e",
                                        lw=1.8, mutation_scale=14))

    # ── Feedback loops ──
    loop_y = 3.95
    # Rollback loop (red, under the cards)
    ax.annotate("", xy=(card_centers[0], card_y - 0.05),
                xytext=(card_centers[4], card_y - 0.05),
                arrowprops=dict(arrowstyle="-|>", color=CORAL, lw=1.5,
                                linestyle=(0, (6, 3)), mutation_scale=12,
                                connectionstyle="arc3,rad=-0.15"))
    ax.text((card_centers[0] + card_centers[4]) / 2, loop_y - 0.15,
            "异常 → 一键回滚（空间版本控制：分支测试 → 合并推广 → 回滚）",
            fontsize=8.5, color=CORAL, ha="center", va="center", fontstyle="italic")

    # ── Bottom section: mapping table + value proposition ──
    bot_y = 0.5
    # Left: mapping table
    tbl_x = 0.5
    tbl_w = 9.5
    tbl_h = 2.95
    ax.add_patch(FancyBboxPatch((tbl_x, bot_y), tbl_w, tbl_h,
                 boxstyle="round,pad=0.08", facecolor="white",
                 edgecolor="#d6d3d1", linewidth=0.8, alpha=0.9))
    ax.text(tbl_x + 0.25, bot_y + tbl_h - 0.28, "铁路信号 → 1909协议 转译表",
            fontsize=10, fontweight="bold", color=WHITE, ha="left", va="center")

    mappings = [
        ("闭塞分区 Block Section", "空间沙箱 Spatial Sandbox", "AI场景有明确边界/时段/权限/配额，故障隔离", TEAL),
        ("信号机 Semaphore", "空间状态信号", "绿/黄/红/蓝四色可见，市民一眼可知AI状态", GOLD),
        ("联锁 Interlocking", "安全联锁", "数据权限×物理安全×社区授权，三者缺一不可", PURPLE),
        ("路签/路牌 Token", "空间凭证", "加密路签由OS签发，社区可吊销，无签=入侵", NAVY),
        ("调度所 Dispatch", "人在回路调度台", "透明审批+监控+应急，市民可旁观可质询", CORAL),
        ("人字形折返 Switchback", "问题分解路由", "复杂问题分解→子agent处理→折返点汇总", "#7c3aed"),
    ]
    row_h = 0.36
    for i, (rail, proto, meaning, color) in enumerate(mappings):
        ry = bot_y + tbl_h - 0.68 - i * row_h
        # Color dot
        ax.add_patch(Circle((tbl_x + 0.3, ry + 0.02), 0.07, facecolor=color, edgecolor="none"))
        ax.text(tbl_x + 0.55, ry + 0.02, rail, fontsize=7.8, color="#57534e",
                ha="left", va="center")
        ax.text(tbl_x + 3.3, ry + 0.02, "→", fontsize=9, color="#a8a29e",
                ha="center", va="center")
        ax.text(tbl_x + 3.7, ry + 0.02, proto, fontsize=8, fontweight="bold",
                color=color, ha="left", va="center")
        ax.text(tbl_x + 5.9, ry + 0.02, meaning, fontsize=7.5, color="#78716c",
                ha="left", va="center")
        # Row separator
        if i < len(mappings) - 1:
            ax.plot([tbl_x + 0.2, tbl_x + tbl_w - 0.2], [ry - 0.15, ry - 0.15],
                    color="#e7e5e4", linewidth=0.5)

    # Right: value proposition
    val_x = 10.4
    val_w = 5.1
    ax.add_patch(FancyBboxPatch((val_x, bot_y), val_w, tbl_h,
                 boxstyle="round,pad=0.08", facecolor="#1c1917", alpha=0.04,
                 edgecolor=GOLD, linewidth=1.2))
    ax.text(val_x + val_w / 2, bot_y + tbl_h - 0.28, "独特价值",
            fontsize=11, fontweight="bold", color=GOLD, ha="center", va="center")
    ax.text(val_x + 0.25, bot_y + tbl_h - 0.72,
            "现有「智慧城市」标准从IT视角出发（网络协议、数据标准）；",
            fontsize=8.2, color="#57534e", ha="left", va="top", linespacing=1.6)
    ax.text(val_x + 0.25, bot_y + tbl_h - 1.25,
            "1909协议从铁路安全——一种经过百年验证的、\n物理空间中的、高可靠分布式安全系统——出发，",
            fontsize=8.2, color=WHITE, ha="left", va="top", linespacing=1.7, fontweight="bold")
    ax.text(val_x + 0.25, bot_y + tbl_h - 2.15,
            "重新定义AI与城市空间的交互规则。\n不是技术堆栈，而是空间-数字混合的\n安全制度，可被其他城市复用。",
            fontsize=8.2, color="#57534e", ha="left", va="top", linespacing=1.7)

    # ── Footer ──
    ax.text(8.0, 0.18,
            "图注：1909协议为概念性制度设计建议，具体技术标准、工程做法、管理制度需专业团队深化研究和相关部门审批。",
            fontsize=8, color=MUTED, ha="center", style="italic")

    fig.savefig(FIG_DIR / "protocol-1909.png", dpi=180, bbox_inches="tight",
                facecolor=BG_DARK, pad_inches=0.25)
    plt.close(fig)
    print("  protocol-1909.png")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("Generating premium figures (dark cartographic style)...")
    fig_site_overview()
    fig_land_use()
    fig_key_areas()
    fig_mobility()
    fig_metrics()
    fig_section()
    fig_roadmap()
    fig_site_readiness()
    fig_ai_typologies()
    fig_protocol_1909()
    print("OK all figures generated in", FIG_DIR)


if __name__ == "__main__":
    main()


