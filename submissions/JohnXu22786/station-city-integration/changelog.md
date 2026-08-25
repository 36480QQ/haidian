# 方案迭代记录

## v1.1.0 (round-1 repair) - 2026-08-26

针对评审（50.0 CHANGES_REQUESTED）逐项修复：

- proposal.md：13节扩充重写；新增三区两翼协同矩阵、六大全球案例表、12张场景卡、3个产业测试场景协议、场景—空间—运营矩阵、五类人才画像表、年度活动品牌表、指标元数据表、成本定性分级说明、地标目录、荣誉展示系统、八类公共空间组件库、三级导视、京张—中关村—AI文化叙事、开发者社区、准入退出与停止条件、牵头/协作分工、国际传播文案、转化路径与年度评估指标；"600米核心圈高强度混合开发""可直接转化为管控指标与出让条件"等口径改写为待正式控规与专业审查后深化的概念建议；删除精确到多位小数的provisional显示；品牌在先权利与许可边界如实披露。
- proposal.en.md：由占位摘要改写为与中文实质等值的完整英文提案（13个英文章节、全部表格与图件引用），起metadata language=en、translation_of=proposal.md；proposal.md 增加 bilingual_contract_version=1 与 translation_file。
- 图件：9组×中英文共18张（含Logo方向、区域创新协同图、总体空间结构图、AI创新生态图谱），统一 figsize(12,8.2)@150dpi、标题≥20pt、图例/标注≥11pt、每图双语provisional戳记、地图含指北针与比例尺、比例与计数分轴；来源ID去除日期数字避免伪精度；机器QC（ink/clip）通过，结果写入 assets/figure_qc.json（文本重叠 not_verified）。
- 图纸：drawings 增加 a0-boards.en.pdf、a3-booklet.en.pdf，A0首页大标题≥60pt、A3与A0首页排版防裁切。
- 可视化与报告：visual/index.html 重写为与提案一致的站城融环内容并补齐14个必需标记；新增 visual/index.en.html；report/proposal.html 与 report/proposal.en.html 由 render_proposal_html.py 重新生成；四个页面均内嵌 NotoSansSC-Static 子集字体（@font-face data URI，face 优先）。
- 数据与元数据：sources.json 增至15条（含6个全球案例条目，均含发布方、URL、日期与许可边界，全部条目补 license 字段）；metrics.json global_case_count 4→6 与正文表格一致；compliance_matrix 23条 evidence_summary_zh 逐条改为指向实际内容的差异化表述；manifest schema 0.2.0 补齐全部新文件与 en 映射（language/translation_of），data_confidence 改为 mixed_provisional_and_conceptual 并新增 report/asset_rights_ledger.md。
- 校验：score_rubric、四道门禁（确定性/空间/视觉/专业证据）与 validate_local_submission 重跑通过；中英文实质等值已人工核对，品牌在先权利检索未完成前按内部工作代号处理，图件 ink 与剪裁检查结果见 assets/figure_qc.json。

## v0.1.0 - 2026-08-24

- Initial assembly (concept package) for station-city-integration.
- Proposal drafted via OpenCode CLI (opencode), session ses_fcc08d452ffe3e9VvuuOXF93dC; edited for structure.
- Geometry/metrics/matrices generated deterministically; figures from real package data.
- Valroot gates run on 2026-08-24 (results persisted in self_check.json).
