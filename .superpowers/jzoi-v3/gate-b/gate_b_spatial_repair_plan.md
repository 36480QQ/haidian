# JZOI Gate B Professional Spatial Repair Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Repair the accepted Gate B package into professionally legible urban-design plans, sections, axonometrics, and physical landmark studies with mandatory PNG visual review.

**Architecture:** Extend the deterministic Gate B builder with one evidence-disciplined overall context layer and selectively reshape accepted route, key-area, and massing features. Split the renderer into map, section, axonometric, landmark, and component compositions; add browser PNG export plus image metrics; add a separate explicit professional spatial review record while preserving semantic QA.

**Tech Stack:** Python 3.12, Shapely, PyProj, Pillow, standard-library JSON/XML/subprocess utilities, GeoJSON, SVG, local Chrome/Edge headless rendering, unittest.

## Global Constraints

- Work only under `.superpowers/jzoi-v3/gate-b/` except for reading frozen evidence and provisional geometry.
- Preserve all six provisional boundaries, 25 ecosystem edges, accepted evidence classes, P01-P12 references, three landmark identities, and five component families.
- Do not reopen Gate A, enter Gate C, modify official validators, or generate final A0/A3/HTML/PDF outputs.
- Do not invent parcels, existing buildings, ownership, station entrances, road redlines, statutory heights, FAR, parking, utilities, or water boundaries.
- Do not increase feature/test counts as a quality proxy; add only context, branch, or catchment objects needed for spatial explanation.
- Keep current semantic QA checks and require zero blockers.
- Final status requires direct visual inspection of all eleven rendered PNGs.

## File Structure

- Modify `build_gate_b.py`: context base, segment metadata, service network, reshaped key-area plans, section specs, and improved 18-feature massing.
- Modify `test_gate_b.py`: behavior contracts for context explanation, route rationale, service network, plan/section correspondence, massing form, PNG output, and professional review.
- Modify `render_gate_b.py`: view-specific map, section, axonometric, landmark, component, label, and note rendering.
- Create `render_review_pngs.py`: Chrome/Edge SVG-to-PNG export and Pillow image metrics.
- Create `professional_spatial_review.py`: explicit qualitative checklist schema and review package writer.
- Generate `spatial/overall_context.geojson`: accepted context, unchanged provisional outlines, intervention envelope, and intentional non-intervention field.
- Regenerate existing spatial GeoJSON layers without changing frozen evidence semantics.
- Regenerate eleven `review/*.svg` and eleven `review/*.png` files.
- Generate `professional_spatial_review.json` and `.md`.
- Update `gate_b_review_package.json` and `.md` with repair outcomes and PNG paths.

---

### Task 1: Whole-Scope Context and Site-Responsive Service Spine

**Files:**
- Modify: `.superpowers/jzoi-v3/gate-b/test_gate_b.py`
- Modify: `.superpowers/jzoi-v3/gate-b/build_gate_b.py`
- Generate: `.superpowers/jzoi-v3/gate-b/spatial/overall_context.geojson`
- Regenerate: `.superpowers/jzoi-v3/gate-b/spatial/overall_structure.geojson`

**Interfaces:**
- Consumes: frozen `existing_conditions.geojson`, `scope_registry.json`, provisional boundaries, accepted overall features.
- Produces: `build_overall_context(existing, boundaries, intervention_layers) -> FeatureCollection` and enriched MAIN-IF/PARALLEL-HUMAN features.

- [ ] **Step 1: Write failing spatial-context tests**

```python
def test_overall_context_explains_full_scope_without_claiming_parcels(self):
    layer = self.model["layers"]["overall_context"]
    classes = {f["properties"]["context_class"] for f in layer["features"]}
    self.assertTrue({"scope", "background_context", "direct_intervention", "outside_direct_intervention"} <= classes)
    remainder = next(f for f in layer["features"] if f["properties"]["context_class"] == "outside_direct_intervention")
    self.assertEqual(remainder["properties"]["parcel_claim"], False)
    self.assertGreater(shape(remainder["geometry"]).area, 0)

def test_every_main_if_segment_records_spatial_reason_and_corridor_status(self):
    segments = by_semantic(self.model, "overall_structure", "main_if_segment")
    for segment in segments:
        self.assertTrue(REQUIRED_MAIN_IF_FIELDS <= set(segment["properties"]))
        self.assertGreater(len(segment["geometry"]["coordinates"]), 2)
        self.assertEqual(segment["properties"]["alignment_status"], "concept_corridor_centerline")
```

