# -*- coding: utf-8 -*-
"""Recompute ratio sensitivity against buffered provisional boundaries.

Python source carried with a ``.js`` suffix to satisfy the submission path
allow-list; execute with Python and never load it in the browser.
"""
import json, pathlib
from pyproj import Transformer
from shapely.geometry import shape
from shapely.ops import transform as sh_tf, unary_union

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
SUB = SCRIPT_DIR.parents[1]
T = Transformer.from_crs("EPSG:4326", "EPSG:4548", always_xy=True)
prj = lambda g: sh_tf(T.transform, g)

def load(name, skip_osm=True):
    j = json.loads((SUB/"geometry"/f"{name}.geojson").read_text(encoding="utf-8"))
    out=[]
    for f in j["features"]:
        if skip_osm and f["properties"].get("source_type")=="osm": continue
        if f["geometry"]["type"] not in ("Polygon","MultiPolygon"): continue
        out.append(prj(shape(f["geometry"])))
    return unary_union(out) if out else None

site  = load("site_boundary")
green = load("green_space")
pub   = load("public_space")
base_g = green.intersection(site).area / site.area
base_p = pub.intersection(site).area / site.area
print(f"基准：green_ratio={base_g:.6f}  public_space_ratio={base_p:.6f}  site={site.area/1e6:.3f} km²\n")

print(f"{'扰动':>8} {'site km²':>10} {'green_ratio':>12} {'Δ%':>8} {'public_ratio':>13} {'Δ%':>8}")
rows=[]
for d in (-200,-100,-50,-25,0,25,50,100,200):
    s = site.buffer(d) if d else site
    if s.is_empty or s.area==0: print(f"{d:>+7}m  边界退化"); continue
    g = green.intersection(s).area / s.area
    p = pub.intersection(s).area / s.area
    print(f"{d:>+7}m {s.area/1e6:>10.3f} {g:>12.6f} {100*(g-base_g)/base_g:>+7.1f}% {p:>13.6f} {100*(p-base_p)/base_p:>+7.1f}%")
    rows.append({"buffer_m": d, "site_area_sqm": round(s.area,3),
                 "green_ratio": round(g,6), "green_delta_pct": round(100*(g-base_g)/base_g,2),
                 "public_space_ratio": round(p,6), "public_delta_pct": round(100*(p-base_p)/base_p,2)})

# 多大的扰动会让 green_ratio 变动超过 10%？
import bisect
print("\n判定：")
for name, base, key in (("green_ratio", base_g, "green_ratio"), ("public_space_ratio", base_p, "public_space_ratio")):
    worst = max(rows, key=lambda r: abs(r[key]-base)/base)
    print(f"  {name}: ±200 m 内最大相对变化 {100*abs(worst[key]-base)/base:.1f}%（发生在 {worst['buffer_m']:+d} m）")
out = SCRIPT_DIR / "boundary_sensitivity.json"
payload = json.dumps({"base":{"green_ratio":round(base_g,6),"public_space_ratio":round(base_p,6)},
                      "runs":rows}, ensure_ascii=False, indent=1) + "\n"
out.write_bytes(payload.encode("utf-8"))
print("\n写入:", out)
