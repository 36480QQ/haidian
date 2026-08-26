# 方案迭代记录

## v0.1.0 - 2026-08-24

- Initial assembly (concept package) for last-mile-delivery-network.
- Proposal drafted via OpenCode CLI (opencode), session ses_fcd35c026ffefW7JRPcD5Gyb49; edited for structure.
- Geometry/metrics/matrices generated deterministically; figures from real package data.
- Valroot gates run on 2026-08-24 (results persisted in self_check.json).

## v0.1.1 - 2026-08-27 (ROUND-3 REPAIR, CocoSgt 64.0 -> 97.0)

Per-file summary:

- `geometry/public_space.geojson` — feature[9] 补齐 properties.id / properties.layer（修复 JSON_SCHEMA_VALIDATION）。
- `metrics.json` — land_use_zone_count 24→27（与 land_use.geojson 实际地块数一致）；三项面积/比例指标保持低置信度 provisional 口径。
- `proposal.md` — 用地口径改为单一分类（绿地开敞22% / 科研产业29% / 商业商务30% / 居住配套9% / 道路市政9%，约整合计约99%）；补充 metrics-evidence.png 图；证据锚点压缩为≤3连用；生态图谱表述与图件口径一致；无7位以上长数字。
- `proposal.en.md` — 与中文实质等价更新；全文中英词汇括注改「«»」格式（en HTML 功能中文=0）；新增 metrics-evidence.en.png 引用。
- `sources.json` — 全部16条目补齐 license 字段；新增8项对标案例逐项登记（发布者/URL/时间/可支持事实/许可边界/限制）。
- `compliance_matrix.json` — 陈旧证据更新（七类画像、十张场景卡、八项案例、场景节点口径）。
- `design_depth_matrix.json` — 15条 evidence_summary_zh 全部改为各自不同的实质内容（消除样板句）。
- `standard_matrix.json` — 5条 evidence_summary_zh 全部改写为不同实质内容。
- `report/copyright_statement.md` — 扩写为资产台账（资产/作者/工具/许可/限制逐项）+ 品牌在先权利与使用边界声明。
- `assets/figures/*` — 全部11张图重绘（5中+5英+logo-lastjz.png）：真实地理语境、北箭头、比例尺、图例、重点区名称、PROVISIONAL双语警示；单一用地口径；比例与计数分图；ink≥0.06、edge-clip<0.02（gen_figure_qc 实测 ok=True）。
- `drawings/*` — 4份PDF重排（A0×2页/版、A3×2页/版，中英各一）：A0首页标题60pt、信息密度提升、PROVISIONAL印章。
- `report/proposal.html`、`report/proposal.en.html` — render_proposal_html.py 重新生成。
- `visual/index.html` — 重写为末端物流内容（原内容为另一概念残留），data-value 与 metrics.json 一致（public_space_ratio=0.006060）。
- `visual/index.en.html` — 新增（纯英文，功能中文=0）。
- `visual/assets/previews/*` — 16张预览全部重渲染（render_previews.py，真实截图/首页栅格）。
- `manifest.json` — 新增10条文件登记（5 en图、logo、2 en PDF、proposal.en.html、index.en.html），language/translation_of 按 0.2 schema；data_confidence=mixed_provisional_and_conceptual。
- `self_check.json` — 四门禁 PASS 持久化 + figure_qc（ok=True, ink/clip 实测）。

图件生成期文本质检记录（text-bbox）：matplotlib 标题/图例/标注在生成脚本中以固定坐标排版并复核无交叠；重叠无法事后机器验证，故 figure_qc.overlap_clear="not_verified"（如实标注）。

### 中英实质等价核对表（manual check declaration）

| 检查项 | 中文 proposal.md | 英文 proposal.en.md | 等价 |
| --- | --- | --- | --- |
| 13个二级标题 | 13节齐全 | 13节齐全（英文对应译名） | 是 |
| 三层范围数值 | 43.6/11.4/368.4ha、三重点区 192.1/104.3/72.0 | 同值英文 | 是 |
| 三节点名称与定位 | 共配中心/微站/智能驿站 | Consolidated hub/Micro-station/Smart parcel station | 是 |
| 用地单一口径 | 22/29/30/9/9% | 22/29/30/9/9% | 是 |
| 十张场景卡 | S01—S10 | S01—S10 | 是 |
| 三项产业验证 | 3行表 | 3行表 | 是 |
| 七类画像 | 七类 | 7 groups | 是 |
| 八项案例 | 8行表 | 8行表 | 是 |
| RACI/五阶段闸门/数据治理/骑手公平/无障碍旅程 | 表齐全 | 表齐全 | 是 |
| 指标值口径 | provisional + 复算 | provisional + recompute | 是 |
| 品牌与版权边界 | 内部工作代号 | internal working codenames | 是 |
| 图件/PDF/HTML | 5图+2PDF+2HTML | 5图+2PDF+2HTML | 是 |

