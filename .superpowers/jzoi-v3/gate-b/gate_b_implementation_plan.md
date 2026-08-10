# JZOI Gate B Spatial Design Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the internal three-scale JZOI spatial proposal, review representations, and zero-blocker semantic QA without modifying Gate A or final submission outputs.

**Architecture:** `build_gate_b.py` is the deterministic source-model builder and GeoJSON exporter. `jzoi_semantic_qa.py` independently validates generated geometry and references. `render_gate_b.py` converts the generated data into internal SVG review drawings, while `build_review_package.py` summarizes model counts, design decisions, limitations, and QA evidence.

**Tech Stack:** Python 3.12, standard-library JSON/XML/path utilities, Shapely, PyProj, unittest, GeoJSON, SVG.

## Global Constraints

- Work only under `.superpowers/jzoi-v3/gate-b/` except for reading frozen Gate A and repository reference files.
- Preserve all six provisional boundary geometries byte-for-byte; never move `PROV-KEY-001/002/003`.
- Preserve JZOI, Civic Protocol Modernism, MAIN-IF, PARALLEL-HUMAN, endpoint identities, Three Areas + Two Wings, and all 25 Gate A typed edges.
- New spatial geometry uses `evidence_class: DESIGN TARGET`, `design_status: concept`, and honest concept semantics.
- DZS station anchoring remains an unresolved background relationship with no invented entrance or physical link.
- Do not modify the official validator or final A0/A3/HTML/PDF/figure files.
- Do not enter Gate C, finalize the phase registry, push, or create a PR.

## File Structure

- Create `.superpowers/jzoi-v3/gate-b/build_gate_b.py`: geometry helpers, canonical feature definitions, and deterministic GeoJSON/model generation.
- Create `.superpowers/jzoi-v3/gate-b/jzoi_semantic_qa.py`: independent spatial and semantic checks with JSON output.
- Create `.superpowers/jzoi-v3/gate-b/render_gate_b.py`: reusable SVG map/diagram renderer.
- Create `.superpowers/jzoi-v3/gate-b/build_review_package.py`: review JSON/Markdown assembler.
- Create `.superpowers/jzoi-v3/gate-b/test_gate_b.py`: unit and integration tests for model contracts, geometry, QA, SVGs, and deterministic output.
- Generate `.superpowers/jzoi-v3/gate-b/gate_b_spatial_model.json`: canonical registries and design narratives.
- Generate `.superpowers/jzoi-v3/gate-b/spatial/*.geojson`: regional, overall, thematic, key-area, landmark/component, and project layers.
- Generate `.superpowers/jzoi-v3/gate-b/review/*.svg`: internal review maps and diagrams.
- Generate `.superpowers/jzoi-v3/gate-b/gate_b_semantic_qa.json`: blocker/warning/metric report.
- Generate `.superpowers/jzoi-v3/gate-b/gate_b_review_package.json` and `.md`: Gate B handoff.

---

### Task 1: Canonical Three-Scale Spatial Model

**Files:**
- Create: `.superpowers/jzoi-v3/gate-b/test_gate_b.py`
- Create: `.superpowers/jzoi-v3/gate-b/build_gate_b.py`
- Generate: `.superpowers/jzoi-v3/gate-b/gate_b_spatial_model.json`
- Generate: `.superpowers/jzoi-v3/gate-b/spatial/regional_ecosystem.geojson`
- Generate: `.superpowers/jzoi-v3/gate-b/spatial/overall_structure.geojson`

**Interfaces:**
- Consumes: frozen `scope_registry.json`, `existing_conditions.geojson`, `gate_a_ecosystem_edges.json`, and repository `provisional_boundaries.geojson`.
- Produces: `build_all(root: Path) -> dict[str, object]`, `feature(...) -> dict`, and deterministic regional/overall FeatureCollections.

- [ ] **Step 1: Write failing contract tests**

