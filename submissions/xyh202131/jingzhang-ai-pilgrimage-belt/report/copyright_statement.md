# Copyright, licence and authenticity / 版权、许可与真实性

## 分层许可 / Component licences

截至 2026-08-24，投稿方 `xyh202131` 将本包中其原创的文字、表格、图解、SVG、PNG 导出、编辑版式、自编 JSON 与概念 GeoJSON 转化按 **CC BY 4.0** 许可。署名：`Twin-Track Jing-Zhang / 双轨京张, xyh202131, CC BY 4.0`。许可全文：<https://creativecommons.org/licenses/by/4.0/>。

As of 2026-08-24, contributor `xyh202131` licenses contributor-owned text, tables, diagrams, SVG source, PNG exports, editorial layout, package-authored JSON and conceptual GeoJSON transformations under **CC BY 4.0**. Attribution: `Twin-Track Jing-Zhang / 双轨京张, xyh202131, CC BY 4.0`. Full terms: <https://creativecommons.org/licenses/by/4.0/>.

投稿方自编的回放与离线交互代码采用 **MIT License**：Copyright (c) 2026 xyh202131。任何获得本软件及相关文档副本的人，可不受限制地使用、复制、修改、合并、发布、分发、再许可和/或销售，但所有副本或实质部分须保留上述版权和许可声明。本软件按现状提供，不作任何明示或默示担保；作者或版权持有人不对因本软件或其使用产生的索赔、损害或其他责任负责。

Contributor-authored replay and offline interaction code is under the **MIT License**. Copyright (c) 2026 xyh202131. Permission is granted, free of charge, to any person obtaining a copy of the Software and associated documentation to use, copy, modify, merge, publish, distribute, sublicense, and/or sell it, subject to including this copyright and permission notice in all copies or substantial portions. The Software is provided AS IS, without warranty; the authors or copyright holders shall not be liable for claims, damages or other liability arising from the Software or its use.

## 第三方与字体 / Third-party data and font

- `geometry/constraints.geojson` 含 OpenStreetMap 方向性背景，署名 `© OpenStreetMap contributors`，数据库许可为 **ODbL 1.0**：<https://opendatacommons.org/licenses/odbl/1-0/>。该层不进入 CC BY 授权；任何符合衍生数据库定义的再分发须保留署名与相同方式共享。它不是官方道路红线、铁路保护边界、市政线位、测绘或批准依据。
- 四份 PDF 的页眉、页题、说明和页脚在本地构建时使用 Noto Sans SC Regular/Bold 静态字面并确定性栅格化，修复 PyMuPDF CJK cmap 错配；PDF 不嵌入字体程序。Regular/Bold 源 SHA-256 分别为 `a2b93e6c2db05d6bbbf6f27d413ec73269735b7b679019c8a5aa9670ff0ffbf2` 与 `d1961be1161ea1be08496c920862d06ea5c23a757628f4fd69368de1d9f51bed`。四份离线 HTML 则通过 `visual/assets/offline-cjk-font.css` 共用一份 WOFF2 子集，避免干净 Linux Chromium 缺少 CJK 系统字体时出现方框；其源文件 `NotoSansSC-VF.ttf` SHA-256 为 `763146584cf0710223441356b4395e279021b0806c196614377a7a0174ae074a`，子集由 fontTools 4.62.1 对四份最终 HTML 的完整字符并集与声明审查符号生成，覆盖 1158 个 Unicode 码点，WOFF2 SHA-256 为 `311746a1703338c8828c2bcfab61232ed837214351f9f02d7fa562e321aa8f24`。三者均采用 **SIL Open Font License 1.1**：<https://openfontlicense.org/>；源字体不作为独立文件分发。
- Repository-provided provisional inputs, cited policy pages, cases, standards, trademarks, names and links are not relicensed. Their uses remain bounded by `sources.json` and `visual/assets/source-governance-register.json`.

## 逐路径自查 / File-by-file contributor inventory

`visual/assets/file-rights-inventory.json` 覆盖本次分发树的每个路径，并分别记录投稿方原创内容、投稿方代码、OSM 衍生数据库、仓库 provisional 输入、嵌入字体与仅引用外部来源的许可路径。该清单可以证明“每个文件都有明确处理决定”，但它仍是投稿方自查，不等同于独立法律意见、独立逐文件权利审计或商标检索。

`visual/assets/file-rights-inventory.json` covers every path in the current distribution tree and distinguishes contributor-authored content, contributor code, OSM-derived database content, repository provisional inputs, embedded font software and citation-only external sources. It proves that every file has an explicit handling decision, but remains a contributor inventory rather than independent legal advice, an independent file-level rights audit or a trademark search.

## 真实性与排除 / Authenticity and exclusions

- 本轮清退全部可选模型生成图像、视频、音频、海报、字幕和文字稿；最终包不以模型生成媒体冒充现场、居民意见、批准方案、无障碍结果或运营证据。
- 许可不把临时几何升级为官方红线，也不证明现场踏勘、规划批准、工程可行性、无障碍达标、现实服务效果、责任接受、G1 或专业签署。
- 独立法律意见、逐文件独立权利审计与商标检索仍未提供；许可声明不冒充上述专业结论。

- All optional model-generated imagery, video, audio, posters, captions and transcripts are removed. No generated medium is presented as field evidence, resident opinion, approved design, accessibility result or operational proof.
- These licences do not establish an official boundary, field survey, planning approval, engineering feasibility, accessibility compliance, real service result, accepted duty, G1 status or professional sign-off.
- Independent legal advice, independent file-level rights audit and trademark search remain absent; this notice does not claim those professional conclusions.
