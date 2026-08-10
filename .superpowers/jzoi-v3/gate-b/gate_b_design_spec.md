# JZOI Gate B Spatial Design Specification

Date: 2026-08-10
Status: approved for implementation by the Gate B instruction

## Scope and freeze

Gate B converts the frozen Gate A evidence and ecosystem framework into spatial design source material. It does not reopen Gate A, alter the six provisional boundaries, change the 25 accepted ecosystem edges, modify the official validator, or generate final A0/A3/HTML/PDF/figure deliverables.

All new geometry is `DESIGN TARGET` and `concept` unless it is an unchanged reference to a frozen Gate A background feature. Provisional key-area edges are study limits, never parcel or road redlines. DZS station anchoring remains an unresolved background relationship.

## Spatial architecture

Gate B uses one canonical JSON model and a set of thematic GeoJSON layers. A deterministic builder generates the spatial layers, review package, and SVG review exports. The internal semantic QA reads the generated files independently and emits machine-readable blocker, warning, and metric results.

Three scales remain distinct:

- Level 1, 43.6 km2: research anchors, Three Areas + Two Wings, background heritage/water/mobility, and typed resource relationships. Physical corridors, service relationships, and schematic ecosystem edges use separate feature classes and visual semantics.
- Level 2, 11.4 km2: a north-south Civic Protocol Spine with east-west public stitches, a distributed program mosaic, mobility hierarchy, blue-green/heritage rooms, projects, landmarks, MAIN-IF, and PARALLEL-HUMAN.
- Level 3: ZZY Controlled Test Yard, ORG Porous Commons, and DZS Urban Switchboard as detailed prototypes within the unchanged provisional study polygons.

## Overall concept

The overall structure is a sequence of three endpoint districts connected by a site-responsive MAIN-IF and backed by a continuous PARALLEL-HUMAN service network. The design replaces four longitudinal land-use bands with smaller corridor, node, edge, and key-area units. East-west stitches connect campus/community/service relationships into the north-south sequence without asserting existing road or parcel conditions.

The Level 1 ecosystem graph is spatialized as service arcs and resource links, never as roads. Gate A research anchors remain background/context evidence with their accepted confidence classes.

## MAIN-IF and PARALLEL-HUMAN

MAIN-IF is a connected public-space route with named gateways, endpoint sequences, public rooms, scenario interfaces, and the three landmarks. It bends through the three key areas rather than following one abstract meridian. Its human-facing length is rounded and labelled approximate.

PARALLEL-HUMAN is a connected, step-free design-intent network linked to staffed HUMAN-DESK locations and Human Review Gates. It supports non-digital access and bypasses controlled testing zones. Service-distance coverage is reported as a design-intent calculation against conceptual geometry, not as verified accessibility.

## Key areas

ZZY uses a safety-gradient plan: ordinary public movement at the edge, observation and human review on the public/testing interface, a controlled central test yard, separate logistics/emergency access, a closed cycle test loop, rainwater buffers, and a physical emergency-stop rail. Concept massing frames the yard without claiming existing buildings.

ORG uses a four-direction permeability lattice. A civic commons crosses research, translation, prototype, startup, talent, and neighborhood-service clusters. Courtyard massing, active ground-floor frontages, and public-to-controlled gradients preserve a readable campus-city interface while keeping station/campus links at design-intent or background status.

DZS uses a public switchboard spine with pedestrian convergence, cycling, procurement/adoption, enterprise services, consent, appeal, culture, international/talent services, and non-digital fallback. The plan stays inside PROV-KEY-003. The station is represented only as an unresolved background relationship linked by a dashed schematic interface, not a physical connection or entrance.

## Layer contract

Generated GeoJSON layers include:

- `regional_ecosystem.geojson`: anchors, wings, endpoint nodes, physical corridors, service/resource relationships, and schematic ecosystem edges.
- `overall_structure.geojson`: MAIN-IF, PARALLEL-HUMAN, east-west stitches, gateways, public rooms, service nodes, and landmarks.
- `land_use_program.geojson`: design-intent program units with role, activities, project refs, ecosystem refs, confidence, and status.
- `mobility.geojson`: background mobility evidence, proposed streets, pedestrian, cycle, logistics, emergency, and unresolved station relationships.
- `blue_green_heritage.geojson`: frozen background references and proposed rainwater, ecology, heritage/public-room, walking, and cycling design.
- `massing.geojson`: concept buildings and massing envelopes with frontage, permeability, relative height hierarchy, and no statutory claims.
- `zzy_plan.geojson`, `org_plan.geojson`, `dzs_plan.geojson`: detailed prototype objects, paths, gradients, programs, boundaries, and safety/interface features.
- `landmarks.geojson` and `components.geojson`: three endpoint landmarks and the five required component families.
- `project_spatial_basis.geojson`: precise or network geometry refs for P01-P12 without using whole land-use districts as small-project geometry.

Every generated feature has a unique ID, semantic class, evidence class, design status, geometry role, host scope, and project/scenario references where applicable.

## Massing and public realm

Massing uses `concept_building`, `concept_massing`, `new_design_volume`, or `existing_unknown`. No generated object is called retained or renovated. Relative envelopes use `low`, `medium`, `tall`, and `landmark` hierarchy labels rather than statutory heights. Courtyards, active edges, passages, buffers, and skyline roles are encoded as properties and geometry relationships.

Landmarks are physically distinct: a ZZY Safety Gantry, ORG Open Bracket, and DZS Civic Switch. Each records form, scale concept, interaction, accessibility intent, non-digital state, day/night state, maintenance, VI relationship, and endpoint identity.

IF-MARK, CONSENT-POST, HUMAN-DESK, TEST-RAIL, and QUIET-BEACON each record conceptual dimensions, clearances, state, information hierarchy, path relationship, hosts, and scenarios.

## Project closure

P01-P12 receive host areas, intervention types, dependencies, scenarios, and one or more valid feature references. Linear and distributed projects use MultiLineString, MultiPolygon, or multiple feature references where appropriate. Gate B establishes spatial basis only; it does not finalize the project/phase registry.

## Semantic QA

The internal QA checks geometry validity, applicable containment, global ID uniqueness, reference existence, project/geometry and scenario/host consistency, road/building collisions, public-path continuity, MAIN-IF and PARALLEL-HUMAN network validity, land-use/massing compatibility, green semantic classes, key-area containment, duplicate or contradictory geometry, loop naming, and provisional/background/design separation.

Expected exceptions must be explicit in feature semantics; they cannot suppress actual blockers. The Gate B stop condition is zero blockers. Warnings may remain only for evidence-dependent limitations already declared by the model.

## Review outputs

The review package contains `gate_b_review_package.md`, `gate_b_review_package.json`, `gate_b_semantic_qa.json`, canonical/generated spatial data, and intermediate SVG exports for overall structure, overall masterplan, mobility, blue-green/heritage, each key area, sections, massing, landmarks, and components. These are internal review artifacts, not final boards or publication outputs.

## Verification and stop

Builder tests fail first for required layer contracts and QA behavior, then pass after implementation. Verification includes unit tests, deterministic rebuild comparison, JSON/GeoJSON parsing, SVG XML parsing, geometry and semantic QA, and a worktree check proving no final A0/A3/HTML/PDF/figure or official-validator changes.

After all required representations exist and semantic QA reports zero blockers, Gate B stops for review. Gate C, final registry work, final deliverables, push, and PR creation remain out of scope.
