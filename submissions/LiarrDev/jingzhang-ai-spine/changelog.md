# 方案迭代记录

## v1.7 - 2026-08-20

### Visual presentation overhaul (5 figures + visual/index.html)
- Redesigned all 5 SVG figures with richer data visualization, professional design system (brand colors #1B3A6B / #C07A3A / #2e7d32), gradients, filters, bilingual labels, and evidence chain annotations:
  - site-overview: master concept map with legend, area statistics, design concept, and evidence chain
  - land-use-structure: three-tier scope framework, key area breakdown chart, spatial control metrics, and renewal strategy ratios
  - key-areas: three-column card layout for Zhongzhiyuan, AI Origin Community, and Dazhongsi with spatial structure, AI scenarios, and demolition-renovation-retention ratios
  - mobility-bluegreen: composite mobility and blue-green public space map with four-tier road classification, slow-mobility loop, and rail station TOD details
  - metrics-evidence: design scope hierarchy, key area decomposition, spatial metrics, data pipeline, task coverage matrix, and self-check status
- Rewrote visual/index.html with enhanced visual presentation: brand mark SVG, stats bar, inline charts (area breakdown, demolition-renovation-retention ratio), progress bars, scroll-triggered fade-in animations, image lightbox, back-to-top button, and navigation highlight tracking
- Created matching English versions (5 .en.svg files + visual/index.en.html) with all text translated to English, preserving all data values, colors, and layout

### Manifest update
- Added 10 SVG source files to manifest.json (5 zh + 5 en)
- Updated SHA256 hashes for all 22 changed files (10 SVGs, 10 PNGs, 2 HTML)

## v1.6 - 2026-08-20

### Taskbook review-dimension alignment
- Brand identity (brand_identity): expanded the logo direction into a full brand identity system — logo graphic (three variants), color system with per-district accents, typography, international-communication vocabulary, and application extension; added assets/identity/spine-mark.svg
- Regional synergy (regional_synergy): added external regional coordination paragraph (Beiwei Community, Future Science City, Huairou Science City, Beijing E-Town, Beijing-Tianjin-Hebei)
- Long-term operations value (long_term_operation_value): added 90-day minimum operations validation, three evaluation gates, brand asset accumulation loop, and open-source reuse channel
- Transferability (transferability): added layered transferable-deliverables list (branding / urban-design / event-operations / technical teams)

### Bilingual sync
- proposal.en.md synced with all four new sections

## v1.5 - 2026-08-20

### Real existing-condition geometry (OSM data)
- geometry/buildings.geojson: replaced 5 placeholder design-proposal footprints with 1,692 real OSM building footprints (existing_condition, source_type=osm), clipped to site boundary
- geometry/roads.geojson: replaced 5 placeholder road segments with 1,605 real OSM highway segments
- geometry/green_space.geojson: replaced 1 placeholder polygon with 120 real OSM green/water polygons
- geometry/land_use.geojson: retained the design-proposal land-use partition (must fully cover site boundary per spatial review)
- Data fetched via Overpass API on 2026-08-20, licensed ODbL, registered as source OSM-DATA in sources.json

### Metric recalculation (EPSG:4548)
- building_footprint_area_sqm: 303,555.838 → 2,018,037.155 (existing building footprint)
- building_count: 5 → 1,692
- road_segment_count: 5 → 1,605
- green_ratio: 0.123423 → 0.079978 (existing green space ratio)
- Added green_space_area_sqm: 912,777.815

### Proposal narrative sync
- proposal.md / proposal.en.md: updated building/road/green figures to reflect OSM existing-condition data, with explicit "directional reference, OSM coverage incomplete" boundary declarations

## v1.4 - 2026-08-20

### Verifiability (mutation testing + runnable verifier)
- simulation.json: upgraded to version 2 with 4 named assertion types (hard_stop_triggered_correctly / human_review_enforced / recovery_evidence_required / data_disposal_or_exit_verified), 44 assertions across 12 tasks, and 5 mutation tests that inject violations (missing human review, downgraded high-risk, missing rollback, personal trajectory collection, coordinates in concept) and verify the proposal's mechanisms intercept them
- simulation.json: added boundary_statement declaring what the offline simulation proves and does not prove
- visual/assets/verify_spine.js: runnable Node.js verifier (17/17 checks pass) validating risk.json / spatial.json / simulation.json / metrics.json structural consistency offline
- visual/assets/review_evidence.json: evidence summary with per-item "proves / does not prove" declarations across 7 evidence categories

### Proposal narrative structure (taskbook alignment + readability)
- proposal.md: added "Read Me in Three Minutes" section answering the five reviewer questions (what / how to implement / who benefits / how AI integrates / risks and boundaries)
- proposal.md: added Six Agent Task Response Map (agent.1 through agent.6) with per-task proposal response and core evidence
- proposal.md: added Policy Chain Alignment table (national → municipal → district, three levels) with wording boundaries
- proposal.md: added R-01 through R-08 risk index numbering with cross-chapter back-referencing
- proposal.en.md: synced all new sections with English translations

### Evidence and narrative depth
- report/narrative.md: expanded from placeholder to substantive formal narrative (core concept, three-layer cultural progression, implementation phasing, restraint boundaries)
- design_depth_matrix.json: strengthened 5 evidence_summary_zh entries to declare what each proves and does not prove

### Manifest
- 2 new files registered (visual/assets/verify_spine.js, visual/assets/review_evidence.json)
- SHA256 hashes recalculated for 7 modified files

## v1.3 - 2026-08-20

### Structured deliverables (scoring enhancement)
- Added risk.json: 8-dimension structured risk matrix with scores, mitigation measures, and human review requirements for high-risk dimensions (implementation_complexity=4, policy_uncertainty=4)
- Added spatial.json: 13 concept-level spatial items (6 nodes, 4 corridors, 3 areas) with geometry.mode=concept, linked to proposal scenarios
- Added simulation.json: 12 verification tasks with 33 assertions (all pass), covering scenario, persona, landmark, case, project, risk, spatial, and metric validation

### Proposal enhancement (7 scoring dimensions)
- proposal.md: added AI Scenario Data-Governance Audit Table (12 scenarios with data source, privacy boundary, AI role, human review, automation level)
- proposal.md: added Public Interest and Inclusion Safeguards section (vulnerable groups, public participation, non-AI professional accessibility)
- proposal.md: added Verifiable Pilot Pathways and Stakeholders table (4 pilot projects with entry conditions, acceptance gates, rollback conditions)
- proposal.md: added Structured Risk Matrix section referencing risk.json and simulation.json
- proposal.en.md: synced all new sections with English translations

### Manifest
- 3 new files registered in manifest.json (risk.json, spatial.json, simulation.json)
- SHA256 hashes recalculated for all modified files

## v1.2 - 2026-08-20

### Visual interactivity
- visual/index.html: added smooth scroll navigation, scroll-triggered fade-in animations (IntersectionObserver), image lightbox viewer, back-to-top button, and nav active highlighting
- visual/index.en.html: synced all interactivity features with Chinese version

### Proposal depth
- proposal.md: expanded Land Use section with retain-renovate-demolish ratio estimates and 5 building strategy details
- proposal.md: expanded Transport section with road classification system and public service facility allocation per key area
- proposal.en.md: synced all expanded content with English translation

## v1.1 - 2026-08-20

### Fixes
- Land use code 05 (湿地) corrected to 09 (商业服务业用地) per upstream enum update
- self_check.json schema_version aligned from 0.1.0 to 0.2.0
- Bilingual frontmatter tracks synced (proposal.en.md had 5 tracks, now matches proposal.md's 3)
- Unified blue-green metaphor to "工字形" in both zh and en versions
- Visual index.html metric display: green_ratio and public_space_ratio now show 12.34%/7.33% consistently (was 12.3%/7.3% in cards vs 12.34%/7.33% in table)

### Geometry enrichment
- buildings.geojson: expanded from 1 feature to 5, with building_strategy tags (retain/renovate/renew/new)
- roads.geojson: expanded from 1 LineString to 5, including slow-mobility spine, station connection, east-west connector, and blue-green loop
- constraints.geojson: filled from 0 features to 3, adding heritage protection zone, railway corridor buffer, and TOD influence area

### Audit matrices
- design_depth_matrix.json: each of 15 items now has differentiated evidence (proposal_sections, geometry_refs, metric_refs, evidence_summary_zh)
- compliance_matrix.json: each of 23 requirements now has per-requirement evidence mapping
- standard_matrix.json: data_gap item evidence_summary corrected to acknowledge the gap

### Visual
- visual/index.en.html: fully translated from Chinese to English (was a byte-for-byte copy)
- 5 English figure PNGs regenerated with all-English text (were identical MD5 copies of Chinese versions)
- 2 English PDFs (a3-booklet.en.pdf, a0-boards.en.pdf) regenerated with English content and embedded English figures
- cover_image field added to manifest.json with assets/media/cover.jpg as media_poster

### Metrics
- metrics.json: expanded from 6 to 15 metrics (added key area areas, building count, road segments, scenario count)
- visual/index.html: metrics display unified to 12.34%/7.33% across cards and table

### Manifest
- All SHA256 hashes recalculated for modified files
- cover_image field and media_poster file entry added
- manifest.json entry excluded from SHA256 (circular dependency)

## v1.0 - 2026-08-10

### Initial submission
- Bilingual proposal (proposal.md / proposal.en.md)
- 9 GeoJSON layers, 5 design figures, A3/A0 PDFs
- Offline interactive visualization page
- Complete evidence chain with 4-gate self-check
- Passed CI and merged via PR #1349
