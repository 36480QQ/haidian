import copy
import importlib
import importlib.util
import json
import sys
import unittest
from pathlib import Path

from shapely.geometry import shape


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
sys.path.insert(0, str(ROOT))

EXPECTED_BOUNDARY_IDS = [
    "PROV-SITE-001",
    "PROV-RESEARCH-001",
    "PROV-KEY-SCOPE-001",
    "PROV-KEY-001",
    "PROV-KEY-002",
    "PROV-KEY-003",
]

REQUIRED_PROGRAM_CLASSES = {
    "research_r_and_d",
    "innovation_testing",
    "enterprise_service",
    "mixed_public_commercial",
    "community_life_service",
    "cultural_heritage",
    "blue_green_public_realm",
    "mobility_interface",
}

REQUIRED_MOBILITY_CLASSES = {
    "background_road_context",
    "proposed_street",
    "pedestrian_path",
    "cycleway",
    "service_logistics",
    "emergency_access",
    "rail_station_background_relationship",
}

REQUIRED_KEY_AREA_CLASSES = {
    "ZZY": {
        "controlled_test_yard",
        "safety_buffer",
        "public_observation",
        "human_review_gate",
        "ordinary_public_path",
        "cycle_test_loop",
        "service_logistics",
        "emergency_access",
        "ecology_rainwater",
        "physical_emergency_stop",
        "enterprise_testing",
        "public_testing_boundary",
        "concept_massing",
        "section_logic",
    },
    "ORG": {
        "research",
        "translation",
        "prototype",
        "open_source_commons",
        "startup_incubation",
        "permeability_path",
        "neighborhood_service",
        "talent_service",
        "active_ground_floor",
        "public_private_gradient",
        "public_space",
        "concept_massing",
        "section_logic",
    },
    "DZS": {
        "unresolved_station_relationship",
        "pedestrian_convergence",
        "cycleway",
        "procurement_adoption",
        "enterprise_service",
        "consent",
        "appeal",
        "culture",
        "international_talent_service",
        "non_digital_fallback",
        "public_private_service_gradient",
        "public_space",
        "concept_massing",
        "section_logic",
    },
}

REQUIRED_LANDMARK_FIELDS = {
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
}

REQUIRED_COMPONENT_FIELDS = {
    "where_used",
    "dimensions_concept",
    "clearance_accessibility",
    "operational_state",
    "information_hierarchy",
    "public_path_relationship",
    "scenario_refs",
}


def load_builder():
    spec = importlib.util.find_spec("build_gate_b")
    if spec is None:
        return None
    return importlib.import_module("build_gate_b")


def load_qa():
    spec = importlib.util.find_spec("jzoi_semantic_qa")
    if spec is None:
        return None
    return importlib.import_module("jzoi_semantic_qa")


