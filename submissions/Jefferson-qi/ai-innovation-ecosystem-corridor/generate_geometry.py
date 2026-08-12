#!/usr/bin/env python3
"""Generate all GeoJSON files for the AI Innovation Ecosystem Corridor submission."""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# Provisional boundary coordinates from the official repo
SITE_BOUNDARY_COORDS = [
    [116.3407, 39.939], [116.3553, 39.939], [116.3553, 39.965],
    [116.3533, 39.99], [116.3553, 40.0265], [116.3427, 40.0265],
    [116.3417, 40.006], [116.3397, 39.975], [116.3407, 39.939]
]

RESEARCH_AREA_COORDS = [
    [116.31885, 39.938], [116.36615, 39.938], [116.37215, 39.965],
    [116.37215, 40.027], [116.33285, 40.027], [116.32085, 40.0],
    [116.31285, 39.965], [116.31885, 39.938]
]

# Key area polygons
KEY_AREA_1_COORDS = [  # 众智园
    [116.343, 40.0075], [116.354, 40.0075], [116.354, 40.026],
    [116.343, 40.026], [116.343, 40.0075]
]
KEY_AREA_2_COORDS = [  # AI原点社区
    [116.342, 39.9835], [116.353, 39.9835], [116.353, 39.9935],
    [116.342, 39.9935], [116.342, 39.9835]
]
KEY_AREA_3_COORDS = [  # 大钟寺
    [116.342, 39.944], [116.355, 39.944], [116.355, 39.94984],
    [116.342, 39.94984], [116.342, 39.944]
]

def make_feature(fid, layer, geom_type, coords, props=None):
    """Create a GeoJSON feature with standard properties."""
    base_props = {
        "id": fid,
        "layer": layer,
        "source_type": "agent_inferred_from_public_data",
        "confidence": "medium",
        "geometry_role": "provisional_constraint" if layer in ("SITE_BOUNDARY", "KEY_AREA") else "design_concept"
    }
    if props:
        base_props.update(props)
    geometry = {"type": geom_type, "coordinates": coords}
    return {"type": "Feature", "id": fid, "properties": base_props, "geometry": geometry}

