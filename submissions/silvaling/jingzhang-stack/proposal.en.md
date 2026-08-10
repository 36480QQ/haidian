---
title: "JINGZHANG STACK: One Spine · Three Stacks · Two Wings — Centennial Jing-Zhang AI Innovation Belt Urban Design Concept"
author_github: "silvaling"
language: "en"
proposal_format_version: "2"
bilingual_contract_version: "1"
translation_file: "proposal.en.md"
translation_of: "proposal.md"
license: "COMMUNITY-DISPLAY-ONLY"
summary: "English display counterpart of the Chinese formal proposal. Spatial conclusions are evidence-linked to GeoJSON layers and recomputed metrics; boundary precision remains provisional until official redlines are published."
tracks: ["ai-traffic-walkability", "enterprise-services-ecosystem", "civic-agent-governance"]
scenarios: ["ai-traffic-walkability", "enterprise-service-copilot", "public-safety-operations-review"]
---

<!-- ENGLISH DISPLAY COUNTERPART. The authoritative content is proposal.md (zh). -->

# JINGZHANG STACK: One Spine · Three Stacks · Two Wings

This is the English display counterpart of the formal Chinese proposal. All spatial conclusions are evidence-linked to `geometry/` layers and recomputed metrics; this document summarizes the structure and key deliverables rather than duplicating every machine-readable reference.

## Submission Status

- **package_state**: ready_for_review
- **Boundary precision**: provisional — official redlines are pending; the whole package must be recomputed once official polygons are published.
- **Scoring note**: structural data gaps do not block content scoring; precision warnings are preserved.

## Three-Level Scope Framework

| Level | Design Question | Proposal Answer | Data Anchors |
| --- | --- | --- | --- |
| Coordinated research scope (43.6 km²) | How to organize the AI industry ecology and future urban form | Innovation chain: university strategy → open-source collaboration → enterprise incubation → public experience → international outreach | compliance_matrix.json, standard_matrix.json |
| Overall design scope (11.4 km²) | How to implement land use, urban renewal, mobility and image | Land use / buildings / roads / green space / public space / phasing layers | land_use.geojson, roads.geojson |
| Key detailed design areas (368.4 ha) | How to reach detailed design depth in three areas | L0 Zhongzhiyuan (computing & root tech), L1 AI Origin community (models & open source), L2 Dazhongsi (scenarios & applications) | key_areas.geojson |

## Overall Concept

**JINGZHANG STACK — One Spine · Three Stacks · Two Wings.**

- **One Spine**: the Jing-Zhang heritage railway park green corridor (conceptual, ~19.8 km perimeter) connecting the three stacks.
- **Three Stacks**: L0 众智园 (192.9 ha), L1 AI 原点社区 (104.3 ha), L2 大钟寺 (72.0 ha).
- **Two Wings**: 中关村科技服务翼 (west, capital/IP/talent services) and 小月河场景赋能翼 (east, AI+life scenarios).
- **Seam connectors**: three east-west public seam interfaces that stitch the railway corridor with surrounding districts.

## Key Metrics (all recomputed from submitted geometry)

| Metric | Value | Basis |
| --- | --- | --- |
| Site area | 11,412,825 m² | polygon_area(site_boundary, provisional) |
| Green ratio | 26.2% | green_space_area / site_area |
| Public space ratio | 8.2% | public_space_area / site_area |
| Industrial land ratio | 48.2% | (research + commercial + test) / site_area |
| Heritage spine length | 19.8 km | perimeter of green spine corridor |
| Road centerline | 25.9 km | sum(linestring_length(roads)) |
| Conceptual buildings | 20 | building footprints in three key areas |

## AI Scenario Cards (12) & Personas (6)

12 scenario cards cover open-source publishing, governance sandbox, edge-compute stations, AI slow-mobility navigation, international roadshow living room, low-carbon innovation corridor, university commercialization street, data-elements lounge, AI life-service street, global AI week route, intelligent operations & public-safety coordination, and accessible care network. Six personas: open-source developers, startups, enterprise visitors, residents, university staff/students, and international talents.

## AI Pilgrimage Landmarks (4)

Origin Open-Source Honor Wall (PUBLIC-005), Zhongzhiyuan Computing-Light Installation (PUBLIC-004), Dazhongsi Scenario-Experience Window (PUBLIC-006), and the Centennial Jing-Zhang Cultural Stitch Belt (GREEN-001). All are design suggestions requiring rights clearance before implementation.

## Standards & Compliance

Requirements are mapped in `compliance_matrix.json` (announcement tasks), `standard_matrix.json` (professional standards), and `design_depth_matrix.json` (design depth items). AI governance follows data minimization, open sources, explainability, and human review; AI nodes never replace statutory approval and never claim official implementation commitments.

## References

See `sources.json` for the full registry; key sources include the official announcement, the agent task book, MNR land-use classification, MOHURD urban design measures, and the processed fact pack (`data/processed/agent_fact_pack.md`).
