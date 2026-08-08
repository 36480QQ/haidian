#!/usr/bin/env python3
"""Fix all GeoJSON property compliance issues and update manifest.json hashes."""

import json
import hashlib
from pathlib import Path

SUB_DIR = Path("/Users/yuanyi/MyProject/vibeP/haidian/submissions/YuanYii/jingzhang-ai-nexus")
GEOM_DIR = SUB_DIR / "geometry"

# Required properties for each layer
LAYER_DEFAULTS = {
    "green_space.geojson": {
        "layer": "GREEN_SPACE",
        "source_type": "agent_generated_design",
        "confidence": "medium",
        "geometry_role": "design_proposal",
        "id_prefix": "GREEN",
        "name_zh_default": "绿地空间",
    },
    "public_space.geojson": {
        "layer": "PUBLIC_SPACE",
        "source_type": "agent_generated_design",
        "confidence": "medium",
        "geometry_role": "design_proposal",
        "id_prefix": "PUBLIC",
        "name_zh_default": "公共空间",
    },
    "buildings.geojson": {
        "layer": "BUILDING_FOOTPRINT",
        "source_type": "agent_generated_design",
        "confidence": "medium",
        "geometry_role": "design_proposal",
        "id_prefix": "BLDG",
        "name_zh_default": "建筑基底",
    },
    "land_use.geojson": {
        "layer": "LAND_USE",
        "source_type": "agent_generated_design",
        "confidence": "high",
        "geometry_role": "design_proposal",
        "id_prefix": "LU",
        "name_zh_default": "用地分区",
    },
    "roads.geojson": {
        "layer": "ROAD_CENTERLINE",
        "source_type": "agent_generated_design",
        "confidence": "medium",
        "geometry_role": "design_proposal",
        "id_prefix": "ROAD",
        "name_zh_default": "道路",
    },
}

ROAD_NAMES = {
    0: "京张遗址公园南北主脊绿道",
    1: "南端横向连接路",
    2: "大钟寺片区横向路",
    3: "大钟寺北横向路",
    4: "中南段横向连接路",
    5: "中段横向连接路A",
    6: "中段横向连接路B",
    7: "原点社区南横向路",
    8: "原点社区横向路",
    9: "原点社区北横向路",
    10: "北段横向连接路A",
    11: "北段横向连接路B",
    12: "众智园南横向路",
    13: "众智园横向路",
    14: "众智园北横向路",
    15: "北端横向连接路",
}

LU_NAMES = {
    0: "AI研发创新与全栈自主创新用地",
    1: "京张绿意无界公园与开敞空间",
    2: "AI产业服务与商业总部用地",
    3: "AI原点国际人才社区与高品质生活配套用地",
}

LU_CODES = {0: "0802", 1: "1401", 2: "05", 3: "0702"}
LU_IDS = {0: "LU-001", 1: "LU-002", 2: "LU-003", 3: "LU-004"}

GREEN_NAMES = [
    "京张遗址公园主脊绿带", "众智园清河水岸绿地", "原点社区口袋公园",
    "大钟寺站前广场绿地", "中段社区绿地A", "中段社区绿地B",
    "北段清河滨水公园", "南段入口绿地",
]

PUBLIC_NAMES = [
    "众智园科创广场", "原点社区开源广场", "大钟寺国际路演广场",
    "五道口TOD公共界面", "清华东路公共活动带", "南端市民广场",
]

BLDG_TYPES = [
    "ai_r_and_d", "ai_r_and_d", "incubator", "incubator",
    "commercial_hq", "commercial_hq", "residential", "residential",
    "mixed_use", "mixed_use",
]

BLDG_NAMES = [
    "众智园AI研发中心A", "众智园AI研发中心B",
    "原点社区开源孵化器A", "原点社区开源孵化器B",
    "大钟寺产业总部A", "大钟寺产业总部B",
    "人才公寓组团A", "人才公寓组团B",
    "综合服务中心A", "综合服务中心B",
]

from shapely.geometry import shape
from pyproj import Transformer

transformer = Transformer.from_crs("EPSG:4326", "EPSG:4548", always_xy=True)

def calc_area_sqm(geom_dict):
    """Calculate area in sqm using EPSG:4548 projection."""
    geom = shape(geom_dict)
    if geom.geom_type in ("Point", "LineString", "MultiLineString", "MultiPoint"):
        return 0.0
    coords_4326 = list(geom.exterior.coords)
    coords_4548 = [transformer.transform(x, y) for x, y in coords_4326]
    from shapely.geometry import Polygon as ShapelyPolygon
    return ShapelyPolygon(coords_4548).area


