# Copyright / asset and source rights ledger

This package-level ledger is not a legal clearance opinion. The deliverable is a provisional concept package for review. Third-party items are citation-only unless a row says otherwise; no third-party logo, map tile, screenshot, photograph, drawing, or long quotation is republished. `to_verify` remains open where source terms or local authority are not proven.

## Per-asset ledger

| Asset / path | Author, tool, date | Input / source | Licence or authorisation | Attribution | Allowed use | Restriction / status |
|---|---|---|---|---|---|---|
| `proposal.md` | JohnXu22786; direct Codex editing; 2026-08-29 | Taskbook, cited sources, package geometry and review feedback | Original package text; repository display | JohnXu22786 | Review and concept discussion | No claim of official policy, approval, partnership or deployment |
| `proposal.en.md` | JohnXu22786; direct Codex editing; 2026-08-29 | English translation of `proposal.md`; same package evidence | Original translation; repository display | JohnXu22786 | Review and concept discussion | Substantive draft; item-by-item human equivalence review remains required |
| `report/narrative.md` | JohnXu22786; direct Codex editing; 2026-08-29 | Proposal and source registry | Original package text | JohnXu22786 | Offline report | Same provisional / to_verify boundary as proposal |
| `report/proposal.html` / `report/proposal.en.html` | Local deterministic renderer, direct Codex repair; 2026-08-29 | Markdown proposal, local embedded font, package figures | Original wrapper; renderer dependencies build-time only | JohnXu22786; sources in `sources.json` | Offline reading and review | No remote asset dependency; not a regulatory publication |
| `visual/index.html` / `visual/index.en.html` | Local deterministic HTML builder, direct Codex repair; 2026-08-29 | `metrics.json`, package figures, local embedded font | Original wrapper; build-time dependencies only | JohnXu22786 | Offline visual review | Embedded font subset is for this package view; external font redistribution not asserted |
| `assets/figures/site-overview.png` / `.en.png` | Local Matplotlib/Pillow build, direct Codex repair; 2026-08-29 | Package geometry and proposal labels | Original diagram; no basemap | JohnXu22786 | Repository display and review | Concept relation diagram; no survey or redline |
| `assets/figures/key-areas.png` / `.en.png` | Local Matplotlib/Pillow build, direct Codex repair; 2026-08-29 | Package geometry and proposal labels | Original diagram; no third-party imagery | JohnXu22786 | Repository display and review | Concept node diagram; ownership and engineering conditions to_verify |
| `assets/figures/land-use-structure.png` / `.en.png` | Local Matplotlib/Pillow build, direct Codex repair; 2026-08-29 | Six proposal target shares and `metrics.json` boundary note | Original diagram | JohnXu22786 | Repository display and review | Targets are not existing, statutory, or geometric areas |
| `assets/figures/mobility-bluegreen.png` / `.en.png` | Local Matplotlib/Pillow build, direct Codex repair; 2026-08-29 | Package geometry and concept routes | Original diagram; no third-party map | JohnXu22786 | Repository display and review | Relational route diagram; capacity and right-of-way to_verify |
| `assets/figures/metrics-evidence.png` / `.en.png` | Local Matplotlib/Pillow build, direct Codex repair; 2026-08-29 | `metrics.json` | Original diagram | JohnXu22786 | Repository display and review | Provisional ratios/counts; not measured performance |
| `assets/figures/logo-brand.png` | Existing package asset; source/author not independently evidenced in this round | Existing package file | Rights and trademark clearance to_verify | None asserted | Working concept marker only | Do not treat as registered logo; replace/remove before public release if clearance unavailable |
| `drawings/a0-boards.pdf` / `.en.pdf` | Local Matplotlib/Pillow PDF export; direct Codex repair; 2026-08-29 | Ten package figures and package text | Original compilation; build-time dependencies only | JohnXu22786; source registry | Offline review | A0 concept board, not construction or statutory drawing |
| `drawings/a3-booklet.pdf` / `.en.pdf` | Local Matplotlib/Pillow PDF export; direct Codex repair; 2026-08-29 | Ten package figures and package text | Original compilation; build-time dependencies only | JohnXu22786; source registry | Offline review | A3 concept booklet; professional checking required |
| `geometry/*.geojson` | JohnXu22786 / direct Codex repair; 2026-08-29 | Provisional package geometry; no third-party basemap | Original conceptual geometry; repository display | JohnXu22786 | Machine validation and concept diagrams | Low-confidence, non-redline, non-survey geometry; do not infer ownership or approval |
| `metrics.json`, `assumptions.json`, `risk_register.json` | Direct Codex editing; 2026-08-29 | Package geometry, proposal counts, taskbook | Original package records | JohnXu22786 | Audit and reproducibility | Values and thresholds remain provisional or to_verify |
| `sources.json` | Direct Codex editing; 2026-08-29 | Official/cited pages and package provenance | Citation registry; page-specific reuse terms remain separate | Each publisher in row | Citation and short mechanism summary only | C02/C04 verified primary-page facts; C01/C03/C05/C06 non-counted background references |
| `manifest.json`, `self_check.json`, matrices and `changelog.md` | Local validation/build tools, direct Codex repair; 2026-08-29 | Package files and hashes | Original audit metadata | JohnXu22786 | Review and reproducibility | Hashes describe this package state only |

## Sources and case boundaries

Official source snapshots and links are recorded in `sources.json`. C02 (Dutch Government Algorithm Register) and C04 (UK AI Security Institute) have a verified primary landing-page fact in this round and are counted. C01, C03, C05 and C06 remain `background_not_counted`; no screenshot, logo, record, dataset, or long quotation from them is included. Citation does not grant a licence to reproduce page assets.

## Fonts and software dependencies

| Dependency | Author / version record | Licence record | Use and boundary |
|---|---|---|---|
| Noto Sans SC / Noto CJK SC | Local Windows font source used for generation; exact installed build identifier not captured | SIL Open Font License 1.1; official reference: https://openfontlicense.org | A subset is embedded in offline HTML and used for local raster/PDF rendering. The original font file is not added to the package; external redistribution remains `to_verify`. |
| Python standard library | Local bundled Python; exact version in execution log | Python Software Foundation License | Build and validation only; not redistributed |
| Matplotlib | Local bundled dependency; exact version `to_verify` | Matplotlib project licence as distributed | Figure/PDF generation only; capture exact notice before public release |
| Pillow | Local bundled dependency; exact version `to_verify` | HPND/PIL licence as distributed | Image composition only; capture exact notice before public release |
| Shapely / pyproj / jsonschema / ReportLab where invoked | Local bundled dependencies; exact versions `to_verify` | Respective project licences (BSD/MIT/MIT/ReportLab terms as applicable) | Geometry, schema or export support only; no dependency package is republished; capture exact notices before release |

## AI, data, names and public-use limits

Diagrams and text were directly edited/generated in Codex from the existing package, taskbook, review text and cited source summaries. No claim is made that an external AI-generated image, public dataset, logo, name, or partner asset has been cleared. Package geometry is conceptual and contains no asserted personal data. Any future operational pilot must use data minimisation, aggregation, access control, retention/deletion rules, human review, appeal, pause and manual fallback. `COMMUNITY-DISPLAY-ONLY` applies until rights, privacy, accessibility, heritage, fire, ownership and professional review are separately evidenced.
