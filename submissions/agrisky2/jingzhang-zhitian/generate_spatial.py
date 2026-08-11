"""
京张智田 (Jing-Zhang Smart Farm) - Spatial Data Generator
Generates all required GeoJSON files and figures for the submission.
"""
import json
import math
import os

BASE = os.path.dirname(os.path.abspath(__file__))
GEOM_DIR = os.path.join(BASE, "geometry")
FIG_DIR = os.path.join(BASE, "assets", "figures")

os.makedirs(GEOM_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)

# ============================================================
# SITE BOUNDARY (from provisional data)
# ============================================================
SITE_COORDS = [
    [116.3407, 39.939], [116.3553, 39.939], [116.3553, 39.965],
    [116.3533, 39.99], [116.3553, 40.0265], [116.3427, 40.0265],
    [116.3417, 40.006], [116.3397, 39.975], [116.3407, 39.939]
]

# Simplified key areas based on site boundary
# Northern: 众智园 (Smart AgTech R&D) ~40.00-40.026
# Central: AI原点社区 (FoodTech Hub) ~39.975-39.995
# Southern: 大钟寺 (Food Experience) ~39.94-39.955

def make_polygon(feature_id, layer, props, coords):
    return {
        "type": "Feature",
        "id": feature_id,
        "properties": {
            "id": feature_id,
            "layer": layer,
            **props
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [coords]
        }
    }

def make_feature_collection(features, name, metadata=None):
    fc = {
        "type": "FeatureCollection",
        "name": name,
        "features": features
    }
    if metadata:
        fc["metadata"] = metadata
    return fc

# ============================================================
# 1. site_boundary.geojson
# ============================================================
site_meta = {
    "boundary_status": "maintainer_defined_provisional",
    "official_boundary_available_in_repository": False,
    "coordinate_reference_system": "EPSG:4326",
    "area_check_crs": "EPSG:4548",
    "source_id": "DATA-SRC-PROVISIONAL-BOUNDARIES-20260605"
}

site_boundary = make_polygon(
    "PROV-SITE-001", "SITE_BOUNDARY",
    {
        "scope_id": "overall_design_area",
        "name_zh": "总体设计范围",
        "source_type": "agent_inferred_from_public_data",
        "confidence": "medium",
        "geometry_role": "provisional_constraint",
        "official_boundary": False,
        "boundary_precision": "provisional_rough",
        "area_sqm_declared": 11400000
    },
    SITE_COORDS
)

with open(os.path.join(GEOM_DIR, "site_boundary.geojson"), "w") as f:
    json.dump(make_feature_collection([site_boundary], "site_boundary", site_meta), f, indent=2, ensure_ascii=False)

# ============================================================
# 2. key_areas.geojson
# ============================================================
key_areas = [
    make_polygon("PROV-KEY-001", "KEY_AREA",
        {"area_id": "zhongzhiyuan_ai_acceleration_area",
         "name_zh": "众智园AI自主创新加速区 — 智慧育种与农业AI研发验证区",
         "source_type": "agent_inferred_from_public_data",
         "confidence": "medium",
         "geometry_role": "provisional_constraint",
         "official_boundary": False,
         "boundary_precision": "provisional_rough",
         "announced_area_sqm": 1921000},
        [[116.343, 40.0075], [116.354, 40.0075], [116.354, 40.026], [116.343, 40.026], [116.343, 40.0075]]
    ),
    make_polygon("PROV-KEY-002", "KEY_AREA",
        {"area_id": "beijing_ai_origin_community",
         "name_zh": "北京AI原点社区 — 食品科技/FoodTech孵化转化区",
         "source_type": "agent_inferred_from_public_data",
         "confidence": "medium",
         "geometry_role": "provisional_constraint",
         "official_boundary": False,
         "boundary_precision": "provisional_rough",
         "announced_area_sqm": 1043000},
        [[116.342, 39.9835], [116.353, 39.9835], [116.353, 39.9935], [116.342, 39.9935], [116.342, 39.9835]]
    ),
    make_polygon("PROV-KEY-003", "KEY_AREA",
        {"area_id": "dazhongsi_ai_industry_cluster",
         "name_zh": "大钟寺AI产业聚集区 — 未来食品体验与全球粮食安全论坛",
         "source_type": "agent_inferred_from_public_data",
         "confidence": "medium",
         "geometry_role": "provisional_constraint",
         "official_boundary": False,
         "boundary_precision": "provisional_rough",
         "announced_area_sqm": 720000},
        [[116.342, 39.944], [116.355, 39.944], [116.355, 39.94984], [116.342, 39.94984], [116.342, 39.944]]
    )
]

with open(os.path.join(GEOM_DIR, "key_areas.geojson"), "w") as f:
    json.dump(make_feature_collection(key_areas, "key_areas"), f, indent=2, ensure_ascii=False)

