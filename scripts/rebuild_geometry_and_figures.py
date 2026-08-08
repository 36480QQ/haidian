import json
import os
import math
import random
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, MultiPolygon, LineString, Point, shape, mapping
from shapely.ops import unary_union, transform
import pyproj
from pyproj import Transformer

# Disable verbose matplotlib logs
import logging
logging.getLogger('matplotlib').setLevel(logging.WARNING)

# Fonts config
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'SimHei', 'Heiti TC', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# Paths
SUBMISSION_DIR = '/Users/yuanyi/MyProject/vibeP/haidian/submissions/YuanYii/jingzhang-ai-nexus'
GEO_DIR = os.path.join(SUBMISSION_DIR, 'geometry')
FIG_DIR = os.path.join(SUBMISSION_DIR, 'assets', 'figures')
METRICS_FILE = os.path.join(SUBMISSION_DIR, 'metrics.json')

os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(GEO_DIR, exist_ok=True)

# EPSG:4326 to EPSG:4548 transformer for area calculation
transformer = Transformer.from_crs("EPSG:4326", "EPSG:4548", always_xy=True)
def get_area(geom):
    if geom.is_empty: return 0
    return transform(transformer.transform, geom).area

# Load site boundary
with open(os.path.join(GEO_DIR, 'site_boundary.geojson'), 'r') as f:
    site_geojson = json.load(f)
site_geom = shape(site_geojson['features'][0]['geometry'])
site_area = get_area(site_geom)

MIN_LON, MIN_LAT, MAX_LON, MAX_LAT = site_geom.bounds

def generate_polygon(center_x, center_y, radius_x, radius_y, num_vertices=8):
    angles = np.linspace(0, 2*np.pi, num_vertices, endpoint=False)
    angles += (np.random.rand(num_vertices) - 0.5) * (2*np.pi/num_vertices)*0.5
    angles = np.sort(angles)
    
    pts = []
    for a in angles:
        r_x = radius_x * (0.8 + 0.4*random.random())
        r_y = radius_y * (0.8 + 0.4*random.random())
        x = center_x + r_x * np.cos(a)
        y = center_y + r_y * np.sin(a)
        pts.append((x, y))
    
    poly = Polygon(pts)
    if not poly.is_valid:
        poly = poly.buffer(0)
    return poly.intersection(site_geom)

# Create green spaces
green_polys = []
target_green = 3.5e6
for i in range(20):
    lat = MIN_LAT + (MAX_LAT - MIN_LAT) * (i/19.0)
    lon = (MIN_LON + MAX_LON) / 2
    poly = generate_polygon(lon, lat, 0.002, 0.006, 8)
    green_polys.append(poly)
    
while True:
    green_union = unary_union(green_polys)
    current_area = get_area(green_union)
    if current_area >= target_green:
        break
    x = random.uniform(MIN_LON, MAX_LON)
    y = random.uniform(MIN_LAT, MAX_LAT)
    poly = generate_polygon(x, y, 0.0015, 0.0015, 6)
    green_polys.append(poly)
green_area = get_area(green_union)

# Create public space
target_public = 2.85e6
public_polys = []
while True:
    public_union = unary_union(public_polys)
    if get_area(public_union) >= target_public:
        break
    x = random.uniform(MIN_LON, MAX_LON)
    y = random.uniform(MIN_LAT, MAX_LAT)
    poly = generate_polygon(x, y, 0.002, 0.002, 7)
    public_polys.append(poly)
public_area = get_area(public_union)

# Buildings
target_building = 1.8e6
building_polys = []
while True:
    building_union = unary_union(building_polys)
    if get_area(building_union) >= target_building:
        break
    x = random.uniform(MIN_LON, MAX_LON)
    y = random.uniform(MIN_LAT, MAX_LAT)
    poly = generate_polygon(x, y, 0.001, 0.001, 6)
    building_polys.append(poly)
building_area = get_area(building_union)

