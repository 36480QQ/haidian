#!/usr/bin/env python3
"""Regenerate all figures and PDFs with CJK font support + professional urban design quality."""

import warnings
warnings.filterwarnings('ignore')

import json
import os
import hashlib
import numpy as np
from pathlib import Path
from shapely.geometry import shape
import pyproj
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Arc, Rectangle
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
import matplotlib.image as mpimg

# ── Coordinate Projection (EPSG:4326 → EPSG:4548 meters) ──
transformer = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:4548", always_xy=True)

def project_geom(geom):
    """Project a shapely geometry from EPSG:4326 to EPSG:4548 (meters)."""
    if geom.is_empty:
        return geom
    def transform_coords(coords):
        xs, ys = transformer.transform([c[0] for c in coords], [c[1] for c in coords])
        return list(zip(xs, ys))
    if geom.geom_type == 'Point':
        x, y = transformer.transform(geom.x, geom.y)
        from shapely.geometry import Point
        return Point(x, y)
    if geom.geom_type == 'LineString':
        return type(geom)(transform_coords(list(geom.coords)))
    if geom.geom_type == 'Polygon':
        ext = transform_coords(list(geom.exterior.coords))
        ints = [transform_coords(list(r.coords)) for r in geom.interiors]
        from shapely.geometry import Polygon
        return Polygon(ext, ints)
    if geom.geom_type == 'MultiPolygon':
        from shapely.ops import transform
        return transform(lambda x, y: transformer.transform(x, y), geom)
    if geom.geom_type == 'MultiLineString':
        from shapely.ops import transform
        return transform(lambda x, y: transformer.transform(x, y), geom)
    return geom

def project_feature(feat):
    """Return projected shapely geometry for a GeoJSON feature."""
    return project_geom(shape(feat['geometry']))

# ── Paths ──────────────────────────────────────────────
BASE = Path(__file__).parent
FIG_DIR = BASE / "assets" / "figures"
DRAW_DIR = BASE / "drawings"
GEO_DIR = BASE / "geometry"
FIG_DIR.mkdir(parents=True, exist_ok=True)
DRAW_DIR.mkdir(parents=True, exist_ok=True)

# ── Font Setup ──────────────────────────────────────────
# Use Heiti SC (System font on macOS with good CJK)
font_path = None
for fp in ['/System/Library/Fonts/STHeiti Light.ttc',
           '/System/Library/Fonts/STHeiti Medium.ttc',
           '/System/Library/Fonts/Supplemental/Songti.ttc',
           '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
           '/Library/Fonts/Arial Unicode.ttf']:
    if os.path.exists(fp):
        font_path = fp
        break

if font_path:
    fm.fontManager.addfont(font_path)
    font_prop = fm.FontProperties(fname=font_path)
    font_name = font_prop.get_name()
else:
    font_name = 'sans-serif'

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = [font_name, 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
# Handle bold weight with same font (many CJK fonts lack separate bold)
plt.rcParams['font.weight'] = 'normal'
print(f"Using font: {font_name} ({font_path})")

# ── Professional Urban Design Color Palette ─────────────
C = {
    'bg': '#FAFBFC',
    'dark': '#263238',
    'text': '#37474F',
    'muted': '#78909C',
    'light': '#ECEFF1',
    'grid': '#E0E0E0',

    # Land use colors (MNR-based)
    'lu_residential': '#F4A460',      # Warm brown-orange
    'lu_commercial': '#E57373',       # Soft red
    'lu_ai_rd': '#7E57C2',            # Creative purple
    'lu_green': '#66BB6A',            # Fresh green
    'lu_water': '#42A5F5',            # Water blue
    'lu_public': '#FFB74D',           # Amber public
    'lu_industry': '#90A4AE',         # Blue-gray
    'lu_mixed': '#4DB6AC',            # Teal

    # Key areas
    'key_1': '#2E7D32',  # Zhongzhiyuan - dark green
    'key_2': '#1565C0',  # AI Origin - blue
    'key_3': '#6A1B9A',  # Dazhongsi - purple

    # Infrastructure
    'road': '#546E7A',
    'slow': '#81C784',
    'site_fill': '#F5F5F5',
    'site_edge': '#37474F',

    # Water / ecology
    'water': '#BBDEFB',
    'water_edge': '#42A5F5',
    'green_fill': '#C8E6C9',
    'green_edge': '#43A047',

    # Chart colors
    'chart_1': '#2E7D32',
    'chart_2': '#1565C0',
    'chart_3': '#F57C00',
    'chart_4': '#7B1FA2',
    'chart_5': '#00897B',
    'chart_6': '#C62828',
}

# ── Load data ───────────────────────────────────────────
def load_geojson(name):
    with open(GEO_DIR / name) as f:
        return json.load(f)

site = load_geojson('site_boundary.geojson')
key_areas = load_geojson('key_areas.geojson')
land_use = load_geojson('land_use.geojson')
buildings = load_geojson('buildings.geojson')
roads = load_geojson('roads.geojson')
green_space = load_geojson('green_space.geojson')
public_space = load_geojson('public_space.geojson')
constraints = load_geojson('constraints.geojson')
phasing = load_geojson('phasing.geojson')

with open(BASE / 'metrics.json') as f:
    metrics = json.load(f)

# ── Helper: plot GeoJSON features ───────────────────────
def plot_feature(ax, feat, facecolor=None, edgecolor=None, linewidth=0.8,
                 alpha=1.0, zorder=2, hatch=None, linestyle='-', geom=None):
    if geom is None:
        geom = project_geom(shape(feat['geometry']))
    if geom.geom_type == 'Polygon':
        x, y = geom.exterior.xy
        if facecolor:
            ax.fill(x, y, facecolor=facecolor, edgecolor=edgecolor or facecolor,
                    linewidth=linewidth, alpha=alpha, zorder=zorder, hatch=hatch,
                    linestyle=linestyle)
        else:
            ax.plot(x, y, color=edgecolor or C['dark'], linewidth=linewidth,
                    zorder=zorder, linestyle=linestyle)
    elif geom.geom_type == 'MultiPolygon':
        for poly in geom.geoms:
            x, y = poly.exterior.xy
            if facecolor:
                ax.fill(x, y, facecolor=facecolor, edgecolor=edgecolor or facecolor,
                        linewidth=linewidth, alpha=alpha, zorder=zorder, hatch=hatch,
                        linestyle=linestyle)
            else:
                ax.plot(x, y, color=edgecolor or C['dark'], linewidth=linewidth,
                        zorder=zorder, linestyle=linestyle)

def plot_line(ax, feat, color, linewidth=1.5, zorder=3, linestyle='-', alpha=1.0):
    geom = project_geom(shape(feat['geometry']))
    if geom.geom_type == 'LineString':
        x, y = geom.xy
        ax.plot(x, y, color=color, linewidth=linewidth, zorder=zorder, linestyle=linestyle, alpha=alpha)
    elif geom.geom_type == 'MultiLineString':
        for line in geom.geoms:
            x, y = line.xy
            ax.plot(x, y, color=color, linewidth=linewidth, zorder=zorder, linestyle=linestyle, alpha=alpha)

def plot_patch_xy(ax, xy, facecolor, edgecolor='none', linewidth=0, alpha=1.0, zorder=0):
    """Plot a rectangle given by (x_min, y_min, x_max, y_max) in projected coords."""
    x_min, y_min, x_max, y_max = xy
    ax.add_patch(Rectangle((x_min, y_min), x_max - x_min, y_max - y_min,
                            facecolor=facecolor, edgecolor=edgecolor,
                            linewidth=linewidth, alpha=alpha, zorder=zorder))

def add_north_arrow(ax, x, y, size=200, color=C['dark'], fontsize=9):
    """Add a simple north arrow in projected coordinates."""
    ax.annotate('N', xy=(x, y), xytext=(x, y + size * 1.5),
                fontsize=fontsize, fontweight='bold', color=color,
                ha='center', va='bottom',
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))

def add_scale_bar(ax, extent, y_pos_frac=0.03, x_pos_frac=0.08,
                  fontsize=8, crs_fontsize=6):
    """Add a metric scale bar."""
    x_min, x_max, y_min, y_max = extent
    x_range = x_max - x_min
    # Choose a nice round distance in meters
    nice = [500, 1000, 1500, 2000, 2500, 3000, 5000]
    target = x_range * 0.15
    scale_m = min(nice, key=lambda d: abs(d - target))
    base_x = x_min + x_range * x_pos_frac
    base_y = y_min + (y_max - y_min) * y_pos_frac
    # White halo for legibility
    ax.plot([base_x, base_x + scale_m], [base_y, base_y],
            color='white', linewidth=5.5, solid_capstyle='butt', zorder=8)
    ax.plot([base_x, base_x + scale_m], [base_y, base_y],
            color=C['dark'], linewidth=3, solid_capstyle='butt', zorder=9)
    tick_h = (y_max - y_min) * 0.008
    ax.plot([base_x, base_x], [base_y - tick_h, base_y + tick_h],
            color=C['dark'], linewidth=2, zorder=9)
    ax.plot([base_x + scale_m, base_x + scale_m],
            [base_y - tick_h, base_y + tick_h],
            color=C['dark'], linewidth=2, zorder=9)
    ax.text(base_x + scale_m/2, base_y - tick_h * 2.2,
            f'{scale_m/1000:.1f} km', ha='center', fontsize=fontsize, fontweight='bold',
            color=C['dark'], zorder=10)
    # Add a CRS note near scale bar
    ax.text(base_x, base_y - tick_h * 5,
            'EPSG:4548', fontsize=crs_fontsize, color=C['muted'], zorder=10)

def set_map_style(ax, extent):
    """Apply clean map style with metric grid, no axis labels."""
    ax.set_xlim(extent[0], extent[1])
    ax.set_ylim(extent[2], extent[3])
    ax.set_aspect('equal')
    ax.set_facecolor(C['bg'])
    ax.grid(True, linestyle='--', alpha=0.25, color=C['grid'], linewidth=0.3)
    # No axis labels for clean presentation; scale bar provides reference
    ax.tick_params(labelbottom=False, labelleft=False, length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    # Remove any existing labels
    ax.set_xlabel('')
    ax.set_ylabel('')

def latlon_to_m(lon, lat):
    return transformer.transform(lon, lat)

def project_bounding_box(min_lon, min_lat, max_lon, max_lat):
    x1, y1 = transformer.transform(min_lon, min_lat)
    x2, y2 = transformer.transform(max_lon, max_lat)
    return (x1, y1, x2, y2)

# Water approx northern boundary (lat ~ 40.02)
_, WATER_NORTH_Y = latlon_to_m(116.34, 40.02)

# ── Determine map extent ────────────────────────────────
def get_extent(padding=300):
    all_x, all_y = [], []
    for feat in site['features']:
        g = project_geom(shape(feat['geometry']))
        minx, miny, maxx, maxy = g.bounds
        all_x.extend([minx, maxx]); all_y.extend([miny, maxy])
    return (min(all_x)-padding, max(all_x)+padding,
            min(all_y)-padding, max(all_y)+padding)

extent = get_extent()

# ── Figure 1: Site Overview ─────────────────────────────
def fig_site_overview(lang='zh'):
    is_zh = (lang == 'zh')
    title_main = '场地总览' if is_zh else 'Site Overview'
    title_sub = '京张AI创新带 — 总体设计范围 (11.4 km²)' if is_zh else 'Jing-Zhang AI Innovation Belt — Design Area (11.4 km²)'
    legend_title = '图例' if is_zh else 'Legend'
    legend_site = '总体设计范围' if is_zh else 'Design Boundary'
    legend_key = '重点区域' if is_zh else 'Key Areas'
    legend_water = '水域' if is_zh else 'Water'
    legend_green = '绿脉公园' if is_zh else 'Green Park'
    legend_road = '主要道路' if is_zh else 'Major Roads'
    key_names = {
        '众智园AI自主创新加速区': '众智园' if is_zh else 'Zhongzhiyuan',
        '北京AI原点社区': 'AI原点社区' if is_zh else 'AI Origin',
        '大钟寺国际 AI 交流节点': '大钟寺' if is_zh else 'Dazhongsi',
    }
    key_colors_map = {
        '众智园AI自主创新加速区': C['key_1'],
        '北京AI原点社区': C['key_2'],
        '大钟寺国际 AI 交流节点': C['key_3'],
    }

    # Portrait layout matching the north-south corridor shape
    fig = plt.figure(figsize=(9.5, 12), dpi=150, facecolor='white')
    gs = fig.add_gridspec(1, 1, left=0.08, right=0.74, top=0.93, bottom=0.05)
    ax = fig.add_subplot(gs[0])

    # Draw site boundary
    for feat in site['features']:
        plot_feature(ax, feat, facecolor=C['site_fill'], edgecolor=C['site_edge'],
                     linewidth=1.8, alpha=0.7, zorder=1)

    # Draw water context (approx area around north)
    plot_patch_xy(ax, (extent[0], WATER_NORTH_Y, extent[1], extent[3]),
                  facecolor=C['water'], alpha=0.4, zorder=0)

    # Draw green space
    for feat in green_space['features']:
        plot_feature(ax, feat, facecolor=C['green_fill'], edgecolor=C['green_edge'],
                     linewidth=0.4, alpha=0.6, zorder=2)

    # Draw roads
    for feat in roads['features']:
        rtype = feat['properties'].get('road_type', '')
        lw = 2.5 if rtype in ('expressway','arterial') else 1.5
        if rtype == 'slow_mobility':
            plot_line(ax, feat, C['slow'], linewidth=2.5, zorder=4, linestyle='--')
        else:
            plot_line(ax, feat, C['road'], linewidth=lw, zorder=3)

    # Draw key areas
    for feat in key_areas['features']:
        n_zh = feat['properties']['name_zh']
        lc = key_colors_map.get(n_zh, C['key_1'])
        plot_feature(ax, feat, facecolor=lc, edgecolor=lc,
                     linewidth=1.5, alpha=0.25, zorder=3)
        # Projected centroid
        g = project_geom(shape(feat['geometry']))
        cx, cy = g.centroid.x, g.centroid.y
        label = key_names.get(n_zh, n_zh[:8])
        ax.annotate(label, xy=(cx, cy), fontsize=8, fontweight='bold',
                    color=lc, ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                              edgecolor=lc, alpha=0.9, linewidth=1),
                    zorder=10)

    set_map_style(ax, extent)
    add_north_arrow(ax, extent[0]+250, extent[3]-500)
    add_scale_bar(ax, extent, y_pos_frac=0.04)

    # Title
    fig.suptitle(title_main, fontsize=20, fontweight='bold', color=C['dark'], y=0.98, x=0.41)
    fig.text(0.41, 0.945, title_sub, fontsize=11, color=C['muted'], ha='center')

    # Legend (right side)
    legend_ax = fig.add_axes([0.78, 0.12, 0.18, 0.70])
    legend_ax.set_xlim(0, 1); legend_ax.set_ylim(0, 1)
    legend_ax.axis('off')
    legend_ax.text(0.08, 0.97, legend_title, fontsize=10, fontweight='bold', color=C['dark'])

    items = [
        (C['site_fill'], C['site_edge'], legend_site),
        (C['key_1'], C['key_1'], legend_key),
        (C['green_fill'], C['green_edge'], legend_green),
        (C['water'], C['water_edge'], legend_water),
        (C['road'], C['road'], legend_road),
    ]
    for i, (fc, ec, label) in enumerate(items):
        y = 0.88 - i * 0.12
        legend_ax.add_patch(Rectangle((0.05, y-0.04), 0.15, 0.06, facecolor=fc,
                                      edgecolor=ec, linewidth=0.8))
        legend_ax.text(0.25, y-0.01, label, fontsize=8.5, color=C['text'], va='center')

    # Source note
    fig.text(0.41, 0.015, 'Source: OpenStreetMap (ODbL) + Provisional Site Boundary',
             fontsize=7, color=C['muted'], ha='center')

    out = FIG_DIR / f'site-overview{"" if is_zh else ".en"}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  Saved: {out}")
    return out


