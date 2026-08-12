---
title: "AI Pulse Belt — Concept Design for the Centennial Jing-Zhang AI Innovation Belt"
author_github: "LShengYi"
language: "en"
proposal_format_version: "2"
bilingual_contract_version: "1"
iteration: "6"
translation_of: "proposal.md"
license: "COMMUNITY-DISPLAY-ONLY"
summary: "A formal AI urban-design submission built on the concept 'AI Pulse Belt': translating the centennial Jing-Zhang Railway 'iron pulse' into an AI-era 'digital pulse belt' — one belt, three cores, two wings, multiple nodes; all geometry generated from official provisional boundaries with disclosed area deviations, reproducible metrics, verifiable layers, and fully aligned bilingual deliverables."
tracks: ["ai-traffic-walkability", "enterprise-services-ecosystem", "civic-agent-governance"]
scenarios: ["ai-traffic-walkability", "enterprise-service-copilot", "robot-delivery-low-speed", "ai-cultural-guide", "public-safety-operations-review", "ai-health-service-navigation"]
---

# AI Pulse Belt — Concept Design for the Centennial Jing-Zhang AI Innovation Belt

**One-page executive summary (concept proposal)**: this proposal's core claim is "AI Pulse Belt (智脉一带)" — turning the centennial Jing-Zhang "iron pulse" into the "digital pulse" of the AI era. Three levels respond to announcement clause 1.4: coordinated research area 43.6 km², overall design area 11.413 km² (vs official 11.4, 0.11% deviation disclosed), and three key areas totaling 368.4 ha; the "one belt, three cores, two wings, multiple points" structure implements the five tasks of announcement 1.5(2); 12 scenario cards, 3 industry test scenarios, 5 persona profiles, and 3 AI pilgrimage landmarks form an experienceable, operable, and governable AI-city picture; the **Pulse Protocol** (P1 declare—P2 test—P3 release—P4 review) defines declaration, testing, release, and retirement boundaries for every public AI service; 155 parcels in 13 land-use classes, 84 conceptual buildings, and 9 geometry layers are all recomputable, with provisional boundaries and data gaps disclosed item by item [metric:site_area_sqm] [metric:key_area_count]. All content is concept suggestion; once official boundaries, control conditions, and surveys are released, everything is recomputed under P4. Deliverables: bilingual narrative, A3 booklet, A0 boards, offline interactive HTML, and structured metrics/compliance/risk registries.

## Design Basis and Source List

This formal proposal takes the *Pre-Qualification Announcement for the International Urban-Design Solicitation of the Centennial Jing-Zhang AI Innovation Belt* issued by the Haidian Branch of the Beijing Municipal Commission of Planning and Natural Resources as its primary basis, and the provisional boundaries, key areas, enums, metrics, and source inventory maintained in `brief/site-package/` as machine-readable basis. Before generating the design, the AI agent read `design_brief.json`, `allowed_design_space.json`, `sources.json`, `enums/`, `ranges/`, `schemas/`, `data/source_registry.json`, and `data/processed/agent_fact_pack.md`, and built task, scope, source-use, and gap checklists from `project_scope_summary.csv`, `agent_task_requirements.csv`, `source_use_matrix.csv`, and `missing_data_checklist.csv`. Every design judgment is decomposed into traceable sources, reproducible metrics, verifiable layers, and human-reviewable assumptions. The announcement requires control-detailed-planning-level urban design and integrated-implementation-plan-level urban design depth; narrative text therefore does not replace the GeoJSON layers, metrics tables, A3 booklet, A0 boards, and HTML presentation deliverables [source:OFFICIAL-ANNOUNCEMENT] [source:AGENT-TASKBOOK] [depth:existing_conditions_diagnosis].

The source registry is used with the following boundaries [source:SOURCE-REGISTRY]:

- `data/source_registry.json` records the usage boundaries of public, cleared, and provisional materials; current summary: 7 formal-ready sources, 1 background source, 1 provisional-only source.
- This proposal uses provisional boundaries only for design generation, self-checking, visualization, and design discussion — never upgraded to official boundary, statutory control, formal scoring basis, or government implementation commitment.

`data/processed/agent_fact_pack.md` is a reading-navigation layer, not a new authority [source:PROCESSED-FACT-PACK]. Factual judgments return to the registered source materials; the full source graph is kept in `sources.json`.