# ============================================================
# 3. land_use.geojson - Dividing the site into land use zones
# ============================================================
# Land use types based on MNR classification:
# 08=科研, 09=商业, 07=居住, 08H2=科教, 14=绿地

land_use_zones = [
    # Northern - 众智园: AgTech R&D Campus
    make_polygon("LU-001", "LAND_USE",
        {"land_use_code": "08H2", "land_use_zh": "科研用地(农业AI与智慧育种)",
         "area_category": "AI_agritech_rd", "key_area": "zhongzhiyuan",
         "area_sqm_approx": 480000, "far_max_concept": 2.5, "height_max_concept_m": 60},
        [[116.3432, 40.014], [116.3538, 40.014], [116.3538, 40.0245], [116.3432, 40.0245], [116.3432, 40.014]]
    ),
    make_polygon("LU-002", "LAND_USE",
        {"land_use_code": "14", "land_use_zh": "绿地与开敞空间(都市农业试验田)",
         "area_category": "urban_farming_demo", "key_area": "zhongzhiyuan",
         "area_sqm_approx": 240000},
        [[116.3432, 40.0085], [116.3538, 40.0085], [116.3538, 40.0135], [116.3432, 40.0135], [116.3432, 40.0085]]
    ),
    # Central - AI原点社区: FoodTech Innovation
    make_polygon("LU-003", "LAND_USE",
        {"land_use_code": "09", "land_use_zh": "商业服务业用地(FoodTech孵化与转化中心)",
         "area_category": "foodtech_commercial", "key_area": "ai_origin",
         "area_sqm_approx": 350000, "far_max_concept": 3.0, "height_max_concept_m": 80},
        [[116.3422, 39.986], [116.3528, 39.986], [116.3528, 39.9925], [116.3422, 39.9925], [116.3422, 39.986]]
    ),
    make_polygon("LU-004", "LAND_USE",
        {"land_use_code": "07", "land_use_zh": "居住用地(创新人才社区)",
         "area_category": "talent_residential", "key_area": "ai_origin",
         "area_sqm_approx": 250000, "far_max_concept": 2.0, "height_max_concept_m": 45},
        [[116.3422, 39.9838], [116.3528, 39.9838], [116.3528, 39.9855], [116.3422, 39.9855], [116.3422, 39.9838]]
    ),
    # Southern - 大钟寺: Future Food Experience
    make_polygon("LU-005", "LAND_USE",
        {"land_use_code": "09", "land_use_zh": "商业服务业用地(未来食品体验中心/全球粮食安全论坛)",
         "area_category": "food_experience", "key_area": "dazhongsi",
         "area_sqm_approx": 420000, "far_max_concept": 3.5, "height_max_concept_m": 100},
        [[116.3422, 39.9443], [116.3548, 39.9443], [116.3548, 39.9493], [116.3422, 39.9493], [116.3422, 39.9443]]
    ),
    # Central corridor green space (Jing-Zhang Railway Heritage Park)
    make_polygon("LU-006", "LAND_USE",
        {"land_use_code": "14", "land_use_zh": "绿地与开敞空间(京张铁路遗址公园活力带)",
         "area_category": "heritage_park", "key_area": None,
         "area_sqm_approx": 1800000},
        [[116.3445, 39.94], [116.3485, 39.94], [116.3485, 39.975], [116.3475, 39.995],
         [116.3485, 40.025], [116.3445, 40.025], [116.3435, 39.995], [116.3445, 39.975],
         [116.3445, 39.94]]
    ),
    # Technology service wing
    make_polygon("LU-007", "LAND_USE",
        {"land_use_code": "09", "land_use_zh": "商业服务业用地(AI+农业科技服务与知识产权运营)",
         "area_category": "tech_service", "key_area": None,
         "area_sqm_approx": 2000000, "far_max_concept": 2.5},
        [[116.3407, 39.95], [116.344, 39.95], [116.344, 39.985], [116.343, 40.005],
         [116.3417, 40.006], [116.3407, 39.975], [116.3407, 39.95]]
    ),
    # Scenario wing with mixed use
    make_polygon("LU-008", "LAND_USE",
        {"land_use_code": "09", "land_use_zh": "混合用地(AI+农业场景测试与展示)",
         "area_category": "scenario_mixed", "key_area": None,
         "area_sqm_approx": 1500000, "far_max_concept": 2.0},
        [[116.349, 39.94], [116.3553, 39.94], [116.3553, 39.965], [116.3533, 39.99],
         [116.349, 39.99], [116.349, 39.96], [116.349, 39.94]]
    )
]

with open(os.path.join(GEOM_DIR, "land_use.geojson"), "w") as f:
    json.dump(make_feature_collection(land_use_zones, "land_use"), f, indent=2, ensure_ascii=False)

