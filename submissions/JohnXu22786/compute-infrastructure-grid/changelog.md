# 方案迭代记录

## v1.1 - 2026-08-25（评审返修）

- **双语合同补齐（V2）**：proposal.md 声明 bilingual_contract_version="1" 与 translation_file=proposal.en.md；proposal.en.md 提供完整英文译文并声明 language/translation_of；补齐五张英文图（*.en.png）、英文 A0/A3 图纸（a0-boards.en.pdf / a3-booklet.en.pdf）、英文 proposal HTML（report/proposal.en.html）与英文 visual HTML（visual/index.en.html）。
- **HTML 中文字体修复**：report/proposal.html 与 visual/index.html（及英文版）以 Noto Sans SC（SIL OFL 1.1）静态字体子集嵌入（base64 woff2，font-family-first），修复中文方框字；补标题、表格、图例、替代文本与键盘访问（skip-link、:focus-visible）。
- **agent.1—agent.6 实质成果**：新增「品牌识别与视觉规范（Logo/VI）」节与 logo-cmpjz.png；全球案例表扩至 8 行（含来源列）并逐案登记 sources.json；场景卡表 10 张；产业测试验证场景 3 个（测试对象/数据输入/验证指标/退出条件）；地标目录、荣誉展示与体验组件库；文化叙事、三级导视系统与国际传播文案；年度活动品牌表、开发者社区、场景开放与招引转化机制。
- **核心图件重做**：五张中文图 + 五张英文图全部重做（墨水占比 ≥8—10%），补场地语境底图、图例、比例尺、指北针与概念环网连接关系；用地比例与计数分轴图表；provisional 数值低精度显示并保留醒目警告；修复用地标签重叠与 A0 首页留白问题。
- **计数对齐**：proposal.md、metrics.json、compliance_matrix.json 与 visual/index.html 统一 persona_count=6、scenario_card_count=10、industry_test_scenario_count=3、annual_program_count=3、global_case_count=8。
- **实施与长期运营**：新增「实施与长期运营矩阵」节（三节点前置条件/最小试点/责任主体/合作接口/阶段闸门/KPI框架/维护机制/公众反馈/退出恢复），责任主体具体化；manifest data_confidence 修正为 medium 并登记理由。
- **包容性与无障碍**：新增「包容性、无障碍与社区共同设计」节（全龄友好、无障碍人工审核声明、噪声与热影响标准、社区共同设计机制、低数字素养兜底）。
- **范围口径**：全文统一公告口径 统筹约43.6km² / 总体设计约11.4km² / 重点区域约368.4公顷（以官方公布为准），不与本包 provisional 几何混用。
- **权利登记**：新增 report/copyright_statement.md，登记字体、图件、地图、图纸、HTML 与代码的作者/工具/许可/署名/限制；sources.json 逐案例登记发布者/链接/日期/主张/许可边界。

## v0.1.0 - 2026-08-24

- Initial assembly (concept package) for compute-infrastructure-grid.
- Proposal drafted via OpenCode CLI (opencode), session ses_fcda127f0ffeN38Q60NmetnHtD; edited for structure.
- Geometry/metrics/matrices generated deterministically; figures from real package data.
- Valroot gates run on 2026-08-24 (results persisted in self_check.json).