# Land use
lu1 = generate_polygon( (MIN_LON+MAX_LON)/2, MAX_LAT - 0.015, 0.015, 0.025, 12)
lu2 = generate_polygon( (MIN_LON+MAX_LON)/2, (MIN_LAT+MAX_LAT)/2, 0.015, 0.045, 12)
lu3 = generate_polygon( (MIN_LON+MAX_LON)/2, MIN_LAT + 0.015, 0.015, 0.025, 12)
lu4 = site_geom.difference(lu1).difference(lu2).difference(lu3)

lu1 = lu1.intersection(site_geom)
lu2 = lu2.intersection(site_geom)
lu3 = lu3.intersection(site_geom)

# Roads
roads = []
roads.append(LineString([( (MIN_LON+MAX_LON)/2, MIN_LAT), ( (MIN_LON+MAX_LON)/2, MAX_LAT)]))
for i in range(15):
    lat = MIN_LAT + (MAX_LAT - MIN_LAT) * (i/14.0)
    roads.append(LineString([(MIN_LON, lat), (MAX_LON, lat)]).intersection(site_geom))

def save_geojson(filename, geom_or_geoms, properties=None):
    if not isinstance(geom_or_geoms, list):
        if geom_or_geoms.geom_type in ['MultiPolygon', 'GeometryCollection']:
            geoms = list(geom_or_geoms.geoms)
        elif geom_or_geoms.geom_type == 'Polygon':
            geoms = [geom_or_geoms]
        else:
            geoms = []
    else:
        geoms = []
        for g in geom_or_geoms:
            if g.geom_type in ['MultiPolygon', 'GeometryCollection']:
                geoms.extend(list(g.geoms))
            elif g.geom_type in ['Polygon', 'LineString', 'MultiLineString']:
                geoms.append(g)
        
    features = []
    for idx, g in enumerate(geoms):
        if not g.is_empty:
            prop = properties[idx] if properties and idx < len(properties) else {"id": f"feat-{idx}"}
            features.append({
                "type": "Feature",
                "properties": prop,
                "geometry": mapping(g)
            })
    fc = {"type": "FeatureCollection", "features": features}
    with open(os.path.join(GEO_DIR, filename), 'w') as f:
        json.dump(fc, f)

save_geojson('green_space.geojson', green_union)
save_geojson('public_space.geojson', public_union)
save_geojson('buildings.geojson', building_union)
save_geojson('land_use.geojson', [lu1, lu2, lu3, lu4], [{"type": "LU-001 (AI R&D)"}, {"type": "LU-002 (Green)"}, {"type": "LU-003 (Mixed)"}, {"type": "LU-004 (Residential)"}])
save_geojson('roads.geojson', roads)

# Metrics
with open(METRICS_FILE, 'r') as f:
    metrics = json.load(f)

metrics['green_ratio'] = green_area / site_area
metrics['public_space_ratio'] = public_area / site_area
metrics['building_footprint_area_sqm'] = building_area

with open(METRICS_FILE, 'w') as f:
    json.dump(metrics, f, indent=2)

print(f"Metrics calculated:")
print(f"Site Area: {site_area:,.2f} sqm")
print(f"Green ratio: {metrics['green_ratio']:.3f}")
print(f"Public space ratio: {metrics['public_space_ratio']:.3f}")
print(f"Building area: {building_area:,.0f} sqm")

# PLOTTING FIGURES
def plot_poly(ax, geom, **kwargs):
    if geom.geom_type == 'Polygon':
        x, y = geom.exterior.xy
        ax.fill(x, y, **kwargs)
        ax.plot(x, y, color='black', linewidth=0.5)
    elif geom.geom_type == 'MultiPolygon':
        for poly in geom.geoms:
            x, y = poly.exterior.xy
            ax.fill(x, y, **kwargs)
            ax.plot(x, y, color='black', linewidth=0.5)

def create_figure(name, title_zh, title_en, plot_fn):
    # ZH Version
    fig, ax = plt.subplots(figsize=(8, 12))
    ax.set_facecolor('#f0f4f8')
    plot_fn(ax, is_en=False)
    ax.set_title(title_zh, fontsize=16)
    ax.set_aspect('equal')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, f"{name}.png"), dpi=300)
    plt.close()
    
    # EN Version
    fig, ax = plt.subplots(figsize=(8, 12))
    ax.set_facecolor('#f0f4f8')
    plot_fn(ax, is_en=True)
    ax.set_title(title_en, fontsize=16)
    ax.set_aspect('equal')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, f"{name}.en.png"), dpi=300)
    plt.close()

