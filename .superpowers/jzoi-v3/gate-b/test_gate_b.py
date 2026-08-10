import importlib
import importlib.util
import json
import sys
import unittest
from pathlib import Path


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


def load_builder():
    spec = importlib.util.find_spec("build_gate_b")
    if spec is None:
        return None
    return importlib.import_module("build_gate_b")


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
        self.assertEqual(set(model["layers"]), {"regional_ecosystem", "overall_structure"})
        for layer_name in model["layers"]:
            layer = json.loads((ROOT / "spatial" / f"{layer_name}.geojson").read_text(encoding="utf-8"))
            self.assertEqual(layer["type"], "FeatureCollection")
            self.assertGreater(len(layer["features"]), 0)


if __name__ == "__main__":
    unittest.main()
