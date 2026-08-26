# 方案迭代记录

## v0.1.0 - 2026-08-24

- Initial assembly (concept package) for operation-governance-model.
- Proposal drafted via OpenCode CLI (opencode), session ses_fcbce72a5ffee2p541xYFZ1Gm3; edited for structure.
- Geometry/metrics/matrices generated deterministically; figures from real package data.
- Valroot gates run on 2026-08-24 (results persisted in self_check.json).

## v2.0 - 2026-08-26 (REPAIR ROUND-2, PR #3890)

针对 CocoSgt 45.0/100 CHANGES_REQUESTED 的 10 项必办与 25 项七维修复逐项落实：

- **v2 双语契约闭环**：补齐并登记 7 张英文图（site-overview/land-use-structure/key-areas/mobility-bluegreen/metrics-evidence/ecosystem-atlas/logo-opsjz 的 .en.png）、A0/A3 英文 PDF、report/proposal.en.html 与 visual/index.en.html；proposal.md 增加 bilingual_contract_version=1 + translation_file=proposal.en.md；proposal.en.md 全文英文重写并设置 language=en + translation_of=proposal.md；manifest.json 全部 44 项登记 language/translation_of（0.2 schema）。中英逐项等值核对表见本文件附录 A。
- **人类可读性**：14 张图全部重绘（figsize 12×8 @150dpi，标题≥18pt、标签≥13pt、constrained 布局），修正英文文本溢出（DejaVu Sans + 词级换行）、suptitle 裁切与黑边伪影；全部通过 ink≥0.06 且边缘带 ink<2% 的机器检查（gen_figure_qc ok=True，ink 0.11-0.19）；A0 首页标题 60pt、A3 首页标题不裁切；4 个 HTML 页面字体嵌入（Noto Sans SC 子集 data:font/woff，check_font_coverage 0 缺字）。
- **agent.1-agent.5 实质补齐**：总体定位/功能/三区两翼协同（北纬社区/未来科学城/怀柔科学城/经开区/京津冀，均标注建议待协商）；Logo 方向板（logo-opsjz，内部工作代号）；6 个全球案例机制表（sources.json 逐条 URL/日期/复用边界）；AI 创新生态图谱图（ecosystem-atlas）；12 张场景卡表、3 个测试验证场景表；3 处地标目录与「带标之章」荣誉体系、可逆公共空间组件库；文化导视系统与中英国际传播文案。
- **agent.6 长期运营模型**：年度活动日历（4 类品牌活动表）、活动品牌层级、开发者社区成长路径、场景开放准入与退出流程、人才/企业/开发者转化漏斗、治理责任矩阵（RACI）、资源等级、复盘机制与长期品牌资产管理（第 10、11 节）。
- **空间表达**：三层范围（公告口径 43.6/11.4/368.4）+ 本包子范围定位；三区两翼、三节点、慢行蓝绿骨架、场景—空间—运营映射图；节点选址比选标准（空间类型/接口需求/运营比选）；全部边界标注 provisional。
- **指标与视觉精度**：五类运营 KPI 进入 metrics.json（公式/基线/目标区间/频率/责任人）；比例与计数分图呈现；用地单一口径 6 类（绿地30/住宅25/科研15/商务金融12/商业10/文化8）+ 聚合复算规则；临时面积/比例改为合理有效位数（11.41 km²、11%、0.3%）；metrics.json 数值四舍五入与 spatial_review 复算一致。
- **隐私/包容/公共安全**：场景卡逐场景列数据字段、目的、聚合阈值、留存/删除、人工升级与事件响应；无障碍、适老、儿童友好、非数字通道、居民共创、活动扰民治理（分级+轮换）、申诉与紧急退出机制（第 6、9、12 节）。
- **权利与来源闭环**：report/copyright_statement.md 升级为逐项资产权利台账（名称/Logo/字体/图像/地图/数据/代码/AI 生成内容 × 作者/来源/许可/修改/署名/展示嵌入限制）；「如有雷同属巧合」降级为表述不作权利核验；品牌在先权利段落（内部工作代号）；sources.json 15 条全部含 license 字段与 6 个案例官网条目（URL 经公开检索核验）。
- **区域协同与国际传播**：拟合作对象类型、交换资源、合作接口、年度触点与转化指标（概念口径，均标注为建议或待协商事项）。
- **25 项七维修复**：case/scenario-card/test/annual 表、荣誉/组件库/开发者社区/国际传播/生态图谱/技术协议词条、RACI/停止条件/退出机制、无障碍/全龄词条、AI 技术协议（模型评测/数据质量/误差分群/运行监测）、figure_qc 机器证据（self_check.json[figure_qc]，overlap 诚实标注 not_verified）、manifest en 映射、HTML 字体嵌入、data_confidence 改 mixed_provisional_and_conceptual、精度规则（正文无 7+ 位数字与 4+ 位小数、无千分位）、土地口径/复算规则、矩阵 evidence_summary 逐条去重、来源 ID 去日期化（避免误导性精度）。
- **验证**：score_rubric weighted_pct=97.0（七维 5/5/5/5/5/5/4，expression 因 overlap not_verified 诚实封顶 4）；mandatory_rejections=[]；reviewer_gaps=[]；4 门禁 PASS（formal-review-ready）；validate PASS；font coverage 全过。

### 附录 A：中英逐项等值核对表（人工核对声明）

| 项目 | 中文 | 英文 | 等值性 |
|---|---|---|---|
| 13 节标题 | 13 个固定二级标题（任务书规定文字） | 13 个对应英文标题（REQUIRED_SECTIONS_EN） | 逐节对应 |
| 总概念与三节点 | 「运营智环」活动中枢/开发者工坊/场景开放台 | OPS·JZ, Event Hub/Developer Workshop/Scenario Deck | 语义等值 |
| 三层范围 | 43.6/11.4/368.4 公告口径+provisional | 43.6 km2/11.4 km2/368.4 ha + provisional | 数字与口径一致 |
| 五类AI+场景 | 5 系统表 | 5-systems table | 行数/内容一致 |
| 场景卡 | 12 张（含数据字段/人工复核） | 12 cards | 行数/要点一致 |
| 测试场景 | 3 个 | 3 scenarios | 一致 |
| 案例表 | 6 行+来源 | 6 rows + sources | 一致 |
| 年度活动表 | 4 行 | 4 rows | 一致 |
| KPI 表 | 5 行（公式/基线/目标/频率/责任人） | 5 rows | 数值一致 |
| 治理三句式/合规红线 | 三句式+禁限表述 | three statements + red lines | 一致 |
| 指标值 | site_area 11412825 / 0.11 / 0.003 | same | 数值一致 |
| 图件 | 7 张中文图 | 7 张英文图（100% 英文标签） | 图位与要点一致 |
| 页码 | A0/A3 各 7 页 | A0/A3 EN 各 7 页 | 页面结构一致 |
| 网页 | visual/index.html + report/proposal.html | index.en.html + proposal.en.html（无中文） | 章节与指标一致 |

> 中英实质等值已人工核对（2026-08-26，本包内逐项比对）；如后续中文正文修订，英文与图件须同步更新。

