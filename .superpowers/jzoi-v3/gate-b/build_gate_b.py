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


def multi_line(coordinates):
    return {"type": "MultiLineString", "coordinates": coordinates}


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


def rect(x1, y1, x2, y2, chamfer=0.0):
    if not chamfer:
        return polygon([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])
    return polygon(
        [
            [x1 + chamfer, y1],
            [x2, y1],
            [x2, y2 - chamfer],
            [x2 - chamfer, y2],
            [x1, y2],
            [x1, y1 + chamfer],
        ]
    )


def build_land_use_program():
    specs = [
        ("DZS-01", "mobility_interface", 116.3424, 39.9444, 116.3450, 39.9460, ["JZOI-P06"], ["DZS"]),
        ("DZS-02", "mixed_public_commercial", 116.3452, 39.9444, 116.3480, 39.9460, ["JZOI-P06"], ["DZS"]),
        ("DZS-03", "enterprise_service", 116.3482, 39.9444, 116.3512, 39.9460, ["JZOI-P07"], ["DZS"]),
        ("DZS-04", "cultural_heritage", 116.3424, 39.9473, 116.3460, 39.9493, ["JZOI-P07"], ["DZS"]),
        ("DZS-05", "community_life_service", 116.3500, 39.9473, 116.3545, 39.9493, ["JZOI-P10"], ["DZS"]),
        ("ORG-01", "research_r_and_d", 116.3424, 39.9840, 116.3450, 39.9870, ["JZOI-P04"], ["ORG", "ECO-RESEARCH"]),
        ("ORG-02", "enterprise_service", 116.3500, 39.9840, 116.3526, 39.9870, ["JZOI-P05"], ["ORG"]),
        ("ORG-03", "mixed_public_commercial", 116.3454, 39.9840, 116.3496, 39.9870, ["JZOI-P04"], ["ORG"]),
        ("ORG-04", "innovation_testing", 116.3424, 39.9900, 116.3453, 39.9930, ["JZOI-P05"], ["ORG", "ZZY"]),
        ("ORG-05", "community_life_service", 116.3497, 39.9900, 116.3526, 39.9930, ["JZOI-P10"], ["ORG"]),
        ("ORG-06", "blue_green_public_realm", 116.3457, 39.9900, 116.3493, 39.9930, ["JZOI-P09"], ["ORG"]),
        ("ZZY-01", "innovation_testing", 116.3434, 40.0080, 116.3464, 40.0120, ["JZOI-P02"], ["ZZY"]),
        ("ZZY-02", "research_r_and_d", 116.3506, 40.0080, 116.3536, 40.0120, ["JZOI-P02"], ["ZZY"]),
        ("ZZY-03", "blue_green_public_realm", 116.3434, 40.0220, 116.3470, 40.0255, ["JZOI-P03"], ["ZZY"]),
        ("ZZY-04", "enterprise_service", 116.3500, 40.0185, 116.3536, 40.0220, ["JZOI-P03"], ["ZZY"]),
        ("ZZY-05", "mobility_interface", 116.3434, 40.0130, 116.3456, 40.0180, ["JZOI-P01"], ["ZZY"]),
        ("ZZY-06", "community_life_service", 116.3514, 40.0130, 116.3536, 40.0180, ["JZOI-P10"], ["ZZY"]),
        ("ZZY-07", "cultural_heritage", 116.3470, 40.0222, 116.3500, 40.0255, ["JZOI-P11"], ["ZZY"]),
    ]
    activities = {
        "research_r_and_d": ["research", "translation", "shared labs"],
        "innovation_testing": ["controlled testing", "prototype support", "human review"],
        "enterprise_service": ["enterprise support", "procurement", "adoption review"],
        "mixed_public_commercial": ["public hall", "retail", "exhibition", "civic service"],
        "community_life_service": ["neighborhood service", "talent service", "staffed fallback"],
        "cultural_heritage": ["interpretation", "culture", "public room"],
        "blue_green_public_realm": ["rainwater", "ecology", "walking", "public space"],
        "mobility_interface": ["walking", "cycling", "transfer", "wayfinding"],
    }
    features = []
    for unit_id, program_class, x1, y1, x2, y2, projects, ecosystem in specs:
        features.append(
            feature(
                f"PROGRAM-{unit_id}",
                rect(x1, y1, x2, y2, min((x2 - x1), (y2 - y1)) * 0.12),
                "program_unit",
                "OVERALL-DESIGN-001",
                program_class=program_class,
                role=f"{unit_id} {program_class.replace('_', ' ')} design unit",
                compatible_activities=activities[program_class],
                project_refs=projects,
                ecosystem_refs=ecosystem,
                confidence="low",
                planning_status="non_statutory_design_concept",
            )
        )
    return collection("jzoi_gate_b_land_use_program", features)


