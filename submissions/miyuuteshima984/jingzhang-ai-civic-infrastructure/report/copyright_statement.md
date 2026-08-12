# Copyright, Data, and Asset Statement

## Submission authorship

This submission is authored under GitHub account `miyuuteshima984` with AI-assisted drafting, structuring, translation, geometry generation, validation preparation, and visualisation. Final responsibility for what is submitted through the account remains with the participant.

## Repository and official/public source use

Project scope, task requirements, land-use/building enums, provisional geometry, standards references and workflow rules are taken from the public `open-city-ai/haidian` repository and the official/public sources registered in `sources.json`.

The current site and key-area polygons are explicitly provisional. They may be used for generation, relative spatial reasoning, intake visualisation and package checks only. They are not reproduced or described as statutory redlines, ownership boundaries, approved regulatory planning or engineering control lines.

## Global case references

The proposal refers to first-party public webpages from Vector Institute, Mila, the Alan Turing Institute, AI Singapore, Seoul AI Hub and JTC Punggol Digital District. These references are used for factual and organisational-mechanism research only. The submission does not reproduce their logos, proprietary diagrams, photographs, maps or brand assets.

Each case source is kept as a factual reference rather than a reusable visual asset. The v0.5 source pass records publisher, retrieval date, intended use, reuse status and review status in `sources.json`. No case source is used to support Jing-Zhang statutory boundaries, development controls, guaranteed partnerships, investment amounts or implementation commitments.

## Figures and visual assets

Submission figures are generated from the package's own conceptual GeoJSON, metrics, text, and original diagram graphics. No commercial map tiles, remote fonts, third-party stock images, scraped photographs, unauthorised logos or externally hosted visual assets are embedded in the formal package.

Text-bearing figures have separate Chinese and English counterparts under the bilingual contract. Language-neutral geometry may be shared where allowed by the repository contract.

### Per-asset rights and generation ledger

| Asset group | Paths / examples | Author / generation method | Third-party material embedded | License / reuse status | Review note |
| --- | --- | --- | --- | --- | --- |
| Core raster figures | `assets/figures/site-overview*.png`, `land-use-structure*.png`, `key-areas*.png`, `mobility-bluegreen*.png`, `metrics-evidence*.png` | Original package diagrams generated locally from submission GeoJSON, metrics and participant/AI-assisted layout | None | Submission-original; distributed only under the package's `COMMUNITY-DISPLAY-ONLY` license | Re-exported and binary-decoded during PR #1954 repair; no external image layers |
| Taskbook coordination loop | `taskbook-coordination-loop.svg`, `.en.svg` | Original SVG authored for v0.5 from the repository taskbook structure and the submission's C7 concept | None | Submission-original; `COMMUNITY-DISPLAY-ONLY` | Diagram explicitly labels all institutional/spatial relationships as concept proposals |
| Full-factor AI ecosystem | `ai-ecosystem-map.svg`, `.en.svg` | Original SVG authored for v0.5 from the taskbook's land/space/industry/capital/talent/compute/data/scenario requirement | None | Submission-original; `COMMUNITY-DISPLAY-ONLY` | No external company marks, logos or proprietary ecosystem diagrams |
| Ten AI scenario cards | `ai-scenario-cards.svg`, `.en.svg` | Original SVG authored from the ten scenarios already defined by this submission | None | Submission-original; `COMMUNITY-DISPLAY-ONLY` | KPIs are concept-stage validation directions, not measured performance claims |
| Regional collaboration matrix | `regional-collaboration-matrix.svg`, `.en.svg` | Original SVG expressing potential interfaces with named regions/innovation areas | None | Submission-original; `COMMUNITY-DISPLAY-ONLY` | Names identify possible interfaces only; no logo, map, partnership claim or endorsement is reproduced |
| Implementation and operations matrix | `implementation-operations-matrix.svg`, `.en.svg` | Original SVG translating proposal phasing and operations logic into responsibility/threshold/KPI fields | None | Submission-original; `COMMUNITY-DISPLAY-ONLY` | Roles, budgets, contracts and approvals remain conceptual until confirmed by real entities |
| Privacy/data governance matrix | `privacy-data-governance.svg`, `.en.svg` | Original SVG translating the scenario risk model into data-minimisation/access/retention/exit rules | None | Submission-original; `COMMUNITY-DISPLAY-ONLY` | Does not claim completion of any real-world statutory privacy/cybersecurity assessment |
| Brand / VI concept direction | `brand-vi-direction.svg`, `.en.svg` | Original visual concept based on C7, a generic two-rail motif and original typography/layout | None | Submission-original; `COMMUNITY-DISPLAY-ONLY`; not an official event/government identity | Does not use government emblems, event organizer logos, seals, stamps or copied brand assets |
| Public-space components and wayfinding | `public-space-components-wayfinding.svg`, `.en.svg` | Original schematic component and information-system drawings | None | Submission-original; `COMMUNITY-DISPLAY-ONLY` | Concept components only; not construction drawings or proprietary products |
| Proposal HTML | `report/proposal.html`, `report/proposal.en.html` | Generated locally from the proposal text using repository tooling | None | Submission-original rendering; no remote dependencies | No CDN, remote fonts, analytics, external scripts or remote images |
| Offline visual pages | `visual/index.html`, `visual/index.en.html` | Original single-file HTML/SVG presentation | None | Submission-original; no external runtime assets | No remote JavaScript, map tiles, fonts, iframes, forms, analytics or tracking |
| A3/A0 PDFs | `drawings/a3-booklet*.pdf`, `drawings/a0-boards*.pdf` | Generated locally from submission-original text/geometry/figures | None beyond assets listed above | Submission-original compilation | Must be regenerated after v0.5 visual integration before final PR |
| GeoJSON | `geometry/*.geojson` | Conceptual geometry authored/generated for this submission from repository-permitted provisional constraints | Repository provisional boundary inputs are referenced, not claimed as participant-owned official data | Usage constrained by repository/public-source status | Provisional geometry cannot be reused as an official redline or precise-area source |
| Text / JSON / matrices | `proposal*.md`, `*.json`, `report/*.md` | Participant/AI-assisted original drafting using cited repository/public sources | Short factual references only; no copied proprietary diagrams or long-form copyrighted text | Package license applies to original expression; external facts retain source terms | All authority claims must remain traceable to `sources.json` / repository standards |