```python
def test_three_scale_model_preserves_gate_a_contract(self):
    model = build_gate_b.build_all(ROOT)
    self.assertEqual(model["scales"], ["43.6_km2_research", "11.4_km2_overall", "three_key_areas"])
    self.assertEqual(model["frozen_ecosystem_edge_count"], 25)
    self.assertEqual(model["provisional_boundary_ids"], EXPECTED_BOUNDARY_IDS)

def test_overall_backbones_are_connected_design_networks(self):
    layers = build_gate_b.build_all(ROOT)["layers"]
    overall = layers["overall_structure"]["features"]
    self.assertEqual(len(by_class(overall, "main_if_segment")), 4)
    self.assertGreaterEqual(len(by_class(overall, "human_service_node")), 6)
```

- [ ] **Step 2: Run tests and confirm missing-module failure**

Run: `python -m unittest .superpowers/jzoi-v3/gate-b/test_gate_b.py -v`

Expected: FAIL because `build_gate_b` does not exist.

- [ ] **Step 3: Implement deterministic helpers and Level 1/2 layers**

Implement `feature()`, `point()`, `line()`, `polygon()`, `multi_line()`, `load_feature()`, `write_json()`, and `build_all()`. Define a bent MAIN-IF sequence through DZS, ORG, and ZZY; a parallel connected human-service network; east-west stitches; endpoint gateways; public rooms; Level 1 physical corridors; and distinct service/schematic edge classes. Copy Gate A background geometry and classifications without upgrading evidence.

- [ ] **Step 4: Generate data and pass Task 1 tests**

Run: `python .superpowers/jzoi-v3/gate-b/build_gate_b.py`

Run: `python -m unittest .superpowers/jzoi-v3/gate-b/test_gate_b.py -v`

Expected: Task 1 tests PASS; generated JSON parses.

- [ ] **Step 5: Commit Task 1**

```powershell
git add .superpowers/jzoi-v3/gate-b
git commit -m "feat: establish JZOI Gate B spatial model"
```

### Task 2: Overall Program, Mobility, Blue-Green, and Massing

**Files:**
- Modify: `.superpowers/jzoi-v3/gate-b/test_gate_b.py`
- Modify: `.superpowers/jzoi-v3/gate-b/build_gate_b.py`
- Generate: `.superpowers/jzoi-v3/gate-b/spatial/land_use_program.geojson`
- Generate: `.superpowers/jzoi-v3/gate-b/spatial/mobility.geojson`
- Generate: `.superpowers/jzoi-v3/gate-b/spatial/blue_green_heritage.geojson`
- Generate: `.superpowers/jzoi-v3/gate-b/spatial/massing.geojson`

**Interfaces:**
- Consumes: Task 1 feature helpers and overall backbones.
- Produces: program mosaics, separated mobility modes, background/design blue-green semantics, and concept massing envelopes.

- [ ] **Step 1: Add failing thematic-layer tests**

```python
def test_land_use_is_program_mosaic_not_four_bands(self):
    units = self.layers["land_use_program"]["features"]
    self.assertGreaterEqual(len(units), 18)
    self.assertGreaterEqual(len({f["properties"]["program_class"] for f in units}), 8)
    self.assertTrue(all(f["properties"]["design_status"] == "concept" for f in units))

def test_mobility_and_massing_semantics_are_honest(self):
    modes = {f["properties"]["mobility_class"] for f in self.layers["mobility"]["features"]}
    self.assertTrue(REQUIRED_MOBILITY_CLASSES <= modes)
    forbidden = {"retain", "renovate"}
    self.assertFalse(forbidden & {f["properties"]["object_status"] for f in self.layers["massing"]["features"]})
```

- [ ] **Step 2: Run tests and confirm missing-layer failures**

Run: `python -m unittest .superpowers/jzoi-v3/gate-b/test_gate_b.py -v`

Expected: FAIL for absent thematic layers.

- [ ] **Step 3: Add at least 18 program units and mode-separated networks**

