import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
GATE_A = ROOT.parent
MAIN_VERTICES = [
    [116.3485, 39.9443],
    [116.3485, 39.9470],
    [116.3475, 39.9805],
    [116.3475, 39.9885],
    [116.3485, 40.0165],
]
HUMAN_VERTICES = [
    [116.3423, 39.9468],
    [116.3462, 39.9472],
    [116.3445, 39.9805],
    [116.3452, 39.9885],
    [116.3460, 40.0165],
]


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


def multi_point(coordinates):
    return {"type": "MultiPoint", "coordinates": coordinates}


def collection(name, features):
    return {"type": "FeatureCollection", "name": name, "features": features}


def schematic_link(start, end, sequence):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.hypot(dx, dy) or 1.0
    offset = ((sequence % 5) - 2) * 0.00035 + sequence * 0.00001
    midpoint = [
        (start[0] + end[0]) / 2 - (dy / length) * offset,
        (start[1] + end[1]) / 2 + (dx / length) * offset,
    ]
    return line([start, midpoint, end])


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
    for sequence, edge in enumerate(ecosystem_edges["edges"], start=1):
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
                schematic_link(start, end, sequence),
                semantic_class,
                "RESEARCH-SCOPE-001",
                ecosystem_edge_id=edge["edge_id"],
                service_or_resource=edge["service_or_resource"],
                stage=edge["stage"],
                output=edge["output"],
                physical_corridor_claim=False,
                schematic_offset_sequence=sequence,
            )
        )
    return collection("jzoi_gate_b_regional_ecosystem", features)


