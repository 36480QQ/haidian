---
title: "Bio-Physarum Mobility Network Renewal for the Dazhongsi AI Industry Cluster"
author_github: "927420095-bot"
language: "en"
translation_of: "proposal.md"
proposal_format_version: "2"
bilingual_contract_version: "1"
license: "COMMUNITY-DISPLAY-ONLY"
summary: "A differentiated road-network renewal concept for the Dazhongsi AI industry cluster built on the bio-Physarum adaptive network (Tero et al. 2007) and NSGA-II multi-objective optimization. Formal geometry uses a conceptual network inside the provisional boundary; the real Physarum run (167-edge network, optimal efficiency 19.20, zero heritage crossings) is presented as method-validation evidence, never as redline or approval geometry."
tracks: ["ai-traffic-walkability", "enterprise-services-ecosystem", "civic-agent-governance"]
scenarios: ["ai-traffic-walkability", "enterprise-service-copilot", "public-safety-operations-review"]
---

# Bio-Physarum Mobility Network Renewal for the Dazhongsi AI Industry Cluster

## Design Basis and Source List

This formal proposal takes the official pre-qualification announcement for the Centennial Jing-Zhang AI Innovation Belt urban design international competition, issued by the Haidian Branch of the Beijing Municipal Commission of Planning and Natural Resources, as its first basis, and the maintainer-registered provisional rough boundary, key areas, enums, metrics, and source list under `brief/site-package/` as its machine-readable basis. Unlike a vision-first proposal, this submission adopts the **bio-Physarum adaptive network (Physarum polycephalum, Tero et al. 2007)** and **NSGA-II multi-objective evolutionary optimization** as the core method, translating the natural principle of "growing an efficient, robust, low-crossing network from anchors" into a road-network renewal strategy [source:AGENT-TASKBOOK] [depth:existing_conditions_diagnosis].

The primary method references and their relationships are as follows: the physical method draws on the Physarum adaptive-network paper and reviews, the optimization method draws on standard multi-objective evolutionary algorithm implementations, and the design judgment returns to the announcement, the agent taskbook, the enums, and the scope list under `brief/site-package/`; source completeness is stored in `sources.json` and not repeated as machine indices in prose [source:SITE-PACKAGE] [source:SOURCE-REGISTRY].

The usage boundary of the source register is as follows [source:SOURCE-REGISTRY]:

- `brief/site-package/design_brief.json`, `allowed_design_space.json`, `enums/`, and `ranges/` provide the allowed design space and enums.
- `data/processed/agent_fact_pack.md` is a reading-navigation layer for this proposal, not a new authority source [source:PROCESSED-FACT-PACK].
- `data/processed/project_scope_summary.csv`, `agent_task_requirements.csv`, and `missing_data_checklist.csv` establish the task, scope, source-use, and gap lists.

![Evidence chain and package relationship](assets/figures/site-overview.en.png)

