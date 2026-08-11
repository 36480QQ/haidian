# R006.1 assurance register / 审查登记

Status: `CONCEPT_RESEARCH_CANDIDATE`  
Purpose: separate participant-controllable checks from evidence that requires a qualified, independent or project-party actor.

## Completed participant-controllable checks / 已完成的参与者可控检查

| Check | Method | Result | Boundary |
|---|---|---|---|
| Bilingual file presence | Required-file and manifest inventory | PASS | Presence is not translation quality |
| Chinese/English byte separation | SHA-256 pair comparison | PASS after R006.1 rebuild | Different bytes are not semantic parity by themselves |
| Claim/status parity | Shared status register plus phrase scan | PASS for current revision | External facts remain unverified |
| HTML keyboard structure | Static semantic-order and link-target review | PASS | No real assistive-technology user test |
| Colour contrast | Programmatic palette contrast check | PASS for normal text palette | Does not cover every display/viewer condition |
| Figure topic separation | Per-figure title, content and perceptual/hash comparison | PASS | Diagrams remain conceptual |
| Rights inventory | Itemized `rights_ledger.json` | PASS as an inventory | Not independent legal clearance |
| Reproducible package hashes | SHA-256 manifest rebuild | PASS | Does not validate truth of source material |

## Independent or external checks / 独立或外部检查

| Discipline/check | Status | Required evidence | Acceptance authority |
|---|---|---|---|
| Planning and statutory controls | BLOCKED (X1/X6) | Official base, controls, parcels, authority and signed disposition | Qualified planner + project party |
| Transport and station interface | BLOCKED (X2/X6) | Dated field route, counts/measures, operations and signed review | Qualified transport/accessibility reviewer |
| Landscape, ecology and sponge-city performance | BLOCKED (X1/X2/X6) | Seasonal field evidence, hydrology/ecology basis and signed review | Qualified landscape/ecology professional |
| Municipal infrastructure | BLOCKED (X1/X4/X6) | Capacity, utilities, fire, maintenance and operating authority | Relevant municipal/engineering professionals |
| Data governance, privacy and cyber security | BLOCKED (X4/X6) | Named controller, legal basis, DPIA/security testing, incident and appeal contract | Project-party legal/data/cyber authority |
| PDF/UA conformance | BLOCKED (X6) | Tagged-PDF validator output and remediation log | Independent accessibility reviewer |
| Screen-reader and keyboard user testing | BLOCKED (X3/X6) | Named method, assistive technologies, compensated users and findings | Independent accessibility reviewer |
| Physical A0 two-metre readability | BLOCKED (X6) | Printed boards, viewing protocol, photos/measures and disposition | Independent graphic/accessibility reviewer |
| Cost, procurement and vendor exit | BLOCKED (X5/X6) | Quantity basis, quotes/ranges, 3-year TCO, exit and recovery receipt | Independent cost/procurement reviewer |

No row marked `BLOCKED` is represented as passed. Automated or internal checks do not substitute for the named independent checks.