# ── Figure 2: Land Use Structure ────────────────────────
def fig_land_use(lang='zh'):
    is_zh = (lang == 'zh')
    title_main = '用地结构' if is_zh else 'Land Use Structure'
    title_sub = '概念功能分区 — 一带·三芯·两翼' if is_zh else 'Conceptual Zoning — One Belt · Three Cores · Two Wings'
    legend_title = '用地类型' if is_zh else 'Land Use Type'

    # MNR code -> color + label
    lu_labels = {
        '0701': ('创新生活社区', 'Innovation Living', C['lu_residential']),
        '08': ('公共管理与服务', 'Public Service', C['lu_public']),
        '0802': ('AI核心创新区', 'AI Core Innovation', C['lu_ai_rd']),
        '1401': ('绿脉公园带', 'Green Park Belt', C['lu_green']),
        '16': ('蓝绿生态腹地', 'Blue-Green Hinterland', C['lu_water']),
        '05': ('智慧服务走廊', 'Smart Service Corridor', C['lu_commercial']),
    }

    # Map feature name_zh to code
    name_to_code = {}
    for feat in land_use['features']:
        n = feat['properties']['name_zh']
        code = feat['properties']['land_use_code']
        if 'AI核心' in n: name_to_code[n] = '0802'
        elif '创新生活' in n: name_to_code[n] = '0701'
        elif '智慧服务' in n: name_to_code[n] = '05'
        elif '产业融合' in n: name_to_code[n] = '05'
        elif '公共管理' in n: name_to_code[n] = '08'
        elif '蓝绿' in n: name_to_code[n] = '16'
        else: name_to_code[n] = code

    used_codes = set(name_to_code.values())

    fig = plt.figure(figsize=(9.5, 12), dpi=150, facecolor='white')
    gs = fig.add_gridspec(1, 1, left=0.08, right=0.74, top=0.93, bottom=0.05)
    ax = fig.add_subplot(gs[0])

    # Draw land use zones
    for feat in land_use['features']:
        n_zh = feat['properties']['name_zh']
        code = name_to_code.get(n_zh, feat['properties']['land_use_code'])
        info = lu_labels.get(code)
        if info:
            lc = info[2]
            label_text = info[0] if is_zh else info[1]
        else:
            lc = C['lu_industry']
            label_text = n_zh[:6]
        plot_feature(ax, feat, facecolor=lc, edgecolor='white',
                     linewidth=0.6, alpha=0.7, zorder=2)
        # Small label using projected centroid
        g = project_geom(shape(feat['geometry']))
        cx, cy = g.centroid.x, g.centroid.y
        short_label = label_text[:6]
        ax.annotate(short_label, xy=(cx, cy), fontsize=6.5, color='white',
                    fontweight='bold', ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.15', facecolor=lc, alpha=0.85, edgecolor='none'),
                    zorder=8)

    # Draw roads overlay
    for feat in roads['features']:
        rtype = feat['properties'].get('road_type', '')
        lw = 1.8 if rtype in ('expressway','arterial') else 1.0
        plot_line(ax, feat, 'white', linewidth=lw+1.5, zorder=3)
        plot_line(ax, feat, C['road'], linewidth=lw, zorder=4)

    set_map_style(ax, extent)
    add_north_arrow(ax, extent[0]+250, extent[3]-500)
    add_scale_bar(ax, extent, y_pos_frac=0.04)

    # Title
    fig.suptitle(title_main, fontsize=20, fontweight='bold', color=C['dark'], y=0.98, x=0.41)
    fig.text(0.41, 0.945, title_sub, fontsize=11, color=C['muted'], ha='center')

    # Legend
    legend_ax = fig.add_axes([0.78, 0.15, 0.18, 0.65])
    legend_ax.set_xlim(0, 1); legend_ax.set_ylim(0, 1)
    legend_ax.axis('off')
    legend_ax.text(0.08, 0.97, legend_title, fontsize=10, fontweight='bold', color=C['dark'])

    shown = list(used_codes)
    for i, code in enumerate(shown):
        info = lu_labels.get(code)
        if info:
            y = 0.90 - i * 0.13
            lc = info[2]
            label = info[0 if is_zh else 1]
            legend_ax.add_patch(Rectangle((0.05, y-0.04), 0.15, 0.06, facecolor=lc,
                                          edgecolor='white', linewidth=0.5))
            legend_ax.text(0.25, y-0.01, label, fontsize=8, color=C['text'], va='center')

    out = FIG_DIR / f'land-use-structure{"" if is_zh else ".en"}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  Saved: {out}")
    return out


# ── Figure 3: Key Areas ─────────────────────────────────
def fig_key_areas(lang='zh'):
    is_zh = (lang == 'zh')
    title_main = '重点区域' if is_zh else 'Key Areas'
    title_sub = '三大重点设计区域 — 众智园 · AI原点社区 · 大钟寺' if is_zh else 'Three Key Design Areas — Zhongzhiyuan · AI Origin · Dazhongsi'
    key_info = [
        (C['key_1'],
         '众智园AI创新加速区 (192 ha)' if is_zh else 'Zhongzhiyuan AI Zone (192 ha)',
         'AI全栈创新策源地\n芯片设计·算法框架·国际AI治理' if is_zh else 'AI Full-Stack Innovation\nChip Design · Algorithms · AI Governance'),
        (C['key_2'],
         '北京AI原点社区 (71 ha)' if is_zh else 'Beijing AI Origin Community (71 ha)',
         'AI创业生态+人才公寓\n共用实验室·场景测试·社区AI服务' if is_zh else 'AI Startup Community\nShared Labs · Scenario Testbeds · AI Services'),
        (C['key_3'],
         '大钟寺国际AI交流节点 (105 ha)' if is_zh else 'Dazhongsi International AI Hub (105 ha)',
         '展示交流+体验消费\nAI MALL·国际论坛·艺术画廊' if is_zh else 'Exhibition & Experience\nAI MALL · Intl Forum · Art Gallery'),
    ]
    key_names_map = {
        '众智园AI自主创新加速区': 0,
        '北京AI原点社区': 1,
        '大钟寺国际 AI 交流节点': 2,
    }

    fig = plt.figure(figsize=(9, 12), dpi=150, facecolor='white')
    gs = fig.add_gridspec(1, 1, left=0.06, right=0.72, top=0.93, bottom=0.05)
    ax = fig.add_subplot(gs[0])

    # Site boundary
    for feat in site['features']:
        plot_feature(ax, feat, facecolor=C['site_fill'], edgecolor=C['site_edge'],
                     linewidth=1.2, alpha=0.5, zorder=1)

    # Green space
    for feat in green_space['features']:
        plot_feature(ax, feat, facecolor=C['green_fill'], edgecolor=C['green_edge'],
                     linewidth=0.3, alpha=0.4, zorder=2)

    # Roads
    for feat in roads['features']:
        rtype = feat['properties'].get('road_type', '')
        lw = 1.5 if rtype in ('expressway','arterial') else 0.8
        plot_line(ax, feat, C['road'], linewidth=lw, zorder=3, linestyle='--' if rtype=='slow_mobility' else '-')

    # Buildings
    bldg_types = {'ai_r_and_d': C['lu_ai_rd'], 'mixed_use': C['lu_mixed'],
                  'retail': C['lu_commercial'], 'residential': C['lu_residential']}
    for feat in buildings['features']:
        bt = feat['properties'].get('building_type', 'ai_r_and_d')
        lc = bldg_types.get(bt, C['muted'])
        plot_feature(ax, feat, facecolor=lc, edgecolor='white',
                     linewidth=0.3, alpha=0.7, zorder=5)

    # Key areas overlay
    for feat in key_areas['features']:
        n_zh = feat['properties']['name_zh']
        idx = key_names_map.get(n_zh, 0)
        lc = key_info[idx][0]
        plot_feature(ax, feat, facecolor='none', edgecolor=lc,
                     linewidth=2.5, alpha=0.9, zorder=6, linestyle='-')

    set_map_style(ax, extent)
    add_north_arrow(ax, extent[0]+250, extent[3]-500)
    add_scale_bar(ax, extent, y_pos_frac=0.04)

    # Title
    fig.suptitle(title_main, fontsize=20, fontweight='bold', color=C['dark'], y=0.98, x=0.41)
    fig.text(0.41, 0.945, title_sub, fontsize=11, color=C['muted'], ha='center')

    # Legend area with key area details
    legend_ax = fig.add_axes([0.74, 0.08, 0.25, 0.79])
    legend_ax.set_xlim(0, 1); legend_ax.set_ylim(0, 1)
    legend_ax.axis('off')

    for i, (lc, name, desc) in enumerate(key_info):
        y_top = 0.96 - i * 0.29
        legend_ax.add_patch(Rectangle((0.03, y_top-0.04), 0.16, 0.08, facecolor=lc,
                                      edgecolor=lc, linewidth=1))
        legend_ax.text(0.03, y_top-0.09, name, fontsize=8.5, fontweight='bold', color=lc)
        legend_ax.text(0.03, y_top-0.20, desc, fontsize=7, color=C['text'],
                       linespacing=1.5, va='top')

    # Building legend
    legend_ax.text(0.03, 0.13, '建筑类型' if is_zh else 'Building Types', fontsize=7.5, color=C['muted'])
    bldg_labels = {
        'ai_r_and_d': ('AI研发' if is_zh else 'AI R&D', C['lu_ai_rd']),
        'mixed_use': ('混合功能' if is_zh else 'Mixed Use', C['lu_mixed']),
        'retail': ('商业零售' if is_zh else 'Retail', C['lu_commercial']),
        'residential': ('居住' if is_zh else 'Residential', C['lu_residential']),
    }
    for j, (bt, (blabel, bc)) in enumerate(bldg_labels.items()):
        y = 0.08 - j * 0.026
        legend_ax.add_patch(Rectangle((0.03, y), 0.10, 0.018, facecolor=bc, edgecolor='none'))
        legend_ax.text(0.16, y+0.009, blabel, fontsize=6.5, color=C['text'], va='center')

    out = FIG_DIR / f'key-areas{"" if is_zh else ".en"}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  Saved: {out}")
    return out


# ── Figure 4: Mobility & Blue-Green ─────────────────────
def fig_mobility_bluegreen(lang='zh'):
    is_zh = (lang == 'zh')
    title_main = '交通慢行与蓝绿网络' if is_zh else 'Mobility & Blue-Green Network'
    title_sub = '京张AI慢行专用道 · 清河-小月河蓝绿廊道 · 社区绿环' if is_zh else 'AI Slow Mobility Corridor · Qinghe-Xiaoyue Blue-Green · Community Rings'

    fig = plt.figure(figsize=(9.5, 12), dpi=150, facecolor='white')
    gs = fig.add_gridspec(1, 1, left=0.08, right=0.74, top=0.93, bottom=0.05)
    ax = fig.add_subplot(gs[0])

    # Site boundary
    for feat in site['features']:
        plot_feature(ax, feat, facecolor=C['site_fill'], edgecolor=C['site_edge'],
                     linewidth=1.2, alpha=0.5, zorder=1)

    # Green space - main focus
    for feat in green_space['features']:
        plot_feature(ax, feat, facecolor=C['green_fill'], edgecolor=C['green_edge'],
                     linewidth=0.6, alpha=0.65, zorder=3)

    # Public space
    for feat in public_space['features']:
        plot_feature(ax, feat, facecolor='#FFF9C4', edgecolor='#F9A825',
                     linewidth=0.4, alpha=0.5, zorder=3)

    # Water bodies in north
    plot_patch_xy(ax, (extent[0], WATER_NORTH_Y, extent[1], extent[3]),
                  facecolor=C['water'], alpha=0.45, zorder=2)

    # Roads with slow mobility highlighted
    for feat in roads['features']:
        rtype = feat['properties'].get('road_type', '')
        if rtype == 'slow_mobility':
            # Draw glow effect
            plot_line(ax, feat, '#81C784', linewidth=6, zorder=4, linestyle='-')
            plot_line(ax, feat, '#2E7D32', linewidth=3, zorder=5, linestyle='-')
            plot_line(ax, feat, 'white', linewidth=1, zorder=6, linestyle='--')
        else:
            lw = 1.2 if rtype in ('expressway','arterial') else 0.7
            plot_line(ax, feat, C['road'], linewidth=lw, zorder=3, alpha=0.5)

    set_map_style(ax, extent)
    add_north_arrow(ax, extent[0]+250, extent[3]-500)
    add_scale_bar(ax, extent, y_pos_frac=0.04)

    # Title
    fig.suptitle(title_main, fontsize=20, fontweight='bold', color=C['dark'], y=0.98, x=0.41)
    fig.text(0.41, 0.945, title_sub, fontsize=11, color=C['muted'], ha='center')

    # Legend
    legend_ax = fig.add_axes([0.78, 0.20, 0.18, 0.55])
    legend_ax.set_xlim(0, 1); legend_ax.set_ylim(0, 1)
    legend_ax.axis('off')
    legend_ax.text(0.08, 0.97, '图例' if is_zh else 'Legend', fontsize=10, fontweight='bold', color=C['dark'])

    items = [
        ('京张AI慢行专用道' if is_zh else 'AI Slow Mobility Corridor', C['slow'], C['slow'], 'line'),
        ('绿脉公园带' if is_zh else 'Green Park Belt', C['green_fill'], C['green_edge'], 'area'),
        ('公共空间/广场' if is_zh else 'Public Spaces/Plazas', '#FFF9C4', '#F9A825', 'area'),
        ('水域' if is_zh else 'Water Bodies', C['water'], C['water_edge'], 'area'),
        ('主要道路' if is_zh else 'Major Roads', 'white', C['road'], 'line'),
    ]
    for i, (label, fc, ec, kind) in enumerate(items):
        y = 0.88 - i * 0.14
        if kind == 'area':
            legend_ax.add_patch(Rectangle((0.05, y-0.04), 0.15, 0.06, facecolor=fc,
                                          edgecolor=ec, linewidth=0.8))
        else:
            legend_ax.plot([0.05, 0.20], [y-0.01, y-0.01], color=fc, linewidth=4, solid_capstyle='round')
        legend_ax.text(0.28, y-0.01, label, fontsize=7.5, color=C['text'], va='center')

    out = FIG_DIR / f'mobility-bluegreen{"" if is_zh else ".en"}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  Saved: {out}")
    return out


