# JZOI Gate A Revision Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task with review checkpoints.

**Goal:** Build and audit the research/data layer for the existing JZOI proposal from the latest canonical `upstream/main`, without changing the proposal slug, moving provisional boundaries, or entering Gate B.

**Architecture:** Keep the official submission package contract authoritative. Use internal build registries for projects, scenarios, actors, ecosystem cases, landmarks, components, and professional maturity; generate only contract-compatible official artifacts from them. Preserve the repository provisional polygons by reference and express OSM/public-POI material as background context or source-conflict evidence, never as boundary corrections.

**Tech Stack:** Git, Python 3 standard library plus repository review dependencies, GeoJSON, JSON, Markdown, existing repository validators. No validator modifications, no remote visual assets, no final A0/A3 regeneration in Gate A.

## Global Constraints

- Base branch must be the successfully fetched canonical `upstream/main` and must include merge commit `5e30bfce1a5b7ee719987a8bfd179e5b317860f5`.
- Revision branch must be `revision/SharkyyIvy/jingzhang-open-interface-v3`.
- Reuse slug `jingzhang-open-interface`; do not create a new proposal slug.
- Preserve `PROV-RESEARCH-001`, `PROV-SITE-001`, and `PROV-KEY-001..003` geometry and coordinates exactly.
- OSM, Overpass, and public POI evidence is `BACKGROUND` context only and cannot modify any provisional boundary.
- Do not modify official validators, `data/source_registry.json`, `submissions-data.js`, other submissions, A0, or A3 during Gate A.
- Internal registries are build artifacts under `.superpowers/jzoi-v3/` unless the latest package contract provides a legal role and preflight accepts them.
- Unknown facts remain unknown; provisional and agent-generated design must never be written as existing conditions.
- Stop after Gate A Review Package and report all conflicts and remaining uncertainty.

---

### Task 1: Verify canonical branch and baseline contract

**Files:**
- Modify: none
- Test: Git ancestry and package presence checks

- [ ] **Step 1: Verify fetched refs and branch ancestry**

Run:

```powershell
git fetch upstream main
git switch revision/SharkyyIvy/jingzhang-open-interface-v3
git merge-base --is-ancestor 5e30bfce1a5b7ee719987a8bfd179e5b317860f5 upstream/main
git rev-parse HEAD upstream/main
```

Expected: fetch succeeds, `HEAD` equals `upstream/main`, and the merge-base command exits successfully.

- [ ] **Step 2: Confirm merged JZOI exists on the base**

Run:

```powershell
git cat-file -e HEAD:submissions/SharkyyIvy/jingzhang-open-interface/manifest.json
```

Expected: both paths exist on the fetched base.

- [ ] **Step 3: Record baseline in `changelog.md`**

Record the branch, base SHA, merge commit, current package state, latest canonical rule SHA, and the four baseline validator results. Do not alter the submission slug.

- [ ] **Step 4: Commit the synchronization record and plan**

```powershell
```

### Task 2: Build source and assumption contracts

**Files:**
- Create: `.superpowers/jzoi-v3/sources.json`
- Create: `.superpowers/jzoi-v3/assumptions.json`
- Create: `.superpowers/jzoi-v3/source_aliases.json`
- Modify: `submissions/SharkyyIvy/jingzhang-open-interface/changelog.md`

- [ ] **Step 1: Define source classes and aliases**

Every record must include `registry_source_id`, `submission_source_id`, publisher, URL or local path, publication/retrieval date, collection method, spatial/temporal coverage, license, transformations, and known limitations. Map repository aliases such as `DATA-SRC-*`, submission aliases, `SRC-*`, and standard IDs without deleting the original IDs.

- [ ] **Step 2: Register background context inputs**

Register only publicly traceable context layers for rail/heritage park, roads, rail stations, rivers, campuses, research/industry anchors, public services, and public open space. Mark OSM/Overpass/POI inputs as `BACKGROUND` and preserve their ODbL or source-specific constraints.

- [ ] **Step 3: Register data gaps and source conflicts**

Record the `PROV-SITE-001` / OSM park conflict and `PROV-KEY-003` station-anchor uncertainty as unresolved conflicts. Do not change source geometry.

- [ ] **Step 4: Run source-contract checks**

Run the repository source validator and a zero-write JSON schema/alias check against `.superpowers/jzoi-v3`. Expected: all IDs resolve within the build contract, no source is silently promoted to formal, and all conflicts remain explicit.

### Task 3: Build three-scope and existing-conditions evidence

**Files:**
- Create: `.superpowers/jzoi-v3/scope_registry.json`
- Create: `.superpowers/jzoi-v3/existing_conditions.json`
- Create: `.superpowers/jzoi-v3/existing_conditions.geojson`
- Create: `.superpowers/jzoi-v3/context_conflicts.json`

- [ ] **Step 1: Map logical scopes to existing source geometry**

Use these mappings without redrawing polygons:

