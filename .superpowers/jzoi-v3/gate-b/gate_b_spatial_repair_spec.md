# JZOI Gate B Professional Spatial Repair Specification

Date: 2026-08-10
Status: approved for implementation

## Purpose

Repair the professional spatial-design quality of the accepted Gate B package without reopening Gate A, replacing the Gate B architecture, inflating feature counts for appearance, or entering Gate C. The repaired review outputs must read as urban-design drawings rather than connected graphs, program bars, or graphic symbols.

## Frozen Contract

- Preserve all six provisional boundaries and accepted evidence classifications.
- Preserve the 25 typed ecosystem edges and their DESIGN TARGET status.
- Preserve JZOI, Civic Protocol Modernism, MAIN-IF, PARALLEL-HUMAN, Three Areas + Two Wings, endpoint identities, P01-P12 references, three landmark identities, and five component families.
- Do not invent parcels, existing buildings, ownership, station entrances, road redlines, statutory heights, FAR, parking, utilities, water boundaries, or implementation readiness.
- Keep the current semantic QA checks and zero-blocker requirement.
- Generate only internal Gate B review artifacts and PNGs, never final competition outputs.

## Overall Context Base

Create `overall_context.geojson` as the Level 2 base. It references the unchanged provisional site boundary and accepted Gate A context features. It distinguishes `OBSERVED_PUBLIC_DATA`, `APPROXIMATED_CONTEXT`, `SCHEMATIC_INFERENCE`, `DATA_GAP`, and `DESIGN TARGET` through explicit properties and drawing styles.

The layer includes the actual provisional scope outline, accepted heritage/water/road/institution/station/community context, three unchanged provisional key-area outlines, a derived direct-intervention envelope, and an `intentionally_outside_direct_intervention` remainder. The remainder is a design communication mask derived from the provisional scope and proposal geometry, not a parcel, land-use, ownership, or implementation claim.

The overall drawing uses this base to explain the entire 11.4 km2 field. Large areas outside direct intervention remain visible as context-managed urban fabric rather than blank canvas.

## MAIN-IF

Retain `MAIN-IF-01..04` and their connected order. Replace two-point chords with multi-vertex, site-responsive concept alignments that address DZS civic convergence, the heritage/public sequence, ORG commons/campus relationship, blue-green crossings, ZZY public observation, and north/south gateways.

Each segment records:

- `spatial_anchor_refs`
- `context_reason`
- `public_space_type`
- `adjacent_program_refs`
- `crossing_condition`
- `gateway_role`
- `alignment_status`
- `corridor_width_range_m`
- evidence/design status

The review renderer draws a broad translucent corridor envelope behind the concept centerline. The centerline is not a road or precise construction alignment.

## PARALLEL-HUMAN

Retain the connected four-segment backbone required by semantic QA, but represent it as a staffed service network rather than a second route line. Add only the minimum branch and catchment objects needed to show:

- HUMAN-DESK and Human Review Gate relationships
- accessible approaches and crossings
- controlled-area bypasses
- ordinary public-realm connections
- conceptual staffed-service catchments

Catchments use DESIGN INTENT and cannot claim complete accessibility or verified service distance.

## Key-Area Spatial Form

Reshape existing features instead of multiplying them.

ZZY becomes a coherent controlled-test place: a non-rectangular central yard, public observation terrace, ordinary bypass, staffed review threshold, service/logistics gate, emergency route, rainwater/ecology edge, support frontages, public room, landmark, and visible section line. TEST-RAIL and the safety gradient remain physically legible.

ORG becomes a porous urban fabric: a primary commons, linked secondary courts, narrow passages, courtyard/block edges, active frontages, research/translation/prototype/startup sequence, neighborhood and talent services, landscape rooms, and clear public/shared/controlled gradients. Four-direction permeability is expressed in void and block form.

DZS becomes an independent civic switchboard: a central public room, converging public paths, consent/appeal/adoption/enterprise/culture/talent edges, cycle connection, staffed fallback, and Civic Switch landmark. The unresolved station relation remains outside the core as a dashed question interface with no entrance or physical-link claim.

## Sections and Plan Correspondence

Retain `ZZY-SECTION-A`, `ORG-SECTION-A`, and `DZS-SECTION-A` as visible plan cuts. Add conceptual section properties for width ranges, relative height hierarchy, public/controlled gradients, landscape, active frontage, and people-scale use.

The `sections.svg` drawing renders three real transects with ground lines, paths, planting/rainwater, building envelopes, active edges, functions, dimension ranges, people, and section identifiers matching the plan.

## Massing and Axonometrics

Retain exactly 18 massing features. Reshape them into L, U, courtyard, bar, and gateway forms with explicit urban-form properties:

- `block_type`
- `public_gap_refs`
- `permeability_refs`
- `active_frontage_edges`
- `public_space_enclosure`
- `landmark_relation`
- relative height hierarchy

The massing review drawing becomes three endpoint axonometric studies derived from the same footprints and relative heights. No existing-building or statutory-height claim is introduced.

## Physical Landmarks

Retain Safety Gantry, Open Bracket, and Civic Switch. The landmark drawing shows for each:

- conceptual elevation
- plan or axonometric view
- person and path for scale
- approximate design dimensions
- information/service element
- non-digital state
- day/night state
- maintenance access

The forms remain endpoint-specific urban objects, not logos.

## Drawing System and PNG Review

Replace the generic one-size map renderer with view-specific compositions for regional structure, overall masterplan, mobility, blue-green/heritage, key-area plans, sections, endpoint axonometrics, landmarks, and components.

Use the actual provisional scope geometry for map frames. Add wrapped sidebar notes, controlled label callouts, collision-aware label placement, endpoint titles, section markers, scale references, and legends limited to visible classes.

Export every required SVG to PNG using local Chrome or Edge in headless mode. Use Pillow to verify dimensions, nonblank pixels, color variation, and excessive blank-field ratios. Then visually inspect all eleven PNGs and record explicit reviewer observations.

## Professional Spatial Review

Add a separate `professional_spatial_review.json` and `.md`. It does not replace semantic QA and does not derive PASS from file existence, feature count, SVG size, geometry validity, or network connectivity.

The checklist records explicit qualitative decisions for:

- overall context/geographic legibility
- whole-scope explanation
- site-responsive route logic
- each key area's hierarchy, circulation, adjacency, gradient, public-space form, and plan/section correspondence
- drawing readability, non-empty spatial information, plan/section/axon distinction, blank-field control, and physical landmark legibility

Automated image metrics are evidence inputs only. Final checklist status requires direct review of rendered PNGs.

## Verification and Stop

Gate B repair stops only when:

- all current semantic QA checks still report zero blockers;
- all eleven SVGs and PNGs exist and parse;
- plan-linked sections and endpoint axonometrics are present;
- no major label/note collision or clipping remains on visual inspection;
- the overall 11.4 km2 field has no unexplained blank region;
- the professional spatial review records explicit PASS decisions with observations;
- frozen boundaries, Gate A, official validators, and final deliverables remain unchanged.

Then stop for Gate B review. Do not enter Gate C, push, create a PR, or generate final competition outputs.
