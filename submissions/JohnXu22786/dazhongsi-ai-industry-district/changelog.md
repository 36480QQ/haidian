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

## v1.1-round2 - 2026-08-26 (REPAIR ROUND-2, PR #3863)

Per-file summary of the round-2 repair (CocoSgt items: source_id 统一/alias、人类可见精度舍入、图件裁切/混合语言/警示遮挡、矩阵与 HTML 链接重生成):
- sources.json: canonical source_ids unchanged (proposal anchors keep resolving); the three date-bearing ids (DATA-SRC-ANNOUNCEMENT-2026-05-09、DATA-SRC-AGENT-TASKBOOK-2026-05-18、DATA-SRC-PROVISIONAL-BOUNDARIES-2026-06-05) now carry explicit "aliases" arrays mapping the legacy central-registry forms (DATA-SRC-OFFICIAL-ANNOUNCEMENT-20260509 / DATA-SRC-AGENT-TASKBOOK-20260518 / DATA-SRC-PROVISIONAL-BOUNDARIES-20260605), so both id families resolve.
- compliance_matrix.json: all 23 requirement source_ids switched to the canonical dash-form ids identical with sources.json/proposal.md.
- standard_matrix.json: all 5 standard source_ids switched to canonical ids (incl. provisional-boundaries id).
- proposal.md: "不引用任何未经发布的坐标与面积数值" wording replaced by "不将任何临时模型值作为官方事实……低置信概数……官方数据发布后整体复算"; 面积复算原则 paragraph extended with the rounded-low-confidence display rule (图件与页面逐项标注 provisional、非官方与复算触发); wildcard anchor [source:CASE-*] replaced by the seven explicit CASE-* ids (grouped in runs of <=3 markers per claim per the deterministic gate).
- assets/figures (14 PNGs, 7 concepts x zh/en): all regenerated from package geometry/metrics at 150 dpi (12x8 sheets) with constrained layout. land-use-structure.en left-edge label clipping fixed (legend column inside axes, transAxes rows 0.88..0.10); metrics-evidence zh/en axes/categories fully translated (en 100% English), human-visible values rounded ("≈19.5%", "≈0.3%", integer counts), ratios and counts on separate panels, bottom source/formula/confidence/recompute footnote restored, per-figure provisional notes; corridor maps laid out strip+left-legend+top title (north arrow and 1km scale bar inside the strip; blueprint-tint map canvas); every figure carries the bilingual (zh) / English (en) PROVISIONAL stamp 临时概念边界/非官方红线/官方数据发布后复算; en figures contain zero Chinese.
- drawings: a3-booklet(+.en).pdf (8 pages) and a0-boards(+.en).pdf (3 pages, A0 landscape, first-page title >= 60pt, va=top so never clipped) regenerated from the fixed figures; pdf.fonttype=42; provisional stamp on every page; rasterised page QC (edge-band probe, page ink) all clean.
- visual/index.html + visual/index.en.html: human-visible metric values rounded ("约 1141 公顷 / ≈19.5% / ≈0.3%") while machine data-value attributes keep the raw recomputable values (visual_review cross-check preserved); every metric annotated "provisional·低置信·非官方·官方数据到位后复算"; land-use paragraph now states the single caliber (概念用地配比分派合计100%，provisional，发布后按同口径复算); figure-QC pointer fixed to self_check.json[figure_qc] (removed stale asset paths).
- report/proposal.html + proposal.en.html: regenerated with render_proposal_html.py; Noto Sans SC subsets re-embedded last (data URI @font-face, family-first; zh blobs >= 100 KB; en pages 0 functional CJK; check_font_coverage ALL_FONTS_OK).
- metrics.json: unchanged (counts already consistent; they were not part of this round's items).
- self_check.json: four gates re-run (PASS) and persisted; figure_qc injected with machine ink/edge-clip measurements, ok=True ink_bad=[] clip_bad=[]; generation-time text-bbox QC (renderer extents) recorded here: all 14 figures 0 clipped texts / 0 overlapping text pairs; PNG ink (luminance<200 share): maps 0.124-0.135, charts 0.120-0.133, logo 0.080-0.082, ecosystem 0.082-0.087.
- manifest.json: hashes refreshed for all declared files after the figure/PDF/HTML/JSON edits; validation_claim.self_checked=true re-persisted; en counterparts remain declared language=en + translation_of.

Generation-time text-bbox QC (rendered, not guessed): run per figure after savefig at final DPI; criterion = pairwise text window extents overlap > 20 px2 or any text bbox outside the figure -> FAIL, plus 10px edge-band ink probe (<2%) for every PNG. Result: 14/14 figures OK; PDFs 8+8+3+3 pages edge-clean.
