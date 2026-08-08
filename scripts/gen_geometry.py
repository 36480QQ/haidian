#!/usr/bin/env python3
"""
京张智脉 Jingzhang AI Vein — 空间数据生成脚本
基于 provisional 边界生成拓扑安全的 land_use 分区 + 全部设计图层
原则：
- land_use 通过 site_boundary 与横向/纵向带求交集生成（天然全覆盖、无重叠、共享边）
- EPSG:4326 存储，EPSG:4548 投影复算面积
- 全部 feature 带 id/layer/source_type/confidence/geometry_role
"""
import json, math, sys
from shapely.geometry import shape, mapping, Polygon, LineString, Point, box
from shapely.ops import unary_union
from pyproj import Transformer

SUB = "submissions/xusu-ai/jingzhang-ai-vein"
GEOM = f"{SUB}/geometry"

# ---------- 投影 ----------
to_4548 = Transformer.from_crs("EPSG:4326", "EPSG:4548", always_xy=True)

def area_sqm(poly_geom):
    """投影到 EPSG:4548 计算面积"""
    coords = list(poly_geom.exterior.coords)
    projected = [to_4548.transform(x, y) for x, y in coords]
    return abs(Polygon(projected).area)

def simplify_ring(coords, keep=1.0):
    """保留坐标精度"""
    return coords

# ---------- 加载场地 ----------
site_fc = json.load(open(f"{GEOM}/site_boundary.geojson"))
site = shape(site_fc["features"][0]["geometry"])
minx, miny, maxx, maxy = site.bounds
print(f"场地范围: lon[{minx:.5f},{maxx:.5f}] lat[{miny:.5f},{maxy:.5f}]")
print(f"场地面积(4548): {area_sqm(site)/1e6:.2f} km²")

# ---------- 设计分区 ----------
# 京张遗址公园带（纵贯南北的活力主轴）：取场地东侧约 1/3 靠西？实际京张铁路遗址在场地西侧
# 概念布局（自西向东）：
#   [西翼: 中关村科技服务翼/存量更新] [京张遗址公园带] [东翼: 小月河场景赋能翼/新建]
# 自北向南：
#   [北段: 众智园AI加速区] [中段: AI原点社区] [南段: 大钟寺AI集聚区]

# 京张遗址公园带：位于场地中部偏西，宽度约场地宽度的 22%
park_width_frac = 0.22
# 公园带西边界
park_west_x = minx + (maxx - minx) * 0.36
park_east_x = park_west_x + (maxx - minx) * park_width_frac

# 横向分区带（按纬度切分，与三区对应）
# 北段: 众智园区 lat >= 39.995
# 中段: AI原点社区 39.960 <= lat < 39.995
# 南段: 大钟寺区 lat < 39.960

def clip_band(lat_lo, lat_hi):
    """场地与横向带的交集"""
    band = site.intersection(box(minx, lat_lo, maxx, lat_hi))
    if band.is_empty:
        return None
    if band.geom_type == "MultiPolygon":
        return max(band.geoms, key=lambda g: g.area)
    return band

def clip_cell(lat_lo, lat_hi, lon_lo, lon_hi):
    """场地与矩形单元的交集"""
    cell = site.intersection(box(lon_lo, lat_lo, lon_hi, lat_hi))
    if cell.is_empty:
        return None
    if cell.geom_type == "MultiPolygon":
        return max(cell.geoms, key=lambda g: g.area)
    return cell

# 三段
north_lo, north_hi = 39.995, maxy      # 众智园
mid_lo, mid_hi = 39.960, 39.995        # AI原点社区
south_lo, south_hi = miny, 39.960      # 大钟寺

# 东西三带
west_lo, west_hi = minx, park_west_x          # 西翼（中关村科技服务翼）
park_lo, park_hi = park_west_x, park_east_x   # 京张遗址公园带
east_lo, east_hi = park_east_x, maxx          # 东翼（小月河场景赋能翼）

