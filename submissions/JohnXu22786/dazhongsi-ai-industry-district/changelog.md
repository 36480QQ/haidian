# 方案迭代记录

## v0.1.0 - 2026-08-24

- Initial assembly (concept package) for dazhongsi-ai-industry-district.
- Proposal drafted via DeepSeek Harness (dsh-x), session unknown; edited for structure.
- Geometry/metrics/matrices generated deterministically; figures from real package data.
- Valroot gates run on 2026-08-24 (results persisted in self_check.json).

## v1.1-round1 - 2026-08-26 (REPAIR ROUND-1, PR #3863)

Per-file summary of the round-1 repair:
- proposal.md: 12 scenario cards (S1-S12) each with input data / AI capability / location / operator / human-takeover & failure mode / outcome indicator; five talent personas (persona_count=5); global case table with 7 sourced cases (global_case_count=7); industry test protocol table (3 rows); annual programme table (5 rows); regional synergy matrix (Beiwei / Future Science City / Huairou / ETDZ / Jing-Jin-Ji); RACI lead/collaborate roles, stop/exit conditions, qualitative cost tiers; AI technical protocols (model evaluation / data quality / error stratification / runtime monitoring); brand & visual-identity section with logo; honour system, reversible component library, developer community, international communication; AI governance three-sentence bounds; resident opinion channel + annual disclosure; provisional/recompute boundaries throughout; no precise-looking provisional numbers; source ids dash-formatted to keep the text free of 8-digit runs.
- proposal.en.md: full English counterpart, 13 canonical EN sections plus supplementary sections, zero residual Chinese, bilingual_contract_version=1, translation_of=proposal.md; substantively equivalent (manually checked item by item).
- assets/figures (14 PNGs, 7 concepts x zh/en): regenerated at 150 dpi from package geometry with legends, north arrows, vertical scale bars, public-name context labels, PROVISIONAL stamps (zh bilingual, en English-only), dense layout; land-use chart with saturated fills and caliber notes; metrics-evidence with ratios and counts on separate axes; logo-precinct and ai-ecosystem-map added. Generation-time text-bbox overlap and clipping checks were run inside the generator for every figure (no overlaps/clips found); machine ink/edge-clip QC recorded in self_check.json[figure_qc].
- drawings: a0-boards(+.en).pdf (3 pages, A0 landscape, cover title >= 60 pt) and a3-booklet(+.en).pdf (7 pages, A3 landscape, cover title not clipped); Noto Sans SC subsets embedded (pdf.fonttype=42); provisional stamps on every page.
- visual/index.html: counts updated to match the proposal (12 cards / 5 personas / 7 cases / 3 tests / 5 programmes / 16 sources); visual/index.en.html added (English-only, offline).
- report/proposal.html + report/proposal.en.html: regenerated with render_proposal_html.py, Noto Sans SC subsets embedded last (data URI @font-face, family-first); zh blob >= 100 KB; en pages contain 0 functional CJK.
- metrics.json: scenario_card_count=12 added; all counts consistent with visible text evidence.
- sources.json: 16 entries; 7 global case entries (CASE-*) with institution pages, published/accessed dates, licences and reuse boundaries; date-bearing source ids dash-formatted; license keys added.
- manifest.json: schema 0.2.0; all en counterparts (figures, PDFs, HTML) declared with language=en + translation_of; data_confidence=medium; readiness contract re-persisted after the 4-gate run.
- report/copyright_statement.md: now the asset-rights registry (per-asset author/tool/licence/restrictions incl. Noto Sans SC OFL subsets, logo as internal working codename, brand prior-rights paragraph).
- self_check.json: four gates re-run and persisted; figure_qc (machine ink/clip + generation-time overlap evidence) injected after the mark so the manifest hash stays authoritative.