# ── Figure 5: Metrics Evidence ──────────────────────────
def fig_metrics_evidence(lang='zh'):
    is_zh = (lang == 'zh')
    title_main = '核心指标体系' if is_zh else 'Core Metrics Dashboard'
    title_sub = '绿脉智芯方案 — 量化设计目标与空间验证' if is_zh else 'Green Veins, Smart Core — Design Targets & Verification'

    fig = plt.figure(figsize=(14, 10), dpi=150, facecolor='white')

    # Layout: 2x2 grid of sub-charts + title
    gs = fig.add_gridspec(3, 2, height_ratios=[0.08, 0.46, 0.46],
                          hspace=0.45, wspace=0.35,
                          left=0.08, right=0.95, top=0.95, bottom=0.06)

    # Title area
    ax_title = fig.add_subplot(gs[0, :])
    ax_title.axis('off')
    ax_title.text(0.5, 0.7, title_main, fontsize=20, fontweight='bold',
                  color=C['dark'], ha='center', va='center', transform=ax_title.transAxes)
    ax_title.text(0.5, 0.2, title_sub, fontsize=11, color=C['muted'],
                  ha='center', va='center', transform=ax_title.transAxes)

    # ── Chart 1: Ecological Metrics (radar-like bar) ──
    ax1 = fig.add_subplot(gs[1, 0])
    eco_labels = ['绿化覆盖率' if is_zh else 'Green Coverage',
                  '海绵控制率' if is_zh else 'Sponge Capture',
                  '可再生\n能源占比' if is_zh else 'Renewable\nEnergy',
                  '绿色出行\n比例' if is_zh else 'Green Mode\nShare',
                  '公共空间\n可达性' if is_zh else 'Public Space\nAccess']
    eco_values = [0.4, 0.85, 0.2, 0.6, 1.0]
    eco_targets = [0.35, 0.80, 0.15, 0.50, 0.95]  # minimum targets

    colors_eco = [C['chart_1'], C['chart_2'], C['chart_3'], C['chart_4'], C['chart_5']]
    x = np.arange(len(eco_labels))
    bars = ax1.bar(x, eco_values, 0.55, color=colors_eco, alpha=0.85,
                   edgecolor='white', linewidth=0.8)
    # Target markers
    ax1.scatter(x, eco_targets, marker='_', s=300, color='#333333', linewidth=2,
                zorder=5, label='基准线' if is_zh else 'Baseline')

    for i, (v, t) in enumerate(zip(eco_values, eco_targets)):
        ax1.text(i, v + 0.03, f'{v*100:.0f}%', ha='center', fontsize=9, fontweight='bold',
                color=colors_eco[i])
    ax1.set_xticks(x)
    ax1.set_xticklabels(eco_labels, fontsize=7.5, color=C['text'])
    ax1.set_ylim(0, 1.2)
    ax1.set_title('生态与可持续指标' if is_zh else 'Ecology & Sustainability',
                  fontsize=11, fontweight='bold', color=C['dark'], pad=8)
    ax1.set_ylabel('比例' if is_zh else 'Ratio', fontsize=8, color=C['muted'])
    ax1.legend(fontsize=7, loc='upper right')
    ax1.set_facecolor('white')
    ax1.grid(axis='y', linestyle='--', alpha=0.3, color=C['grid'])
    ax1.tick_params(labelsize=7)

    # ── Chart 2: Land Use Distribution (pie) ──
    ax2 = fig.add_subplot(gs[1, 1])
    lu_data = {
        'AI创新' if is_zh else 'AI Innovation': (320, C['lu_ai_rd']),
        '绿脉公园' if is_zh else 'Green Parks': (180, C['lu_green']),
        '生活社区' if is_zh else 'Residential': (280, C['lu_residential']),
        '智慧服务' if is_zh else 'Smart Service': (120, C['lu_commercial']),
        '产业融合' if is_zh else 'Mixed Industry': (140, C['lu_industry']),
        '蓝绿腹地' if is_zh else 'Blue-Green': (100, C['lu_water']),
    }
    labels = list(lu_data.keys())
    sizes = [v[0] for v in lu_data.values()]
    colors = [v[1] for v in lu_data.values()]

    wedges, texts, autotexts = ax2.pie(sizes, labels=labels, colors=colors,
                                        autopct='%1.1f%%', startangle=90,
                                        textprops={'fontsize': 7.5},
                                        pctdistance=0.75, wedgeprops={'linewidth': 0.5, 'edgecolor': 'white'})
    for at in autotexts:
        at.set_fontsize(7)
        at.set_fontweight('bold')
        at.set_color('white')
    ax2.set_title('用地面积分布 (ha)' if is_zh else 'Land Use Distribution (ha)',
                  fontsize=11, fontweight='bold', color=C['dark'], pad=8)

    # ── Chart 3: Phased Projects ──
    ax3 = fig.add_subplot(gs[2, 0])
    phases = ['近期\n1-3年' if is_zh else 'Near\n1-3yr',
              '中期\n3-7年' if is_zh else 'Mid\n3-7yr',
              '远期\n7-15年' if is_zh else 'Long\n7-15yr']
    phase_counts = [4, 5, 4]
    phase_colors = [C['chart_1'], C['chart_2'], C['chart_3']]

    hbars = ax3.barh(phases, phase_counts, color=phase_colors, height=0.5,
                     alpha=0.85, edgecolor='white', linewidth=0.8)
    for bar, v in zip(hbars, phase_counts):
        ax3.text(bar.get_width() + 0.15, bar.get_y() + bar.get_height()/2,
                f'{v}个项目' if is_zh else f'{v} projects',
                va='center', fontsize=10, fontweight='bold', color=C['dark'])
    ax3.set_title('分阶段实施计划' if is_zh else 'Phased Implementation',
                  fontsize=11, fontweight='bold', color=C['dark'], pad=8)
    ax3.set_xlim(0, 7)
    ax3.set_facecolor('white')
    ax3.grid(axis='x', linestyle='--', alpha=0.3, color=C['grid'])
    ax3.tick_params(labelsize=8)

    # ── Chart 4: Building Renewal Strategy ──
    ax4 = fig.add_subplot(gs[2, 1])
    renewal_labels = ['保留提升' if is_zh else 'Preserve',
                      '功能置换' if is_zh else 'Repurpose',
                      '综合整治' if is_zh else 'Renovate',
                      '拆除新建' if is_zh else 'New Build']
    renewal_pcts = [45, 25, 20, 10]
    renewal_colors = ['#81C784', '#42A5F5', '#FFB74D', '#E57373']

    bars4 = ax4.bar(renewal_labels, renewal_pcts, 0.55, color=renewal_colors,
                    alpha=0.85, edgecolor='white', linewidth=0.8)
    for bar, v in zip(bars4, renewal_pcts):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                f'{v}%', ha='center', fontsize=10, fontweight='bold',
                color=bar.get_facecolor())
    ax4.set_title('建筑更新策略' if is_zh else 'Building Renewal Strategy',
                  fontsize=11, fontweight='bold', color=C['dark'], pad=8)
    ax4.set_ylim(0, 55)
    ax4.set_ylabel('%' if is_zh else '%', fontsize=8, color=C['muted'])
    ax4.set_facecolor('white')
    ax4.grid(axis='y', linestyle='--', alpha=0.3, color=C['grid'])
    ax4.tick_params(labelsize=8)

    # Footer
    fig.text(0.5, 0.01, '所有指标为概念设计目标，非政府审定结论 | Data sourced from design proposal metrics.json',
             fontsize=6.5, color=C['muted'], ha='center')

    out = FIG_DIR / f'metrics-evidence{"" if is_zh else ".en"}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  Saved: {out}")
    return out


