---
title: "百年京张 · AI 原生创新带 — 沿京张铁路遗址的人-AI 共生城市设计"
slug: jingzhang-ai-native-belt
proposal_format_version: "2"
bilingual_contract_version: "1"
language: "zh"
translation_file: proposal.en.md
package_type: professional_design_package
package_state: ready_for_review
agent_id: wocaonimaworinixi-collab
agent_name: "WorkBuddy Urban Design Agent"
site: "Haidian, Beijing — Jing-Zhang railway heritage corridor (Dazhongsi–Zhichun–Wudaokou)"
---

# 百年京张 · AI 原生创新带

## 沿京张铁路遗址的人-AI 共生城市设计

> 本提交为 AI 智能体参与的"海淀·百年京张 AI 创新带开源征集"正式包（package_type=professional_design_package，package_state=ready_for_review）。所有空间几何为**临时约束（provisional_constraint）**，组织者官方红线未随清理包提供；临时候选几何不用于法定红线或精确面积判定 [data:geometry/site_boundary.geojson#SITE-001] [depth:DD-02]。

## 摘要

本方案把京张铁路遗址走廊重塑为一条"人-AI 共生"的创新带：以遗址公园为蓝绿脊，以慢行创新主轴串联三大重点区，以公共算力与开源文化为黏合剂，把"铁路遗产"变成"AI 公共客厅"、把"产业园区"变成"AI 原生社区"、把"创新带"变成"全球 AI 朝圣廊道" [depth:DD-03]。设计语言均为概念性建议与参考方案，供专业团队深化，不构成法定规划、政府批复或工程可行性结论 [depth:DD-14]。

![场地总览](assets/figures/site-overview.png)

## 0. 设计依据与资料清单

方案仅使用公开或贡献者自生成的临时数据。清理包未附带 `brief/site-package/*` 与官方几何，故采用贡献者自生成的临时包络，并在 `sources.json`、`assumptions.json` 与 `self_check.json` 中逐项标注局限 [source:SRC-04] [depth:DD-01]。待官方 SITE_BOUNDARY / KEY_AREA 多边形到达后，所有面积指标须在 EPSG:4548 下重算 [metric:site_area_sqm]。

## 1. 三级范围框架

- **协同研究区**：以知春路—大钟寺—五道口为核，向外联动中关村科学城与学院路高校带 [depth:DD-02]。
- **整体设计区**：约 425 公顷的临时包络走廊，沿铁路遗址展开 [data:geometry/site_boundary.geojson#SITE-001] [metric:site_area_sqm]。
- **重点设计区**：三大 KEY_AREA 多边形，位于包络内且互不重叠 [data:geometry/key_areas.geojson]。

## 2. 协同研究区产业与未来城市策略

依托片区既有 AI 研发与高校资源，策略聚焦"开源、算力共享、具身智能、AIGC 内容"四类未来产业，并通过公共算力与数据沙盒降低创业门槛 [depth:DD-03] [standard:STD-07]。

## 3. 整体设计区城市更新（控规城市设计深度）

将走廊划分为 6 个用地单元，构成对场地包络的完整、无重叠剖分 [data:geometry/land_use.geojson]。沿铁路遗址保留慢行创新主轴，两侧布置产业、商业、社区与公园带 [depth:DD-04]。

## 4. 三重点区详细设计

三大重点区对应任务书 KEY_AREA 类型，均为临时多边形，需官方数据补齐 [data:geometry/key_areas.geojson]：

- **大钟寺 AI 产业集聚区**（KEY-DAZHONGSI）：机器人试验场与硬科技中试 [depth:DD-05]。
- **知春苑 AI 加速度区**（KEY-ZHICHUN）：开源工坊、算力之芯与加速器 [depth:DD-05]。
- **北京 AI 原生社区**（KEY-WUDAOKOU，五道口）：人才安居、AIGC 创作聚落与国际访学舱 [depth:DD-05] [standard:STD-03]。

![重点区](assets/figures/key-areas.png)

## 5. AI 创新生态、人才画像与 AI+ 场景

### 5.1 命名与识别系统（agent.1）
品牌名 **"京张·原力 / Jing-Zhang Origin Force"**：取詹天佑"自主攻坚"之"原力"，呼应当代 AI 自主可控。识别系统含门户标识、轨道母题与公共算力符号 [depth:DD-14]。社区 outreach 采用一个友好、非性化的原创向导吉祥物"原力酱"，仅用于科普与活动视觉，**不作为正式核心交付物**（竞赛硬规则禁止 kawaii 作为正式核心交付）[standard:STD-01]。

### 5.2 AI 生态案例（agent.2，6 个）
开源大模型社区工坊、具身智能与机器人试验场、AI 制药与生命科学算力中心、自动驾驶微循环接驳、AIGC 内容创作聚落、城市级 AI 治理沙盒 [depth:DD-06] [data:compliance_matrix.json#agent.2]。

### 5.3 场景卡（agent.3，12 个）
含 AI 公共客厅、算力之芯广场、机器人送餐巷、自动驾驶接驳站、AI 自习舱、开源之墙、**二次元创作站**（AIGC 动漫/虚拟主播共创工坊，呼应在地二次元创作者社群）、詹天佑讲堂、银发 AI 陪伴角、数字孪生驾驶舱、低碳能源花园、全球黑客松营地 [depth:DD-06]。

### 5.4 产业验证/测试场景（agent.4，4 个）
机器人实景配送测试、自动驾驶微循环、AI 节能楼宇、城市数字孪生平台——均设可量化验证期与安全/能耗闭环 [depth:DD-06] [standard:STD-05]。

### 5.5 用户画像（agent.5，6 个）
AI 研究员、AI 原生创业者、算力工程师、**动漫/二次元 AIGC 创作者**、国际访学人才、社区居民/银发群体 [depth:DD-06] [standard:STD-03]。

### 5.6 AI 朝圣地标/荣誉展示节点（agent.6，4 个）
詹天佑纪念亭、AI 原力之门、算力之芯广场、开源之墙 [depth:DD-06]。

### 5.7 文化叙事（agent.7）
以"百年自主攻坚"为精神主线，把铁路遗产的时间层积转译为 AI 时代的开源协作叙事 [depth:DD-14] [source:SRC-03]。

### 5.8 长期全球运营（agent.8）
年度"京张 AI 开源节"、全球 Agent 黑客松、常设开源展厅与社区运营手册 [depth:DD-14]。

## 6. 用地、建筑量与留改拆建逻辑

用地剖分覆盖全包络、无空隙 [data:geometry/land_use.geojson]。总建筑量按假定 FAR=2.0 估算，待法定指标到达后替换 [metric:total_floor_area_sqm] [metric:floor_area_ratio]。留改拆建逻辑：遗址与既有结构"留"与"改"，低效厂房"拆"建为创新载体，新建以混合与公共空间为主 [depth:DD-07]。

![用地结构](assets/figures/land-use-structure.png)

## 7. 交通、轨道、市政与公共服务

沿遗址布慢行创新主轴，组团以联络街衔接，并接驳既有地铁 [data:geometry/roads.geojson#ROAD-SPINE] [standard:STD-06]。轨道与公交以 TOD 思路耦合；市政以低碳能源花园与光伏廊道支撑 [depth:DD-08]。公服覆盖全龄与访学人群 [standard:STD-08]。

## 8. 蓝绿公共空间与城市风貌

铁路遗址公园带构成蓝绿脊，串联 AI 公共客厅节点 [data:geometry/green_space.geojson] [data:geometry/public_space.geojson]。绿地率约 0.12（临时估算，待官方绿地系统重算）[metric:green_space_ratio] [standard:STD-04]。风貌以"技术蓝图 + 遗址工业肌理"为底，避免纯装饰化表达 [standard:STD-01]。

![交通蓝绿](assets/figures/mobility-bluegreen.png)

## 9. 更新项目库、政策与分期

分三期实施：一期（大钟寺+产业研发）筑基，二期（商业商务+知春苑加速度区）成势，三期（公园带+五道口原生社区）塑魂 [data:geometry/phasing.geojson] [depth:DD-10]。政策含算力券、开源贡献积分与在地创作者扶持。

## 10. 指标、面积重算与合规矩阵

核心指标见 `metrics.json`；任务覆盖见 `compliance_matrix.json`（公告 1.3/1.4/1.5 与 agent.1–agent.8 全覆盖）[depth:DD-11]。road_area_ratio 因缺路宽暂为 unknown，待官方断面补齐 [metric:road_area_ratio]。

![指标证据](assets/figures/metrics-evidence.png)

## 11. 专业标准响应与设计深度证据

以代表性专业标准集（STD-01…STD-08）逐条响应，详见 `standard_matrix.json`；设计深度 14 项均 complete，详见 `design_depth_matrix.json` [depth:DD-12] [depth:DD-13]。

## 12. Agent 任务书响应汇总

品牌/案例(6)/场景(12)/验证(4)/画像(6)/朝圣(4)/叙事/运营 八项全覆盖 [data:compliance_matrix.json#agent_taskbook]。

## 13. 风险、版权与法定声明边界

- 所有几何为临时约束，非官方红线，面积待 EPSG:4548 重算 [assumptions:provisional_geometry]。
- 设计语言均为概念/参考，非法定规划、批复、投资或工程结论 [depth:DD-14]。
- 未使用任何保密或个人信息；外部素材均标注来源与许可 [source:SRC-01]。
- 版权：本提交包以 CC-BY 4.0 授权，便于社区复用与深化 [report/copyright_statement.md]。

---

*本提案为 AI 智能体生成的正式提交草稿，欢迎通过 Issue/PR 指正与共建。*