def write_geojson(filename, features, name=""):
    fc = {"type": "FeatureCollection", "name": name, "features": features}
    path = os.path.join(BASE, "geometry", filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(fc, f, ensure_ascii=False, indent=2)
    print(f"  Written: {filename} ({len(features)} features)")

# 1. site_boundary.geojson
site_features = [
    make_feature("PROV-SITE-001", "SITE_BOUNDARY", "Polygon", [SITE_BOUNDARY_COORDS], {
        "scope_id": "overall_design_area",
        "name_zh": "总体设计范围临时粗略边界",
        "official_boundary": False,
        "boundary_precision": "provisional_rough",
        "announced_area_sqm": 11400000,
        "usage_note": "临时粗略边界，仅用于AI生成和展示，不得作为官方红线"
    }),
    make_feature("PROV-RESEARCH-001", "SITE_BOUNDARY", "Polygon", [RESEARCH_AREA_COORDS], {
        "scope_id": "coordinated_research_area",
        "name_zh": "统筹研究范围临时粗略边界",
        "official_boundary": False,
        "boundary_precision": "provisional_rough",
        "announced_area_sqm": 43600000,
        "usage_note": "临时粗略边界，仅用于统筹研究参考"
    })
]
write_geojson("site_boundary.geojson", site_features, "site_boundary")

# 2. key_areas.geojson
key_features = [
    make_feature("PROV-KEY-001", "KEY_AREA", "Polygon", [KEY_AREA_1_COORDS], {
        "area_id": "zhongzhiyuan_ai_acceleration_area",
        "name_zh": "众智园AI自主创新加速区",
        "official_boundary": False,
        "announced_area_sqm": 1921000
    }),
    make_feature("PROV-KEY-002", "KEY_AREA", "Polygon", [KEY_AREA_2_COORDS], {
        "area_id": "beijing_ai_origin_community",
        "name_zh": "北京AI原点社区",
        "official_boundary": False,
        "announced_area_sqm": 1043000
    }),
    make_feature("PROV-KEY-003", "KEY_AREA", "Polygon", [KEY_AREA_3_COORDS], {
        "area_id": "dazhongsi_ai_industry_cluster",
        "name_zh": "大钟寺AI产业聚集区",
        "official_boundary": False,
        "announced_area_sqm": 720000
    })
]
write_geojson("key_areas.geojson", key_features, "key_areas")

# 3. land_use.geojson - partition the site boundary into land use zones
# Create a north-south corridor with different zones
land_uses = [
    # Northern section - 众智园 area: AI R&D and incubation
    ("LU-001", "AI研发与孵化", "ai_r_and_d", [
        [116.343, 40.0075], [116.349, 40.0075], [116.349, 40.026],
        [116.343, 40.026], [116.343, 40.0075]
    ]),
    ("LU-002", "实验室与加速器", "lab", [
        [116.349, 40.0075], [116.354, 40.0075], [116.354, 40.026],
        [116.349, 40.026], [116.349, 40.0075]
    ]),
    # Central section - AI原点社区: mixed use, residential, community
    ("LU-003", "AI混合功能核心", "mixed_use", [
        [116.342, 39.9835], [116.348, 39.9835], [116.348, 39.9935],
        [116.342, 39.9935], [116.342, 39.9835]
    ]),
    ("LU-004", "人才公寓与社区", "talent_apartment", [
        [116.348, 39.9835], [116.353, 39.9835], [116.353, 39.9935],
        [116.348, 39.9935], [116.348, 39.9835]
    ]),
    # Southern section - 大钟寺: industry and commercial
    ("LU-005", "AI产业办公", "office", [
        [116.342, 39.944], [116.349, 39.944], [116.349, 39.94984],
        [116.342, 39.94984], [116.342, 39.944]
    ]),
    ("LU-006", "智能商业服务", "retail", [
        [116.349, 39.944], [116.355, 39.944], [116.355, 39.94984],
        [116.349, 39.94984], [116.349, 39.944]
    ]),
    # Corridor connecting sections - railway park and green
    ("LU-007", "京张遗址公园绿廊", "green_space", [
        [116.3407, 39.939], [116.342, 39.939], [116.342, 40.0265],
        [116.3407, 40.0265], [116.3407, 39.939]
    ]),
    ("LU-008", "文化展示与公共空间", "cultural", [
        [116.354, 39.939], [116.3553, 39.939], [116.3553, 40.0265],
        [116.354, 40.0265], [116.354, 39.939]
    ]),
    # Connecting zones between key areas
    ("LU-009", "教育科研配套", "education", [
        [116.342, 39.94984], [116.355, 39.94984], [116.353, 39.9835],
        [116.342, 39.9835], [116.342, 39.94984]
    ]),
    ("LU-010", "交通接驳与社区服务", "community_service", [
        [116.342, 39.9935], [116.353, 39.9935], [116.354, 40.0075],
        [116.343, 40.0075], [116.342, 39.9935]
    ]),
]

land_features = []
for fid, name, lu_type, coords in land_uses:
    land_features.append(make_feature(fid, "LAND_USE", "Polygon", [coords], {
        "name_zh": name,
        "land_use_type": lu_type,
        "official_boundary": False
    }))
write_geojson("land_use.geojson", land_features, "land_use")

# 4. buildings.geojson - representative building footprints
buildings = [
    ("BLD-001", "ai_r_and_d", 116.345, 40.010, 0.003, 0.003),
    ("BLD-002", "ai_r_and_d", 116.350, 40.012, 0.003, 0.003),
    ("BLD-003", "lab", 116.351, 40.018, 0.002, 0.003),
    ("BLD-004", "incubator", 116.346, 40.020, 0.003, 0.002),
    ("BLD-005", "mixed_use", 116.344, 39.985, 0.003, 0.003),
    ("BLD-006", "mixed_use", 116.349, 39.987, 0.003, 0.003),
    ("BLD-007", "talent_apartment", 116.350, 39.990, 0.002, 0.002),
    ("BLD-008", "office", 116.344, 39.945, 0.003, 0.002),
    ("BLD-009", "office", 116.350, 39.946, 0.003, 0.002),
    ("BLD-010", "retail", 116.352, 39.947, 0.002, 0.002),
    ("BLD-011", "cultural", 116.346, 39.952, 0.003, 0.002),
    ("BLD-012", "education", 116.348, 39.960, 0.003, 0.003),
    ("BLD-013", "community_service", 116.345, 39.970, 0.002, 0.002),
    ("BLD-014", "ai_r_and_d", 116.347, 40.005, 0.002, 0.002),
    ("BLD-015", "mobility_hub", 116.348, 39.978, 0.002, 0.001),
]

bld_features = []
for fid, btype, cx, cy, dx, dy in buildings:
    coords = [
        [cx-dx, cy-dy], [cx+dx, cy-dy], [cx+dx, cy+dy],
        [cx-dx, cy+dy], [cx-dx, cy-dy]
    ]
    bld_features.append(make_feature(fid, "BUILDING_FOOTPRINT", "Polygon", [coords], {
        "name_zh": f"建筑{fid}",
        "building_type": btype,
        "official_boundary": False
    }))
write_geojson("buildings.geojson", bld_features, "buildings")

# 5. roads.geojson - road centerlines along the corridor
roads = [
    ("RD-001", "主干道", "trunk_road", [
        [116.341, 39.939], [116.341, 40.0265]
    ]),
    ("RD-002", "主干道", "trunk_road", [
        [116.355, 39.939], [116.355, 40.0265]
    ]),
    ("RD-003", "次干道", "secondary_road", [
        [116.3407, 39.965], [116.3553, 39.965]
    ]),
    ("RD-004", "次干道", "secondary_road", [
        [116.3407, 39.99], [116.3553, 39.99]
    ]),
    ("RD-005", "次干道", "secondary_road", [
        [116.3407, 40.0075], [116.3553, 40.0075]
    ]),
    ("RD-006", "慢行廊道", "slow_mobility", [
        [116.348, 39.939], [116.348, 40.0265]
    ]),
    ("RD-007", "慢行廊道", "slow_mobility", [
        [116.343, 39.944], [116.349, 39.949]
    ]),
    ("RD-008", "慢行廊道", "slow_mobility", [
        [116.343, 39.984], [116.349, 39.993]
    ]),
    ("RD-009", "慢行廊道", "slow_mobility", [
        [116.343, 40.008], [116.349, 40.026]
    ]),
]

road_features = []
for fid, name, rtype, coords in roads:
    road_features.append(make_feature(fid, "ROAD_CENTERLINE", "LineString", coords, {
        "name_zh": name,
        "road_type": rtype,
        "official_boundary": False
    }))
write_geojson("roads.geojson", road_features, "roads")

# 6. green_space.geojson
greens = [
    ("GS-001", "京张遗址公园绿廊", [
        [116.3407, 39.939], [116.342, 39.939], [116.342, 40.0265],
        [116.3407, 40.0265], [116.3407, 39.939]
    ]),
    ("GS-002", "众智园中央绿地", [
        [116.343, 40.015], [116.354, 40.015], [116.354, 40.020],
        [116.343, 40.020], [116.343, 40.015]
    ]),
    ("GS-003", "AI原点社区公园", [
        [116.342, 39.988], [116.353, 39.988], [116.353, 39.991],
        [116.342, 39.991], [116.342, 39.988]
    ]),
    ("GS-004", "大钟寺口袋公园", [
        [116.342, 39.946], [116.346, 39.946], [116.346, 39.949],
        [116.342, 39.949], [116.342, 39.946]
    ]),
    ("GS-005", "小月河滨水绿带", [
        [116.342, 39.95], [116.355, 39.95], [116.353, 39.984],
        [116.342, 39.984], [116.342, 39.95]
    ]),
]

green_features = []
for fid, name, coords in greens:
    green_features.append(make_feature(fid, "GREEN_SPACE", "Polygon", [coords], {
        "name_zh": name,
        "green_type": "park_and_corridor",
        "official_boundary": False
    }))
write_geojson("green_space.geojson", green_features, "green_space")

# 7. public_space.geojson
publics = [
    ("PS-001", "AI开发者广场", [
        [116.344, 39.985], [116.350, 39.985], [116.350, 39.989],
        [116.344, 39.989], [116.344, 39.985]
    ]),
    ("PS-002", "开源成果展示廊", [
        [116.341, 39.960], [116.347, 39.960], [116.347, 39.964],
        [116.341, 39.964], [116.341, 39.960]
    ]),
    ("PS-003", "智能体贡献荣誉墙", [
        [116.349, 40.010], [116.353, 40.010], [116.353, 40.014],
        [116.349, 40.014], [116.349, 40.010]
    ]),
    ("PS-004", "京张文化体验广场", [
        [116.344, 39.948], [116.350, 39.948], [116.350, 39.951],
        [116.344, 39.951], [116.344, 39.948]
    ]),
    ("PS-005", "AI场景测试广场", [
        [116.345, 40.005], [116.351, 40.005], [116.351, 40.008],
        [116.345, 40.008], [116.345, 40.005]
    ]),
    ("PS-006", "未来生活体验街", [
        [116.343, 39.970], [116.353, 39.970], [116.353, 39.974],
        [116.343, 39.974], [116.343, 39.970]
    ]),
]

public_features = []
for fid, name, coords in publics:
    public_features.append(make_feature(fid, "PUBLIC_SPACE", "Polygon", [coords], {
        "name_zh": name,
        "public_space_type": "plaza_and_experience",
        "official_boundary": False
    }))
write_geojson("public_space.geojson", public_features, "public_space")

# 8. constraints.geojson
constraints = [
    ("CON-001", "京张铁路遗址保护带", [
        [116.3475, 39.939], [116.349, 39.939], [116.349, 40.0265],
        [116.3475, 40.0265], [116.3475, 39.939]
    ]),
    ("CON-002", "北五环路控制线", [
        [116.3407, 40.025], [116.3553, 40.025], [116.3553, 40.0265],
        [116.3407, 40.0265], [116.3407, 40.025]
    ]),
    ("CON-003", "轨道站点影响范围", [
        [116.346, 39.946], [116.350, 39.946], [116.350, 39.950],
        [116.346, 39.950], [116.346, 39.946]
    ]),
]

con_features = []
for fid, name, coords in constraints:
    con_features.append(make_feature(fid, "REGULATORY_CONTROL", "Polygon", [coords], {
        "name_zh": name,
        "constraint_type": "heritage_and_infrastructure",
        "official_boundary": False,
        "usage_note": "概念性约束，需官方确认"
    }))
write_geojson("constraints.geojson", con_features, "constraints")

# 9. phasing.geojson
phases = [
    ("PH-001", "近期(2026-2028)", [
        [116.342, 39.944], [116.355, 39.944], [116.355, 39.952],
        [116.342, 39.952], [116.342, 39.944]
    ]),
    ("PH-002", "中期(2028-2030)", [
        [116.342, 39.952], [116.355, 39.952], [116.353, 39.994],
        [116.342, 39.994], [116.342, 39.952]
    ]),
    ("PH-003", "远期(2030-2035)", [
        [116.342, 39.994], [116.354, 39.994], [116.354, 40.026],
        [116.343, 40.026], [116.342, 39.994]
    ]),
]

phase_features = []
for fid, name, coords in phases:
    phase_features.append(make_feature(fid, "PHASE", "Polygon", [coords], {
        "name_zh": name,
        "phase_type": "implementation_phase",
        "official_boundary": False
    }))
write_geojson("phasing.geojson", phase_features, "phasing")

print("\nAll GeoJSON files generated successfully.")