- [ ] **Step 2: Run tests and verify missing context/metadata failures**

Run: `python -m unittest discover -s ".superpowers/jzoi-v3/gate-b" -p "test_gate_b.py" -v`

Expected: FAIL for absent `overall_context` and missing MAIN-IF properties.

- [ ] **Step 3: Build the evidence-disciplined whole-scope context layer**

Copy accepted context features with original evidence classes; add unchanged provisional scope/key-area outlines; derive direct-intervention envelope from buffered proposal routes/program units; derive scope remainder with Shapely difference. Mark remainder `DESIGN TARGET`, `communication_mask`, `parcel_claim: false`, and `implementation_claim: false`.

- [ ] **Step 4: Reshape and document MAIN-IF**

Keep four IDs and connected endpoints but add context-responsive intermediate vertices. Populate all required anchor, reason, public-space, adjacency, crossing, gateway, width-range, and alignment-status fields. Keep `physical_corridor_claim: false` for the conceptual centerline and add `corridor_expression: envelope`.

- [ ] **Step 5: Convert PARALLEL-HUMAN into backbone plus branches/catchments**

Keep four connected backbone segments. Add one MultiLineString branch object linking staffed desks/review gates/public rooms and one MultiPolygon catchment object with `coverage_status: DESIGN INTENT`, `verified_accessibility: false`, and approximate service rationale.

- [ ] **Step 6: Rebuild and verify semantic QA remains zero-blocker**

Run builder, semantic QA, and full tests. Expected: new context tests PASS and semantic blocker count remains `0`.

- [ ] **Step 7: Commit Task 1**

```powershell
git add --sparse .superpowers/jzoi-v3/gate-b
git commit -m "feat: explain JZOI overall context and service spine"
```

### Task 2: Key-Area Place Form, Plan-Linked Sections, and Urban Massing

**Files:**
- Modify: `.superpowers/jzoi-v3/gate-b/test_gate_b.py`
- Modify: `.superpowers/jzoi-v3/gate-b/build_gate_b.py`
- Regenerate: `spatial/zzy_plan.geojson`, `org_plan.geojson`, `dzs_plan.geojson`, `massing.geojson`

**Interfaces:**
- Consumes: accepted key-area IDs, program semantics, landmarks, and provisional key polygons.
- Produces: reshaped plan geometries, section-spec properties, and exactly 18 urban-form massing features.

- [ ] **Step 1: Write failing form and section-correspondence tests**

```python
def test_key_area_plans_use_spatial_form_not_only_rectangles(self):
    for layer_name in ["zzy_plan", "org_plan", "dzs_plan"]:
        polygons = polygon_features(self.model["layers"][layer_name])
        self.assertGreaterEqual(sum(len(f["geometry"]["coordinates"][0]) > 7 for f in polygons), 2)

def test_each_section_line_has_people_scaled_section_spec(self):
    for endpoint in ["ZZY", "ORG", "DZS"]:
        section = find_feature(self.model, f"{endpoint}-SECTION-A")
        self.assertTrue(REQUIRED_SECTION_FIELDS <= set(section["properties"]))
        self.assertEqual(section["properties"]["plan_correspondence_id"], section["id"])
```

- [ ] **Step 2: Run tests and verify current box/bar model fails**

Run full Gate B tests. Expected: FAIL for polygon complexity, missing section dimensions, and missing urban-form fields.

- [ ] **Step 3: Reshape ZZY, ORG, and DZS in place**

ZZY: faceted yard, crescent/terrace observation edge, bypass, ecology swale, gates and support frontage. ORG: linked court/commons void, L/U blocks, secondary passages, active frontages, public/shared/controlled gradient. DZS: civic-room polygon, converging paths, service/cultural edges, cycle crossing, fallback point, and null-geometry station question relationship.

- [ ] **Step 4: Add section specifications to visible plan cuts**