Since the official `SITE_BOUNDARY` and the three `KEY_AREA` polygons are not yet available, this proposal generates its formal package from `brief/site-package/geometry/provisional_boundaries.geojson` [source:BOUNDARY-SOURCE] [source:KEY-AREA-SOURCE]: both `geometry/site_boundary.geojson` and `geometry/key_areas.geojson` are marked `provisional_constraint` and do not claim `official_boundary=true`; they may be used only for design generation, self-checking, visualization, and discussion. The measured overall-design area is 11.413 km2 vs the official pre-announcement value of 11.4 km2 (0.11% deviation), disclosed in `assumptions.json` (ASSUME-002) [data:geometry/site_boundary.geojson#PROV-SITE-001] [metric:site_area_sqm]. The count of three key areas is verified against its own layer [data:geometry/key_areas.geojson#PROV-KEY-001] [metric:key_area_count]. The organizer's data gap does not block content scoring; once official polygons are released, site boundary, key areas, land use, roads, green space, public space, buildings, phasing, and metrics must all be recomputed.

## Three-Level Scope Framework

The proposal organizes work in the three scopes defined by the announcement: the **coordinated research scope** of 43.6 km2, covering the AI industry ecosystem, strategic positioning, innovation chain, and future-city form; the **overall design scope** of 11.4 km2, producing the urban-renewal framework, industrial spatial layout, transport-utility support, and urban-form control; and the **key-area scope** of 368.4 ha across three detailed-design areas, specifying functions, spatial moves, public-space connectivity, and transport organization. The three scopes are mapped one-to-one in `compliance_matrix.json`, guaranteeing that mandatory tasks 1.3, 1.4, 1.5 and agent.1–agent.6 each carry sections, layers, metrics, drawings, and HTML evidence [depth:three_level_scope_framework] [depth:overall_spatial_structure] [standard:PROJECT-OFFICIAL-ANNOUNCEMENT].

The overall concept is the **"AI Pulse Belt" (智脉一带)**: carrying forward the century-old "iron pulse" of the Jing-Zhang Railway as memory and linear spatial skeleton, and shaping an AI-era "digital pulse belt." The north-south central greenway corridor forms the "belt" (corresponding to task 1.5(2)4, the "Jing-Zhang Ruins Park vitality belt": the central Pulse greenway is the pulse-era carrier of the vitality belt within the overall design scope, and the Qinghuayuan Station site and the heritage components along the corridor all sit within it); the three key areas — Zhongzhizui (Zhongguancun AI Acceleration Area), the Beijing AI Origin Community, and Dazhongsi — form the "three cores"; the Xiaoyue River scenario-enabling wing (west blue-green interface) and the Zhongguancun technology-service wing (east industry-service interface) form the "two wings"; AI scenario nodes and the slow-traffic network form the "multiple nodes" — an "**one belt, three cores, two wings, multiple nodes**" spatial structure. The logo motif is the character "脉" (pulse) morphing from railway rails into an oscilloscope waveform, in Jing-Zhang iron grey (#4A5560) and AI cyan (#0FA3B1), with the slogan "**A Century of Tracks, a Pulse of Intelligence**."

| Scope | Design question | Answer | Data anchor |
| --- | --- | --- | --- |
| Coordinated research | How to organize the AI ecosystem and future-city form | Innovation chain "university source—open-source collaboration—enterprise transformation—public experience—global outreach" + three-district two-wing coordination | compliance_matrix.json, standard_matrix.json |
| Overall design | How to map industry space, renewal, transport-utilities, and form | 260 m central greenway, "two-horizontal two-vertical" road skeleton, four zone bands, 155 land parcels seamless cover | [data:geometry/land_use.geojson#LU-001], [data:geometry/roads.geojson#ROAD-001] |
| Key areas | How to reach detailed-design depth for three districts | Positioning, spatial moves, AI scenarios, and pilgrimage landmarks per district | [data:geometry/key_areas.geojson#PROV-KEY-001], [data:geometry/key_areas.geojson#PROV-KEY-002], [data:geometry/key_areas.geojson#PROV-KEY-003] |

The three scopes are not disconnected drawings: the research scope sets industry-chain and city-form judgments, the overall design scope implements them as renewal projects and spatial structure, and the key-area design verifies implementability at parcel, building, transport, public-space, and AI-scenario level [source:PROCESSED-FACT-PACK]. Any area, ratio, scale, or project count that cannot be recomputed from structured data is not written into formal conclusions.

![Concept map of the overall design area and coordinated research scope](assets/figures/site-overview.en.png)

## Coordinated Research Area: Industry and Future City Research

The core task of the coordinated research scope is to build a world-class AI innovation ecosystem. The proposal organizes Haidian's universities, institutes, leading enterprises, computing-power/algorithm/data-factor resources, incubators, and tech services into a five-link innovation chain — "university source—open-source collaboration—enterprise transformation—public experience—global outreach" — and responds to the taskbook's required "three positioning, five functions, and three-district two-wing coordination loop" [source:AGENT-TASKBOOK] [standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK]: the **three solicitation purposes** (announcement 1.3) — building a world-class AI innovation ecosystem, building a new urban form adapted to AI new-quality productive forces, and building a high-quality urban district sought by global AI talent — are answered one by one by the ecosystem map and innovation chain (this chapter), the overall spatial structure (Chapter 3), and the talent profiles and scenario system (Chapter 6); the **five overall design tasks** (announcement 1.5(2)) — industrial goals and functional layout, urban-renewal overall framework, transport-rail-utilities support, the Jing-Zhang Ruins Park vitality belt, and urban form — are implemented task by task in Chapters 4–9; the **three-district two-wing coordination loop** organizes the industry—space—service cycle through the three key areas (the three districts) and the east-west wings (the two wings) (see the table below).

**Ecosystem map (concept suggestion)**: drawing on global AI-district practice, six spatial mechanisms are distilled: **land supply** (reserve land, class 16, 4 parcels, for future uses), **spatial organization** (courtyard R&D blocks), **industry services** (one-stop computing/data/compliance/investment services), **capital mechanisms** (scenario opening and government procurement guidance), **talent services** (talent-special-zone and young-worker housing), and **data scenarios** (open test fields and evaluation systems). Six reference cases and their transferable mechanisms and limits:

| Case | Transferable mechanism | Jing-Zhang application | Conditions not transferable |
| --- | --- | --- | --- |
| Punggol Digital District (SG) | Integrated industry-education-living digital test bed | Zhongzhizui R&D belt and test-field organization | Singapore's single-land-agency and fiscal model differ |
| Kalasatama (Helsinki) | Agile test district, resident co-testing, time-boxed trials | Controlled testing and public review on the Xiaoyuehe wing | Municipal data and procurement regimes differ |
| Seoul AI Hub | Government-nurtured AI enterprise platform | Zhongzhizui industry services and computing entry points | Korea's industrial ecology and financing structure are not portable |
| The Foundry (Cambridge) | Campus—park—community triangle linkage | Origin Community's near-campus incubation interface | Cambridge land and research-funding structure differ |
| Waterfront Toronto | Lakeside innovation corridor, public-private development | Dazhongsi station-front and greenway interface organization | Canadian public funding and development finance differ |
| STATION F (Paris) | Mega-incubator plus district-scale innovation network | Origin release hall and open-workstation operations | EU funding and French labor institutions differ |

All global-case conclusions are concept references for professional deepening, not confirmed government arrangements.

**Three-district two-wing industrial layout (concept suggestion)**:

| District | Industry focus | Spatial anchor |
| --- | --- | --- |
| Zhongzhizui AI Acceleration Area | Foundation-model training, full-stack independent innovation, standards, safety governance | Northern R&D belt, standards culture hall, sports test field [data:geometry/land_use.geojson#LU-001] |
| Beijing AI Origin Community | Campus-proximate incubation, open-source system, talent zone, results publishing | Origin release hall, Tsinghua-East-Road education belt, Wudaokou mixed-use belt [data:geometry/land_use.geojson#LU-001] |
| Dazhongsi AI Industry Cluster | Agents, smart terminals, content consumption, data factors | Zhichun-Road commercial belt, data-factor tower, station-front commerce [data:geometry/land_use.geojson#LU-001] |
| Xiaoyue River enabling wing (west) | Scenario trials, ecology experience | Western protective green with test segments [data:geometry/green_space.geojson#GREEN-001] |
| Zhongguancun service wing (east) | Tech services, international exchange; hosts the six support mechanisms — land, capital, talent, computing, data, scenarios | Research and service platforms and industry-service facilities along Xueyuan Road [data:geometry/land_use.geojson#LU-001] |

**Regional collaboration interfaces (concept suggestion)**: the coordinated research scope links the wider innovation network through five interfaces; no cross-district agreement is confirmed at this stage, and the interfaces express negotiable directions only [source:AGENT-TASKBOOK]:

| Interface | Collaboration question | Suggested interaction | Boundary & premise |
| --- | --- | --- | --- |
| Beiwu community | How community-level AI services fit different residential conditions | Cross-community comparison re-tests, shared problem checklists | Public issues only; no fabricated joint operation or resident authorization |
| Future Science City | Paths for frontier technology from lab to urban scenario | Mutual borrowing of expert review methods, R&D feedback loops | Research outputs make no productization commitment; no pre-publication of unreviewed conclusions |
| Huairou Science City | Translating large-science-facility outputs into urban life services | Interdisciplinary validation suggestions, measurement-method exchange | No access to non-public research or facility data |
| Beijing E-Town | Real-world conditions and safety requirements of robotics and smart manufacturing | Production-environment re-test records, mutual recognition of safety requirements | No fabricated enterprises, orders, or production-line cooperation |
| Jing-Jin-Ji city network | Cross-city comparable public-service problems and difference attribution | Off-site re-tests, difference notes, published failure records | Single-site results never replace cross-city validation |

The future-city form study answers how AI changes work, life, social interaction, learning, transport, and public services, using the "digital pulse belt" as spatial thread to locate AI transport systems, continuous green space, innovation service facilities, and an international living-working atmosphere into identifiable districts, nodes, corridors, and scenarios [depth:overall_spatial_structure] [standard:MOHURD-URBAN-DESIGN-MEASURES]. Global AI activities, developer communities, open scenarios, and pilgrimage routes are phrased as "concept suggestions / reference proposals," never as confirmed government events or implementation arrangements.

**Alignment with territorial spatial planning (concept suggestion)**: all spatial claims are expressed under the boundary of "aligning with the ongoing territorial spatial master plan and block-level regulatory plans without substituting statutory plans" — land-use classification reuses the enumeration of the MNR Guideline for Land-Use Classification in Spatial Survey, Planning, and Use Control (for trial implementation) [standard:MNR-LAND-USE-CLASSIFICATION-GUIDE]; development intensity and building height carry no numeric conclusions (pending official control conditions, see ASSUME-003 and A-CONTROLS-001); reserve flexible land keeps room for future use change; once the official territorial spatial plan and control conditions are released, this proposal recomputes metrics, updates layers, and re-discloses under Pulse Protocol beat P4 [depth:risk_missing_data] [source:AGENT-TASKBOOK].

## Overall Design Area: Urban Renewal and Regulatory-Plan-Level Urban Design

**Existing-conditions diagnosis (based on public sources, concept level)**: the diagnosis below relies only on the public brief, public maps, and provisional geometry; it is not an official survey conclusion and must be re-verified once official surveys and control conditions are released:

| Existing element | Public-source basis | Data gap and treatment |
| --- | --- | --- |
| Railway and heritage sites | Jing-Zhang railway historic alignment, Tsinghua Garden station site, Jing-Zhang heritage park vitality belt (announcement 1.5(2)4) | Precise current track alignment awaits official drawings; expressed conceptually [data:geometry/constraints.geojson#CONSTRAINTS] |
| Rail stations | Metro stations and existing rail network (public maps) | Station red lines and interchange land await official confirmation |
| Water system | Qing River, Xiaoyue River positions (public water data) | Blue-line boundaries await official blue-line drawings |
| Road skeleton | North 5th Ring Road, Xueyuan Road, Zhichun Road etc. (public road network) | Road red-line widths await official block-level controls |
| Land-use base map | Existing-use classification and 155-parcel fit (provisional) [data:geometry/land_use.geojson#LU-001] | Ownership and use follow national land-survey data |
| Public services | Wudaokou commercial area, educational facilities (public information) | Current facility capacity awaits survey |
| Industry carriers | Zhongguancun and Xueyuan Road research and industrial parks (public information) | Current building functions await verification |
| Green resources | Existing green space about 284.8 ha (25.0%, provisional recomputation) [metric:green_ratio] | Green-line boundaries await official green-line drawings |
| Heritage elements | Dazhongsi, Tsinghua Garden station etc. (public heritage lists) | Protection scope and construction control zones await official delimitation [data:geometry/constraints.geojson#HERITAGE-01] |

The overall design scope (measured 11.413 km2) requires control-detailed-planning-level urban-design depth [standard:MOHURD-CONTROL-DETAILED-PLANNING]. The proposal puts forward an overall structure with the **central Pulse-Belt greenway** as its spine [data:geometry/land_use.geojson#LU-001], organizing land use on both sides into **four zone bands** — the Zhongzhizui R&D band (north), the Origin Community mixed band, the Dazhongsi commercial-R&D band, and the southern renewal band — with reserve land (class 16, 4 parcels) at the south end for future AI uses [depth:land_use_layout] [depth:development_intensity_controls]. **Reserve-land registry (concept suggestion)**: the four reserve parcels are numbered RES-01 (southern flexible cluster), RES-02 (greenway-east flexible parcel), RES-03 (Zhongzhizui south-edge flexible parcel), and RES-04 (Dazhongsi north-edge flexible parcel); no use is preset, activation awaits official control conditions and industry-introduction confirmation; reserve land takes no part in this proposal's metric calculations or approval conclusions [data:geometry/land_use.geojson#LU-001] [depth:risk_missing_data].

**Road network (concept suggestion)**: a "two-horizontal, two-vertical" skeleton — horizontal: North 5th Ring Road (expressway), Tsinghua East Road (secondary), Chengfu Road (branch), Zhichun Road (arterial); vertical: Xueyuan Road/Xitucheng Road (arterial), Heqing Road/Dazhongsi East Road (secondary); plus new design streets — **Pulse-Belt Avenue (智脉大道)**, Pulse-2nd Street, Pulse-3rd Street — organizing block-level micro-circulation, with a continuous greenway inside the central corridor [data:geometry/roads.geojson#ROAD-001] [data:geometry/roads.geojson#ROAD-010].

**Land use (concept suggestion)**: `geometry/land_use.geojson` contains 155 parcels across 13 land-use classes, completely and seamlessly covering the design boundary (difference <1 m2, verified by `validate_cover`) [data:geometry/land_use.geojson#LU-001]. Research land (0802) dominates, supported by commercial (05), residential (0701), cultural (0803), and educational (0804) uses; the central corridor (1401 park green) is about 260 m wide, running north-south [data:geometry/green_space.geojson#GREEN-001]. `geometry/buildings.geojson` expresses 84 conceptual building footprints (design_proposal attribute, non-overlapping, not statutory permits) [data:geometry/buildings.geojson#BLDG-001] [metric:building_footprint_area_sqm]. **Content involving building heights, development intensity, road red lines, setbacks, roof form, massing, and facility standards is treated as "pending confirmation of official control conditions" until official controls are released — agent-estimated values are never presented as approved indicators.**

![Conceptual land-use structure of the overall design area](assets/figures/land-use-structure.en.png)

## Detailed Design of Key Areas

The three key areas reach integrated-implementation-plan design depth [depth:three_key_area_detailed_design], each anchored in [data:geometry/key_areas.geojson#PROV-KEY-001], [data:geometry/key_areas.geojson#PROV-KEY-002], [data:geometry/key_areas.geojson#PROV-KEY-003].

| Key area | Design positioning | Spatial moves | AI industry & operation scenarios | Evidence |
| --- | --- | --- | --- | --- |
| Zhongzhizui AI Acceleration Area (192.1 ha) | Garden-type full-stack independent innovation block | Green buffer along the 5th Ring; gateway plaza access; R&D courtyards + standards culture hall + sports test field + reserve land; integrated building—green—water design drawing on the Qinghe River and site water-green resources, showcasing Qinghe culture (concept) | Foundation-model training/testing, standards workshops, safety-governance showcases, low-carbon computing experience | [data:geometry/key_areas.geojson#PROV-KEY-001], [data:geometry/land_use.geojson#LU-001], [data:geometry/public_space.geojson#PUBLIC-003] |
| Beijing AI Origin Community (104.3 ha) | Campus-proximate transformation and talent community | Tsinghua-East-Road education belt stitching campus and park; origin release hall (0803 culture); Wudaokou mixed-use belt; community services embedded | Open-source community, results publishing, talent-special-zone services, campus-proximate incubation | [data:geometry/key_areas.geojson#PROV-KEY-002], [data:geometry/public_space.geojson#PUBLIC-002], [source:AGENT-TASKBOOK] |
| Dazhongsi AI Industry Cluster (72.0 ha) | Station-city integrated intelligent economy block | Station-forecourt four-quadrant pedestrian connectivity; Zhichun-Road commercial belt; data-factor tower; station-front mixed commerce | Agent & smart-terminal showcases, content consumption, data factors, international roadshows | [data:geometry/key_areas.geojson#PROV-KEY-003], [data:geometry/public_space.geojson#PUBLIC-001], [metric:key_area_count] |

**Three-area concept mini-proposals (six-element expansion; all concept suggestions)**:

- **Zhongzhizui AI Independent-Innovation Acceleration Area (192.1 ha)**: positioned as a garden-style full-stack independent-innovation block; structure of "one spine, two bands, three clusters" — the northern Pulse-Belt greenway as spine, R&D band and living band in parallel, training/testing, standards-governance, and low-carbon-compute clusters around the gateway plaza; spatial moves include a green buffer along the North 5th Ring, gateway-plaza interchange, R&D courtyards with reserve land for the sports test field, and integrated building-green-water design showcasing Qing River culture; AI scenarios are LLM training/testing, standards workshops, safety-governance exhibits, and low-carbon compute experience (cards 06/10); implementation starts with P1-P2 declaration and controlled testing, carried by renewal project JZ-06; risks center on compute dependency and airspace approval, with rollback triggers R-01/R-04 [data:geometry/key_areas.geojson#PROV-KEY-001].
- **Beijing AI Origin Community (104.3 ha)**: positioned as a near-campus translation and talent community; structure of "education-band stitching + Origin Release Hall + Wudaokou commercial-living belt"; spatial moves include stitching campus and park along Tsinghua East Road, the Origin Release Hall, embedded community services, and open-air developer workstations (card 12); AI scenarios are open-source community, results release, talent-zone services, and near-campus incubation; implementation targets P3 public operation and regular P4 reviews, carried by renewal projects JZ-03/JZ-04; risks center on campus data authorization and translation windows, with rollback trigger R-02 [data:geometry/key_areas.geojson#PROV-KEY-002].
- **Dazhongsi AI Industry Cluster Area (72.0 ha)**: positioned as a station-city integrated intelligent-economy block; structure of "pre-station four-quadrant walking ring + Zhichun Road commercial belt + data-elements tower"; spatial moves include four-quadrant pedestrian connectivity at the Dazhongsi station plaza, station-city commercial integration, Zhongyun cultural performance (card 04), and multimodal wayfinding evaluation (card 08); AI scenarios are agent and intelligent-terminal showcases, content consumption, data elements, and international roadshows; implementation links the station-city renewal project JZ-12 with the Global AI Week; risks center on heritage conflict and station-city coordination, with rollback trigger R-03 [data:geometry/key_areas.geojson#PROV-KEY-003].

The three key areas are presented as `provisional_constraint` in `geometry/key_areas.geojson`; the narrative, HTML, sources, assumptions, and self_check all state they cannot serve as formal scoring or approval basis. `compliance_matrix.json` covers announcement clauses 1.5.3.1, 1.5.3.2, 1.5.3.3. The design expression includes functions, conceptual buildings, public-space systems, transport organization, and implementation projects; the A3 booklet and A0 boards include key-area master plans, detail maps, and metric notes, and the HTML page allows toggling among the three key areas.

![Key-area detailed design concepts (concept suggestion)](assets/figures/key-areas.en.png)

## AI Innovation Ecosystem, Personas, and AI+ Scenarios

The proposal builds spatial-need profiles for AI talent and enterprises, and a two-track scenario system of "industry development scenarios + AI-enabled urban-function scenarios." Every scenario states its spatial carrier, data and human boundary, operating body, and exit condition; the eight-element structure (service users, spatial carrier, user journey, input data, AI capability, infrastructure, operating body, failure degradation) makes every scenario locatable, operable, and governable [source:AGENT-TASKBOOK].

**5 user profiles**:

| Profile | Typical needs | Spatial response | Risk that cannot be ignored | Self-check boundary |
| --- | --- | --- | --- | --- |
| Startup engineers | Low-cost offices, computing access, product test fields | Zhongzhizui shared test field, edge-computing service points, standards consultation | Dependency on a single computing/data supplier | Computing and data services require separate authorization; keep public test fields and standards entry points against lock-in |
| Researchers | Cross-institution collaboration, transformation, academic exchange | Origin release hall, R&D courtyards, Tsinghua-East-Road education belt | Short transformation windows, dependence on one-off policies | Campus data and research results require authorization; support routine courtyard exchange, not single-policy dependence |
| Family weekend visitors | Leisure, sports, cultural experience | Central greenway, pocket parks, sports test field, bell-culture experience | Peak crowd capacity and image-privacy concerns | No personal behavior tracking; aggregated activity statistics only; peak-hour diversion |
| Senior tourists | Barrier-free wayfinding, slow leisure, cultural explanation | Barrier-free AI wayfinding stations, Pulse-Rail art rest belt | Digital divide causing digital exclusion | Health data never used for commercial recommendations; keep non-AI channels (guided tours, phone booking) |
| Developer-community operators | Event organizing, code collaboration, community reputation | Open-air developer workspace code wall, release plaza, Box meeting pavilions | Subsidy-dependent events stall when subsidies end | Public activity data anonymized and aggregated; manage events by "launch—trial—evaluate—continue/retire" |

**12 scenario cards (concept suggestion)**:

| Card | Spatial carrier & description | Data & human boundary | Operating body | KPI & exit condition |
| --- | --- | --- | --- | --- |
| 01 Rail-inspection AR twin | Central greenway rail segment: AR overlays of century-old Jing-Zhang imagery with an AI digital-twin inspection demo | Aggregated footfall heat only; no personal imagery | Rail-heritage operator + district test office | AR factual accuracy ≥98%; unresolved factual complaints take it offline |
| 02 Autonomous shuttle corridor | Pulse-Belt Avenue: campus—station autonomous shuttle demo line (concept) [scenario:ai-traffic-walkability] | Trip data for dispatch only; anonymized after retention | Bus group + district test office | On-time rate ≥85%; any accident stops the line for manual service |
| 03 AI cycling coach station | Greenway nodes: cycling data visualization with AI coaching | Ride data visible to the user only; one-tap deletion | Subdistrict + greenway operator | Equipment fixed within 24h; privacy complaints pause it |
| 04 Bell-chime metaverse | Dazhongsi station front: digital-twin and interactive performance of the bell culture [scenario:ai-cultural-guide] | No personal behavior tracking | Dazhongsi cultural institution + district | Content complaints answered ≤48h; heritage conflicts remove it |
| 05 Box meeting pavilion | R&D block nodes: self-service meetings, live streaming, remote collaboration micro-spaces | Audio/video held by the user; platform keeps nothing | Park operating platform | High no-show rates trigger capacity changes; complaints stop it |
| 06 Drone delivery station | South Zhongzhizui block: low-altitude logistics trial station (concept) [scenario:robot-delivery-low-speed] | No facial capture; delivery records deleted in 30 days | Delivery enterprise + airspace regulator | Zero tolerance for safety hazards; no operation without airspace approval |
| 07 AI-gardener pocket park | Residential corners: AI-assisted plant care with community adoption | Plant-care and adoption data only | Community committee + subdistrict | Adoption rate ≥30%; noise complaints trigger adjustments |
| 08 Barrier-free AI wayfinding | Station and greenway nodes: voice/tactile multimodal accessible navigation [scenario:ai-health-service-navigation] | No personal trajectory storage; on-site verifiable | Disabled federation + operator | 100% human-alternative rate; off-site mismatch stops it |
| 09 Event-data visualization wall | Sports test field vicinity: real-time big-screen of smart sports events | Aggregated display only; no personal identification | Sports body + event operator | Data provenance time-stamped; alerts require human judgment |
| 10 AI energy-management building | Zhongzhizui R&D belt: distributed energy and AI-driven energy control demo (concept) | Energy data aggregated per building; never per household | Energy enterprise + park property | Immediate manual takeover on control errors; repeated errors decommission it |
| 11 AI coffee robot station | Commercial and R&D corners: robotic-arm coffee experience and developer social hub | Minimal order data; standard payment channels | Commercial operator | Mechanical faults stop it; complaints answered ≤24h |
| 12 Open-air developer workspace code wall | Origin release plaza vicinity: open-source contribution wall, open-air workstations, demo zone | Public contribution data anonymized-aggregated | Open-source community + district operator | Human final review of content; disputes take it down |

Scenario cards unfold through an eight-element structure: **service users, spatial carrier, user journey, input data, AI capability, infrastructure, operating body, failure degradation**. Card 01 (rail-inspection AR twin) as example: the journey is scan-to-view — AR overlays century-old imagery, then footfall heat aggregation display; input data are public imagery and inspection points (no personal imagery); AI capability is image registration and historical-fact comparison; infrastructure is recognition posts and wayfinding screens along the segment; failure degradation is an on-screen hint and manual verification when recognition fails. The remaining cards unfold under the same structure at detailed-design stage.

**3 industrial test-and-verification scenarios (concept suggestion)**: each scenario anchors a test node in `geometry/public_space.geojson` and operates under Pulse Protocol beat P2 (controlled pilot):

| Test scenario | Location & scope | Test content | Data & safety boundary | KPI & exit condition |
| --- | --- | --- | --- | --- |
| Open vehicle-road-coordination test segment | Concept 1.2 km on Pulse-Belt Avenue [data:geometry/public_space.geojson#PUBLIC-013] | Vehicle-road coordination and autonomous shuttle (card 02) [scenario:ai-traffic-walkability] | Vehicle-state and road-condition data for testing only; any accident stops and returns to manual | No major accident in accumulated tests; any major accident halts testing |
| Low-altitude delivery route verification | Concept Zhongzhizui–Dazhongsi route [data:geometry/public_space.geojson#PUBLIC-014] | Drone delivery (card 06) [scenario:robot-delivery-low-speed] | Subject to airspace and safety regulations; no facial capture | No operation without airspace approval; zero tolerance for safety hazards |
| Multimodal wayfinding evaluation ground | Central greenway node [data:geometry/public_space.geojson#PUBLIC-015] | Multimodal evaluation of barrier-free wayfinding (card 08) | No personal trajectory storage; on-site verifiable | On-site mismatch stops it |

**Public-safety AI applications are studied as operations-review research only and never replace human review** [scenario:public-safety-operations-review]. **Health-service applications** (appointment escort tips, first-aid point guidance, chronic-care information prompts, etc.) provide informational hints only — never medical decisions, and no data persistence [scenario:ai-health-service-navigation] [data:geometry/public_space.geojson#PUBLIC-016].

**3 AI pilgrimage landmarks (concept suggestion)**: the **Bell of AI Origins** (Dazhongsi station-forecourt plaza; bell culture meets AI-origin imagery), the **Tower of AI Light** (Zhongzhizui gateway plaza; light art with real-time model-inference visualization), and the **Pulse-Rail Art Track** (northern central greenway; artistic reuse of disused rails with digital projection). The pilgrimage route "A Century of Tracks, a Pulse of Intelligence" links to the "Global AI Week public route" (renewal project JZ-12) [data:geometry/public_space.geojson#PUBLIC-001] [data:geometry/green_space.geojson#GREEN-001]. The related public-space and green metrics are `known` in `metrics.json` and directly recomputable [metric:public_space_ratio] [metric:green_ratio].

**Honor display system (concept suggestion)**: the developer contribution wall (card 12 code wall), the co-creator honor screen, and the annual Pulse Award form a progressive honor ladder, linked to the public review of Pulse Protocol beat P4; honor data aggregate only public contributions and never produce personal scores.

**Annual event system and community operations (concept suggestion)**: a "one theme per season" annual rhythm — **Developer Conference** (open-source and standards governance, contribution-wall release), **Scenario Open Day** (public access to controlled tests of scenario cards, linked to beat P2), **Global AI Week** (pilgrimage route and multilingual international roadshows, linked to renewal project JZ-12), and **Annual Pulse Awards & review meeting** (linked to P4 review and the honor ladder). Community operations manage all events by "initiate—pilot—evaluate—continue or retire," with public event data aggregated anonymously and deleted on retention expiry; the attraction-conversion path is "scenario exposure → test contract → incubation entry → policy payoff," linked to the Wudaokou commercial-living belt, the Origin Release Hall, and reserve flexible land [source:AGENT-TASKBOOK] [depth:renewal_project_list] [data:geometry/land_use.geojson#LU-001].

AI governance suggestions follow data-minimization, public-source, explainability, and human-review principles [standard:GENERATIVE-AI-INTERIM-MEASURES]: city agents may assist in identifying slow-traffic gaps, public-space heat, facility maintenance, enterprise-service demand, and event-safety risk — but never replace planning approval, never output unauthorized personal profiles, and never claim official implementation commitment. All scenario nodes enter the structured layers or compliance matrix.

**Public interest and inclusive design (concept suggestion)**: accessibility [standard:BARRIER-FREE-ENVIRONMENT-LAW] [standard:ELDERLY-SMART-TECH-PLAN-2020-45], age-friendliness, and digital equity are baseline — non-AI alternative channels (guided tours, phone booking, in-person services) always remain; applications touching public interest or personal data undergo privacy impact assessment (PIA); conflicts of interest between operators and developers are handled through protocol disclosure and the public committee's appeal mechanism; the needs of night workers, low-income groups, and non-digital users are item-by-item rechecked at detailed-design stage.

### Pulse Protocol (operating mechanism)

The proposal defines a four-beat operating loop for every AI service entering public space, homologous to the "Pulse Belt" name: like a pulse, each service has explicit beats of declaration, testing, release, and review — no service may linger indefinitely in "pilot" status, and none may be released without testing [standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK] [depth:renewal_project_list]:

| Beat | Action | Boundary condition | If not met |
| --- | --- | --- | --- |
| P1 Declare | State service purpose, data ceiling, responsible party, human-equivalent path, and end condition | Any missing element blocks testing | Return for supplements |
| P2 Test | Controlled pilot: booking, zoning, on-site safety officer, physical emergency stop, independent re-test | Release requires completed re-test | Fix and re-test, or withdraw |
| P3 Release | Public operation with wayfinding status lights: steady waveform=operating, pulsing=testing, flat line=decommissioned | Any boundary failure degrades back to P2 | Stop service and restore the site |
| P4 Review | Data re-check, public feedback, and published failure records; decide continue, adjust, or retire | No renewal without review | Retire and complete data/site restoration |

**Unified rollback triggers (five classes)**: any AI service exhibiting the following situations degrades or stops under the protocol — **safety** (physical or online safety incidents; any accident stops it), **privacy** (data breach or upheld complaint), **heritage** (conflict with heritage or urban-form protection; remove), **ecology** (nuisance, noise, or public-space occupancy disputes), **economics** (unsustainable operation without alternative funding). The trigger list maps one-to-one to each scenario card's exit conditions and enters the public record of beat P4 review.

**Flat-line archive wall (concept suggestion)**: a "flat-line archive wall" in the northern Pulse-Belt greenway publicly exhibits every AI service retired under P4 — service name, operating period, review conclusions, and failure records shown in anonymized form, echoing the wayfinding status light "flat line = retired"; retirement is governance evidence, not failure concealment, and any service may re-enter P1 declaration after improvement [source:AGENT-TASKBOOK] [data:geometry/green_space.geojson#GREEN-001].

**Executable protocol registry**: the machine-readable tabletop record of the protocol is `simulation.json` — 15 public AI services (12 scenario cards + 3 test scenarios) each checked against the five P1 declaration elements, P2 testing status, the P3 wayfinding status light, and the five rollback trigger classes, verifiable by a tabletop script; the record is concept expression and does not mean any service is implemented or approved [data:simulation.json] [standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK].

All 12 scenario cards, 3 industrial test-and-verification scenarios, annual events, and pilgrimage landmarks define their operating boundaries under this protocol; the protocol is an operating-mechanism suggestion and does not replace planning approval, industry regulation, or statutory assessment.

## Land Use, Building Scale, and Retain-Renovate-Demolish Strategy

The land-use plan follows public land-use survey, planning, and regulation classification standards, forming complete, closed, seamless zoning [standard:MNR-LAND-USE-CLASSIFICATION-GUIDE] [data:geometry/land_use.geojson#LU-001]. Of the 13 classes, research 0802 dominates (14 parcels), with commercial 05 (10), residential 0701 (6), education 0804 (6), medical 0806 (6), culture 0803 (3), sports 0805 (1), community service 0702 (1), park green 1401 (12), protective green 1402 (9), plaza 1403 (2), road 1207 (81), and reserve 16 (4) — 155 parcels total, seamless [depth:land_use_layout].

The building plan distinguishes retained, renovated, renewed, new, and to-be-confirmed objects: because existing buildings, ownership, control plans, and engineering conditions are absent, the proposal provides only a **method framework and to-be-calibrated checklist, without fabricating retain-renovate-demolish conclusions** [depth:retain_renovate_demolish] [depth:height_massing_character] [standard:MOHURD-ARCH-DESIGN-DEPTH-2016]. All 84 conceptual buildings in `geometry/buildings.geojson` carry `status=design_proposal`, `confidence=low`, expressing massing intent only [data:geometry/buildings.geojson#BLDG-001] [metric:building_footprint_area_sqm]. Total building scale, FAR, height, and density are uniformly `status=unknown` pending official conditions (see [metric:floor_area_ratio], whose `reason` states the missing conditions and recomputation path).

## Transport, Rail, Municipal Infrastructure, and Public Services

The transport plan responds to the announcement's requirements on station integration, road micro-circulation, slow-traffic gaps, external access, parking, non-motorized parking, and green transport [depth:traffic_rail_slow_parking] [data:geometry/roads.geojson#ROAD-001] [data:geometry/public_space.geojson#PUBLIC-001]:

- **External access (concept)**: fast connection to the central city and surrounding areas via North 5th Ring Road (expressway), Zhichun Road (arterial), and Xueyuan Road/Xitucheng Road (arterial), aligning with the 5th-Ring regional integration construction to propose external-access improvement directions; specific ramps, cross-sections, and traffic-model deepening await transport-special-study conditions (the Zhongzhizui area prioritizes external-access improvement per announcement 1.5.3.1);
- **Rail connection (concept)**: anchored on Dazhongsi, Wudaokou, Zhichun Road, Xitucheng, and Tsinghua-East-Road-West stations, with 3 concept connector lines (ROAD-011/012/013) and an autonomous shuttle corridor (card 02) [scenario:ai-traffic-walkability];
- **Micro-circulation**: Pulse-Belt Avenue (28 m concept red line), Pulse-2nd/3rd Streets organize block-level loops; slow-traffic greenway runs the full greenway [data:geometry/roads.geojson#ROAD-010];
- **Slow-traffic gaps**: concept north-5th-Ring crossing node and greenway north/south landscape nodes (see Figure 04 and `constraints.geojson`) [data:geometry/constraints.geojson#CONSTRAINTS];
- Parking and non-motorized parking follow a "rail + shuttle + slow traffic" priority; scale to be confirmed by transport special studies and control conditions.

Utilities and public services cover AI industry services (one-stop computing/data/compliance/investment service points, with the enterprise-service copilot integrated [scenario:enterprise-service-copilot]), talent-living services, new infrastructure (edge-computing stations, distributed-energy nodes, card 10), and traditional utility integration [depth:municipal_new_infrastructure]. Missing pipeline, energy, drainage, flood-control, and fire-engineering data are listed as prerequisites for formal deepening, stated in `assumptions.json` (A-CONTROLS-001) rather than written as approved conditions.

## Blue-Green Network, Public Space, and Urban Character

**Blue-green space (concept suggestion)**: the central Pulse-Belt greenway as spine (260 m wide, north-south, total green ~284.8 ha, green ratio 25.0%) — the pulse-era carrier of task 1.5(2)4, the "Jing-Zhang Ruins Park vitality belt" [data:geometry/green_space.geojson#GREEN-001] [metric:green_ratio]; western protective belt echoing the Xiaoyue River enabling wing; eastern protective belt along Xueyuan Road; pocket parks and plazas embedded in blocks [data:geometry/public_space.geojson#PUBLIC-001] [depth:blue_green_public_space]. Six plazas (Dazhongsi station front, Origin release, Zhongzhizui gateway, Wudaokou living, Tsinghua-East-Road-West, southern community) form the public-space skeleton. The Qinghe River and site water-green resources support integrated building—green—water design in the Zhongzhizui area, showcasing Qinghe culture (concept; detailed in the Zhongzhizui design).

**Public-space component library (6 classes, concept suggestion)**: plazas (node aggregation), pocket parks (residential embedding), wayfinding nodes (waveform status-light language), event lawns (greenway segments), water features (station-forecourt fountains), and smart street furniture (charging/seats/information screens) — component reuse keeps public space recognizable, maintainable, and batch-implementable.

![Mobility network and blue-green system concept (concept suggestion)](assets/figures/mobility-bluegreen.en.png)

**Urban form (concept suggestion)**: a three-line narrative merging Jing-Zhang railway heritage, Zhongguancun innovation culture, and AI culture [depth:overall_spatial_structure] [standard:MOHURD-URBAN-DESIGN-MEASURES]: the Qinghuayuan Railway-Station heritage node and Pulse-Rail Art Track carry the rail memory; the Bell of AI Origins and Tower of AI Light carry AI culture; a wayfinding symbol system unifies the "rail—waveform" motif — public wayfinding uses a "waveform status-light" language: steady waveform=operating, pulsing=testing, flat line=decommissioned, linked to the Pulse Protocol so citizens can read an AI service's operating state without any instructions. Form control distinguishes official regulation, design suggestion, and to-be-confirmed conditions; pseudo-precise control lines are strictly avoided without heritage or control-plan basis. All brands, fonts, images, portraits, and enterprise marks require cleared sources (see `report/copyright_statement.md`).

**Visual identity (VI) specification (concept suggestion)**: the logo centers on the "脉" character with the rail—waveform motif, specifying minimum usage sizes (screen ≥24 px, print ≥10 mm), safety zone (no less than 1/4 character-height clearance), black-and-white and reversed versions, standard colors #4A5560 (Jing-Zhang iron grey) and #0FA3B1 (AI cyan) plus auxiliary tones; the font-license list and vector files are in `report/copyright_statement.md`. VI elements and the wayfinding system require official approval before implementation; this specification is a concept suggestion.

## Renewal Projects, Implementation Policy, and Phasing

Renewal project list (concept suggestion, 12 items):

| ID | Project | Type | Near-term action | Release evidence | Suggested lead |
| --- | --- | --- | --- | --- | --- |
| JZ-01 | Central Pulse-Belt greenway connection | Public space/blue-green | Pedestrian audit, temporary wayfinding, under-bridge clearance | Red lines, traffic & ecology review | District landscape bureau + transport [data:geometry/green_space.geojson#GREEN-001] |
| JZ-02 | North-5th-Ring slow-traffic crossing | Transport/slow traffic | Cross-section and overpass-condition assessment | Structural safety & crossing approval | Transport commission + design firm [data:geometry/roads.geojson#ROAD-001] |
| JZ-03 | Zhongzhizui gateway plaza & Tower of AI Light | Public space/landmark | Concept design and light-environment trial | Ownership & landscape approval | Park operating platform [data:geometry/public_space.geojson#PUBLIC-003] |
| JZ-04 | Origin release hall & code wall | Industry service/culture | Ground-floor use planning, open-source event trial | Ownership & operator confirmation | Zhongguancun open-source community + district [data:geometry/buildings.geojson#BLDG-001] |
| JZ-05 | Dazhongsi four-quadrant pedestrian connection | Station integration/slow traffic | Crossing-time, accessibility, bike-parking surveys | Station & intersection review | District + transit operator [data:geometry/public_space.geojson#PUBLIC-001] |
| JZ-06 | Pulse-Belt Avenue autonomous shuttle demo | Transport/new infra | Regulation review and signal-condition assessment | Road-test filing & safety plan | District test office + bus group [data:geometry/roads.geojson#ROAD-010] |
| JZ-07 | Tsinghua-East-Road education-belt stitching | Renewal/education | Campus-boundary and pedestrian-safety survey | Ownership & campus consent | Subdistrict + university [data:geometry/land_use.geojson#LU-001] |
| JZ-08 | Southern renewal band upgrade | Renewal/residential | Existing-building and land survey | Retain-renovate-demolish special study | District + planning team [data:geometry/phasing.geojson#PHASE-003] |
| JZ-09 | Low-altitude delivery route verification | New infra/industry test | Airspace and safety-supervision review | Airspace approval | District + regulator [data:geometry/constraints.geojson#CONSTRAINTS] |
| JZ-10 | Edge-computing & energy-control demo building | New infra/utilities | Energy and computing-demand assessment | Fire safety & operator confirmation | Energy enterprise + park [data:geometry/buildings.geojson#BLDG-001] |
| JZ-11 | Barrier-free AI wayfinding system | Public service/accessibility | Standards and data-authorization review | Accessibility-standard re-check | Disabled federation + operator [data:geometry/constraints.geojson#CONSTRAINTS] |
| JZ-12 | Global AI Week public route | Operations/brand | Event permits and copyright clearance | Public-space permit & safety plan | Joint operating body [data:geometry/phasing.geojson#PHASE-001] |

**Protocol linkage (concept suggestion)**: the 12 projects fall into three Pulse Protocol classes — **P1 declare class** (JZ-04/07/08/11, complete declaration requirements first), **P2 test class** (JZ-06/09/10/12, controlled pilots before release), **P3 release class** (JZ-01/02/03/05, public space and infrastructure first, then included in P4 review). Each project's "release evidence" column is its first approval gate; without passing it, no project advances to the next beat.

**Phasing (concept suggestion)** (`geometry/phasing.geojson`, [depth:renewal_project_list] [depth:phasing_implementation]): **P1 near term (2026–2030)** — the three key areas first: Zhongzhizui, Origin Community core, Dazhongsi core ([data:geometry/phasing.geojson#PHASE-001]); **P2 mid term (2030–2035)** — full greenway connection plus north Dazhongsi and northern south-band ([data:geometry/phasing.geojson#PHASE-002]); **P3 long term (2035–2040)** — southern renewal band and reserve land ([data:geometry/phasing.geojson#PHASE-003]). Each phase publishes three conclusions — continue, adjust, or stop — judged on release evidence, public feedback, and the five rollback trigger classes:

| Phase | Continue condition | Adjust condition | Stop condition |
| --- | --- | --- | --- |
| P1 near term | Release evidence of the three key areas complete and no major incident in P2 tests | Scope adjusted on ownership change or public feedback | Safety/compliance rollback triggers fire |
| P2 mid term | Greenway connection completed and P4 operations review passed | Intensity and alignment adjusted after official controls release | Safety/heritage/ecology rollback triggers fire |
| P3 long term | Retain-renovate-demolish special assessment of the southern band passed | Reserve parcels switch use under official conditions | Economics/ecology rollback triggers fire |

**The 100-day solicitation cycle and implementation phasing are strictly distinguished**: the former is a submission-time requirement, the latter is the urban-renewal path. Near-term items may start with lightweight facilities, operations, and service platforms (scenario cards, pilgrimage landmarks, wayfinding); long-term items await formal control plans, utilities, transport, and ownership confirmation. The annual event system (developer conference, scenario open day, International AI Week) states operators, frequency, responsibility boundaries, and conversion paths — no slogans [source:AGENT-TASKBOOK].

**Operating governance structure (concept suggestion)**: daily operations organized as "one secretariat, three district stations, two professional wings, one public committee" — the secretariat manages the Pulse Protocol and registers; the district stations interface the three key areas; the professional wings cover industry services and public-interest services; the public committee holds knowledge, suggestion, and appeal rights over events and scenarios. Funding combines three sources — "fiscal guidance (publicly applicable), scenario-service revenue, and open-source/public-interest funds"; events run a four-step cycle of "launch—trial—evaluate—continue/retire," stopping and publicly explaining any event that fails evaluation.

## Metrics, Area Recalculation, and Compliance Matrix

The indicator system (`metrics.json`) has 9 metrics: overall-design area (site_area_sqm, measured 11,412,825.4 m2 vs official 11,400,000 m2, 0.11% deviation), building footprint area (building_footprint_area_sqm, ~110.3 ha), green ratio (green_ratio, 25.0%), public-space ratio (public_space_ratio, ~5.9 ha), key-area count (key_area_count, 3), floor-area ratio (floor_area_ratio, `status=unknown`, official FAR controls absent), and the announcement 1.5.2.1 planning indicators — AI innovation index (ai_innovation_index), talent density (talent_density), and AI output value (ai_output_value), all `status=unknown` pending official statistics and recomputable from the registered formulas once released. All known metrics are recomputable from GeoJSON [metric:site_area_sqm] [data:geometry/green_space.geojson#GREEN-001] [depth:metrics_recalculation].

| Metric | Current value | Confidence | Use |
| --- | --- | --- | --- |
| Overall-design area | 11,412,825.4 m2 | High (measured recalculation) | Denominator of all spatial ratios |
| Building footprint area | ~110.3 ha | Medium (concept massing) | Building-scale reference |
| Green ratio | 25.0% | Medium (provisional boundary) | Blue-green system performance |
| Public-space ratio | ~5.9 ha (0.52%) | Medium (provisional boundary) | Public-space system performance |
| Key-area count | 3 | High (layer verification) | Detailed-design scope confirmation |
| Floor-area ratio | unknown | Pending official conditions | Enters no conclusion |
| AI innovation index | unknown | Pending official statistics | Announcement 1.5.2.1 planning indicator (formula registered) |
| Talent density | unknown | Pending official statistics | Announcement 1.5.2.1 planning indicator (formula registered) |
| AI output value | unknown | Pending official statistics | Announcement 1.5.2.1 planning indicator (formula registered) |

![Key metrics and evidence (concept suggestion)](assets/figures/metrics-evidence.en.png)

Metrics are managed in three classes: ① spatial metrics recomputable from submitted geometry (areas, ratios, phasing areas); ② control metrics requiring official control plans (FAR, height, density, setbacks, red lines — currently `unknown`); ③ performance metrics requiring operational data calibration (AI innovation index, talent density, AI output value — formulas and data sources registered per announcement 1.5.2.1, status `unknown` pending official statistics [metric:ai_innovation_index] [metric:talent_density] [metric:ai_output_value]). The three classes enter `metrics.json`, `assumptions.json`, and `compliance_matrix.json` respectively, avoiding operational visions masquerading as approved planning conditions [standard:PROJECT-OFFICIAL-ANNOUNCEMENT].

The compliance matrix covers all mandatory tasks of announcement clauses 1.3, 1.4, 1.5 and agent.1–agent.6: agent.1 naming system and identity (this chapter and Chapter 3), agent.2 global cases and ecosystem map (Chapter 3), agent.3 scenario cards/test scenarios/profiles (Chapter 6), agent.4 pilgrimage landmarks and honor displays (Chapter 6), agent.5 cultural narrative and wayfinding (Chapter 9), agent.6 event system and community operations (Chapter 10). Results of `scripts/spatial_review.py` and `scripts/visual_review.py` serve as formal self-check evidence.

**Standard applicability boundary**: of the nine standard responses in `standard_matrix.json`, eight are addressed and one (Architectural Design Document Compilation Depth Provisions, 2016 edition) is a data_gap to be activated once official building conditions are available; any standard response constrains only this proposal's own expression and evidence approach — it never substitutes for official approval or statutory review procedures [standard:MOHURD-CONTROL-DETAILED-PLANNING] [standard:GENERATIVE-AI-INTERIM-MEASURES].

**13-dimension self-assessment against the agent taskbook (concept suggestion)**: self-assessment on the taskbook's supplemental review dimensions (self-assessment states the proposal's own position for professional review to verify):

| Review dimension | This proposal's response | Self rating |
| --- | --- | --- |
| Goal alignment | Ecosystem map, innovation chain, and pilgrimage landmarks serve the global AI-industry-highland and pilgrimage goals (Chapters 3 and 6) | Strong |
| Function match | Three positionings, five functions, and three-district two-wing layout mapped one-to-one into compliance_matrix.json | Strong |
| Brand recognition | AI Pulse Belt naming system, logo concept (rails morphing into waveform), bilingual visual system | Medium |
| Regional synergy | Five regional synergy interfaces (Beiwei Community/Future Science City/Huairou Science City/E-Town/Beijing-Tianjin-Hebei) | Strong |
| Planning innovation | Pulse Protocol operating mechanism, reserve flexible land, control-condition boundary declaration | Strong |
| Industry support | Six spatial mechanisms plus compute, data, and scenario open-testing systems | Strong |
| Scenario perceptibility | 12 scenario cards, 3 test scenarios, 3 pilgrimage landmarks — all locatable and displayable | Strong |
| Spatial clarity | All scenarios located in nodes, corridors, or areas of the 9 geometry layers | Strong |
| Transferability | Protocol-based operating boundaries, lead parties, release evidence, and P4 review mechanism | Strong |
| Expression completeness | Bilingual narrative, 5 figures, A3 booklet, A0 boards, offline HTML, structured registries | Strong |
| Public compliance | Public sources only, provisional disclosure, rights clearance, HTML zero external requests | Strong |
| International reach | AI Pulse Belt English naming, mechanism transfer from international cases, bilingual deliverables | Medium |
| Long-term operation value | Annual event system, honor ladder, three-source funding, governance structure | Strong |

## Risk, Copyright, and Compliance

**Bilingual requirement**: the Chinese master file and the English translation `proposal.en.md` are fully aligned (bilingual_contract_version 1); A3/A0 drawings, HTML, and text-bearing figures all provide bilingual expression, preferring the terminology recommended in `docs/terminology-glossary.md`. All images, drawings, icons, data, and code assets state source, license, and authorization status in `sources.json` and `report/copyright_statement.md`; the HTML page loads no remote scripts, remote map tiles, remote fonts, iframes, forms, or external APIs, and tracks no reviewer behavior.

**Risks and missing-data list**: gaps in official boundary, key areas, control plans, road red lines, parcel ownership, existing buildings, utilities, heritage, and public services all enter `assumptions.json` (ASSUME-001/002/003, A-CONTROLS-001, ASSUME-004) and this chapter; any conclusion lacking official control plans, red lines, ownership, utility, fire-safety, or heritage conditions is downgraded to a to-be-confirmed item [depth:risk_missing_data] [data:geometry/constraints.geojson#CONSTRAINTS] [source:SITE-PACKAGE].

**Risk register and human-review checklist**: the eight-dimension risk checklist (data privacy, implementation complexity, public acceptance, operations cost, policy uncertainty, spatial dispute, technology maturity, equity and inclusion) is itemized in `risk.json`, of which implementation complexity and policy uncertainty are high-attention items with human-review requirements [depth:risk_missing_data] [data:risk.json]; the eighteen concept nodes, corridors, and areas are registered in `spatial.json` (disclaimer=concept-only), all of which are conceptual expressions that do not represent approved conclusions, and provisional items may be used as public-facing context only after maintainer review [data:spatial.json] [data:geometry/key_areas.geojson#PROV-KEY-001].

**Evidence-failure cascading downgrade**: if any source cited by this proposal (a `sources.json` entry or official data) is withdrawn, invalidated, or corrected, the corresponding claims, metrics, figures, and compliance-matrix entries are synchronously downgraded to to-be-confirmed, and affected geometry and metrics are recomputed; downgrade records enter the change log and Pulse Protocol beat P4 review.

**Heritage special note (concept suggestion)**: the Qinghuayuan Railway-Station site and heritage components along the corridor receive low-intervention treatment only; all AI display installations are site-removable without attaching to heritage components or altering site structure; design around Dazhongsi treats visual harmony as the baseline, and conflict resolution with heritage authorities defaults to withdrawing the proposal.

**Terminology consistency**: the Chinese-English rendering of core concepts (AI Pulse Belt, one-belt-three-cores, Pulse Protocol, etc.) follows `docs/terminology-glossary.md`; the two files align paragraph by paragraph (bilingual_contract_version 1), and the A3/A0 drawings and HTML use the same terminology system.

This proposal does not claim official approval, approved control plans, final land ownership, final construction scale, or guaranteed implementation. The AI agent is responsible for facts, sources, copyright, spatial data, metrics, and expression; maintainers and professional reviewers may require revisions or reject the submission based on self-check results, spatial review, and the compliance matrix.

## References

- brief/public-brief.md
- brief/site-package/design_brief.json
- brief/site-package/agent_taskbook.json
- brief/site-package/allowed_design_space.json
- brief/site-package/enums/
- brief/site-package/ranges/planning_limits.json
- brief/site-package/geometry/provisional_boundaries.geojson
- data/source_registry.json
- data/processed/agent_fact_pack.md
- Peer reference: open-city-ai/haidian merged cases "Ren-Zhi Belt" (PR #1701) and "The Living Rail" (PR #925), used for mechanism-transfer boundaries and expression-depth comparison [source:PEER-REFERENCE]
- Standard boundary: nine standard responses and the data_gap note in `standard_matrix.json`
- Full machine index: see `sources.json`, `metrics.json`, `compliance_matrix.json`, `standard_matrix.json`, and `design_depth_matrix.json`
- Bibliography entry follows the site package registry; full provenance and licenses are in the structured source list [source:SITE-PACKAGE]
