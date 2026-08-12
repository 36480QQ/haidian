---
title: "智脉一带 · AI Pulse Belt —— 百年京张AI创新带城市设计概念方案"
author_github: "LShengYi"
language: "zh"
proposal_format_version: "2"
bilingual_contract_version: "1"
translation_file: "proposal.en.md"
license: "COMMUNITY-DISPLAY-ONLY"
summary: "以「智脉一带 · AI Pulse Belt」为总体意象的 formal AI 城市设计方案包：京张铁路百年'铁脉'转译为 AI 时代'数字智脉'，一带三核、双翼多点；全部几何基于官方临时边界生成并披露面积偏差，指标可复算、图层可校验、双语全对齐。"
tracks: ["ai-traffic-walkability", "enterprise-services-ecosystem", "civic-agent-governance"]
scenarios: ["ai-traffic-walkability", "enterprise-service-copilot", "robot-delivery-low-speed", "ai-cultural-guide", "public-safety-operations-review"]
---

# 智脉一带 · AI Pulse Belt —— 百年京张AI创新带城市设计概念方案

## 设计依据与资料清单

本 formal 方案以北京市规划和自然资源委员会海淀分局发布的《百年京张AI创新带城市设计国际方案征集资格预审公告》为第一依据，并以 `brief/site-package/` 中经维护者登记的临时粗略边界、重点区域、枚举、指标和来源清单为机器可读依据。AI agent 在生成方案前读取了 `design_brief.json`、`allowed_design_space.json`、`sources.json`、`enums/`、`ranges/`、`schemas/`、`data/source_registry.json` 与 `data/processed/agent_fact_pack.md`，并按 `project_scope_summary.csv`、`agent_task_requirements.csv`、`source_use_matrix.csv`、`missing_data_checklist.csv` 建立任务、范围、资料用途和缺口清单。所有设计判断均拆分为可追溯来源、可复算指标、可校验图层和可人工复核假设。公告要求方案达到控制性详细规划的城市设计深度和规划综合实施方案的城市设计深度，因此文本叙述不替代 GeoJSON、指标表、A3 文册、A0 展板和 HTML 电子展示成果 [source:OFFICIAL-ANNOUNCEMENT] [source:AGENT-TASKBOOK] [depth:existing_conditions_diagnosis]。

资料登记表的使用边界如下 [source:SOURCE-REGISTRY]：

- `data/source_registry.json` 登记公开、清权与临时资料的用途边界；当前登记摘要：formal 可用资料 7 条、背景资料 1 条、provisional-only 资料 1 条。
- 本方案仅将 provisional 边界用于方案生成、自检、可视化和设计讨论，不升级为 official boundary、法定控规、正式评分依据或政府实施承诺。

`data/processed/agent_fact_pack.md` 是本方案的阅读导航层，不是新的权威来源 [source:PROCESSED-FACT-PACK]。事实判断均回到已登记原始材料；完整来源关系由 `sources.json` 保存。