For each section feature add `ground_sequence`, `width_ranges_m`, `relative_height_sequence`, `active_edge_refs`, `landscape_elements`, `gradient_sequence`, `people_scale_use`, and `plan_correspondence_id`. Values remain approximate design ranges.

- [ ] **Step 5: Reshape exactly 18 massing features**

Use L/U/courtyard/bar/gateway footprints, including holes where needed. Add `block_type`, `public_gap_refs`, `permeability_refs`, `active_frontage_edges`, `public_space_enclosure`, and `landmark_relation`. Preserve concept-only and relative-height semantics.

- [ ] **Step 6: Rebuild and pass form, containment, collision, and semantic tests**

Run builder, semantic QA, and tests. Expected: 18 massing features, all physical key-area objects contained, no route collisions, zero semantic blockers.

- [ ] **Step 7: Commit Task 2**

```powershell
git add --sparse .superpowers/jzoi-v3/gate-b
git commit -m "feat: reshape JZOI endpoint urban form"
```

### Task 3: Contextual Plans and Readable Map Composition

**Files:**
- Modify: `.superpowers/jzoi-v3/gate-b/test_gate_b.py`
- Modify: `.superpowers/jzoi-v3/gate-b/render_gate_b.py`
- Regenerate: `review/overall_structure.svg`, `overall_masterplan.svg`, `mobility.svg`, `blue_green_heritage.svg`, `zzy_plan.svg`, `org_plan.svg`, `dzs_plan.svg`

**Interfaces:**
- Consumes: all spatial layers and actual scope geometry.
- Produces: `render_context_map(...)`, `place_labels(...)`, `wrapped_text(...)`, and seven contextual plan SVGs.

- [ ] **Step 1: Write failing renderer-layout tests**

```python
def test_overall_masterplan_uses_actual_scope_and_context_classes(self):
    svg = renderer.render_all(ROOT)["overall_masterplan"]
    text = svg.read_text(encoding="utf-8")
    self.assertIn('data-context-class="outside_direct_intervention"', text)
    self.assertIn('data-evidence-class="APPROXIMATED_CONTEXT"', text)
    self.assertIn('data-route-envelope="MAIN-IF"', text)

def test_rendered_text_boxes_do_not_overlap_or_clip(self):
    for report in renderer.layout_reports(ROOT):
        self.assertEqual(report["major_overlap_count"], 0, report)
        self.assertEqual(report["clipped_text_count"], 0, report)
```

- [ ] **Step 2: Run tests and verify generic renderer fails**

Expected: FAIL for missing context data attributes and absent layout reports.

- [ ] **Step 3: Implement wrapped notes and collision-aware callouts**

Create text wrapping by measured character budgets, bounded sidebar columns, label candidate positions, occupied-box tracking, leader lines, endpoint callouts, and per-drawing layout metrics. Eliminate unconstrained one-line review notes.

- [ ] **Step 4: Implement view-specific contextual maps**

Regional: context labels and separated relationship bundles. Overall: actual scope shape, context field, intervention mask, route envelope, program/massing, institutional and unresolved context. Mobility and blue-green: destination/intersection sequences. Key plans: actual boundary shape, hierarchy, frontages, section markers, landmarks, and unresolved DZS interface.

- [ ] **Step 5: Render and pass SVG/layout tests**

Run renderer and tests. Expected: seven maps parse, context classes visible, zero major text overlap/clipping in layout report.

- [ ] **Step 6: Commit Task 3**

```powershell
git add --sparse .superpowers/jzoi-v3/gate-b
git commit -m "feat: render contextual JZOI spatial plans"
```

### Task 4: Real Sections, Endpoint Axonometrics, and Physical Landmarks

**Files:**
- Modify: `.superpowers/jzoi-v3/gate-b/test_gate_b.py`
- Modify: `.superpowers/jzoi-v3/gate-b/render_gate_b.py`
- Regenerate: `review/sections.svg`, `massing.svg`, `landmarks.svg`, `components.svg`

**Interfaces:**
- Consumes: section specs, massing footprints/hierarchies, landmark/component operational properties.
- Produces: three transects, three endpoint axonometrics, three landmark elevation/plan studies, and detailed component diagrams.