Use research/R&D, innovation testing, enterprise/service, mixed public/commercial, community/life service, cultural/heritage, blue-green/public realm, and mobility/interface classes. Each unit records role, compatible activities, project refs, ecosystem refs, confidence, and design status. Mobility separates background context, proposed street, pedestrian, cycling, logistics, emergency, and unresolved rail/station relationship.

- [ ] **Step 4: Add blue-green/heritage sequences and non-rectangular concept massing**

Represent frozen Qinghe, Xiaoyuehe, and Jingzhang evidence as reference points/lines with original evidence classes. Add proposed rain gardens, water-sensitive edges, heritage/public rooms, and ecological stitches as DESIGN TARGET. Build courtyard, bar, gateway, and perimeter massing polygons with relative hierarchy only.

- [ ] **Step 5: Rebuild and pass thematic tests**

Run: `python .superpowers/jzoi-v3/gate-b/build_gate_b.py`

Run: `python -m unittest .superpowers/jzoi-v3/gate-b/test_gate_b.py -v`

Expected: PASS.

- [ ] **Step 6: Commit Task 2**

```powershell
git add .superpowers/jzoi-v3/gate-b
git commit -m "feat: spatialize JZOI overall systems"
```

### Task 3: Three Detailed Key-Area Prototypes

**Files:**
- Modify: `.superpowers/jzoi-v3/gate-b/test_gate_b.py`
- Modify: `.superpowers/jzoi-v3/gate-b/build_gate_b.py`
- Generate: `.superpowers/jzoi-v3/gate-b/spatial/zzy_plan.geojson`
- Generate: `.superpowers/jzoi-v3/gate-b/spatial/org_plan.geojson`
- Generate: `.superpowers/jzoi-v3/gate-b/spatial/dzs_plan.geojson`

**Interfaces:**
- Consumes: provisional key-area polygons and Task 1/2 helpers.
- Produces: detailed plan objects, circulation, gradients, programs, sections, massing roles, public-space structures, and special ZZY/DZS interface semantics.

- [ ] **Step 1: Add failing key-area completeness tests**

```python
def test_each_key_area_has_required_design_systems(self):
    for area, required in REQUIRED_KEY_AREA_CLASSES.items():
        classes = {f["properties"]["semantic_class"] for f in self.layers[f"{area.lower()}_plan"]["features"]}
        self.assertTrue(required <= classes, (area, required - classes))

def test_zzy_cycle_loop_is_closed_and_dzs_station_is_unresolved(self):
    loop = find(self.layers["zzy_plan"], "ZZY-CYCLE-LOOP")
    self.assertEqual(loop["geometry"]["coordinates"][0], loop["geometry"]["coordinates"][-1])
    station = find(self.layers["dzs_plan"], "DZS-STATION-REL-UNRESOLVED")
    self.assertEqual(station["properties"]["geometry_role"], "unresolved_context")
    self.assertEqual(station["properties"]["physical_connection_claim"], False)
```

- [ ] **Step 2: Run tests and confirm missing-prototype failures**

Run: `python -m unittest .superpowers/jzoi-v3/gate-b/test_gate_b.py -v`

Expected: FAIL for absent prototype classes.

- [ ] **Step 3: Implement ZZY safety-gradient prototype**

Add controlled test yard, safety buffer, public observation edge, staffed Human Review Gate, normal public path, closed cycle loop, logistics and emergency routes, rainwater/ecology edge, physical emergency stop rail, and concept massing. Encode operating boundary and fail-safe state explicitly.

- [ ] **Step 4: Implement ORG four-direction porous prototype**

Add four cardinal passages, central commons, research-to-translation-to-prototype sequence, startup/incubation, open-source commons, talent and neighborhood services, active ground floor, public/shared/controlled/private gradient, courtyard massing, and public rooms.

- [ ] **Step 5: Implement DZS switchboard prototype**

Add pedestrian convergence, cycle link, procurement/adoption, enterprise service, consent, appeal, culture, international/talent service, staffed fallback, public/service/private gradients, concept massing, and unresolved station relation. Keep every physical design object inside PROV-KEY-003.

