# 方案迭代记录

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