- [ ] **Step 1: Write failing drawing-type tests**

```python
def test_sections_contain_ground_people_landscape_dimensions_and_plan_ids(self):
    text = (ROOT / "review/sections.svg").read_text(encoding="utf-8")
    for token in ["section-ground", "section-person", "section-landscape", "dimension-range", "ZZY-SECTION-A", "ORG-SECTION-A", "DZS-SECTION-A"]:
        self.assertIn(token, text)

def test_massing_has_three_endpoint_axonometrics_and_landmarks_have_plan_elevation(self):
    self.assertEqual(read_svg("massing").count('data-view="axonometric"'), 3)
    self.assertEqual(read_svg("landmarks").count('data-view="elevation"'), 3)
    self.assertEqual(read_svg("landmarks").count('data-view="plan-axon"'), 3)
```

- [ ] **Step 2: Run tests and verify adjacency bars/logo symbols fail**

Expected: FAIL for missing people-scaled section and physical-object view tokens.

- [ ] **Step 3: Render three plan-linked conceptual transects**

Draw ground profiles, public paths, vegetation/rainwater, building envelopes, active edges, gradients, relative heights, dimension arrows/ranges, and people. Match each title to the plan section feature ID.

- [ ] **Step 4: Render three massing axonometrics**

Project endpoint footprints into oblique axonometric coordinates and extrude by relative hierarchy. Show public gaps, permeability, courtyard voids, public-space enclosure, active frontage, and landmark relation.

- [ ] **Step 5: Render three physical landmark studies and detailed components**

For each landmark show elevation plus plan/axon, person, route, conceptual dimensions, service/information element, night/non-digital states, and maintenance access. Components show section/clearance and public-path relationship rather than icon-only blocks.

- [ ] **Step 6: Render and pass drawing-type/layout tests**

Run renderer and tests. Expected: plan/section/axon distinction present and layout reports remain collision-free.

- [ ] **Step 7: Commit Task 4**

```powershell
git add --sparse .superpowers/jzoi-v3/gate-b
git commit -m "feat: add JZOI sections axons and landmark studies"
```

### Task 5: PNG Export, Image Metrics, and Professional Spatial Review

**Files:**
- Modify: `.superpowers/jzoi-v3/gate-b/test_gate_b.py`
- Create: `.superpowers/jzoi-v3/gate-b/render_review_pngs.py`
- Create: `.superpowers/jzoi-v3/gate-b/professional_spatial_review.py`
- Generate: eleven `.superpowers/jzoi-v3/gate-b/review/*.png`
- Generate: `.superpowers/jzoi-v3/gate-b/professional_spatial_review.json`
- Generate: `.superpowers/jzoi-v3/gate-b/professional_spatial_review.md`

**Interfaces:**
- Consumes: eleven SVGs, local Chrome/Edge executable, Pillow.
- Produces: `render_pngs(root: Path) -> list[Path]`, `image_metrics(path: Path) -> dict`, and `build_professional_review(root, manual_observations) -> dict`.

- [ ] **Step 1: Write failing PNG and qualitative-review tests**

```python
def test_all_review_pngs_are_nonblank_and_match_svg_dimensions(self):
    results = png_renderer.render_pngs(ROOT)
    self.assertEqual({p.stem for p in results}, REQUIRED_REVIEW_STEMS)
    for path in results:
        metrics = png_renderer.image_metrics(path)
        self.assertEqual(metrics["dimensions"], [1400, 900])
        self.assertGreater(metrics["non_background_ratio"], 0.12)
        self.assertGreater(metrics["distinct_color_count"], 12)

def test_professional_review_requires_explicit_observation_for_each_criterion(self):
    report = professional_review.build_review(ROOT, manual_observations={})
    self.assertFalse(report["ok"])
    self.assertIn("missing_manual_observation", {b["code"] for b in report["blockers"]})
```

- [ ] **Step 2: Run tests and verify missing PNG/review modules fail**

Expected: FAIL because exporters and professional review do not exist.

- [ ] **Step 3: Implement deterministic local-browser PNG export**

