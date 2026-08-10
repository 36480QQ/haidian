import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
GATE_A = ROOT.parent


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def feature(
    feature_id,
    geometry,
    semantic_class,
    host_scope,
    *,
    evidence_class="DESIGN TARGET",
    design_status="concept",
    geometry_role="design_proposal",
    **properties,
):
    values = {
        "id": feature_id,
        "semantic_class": semantic_class,
        "evidence_class": evidence_class,
        "design_status": design_status,
        "geometry_role": geometry_role,
        "host_scope": host_scope,
    }
    values.update(properties)
    return {"type": "Feature", "id": feature_id, "properties": values, "geometry": geometry}


def point(x, y):
    return {"type": "Point", "coordinates": [x, y]}


def line(coordinates):
    return {"type": "LineString", "coordinates": coordinates}


def polygon(coordinates):
    ring = list(coordinates)
    if ring[0] != ring[-1]:
        ring.append(ring[0])
    return {"type": "Polygon", "coordinates": [ring]}


def collection(name, features):
    return {"type": "FeatureCollection", "name": name, "features": features}


def feature_by_id(collection_value, feature_id):
    return next(item for item in collection_value["features"] if item.get("id") == feature_id)


def build_regional(existing, ecosystem_edges):
    nodes = {
        "ECO-RESEARCH": [116.326, 40.003],
        "ECO-FEEDBACK": [116.323, 39.958],
        "ECO-DATA-ACCESS": [116.321, 39.982],
        "zhongguancun_technology_service_wing": [116.318, 39.982],
        "xiaoyuehe_scenario_empowerment_wing": [116.359, 39.981],
        "ZZY": [116.3485, 40.0165],
        "ORG": [116.3475, 39.9885],
        "DZS": [116.3485, 39.947],
    }
    features = []
    for item in existing["features"]:
        if item["id"] not in {
            "EX-ROAD-001",
            "EX-ROAD-002",
            "EX-RAIL-001",
            "EX-RAIL-002",
            "EX-WATER-001",
            "EX-WATER-002",
            "EX-INST-001",
            "EX-INST-002",
            "EX-INST-003",
            "EX-INDUSTRY-001",
        }:
            continue
        source = item["properties"]
        semantic_class = "physical_corridor_background" if item["geometry"]["type"] == "LineString" else "context_anchor"
        features.append(
            feature(
                f"REG-{item['id']}",
                item["geometry"],
                semantic_class,
                "RESEARCH-SCOPE-001",
                evidence_class=source["evidence_class"],
                design_status="background_reference",
                geometry_role=source["geometry_role"],
                source_feature_id=item["id"],
                source_ids=source["source_ids"],
                confidence=source["confidence"],
                name_en=source["name_en"],
            )
        )
    for node_id, coordinates in nodes.items():
        features.append(
            feature(
                f"REG-NODE-{node_id}",
                point(*coordinates),
                "ecosystem_node",
                "RESEARCH-SCOPE-001",
                ecosystem_ref=node_id,
                confidence="low",
                spatial_claim="schematic node for relationship mapping",
            )
        )
    for edge in ecosystem_edges["edges"]:
        semantic_class = "service_resource_relationship"
        if edge["edge_id"].startswith("ECO-"):
            semantic_class = "schematic_ecosystem_edge"
        elif edge["edge_id"].startswith("DATA-"):
            semantic_class = "data_governance_relationship"
        start = nodes[edge["from_id"]]
        end = nodes[edge["to_id"]]
        features.append(
            feature(
                f"REG-{edge['edge_id']}",
                line([start, end]),
                semantic_class,
                "RESEARCH-SCOPE-001",
                ecosystem_edge_id=edge["edge_id"],
                service_or_resource=edge["service_or_resource"],
                stage=edge["stage"],
                output=edge["output"],
                physical_corridor_claim=False,
            )
        )
    return collection("jzoi_gate_b_regional_ecosystem", features)