- [ ] **Step 6: Rebuild and pass prototype tests**

Run: `python .superpowers/jzoi-v3/gate-b/build_gate_b.py`

Run: `python -m unittest .superpowers/jzoi-v3/gate-b/test_gate_b.py -v`

Expected: PASS.

- [ ] **Step 7: Commit Task 3**

```powershell
git add .superpowers/jzoi-v3/gate-b
git commit -m "feat: detail three JZOI endpoint prototypes"
```

### Task 4: Landmarks, Components, and P01-P12 Spatial Closure

**Files:**
- Modify: `.superpowers/jzoi-v3/gate-b/test_gate_b.py`
- Modify: `.superpowers/jzoi-v3/gate-b/build_gate_b.py`
- Generate: `.superpowers/jzoi-v3/gate-b/spatial/landmarks.geojson`
- Generate: `.superpowers/jzoi-v3/gate-b/spatial/components.geojson`
- Generate: `.superpowers/jzoi-v3/gate-b/spatial/project_spatial_basis.geojson`

**Interfaces:**
- Consumes: all spatial feature IDs and area/scenario registries.
- Produces: three landmark records, five component-family records/instances, and exactly twelve project spatial-basis records.

- [ ] **Step 1: Add failing closure tests**

```python
def test_landmarks_and_components_are_complete(self):
    self.assertEqual(len(self.layers["landmarks"]["features"]), 3)
    families = {f["properties"]["component_family"] for f in self.layers["components"]["features"]}
    self.assertEqual(families, {"IF-MARK", "CONSENT-POST", "HUMAN-DESK", "TEST-RAIL", "QUIET-BEACON"})

def test_all_twelve_projects_have_specific_spatial_basis(self):
    features = self.layers["project_spatial_basis"]["features"]
    self.assertEqual({f"JZOI-P{i:02d}" for i in range(1, 13)}, {f["properties"]["project_id"] for f in features})
    self.assertTrue(all(f["properties"]["host_refs"] for f in features))
```

- [ ] **Step 2: Run tests and confirm closure failures**

Run: `python -m unittest .superpowers/jzoi-v3/gate-b/test_gate_b.py -v`

Expected: FAIL for absent landmarks/components/projects.

- [ ] **Step 3: Implement landmark and component registries**

Define ZZY Safety Gantry, ORG Open Bracket, and DZS Civic Switch with all required operational fields. Define the five component families with conceptual dimensions, clearances, operating states, information hierarchy, path relation, hosts, and scenarios. Use point/line geometry appropriate to each instance.

- [ ] **Step 4: Implement P01-P12 spatial records**

Assign each project a host area, key intervention, dependencies, scenarios, and exact feature refs. Use MultiLineString or MultiPolygon for network projects; use compact point/polygon basis for local projects. Do not assign an entire program district to a small project.

- [ ] **Step 5: Rebuild and pass closure tests**

Run: `python .superpowers/jzoi-v3/gate-b/build_gate_b.py`

Run: `python -m unittest .superpowers/jzoi-v3/gate-b/test_gate_b.py -v`

Expected: PASS.

- [ ] **Step 6: Commit Task 4**

```powershell
git add .superpowers/jzoi-v3/gate-b
git commit -m "feat: close JZOI Gate B project references"
```

### Task 5: Independent Semantic Spatial QA

**Files:**
- Modify: `.superpowers/jzoi-v3/gate-b/test_gate_b.py`
- Create: `.superpowers/jzoi-v3/gate-b/jzoi_semantic_qa.py`
- Generate: `.superpowers/jzoi-v3/gate-b/gate_b_semantic_qa.json`

**Interfaces:**
- Consumes: `spatial/*.geojson`, model registries, and frozen boundary/reference files.
- Produces: `run_qa(root: Path) -> dict` with `ok`, `blocker_count`, `warning_count`, `checks`, `blockers`, `warnings`, and `metrics`.

