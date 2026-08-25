# Copyright and Source Statement

## Rights status

The four realistic concept images registered on 2026-08-24 were replaced by participant-provided source images on 2026-08-25. The participant described these four files as newly created work and explicitly requested their inclusion in this submission. The files did not retain participant-side service or model metadata, so those fields remain `unknown` rather than being guessed. The package therefore relies on the participant's authorship and redistribution representation for the supplied source pixels; it does not independently certify copyrightability, uniqueness or non-infringement.

The Dazhongsi source was subsequently edited with the OpenAI built-in image-generation tool in Codex to make the step-free route, wheelchair use and staffed non-digital service legible. The tool did not expose a model identifier. All four source images then received a deterministic embedded bilingual disclosure; the aerial additionally received deterministic bilingual station labels. No external photograph, map tile or logo was introduced by the package-side edit.

The rights basis is the [OpenAI Terms of Use effective 2026-01-01](https://openai.com/policies/terms-of-use/): as between the user and OpenAI, the user retains rights in Input and owns Output to the extent permitted by applicable law. The [OpenAI Sharing & Publication Policy](https://openai.com/policies/sharing-publication-policy/) is also recorded because it requires clear disclosure of AI involvement and human review. These terms support submission display and repository redistribution, but they do not guarantee copyrightability, uniqueness, non-infringement, factual accuracy or planning approval. The participant remains responsible for the published use.

## Generative asset register

| Asset path | Asset type | Creation method | Generation service | Model | Generation date | Source inputs | Post-processing | Rights basis | Redistribution status | Evidence status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `assets/figures/site-overview.png` | Realistic aerial concept image | Participant-provided generative concept image | `unknown` - participant-side metadata not supplied | `unknown` | Received 2026-08-25, Asia/Shanghai; original creation date unknown | Participant-provided source; source-input metadata not retained in package | Human review; Pillow 12.2.0 bilingual disclosure and station labels; pngquant 2.12.5 palette compression; no package-side photo compositing | Participant authorship/redistribution representation recorded in the task conversation | Authorized by participant for this submission and repository distribution; underlying service terms not independently recorded | `PARTICIPANT_ATTESTED_TOOL_METADATA_UNKNOWN` |
| `assets/figures/experience-zhongzhi.png` | Realistic station concept image | Participant-provided generative concept image | `unknown` - participant-side metadata not supplied | `unknown` | Received 2026-08-25, Asia/Shanghai; original creation date unknown | Participant-provided source; source-input metadata not retained in package | Human review; Pillow 12.2.0 bilingual disclosure; pngquant 2.12.5 palette compression; no package-side photo compositing | Same as above | Same as above | `PARTICIPANT_ATTESTED_TOOL_METADATA_UNKNOWN` |
| `assets/figures/experience-ai-origin.png` | Realistic station concept image | Participant-provided generative concept image | `unknown` - participant-side metadata not supplied | `unknown` | Received 2026-08-25, Asia/Shanghai; original creation date unknown | Participant-provided source; source-input metadata not retained in package | Human review; Pillow 12.2.0 bilingual disclosure; pngquant 2.12.5 palette compression; no package-side photo compositing | Same as above | Same as above | `PARTICIPANT_ATTESTED_TOOL_METADATA_UNKNOWN` |
| `assets/figures/experience-dazhongsi.png` | Realistic station concept image | Participant-provided source plus generative image edit | Participant-side service unknown; OpenAI built-in image generation in Codex for package-side edit | Participant-side model unknown; OpenAI edit model not surfaced | Source received and package-side edit completed 2026-08-25, Asia/Shanghai | Participant-provided source image; package-side edit used no additional third-party image | OpenAI image edit for step-free route, wheelchair user and staffed service; human review; Pillow 12.2.0 bilingual disclosure; pngquant 2.12.5 palette compression | Participant authorship/redistribution representation plus OpenAI Terms of Use effective 2026-01-01 for the package-side edit | Authorized by participant for submission/repository use; OpenAI edit subject to recorded terms and applicable law | `PARTICIPANT_ATTESTED_AND_OPENAI_EDIT_DISCLOSED` |

### Prompt record

- `site-overview.png`: high-oblique 16:9 aerial concept of the X Jingzhang Beijing rail-heritage corridor, linear park and Xiaoyue River connecting campus, research, neighbourhood and transit conditions; contemporary Beijing scale; no text, logo or watermark.
- `experience-zhongzhi.png`: realistic 16:9 public experiment garden with a continuous public path, independently closable robot-test court, movable conditions, observation, staffed stop point, workshop and equipment withdrawal route; no text, logo or watermark.
- `experience-ai-origin.png`: realistic 16:9 rail-heritage public co-development hall with open-source theatre, developer steps, prototype table, transparent laboratories, staffed rights/withdrawal desk, cafe and community activity; no text, logo or watermark.
- `experience-dazhongsi.png`: realistic 16:9 transit-arrival civic room with an accessible main path, staffed non-digital service, rest and commerce, limited AI side zone, complaint/return point, equipment exit and neighbourhood worktable; no text, logo or watermark.

### Integrity record

| Asset | Raw generated SHA-256 | Final disclosed SHA-256 |
| --- | --- | --- |
| `site-overview.png` | `5a07a90742e03d4ebb8ab9672a6c5fd2c35fdf3ab28f34c792143b3cea5f210a` | `9e1e04d3d490acb6cf3a07beb2b04c013bb224d3cbaab72f6e597791640044c2` |
| `experience-zhongzhi.png` | `bbee202060b75e62768d050ecb3565731d4b17a6286c19a8bb6495e49458e3de` | `ad175e48876c99126a31c866068e584553b578e21480f31136afd47653e22f75` |
| `experience-ai-origin.png` | `676e8728e5912781c2ea0ab172493f392c575ed978ff633d7778abec025d7836` | `a03c47f833846a68838d491972361fa0426aa34134a408fac56c3e6f8286c08f` |
| `experience-dazhongsi.png` | participant source `dc73f18d52598bc59735b6ccf4a416aece1de3989137843a4c832a1ccaaa9fc9`; OpenAI-edited intermediate `cd5967c21e887a4719ccefe04d80aa47aa6b1a5aef1f7239ab3b7af38f7d803e` | `5f810e30033965bd39c9e54ece6b6b438fa6a901052eab88ca757c5ad2f052b5` |

The raw generated files are not published because they lack the mandatory disclosure. The final files above are the only publishable source versions.

## Derivative and non-generative assets

| Asset group | Creation/source | Rights and limitation |
| --- | --- | --- |
| `station-experiences*`, `persona-day*`, `failure-atlas*`, `x-operating-proof*`, `mobility-bluegreen*`, `key-areas*`, `aerial-design-key*` | Locally rebuilt from the four registered concept images plus submission text, geometry and rules | Each layout repeats a visible language-appropriate concept-image disclosure. Generated pixels remain conceptual and are not site, boundary, ownership, engineering, implementation or approval evidence. |
| `framework-overview*`, `implementation-roadmap*`, `station-topology-proof*`, `metrics-evidence*`, `three-station-flagship-contracts*`, `station-design-atlas*`, `sections-accessibility*`, `identity-guidelines*`, `delivery-dashboard*` and remaining diagrams | Locally composed from submission GeoJSON, metrics, text and checked-in machine evidence | Participant-generated diagrams; no third-party photograph or commercial basemap. Provisional geometry remains conceptual. |
| `visual/assets/site-context-osm.json` and map-derived figures | Normalized OpenStreetMap data obtained through Overpass on 2026-08-17 | © OpenStreetMap contributors, ODbL 1.0. The shipped subset retains attribution and is not a survey, official boundary, ownership or accessibility record. |
| `visual/assets/cjk-font.css` | Locally subset Noto Sans CJK SC Regular and Bold embedded as WOFF2 data | SIL Open Font License 1.1; licence text is embedded in the CSS. Used to prevent Chinese missing-glyph boxes in offline HTML. |
| Lifecycle, topology, station-contract and tabletop scripts/results | Participant-generated deterministic validators and synthetic fixtures | Package evidence only; not field validation, certification, railway operation or implementation approval. |
| `proposal.md`, `proposal.en.md`, HTML, PDF and narrative | Participant submission assembled from registered sources and assets | Submission text/layout under CC BY-SA 4.0 where the participant may license it; third-party source rights and the limitations above remain in force. |

## Current-version asset audit

**Status: participant authorization recorded; participant-side generation metadata remains `unknown`.** The 2026-08-25 replacement introduces no package-known third-party map tile, logo or font. The updated figure sets, HTML and A3/A0 pages are local derivatives of the registered concept images, submission text and concept geometry. Current file integrity is recorded in `manifest.json`. Registration of any later asset remains a continuing publication rule.

All realistic concept images visibly state, in the relevant language, that they are AI/generative concept images, not site photographs and not planning or implementation approval. Captions carry the same evidentiary boundary. No enterprise logo, personal data, non-public spatial data, commercial map imagery, third-party photograph or unlicensed icon is intentionally included.

## QA and external blockers

Human bilingual and full-page visual checks are persisted in `visual/assets/bilingual-qa.json` and `visual/assets/visual-qa.json`. The PR #3828 repair closure is persisted in `visual/assets/review-3828-repair-matrix.json`; JSON is used because the submission validator permits only the fixed report filenames in `report/`.

Real deployment remains blocked until a legal operator, site permission, insurance, safety responsibility, data controller, accessibility reviewer and restoration funding are evidenced. Those future field-launch conditions do not weaken the asset-rights disclosure above, are not represented as completed partnerships and are not current asset repairs.