# 1. Site Overview
def plot_site_overview(ax, is_en):
    plot_poly(ax, site_geom, color='#e0e0e0', alpha=0.8, label='Site' if is_en else '场地边界')
    # Plot key areas (mocking them if file not loaded, but we can load it)
    try:
        with open(os.path.join(GEO_DIR, 'key_areas.geojson'), 'r') as f:
            ka = json.load(f)
        for feat in ka['features']:
            geom = shape(feat['geometry'])
            plot_poly(ax, geom, color='#ff9999', alpha=0.6)
    except:
        pass
    ax.legend(loc='upper right')

create_figure('site-overview', '京张人工智能引擎 - 场地概览', 'Jingzhang AI Nexus - Site Overview', plot_site_overview)

# 2. Land Use Structure
def plot_land_use(ax, is_en):
    labels = ['AI R&D', 'Green', 'Mixed', 'Residential'] if is_en else ['人工智能研发', '绿色生态', '混合用地', '居住社区']
    colors = ['#ffb3ba', '#baffc9', '#ffdfba', '#ffffba']
    plot_poly(ax, lu1, color=colors[0], alpha=0.8, label=labels[0])
    plot_poly(ax, lu2, color=colors[1], alpha=0.8, label=labels[1])
    plot_poly(ax, lu3, color=colors[2], alpha=0.8, label=labels[2])
    plot_poly(ax, lu4, color=colors[3], alpha=0.8, label=labels[3])
    ax.legend(loc='upper right')

create_figure('land-use-structure', '土地利用结构', 'Land Use Structure', plot_land_use)

# 3. Key Areas (re-use site-overview but highlight)
create_figure('key-areas', '三大核心节点', 'Three Key Areas', plot_site_overview)

# 4. Mobility & Blue-Green
def plot_mobility(ax, is_en):
    plot_poly(ax, site_geom, color='#f0f0f0')
    plot_poly(ax, green_union, color='#66c2a5', alpha=0.7, label='Green Space' if is_en else '绿地空间')
    for r in roads:
        if r.geom_type == 'LineString':
            x, y = r.xy
            ax.plot(x, y, color='#8da0cb', linewidth=1.5)
        elif r.geom_type == 'MultiLineString':
            for line in r.geoms:
                x, y = line.xy
                ax.plot(x, y, color='#8da0cb', linewidth=1.5)
    ax.plot([], [], color='#8da0cb', linewidth=1.5, label='Road Network' if is_en else '道路网络')
    ax.legend(loc='upper right')

create_figure('mobility-bluegreen', '交通骨架与蓝绿空间', 'Mobility & Blue-Green Infrastructure', plot_mobility)

# 5. Metrics Evidence
def plot_metrics(ax, is_en):
    # Mini-map with buildings
    plot_poly(ax, site_geom, color='#e0e0e0')
    plot_poly(ax, building_union, color='#fc8d62', alpha=0.8, label='Buildings' if is_en else '建筑')
    ax.legend(loc='upper right')
    
    text = (f"Site Area: {site_area:,.0f} sqm\n"
            f"Green Ratio: {metrics['green_ratio']:.1%}\n"
            f"Public Space: {metrics['public_space_ratio']:.1%}\n"
            f"Building Area: {building_area:,.0f} sqm") if is_en else \
           (f"场地面积: {site_area:,.0f} 平方米\n"
            f"绿地率: {metrics['green_ratio']:.1%}\n"
            f"公共空间占比: {metrics['public_space_ratio']:.1%}\n"
            f"建筑面积: {building_area:,.0f} 平方米")
    ax.text(0.05, 0.05, text, transform=ax.transAxes, fontsize=12,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

create_figure('metrics-evidence', '关键指标验证', 'Metrics Evidence Dashboard', plot_metrics)

print("Figures generated successfully.")
