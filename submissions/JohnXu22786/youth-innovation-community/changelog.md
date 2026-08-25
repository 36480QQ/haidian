# 方案迭代记录

## v0.3.0 - 2026-08-25（Round 2 修复）

- P0 修复「15 分钟公共生活圈 = 2 km 步程圆」无依据对应：mobility-bluegreen（中英）删除「十五分钟公共生活圈」表述，将 2 km 圆改标为「等距示意圆、非路网等时圈」，图上注明步速假设（1.2–1.4 m/s 时单向约 24–28 分钟）、未计入交叉口/屏障、检索日（2026-08-25）无公开路网级数据、等时圈须待官方路网数据发布后重算；proposal.md / proposal.en.md 同步补概念命名与非等时圈声明；A3/A0 图册（中英）随图件重生成。
- P0 修复五项案例来源为主张级可核验链接：CASE-SHENZHEN-SHUIWEI（深圳新闻网 2017-12-15、深圳商报 2018-03-28、DOFFICE 项目页，2026-08-25 全部抓取核验；「全国首个」降级为「深圳首个」口径并附学术佐证）、CASE-SEOUL-YOUTH-HOUSING（english.seoul.go.kr 三个主张级页面）、CASE-SINGAPORE-HDB-COMMONS（HDB 官网设计特征页、NHB Void Decks 电子书 2013、DP Architects GoodLife! Makan）、CASE-HK-YOUTH-HOSTEL（hyab.gov.hk 官方页面 + 2025-10-15 立法会书面答复；主管域名由 hab.gov.hk 更正为 hyab.gov.hk）、CASE-YOUTH-DEVELOPMENT-CITIES（中国共青团网官方全文 中青联发〔2022〕1号 + 新华网 2022-06-02 试点名单稿）；逐项补准确元数据、所支持主张与引用边界，正文案例表与参考资料表同步更新并加 [source:CASE-…] 锚点（正文表格内 URL 数字串过长会误触规则，完整主张级链接全部落在 sources.json）。
- P1 修复图件可读性：根因修复 plot_geoms 对 fc=None 的多边形默认填充（此前整个场地被默认蓝覆盖，即「九类用地大面积统一蓝色」来源）；用地结构图（中英）重绘为九类概念分区实际图斑可区分配色 + 图例一一对应（含商务金融用地 0902 实际图斑），占比为几何复算口径并注明与正文概念口径的差异；geometry/land_use.geojson 确定性重建并以内嵌（interior re-cut）方式实现 0804、1207、16 三类目（union 保持精确、投影后无重叠、无自相交），metrics.json 的 land_use_zone_count 更新为 30；site-overview 环线说明移到无碰撞区；key-areas 英文副标改为两行换行+加大间距（消除「honorsLive」式粘连）；A0 展板改为真实 A0 幅面并以更大图幅铺排（首页核心图件 65%→70% 宽度、全高 93%）。
- 校验复跑：四门禁全部 PASS（validate_local_submission / spatial_review / visual_review / professional_review，exit=0；spatial 仅保留 3 条既有 minor KEY_AREA_PROVISIONAL 提示）；score_rubric 100.0/100（无 mandatory_rejections、无 reviewer_gaps）；embed_fonts + check_font_coverage → ALL_FONTS_OK；manifest 哈希与 self_check.json（formal-review-ready）持久化。

## v0.2.0 - 2026-08-25

- 修复 v2 双语合同：proposal.md 声明 bilingual_contract_version=1 与 translation_file=proposal.en.md；proposal.en.md 声明 language=en、translation_of=proposal.md，并提供完整英文译文。
- 补齐英文 counterpart：五张基础图与五张扩展图（*.en.png）、A0/A3 英文图册（a0-boards.en.pdf / a3-booklet.en.pdf）、report/proposal.en.html、visual/index.en.html，全部登记在 manifest.json（language=en + translation_of）。
- 重构专业图包：全部图件重渲染，加入 provisional 场地语境、比例尺、指北针、图例、三节点平面/剖面与空间序列、创新生态图谱、品牌识别（一环三点 Logo 母版与色板）、地标目录、组件库、场景卡总览与运营流程；A0 改为 3 张满幅展板（zh/en 各 3 页），A3 为封面+10 页图册（zh/en 各 11 页）。
- 正文补齐 agent.1—agent.6 实质交付：案例扩至 6 个（逐项登记来源与许可边界）；场景卡扩至 10 张（C-01—C-10）；新增 3 张产业测试验证场景卡（T-01—T-03）；地标编号对象 LM-01—LM-03；年度活动品牌 A-01—A-03；新增区域协同专章（北纬社区、未来科学城、怀柔科学城、经开区、京津冀）与品牌识别专章。
- 统一口径：persona_count=6（正文六类人才画像）、global_case_count=6、industry_test_scenario_count=3、annual_program_count=3、landmark_count=3，均与正文编号对象一致；补充公园绿地 30%（用地分区口径）与 green_ratio/public_space_ratio（几何复算口径）的关系说明。
- 新增试点执行表（牵头/协作/前置调查/成本等级/维护频率/数据最小化/人工复核/无障碍替代/KPI/投诉与申诉/停止条件）；provisional 数值一律以约数与低置信度标注。
- 闭合来源与版权链条：sources.json 新增六个案例条目（发布者/链接/日期/具体主张/许可边界）；report/copyright_statement.md 转为逐项资产台账；report/narrative.md 记录中英文主张、指标、免责声明与图位等价核对表。
- 修复 HTML 中文字体问题：visual 两版与 report 两版 HTML 均采用中文优先字体栈（Microsoft YaHei/PingFang SC/Noto Sans CJK SC），消除方框字风险；visual/index.html 与 proposal 内容对齐并补齐 14 个展示标记。
- Valroot 四门禁与评分器复跑（结果持久化于 self_check.json）。

## v0.1.0 - 2026-08-24

- Initial assembly (concept package) for youth-innovation-community.
- Proposal drafted via OpenCode CLI (opencode), session ses_fcd92677bffeAVm1X03iqfJfdP; edited for structure.
- Geometry/metrics/matrices generated deterministically; figures from real package data.
- Valroot gates run on 2026-08-24 (results persisted in self_check.json).