# ============================================================
# 4. buildings.geojson - Conceptual building footprints
# ============================================================
buildings = []
bid = 0
# Generate building footprints in key areas
for lu_zone in land_use_zones:
    lu = lu_zone["properties"]
    coords = lu_zone["geometry"]["coordinates"][0]
    if lu.get("far_max_concept"):
        # Generate a few building blocks within the zone
        min_lon = min(c[0] for c in coords)
        max_lon = max(c[0] for c in coords)
        min_lat = min(c[1] for c in coords)
        max_lat = max(c[1] for c in coords)
        w = max_lon - min_lon
        h = max_lat - min_lat
        for row in range(2):
            for col in range(3):
                bx = min_lon + w * 0.1 + col * w * 0.28
                by = min_lat + h * 0.1 + row * h * 0.4
                bw = w * 0.2
                bh = h * 0.25
                bid += 1
                buildings.append(make_polygon(
                    f"BLD-{bid:03d}", "BUILDING_FOOTPRINT",
                    {"building_type": lu["area_category"] if row == 0 else "mix",
                     "height_concept_m": lu.get("height_max_concept_m", 30) * (0.6 + row * 0.3),
                     "floors_concept": int(lu.get("height_max_concept_m", 30) * (0.6 + row * 0.3) / 4),
                     "status": "proposed"},
                    [[bx, by], [bx + bw, by], [bx + bw, by + bh], [bx, by + bh], [bx, by]]
                ))

with open(os.path.join(GEOM_DIR, "buildings.geojson"), "w") as f:
    json.dump(make_feature_collection(buildings, "buildings"), f, indent=2, ensure_ascii=False)

# ============================================================
# 5. roads.geojson - Conceptual road network
# ============================================================
roads = []
rid = 0
# North-South main corridor (along Jing-Zhang)
for lat in [39.942, 39.95, 39.96, 39.97, 39.98, 39.99, 40.005, 40.015, 40.024]:
    rid += 1
    roads.append({
        "type": "Feature",
        "id": f"ROAD-{rid:03d}",
        "properties": {
            "id": f"ROAD-{rid:03d}", "layer": "ROAD_CENTERLINE",
            "road_type": "primary" if rid % 3 == 0 else "secondary",
            "name_zh": f"京张创新走廊{['北','中','南'][rid%3]}段",
            "source_type": "design_concept", "confidence": "medium"
        },
        "geometry": {
            "type": "LineString",
            "coordinates": [[116.345, lat], [116.354, lat]]
        }
    })
# Longitudinal connectors
for lon in [116.341, 116.343, 116.347, 116.35, 116.354]:
    rid += 1
    roads.append({
        "type": "Feature",
        "id": f"ROAD-{rid:03d}",
        "properties": {
            "id": f"ROAD-{rid:03d}", "layer": "ROAD_CENTERLINE",
            "road_type": "connector",
            "name_zh": "创新连接路",
            "source_type": "design_concept", "confidence": "medium"
        },
        "geometry": {
            "type": "LineString",
            "coordinates": [[lon, 39.94], [lon, 40.025]]
        }
    })

with open(os.path.join(GEOM_DIR, "roads.geojson"), "w") as f:
    json.dump(make_feature_collection(roads, "roads"), f, indent=2, ensure_ascii=False)

# ============================================================
# 6. green_space.geojson
# ============================================================
green_spaces = [
    make_polygon("GRN-001", "GREEN_SPACE",
        {"name_zh": "京张铁路遗址公园(线性绿廊)", "green_type": "linear_park",
         "source_type": "design_concept", "area_sqm_approx": 350000},
        [[116.3455, 39.940], [116.3475, 39.940], [116.3475, 39.975], [116.3465, 39.995],
         [116.3475, 40.025], [116.3455, 40.025], [116.3445, 39.995], [116.3455, 39.975],
         [116.3455, 39.940]]
    ),
    make_polygon("GRN-002", "GREEN_SPACE",
        {"name_zh": "清河滨水绿廊", "green_type": "waterfront",
         "source_type": "design_concept", "area_sqm_approx": 180000},
        [[116.3407, 40.022], [116.355, 40.022], [116.355, 40.0265], [116.3427, 40.0265],
         [116.3407, 40.022]]
    ),
    make_polygon("GRN-003", "GREEN_SPACE",
        {"name_zh": "小月河生态廊道", "green_type": "waterfront",
         "source_type": "design_concept", "area_sqm_approx": 120000},
        [[116.3407, 39.987], [116.354, 39.987], [116.354, 39.9935], [116.342, 39.9935],
         [116.3407, 39.987]]
    ),
    make_polygon("GRN-004", "GREEN_SPACE",
        {"name_zh": "都市农业示范园", "green_type": "urban_farm",
         "source_type": "design_concept", "area_sqm_approx": 80000},
        [[116.3485, 40.008], [116.3535, 40.008], [116.3535, 40.0135], [116.3485, 40.0135],
         [116.3485, 40.008]]
    )
]

