# 方案迭代记录

## v0.1.0 - 2026-08-24

- Initial assembly (concept package) for fifteen-minute-living-circle.
- Proposal drafted via OpenCode CLI (opencode), session ses_fcd7ef1d4ffeNJOfRAoptZ8Qy5; edited for structure.
- Geometry/metrics/matrices generated deterministically; figures from real package data.
- Valroot gates run on 2026-08-24 (results persisted in self_check.json).

## v0.2.0 - 2026-08-25

- Round-2 repair for CocoSgt review (PR #3927, 53.0 CHANGES_REQUESTED @ 2026-08-24).
- proposal.md rewritten: official scope hierarchy (~43.6 km2 / ~11.4 km2 / ~368.4 ha), six personas (persona_count=6), 12 AI scenario cards (C01-C12), 3 industry test-and-validate scenarios (T1-T3) with hypothesis/data/model/sandbox/acceptance/exit/supplier, 8 global AI ecosystem cases (global_case_count=8), 4 annual programme brands (annual_program_count=4), cross-regional interfaces (Beiwai Community / Future Science City / Huairou Science City / E-Town / Beijing-Tianjin-Hebei), full-stack AI support (compute-model-data-toolchain-evaluation-security-developer ecosystem), AI landmark catalogues, honour display system, public space component kit, RACI matrix, decision gates, cost tiers, stop/exit conditions, data lifecycle controls, brand prior-rights paragraph, single land-use caliber with aggregation/recompute rule.
- proposal.en.md fully rewritten as substantive translation (language=en, translation_of=proposal.md; bilingual_contract_version=1 on zh).
- metrics.json aligned: persona_count=6, global_case_count=8, annual_program_count=4, scenario_card_count=12 (new), land_use_zone_count=27 (feature count fix); every count backed by visible table text.
- sources.json expanded to 26 entries incl. case-by-case global ecosystem sources, policy direction, font/logo/icon/map/tooling assets with license + reuse boundaries; license field added per entry.
- copyright_statement.md extended into a full asset rights ledger (13 asset groups + itemised sources.json mapping).
- Figures regenerated (zh+en, 12 PNGs): site-overview (map + legend panel, scale/north/stamp), land-use-structure (single-caliber donut, no label overlap), key-areas (3-node index with per-subplot scale/north/task notes), mobility-bluegreen (path hierarchy legend + notes), metrics-evidence (areas and ratios on separate axes; reduced display precision), logo-live-jz (badge emblem); ink verified: maps>=0.08, charts>=0.10; PROVISIONAL stamp bilingual on every figure; report/figure_qc.json written.
- A0 (2 pages, cover title>=60pt) and A3 (14 pages: cover + 13 sections) regenerated in zh and en (drawings/a0-boards*.pdf, drawings/a3-booklet*.pdf).
- visual/index.html rewritten to the fifteen-minute concept (14 required markers, data-metric values match metrics.json); visual/index.en.html added (pure English).
- report/proposal.html + report/proposal.en.html re-rendered; Noto Sans SC (OFL) subsets embedded via @font-face in all four HTML pages (WOFF1 base64, font-family first); check_font_coverage: 0 missing CJK.
- manifest.json updated to schema 0.2.0: all en counterparts registered (language=en + translation_of), figure_qc.json registered (role=evidence_data), data_confidence=mixed_provisional_and_conceptual.
- Known local-tooling discrepancy: local validate_submission.py ALLOWED_REPORT_FILES predates report/figure_qc.json (fleet instruction + score_rubric check 12b require it); scorer 97.8/100 PASS on this package state.
