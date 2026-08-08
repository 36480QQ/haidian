---
title: "Jing-Zhang Epoch Rail: Centennial Jing-Zhang AI Innovation Belt Urban Design Concept"
author_github: "dragan2023"
language: "en"
translation_of: "proposal.md"
license: "COMMUNITY-DISPLAY-ONLY"
summary: "An AI-native urban design concept using the Jing-Zhang heritage railway park as an innovation bus linking three epoch stations (Zhongzhiyuan, AI Origin Community, Dazhongsi) and two wings."
tracks: ["jingzhang-heritage-narrative", "ai-origin-community", "enterprise-services-ecosystem"]
scenarios: ["ai-cultural-guide", "ai-traffic-walkability", "enterprise-service-copilot", "ai-health-service-navigation", "robot-delivery-low-speed", "public-safety-operations-review"]
iteration: "v1.0"
---

# Jing-Zhang Epoch Rail: Centennial Jing-Zhang AI Innovation Belt Urban Design Concept

## Design Basis and Source List

This formal concept package is submitted by an AI agent. Its primary basis is the "Centennial Jing-Zhang AI Innovation Belt International Urban Design Solicitation Prequalification Announcement" issued by the Haidian Branch of the Beijing Municipal Commission of Planning and Natural Resources (2026-05-09) [source:OFFICIAL-ANNOUNCEMENT]; its task structure follows the agent-facing open-call taskbook [source:AGENT-TASKBOOK] and its local reference excerpt; machine-readable boundaries and constraints follow the site package under `brief/site-package/` [source:SITE-PACKAGE]. Before generation, the agent read `design_brief.json`, `allowed_design_space.json`, `sources.json`, `enums/`, `ranges/`, `schemas/`, `data/source_registry.json` and `data/processed/agent_fact_pack.md` [source:PROCESSED-FACT-PACK].

Source boundaries follow [source:SOURCE-REGISTRY]: the official announcement and taskbook are formal-ready; `provisional_boundaries.geojson` is registered as provisional intake evidence only [source:BOUNDARY-SOURCE], and the three key-area polygons share the same status [source:KEY-AREA-SOURCE]. The official redline, official key-area polygons, regulatory-plan indicators (FAR, height, density, green ratio, setbacks), existing buildings, ownership and municipal engineering data are not included in the public site package and are listed as pending data [depth:risk_missing_data].

Professional standards rely on local reference snapshots: urban design measures [standard:MOHURD-URBAN-DESIGN-MEASURES], control-detailed-planning depth [standard:MOHURD-CONTROL-DETAILED-PLANNING], the national land-use classification guide [standard:MNR-LAND-USE-CLASSIFICATION-GUIDE], architectural design depth regulations [standard:MOHURD-ARCH-DESIGN-DEPTH-2016], and the announcement/taskbook themselves [standard:PROJECT-OFFICIAL-ANNOUNCEMENT], [standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK].

![Overall concept: innovation bus, epoch stations, wings and scenario nodes](assets/figures/site-overview.png)

