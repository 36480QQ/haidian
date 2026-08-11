# PR #1822 review response — R006.1

Date: 2026-08-12  
Package status: `CONCEPT_RESEARCH_CANDIDATE`  
Formal professional scoring: `false`

## P0 repairs

1. **Bilingual package rebuilt**: Chinese and English proposals, five thematic figures, nine option maps, HTML reports, visual pages, A0 boards and A3 booklets are independently rendered. Every paired artifact has a different SHA-256 value. The repository bilingual audit passes.
2. **Stale semantics removed**: current-state text contains no legacy revision label, candidate-not-submitted label, or readiness claim. The land-use and mobility/blue-green figures now have distinct topic-specific content.
3. **Six agent workstreams added**: the bilingual deliverables register contains the brand/master diagram; five named cases and ecosystem; ten scenarios, three industry tests and five personas; public-space/landmark/recognition/component systems; cultural wayfinding/international communication; annual events/developer/scene-opening/conversion mechanisms.

## P1 repairs

4. **External evidence boundary**: X1-X6 remain `BLOCKED`. No field, real-user, operating-authority, cost/exit or independent-review evidence was fabricated. A five-stage approximately 100-day plan names role owners, dependencies, ROM cost bands, acceptance and stop conditions.
5. **Rights ledger**: `rights_ledger.json` itemizes participant identity, AI assistance, fonts, figures, primitive icons, provisional geometry, OpenStreetMap-derived records, official sources, standards, code, photography and named case references. `COMMUNITY-DISPLAY-ONLY` is explicitly not treated as an upstream relicensing power.
6. **Assurance register**: `assurance_register.md` separates completed internal checks from planning, transport, landscape, municipal, data-governance, PDF/UA, assistive-technology, physical-A0 and cost/exit reviews that require independent actors.

## Bilingual comparison

| Pair | Chinese | English | Result |
|---|---|---|---|
| Main proposal | `proposal.md` | `proposal.en.md` | Heading/evidence-reference audit PASS; language-specific bytes |
| Thematic figures | five `.png` files | five `.en.png` files | 5/5 language-specific and topic-specific |
| Option maps | nine `.svg` files | nine `.en.svg` files | 9/9 language-specific |
| Proposal reports | `report/proposal.html` | `report/proposal.en.html` | Offline, no active or remote assets |
| Visual pages | `visual/index.html` | `visual/index.en.html` | Offline and language-specific |
| A0 boards | `drawings/a0-boards.pdf` | `drawings/a0-boards.en.pdf` | six pages each; different hashes |
| A3 booklets | `drawings/a3-booklet.pdf` | `drawings/a3-booklet.en.pdf` | eight pages each; different hashes |
| Agent deliverables | `agent-deliverables.zh.md` | `agent-deliverables.en.md` | six workstreams in each language |

## X1-X6 status after repair

| Gate | Status | What is still required |
|---|---|---|
| X1 official spatial authority | BLOCKED | Official CAD/GIS/PDF, CRS, controls, parcels, ownership and rights |
| X2 field journey/interfaces | BLOCKED | Dated route, measurements, photos, obstacles and independent repeat walk |
| X3 real users/burden | BLOCKED | Accessible compensated participation, dissent and non-adoption reasons |
| X4 operating/data/legal authority | BLOCKED | Named accountable roles, legal basis, service/incident/appeal/data contract |
| X5 cost/procurement/exit | BLOCKED | Quantity basis, checked cost range, 3-year TCO, procurement and exit receipt |
| X6 independent assurance | BLOCKED | Qualified discipline reviews, PDF/UA, assistive technology and physical A0 test |

## Validation evidence

- `scripts/audit_bilingual_backfill.py`: PASS.
- Local R006.1 QA: nine checks PASS, covering 64/64 manifest integrity, JSON parse, stale labels, bilingual byte separation, image dimensions/difference, PDF decode/pages/text, offline HTML targets, agent coverage and rights fields.
- Git diff whitespace check: PASS.
- GitHub `submission-validation`: required after each pushed repair commit; the check result remains the authoritative repository gate.

The repair improves the participant-controlled package without converting missing external evidence into approval.
