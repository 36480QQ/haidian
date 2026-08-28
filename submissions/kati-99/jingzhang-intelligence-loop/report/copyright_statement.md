# Copyright Statement / 版权声明

Canonical path / 规范路径：`submissions/kati-99/jingzhang-intelligence-loop/report/copyright_statement.md`
（同一文件在 `manifest.json` 中登记为 `role: copyright_statement`；`sources.json`、`proposal.md`、`proposal.en.md`、HTML 与 PDF 均引用此路径，不存在 `copyrights/` 目录版本。/ All references in `sources.json`, `proposal.md`, `proposal.en.md`, HTML and PDF point to this path; no `copyrights/` variant exists.）

---

## 1. Original works / 原创作品

| Category 类别 | Items 条目 | Author 权利归属 | License / status 授权状态 |
| --- | --- | --- | --- |
| Text 文字 | `proposal.md`, `proposal.en.md`, `report/narrative.md`, HTML/PDF rendered copies | Declared AI agent on behalf of the submitter (`kati-99`) | Original; submitted under the open-call submission terms |
| Geometry 空间数据 | `geometry/*.geojson` (site_boundary, key_areas, land_use, roads, green_space, public_space, buildings, constraints, phasing) | Derived by the AI agent from repository-provided provisional data | Generated/derived; **provisional_only**, not official redline data |
| Figures 原创图件 | `assets/figures/*.png` and `*.svg` (site-overview, land-use-structure, key-areas, mobility-bluegreen, metrics-evidence, site-structure, implementation-roadmap, brand-identity, ai-landmarks, ecosystem-map, global-ai-cases, honor-component-library, wayfinding-ops) | AI-agent generated; plotted from the above geometry layers | Original; no third-party imagery |
| Drawings 图纸 | `drawings/a3-booklet.pdf`, `drawings/a3-booklet.en.pdf`, `drawings/a0-boards.pdf`, `drawings/a0-boards.en.pdf` | AI-agent generated | Original |
| Brand assets 品牌资产 | Logo "京张智环 / JingZhang Intelligence Loop", five-colour palette, contribution-wall and honour-component-library designs, wayfinding symbol set | AI-agent generated | Original; **no third-party trademark, logo or portrait is reproduced** |

## 2. Fonts / 字体

| Usage 用途 | Font 字体 | Version 版本 | Licence 许可 | Note 说明 |
| --- | --- | --- | --- | --- |
| Embedded in HTML (base64 woff2 subset) HTML 内嵌子集 | Heiti TC (STHeiti Medium) | 17.0d1e2 | macOS system-bundled font; bundled with the operating system, **not** an OFL / open-source licence | Subset contains only the glyphs actually used by each page (report: 934 glyphs; visual index: 423–433 glyphs). The subset is embedded so that the pages need no remote font loading (a submission requirement). Because system-font redistribution terms are not governed by an open licence, **if the organiser requires redistribution of the HTML outside the review context, the submitter will replace it with an OFL-licensed open-source CJK font (e.g. Source Han Sans / Noto Sans CJK / LXGW WenKai) and re-export.** |
| Figure rendering 图件渲染 | Heiti TC (STHeiti Medium) | same | same | Figures are exported as static PNG/SVG; SVG text is converted to paths (`svg.fonttype = path`) where applicable. |
| CSS font stack (fallback) CSS 回退栈 | PingFang SC, Microsoft YaHei, Noto Sans CJK SC, Source Han Sans, LXGW WenKai | — | system-bundled / OFL | Used only as a fallback when the embedded subset is unavailable; no remote font is ever loaded. |

**No commercial or licensed third-party font is distributed as a full font file.** Only per-page glyph subsets are embedded, and no remote font, remote script, remote map tile, iframe, form or external API is loaded by any HTML page.

## 3. Map and data sources / 地图与数据来源

| Source 来源 | Registered as 登记 ID | Status 状态 |
| --- | --- | --- |
| Official open-call announcement (Beijing Municipal Commission of Planning and Natural Resources, 2026-05-09) | `OFFICIAL-ANNOUNCEMENT` | `approved_formal` — document-level official source |
| Agent taskbook (repository-provided, rights cleared) | `AGENT-TASKBOOK` | `approved_formal` |
| Site package / provisional boundaries (repository maintainers) | `SITE-PACKAGE`, `BOUNDARY-SOURCE`, `KEY-AREA-SOURCE`, `DATA-SRC-PROVISIONAL-BOUNDARIES-20260605` | `repository_maintainer_provisional` — usable for generation and self-check, **not** for official redline, approval or precise area basis |
| Processed fact pack / navigation layer | `PROCESSED-FACT-PACK`, `SOURCE-REGISTRY` | `repository_processed_reference` |
| Six international city references (Helsinki, Amsterdam, Barcelona, Seoul, Montreal Declaration, Singapore Smart Nation) | `REF-HELSINKI`, `REF-AMSTERDAM`, `REF-BARCELONA`, `REF-SEOUL`, `REF-MONTREAL`, `REF-SINGAPORE` | `conceptual_reference_pending_source_verification` — portal home pages only; **not** source-registry-approved formal sources and **not** evidence for specific programme claims |

No commercial basemap, satellite imagery, street-view image or third-party map tile is used. All map-like graphics are plotted from the GeoJSON layers listed in section 1.

## 4. Embedded and third-party assets / 嵌入与第三方资产

- **No third-party brand, trademark, logo, portrait, stock image or photograph is embedded.**
- **No third-party text passage is quoted beyond short citations** of the official announcement and agent taskbook, both registered in `sources.json`.
- The six international city references are **names and public concepts only**; no image, diagram, document excerpt or logo from those cities is reproduced.
- All HTML files are self-contained: fonts are base64-embedded, figures are local relative paths, and no network request is made at render time.

## 5. Open items / 待清权事项

| Item 事项 | Action required 需采取的行动 | Trigger 触发条件 |
| --- | --- | --- |
| Heiti TC subset redistribution | Replace with an OFL-licensed CJK font and re-export HTML/PDF/figures | If the organiser publishes or redistributes the package outside review |
| Six international references | Register document-level URL, page title, publisher, publication/access date, supporting paragraph, licence, and manual verification status | Before any external publication or citation of a specific programme claim |
| Any future third-party font, image, trademark, portrait, map or case image | Obtain verifiable licence and update this statement and `sources.json`; otherwise replace or delete | On introduction of any asset outside the current original/open scope |

## 6. Responsibility / 责任声明

The AI agent is responsible for facts, sources, copyright, spatial data, indicators and expression. This statement covers only the assets present in this submission package; it does not constitute legal proof of rights over third-party material, nor does it certify that no third-party right exists. Maintainers and professional reviewers may require rework or rejection based on self-check, spatial review and compliance-matrix requirements.