## Fonts, icons, code, and toolchain

The v0.5 SVG assets use generic CSS `font-family: sans-serif` and do not redistribute font files. No downloaded icon font, commercial typeface, third-party icon pack or proprietary design-system asset is embedded. Symbols in the C7/VI and component diagrams are original geometric primitives authored in SVG.

Repository validation/rendering scripts remain repository code and are not copied into this submission package. The package records results produced by those tools but does not relicense the repository's scripts. The offline HTML contains only submission-authored markup/CSS/SVG and no remote runtime dependency.

## HTML

`visual/index.html` and `visual/index.en.html` are self-contained offline pages using only embedded CSS and SVG. They load no remote JavaScript, map tiles, fonts, iframes, forms, analytics or tracking resources.

## AI generation disclosure

AI tools were used to help:

- inspect repository rules and peer submissions;
- structure the C7 City Completeness concept;
- draft and translate proposal text;
- create conceptual GeoJSON and machine-readable matrices;
- prepare local SVG/HTML presentation graphics;
- identify data gaps and consistency checks;
- prepare the v0.5 coordination, ecosystem, scenario, regional collaboration, operations, privacy, brand and wayfinding diagrams.

The declared model for the submission agent is recorded in `agent.json`. AI-generated content is treated as proposal material, not as an authority source. External factual claims are registered in `sources.json`, and statutory or engineering conclusions are not inferred from AI output.

## Rights-state vocabulary used by this package

- **submission-original**: original expression authored for this submission, including AI-assisted drafting or drawing under participant responsibility.
- **factual-reference-only**: a public source is used to support a factual or organisational statement; no source visual/brand asset is embedded.
- **repository-permitted-input**: repository material is used only within the usage boundary stated by the repository and source registry.
- **provisional-only**: material may support generation, visualisation or discussion but cannot support official redlines, statutory controls or precise-area claims.
- **not-embedded**: the source may be cited but its copyrighted image, logo, font, code or media is not included in this package.

## Future replacement and verification

When official site/key-area polygons, regulatory controls, existing-building surveys, heritage boundaries, transport interfaces or municipal data become available, all affected geometry, metrics, figures, HTML and PDFs must be regenerated and revalidated before any professional or statutory use.

Any future third-party image, font, code library, map layer, institutional logo or media asset must be added to this ledger with author/publisher, source, retrieval date, license/reuse term, transformation record, embedded/not-embedded state and reviewer note before it enters the formal package.