# Copyright Statement

## Generation tools

- All proposal text (`proposal.md`, `proposal.en.md`), structured data (`sources.json`, `metrics.json`, GeoJSON layers, compliance/standard/depth matrices), and narrative content were authored by the declared AI agent (Claude, agent family declared in `agent.json`) under human direction, based on the officially registered sources listed in `sources.json`.
- Derived figures under `assets/figures/` are generated locally and programmatically from the package's own GeoJSON, metrics, and matrix data using the Python imaging/plotting toolchain (Pillow; matplotlib where used in figure regeneration), plus — for the five core map figures — an OpenStreetMap-derived urban-fabric reference layer described in the section below. No remote assets, remote fonts, or external map tiles are loaded at view time by `visual/index.html`, `report/proposal.html`, or any figure; all figures are pre-rendered raster files.

## Third-party data and OSM/ODbL

- **OpenStreetMap attribution — © OpenStreetMap contributors, ODbL 1.0.** The five core map figures in `assets/figures/` (`site-overview`, `land-use-structure`, `key-areas`, `mobility-bluegreen`, `metrics-evidence`, each in `.png` and `.en.png`) are drawn over an urban-fabric reference layer derived from OpenStreetMap data — streets, railways, metro lines and stations, rivers and water bodies, parks and green space — retrieved from the Overpass API on 2026-08-18 for the bounding box 39.950–40.040 N, 116.320–116.395 E. This layer is licensed under the Open Database License (ODbL) 1.0; the licence and attribution requirement travel with any reuse of these figures. Source registered in `sources.json` as `OSM-ODBL-2026`; attribution is additionally printed inside every affected figure.
- The OSM layer serves **orientation only** — it shows where the real city is, so a reader can locate the proposal. It is not an official boundary, not a statutory drawing, and not an approval basis. No OSM geometry is used in the package's own GeoJSON: all geometry in `geometry/` derives from the maintainer-registered provisional boundaries in `brief/site-package/geometry/` plus agent-generated conceptual features, tagged `provisional_constraint` / `official_boundary=false`.
- The conceptual design layers overlaid on the OSM basemap (corridor spine, chainage, key-area extents, nodes, seams) are this proposal's own provisional content, drawn dashed/semi-transparent and labelled as such; they are not part of, and are not contributed back to, the OSM database.
- Factual claims (registration counts, park dimensions, historical dates) cite publicly available official sources registered in `sources.json`; short factual references are used under lawful quotation for review purposes with sources named.

## AI-generated imagery statement

- Every figure and diagram in `assets/figures/` and every drawing sheet in `drawings/` is AI-assisted, programmatically generated content. These images are explanatory illustrations of conceptual recommendations only; they are not official planning drawings, not government-approved documents, and not evidence of boundaries, areas, or regulatory conditions. Authoritative data remains the GeoJSON/JSON packages and the registered sources.
- No photographic material, third-party artwork, scanned official drawings, or commercial map screenshots are included. The basemap in the five core map figures is vector geometry rendered locally from OSM data (see attribution above), not a screenshot of any commercial map service.

## License

- The entire submission package is provided under the **COMMUNITY-DISPLAY-ONLY** license declared in `proposal.md` front matter: it may be displayed and reviewed within this open-call community process; it grants no rights for commercial use, redistribution outside the review context, or representation as an approved plan.
- The bilingual counterpart `proposal.en.md` is covered by the same license and the same source registrations as the primary `proposal.md`.

## 多模态资产的生成方式与权利边界

本包 `assets/media/` 下的多模态资产全部为**程序化生成或本方案自制**，不含任何来源不明或未清权的第三方素材：

| 资产 | 生成方式 | 权利与事实边界 |
| --- | --- | --- |
| `cover.png` 封面 | Python（matplotlib/PIL）程序化绘制，母题为本方案 Logo「道钉截面×应答声环」 | 本方案原创图形，无第三方素材 |
| `narrative.mp4` 概念短片 | Python 逐帧渲染后合成，素材取自本包内 `assets/figures/` 图件与 `geometry/` 几何数据 | **静音短片、无音轨**；画面为概念方案示意，**非实景照片、非实测数据、非官方审定成果**；片中数字均为方案引用的公开统计口径，来源标注见画面与 `sources.json` |
| `narrative.vtt` 字幕 | 与画面烧录字幕逐字一致 | 字幕即全部叙述内容 |
| `narrative-transcript.md` 文字稿 | 同上 | 供无法播放视频时完整获取内容 |
| `answer-bell.mp3` 应答钟示意音 | Python（numpy）合成衰减正弦与谐波叠加 | **程序化合成的示意音，不是任何实体钟的实录**；与大钟寺古钟博物馆及其馆藏文物无关；方案绝不敲击、移动或商业化使用任何文物古钟 |
| `answer-bell-transcript.md` 音频说明 | 同上 | 音频内容的文字说明 |

**播放约束**：本包任何页面引用上述音视频一律**不设自动播放**。

**AI 生成内容声明**：`visual/assets/renders/` 下四张概念意象图由 LibTV 平台 Lib Image 模型生成，属解释层素材，**不冒充实景照片、居民意见、官方边界或实测数据**；其中「应答钟广场」一张以公开授权的大钟寺实景照片（Wikimedia Commons，CC 许可）为参考图生成，用于还原古建形制。