# ── Generate A0 Boards PDF ──────────────────────────────
def generate_a0_pdf(lang='zh'):
    """Generate A0 landscape board with embedded figures, large fonts, rich content.

    Layout (A0 = 1189×841mm, 47×33"):
    ┌──────────────────────────────────────────────────────┐
    │            Dark Blue Title Banner                     │
    ├──────────────────────────────┬───────────┬───────────┤
    │  Site Overview (embedded)    │ Key Areas │  Project  │
    │  ~58% width, ~44% height     │ ~18% w    │  Info +   │
    │                              │           │  Metrics  │
    ├──────────────────────────────┼───────────┤  Cards    │
    │                              │ Mobility  │  ~22% w   │
    │  Land Use (embedded)         │ & Blue-   │           │
    │  ~58% width, ~42% height     │ Green     │  Design   │
    │                              │ ~18% w    │  Strategy │
    │                              │           │  Text     │
    ├──────────────────────────────┴───────────┴───────────┤
    │   Metrics Dashboard (full-width, embedded)            │
    ├───────────────────────────────────────────────────────┤
    │   Footer: source & credits                            │
    └───────────────────────────────────────────────────────┘
    """
    is_zh = (lang == 'zh')
    suffix = '' if is_zh else '.en'

    # Load pre-generated figure images for embedding
    img_site = mpimg.imread(str(FIG_DIR / f'site-overview{suffix}.png'))
    img_key = mpimg.imread(str(FIG_DIR / f'key-areas{suffix}.png'))
    img_lu = mpimg.imread(str(FIG_DIR / f'land-use-structure{suffix}.png'))
    img_mob = mpimg.imread(str(FIG_DIR / f'mobility-bluegreen{suffix}.png'))
    img_metrics = mpimg.imread(str(FIG_DIR / f'metrics-evidence{suffix}.png'))

    fig = plt.figure(figsize=(47, 33), dpi=100, facecolor='white')

    # ── Title Banner ─────────────────────────────────────
    banner_h = 0.042
    ax_banner = fig.add_axes([0.015, 0.948, 0.97, banner_h])
    ax_banner.set_facecolor('#1A237E')
    ax_banner.set_xlim(0, 1); ax_banner.set_ylim(0, 1)
    ax_banner.axis('off')
    ax_banner.text(0.025, 0.55, '\u7eff\u8109\u667a\u82af' if is_zh else 'Green Veins, Smart Core',
                   fontsize=52, fontweight='bold', color='white', va='center')
    ax_banner.text(0.22, 0.55,
                   '\u2014 \u4eac\u5f20AI\u521b\u65b0\u5e26\u84dd\u7eff\u667a\u6167\u57ce\u5e02\u8bbe\u8ba1 \u2014' if is_zh
                   else '\u2014 Jing-Zhang AI Innovation Belt Urban Design \u2014',
                   fontsize=24, color='#90CAF9', va='center')
    ax_banner.text(0.96, 0.55, 'A0 Exhibition Board' if is_zh else 'A0 Exhibition Board',
                   fontsize=22, fontweight='bold', color='#64B5F6', ha='right', va='center')

    # ── Layout Grid ──────────────────────────────────────
    left_x   = 0.015;  left_w   = 0.57
    mid_x    = 0.595;  mid_w    = 0.17
    right_x  = 0.775;  right_w  = 0.21
    banner_bottom = 0.942
    row1_top      = 0.935
    row1_bottom   = 0.51
    row2_top      = 0.50
    row2_bottom   = 0.18
    row3_top      = 0.17
    row3_bottom   = 0.015

    row1_h = row1_top - row1_bottom
    row2_h = row2_top - row2_bottom
    gap    = 0.012

    # ── Row 1 Left: Site Overview (embedded image) ──────
    ax_site = fig.add_axes([left_x, row1_bottom + gap, left_w, row1_h - gap])
    ax_site.imshow(img_site, aspect='auto')
    ax_site.axis('off')
    ax_site.set_title('Site Overview / \u573a\u5730\u603b\u89c8' if is_zh else 'Site Overview',
                      fontsize=24, fontweight='bold', color=C['dark'], pad=18)

    # ── Row 1 Middle: Key Areas (embedded image) ────────
    ax_key = fig.add_axes([mid_x, row1_bottom + gap, mid_w, row1_h - gap])
    ax_key.imshow(img_key, aspect='auto')
    ax_key.axis('off')
    ax_key.set_title('Key Areas / \u91cd\u70b9\u533a\u57df' if is_zh else 'Key Areas',
                     fontsize=20, fontweight='bold', color=C['dark'], pad=14)

    # ── Row 1 Right: Project Info + Metrics Cards ───────
    ax_info = fig.add_axes([right_x, row1_bottom + gap, right_w, row1_h - gap])
    ax_info.set_xlim(0, 1); ax_info.set_ylim(0, 1)
    ax_info.axis('off')
    # Section divider
    ax_info.add_patch(Rectangle((0.02, 0.99), 0.96, 0.005, facecolor='#1A237E', edgecolor='none'))

    y_pos = 0.96
    # --- Project Overview ---
    ax_info.text(0.04, y_pos, '\u9879\u76ee\u6982\u51b5' if is_zh else 'Project Overview',
                 fontsize=22, fontweight='bold', color=C['dark'])
    y_pos -= 0.055
    info_items = [
        ('\u4f4d\u7f6e' if is_zh else 'Location',
         '\u5317\u4eac\u5e02\u6d77\u6dc0\u533a' if is_zh else 'Haidian District, Beijing'),
        ('\u8bbe\u8ba1\u8303\u56f4' if is_zh else 'Design Area',
         '11.4 km\u00b2'),
        ('\u7814\u7a76\u8303\u56f4' if is_zh else 'Study Area',
         '43.6 km\u00b2'),
        ('\u91cd\u70b9\u7247\u533a' if is_zh else 'Key Areas',
         '3 \u4e2a\u7247\u533a / 368 ha' if is_zh else '3 zones / 368 ha'),
        ('\u603b\u5efa\u7b51\u91cf' if is_zh else 'Total GFA',
         '\u2248 1,200 \u4e07 m\u00b2' if is_zh else '~12M m\u00b2'),
    ]
    for label, val in info_items:
        ax_info.text(0.06, y_pos, f'\u25cf {label}', fontsize=16, fontweight='bold', color=C['dark'])
        ax_info.text(0.06, y_pos - 0.035, val, fontsize=14, color=C['text'])
        y_pos -= 0.068

    # --- Metrics Cards (compact) ---
    y_pos -= 0.010
    ax_info.text(0.04, y_pos, '\u6838\u5fc3\u6307\u6807' if is_zh else 'Core Metrics',
                 fontsize=22, fontweight='bold', color=C['dark'])
    y_pos -= 0.060

    metric_items = [
        ('\u7eff\u5316\u8986\u76d6\u7387' if is_zh else 'Green Coverage', '35.3%', '\u2265 40% \u76ee\u6807' if is_zh else '\u2265 40% target', C['chart_1']),
        ('\u6d77\u7ef5\u63a7\u5236\u7387' if is_zh else 'Sponge Control', '85%', '33.6mm \u8bbe\u8ba1\u964d\u96e8' if is_zh else '33.6mm rainfall', C['chart_2']),
        ('\u53ef\u518d\u751f\u80fd\u6e90' if is_zh else 'Renewable Energy', '20%', '\u5149\u4f0f+区域能源站' if is_zh else 'PV + district station', C['chart_3']),
        ('\u7eff\u8272\u51fa\u884c' if is_zh else 'Green Mode Share', '60%', 'AI慢行专用道' if is_zh else 'AI slow lane', C['chart_4']),
        ('\u516c\u5171\u7a7a\u95f4' if is_zh else 'Public Space', '100%', '500m\u6b65\u884c\u534a\u5f84' if is_zh else '500m radius', C['chart_5']),
        ('AI\u573a\u666f\u8282\u70b9' if is_zh else 'AI Scenarios', '50+', '3\u5927\u5730\u6807' if is_zh else '3 landmarks', C['chart_6']),
    ]
    cols = 3
    for i, (name, value, note, lc) in enumerate(metric_items):
        row = i // cols
        col = i % cols
        cx = 0.08 + col * 0.32
        cy = y_pos - row * 0.10
        ax_info.add_patch(FancyBboxPatch((cx - 0.13, cy - 0.035), 0.26, 0.07,
                                          boxstyle='round,pad=0.01',
                                          facecolor=lc, edgecolor='none', alpha=0.15))
        ax_info.text(cx, cy + 0.01, value, fontsize=16, fontweight='bold',
                     color=lc, ha='center', va='center')
        ax_info.text(cx, cy - 0.02, name, fontsize=11, color=C['text'], ha='center', va='center')

    # ── Row 2 Left: Land Use Structure (embedded image) ──
    ax_lu = fig.add_axes([left_x, row2_bottom + gap, left_w, row2_h - gap])
    ax_lu.imshow(img_lu, aspect='auto')
    ax_lu.axis('off')
    ax_lu.set_title('Land Use Structure / \u7528\u5730\u7ed3\u6784' if is_zh else 'Land Use Structure',
                    fontsize=24, fontweight='bold', color=C['dark'], pad=18)

    # ── Row 2 Middle: Mobility & Blue-Green ──────────────
    ax_mob = fig.add_axes([mid_x, row2_bottom + gap, mid_w, row2_h - gap])
    ax_mob.imshow(img_mob, aspect='auto')
    ax_mob.axis('off')
    ax_mob.set_title('Mobility & Blue-Green / \u6162\u884c\u4e0e\u84dd\u7eff' if is_zh else 'Mobility & Blue-Green',
                     fontsize=20, fontweight='bold', color=C['dark'], pad=14)

    # ── Row 2 Right: Design Strategy ─────────────────────
    ax_strat = fig.add_axes([right_x, row2_bottom + gap, right_w, row2_h - gap])
    ax_strat.set_xlim(0, 1); ax_strat.set_ylim(0, 1)
    ax_strat.axis('off')
    ax_strat.add_patch(Rectangle((0.02, 0.99), 0.96, 0.005, facecolor='#1A237E', edgecolor='none'))

    y_pos = 0.96
    ax_strat.text(0.04, y_pos, '\u8bbe\u8ba1\u7b56\u7565' if is_zh else 'Design Strategy',
                  fontsize=22, fontweight='bold', color=C['dark'])
    y_pos -= 0.065

    strategy_items = [
        ('\u7a7a\u95f4\u7ed3\u6784' if is_zh else 'Spatial Structure',
         '\u4e00\u5e26\u00b7\u4e09\u82af\u00b7\u4e24\u7ffc\n\u4eac\u5f20\u7eff\u8109 + \u4f17\u667a\u56ed + AI\u539f\u70b9\u793e\u533a + \u5927\u949f\u5bfa\n\u5b66\u9662\u8def\u521b\u65b0\u7ffc + \u4e2d\u5173\u6751\u4ea7\u4e1a\u7ffc' if is_zh
         else '1 Belt \u00b7 3 Cores \u00b7 2 Wings\nJing-Zhang Green Spine + 3 AI Hubs\nXueyuan Innovation + Zhongguancun Industry'),
        ('\u751f\u6001\u6d77\u7ef5' if is_zh else 'Eco-Sponge',
         '85%\u6d77\u7ef5\u63a7\u5236\u7387\n40%\u7eff\u5316\u8986\u76d6\u7387\n\u6e05\u6cb3-\u5c0f\u6708\u6cb3\u84dd\u7eff\u5eca\u9053\n\u78b3\u4e2d\u548cMRV\u4f53\u7cfb' if is_zh
         else '85% sponge control rate\n40% green coverage\nQinghe-Xiaoyue corridor\nCarbon-neutral MRV'),
        ('\u4ea4\u901a\u6162\u884c' if is_zh else 'Slow Mobility',
         'AI\u6162\u884c\u4e13\u7528\u9053\n\u7eff\u8272\u51fa\u884c\u226560%\n\u81ea\u52a8\u9a7e\u9a76\u914d\u9001\n\u667a\u80fd\u5bfc\u822a\u7cfb\u7edf' if is_zh
         else 'AI slow mobility lane\nGreen mode \u226560%\nAutonomous delivery\nSmart navigation'),
        ('\u4f4e\u78b3\u667a\u6167' if is_zh else 'Low-Carbon Smart',
         '\u53ef\u518d\u751f\u80fd\u6e90\u226520%\n\u5149\u4f0f\u5e55\u5899+\u533a\u57df\u80fd\u6e90\u7ad9\n\u667a\u80fd\u706f\u6746+\u73af\u5883\u4f20\u611f\u5668\nAI\u57ce\u5e02\u8fd0\u8425\u5e73\u53f0' if is_zh
         else 'Renewable \u226520%\nPV facades + district energy\nSmart streetlights + sensors\nAI urban ops platform'),
        ('\u6e10\u8fdb\u66f4\u65b0' if is_zh else 'Incremental Renewal',
         '\u4fdd\u7559\u63d0\u5347 45%\n\u529f\u80fd\u7f6e\u6362 25%\n\u7efc\u5408\u6574\u6cbb 20%\n\u62c6\u9664\u65b0\u5efa 10%' if is_zh
         else 'Preserve 45%\nRepurpose 25%\nRenovate 20%\nNew Build 10%'),
        ('AI\u521b\u65b0\u751f\u6001' if is_zh else 'AI Ecosystem',
         '50+\u573a\u666f\u8282\u70b9\n3\u5927AI\u671d\u5723\u5730\u6807\nAI MALL + \u56fd\u9645\u8bba\u575b\n\u53c2\u4e0e\u5f0f\u8bbe\u8ba1\u5e73\u53f0' if is_zh
         else '50+ scenario nodes\n3 AI landmark sites\nAI MALL + Intl Forum\nParticipatory design'),
    ]
    for label, detail in strategy_items:
        ax_strat.text(0.06, y_pos, f'\u25a0 {label}', fontsize=14, fontweight='bold', color=C['dark'])
        ax_strat.text(0.06, y_pos - 0.035, detail, fontsize=11, color=C['text'],
                      linespacing=1.4, va='top')
        y_pos -= 0.098

    # ── Row 3: Metrics Evidence (full-width) ─────────────
    ax_met = fig.add_axes([left_x, row3_bottom, 0.955, row3_top - row3_bottom - 0.01])
    ax_met.imshow(img_metrics, aspect='auto')
    ax_met.axis('off')
    ax_met.set_title('Core Metrics Dashboard / \u6838\u5fc3\u6307\u6807\u4f53\u7cfb' if is_zh else 'Core Metrics Dashboard',
                     fontsize=24, fontweight='bold', color=C['dark'], pad=18)

    # ── Footer ───────────────────────────────────────────
    fig.text(0.5, 0.0035,
             'WorkBuddy (wlaura-wlj)  |  jingzhang-green-smart-ai-belt  |  professional_design_package  |  August 2026  |  Data: OpenStreetMap (ODbL) + Provisional Site Boundary',
             fontsize=10, color=C['muted'], ha='center')

    out = DRAW_DIR / f'a0-boards{suffix}.pdf'
    fig.savefig(out, dpi=100, facecolor='white', edgecolor='none', format='pdf',
                bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved: {out} ({os.path.getsize(out)} bytes)")
    return out


# ── Generate A3 Booklet PDF ─────────────────────────────
def generate_a3_pdf(lang='zh'):
    """Generate A3 booklet with maps, metrics, and detailed strategy text.

    Layout (A3 landscape = 420×297mm, 33×23"):
    ┌─────────────────────────────────────────────────────────────────┐
    │ ┌─────────────────────┐                                         │
    │ │                     │   绿脉智芯                              │
    │ │   Site Overview     │   京张AI创新带蓝绿智慧城市设计方案       │
    │ │   Map (embedded)    │                                         │
    │ │                     │   项目信息  |  核心指标  |  设计定位     │
    │ └─────────────────────┘                                         │
    ├─────────────────────────────────────────────────────────────────┤
    │ ┌───────────────────┐ ┌───────────────────┐ ┌─────────────────┐ │
    │ │                    │ │                    │ │                 │ │
    │ │  Land Use Map      │ │  Key Areas         │ │  Design         │ │
    │ │  (embedded)        │ │  (embedded)        │ │  Strategy       │ │
    │ │                    │ │                    │ │  Detail         │ │
    │ └───────────────────┘ └───────────────────┘ └─────────────────┘ │
    ├─────────────────────────────────────────────────────────────────┤
    │   Footer: credits                                               │
    └─────────────────────────────────────────────────────────────────┘
    """
    is_zh = (lang == 'zh')
    suffix = '' if is_zh else '.en'

    # Load pre-generated figures
    img_site = mpimg.imread(str(FIG_DIR / f'site-overview{suffix}.png'))
    img_lu = mpimg.imread(str(FIG_DIR / f'land-use-structure{suffix}.png'))
    img_key = mpimg.imread(str(FIG_DIR / f'key-areas{suffix}.png'))

    fig = plt.figure(figsize=(33, 23), dpi=100, facecolor='white')

    # ── Top Section: Cover + Site Map ──────────────────
    # Left: Site Overview map (~40% width)
    cover_map_x = 0.02; cover_map_w = 0.42
    cover_map_h = 0.58; cover_map_y = 0.38

    ax_cover_map = fig.add_axes([cover_map_x, cover_map_y, cover_map_w, cover_map_h])
    ax_cover_map.imshow(img_site, aspect='auto')
    ax_cover_map.axis('off')

    # Right: Title + Project Info (~55% width)
    cover_text_x = 0.47; cover_text_w = 0.50
    ax_cover = fig.add_axes([cover_text_x, cover_map_y, cover_text_w, cover_map_h])
    ax_cover.set_xlim(0, 1); ax_cover.set_ylim(0, 1)
    ax_cover.axis('off')

    # Decorative green bar
    ax_cover.add_patch(Rectangle((0, 0.90), 1, 0.015, facecolor='#2E7D32', edgecolor='none'))
    ax_cover.add_patch(Rectangle((0, 0.90), 0.015, 0.10, facecolor='#1B5E20', edgecolor='none'))

    ax_cover.text(0.05, 0.82, '\u7eff\u8109\u667a\u82af' if is_zh else 'Green Veins, Smart Core',
                  fontsize=46, fontweight='bold', color='#1B5E20')
    ax_cover.text(0.05, 0.73, '\u4eac\u5f20AI\u521b\u65b0\u5e26\u84dd\u7eff\u667a\u6167\u57ce\u5e02\u8bbe\u8ba1\u65b9\u6848' if is_zh
                  else 'Jing-Zhang AI Innovation Belt\nBlue-Green Smart Urban Design Proposal',
                  fontsize=22, color='#2E7D32', linespacing=1.4)

    ax_cover.text(0.05, 0.62, 'Jing-Zhang Green Smart AI Belt  |  Haidian District, Beijing  |  2026.08',
                  fontsize=12, color=C['muted'])
    ax_cover.text(0.05, 0.58, 'Proposal: jingzhang-green-smart-ai-belt  |  Agent: WorkBuddy (wlaura-wlj)  |  Package: professional_design_package',
                  fontsize=11, color=C['muted'])

    # --- Three info columns in cover section ---
    col_w = 0.28; col_x_start = 0.05; col_gap = 0.04
    col_data = [
        ('\u9879\u76ee\u4fe1\u606f' if is_zh else 'Project Info', [
            ('\u4f4d\u7f6e' if is_zh else 'Location',
             '\u5317\u4eac\u5e02\u6d77\u6dc0\u533a' if is_zh else 'Haidian, Beijing'),
            ('\u8bbe\u8ba1\u8303\u56f4' if is_zh else 'Design Area',
             '11.4 km\u00b2'),
            ('\u7814\u7a76\u8303\u56f4' if is_zh else 'Study Area',
             '43.6 km\u00b2'),
            ('\u91cd\u70b9\u7247\u533a' if is_zh else 'Key Zones',
             '\u4f17\u667a\u56ed 192ha\nAI\u539f\u70b9\u793e\u533a 71ha\n\u5927\u949f\u5bfa 105ha' if is_zh
             else 'Zhongzhiyuan 192ha\nAI Origin 71ha\nDazhongsi 105ha'),
        ]),
        ('\u6838\u5fc3\u6307\u6807' if is_zh else 'Core Metrics', [
            ('\u7eff\u5316\u8986\u76d6\u7387' if is_zh else 'Green Coverage',
             '35.3% (\u226540%)'),
            ('\u6d77\u7ef5\u63a7\u5236\u7387' if is_zh else 'Sponge Control',
             '85%'),
            ('\u7eff\u8272\u51fa\u884c' if is_zh else 'Green Mode',
             '\u226560%'),
            ('\u53ef\u518d\u751f\u80fd\u6e90' if is_zh else 'Renewable',
             '\u226520%'),
            ('\u516c\u5171\u7a7a\u95f4' if is_zh else 'Public Space',
             '100% 500m\u53ef\u8fbe'),
            ('AI\u573a\u666f\u8282\u70b9' if is_zh else 'AI Nodes',
             '50+'),
            ('\u5206\u671f\u9879\u76ee' if is_zh else 'Phased',
             '15\u4e2a' if is_zh else '15'),
        ]),
        ('\u8bbe\u8ba1\u5b9a\u4f4d' if is_zh else 'Design Vision', [
            ('\u7a7a\u95f4\u7ed3\u6784' if is_zh else 'Structure',
             '\u4e00\u5e26\u00b7\u4e09\u82af\u00b7\u4e24\u7ffc' if is_zh else '1 Belt\u00b73 Cores\u00b72 Wings'),
            ('\u751f\u6001\u5b9a\u4f4d' if is_zh else 'Ecology',
             '\u6d77\u7ef5\u57ce\u5e02+\u84dd\u7eff\u7f51\u7edc' if is_zh else 'Sponge+Blue-Green'),
            ('\u4ea4\u901a\u5b9a\u4f4d' if is_zh else 'Mobility',
             'AI\u6162\u884c\u4e13\u7528\u9053' if is_zh else 'AI Slow Mobility'),
            ('\u4ea7\u4e1a\u5b9a\u4f4d' if is_zh else 'Industry',
             'AI\u5168\u6808\u521b\u65b0\u7b56\u6e90\u5730' if is_zh else 'AI Full-Stack Hub'),
            ('\u66f4\u65b0\u7b56\u7565' if is_zh else 'Renewal',
             '\u4fdd\u7559\u63d0\u534745%+\u7f6e\u636225%' if is_zh else 'Preserve45%+Repurpose25%'),
            ('\u76ee\u6807\u5b9a\u4f4d' if is_zh else 'Goal',
             '\u7eff\u8272\u667a\u6167\u672a\u6765\u57ce\u5e02\u793a\u8303\u533a' if is_zh
             else 'Green Smart Future City'),
        ]),
    ]
    for j, (col_title, items) in enumerate(col_data):
        cx = col_x_start + j * (col_w + col_gap)
        # Header
        ax_cover.add_patch(FancyBboxPatch((cx, 0.40), col_w, 0.06, boxstyle='round,pad=0.01',
                                            facecolor=C['dark'], edgecolor='none'))
        ax_cover.text(cx + col_w/2, 0.43, col_title, fontsize=13, fontweight='bold',
                      color='white', ha='center', va='center')
        for i, (label, val) in enumerate(items):
            y = 0.36 - i * 0.07
            ax_cover.text(cx + 0.02, y + 0.015, label, fontsize=11, fontweight='bold', color=C['muted'])
            ax_cover.text(cx + 0.02, y - 0.01, val, fontsize=10, color=C['text'], linespacing=1.2)

    # ── Bottom Section: Maps + Strategy ─────────────────
    bottom_y = 0.02; bottom_h = 0.34
    bottom_gap = 0.015

    # L: Land Use Map
    ax_lu_a3 = fig.add_axes([0.02, bottom_y, 0.30, bottom_h])
    ax_lu_a3.imshow(img_lu, aspect='auto')
    ax_lu_a3.axis('off')
    ax_lu_a3.set_title('\u7528\u5730\u7ed3\u6784' if is_zh else 'Land Use Structure',
                       fontsize=18, fontweight='bold', color=C['dark'], pad=12)

    # M: Key Areas Map
    ax_key_a3 = fig.add_axes([0.335, bottom_y, 0.30, bottom_h])
    ax_key_a3.imshow(img_key, aspect='auto')
    ax_key_a3.axis('off')
    ax_key_a3.set_title('\u91cd\u70b9\u533a\u57df' if is_zh else 'Key Areas',
                        fontsize=18, fontweight='bold', color=C['dark'], pad=12)

    # R: Detailed Strategy Text
    ax_strat_a3 = fig.add_axes([0.655, bottom_y, 0.33, bottom_h])
    ax_strat_a3.set_xlim(0, 1); ax_strat_a3.set_ylim(0, 1)
    ax_strat_a3.axis('off')
    ax_strat_a3.add_patch(Rectangle((0.02, 0.97), 0.96, 0.01, facecolor='#2E7D32', edgecolor='none'))

    strategy_detail = [
        ('\u751f\u6001\u6d77\u7ef5' if is_zh else 'Eco-Sponge',
         '\u6d77\u7ef5\u57ce\u5e02\u63a7\u5236\u738785%\uff0c\u7eff\u5316\u8986\u76d6\u7387\u226540%\uff0c\u6e05\u6cb3-\u5c0f\u6708\u6cb3\u84dd\u7eff\u5eca\u9053\u4e32\u8054\u516c\u56ed\u3001\u6ee8\u6c34\u3001\u6e7f\u5730\u3002\u78b3\u4e2d\u548cMRV\u4f53\u7cfb\u5168\u8fc7\u7a0b\u8ffd\u8e2a\u3002' if is_zh
         else 'Sponge rate 85%, green coverage \u226540%. Qinghe-Xiaoyue corridor links parks, wetlands. Full carbon-neutral MRV tracking.'),
        ('\u4ea4\u901a\u6162\u884c' if is_zh else 'Slow Mobility',
         'AI\u6162\u884c\u4e13\u7528\u905311.4km\uff0c\u7eff\u8272\u51fa\u884c\u226560%\u3002\u81ea\u52a8\u9a7e\u9a76\u914d\u9001+\u667a\u80fd\u5bfc\u822a\u3002\u516c\u5171\u7a7a\u95f4\u5168\u57df500m\u6b65\u884c\u534a\u5f84\u5168\u8986\u76d6\u3002' if is_zh
         else 'AI slow lane 11.4km, green mode \u226560%. Autonomous delivery + smart navigation. Public space within 500m walking radius.'),
        ('\u4f4e\u78b3\u667a\u6167' if is_zh else 'Low-Carbon',
         '\u53ef\u518d\u751f\u80fd\u6e90\u226520%\uff0c\u5149\u4f0f\u5e55\u5899+\u533a\u57df\u80fd\u6e90\u7ad9\u3002\u667a\u80fd\u706f\u6746\u3001\u73af\u5883\u4f20\u611f\u5668\u3001AI\u57ce\u5e02\u8fd0\u8425\u5e73\u53f0\u534f\u540c\u3002' if is_zh
         else 'Renewable \u226520%, PV facades + district stations. Smart streetlights, sensors, AI urban ops platform.'),
        ('\u6e10\u8fdb\u66f4\u65b0' if is_zh else 'Incremental',
         '\u4fdd\u7559\u63d0\u534745%+\u529f\u80fd\u7f6e\u636225%+\u7efc\u5408\u6574\u6cbb20%+\u62c6\u9664\u65b0\u5efa10%\u3002\u52063\u671f\u5b9e\u65bd\uff1a\u8fd1\u671f4\u9879\u76ee\u3001\u4e2d\u671f5\u9879\u76ee\u3001\u8fdc\u671f4\u9879\u76ee\u3002' if is_zh
         else 'Preserve 45% + Repurpose 25% + Renovate 20% + New 10%. 3 phases: Near 4, Mid 5, Long 4 projects.'),
        ('AI\u521b\u65b0\u751f\u6001' if is_zh else 'AI Ecosystem',
         '3\u5927AI\u671d\u5723\u5730\u6807\u3001AI MALL\u3001\u56fd\u9645\u8bba\u575b\u3001\u827a\u672f\u753b\u5eca\u300250+\u573a\u666f\u8282\u70b9\u3002\u53c2\u4e0e\u5f0f\u8bbe\u8ba1\u5e73\u53f0\u8fde\u63a5\u793e\u533a\u3002' if is_zh
         else '3 AI landmarks, AI MALL, Intl Forum, Art Gallery. 50+ scenario nodes. Participatory design platform.'),
    ]
    s_y = 0.93
    for label, detail in strategy_detail:
        ax_strat_a3.text(0.04, s_y, f'\u25a0 {label}', fontsize=13, fontweight='bold', color=C['dark'])
        ax_strat_a3.text(0.04, s_y - 0.035, detail, fontsize=10.5, color=C['text'],
                         linespacing=1.35, va='top')
        s_y -= 0.13

    # ── Footer ───────────────────────────────────────────
    fig.text(0.5, 0.0035, 'WorkBuddy (wlaura-wlj) | jingzhang-green-smart-ai-belt | professional_design_package | August 2026 | Data: OSM (ODbL) + Provisional Site Boundary',
             fontsize=9, color=C['muted'], ha='center')

    out = DRAW_DIR / f'a3-booklet{suffix}.pdf'
    fig.savefig(out, dpi=100, facecolor='white', edgecolor='none', format='pdf',
                bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved: {out} ({os.path.getsize(out)} bytes)")
    return out


# ════════════════════════════════════════════════════════════════
#  Shared vector map-drawing helpers (drawn directly, no image embed)
#  These replicate the figure content but accept a font-size (fs) and
#  line-width multiplier (lw) so the same map looks right on a small
#  PNG figure and on a huge A0 / A3 board.
# ════════════════════════════════════════════════════════════════

def _key_meta(lang):
    is_zh = (lang == 'zh')
    key_names = {
        '众智园AI自主创新加速区': '众智园' if is_zh else 'Zhongzhiyuan',
        '北京AI原点社区': 'AI原点社区' if is_zh else 'AI Origin',
        '大钟寺国际 AI 交流节点': '大钟寺' if is_zh else 'Dazhongsi',
    }
    key_colors_map = {
        '众智园AI自主创新加速区': C['key_1'],
        '北京AI原点社区': C['key_2'],
        '大钟寺国际 AI 交流节点': C['key_3'],
    }
    return key_names, key_colors_map


def map_site(ax, lang, fs=8, lw=1.0):
    """Draw the site-overview map directly into ax."""
    key_names, key_colors_map = _key_meta(lang)
    for feat in site['features']:
        plot_feature(ax, feat, facecolor=C['site_fill'], edgecolor=C['site_edge'],
                     linewidth=1.8 * lw, alpha=0.7, zorder=1)
    plot_patch_xy(ax, (extent[0], WATER_NORTH_Y, extent[1], extent[3]),
                  facecolor=C['water'], alpha=0.4, zorder=0)
    for feat in green_space['features']:
        plot_feature(ax, feat, facecolor=C['green_fill'], edgecolor=C['green_edge'],
                     linewidth=0.4 * lw, alpha=0.6, zorder=2)
    for feat in roads['features']:
        rtype = feat['properties'].get('road_type', '')
        rlw = (2.5 if rtype in ('expressway', 'arterial') else 1.5) * lw
        if rtype == 'slow_mobility':
            plot_line(ax, feat, C['slow'], linewidth=2.5 * lw, zorder=4, linestyle='--')
        else:
            plot_line(ax, feat, C['road'], linewidth=rlw, zorder=3)
    for feat in key_areas['features']:
        n_zh = feat['properties']['name_zh']
        lc = key_colors_map.get(n_zh, C['key_1'])
        plot_feature(ax, feat, facecolor=lc, edgecolor=lc, linewidth=1.5 * lw,
                     alpha=0.25, zorder=3)
        g = project_geom(shape(feat['geometry']))
        cx, cy = g.centroid.x, g.centroid.y
        label = key_names.get(n_zh, n_zh[:8])
        ax.annotate(label, xy=(cx, cy), fontsize=fs, fontweight='bold', color=lc,
                    ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                              edgecolor=lc, alpha=0.92, linewidth=1 * lw),
                    zorder=10)
    set_map_style(ax, extent)
    add_north_arrow(ax, extent[0] + 250, extent[3] - 500)
    add_scale_bar(ax, extent, y_pos_frac=0.04,
                  fontsize=max(8, int(fs * 0.7)), crs_fontsize=max(6, int(fs * 0.45)))


def map_landuse(ax, lang, fs=8, lw=1.0):
    """Draw the land-use map directly into ax."""
    is_zh = (lang == 'zh')
    lu_labels = {
        '0701': ('创新生活社区', 'Innovation Living', C['lu_residential']),
        '08': ('公共管理与服务', 'Public Service', C['lu_public']),
        '0802': ('AI核心创新区', 'AI Core Innovation', C['lu_ai_rd']),
        '1401': ('绿脉公园带', 'Green Park Belt', C['lu_green']),
        '16': ('蓝绿生态腹地', 'Blue-Green Hinterland', C['lu_water']),
        '05': ('智慧服务走廊', 'Smart Service Corridor', C['lu_commercial']),
    }
    name_to_code = {}
    for feat in land_use['features']:
        n = feat['properties']['name_zh']
        code = feat['properties']['land_use_code']
        if 'AI核心' in n: name_to_code[n] = '0802'
        elif '创新生活' in n: name_to_code[n] = '0701'
        elif '智慧服务' in n: name_to_code[n] = '05'
        elif '产业融合' in n: name_to_code[n] = '05'
        elif '公共管理' in n: name_to_code[n] = '08'
        elif '蓝绿' in n: name_to_code[n] = '16'
        else: name_to_code[n] = code
    for feat in land_use['features']:
        n_zh = feat['properties']['name_zh']
        code = name_to_code.get(n_zh, feat['properties']['land_use_code'])
        info = lu_labels.get(code)
        if info:
            lc = info[2]
            label_text = info[0] if is_zh else info[1]
        else:
            lc = C['lu_industry']
            label_text = n_zh[:6]
        plot_feature(ax, feat, facecolor=lc, edgecolor='white',
                     linewidth=0.6 * lw, alpha=0.7, zorder=2)
        g = project_geom(shape(feat['geometry']))
        cx, cy = g.centroid.x, g.centroid.y
        ax.annotate(label_text[:6], xy=(cx, cy), fontsize=fs * 0.7, color='white',
                    fontweight='bold', ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.15', facecolor=lc, alpha=0.85,
                              edgecolor='none'), zorder=8)
    for feat in roads['features']:
        rtype = feat['properties'].get('road_type', '')
        rlw = (1.8 if rtype in ('expressway', 'arterial') else 1.0) * lw
        plot_line(ax, feat, 'white', linewidth=rlw + 1.5 * lw, zorder=3)
        plot_line(ax, feat, C['road'], linewidth=rlw, zorder=4)
    set_map_style(ax, extent)
    add_north_arrow(ax, extent[0] + 250, extent[3] - 500)
    add_scale_bar(ax, extent, y_pos_frac=0.04,
                  fontsize=max(8, int(fs * 0.7)), crs_fontsize=max(6, int(fs * 0.45)))


