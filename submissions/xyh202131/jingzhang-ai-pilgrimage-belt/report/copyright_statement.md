# Copyright, licence and authenticity / 版权、许可与真实性

## 分层许可 / Component licences

截至 2026-08-24，投稿方 `xyh202131` 将本包中其原创的文字、表格、图解、SVG、PNG 导出、编辑版式、自编 JSON 与概念 GeoJSON 转化按 **CC BY 4.0** 许可。署名：`Twin-Track Jing-Zhang / 双轨京张, xyh202131, CC BY 4.0`。许可全文：<https://creativecommons.org/licenses/by/4.0/>。

As of 2026-08-25, contributor `xyh202131` licenses contributor-owned text, tables, diagrams, SVG source, PNG exports, editorial layout, package-authored JSON and conceptual GeoJSON transformations under **CC BY 4.0**. Attribution: `Twin-Track Jing-Zhang / 双轨京张, xyh202131, CC BY 4.0`. Full terms: <https://creativecommons.org/licenses/by/4.0/>.

投稿方自编的回放与离线交互代码采用 **MIT License**：Copyright (c) 2026 xyh202131。任何获得本软件及相关文档副本的人，可不受限制地使用、复制、修改、合并、发布、分发、再许可和/或销售，但所有副本或实质部分须保留上述版权和许可声明。本软件按现状提供，不作任何明示或默示担保；作者或版权持有人不对因本软件或其使用产生的索赔、损害或其他责任负责。

Contributor-authored replay and offline interaction code is under the **MIT License**. Copyright (c) 2026 xyh202131. Permission is granted, free of charge, to any person obtaining a copy of the Software and associated documentation to use, copy, modify, merge, publish, distribute, sublicense, and/or sell it, subject to including this copyright and permission notice in all copies or substantial portions. The Software is provided AS IS, without warranty; the authors or copyright holders shall not be liable for claims, damages or other liability arising from the Software or its use.

## 第三方与字体 / Third-party data and font

- `geometry/constraints.geojson` 含 OpenStreetMap 方向性背景，署名 `© OpenStreetMap contributors`，数据库许可为 **ODbL 1.0**：<https://opendatacommons.org/licenses/odbl/1-0/>。该层不进入 CC BY 授权；任何符合衍生数据库定义的再分发须保留署名与相同方式共享。它不是官方道路红线、铁路保护边界、市政线位、测绘或批准依据。
- 四份 PDF 的页眉、页题、说明和页脚在本地构建时使用 `NotoSansCJKsc-Regular.otf`（SHA-256 `2c76254f6fc379fddfce0a7e84fb5385bb135d3e399294f6eeb6680d0365b74b`）与 Pillow 12.2.0 确定性栅格化，既有投稿方 PNG 图件同样以像素嵌入；PDF 不嵌入字体程序。四份离线 HTML 通过 `visual/assets/offline-cjk-font.css` 共用由同一源字体生成的 WOFF2 子集，避免干净浏览器缺少 CJK 系统字体时出现方框；子集由 fontTools 4.62.1 对四份最终 HTML 的字面字符并集生成，覆盖 1144 个 Unicode 码点，WOFF2 SHA-256 为 `9eaffa9b2f5786ec59e1beb8b98b67ecb428fd602dc20fba9d79921d3a6fb4c8`。字体采用 **SIL Open Font License 1.1**：<https://openfontlicense.org/>；源字体不作为独立文件分发。四份 PDF 是定页视觉出版物，不声明可搜索文本或 tagged-PDF 合规；配套离线 HTML 承担机器可读与键盘阅读入口。
- Repository-provided provisional inputs, cited policy pages, cases, standards, trademarks, names and links are not relicensed. Their uses remain bounded by `sources.json` and `visual/assets/source-governance-register.json`.

## 逐路径自查 / File-by-file contributor inventory

`visual/assets/file-rights-inventory.json` 覆盖本次分发树的每个路径，并分别记录投稿方原创内容、投稿方代码、OSM 衍生数据库、仓库 provisional 输入、嵌入字体与仅引用外部来源的许可路径。该清单可以证明“每个文件都有明确处理决定”，但它仍是投稿方自查，不等同于独立法律意见、独立逐文件权利审计或商标检索。

`visual/assets/file-rights-inventory.json` covers every path in the current distribution tree and distinguishes contributor-authored content, contributor code, OSM-derived database content, repository provisional inputs, embedded font software and citation-only external sources. It proves that every file has an explicit handling decision, but remains a contributor inventory rather than independent legal advice, an independent file-level rights audit or a trademark search.

## 第59轮概念媒体方法 / Round 59 concept-media method

- `four-state-cover.webp`、54 秒无声 H.264 视频、双语 VTT、双语文字稿和四态合同均为投稿方原创概念表达，采用 Python 3.14.7、Pillow 12.2.0、Chrome 151.0.7922.174、FFmpeg/FFprobe 6.1.1 与登记的 Noto Sans CJK SC 源字体在本地确定性生成；未访问网络、未调用模型 API、未下载或嵌入外部媒体，不含音乐、配音或音轨。Chrome SHA-256 为 `b6d40f55e48e61760335d18f46abcec929e1a11b8330e7f2b501037584af4aa4`；FFmpeg 为 `0c4760db80d73a6ddc05c828a20c1b51c84bf61f4fcecff17f759c3edab800fb`；FFprobe 为 `01b99c76134e5c7a6b3f40f1d6c1e50f1084d5d5d763dfec1fde66bb1b575346`。工具二进制与源 OTF 不随包分发，继续适用各自独立许可。
- The cover, silent 54-second H.264 video, bilingual VTT, bilingual transcript and four-state contract are contributor-authored conceptual expression, produced locally and deterministically with Python 3.14.7, Pillow 12.2.0, Chrome 151.0.7922.174, FFmpeg/FFprobe 6.1.1 and the registered Noto source. No network, model API, download, external media, voice, music or audio stream was used. Tool binaries and the source OTF are not redistributed and retain independent licences.

## 真实性与排除 / Authenticity and exclusions

- 本轮新增的确定性概念媒体不是模型生成的现场图像，也不冒充现场、居民意见、批准方案、无障碍结果、现实恢复时间或运营证据；54 秒仅为编辑播放节奏。
- 许可不把临时几何升级为官方红线，也不证明现场踏勘、规划批准、工程可行性、无障碍达标、现实服务效果、责任接受、G1 或专业签署。
- 独立法律意见、逐文件独立权利审计与商标检索仍未提供；许可声明不冒充上述专业结论。

- The new deterministic concept media is not model-generated site imagery and is not presented as field evidence, resident opinion, approved design, accessibility result, real recovery duration or operational proof; 54 seconds is editorial pacing only.
- These licences do not establish an official boundary, field survey, planning approval, engineering feasibility, accessibility compliance, real service result, accepted duty, G1 status or professional sign-off.
- Independent legal advice, independent file-level rights audit and trademark search remain absent; this notice does not claim those professional conclusions.
