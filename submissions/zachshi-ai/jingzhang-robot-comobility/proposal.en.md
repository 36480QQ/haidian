---
title: "Jingzhang AI Low-Speed Robot Co-Mobility Network: A New Human-Robot Shared Spine for the Smart City"
author_github: "zachshi-ai"
language: "en"
proposal_format_version: "2"
bilingual_contract_version: "1"
translation_of: "proposal.md"
license: "COMMUNITY-DISPLAY-ONLY"
summary: "Anchored on the Jingzhang Railway Heritage Park slow-traffic spine, this proposal introduces the concept 'Jingzhang Smart Mobility Network · AI Low-Speed Robot Co-Mobility Belt': a dedicated low-speed robot lane network (15.4 km dedicated + 3.4 km shared), six smart delivery stations and two charging-maintenance depots serving communities, campuses and parks with delivery, tour-guide, patrol and cleaning robots. Human-robot co-mobility is the design core: three cross-sections (dedicated/shared/pedestrian-priority) and four speed tiers (5/8/10/15 km/h), supported by 12 AI scenario cards (incl. 4 test/validation scenarios), 8 personas, 3 AI pilgrimage landmarks, 7 global ecosystem cases, a brand visual identity and an operational KPI system — a tangible, verifiable and replicable low-speed robot co-mobility concept."
tracks: ["robotics-autonomous-mobility", "ai-origin-community"]
scenarios: ["robot-delivery-low-speed", "ai-traffic-walkability"]
---

# Jingzhang AI Low-Speed Robot Co-Mobility Network: A New Human-Robot Shared Spine for the Smart City

## Design Basis and Source List

This formal proposal takes the pre-qualification announcement of the Centennial Jingzhang AI Innovation Belt international urban design call, published by the Haidian Branch of the Beijing Municipal Commission of Planning and Natural Resources, as its first authority [source:official-announcement]; the agent-oriented taskbook excerpt as the supplementary authority [source:agent-taskbook]; and the maintainer-registered provisional boundaries, key areas, enums, metrics and source lists under `brief/site-package/` as machine-readable basis [source:site-package-registry]. The proposal focuses on two tracks — `robotics-autonomous-mobility` (delivery, tour-guide, patrol, cleaning and low-speed autonomous shuttle pilots) and `ai-origin-community` (AI Origin Community and innovation services) — mapped to the `robot-delivery-low-speed` and `ai-traffic-walkability` scenarios, re-imagining the heritage park corridor as a human-robot co-mobility spine for low-speed robot services.

Every design judgement decomposes into traceable sources, recomputable metrics, checkable layers and human-reviewable assumptions. All robot co-mobility facilities (lanes, stations, depots) are recorded in nine GeoJSON layers, and core metrics are recomputed in EPSG:4548 consistent with the union rule of `scripts/spatial_review.py` [depth:existing_conditions_diagnosis] [depth:metrics_recalculation].

