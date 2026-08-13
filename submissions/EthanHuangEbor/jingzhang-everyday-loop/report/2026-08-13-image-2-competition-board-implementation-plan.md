# Image-2 Competition Board Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace all ten bilingual primary figures with image-2-generated architectural competition boards, rebuild every dependent deliverable, and update PR #2398.

**Architecture:** Treat each final PNG as a self-contained generated board with a shared visual grammar and a content-specific prompt. Validate every output against fixed narrative and numerical invariants, then reuse the existing report/PDF assembly functions without invoking the legacy `build_figures()` routine.

**Tech Stack:** Built-in image generation (image-2), Python/Pillow, ReportLab, repository render and validation scripts, Poppler/PyPDF, Git/GitHub CLI.

## Global Constraints

- Palette: warm grey paper, deep navy linework, brick red and copper-gold accents, oxidized copper green for ecology.
- Style: architectural/urban-design competition board with axonometric drawings, sectional perspective, restrained collage figures, model shadows, fine paper grain and disciplined white space.
- Produce separate Chinese and English images for all five required figure stems.
- Preserve exact invariants: one spine, three loops, nine stations; four functional families; six mobility/blue-green elements; three differentiated key areas; `11.41 km²`, `9`, `12`, and `3` in the metrics board.
- Never introduce statutory FAR, height, official redlines, ownership claims or implementation commitments.
- Keep all tracked changes inside `submissions/EthanHuangEbor/jingzhang-everyday-loop`.

---

### Task 1: Generate the bilingual competition boards

**Files:**
- Replace: `assets/figures/site-overview.png`
- Replace: `assets/figures/site-overview.en.png`
- Replace: `assets/figures/land-use-structure.png`
- Replace: `assets/figures/land-use-structure.en.png`
- Replace: `assets/figures/mobility-bluegreen.png`
- Replace: `assets/figures/mobility-bluegreen.en.png`
- Replace: `assets/figures/key-areas.png`
- Replace: `assets/figures/key-areas.en.png`
- Replace: `assets/figures/metrics-evidence.png`
- Replace: `assets/figures/metrics-evidence.en.png`

**Interfaces:**
- Consumes: the approved visual specification and the fixed invariants in Global Constraints.
- Produces: ten 3:2 landscape PNG boards, each legible at report and A3/A0 placement sizes.

- [ ] Generate one Chinese and one English image per figure stem using a shared master style block plus a content-specific prompt.
- [ ] Save the generated images non-destructively, inspect them, then replace only the approved target filenames.
- [ ] Reject and regenerate any board containing illegible titles, wrong numbers, contradictory spatial relationships, neon/corporate styling, watermarks or unsupported official claims.
- [ ] Confirm all ten PNGs decode successfully, have landscape aspect ratio between 1.45 and 1.60, and exceed 1200 px on the long edge.
- [ ] Commit the approved image set with `git commit -m "Redesign competition board figures with image-2"`.

### Task 2: Rebuild dependent HTML and PDF deliverables

**Files:**
- Modify: `report/proposal.html`
- Modify: `report/proposal.en.html`
- Modify: `visual/index.html`
- Modify: `visual/index.en.html`
- Modify: `drawings/a3-booklet.pdf`
- Modify: `drawings/a3-booklet.en.pdf`
- Modify: `drawings/a0-boards.pdf`
- Modify: `drawings/a0-boards.en.pdf`

**Interfaces:**
- Consumes: the ten approved PNG paths from Task 1 and existing proposals/metrics.
- Produces: bilingual HTML pages and four PDFs referencing the new boards.

- [ ] Run `scripts/render_proposal_html.py` for both language proposals.
- [ ] Invoke only `build_visual()` and `build_pdf()` from `project-notes/build_everyday_loop.py`; do not invoke `build_figures()` or `main()`.
- [ ] Verify HTML references resolve to all ten new images.
- [ ] Render all fourteen PDF pages and inspect contact sheets for clipping, overlap, missing glyphs or black boxes.
- [ ] Commit rebuilt deliverables with `git commit -m "Rebuild bilingual board deliverables"`.

### Task 3: Refresh integrity metadata and validate

**Files:**
- Modify: `manifest.json`
- Modify: `self_check.json`
- Modify: `changelog.md`

**Interfaces:**
- Consumes: final output bytes from Tasks 1–2.
- Produces: refreshed hashes and a persisted formal-review-ready contract.

- [ ] Add a changelog entry describing the image-2 redesign and explicitly preserving provisional-boundary/data caveats.
- [ ] Ensure both report specification files are declared in `manifest.json` before refreshing hashes.
- [ ] Run `scripts/refresh_submission_manifest.py` and confirm every declared file hash is current.
- [ ] Run formal self-check with `--mark-self-checked --json` and require `can_enter_formal_review: true`.
- [ ] Run participant preflight with `--check-push --json` and require no blockers or out-of-scope files.
- [ ] Run targeted repository tests covering manifest, visual, spatial, professional, rendering and preflight behavior.
- [ ] Commit metadata and validation updates with `git commit -m "Refresh submission validation after board redesign"`.

### Task 4: Update and verify PR #2398

**Files:**
- No additional tracked files.

**Interfaces:**
- Consumes: the clean validated branch.
- Produces: an updated upstream PR with verified head SHA and CI state.

- [ ] Inspect `git status --short` and `git diff --stat upstream/main...HEAD`; require changes only inside the submission directory.
- [ ] Push `codex/formal-jingzhang-proposal` to `origin` over SSH.
- [ ] Update PR #2398 body with the image-2 redesign and validation evidence.
- [ ] Verify PR head SHA, target `open-city-ai/haidian:main`, changed-file scope and mergeability.
- [ ] Monitor `submission-validation`; fix and push any actionable failures.

## Plan Self-Review

- Specification coverage: all ten images, four rendered formats, manifest/self-check, visual and PDF QA, tests, push and PR update are covered.
- Placeholder scan: no `TBD`, `TODO`, deferred implementation or unspecified test steps.
- Interface consistency: Task 2 consumes the exact figure paths produced by Task 1; Task 3 hashes the outputs of Tasks 1–2; Task 4 publishes the validated result of Task 3.