def build_mobility(existing):
    road_context = feature_by_id(existing, "EX-ROAD-001")
    features = [
        feature(
            "MOB-BG-ROAD-NS",
            road_context["geometry"],
            "mobility_background",
            "OVERALL-DESIGN-001",
            evidence_class=road_context["properties"]["evidence_class"],
            design_status="background_reference",
            geometry_role="context_evidence",
            mobility_class="background_road_context",
            source_feature_id="EX-ROAD-001",
            redline_claim=False,
            containment_applicable=False,
        ),
        feature(
            "MOB-PROPOSED-STREETS",
            multi_line(
                [
                    [[116.3424, 39.9465], [116.3545, 39.9465]],
                    [[116.3424, 39.9885], [116.3526, 39.9885]],
                    [[116.3434, 40.0165], [116.3536, 40.0165]],
                ]
            ),
            "mobility_design",
            "OVERALL-DESIGN-001",
            mobility_class="proposed_street",
            public_path=True,
            redline_claim=False,
        ),
        feature(
            "MOB-PEDESTRIAN-NETWORK",
            multi_line(
                [
                    [[116.3460, 39.9452], [116.3485, 39.9470], [116.3450, 39.9720], [116.3475, 39.9885], [116.3485, 40.0165]],
                    [[116.3418, 39.9885], [116.3530, 39.9885]],
                    [[116.3432, 40.0165], [116.3538, 40.0165]],
                ]
            ),
            "mobility_design",
            "OVERALL-DESIGN-001",
            mobility_class="pedestrian_path",
            public_path=True,
            access_intent="step-free; detailed grades require survey",
        ),
        feature(
            "MOB-CYCLE-NETWORK",
            multi_line(
                [
                    [[116.3430, 39.9482], [116.3537, 39.9482]],
                    [[116.3426, 39.9927], [116.3524, 39.9927]],
                    [[116.3435, 40.0238], [116.3534, 40.0238]],
                ]
            ),
            "mobility_design",
            "OVERALL-DESIGN-001",
            mobility_class="cycleway",
            public_path=True,
        ),
        feature(
            "MOB-LOGISTICS-NETWORK",
            multi_line(
                [
                    [[116.3542, 39.9445], [116.3542, 39.9488]],
                    [[116.3524, 39.9840], [116.3524, 39.9870]],
                    [[116.3534, 40.0080], [116.3534, 40.0148]],
                ]
            ),
            "mobility_design",
            "OVERALL-DESIGN-001",
            mobility_class="service_logistics",
            public_path=False,
            separation_rule="time and access controlled; no public-path claim",
        ),
        feature(
            "MOB-EMERGENCY-NETWORK",
            multi_line(
                [
                    [[116.3426, 39.9446], [116.3426, 39.9490]],
                    [[116.3426, 39.9840], [116.3426, 39.9928]],
                    [[116.3435, 40.0080], [116.3435, 40.0248]],
                ]
            ),
            "mobility_design",
            "OVERALL-DESIGN-001",
            mobility_class="emergency_access",
            public_path=False,
            separation_rule="controlled emergency access; detailed code review pending",
        ),
        feature(
            "DZS-STATION-BACKGROUND-RELATIONSHIP",
            None,
            "unresolved_station_relationship",
            "KEY-AREA-SCOPE-DZS",
            evidence_class="DATA_GAP",
            design_status="background_reference",
            geometry_role="unresolved_context",
            mobility_class="rail_station_background_relationship",
            source_feature_id="EX-TRANSIT-003",
            physical_connection_claim=False,
            station_entrance_claim=False,
        ),
    ]
    return collection("jzoi_gate_b_mobility", features)


def build_blue_green_heritage(existing):
    features = []
    for source_id in ["EX-WATER-001", "EX-WATER-002", "EX-RAIL-001", "EX-RAIL-002"]:
        item = feature_by_id(existing, source_id)
        props = item["properties"]
        features.append(
            feature(
                f"BGH-BG-{source_id}",
                item["geometry"],
                "background_blue_green_heritage",
                "OVERALL-DESIGN-001",
                evidence_class=props["evidence_class"],
                design_status="background_reference",
                geometry_role=props["geometry_role"],
                source_feature_id=source_id,
                source_ids=props["source_ids"],
                exact_boundary_claim=False,
            )
        )
    proposals = [
        ("QINGHE-RAIN-EDGE", "rainwater_ecology", rect(116.3433, 40.0208, 116.3537, 40.0220), ["ZZY"]),
        ("XIAOYUEHE-SCENARIO-SPINE", "ecology_scenario", line([[116.3530, 39.9760], [116.3520, 39.9885], [116.3530, 40.0020]]), ["ORG", "ZZY"]),
        ("JINGZHANG-PUBLIC-SEQUENCE", "heritage_public_sequence", line([[116.3460, 39.9452], [116.3450, 39.9720], [116.3475, 39.9885], [116.3485, 40.0165]]), ["DZS", "ORG", "ZZY"]),
        ("DZS-CIVIC-RAIN-ROOM", "rainwater_public_room", rect(116.3464, 39.9462, 116.3496, 39.9477), ["DZS"]),
        ("ORG-COMMONS-GARDEN", "commons_garden", rect(116.3455, 39.9875, 116.3495, 39.9895), ["ORG"]),
        ("ZZY-OBSERVATION-WETLAND", "safety_ecology_buffer", rect(116.3462, 40.0182, 116.3508, 40.0195), ["ZZY"]),
        ("SOUTH-RAIN-STITCH", "rainwater_stitch", line([[116.3418, 39.9550], [116.3538, 39.9550]]), ["OVERALL"]),
        ("CENTRAL-RAIN-STITCH", "rainwater_stitch", line([[116.3418, 39.9800], [116.3530, 39.9800]]), ["OVERALL"]),
        ("NORTH-RAIN-STITCH", "rainwater_stitch", line([[116.3432, 40.0060], [116.3538, 40.0060]]), ["OVERALL"]),
    ]
    for item_id, system_class, geometry, endpoints in proposals:
        features.append(
            feature(
                f"BGH-{item_id}",
                geometry,
                "proposed_blue_green_heritage",
                "OVERALL-DESIGN-001",
                system_class=system_class,
                endpoint_refs=endpoints,
                statutory_green_claim=False,
                water_boundary_claim=False,
                functions=["public realm", "walking/cycling support", "rainwater/ecology intent"],
            )
        )
    return collection("jzoi_gate_b_blue_green_heritage", features)


