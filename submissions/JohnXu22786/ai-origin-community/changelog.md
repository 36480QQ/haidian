# 方案迭代记录

## v1.2 - 2026-08-25

- Round-3 repair (CocoSgt round-2 CHANGES_REQUESTED 66.0/100) — closed the 5 review items:
  1. 范围命名与嵌套改为官方公告口径（统筹研究范围约43.6km2—总体设计范围约11.4km2—重点区域约368.4公顷），本包自定义研究子范围约1.1km2 改称"本包子范围"并明确位于总体设计范围之内；proposal.md/en、compliance_matrix.json（1.4.1/1.4.2/1.4.3）、sources.json 对照说明、assumptions.json（新增 A-SCOPE-001）、全部图件、中英 HTML 与 PDF 的 11.4/1.1/43.6/368.4 表述统一为该嵌套口径；正文指标分母一律注明"总体设计范围（provisional）"。
  2. 全部图件按可读性标准重绘（1800×1200px，标题≥20pt，标注≥12pt）：逐张自检 ink 墨量（地图≥0.08、图表≥0.10，全部达标，数值见评审报告表）；英文图 100% 英文标注；site-overview 含真实用地分区、三重点区、本包子范围、示意街道（知春路/学院路/京张遗址公园活力带）、指北针、比例尺、NOT-TO-SCALE 与 PROVISIONAL 戳记；metrics-evidence 分开比例%与整数计数双图，逐指标标注来源/公式/置信度/适用范围并按 20.6% 式展示。
  3. 中英 HTML（report/proposal.html、proposal.en.html、visual/index.html、index.en.html）在最终渲染后以 fontTools 将 NotoSansSC-VF 实例化为 wght=400 静态字并逐文件子集化（zh 子集约 281KB / en 子集约 18-23KB），base64 注入 @font-face 'NotoSansSC-Static' 并追加 body/h1-h6/table/td/th/li/p/span/div 字体覆盖规则；校验 data URI 以 AAEAAA（sfnt）开头且文件仍可解析为 HTML。渲染器级字形支持仍取决于评审环境（如实说明）。
  4. 15 项更新项目成本由无依据的人民币区间改为定性等级（低/中/高）并补齐列：估算方法（同类项目单价类比）、价格基期（2025年北京市价格水平·概念）、包含范围（设计+建安工程，不含运营维护/税费/土地）、置信等级（低·待专业校核）、复算触发条件（立项估算与限额设计完成后）；不再保留任何无推导的金额。
  5. 中英 A0 展板（2页，首页标题 60pt、含总览图/指标面板/机制图/复算戳记/页码）与 A3 文册（7页，正文≥14pt、封面标题无裁切、逐页页码）全部重排重导；用地结构按机器复算更新为 7 类（34.9/18.3/14.7/11.2/7.9/6.8/6.2%）。
- 中英实质等值已由参与方人工核对（声明式）；确定性、空间、视觉、专业四门禁复跑全部 PASS；hardened scorer weighted_pct=100.0、reviewer_gaps 空、无强制拒绝；validate_local_submission PASS。
- 复查修正（同轮次内）：15项成本表补充"复算触发条件"列（统一为立项估算与限额设计完成后复算）；用地结构占比注明与图件同一机器复算管线（类别面积占概念几何内用地合计比例，四舍五入合计约100%）；A0/A3 中英 PDF 全面消除越界裁切（PyMuPDF 逐字span检查 overflow=0）、A3 表格字号升至14pt、封面标题换行不裁切、EN 标题与英文正文front matter一致（AI Origin Community…in Beijing）；visual 两页清除 NotoSansSC-Embedded 残留并把 svg text 纳入嵌入字体覆盖；changelog v1.1 历史口径加指针说明；metrics.json 数值未改动（含既有 land_use_zone_count=21 与土地分类要素数 24 的口径差，属 pre-existing、随官方数据发布后一并复算，已知但未变更数据）。

## v1.1 - 2026-08-25

- Reviewer (CocoSgt 2026-08-24) CHANGES_REQUESTED repair round: closed all 11 hardened-scorer gaps and the 9 mandatory next steps.
- Fixed XX placeholders to unknown + estimation method + required data + recalculation trigger; unified persona count (6类人才画像 = metrics.json persona_count=6) with two 6-row persona/journey tables.
- Added 7-row sourced global case table (Station F / One-North / Toronto Quayside / King's Cross / 22@ / Cyberport / Zhangjiang) with publisher-level citations in sources.json (7 case entries); added per-asset rights ledger (font/logo/figures/geometry/HTML-PDF/code/generation tool/policy snapshots, 8 entries, license+attribution+restrictions), COMMUNITY-DISPLAY-ONLY scope stated.
- Expanded content to 21 sections: 三区两翼与区域协同回路（北纬社区/未来科学城/怀柔科学城/经开区/京津冀，建议性机制+机制图）、品牌与视觉识别（AI Origin Community 原点公社、命名体系、原创概念Logo、VI规则、中英传播文案）、全球案例对标与产业要素保障、10张场景卡+场景-空间-运营矩阵+TRL估算、3份产业测试验证协议+场景开放运营、公共空间地标与组件库深化、历史文化叙事与导视系统、年度活动品牌体系（5项）+开发者社区+人才转化、无障碍与包容设计（六类服务人群旅程+概念验收清单）。
- Regenerated all figures (legend/north arrow/scale/NOT-TO-SCALE/PROVISIONAL stamps; metrics split into ratio % and integer count panels), added mechanism diagram and neutral logo asset; regenerated A0 (real 1189x841mm, dense single board) and A3 (real 420x297mm, 7 pages) PDFs with headers/footers/page numbers/provisional notes.
- Full bilingual v2 contract: proposal.en.md complete translation; 6 English figures; English A0/A3 PDFs; visual/index.en.html; report/proposal.en.html via renderer; manifest maps every counterpart (language en + translation_of).
- Chinese-box fix: OFL-1.1 Noto Sans SC subset (fontTools) base64-embedded with @font-face into report/proposal.html, report/proposal.en.html, visual/index.html, visual/index.en.html (recorded as ASSET-FONT-NOTOSANSSC-OFL in sources.json).
- Unified provisional scope vocabulary (统筹研究范围约11.4km² / 总体设计范围约1.1km² / 重点区域约368公顷概念口径) with recalculation triggers; rounded all human-facing numbers. 【该 v1.1 旧口径已在 v1.2 条目中按官方公告修正为：统筹约43.6km²／总体约11.4km²／重点区域约368.4公顷／本包子范围约1.1km²（位于总体设计范围之内），本行仅作历史记录】
- Valroot gates + scorer re-run on 2026-08-25 (all four gates PASS, weighted_pct 100.0, reviewer_gaps empty).

## v0.1.0 - 2026-08-24

- Initial assembly (concept package) for ai-origin-community.
- Proposal drafted via OpenCode CLI (opencode), session ses_fccc7fe77ffeLlXpKBXz2Wm0ad; edited for structure.
- Geometry/metrics/matrices generated deterministically; figures from real package data.
- Valroot gates run on 2026-08-24 (results persisted in self_check.json).
