# 版权、生成内容与公开边界说明

## 本包原创成果

`proposal.md`、结构化 JSON/GeoJSON 的方案表达、V13 分析图的自制版式、五张核心图、A3/A0 图册、离线 HTML、节点设计记录与自制图形由本项目的人类协作者与 AI agent 共同整理。工作流协作 agent 为 zcode、Codex、Ima；概念生成由 Fable、DeepSeek、Kimi3、Hunyuan3、OpusT5 共同完成；详细规划图与设计图由 Fable5、GPT-5.6 共同完成。

## AI 生成视觉

附件含 Tokai、Oskyi、GPT-image 等生成或编辑图。它们统一按“视觉意向 / 研究表达 / 非现状 / 非测绘 / 非法定方案”使用，不得描述为现场摄影、测绘成果、已建方案或政府批准方案。

逐资产或资产组盘点已经写入 `visual/assets/asset-rights-ledger.json`。AR-013 共登记 38 个生成或编辑组件；每项均保留工作流角色、批次或日期、输入权利、编辑记录、输出哈希、复用边界和证据强度。N02 白模/概念编辑系列另有 Oskyi、gpt-image-2、prompt、输入、输出和成品像素映射证据。其他组件没有精确 provider/run 的，不从目录名推断，明确保留为不可用字段。

## 第三方与公开资料

任务书、公告、规范和国际案例仅按 `sources.json` 引用。当前包没有识别到独立的街景或案例图片文件；AR-013 生成视觉谱系已按可用证据强度闭合。AR-010 的 Esri World Imagery 静态派生图依据 Esri Master License Agreement 及官方出版/展览引用指引使用，署名为 “Sources: Esri, Vantor, Earthstar Geographics, and the GIS User Community”。包内不发布原始瓦片、离线底图包或可独立复用的源图。工作名称和 Logo 方向的正式商标审查仅在未来公开品牌使用时触发。字体单列使用 Noto Sans SC 子集，并随包保留 SIL OFL 1.1 许可文本。代码依赖审计只发现 Node.js 内置模块，没有打包第三方代码库。

## AI Review Layer 权利台账

机器评审专用记录分为三份：`asset-rights-ledger.json` 负责来源、创作者角色、许可、工具、变换和哈希；`asset-clearance-disposition.json` 负责公开处置；`brand-model-provenance.json` 负责品牌、模型与现有 run 证据。公开处置使用 `cleared_with_evidence`、`replaced_with_cleared_asset`、`excluded_from_public_package` 和 `unresolved_pending_permission_or_replacement`；未知项不会写成已清权。

本次评审包已完成资产盘点、AR-013 逐组件谱系、最终署名核对和 AR-010 静态出版许可核验。AR-010 的清权仅适用于本次参与者 PR 与非商业社区评审中的带署名静态派生图，不扩展到原始瓦片、离线底图包、自托管、商用、独立源图复用、再许可或服务商背书。未知 provider/run 不作推断；维护者复评与更广范围的发布决定仍独立进行。

## 提交许可

本包当前 manifest 使用 `COMMUNITY-DISPLAY-ONLY`。该许可只覆盖本项目有权处分的文字、结构、数据整理与自制视觉，不替代第三方权利人的授权。任何公开发布、商业使用、再许可或衍生传播都需按来源逐项核验。

## 合规声明

方案不使用秘密地图、非公开政府数据、企业内部数据或个人隐私；不虚构官方背书、资金承诺、审批状态或实施结果。涉及权属、控规、工程、交通、水务、文保、消防、无障碍与公共安全的内容均为待专业团队深化的概念建议。