def build_overall():
    main_vertices = [
        [116.3460, 39.9452],
        [116.3485, 39.9470],
        [116.3450, 39.9720],
        [116.3475, 39.9885],
        [116.3485, 40.0165],
    ]
    human_vertices = [
        [116.3438, 39.9452],
        [116.3462, 39.9472],
        [116.3434, 39.9720],
        [116.3452, 39.9885],
        [116.3460, 40.0165],
    ]
    features = []
    segment_names = ["DZS switch", "South civic link", "ORG commons link", "North test link"]
    for index, name in enumerate(segment_names, start=1):
        features.append(
            feature(
                f"MAIN-IF-{index:02d}",
                line([main_vertices[index - 1], main_vertices[index]]),
                "main_if_segment",
                "OVERALL-DESIGN-001",
                network_id="MAIN-IF",
                sequence=index,
                name_en=name,
                public_path=True,
                access_intent="step-free continuous public route; verification pending",
                physical_corridor_claim=True,
            )
        )
        features.append(
            feature(
                f"PARALLEL-HUMAN-{index:02d}",
                line([human_vertices[index - 1], human_vertices[index]]),
                "parallel_human_segment",
                "OVERALL-DESIGN-001",
                network_id="PARALLEL-HUMAN",
                sequence=index,
                public_path=True,
                access_intent="step-free staffed alternative; DESIGN INTENT",
                non_digital_access=True,
                physical_corridor_claim=True,
            )
        )
    service_nodes = [
        ("DZS-SOUTH", 116.3438, 39.9452, "DZS"),
        ("DZS-HRG", 116.3462, 39.9472, "DZS"),
        ("SOUTH-RELAY", 116.3434, 39.9720, "OVERALL"),
        ("ORG-HRG", 116.3452, 39.9885, "ORG"),
        ("NORTH-RELAY", 116.3450, 40.0020, "OVERALL"),
        ("ZZY-HRG", 116.3460, 40.0165, "ZZY"),
    ]
    for node_id, x, y, endpoint in service_nodes:
        features.append(
            feature(
                f"HUMAN-NODE-{node_id}",
                point(x, y),
                "human_service_node",
                "OVERALL-DESIGN-001",
                network_id="PARALLEL-HUMAN",
                endpoint=endpoint,
                staffed_service=True,
                non_digital_access=True,
                coverage_status="DESIGN INTENT",
            )
        )
    stitches = [
        ("DZS", [[116.3415, 39.9470], [116.3538, 39.9470]]),
        ("ORG", [[116.3418, 39.9885], [116.3530, 39.9885]]),
        ("ZZY", [[116.3432, 40.0165], [116.3538, 40.0165]]),
    ]
    for endpoint, coordinates in stitches:
        features.append(
            feature(
                f"EW-STITCH-{endpoint}",
                line(coordinates),
                "east_west_public_stitch",
                "OVERALL-DESIGN-001",
                endpoint=endpoint,
                public_path=True,
                spatial_claim="proposed public connection; alignment subject to survey",
            )
        )
    for endpoint, coordinates in {
        "DZS": [116.3485, 39.9470],
        "ORG": [116.3475, 39.9885],
        "ZZY": [116.3485, 40.0165],
    }.items():
        features.append(
            feature(
                f"GATEWAY-{endpoint}",
                point(*coordinates),
                "endpoint_gateway",
                "OVERALL-DESIGN-001",
                endpoint=endpoint,
                network_id="MAIN-IF",
                destination_ref=f"PUBLIC-ROOM-{endpoint}",
            )
        )
        x, y = coordinates
        features.append(
            feature(
                f"PUBLIC-ROOM-{endpoint}",
                polygon(
                    [
                        [x - 0.0010, y - 0.0007],
                        [x + 0.0010, y - 0.0007],
                        [x + 0.0010, y + 0.0007],
                        [x - 0.0010, y + 0.0007],
                    ]
                ),
                "endpoint_public_room",
                "OVERALL-DESIGN-001",
                endpoint=endpoint,
                public_path=True,
                project_refs=["JZOI-P01"],
            )
        )
    return collection("jzoi_gate_b_overall_structure", features)


def build_all(root=ROOT, write=True):
    root = Path(root)
    boundaries = read_json(REPO / "brief" / "site-package" / "geometry" / "provisional_boundaries.geojson")
    existing = read_json(GATE_A / "existing_conditions.geojson")
    ecosystem_edges = read_json(GATE_A / "gate_a_ecosystem_edges.json")
    boundary_ids = [item["id"] for item in boundaries["features"]]
    layers = {
        "regional_ecosystem": build_regional(existing, ecosystem_edges),
        "overall_structure": build_overall(),
    }
    model = {
        "model_id": "JZOI-GATE-B",
        "schema_version": "gate-b-1",
        "status": "internal_spatial_review",
        "scales": ["43.6_km2_research", "11.4_km2_overall", "three_key_areas"],
        "endpoint_sequence": ["DZS", "ORG", "ZZY"],
        "frozen_ecosystem_edge_count": ecosystem_edges["edge_count"],
        "provisional_boundary_ids": boundary_ids,
        "boundary_policy": "reference only; unchanged provisional geometry",
        "design_evidence_class": "DESIGN TARGET",
        "design_status": "concept",
        "layers": layers,
    }
    if write:
        for layer_name, layer in layers.items():
            write_json(root / "spatial" / f"{layer_name}.geojson", layer)
        persisted = {key: value for key, value in model.items() if key != "layers"}
        persisted["layer_manifest"] = {
            name: {"path": f"spatial/{name}.geojson", "feature_count": len(layer["features"])}
            for name, layer in layers.items()
        }
        write_json(root / "gate_b_spatial_model.json", persisted)
    return model


if __name__ == "__main__":
    result = build_all()
    print(json.dumps({"model_id": result["model_id"], "layers": list(result["layers"])}, indent=2))
