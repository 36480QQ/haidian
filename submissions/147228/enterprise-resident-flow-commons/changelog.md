# 方案迭代记录

## v1.11 - 2026-08-12

- Downgraded the provisional site-area metric confidence from `high` to `low`. The value remains a transparent working-area calculation, but its source is explicitly provisional geometry and must not be read as an official area or scoring basis.

## v1.10 - 2026-08-10

- Closed the projected-length formula expression in the normalized metric ledger; this is a text-quality fix only and does not change the metric value, source, status, or claim boundary.

## v1.9 - 2026-08-10

- Added a checked-in deterministic schema-audit summary so reviewers can see the 29-record split (`known=11`, `unknown=18`) without manually reconstructing the normalized object.
- Linked the audit summary and runner from both bilingual metric sections; the artifact keeps the claim boundary explicit and does not add field data or performance claims.

## v1.8 - 2026-08-10

- Normalized `metrics.json`: all 29 metric records now live under the single `metrics` object; the eight previously top-level mobility and simulation indicators were moved without changing their `unknown`/`null` values, formulas, sources or targets.
- Added `visual/assets/run-metrics-schema-audit.js`, a dependency-free deterministic check for top-level placement and `status`/`value` consistency.
- Kept the change schema-only; no geometry, simulation output, public snapshot, ranking field or operational-performance claim was changed.

## v1.7 - 2026-08-09

- Added a bilingual one-page executive brief at the top of both readable proposals.
- Bound one ordinary-person door-to-door chain to choice, request, takeover, fail-closed exit and independent replay.
- Kept the M-09 evidence explicitly synthetic/offline with `performance_results=null` and `operational_status=not_authorized_not_run`.

## v1.6 - 2026-08-09

- Added a minimum offline tabletop for the existing M-09 storm/network-outage fallback scenario.
- Added a machine-readable contract, deterministic replay runner and evidence output for four synthetic service requests, six checks and five rollback steps.
- Kept `performance_results=null` and `operational_status=not_authorized_not_run`; the tabletop does not claim staffing, accessibility performance, public acceptance, safety or implementation.

## v1.5 - 2026-08-09

- Added a bilingual implementation–operation contract that makes phase, participating roles, acceptance metrics, human fallback and stop/withdrawal conditions explicit at the start of the phasing section.
- Kept all role labels conceptual and all local baselines `unknown`; no institution, contract, funding, permit or achieved outcome is claimed.

## v1.0 - 2026-08-09

- Created an independent enterprise–resident mobility submission package.
- Replaced autonomy-first narrative with demand ledger, curb states, rail/bus feeder logic and four service levels.
- Added Beijing transport and Haidian parking-service evidence, employer TDM and curb-management research.
- Regenerated bilingual figures, offline visual pages and A3/A0 boards.

## v1.2 - 2026-08-09

- Added an explicit multi-agent queue/network sandbox for residents, enterprise employees, carers/children, visitors, logistics, night workers, metro trains, buses, bicycles, cars, walking/wheelchair flows and the gated air candidate.
- Added synthetic, clearly non-local readouts for queues, station load, transfer wait and curb service, with a calibration list for dated OD, headways, capacity, signals, conflicts and accessibility.
- Refreshed the simulation and evidence boards and added bilingual model-object diagrams with readable units, thresholds, status gates and source notes.

## v1.3 - 2026-08-09

- Added inspectable trip-leg templates for external enterprise commuting, resident services, shuttle transfers, logistics windows and ground-first air fallback.
- Added a dependency-free deterministic runner at `visual/assets/run-mobility-simulation.js`; it recalculates grouped mode shares, service supply, one-minute queues and calibration fields without network access.
- Added activity/agent-based multimodal and grouped accessibility method references; formal calibration now calls for mode share, road/curb volume, door-to-door time, distance and distributional access checks rather than a single efficiency score.

## v1.4 - 2026-08-09

- Added machine-readable `model_family` and `model_detail` disclosure fields while retaining the legacy `model` field for compatibility.