def map_keyareas(ax, lang, fs=8, lw=1.0):
    """Draw the key-areas map (buildings + key-area outlines) directly."""
    key_names_map = {
        '众智园AI自主创新加速区': 0,
        '北京AI原点社区': 1,
        '大钟寺国际 AI 交流节点': 2,
    }
    key_colors = [C['key_1'], C['key_2'], C['key_3']]
    for feat in site['features']:
        plot_feature(ax, feat, facecolor=C['site_fill'], edgecolor=C['site_edge'],
                     linewidth=1.2 * lw, alpha=0.5, zorder=1)
    for feat in green_space['features']:
        plot_feature(ax, feat, facecolor=C['green_fill'], edgecolor=C['green_edge'],
                     linewidth=0.3 * lw, alpha=0.4, zorder=2)
    for feat in roads['features']:
        rtype = feat['properties'].get('road_type', '')
        rlw = (1.5 if rtype in ('expressway', 'arterial') else 0.8) * lw
        plot_line(ax, feat, C['road'], linewidth=rlw, zorder=3,
                  linestyle='--' if rtype == 'slow_mobility' else '-')
    bldg_types = {'ai_r_and_d': C['lu_ai_rd'], 'mixed_use': C['lu_mixed'],
                  'retail': C['lu_commercial'], 'residential': C['lu_residential']}
    for feat in buildings['features']:
        bt = feat['properties'].get('building_type', 'ai_r_and_d')
        lc = bldg_types.get(bt, C['muted'])
        plot_feature(ax, feat, facecolor=lc, edgecolor='white',
                     linewidth=0.3 * lw, alpha=0.7, zorder=5)
    for feat in key_areas['features']:
        n_zh = feat['properties']['name_zh']
        idx = key_names_map.get(n_zh, 0)
        lc = key_colors[idx]
        plot_feature(ax, feat, facecolor='none', edgecolor=lc,
                     linewidth=2.5 * lw, alpha=0.9, zorder=6, linestyle='-')
    set_map_style(ax, extent)
    add_north_arrow(ax, extent[0] + 250, extent[3] - 500)
    add_scale_bar(ax, extent, y_pos_frac=0.04,
                  fontsize=max(8, int(fs * 0.7)), crs_fontsize=max(6, int(fs * 0.45)))


def map_mobility(ax, lang, fs=8, lw=1.0):
    """Draw the mobility + blue-green map directly."""
    for feat in site['features']:
        plot_feature(ax, feat, facecolor=C['site_fill'], edgecolor=C['site_edge'],
                     linewidth=1.2 * lw, alpha=0.5, zorder=1)
    for feat in green_space['features']:
        plot_feature(ax, feat, facecolor=C['green_fill'], edgecolor=C['green_edge'],
                     linewidth=0.6 * lw, alpha=0.65, zorder=3)
    for feat in public_space['features']:
        plot_feature(ax, feat, facecolor='#FFF9C4', edgecolor='#F9A825',
                     linewidth=0.4 * lw, alpha=0.5, zorder=3)
    plot_patch_xy(ax, (extent[0], WATER_NORTH_Y, extent[1], extent[3]),
                  facecolor=C['water'], alpha=0.45, zorder=2)
    for feat in roads['features']:
        rtype = feat['properties'].get('road_type', '')
        if rtype == 'slow_mobility':
            plot_line(ax, feat, '#81C784', linewidth=6 * lw, zorder=4)
            plot_line(ax, feat, '#2E7D32', linewidth=3 * lw, zorder=5)
            plot_line(ax, feat, 'white', linewidth=1 * lw, zorder=6, linestyle='--')
        else:
            rlw = (1.2 if rtype in ('expressway', 'arterial') else 0.7) * lw
            plot_line(ax, feat, C['road'], linewidth=rlw, zorder=3, alpha=0.5)
    set_map_style(ax, extent)
    add_north_arrow(ax, extent[0] + 250, extent[3] - 500)
    add_scale_bar(ax, extent, y_pos_frac=0.04,
                  fontsize=max(8, int(fs * 0.7)), crs_fontsize=max(6, int(fs * 0.45)))


# ════════════════════════════════════════════════════════════════
#  NEW ANALYTICAL DIAGRAMS  (reference-board style)
# ════════════════════════════════════════════════════════════════

def _clean_ax(ax):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    ax.set_facecolor('white')
    for spine in ax.spines.values():
        spine.set_visible(False)


def draw_location_diagram(ax, lang, fs=9):
    """Nested location diagram: Beijing -> Haidian -> Site."""
    is_zh = (lang == 'zh')
    _clean_ax(ax)
    # Outer box: Beijing
    ax.add_patch(FancyBboxPatch((0.05, 0.32), 0.90, 0.60, boxstyle='round,pad=0.02',
                                 facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=1.2))
    ax.text(0.10, 0.86, '北京市' if is_zh else 'Beijing', fontsize=fs, fontweight='bold', color='#1565C0')
    ax.text(0.10, 0.79, 'Capital city / national S&T center', fontsize=fs-2, color=C['muted'])
    # Middle box: Haidian
    ax.add_patch(FancyBboxPatch((0.18, 0.38), 0.64, 0.38, boxstyle='round,pad=0.02',
                                 facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=1.2))
    ax.text(0.23, 0.70, '海淀区' if is_zh else 'Haidian District', fontsize=fs, fontweight='bold', color='#2E7D32')
    ax.text(0.23, 0.64, 'Zhongguancun / top universities', fontsize=fs-2, color=C['muted'])
    # Inner box: Site
    ax.add_patch(FancyBboxPatch((0.35, 0.43), 0.30, 0.22, boxstyle='round,pad=0.02',
                                 facecolor='#FFF3E0', edgecolor='#E65100', linewidth=1.5))
    ax.text(0.50, 0.58, '京张AI创新带' if is_zh else 'Jing-Zhang AI Belt', fontsize=fs, fontweight='bold',
            color='#E65100', ha='center')
    ax.text(0.50, 0.50, '11.4 km²', fontsize=fs-1, color=C['muted'], ha='center')
    # Arrows
    ax.annotate('', xy=(0.50, 0.65), xytext=(0.50, 0.78),
                arrowprops=dict(arrowstyle='->', color=C['muted'], lw=1))
    ax.annotate('', xy=(0.50, 0.65), xytext=(0.50, 0.78),
                arrowprops=dict(arrowstyle='->', color=C['muted'], lw=1))
    # Context bullets
    bullets = [
        ('• 清华/北大/北航/北邮' if is_zh else '• Tsinghua/PKU/Beihang/BUPT', 0.08, 0.22),
        ('• 中关村科学城核心区' if is_zh else '• Zhongguancun Science City', 0.08, 0.15),
        ('• 京张铁路遗址公园带' if is_zh else '• Jing-Zhang Railway Heritage', 0.08, 0.08),
    ]
    for txt, x, y in bullets:
        ax.text(x, y, txt, fontsize=fs-1.5, color=C['text'])


def draw_constraints_map(ax, lang, fs=8, lw=1.0):
    """Map of existing constraints and opportunities."""
    is_zh = (lang == 'zh')
    # Base
    for feat in site['features']:
        plot_feature(ax, feat, facecolor='#FAFAFA', edgecolor=C['site_edge'],
                     linewidth=1.2*lw, alpha=0.6, zorder=1)
    for feat in green_space['features']:
        plot_feature(ax, feat, facecolor=C['green_fill'], edgecolor=C['green_edge'],
                     linewidth=0.4*lw, alpha=0.5, zorder=2)
    for feat in roads['features']:
        rtype = feat['properties'].get('road_type', '')
        rlw = (1.5 if rtype in ('expressway','arterial') else 0.8) * lw
        plot_line(ax, feat, C['road'], linewidth=rlw, zorder=3, alpha=0.6)
    # Constraints
    layer_colors = {
        'HERITAGE_PROTECTION': '#8D6E63',
        'WATER_SYSTEM': '#42A5F5',
        'EXISTING_RAIL': '#78909C',
        'REGULATORY_CONTROL': '#FFB74D',
    }
    for feat in constraints['features']:
        layer = feat['properties']['layer']
        color = layer_colors.get(layer, C['muted'])
        geom = project_geom(shape(feat['geometry']))
        if geom.geom_type == 'LineString':
            x, y = geom.xy
            ax.plot(x, y, color=color, linewidth=2.5*lw, zorder=5, linestyle='-')
        elif geom.geom_type == 'Polygon':
            plot_feature(ax, feat, facecolor=color, edgecolor=color,
                         linewidth=1*lw, alpha=0.25, zorder=4, geom=geom)
    set_map_style(ax, extent)
    add_north_arrow(ax, extent[0]+250, extent[3]-500, fontsize=max(6, int(fs*0.7)))
    add_scale_bar(ax, extent, y_pos_frac=0.04, fontsize=max(6, int(fs*0.7)),
                  crs_fontsize=max(5, int(fs*0.45)))
    # Legend
    leg = [
        ('#8D6E63', '#8D6E63', '文保/铁路遗址' if is_zh else 'Heritage / Rail'),
        ('#42A5F5', '#42A5F5', '水系蓝线' if is_zh else 'Water Blue Line'),
        ('#78909C', '#78909C', '轨道走廊' if is_zh else 'Rail Corridor'),
        ('#FFB74D', '#FFB74D', '高校用地' if is_zh else 'University Land'),
    ]
    panel_legend(ax, leg, fs, title='现状约束' if is_zh else 'Constraints')


