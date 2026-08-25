# 方案迭代记录

## v0.1.0 - 2026-08-24

- Initial assembly (concept package) for digital-twin-ops.
- Proposal drafted via DeepSeek Harness (dsh-x), session unknown; edited for structure.
- Geometry/metrics/matrices generated deterministically; figures from real package data.
- Valroot gates run on 2026-08-24 (results persisted in self_check.json).

## v0.2.0 - 2026-08-26 (repair round 1, CocoSgt CHANGES_REQUESTED 53.0 -> target >=90)

- proposal.md: full rewrite to v2 bilingual contract (bilingual_contract_version=1, translation_file=proposal.en.md). Added official three-tier scope hierarchy (about 43.6 km2 / 11.4 km2 / 368.4 ha), three-areas-two-wings and five-region coordination loop, brand/VI section with logo direction, trademark prior-rights paragraph, twelve AI+ scenario cards, six sourced global cases, three industry test-and-validation scenarios, five personas, landmark catalogue, reversible component library, honour-display system, developer-community mechanism, scenario-opening five-step process, talent/enterprise/developer pathways, international-communication copy, annual event brands, RACI implementation matrix with stop/exit conditions, indicator table with confidence/recompute triggers, item-by-item rights register, and two tables for land use and perceptible design. All claims keep the honesty bar (concept only, no FAR/height/investment/capacity conclusions, provisional recompute language). Land ratios now match geometry (27/26/17/13/9/8).
- proposal.en.md: full language=en translation (translation_of=proposal.md) with the 13 EN canonical sections, tables and evidence anchors; no functional Chinese on en pages.
- assets/figures: regenerated 8 zh + 8 en figures (site-overview, land-use-structure, key-areas, mobility-bluegreen, metrics-evidence, belt-structure, ai-ecosystem, logo-concept). Maps carry place names, scale bar, north arrow, legends and bilingual PROVISIONAL stamps; metrics-evidence uses separate axes (no cross-unit sharing); site-overview vs mobility-bluegreen have distinct information tasks; diagram text-bbox checks (no clip, no overlap) run at generation time; ink >= 0.08 maps / >= 0.10 charts and edge-clip < 0.02 verified by machine; en variants are 100% English.
- drawings: regenerated a0-boards.pdf / a0-boards.en.pdf (2 pages, first page dense, title >= 60 pt) and a3-booklet.pdf / a3-booklet.en.pdf (8-page booklet, cover title not clipped) with bilingual provisional stamps and Noto Sans SC embedded.
- visual/index.html (zh) and visual/index.en.html (en): rebuilt dashboards embedding all figures, the 14 required zh markers, metric declarations matching metrics.json, scope/indicator/implementation tables and self-check/source/assumption sections; en page is English-only.
- metrics.json: global_case_count 4 -> 6 (visible-text table has six sourced rows); all counts consistent with proposal tables.
- sources.json: +8 entries (6 traceable global cases with publisher/URL/dates, Noto Sans SC OFL entry, Python toolchain BSD entry); added explicit licence fields; per-item reuse boundaries.
- standard_matrix.json / design_depth_matrix.json: evidence_summary_zh rewritten per item to point at distinct real content (5 standards / 15 depth items unique).
- risk.json: rewritten to the digital-twin-ops theme (boundary/data-gap/privacy/statutory/technology/acceptance/operation risks) with the 8 rubric dimensions.
- report/copyright_statement.md: item-by-item rights register + brand prior-rights paragraph added.
- manifest.json: schema 0.2.0 rebuilt with all en counterparts (language=en + translation_of), new figure/drawing/HTML entries, hashes refreshed, validation_claim.data_confidence=medium (provisional data), readiness_contract persisted-self-check-v1 re-marked.
- self_check.json: four-gate report re-persisted (2026-08-26) and figure_qc machine evidence (ink/clip; text-overlap not verified post-hoc) appended; figure generation-time text-bbox checks recorded in this changelog.
- HTML (proposal.html / proposal.en.html / visual/index.html / visual/index.en.html): regenerated from markdown via render_proposal_html.py where applicable, then Noto Sans SC subset WOFF1 data-URI fonts embedded last (embed_fonts.py).
- 中英实质等值已人工核对（数值、范围、计数、机制词与表格口径一致）；品牌在先权利检索未完成前按内部工作代号处理。