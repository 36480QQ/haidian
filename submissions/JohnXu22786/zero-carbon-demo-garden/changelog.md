# 方案迭代记录

## v0.1.0 - 2026-08-24

- Initial assembly (concept package) for zero-carbon-demo-garden.
- Proposal drafted via OpenCode CLI (opencode), session ses_fcbc6272affedWIXABykLHWy1b; edited for structure.
- Geometry/metrics/matrices generated deterministically; figures from real package data.
- Valroot gates run on 2026-08-24 (results persisted in self_check.json).

## v3.0 - 2026-08-26

Round-3 repair (PR #3929, CocoSgt 61.0/100 CHANGES_REQUESTED). Per-file summary:

- proposal.md: rewritten to v3.0 - added four chapters (区域协同与带内接口 / 品牌识别、荣誉展示与国际传播 / 试点阶段门与运维管理), single land-use calibre (six MNR-2023 classes with formula + confidence + recompute trigger, replacing unbacked 32%/18% pie figures), eight persona groups, twelve scenario cards, three industry test protocols, AI technical protocol set (model evaluation/data quality/error stratification/runtime monitoring), developer community + conversion pathway, honour display, reversible component library, international communication, stage gates G0-G4 + RACI + data dictionary + fallback/appeal/exit, official three-level scope hierarchy statement, per-item source registration, trademark prior-rights paragraph, precision and authority-word discipline (participant provisional model data).
- proposal.en.md: full English translation with front matter (language=en, translation_of=proposal.md); substantively equivalent to the zh text (manually checked).
- assets/figures/*.png + *.en.png (18 figures): regenerated from the package's own GeoJSON (EPSG:4548) with geographic context backdrop, legend, north arrow, scale bar, node numbering, provisional stamps (zh+en), separated ratio/count axes with units; generation-time machine QC: ink >= 0.08 (maps) / 0.10 (charts), edge-clip < 0.02, figure-level text/legend overlap and annotation anchor-distance checks (all measurements recorded in self_check.json[figure_qc]).
- drawings/a0-boards.pdf(+.en): dense single-page A0 board, title 60pt, 2x2 figure grid, scope hierarchy and formula footer; drawings/a3-booklet.pdf(+.en): 8-page booklet (cover/scope/three key areas/land+metrics/implementation gates/sources).
- report/proposal.html + report/proposal.en.html: rendered from the v2 bilingual proposal, Noto Sans SC WOFF1 subsets embedded as data URIs (family NotoSansSC-Static, first in font-family); visual/index.html + visual/index.en.html: rewritten for this package (14 required sections, core metrics data-values matching metrics.json), en page pure English, fonts embedded.
- metrics.json: persona_count=8, global_case_count=6, scenario_card_count=12, land_use_zone_count=27 (geometry feature count), six land class ratio metrics with formula/confidence/recompute triggers.
- sources.json: six benchmark cases + 007xf style reference + Noto Sans SC font + figure tools + map-context + package figures registered per item (publisher/URL/access date/licence), and licence fields added to all entries (>=3 licensed entries per rubric).
- compliance_matrix.json / standard_matrix.json: evidence summaries rewritten per agent.1-6 and per standard so each entry points at distinct real content.
- manifest.json: schema 0.2.0 inventory completed for the v2 bilingual contract (9 en figures, en A0/A3, report/proposal.en.html, visual/index.en.html, proposal.en.md with language=en + translation_of), validation_claim.data_confidence=medium (honest mix of provisional-model and count metrics).
- self_check.json: four-gate report regenerated and persisted; figure_qc machine evidence injected under self_check.json[figure_qc].
- report/figure_qc.json removed (deterministic gate whitelist: report/ holds only the five named files).
