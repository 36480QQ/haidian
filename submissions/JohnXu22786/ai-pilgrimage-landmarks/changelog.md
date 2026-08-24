# 方案迭代记录

## v0.2.0 - 2026-08-25

Round-2 repair (CocoSgt CHANGES_REQUESTED 75.0 -> 100.0):

- 双语映射修复：proposal.en.md 补齐 front matter（language=en, translation_of=proposal.md）；proposal.md 声明 bilingual_contract_version=1 + translation_file；manifest 补登记全部英文图件（5 张 .en.png 修正 language=en + translation_of）、A0/A3 英文 PDF、visual/index.en.html、report/proposal.en.html，并新增 mvp 节点图与 logo 图条目；英文正文改为提案全文实质翻译（中英实质等值已人工核对）。
- 缺字渲染修复：基于 C:/Windows/Fonts/NotoSansSC-VF.ttf 以 fontTools varLib.instancer 实例化 wght=400 静态字体，pyftsubset 按页面用字子集化，以 base64 @font-face（NotoSansSC-Static）嵌入 4 个 HTML（report/proposal.html、report/proposal.en.html、visual/index.html、visual/index.en.html），font-family 优先引用；A0/A3 PDF 与全部图件以同字体族重绘（pdf.fonttype=42 内嵌子集）。
- 来源登记：CASE-REF-01…07 与 HIST-REF-01…03 逐项登记 sources.json（发布方/机构页面 URL、发布与访问日期、复用边界、license），并更新正文引用与证据登记表；无法逐项核实的陈述标注待核实/待研究假设。
- 品牌在先权利与使用边界：新增「品牌与视觉识别（VI）方向（概念）」章节与 logo 资产；如实登记 智脉京张/JZ-PULSE、四座地标名、0∞ 图形 未完成在先权利检索（NAME-CLEAR-01），一律按内部工作代号处理，未经清权不对外采用或注册；assumptions.json 增补 A-BRAND-001。
- 证据/假设表：成本改为低/中/高定性分级（不发布具体金额），容量/寿命/维护/声光/无障碍与 go/no-go 逐项给出类型、依据或推导方法、适用标准、置信等级、复算触发。
- 图件统一声明：全部空间与指标图（中英文）显著标注「临时概念边界、非官方红线、官方数据发布后复算」，双语文例、图例、指北针与示意比例齐全；新增 原点场与轨道琴步道 MVP 节点级关系示意图（空间类型/入口与人流/人工替代点/无感离线区/敏感界面/待核验约束）。
- 细项修复：人才画像表述与 persona_count 一致；场景卡表头/测试协议表/年度活动表（与 metrics count 对齐）；区域协作矩阵引入三区两翼与五类区域对象表述；试点补充停止条件与退出/撤收机制；manifest data_confidence 改为 mixed_provisional_and_conceptual。
- 评分与门禁：score_rubric 100.0/100（reviewer_gaps 空、无拒绝）；四门禁（deterministic/spatial/visual/professional）全部 PASS；validate_local_submission PASS。

## v0.1.0 - 2026-08-24

- Initial assembly (concept package) for ai-pilgrimage-landmarks.
- Proposal drafted via OpenCode CLI (opencode), session oc-repair-3852-r2; edited for structure.
- Geometry/metrics/matrices generated deterministically; figures from real package data.
- Valroot gates run on 2026-08-24 (results persisted in self_check.json).