def build_overall():
    features = []
    segment_names = ["DZS switch", "South civic link", "ORG commons link", "North test link"]
    for index, name in enumerate(segment_names, start=1):
        features.append(
            feature(
                f"MAIN-IF-{index:02d}",
                line([MAIN_VERTICES[index - 1], MAIN_VERTICES[index]]),
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
                line([HUMAN_VERTICES[index - 1], HUMAN_VERTICES[index]]),
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
        ("DZS-SOUTH", 116.3423, 39.9468, "DZS"),
        ("DZS-HRG", 116.3462, 39.9472, "DZS"),
        ("SOUTH-RELAY", 116.3445, 39.9805, "OVERALL"),
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
        ("DZS-03", "enterprise_service", 116.3482, 39.9444, 116.3545, 39.9460, ["JZOI-P07"], ["DZS"]),
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
        ("ZZY-07", "cultural_heritage", 116.3470, 40.0222, 116.3536, 40.0255, ["JZOI-P11"], ["ZZY"]),
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
                    MAIN_VERTICES,
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
                    [[116.3430, 39.9478], [116.3537, 39.9478]],
                    [[116.3426, 39.9931], [116.3524, 39.9931]],
                    [[116.3435, 40.0200], [116.3534, 40.0200]],
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
        ("JINGZHANG-PUBLIC-SEQUENCE", "heritage_public_sequence", line([MAIN_VERTICES[0], MAIN_VERTICES[2], MAIN_VERTICES[3], MAIN_VERTICES[4]]), ["DZS", "ORG", "ZZY"]),
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
        ("ZZY-C", 116.3440, 40.0130, 116.3455, 40.0158, "low", "public_observation"),
        ("ZZY-D", 116.3515, 40.0130, 116.3530, 40.0158, "medium", "test_support"),
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


def key_feature(endpoint, feature_id, geometry, semantic_class, **properties):
    return feature(
        feature_id,
        geometry,
        semantic_class,
        f"KEY-AREA-SCOPE-{endpoint}",
        endpoint=endpoint,
        confidence="low",
        boundary_interpretation="provisional study polygon; not parcel or road redline",
        **properties,
    )


def build_zzy_plan():
    features = [
        key_feature(
            "ZZY",
            "ZZY-CONTROLLED-YARD",
            rect(116.3468, 40.0122, 116.3505, 40.0172, 0.0003),
            "controlled_test_yard",
            access_state="controlled during tests; ordinary public route remains outside",
            scenario_refs=["SC-01", "SC-02", "SC-03"],
            project_refs=["JZOI-P02"],
        ),
        key_feature(
            "ZZY",
            "ZZY-SAFETY-BUFFER",
            rect(116.3462, 40.0116, 116.3511, 40.0178, 0.00035),
            "safety_buffer",
            buffer_status="design envelope; test-specific distance requires safety case",
            public_access=False,
            project_refs=["JZOI-P02"],
        ),
        key_feature(
            "ZZY",
            "ZZY-PUBLIC-OBSERVATION",
            line([[116.3463, 40.0112], [116.3510, 40.0112]]),
            "public_observation",
            visibility="screened direct view to controlled yard",
            public_path=True,
            project_refs=["JZOI-P02"],
        ),
        key_feature(
            "ZZY",
            "ZZY-HUMAN-REVIEW-GATE",
            point(116.3487, 40.0112),
            "human_review_gate",
            staffed_service=True,
            non_digital_access=True,
            fallback_state="manual check-in, printed test brief, physical stop control",
            scenario_refs=["SC-01", "SC-03", "SC-04"],
        ),
        key_feature(
            "ZZY",
            "ZZY-ORDINARY-PUBLIC-PATH",
            line(
                [
                    [116.3435, 40.0083],
                    [116.3458, 40.0112],
                    [116.3487, 40.0112],
                    [116.3512, 40.0182],
                    [116.3535, 40.0238],
                ]
            ),
            "ordinary_public_path",
            public_path=True,
            access_intent="step-free bypass outside controlled test boundary",
        ),
        key_feature(
            "ZZY",
            "ZZY-CYCLE-LOOP",
            line(
                [
                    [116.3437, 40.0079],
                    [116.3533, 40.0079],
                    [116.3533, 40.0252],
                    [116.3437, 40.0252],
                    [116.3437, 40.0079],
                ]
            ),
            "cycle_test_loop",
            loop_claim=True,
            operating_modes=["ordinary cycle circulation", "booked controlled test"],
            public_path=True,
            project_refs=["JZOI-P03"],
        ),
        key_feature(
            "ZZY",
            "ZZY-LOGISTICS",
            line([[116.3533, 40.0082], [116.3533, 40.0180], [116.3512, 40.0180]]),
            "service_logistics",
            public_path=False,
            separation_rule="controlled access and timed operation",
        ),
        key_feature(
            "ZZY",
            "ZZY-EMERGENCY-ACCESS",
            line([[116.3436, 40.0082], [116.3436, 40.0180], [116.3461, 40.0180]]),
            "emergency_access",
            public_path=False,
            fail_safe_priority="unobstructed emergency route",
        ),
        key_feature(
            "ZZY",
            "ZZY-QINGHE-RAIN-GARDEN",
            rect(116.3435, 40.0204, 116.3535, 40.0220, 0.00025),
            "ecology_rainwater",
            source_relation="Qinghe background point; exact bank and blue-line unknown",
            water_boundary_claim=False,
            functions=["rainwater detention intent", "habitat edge", "public walk"],
        ),
        key_feature(
            "ZZY",
            "ZZY-TEST-RAIL-STOP",
            multi_line(
                [
                    [[116.3468, 40.0122], [116.3505, 40.0122]],
                    [[116.3505, 40.0122], [116.3505, 40.0172]],
                    [[116.3505, 40.0172], [116.3468, 40.0172]],
                    [[116.3468, 40.0172], [116.3468, 40.0122]],
                ]
            ),
            "physical_emergency_stop",
            physical_control=True,
            operational_state="red stop rail and manual isolation points during tests",
        ),
        key_feature(
            "ZZY",
            "ZZY-ENTERPRISE-TEST-BAY",
            rect(116.3508, 40.0083, 116.3530, 40.0110, 0.00025),
            "enterprise_testing",
            access_state="booked enterprise test support; no automatic public access",
            project_refs=["JZOI-P02"],
        ),
        key_feature(
            "ZZY",
            "ZZY-PUBLIC-TEST-BOUNDARY",
            line([[116.3462, 40.0116], [116.3511, 40.0116], [116.3511, 40.0178]]),
            "public_testing_boundary",
            boundary_type="operational design boundary",
            legal_boundary_claim=False,
        ),
        key_feature(
            "ZZY",
            "ZZY-MASSING-FRAME",
            rect(116.3441, 40.0084, 116.3460, 40.0110, 0.00025),
            "concept_massing",
            object_status="new_design_volume",
            height_hierarchy="medium",
            height_status="relative_design_envelope",
            frontage="active public/testing interface",
        ),
        key_feature(
            "ZZY",
            "ZZY-SECTION-A",
            line([[116.3434, 40.0146], [116.3535, 40.0146]]),
            "section_logic",
            sequence=["ordinary city", "public observation", "safety buffer", "controlled yard", "test support"],
        ),
    ]
    return collection("jzoi_gate_b_zzy_plan", features)


def build_org_plan():
    features = [
        key_feature("ORG", "ORG-RESEARCH", rect(116.3426, 39.9840, 116.3450, 39.9868, 0.00025), "research", project_refs=["JZOI-P04"]),
        key_feature("ORG", "ORG-TRANSLATION", rect(116.3454, 39.9840, 116.3472, 39.9868, 0.00022), "translation", project_refs=["JZOI-P04"]),
        key_feature("ORG", "ORG-PROTOTYPE", rect(116.3478, 39.9840, 116.3496, 39.9868, 0.00022), "prototype", project_refs=["JZOI-P04", "JZOI-P05"]),
        key_feature("ORG", "ORG-OPEN-SOURCE-COMMONS", rect(116.3452, 39.9874, 116.3498, 39.9896, 0.00028), "open_source_commons", public_path=True, ground_floor_access="open public commons during operating hours"),
        key_feature("ORG", "ORG-STARTUP-INCUBATION", rect(116.3500, 39.9840, 116.3524, 39.9868, 0.00025), "startup_incubation", project_refs=["JZOI-P05"]),
        key_feature(
            "ORG",
            "ORG-FOUR-WAY-PERMEABILITY",
            multi_line(
                [
                    [[116.3422, 39.9885], [116.3528, 39.9885]],
                    [[116.3475, 39.9838], [116.3475, 39.9932]],
                    [[116.3424, 39.9855], [116.3475, 39.9885]],
                    [[116.3526, 39.9915], [116.3475, 39.9885]],
                ]
            ),
            "permeability_path",
            public_path=True,
            directions=["west", "east", "south", "north"],
            access_intent="step-free four-direction public network; grades require survey",
        ),
        key_feature("ORG", "ORG-NEIGHBORHOOD-SERVICE", rect(116.3426, 39.9902, 116.3450, 39.9929, 0.00025), "neighborhood_service", non_digital_access=True, project_refs=["JZOI-P05"]),
        key_feature("ORG", "ORG-TALENT-SERVICE", rect(116.3500, 39.9902, 116.3524, 39.9929, 0.00025), "talent_service", non_digital_access=True, project_refs=["JZOI-P10"]),
        key_feature(
            "ORG",
            "ORG-ACTIVE-GROUND-FLOOR",
            multi_line(
                [
                    [[116.3428, 39.9872], [116.3468, 39.9872]],
                    [[116.3482, 39.9898], [116.3522, 39.9898]],
                ]
            ),
            "active_ground_floor",
            ground_floor_programs=["commons", "translation desk", "neighborhood service", "startup showcase"],
        ),
        key_feature(
            "ORG",
            "ORG-PUBLIC-PRIVATE-GRADIENT",
            rect(116.3450, 39.9869, 116.3500, 39.9901, 0.00025),
            "public_private_gradient",
            sequence=["public commons", "shared translation", "booked prototype", "controlled research"],
        ),
        key_feature("ORG", "ORG-COMMONS-ROOM", rect(116.3462, 39.9877, 116.3488, 39.9893, 0.0002), "public_space", public_path=True, project_refs=["JZOI-P04"]),
        key_feature("ORG", "ORG-COURTYARD-MASSING", rect(116.3502, 39.9872, 116.3523, 39.9896, 0.0003), "concept_massing", object_status="concept_building", height_hierarchy="medium", height_status="relative_design_envelope", courtyard_logic=True),
        key_feature("ORG", "ORG-SECTION-A", line([[116.3423, 39.9885], [116.3527, 39.9885]]), "section_logic", sequence=["campus context", "research", "commons", "startup", "neighborhood context"]),
    ]
    return collection("jzoi_gate_b_org_plan", features)


def build_dzs_plan():
    features = [
        feature(
            "DZS-STATION-REL-UNRESOLVED",
            None,
            "unresolved_station_relationship",
            "KEY-AREA-SCOPE-DZS",
            evidence_class="DATA_GAP",
            design_status="background_reference",
            geometry_role="unresolved_context",
            endpoint="DZS",
            source_feature_id="EX-TRANSIT-003",
            physical_connection_claim=False,
            station_entrance_claim=False,
            interface_condition="background station relationship cannot be reconciled to provisional polygon",
        ),
        key_feature(
            "DZS",
            "DZS-PEDESTRIAN-CONVERGENCE",
            multi_line(
                [
                    [[116.3423, 39.9470], [116.3546, 39.9470]],
                    [[116.3485, 39.9443], [116.3485, 39.9495]],
                    [[116.3430, 39.9446], [116.3485, 39.9470], [116.3540, 39.9492]],
                ]
            ),
            "pedestrian_convergence",
            public_path=True,
            station_connection_claim=False,
        ),
        key_feature("DZS", "DZS-CYCLEWAY", line([[116.3424, 39.9480], [116.3545, 39.9480]]), "cycleway", public_path=True),
        key_feature("DZS", "DZS-PROCUREMENT-ADOPTION", rect(116.3489, 39.9444, 116.3513, 39.9464, 0.00022), "procurement_adoption", project_refs=["JZOI-P06"]),
        key_feature("DZS", "DZS-ENTERPRISE-SERVICE", rect(116.3517, 39.9444, 116.3543, 39.9464, 0.00022), "enterprise_service", project_refs=["JZOI-P07"]),
        key_feature("DZS", "DZS-CONSENT-ROOM", rect(116.3454, 39.9444, 116.3472, 39.9462, 0.0002), "consent", non_digital_access=True, project_refs=["JZOI-P06"]),
        key_feature("DZS", "DZS-APPEAL-ROOM", rect(116.3430, 39.9444, 116.3448, 39.9462, 0.0002), "appeal", non_digital_access=True, project_refs=["JZOI-P06"]),
        key_feature("DZS", "DZS-CULTURE-ROOM", rect(116.3426, 39.9483, 116.3456, 39.9494, 0.0002), "culture", project_refs=["JZOI-P07"]),
        key_feature("DZS", "DZS-INTERNATIONAL-TALENT", rect(116.3510, 39.9483, 116.3542, 39.9494, 0.0002), "international_talent_service", non_digital_access=True, project_refs=["JZOI-P10"]),
        key_feature(
            "DZS",
            "DZS-HUMAN-DESK",
            point(116.3477, 39.9470),
            "non_digital_fallback",
            staffed_service=True,
            operational_state="printed forms, spoken support, manual queue and appeal intake",
        ),
        key_feature(
            "DZS",
            "DZS-SERVICE-GRADIENT",
            rect(116.3458, 39.9463, 116.3510, 39.9477, 0.00018),
            "public_private_service_gradient",
            sequence=["public arrival", "consent and orientation", "staffed service", "enterprise review", "controlled adoption"],
        ),
        key_feature("DZS", "DZS-SWITCHBOARD-PLAZA", rect(116.3464, 39.9462, 116.3505, 39.9478, 0.0002), "public_space", public_path=True, project_refs=["JZOI-P06"]),
        key_feature("DZS", "DZS-SWITCH-MASSING", rect(116.3488, 39.9482, 116.3505, 39.9494, 0.00018), "concept_massing", object_status="new_design_volume", height_hierarchy="landmark", height_status="relative_design_envelope", statutory_height_claim=False),
        key_feature("DZS", "DZS-SECTION-A", line([[116.3424, 39.9470], [116.3545, 39.9470]]), "section_logic", sequence=["city edge", "appeal", "public switchboard", "adoption service", "city edge"], station_connection_claim=False),
    ]
    return collection("jzoi_gate_b_dzs_plan", features)


def build_landmarks():
    specs = [
        (
            "LANDMARK-ZZY-SAFETY-GANTRY",
            "ZZY",
            [116.3492, 40.0112],
            "ZZY-HUMAN-REVIEW-GATE",
            "marks the transition between ordinary city movement and controlled testing",
            "open steel gantry with visible manual stop bar",
            "district gateway; relative scale below surrounding landmark massing",
            "walk-through threshold with staffed test-status panel",
            "wide step-free passage, tactile edge, high-contrast stop state",
            "fixed sign, manual stop bar, and staffed explanation remain available",
            "open frame and test-status board",
            "low-glare white frame with red physical stop state; no dynamic advertising",
            "quarterly stop drill and replaceable rail/panel inspection",
            "black frame, cyan access line, yellow bounded-test field, orange review point",
            "Controlled Test Yard",
        ),
        (
            "LANDMARK-ORG-OPEN-BRACKET",
            "ORG",
            [116.3475, 39.9888],
            "ORG-COMMONS-ROOM",
            "makes the public commons and four-way permeability legible",
            "two offset enterable brackets framing the commons crossing",
            "civic room marker; lower than adjacent medium massing",
            "seating, notice rail, open-source display, and four-way passage",
            "step-free central opening, tactile route, quiet seating edge",
            "printed dependency board and staffed commons desk",
            "open frame, shade, and public work surface",
            "soft white task light and fixed green commons marker",
            "monthly fastener, surface, tactile-route, and notice-board check",
            "black brackets, green commons plane, cyan path, orange help point",
            "Porous Commons",
        ),
        (
            "LANDMARK-DZS-CIVIC-SWITCH",
            "DZS",
            [116.3507, 39.9470],
            "DZS-SWITCHBOARD-PLAZA",
            "marks consent, appeal, enterprise service, and culture as one civic interface",
            "four-faced vertical switch with a low public canopy",
            "endpoint marker using a relative landmark envelope, not a statutory height",
            "four directional faces point to consent, appeal, adoption, and culture",
            "step-free canopy, tactile orientation strip, quiet waiting bay",
            "paper directory, staffed HUMAN-DESK, and fixed arrows remain operational",
            "fixed civic directory and shaded waiting point",
            "low-glare face lighting; service-open state shown without tracking",
            "weekly directory update and quarterly lighting/manual-mode inspection",
            "black switch frame, cyan movement, orange human service, white civic text",
            "Urban Switchboard",
        ),
    ]
    features = []
    fields = [
        "location_ref",
        "role",
        "form",
        "scale_concept",
        "interaction",
        "accessibility",
        "non_digital_state",
        "daytime_state",
        "nighttime_state",
        "maintenance",
        "vi_relationship",
        "endpoint_identity",
    ]
    for item in specs:
        feature_id, endpoint, coordinates, *values = item
        features.append(
            key_feature(
                endpoint,
                feature_id,
                point(*coordinates),
                "endpoint_landmark",
                **dict(zip(fields, values)),
            )
        )
    return collection("jzoi_gate_b_landmarks", features)


def build_components():
    specs = [
        (
            "COMP-IF-MARK",
            "IF-MARK",
            multi_point([[116.3485, 39.9470], [116.3475, 39.9885], [116.3485, 40.0165]]),
            ["DZS", "ORG", "ZZY"],
            "900 mm wide x 2200 mm high marker; concept dimension",
            "1800 mm clear path beside marker; tactile base kept outside through-route",
            "fixed endpoint and route identity; digital panel optional and independently switchable",
            ["endpoint", "next public room", "human route", "operator/contact"],
            "placed at gateways beside, never within, the clear public path",
            ["SC-02", "SC-05", "SC-09"],
        ),
        (
            "COMP-CONSENT-POST",
            "CONSENT-POST",
            multi_point([[116.3487, 40.0110], [116.3472, 39.9882], [116.3462, 39.9458]]),
            ["ZZY", "ORG", "DZS"],
            "450 mm wide x 1100 mm high post; concept dimension",
            "1500 mm turning space and approach from both sides",
            "notice, refusal, withdrawal, and human-contact states remain legible without power",
            ["purpose", "minimum data", "refuse/withdraw", "human review", "complaint"],
            "aligned with service threshold but set back from walking desire line",
            ["SC-01", "SC-05", "SC-09"],
        ),
        (
            "COMP-HUMAN-DESK",
            "HUMAN-DESK",
            multi_point(
                [
                    [116.3477, 39.9470],
                    [116.3452, 39.9885],
                    [116.3487, 40.0112],
                    [116.3434, 39.9720],
                    [116.3450, 40.0020],
                    [116.3460, 40.0165],
                ]
            ),
            ["DZS", "ORG", "ZZY", "OVERALL"],
            "1800 mm desk module with 760 mm and 900 mm work surfaces; concept dimension",
            "1500 mm turning circle, knee clearance, quiet-side waiting space",
            "staffed, paper, telephone, and spoken-service modes; screen never mandatory",
            ["service name", "queue", "documents", "appeal", "operator"],
            "visible from PARALLEL-HUMAN with no controlled threshold before help",
            [f"SC-{index:02d}" for index in range(1, 13)],
        ),
        (
            "COMP-TEST-RAIL",
            "TEST-RAIL",
            point(116.3468, 40.0147),
            ["ZZY"],
            "1000 mm high modular rail; bay length set by test safety case",
            "rail never reduces ordinary public bypass below concept clear width",
            "manual red stop, lockable isolation, and staffed release; power not required",
            ["test state", "stop", "responsible reviewer", "safe bypass"],
            "defines controlled yard edge while preserving the separate ordinary path",
            ["SC-01", "SC-02"],
        ),
        (
            "COMP-QUIET-BEACON",
            "QUIET-BEACON",
            multi_point([[116.3445, 39.9487], [116.3458, 39.9908], [116.3518, 40.0190]]),
            ["DZS", "ORG", "ZZY"],
            "300 mm wide x 1400 mm high non-audio marker; concept dimension",
            "located beyond tactile route with 1500 mm turning space nearby",
            "fixed quiet-route symbol, tactile arrow, and low-glare status light",
            ["quiet route", "distance band", "staffed help", "night state"],
            "marks quiet waiting/route branches without narrowing the main path",
            ["SC-04", "SC-07", "SC-12"],
        ),
    ]
    features = []
    for index, spec in enumerate(specs, start=1):
        (
            feature_id,
            family,
            geometry,
            where_used,
            dimensions,
            clearance,
            state,
            hierarchy,
            path_relation,
            scenarios,
        ) = spec
        features.append(
            feature(
                feature_id,
                geometry,
                "spatial_component",
                "OVERALL-DESIGN-001",
                component_family=family,
                where_used=where_used,
                dimensions_concept=dimensions,
                clearance_accessibility=clearance,
                operational_state=state,
                information_hierarchy=hierarchy,
                public_path_relationship=path_relation,
                scenario_refs=scenarios,
                component_status="concept family and indicative instances",
                detail_sequence=index,
            )
        )
    return collection("jzoi_gate_b_components", features)


def build_project_spatial_basis():
    main_route = [
        MAIN_VERTICES,
        HUMAN_VERTICES,
    ]
    specs = [
        ("JZOI-P01", "Continuous public interface", multi_line(main_route), ["OVERALL-DESIGN-001"], "connect MAIN-IF, PARALLEL-HUMAN, gateways, and endpoint public rooms", ["official redlines", "accessibility survey", "fire access"], ["SC-02", "SC-04", "SC-08", "SC-12"], ["MAIN-IF-01", "MAIN-IF-02", "MAIN-IF-03", "MAIN-IF-04", "PARALLEL-HUMAN-01", "PARALLEL-HUMAN-02", "PARALLEL-HUMAN-03", "PARALLEL-HUMAN-04"]),
        ("JZOI-P02", "Controlled Yard", point(116.3487, 40.0147), ["KEY-AREA-SCOPE-ZZY"], "controlled test yard, human review, observation, and physical stop", ["test safety case", "responsibility insurance", "professional review"], ["SC-01", "SC-02"], ["ZZY-CONTROLLED-YARD", "ZZY-HUMAN-REVIEW-GATE", "ZZY-TEST-RAIL-STOP"]),
        ("JZOI-P03", "Qinghe human and ecology interface", line([[116.3435, 40.0212], [116.3535, 40.0212]]), ["KEY-AREA-SCOPE-ZZY"], "rainwater ecology edge, manual operation, and public bypass", ["Qinghe blue-line", "flood data", "maintenance agreement"], ["SC-03", "SC-04"], ["ZZY-QINGHE-RAIN-GARDEN", "ZZY-ORDINARY-PUBLIC-PATH", "COMP-QUIET-BEACON"]),
        ("JZOI-P04", "Origin open-source commons", point(116.3475, 39.9885), ["KEY-AREA-SCOPE-ORG"], "four-way commons linking research, translation, and prototype", ["campus-city agreement", "open-source licensing review", "operating hours"], ["SC-05", "SC-06"], ["ORG-OPEN-SOURCE-COMMONS", "ORG-FOUR-WAY-PERMEABILITY", "ORG-TRANSLATION"]),
        ("JZOI-P05", "Origin neighborhood service edge", line([[116.3426, 39.9915], [116.3524, 39.9915]]), ["KEY-AREA-SCOPE-ORG"], "staffed neighborhood and talent service edge", ["ownership survey", "ground-floor access agreement", "operating budget"], ["SC-07", "SC-08"], ["ORG-NEIGHBORHOOD-SERVICE", "ORG-TALENT-SERVICE", "COMP-HUMAN-DESK"]),
        ("JZOI-P06", "Dazhongsi switchboard", point(116.3485, 39.9470), ["KEY-AREA-SCOPE-DZS"], "pedestrian convergence, consent, appeal, and procurement interface", ["station entrance evidence", "traffic survey", "municipal capacity"], ["SC-09", "SC-10", "SC-12"], ["DZS-PEDESTRIAN-CONVERGENCE", "DZS-CONSENT-ROOM", "DZS-APPEAL-ROOM", "DZS-PROCUREMENT-ADOPTION"]),
        ("JZOI-P07", "Dazhongsi cultural forecourt", point(116.3507, 39.9470), ["KEY-AREA-SCOPE-DZS"], "culture, quiet navigation, and civic landmark interface", ["content rights", "noise review", "event safety"], ["SC-11", "SC-12"], ["DZS-CULTURE-ROOM", "LANDMARK-DZS-CIVIC-SWITCH", "COMP-QUIET-BEACON"]),
        ("JZOI-P08", "Open research frontage", multi_line([[[116.3428, 39.9872], [116.3468, 39.9872]], [[116.3482, 39.9898], [116.3522, 39.9898]]]), ["KEY-AREA-SCOPE-ORG", "OVERALL-DESIGN-001"], "bookable public research and evaluation frontages", ["building survey", "fire review", "owner agreement"], ["SC-05", "SC-06"], ["ORG-ACTIVE-GROUND-FLOOR", "MASS-ORG-A", "MASS-ORG-B"]),
        ("JZOI-P09", "Mixed service edge", multi_line([[[116.3464, 39.9462], [116.3505, 39.9462]], [[116.3452, 39.9874], [116.3498, 39.9874]], [[116.3463, 40.0112], [116.3510, 40.0112]]]), ["OVERALL-DESIGN-001"], "alternate civic and enterprise service frontage at three endpoints", ["tenancy review", "fire review", "public-service operating covenant"], ["SC-04", "SC-07", "SC-09"], ["DZS-SWITCHBOARD-PLAZA", "ORG-OPEN-SOURCE-COMMONS", "ZZY-PUBLIC-OBSERVATION"]),
        ("JZOI-P10", "No-device service network", multi_point([[116.3477, 39.9470], [116.3452, 39.9885], [116.3487, 40.0112], [116.3434, 39.9720], [116.3450, 40.0020], [116.3460, 40.0165]]), ["OVERALL-DESIGN-001", "KEY-AREA-SCOPE-DZS", "KEY-AREA-SCOPE-ORG", "KEY-AREA-SCOPE-ZZY"], "distributed staffed, paper, telephone, and spoken-service network", ["staffing plan", "long-term operating budget", "service-distance survey"], [f"SC-{index:02d}" for index in range(1, 13)], ["COMP-HUMAN-DESK", "HUMAN-NODE-DZS-HRG", "HUMAN-NODE-ORG-HRG", "HUMAN-NODE-ZZY-HRG"]),
        ("JZOI-P11", "Contribution and evidence ledger", multi_point([[116.3492, 40.0112], [116.3475, 39.9888], [116.3507, 39.9470]]), ["OVERALL-DESIGN-001"], "physical public ledger points at all three endpoint landmarks", ["consent procedure", "content rights", "independent audit"], ["SC-01", "SC-05", "SC-09", "SC-11"], ["LANDMARK-ZZY-SAFETY-GANTRY", "LANDMARK-ORG-OPEN-BRACKET", "LANDMARK-DZS-CIVIC-SWITCH"]),
        ("JZOI-P12", "Annual public operations", multi_point([[116.3485, 39.9470], [116.3475, 39.9885], [116.3485, 40.0165]]), ["OVERALL-DESIGN-001"], "seasonal program distributed across the three endpoint public rooms", ["venue permissions", "annual budget", "event safety"], ["SC-02", "SC-05", "SC-07", "SC-10", "SC-11"], ["PUBLIC-ROOM-DZS", "PUBLIC-ROOM-ORG", "PUBLIC-ROOM-ZZY"]),
    ]
    features = []
    for project_id, name, geometry, hosts, intervention, dependencies, scenarios, refs in specs:
        features.append(
            feature(
                f"PROJECT-BASIS-{project_id}",
                geometry,
                "project_spatial_basis",
                "OVERALL-DESIGN-001",
                project_id=project_id,
                project_name=name,
                host_refs=hosts,
                key_spatial_intervention=intervention,
                dependencies=dependencies,
                scenario_refs=scenarios,
                feature_refs=refs,
                spatial_status="Gate B basis only; project registry not finalized",
            )
        )
    return collection("jzoi_gate_b_project_spatial_basis", features)


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
        "zzy_plan": build_zzy_plan(),
        "org_plan": build_org_plan(),
        "dzs_plan": build_dzs_plan(),
        "landmarks": build_landmarks(),
        "components": build_components(),
        "project_spatial_basis": build_project_spatial_basis(),
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
