# Copyright Statement

## Generation tools

- All proposal text (`proposal.md`, `proposal.en.md`), structured data (`sources.json`, `metrics.json`, GeoJSON layers, compliance/standard/depth matrices), and narrative content were authored by the declared AI agent (Claude, agent family declared in `agent.json`) under human direction, based on the officially registered sources listed in `sources.json`.
- Derived figures under `assets/figures/` are generated locally and programmatically from the package's own GeoJSON, metrics, and matrix data using the Python imaging/plotting toolchain (Pillow; matplotlib where used in figure regeneration). No remote assets, remote fonts, or external map tiles are loaded by `visual/index.html`, `report/proposal.html`, or any figure.

## Third-party data and OSM/ODbL

- No OpenStreetMap (OSM) or other ODbL-licensed geometry, basemap, or attribute data is used in any layer of this package. All geometry derives from the maintainer-registered provisional boundaries in `brief/site-package/geometry/` plus agent-generated conceptual features, tagged `provisional_constraint` / `official_boundary=false`.
- Should any future revision introduce OSM-derived geometry, it will carry the attribution "© OpenStreetMap contributors, ODbL 1.0" in this statement, in the affected layer properties, and in `sources.json` before submission.
- Factual claims (registration counts, park dimensions, historical dates) cite publicly available official sources registered in `sources.json`; short factual references are used under lawful quotation for review purposes with sources named.

## AI-generated imagery statement

- Every figure and diagram in `assets/figures/` and every drawing sheet in `drawings/` is AI-assisted, programmatically generated content. These images are explanatory illustrations of conceptual recommendations only; they are not official planning drawings, not government-approved documents, and not evidence of boundaries, areas, or regulatory conditions. Authoritative data remains the GeoJSON/JSON packages and the registered sources.
- No photographic material, third-party artwork, scanned official drawings, or commercial map screenshots are included.

## License

- The entire submission package is provided under the **COMMUNITY-DISPLAY-ONLY** license declared in `proposal.md` front matter: it may be displayed and reviewed within this open-call community process; it grants no rights for commercial use, redistribution outside the review context, or representation as an approved plan.
- The bilingual counterpart `proposal.en.md` is covered by the same license and the same source registrations as the primary `proposal.md`.
