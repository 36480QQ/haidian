# 方案迭代记录

## v1.1 - 2026-08-26

Round-2 repair per reviewer (CocoSgt CHANGES_REQUESTED). Per-file summary:

- proposal.md: v2 bilingual contract declared (bilingual_contract_version 1 + translation_file); scope hierarchy per announcement (43.6 km2 / 11.4 km2 / 368.4 ha, self-computed, not officially issued); 6 sourced global cases with claim-level source ids; 10 AI+ scenario cards (A1-A10) and 3 industry test protocols (B1-B3) with data-contract/baseline/error-stratification/runtime-monitoring/public-report wording; 7 personas; 3 pilgrimage landmarks + honour-display system + reversible component library; ecosystem map section; regional synergy (Beiwei / Future Science City / Huairou / E-Town / Jing-Jin-Ji) with info/talent/test/service interfaces; brand identity section (logo, grammar, applications, internal-codename disclaimer); annual programme brands (3), developer community, open operation and conversion pathway; implementation mechanism matrix (pilot criteria, lead/collaborate actors, checkpoints, privacy/accessibility checks, maintenance, qualitative cost classes, KPIs, complaints, escalation, stop conditions); single land-use caliber (8 classes, formula + confidence + recompute trigger); display-precision convention (provisional values at reduced precision only); per-asset rights ledger incl. font/figures/code/cases; source ids renumbered (date suffixes removed) to avoid digit precision patterns.
- proposal.en.md: full English translation (front matter language=en, translation_of=proposal.md; 100% English, mirrors all counts and sections).
- metrics.json: persona_count 7, global_case_count 6, scenario_card_count 10, land_use_zone_count 27 (matches features), green_ratio/public_space_ratio/road length rounded to display precision; 8 land-use ratio metrics (single caliber anchors); formulas and recompute triggers on every metric.
- sources.json: source ids renumbered; 6 case entries with publisher/URL/published+accessed dates/supporting_claims/license/reuse boundary; font entry (Noto Sans SC, OFL) and package figures/drawings entry; license keys added for ledger check.
- assumptions.json: added A-TRADEMARK-001 (brand prior rights, internal codename) and A-LANDUSE-001 (single caliber recompute), both accepted limitations.
- compliance_matrix.json / standard_matrix.json / design_depth_matrix.json: source ids renumbered; evidence summaries made distinct per entry (boilerplate removed); counts in evidence text updated to 6 cases / 10 cards / 3 tests / 3 landmarks / 9 nodes / 3 programmes / 7 personas.
- assets/figures: all 5 canonical figures regenerated at higher density plus 4 new figures (ai-ecosystem-map, logo-viaduct-loop, regional-synergy, node-experience), zh + en variants (18 PNGs). Machine QC at generation time: every figure edge-clip = 0.0000 on all four 10px bands; text-bbox edge violations = 0 per figure; glyph coverage verified for all figure text against Noto Sans SC cmap (0 missing CJK); ink coverage: site-overview 0.078/0.080, mobility-bluegreen 0.840/0.839, key-areas 0.622/0.621, land-use-structure 0.519/0.516, metrics-evidence 0.452/0.452, ai-ecosystem-map 0.250/0.254, logo 0.161/0.163, regional-synergy 0.198/0.196, node-experience 0.333/0.333 (zh/en). Provisional stamps (临时概念边界·非官方红线·官方数据发布后复算 / PROVISIONAL...) on every figure; scale bar + north arrow on the overview map; counts and ratios on separate axes in the metric figure; land-use pie uses the single caliber with formula note.
- drawings: a0-boards.pdf / a3-booklet.pdf regenerated (title >=60 pt on A0 page 1, non-clipped A3 cover) plus English counterparts a0-boards.en.pdf / a3-booklet.en.pdf.
- report/proposal.html + report/proposal.en.html: re-rendered from the md pair; en page contains zero CJK characters.
- visual/index.html + visual/index.en.html: rebuilt with the 14 required zh markers, data-metric/data-value declarations matching metrics.json (core 3 + counts + 8 land-use ratios), single land-use caliber table, task coverage, sources and assumptions lists, alt text on all images; en page zero CJK.
- Fonts: Noto Sans SC subsets embedded as data:font/woff in all 4 HTML surfaces (applied last); check_font_coverage reports 0 missing CJK everywhere.
- manifest.json: en counterparts registered (language=en, translation_of), data_confidence mixed_provisional_and_conceptual, sha256 hashes refreshed; self-check persisted.
- Manual checks (round 2): 中英实质等值已人工核对（计数、案例表、指标、provisional 警示逐项对应）; 品牌在先权利检索未完成前按内部工作代号处理; 图表 ink 值与剪裁检查结果见本条目图件段（ink 0.078-0.840 区间，edge_clip 全部 0.0000，text-bbox 边溢 0）。

## v0.1.0 - 2026-08-24

- Initial assembly (concept package) for viaduct-under-space-revival.
- Proposal drafted via OpenCode CLI (opencode), session ses_fcd6b17e6ffe38zfRj1PbxChbk; edited for structure.
- Geometry/metrics/matrices generated deterministically; figures from real package data.
- Valroot gates run on 2026-08-24 (results persisted in self_check.json).
