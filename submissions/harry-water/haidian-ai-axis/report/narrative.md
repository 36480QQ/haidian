# 评审导读（当前状态：OC-D-007 双语正文与几何／指标同源同步后）

This note is the current reviewer-facing reading guide for `proposal.md` and `proposal.en.md`. The complete Chinese and English bodies and 42 registered sources exist and are cross-referenced from both bodies, and the current-package concept geometry, metrics, and assumptions have passed this round's internal review; the bilingual figure pairs, bilingual HTML, A3/A0 PDF pairs, manifest refresh, and package finalization remain pending, so `manifest.package_state` stays `scaffold`.

## 1. 当前主线

全文只有一条阅读主线：**遗产主线 → 三站分工 → 两翼供给/反馈 → 六类空间原型 → 十个运行场景 → 一套年度账本**（第一章提出、第十一章收束）。中英文正文逐段等义，13 个官方章节标题与顺序一致；source／standard／depth／data／metric 五类机器可读标签在两稿中的集合完全相等。

## 2. 证据边界（必须一起阅读）

1. **海淀新轴 / HAIDIAN AI AXIS** 是本方案提出的空间与功能协同框架，不是法定规划轴线、北京中轴线延长线或世界遗产关联项目；正文只转译中轴线的城市组织方法（三项独特对应＋三项本地规划推论，见第三章）。
2. **1909 年京张本线止于张家口**，通往内蒙古属于其后平绥—京包演进链；鸡鸣山煤矿支线定位为“煤炭外运＋铁路燃料供给”的能源供给支线。
3. **海淀—乌兰察布双城计算是基于已核验政策、合作与网络条件的设计推演（proposal inference）**，不是官方架构。公开合作事实不构成本方案专属调度架构的证据：截至 2026-08-08，尚无任何项目专属的协议、SLA、数据集或审批、运行证据被提供给本提交或经独立核验；正文不据此断言其不存在，也不宣称零碳算力、4.2 ms 直达海淀或使用全乌兰察布口径 PUE。
4. 中东五案例的绩效均为项目方或主办机构主张，正文只转移机制，并逐条写明“不复制／不可推断”与本地失效条件。
5. 气候数据为全市或区级口径，不得视为 43.6 平方公里研究区的站点级观测（cannot be treated as site-level station observations）。

## 3. 已通过本轮内部评审的空间契约（geometry 同源）

九个几何图层均为已通过本轮内部评审的概念图层（`source_type=agent_generated_design` 或维护者临时边界，confidence=low）：

- 边界与重点区：`SITE-001`（临时粗略边界）、`PROV-KEY-001/002/003`（三处临时重点区）。
- 用地：`LU-001..006` 概念分区；建筑：`BLDG-ST01/ST02/ST03-001` 三个站点概念干预包络（仅为干预包络，非现状建筑）。
- 道路：`ROAD-AXIS-001` 主脊、`ROAD-WING-TECH-001` 与 `ROAD-WING-XIAOYUE-001` 两翼连线、`ROAD-STITCH-N4/N5` 两条缝合线，均为概念慢行连线，非工程线位。
- 绿地：`GREEN-AXIS-001` 主线遮荫廊道、清河／小月河与三处站前概念绿地。
- 公共空间：`N1–N6` 六类原型节点；**N4 为 `mobility_stitch`，状态 `design_only_closed_pending_study`**——在交通、无障碍与工程专项论证完成前视为未开通，桥、地道、平面过街、遮蔽段、落地广场、绕行与人工值守均为待论证概念选项，正文不把任何一项表述为已决定。
- 约束：`CONSTRAINTS` 为缺数据适用性／实施前置校验总览面（分析辅助层，非法定管控线、非 AI 服务覆盖承诺），另含两翼概念服务范围面 `WING-TECH-001`／`WING-XIAOYUE-001`。
- 分期：`PHASE-001..003`。

人工值守、人工可呼叫与人工引导在全文一律为“运营主体确认后、经授权服务时段内的设计目标”，不构成人员配置承诺。

## 4. 指标（metrics 同源）

`metrics.json` 当前为 **14 项 known + 23 项 unknown**。第十一章的「已知指标同源对照表」把 14 项 known 按三组同源对照，并给出机器值与展示口径：

- 临时／设计几何数学：site_area_sqm、building_footprint_area_sqm（仅为三个提交概念干预包络）、green_ratio、public_space_ratio、conceptual_mobility_length_m；
- 已申报设计计数：key_area_count、station_count、wing_count、prototype_node_count、scenario_count、industry_test_count、phase_count；
- 申报／文档覆盖度：declared_reversible_prototype_ratio 与 declared_manual_fallback_documentation_ratio（均为 1.0 的申报口径声明，**不得称为绩效或有效性指标**）。

全部 known 值均为临时边界与提交概念几何的低置信度输出；`floor_area_ratio` 等 23 项保持 `unknown`，官方数据到位后须整体重算，不能只替换单个文件。「可验证设计目标」表的六项当前值仍为 `unknown`。

## 5. 章节与任务对应速查

章节结构与 agent.1–agent.6 对应关系未变：第三章（agent.1/2/5）、第五章节点卡 N1–N6（agent.4）、第六章画像／场景卡／治理矩阵与海乌模型（agent.3/6）、第九章地标与导视（agent.4/5）、第十章长期运营（agent.6）、第十一章指标同源对照与合规矩阵。

## 6. 剩余下游阻断项（集成方待办）

1. 五对双语图件（当前五张 PNG 为占位）与双语 `visual/index.html`、`report/proposal.html` 的同源重渲染。
2. A3/A0 PDF 对（`drawings/` 当前为占位 PDF）。
3. `manifest.json` 清单与哈希刷新、`SCAFFOLD-DRAFT` 标记移除与 `package_state` 终态化（`finalize_submission.py` + `self_check_submission.py`）。
4. 官方 `SITE_BOUNDARY` 与三处 `KEY_AREA` polygon 发布后：九个几何图层与全部指标整体重算。
5. 官方控制线数据（文保紫线、河道蓝线、绿线、道路红线、轨道控制线）仍未在公开渠道找到可核验来源，`CONSTRAINTS` 面保持缺数据校验状态，不为其编造 source 记录。

在第 1–3 项关闭之前，官方校验器对 figures／PDF／manifest／scaffold／visual 的报错属预期；正文的 data／metric 引用不应再产生缺失或悬空报错。