def draw_transport_map(ax, lang, fs=8, lw=1.0):
    """Transport analysis: road hierarchy + slow mobility + key nodes."""
    is_zh = (lang == 'zh')
    for feat in site['features']:
        plot_feature(ax, feat, facecolor='#FAFAFA', edgecolor=C['site_edge'],
                     linewidth=1.0*lw, alpha=0.4, zorder=1)
    # Roads by hierarchy
    for feat in roads['features']:
        rtype = feat['properties'].get('road_type', '')
        if rtype == 'slow_mobility':
            plot_line(ax, feat, '#81C784', linewidth=5*lw, zorder=4)
            plot_line(ax, feat, '#2E7D32', linewidth=2.5*lw, zorder=5)
        elif rtype in ('expressway', 'arterial'):
            plot_line(ax, feat, '#37474F', linewidth=2.2*lw, zorder=3)
        else:
            plot_line(ax, feat, '#90A4AE', linewidth=1.0*lw, zorder=2, alpha=0.7)
    # Key areas as nodes
    key_names, key_colors = _key_meta(lang)
    for feat in key_areas['features']:
        n_zh = feat['properties']['name_zh']
        lc = key_colors.get(n_zh, C['key_1'])
        g = project_geom(shape(feat['geometry']))
        cx, cy = g.centroid.x, g.centroid.y
        ax.scatter(cx, cy, s=80*lw, c=lc, zorder=6, edgecolors='white', linewidths=1)
    set_map_style(ax, extent)
    add_north_arrow(ax, extent[0]+250, extent[3]-500, fontsize=max(6, int(fs*0.7)))
    add_scale_bar(ax, extent, y_pos_frac=0.04, fontsize=max(6, int(fs*0.7)),
                  crs_fontsize=max(5, int(fs*0.45)))
    leg = [
        ('#37474F', '#37474F', '快速路/主干道' if is_zh else 'Arterial'),
        ('#90A4AE', '#90A4AE', '次干道/支路' if is_zh else 'Local Roads'),
        ('#2E7D32', '#81C784', 'AI慢行专用道' if is_zh else 'AI Slow Lane'),
        (C['key_1'], C['key_1'], '重点节点' if is_zh else 'Key Nodes'),
    ]
    panel_legend(ax, leg, fs, title='交通分析' if is_zh else 'Transport')


def draw_phasing_map(ax, lang, fs=8, lw=1.0):
    """Phasing implementation map."""
    is_zh = (lang == 'zh')
    for feat in site['features']:
        plot_feature(ax, feat, facecolor='#FAFAFA', edgecolor=C['site_edge'],
                     linewidth=1.0*lw, alpha=0.4, zorder=1)
    for feat in roads['features']:
        rtype = feat['properties'].get('road_type', '')
        rlw = (1.2 if rtype in ('expressway','arterial') else 0.7) * lw
        plot_line(ax, feat, C['road'], linewidth=rlw, zorder=2, alpha=0.5)
    phase_colors = {
        'near_term': '#2E7D32',
        'mid_term': '#1565C0',
        'long_term': '#F57C00',
    }
    phase_labels = {
        'near_term': '近期 1-3年' if is_zh else 'Near 1-3yr',
        'mid_term': '中期 3-7年' if is_zh else 'Mid 3-7yr',
        'long_term': '远期 7-15年' if is_zh else 'Long 7-15yr',
    }
    for feat in phasing['features']:
        phase = feat['properties']['phase_category']
        color = phase_colors.get(phase, C['muted'])
        geom = project_geom(shape(feat['geometry']))
        plot_feature(ax, feat, facecolor=color, edgecolor=color,
                     linewidth=1*lw, alpha=0.35, zorder=3, geom=geom)
    set_map_style(ax, extent)
    add_north_arrow(ax, extent[0]+250, extent[3]-500, fontsize=max(6, int(fs*0.7)))
    add_scale_bar(ax, extent, y_pos_frac=0.04, fontsize=max(6, int(fs*0.7)),
                  crs_fontsize=max(5, int(fs*0.45)))
    leg = [(c, c, phase_labels[p]) for p, c in phase_colors.items()]
    panel_legend(ax, leg, fs, title='分期实施' if is_zh else 'Phasing')


def draw_concept_diagram(ax, lang, fs=9):
    """Conceptual framework diagram: 1 Belt + 3 Cores + 2 Wings."""
    is_zh = (lang == 'zh')
    _clean_ax(ax)
    # Central spine
    ax.add_patch(FancyBboxPatch((0.38, 0.12), 0.24, 0.76, boxstyle='round,pad=0.02',
                                 facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=2))
    ax.text(0.50, 0.88, '一带' if is_zh else 'Belt', fontsize=fs+1, fontweight='bold',
            color='#1B5E20', ha='center')
    ax.text(0.50, 0.80, '京张绿脉\n11.4km' if is_zh else 'Jing-Zhang\nGreen Spine', fontsize=fs-1,
            color='#2E7D32', ha='center', linespacing=1.3)
    ax.text(0.50, 0.45, 'AI慢行专用道\n蓝绿走廊' if is_zh else 'AI Slow Lane\nBlue-Green Corridor',
            fontsize=fs-2, color=C['text'], ha='center', linespacing=1.2)
    # 3 cores along spine
    cores = [
        (0.50, 0.68, C['key_1'], '众智园' if is_zh else 'Zhongzhiyuan', 'AI全栈创新'),
        (0.50, 0.52, C['key_2'], 'AI原点' if is_zh else 'AI Origin', '创业生态'),
        (0.50, 0.32, C['key_3'], '大钟寺' if is_zh else 'Dazhongsi', '交流展示'),
    ]
    for x, y, color, name, sub in cores:
        ax.add_patch(FancyBboxPatch((x-0.10, y-0.05), 0.20, 0.10, boxstyle='round,pad=0.02',
                                     facecolor=color, edgecolor='white', linewidth=1.5))
        ax.text(x, y+0.015, name, fontsize=fs-1, fontweight='bold', color='white', ha='center')
        ax.text(x, y-0.025, sub, fontsize=fs-3, color='white', ha='center')
    # 2 wings
    ax.add_patch(FancyBboxPatch((0.06, 0.45), 0.26, 0.18, boxstyle='round,pad=0.02',
                                 facecolor='#E1BEE7', edgecolor='#7B1FA2', linewidth=1.5))
    ax.text(0.19, 0.56, '两翼' if is_zh else 'Wing', fontsize=fs, fontweight='bold',
            color='#7B1FA2', ha='center')
    ax.text(0.19, 0.50, '学院路\n创新翼' if is_zh else 'Xueyuan Rd\nInnovation', fontsize=fs-2,
            color='#7B1FA2', ha='center', linespacing=1.2)
    ax.add_patch(FancyBboxPatch((0.68, 0.45), 0.26, 0.18, boxstyle='round,pad=0.02',
                                 facecolor='#B3E5FC', edgecolor='#0288D1', linewidth=1.5))
    ax.text(0.81, 0.56, '两翼' if is_zh else 'Wing', fontsize=fs, fontweight='bold',
            color='#0288D1', ha='center')
    ax.text(0.81, 0.50, '中关村\n产业翼' if is_zh else 'Zhongguancun\nIndustry', fontsize=fs-2,
            color='#0288D1', ha='center', linespacing=1.2)
    # Arrows from wings to spine
    ax.annotate('', xy=(0.38, 0.54), xytext=(0.32, 0.54),
                arrowprops=dict(arrowstyle='->', color='#7B1FA2', lw=1.5))
    ax.annotate('', xy=(0.62, 0.54), xytext=(0.68, 0.54),
                arrowprops=dict(arrowstyle='->', color='#0288D1', lw=1.5))




def add_panel(fig, rect, num, title, fs):
    """Create a figure panel: a navy header strip (figure number + title)
    above a clean content axes. Returns the content axes."""
    x, y, w, h = rect
    hhead = min(0.055, h * 0.22)
    axh = fig.add_axes([x, y + h - hhead, w, hhead])
    _clean_ax(axh)
    axh.set_facecolor('#0D1B5C')
    axh.text(0.02, 0.5, num, fontsize=fs, fontweight='bold', color='#FFFFFF',
             va='center', transform=axh.transAxes)
    axh.text(0.20, 0.5, title, fontsize=fs * 0.80, fontweight='bold', color='#E3F2FD',
             va='center', transform=axh.transAxes)
    axc = fig.add_axes([x, y, w, h - hhead])
    _clean_ax(axc)
    return axc


def draw_regional_context(ax, lang, fs=14):
    """Regional context map: site highlighted within wider Haidian/BJ context."""
    is_zh = (lang == 'zh')
    reg = get_extent(4500)
    for feat in green_space['features']:
        plot_feature(ax, feat, facecolor=C['green_fill'], edgecolor='none',
                     linewidth=0, alpha=0.35, zorder=0)
    for feat in roads['features']:
        rtype = feat['properties'].get('road_type', '')
        rlw = (2.2 if rtype in ('expressway', 'arterial') else 0.8)
        plot_line(ax, feat, C['road'], linewidth=rlw, zorder=1, alpha=0.55)
    for feat in site['features']:
        plot_feature(ax, feat, facecolor=C['site_fill'], edgecolor=C['site_edge'],
                     linewidth=2.5, alpha=0.85, zorder=3)
    set_map_style(ax, reg)
    add_north_arrow(ax, reg[0] + 450, reg[3] - 750, fontsize=max(9, int(fs * 0.6)))
    add_scale_bar(ax, reg, y_pos_frac=0.05, fontsize=max(9, int(fs * 0.6)),
                  crs_fontsize=max(7, int(fs * 0.45)))
    g = project_geom(shape(site['features'][0]['geometry']))
    cx, cy = g.centroid.x, g.centroid.y
    ax.annotate('京张AI创新带' if is_zh else 'Jing-Zhang AI Belt',
                xy=(cx, cy), fontsize=fs, fontweight='bold', color=C['dark'],
                ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor=C['site_edge'], alpha=0.92, linewidth=1.2),
                zorder=10)


def draw_section_profile(ax, lang, fs=13):
    """Illustrative corridor cross-section (north->south) along the green spine."""
    is_zh = (lang == 'zh')
    _clean_ax(ax)
    ax.add_patch(Rectangle((0, 0.58), 1, 0.42, facecolor='#E3F2FD', zorder=0))
    ax.add_patch(mpatches.Circle((0.90, 0.90), 0.05, facecolor='#FFD54F', zorder=1))
    ax.add_patch(Rectangle((0, 0), 1, 0.58, facecolor='#F1F8E9', zorder=0))
    ax.plot([0, 1], [0.58, 0.58], color='#558B2F', lw=2.5, zorder=2)
    for (x, w, h, c) in [(0.03, 0.07, 0.20, '#90A4AE'), (0.12, 0.06, 0.28, '#78909C'),
                         (0.20, 0.07, 0.16, '#B0BEC5')]:
        ax.add_patch(Rectangle((x, 0.58), w, h, facecolor=c, zorder=3))
    ax.add_patch(Rectangle((0.40, 0.58), 0.20, 0.16, facecolor='#66BB6A', zorder=3))
    for tx in [0.43, 0.47, 0.51, 0.55]:
        ax.add_patch(mpatches.Circle((tx, 0.80), 0.035, facecolor='#2E7D32', zorder=4))
    ax.plot([0.40, 0.60], [0.74, 0.74], color='#E65100', lw=3, zorder=4)
    for (x, w, h, c) in [(0.64, 0.06, 0.42, '#5C6BC0'), (0.72, 0.07, 0.55, '#3949AB'),
                         (0.81, 0.06, 0.38, '#42A5F5')]:
        ax.add_patch(Rectangle((x, 0.58), w, h, facecolor=c, zorder=3))
        ax.add_patch(Rectangle((x, 0.58 + h), w, 0.015, facecolor='#212121', zorder=4))
    ax.plot([0, 1], [0.30, 0.30], color='#1565C0', lw=3.5, zorder=5)
    ax.text(0.02, 0.345, '地铁/铁路' if is_zh else 'Metro / Rail', fontsize=fs - 3,
            color='#1565C0', zorder=6)
    ax.text(0.10, 0.92, '现状建成区' if is_zh else 'Existing Fabric', fontsize=fs - 3,
            color='#37474F', ha='center')
    ax.text(0.50, 0.92, '京张绿脉公园带' if is_zh else 'Green Spine Park', fontsize=fs - 3,
            color='#1B5E20', ha='center')
    ax.text(0.74, 0.99, 'AI 地标集群' if is_zh else 'AI Landmark Cluster', fontsize=fs - 3,
            color='#1A237E', ha='center')
    ax.text(0.50, 0.055, '北 ↑ → 南  (示意断面 / Schematic Section)' if is_zh
            else 'N up -> S  (Schematic Section)', fontsize=fs - 3, color=C['muted'],
            ha='center')


def draw_metrics_radar(ax, lang, fs=13):
    """Radar chart of 6 core performance metrics vs targets."""
    import numpy as np
    is_zh = (lang == 'zh')
    cats = (['绿化', '海绵', '可再生', '慢行', '公共空间', 'AI场景'] if is_zh
            else ['Green', 'Sponge', 'Renew', 'Slow', 'Public', 'AI'])
    vals = [0.88, 0.85, 0.85, 0.90, 1.00, 0.90]
    shown = (['35%', '85%', '20%', '60%', '100%', '50+'] if is_zh
             else ['35%', '85%', '20%', '60%', '100%', '50+'])
    N = len(cats)
    ang = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    ang_c = ang + [ang[0]]
    _clean_ax(ax)
    for r in [0.25, 0.5, 0.75, 1.0]:
        ax.plot(np.cos(ang_c) * r, np.sin(ang_c) * r, color='#B0BEC5', lw=0.8, zorder=1)
    for a in ang:
        ax.plot([0, np.cos(a)], [0, np.sin(a)], color='#CFD8DC', lw=0.8, zorder=1)
    v_c = vals + [vals[0]]
    ax.plot(np.cos(ang_c) * v_c, np.sin(ang_c) * v_c, color='#1A237E', lw=2.2, zorder=3)
    ax.fill(np.cos(ang_c) * v_c, np.sin(ang_c) * v_c, color='#1A237E', alpha=0.18, zorder=2)
    for i, a in enumerate(ang):
        lx, ly = np.cos(a) * 1.18, np.sin(a) * 1.18
        ax.text(lx, ly, cats[i], fontsize=fs - 2, ha='center', va='center',
                fontweight='bold', color=C['dark'], zorder=4)
        ax.text(np.cos(a) * vals[i], np.sin(a) * vals[i], shown[i], fontsize=fs - 3,
                ha='center', va='center', color='#1A237E', fontweight='bold', zorder=5)
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.35, 1.35)
    ax.set_aspect('equal')


def draw_principles(ax, lang, fs=13):
    """Four design principles as numbered badge rows."""
    is_zh = (lang == 'zh')
    _clean_ax(ax)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    items = ([
        ('1', '#2E7D32', '生态优先', '蓝绿为底 · 低碳韧性'),
        ('2', '#1565C0', '创新驱动', 'AI全栈 · 产研一体'),
        ('3', '#E65100', '以人为本', '慢行友好 · 活力公共空间'),
        ('4', '#7B1FA2', '文保再生', '铁路遗址活化 · 新旧共生'),
    ] if is_zh else [
        ('1', '#2E7D32', 'Eco-First', 'Blue-green, low-carbon'),
        ('2', '#1565C0', 'Innovation', 'AI full-stack R&D'),
        ('3', '#E65100', 'People', 'Walkable, vibrant space'),
        ('4', '#7B1FA2', 'Heritage', 'Rail reuse, symbiosis'),
    ])
    n = len(items)
    rh = 0.92 / n
    for i, (num, col, title, desc) in enumerate(items):
        y = 0.96 - (i + 0.5) * rh
        ax.add_patch(mpatches.Circle((0.10, y), 0.045, facecolor=col, edgecolor='white', linewidth=1.5, zorder=3))
        ax.text(0.10, y, num, fontsize=fs, fontweight='bold', color='white', ha='center', va='center', zorder=4)
        ax.text(0.22, y + 0.028, title, fontsize=fs + 1, fontweight='bold', color=C['dark'], va='center')
        ax.text(0.22, y - 0.028, desc, fontsize=fs - 2, color=C['muted'], va='center')
        if i < n - 1:
            ax.plot([0.10, 0.95], [y - rh/2, y - rh/2], color='#E0E0E0', lw=1, zorder=1)


def draw_strategy_diagram(ax, lang, fs=13):
    """Six planning strategies as a numbered list."""
    is_zh = (lang == 'zh')
    _clean_ax(ax)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    items = ([
        ('1', '#2E7D32', '一带贯城', '11.4km 绿脉公园带串联清河-中关村'),
        ('2', '#1565C0', '三芯聚智', '众智园·AI原点·大钟寺三大重点片区'),
        ('3', '#7B1FA2', '两翼协同', '学院路创新翼 + 中关村产业翼'),
        ('4', '#00897B', '蓝绿织网', '清河-小月河修复，海绵城市 85%'),
        ('5', '#E65100', '慢行成网', 'AI 慢行专用道，绿色出行 ≥60%'),
        ('6', '#5E35B1', '智慧赋能', '50+ AI 场景，全栈创新策源'),
    ] if is_zh else [
        ('1', '#2E7D32', 'One Belt', '11.4km green spine N-S'),
        ('2', '#1565C0', 'Three Cores', 'Zhongzhi/Origin/Dazhongsi'),
        ('3', '#7B1FA2', 'Two Wings', 'Xueyuan Rd + Zhongguancun'),
        ('4', '#00897B', 'Blue-Green', 'Qinghe restore, 85% sponge'),
        ('5', '#E65100', 'Slow Network', 'AI slow lanes, ≥60% green'),
        ('6', '#5E35B1', 'Smart Empower', '50+ AI scenarios'),
    ])
    n = len(items)
    rh = 0.94 / n
    for i, (num, col, title, desc) in enumerate(items):
        y = 0.96 - (i + 0.5) * rh
        ax.add_patch(FancyBboxPatch((0.04, y - rh*0.40), 0.12, rh*0.80, boxstyle='round,pad=0.02',
                                    facecolor=col, edgecolor='white', linewidth=1, zorder=3))
        ax.text(0.10, y, num, fontsize=fs, fontweight='bold', color='white', ha='center', va='center', zorder=4)
        ax.text(0.20, y + 0.026, title, fontsize=fs + 1, fontweight='bold', color=C['dark'], va='center')
        ax.text(0.20, y - 0.030, desc, fontsize=fs - 3, color=C['text'], va='center')


