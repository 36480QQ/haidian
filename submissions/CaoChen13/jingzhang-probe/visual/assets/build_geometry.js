# -*- coding: utf-8 -*-
"""Deterministically rebuild the submitted spatial package.

This file contains Python despite its ``.js`` transport suffix.  The repository
submission allow-list accepts auxiliary executable text only under
``visual/assets`` with a web-asset suffix.  Execute it with Python exactly as
documented in proposal.md; it is not loaded by visual/index.html.

Inputs are deliberately limited to:

* the repository's provisional boundary collection;
* the official/cleared planning-limit values in the site package; and
* a fixed OSM snapshot used only to emit non-quantified analysis-helper lines.

No random choices, filesystem-order choices, OSM-derived areas, OSM-derived
lengths, statutory controls, heights, or floor-area ratios are produced.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable

from pyproj import Transformer
from shapely import affinity
from shapely.geometry import (
    GeometryCollection,
    LineString,
    MultiLineString,
    MultiPolygon,
    Point,
    Polygon,
    box,
    mapping,
    shape,
)
from shapely.geometry.polygon import orient
from shapely.ops import transform, unary_union


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_SUBMISSION = SCRIPT_DIR.parents[1]
INPUT_BUNDLE = SCRIPT_DIR / "repro_inputs.js"

WGS84 = "EPSG:4326"
AREA_CRS = "EPSG:4548"
TO_METRIC = Transformer.from_crs(WGS84, AREA_CRS, always_xy=True)
TO_WGS84 = Transformer.from_crs(AREA_CRS, WGS84, always_xy=True)
COORDINATE_DECIMALS = 14

# All geometric criteria are executable constants, not descriptive comments.
SPINE_Y_FRACTIONS = (0.02, 0.12, 0.24, 0.36, 0.49, 0.62, 0.75, 0.87, 0.98)
SPINE_X_FRACTIONS = (0.56, 0.54, 0.52, 0.49, 0.51, 0.48, 0.52, 0.55, 0.57)
NODE_SPECS = (
    (0.08, 118.0, 48.0, "南门户日常会合点"),
    (0.19, 132.0, 55.0, "社区服务与休憩点"),
    (0.33, 145.0, 62.0, "公共文化与展示点"),
    (0.48, 125.0, 52.0, "日常市集与共享桌点"),
    (0.62, 150.0, 68.0, "学研开放交流点"),
    (0.76, 138.0, 58.0, "青年服务与活动点"),
    (0.91, 120.0, 50.0, "北门户便民服务点"),
)
GREEN_SPINE_HALF_WIDTH_M = 55.0
PUBLIC_SPINE_HALF_WIDTH_M = 18.0
LAND_USE_GREEN_HALF_WIDTH_M = 85.0
DAILY_PUBLIC_BAND_HALF_WIDTH_M = 260.0
COST_SCREEN_INNER_M = 90.0
COST_SCREEN_OUTER_M = 260.0
PHASE_1_HALF_WIDTH_M = 110.0
PHASE_2_HALF_WIDTH_M = 320.0
OSM_RESIDENTIAL_TAG = ("landuse", "residential")
OSM_EXPECTED_TIMESTAMP = "2026-05-06T03:25:00Z"

KEY_AREA_OFFICIAL_SQM = {
    "PROV-KEY-001": 1_921_000,
    "PROV-KEY-002": 1_043_000,
    "PROV-KEY-003": 720_000,
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    payload = json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload.encode("utf-8"))


def metric_geometry(geojson_geometry: dict[str, Any]) -> Any:
    return transform(TO_METRIC.transform, shape(geojson_geometry))


def _polygon_parts(geometry: Any) -> list[Polygon]:
    if geometry.is_empty:
        return []
    if isinstance(geometry, Polygon):
        return [geometry]
    if isinstance(geometry, MultiPolygon):
        return list(geometry.geoms)
    if isinstance(geometry, GeometryCollection):
        parts: list[Polygon] = []
        for item in geometry.geoms:
            parts.extend(_polygon_parts(item))
        return parts
    return []


def polygonal(geometry: Any) -> Polygon | MultiPolygon:
    if not geometry.is_valid:
        geometry = geometry.buffer(0)
    parts = [part for part in _polygon_parts(geometry) if part.area > 0.01]
    if not parts:
        raise ValueError("expected non-empty polygonal geometry")
    normalized = [orient(part, sign=1.0) for part in parts]
    normalized.sort(key=lambda part: (-round(part.area, 6), round(part.centroid.x, 6), round(part.centroid.y, 6)))
    return normalized[0] if len(normalized) == 1 else MultiPolygon(normalized)


def _line_parts(geometry: Any) -> list[LineString]:
    if geometry.is_empty:
        return []
    if isinstance(geometry, LineString):
        return [geometry]
    if isinstance(geometry, MultiLineString):
        return list(geometry.geoms)
    if isinstance(geometry, GeometryCollection):
        parts: list[LineString] = []
        for item in geometry.geoms:
            parts.extend(_line_parts(item))
        return parts
    return []


def linear(geometry: Any) -> LineString | MultiLineString:
    parts = [part for part in _line_parts(geometry) if part.length > 0.01]
    if not parts:
        raise ValueError("expected non-empty linear geometry")
    normalized: list[LineString] = []
    for part in parts:
        coords = list(part.coords)
        if coords[-1] < coords[0]:
            coords.reverse()
        normalized.append(LineString(coords))
    normalized.sort(
        key=lambda part: (
            -round(part.length, 6),
            round(part.bounds[0], 6),
            round(part.bounds[1], 6),
            round(part.bounds[2], 6),
            round(part.bounds[3], 6),
        )
    )
    return normalized[0] if len(normalized) == 1 else MultiLineString(normalized)


def _round_coordinates(value: Any) -> Any:
    if isinstance(value, (tuple, list)):
        if value and all(isinstance(item, (int, float)) for item in value):
            return [round(float(item), COORDINATE_DECIMALS) for item in value]
        return [_round_coordinates(item) for item in value]
    return value


def serialized_geometry(metric_geom: Any) -> dict[str, Any]:
    if metric_geom.geom_type in {"Polygon", "MultiPolygon"}:
        clean = polygonal(metric_geom)
    elif metric_geom.geom_type in {"LineString", "MultiLineString"}:
        clean = linear(metric_geom)
    else:
        clean = metric_geom
    wgs_geom = transform(TO_WGS84.transform, clean)
    result = mapping(wgs_geom)
    rounded = {"type": result["type"], "coordinates": _round_coordinates(result["coordinates"])}
    rounded_shape = shape(rounded)
    if rounded_shape.geom_type in {"Polygon", "MultiPolygon"} and not rounded_shape.is_valid:
        rounded_metric = transform(TO_METRIC.transform, rounded_shape)
        repaired_metric = polygonal(rounded_metric.buffer(0))
        repaired_mapping = mapping(transform(TO_WGS84.transform, repaired_metric))
        rounded = {
            "type": repaired_mapping["type"],
            "coordinates": _round_coordinates(repaired_mapping["coordinates"]),
        }
    if not shape(rounded).is_valid:
        raise ValueError("serialized geometry is invalid after deterministic repair")
    return rounded


def make_feature(
    feature_id: str,
    metric_geom: Any,
    properties: dict[str, Any],
    *,
    declared_area_override: float | int | None = None,
) -> dict[str, Any]:
    try:
        geometry = serialized_geometry(metric_geom)
    except ValueError as exc:
        raise ValueError(f"{feature_id}: {exc}") from exc
    props = copy.deepcopy(properties)
    props["id"] = feature_id
    serialized_metric_geom = metric_geometry(geometry)
    if serialized_metric_geom.geom_type in {"Polygon", "MultiPolygon"}:
        props["area_sqm_declared"] = (
            declared_area_override
            if declared_area_override is not None
            else round(float(serialized_metric_geom.area), 3)
        )
    return {
        "type": "Feature",
        "id": feature_id,
        "properties": props,
        "geometry": geometry,
    }


def collection(name: str, features: list[dict[str, Any]]) -> dict[str, Any]:
    return {"type": "FeatureCollection", "name": name, "features": features}


def horizontal_section(site: Any, y: float) -> LineString:
    minx, _miny, maxx, _maxy = site.bounds
    probe = LineString([(minx - 2000.0, y), (maxx + 2000.0, y)])
    parts = _line_parts(site.intersection(probe))
    if not parts:
        raise ValueError(f"site has no horizontal section at y={y}")
    parts.sort(key=lambda item: (-round(item.length, 6), round(item.bounds[0], 6)))
    return parts[0]


def normalized_site_point(site: Any, y_fraction: float, x_fraction: float) -> tuple[float, float]:
    _minx, miny, _maxx, maxy = site.bounds
    y = miny + (maxy - miny) * y_fraction
    section = horizontal_section(site, y)
    left = min(point[0] for point in section.coords)
    right = max(point[0] for point in section.coords)
    return (left + (right - left) * x_fraction, y)


def build_spine(site: Any) -> LineString:
    points = [
        normalized_site_point(site, y_fraction, x_fraction)
        for y_fraction, x_fraction in zip(SPINE_Y_FRACTIONS, SPINE_X_FRACTIONS, strict=True)
    ]
    spine = LineString(points)
    if not site.buffer(0.01).contains(spine):
        raise ValueError("generated daily-public-belt spine left the provisional design boundary")
    return spine


def build_boundary_layers(boundary_data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], Any]:
    by_id = {feature["id"]: feature for feature in boundary_data["features"]}
    source_site = by_id["PROV-SITE-001"]
    site_metric = metric_geometry(source_site["geometry"])
    site_props = copy.deepcopy(source_site["properties"])
    site_props["source_feature_id"] = "PROV-SITE-001"
    site_props["generation_note"] = "保留仓库 provisional 边界几何；本阶段未作线位或红线调整。"
    site = collection(
        "site_boundary_provisional_preserved",
        [make_feature("SITE-001", site_metric, site_props)],
    )

    key_features: list[dict[str, Any]] = []
    for source_id in ("PROV-KEY-001", "PROV-KEY-002", "PROV-KEY-003"):
        source = by_id[source_id]
        props = copy.deepcopy(source["properties"])
        props["official_area_reference_sqm"] = KEY_AREA_OFFICIAL_SQM[source_id]
        props["area_basis"] = "ranges/planning_limits.json official announced value; not provisional rectangle measurement"
        key_features.append(
            make_feature(
                source_id,
                metric_geometry(source["geometry"]),
                props,
                declared_area_override=KEY_AREA_OFFICIAL_SQM[source_id],
            )
        )
    keys = collection("key_areas_provisional_geometry_official_area_references", key_features)
    return site, keys, site_metric


def build_green_space(site: Any, spine: LineString) -> dict[str, Any]:
    base = polygonal(site.intersection(spine.buffer(GREEN_SPINE_HALF_WIDTH_M, resolution=4, cap_style=2, join_style=2)))
    features = [
        make_feature(
            "GREEN-001",
            base,
            {
                "layer": "GREEN_SPACE",
                "source_type": "agent_generated_design",
                "confidence": "medium",
                "geometry_role": "design_proposal",
                "land_use_code": "1401",
                "name_zh": "日常公共带连续绿脊（概念建议）",
                "shape_basis": f"submitted provisional overall-design polygon clipped by a {GREEN_SPINE_HALF_WIDTH_M:g} m half-width design buffer",
                "design_status": "concept_reference_for_professional_development",
                "statutory_status": "none",
            },
        )
    ]
    used = base
    for index, (fraction, green_radius, _public_radius, label) in enumerate(NODE_SPECS, start=2):
        node = spine.interpolate(fraction, normalized=True)
        candidate = node.buffer(green_radius, resolution=8).intersection(site).difference(used)
        if candidate.is_empty or candidate.area <= 1.0:
            raise ValueError(f"green node {index} collapsed")
        candidate = polygonal(candidate)
        features.append(
            make_feature(
                f"GREEN-{index:03d}",
                candidate,
                {
                    "layer": "GREEN_SPACE",
                    "source_type": "agent_generated_design",
                    "confidence": "medium",
                    "geometry_role": "design_proposal",
                    "land_use_code": "1401",
                    "name_zh": f"{label}树荫口袋（概念建议）",
                    "node_fraction_from_south": fraction,
                    "design_radius_m": green_radius,
                    "shape_basis": "fixed node on deterministic daily-public-belt spine; overlap with earlier green features removed",
                    "design_status": "concept_reference_for_professional_development",
                    "statutory_status": "none",
                },
            )
        )
        used = unary_union([used, candidate])
    return collection("daily_public_belt_green_space_design", features)


def build_public_space(site: Any, spine: LineString) -> dict[str, Any]:
    base = polygonal(site.intersection(spine.buffer(PUBLIC_SPINE_HALF_WIDTH_M, resolution=4, cap_style=2, join_style=2)))
    features = [
        make_feature(
            "PUBLIC-001",
            base,
            {
                "layer": "PUBLIC_SPACE",
                "source_type": "agent_generated_design",
                "confidence": "medium",
                "geometry_role": "design_proposal",
                "name_zh": "全时可达日常公共带（概念建议）",
                "beneficiary_groups_proposed": ["沿线居民", "通勤者", "学研与创新从业者", "访客"],
                "operation_principle": "daily access before event programming; human-reviewed operating rules",
                "shape_basis": f"submitted provisional overall-design polygon clipped by a {PUBLIC_SPINE_HALF_WIDTH_M:g} m half-width design buffer",
                "statutory_status": "none",
            },
        )
    ]
    used = base
    for index, (fraction, _green_radius, public_radius, label) in enumerate(NODE_SPECS, start=2):
        node = spine.interpolate(fraction, normalized=True)
        candidate = node.buffer(public_radius, resolution=8).intersection(site).difference(used)
        if candidate.is_empty or candidate.area <= 1.0:
            raise ValueError(f"public node {index} collapsed")
        candidate = polygonal(candidate)
        features.append(
            make_feature(
                f"PUBLIC-{index:03d}",
                candidate,
                {
                    "layer": "PUBLIC_SPACE",
                    "source_type": "agent_generated_design",
                    "confidence": "medium",
                    "geometry_role": "design_proposal",
                    "name_zh": f"{label}（概念建议）",
                    "beneficiary_groups_proposed": ["沿线居民", "日常通行人群", "开放活动参与者"],
                    "node_fraction_from_south": fraction,
                    "design_radius_m": public_radius,
                    "shape_basis": "fixed node on deterministic daily-public-belt spine; overlap with earlier public features removed",
                    "operation_principle": "free daily use is the baseline; commercial events require separate review",
                    "statutory_status": "none",
                },
            )
        )
        used = unary_union([used, candidate])
    return collection("daily_public_belt_public_space_design", features)


def west_of_spine_mask(site: Any, spine: LineString) -> Polygon:
    minx, miny, _maxx, maxy = site.bounds
    far_left = minx - 2000.0
    spine_coords = list(spine.coords)
    coordinates = [
        (far_left, miny - 2000.0),
        (far_left, maxy + 2000.0),
        (spine_coords[-1][0], maxy + 2000.0),
        *reversed(spine_coords),
        (spine_coords[0][0], miny - 2000.0),
        (far_left, miny - 2000.0),
    ]
    mask = Polygon(coordinates)
    if not mask.is_valid:
        raise ValueError("west-of-spine partition mask is invalid")
    return mask


def build_land_use(site: Any, spine: LineString) -> dict[str, Any]:
    green = polygonal(site.intersection(spine.buffer(LAND_USE_GREEN_HALF_WIDTH_M, resolution=8, cap_style=1, join_style=2)))
    daily = polygonal(
        site.intersection(spine.buffer(DAILY_PUBLIC_BAND_HALF_WIDTH_M, resolution=8, cap_style=1, join_style=2)).difference(green)
    )
    outer = polygonal(site.difference(unary_union([green, daily])))
    west = polygonal(outer.intersection(west_of_spine_mask(site, spine)))
    east = polygonal(outer.difference(west))

    minx, miny, maxx, maxy = site.bounds
    south_cut = miny + (maxy - miny) * 0.27
    north_cut = miny + (maxy - miny) * 0.69
    margin = 2000.0
    south = polygonal(east.intersection(box(minx - margin, miny - margin, maxx + margin, south_cut)))
    middle = polygonal(east.intersection(box(minx - margin, south_cut, maxx + margin, north_cut)))
    north = polygonal(east.intersection(box(minx - margin, north_cut, maxx + margin, maxy + margin)))

    specs = (
        (
            "LU-001", green, "1401", "日常公共带绿地核心（概念分区）",
            "85 m half-width green core around the deterministic public-belt spine",
        ),
        (
            "LU-002", daily, "0702", "日常社区服务界面带（概念分区）",
            "260 m public-service band minus the green core",
        ),
        (
            "LU-003", west, "0701", "居住兼容更新区（概念分区，现状用途待核）",
            "west outer wing after removing the public-service band; not an existing-use finding",
        ),
        (
            "LU-004", south, "05", "南段商业服务兼容区（概念分区）",
            "east outer wing south of normalized y=0.27",
        ),
        (
            "LU-005", middle, "0802", "中段科研开放兼容区（概念分区）",
            "east outer wing between normalized y=0.27 and y=0.69",
        ),
        (
            "LU-006", north, "0804", "北段教育共享兼容区（概念分区）",
            "remaining east outer wing north of normalized y=0.69",
        ),
    )
    features = []
    for feature_id, geom, code, name, basis in specs:
        features.append(
            make_feature(
                feature_id,
                geom,
                {
                    "layer": "LAND_USE",
                    "source_type": "agent_generated_design",
                    "confidence": "low",
                    "geometry_role": "design_proposal",
                    "land_use_code": code,
                    "name_zh": name,
                    "shape_basis": basis,
                    "existing_condition_status": "unknown_requires_official_land_use_and_field_verification",
                    "statutory_status": "concept_only_not_regulatory_plan",
                },
            )
        )
    return collection("daily_public_belt_land_use_partition", features)


def spine_tangent(spine: LineString, fraction: float) -> tuple[float, float, float]:
    before = spine.interpolate(max(0.0, fraction - 0.004), normalized=True)
    after = spine.interpolate(min(1.0, fraction + 0.004), normalized=True)
    dx = after.x - before.x
    dy = after.y - before.y
    length = math.hypot(dx, dy)
    if length == 0:
        raise ValueError("zero-length spine tangent")
    dx /= length
    dy /= length
    angle = math.degrees(math.atan2(dy, dx))
    return dx, dy, angle


def build_buildings(site: Any, spine: LineString) -> dict[str, Any]:
    module_types = (
        ("community_service", "社区服务小站"),
        ("cultural", "公共文化小站"),
        ("retail", "便民业态小站"),
        ("mobility_hub", "慢行服务小站"),
        ("incubator", "开放创新小站"),
    )
    features: list[dict[str, Any]] = []
    sequence = 1
    for node_index, (fraction, _green_radius, _public_radius, node_label) in enumerate(NODE_SPECS):
        point = spine.interpolate(fraction, normalized=True)
        dx, dy, angle = spine_tangent(spine, fraction)
        nx, ny = -dy, dx
        for side in (-1, 1):
            offset = 142.0 + (node_index % 3) * 18.0
            center_x = point.x + nx * side * offset
            center_y = point.y + ny * side * offset
            long_side = 38.0 + (node_index % 2) * 8.0
            short_side = 22.0 + ((node_index + (1 if side > 0 else 0)) % 3) * 4.0
            footprint = box(
                center_x - long_side / 2,
                center_y - short_side / 2,
                center_x + long_side / 2,
                center_y + short_side / 2,
            )
            footprint = affinity.rotate(footprint, angle, origin=(center_x, center_y), use_radians=False)
            footprint = footprint.intersection(site.buffer(-5.0))
            if footprint.is_empty or footprint.area < 100.0:
                raise ValueError(f"building module {sequence} left the usable design envelope")
            building_type, module_name = module_types[(sequence - 1) % len(module_types)]
            feature_id = f"BLDG-{sequence:03d}"
            features.append(
                make_feature(
                    feature_id,
                    polygonal(footprint),
                    {
                        "layer": "BUILDING_FOOTPRINT",
                        "source_type": "agent_generated_design",
                        "confidence": "low",
                        "geometry_role": "design_proposal",
                        "building_type": building_type,
                        "name_zh": f"{node_label}·{module_name}（概念建议）",
                        "shape_basis": f"fixed module {long_side:g} m x {short_side:g} m, offset {offset:g} m from deterministic public-belt node",
                        "building_height_m": None,
                        "floor_area_ratio": None,
                        "existing_building_status": "unknown",
                        "implementation_note": "footprint is a transferable concept module, not a demolition/new-build decision",
                    },
                )
            )
            sequence += 1
    return collection("daily_public_belt_concept_building_modules", features)


def build_roads(site: Any, spine: LineString) -> dict[str, Any]:
    usable = site.buffer(-10.0)
    line_specs: list[tuple[str, Any, str, str, str]] = [
        ("ROAD-001", spine.intersection(usable), "greenway", "日常公共带慢行主脊（概念建议）", "deterministic normalized site spine"),
        ("ROAD-002", spine.parallel_offset(20.0, "left", resolution=4, join_style=2).intersection(usable), "cycleway", "自行车连续通道（概念建议）", "20 m design offset left of spine; not a road redline"),
        ("ROAD-003", spine.parallel_offset(20.0, "right", resolution=4, join_style=2).intersection(usable), "pedestrian", "无障碍步行连续通道（概念建议）", "20 m design offset right of spine; not a road redline"),
    ]
    connector_fractions = (0.19, 0.33, 0.48, 0.62, 0.76, 0.91)
    for index, fraction in enumerate(connector_fractions, start=4):
        _minx, miny, _maxx, maxy = site.bounds
        y = miny + (maxy - miny) * fraction
        section = horizontal_section(site, y)
        left = min(point[0] for point in section.coords)
        right = max(point[0] for point in section.coords)
        start = (left + (right - left) * 0.08, y)
        end = (left + (right - left) * 0.92, y)
        connector = LineString([start, end]).intersection(usable)
        line_specs.append(
            (
                f"ROAD-{index:03d}",
                connector,
                "pedestrian" if index % 2 == 0 else "transit_connection",
                f"东西日常缝合联络 {index - 3}（概念建议）",
                f"normalized y={fraction}; connects 8% to 92% of the provisional cross-section",
            )
        )
    features = []
    for feature_id, geom, road_class, name, basis in line_specs:
        features.append(
            make_feature(
                feature_id,
                linear(geom),
                {
                    "layer": "ROAD_CENTERLINE",
                    "source_type": "agent_generated_design",
                    "confidence": "low",
                    "geometry_role": "design_proposal",
                    "road_class": road_class,
                    "name_zh": name,
                    "shape_basis": basis,
                    "engineering_status": "concept_alignment_only_no_redline_or_feasibility_conclusion",
                    "cost_duty": "crossing design and construction impact require separate professional and public review",
                },
            )
        )
    return collection("daily_public_belt_slow_mobility_concept", features)


def build_phasing(site: Any, spine: LineString) -> dict[str, Any]:
    phase_1 = polygonal(site.intersection(spine.buffer(PHASE_1_HALF_WIDTH_M, resolution=8, cap_style=1, join_style=2)))
    phase_2_envelope = site.intersection(spine.buffer(PHASE_2_HALF_WIDTH_M, resolution=8, cap_style=1, join_style=2))
    phase_2 = polygonal(phase_2_envelope.difference(phase_1))
    phase_3 = polygonal(site.difference(unary_union([phase_1, phase_2])))
    specs = (
        (
            "PHASE-001", phase_1, "phase_1", "先行：日常公共带与基线调研",
            "complete interface inventory, accessibility audit, and public-space operating charter before construction design",
            "proposed corridor operating entity plus district/community co-review; subject to agreement",
        ),
        (
            "PHASE-002", phase_2, "phase_2", "联动：界面减扰与服务补偿",
            "verify each screened residential interface and bind mitigation actions, complaint route, owner, and deadline",
            "project implementation entity funds mitigation; community and affected users verify closure",
        ),
        (
            "PHASE-003", phase_3, "phase_3", "待核：外翼合作与用地深化",
            "start only after official land use, ownership, statutory controls, and engineering constraints are supplied",
            "professional planning team and competent authorities; no commitment is asserted here",
        ),
    )
    features = [
        make_feature(
            feature_id,
            geom,
            {
                "layer": "PHASE",
                "source_type": "agent_generated_design",
                "confidence": "low",
                "geometry_role": "design_proposal",
                "phase": phase,
                "name_zh": name,
                "entry_gate": gate,
                "responsibility_proposal": responsibility,
                "approval_status": "concept_only_not_approved_schedule",
            },
        )
        for feature_id, geom, phase, name, gate, responsibility in specs
    ]
    return collection("benefit_cost_responsibility_phasing", features)


def osm_polygon(element: dict[str, Any]) -> Polygon | MultiPolygon | None:
    geometry = element.get("geometry")
    if not isinstance(geometry, list) or len(geometry) < 4:
        return None
    coordinates = [(float(point["lon"]), float(point["lat"])) for point in geometry]
    if coordinates[0] != coordinates[-1]:
        return None
    candidate = Polygon(coordinates)
    if not candidate.is_valid:
        candidate = candidate.buffer(0)
    if candidate.is_empty or candidate.geom_type not in {"Polygon", "MultiPolygon"}:
        return None
    return candidate


def build_constraints(site: Any, spine: LineString, osm_data: dict[str, Any]) -> dict[str, Any]:
    timestamp = str(osm_data.get("osm3s", {}).get("timestamp_osm_base", ""))
    if timestamp != OSM_EXPECTED_TIMESTAMP:
        raise ValueError(f"OSM snapshot timestamp changed: expected {OSM_EXPECTED_TIMESTAMP}, got {timestamp}")

    outer = site.intersection(spine.buffer(COST_SCREEN_OUTER_M, resolution=8, cap_style=1, join_style=2))
    inner = site.intersection(spine.buffer(COST_SCREEN_INNER_M, resolution=8, cap_style=1, join_style=2))
    cost_zone = polygonal(outer.difference(inner))
    features = [
        make_feature(
            "COST-SCREEN-001",
            cost_zone,
            {
                "layer": "AI_SERVICE_ZONE",
                "source_type": "agent_generated_design",
                "confidence": "low",
                "geometry_role": "analysis_helper",
                "name_zh": "界面成本与责任核查带（设计分析，非现状事实）",
                "shape_basis": f"{COST_SCREEN_INNER_M:g}-{COST_SCREEN_OUTER_M:g} m design annulus around the deterministic daily-public-belt spine, clipped to the provisional overall design area",
                "benefit_cost_test": "every intervention inside this design audit envelope must register beneficiary, affected interface, mitigation action, proposed duty holder, trigger, deadline, and human verification",
                "responsibility_proposal": "corridor operating entity maintains the ledger; project implementer funds verified mitigation; both remain subject to agreement",
                "not_existing_condition": True,
                "not_regulatory_control": True,
            },
        )
    ]

    screening_envelope = outer
    elements = sorted(
        (item for item in osm_data.get("elements", []) if isinstance(item, dict)),
        key=lambda item: (str(item.get("type", "")), int(item.get("id", 0))),
    )
    selected_ids: set[int] = set()
    for element in elements:
        tags = element.get("tags") or {}
        if element.get("type") != "way" or tags.get(OSM_RESIDENTIAL_TAG[0]) != OSM_RESIDENTIAL_TAG[1]:
            continue
        source_polygon = osm_polygon(element)
        if source_polygon is None:
            continue
        metric_polygon = transform(TO_METRIC.transform, source_polygon)
        interface = metric_polygon.boundary.intersection(screening_envelope)
        if interface.is_empty or not _line_parts(interface):
            continue
        osm_id = int(element["id"])
        if osm_id in selected_ids:
            raise ValueError(f"duplicate OSM residential way {osm_id}")
        selected_ids.add(osm_id)
        name = str(tags.get("name") or f"OSM residential way {osm_id}")
        features.append(
            make_feature(
                f"OSM-RES-{osm_id}",
                linear(interface),
                {
                    "layer": "REGULATORY_CONTROL",
                    "source_type": "osm",
                    "confidence": "low",
                    "geometry_role": "analysis_helper",
                    "name_zh": f"待核受影响居住界面线索：{name}",
                    "osm_element_type": "way",
                    "osm_id": osm_id,
                    "osm_tags_used": {"landuse": "residential", "name": tags.get("name")},
                    "osm_data_timestamp": timestamp,
                    "selection_rule": f"OSM landuse=residential boundary intersects the {COST_SCREEN_OUTER_M:g} m design screening envelope; only the intersecting boundary segment is emitted",
                    "analysis_conclusion": "candidate interface for field and official-data verification; not a finding about households, tenure, vulnerability, ownership, or causation",
                    "metric_use": "forbidden: no OSM-derived area, length, ratio, redline, or statutory control is calculated or published",
                    "official_boundary": False,
                    "not_regulatory_control": True,
                    "attribution": "© OpenStreetMap contributors, ODbL 1.0",
                },
            )
        )
    if not selected_ids:
        raise ValueError("OSM screening produced no residential-interface leads")
    return collection("distributional_cost_constraints_and_osm_leads", features)


def collection_union(data: dict[str, Any], *, feature_ids: set[str] | None = None) -> Any:
    geometries = []
    for feature in data["features"]:
        if feature_ids is not None and feature["id"] not in feature_ids:
            continue
        geometries.append(metric_geometry(feature["geometry"]))
    if not geometries:
        raise ValueError("cannot union an empty feature selection")
    return unary_union(geometries)


def metric_known(
    value: int | float,
    unit: str,
    source_files: list[str],
    formula: str,
    confidence: str,
    assumptions: list[str],
) -> dict[str, Any]:
    return {
        "status": "known",
        "value": value,
        "unit": unit,
        "source_files": source_files,
        "formula": formula,
        "confidence": confidence,
        "assumptions": assumptions,
    }


def metric_unknown(
    unit: str,
    source_files: list[str],
    formula: str,
    reason: str,
    needed_from: str,
) -> dict[str, Any]:
    return {
        "status": "unknown",
        "value": None,
        "unit": unit,
        "source_files": source_files,
        "formula": formula,
        "confidence": "unknown",
        "assumptions": [],
        "reason": reason,
        "needed_from": needed_from,
    }


def build_metrics(layers: dict[str, dict[str, Any]], planning_limits: dict[str, Any]) -> dict[str, Any]:
    site_area = round(float(collection_union(layers["site_boundary.geojson"]).area), 3)
    building_area = round(float(collection_union(layers["buildings.geojson"]).area), 3)
    green_area = round(float(collection_union(layers["green_space.geojson"]).area), 3)
    public_area = round(float(collection_union(layers["public_space.geojson"]).area), 3)
    key_features = layers["key_areas.geojson"]["features"]
    if len(key_features) != 3:
        raise ValueError("expected exactly three key-area features")
    for feature in key_features:
        expected = KEY_AREA_OFFICIAL_SQM[feature["id"]]
        if feature["properties"].get("area_sqm_declared") != expected:
            raise ValueError(f"key area {feature['id']} does not use its official declared value")

    denominator_note = (
        f"ratio denominator = overall_design_area ({site_area} sqm = {site_area / 1_000_000:.5f} km², "
        "reported only as about 11.4 km² in narrative display); coordinated_research_area "
        "(about 43.6 km² context) is never used"
    )
    geometry_note = "areas are recomputed in EPSG:4548 from the serialized EPSG:4326 proposal geometry"
    limits = planning_limits["official_planning_controls"]
    metrics = {
        "site_area_sqm": metric_known(
            site_area,
            "sqm",
            ["geometry/site_boundary.geojson"],
            "round(area_EPSG4548(union(feature.id == 'SITE-001')), 3)",
            "medium",
            [
                geometry_note,
                "This is the submitted provisional overall_design_area polygon, not an official redline; narrative display rounds it to about 11.4 km².",
                "The coordinated_research_area (about 43.6 km²) is context only and is not the denominator.",
            ],
        ),
        "building_footprint_area_sqm": metric_known(
            building_area,
            "sqm",
            ["geometry/buildings.geojson"],
            "round(area_EPSG4548(union(all BUILDING_FOOTPRINT features)), 3)",
            "low",
            [geometry_note, "Concept footprints only; no height, storey, floor-area, demolition, or approval claim."],
        ),
        "green_ratio": metric_known(
            round(green_area / site_area, 6),
            "ratio",
            ["geometry/green_space.geojson", "geometry/site_boundary.geojson"],
            "round(area_EPSG4548(union(all GREEN_SPACE features)) / area_EPSG4548(feature.id == 'SITE-001'), 6)",
            "medium",
            [denominator_note, "Numerator is the union area, so overlapping proposal features cannot be double-counted."],
        ),
        "public_space_ratio": metric_known(
            round(public_area / site_area, 6),
            "ratio",
            ["geometry/public_space.geojson", "geometry/site_boundary.geojson"],
            "round(area_EPSG4548(union(all PUBLIC_SPACE features)) / area_EPSG4548(feature.id == 'SITE-001'), 6)",
            "medium",
            [denominator_note, "Numerator is the union area, so overlapping proposal features cannot be double-counted."],
        ),
        "key_area_count": metric_known(
            len(key_features),
            "count",
            ["geometry/key_areas.geojson"],
            "count(features where layer == 'KEY_AREA')",
            "high",
            ["Counts the three named official key-area concepts; their polygons remain provisional."],
        ),
        "ecosystem_case_count": metric_known(
            5,
            "count",
            ["proposal.md", "sources.json"],
            "count(distinct rows in section '五个公开案例：只迁移机制，不移植结论')",
            "high",
            ["Submission-content inventory only; not a claim about the total global ecosystem population."],
        ),
        "scenario_card_count": metric_known(
            12,
            "count",
            ["proposal.md"],
            "count(distinct SC-01...SC-12 rows in section '十二张场景卡')",
            "high",
            ["Concept-card inventory; no card is an approved or deployed service."],
        ),
        "industry_test_scenario_count": metric_known(
            4,
            "count",
            ["proposal.md"],
            "count(scenario cards whose class is INDUSTRY-TEST)",
            "high",
            ["Concept-card inventory; approval, operator, site, capacity, and safety evidence remain unknown."],
        ),
        "persona_count": metric_known(
            8,
            "count",
            ["proposal.md"],
            "count(distinct P-01...P-08 rows in section '八类任务画像')",
            "high",
            ["Task-persona inventory, not a survey result or a count of real people."],
        ),
        "landmark_count": metric_known(
            3,
            "count",
            ["proposal.md"],
            "count(distinct LM-01...LM-03 rows in section '三个朝圣地标概念')",
            "high",
            ["Concept inventory; location, heritage, ownership, engineering, and approval are unconfirmed."],
        ),
        "public_space_component_type_count": metric_known(
            8,
            "count",
            ["proposal.md"],
            "count(distinct C-01...C-08 rows in section '公共空间组件库')",
            "high",
            ["Reusable concept-type inventory, not a constructed-asset count."],
        ),
        "spatial_story_stage_count": metric_known(
            5,
            "count",
            ["proposal.md"],
            "count(distinct 01...05 rows in section '五幕空间故事线')",
            "high",
            ["Submission-content inventory; heritage interpretation and physical placement still require review."],
        ),
        "signage_information_level_count": metric_known(
            4,
            "count",
            ["proposal.md"],
            "count(distinct LINE, NODE, STORY, STATUS information levels)",
            "high",
            ["Concept-system inventory, not a fabricated or installed sign count."],
        ),
        "annual_program_family_count": metric_known(
            4,
            "count",
            ["proposal.md"],
            "count(distinct OP-01...OP-04 rows in section '年度活动体系')",
            "high",
            ["Proposed recurring-program inventory; no event date, funding, venue, or organizer is confirmed."],
        ),
        "floor_area_ratio": metric_unknown(
            "ratio",
            ["brief/site-package/ranges/planning_limits.json"],
            "total_floor_area_sqm / approved_overall_design_area_sqm",
            "The public site package marks floor_area_ratio as missing; concept footprints do not supply floor area.",
            limits["floor_area_ratio"]["needed_from"],
        ),
        "building_height_m": metric_unknown(
            "m",
            ["brief/site-package/ranges/planning_limits.json"],
            "approved_or_surveyed_height_m",
            "The public site package marks building_height_m as missing; no height is inferred from OSM or concept footprints.",
            limits["building_height_m"]["needed_from"],
        ),
        "building_density": metric_unknown(
            "ratio",
            ["brief/site-package/ranges/planning_limits.json"],
            "approved_building_footprint_area_sqm / approved_site_area_sqm",
            "The public site package marks the statutory building-density control as missing; concept-module density is not substituted.",
            limits["building_density"]["needed_from"],
        ),
        "statutory_green_ratio": metric_unknown(
            "ratio",
            ["brief/site-package/ranges/planning_limits.json"],
            "approved_green_area_sqm / approved_site_area_sqm",
            "The public site package marks the statutory green ratio as missing; green_ratio above is only a recomputed design-proposal ratio.",
            limits["green_ratio"]["needed_from"],
        ),
        "setback_m": metric_unknown(
            "m",
            ["brief/site-package/ranges/planning_limits.json"],
            "approved_building_control_line_distance",
            "The public site package marks setbacks as missing; no road-redline or fire-control inference is made.",
            limits["setback_m"]["needed_from"],
        ),
        "affected_household_count": metric_unknown(
            "count",
            ["geometry/constraints.geojson"],
            "verified_households_intersecting_professionally_confirmed_impact_area",
            "OSM interface leads cannot establish households, occupancy, tenure, vulnerability, or causation.",
            "field survey, consented/cleared household data, official address/building data, and a professionally confirmed impact method",
        ),
        "mitigation_budget_cny": metric_unknown(
            "CNY",
            ["geometry/constraints.geojson", "geometry/phasing.geojson"],
            "sum(verified_action_quantity * reviewed_unit_cost)",
            "No verified action quantities, unit costs, compensation rules, funding commitment, or responsible-party agreement is available.",
            "verified mitigation ledger, reviewed unit rates, affected-party process, funding agreement, and human approval",
        ),
        "ecosystem_partner_count": metric_unknown(
            "count",
            ["proposal.md"],
            "count(organizations with cleared identity, signed role, effective term, and disclosure permission)",
            "No cleared project partner roster or signed participation record is available.",
            "cleared organization registry, signed role/term records, and publication permission",
        ),
        "compute_capacity": metric_unknown(
            "compute_unit",
            ["proposal.md"],
            "sum(available capacity under one disclosed unit, time window, service level, and access rule)",
            "No provider-neutral capacity inventory, service window, allocation rule, or energy/cost record is available.",
            "cleared compute inventory, common unit, service-level window, access policy, cost and energy records",
        ),
        "service_use_ratio": metric_unknown(
            "ratio",
            ["proposal.md"],
            "deduplicated_eligible_use_events / verified_serviceable_population_in_same_window",
            "No cleared event log or verified serviceable-population denominator exists.",
            "privacy-reviewed aggregate event log, service-open record, population denominator, exclusions, and audit signature",
        ),
        "approved_scenario_count": metric_unknown(
            "count",
            ["proposal.md"],
            "count(concept scenarios with site, operator, safety, privacy, accessibility, and human-review approvals all effective)",
            "The package contains concept cards only and no approval record.",
            "site and operator confirmations plus safety, privacy, accessibility, and human-review approvals",
        ),
        "annual_participant_count": metric_unknown(
            "count",
            ["proposal.md"],
            "deduplicated_opt_in_participants_within_declared_program_year",
            "No event schedule, registration system, privacy notice, or attendance log exists.",
            "approved annual schedule, opt-in registration rules, privacy notice, deduplication method, and attendance log",
        ),
        "developer_to_pilot_conversion_ratio": metric_unknown(
            "ratio",
            ["proposal.md"],
            "developers_entering_human_approved_pilot / eligible_opt_in_developers_in_same_cohort_window",
            "No eligible cohort, approved pilot ledger, or common observation window exists.",
            "opt-in cohort registry, eligibility rule, approved pilot ledger, observation window, and independent audit",
        ),
    }
    return {
        "schema_version": "0.1.0",
        "units": {"length": "m", "area": "sqm"},
        "metrics": metrics,
    }


def validate_layer_contracts(layers: dict[str, dict[str, Any]]) -> None:
    expected_names = {
        "site_boundary.geojson",
        "key_areas.geojson",
        "land_use.geojson",
        "buildings.geojson",
        "roads.geojson",
        "green_space.geojson",
        "public_space.geojson",
        "constraints.geojson",
        "phasing.geojson",
    }
    if set(layers) != expected_names:
        raise ValueError(f"generated layer set mismatch: {sorted(layers)}")
    seen: set[str] = set()
    for filename in sorted(layers):
        data = layers[filename]
        if data.get("type") != "FeatureCollection" or not data.get("features"):
            raise ValueError(f"{filename} must be a non-empty FeatureCollection")
        for feature in data["features"]:
            feature_id = feature.get("id")
            props = feature.get("properties", {})
            if not feature_id or feature_id in seen:
                raise ValueError(f"missing or duplicate feature id {feature_id!r}")
            seen.add(feature_id)
            for field in ("id", "layer", "source_type", "confidence", "geometry_role"):
                if not props.get(field):
                    raise ValueError(f"{filename} {feature_id}: missing {field}")
            geom_type = feature["geometry"]["type"]
            if geom_type in {"Polygon", "MultiPolygon"} and not isinstance(props.get("area_sqm_declared"), (int, float)):
                raise ValueError(f"{filename} {feature_id}: polygon lacks numeric area_sqm_declared")
            if props.get("source_type") == "osm":
                if props.get("geometry_role") not in {"existing_condition", "analysis_helper"}:
                    raise ValueError(f"{filename} {feature_id}: invalid OSM geometry role")
                if props.get("geometry_role") == "official_constraint" or props.get("official_boundary") is True:
                    raise ValueError(f"{filename} {feature_id}: OSM promoted to official constraint")
                if props.get("area_sqm_declared") is not None:
                    raise ValueError(f"{filename} {feature_id}: OSM entered an area declaration")


def update_manifest_hashes(submission_dir: Path) -> None:
    manifest_path = submission_dir / "manifest.json"
    manifest = read_json(manifest_path)
    for item in manifest.get("files", []):
        relative = item.get("path")
        if not relative or relative == "manifest.json":
            continue
        target = submission_dir / relative
        if target.is_file():
            item["sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
    write_json(manifest_path, manifest)


def build(submission_dir: Path) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    bundled_inputs = read_json(INPUT_BUNDLE)
    boundary_data = bundled_inputs["provisional_boundaries"]
    planning_limits = bundled_inputs["planning_limits"]
    osm_data = bundled_inputs["osm_corridor"]
    site_layer, key_layer, site_metric = build_boundary_layers(boundary_data)
    spine = build_spine(site_metric)
    layers = {
        "site_boundary.geojson": site_layer,
        "key_areas.geojson": key_layer,
        "land_use.geojson": build_land_use(site_metric, spine),
        "buildings.geojson": build_buildings(site_metric, spine),
        "roads.geojson": build_roads(site_metric, spine),
        "green_space.geojson": build_green_space(site_metric, spine),
        "public_space.geojson": build_public_space(site_metric, spine),
        "constraints.geojson": build_constraints(site_metric, spine, osm_data),
        "phasing.geojson": build_phasing(site_metric, spine),
    }
    validate_layer_contracts(layers)
    metrics = build_metrics(layers, planning_limits)
    for filename in sorted(layers):
        write_json(submission_dir / "geometry" / filename, layers[filename])
    write_json(submission_dir / "metrics.json", metrics)
    update_manifest_hashes(submission_dir)
    return layers, metrics


def print_summary(layers: dict[str, dict[str, Any]], metrics: dict[str, Any]) -> None:
    print("阶段 2 几何生成完成（确定性参数，无随机选择）")
    for filename in sorted(layers):
        print(f"- geometry/{filename}: {len(layers[filename]['features'])} features")
    known = metrics["metrics"]
    print(f"- site_area_sqm: {known['site_area_sqm']['value']}")
    print(f"- green_ratio: {known['green_ratio']['value']}")
    print(f"- public_space_ratio: {known['public_space_ratio']['value']}")
    osm_count = sum(
        feature["properties"].get("source_type") == "osm"
        for feature in layers["constraints.geojson"]["features"]
    )
    print(f"- OSM 居住界面待核线索: {osm_count} features（0 个进入面积/比率公式）")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--submission-dir",
        type=Path,
        default=DEFAULT_SUBMISSION,
        help="target submission package",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    submission_dir = args.submission_dir.resolve()
    layers, metrics = build(submission_dir)
    print_summary(layers, metrics)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
