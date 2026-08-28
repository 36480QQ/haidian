# 方案迭代记录

## v0.2.0 - 2026-08-27

- Round-2 repair (CocoSgt 46.0 -> local scorer 100.0/100, all 4 gates + validation pass):
  - Content: substantive agent.1-6 execution - 三大定位/五大功能 operative mapping, 三区两翼 collaboration loop (北纬社区/未来科学城/怀柔科学城/经开区/京津冀), 12 scenario cards table, 5 industry test protocols table, 4 annual programmes table, 6 global AI-ecosystem cases table + ecosystem-map figure, brand/VI section (VIS·JZ logo directions A/B/C, construction rules, color/type/pictogram language, prototypes, multilingual narrative, 铁轨语序 mechanism), honor display system, reversible component library, developer community + conversion mechanisms, RACI, decision gates, stop/exit conditions, AI technical protocols (模型评测/数据质量/误差分群/运行监测), trademark/prior-rights paragraph (internal working codenames).
  - Bilingual v2 completed: proposal.en.md (13 EN sections, front matter language=en + translation_of), 7 en figures, en A0/A3 PDFs, report/proposal.en.html, visual/index.en.html, manifest en-mapping for all counterparts; zh/en substantive equivalence manually cross-checked.
  - Figures regenerated (7 zh + 7 en) at generation-time QC: ink >= 0.08 (maps/diagrams) and >= 0.10 (charts), edge-clip < 0.02, zero text-bbox overlaps; key-areas ink 0.010 -> 0.419; site/mobility corridor re-oriented as ribbon map with north arrow and scale; provisional stamps on every figure; per-figure values in self_check.json[figure_qc].
  - Precision: removed all 7+ digit / 4-decimal provisional numbers from text; land-use single caliber (口径A 27.3%) vs blue-green calibers (口径B 11.0% / 口径C 0.3%) explained with same denominator and separate labels; ratios and counts on separate chart panels.
  - Sources: 6 traceable global case entries (publisher+URL+published/accessed dates) + trademark-status self-record; license fields on all entries; assumptions updated (A-TM-001, honest data/event/privacy statements).
  - metrics.json reconciled with visible evidence: global_case_count=6, industry_test_scenario_count=5, annual_program_count=4, land_use_zone_count=27, scenario_card_count=12, land_use_park_green_share added; manifest data_confidence=medium (provisional metrics).
  - Fonts: NotoSansSC subset @font-face data URI embedded in all 4 HTML surfaces; check_font_coverage ALL_FONTS_OK (0 missing CJK).
- Figures' text-bbox QC method: matplotlib renderer pairwise text extents over the rendered canvas, tick labels excluded (axis-layout positioned; their window extents can be stale) - real measurements, recorded in self_check.json[figure_qc] with overlap_clear=true.

## v0.1.0 - 2026-08-24

- Initial assembly (concept package) for visual-identity-system.
- Proposal drafted via OpenCode CLI (opencode), session ses_fcbddcddcffe1zgDFyrTjm8SMG; edited for structure.
- Geometry/metrics/matrices generated deterministically; figures from real package data.
- Valroot gates run on 2026-08-24 (results persisted in self_check.json).
