# 版权、生成内容与公开边界说明

## 本包原创成果

`proposal.md`、结构化 JSON/GeoJSON 的方案表达、V13 分析图的自制版式、五张核心图、A3/A0 图册、离线 HTML、节点设计记录与自制图形由本项目的人类协作者与 AI agent 共同整理。工作流协作 agent 为 zcode、Codex、Ima；概念生成由 Fable、DeepSeek、Kimi3、Hunyuan3、OpusT5 共同完成；详细规划图与设计图由 Fable5、GPT-5.6 共同完成。

## AI 生成视觉

附件含 Tokai、Oskyi、GPT-image 等生成或编辑图。它们统一按“视觉意向 / 研究表达 / 非现状 / 非测绘 / 非法定方案”使用，不得描述为现场摄影、测绘成果、已建方案或政府批准方案。

逐资产或资产组盘点已经写入 `visual/assets/asset-rights-ledger.json`。盘点确认：部分节点档案有 provider、model、prompt、run manifest、hash 和 approval，但这些记录尚不能逐一映射到本包图像；对应 V13 源集审计识别的 36 个生成图候选块中，逐块明确 provider provenance 为 0。Tokai、Oskyi、GPT-image 只按现有证据强度记录，缺失的 provider、model、batch、run、源图哈希或成品映射均保留为 `unknown` 或 `null`。

## 第三方与公开资料

任务书、公告、规范和国际案例仅按 `sources.json` 引用。当前包没有识别到独立的街景或案例图片文件，但 V13、核心图、PDF 和封面仍含来源未闭环的卫星/地图与生成视觉组件；工作名称和 Logo 方向也未完成商标与国际语义审查。字体单列使用 Noto Sans SC 子集，并随包保留 SIL OFL 1.1 许可文本。代码依赖审计只发现 Node.js 内置模块，没有打包第三方代码库。

## AI Review Layer 权利台账

机器评审专用记录分为三份：`asset-rights-ledger.json` 负责来源、创作者角色、许可、工具、变换和哈希；`asset-clearance-disposition.json` 负责公开处置；`brand-model-provenance.json` 负责品牌、模型与现有 run 证据。公开处置只使用 `cleared_with_evidence`、`replaced_with_cleared_asset`、`excluded_from_public_package` 三种值，未知项不会写成已清权。

当前按资产组统计仍有 8 组未清权内容物理存在于评审包，包括 V13、核心图、英文核心图、Logo 方向、四份 PDF、封面，以及其中的地图/卫星和生成视觉组件。它们统一标为 `excluded_from_public_package`；这里的“排除”是包级发布禁令，并不谎称文件已从本次评审包删除。因此当前总包仍为 `do_not_publish`，只能用于受限评审，不能据此制作公开发布包。

## 提交许可

本包当前 manifest 使用 `COMMUNITY-DISPLAY-ONLY`。该许可只覆盖本项目有权处分的文字、结构、数据整理与自制视觉，不替代第三方权利人的授权。任何公开发布、商业使用、再许可或衍生传播都需按来源逐项核验。

## 合规声明

方案不使用秘密地图、非公开政府数据、企业内部数据或个人隐私；不虚构官方背书、资金承诺、审批状态或实施结果。涉及权属、控规、工程、交通、水务、文保、消防、无障碍与公共安全的内容均为待专业团队深化的概念建议。
