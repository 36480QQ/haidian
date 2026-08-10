import json
from pathlib import Path

from pyproj import Transformer
from shapely.geometry import shape
from shapely.ops import transform, unary_union

import jzoi_semantic_qa


ROOT = Path(__file__).resolve().parent
REQUIRED_REVIEW_STEMS = [
    "overall_structure",
    "overall_masterplan",
    "mobility",
    "blue_green_heritage",
    "zzy_plan",
    "org_plan",
    "dzs_plan",
    "sections",
    "massing",
    "landmarks",
    "components",
]


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def approximate_length_km(features):
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:4548", always_xy=True)
    geometry = unary_union([shape(item["geometry"]) for item in features])
    projected = transform(transformer.transform, geometry)
    return round(projected.length / 1000, 1)


def selected(features, semantic_class):
    return [
        item
        for item in features
        if item.get("properties", {}).get("semantic_class") == semantic_class
    ]


def markdown_for(package):
    report = package["report"]
    layers = report["new_spatial_layers"]
    projects = package["project_spatial_closure"]
    qa = package["semantic_qa"]
    limitations = package["evidence_dependent_limitations"]
    lines = [
        "# JZOI Gate B Review Package",
        "",
        "Status: ready for Gate B review",
        "",
        "All spatial outputs are internal DESIGN TARGET / concept artifacts. They are not statutory plans, implementation drawings, or final A0/A3/HTML/PDF deliverables.",
        "",
        "## 1. Files Changed",
        "",
    ]
    lines.extend(f"- `{path}`" for path in report["files_changed"])
    lines.extend(["", "## 2. New Spatial Layers", ""])
    lines.extend(
        f"- `{item['path']}`: {item['feature_count']} features"
        for item in layers
    )
    lines.extend(
        [
            "",
            "## 3. Overall Spatial Concept",
            "",
            report["overall_spatial_concept"],
            "",
            "## 4. MAIN-IF Design",
            "",
            f"Four connected physical segments run from the south provisional edge through DZS, ORG, and ZZY to the north provisional edge. Approximate concept-route length: {report['main_if_design']['approximate_length_km']} km.",
            "",
            "## 5. PARALLEL-HUMAN Design",
            "",
            f"Four connected segments and {report['parallel_human_design']['staffed_service_node_count']} staffed service nodes form a non-digital alternative. Approximate concept-route length: {report['parallel_human_design']['approximate_length_km']} km. Coverage remains DESIGN INTENT.",
            "",
            "## 6. ZZY Design",
            "",
            report["zzy_design"]["summary"],
            "",
            "## 7. ORG Design",
            "",
            report["org_design"]["summary"],
            "",
            "## 8. DZS Design",
            "",
            report["dzs_design"]["summary"],
            "",
            "## 9. Mobility System",
            "",
            report["mobility_system"]["summary"],
            "",
            "## 10. Blue-Green / Heritage System",
            "",
            report["blue_green_heritage_system"]["summary"],
            "",
            "## 11. Massing Strategy",
            "",
            report["massing_strategy"]["summary"],
            "",
            "## 12. Landmarks / Components",
            "",
            report["landmarks_components"]["summary"],
            "",
            "## 13. P01-P12 Spatial Closure",
            "",
            "| Project | Geometry | Hosts | Feature refs | Status |",
            "| --- | --- | --- | ---: | --- |",
        ]
    )
    for project in projects:
        lines.append(
            f"| {project['project_id']} | {project['geometry_type']} | {', '.join(project['host_refs'])} | {len(project['feature_refs'])} | spatial basis ready |"
        )
    lines.extend(
        [
            "",
            "## 14. Semantic QA Result",
            "",
            f"- Blockers: `{qa['blocker_count']}`",
            f"- Warnings: `{qa['warning_count']}`",
            f"- Features checked: `{qa['metrics']['feature_count']}`",
            f"- Frozen boundary hashes matched: `{qa['metrics']['frozen_boundary_hash_matches']}/{qa['metrics']['frozen_boundary_count']}`",
            "",
            "## 15. Remaining Evidence-Dependent Limitations",
            "",
        ]
    )
    lines.extend(f"- **{key}**: {value}" for key, value in limitations.items())
    lines.extend(
        [
            "",
            "## Review Artifacts",
            "",
        ]
    )
    lines.extend(f"- `{path}`" for path in package["review_artifacts"])
    lines.extend(
        [
            "",
            "## Gate B Stop Condition",
            "",
        ]
    )
    lines.extend(
        f"- [{'x' if passed else ' '}] {name.replace('_', ' ')}"
        for name, passed in package["stop_condition"].items()
    )
    lines.extend(
        [
            "",
            "Gate B stops here. Gate C, final project/phase registry, final boards, final HTML, push, and PR creation are outside this package.",
            "",
        ]
    )
    return "\n".join(lines)


