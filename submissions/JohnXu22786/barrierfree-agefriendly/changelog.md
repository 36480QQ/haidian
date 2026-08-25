# 方案迭代记录

## v0.1.0 - 2026-08-24

- Initial assembly (concept package) for barrierfree-agefriendly.
- Proposal drafted via DeepSeek Harness (dsh-x), session unknown; edited for structure.
- Geometry/metrics/matrices generated deterministically; figures from real package data.
- Valroot gates run on 2026-08-24 (results persisted in self_check.json).

## v1.0 - 2026-08-26

- Repair round 1 per CocoSgt review (PR #3882, 2026-08-23T23:29, 45.0/100 CHANGES_REQUESTED):
  - proposal.md / proposal.en.md rewritten: removed carbon/绿电/低碳/BedZED/Vauban template residue; added 10-field scenario card table, 6-row sourced case table, 3-row industry test protocol table, 3-row annual programme table and per-scenario field-level data governance table; added 三区两翼 + five region names, 生态图谱/模型评测/数据质量/运行监测/荣誉/组件库/开发者社区/国际传播 vocabulary; unified the land-ratio caliber story (geometry-recomputed vs classification-illustration calibers) with recompute triggers; kept honest provisional framing with no invented figures.
  - assets/figures: 14 PNGs regenerated (7 topics x zh/en: site-overview, land-use-structure, key-areas, mobility-bluegreen, metrics-evidence, ecosystem-map, logo-carejz) at figsize (12,8)/150dpi with titles>=18pt, labels>=13pt, annotations>=11pt, legend/scale/north + PROVISIONAL stamp on spatial figures; ink 0.084-0.337 (>=0.06 guard) and edge-clip clear; en variants 100% English.
  - drawings: a0-boards(.en).pdf (3 pages, title>=60pt, first-page ink 0.119) and a3-booklet(.en).pdf (5 pages, cover title not clipped) regenerated.
  - report/proposal.html + report/proposal.en.html regenerated via render_proposal_html.py (zh + en from the same markdown) and visual/index.html + visual/index.en.html rebuilt; all 4 surfaces font-embedded LAST with an OFL Noto Sans SC subset (data:font/woff base64, family-first override); zh proposal.html subset 197KB.
  - structured JSON aligned: metrics.json (global_case_count 4->6 per the 6-row case table, land_use_zone_count 24->27 per feature count, scenario_card_count=10 added); sources.json (+6 verified case entries with publisher URL/published/accessed dates, +license field on every entry); compliance_matrix/standard_matrix/design_depth_matrix evidence rewritten to distinct non-carbon content; risk.json (carbon risks replaced by accessibility data/survey/maturity risks; 8 dimensions re-scored to barrier-free theme); assumptions.json carbon statements replaced.
  - report/copyright_statement.md expanded into a per-asset rights ledger (figures/fonts/logo/geometry/cases) with brand prior-rights and internal-codename boundary; report/narrative.md rewritten.
  - manifest.json upgraded to the full v2 bilingual contract (all .en counterparts with language=en + translation_of, data_confidence=mixed_provisional_and_conceptual); self_check.json[figure_qc] = machine ink/clip evidence (ok=True, ink_ok=True, clip_clear=True, overlap_clear=not_verified - text-bbox overlap is not machine-verifiable post-hoc; figure-generation time had no matplotlib clipping/layout warnings, noted here).
  - Gates: 4-gate self-check PASS (deterministic/spatial/visual/professional), validate_local_submission PASS, score_rubric 97.0/100 PASS with empty reviewer_gaps and no mandatory rejections.
  - Manual declarations: zh/en substantive equivalence checked for claims, indicators, sources, warnings and figure captions (numbers 43.6/11.4/368.4, counts 10/3/6/5, ratios approx 0.11/0.003); brand prior-rights search not completed - treated as internal working codenames; figure ink/clip values recorded in self_check.json[figure_qc].