def build_massing():
    specs = [
        ("DZS-A", 116.3428, 39.9445, 116.3445, 39.9457, "medium", "active_service"),
        ("DZS-B", 116.3450, 39.9445, 116.3466, 39.9457, "low", "public_commercial"),
        ("DZS-C", 116.3498, 39.9445, 116.3514, 39.9457, "medium", "enterprise_service"),
        ("DZS-D", 116.3520, 39.9445, 116.3540, 39.9457, "tall", "landmark_support"),
        ("DZS-E", 116.3430, 39.9481, 116.3455, 39.9492, "low", "culture"),
        ("DZS-F", 116.3508, 39.9481, 116.3538, 39.9492, "medium", "talent_service"),
        ("ORG-A", 116.3430, 39.9842, 116.3448, 39.9864, "medium", "research"),
        ("ORG-B", 116.3454, 39.9842, 116.3470, 39.9864, "low", "open_source_commons"),
        ("ORG-C", 116.3498, 39.9842, 116.3518, 39.9864, "medium", "startup"),
        ("ORG-D", 116.3430, 39.9905, 116.3448, 39.9926, "medium", "prototype"),
        ("ORG-E", 116.3454, 39.9905, 116.3472, 39.9926, "low", "neighborhood_service"),
        ("ORG-F", 116.3500, 39.9905, 116.3520, 39.9926, "tall", "talent_service"),
        ("ZZY-A", 116.3440, 40.0083, 116.3460, 40.0112, "medium", "enterprise_test"),
        ("ZZY-B", 116.3508, 40.0083, 116.3530, 40.0112, "medium", "human_review"),
        ("ZZY-C", 116.3440, 40.0130, 116.3455, 40.0174, "low", "public_observation"),
        ("ZZY-D", 116.3515, 40.0130, 116.3530, 40.0174, "medium", "test_support"),
        ("ZZY-E", 116.3440, 40.0225, 116.3465, 40.0248, "low", "ecology_workshop"),
        ("ZZY-F", 116.3505, 40.0225, 116.3530, 40.0248, "tall", "landmark_support"),
    ]
    features = []
    for index, (item_id, x1, y1, x2, y2, hierarchy, ground_floor) in enumerate(specs):
        features.append(
            feature(
                f"MASS-{item_id}",
                rect(x1, y1, x2, y2, min(x2 - x1, y2 - y1) * 0.15),
                "concept_massing",
                "OVERALL-DESIGN-001",
                object_status=["concept_building", "concept_massing", "new_design_volume"][index % 3],
                height_hierarchy=hierarchy,
                height_status="relative_design_envelope",
                ground_floor_role=ground_floor,
                active_ground_floor=True,
                frontage_rule="face public room or stitch; detailed setback requires survey",
                existing_building_claim=False,
            )
        )
    return collection("jzoi_gate_b_massing", features)


def build_all(root=ROOT, write=True):
    root = Path(root)
    boundaries = read_json(REPO / "brief" / "site-package" / "geometry" / "provisional_boundaries.geojson")
    existing = read_json(GATE_A / "existing_conditions.geojson")
    ecosystem_edges = read_json(GATE_A / "gate_a_ecosystem_edges.json")
    boundary_ids = [item["id"] for item in boundaries["features"]]
    layers = {
        "regional_ecosystem": build_regional(existing, ecosystem_edges),
        "overall_structure": build_overall(),
        "land_use_program": build_land_use_program(),
        "mobility": build_mobility(existing),
        "blue_green_heritage": build_blue_green_heritage(existing),
        "massing": build_massing(),
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
