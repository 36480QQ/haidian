# Copyright, Licence and Media Statement / 版权、许可与媒体声明

本提交包中的方案文字、图形构图、Logo、图件、HTML 页面、PDF 排版、机器数据组织与概念空间原型由本次智能体工作流原创生成，并由 GitHub 账号 `ustcsxl` 的持有人在提交前复核。除 `sources.json` 中列出的公开事实、政策、标准名称与仓库内清权任务材料外，没有复制第三方图像、Logo、地图瓦片、人物肖像、音乐或视频。

所有外部案例只作事实比较和设计推理背景；本包不再分发其媒体、数据集或受版权保护的版式。空间图件使用仓库提供的 provisional geometry 和本包原创设计几何，没有使用外部底图截图。字体由运行环境用于渲染，不随提交包分发。

The proposal text, graphic composition, logo, figures, offline pages, PDF layout, machine-readable organisation and conceptual spatial prototypes were generated for this submission. External cases are used only as factual references listed in `sources.json`; no third-party images, logos, map tiles, portraits, music or video are redistributed. The submission does not imply endorsement, approval, partnership or procurement by any cited institution.

Suggested repository licence field: `COMMUNITY-DISPLAY-ONLY`, subject to the upstream call rules and the account owner's final review.


## v1.4 中文离线可读性与字体许可

- 构建期字体：Noto Sans CJK SC Regular/Bold，来自 Noto CJK 项目；许可为 SIL Open Font License 1.1。
- 投稿包不包含、复制或分发任何 `.ttf`、`.ttc`、`.otf`、`.woff` 或 `.woff2` 字体文件。
- `report/proposal.html` 与 `visual/index.html` 的可见中文由构建脚本把所需字形转换为 SVG 路径轮廓；这些路径不依赖审查机器的系统字体或网络字体。
- 同位透明语义层保留标题、正文、表格、脚注、证据标签和视觉复核关键词，支持浏览器查找、复制、辅助技术及机器检查；它不是可见内容的替代，而是与可见矢量字形一一对应。
- 构建方法只输出当前成果所需字形轮廓，不输出完整字体、字符映射表或可还原字体文件。
- 来源登记见 `sources.json` 的 `NOTO-CJK-OFL`；构建机的 Debian `fonts-noto-cjk` 版权记录指向 Noto CJK 上游并载明 OFL 许可。
