# 方案迭代记录

## v0.1.0 - 2026-08-24

- Initial assembly (concept package) for qinghe-bluegreen-commons.
- Proposal drafted via OpenCode CLI (opencode), session oc-repair-3856; edited for structure.
- Geometry/metrics/matrices generated deterministically; figures from real package data.
- Valroot gates run on 2026-08-24 (results persisted in self_check.json).

## v2.3 - 2026-08-25 (REPAIR ROUND-3, PR #3856)

- **proposal.md**: official three-tier scope hierarchy added (统筹 ≈43.6 km² / 总体 ≈11.4 km² / 重点区域 ≈368.4 ha) and the provisional site boundary repositioned as a temporary interpretation of the overall design area; deprecated the old 2.3 km² concept. Section 2.3 rewritten as item-by-item differentiated task evidence for the three mandated key areas (1.5.3.1–1.5.3.3) with explicit boundary statement; two-wing interface table added. Section 6: case table expanded with per-case source/access date/reuse boundary (7 rows); scenario-card table header now "场景卡编号与名称"; S02 minor-data flow clarified (guardian consent + revocable, environmental/collective sounds only); AI governance review table added. Section 7.2: facility-quantity derivation chain table (40–70 units / 150–400 m² / 10k–20k m², demand-capacity-phasing). Section 8.5: accessibility concept checklist. Section 10: RACI matrix + annual-program table (5 rows). Section 11: indicator table with source/formula/confidence/use-limit/recompute columns; fact-base table renamed to 出处基线 and aligned to official scopes; ratio display precision to one decimal. New VI chapter (logo construction, proportion, color, bilingual lock-up, forbidden uses) + logo figure. Chapter 12: brand prior-rights paragraph (internal working codenames). Source IDs hyphenated (e.g., DATA-SRC-OFFICIAL-ANNOUNCEMENT-2026-05-09).
- **proposal.en.md**: full English translation rewritten (front matter language=en, translation_of=proposal.md; all 13 EN sections; substantively equivalent statements/numerals; en figure references), manually cross-checked against zh.
- **sources.json**: 7 CASE-* case-study entries + 3 HIST-* historical-statement entries with publisher/page URL, published+accessed dates and reuse boundaries; license fields added; asset entry ASSET-LOGO-QSS-AIC added; renamed 3 IDs to hyphenated form.
- **Matrices**: compliance_matrix (23 entries), design_depth_matrix (15 items), standard_matrix (5 items) regenerated with distinct, content-specific evidence summaries; 1.5.3.1–1.5.3.3 correctly mapped to Section 2.3/6 task evidence; three_key_area_detailed_design limited-by official polygons.
- **Figures (12)**: all 6 canonical figures redrawn at (12,8)/150dpi with legend/north/schematic scale + bilingual PROVISIONAL stamp; key-areas now shows the three segment cores, their landmarks AND the three mandated key areas with synergy arrows and a correspondence mini-table; metrics-evidence splits area/ratio/count onto separate axes; land-use figure explains pie vs ratio denominators in-figure; new logo-qss-aic VI sheet (zh+en); ink ≥0.08 maps / ≥0.10 charts verified programmatically.
- **Drawings**: a0-boards (2 pages) and a3-booklet (6 pages) regenerated zh+en (raster pipeline, A0 title 60pt, A3 first-page title inside margins, PROVISIONAL stamps on every page).
- **HTML**: report/proposal.html + report/proposal.en.html regenerated; visual/index.html + visual/index.en.html rewritten (14 zh markers, data-metric attributes matching metrics.json, offline-only); Noto Sans SC subset woff embedded via base64 @font-face on all 4 pages, font-family-first verified, glyph coverage check = 0 missing.
- **report/**: asset rights ledger folded into report/copyright_statement.md as the "资产权利台账附录" appendix; copyright_statement.md gained the brand prior-rights paragraph; assumptions.json +2 assumptions (A-MINOR-DATA-001, A-FACILITY-DERIVE-001).
- **manifest.json**: 43 files; all en counterparts declared with language=en + translation_of; data_confidence set to "medium" (provisional geometry honesty).
- Four-gate self-check re-run; results persisted in self_check.json (2026-08-25).
