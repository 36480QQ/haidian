# 方案迭代记录

# 学院路环高校创新带 - 变更记录

## v0.1.0 - 2026-08-24

- Initial assembly (concept package) for xueyuanlu-university-innovation-belt.
- Proposal drafted via DeepSeek Harness (dsh-x); edited for structure.
- Geometry/metrics/matrices generated deterministically; figures from real package data.
- Valroot gates run on 2026-08-24 (results persisted in self_check.json).

## v0.2.0 - 2026-08-25

Round-2 repair per reviewer items (CocoSgt 2026-08-24 review, score 55/100):

- proposal.md: adopted bilingual_contract_version=1; added agent.1-6 delivery sections (brand/VI + regional coordination map, 7 sourced global cases + ecosystem map, 10 scenario cards + 3 industry test protocols, AI public space/3 landmarks/honor system/component library, cultural wayfinding + international copy, developer community/scenario opening/investment funnel); transformable project table with lead/collaborator roles, preconditions, permit/ownership interfaces, cost tiers (method/base-period scope), stage decision gates, KPIs, acceptance evidence, human fallback and stop/exit conditions; per-metric source/formula/confidence/use-limits/recompute-trigger table; brand prior-rights paragraph (internal working codenames pending clearance); barrier-free law anchored to Article 39 service scenarios; all provisional values shown rounded (no 7+ digit numbers, no >3 decimals, no thousands separators); land-use caliber and recalculation rule stated; region names (Beiwei, Future Science City, Huairou, E-Town, Jing-Jin-Ji) added.
- proposal.en.md: full English counterpart, language=en + translation_of=proposal.md; substantively equivalent numerals/tables/claims; no functional Chinese (brand glosses are English/pinyin).
- metrics.json: aligned counts with visible tables (land_use_zone_count 21->24); rounded provisional values (site ~1141 ha, ratios to <=2 decimals); added display_precision/use_limits/recompute_trigger per metric.
- sources.json: renamed long-digit source IDs (precision guard); added JZ heritage park gov source (2023-06-26) and 7 verified global-case institutional sources; added PACKAGE-ASSET-* provenance entries with license fields; every entry carries license + reuse boundary.
- assumptions.json / risk.json: rewrote garbled UTF-8 (round-1 mojibake) with clean zh/en statements.
- Figures (zh+en): 7 figures, all regenerated at 12x8 in 150dpi with Noto Sans SC; every spatial sheet carries scale/north/legend + bilingual PROVISIONAL stamp; ratios and counts on separate axes; land-use chart carries baseline note; ink targets met (>=0.08 maps, >=0.10 charts, verified by PIL/numpy); generation-time text-bbox overlap check ran clean (0 overlaps reported; post-hoc overlap re-verification stays not_verified).
- Drawings: A0 (2 pages) + A3 (4 pages) regenerated in zh + en; A0 page 1 has >=60pt title and a dense statement panel.
- Visuals: visual/index.html rewritten with 14 required content markers and rounded metric data-values matching metrics.json; visual/index.en.html added (en-only labels).
- Matrices: compliance/standard/design-depth evidence summaries rewritten to point at distinct real content (sections/figures/metrics/anchors); anchors [standard:]/[depth:]/[data:]/[metric:] added in proposal.md per reviewer item.
- HTMLs: report/proposal.html + report/proposal.en.html re-rendered offline; Noto Sans SC subset embedded as base64 data-URI with @font-face on all 4 HTML surfaces.
- manifest.json: declared en counterparts (figures, PDFs, HTMLs, proposal.en.md) with language=en + translation_of; validation data_confidence=mixed_provisional_and_conceptual.

- Final verification (2026-08-25): score_rubric.py 97.0/100 with empty reviewer_gaps and no mandatory rejections; validate_local_submission PASS (0 errors, 1 benign provisional-boundary warning); 4 gates (deterministic/spatial/visual/professional) PASS; figure_qc embedded in self_check.json[figure_qc] with machine ink/edge-clip measurements over all zh+en PNGs and A0/A3 PDFs (ok=True, overlap_clear=not_verified by design).
