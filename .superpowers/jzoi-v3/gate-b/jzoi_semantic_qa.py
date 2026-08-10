import hashlib
import json
from collections import Counter, defaultdict, deque
from pathlib import Path

from shapely.geometry import shape
from shapely.ops import unary_union


ROOT = Path(__file__).resolve().parent
CHECK_NAMES = [
    "geometry_validity",
    "scope_containment",
    "feature_id_uniqueness",
    "host_reference_existence",
    "project_geometry_consistency",
    "scenario_host_consistency",
    "road_building_collision",
    "public_path_continuity",
    "main_if_continuity",
    "parallel_human_continuity",
    "land_use_building_compatibility",
    "green_space_semantic_class",
    "key_area_object_containment",
    "duplicate_contradictory_geometry",
    "loop_cycle_naming_semantics",
    "provisional_background_design_separation",
]


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def repo_paths(root):
    root = Path(root)
    repo = root.parents[2]
    gate_a = root.parent
    return repo, gate_a


def load_generated(root=ROOT):
    root = Path(root)
    model = read_json(root / "gate_b_spatial_model.json")
    layers = {
        path.stem: read_json(path)
        for path in sorted((root / "spatial").glob("*.geojson"), key=lambda item: item.name)
    }
    return model, layers


def rounded_point(coordinate):
    return tuple(round(value, 8) for value in coordinate[:2])


def line_network_connected(features):
    adjacency = defaultdict(set)
    for item in features:
        geometry = item.get("geometry")
        if not geometry or geometry["type"] != "LineString":
            return False
        start = rounded_point(geometry["coordinates"][0])
        end = rounded_point(geometry["coordinates"][-1])
        adjacency[start].add(end)
        adjacency[end].add(start)
    if not adjacency:
        return False
    visited = set()
    queue = deque([next(iter(adjacency))])
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        queue.extend(adjacency[node] - visited)
    return visited == set(adjacency)