**Provisional boundary and conceptual nature.** This package uses a provisional rough boundary with `geometry_role="provisional_constraint"` and `official_boundary=false` [data:geometry/site_boundary.geojson#SITE-001]; this organizer-side data gap does not block content scoring, and everything must be recalculated once official polygons are published. All lanes, speed limits, station siting, phasing and operating mechanisms are expressed as conceptual proposals / reference schemes for professional deepening; they constitute no government review conclusion or implementation commitment.

### Baseline Diagnosis and Problem Profile

The robot co-mobility network is not technological imagination but a spatial response to three verifiable problems [depth:existing_conditions_diagnosis]:

1. **High last-mile delivery cost.** Public industry data indicate last-mile cost commonly takes 30%-50% of total logistics cost, and the human-courier model faces sustained pressure from aging workforce and rising labor costs [source:jd-smart-delivery-vehicle]. The Jingzhang corridor's campuses, parks and communities offer high order density and regular routes — natural conditions for scaling low-speed robots.
2. **Frequent terminal traffic conflicts.** Courier wrong-way riding and pedestrian disputes are a national urban governance pain point and the core target of this proposal's co-mobility design. The network separates robots from pedestrian flows with dedicated lanes and front-loads safety through speed tiers and a conflict test field [assumption:A-ROBOT-001].
3. **Parcel pickup hardship for elderly and mobility-impaired residents.** Heavy parcels and medicine deliveries make the "last 100 meters" hardest for vulnerable groups; barrier-free pickup assistance and voice pickup are the starting point of this proposal's public-interest design [source:barrier-free-environment-law].

**Honest data-gap disclosure.** Official delivery OD volumes, pedestrian-flow baselines, building and ownership inventories are unpublished; corresponding indicators stay `status=unknown` or are marked directional. The gap checklist lives in `assumptions.json` and the risk section [assumption:A-ROBOT-002] [assumption:A-ROBOT-006].

![Evidence chain and overall scope map](assets/figures/site-overview.png)

## Three-Level Scope Framework

The proposal maps the robot co-mobility network onto the announcement's three levels: the **coordinated research scope** (43.6 km² provisional) answers "robot industrial ecosystem and regional coordination"; the **overall design scope** (~11.4 km² provisional boundary) answers "co-mobility spatial structure and facility layout"; the **key-area scope** (368.4 ha provisional aggregate) answers "detailed robot scenario design in three areas". The three levels map one-to-one onto announcement items 1.3/1.4/1.5 and agent tasks agent.1-agent.6 in `compliance_matrix.json` [standard:PROJECT-OFFICIAL-ANNOUNCEMENT] [source:agent-taskbook].

| Level | Design question | Proposal answer | Data anchor |
| --- | --- | --- | --- |
| Coordinated research | How to organize robot ecosystem and Jing-Jin-Ji coordination | Haidian R&D source - Yizhuang policy demo - Shunyi operations base "triangle", seven-element ecosystem map | compliance_matrix.json, standard_matrix.json |
| Overall design | How the co-mobility network lands on maps | "One corridor, four branches, six stations, two depots"; 11 co-mobility roads and 23 robot-related buildings all mapped | [data:geometry/roads.geojson#RD-001], [data:geometry/buildings.geojson#BLD-016] |
| Key areas | How three areas reach detailed-design depth | Zhongzhiyuan = R&D test ground; Origin Community = pilot operation zone; Dazhongsi = terminal consumption experience | [data:geometry/key_areas.geojson#zhongzhiyuan_ai_acceleration_area], [metric:key_area_count] |

The three levels are not disconnected drawing sets: coordinated research decides industrial and policy judgement, overall design lands the judgement in lanes, stations and phasing layers, and key-area design verifies human-robot safety and operational feasibility on concrete parcels. No area, ratio, scale or count that cannot be recomputed from structured data enters formal conclusions [depth:three_level_scope_framework] [depth:overall_spatial_structure].

![Three-level scope and land-use partition map](assets/figures/land-use-structure.png)

## Coordinated Research Area: Industry and Future City Research

The coordinated research task is building a world-class AI innovation ecosystem, and the robot co-mobility network is its perceptible, experiential layer. Beijing already has the nation's most complete low-speed autonomous driving policy and industry base: the Beijing High-level Automated Driving Demonstration Zone has expanded continuously since its 2020 establishment, providing road-right and policy testbeds for low-speed delivery [source:beijing-advanced-ad-zone]; Meituan autonomous delivery vehicles pilot fresh-food and medicine delivery on public roads in Beijing [source:meituan-auto-delivery-car]; Neolix low-speed vehicles operate long-term in Yizhuang [source:neolix-low-speed-av]; JD Logistics smart delivery vehicles run routine last-mile delivery [source:jd-smart-delivery-vehicle]. Internationally, Starship Technologies has delivered over one million orders across campus and suburban communities [source:starship-technologies], and Serve Robotics runs sidewalk-level delivery in Los Angeles [source:serve-robotics-la]. The seven lines of evidence converge on one point: low-speed delivery robots have moved from lab to street; what is missing is not technology but **urban space design for co-existence with people** — exactly this proposal's attack point [standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK].

**Seven-element ecosystem map.** The network lands the seven elements — land, industry, capital, talent, compute, data, scenarios — on one spatial map: land = 18 parcels (incl. robot test buffer green and strategic reserve); industry = vehicle R&D - algorithm/compute - terminal application chain; capital = conceptual multi-source mix led by public-space operation and business partnership; talent = robot engineer apartments and developer community; compute = cloud dispatch and compute center (BLD-003); data = compliant governance of dispatch and order data; scenarios = 12 scenario cards.

**Regional coordination.** The proposal forms innovation coordination loops with Beiwei Community, the Future Science City, Huairou Science City, the Beijing Economic-Technological Development Area (Yizhuang) and the broader Jing-Jin-Ji region: Yizhuang carries policy pilots and scaled operation, Shunyi carries logistics bases, Haidian carries R&D sourcing and scenario opening; perception and chip technologies from the Future Science City and Huairou Science City can be reverse-validated through co-mobility scenarios. All coordination relations are conceptual proposals [source:agent-taskbook].

**Future urban form.** The proposal offers a "human-robot co-mobility block" paradigm: robots are not street outliers but share a predictable spatial rule set with pedestrians and cyclists — dedicated lanes, stations, chargers and signal priority form a "robot-reachable street furniture system", a replicable cross-section prototype for global AI cities.

## Overall Design Area: Urban Renewal and Regulatory-Plan-Level Urban Design

**Overall concept: Jingzhang Smart Mobility Network.** Naming system: main name 「京张AI低速机器人共行带」, short name 「京张智行网」, English "Jingzhang AI Low-Speed Robot Co-Mobility Belt (JZ CoMobility)"; sub-naming: Co-Mobility Main Corridor, Smart Delivery Station, Co-Mobility Zero Plaza. The naming echoes the Jingzhang Railway's self-reliant construction spirit and the AI Origin Community's pilgrimage positioning — extensible and internationally communicable [source:agent-taskbook].

**Logo visual identity (brand recognizability).** Core form: a rail arc splitting into two lines from a "人" (human) chevron — abstracting the Jingzhang herringbone railway — with a circular wheel dot on the right, composing "rail × wheel × chevron"; primary colors: Jingzhang Green `#1F7A5C` (heritage park green), Smart Silver-Grey `#8E9BA8` (robot metal), Origin Orange `#E86A33` (energy and warning accent); application rules: minimum size 12 mm / 32 px, clear space ≥1/4 of core-form height, reversed white on dark backgrounds, no gradients or strokes; extension system: four functional icon families (station/charging/transfer/patrol), lane-dash rhythm auxiliary graphics, bilingual wordmark lockups. All fonts and graphics are original geometric compositions without infringement risk.

**Overall spatial structure: "one corridor, four branches, six stations, two depots, three areas".** The main corridor follows the heritage park slow-traffic spine [data:geometry/roads.geojson#RD-001]: 15.4 km dedicated plus 3.4 km shared, about 18.8 km of drivable lanes in total [metric:robot_lane_length_m]; four branches cover the north loop, the central connector, the south industrial connector and two robot trunk lines (RD-009/RD-010); six delivery stations spread along the corridor at roughly 1.2 km service radius [metric:robot_delivery_station_count], and two charging-maintenance depots guard north and south [metric:robot_charging_depot_count]. Eighteen land-use parcels cover the provisional boundary completely without overlap [data:geometry/land_use.geojson#LU-001].

The renewal framework follows "**zero large-scale demolition, light infrastructure first**": the network starts with lane markings, modular stations and temporary charging — movable, reversible, exit-able; all building scale and intensity metrics stay `status=unknown` pending official control conditions [depth:development_intensity_controls] [depth:land_use_layout].

## Detailed Design of Key Areas

| Key area | Design positioning | Robot spatial moves | AI industry & operation scenarios | Evidence |
| --- | --- | --- | --- | --- |
| Zhongzhiyuan AI Acceleration Area | Full-stack robot R&D test ground | Vehicle R&D centers A/B, cloud dispatch-compute center, test buffer green, release-test plaza, charging depot, 8 km/h closed test trail | Perception algorithm testing, vehicle release, standard-setting, safety evaluation | [data:geometry/key_areas.geojson#zhongzhiyuan_ai_acceleration_area], [depth:three_key_area_detailed_design] |
| Beijing AI Origin Community | Pilot operation zone (near-term demo) | Robot Time-Space Museum (landmark 1), Co-Mobility Zero Plaza (landmark 3), delivery stations, talent-apartment delivery coverage | Community delivery pilot, co-mobility experience, open-source developer community | [data:geometry/key_areas.geojson#beijing_ai_origin_community], [metric:robot_delivery_station_count] |
| Dazhongsi AI Industry Cluster | Terminal consumption experience zone | Flagship delivery ark station (landmark 2), delivery experience plaza, terminal incubator, Dazhongsi station feeder line | Smart terminal showcase, unmanned retail, parcel-metro handoff | [data:geometry/key_areas.geojson#dazhongsi_ai_industry_cluster], [data:geometry/roads.geojson#RD-011] |

All three areas reach conceptual-deepening depth with positioning, spatial moves, AI scenarios, implementation dependencies and area recalculation each; depth is audited by the design-depth matrix [depth:three_key_area_detailed_design]. Describing a "demonstration zone" without functional, building, transport and implementation evidence counts as unfinished — this proposal supplies the corresponding layer evidence in `geometry/`.

![Key-area index and design tasks](assets/figures/key-areas.png)

## AI Innovation Ecosystem, Personas, and AI+ Scenarios

**Ecosystem case evidence (7 items: 6 global cases + 1 local ecosystem mothership, all with primary sources).** See the coordinated-research case list: Beijing High-level AD Zone [source:beijing-advanced-ad-zone], Meituan auto-delivery [source:meituan-auto-delivery-car], Neolix low-speed vehicles [source:neolix-low-speed-av], JD smart delivery vehicles [source:jd-smart-delivery-vehicle], Starship Technologies [source:starship-technologies], Serve Robotics [source:serve-robotics-la], and Haidian's Zhongguancun Science City itself as the seventh "ecosystem mothership" evidence item (evidenced by the announcement and taskbook [source:official-announcement]). The seven-element map (land/industry/capital/talent/compute/data/scenarios) is itemized under the agent.2 entry of `compliance_matrix.json`.

**Personas (8, incl. 4 vulnerable groups).** Every persona carries a no-AI alternative path and complaint channel, safeguarding public interest [source:barrier-free-environment-law]:

| Persona | Typical needs | Spatial response | No-AI alternative |
| --- | --- | --- | --- |
| Young AI engineer | Time-saving pickup, late-night meals | Apartment/park stations, night feeder | Human delivery window kept |
| Park enterprise admin | Internal mail, office supplies | Internal-mail robot line | Human mailroom kept |
| University student | Campus parcels, textbooks | Campus stations, dorm handoff | Human parcel points kept |
| Elderly resident | Medicine, heavy items, voice pickup | Voice pickup lane, human receiving | Volunteer receiving point |
| Mobility-impaired person | Barrier-free pickup, errand delivery | Barrier-free delivery channel, ramps | Door-to-door service booking |
| Child and parent | Safe passage, school shuttle | Pedestrian-priority segments, 5 km/h | Parent escort posts kept |
| Low-digital-skill resident | Pickup without apps | Phone/voice ordering, staffed window | Full manual service window |
| Courier (transitioning) | Career transition, upskilling | Remote safety-operator & O&M training | Traditional delivery jobs kept |

**12 AI scenario cards (incl. 4 ★ test/validation scenarios).** Cards cover delivery, tour-guide, patrol and cleaning robots, each with nine columns: card id / scenario / users / spatial carrier / data needed / data-legality boundary / model role / public value / operation responsibility & exit [source:agent-taskbook]:

| Card | Scenario | Users | Carrier | Data needed | Legality boundary | Model role | Public value | Responsibility & exit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RB-01 | Community smart delivery | Residents | 6 stations + local roads | Order address, locker slots | Minimized collection, aggregated stats | Routing + locker scheduling | Lower last-mile cost & traffic | Station operator; two failing quarters trigger adjustment |
| RB-02 | Medicine express | Elderly & chronic patients | Pharmacy-station-community | Rx delivery demand | No health-data collection, fulfillment only | Priority dispatch + temperature control | Medication accessibility | Pharmacy joint ops; temperature fault halts |
| RB-03 | Campus delivery | Students | Campus stations + roads | Campus network, schedules | Authorized campus data only | Avoidance + crowd prediction | Fewer campus e-bike hazards | School review; safety incident halts |
| RB-04 | Park tour guide | Visitors & residents | Five greenway segments | POI coords, crowd flow | No personal trajectories | Multilingual guidance + obstacle avoidance | Better park access experience | Park operator; complaint threshold triggers adjustment |
| RB-05 | Night safety patrol | Parks & communities | Patrol buffer + park roads | Video, device status | Zone-scoped, anonymized, audited | Anomaly detection + alerting | Night security supplement | Security joint duty; false-alarm recalibration |
| RB-06 | Barrier-free pickup assist | Mobility-impaired & elderly | Barrier-free channel + stations | Booking requirement list | Fulfillment-only data | Demand matching + dispatch | Removing the last-100-m barrier | Community joint ops; satisfaction-driven optimization |
| RB-07 | Park internal mail | Park enterprises | Internal mail line | Internal send/receive info | Enterprise intranet isolation | Batch path optimization | Less admin time | Park property; cost overrun shrinks line |
| RB-08 | Parcel-metro handoff | Commuters | Dazhongsi feeder line | Station flows, lockers | Aggregated flow data | Off-peak handoff scheduling | Eases station-side parking | Rail+logistics joint; peak conflict re-times |
| ★RB-09 | Co-mobility conflict test field | Test fleet & public | Public robot test field | Simulated + real conflict samples | Public test protocol + consent | Conflict prediction & avoidance validation | Front-loading safety | Joint lab; unresolved conflict rate stops testing |
| ★RB-10 | Night & rain-snow validation | Operators & regulators | Demo road segments | Weather + sensor data | Anonymized test data | Adverse-condition reliability | Defining safe operation windows | Third-party evaluation; threshold miss limits ops |
| ★RB-11 | Barrier-free delivery end-to-end validation | Mobility-impaired & elderly | Full barrier-free channel | End-to-end measured records | Consent + privacy masking | End-to-end usability metrics | Verifying inclusion promise | Accessibility org acceptance; failure triggers retrofit |
| ★RB-12 | Remote takeover emergency drill | Safety operators | Dispatch center + network | Drill scripts, takeover logs | Isolated archived drill data | Takeover latency evaluation | Safety backstop capability | Periodic drills; latency miss pauses expansion |

**Privacy and human-review boundary.** All scenarios follow data minimization, public sources, explainability and human review: robots only navigate, deliver and alert — never diagnose, approve or enforce; dispatch algorithms follow generative-AI service requirements [source:generative-ai-interim-measures]; no supplier is designated as a necessary condition [assumption:A-ROBOT-003].

## Land Use, Building Scale, and Retain-Renovate-Demolish Strategy

The land-use plan follows the national land-use classification guide, expressed as 18 complete, closed, non-overlapping parcels [standard:MNR-LAND-USE-CLASSIFICATION-GUIDE]; robot semantics ride on the extra property `robot_zone` without touching code enums: five co-mobility greenway segments (1401), full-stack robot R&D-test zone (0802), terminal industry and smart-delivery retail (05), residential demo (07), test buffer green (1402) and strategic reserve (16) [data:geometry/land_use.geojson#LU-003]. The 18 parcels fully cover the provisional boundary with no overlap or gap, satisfying the spatial-review coverage requirement [metric:land_use_parcel_count].

Buildings split into three classes: **existing retained/renovated** (15 of the 23 buildings, all reusing original footprints, no new towers), **new light stations** (6 delivery stations, conceptual height 4.5 m, modular and relocatable), **new charging-maintenance depots** (2, conceptual height 6.0 m) [data:geometry/buildings.geojson#BLD-016]. The retain-renovate-demolish principle is "zero large-scale demolition": the proposal advocates no demolition of existing buildings; all renovations and new builds are conceptual proposals pending official ownership and control conditions [depth:retain_renovate_demolish].

Building scale and intensity metrics (total floor area, FAR, height, density, setbacks, road redlines) have no official conditions and stay uniformly `status=unknown` with backfill paths in `assumptions.json`; conceptual heights are form illustrations only [depth:development_intensity_controls] [depth:height_massing_character] [assumption:A-ROBOT-006].

## Transport, Rail, Municipal Infrastructure, and Public Services

**Co-mobility lane system (core transport innovation).** Three cross-sections: dedicated (2.5 m robot lane, physical separation, 15 km/h), shared (same surface as slow traffic, visual separation, 10 km/h), pedestrian-priority (inside heritage protection and around plazas, robots follow pedestrian flow, 5 km/h); test trail at 8 km/h. The four speed tiers and lane widths are conceptual proposals to be confirmed by the traffic authority [assumption:A-ROBOT-001]. The main corridor **overlays rather than replaces** the Jingzhang slow-traffic spine: the park slow system stays complete and continuous, with robot facilities joining as an overlay layer [data:geometry/roads.geojson#RD-001].

**Intersections and key segments.** The N. 5th Ring overpass and metro-interface segments form key design segment CON-002, requiring professional traffic/municipal review [data:geometry/constraints.geojson#CON-002]; the Dazhongsi feeder (RD-011) uses off-peak scheduling to ease station-side conflicts; all road layers stay inside the provisional submission boundary. Transport depth is managed by [depth:traffic_rail_slow_parking], municipal/new-infrastructure depth by [depth:municipal_new_infrastructure].

**Municipal preconditions.** Station power supply, charging loads, telecom coverage and fire access are formal deepening preconditions; the two depots and six stations follow "modular + relocatable" design to avoid one-off municipal overhauls [data:geometry/buildings.geojson#BLD-022]. Where pipeline, energy or fire engineering data are missing, they are listed as preconditions rather than design conclusions.

![Mobility and blue-green composite system](assets/figures/mobility-bluegreen.png)

## Blue-Green Network, Public Space, and Urban Character

The blue-green system uses the heritage park vitality belt as skeleton: five co-mobility greenway segments match the green layer [data:geometry/green_space.geojson#GS-001], with green ratio 0.256389 and public-space ratio 0.209042 (EPSG:4548 union recalculation) [metric:green_ratio] [metric:public_space_ratio]. The greenway hosts public activities where robots are "watchable, experiential and rideable": the Co-Mobility Zero Plaza (PS-001) carries a human-robot experience field and the Jingzhang Co-Mobility Contribution Wall (honor display system); the co-mobility memory corridor (PS-004) links railway memory with the museum route [data:geometry/public_space.geojson#PS-001] [depth:blue_green_public_space].

**Public-space component library.** Station modules, chargers, transfer berths and info totems share one design language (silver-grey + Jingzhang green), composable and movable for professional deepening reuse.

**Urban character.** Character controls split into three classes: official controls (heritage, green, blue-line statutory conditions, pending official data), design suggestions (robot facility colors/materials: silver-grey body + green identity band + orange safety accents), and pending confirmations (building massing, interfaces). No pseudo-precise control lines without heritage or regulatory-plan basis [standard:MOHURD-URBAN-DESIGN-MEASURES]. Inside heritage protection, co-mobility uses pedestrian-priority mode capped at 5 km/h [data:geometry/constraints.geojson#CON-001].

## Renewal Projects, Implementation Policy, and Phasing

**12 reviewable conceptual project packages (JZ-01..JZ-12).** Each lists location, type, preconditions, actor types, funding category and exit conditions — all conceptual proposals, not implementation commitments [depth:renewal_project_list] [depth:phasing_implementation]:

| ID | Project | Location | Type | Preconditions | Actors | Funding | Exit condition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| JZ-01 | Origin Community delivery demo | Origin Community | Pilot ops | Pilot demand survey, community consent | Operator + community | Commercial + public subsidy | Two failing quarters shrink demo |
| JZ-02 | Main corridor dedicated-lane marking | Park spine | Transport | Traffic professional review | Traffic dept + professional team | Public investment | Failed review falls back to shared mode |
| JZ-03 | Six smart delivery stations | Along corridor | Modular building | Site ownership confirmation | Operator | Commercial investment | Underuse triggers relocation |
| JZ-04 | Two charging-maintenance depots | North/south | New infrastructure | Power & fire conditions | Energy + operator | Mixed | Insufficient load shrinks fleet |
| JZ-05 | Cloud dispatch digital-twin platform | Dispatch center | Digital platform | Algorithm filing & safety evaluation | Tech firm + regulator | Commercial + public | Safety threshold breach stops network |
| JZ-06 | Co-mobility conflict test field | Public test field | Test facility | Public test protocol | Joint laboratory | Public + commercial | Unresolved conflicts stop testing |
| JZ-07 | Robot Time-Space Museum | Origin Community | Cultural building | Exhibit rights clearance | Cultural operator | Mixed | Low visits trigger re-exhibition |
| JZ-08 | Flagship delivery ark station | Dazhongsi | Experience building | Business partnership | Commercial operator | Commercial investment | Underperformance triggers pivot |
| JZ-09 | Co-Mobility Zero Plaza | Origin Community | Public space | Public-space permit | Public operator | Public investment | Activity safety risk triggers adjustment |
| JZ-10 | Dazhongsi station feeder | Dazhongsi station | Transport feeder | Rail & traffic coordination | Rail + logistics joint | Mixed | Peak conflict re-times windows |
| JZ-11 | N. 5th Ring overpass segment | 5th Ring node | Key design segment | Traffic/municipal special review | Professional team + dept | Public investment | Failed review reroutes alternative |
| JZ-12 | Barrier-free delivery & voice pickup | All stations | Inclusive service | Accessibility org acceptance | Operator + community | Public subsidy | Failed acceptance triggers retrofit |

**Phasing (distinct from the 100-day call period).** Near-term demo (PH-001, Origin Community delivery pilot, 6-12 months), mid-term networking (PH-002, Dazhongsi + park core connected, 1-3 years), long-term through-connection (PH-003, Zhongzhiyuan full-stack testing joins the line, 3-5 years) [data:geometry/phasing.geojson#PH-001]. Preconditions, actors, funding and exits per phase are as above; timelines are conceptual [metric:phasing_zone_count].

**Long-term operation (agent.6).** Four-season events: spring new-product release (Zhongzhiyuan release plaza), summer night co-mobility festival (park greenway), autumn developer festival (Origin Community), winter warm delivery (extra elderly medicine runs); developer community: annual open-sourcing of co-mobility rule libraries and simulation datasets; scenario open days: monthly public test-rides and safety literacy; three public experience routes: Zero Plaza → Museum cultural line, test field → release plaza innovation line, station → ark flagship consumption line; international communication: bilingual copy and the narrative of "the world's first low-speed robot co-mobility network in a railway-heritage park". All are conceptual proposals [source:agent-taskbook].

## Metrics, Area Recalculation, and Compliance Matrix

Metric recalculation follows the unified design-depth requirement [depth:metrics_recalculation]. Core metrics match `metrics.json` (EPSG:4548, unary_union deduplication):

| Metric | Value | Unit | Status |
| --- | --- | --- | --- |
| Overall design area | 11,412,825.386 | m² | known (provisional) |
| Key area count | 3 | areas | known |
| Green ratio | 0.256389 | ratio | known |
| Public space ratio | 0.209042 | ratio | known |
| Building footprint (union) | 558,040.811 | m² | known |
| Robot drivable lanes | 18,780.730 | m | known |
| of which dedicated | 15,351.069 | m | known |
| Delivery stations | 6 | stations | known |
| Charging depots | 2 | depots | known |
| Scenario cards / test-validation | 12 / 4 | cards | known |
| Personas / vulnerable groups | 8 / 4 | types | known |
| FAR, height, density | — | — | unknown (pending official) |

Metrics are managed in three classes: class one — spatial metrics directly recomputable from submitted geometry (boundary area, green ratio, public-space ratio, footprints, lane length); class two — control metrics needing official regulatory-plan support (FAR, height, density, all unknown); class three — performance metrics needing operational calibration (volumes, conflict rate, satisfaction — see operational KPIs below). The three classes enter `metrics.json`, `assumptions.json` and `compliance_matrix.json` respectively, so operational visions are never mistaken for approved planning conditions [metric:site_area_sqm] [metric:building_footprint_area_sqm].

**Operational KPI system (implementation-feasibility evidence).** Targets, monitoring cadence and exit/adjustment thresholds tabulated:

| KPI | Target | Cadence | Exit/adjustment threshold |
| --- | --- | --- | --- |
| Demo daily delivery volume | ≥2,000 orders/day | Monthly | Two quarters <50% shrinks demo |
| Average delivery time | ≤30 min | Real-time + monthly | One month over shrinks routes |
| Human-robot conflict rate | ≤0.1 per 1,000 km | Monthly | 3× triggers network-wide speed cut |
| Human-intervention rate | ≤0.5 per 10,000 orders | Real-time + monthly | 3× pauses expansion |
| Station coverage rate | ≥80% | Quarterly | Miss adds/relocates stations |
| Public satisfaction | ≥75% | Quarterly survey | Two quarters fail rewrites rules |
| Unit delivery cost | ≤90% of human courier | Monthly | Above human cost switches to mixed mode |
| Vulnerable-group usage share | ≥10% | Quarterly | Miss strengthens barrier-free retrofit |

**Compliance matrix.** All 23 mandatory tasks of announcement 1.3/1.4/1.5 and agent.1-agent.6 map to sections, layers, metrics, drawings, HTML and assumptions [standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK]; all 15 design-depth items are `complete`, with 4 noting "pending official conditions" completeness limits — no false completeness claims.

![Core metric recalculation and evidence chain](assets/figures/metrics-evidence.png)

## Risk, Copyright, and Compliance

**Six risk dimensions (risk.json).** Data privacy (score 3: minimized collection, fulfillment-only use, no commercial profiling), public acceptance & safety perception (score 4: tiered speed limits, education, public incident ledger), technology maturity (score 3: weather windows, redundant takeover, human backup), policy & regulatory uncertainty (score 4: referencing the Beijing High-level AD Zone practice; submitted as concept only), operations cost (score 3: modular cost reduction, quarterly reviews), spatial ownership disputes (score 3: relocatable facilities, joint confirmation). Every score≥3 dimension carries a `human_review` arrangement [depth:risk_missing_data] [assumption:A-ROBOT-005].

**Compliance boundary.** This proposal constitutes no government review conclusion or implementation commitment and implies no official endorsement of any lane, station, speed limit or operation arrangement; all spatial content is conceptual for professional deepening [source:official-announcement]. Robot dispatch and AI interactions follow generative-AI service requirements (algorithm filing, content labelling, human review, complaint channels) [source:generative-ai-interim-measures]; co-mobility lanes do not occupy barrier-free passage, consistent with the Barrier-Free Environment Law [source:barrier-free-environment-law]. The proposal contains no personal privacy, classified or non-public spatial data, and no fabricated official endorsement.

**Copyright ledger.** All text, geometry, figures, PDFs and HTML are original works of this agent or citations from public materials; free commercial Chinese fonts are used; case citations carry source and background-only attributes; the itemized asset-rights ledger lives in `report/copyright_statement.md`. The HTML page loads no remote scripts, tiles, fonts or APIs and does not track reviewers.

## References

1. brief/public-brief.md (public brief overview)
2. brief/site-package/design_brief.json (submission policy and boundary rules)
3. brief/site-package/agent_taskbook.json (agent.1-agent.6 tasks)
4. brief/site-package/geometry/provisional_boundaries.geojson (provisional boundaries)
5. brief/site-package/enums/ (enums)
6. data/source_registry.json (source-use registry)
7. data/processed/agent_fact_pack.md (fact navigation pack)
8. Full machine indexes: sources.json, metrics.json, compliance_matrix.json, standard_matrix.json, design_depth_matrix.json and risk.json [source:site-package-registry]