- [ ] **Step 1: Write failing QA behavior tests**

```python
def test_qa_detects_duplicate_ids_and_open_named_loop(self):
    layers = copy.deepcopy(self.layers)
    layers["mobility"]["features"].append(copy.deepcopy(layers["mobility"]["features"][0]))
    report = jzoi_semantic_qa.audit_layers(layers, self.model)
    self.assertIn("duplicate_feature_id", {b["code"] for b in report["blockers"]})

def test_generated_model_has_zero_blockers(self):
    report = jzoi_semantic_qa.run_qa(ROOT)
    self.assertTrue(report["ok"], report["blockers"])
    self.assertEqual(report["blocker_count"], 0)
```

- [ ] **Step 2: Run tests and confirm missing-QA failure**

Run: `python -m unittest .superpowers/jzoi-v3/gate-b/test_gate_b.py -v`

Expected: FAIL because `jzoi_semantic_qa` does not exist.

- [ ] **Step 3: Implement structural and reference checks**

Implement GeoJSON validity, Shapely geometry validity, global ID uniqueness, host/project/scenario reference existence, project geometry consistency, scenario-host consistency, applicable scope/key-area containment, duplicate geometry, and provisional/background/design semantic separation.

- [ ] **Step 4: Implement network and compatibility checks**

Implement road/building collision detection, walk/cycle obstruction, public-path connectivity, MAIN-IF connectivity, PARALLEL-HUMAN connectivity and service-node relation, gateway destinations, named-loop closure, land-use/massing compatibility, and green semantic-class checks.

- [ ] **Step 5: Run QA and pass all tests**

Run: `python .superpowers/jzoi-v3/gate-b/jzoi_semantic_qa.py`

Run: `python -m unittest .superpowers/jzoi-v3/gate-b/test_gate_b.py -v`

Expected: `ok: true`, `blocker_count: 0`, tests PASS.

- [ ] **Step 6: Commit Task 5**

```powershell
git add .superpowers/jzoi-v3/gate-b
git commit -m "test: add JZOI Gate B semantic spatial QA"
```

### Task 6: Internal SVG Review Representations

**Files:**
- Modify: `.superpowers/jzoi-v3/gate-b/test_gate_b.py`
- Create: `.superpowers/jzoi-v3/gate-b/render_gate_b.py`
- Generate: `.superpowers/jzoi-v3/gate-b/review/overall_structure.svg`
- Generate: `.superpowers/jzoi-v3/gate-b/review/overall_masterplan.svg`
- Generate: `.superpowers/jzoi-v3/gate-b/review/mobility.svg`
- Generate: `.superpowers/jzoi-v3/gate-b/review/blue_green_heritage.svg`
- Generate: `.superpowers/jzoi-v3/gate-b/review/zzy_plan.svg`
- Generate: `.superpowers/jzoi-v3/gate-b/review/org_plan.svg`
- Generate: `.superpowers/jzoi-v3/gate-b/review/dzs_plan.svg`
- Generate: `.superpowers/jzoi-v3/gate-b/review/sections.svg`
- Generate: `.superpowers/jzoi-v3/gate-b/review/massing.svg`
- Generate: `.superpowers/jzoi-v3/gate-b/review/landmarks.svg`
- Generate: `.superpowers/jzoi-v3/gate-b/review/components.svg`

**Interfaces:**
- Consumes: generated GeoJSON and model narratives.
- Produces: `render_all(root: Path) -> list[Path]` with parseable standalone SVGs.

- [ ] **Step 1: Add failing review-output tests**

```python
def test_all_required_review_svgs_exist_and_parse(self):
    paths = render_gate_b.render_all(ROOT)
    self.assertEqual({p.stem for p in paths}, REQUIRED_REVIEW_STEMS)
    for path in paths:
        root = ElementTree.parse(path).getroot()
        self.assertTrue(root.tag.endswith("svg"))
        self.assertGreater(path.stat().st_size, 3000)
```

- [ ] **Step 2: Run tests and confirm missing-renderer failure**