class GateBModelTests(unittest.TestCase):
    def test_three_scale_model_preserves_frozen_gate_a_contract(self):
        builder = load_builder()
        self.assertIsNotNone(builder, "Gate B builder must exist")

        model = builder.build_all(ROOT, write=False)

        self.assertEqual(
            model["scales"],
            ["43.6_km2_research", "11.4_km2_overall", "three_key_areas"],
        )
        self.assertEqual(model["frozen_ecosystem_edge_count"], 25)
        self.assertEqual(model["provisional_boundary_ids"], EXPECTED_BOUNDARY_IDS)
        self.assertEqual(model["endpoint_sequence"], ["DZS", "ORG", "ZZY"])

    def test_overall_backbones_are_connected_design_networks(self):
        builder = load_builder()
        self.assertIsNotNone(builder, "Gate B builder must exist")

        model = builder.build_all(ROOT, write=False)
        features = model["layers"]["overall_structure"]["features"]
        main_if = [f for f in features if f["properties"]["semantic_class"] == "main_if_segment"]
        human_nodes = [
            f for f in features if f["properties"]["semantic_class"] == "human_service_node"
        ]

        self.assertEqual(len(main_if), 4)
        self.assertGreaterEqual(len(human_nodes), 6)
        self.assertTrue(all(f["properties"]["evidence_class"] == "DESIGN TARGET" for f in main_if))
        self.assertTrue(all(f["properties"]["design_status"] == "concept" for f in main_if))

    def test_written_model_and_layers_are_valid_json(self):
        builder = load_builder()
        self.assertIsNotNone(builder, "Gate B builder must exist")

        model = builder.build_all(ROOT, write=True)
        loaded = json.loads((ROOT / "gate_b_spatial_model.json").read_text(encoding="utf-8"))

        self.assertEqual(loaded["model_id"], "JZOI-GATE-B")
        self.assertTrue({"regional_ecosystem", "overall_structure"} <= set(model["layers"]))
        for layer_name in model["layers"]:
            layer = json.loads((ROOT / "spatial" / f"{layer_name}.geojson").read_text(encoding="utf-8"))
            self.assertEqual(layer["type"], "FeatureCollection")
            self.assertGreater(len(layer["features"]), 0)

    def test_land_use_is_program_mosaic_not_four_giant_bands(self):
        builder = load_builder()
        model = builder.build_all(ROOT, write=False)
        self.assertIn("land_use_program", model["layers"])
        units = model["layers"]["land_use_program"]["features"]

        self.assertGreaterEqual(len(units), 18)
        self.assertEqual(
            {item["properties"]["program_class"] for item in units},
            REQUIRED_PROGRAM_CLASSES,
        )
        self.assertTrue(all(item["properties"]["design_status"] == "concept" for item in units))
        self.assertTrue(all(item["properties"]["compatible_activities"] for item in units))
        self.assertTrue(all(item["properties"]["project_refs"] for item in units))

    def test_mobility_modes_and_massing_semantics_are_explicit(self):
        builder = load_builder()
        model = builder.build_all(ROOT, write=False)
        self.assertIn("mobility", model["layers"])
        self.assertIn("massing", model["layers"])
        mobility = model["layers"]["mobility"]["features"]
        massing = model["layers"]["massing"]["features"]

        self.assertEqual(
            {item["properties"]["mobility_class"] for item in mobility},
            REQUIRED_MOBILITY_CLASSES,
        )
        self.assertGreaterEqual(len(massing), 18)
        self.assertFalse(
            {"retain", "renovate"}
            & {item["properties"]["object_status"] for item in massing}
        )
        self.assertTrue(
            all(
                item["properties"]["height_status"] == "relative_design_envelope"
                for item in massing
            )
        )

    def test_blue_green_layer_separates_background_evidence_from_design(self):
        builder = load_builder()
        model = builder.build_all(ROOT, write=False)
        self.assertIn("blue_green_heritage", model["layers"])
        features = model["layers"]["blue_green_heritage"]["features"]
        background = [item for item in features if item["properties"]["design_status"] == "background_reference"]
        proposed = [item for item in features if item["properties"]["design_status"] == "concept"]

        self.assertGreaterEqual(len(background), 4)
        self.assertGreaterEqual(len(proposed), 8)
        self.assertTrue(all(item["properties"]["evidence_class"] != "DESIGN TARGET" for item in background))
        self.assertTrue(all(item["properties"]["evidence_class"] == "DESIGN TARGET" for item in proposed))
        self.assertTrue(all(item["properties"]["statutory_green_claim"] is False for item in proposed))

    def test_each_key_area_has_a_complete_spatial_prototype(self):
        builder = load_builder()
        model = builder.build_all(ROOT, write=False)

        for endpoint, required in REQUIRED_KEY_AREA_CLASSES.items():
            layer_name = f"{endpoint.lower()}_plan"
            self.assertIn(layer_name, model["layers"])
            classes = {
                item["properties"]["semantic_class"]
                for item in model["layers"][layer_name]["features"]
            }
            self.assertTrue(required <= classes, (endpoint, sorted(required - classes)))

    def test_key_area_physical_objects_stay_within_provisional_study_polygons(self):
        builder = load_builder()
        model = builder.build_all(ROOT, write=False)
        boundaries = json.loads(
            (REPO / "brief" / "site-package" / "geometry" / "provisional_boundaries.geojson").read_text(
                encoding="utf-8"
            )
        )
        boundary_by_endpoint = {
            "ZZY": shape(next(item["geometry"] for item in boundaries["features"] if item["id"] == "PROV-KEY-001")),
            "ORG": shape(next(item["geometry"] for item in boundaries["features"] if item["id"] == "PROV-KEY-002")),
            "DZS": shape(next(item["geometry"] for item in boundaries["features"] if item["id"] == "PROV-KEY-003")),
        }

        for endpoint, boundary in boundary_by_endpoint.items():
            self.assertIn(f"{endpoint.lower()}_plan", model["layers"])
            for item in model["layers"][f"{endpoint.lower()}_plan"]["features"]:
                if item["geometry"] is None:
                    continue
                self.assertTrue(boundary.covers(shape(item["geometry"])), item["id"])

    def test_zzy_cycle_is_closed_and_dzs_station_relationship_is_unresolved(self):
        builder = load_builder()
        model = builder.build_all(ROOT, write=False)
        self.assertIn("zzy_plan", model["layers"])
        self.assertIn("dzs_plan", model["layers"])
        zzy_loop = next(
            item for item in model["layers"]["zzy_plan"]["features"] if item["id"] == "ZZY-CYCLE-LOOP"
        )
        station = next(
            item
            for item in model["layers"]["dzs_plan"]["features"]
            if item["id"] == "DZS-STATION-REL-UNRESOLVED"
        )

        self.assertEqual(zzy_loop["geometry"]["coordinates"][0], zzy_loop["geometry"]["coordinates"][-1])
        self.assertEqual(station["properties"]["evidence_class"], "DATA_GAP")
        self.assertEqual(station["properties"]["geometry_role"], "unresolved_context")
        self.assertFalse(station["properties"]["physical_connection_claim"])
        self.assertIsNone(station["geometry"])

    def test_three_landmarks_define_physical_and_operational_states(self):
        builder = load_builder()
        model = builder.build_all(ROOT, write=False)
        self.assertIn("landmarks", model["layers"])
        landmarks = model["layers"]["landmarks"]["features"]

        self.assertEqual(len(landmarks), 3)
        self.assertEqual({item["properties"]["endpoint"] for item in landmarks}, {"ZZY", "ORG", "DZS"})
        for item in landmarks:
            self.assertTrue(REQUIRED_LANDMARK_FIELDS <= set(item["properties"]), item["id"])
            self.assertEqual(item["properties"]["evidence_class"], "DESIGN TARGET")

    def test_all_component_families_have_spatial_and_operational_contracts(self):
        builder = load_builder()
        model = builder.build_all(ROOT, write=False)
        self.assertIn("components", model["layers"])
        components = model["layers"]["components"]["features"]

        self.assertEqual(
            {item["properties"]["component_family"] for item in components},
            {"IF-MARK", "CONSENT-POST", "HUMAN-DESK", "TEST-RAIL", "QUIET-BEACON"},
        )
        for item in components:
            self.assertTrue(REQUIRED_COMPONENT_FIELDS <= set(item["properties"]), item["id"])

    def test_all_twelve_projects_have_resolvable_specific_spatial_basis(self):
        builder = load_builder()
        model = builder.build_all(ROOT, write=False)
        self.assertIn("project_spatial_basis", model["layers"])
        projects = model["layers"]["project_spatial_basis"]["features"]
        all_feature_ids = {
            item["id"]
            for layer_name, layer in model["layers"].items()
            if layer_name != "project_spatial_basis"
            for item in layer["features"]
        }

        self.assertEqual(
            {item["properties"]["project_id"] for item in projects},
            {f"JZOI-P{index:02d}" for index in range(1, 13)},
        )
        self.assertEqual(len(projects), 12)
        for item in projects:
            props = item["properties"]
            self.assertTrue(props["host_refs"], item["id"])
            self.assertTrue(props["feature_refs"], item["id"])
            self.assertTrue(set(props["feature_refs"]) <= all_feature_ids, item["id"])
            self.assertTrue(props["dependencies"], item["id"])
            self.assertTrue(props["scenario_refs"], item["id"])