cells = {}
# 北段
cells["N-W"] = clip_cell(north_lo, north_hi, west_lo, west_hi)
cells["N-P"] = clip_cell(north_lo, north_hi, park_lo, park_hi)
cells["N-E"] = clip_cell(north_lo, north_hi, east_lo, east_hi)
# 中段
cells["M-W"] = clip_cell(mid_lo, mid_hi, west_lo, west_hi)
cells["M-P"] = clip_cell(mid_lo, mid_hi, park_lo, park_hi)
cells["M-E"] = clip_cell(mid_lo, mid_hi, east_lo, east_hi)
# 南段
cells["S-W"] = clip_cell(south_lo, south_hi, west_lo, west_hi)
cells["S-P"] = clip_cell(south_lo, south_hi, park_lo, park_hi)
cells["S-E"] = clip_cell(south_lo, south_hi, east_lo, east_hi)

# 用地分配（MNR 分类码）
LAND_USE_PLAN = {
    # 众智园：AI研发主导 + 教育 + 公园绿地
    "N-W": ("0802", "科研用地（AI自主创新加速）"),
    "N-P": ("1401", "公园绿地（京张遗址公园北段）"),
    "N-E": ("0803", "文化用地（AI展示与体验）"),
    # AI原点社区：科研 + 居住 + 商业 + 公园
    "M-W": ("0701", "城镇住宅用地（人才社区更新）"),
    "M-P": ("1401", "公园绿地（京张遗址公园中段）"),
    "M-E": ("05", "商业服务业用地（原点社区配套）"),
    # 大钟寺：商业 + 科研 + 公园
    "S-W": ("05", "商业服务业用地（大钟寺智能消费）"),
    "S-P": ("1401", "公园绿地（京张遗址公园南段）"),
    "S-E": ("0802", "科研用地（AI产业集聚）"),
}

# 再细分：公园带内部要拆出道路用地和广场；东西翼也需道路
# 简化处理：主要用地 = 上述 9 格；道路另建图层；绿地另建图层；公共空间另建图层
# 为保证 land_use 全覆盖，我们在 9 格基础上叠加入口广场（从相邻商业/文化格切割）

# 生成 land_use features
land_use_features = []
lu_id = 0
for key, (code, label) in LAND_USE_PLAN.items():
    poly = cells[key]
    if poly is None or poly.is_empty:
        print(f"  ⚠️ {key} 为空，跳过")
        continue
    lu_id += 1
    a = area_sqm(poly)
    land_use_features.append({
        "type": "Feature",
        "id": f"LU-{lu_id:03d}",
        "properties": {
            "id": f"LU-{lu_id:03d}",
            "layer": "LAND_USE",
            "land_use_code": code,
            "label_zh": label,
            "source_type": "agent_design_proposal",
            "confidence": "medium",
            "geometry_role": "design_proposal",
            "official_boundary": False,
            "area_sqm_declared": round(a, 1),
            "design_note": "基于 provisional 边界的概念性分区建议",
        },
        "geometry": mapping(poly),
    })
    print(f"  {key}: {label} {a/1e4:.1f}ha")

# 输出 land_use
lu_fc = {"type": "FeatureCollection", "features": land_use_features}
with open(f"{GEOM}/land_use.geojson", "w") as f:
    json.dump(lu_fc, f, ensure_ascii=False)
print(f"\n✅ land_use.geojson: {len(land_use_features)} features")

# ---------- 校验拓扑 ----------
lu_polys = [shape(fe["geometry"]) for fe in land_use_features]
union = unary_union(lu_polys)
gap = site.difference(union)
overlap_area = sum(p.area for p in lu_polys) - union.area
print(f"覆盖检查: 场地 {area_sqm(site)/1e6:.4f} km² | 联合 {area_sqm(union)/1e6:.4f} km² | 缝隙 {gap.area:.2e} | 重叠 {overlap_area:.2e}")