Run: `python -m unittest .superpowers/jzoi-v3/gate-b/test_gate_b.py -v`

Expected: FAIL because `render_gate_b` does not exist.

- [ ] **Step 3: Implement reusable geospatial SVG renderer**

Implement feature bounds, map projection, geometry paths, semantic style mapping, legend, title block, status labels, north marker, rounded approximate scale notes, and separate line styles for physical corridors, service/resource relationships, and schematic edges.

- [ ] **Step 4: Implement plans, sections, massing, landmarks, and components sheets**

Render each required drawing with enough geometry and annotation to review spatial feasibility. Sections show public/testing safety gradient, ORG permeability/active edge, and DZS service gradient. Landmark/component drawings show conceptual dimensions and states without presentation rendering.

- [ ] **Step 5: Render and pass SVG tests**

Run: `python .superpowers/jzoi-v3/gate-b/render_gate_b.py`

Run: `python -m unittest .superpowers/jzoi-v3/gate-b/test_gate_b.py -v`

Expected: all 11 SVGs parse and tests PASS.

- [ ] **Step 6: Commit Task 6**

```powershell
git add .superpowers/jzoi-v3/gate-b
git commit -m "feat: render JZOI Gate B review drawings"
```

### Task 7: Review Package and Final Verification

**Files:**
- Modify: `.superpowers/jzoi-v3/gate-b/test_gate_b.py`
- Create: `.superpowers/jzoi-v3/gate-b/build_review_package.py`
- Generate: `.superpowers/jzoi-v3/gate-b/gate_b_review_package.json`
- Generate: `.superpowers/jzoi-v3/gate-b/gate_b_review_package.md`

**Interfaces:**
- Consumes: model, all layers, SVG paths, semantic QA, frozen Gate A hash/edge evidence, and Git diff.
- Produces: complete Gate B handoff with the 15 requested report topics and explicit evidence-dependent limitations.

- [ ] **Step 1: Add failing package-completeness tests**

```python
def test_review_package_records_stop_condition_and_limitations(self):
    package = build_review_package.build_package(ROOT)
    self.assertEqual(package["semantic_qa"]["blocker_count"], 0)
    self.assertEqual(len(package["project_spatial_closure"]), 12)
    self.assertTrue(all(package["stop_condition"].values()))
    self.assertIn("official_scope_boundaries", package["evidence_dependent_limitations"])
    self.assertIn("parking", package["evidence_dependent_limitations"])
```

- [ ] **Step 2: Run tests and confirm missing-package failure**

Run: `python -m unittest .superpowers/jzoi-v3/gate-b/test_gate_b.py -v`

Expected: FAIL because `build_review_package` does not exist.

- [ ] **Step 3: Implement machine-readable and Markdown handoff**

Report files changed, new layers, overall concept, MAIN-IF, PARALLEL-HUMAN, ZZY, ORG, DZS, mobility, blue-green/heritage, massing, landmarks/components, P01-P12 closure, QA, and remaining evidence limits. Include counts and rounded human-facing distances only.

- [ ] **Step 4: Run deterministic rebuild and parse verification**

Run builder, QA, renderer, and package builder twice. Hash generated outputs after each run and assert identical hashes. Parse every JSON/GeoJSON with `json` and every SVG with `xml.etree.ElementTree`.

- [ ] **Step 5: Run full tests and scope diff check**

Run: `python -m unittest .superpowers/jzoi-v3/gate-b/test_gate_b.py -v`

Run: `git status --short`

Expected: all tests PASS; no Gate A, official-validator, A0/A3/HTML/PDF/final-figure changes introduced by Gate B.

- [ ] **Step 6: Commit Task 7**

```powershell
git add .superpowers/jzoi-v3/gate-b
git commit -m "docs: add JZOI Gate B review package"
```

- [ ] **Step 7: Stop for Gate B review**

Report the review package paths and the 15 requested Gate B outcomes. Do not enter Gate C, push, or create a PR.