def geometry_hash(geometry):
    return hashlib.sha256(
        json.dumps(geometry, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()


def audit_layers(layers, model, root=ROOT):
    root = Path(root)
    repo, gate_a = repo_paths(root)
    blockers = []
    warnings = []

    def block(check, code, message, feature_id=None, related_ids=None):
        item = {"check": check, "code": code, "message": message}
        if feature_id:
            item["feature_id"] = feature_id
        if related_ids:
            item["related_ids"] = related_ids
        blockers.append(item)

    all_items = [
        (layer_name, item)
        for layer_name, layer in layers.items()
        for item in layer.get("features", [])
    ]
    all_ids = [item.get("id") for _, item in all_items]
    feature_by_id = {item.get("id"): item for _, item in all_items}

    for layer_name, item in all_items:
        geometry = item.get("geometry")
        if geometry is None:
            if item.get("properties", {}).get("geometry_role") != "unresolved_context":
                block(
                    "geometry_validity",
                    "unexpected_null_geometry",
                    "Only unresolved context may use null geometry.",
                    item.get("id"),
                )
            continue
        try:
            value = shape(geometry)
            if value.is_empty or not value.is_valid:
                block(
                    "geometry_validity",
                    "invalid_geometry",
                    "Geometry is empty or invalid.",
                    item.get("id"),
                )
        except Exception as error:
            block(
                "geometry_validity",
                "unreadable_geometry",
                f"Geometry cannot be parsed: {error}",
                item.get("id"),
            )

    duplicates = {feature_id for feature_id, count in Counter(all_ids).items() if count > 1}
    for feature_id in sorted(duplicates):
        block(
            "feature_id_uniqueness",
            "duplicate_feature_id",
            "Feature ID appears more than once across generated layers.",
            feature_id,
        )

    scopes = read_json(gate_a / "scope_registry.json")
    valid_scopes = {item["scope_id"] for item in scopes["scopes"]}
    for _, item in all_items:
        props = item.get("properties", {})
        if props.get("host_scope") not in valid_scopes:
            block(
                "host_reference_existence",
                "unknown_host_scope",
                "Feature host scope does not resolve to the frozen scope registry.",
                item.get("id"),
            )
        for host_ref in props.get("host_refs", []):
            if host_ref not in valid_scopes:
                block(
                    "host_reference_existence",
                    "unknown_project_host",
                    "Project host reference does not resolve to the frozen scope registry.",
                    item.get("id"),
                    [host_ref],
                )

    boundary_file = read_json(
        repo / "brief" / "site-package" / "geometry" / "provisional_boundaries.geojson"
    )
    boundaries = {item["id"]: shape(item["geometry"]) for item in boundary_file["features"]}
    scope_geometries = {
        "RESEARCH-SCOPE-001": boundaries["PROV-RESEARCH-001"],
        "OVERALL-DESIGN-001": boundaries["PROV-SITE-001"],
        "KEY-AREA-SCOPE-ZZY": boundaries["PROV-KEY-001"],
        "KEY-AREA-SCOPE-ORG": boundaries["PROV-KEY-002"],
        "KEY-AREA-SCOPE-DZS": boundaries["PROV-KEY-003"],
    }
    for layer_name, item in all_items:
        props = item.get("properties", {})
        geometry = item.get("geometry")
        if (
            geometry is None
            or props.get("design_status") != "concept"
            or props.get("containment_applicable") is False
            or layer_name == "regional_ecosystem"
        ):
            continue
        scope = scope_geometries.get(props.get("host_scope"))
        if scope is not None and not scope.covers(shape(geometry)):
            block(
                "scope_containment",
                "design_outside_host_scope",
                "Concept geometry is outside its applicable host scope.",
                item.get("id"),
            )

    for endpoint, layer_name, boundary_id in [
        ("ZZY", "zzy_plan", "PROV-KEY-001"),
        ("ORG", "org_plan", "PROV-KEY-002"),
        ("DZS", "dzs_plan", "PROV-KEY-003"),
    ]:
        boundary = boundaries[boundary_id]
        for item in layers.get(layer_name, {}).get("features", []):
            if item.get("geometry") is not None and not boundary.covers(shape(item["geometry"])):
                block(
                    "key_area_object_containment",
                    "key_area_object_outside_provisional_scope",
                    f"{endpoint} physical object is outside its unchanged provisional study polygon.",
                    item.get("id"),
                )

    projects = layers.get("project_spatial_basis", {}).get("features", [])
    project_ids = []
    for item in projects:
        props = item.get("properties", {})
        project_ids.append(props.get("project_id"))
        if not item.get("geometry") or not props.get("feature_refs"):
            block(
                "project_geometry_consistency",
                "project_missing_spatial_basis",
                "Project requires geometry and one or more feature references.",
                item.get("id"),
            )
        missing = [reference for reference in props.get("feature_refs", []) if reference not in feature_by_id]
        if missing:
            block(
                "project_geometry_consistency",
                "project_feature_reference_missing",
                "Project references generated features that do not exist.",
                item.get("id"),
                missing,
            )
    expected_projects = {f"JZOI-P{index:02d}" for index in range(1, 13)}
    if set(project_ids) != expected_projects or len(project_ids) != 12:
        block(
            "project_geometry_consistency",
            "project_set_incomplete",
            "Project spatial basis must contain exactly JZOI-P01 through JZOI-P12.",
        )

    scenario_hosts = {
        "ZZY": {f"SC-{index:02d}" for index in range(1, 5)},
        "ORG": {f"SC-{index:02d}" for index in range(5, 9)},
        "DZS": {f"SC-{index:02d}" for index in range(9, 13)},
    }
    for _, item in all_items:
        props = item.get("properties", {})
        endpoint = props.get("endpoint")
        scenarios = set(props.get("scenario_refs", []))
        if endpoint in scenario_hosts and scenarios and not scenarios <= scenario_hosts[endpoint]:
            block(
                "scenario_host_consistency",
                "scenario_endpoint_mismatch",
                "Endpoint feature references a scenario hosted by another endpoint.",
                item.get("id"),
                sorted(scenarios - scenario_hosts[endpoint]),
            )

    massing = layers.get("massing", {}).get("features", [])
    building_shapes = [(item["id"], shape(item["geometry"])) for item in massing]
    mobility = layers.get("mobility", {}).get("features", [])
    for item in mobility:
        mobility_class = item.get("properties", {}).get("mobility_class")
        if mobility_class not in {"proposed_street", "pedestrian_path", "cycleway"}:
            continue
        route = shape(item["geometry"])
        for building_id, building in building_shapes:
            if route.crosses(building) or route.within(building) or building.contains(route):
                code = "road_building_collision" if mobility_class == "proposed_street" else "public_route_building_collision"
                block(
                    "road_building_collision",
                    code,
                    f"{mobility_class} unexpectedly crosses concept massing.",
                    item.get("id"),
                    [building_id],
                )

    main_if = [
        item
        for item in layers.get("overall_structure", {}).get("features", [])
        if item.get("properties", {}).get("semantic_class") == "main_if_segment"
    ]
    parallel = [
        item
        for item in layers.get("overall_structure", {}).get("features", [])
        if item.get("properties", {}).get("semantic_class") == "parallel_human_segment"
    ]
    if not line_network_connected(main_if):
        block(
            "main_if_continuity",
            "main_if_disconnected",
            "MAIN-IF segments do not form one connected network.",
        )
    if not line_network_connected(parallel):
        block(
            "parallel_human_continuity",
            "parallel_human_disconnected",
            "PARALLEL-HUMAN segments do not form one connected network.",
        )
    if parallel:
        parallel_shape = unary_union([shape(item["geometry"]) for item in parallel])
        for item in layers.get("overall_structure", {}).get("features", []):
            if item.get("properties", {}).get("semantic_class") != "human_service_node":
                continue
            if shape(item["geometry"]).distance(parallel_shape) > 0.0015:
                block(
                    "parallel_human_continuity",
                    "human_service_node_off_network",
                    "Human service node is not within the conceptual service reach of PARALLEL-HUMAN.",
                    item.get("id"),
                )

    overall = layers.get("overall_structure", {}).get("features", [])
    if main_if:
        main_shape = unary_union([shape(item["geometry"]) for item in main_if])
        for item in overall:
            props = item.get("properties", {})
            semantic_class = props.get("semantic_class")
            if semantic_class == "east_west_public_stitch" and not shape(item["geometry"]).intersects(main_shape):
                block(
                    "public_path_continuity",
                    "public_stitch_disconnected",
                    "East-west public stitch does not connect to MAIN-IF.",
                    item.get("id"),
                )
            if semantic_class == "endpoint_gateway":
                destination = feature_by_id.get(props.get("destination_ref"))
                if destination is None or not shape(destination["geometry"]).covers(shape(item["geometry"])):
                    block(
                        "public_path_continuity",
                        "gateway_without_destination",
                        "Gateway lacks a spatially coincident destination public room.",
                        item.get("id"),
                    )

    land_use = [shape(item["geometry"]) for item in layers.get("land_use_program", {}).get("features", [])]
    for item in massing:
        centroid = shape(item["geometry"]).representative_point()
        if not any(unit.covers(centroid) for unit in land_use):
            block(
                "land_use_building_compatibility",
                "massing_without_compatible_program_unit",
                "Concept massing has no containing program unit.",
                item.get("id"),
            )

    for item in layers.get("blue_green_heritage", {}).get("features", []):
        props = item.get("properties", {})
        if props.get("design_status") == "concept" and props.get("statutory_green_claim") is not False:
            block(
                "green_space_semantic_class",
                "proposed_green_has_statutory_claim",
                "Proposed blue-green geometry must explicitly deny statutory green-land status.",
                item.get("id"),
            )
        if props.get("design_status") == "background_reference" and props.get("evidence_class") == "DESIGN TARGET":
            block(
                "green_space_semantic_class",
                "background_green_mislabeled_design",
                "Background blue-green evidence cannot be a design target.",
                item.get("id"),
            )

    geometry_groups = defaultdict(list)
    for layer_name, item in all_items:
        if layer_name == "project_spatial_basis" or item.get("geometry") is None:
            continue
        key = (
            json.dumps(item["geometry"], sort_keys=True),
            item.get("properties", {}).get("semantic_class"),
        )
        geometry_groups[key].append(item.get("id"))
    for ids in geometry_groups.values():
        if len(ids) > 1:
            block(
                "duplicate_contradictory_geometry",
                "duplicate_geometry_same_semantics",
                "Multiple features repeat identical geometry and semantics.",
                ids[0],
                ids[1:],
            )

    for _, item in all_items:
        props = item.get("properties", {})
        name = " ".join(
            str(value)
            for value in [item.get("id", ""), props.get("name_en", ""), props.get("name_zh", "")]
        ).upper()
        if not (props.get("loop_claim") or "LOOP" in name):
            continue
        geometry = item.get("geometry")
        closed = geometry and geometry.get("type") == "LineString" and geometry["coordinates"][0] == geometry["coordinates"][-1]
        if not closed:
            block(
                "loop_cycle_naming_semantics",
                "named_loop_not_closed",
                "Feature claimed or named as a loop is not geometrically closed.",
                item.get("id"),
            )

    for _, item in all_items:
        props = item.get("properties", {})
        evidence = props.get("evidence_class")
        status = props.get("design_status")
        role = props.get("geometry_role")
        if evidence == "DESIGN TARGET" and (status != "concept" or role != "design_proposal"):
            block(
                "provisional_background_design_separation",
                "design_target_semantics_inconsistent",
                "DESIGN TARGET geometry must be a concept design proposal.",
                item.get("id"),
            )
        if status == "background_reference" and (
            evidence == "DESIGN TARGET" or role not in {"context_evidence", "unresolved_context"}
        ):
            block(
                "provisional_background_design_separation",
                "background_semantics_inconsistent",
                "Background reference must retain context or unresolved evidence semantics.",
                item.get("id"),
            )
        if item.get("id", "").startswith("PROV-"):
            block(
                "provisional_background_design_separation",
                "generated_feature_uses_provisional_id",
                "Gate B generated features cannot replace provisional scope features.",
                item.get("id"),
            )

    baseline = read_json(gate_a / "boundary_baseline.json")["feature_hashes"]
    actual_hashes = {item["id"]: geometry_hash(item["geometry"]) for item in boundary_file["features"]}
    if actual_hashes != baseline:
        block(
            "provisional_background_design_separation",
            "frozen_boundary_hash_mismatch",
            "One or more provisional boundary geometries differ from the frozen Gate A baseline.",
        )

    warning_specs = [
        ("official_scope_boundaries", "Official scope and key-area boundaries remain unavailable."),
        ("existing_buildings_and_ownership", "Existing building footprints, condition, and ownership remain unverified."),
        ("road_redlines_and_station_entrances", "Road redlines and station entrances remain unavailable; DZS station relation is unresolved."),
        ("statutory_height_far", "Statutory height, FAR, and density controls remain unavailable."),
        ("utilities_and_flood", "Municipal capacity, water blue-lines, flood, and drainage evidence remain unavailable."),
        ("parking", "Parking supply, demand, access, and statutory requirements remain UNKNOWN."),
    ]
    warnings.extend({"code": code, "message": message} for code, message in warning_specs)

    checks = {}
    for name in CHECK_NAMES:
        count = sum(1 for item in blockers if item["check"] == name)
        checks[name] = {"status": "PASS" if count == 0 else "BLOCKED", "blocker_count": count}
    metrics = {
        "layer_count": len(layers),
        "feature_count": len(all_items),
        "program_unit_count": len(layers.get("land_use_program", {}).get("features", [])),
        "concept_massing_count": len(massing),
        "project_spatial_basis_count": len(projects),
        "frozen_boundary_hash_matches": sum(
            1 for feature_id, value in baseline.items() if actual_hashes.get(feature_id) == value
        ),
        "frozen_boundary_count": len(baseline),
    }
    return {
        "schema_version": "gate-b-1",
        "ok": not blockers,
        "blocker_count": len(blockers),
        "warning_count": len(warnings),
        "checks": checks,
        "blockers": blockers,
        "warnings": warnings,
        "metrics": metrics,
    }


def run_qa(root=ROOT):
    root = Path(root)
    model, layers = load_generated(root)
    report = audit_layers(layers, model, root)
    write_json(root / "gate_b_semantic_qa.json", report)
    return report


if __name__ == "__main__":
    result = run_qa()
    print(json.dumps({"ok": result["ok"], "blockers": result["blocker_count"], "warnings": result["warning_count"]}, indent=2))
    raise SystemExit(0 if result["ok"] else 1)