本方案在官方 `SITE_BOUNDARY` 与三处 `KEY_AREA` 尚未取得时，使用 `brief/site-package/geometry/provisional_boundaries.geojson` 生成 formal 包：`geometry/site_boundary.geojson` 与 `geometry/key_areas.geojson` 均标注为 `provisional_constraint`、不声明 `official_boundary=true`，只能用于方案生成、自检、可视化和设计讨论。实测总体设计区面积 11.413 km2，与官方预公告值 11.4 km2 偏差 0.11%，已在 `assumptions.json`（ASSUME-002）披露 [data:geometry/site_boundary.geojson#PROV-SITE-001] [metric:site_area_sqm]。三处重点区数量由独立图层核对 [data:geometry/key_areas.geojson#PROV-KEY-001] [metric:key_area_count]。组织方数据缺口不阻断内容评分；官方 polygons 发布后需重算 site boundary、key areas、land use、roads、green space、public space、buildings、phasing 与 metrics。

## 三层范围工作框架

方案按公告确定的三层范围组织工作：**统筹研究范围** 43.6 km2，研究 AI 产业生态、战略定位、创新链与未来城市形态；**总体设计范围** 11.4 km2，形成城市更新总体框架、产业空间布局、交通市政支撑和城市风貌控制；**重点区域范围** 368.4 ha 三处详细设计地区，明确功能业态、空间动作、公共空间连通与交通组织。三层范围在 `compliance_matrix.json` 中逐条映射，保证公告 1.3、1.4、1.5 与 agent.1–agent.6 必选任务均有章节、图层、指标、图纸和 HTML 证据 [depth:three_level_scope_framework] [depth:overall_spatial_structure] [standard:PROJECT-OFFICIAL-ANNOUNCEMENT]。

本方案总体概念为**「智脉一带 · AI Pulse Belt」**：延续京张铁路百年"铁脉"的记忆与线性空间骨架，塑造面向人工智能时代的"数字智脉"——以贯穿南北的中央绿廊为"一带"，以众智园、北京AI原点社区、大钟寺三处重点区为"三核"，以小月河场景赋能翼（西侧蓝绿生态界面）与中关村科技服务翼（东侧产业服务界面）为"双翼"，以 AI 场景节点与慢行网络为"多点"，形成"**一带三核、双翼多点**"的总体空间结构。Logo 意象为"脉"字与铁轨线渐变示波器波形：京张铁灰（#4A5560）与 AI 青（#0FA3B1）双色，口号"**百年轨道，智慧脉动**"。

| 层级 | 设计问题 | 方案回答 | 数据落点 |
| --- | --- | --- | --- |
| 统筹研究范围 | AI 产业生态与未来城市形态如何组织 | "高校策源—开源协作—企业转化—公共体验—国际传播"创新链 + 三区两翼协同 | compliance_matrix.json、standard_matrix.json |
| 总体设计范围 | 产业空间、城市更新、交通市政与风貌如何落图 | 中央绿廊 260 m 宽、"两横两纵"道路骨架、四分区带、155 块用地无缝覆盖 | [data:geometry/land_use.geojson#LU-001]、[data:geometry/roads.geojson#ROAD-001] |
| 重点区域范围 | 三处片区如何达到详细设计深度 | 分别提出定位、空间动作、AI 场景与朝圣地标 | [data:geometry/key_areas.geojson#PROV-KEY-001]、[data:geometry/key_areas.geojson#PROV-KEY-002]、[data:geometry/key_areas.geojson#PROV-KEY-003] |

三层工作不是割裂图纸：统筹研究决定产业链与城市形态判断，总体设计将判断落实为更新项目与空间结构，重点区域详细设计验证具体地块、建筑、交通、公共空间与 AI 应用场景的可实施性 [source:PROCESSED-FACT-PACK]。任何无法从结构化数据复算的面积、比例、规模或项目数量，均不写入正式结论。

![总体设计区与统筹研究区范围示意图（概念建议）](assets/figures/site-overview.png)

## 统筹研究范围产业与未来城市研究

统筹研究范围的核心任务是构建世界级 AI 创新生态体系。方案梳理海淀高校院所、头部企业、算力算法数据要素、孵化平台与科技服务资源，提出"高校策源—开源协作—企业转化—公共体验—国际传播"五环创新链的空间协同框架，并回应任务书"五大功能"与"三区两翼"协同要求 [source:AGENT-TASKBOOK] [standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK]。

**生态图谱（概念建议）**：参照全球 AI 创新区成功经验——新加坡 Punggol Digital District（产学研住一体、数字试验床）、赫尔辛基 Kalasatama（敏捷试验街区）、首尔 AI Hub、剑桥 The Foundry、多伦多 Waterfront Toronto（滨水创新走廊）、巴黎 STATION F（巨型孵化器）+ 大巴黎智能街区——提炼六类空间机制：**土地供给**（留白弹性用地 16 类承载未来业态）、**空间组织**（庭院式研发街区）、**产业服务**（算力/数据/合规/投融资一站式）、**资金机制**（场景开放与政府采购引导）、**人才服务**（人才特区与青年公寓）、**数据场景**（开放测试场与测评体系）。全球案例结论均为概念参考，供专业团队深化，不构成已确定的政府安排。

**三区两翼产业布局（概念建议）**：

| 片区 | 产业侧重 | 空间落点 |
| --- | --- | --- |
| 众智园AI自主创新加速区 | 大模型训练、全栈自主创新、标准制定与安全治理 | 众智园北部科研带、标准文化馆、体育测试场 [data:geometry/land_use.geojson#LU-001] |
| 北京AI原点社区 | 近校孵化转化、开源体系、人才特区、成果发布 | 原点发布厅、清华东路教育带、五道口商住带 [data:geometry/land_use.geojson#LU-001] |
| 大钟寺AI产业聚集区 | 智能体、智能终端、内容消费、数据要素 | 知春路商业带、数据要素楼、站前商业 [data:geometry/land_use.geojson#LU-001] |
| 小月河场景赋能翼（西翼） | 场景试验、生态体验 | 西侧防护绿地与场景测试段 [data:geometry/green_space.geojson#GREEN-001] |
| 中关村科技服务翼（东翼） | 科技服务、国际交往 | 学院路沿线科研与服务平台 [data:geometry/land_use.geojson#LU-001] |

未来城市形态研究回答人工智能如何改变工作、生活、社交、学习、交通与公共服务：以"数字智脉"为空间线索，把 AI 交通系统、连续绿色空间、创新服务设施与国际化生活工作氛围落实为可定位的功能区、节点、廊道与场景 [depth:overall_spatial_structure] [standard:MOHURD-URBAN-DESIGN-MEASURES]。全球 AI 创新活动、开发者社区、开放场景与朝圣路线均表述为"概念建议/参考方案"，不写为已确定的政府活动或实施安排。

## 总体设计范围城市更新与控规深度城市设计

总体设计范围（实测 11.413 km2）要求达到控制性详细规划的城市设计深度。本方案提出以**中央智脉绿廊**为脊的总体结构 [data:geometry/land_use.geojson#LU-001]：沿绿廊东西两侧组织用地，形成**四个分区带**——众智园科研带（北）、原点社区产城融合带、大钟寺商业科研带、南部更新带，并预留南端留白弹性用地承载未来 AI 业态（16 留白用地 4 处）[depth:land_use_layout] [depth:development_intensity_controls]。

**道路网络（概念建议）**：以"两横两纵"为骨架——横向北五环（快速路）、清华东路（次干路）、成府路（支路）、知春路（主干路）；纵向学院路/西土城路（主干路）、荷清路/大钟寺东路（次干路）；并新增设计道路**智脉大道**、智脉二街、智脉三街组织地块微循环，中央绿廊内设连续绿道 [data:geometry/roads.geojson#ROAD-001] [data:geometry/roads.geojson#ROAD-010]。

**用地结构（概念建议）**：`geometry/land_use.geojson` 共 155 个地块，13 类用地，完整覆盖设计边界且无重叠（差集 <1 m2，已由 `validate_cover` 校验）[data:geometry/land_use.geojson#LU-001]。科研用地（0802）为主导类型，商业（05）、住宅（0701）、文化（0803）、教育（0804）等协同支撑；中央绿廊（1401 公园绿地）宽约 260 m，贯通南北 [data:geometry/green_space.geojson#GREEN-001]。`geometry/buildings.geojson` 表达 93 栋概念建筑基底（design_proposal 属性，非法定许可）[data:geometry/buildings.geojson#BLDG-001] [metric:building_footprint_area_sqm]。**涉及建筑高度、开发强度、道路红线、退线与设施标准的内容，在官方控制条件发布前一律按"待正式控规条件确认"处理，不以 agent 推测值冒充审定指标**。

![总体设计区用地结构图（概念建议）](assets/figures/land-use-structure.png)

## 重点区域详细设计

三处重点区域达到规划综合实施方案深度 [depth:three_key_area_detailed_design]，分别引用 [data:geometry/key_areas.geojson#PROV-KEY-001]、[data:geometry/key_areas.geojson#PROV-KEY-002]、[data:geometry/key_areas.geojson#PROV-KEY-003]。

| 重点片区 | 设计定位 | 空间动作 | AI 产业与运营场景 | 证据引用 |
| --- | --- | --- | --- | --- |
| 众智园AI自主创新加速区（192.1 ha） | 花园型全栈自主创新街区 | 北临五环设绿带缓冲；门户广场接驳；科研院落 + 标准文化馆 + 体育测试场 + 留白弹性用地 | 大模型训练测试、标准制定工作坊、安全治理展示、低碳算力体验 | [data:geometry/key_areas.geojson#PROV-KEY-001]、[data:geometry/land_use.geojson#LU-001]、[data:geometry/public_space.geojson#PUBLIC-003] |
| 北京AI原点社区（104.3 ha） | 近校型成果转化与人才社区 | 清华东路教育带缝合校区园区；原点发布厅（文化 0803）；五道口商住带；社区服务嵌入 | 开源社区、成果发布、人才特区服务、近校孵化 | [data:geometry/key_areas.geojson#PROV-KEY-002]、[data:geometry/public_space.geojson#PUBLIC-002]、[source:AGENT-TASKBOOK] |
| 大钟寺AI产业聚集区（72.0 ha） | 站城一体化智能经济街区 | 大钟寺站前广场四象限步行连通；知春路商业带；数据要素楼；站城商业复合 | 智能体与智能终端展示、内容消费、数据要素与国际路演 | [data:geometry/key_areas.geojson#PROV-KEY-003]、[data:geometry/public_space.geojson#PUBLIC-001]、[metric:key_area_count] |

三处重点区在 `geometry/key_areas.geojson` 中均以 `provisional_constraint` 呈现，正文、HTML、sources、assumptions 与 self_check 均说明其不可作为正式评分或审批依据。`compliance_matrix.json` 分别覆盖公告 1.5.3.1、1.5.3.2、1.5.3.3。设计表达包含功能业态、概念建筑、公共空间系统、交通组织与实施项目；A3 文册与 A0 展板含重点片区总图、局部详图与指标说明，HTML 页面可切换查看三处重点区域。

![三重点区详细设计概念图（概念建议）](assets/figures/key-areas.png)

## AI 创新生态、人才画像与 AI+ 场景

方案建立面向 AI 人才和企业的空间需求画像，并形成"产业发展场景 + AI 赋能城市功能场景"双线场景体系。每个场景均说明服务对象、空间位置、数据来源、隐私边界、人工复核机制与运营主体 [source:AGENT-TASKBOOK]。

**5 类用户画像**：

| 用户画像 | 典型需求 | 空间响应 | 自检边界 |
| --- | --- | --- | --- |
| 初创工程师 | 低成本办公、算力入口、产品试验场 | 众智园共享测试场、端侧算力服务点、标准治理咨询 | 算力和数据服务需另行授权 |
| 科研人员 | 跨机构协作、成果转化、学术交流 | 原点发布厅、科研院落、清华东路教育带 | 校园数据和科研成果需授权 |
| 家庭周末客 | 亲子休闲、运动、文化体验 | 中央绿廊、口袋公园、体育测试场、钟韵文化体验 | 不采集个人行为轨迹，活动数据只做聚合统计 |
| 银发游客 | 无障碍导行、慢速休闲、文化讲解 | 无障碍 AI 导行站、智脉艺术铁轨休憩带 | 健康类数据不用于商业推荐 |
| 开发者社区运营者 | 活动组织、代码协作、社区声誉 | 开发者露天工位代码墙、发布广场、智盒会议亭 | 公共活动数据匿名聚合 |

**12 张场景卡（概念建议）**：

| 场景卡 | 空间载体 | 设计说明 |
| --- | --- | --- |
| 01 铁轨巡检AR孪生 | 中央绿廊铁轨段 | AR 叠加京张铁路百年影像与 AI 孪生巡检演示 |
| 02 无人接驳巴士走廊 | 智脉大道沿线 | 园区—轨道站无人接驳示范线（概念）[scenario:ai-traffic-walkability] |
| 03 AI 骑行教练站 | 绿廊绿道节点 | 骑行数据可视化与 AI 运动指导 |
| 04 钟韵元宇宙 | 大钟寺站前 | 钟声文化的数字孪生与互动展演 |
| 05 智盒会议亭 | 各研发街块节点 | 自助会议、直播与远程协作微型空间 |
| 06 无人机配送驿站 | 众智园南块 | 低空物流接驳试验驿站（概念）[scenario:robot-delivery-low-speed] |
| 07 AI 园艺师口袋公园 | 各住区街角 | 植物养护 AI 协作与社区认养机制 |
| 08 无障碍 AI 导行站 | 轨道站与绿廊节点 | 语音/触觉多模态无障碍导航 |
| 09 赛事数据可视化墙 | 体育测试场周边 | 智能体育赛事实时数据大屏（聚合展示） |
| 10 建筑能耗 AI 调控楼 | 众智园科研带 | 分布式能源与 AI 能耗调控示范（概念） |
| 11 AI 咖啡机器人驿站 | 商业街与研发街角 | 机器臂咖啡体验与开发者社交 |
| 12 开发者露天工位代码墙 | 原点发布广场周边 | 开源贡献墙、露天工位与演示区 |

**3 个产业测试验证场景（概念建议）**：① 车路协同开放测试段（智脉大道 1.2 km 概念段）；② 低空配送航线验证（众智园—大钟寺概念航线，遵守空域与安全法规）[scenario:robot-delivery-low-speed]；③ 多模态导视系统测评场（绿廊全线）。**公共安全类 AI 应用仅做运营评审研究，不替代人工复核** [scenario:public-safety-operations-review]。

**3 个 AI 朝圣地标（概念建议）**：**AI 原点之钟**（大钟寺站前广场，钟韵文化与 AI 起源意象）、**AI 之光塔**（众智园门户广场，光艺术 + 模型推理实时可视）、**智脉艺术铁轨**（中央绿廊北段，废弃铁轨艺术化改造 + 数字投影）。朝圣路线"**百年轨道，智慧脉动**"与 10 号场景卡"全球 AI 活动周路线"联动 [data:geometry/public_space.geojson#PUBLIC-001] [data:geometry/green_space.geojson#GREEN-001]。相关公共空间与绿地指标在 `metrics.json` 中均为 known 状态、可直接复算 [metric:public_space_ratio] [metric:green_ratio]。

AI 治理建议遵守数据最小化、公开来源、可解释与人工复核原则：城市智能体可辅助识别慢行断点、公共空间热力、设施维护、企业服务需求与活动安全风险，但不替代规划审批、不输出未经授权的个人画像、不声称获得官方实施承诺。所有场景节点均进入结构化图层或合规矩阵。

## 用地、建筑规模与拆改留方案

用地方案依据国土空间调查、规划、用途管制分类等公开标准表达，形成完整、闭合、无缝的用地分区 [standard:MNR-LAND-USE-CLASSIFICATION-GUIDE] [data:geometry/land_use.geojson#LU-001]。13 类用地中科研 0802 为主导（14 地块），商业 05（10）、住宅 0701（6）、教育 0804（6）、医疗 0806（6）、文化 0803（3）、体育 0805（1）、社区服务 0702（1）、公园绿地 1401（12）、防护绿地 1402（9）、广场 1403（2）、道路 1207（81）、留白 16（4），合计 155 地块无缝覆盖 [depth:land_use_layout]。

建筑方案区分保留、改造、更新、新建与待确认对象：由于缺少现状建筑、权属、控规与工程条件，本方案只提供**方法框架与待校准清单**，不编造拆改留结论 [depth:retain_renovate_demolish] [depth:height_massing_character]。`geometry/buildings.geojson` 的 93 栋概念建筑全部标注 `status=design_proposal`、`confidence=low`，仅表达体量组织意图 [data:geometry/buildings.geojson#BLDG-001] [metric:building_footprint_area_sqm]。总建筑规模、容积率、建筑高度、建筑密度等指标在官方条件缺失时统一为 `status=unknown`（见 `metrics.json` 的 floor_area_ratio，reason 已说明待补条件与复算路径）。

## 交通、轨道、市政与公共服务设施

交通方案回应公告对轨道站点一体化、道路微循环、慢行断点、对外交通、停车、非机动车停放与绿色交通系统的要求 [depth:traffic_rail_slow_parking] [data:geometry/roads.geojson#ROAD-001] [data:geometry/public_space.geojson#PUBLIC-001]：

- **轨道接驳（概念）**：以大钟寺站、五道口站、知春路站、西土城站、清华东路西口站为锚点，设 3 条概念接驳线（ROAD-011/012/013）与无人接驳巴士走廊（场景卡 02）[scenario:ai-traffic-walkability]；
- **道路微循环**：智脉大道（28 m 概念红线）、智脉二街/三街组织街区级循环，慢行绿道沿中央绿廊全线贯通 [data:geometry/roads.geojson#ROAD-010]；
- **慢行断点**：概念提出北五环跨环慢行节点与绿廊南北两端景观节点（详见图 04 与 `constraints.geojson`）[data:geometry/constraints.geojson#CONSTRAINTS]；
- 停车与非机动车停放以"轨道 + 接驳 + 慢行"为优先序，具体规模待交通专项与控规条件确认。

市政与公共服务设施覆盖 AI 产业服务设施（算力、数据、合规、投融资服务点）、人才生活服务设施、新型基础设施（端侧算力驿站、分布式能源节点，场景卡 10）与传统市政设施融合 [depth:municipal_new_infrastructure]。管线、能源、排水、防洪、消防等工程资料缺失时列为正式深化前置条件，通过 `assumptions.json` 说明待补，不写成审定条件。

## 蓝绿空间、公共空间与城市风貌

**蓝绿空间（概念建议）**：以中央智脉绿廊为脊（260 m 宽、贯通南北、总面积约 284.9 ha、绿地率 25.0%）[data:geometry/green_space.geojson#GREEN-001] [metric:green_ratio]，西侧防护绿带呼应小月河场景赋能翼，东侧沿学院路设防护绿带，各街区植入口袋公园与广场节点 [data:geometry/public_space.geojson#PUBLIC-001] [depth:blue_green_public_space]。6 处广场（大钟寺站前、原点发布、众智园门户、五道口生活、清华东路西口、南部社区）构成公共空间骨架 [data:geometry/public_space.geojson#PUBLIC-001]。

![交通骨架与蓝绿系统概念图（概念建议）](assets/figures/mobility-bluegreen.png)

**城市风貌（概念建议）**：融合京张铁路历史文化、中关村创新文化与 AI 创新文化三线叙事 [depth:overall_spatial_structure] [standard:MOHURD-URBAN-DESIGN-MEASURES]：清华园火车站遗址节点与智脉艺术铁轨承载铁路记忆；AI 原点之钟、AI 之光塔承载 AI 文化；导视符号系统以"铁轨—波形"母题统一。风貌控制区分官方管控、设计建议与待确认条件，严禁在无文保或控规依据时给出伪精确控制线。所有品牌、字体、图像、肖像与企业标识均需清权来源（见 `report/copyright_statement.md`）。

## 更新项目清单、实施政策与分期计划

更新项目清单（概念建议，共 12 项）：

| 项目编号 | 项目名称 | 类型 | 主要依赖 | 证据引用 |
| --- | --- | --- | --- | --- |
| JZ-01 | 中央智脉绿廊贯通工程 | 公共空间/蓝绿 | 道路红线、桥下空间、交通组织复核 | [data:geometry/green_space.geojson#GREEN-001] |
| JZ-02 | 北五环跨环慢行节点 | 交通/慢行 | 高架与跨线条件、交通安全评估 | [data:geometry/roads.geojson#ROAD-001] |
| JZ-03 | 众智园门户广场与 AI 之光塔 | 公共空间/地标 | 权属、景观与光环境设计 | [data:geometry/public_space.geojson#PUBLIC-003] |
| JZ-04 | 原点发布厅与代码墙 | 产业服务/文化 | 权属、首层业态、运营主体 | [data:geometry/buildings.geojson#BLDG-001] |
| JZ-05 | 大钟寺站四象限步行连通 | 轨道一体化/慢行 | 轨道站点、道路交叉口、市政管线 | [data:geometry/public_space.geojson#PUBLIC-001] |
| JZ-06 | 智脉大道无人接驳示范段 | 交通/新基建 | 交通法规、运营主体、信号条件 | [data:geometry/roads.geojson#ROAD-010] |
| JZ-07 | 清华东路教育带缝合 | 城市更新/教育 | 校区边界、权属、慢行安全 | [data:geometry/land_use.geojson#LU-001] |
| JZ-08 | 南部更新带提升 | 城市更新/住宅 | 权属、拆改留专项评估 | [data:geometry/phasing.geojson#PHASE-003] |
| JZ-09 | 低空配送航线验证场 | 新基建/产业测试 | 空域审批、安全监管 | [data:geometry/constraints.geojson#CONSTRAINTS] |
| JZ-10 | 端侧算力与能耗调控示范楼 | 新基建/市政 | 能源、算力、消防与运营主体 | [data:geometry/buildings.geojson#BLDG-001] |
| JZ-11 | 无障碍 AI 导行系统 | 公共服务/无障碍 | 无障碍设施标准、数据授权 | [data:geometry/constraints.geojson#CONSTRAINTS] |
| JZ-12 | 全球 AI 活动周公共路线 | 运营/品牌 | 公共空间许可、活动安全、版权清权 | [data:geometry/phasing.geojson#PHASE-001] |

**实施分期（概念建议）**（`geometry/phasing.geojson`，[depth:renewal_project_list] [depth:phasing_implementation]）：**P1 近期（2026–2030）**——三重点区先行：众智园、原点社区核心带、大钟寺核心带（[data:geometry/phasing.geojson#PHASE-001]）；**P2 中期（2030–2035）**——绿廊全线贯通 + 大钟寺北块与南部北块（[data:geometry/phasing.geojson#PHASE-002]）；**P3 远期（2035–2040）**——南部更新带与留白弹性用地（[data:geometry/phasing.geojson#PHASE-003]）。**征集周期（100 天）与实施分期严格区分**：前者是提交成果时间要求，后者是城市更新推进路径。近期可先以轻量设施、运营活动与服务平台启动（场景卡、朝圣地标、导行系统），远期内容等待正式控规、市政、交通与权属条件确认。年度活动体系（开发者大会、场景开放日、国际 AI 周）说明运营对象、频率、责任边界与转化路径，不写宣传口号 [source:AGENT-TASKBOOK]。

## 指标体系、面积复算与合规矩阵

指标体系（`metrics.json`）含 6 项：总体设计范围面积（site_area_sqm，实测 11,412,825.4 m2，官方 11,400,000 m2，偏差 0.11%）、建筑基底面积（building_footprint_area_sqm，约 116.8 ha）、绿地率（green_ratio，25.0%）、公共空间比例（public_space_ratio）、重点区数量（key_area_count，3）与容积率（floor_area_ratio，`status=unknown`，官方 FAR 控制缺失）。所有 known 指标均可从 GeoJSON 复算 [metric:site_area_sqm] [data:geometry/green_space.geojson#GREEN-001] [depth:metrics_recalculation]。

![核心指标与证据图（概念建议）](assets/figures/metrics-evidence.png)

指标分三类管理：① 可由提交几何直接复算的空间指标（面积、比例、分期面积）；② 需官方控规支撑的管控指标（容积率、高度、密度、退线、红线——目前 `unknown`）；③ 需运营数据校准的绩效指标（AI 创新指数、人才密度、场景使用频次——概念建议）。三类分别进入 `metrics.json`、`assumptions.json` 与 `compliance_matrix.json`，避免把运营愿景误写成审定规划条件 [standard:PROJECT-OFFICIAL-ANNOUNCEMENT]。

合规矩阵覆盖公告 1.3、1.4、1.5 与 agent.1–agent.6 全部必选任务：agent.1 命名体系与标识（本节与第三章）、agent.2 全球案例与生态图谱（第三章）、agent.3 场景卡/测试场景/画像（第六章）、agent.4 朝圣地标与荣誉展示（第六章、第九章）、agent.5 文化叙事与导视（第九章）、agent.6 活动体系与社区运营（第十章）。`scripts/spatial_review.py` 与 `scripts/visual_review.py` 的结果是 formal 自检证据。

## 风险、版权与合规说明

**双语要求**：本方案中文主文件与英文对照译稿 `proposal.en.md` 完整对齐（bilingual_contract_version 1）；A3/A0 图纸、HTML 与含文字图件均提供双语表达，优先使用 `docs/terminology-glossary.md` 推荐译法。所有图片、图纸、图标、数据与代码资产在 `sources.json` 与 `report/copyright_statement.md` 中说明来源、许可与授权状态；HTML 页面不加载远程脚本、远程地图瓦片、远程字体、iframe、表单或外部 API，不跟踪评审者行为。

**风险与缺资料清单**：official boundary、key area、控规、道路红线、地块权属、建筑现状、市政管线、文保与公共服务缺口均进入 `assumptions.json`（ASSUME-001/002/003）与本节；任何缺少官方控规、道路红线、权属、市政、消防或文保条件的结论均降级为待确认事项 [depth:risk_missing_data] [data:geometry/constraints.geojson#CONSTRAINTS] [source:SITE-PACKAGE]。

本方案不声称官方批准、审定控规、最终土地权属、最终建设规模或保证实施。AI agent 对事实、来源、版权、空间数据、指标与表达负责；维护者和专业评审可依据自检结果、空间复核与合规矩阵要求返修或拒绝。

## 参考资料

- brief/public-brief.md
- brief/site-package/design_brief.json
- brief/site-package/agent_taskbook.json
- brief/site-package/allowed_design_space.json
- brief/site-package/enums/
- brief/site-package/ranges/planning_limits.json
- brief/site-package/geometry/provisional_boundaries.geojson
- data/source_registry.json
- data/processed/agent_fact_pack.md
- data/processed/project_scope_summary.csv
- data/processed/agent_task_requirements.csv
- data/processed/source_use_matrix.csv
- data/processed/missing_data_checklist.csv
- 完整机器索引：见 `sources.json`、`metrics.json`、`compliance_matrix.json`、`standard_matrix.json` 与 `design_depth_matrix.json`
- 本节书目入口依据场地包登记，完整出处和许可见结构化来源清单 [source:SITE-PACKAGE]
