# Changelog — 京张智脉·百年共创带 (jingzhang-intelligent-artery)

## 2026-08-10 — Remediation pass (gates green)
Addresses maintainer review of PR #1548 (score 52/100, do-not-publish):

- Embedded the agent.1–agent.6 detailed deliverables directly into `proposal.md` (zh) and `proposal.en.md` (en) as appendices, and removed the non-whitelisted `report/agent_outputs/` directory.
- Fixed `manifest.json`: removed the 12 `report/agent_outputs/*` entries (outside the allowed path whitelist) and removed the stale self-referential `sha256` on the `manifest.json` entry (kept listed per `REQUIRED_AI_PACKAGE_FILES`); recomputed all remaining manifest `sha256` values.
- Prior passes (this branch history) rebuilt the bilingual outputs: real English A3/A0 PDFs and `visual/index.en.html` (distinct from zh, page-by-page CJ/EN cross-check), fixed figure rendering (overview / key-areas / metrics / mobility), realized agent.1–agent.6 into substantive deliverables, and added privacy / human-review statements (agent.3) plus a copyright statement (`report/copyright_statement.md`).
- Regenerated `self_check.json` (checks-array format). All gates pass: deterministic validation, spatial review, visual packaging review, professional evidence review. `can_enter_formal_review = true`.

## 2026-08-09 — Initial submission
- Created the submission package (schema_version 0.2.0) with proposal, AI package (metrics / assumptions / sources / matrices), geometry, figures, drawings, static visual, and report HTML.