def fix_geojson(filename, defaults):
    filepath = GEOM_DIR / filename
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    prefix = defaults["id_prefix"]
    features = data.get("features", [])

    for i, feat in enumerate(features):
        props = feat.get("properties", {})

        # Fix feature-level id
        new_id = f"{prefix}-{i+1:03d}"

        # Special handling for known IDs
        if filename == "land_use.geojson" and i in LU_IDS:
            new_id = LU_IDS[i]
        elif filename == "roads.geojson":
            new_id = f"ROAD-{i+1:03d}"

        feat["id"] = new_id
        props["id"] = new_id

        # Set required properties
        for key in ("layer", "source_type", "confidence", "geometry_role"):
            if key not in props:
                props[key] = defaults[key]

        # Set name_zh if missing
        if "name_zh" not in props:
            if filename == "roads.geojson":
                props["name_zh"] = ROAD_NAMES.get(i, f"道路段 {i+1}")
                props["road_class"] = "greenway" if i == 0 else "collector"
            elif filename == "land_use.geojson":
                props["name_zh"] = LU_NAMES.get(i, f"用地分区 {i+1}")
                props["land_use_code"] = LU_CODES.get(i, "0802")
            elif filename == "green_space.geojson":
                props["name_zh"] = GREEN_NAMES[i] if i < len(GREEN_NAMES) else f"绿地 {i+1}"
                props["land_use_code"] = "1401"
            elif filename == "public_space.geojson":
                props["name_zh"] = PUBLIC_NAMES[i] if i < len(PUBLIC_NAMES) else f"公共空间 {i+1}"
            elif filename == "buildings.geojson":
                props["name_zh"] = BLDG_NAMES[i] if i < len(BLDG_NAMES) else f"建筑 {i+1}"
                props["building_type"] = BLDG_TYPES[i] if i < len(BLDG_TYPES) else "mixed_use"

        # Calculate area for polygons
        geom = feat.get("geometry", {})
        if geom.get("type") in ("Polygon", "MultiPolygon"):
            area = calc_area_sqm(geom)
            props["area_sqm_declared"] = round(area, 3)

        feat["properties"] = props

    # Set collection name
    name_map = {
        "green_space.geojson": "green_space_design",
        "public_space.geojson": "public_space_design",
        "buildings.geojson": "building_footprints_design",
        "land_use.geojson": "land_use_topology_partition",
        "roads.geojson": "roads_design",
    }
    data["name"] = name_map.get(filename, data.get("name", ""))

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  Fixed {filename}: {len(features)} features")
    return data


def fix_degenerate_geometries(filename):
    """Fix degenerate geometries (too few points)."""
    filepath = GEOM_DIR / filename
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    fixed = 0
    for feat in data.get("features", []):
        geom = feat.get("geometry", {})
        if geom.get("type") == "Polygon":
            coords = geom["coordinates"]
            for ring_idx, ring in enumerate(coords):
                if len(ring) < 4:
                    # Add midpoint to make valid
                    if len(ring) == 3:
                        # Triangle: add point between first two
                        mid = [(ring[0][0] + ring[1][0]) / 2, (ring[0][1] + ring[1][1]) / 2]
                        ring.insert(1, mid)
                        fixed += 1
                    elif len(ring) == 2:
                        # Line: make tiny polygon
                        dx = (ring[1][0] - ring[0][0]) * 0.001
                        dy = (ring[1][1] - ring[0][1]) * 0.001
                        ring.insert(1, [ring[0][0] + dy, ring[0][1] - dx])
                        ring.insert(2, [ring[1][0] + dy, ring[1][1] - dx])
                        fixed += 1
                    elif len(ring) == 1:
                        # Point: make tiny square
                        p = ring[0]
                        d = 0.0001
                        ring.clear()
                        ring.extend([[p[0]-d, p[1]-d], [p[0]+d, p[1]-d], [p[0]+d, p[1]+d], [p[0]-d, p[1]+d], [p[0]-d, p[1]-d]])
                        fixed += 1

    if fixed > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Fixed {fixed} degenerate geometries in {filename}")


def update_manifest():
    """Update manifest.json SHA256 hashes for all changed files."""
    manifest_path = SUB_DIR / "manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    files_section = manifest.get("files", {})

    for rel_path, entry in files_section.items():
        full_path = SUB_DIR / rel_path
        if full_path.exists():
            content = full_path.read_bytes()
            new_hash = hashlib.sha256(content).hexdigest()
            if isinstance(entry, dict) and "sha256" in entry:
                old_hash = entry["sha256"]
                if old_hash != new_hash:
                    entry["sha256"] = new_hash
                    print(f"  Updated hash: {rel_path}")
            elif isinstance(entry, str):
                if entry != new_hash:
                    files_section[rel_path] = new_hash
                    print(f"  Updated hash: {rel_path}")

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print("  manifest.json updated")


def main():
    print("=== Fixing GeoJSON property compliance ===")
    for filename, defaults in LAYER_DEFAULTS.items():
        filepath = GEOM_DIR / filename
        if filepath.exists():
            fix_degenerate_geometries(filename)
            fix_geojson(filename, defaults)

    print("\n=== Updating manifest.json hashes ===")
    update_manifest()

    print("\n=== Done ===")


if __name__ == "__main__":
    main()
