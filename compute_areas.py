#!/usr/bin/env python3
"""Compute projected areas for geometry features."""
import json
from pathlib import Path
from pyproj import Transformer
from shapely.geometry import shape, Polygon

transformer = Transformer.from_crs("EPSG:4326", "EPSG:4548", always_xy=True)

PKG = Path("submissions/FionaXia008/open-jing-zhang/geometry")

def projected_area(geom):
    """Project polygon to EPSG:4548 and compute area."""
    coords = list(geom.exterior.coords)
    xs, ys = transformer.transform([c[0] for c in coords], [c[1] for c in coords])
    return Polygon(zip(xs, ys)).area

# Land use
with open(PKG / "land_use.geojson", encoding="utf-8") as f:
    lu = json.load(f)

print("=== Land Use ===")
for feat in lu["features"]:
    geom = shape(feat["geometry"])
    area = projected_area(geom)
    declared = feat["properties"]["area_sqm_declared"]
    delta = abs(area - declared)
    tol = max(1.0, area * 0.01)
    status = "OK" if delta <= tol else "MISMATCH"
    print(f'{feat["id"]}: declared={declared}, calculated={area:.3f}, delta={delta:.3f}, tol={tol:.3f} [{status}]')

# Site boundary
with open(PKG / "site_boundary.geojson") as f:
    sb = json.load(f)

print("\n=== Site Boundary ===")
for feat in sb["features"]:
    geom = shape(feat["geometry"])
    area = projected_area(geom)
    declared = feat["properties"]["area_sqm_declared"]
    print(f'{feat["id"]}: declared={declared}, calculated={area:.3f}')

site_geom = shape(sb["features"][0]["geometry"])
site_area = projected_area(site_geom)

# Green space
with open(PKG / "green_space.geojson") as f:
    gs = json.load(f)

print("\n=== Green Space ===")
green_features = []
for feat in gs["features"]:
    geom = shape(feat["geometry"])
    area = projected_area(geom)
    print(f'{feat["id"]}: area={area:.3f}')
    green_features.append(geom)

# Land use coverage
from shapely.ops import unary_union
lu_geom = unary_union([shape(f["geometry"]) for f in lu["features"]])
lu_area = projected_area(lu_geom)
gap = site_area - lu_area
print(f'\n=== Coverage ===')
print(f'Site area: {site_area:.3f}')
print(f'Land use union area: {lu_area:.3f}')
print(f'Gap: {gap:.3f}')

# Green space outside site
gs002 = shape(gs["features"][1]["geometry"])
outside = gs002.difference(site_geom)
outside_area = projected_area(outside)
print(f'\nGS-002 outside site: {outside_area:.3f}')