```json
{
  "RESEARCH-SCOPE-001": "brief/site-package/geometry/provisional_boundaries.geojson#PROV-RESEARCH-001",
  "OVERALL-DESIGN-001": "brief/site-package/geometry/provisional_boundaries.geojson#PROV-SITE-001",
  "KEY-AREA-SCOPE-ZZY": "brief/site-package/geometry/provisional_boundaries.geojson#PROV-KEY-001",
  "KEY-AREA-SCOPE-ORG": "brief/site-package/geometry/provisional_boundaries.geojson#PROV-KEY-002",
  "KEY-AREA-SCOPE-DZS": "brief/site-package/geometry/provisional_boundaries.geojson#PROV-KEY-003"
}
```

- [ ] **Step 2: Create existing-condition features**

Use points, corridors, and approximate public-data-derived layers for rail, park, rivers, roads, rail stations, universities, research institutions, industry/enterprise context, communities, public services, open spaces, heritage resources, Five Ring connection, and the school/station/river/industrial interfaces. Each feature must disclose precision, confidence, source IDs, and whether it is observed, contextual, inferred, or unresolved.

- [ ] **Step 3: Separate diagnosis from gaps**

`existing_conditions.json` must state observed spatial diagnoses such as discontinuous interfaces, access barriers, fragmented public realm, and missing public-facing transition spaces. `context_conflicts.json` must separately list missing official boundaries, station/POI discrepancies, unverified ownership, missing traffic counts, missing parking, missing utilities, missing heritage drawings, and other professional gaps.

- [ ] **Step 4: Run Gate A spatial provenance checks**

Confirm every new geometry has a source or assumption chain and that no feature claims official boundary status. Do not run or generate any final A0/A3 output.

### Task 4: Build three areas + two wings and AI ecosystem registries

**Files:**
- Create: `.superpowers/jzoi-v3/ecosystem_cases.json`
- Create: `.superpowers/jzoi-v3/ecosystem_registry.json`
- Create: `.superpowers/jzoi-v3/areas_wings_coordination.json`
- Create: `.superpowers/jzoi-v3/ecosystem.geojson`

- [ ] **Step 1: Register 5-8 global AI ecosystem cases**

Use cases covering university research, startup formation, capital/IP, compute/data, open source, testing, procurement/adoption, enterprise scaling, talent, and mixed innovation districts. For each case include the required structured fields, source metadata, transferable principle, rejected copy, and known limitations. Do not invent local company counts, capital, compute, or talent data.

- [ ] **Step 2: Register the three areas**

Retain the taskbook area IDs and map each to its endpoint role: ZZY Controlled Test Yard, ORG Porous Commons, and DZS Urban Switchboard. Each area must reference its logical scope and source provisional geometry.

- [ ] **Step 3: Register the two wings**

Define the Zhongguancun technology-service wing as a service flow for IP, law, standards, capital, startup support, international resources, technical services, compute, talent, and enterprise growth. Define the Xiaoyuehe scenario-empowerment wing as public-life, ecological, community, mobility, robotics, and AI public-service testing-to-adoption contexts.

- [ ] **Step 4: Build the coordination loop**

Represent the loop as explicit directed relationships: university/research → open source/prototype → ZZY testing → human review → ORG translation → Xiaoyuehe scenario → DZS adoption/procurement → Zhongguancun services/capital/IP → scaling → international network → exit/feedback.

- [ ] **Step 5: Build the eight-element mechanism table**

For `LAND`, `SPACE`, `INDUSTRY`, `CAPITAL`, `TALENT`, `COMPUTE`, `DATA`, and `SCENARIO`, record current observed evidence, unknowns, design targets, future monitoring KPIs, spatial hooks, responsible actors, and evidence limitations.

### Task 5: Produce Gate A Review Package and self-audit

**Files:**
- Create: `.superpowers/jzoi-v3/gate_a_review_package.json`
- Create: `.superpowers/jzoi-v3/gate_a_review_package.md`
- Create: `.superpowers/jzoi-v3/gate_a_self_audit.json`
- Modify: `submissions/SharkyyIvy/jingzhang-open-interface/changelog.md`

- [ ] **Step 1: Assemble the requested twelve review sections**

Include branch/base, all new sources, scope mapping, existing-condition diagnosis, data-gap diagnosis, three-areas/two-wings model, case matrix, eight-element map, metric-state table, geometry provenance, self-audit, and unresolved conflicts.

- [ ] **Step 2: Enforce Gate A stop conditions**

The self-audit must fail if any provisional polygon moved, any background source is used as a boundary, any existing condition lacks provenance, any requested area/wing/case/element is absent, or any unknown is represented as an observed fact. It must also assert that no final A0/A3 files changed during Gate A.

- [ ] **Step 3: Run verification**

Run JSON parsing, source/alias checks, scope-reference checks, provenance checks, and the existing official deterministic/spatial/visual/professional checks against the unchanged official package. The official checks are baseline evidence only; Gate A acceptance depends on the custom audit.

- [ ] **Step 4: Commit Gate A artifacts only**

```powershell
git commit -m "feat: add JZOI Gate A research evidence package"
```

Stop and report the Gate A Review Package. Do not proceed to Gate B, generate final A0/A3, push, or create a PR until the user reviews it.