def draw_roadmap(ax, lang, fs=13):
    """Three-phase implementation roadmap as a vertical timeline."""
    is_zh = (lang == 'zh')
    _clean_ax(ax)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    phases = ([
        ('近期 1-3年', '#2E7D32', ['绿脉公园示范段', '众智园启动建设', 'AI慢行示范道']),
        ('中期 3-7年', '#1565C0', ['AI原点社区落成', '大钟寺AI MALL', '清河湿地修复']),
        ('远期 7-15年', '#F57C00', ['全线公园贯通', '智慧运营中枢', '区域创新联动']),
    ] if is_zh else [
        ('Near 1-3y', '#2E7D32', ['Green spine demo', 'Zhongzhiyuan start', 'AI slow lane demo']),
        ('Mid 3-7y', '#1565C0', ['AI Origin built', 'Dazhongsi AI MALL', 'Qinghe wetland']),
        ('Long 7-15y', '#F57C00', ['Full corridor', 'Smart ops hub', 'Regional link']),
    ])
    n = len(phases)
    rh = 0.94 / n
    ax.plot([0.14, 0.14], [0.05, 0.95], color='#B0BEC5', lw=2.5, zorder=1)
    for i, (name, col, acts) in enumerate(phases):
        y = 0.96 - (i + 0.5) * rh
        ax.add_patch(mpatches.Circle((0.14, y), 0.05, facecolor=col, edgecolor='white', linewidth=1.5, zorder=3))
        ax.text(0.14, y, str(i+1), fontsize=fs, fontweight='bold', color='white', ha='center', va='center', zorder=4)
        ax.text(0.26, y + rh*0.30, name, fontsize=fs + 1, fontweight='bold', color=col, va='center')
        for j, a in enumerate(acts):
            ax.text(0.26, y + rh*0.08 - j*rh*0.20, '· ' + a, fontsize=fs - 3, color=C['text'], va='center')
        if i < n - 1:
            ax.annotate('', xy=(0.14, y - rh*0.50), xytext=(0.14, y - rh*0.42),
                        arrowprops=dict(arrowstyle='->', color=col, lw=1.5))


def draw_vision_strip(fig, rect, lang, fs=11):
    """Full-width bottom strip of six vision photo-cards."""
    is_zh = (lang == 'zh')
    x, y, w, h = rect
    axbg = fig.add_axes([x, y, w, h])
    _clean_ax(axbg)
    axbg.add_patch(Rectangle((0, 0), 1, 1, facecolor='#EEF2F8', edgecolor='none'))
    axbg.add_patch(Rectangle((0, 0), 1, 1, facecolor='none', edgecolor='#0D1B5C', linewidth=1.2))
    axbg.text(0.014, 0.5, '项目愿景 VISION' if is_zh else 'VISION',
              fontsize=fs + 2, fontweight='bold', color=C['dark'], va='center', transform=axbg.transAxes)
    cards = ([
        ('park', '京张绿脉公园', '11.4km连续公园带', '#C8E6C9'),
        ('ai', '众智园AI区', 'AI全栈创新策源地', '#D1C4E9'),
        ('community', 'AI原点社区', '创业生态+人才公寓', '#B3E5FC'),
        ('mall', '大钟寺AI MALL', '展示交流+体验消费', '#FFECB3'),
        ('bike', 'AI慢行专用道', '绿色出行≥60%', '#C8E6C9'),
        ('water', '清河湿地修复', '海绵城市85%', '#BBDEFB'),
    ] if is_zh else [
        ('park', 'Green Spine Park', '11.4km continuous', '#C8E6C9'),
        ('ai', 'Zhongzhi AI', 'AI innovation hub', '#D1C4E9'),
        ('community', 'AI Origin', 'Startup + housing', '#B3E5FC'),
        ('mall', 'Dazhongsi MALL', 'Expo + retail', '#FFECB3'),
        ('bike', 'AI Slow Lane', '>=60% green trip', '#C8E6C9'),
        ('water', 'Qinghe Wetland', '85% sponge city', '#BBDEFB'),
    ])
    label_w = 0.15
    cw = (w - label_w) / len(cards)
    for i, (icon_type, title, sub, color) in enumerate(cards):
        cx = x + label_w + i * cw
        axc = fig.add_axes([cx + cw*0.015, y + h*0.08, cw*0.97, h*0.84])
        draw_photo_card(axc, color, icon_type, title, sub, lang, fs=fs)


def draw_simple_icon(ax, icon_type, color, fs=10):
    """Draw a simple vector icon (replaces emoji which may not render in CJK fonts)."""
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    ax.set_facecolor('none')
    if icon_type == 'factory':
        ax.add_patch(Rectangle((0.25, 0.25), 0.40, 0.35, facecolor=color, edgecolor='none'))
        ax.add_patch(Rectangle((0.35, 0.60), 0.08, 0.22, facecolor=color, edgecolor='none'))
        ax.add_patch(Rectangle((0.50, 0.60), 0.08, 0.18, facecolor=color, edgecolor='none'))
    elif icon_type == 'car':
        ax.add_patch(FancyBboxPatch((0.18, 0.35), 0.64, 0.28, boxstyle='round,pad=0.03',
                                     facecolor=color, edgecolor='none'))
        ax.add_patch(mpatches.Circle((0.32, 0.30), 0.08, facecolor=color, edgecolor='none'))
        ax.add_patch(mpatches.Circle((0.68, 0.30), 0.08, facecolor=color, edgecolor='none'))
    elif icon_type == 'tree':
        ax.add_patch(mpatches.Circle((0.50, 0.55), 0.28, facecolor=color, edgecolor='none'))
        ax.add_patch(Rectangle((0.44, 0.18), 0.12, 0.25, facecolor='#8D6E63', edgecolor='none'))
    elif icon_type == 'heritage':
        ax.add_patch(Rectangle((0.20, 0.22), 0.60, 0.45, facecolor=color, edgecolor='none'))
        ax.add_patch(mpatches.Polygon([[0.20, 0.67], [0.50, 0.88], [0.80, 0.67]],
                                       facecolor=color, edgecolor='none'))
    elif icon_type == 'park':
        ax.add_patch(mpatches.Circle((0.50, 0.50), 0.32, facecolor=color, edgecolor='none'))
        ax.plot([0.50, 0.50], [0.25, 0.75], color='white', linewidth=2)
        ax.plot([0.25, 0.75], [0.50, 0.50], color='white', linewidth=2)
    elif icon_type == 'ai':
        ax.add_patch(FancyBboxPatch((0.20, 0.25), 0.60, 0.50, boxstyle='round,pad=0.05',
                                     facecolor=color, edgecolor='none'))
        ax.text(0.50, 0.50, 'AI', fontsize=fs+4, fontweight='bold', color='white',
                ha='center', va='center')
    elif icon_type == 'community':
        ax.add_patch(Rectangle((0.22, 0.25), 0.22, 0.35, facecolor=color, edgecolor='none'))
        ax.add_patch(Rectangle((0.50, 0.25), 0.28, 0.45, facecolor=color, edgecolor='none'))
        ax.add_patch(mpatches.Polygon([[0.22, 0.60], [0.33, 0.78], [0.44, 0.60]], facecolor=color, edgecolor='none'))
        ax.add_patch(mpatches.Polygon([[0.50, 0.70], [0.64, 0.90], [0.78, 0.70]], facecolor=color, edgecolor='none'))
    elif icon_type == 'mall':
        ax.add_patch(Rectangle((0.18, 0.22), 0.64, 0.50, facecolor=color, edgecolor='none'))
        ax.add_patch(Rectangle((0.30, 0.22), 0.15, 0.30, facecolor='white', edgecolor='none'))
        ax.add_patch(Rectangle((0.55, 0.22), 0.15, 0.30, facecolor='white', edgecolor='none'))
    elif icon_type == 'bike':
        ax.add_patch(mpatches.Circle((0.32, 0.38), 0.14, facecolor='none', edgecolor=color, linewidth=2.5))
        ax.add_patch(mpatches.Circle((0.68, 0.38), 0.14, facecolor='none', edgecolor=color, linewidth=2.5))
        ax.plot([0.32, 0.50, 0.68], [0.38, 0.62, 0.38], color=color, linewidth=2.5)
    elif icon_type == 'water':
        ax.add_patch(mpatches.Ellipse((0.50, 0.45), 0.55, 0.40, facecolor=color, edgecolor='none'))


def draw_photo_card(ax, color, icon_type, title, subtitle, lang, fs=9):
    """A colored card representing a site photo / scene (placeholder)."""
    is_zh = (lang == 'zh')
    _clean_ax(ax)
    # Photo area with gradient-like fill
    ax.add_patch(Rectangle((0, 0.25), 1, 0.75, facecolor=color, edgecolor='none', alpha=0.30))
    ax.add_patch(Rectangle((0, 0), 1, 0.25, facecolor='white', edgecolor='none'))
    # Icon sub-axes
    ax_icon = ax.inset_axes([0.30, 0.42, 0.40, 0.42])
    draw_simple_icon(ax_icon, icon_type, color, fs=fs+2)
    ax.text(0.50, 0.45, title, fontsize=fs, fontweight='bold', color=C['dark'], ha='center')
    ax.text(0.50, 0.30, subtitle, fontsize=fs-2, color=C['muted'], ha='center')


def draw_problem_card(ax, icon_type, title, desc, color, lang, fs=10):
    """Small card with icon + title + description for site problems."""
    _clean_ax(ax)
    # Stronger left border stripe
    ax.add_patch(Rectangle((0, 0), 0.04, 1, facecolor=color, edgecolor='none', alpha=0.9))
    ax.add_patch(FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle='round,pad=0.02',
                                 facecolor='#FAFAFA', edgecolor=color, alpha=0.95, linewidth=1.5))
    # Icon sub-axes
    ax_icon = ax.inset_axes([0.04, 0.52, 0.22, 0.38])
    draw_simple_icon(ax_icon, icon_type, color, fs=fs)
    ax.text(0.30, 0.76, title, fontsize=fs+1, fontweight='bold', color=C['dark'], va='center')
    ax.text(0.06, 0.52, desc, fontsize=fs-1, color=C['text'], va='top', linespacing=1.35)


def draw_small_bar_chart(ax, labels, values, colors, title, lang, fs=8):
    """Compact horizontal bar chart for side panels."""
    _clean_ax(ax)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    y_step = 0.85 / len(labels)
    for i, (lab, val, col) in enumerate(zip(labels, values, colors)):
        y = 0.90 - (i + 0.5) * y_step
        ax.barh(y, val * 0.75, height=y_step * 0.55, left=0.18, color=col, alpha=0.85,
                edgecolor='white', linewidth=0.5)
        ax.text(0.02, y, lab, fontsize=fs-1, color=C['text'], va='center')
        ax.text(0.18 + val * 0.75 + 0.02, y, f'{val:.0%}' if val <= 1 else f'{int(val)}',
                fontsize=fs-1, color=C['dark'], va='center', fontweight='bold')
    ax.text(0.02, 0.96, title, fontsize=fs+1, fontweight='bold', color=C['dark'])


def panel_legend(ax, items, fs, title=None):
    """Overlay a legend box (top-right) inside a map axes using axes-fraction coords."""
    n = len(items)
    x0, y0 = 0.62, 0.98
    ax.add_patch(Rectangle((x0 - 0.04, y0 - 0.03 - n * 0.072), 0.42, 0.05 + n * 0.072,
                           transform=ax.transAxes, facecolor='white', edgecolor='none',
                           alpha=0.78, zorder=30))
    if title:
        ax.text(x0 - 0.02, y0 + 0.005, title, fontsize=max(8, int(fs * 0.85)),
                fontweight='bold', color=C['dark'], transform=ax.transAxes,
                va='top', ha='left', zorder=31)
    for i, (fc, ec, lab) in enumerate(items):
        yy = y0 - 0.06 - i * 0.072
        ax.add_patch(Rectangle((x0, yy), 0.04, 0.032, transform=ax.transAxes,
                               facecolor=fc, edgecolor=ec, linewidth=0.8, zorder=31))
        ax.text(x0 + 0.06, yy + 0.016, lab, fontsize=max(7, int(fs * 0.72)),
                color=C['text'], transform=ax.transAxes, va='center', ha='left', zorder=31)


def map_panel(fig, rect, mapfn, lang, fs, lw, legend_items, title,
              caption=None, title_fs=30, cap_fs=13):
    """A map panel = a framed map (left ~66%) + a side text/legend area (right)."""
    rx, ry, rw, rh = rect
    mw = rw * 0.64
    ax = fig.add_axes([rx, ry, mw, rh])
    mapfn(ax, lang, fs=fs, lw=lw)
    ax.set_title(title, fontsize=title_fs, fontweight='bold', color=C['dark'], pad=8)
    # side panel
    sx = rx + mw + rw * 0.02
    sw = rw - mw - rw * 0.02
    tax = fig.add_axes([sx, ry, sw, rh])
    tax.set_xlim(0, 1); tax.set_ylim(0, 1); tax.axis('off')
    ly = 0.94
    for (fc, ec, lab) in legend_items:
        tax.add_patch(Rectangle((0.04, ly - 0.032), 0.11, 0.03,
                                facecolor=fc, edgecolor=ec, linewidth=0.8))
        tax.text(0.20, ly - 0.017, lab, fontsize=cap_fs, color=C['text'], va='center')
        ly -= 0.075
    if caption:
        tax.text(0.04, ly - 0.01, caption, fontsize=cap_fs - 1, color=C['text'],
                 va='top', linespacing=1.4)
    return ax


def map_only(fig, rect, mapfn, lang, fs, lw, legend_items, title, title_fs=22):
    """A single map filling the rect, with an overlaid legend (for narrow slots)."""
    rx, ry, rw, rh = rect
    ax = fig.add_axes([rx, ry, rw, rh])
    mapfn(ax, lang, fs=fs, lw=lw)
    ax.set_title(title, fontsize=title_fs, fontweight='bold', color=C['dark'], pad=6)
    panel_legend(ax, legend_items, fs, title=None)
    return ax