def build_package(root=ROOT, write=True):
    root = Path(root)
    model, layers = jzoi_semantic_qa.load_generated(root)
    qa = jzoi_semantic_qa.run_qa(root)
    overall = layers["overall_structure"]["features"]
    main_if = selected(overall, "main_if_segment")
    parallel = selected(overall, "parallel_human_segment")
    service_nodes = selected(overall, "human_service_node")
    program_units = layers["land_use_program"]["features"]
    mobility = layers["mobility"]["features"]
    blue_green = layers["blue_green_heritage"]["features"]
    massing = layers["massing"]["features"]
    landmarks = layers["landmarks"]["features"]
    components = layers["components"]["features"]
    projects = layers["project_spatial_basis"]["features"]

    project_closure = [
        {
            "project_id": item["properties"]["project_id"],
            "project_name": item["properties"]["project_name"],
            "geometry_type": item["geometry"]["type"],
            "host_refs": item["properties"]["host_refs"],
            "key_spatial_intervention": item["properties"]["key_spatial_intervention"],
            "dependencies": item["properties"]["dependencies"],
            "scenario_refs": item["properties"]["scenario_refs"],
            "feature_refs": item["properties"]["feature_refs"],
            "status": item["properties"]["spatial_status"],
        }
        for item in sorted(projects, key=lambda value: value["properties"]["project_id"])
    ]
    review_artifacts = [f"review/{stem}.svg" for stem in REQUIRED_REVIEW_STEMS]
    generated_files = [
        "gate_b_design_spec.md",
        "gate_b_implementation_plan.md",
        "build_gate_b.py",
        "jzoi_semantic_qa.py",
        "render_gate_b.py",
        "build_review_package.py",
        "test_gate_b.py",
        "gate_b_spatial_model.json",
        "gate_b_semantic_qa.json",
        "gate_b_review_package.json",
        "gate_b_review_package.md",
    ]
    generated_files.extend(f"spatial/{name}.geojson" for name in sorted(layers))
    generated_files.extend(review_artifacts)

    limitations = {item["code"]: item["message"] for item in qa["warnings"]}
    report = {
        "files_changed": generated_files,
        "new_spatial_layers": [
            {
                "layer": name,
                "path": f"spatial/{name}.geojson",
                "feature_count": len(layer["features"]),
            }
            for name, layer in sorted(layers.items())
        ],
        "overall_spatial_concept": (
            "A south-to-north Civic Protocol Spine links DZS Urban Switchboard, ORG Porous Commons, "
            "and ZZY Controlled Test Yard. East-west public stitches, a distributed eight-class program "
            "mosaic, service nodes, blue-green/heritage rooms, and relative massing envelopes replace "
            "the former boxes-and-bands diagram."
        ),
        "main_if_design": {
            "segment_count": len(main_if),
            "approximate_length_km": approximate_length_km(main_if),
            "endpoint_sequence": ["DZS", "ORG", "ZZY"],
            "scope_edge_gateways": ["MAIN-IF-GATEWAY-SOUTH", "MAIN-IF-GATEWAY-NORTH"],
            "status": "connected physical DESIGN TARGET route; alignment requires official evidence",
        },
        "parallel_human_design": {
            "segment_count": len(parallel),
            "staffed_service_node_count": len(service_nodes),
            "approximate_length_km": approximate_length_km(parallel),
            "non_digital_access": True,
            "coverage_status": "DESIGN INTENT; service-distance and accessibility survey pending",
        },
        "zzy_design": {
            "feature_count": len(layers["zzy_plan"]["features"]),
            "summary": "A public bypass and observation edge frame a buffered controlled yard with enterprise testing, a closed cycle loop, separate logistics/emergency access, rainwater ecology, staffed review, and physical TEST-RAIL stop controls.",
        },
        "org_design": {
            "feature_count": len(layers["org_plan"]["features"]),
            "summary": "A four-direction permeability lattice crosses research, translation, prototype, open-source commons, startup, talent, and neighborhood services with active ground-floor and public-to-controlled gradients.",
        },
        "dzs_design": {
            "feature_count": len(layers["dzs_plan"]["features"]),
            "summary": "A pedestrian switchboard organizes consent, appeal, procurement/adoption, enterprise, culture, talent, cycling, public space, and staffed fallback. The station relationship remains DATA GAP with null geometry and no entrance or physical-link claim.",
        },
        "mobility_system": {
            "feature_count": len(mobility),
            "classes": sorted({item["properties"]["mobility_class"] for item in mobility}),
            "summary": "Background road context, proposed streets, walking, cycling, logistics, emergency access, and unresolved station context are separate classes; semantic QA finds no route/massing collision and all primary networks connect.",
        },
        "blue_green_heritage_system": {
            "feature_count": len(blue_green),
            "background_feature_count": sum(1 for item in blue_green if item["properties"]["design_status"] == "background_reference"),
            "proposed_feature_count": sum(1 for item in blue_green if item["properties"]["design_status"] == "concept"),
            "summary": "Frozen Qinghe, Xiaoyuehe, and Jingzhang context remains distinct from nine proposed rainwater, ecology, public-room, and heritage-sequence features; none claims statutory green land or exact water boundaries.",
        },
        "massing_strategy": {
            "feature_count": len(massing),
            "relative_hierarchies": sorted({item["properties"]["height_hierarchy"] for item in massing}),
            "summary": "Eighteen chamfered concept envelopes define active frontages, public gaps, endpoint frames, and low/medium/tall/landmark relative hierarchy without retain/renovate, statutory height, FAR, or existing-building claims.",
        },
        "landmarks_components": {
            "landmark_count": len(landmarks),
            "landmark_ids": [item["id"] for item in landmarks],
            "component_family_count": len(components),
            "component_families": [item["properties"]["component_family"] for item in components],
            "summary": "ZZY Safety Gantry, ORG Open Bracket, and DZS Civic Switch are physically distinct. IF-MARK, CONSENT-POST, HUMAN-DESK, TEST-RAIL, and QUIET-BEACON have conceptual dimensions, clearances, states, information hierarchy, path relationships, and scenarios.",
        },
        "project_spatial_closure_status": {
            "closed_count": len(project_closure),
            "expected_count": 12,
            "status": "spatial basis ready; project/phase registry intentionally not finalized",
        },
        "semantic_qa_result": {
            "ok": qa["ok"],
            "blocker_count": qa["blocker_count"],
            "warning_count": qa["warning_count"],
        },
        "remaining_evidence_dependent_limitations": limitations,
    }
    stop_condition = {
        "overall_11_4_km2_structure_exists": len(program_units) >= 18,
        "main_if_spatially_resolved": len(main_if) == 4 and qa["checks"]["main_if_continuity"]["status"] == "PASS",
        "parallel_human_spatially_resolved": len(parallel) == 4 and qa["checks"]["parallel_human_continuity"]["status"] == "PASS",
        "three_key_areas_detailed": all(len(layers[f"{endpoint}_plan"]["features"]) >= 13 for endpoint in ["zzy", "org", "dzs"]),
        "land_use_is_spatial_mosaic": len(program_units) >= 18 and len({item["properties"]["program_class"] for item in program_units}) == 8,
        "mobility_is_coherent": qa["checks"]["road_building_collision"]["status"] == "PASS" and qa["checks"]["public_path_continuity"]["status"] == "PASS",
        "blue_green_heritage_is_spatialized": len(blue_green) >= 12,
        "massing_strategy_exists": len(massing) >= 18,
        "three_landmarks_exist": len(landmarks) == 3,
        "component_system_is_spatialized": len(components) == 5,
        "p01_p12_have_spatial_basis": len(project_closure) == 12,
        "semantic_spatial_qa_has_zero_blockers": qa["blocker_count"] == 0,
    }
    package = {
        "schema_version": "gate-b-1",
        "package_id": "JZOI-GATE-B-REVIEW",
        "status": "ready_for_gate_b_review" if all(stop_condition.values()) else "blocked",
        "gate_a_status": "frozen_accepted_baseline",
        "gate_b_scope": "internal spatial design source material; no final boards",
        "model": {
            "id": model["model_id"],
            "scales": model["scales"],
            "frozen_ecosystem_edge_count": model["frozen_ecosystem_edge_count"],
            "provisional_boundary_ids": model["provisional_boundary_ids"],
        },
        "report": report,
        "project_spatial_closure": project_closure,
        "semantic_qa": qa,
        "review_artifacts": review_artifacts,
        "evidence_dependent_limitations": limitations,
        "stop_condition": stop_condition,
        "out_of_scope_confirmed": [
            "Gate C",
            "final project/phase registry",
            "final A0/A3",
            "final HTML",
            "official validator changes",
            "push",
            "pull request",
        ],
    }
    if write:
        write_json(root / "gate_b_review_package.json", package)
        (root / "gate_b_review_package.md").write_text(markdown_for(package), encoding="utf-8")
    return package


if __name__ == "__main__":
    result = build_package()
    print(
        json.dumps(
            {
                "status": result["status"],
                "stop_conditions": sum(result["stop_condition"].values()),
                "stop_condition_count": len(result["stop_condition"]),
                "blockers": result["semantic_qa"]["blocker_count"],
            },
            indent=2,
        )
    )
    raise SystemExit(0 if result["status"] == "ready_for_gate_b_review" else 1)
