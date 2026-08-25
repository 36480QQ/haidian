# 方案迭代记录

## v0.1.0 - 2026-08-24

- Initial assembly (concept package) for shangdi-lowaltitude-workplace.
- Proposal drafted via OpenCode CLI (opencode), session oc-repair-3854; edited for structure.
- Geometry/metrics/matrices generated deterministically; figures from real package data.
- Valroot gates run on 2026-08-24 (results persisted in self_check.json).

## v0.2.0 - 2026-08-25 (repair round-3, CocoSgt PR #3854)

- P0 字体与渲染：全部 HTML（proposal/visual 中英 4 页）嵌入 Noto Sans SC（OFL-1.1）子集（varLib instancer wght=400 → pyftsubset 实际字形 → base64 @font-face，1098 字形、376.5 KiB）；图件/PDF 均使用 Noto Sans SC 静态实例（400/700），未使用未清权字体；copyright_statement.md 建立逐项权利台账。
- P0 双语交付：补齐 5 张 .en.png、A0/A3 .en.pdf、report/proposal.en.html、visual/index.en.html；proposal.en.md 重写为完整英文译文（front matter language=en、translation_of=proposal.md；proposal.md 增加 bilingual_contract_version=1、translation_file=proposal.en.md）；manifest 逐项登记 language/translation_of。
- P1 任务书成果补齐：表三全球七案例对照（逐案登记 sources.json 并附来源列）、生态图谱、公共空间组件库 8 项表、京张文化资源清单与导视叙事 6 项表、荣誉展示体系 5 项表、年度活动品牌 5 项表、开发者社区/场景开放/国际传播/转化路径四节。
- P1 来源与权利闭环：sources.json 扩至 22 条（北京低空行动方案、暂行条例、GB 42590-2023、京张遗址公园设计方案与解读、沿线街区控规公示、七案例、自产几何等，逐条含来源机构/URL/日期/复用边界）；商标在先权利条款按内部工作代号诚实声明。
- P1 实施证据校正：更新项目表扩至 21 行（设施类 8 项逐项列全）；通勤接驳技术类型与监管路径概念限定；净空 180—260 米、隔离 3/5 米、风速 6/8 米/秒、30 天/1000 架次退出条件、事故/投诉阈值与 KPI 均改为运行阈值表（含口径与推导依据、待专业评估事项、复算触发）；投资金额改为低/中/高投资档位+估算口径。
- 表达完整度：图件全部重绘（12×8 @150dpi，ink 覆盖：地图/图表分别 ≥0.08/≥0.10：site-overview≈0.22、key-areas≈0.45、mobility≈0.21、land-use≈0.57、metrics≈0.27），每图含双语 provisional 戳与图例；A0 首页标题 60pt、第二版式密集填充；A3 封面加色带；精度降水：正文以 11.41 平方公里/1141 万平方米/≈0.329/≈0.007 展示。
- 一致性：sources/assumptions/compliance_matrix/standard_matrix/design_depth_matrix 全文更新（source_id 去年份后缀、evidence_summary 逐条改写为指向具体正文内容）；metrics.json 修正 land_use_zone_count=21；manifest data_confidence 改为 mixed_provisional_and_conceptual。
- Valroot 门禁 2026-08-25 重新运行（结果持久化于 self_check.json）。

## v0.3.0 - 2026-08-25 (repair round-4, CocoSgt PR #3854 74.0/100)

- P0 图面质量（表达完整度 2/5 → 修复）：5 对图件全部重绘并程序化质检。布局改为显式分栏（地图 + 独立文本面板），以 PIL 实测字形宽度换行、以 vstep/px 数据坐标排布，生成后逐图校验：①6px 边缘带 ink=0（无裁切/越界）；②文字 AABB 两两无重叠（0 重叠）；③无文本出画布；④中部无大段空白带（主图不空）；⑤ink 覆盖 site-overview≈0.131 / land-use≈0.193 / key-areas≈0.132 / mobility≈0.124 / metrics≈0.210（地图≥0.08、图表≥0.10）；规格 12×8in @150dpi，标题 20pt、标签/图例 ≥13pt、注释 ≥11pt。修复点对照：site-overview 图例与指标不再共区（独立图例列 + 三层范围 + 复算指标），右侧无越界；land-use 左右轴标签不再裁切（barh 纵向标签 + 图例按列换行）；key-areas 主图填满左栏（三重点区 + 净空走廊 + 图例条），任务卡右侧不再截断（缩短文案 + 收缩行距）；mobility 说明与图例换行不出界；metrics-evidence 无空白带，三类指标分轴（计数/面积/比率不共轴），三项 formal 指标口径表 + 数据来源注脚。
- P0 双语实质等效：5 对图件全部重绘 EN 版本，生成时断言 100% ASCII（零中文残留：图例/节点说明/底部警示/指标标签均已英文，含原“计数指标”残留）；A0/A3 英文板全部重排且全页文本抽取校验：除强制双语 PROVISIONAL 戳外无任一中文行（0 条非戳中文）；中英数值、图位、图例条目一一对应（同一 labels.py 词表驱动）。
- P1 A0/A3 板册重导出：a0-boards 2 页（首页总览 64pt 标题 + 二层节点任务板）、a3-booklet 6 页（封面 + 5 内容页），均复用质检通过的图件布局（FS 字体缩放）；PDF 逐页栅格化校验：4 份 PDF 全部页面边缘带 ink=0、首页含双语戳、EN 页无中文（除强制戳）；A0 首页标题 64pt≥60pt，A3 首页标题 40pt 未裁切。
- P1 数字与口径一致性：图件全部数值与 metrics.json/proposal.md 逐项核对（site≈1141万 m²、green≈0.329、public≈0.007、计数 3/21/12/13/7/5 等）；全套 doc 链（figures→HTML→manifest）保持同径。
- 机器一致性：render_proposal_html.py 重出 report HTML（13 个规范 ## 标题保持）；4 个 HTML 表面重嵌 OFL Noto Sans SC 子集（family NotoSansSC-Static、font-family-first override、单份 data URI）；manifest 40 项 hash 刷新；新增文档集未变（figures 10 + logo 1 + PDF 4 + HTML 4 + md 2）。
- Valroot 门禁 2026-08-25 四门重新运行（self_check.json 持久化）。