class GateBSemanticQATests(unittest.TestCase):
    def setUp(self):
        self.builder = load_builder()
        self.model = self.builder.build_all(ROOT, write=True)

    def test_qa_detects_duplicate_feature_ids(self):
        qa = load_qa()
        self.assertIsNotNone(qa, "Gate B semantic QA module must exist")
        layers = copy.deepcopy(self.model["layers"])
        layers["mobility"]["features"].append(copy.deepcopy(layers["mobility"]["features"][0]))

        report = qa.audit_layers(layers, self.model, ROOT)

        self.assertIn("duplicate_feature_id", {item["code"] for item in report["blockers"]})

    def test_qa_detects_open_geometry_claimed_as_loop(self):
        qa = load_qa()
        self.assertIsNotNone(qa, "Gate B semantic QA module must exist")
        layers = copy.deepcopy(self.model["layers"])
        loop = next(item for item in layers["zzy_plan"]["features"] if item["id"] == "ZZY-CYCLE-LOOP")
        loop["geometry"]["coordinates"][-1] = [116.3450, 40.0100]

        report = qa.audit_layers(layers, self.model, ROOT)

        self.assertIn("named_loop_not_closed", {item["code"] for item in report["blockers"]})

    def test_qa_detects_proposed_road_crossing_concept_massing(self):
        qa = load_qa()
        self.assertIsNotNone(qa, "Gate B semantic QA module must exist")
        layers = copy.deepcopy(self.model["layers"])
        street = next(
            item
            for item in layers["mobility"]["features"]
            if item["properties"]["mobility_class"] == "proposed_street"
        )
        street["geometry"] = {
            "type": "LineString",
            "coordinates": [[116.3430, 39.9450], [116.3540, 39.9450]],
        }

        report = qa.audit_layers(layers, self.model, ROOT)

        self.assertIn("road_building_collision", {item["code"] for item in report["blockers"]})

    def test_generated_gate_b_model_has_zero_semantic_blockers(self):
        qa = load_qa()
        self.assertIsNotNone(qa, "Gate B semantic QA module must exist")

        report = qa.run_qa(ROOT)

        required_checks = {
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
        }
        self.assertEqual(required_checks, set(report["checks"]))
        self.assertTrue(report["ok"], report["blockers"])
        self.assertEqual(report["blocker_count"], 0)


if __name__ == "__main__":
    unittest.main()