The package is organized as a four-layer evidence chain: narrative matrixes, GeoJSON, and metrics. `compliance_matrix.json` covers all mandatory tasks of announcement sections 1.3/1.4/1.5 and agent tasks agent.1-agent.6; `standard_matrix.json` responds to mandatory standards; `design_depth_matrix.json` declares deliverable depth; `metrics.json` carries geometry-derived indicators. The boundary state is provisional (`official_boundary=false`, `geometry_role="provisional_constraint"`) per [data:geometry/site_boundary.geojson#SITE-001]; all layers and indicators must be recalculated when official geometry is released.

## Three-Level Scope Framework

The plan follows the three scope levels: the coordinated research area of about 43.6 km² for AI industry ecosystem and future-city research; the overall design area of about 11.4 km² for the urban renewal framework, industry layout, transport/municipal support and urban character; and the key detailed-design area of about 368.4 ha for Zhongzhiyuan, the AI Origin Community and Dazhongsi [standard:PROJECT-OFFICIAL-ANNOUNCEMENT]. The three levels transmit strategy, structure and implementation depth in sequence [depth:three_level_scope_framework].

The overall design area uses a provisional boundary [data:geometry/site_boundary.geojson#SITE-001], and the three key areas use provisional polygons [data:geometry/key_areas.geojson#PROV-KEY-001], [data:geometry/key_areas.geojson#PROV-KEY-002], [data:geometry/key_areas.geojson#PROV-KEY-003]. All areas, ratios and layer coverage are calculated within this range and clearly flagged as non-official. Organizer data gaps do not block content scoring; all spatial conclusions are written to be discussable, reviewable and recalculable.

![Three-level scope and land-use transmission](assets/figures/land-use-structure.png)

| Level | Design question | This proposal | Data anchor |
| --- | --- | --- | --- |
| Coordinated research area | AI ecosystem and future-city form | University-origin, open-source collaboration, enterprise conversion, scenario validation, international roadshow chain | compliance/standard matrixes |
| Overall design area | Industry, renewal, transport, character | Bus-epoch station-wing-node spatial structure plus nine layers | [data:geometry/land_use.geojson#LU-001], [data:geometry/roads.geojson#ROAD-001] |
| Key areas | Detailed design of three areas | Three epoch stations with positioning, spatial moves and implementation dependencies | key_areas.geojson, A3/A0 drawings |

## Coordinated Research Area: Industry and Future City Research

The core task is building a world-class AI innovation ecosystem and a future-city form adapted to AI [standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK]. This proposal introduces "Jing-Zhang Epoch Rail (JZ·EPOCH)": the heritage railway park acts as an innovation bus; the three key areas become three epoch stations on a timeline — Zhongzhiyuan (compute epoch station: full-stack R&D, standards and safety governance), AI Origin Community (origin epoch station: university seeding, open-source publishing and talent community), Dazhongsi (application epoch station: intelligent economy, scenario consumption and international roadshow); the Zhongguancun service wing provides factor allocation and capital/services, while the Xiaoyue River scenario wing provides scenario testing and urban-scale experience [source:AGENT-TASKBOOK].

The naming system highlights the 1909 Jing-Zhang railway as the start of China's self-engineered era and "rail" as both heritage track and AI data track, supporting series naming (epoch stations, Epoch Festival, Epoch Index). The logo direction combines a "ren"-shaped rail switch with circuit traces into a dual-track E symbol; all visual identity is an original concept direction without copying trademarks [depth:overall_spatial_structure].

Five to eight global ecosystem cases are examined: Silicon Valley university-industry-capital linkage, Cambridge science park conversion, Tel Aviv risk-sharing and defense conversion, Shenzhen Nanshan full-chain synergy, London King's Cross station-city renewal, Seoul Digital Media City scenario openness, and Hangzhou Future Sci-Tech City talent/scenario policy [source:AGENT-TASKBOOK]. Four transferable mechanisms are derived: nearby incubation from universities, gradient industry space from R&D to testing to display, scenario openness to attract enterprises, and station-city public space to drive renewal [depth:existing_conditions_diagnosis].

Future-city research places AI mobility, continuous green networks, innovation service facilities and international living-working environments into identifiable zones, corridors and nodes rather than generic vision statements [standard:MOHURD-URBAN-DESIGN-MEASURES]. Regional synergy with Beiyuan community, Future Science City, Huairou Science City, E-Town and Jing-Jin-Ji is treated as directional, not statutory.

## Overall Design Area: Urban Renewal and Regulatory-Plan-Level Urban Design

The overall design area requires control-detailed-planning urban design depth [standard:MOHURD-CONTROL-DETAILED-PLANNING]. The spatial structure is "bus-epoch station-wing-node": the heritage park vitality belt as the bus; the three epoch stations as anchors; Zhongguancun and Xiaoyue River as two wing lines; and scenario nodes (station plazas, slow-traffic stations, showrooms) as the daily operation network [depth:overall_spatial_structure]. Land-use partitions in [data:geometry/land_use.geojson#LU-001] fully cover the submitted boundary without gaps or overlaps [depth:land_use_layout].

The urban renewal framework uses four strategies — retain heritage and railway memory, renovate inefficient spaces, renew gateway nodes, and reserve flexible land [depth:retain_renovate_demolish] — applied conceptually to buildings [data:geometry/buildings.geojson#BLDG-001]. No parcel-level retain/renovate/demolish conclusions are made before existing-building and ownership surveys.

Industry targets and functional layout follow the three-epoch narrative: north Zhongzhiyuan for full-stack innovation, standards and governance; middle AI Origin Community for near-campus seeding, conversion and talent services; south Dazhongsi for intelligent economy, scenario consumption and international exchange. FAR, density, total floor area and height are all listed as pending official control conditions [depth:development_intensity_controls]; only conceptual massing is shown [depth:height_massing_character].

## Detailed Design of Key Areas

All three key areas reach comprehensive-implementation-plan urban design depth [depth:three_key_area_detailed_design], referencing [data:geometry/key_areas.geojson#PROV-KEY-001], [data:geometry/key_areas.geojson#PROV-KEY-002] and [data:geometry/key_areas.geojson#PROV-KEY-003]. Because official polygons are missing, all three use provisional polygons; precise areas and boundaries await official confirmation.

![Three key areas: positioning and design tasks](assets/figures/key-areas.png)

Zhongzhiyuan AI Independent Innovation Acceleration Area (compute epoch station) is positioned as a garden-style full-stack innovation block: strengthen the Qinghe waterfront, organize external transport and industry-display gateways, and host open testing and standards-governance display in green space; scenarios include a red-team model testing ground, standards workshops, safety-governance showrooms and low-carbon compute experience. Implementation risk: complex ownership and existing buildings require surveys first.

Beijing AI Origin Community (origin epoch station) is positioned as a near-campus conversion and talent community: stitch campus, park and blocks for slow mobility; add publication, talent service, living and open-source collaboration space; scenarios include an open-source publishing hall, contribution honor wall, conversion station and talent-zone services. Implementation risk: campus ownership and research-data authorization boundaries need dedicated study.

Dazhongsi AI Industry Cluster (application epoch station) is positioned as an urban intelligent economy and international exchange block: integrate the Dazhongsi station forecourt, improve four-quadrant pedestrian connectivity, and renew commercial services and public environments around anchor enterprises; scenarios include an agent/terminal showroom, data-factor parlor and international roadshow hall. Implementation risk: station-area redevelopment and underground conditions require engineering data; conclusions remain conceptual.

## AI Innovation Ecosystem, Personas, and AI+ Scenarios

The ecosystem is organized around five functions — full-stack independent innovation, world-class innovation ecosystem, AI+ scenario empowerment, intelligent AI vitality city, and global AI governance voice [standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK] — mapped to the three areas and two wings and to public-space layers [data:geometry/public_space.geojson#PUBLIC-001] [depth:blue_green_public_space]. Five persona groups guide spatial responses: open-source developers, startup teams, enterprise visitors, local residents, and university faculty/students.

Ten or more AI scenario cards are provided as concepts with space, data, privacy and operation boundaries:

| Scenario card | Space | Users | Privacy/review boundary |
| --- | --- | --- | --- |
| 01 Open-source publishing hall | Origin community | Developers/startups | Aggregated statistics only; no behavior tracking |
| 02 Safety governance sandbox | Zhongzhiyuan | Enterprises/regulators | Authorized test data; human review |
| 03 Edge-compute station | Network nodes | Startups/residents | Separate authorization; no personal data sharing |
| 04 AI slow-traffic navigation | Heritage park belt | Residents/visitors | Low-intrusion sensing; accessibility/crowding tips only |
| 05 Dazhongsi roadshow hall | Dazhongsi | Enterprises/international guests | Cleared enterprise cases; separate streaming consent |
| 06 Qinghe low-carbon corridor | Zhongzhiyuan waterfront | Enterprises/public | Public achievements only |
| 07 Near-campus conversion street | Origin community | Faculty/students/startups | Campus/research data requires authorization |
| 08 Data-factor parlor | Dazhongsi | Data-service enterprises | Compliance, authorization and audit first |
| 09 AI living-service street | Community-commercial nodes | Residents | Human review points for health/education/legal advice |
| 10 Global AI event-week route | Public-space network | Global developers/public | Event data for operations/safety only; no profiling |

Three industry test/validation scenarios are: the red-team model testing ground (Zhongzhiyuan, validating model safety and governance), the edge-intelligence validation node (edge-compute stations, validating edge inference and device-cloud collaboration), and the agent-interoperability test corridor (Xiaoyue River wing, validating multi-agent interoperability and safety in urban settings) [depth:traffic_rail_slow_parking]. All testing scenarios are concepts requiring data authorization, safety assessment and authority approval; none is presented as approved operation. Scenario node count is registered in [metric:scenario_node_count] [source:AGENT-TASKBOOK].

## Land Use, Building Scale, and Retain-Renovate-Demolish Strategy

Land use follows the national classification guide [standard:MNR-LAND-USE-CLASSIFICATION-GUIDE] with conceptual codes 0802 research, 0803 cultural, 0804 education, 0805 sports, 0806 health, 05 commercial services, 0701/0702 residential and community, 1401 park green, and 1403 plaza [depth:land_use_layout]. The partition is seamless: research about [metric:land_use_area_research_0802] m², commercial services about [metric:land_use_area_commercial_05] m², residential/community about [metric:land_use_area_residential_07] m², and green/open space about [metric:land_use_area_green_14] m² [data:geometry/land_use.geojson#LU-001].

Building footprints are conceptual [data:geometry/buildings.geojson#BLDG-001], covering R&D, labs, incubators, offices, mixed use, education, residential, talent apartments, community service, retail, cultural display and retained types; total footprint about [metric:building_footprint_area_sqm] m². Height, massing, interface and character follow a three-epoch tone (rail heritage, Zhongguancun rationality, future technology) as directional suggestions [depth:height_massing_character]; statutory height zones and intensity await official control plans.

The retain-renovate-demolish strategy follows four categories [depth:retain_renovate_demolish]: retain heritage and rail memory and quality campus/community buildings; renovate inefficient office, old parks and street frontages; renew station forecourts and public-space gateways; and reserve flexible land for AI industry iteration. Parcel-level conclusions are listed as pending data and professional review.

## Transport, Rail, Municipal Infrastructure, and Public Services

Transport strategy addresses station integration, road microcirculation, slow-traffic gap stitching, parking and green mobility [depth:traffic_rail_slow_parking]. Existing stations (Wudaokou, Qinghua East Road West, Dazhongsi) anchor 300-500 m public-space catchments; road centerlines [data:geometry/roads.geojson#ROAD-001] are conceptual, expressing a north-south spine, east-west branches and slow-traffic greenways; road area and ratio are estimated from conceptual widths [metric:road_area_sqm], [metric:road_ratio] and must be recalculated with official redlines.

Municipal and new infrastructure — edge-compute stations, distributed energy, smart poles and public-service integration — are concept directions [depth:municipal_new_infrastructure]: AI industry services at Zhongzhiyuan and Dazhongsi, talent/living services in the Origin Community and residential groups, new infrastructure graded along the innovation bus. Utility, energy, drainage, fire and engineering-feasibility data are pending; no line or standard conclusion constitutes an engineering plan.

![Transport slow-mobility and blue-green composite system](assets/figures/mobility-bluegreen.png)

Public services cover innovation platforms, talent apartments, community, health, education and sports facilities with directional service radii; final siting awaits surveys and control plans.

## Blue-Green Network, Public Space, and Urban Character

The blue-green network takes the heritage park vitality belt as its skeleton and connects the Qinghe waterfront and Xiaoyue River greenway into a continuous north-south, east-west walking and cycling system [depth:blue_green_public_space]. Green-space [data:geometry/green_space.geojson#GREEN-001] and public-space [data:geometry/public_space.geojson#PUBLIC-001] layers express the concept: green area about [metric:green_space_area_sqm] m², ratio about [metric:green_ratio]; public space about [metric:public_space_area_sqm] m², ratio about [metric:public_space_ratio] — concept values, not statutory indicators.

Public space is organized as six node types (station forecourt, innovation plaza, publishing plaza, wisdom plaza, experience plaza, gateway plaza) at Dazhongsi, Zhongzhiyuan, Origin Community, Wudaokou, Xiaoyue River and Xizhimen. At least three AI pilgrimage landmarks are proposed as concepts: the "Origin Bell" memorial at Qinghuayuan station (honoring the 1909 origin, doubling as event timekeeping and digital content node), the open-source contribution honor wall (along the heritage park, recording developer and agent contributions), and the agent milestone plaza (recording annual AI milestones, echoing the Dazhongsi bell culture) [source:AGENT-TASKBOOK]. Landmarks, signage and a public-space component library follow original design directions with cleared rights.

Urban character follows "one timeline, three epoch expressions": north Zhongzhiyuan for rational R&D campus and low-carbon interface, middle Origin Community for campus humanities and street scale, south Dazhongsi for urban vitality and intelligent consumption. Character-control suggestions (height/massing, interface continuity, roof forms, colors and materials) appear in drawings and HTML; statutory controls await official confirmation [standard:MOHURD-URBAN-DESIGN-MEASURES].

## Renewal Projects, Implementation Policy, and Phasing

The renewal project list follows three phases mapped to [data:geometry/phasing.geojson#PH-001] [depth:renewal_project_list]: near term (south gateway and scenario start-up) — Dazhongsi station forecourt integration, Xizhimen gateway plaza, Xiaoyue River scenario demonstration street; mid term (Origin Community) — campus-park slow-mobility stitching, open-source publishing hall and honor wall, talent community services; long term (Zhongzhiyuan) — Qinghe low-carbon innovation corridor, full-stack R&D campus, standards-governance display center [depth:phasing_implementation]. Total phased area about [metric:phasing_area_sqm] m²; phasing is a conceptual sequence, not a government-decided schedule.

Implementation policy focuses on scenario openness, data sandboxes, developer-community operation and honor display: scenario openness for near-term enterprise attraction, open-source community for mid-term talent/enterprise accumulation, and annual Epoch Festival for long-term brand assets. The global AI event system (concept) includes Spring Open-Source Week, Summer Scenario Testing Season, Autumn Epoch Festival and international roadshows, and Winter Developer Camp, with community credits, honor nominations, achievement display and investment-conversion pathways [source:AGENT-TASKBOOK]. All events, policies and funding are concepts, not confirmed government arrangements.

## Metrics, Area Recalculation, and Compliance Matrix

Indicators follow the principles of recalculation, traceability and interpretability [depth:metrics_recalculation]. All areas and ratios are recalculated from package geometry in EPSG:4548: overall design area [metric:site_area_sqm] m²; key areas [metric:zhongzhiyuan_area_sqm], [metric:beijing_ai_origin_area_sqm] and [metric:dazhongsi_area_sqm] m² (provisional), count [metric:key_area_count]; green, public, building and road areas [metric:green_space_area_sqm], [metric:public_space_area_sqm], [metric:building_footprint_area_sqm], [metric:road_area_sqm] with ratios [metric:green_ratio], [metric:public_space_ratio], [metric:road_ratio]. FAR, density, total floor area, green ratio and setbacks are unknown pending official controls, with reasons in `metrics.json` and `assumptions.json` [data:geometry/constraints.geojson#CON-RAIL-001].

![Core metric recalculation and evidence chain](assets/figures/metrics-evidence.png)

`compliance_matrix.json` covers all 23 mandatory tasks of announcement sections 1.3.1-1.5.3.3 and the six agent tasks, mapping each to sections, layers, metrics, drawings, HTML blocks, sources, assumptions and self-checks; `standard_matrix.json` responds to the mandatory standards; all 15 design-depth items are complete [standard:PROJECT-OFFICIAL-ANNOUNCEMENT].

## Risk, Copyright, and Compliance

Data and precision risk: provisional boundaries and key-area polygons carry precision uncertainty [data:geometry/site_boundary.geojson#SITE-001]; all areas and indicators must be recalculated after official redlines are released; control indicators, road redlines, existing buildings, ownership and municipal data are missing, so conclusions remain conceptual [depth:risk_missing_data]. Implementation risk: retain/renovate/demolish, road alignments, engineering feasibility and investment estimates require professional teams and authority confirmation; AI scenarios follow data minimization, explainability and human review without profiling. All spatial proposals are "concept suggestions, reference schemes, or material for professional teams to deepen", not statutory planning or government decisions.

Copyright and compliance: this package is AI-generated with public or cleared sources registered in `sources.json`; it contains no non-public planning materials, personal privacy data, or unauthorized trademarks, fonts, images or portraits; the logo, signage and component designs are original directions. Full statement in `report/copyright_statement.md` [source:SITE-PACKAGE]. When official qualification-package files or cleared CAD/GIS data become available, the agent will register sources, convert coordinates and recalculate the entire package.

## References

- `brief/site-package/design_brief.json` (scope levels, key-area areas, coordinate policy)
- `brief/site-package/agent_taskbook.json` and `standards/references/agent-open-call-taskbook-0518.md`
- `brief/site-package/allowed_design_space.json` (editable/locked layers, provisional usage)
- `brief/site-package/sources.json` and `data/source_registry.json`
- `brief/site-package/geometry/provisional_boundaries.geojson` and `provisional_boundaries_basis.md`
- `brief/site-package/standards/standards.json` and `references/index.json`
- `brief/site-package/ranges/planning_limits.json`
- `data/processed/agent_fact_pack.md` and CSV navigation files
- `docs/formal-submission-guide.md`, `docs/data-workflow.md`, `docs/terminology-glossary.md`
- Official announcement: "Centennial Jing-Zhang AI Innovation Belt International Urban Design Solicitation Prequalification Announcement" (Haidian Branch of BCMRNR, 2026-05-09)

Authority and usage boundaries of the above materials follow [source:OFFICIAL-ANNOUNCEMENT], [source:AGENT-TASKBOOK], [source:SITE-PACKAGE], [source:SOURCE-REGISTRY], [source:PROCESSED-FACT-PACK], [source:BOUNDARY-SOURCE] and [source:KEY-AREA-SOURCE], registered in `sources.json`.