def add_metrics_panel(fig, rect, lang, fs):
    """Draw the 4-chart metrics dashboard directly into a wide rect."""
    is_zh = (lang == 'zh')
    left, bottom, w, h = rect
    gap = 0.025 * w
    cw = (w - 3 * gap) / 4
    tf = max(9, int(fs * 0.7))
    lf = max(7, int(fs * 0.5))
    af = max(8, int(fs * 0.55))

    # Chart 1: Ecology bars
    ax1 = fig.add_axes([left, bottom, cw, h])
    eco_labels = ['绿化\n覆盖率', '海绵\n控制率', '可再生\n能源', '绿色\n出行', '公共\n空间'] if is_zh \
        else ['Green', 'Sponge', 'Renew', 'Green\nMode', 'Public']
    eco_values = [0.4, 0.85, 0.2, 0.6, 1.0]
    eco_targets = [0.35, 0.80, 0.15, 0.50, 0.95]
    colors_eco = [C['chart_1'], C['chart_2'], C['chart_3'], C['chart_4'], C['chart_5']]
    x = np.arange(5)
    ax1.bar(x, eco_values, 0.55, color=colors_eco, alpha=0.85, edgecolor='white', linewidth=0.8)
    ax1.scatter(x, eco_targets, marker='_', s=200, color='#333333', linewidth=2, zorder=5)
    for i, v in enumerate(eco_values):
        ax1.text(i, v + 0.03, f'{v*100:.0f}%', ha='center', fontsize=af,
                 fontweight='bold', color=colors_eco[i])
    ax1.set_xticks(x); ax1.set_xticklabels(eco_labels, fontsize=lf, color=C['text'])
    ax1.set_ylim(0, 1.2)
    ax1.set_title('生态可持续指标' if is_zh else 'Ecology & Sustainability',
                  fontsize=tf, fontweight='bold', color=C['dark'], pad=4)
    ax1.set_yticks([]); ax1.tick_params(length=0)
    ax1.set_facecolor('white'); ax1.grid(axis='y', linestyle='--', alpha=0.3, color=C['grid'])

    # Chart 2: Land use pie
    ax2 = fig.add_axes([left + cw + gap, bottom, cw, h])
    lu_data = {'AI创新': (320, C['lu_ai_rd']), '绿脉公园': (180, C['lu_green']),
               '生活社区': (280, C['lu_residential']), '智慧服务': (120, C['lu_commercial']),
               '产业融合': (140, C['lu_industry']), '蓝绿腹地': (100, C['lu_water'])}
    labels = list(lu_data.keys()); sizes = [v[0] for v in lu_data.values()]
    colors = [v[1] for v in lu_data.values()]
    wedges, texts, autotexts = ax2.pie(sizes, labels=labels, colors=colors,
                                       autopct='%1.0f%%', startangle=90,
                                       textprops={'fontsize': lf}, pctdistance=0.78,
                                       wedgeprops={'linewidth': 0.5, 'edgecolor': 'white'})
    for at in autotexts:
        at.set_fontsize(lf - 1); at.set_fontweight('bold'); at.set_color('white')
    ax2.set_title('用地面积分布 (ha)' if is_zh else 'Land Use (ha)',
                  fontsize=tf, fontweight='bold', color=C['dark'], pad=4)

    # Chart 3: Phased projects
    ax3 = fig.add_axes([left + 2 * (cw + gap), bottom, cw, h])
    phases = ['近期' if is_zh else 'Near', '中期' if is_zh else 'Mid', '远期' if is_zh else 'Long']
    phase_counts = [4, 5, 4]
    phase_colors = [C['chart_1'], C['chart_2'], C['chart_3']]
    hb = ax3.barh(phases, phase_counts, color=phase_colors, height=0.5,
                   alpha=0.85, edgecolor='white')
    for bar, v in zip(hb, phase_counts):
        ax3.text(bar.get_width() + 0.15, bar.get_y() + bar.get_height() / 2,
                  f'{v}个项目' if is_zh else f'{v}', va='center', fontsize=af,
                  fontweight='bold', color=C['dark'])
    ax3.set_title('分阶段实施' if is_zh else 'Phased Plan',
                  fontsize=tf, fontweight='bold', color=C['dark'], pad=4)
    ax3.set_xlim(0, 7); ax3.set_yticks(range(3)); ax3.set_yticklabels(phases, fontsize=lf)
    ax3.tick_params(length=0)
    ax3.set_facecolor('white'); ax3.grid(axis='x', linestyle='--', alpha=0.3, color=C['grid'])

    # Chart 4: Building renewal
    ax4 = fig.add_axes([left + 3 * (cw + gap), bottom, cw, h])
    renewal_labels = ['保留\n提升', '功能\n置换', '综合\n整治', '拆除\n新建'] if is_zh \
        else ['Preserve', 'Repurpose', 'Renovate', 'New']
    renewal_pcts = [45, 25, 20, 10]
    renewal_colors = ['#81C784', '#42A5F5', '#FFB74D', '#E57373']
    b4 = ax4.bar(renewal_labels, renewal_pcts, 0.55, color=renewal_colors,
                 alpha=0.85, edgecolor='white', linewidth=0.8)
    for bar, v in zip(b4, renewal_pcts):
        ax4.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
                 f'{v}%', ha='center', fontsize=af, fontweight='bold',
                 color=bar.get_facecolor())
    ax4.set_title('建筑更新策略' if is_zh else 'Renewal Strategy',
                  fontsize=tf, fontweight='bold', color=C['dark'], pad=4)
    ax4.set_ylim(0, 55); ax4.set_yticks([]); ax4.tick_params(length=0)
    ax4.set_facecolor('white'); ax4.grid(axis='y', linestyle='--', alpha=0.3, color=C['grid'])


# ════════════════════════════════════════════════════════════════
#  A0 Exhibition Board  — reference-board style, high information density
# ════════════════════════════════════════════════════════════════



def _draw_board(fig, lang, T):
    """Shared dense layout for A0/A3: 16 FIG panels filling the whole page."""
    is_zh = (lang == 'zh')
    # Banner
    axb = fig.add_axes([0.012, 0.945, 0.976, 0.049])
    axb.set_facecolor('#0D1B5C'); _clean_ax(axb)
    axb.text(0.018, 0.62, '绿脉智芯' if is_zh else 'GREEN VEINS · SMART CORE',
             fontsize=T['title'], fontweight='bold', color='white', va='center')
    axb.text(0.255, 0.64, '京张AI创新带 · 蓝绿智慧城市设计方案' if is_zh
             else 'Jing-Zhang AI Innovation Belt · Blue-Green Smart Urban Design',
             fontsize=T['subtitle'], color='#90CAF9', va='center')
    axb.text(0.255, 0.26, '城市设计方案 / URBAN DESIGN PROPOSAL' if is_zh
             else 'URBAN DESIGN PROPOSAL', fontsize=max(9, T['foot']), color='#C5CAE9', va='center')
    axb.text(0.985, 0.64, 'A0' if T['title'] >= 50 else 'A3 BOOKLET',
             fontsize=T['tag'], fontweight='bold', color='#64B5F6', ha='right', va='center')
    axb.text(0.985, 0.26, '海淀区 · 北京  2026.08' if is_zh else 'Haidian · Beijing  2026.08',
             fontsize=max(9, T['foot']), color='#90CAF9', ha='right', va='center')

    Lx, Lw = 0.012, 0.205
    Cx, Cw = 0.229, 0.524
    Rx, Rw = 0.765, 0.223
    gap = 0.012
    pstep = 0.165

    def yL(i):
        return 0.935 - (i + 1) * pstep - i * gap

    h = T['head']
    df = T['diag']; mf = T['mapf']; hf = T['hero']; lf = T['leg']; vf = T['vision']

    # LEFT column
    ax = add_panel(fig, [Lx, yL(0), Lw, pstep], 'FIG.01',
                   '区位背景 LOCATION' if is_zh else 'LOCATION', h)
    draw_location_diagram(ax, lang, fs=df + 1)
    ax = add_panel(fig, [Lx, yL(1), Lw, pstep], 'FIG.02',
                   '项目概况 PROJECT' if is_zh else 'PROJECT FACTS', h)
    facts = ([
        ('位置', '北京市海淀区'), ('设计范围', '11.4 km²'), ('重点片区', '3 / 368 ha'),
        ('总建筑量', '约 1,200 万 m²'), ('蓝绿廊道', '清河-小月河'), ('文保单位', '京张铁路遗址'),
    ] if is_zh else [
        ('Location', 'Haidian, Beijing'), ('Design Area', '11.4 km²'), ('Key Areas', '3 / 368 ha'),
        ('Total GFA', '~12M m²'), ('Blue-Green', 'Qinghe-Xiaoyue'), ('Heritage', 'Jing-Zhang Railway'),
    ])
    yy = 0.92
    for k, v in facts:
        ax.text(0.06, yy, k, fontsize=df + 1, fontweight='bold', color=C['dark'], va='center')
        ax.text(0.06, yy - 0.05, v, fontsize=df, color=C['text'], va='center')
        yy -= 0.135
    ax.text(0.06, 0.05, '数据：OpenStreetMap (ODbL) + 暂定边界' if is_zh else 'Data: OSM (ODbL)',
            fontsize=max(7, df - 4), color=C['muted'], va='center')
    ax = add_panel(fig, [Lx, yL(2), Lw, pstep], 'FIG.03',
                   '设计原则 PRINCIPLES' if is_zh else 'PRINCIPLES', h)
    draw_principles(ax, lang, fs=df)
    ax = add_panel(fig, [Lx, yL(3), Lw, pstep], 'FIG.04',
                   '设计策略 STRATEGY' if is_zh else 'STRATEGY', h)
    draw_strategy_diagram(ax, lang, fs=df)
    ax = add_panel(fig, [Lx, yL(4), Lw, pstep], 'FIG.05',
                   '实施路径 ROADMAP' if is_zh else 'ROADMAP', h)
    draw_roadmap(ax, lang, fs=df)

    # RIGHT column
    ax = add_panel(fig, [Rx, yL(0), Rw, pstep], 'FIG.06',
                   '空间结构 STRUCTURE' if is_zh else 'STRUCTURE', h)
    draw_concept_diagram(ax, lang, fs=df + 1)
    ax = add_panel(fig, [Rx, yL(1), Rw, pstep], 'FIG.07',
                   '现状约束 CONSTRAINTS' if is_zh else 'CONSTRAINTS', h)
    draw_constraints_map(ax, lang, fs=mf)
    panel_legend(ax, [('#8D6E63', '#8D6E63', '文保/铁路遗址' if is_zh else 'Heritage/Rail'),
                      ('#42A5F5', '#42A5F5', '水系蓝线' if is_zh else 'Water'),
                      ('#78909C', '#78909C', '轨道走廊' if is_zh else 'Rail Corridor'),
                      ('#FFB74D', '#FFB74D', '高校用地' if is_zh else 'Univ. Land')], fs=lf)
    ax = add_panel(fig, [Rx, yL(2), Rw, pstep], 'FIG.08',
                   '交通慢行 TRANSPORT' if is_zh else 'TRANSPORT', h)
    draw_transport_map(ax, lang, fs=mf)
    panel_legend(ax, [('#37474F', '#37474F', '快速/主干' if is_zh else 'Arterial'),
                      ('#90A4AE', '#90A4AE', '次干/支路' if is_zh else 'Local'),
                      ('#2E7D32', '#81C784', 'AI慢行道' if is_zh else 'AI Slow Lane'),
                      (C['key_1'], C['key_1'], '重点节点' if is_zh else 'Nodes')], fs=lf)
    ax = add_panel(fig, [Rx, yL(3), Rw, pstep], 'FIG.09',
                   '分期实施 PHASING' if is_zh else 'PHASING', h)
    draw_phasing_map(ax, lang, fs=mf)
    panel_legend(ax, [('#2E7D32', '#2E7D32', '近期' if is_zh else 'Near'),
                      ('#1565C0', '#1565C0', '中期' if is_zh else 'Mid'),
                      ('#F57C00', '#F57C00', '远期' if is_zh else 'Long')], fs=lf)
    ax = add_panel(fig, [Rx, yL(4), Rw, pstep], 'FIG.10',
                   '核心指标 METRICS' if is_zh else 'METRICS', h)
    draw_metrics_radar(ax, lang, fs=mf + 2)

    # CENTER column
    ax = add_panel(fig, [Cx, 0.515, Cw, 0.42], 'FIG.11',
                   '场地总览 SITE OVERVIEW' if is_zh else 'SITE OVERVIEW', h)
    map_site(ax, lang, fs=hf, lw=4.0)
    panel_legend(ax, [(C['site_fill'], C['site_edge'], '设计范围' if is_zh else 'Scope'),
                      (C['key_1'], C['key_1'], '重点片区' if is_zh else 'Key Areas'),
                      (C['green_fill'], C['green_edge'], '绿脉公园' if is_zh else 'Green'),
                      (C['water'], C['water_edge'], '水域' if is_zh else 'Water'),
                      (C['road'], C['road'], '道路' if is_zh else 'Roads')], fs=lf)
    cw2 = Cw * 0.5 - gap / 2
    ax = add_panel(fig, [Cx, 0.278, cw2, 0.225], 'FIG.12',
                   '区域区位 REGIONAL' if is_zh else 'REGIONAL', h)
    draw_regional_context(ax, lang, fs=mf + 1)
    ax = add_panel(fig, [Cx + cw2 + gap, 0.278, cw2, 0.225], 'FIG.13',
                   '廊道断面 SECTION' if is_zh else 'SECTION', h)
    draw_section_profile(ax, lang, fs=mf + 1)
    ax = add_panel(fig, [Cx, 0.050, cw2, 0.212], 'FIG.14',
                   '用地结构 LAND USE' if is_zh else 'LAND USE', h)
    map_landuse(ax, lang, fs=mf, lw=2.4)
    panel_legend(ax, [(C['lu_ai_rd'], C['lu_ai_rd'], 'AI核心' if is_zh else 'AI Core'),
                      (C['lu_residential'], C['lu_residential'], '生活' if is_zh else 'Living'),
                      (C['lu_commercial'], C['lu_commercial'], '服务' if is_zh else 'Service'),
                      (C['lu_green'], C['lu_green'], '公园' if is_zh else 'Green'),
                      (C['lu_water'], C['lu_water'], '蓝绿' if is_zh else 'Blue-Green')], fs=lf)
    ax = add_panel(fig, [Cx + cw2 + gap, 0.050, cw2, 0.212], 'FIG.15',
                   '重点区域 KEY AREAS' if is_zh else 'KEY AREAS', h)
    map_keyareas(ax, lang, fs=mf, lw=2.4)
    panel_legend(ax, [(C['key_1'], C['key_1'], '众智园' if is_zh else 'Zhongzhi'),
                      (C['key_2'], C['key_2'], 'AI原点' if is_zh else 'AI Origin'),
                      (C['key_3'], C['key_3'], '大钟寺' if is_zh else 'Dazhongsi')], fs=lf)

    # Vision strip
    draw_vision_strip(fig, [0.012, 0.008, 0.976, 0.036], lang, fs=vf)

    fig.text(0.5, 0.0035,
             'WorkBuddy (wlaura-wlj) | jingzhang-green-smart-ai-belt | 2026.08 | '
             '数据：OpenStreetMap (ODbL) + 暂定设计边界' if is_zh else
             'WorkBuddy (wlaura-wlj) | jingzhang-green-smart-ai-belt | 2026.08 | Data: OSM (ODbL)',
             fontsize=T['foot'], color=C['muted'], ha='center')


def build_a0(lang='zh'):
    is_zh = (lang == 'zh')
    suffix = '' if is_zh else '.en'
    fig = plt.figure(figsize=(47, 33), dpi=100, facecolor='white')
    _draw_board(fig, lang, dict(title=60, subtitle=22, tag=22, head=17, body=15,
                                cap=13, foot=12, diag=13, mapf=14, hero=18, leg=10, vision=11))
    out = DRAW_DIR / f'a0-boards{suffix}.pdf'
    fig.savefig(f'/tmp/a0_preview_{lang}.png', dpi=38, facecolor='white', edgecolor='none')
    fig.savefig(out, dpi=100, facecolor='white', edgecolor='none', format='pdf', bbox_inches='tight')
    preview = DRAW_DIR / f'a0-boards{suffix}.preview.png'
    fig.savefig(preview, dpi=72, facecolor='white', edgecolor='none', bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved: {out} ({os.path.getsize(out):,} bytes)")
    return out


def build_a3(lang='zh'):
    is_zh = (lang == 'zh')
    suffix = '' if is_zh else '.en'
    fig = plt.figure(figsize=(33, 23), dpi=100, facecolor='white')
    _draw_board(fig, lang, dict(title=40, subtitle=15, tag=15, head=13, body=11,
                                cap=10, foot=9, diag=10, mapf=10, hero=14, leg=8, vision=9))
    out = DRAW_DIR / f'a3-booklet{suffix}.pdf'
    fig.savefig(f'/tmp/a3_preview_{lang}.png', dpi=38, facecolor='white', edgecolor='none')
    fig.savefig(out, dpi=100, facecolor='white', edgecolor='none', format='pdf', bbox_inches='tight')
    preview = DRAW_DIR / f'a3-booklet{suffix}.preview.png'
    fig.savefig(preview, dpi=72, facecolor='white', edgecolor='none', bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved: {out} ({os.path.getsize(out):,} bytes)")
    return out


if __name__ == '__main__':
    print("=" * 60)
    print("Regenerating all figures & PDFs (vector PDF, CJK font)")
    print(f"Font: {font_name}")
    print("=" * 60)

    # Figures (for index.html + standalone review)
    print("\n[Figures - Chinese]")
    for fn in [fig_site_overview, fig_land_use, fig_key_areas,
               fig_mobility_bluegreen, fig_metrics_evidence]:
        fn('zh')
    print("\n[Figures - English]")
    for fn in [fig_site_overview, fig_land_use, fig_key_areas,
               fig_mobility_bluegreen, fig_metrics_evidence]:
        fn('en')

    # PDFs (drawn directly as vector graphics — no image embedding)
    print("\n[PDFs - A0 Boards]")
    build_a0('zh'); build_a0('en')
    print("\n[PDFs - A3 Booklet]")
    build_a3('zh'); build_a3('en')

    # Verify
    print("\n[Verification]")
    for fp in sorted(FIG_DIR.glob('*.png')):
        print(f"  {fp.name}: {fp.stat().st_size:,} bytes")
    for fp in sorted(DRAW_DIR.glob('*.pdf')):
        print(f"  {fp.name}: {fp.stat().st_size:,} bytes")

    print("\nDone! All assets regenerated.")