**Honest statement on boundary and coordinates (method-first)**. The formal geometry layers (`geometry/*.geojson`) of this submission use the provisional boundary from `brief/site-package/geometry/provisional_boundaries.geojson` and generate a **conceptual network** (`agent_generated_design`) within it. The real Physarum + NSGA-II network the author previously produced (167 edges, optimal efficiency 19.20, zero heritage crossings) lies roughly 2–3 km to the west and overlaps the provisional site boundary by only about 140 m; a direct clip would discard roughly 95% of the real network. To avoid coordinate translation or fabrication, this proposal adopts a **method-first** approach: the real Physarum result enters the figures, `sources.json`, and prose as **method-validation evidence**, not as formal geometry, not as a redline, and not as approval basis [data:geometry/site_boundary.geojson#SITE-001] [metric:site_area_sqm].

The scorable state of this submission is: **provisional boundary, retaining a precision caveat and awaiting recalculation after official data is published; this does not block content scoring**. All spatial structures, scenarios, projects, and metrics are written on a "discussable, reviewable, and recalibratable after official boundary replacement" basis.

## Three-Level Scope Framework

The proposal is organized along the three levels defined by the announcement: the coordinated research area addresses the 43.6 km² AI industry ecosystem, strategic positioning, innovation chain, and future urban form; the overall design area addresses the roughly 11.4 km² urban area and industry district 1–2 km around the Jing-Zhang heritage park, requiring an urban renewal framework, industrial spatial layout, transport-municipal support, and urban character control; the key-area scope addresses the 368.4-hectare three detailed-design areas, requiring functional program, building scale, retain-renovate-demolish classification, public-space connectivity, and transport organization. The three levels are mapped item-by-item in `compliance_matrix.json` [depth:three_level_scope_framework] [depth:overall_spatial_structure].

The depth items of the three-level framework are constrained by [depth:three_level_scope_framework] and [depth:overall_spatial_structure], the spatial evidence is anchored to [data:geometry/site_boundary.geojson#SITE-001] and [data:geometry/key_areas.geojson#PROV-KEY-001], and the task basis is anchored to [standard:PROJECT-OFFICIAL-ANNOUNCEMENT].

![Three-level scope and spatial structure](assets/figures/land-use-structure.en.png)

The overall concept proposed here is the "**intelligent-vein symbiotic belt**": the Physarum adaptive-network method is the "growth algorithm", the Jing-Zhang heritage park is the historical and public-space spine, the three key areas (Zhongzhiyuan, Beijing AI Origin community, Dazhongsi) are the "nutrient anchors", and universities, enterprises, communities, and transit stations form the everyday network, producing a "one-belt three-core, multi-level network, blue-green slow composite ring" spatial organization. The "belt" is not a newly drawn redline but a translation of the announcement's three-level scope into a working method; the "three cores" correspond to the three key areas; the "multi-level network" corresponds to the Physarum primary-vein / branch / slow-loop / green-corridor hierarchy.

| Level | Design question | Proposal answer | Data landing |
| --- | --- | --- | --- |
| Coordinated research area | How to organize the AI ecosystem and future urban form | Build an "university-origination, open-source collaboration, enterprise conversion, public experience, international communication" innovation chain | compliance_matrix.json, standard_matrix.json |
| Overall design area | How to map industrial space, urban renewal, transport-municipal, and character | Land use, buildings, conceptual network, green space, public space, and phasing layers jointly express it | [data:geometry/land_use.geojson#LU-001], [data:geometry/roads.geojson#ROAD-001] |
| Key-area scope | How the three areas reach detailed-design depth | Propose positioning, spatial actions, AI scenarios, and implementation dependencies respectively | [data:geometry/key_areas.geojson#PROV-KEY-001], [data:geometry/key_areas.geojson#PROV-KEY-002], [data:geometry/key_areas.geojson#PROV-KEY-003] |

## Coordinated Research Area: Industry and Future City Research

The core task of the coordinated research area is to build a world-class AI innovation ecosystem. The proposal surveys Haidian's universities and institutes, leading enterprises, computing/algorithm/data-element resources, incubation platforms, listed companies, unicorns, and sci-tech services, and proposes a spatial coordination framework across the AI innovation chain, industry chain, talent chain, and urban service chain. The agent open-call taskbook also requires responding to the "five functions" and "three-district two-wing" coordination; this section uses [source:AGENT-TASKBOOK] and [standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK] to mark that these requirements come from the agent open-call, not statutory planning control.

The differentiating value of this proposal is treating "network self-organization" as a computable urban-design method: the Physarum network's minimum-cost, multi-source shortest-path, and fault-tolerant redundancy properties map onto the efficiency, connectivity, and robustness objectives of road-network renewal, while the four NSGA-II objectives (efficiency, connectivity redundancy, heritage impact, cost) map onto planning's multi-criteria trade-off [depth:overall_spatial_structure]. The coordinated research does not add pseudo-precise redlines; it ties back to [data:geometry/land_use.geojson#LU-001] through [standard:MOHURD-URBAN-DESIGN-MEASURES].

## Overall Design Area: Urban Renewal and Regulatory-Plan-Level Urban Design

The overall design area must reach regulatory-plan-level urban design depth. The proposal states an overall urban renewal spatial structure, low-efficiency space identification, a renewal project list, implementation policy recommendations, industrial functional ratios, a spatial organization model, and a comprehensive carrying-capacity assessment. `geometry/land_use.geojson` fully covers the design boundary without overlap, `geometry/buildings.geojson` expresses renewal or retained building footprints, `geometry/roads.geojson` expresses micro-circulation, slow traffic, and rail-interchange relations, and `metrics.json` recalculates core areas, ratios, and layer counts [depth:land_use_layout] [depth:development_intensity_controls].

This section uses [standard:MOHURD-CONTROL-DETAILED-PLANNING] to split regulatory-depth content into reviewable objects: [data:geometry/land_use.geojson#LU-001] expresses land-use structure, [data:geometry/buildings.geojson#BLDG-001] expresses building footprints, [data:geometry/roads.geojson#ROAD-001] expresses the conceptual primary vein, and [metric:building_footprint_area_sqm] is used to cross-check the footprint area.

The overall design must also support transport, rail, municipal, and supporting facilities. Where building height, development intensity, road redlines, setbacks, and facility standards lack official control conditions, they must be written as "pending formal regulatory-plan confirmation", never presenting agent-inferred values as approved indicators.

## Detailed Design of Key Areas

The detailed design of the three key areas must reference [data:geometry/key_areas.geojson#PROV-KEY-001], [data:geometry/key_areas.geojson#PROV-KEY-002], and [data:geometry/key_areas.geojson#PROV-KEY-003], and is checked by [depth:three_key_area_detailed_design].

![Three key-area index and design tasks](assets/figures/key-areas.en.png)

| Key area | Design positioning | Spatial actions | AI industry & operation scenarios | Evidence reference |
| --- | --- | --- | --- | --- |
| Zhongzhiyuan AI autonomous innovation acceleration area | Garden full-stack autonomous innovation block | Strengthen the Qinghe interface, industry display, low-carbon innovation exchange, and external transport; the Physarum slow loop carries open testing and standards-governance display | Autonomous model testing, standards workshops, safety-governance display, low-carbon computing experience | [data:geometry/key_areas.geojson#PROV-KEY-001], [depth:three_key_area_detailed_design] |
| Beijing AI Origin community | Campus conversion and talent community | Organize campus-park-block slow stitching; the Physarum branch links outcome-release, talent-service, and open-source collaboration spaces | Open-source community, outcome release, talent-zone service, near-campus incubation | [data:geometry/key_areas.geojson#PROV-KEY-002], [source:AGENT-TASKBOOK] |
| Dazhongsi AI industry cluster | Urban intelligent-economy and international exchange block | Dazhongsi station integration, four-quadrant pedestrian connectivity, commercial services, and public-environment renewal around key enterprises | Agent and terminal display, content consumption, data elements, international roadshows | [data:geometry/key_areas.geojson#PROV-KEY-003], [metric:key_area_count] |

## AI Innovation Ecosystem, Personas, and AI+ Scenarios

The proposal builds a spatial-demand persona for AI talent and enterprises covering R&D office, open-source collaboration, outcome release, enterprise services, talent housing, social learning, consumption and living, sports and leisure, and international exchange. AI+ scenarios address transport, services, consumption, healthcare, education, legal, and life services; each scenario states its service target, spatial location, data source, privacy boundary, human-review mechanism, and operating entity [depth:traffic_rail_slow_parking].

| Persona | Typical need | Spatial response | Self-check boundary |
| --- | --- | --- | --- |
| Open-source developer | Release, collaboration, testing, community reputation | Origin-community open-source release hall, public code wall, night collaboration space | No personal trajectory collection; activity data aggregated only |
| Startup team | Low-cost office, computing entry, product testbed | Zhongzhiyuan shared testbed, edge-computing service point, standards-governance advisory | Computing and data services require separate authorization |
| Leading-enterprise visitor | Display, business, international reception, talent recruitment | Dazhongsi international roadshow lounge, station interchange, public space around key enterprises | Enterprise marks and cases must be cleared |
| Nearby resident | Commuting, leisure, community service, low-disturbance renewal | Jing-Zhang heritage park slow loop, embedded community service, graded night lighting and activities | No commercial recommendation from resident personas |
| University teacher/student | Technology conversion, cross-campus collaboration, daily slow travel | Campus-park slow stitching, conversion relay station, AI education experience point | Campus data and research results need authorization |

| Scenario card | Spatial carrier | Design note |
| --- | --- | --- |
| 01 Open-source release hall | Beijing AI Origin community | Outcome release, code contribution display, and small roadshow space for universities, open-source communities, and startups |
| 02 Safety-governance sandbox | Zhongzhiyuan | Translate standards-making, safety evaluation, and model red-teaming into visitable, reservable, supervised display and collaboration nodes |
| 03 Edge-computing station | Overall design area node | Combined with public services, enterprise services, and low-carbon energy strategy as a new-infrastructure prototype |
| 04 AI slow-travel navigation | Jing-Zhang heritage park vitality belt | Explainable signage and low-intrusion sensing to identify slow-travel gaps, congestion nodes, and accessibility needs |
| 05 Dazhongsi international roadshow lounge | Dazhongsi AI industry cluster | Display, negotiation, media release, and international exchange for agent, terminal, and content-consumption enterprises |
| 06 Qinghe low-carbon innovation corridor | Zhongzhiyuan Qinghe interface | Combine green space, stormwater, walking/cycling, and AI display as a park public living room |
| 07 Near-campus conversion street | Beijing AI Origin community | Incubation, display, legal, IP, and investment services for university technology conversion |
| 08 Data-element lounge | Dazhongsi area | A compliant, authorized, auditable urban service interface for data elements and digital-asset circulation |
| 09 AI life-service model street | Community-commercial junction | Land AI+ scenarios for healthcare, education, legal, and life services onto operable small-scale blocks |
| 10 Global AI activity-week route | The belt's public-space system | A walkable, spreadable experience route from heritage culture, open-source community, industry display to international roadshow |

## Land Use, Building Scale, and Retain-Renovate-Demolish Strategy

The land-use proposal expresses a complete, closed, seamless partition following the public standards of territorial survey, planning, and use-control classification. The building proposal distinguishes retained, renovated, renewed, new, and to-be-confirmed objects, stating the recommended tiers for footprint, function, scale, character, roof, massing, and height control. Where existing buildings, ownership, regulatory plan, and engineering conditions are missing, the proposal only states a method and a calibration checklist, never fabricating retain-renovate-demolish conclusions [standard:MNR-LAND-USE-CLASSIFICATION-GUIDE] [depth:retain_renovate_demolish].

The main land-use and building evidence is [data:geometry/land_use.geojson#LU-001], [data:geometry/buildings.geojson#BLDG-001], and [metric:building_footprint_area_sqm]. Building scale and intensity metrics must be consistent with `metrics.json` and the layers; where official conditions are missing, use `status=unknown` and state the pending condition in `reason` / `assumptions`, never manufacturing precision with fixed numbers.

## Transport, Rail, Municipal Infrastructure, and Public Services

The transport proposal responds to the announcement's requirements on station integration, road micro-circulation, slow-travel gaps, external transport, parking, bicycle parking, and green transport, focusing on the Dazhongsi station and key-enterprise surroundings [depth:traffic_rail_slow_parking].

**Physarum network hierarchy (conceptual network)**. This proposal generates a conceptual network in `geometry/roads.geojson` inside the provisional boundary, translating the Physarum primary-vein / branch / terminal structure into road tiers [data:geometry/roads.geojson#ROAD-001] [data:geometry/roads.geojson#ROAD-005]:

- **Primary vein (secondary)**: the north-south spine through Dazhongsi → AI Origin → Zhongzhiyuan, the backbone carrying the highest connectivity demand and rail interchange.
- **Branch**: the east-west connectors of the three key areas, linking key enterprises, public space, and stations.
- **Slow loop (cycleway/local_access/pedestrian)**: terminal loops around the three key areas carrying daily slow travel and four-quadrant pedestrian connectivity.
- **Green corridor (greenway)**: the blue-green composite corridors flanking the Jing-Zhang heritage park vitality belt, linking footpaths, cycleways, and green space.
- **Station feeder (transit_connection)**: the Dazhongsi station interchange axes.

**Method-validation evidence (not entering formal geometry)**. The author's real Physarum + NSGA-II run produced a 167-edge adaptive network with optimal efficiency index 19.20, Run7 frozen objective 2.802, and baseline efficiency 1.143, and **zero heritage crossings** (objective f3≡f2, heritage impact coupled to cost) [metric:physarum_efficiency_index] [metric:physarum_heritage_crossing_count]. Because of a coordinate offset of roughly 2–3 km, this result is method-level convergence and constraint-behavior evidence only; it is not a redline or approval geometry for this site, as detailed in `assumptions.json` and the risk section.

![Transport slow-travel and blue-green public space composite system](assets/figures/mobility-bluegreen.en.png)

Municipal and public-service facilities cover AI industry service facilities, innovation service platforms, talent living services, new infrastructure, distributed energy, edge computing, and traditional municipal facilities [depth:municipal_new_infrastructure]. Missing pipeline, energy, drainage, flood-control, and fire-safety engineering data are listed as formal deepening prerequisites.

## Blue-Green Network, Public Space, and Urban Character

The blue-green proposal takes the Jing-Zhang heritage park vitality belt as the skeleton, coordinating the Qinghe and Xiaoyue rivers and the travel needs of surrounding universities, enterprises, and communities, proposing a north-south connected and east-west linked footpath, cycleway, and green-space system [depth:blue_green_public_space] [data:geometry/green_space.geojson#GREEN-001] [data:geometry/public_space.geojson#PUBLIC-001].

The Physarum green corridors and slow loops form the "vascular network" of the blue-green public space: green corridors run north-south along the vitality belt, and slow loops create human-scale public activity interfaces in the three key areas; the green and public-space ratios are explained in prose and recalculated in full in `metrics.json` [metric:green_ratio] [metric:public_space_ratio]. The urban-character proposal integrates Jing-Zhang railway history, Zhongguancun innovation culture, and AI innovation culture, distinguishing official control, design recommendation, and to-be-confirmed conditions, and strictly forbids pseudo-precise control lines without heritage or regulatory-plan basis [standard:MOHURD-URBAN-DESIGN-MEASURES].

## Renewal Projects, Implementation Policy, and Phasing

The implementation plan forms a reviewable renewal project list stating location, type, function, responsible entity, dependency conditions, phase, risk, and evaluation metrics [depth:renewal_project_list] [depth:phasing_implementation].

| Project ID | Project name | Type | Main dependency | Evidence reference |
| --- | --- | --- | --- | --- |
| JZ-01 | Jing-Zhang heritage park slow-travel gap stitching | Public space / transport | Road redline, under-bridge space, traffic organization review | [data:geometry/roads.geojson#ROAD-011] |
| JZ-02 | Zhongzhiyuan Qinghe innovation interface | Blue-green / industry display | River blue line, ecology and flood conditions | [data:geometry/green_space.geojson#GREEN-001] |
| JZ-03 | Origin-community near-campus conversion street | Urban renewal / industry service | Campus boundary, ownership, ground-floor program | [data:geometry/buildings.geojson#BLDG-001] |
| JZ-04 | Dazhongsi station four-quadrant pedestrian connectivity | Rail integration / slow travel | Station, road intersection, municipal pipelines | [data:geometry/public_space.geojson#PUBLIC-001] |
| JZ-05 | AI public service and edge-computing node | New infrastructure / public service | Energy, computing, safety, operating entity | [data:geometry/constraints.geojson#CONSTRAINTS] |
| JZ-06 | Physarum network deepening and real-site recalculation | Research / calibration | Official boundary, road redline, real Physarum coordinate alignment | [data:geometry/roads.geojson#ROAD-001] |

Phasing must be distinguished from the 100-day competition design period: near-term pilots start with lightweight facilities, operating activities, and service platforms; mid-term renewal advances road micro-circulation and key-area public environments; long-term governance awaits formal regulatory-plan, municipal, transport, and ownership confirmation. Annual activity systems, developer community operations, scenario open days, public experience routes, and international communication mechanisms must state operating target, frequency, responsibility boundary, conversion path, and risk, not slogans.

## Metrics, Area Recalculation, and Compliance Matrix

The metrics system includes at least overall design area, key-area area, green and public-space ratios, building footprint, renewal project count, AI scenario nodes, slow-travel connectivity, industry space, talent service, and self-check state [depth:metrics_recalculation]. Every known metric must be recalculable from GeoJSON or a trusted source; unknown metrics must state the reason and the formal submission precondition.

**Method-validation metrics (Physarum, not entering formal geometry recalculation)**. The following metrics come from the author's real Physarum + NSGA-II run, stored in `metrics.json` as method-level evidence, and are not treated as formal spatial conclusions for this site due to the coordinate offset:

- Network edge count 167 [metric:physarum_network_edge_count]
- Optimal efficiency index 19.20 [metric:physarum_efficiency_index]
- Baseline efficiency 1.143 [metric:physarum_baseline_efficiency]
- Run7 frozen objective 2.802 [metric:physarum_run7_frozen_objective]
- Heritage crossing count 0 [metric:physarum_heritage_crossing_count]
- Recommended plan Plan03 urban-integration UDS 80.34 [metric:physarum_recommended_plan_uds]

![Core metrics recalculation and evidence chain](assets/figures/metrics-evidence.en.png)

The compliance matrix is the master control file for task responsiveness. Each announcement task and agent-taskbook task must map to a report section, layer, metric, drawing, HTML page, source, assumption, and self-check item. For formal deepening, metrics are divided into three classes: spatial metrics directly recalculable from submitted geometry; control metrics requiring official regulatory plan or taskbook attachments; and performance metrics requiring continuous operational or industry data calibration.

## Risk, Copyright, and Compliance

**Bilingual required.** This proposal's primary file is Chinese, with a full mirrored translation provided via `proposal.en.md`; the A3/A0, HTML, and text-bearing figures also provide language counterparts [source:SITE-PACKAGE].

**Honest statement on coordinate offset and heritage protection.** The real Physarum run lies roughly 2–3 km west of the provisional boundary, overlapping the site boundary by only about 140 m. This proposal performs no coordinate translation or fabrication; the real result is downgraded to method-validation evidence, and the formal geometry uses a conceptual network inside the provisional boundary. Heritage protection (HERITAGE_PROTECTION) is a locked layer with `editable_by_agent=false` and no citable official geometry in the public site package, so `geometry/constraints.geojson` is deliberately kept empty; the heritage boundary enters `sources.json`/`assumptions.json` as a declaration rather than the constraint layer [depth:risk_missing_data] [data:geometry/constraints.geojson#CONSTRAINTS].

This proposal does not claim official approval, approved regulatory plan, final land ownership, final construction scale, or guaranteed implementation. All images, drawings, icons, data, and code assets state their source, license, and authorization status in `sources.json` or `report/copyright_statement.md`. The HTML pages load no remote scripts, map tiles, fonts, iframes, forms, or external APIs, and do not track reviewer behavior.

## References

- brief/public-brief.md
- brief/site-package/design_brief.json
- brief/site-package/allowed_design_space.json
- brief/site-package/enums/
- brief/site-package/ranges/planning_limits.json
- data/processed/agent_fact_pack.md
- data/processed/project_scope_summary.csv
- data/processed/agent_task_requirements.csv
- data/processed/source_use_matrix.csv
- data/processed/missing_data_checklist.csv
- Tero A., Takagi S., Saigusa T., et al. Rules for biologically inspired adaptive network design. *Science*, 327(5964): 439–442, 2010.
- Deb K., Pratap A., Agarwal S., Meyarivan T. A fast and elitist multiobjective genetic algorithm: NSGA-II. *IEEE Transactions on Evolutionary Computation*, 6(2): 182–197, 2002.
- Complete machine index: see `sources.json`, `metrics.json`, `compliance_matrix.json`, `standard_matrix.json`, and `design_depth_matrix.json`.
- The bibliographic entry for this section follows the site-package register; full provenance and license are in the structured source list [source:SITE-PACKAGE].