with open(os.path.join(GEOM_DIR, "green_space.geojson"), "w") as f:
    json.dump(make_feature_collection(green_spaces, "green_space"), f, indent=2, ensure_ascii=False)

# ============================================================
# 7. public_space.geojson
# ============================================================
public_spaces = [
    make_polygon("PUB-001", "PUBLIC_SPACE",
        {"name_zh": "开源广场/Agent贡献荣誉墙", "public_type": "plaza",
         "source_type": "design_concept"},
        [[116.346, 39.982], [116.348, 39.982], [116.348, 39.984], [116.346, 39.984], [116.346, 39.982]]
    ),
    make_polygon("PUB-002", "PUBLIC_SPACE",
        {"name_zh": "AI+农业创新展示廊", "public_type": "exhibition_corridor",
         "source_type": "design_concept"},
        [[116.346, 39.99], [116.348, 39.99], [116.348, 39.992], [116.346, 39.992], [116.346, 39.99]]
    ),
    make_polygon("PUB-003", "PUBLIC_SPACE",
        {"name_zh": "全球粮食安全论坛广场", "public_type": "forum_plaza",
         "source_type": "design_concept"},
        [[116.346, 39.946], [116.348, 39.946], [116.348, 39.948], [116.346, 39.948], [116.346, 39.946]]
    ),
    make_polygon("PUB-004", "PUBLIC_SPACE",
        {"name_zh": "开发者散步道", "public_type": "promenade",
         "source_type": "design_concept"},
        [[116.345, 39.955], [116.3475, 39.955], [116.3475, 39.965], [116.345, 39.965], [116.345, 39.955]]
    )
]

with open(os.path.join(GEOM_DIR, "public_space.geojson"), "w") as f:
    json.dump(make_feature_collection(public_spaces, "public_space"), f, indent=2, ensure_ascii=False)

# ============================================================
# 8. constraints.geojson
# ============================================================
constraints = [
    make_polygon("CST-001", "CONSTRAINTS",
        {"name_zh": "京张铁路遗址保护廊道", "constraint_type": "heritage_protection",
         "source_type": "public_context", "restriction": "历史文化保护要求，具体保护范围和控高待确认"},
        [[116.3458, 39.940], [116.3472, 39.940], [116.3472, 40.025], [116.3458, 40.025], [116.3458, 39.940]]
    ),
    make_polygon("CST-002", "CONSTRAINTS",
        {"name_zh": "清河蓝线及生态缓冲区", "constraint_type": "water_protection",
         "source_type": "public_context", "restriction": "河道蓝线及生态保护要求，具体范围待确认"},
        [[116.341, 40.023], [116.354, 40.023], [116.354, 40.0265], [116.3427, 40.0265], [116.341, 40.023]]
    )
]

with open(os.path.join(GEOM_DIR, "constraints.geojson"), "w") as f:
    json.dump(make_feature_collection(constraints, "constraints"), f, indent=2, ensure_ascii=False)

# ============================================================
# 9. phasing.geojson
# ============================================================
phases = [
    make_polygon("PHS-001", "PHASE",
        {"phase": "near_term", "name_zh": "近期(2026-2028): 大钟寺未来食品体验区先导项目",
         "timeline": "2026-2028", "priority": 1},
        [[116.342, 39.944], [116.355, 39.944], [116.355, 39.9495], [116.342, 39.9495], [116.342, 39.944]]
    ),
    make_polygon("PHS-002", "PHASE",
        {"phase": "mid_term", "name_zh": "中期(2028-2031): AI原点社区FoodTech孵化转化区",
         "timeline": "2028-2031", "priority": 2},
        [[116.342, 39.984], [116.353, 39.984], [116.353, 39.993], [116.342, 39.993], [116.342, 39.984]]
    ),
    make_polygon("PHS-003", "PHASE",
        {"phase": "long_term", "name_zh": "远期(2031-2035): 众智园智慧育种研发区",
         "timeline": "2031-2035", "priority": 3},
        [[116.343, 40.008], [116.354, 40.008], [116.354, 40.0255], [116.343, 40.0255], [116.343, 40.008]]
    )
]

with open(os.path.join(GEOM_DIR, "phasing.geojson"), "w") as f:
    json.dump(make_feature_collection(phases, "phasing"), f, indent=2, ensure_ascii=False)

print("All 9 GeoJSON files generated successfully.")
print(f"Files in {GEOM_DIR}:")
for fname in sorted(os.listdir(GEOM_DIR)):
    size = os.path.getsize(os.path.join(GEOM_DIR, fname))
    print(f"  {fname} ({size:,} bytes)")