Detect Chrome then Edge at known Windows locations. Use `--headless --disable-gpu --hide-scrollbars --window-size=1400,900 --screenshot=<png> <file-uri>`. Fail clearly if neither browser exists.

- [ ] **Step 4: Implement Pillow image metrics**

Measure dimensions, background/non-background ratio, distinct quantized colors, content bounding box, edge clipping, and quadrant occupancy. These metrics inform review but do not determine professional PASS alone.

- [ ] **Step 5: Implement explicit professional review schema**

Define overall, key-area, and drawing criteria from the approved spec. Require `status`, `observation`, and `evidence_pngs` for every criterion. Automated metrics attach as evidence only. Missing or RETURN status creates blockers.

- [ ] **Step 6: Export all PNGs and pass automated image tests**

Run PNG exporter and tests. Expected: eleven 1400x900 PNGs, nonblank metrics, no edge clipping.

- [ ] **Step 7: Visually inspect every PNG and record observations**

Open each PNG through the workspace image reader. Record specific observations for context legibility, hierarchy, section/plan correspondence, axon/form clarity, landmark physicality, labels, legends, and blank fields. Re-render any drawing with a visible defect before marking its criterion PASS.

- [ ] **Step 8: Build professional review with explicit manual evidence**

Run `professional_spatial_review.py` using the recorded observations. Expected: `ok: true`, `blocker_count: 0`; report states qualitative judgment is manual and image metrics are supporting evidence.

- [ ] **Step 9: Commit Task 5**

```powershell
git add --sparse .superpowers/jzoi-v3/gate-b
git commit -m "test: add JZOI professional spatial review"
```

### Task 6: Repair Review Package and Final Gate B Verification

**Files:**
- Modify: `.superpowers/jzoi-v3/gate-b/build_review_package.py`
- Modify: `.superpowers/jzoi-v3/gate-b/test_gate_b.py`
- Regenerate: `.superpowers/jzoi-v3/gate-b/gate_b_review_package.json`
- Regenerate: `.superpowers/jzoi-v3/gate-b/gate_b_review_package.md`

**Interfaces:**
- Consumes: spatial model, semantic QA, professional review, SVG/PNG manifests, visual observations.
- Produces: updated 15-topic Gate B repair handoff and review paths.

- [ ] **Step 1: Write failing repair-package tests**

```python
def test_package_requires_semantic_and_professional_review(self):
    package = build_review_package.build_package(ROOT)
    self.assertEqual(package["semantic_qa"]["blocker_count"], 0)
    self.assertEqual(package["professional_spatial_review"]["blocker_count"], 0)
    self.assertEqual(len(package["png_review_artifacts"]), 11)
    self.assertIn("material_spatial_changes", package["repair_report"])
```

- [ ] **Step 2: Run tests and verify current package lacks repair review**

Expected: FAIL for absent professional review, PNG manifest, and material-spatial-change report.

- [ ] **Step 3: Update JSON and Markdown handoff**

Report the 15 requested repair topics: material logic changes, whole-scope explanation, four MAIN-IF reasons, PARALLEL-HUMAN operation, three key-area hierarchies, plan/section correspondence, mobility, blue-green/heritage, massing, landmarks, visual readability, semantic QA, and evidence warnings.

- [ ] **Step 4: Run complete deterministic and regression verification**

Run builder, semantic QA, SVG renderer, PNG renderer, professional review, and package builder twice; compare hashes. Run Gate A tests, Gate B tests, official deterministic/spatial/visual/professional reviews, JSON parsing, SVG parsing, PNG decoding, and Git scope guard.

- [ ] **Step 5: Perform final visual inspection of all eleven PNGs**

Read every final PNG after the last deterministic build. Confirm no major label overlap, note clipping, unexplained blank field, plan/section mismatch, or icon-only landmark representation. If any fails, return to the relevant renderer task.

- [ ] **Step 6: Commit final package**

```powershell
git add --sparse .superpowers/jzoi-v3/gate-b
git commit -m "docs: update JZOI Gate B spatial repair package"
```

- [ ] **Step 7: Stop for Gate B review**

Report the updated review package and all eleven PNG paths. Keep the branch in place; do not enter Gate C, push, or create a PR.
