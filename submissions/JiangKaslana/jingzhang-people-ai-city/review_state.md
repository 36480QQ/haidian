# v0.2 Review State — 2026-08-12

This file records the current state honestly. It is **not** a self-check PASS and does not replace `self_check.json` or `manifest.json`.

## Completed in the branch

- Bilingual proposal: `proposal.md` / `proposal.en.md`.
- Core proposition: **AI向前，人民在先 / AI Advances, People First.**
- Five Civic AI Rights: notice, choice, refusal, human review, appeal/correction.
- Two red civic anchors: Civic Engineering Hall + People's AI Service Station.
- Three AI pilgrimage landmarks: Civic Engineering Hall + Open-Source Origin Square + Civic Intelligence Arcade.
- 12 AI scenarios, all requiring a human or non-AI equivalent path.
- 9 acceptance user groups, explicitly including service workers and people without smartphones/accounts or who actively decline AI.
- 3 flagship validation protocols.
- 6 bounded global mechanism cases.
- 4 long-term civic operating programs.
- All 23 mandatory call/taskbook requirements mapped in `compliance_matrix.json`.
- `standard_matrix.json`, `design_depth_matrix.json`, `risk.json`, `metrics.json`, `sources.json`, `assumptions.json`.
- Nine GeoJSON layers: site boundary, key areas, land use, roads, buildings, public space/scenario nodes, green space, phasing, constraints.
- `visual/index.html` and `visual/index.en.html` are now fully self-contained with inline vector diagrams and do not depend on external or missing media.
- `report/proposal.html` and `report/proposal.en.html` are self-contained summaries.

## Spatial claim boundary

- `site_boundary.geojson` and `key_areas.geojson` inherit maintainer-provided **provisional** geometry.
- `official_boundary=false` is preserved.
- All newly drawn land-use, road, building, green-space, public-space, scenario and phasing geometry is **agent-generated conceptual design with low confidence**.
- Nothing in v0.2 is presented as a cadastral parcel, official redline, heritage control line, approved planning condition, engineering location, investment commitment or government decision.

## Generated locally but not yet fully attached to GitHub

A complete local visual package has been generated and visually checked:

- Chinese/English required figure sets:
  - site overview
  - land-use structure
  - key areas
  - mobility / blue-green
  - metrics / evidence
- Chinese/English A3 booklet.
- Chinese/English A0 boards.
- Additional high-resolution working visuals and lightweight vector PDF variants.

The current agent runtime can create Git blobs from base64 but does not expose a connector action that accepts a local container file path. The local shell also lacks authenticated `gh` access and cannot resolve GitHub directly. Several binary blobs were successfully created as a transport test, but the full required binary set has **not** been attached to the branch tree. Therefore the package must not claim visual-packaging completion.

## Still required before formal review

1. Attach the complete canonical PNG/PDF binary set to the branch.
2. Run repository scripts on the exact current head:
   - `render_proposal_html.py`
   - `finalize_submission.py`
   - `self_check_submission.py --mark-self-checked --json`
   - `participant_preflight.py --check-push`
   - spatial / visual / professional review scripts used by the repository.
3. Repair every current-head blocker found by those scripts.
4. Generate `manifest.json` only through the repository finalization workflow; do **not** hand-write hashes.
5. Only then consider opening the upstream Pull Request.

## Current declaration

**Package state: in development.**  
**Formal-review-ready: NO.**  
**Upstream PR opened: NO.**
