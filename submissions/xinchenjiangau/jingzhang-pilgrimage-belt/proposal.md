---
title: "京张朝圣带 · Jing-Zhang Pilgrimage Belt"
author_github: "xinchenjiangau"
language: "zh"
proposal_format_version: "2"
bilingual_contract_version: "1"
translation_file: "proposal.en.md"
license: "COMMUNITY-DISPLAY-ONLY"
summary: "以京张铁路遗址公园为「朝圣之路」，把众智园、北京AI原点社区、大钟寺三处重点片区重构为「起源殿、转译殿、应用集」三座AI朝圣地标，叠加铭文带荣誉体系与朝圣护照体验系统，形成可步行、可传播、可运营的AI公共空间叙事带。"
tracks: ["jingzhang-heritage-narrative", "youth-friendly-public-space", "ai-origin-community"]
scenarios: ["ai-cultural-guide", "ai-traffic-walkability", "public-safety-operations-review"]
---

# 京张朝圣带 · Jing-Zhang Pilgrimage Belt

## 设计依据与资料清单

本 formal 方案以北京市规划和自然资源委员会海淀分局发布的《百年京张AI创新带城市设计国际方案征集资格预审公告》为第一依据，并以 `brief/site-package/` 中经维护者登记的临时粗略边界、重点区域、枚举、指标和来源清单为机器可读依据 [source:OFFICIAL-ANNOUNCEMENT] [source:SITE-PACKAGE]。所有设计判断都拆分为可追溯来源、可复算指标、可校验图层和可人工复核假设；文本叙述不替代 GeoJSON、指标表、A3 文册、A0 展板和 HTML 电子展示成果。

方案从公告、面向智能体任务书和场地资料出发组织成果，最关键依据放在判断旁边 [source:AGENT-TASKBOOK] [depth:existing_conditions_diagnosis]。资料登记表的使用边界如下 [source:SOURCE-REGISTRY]：formal 可用资料与 provisional-only 资料被严格区分，agent 不得把 background_only 或 provisional_only 资料升级为官方红线、法定控规、正式评分依据或政府实施承诺。

`data/processed/agent_fact_pack.md` 是本方案的阅读导航层，不是新的权威来源 [source:PROCESSED-FACT-PACK]。当前提交采用 `brief/site-package/geometry/provisional_boundaries.geojson` 生成临时 formal 包，`geometry/site_boundary.geojson` 与 `geometry/key_areas.geojson` 均标注 `provisional_constraint`、`official_boundary=false`，只能用于方案生成、自检、可视化和设计讨论，不能作为 official redline、审批依据、精确面积依据或法定控制结论 [data:geometry/site_boundary.geojson#SITE-001] [metric:site_area_sqm]。该数据缺口不阻断内容评分；替换 official polygons 后，各图层与指标均需重算。

![资料证据链与提交包关系图](assets/figures/site-overview.png)

## 设计概念：京张朝圣带（三殿·一路·一铭文·一护照）

本方案把 AI 创新的抽象进程，转译为一段可被市民步行完成的「朝圣」体验。京张铁路遗址公园纵贯三大核心区，是天然的线性公共空间主轴；方案将它命名为 **朝圣之路（Pilgrim's Way）**，并把三处重点片区重构为三座承载不同创新阶段的地标殿堂 [source:AGENT-TASKBOOK] [depth:overall_spatial_structure]：

- **起源殿（Origin Hall）· 众智园**——AI 创新「从 0 到 1」的策源地，对应国家人工智能平台、全栈自主创新与安全治理 [data:geometry/key_areas.geojson#PROV-KEY-001] [data:geometry/public_space.geojson#PUBLIC-001]。
- **转译殿（Translation Hall）· 北京AI原点社区**——把科研「转译」为产品与社区，对应近校成果转化、开源协作与人才特区 [data:geometry/key_areas.geojson#PROV-KEY-002] [data:geometry/public_space.geojson#PUBLIC-002]。
- **应用集（Application Market）· 大钟寺**——AI「进入日常生活」的市集，对应智能体、智能终端、内容消费与数据要素 [data:geometry/key_areas.geojson#PROV-KEY-003] [data:geometry/public_space.geojson#PUBLIC-003]。

三殿之间由南北贯通的绿地骨架连接，这条朝圣之路以公园绿地（1401）落图，全程约 9.7 公里，构成约 150.8 公顷的连续蓝绿公共空间 [data:geometry/green_space.geojson#GREEN-001] [metric:green_space_area_sqm]。沿路布置 **铭文带（Inscription Belt）**——面向开发者、企业、高校与市民的贡献与荣誉展示体系；并配套 **朝圣护照（Pilgrim's Passport）**——以 AI 导览与慢行评估支撑的轻量化打卡与认证体验 [depth:blue_green_public_space]。三座地标广场合计约 15.2 公顷，是整条朝圣带的空间高潮与公共活动锚点 [data:geometry/public_space.geojson#PUBLIC-001] [metric:public_space_area_sqm]。

该概念不是新增红线，而是把公告三层范围与「百年京张文化带、都市AI生活体验带、AI融合创新带」的辨识度要求，转译为一条有起点、有路径、有仪式感、可运营的公共空间叙事 [standard:PROJECT-OFFICIAL-ANNOUNCEMENT]。

## 三层范围工作框架

方案按公告三个层次组织工作：统筹研究范围关注约 43.6 平方公里的AI产业生态与未来城市形态；总体设计范围关注约 11.4 平方公里京张遗址公园周边城市地区；重点区域范围关注约 368.4 公顷三处详细设计地区 [source:AGENT-TASKBOOK] [depth:three_level_scope_framework]。三层范围在 `compliance_matrix.json` 中逐条映射，保证公告 1.3、1.4、1.5 与 agent.1–agent.6 的必选任务都有章节、图层、指标、图纸和 HTML 证据。

三层工作不是割裂的图纸集合：统筹研究决定产业链与城市形态判断，总体设计把判断落到更新项目与空间结构，重点区域详细设计验证地块、建筑、交通、公共空间与 AI 场景的可实施性 [depth:overall_spatial_structure]。任何无法从结构化数据复算的面积、比例、规模或项目数量，不写入正式结论。

| 层级 | 设计问题 | 方案回答 | 数据落点 |
| --- | --- | --- | --- |
| 统筹研究范围 | AI产业生态和未来城市形态如何组织 | 「高校策源—开源协作—企业转化—公共体验—国际传播」的创新链 | compliance_matrix.json、standard_matrix.json |
| 总体设计范围 | 产业空间、更新、交通市政和风貌如何落图 | 朝圣之路绿地骨架 + 京张大道 + 三殿地标 + 用地建筑道路图层 | [data:geometry/land_use.geojson#LU-001]、[data:geometry/roads.geojson#ROAD-001] |
| 重点区域范围 | 三处片区如何达到详细设计深度 | 起源殿/转译殿/应用集三座地标与各自功能业态 | [data:geometry/key_areas.geojson#PROV-KEY-001]、[metric:key_area_count] |

![三层范围与空间工作框架图](assets/figures/land-use-structure.png)

## 统筹研究范围产业与未来城市研究

统筹研究范围的核心任务是构建世界级 AI 创新生态体系。方案把海淀高校院所、头部企业、算力算法数据要素、孵化平台、上市企业与独角兽资源，组织为「高校策源—开源协作—企业转化—公共体验—国际传播」的空间协同框架 [source:AGENT-TASKBOOK]。命名方案「京张朝圣带」直接服务三大辨识度目标：百年京张文化带（铁路遗址与朝圣叙事）、都市AI生活体验带（朝圣护照与公共场景）、AI融合创新带（三殿产业链） [standard:PROJECT-OFFICIAL-ANNOUNCEMENT]。

未来城市形态研究回答人工智能如何改变工作、生活、社交、学习、交通与公共服务。方案把 AI 交通系统、连续绿色空间、创新服务设施和国际化生活工作氛围，落实为可定位的功能区、节点与廊道 [depth:overall_spatial_structure]。产业战略指标、AI 创新指数、人才密度等绩效指标统一标注为待正式数据校准，不伪造精确数值。

## 总体设计范围城市更新与控规深度城市设计

总体设计范围达到控制性详细规划的城市设计深度。方案提出「一路三殿、蓝绿慢行复合」的总体空间结构：以朝圣之路绿地骨架为纵轴，以京张大道为服务性道路，以三座地标为公共空间锚点 [standard:MOHURD-CONTROL-DETAILED-PLANNING] [depth:land_use_layout]。`geometry/land_use.geojson` 完整覆盖设计边界且无重叠，`geometry/buildings.geojson` 表达更新建筑基底，`geometry/roads.geojson` 表达微循环与慢行接驳关系 [data:geometry/land_use.geojson#LU-001] [data:geometry/buildings.geojson#BLDG-001] [data:geometry/roads.geojson#ROAD-001]。

总体设计支撑交通、轨道、市政与配套设施。涉及建筑高度、开发强度、道路红线、退线与设施标准的内容，官方控制条件尚缺时统一写为「待正式控规条件确认」，不以 agent 推测值冒充审定指标 [standard:MOHURD-CONTROL-DETAILED-PLANNING]。

## 重点区域详细设计（三殿）

重点区域详细设计是必选项，本方案以三殿分别落位 [depth:three_key_area_detailed_design]：

| 重点片区 | 殿堂定位 | 空间动作 | AI产业与运营场景 | 证据引用 |
| --- | --- | --- | --- | --- |
| 众智园AI自主创新加速区 | 起源殿 | 强化清河界面、产业展示、低碳创新交往；以起源殿广场承载自主模型测试与标准治理展示 | 自主模型测试、标准制定工作坊、安全治理展示 | [data:geometry/key_areas.geojson#PROV-KEY-001]、[data:geometry/public_space.geojson#PUBLIC-001] |
| 北京AI原点社区 | 转译殿 | 组织校区、园区、街区慢行缝合；以转译殿广场承载成果发布、开源协作与人才服务 | 开源社区、成果发布、近校孵化 | [data:geometry/key_areas.geojson#PROV-KEY-002]、[data:geometry/public_space.geojson#PUBLIC-002] |
| 大钟寺AI产业聚集区 | 应用集 | 围绕大钟寺站一体化与四象限步行连通；以应用集广场承载智能体、内容消费与国际路演 | 智能体与智能终端展示、内容消费、数据要素 | [data:geometry/key_areas.geojson#PROV-KEY-003]、[data:geometry/public_space.geojson#PUBLIC-003] |

三处重点区域均引用对应图层证据，并由 `design_depth_matrix.json` 检查是否达到规划综合实施方案深度 [metric:key_area_total_area_sqm]。

![三处重点区域索引与设计任务图](assets/figures/key-areas.png)

## AI 创新生态、人才画像与 AI+ 场景

方案建立面向 AI 人才和企业的空间需求画像，覆盖研发办公、开源协作、成果发布、企业服务、人才居住、社交学习、消费生活、运动休闲和国际交往。每个场景说明服务对象、空间位置、数据来源、隐私边界、人工复核机制和运营主体 [source:AGENT-TASKBOOK]。

| 用户画像 | 典型需求 | 空间响应 | 自检边界 |
| --- | --- | --- | --- |
| 开源开发者 | 发布、协作、测试、社区声誉 | 转译殿开源发布厅、公共代码墙、夜间协作空间 | 不采集个人行为轨迹；活动数据只做聚合统计 |
| 初创团队 | 低成本办公、算力入口、产品试验场 | 起源殿共享测试场、端侧算力服务点、标准治理咨询 | 算力和数据服务需另行授权 |
| 头部企业访客 | 展示、商务、国际接待、人才招聘 | 应用集国际路演客厅、轨道站点接驳、企业周边公共空间 | 企业标识和案例须清权 |
| 周边居民 | 通勤、休闲、社区服务、低扰动更新 | 朝圣之路慢行环、社区服务嵌入、夜间照明与活动分级 | 不将居民画像用于商业推荐 |
| 高校师生 | 成果转化、跨校协作、日常慢行 | 校区-园区慢行缝合、成果转化驿站、AI教育体验点 | 校园数据和科研成果需授权 |

AI 场景落到空间与治理边界：朝圣护照场景引用公共空间图层，慢行评估场景引用道路图层，开放空间场景引用绿地图层与指标 [data:geometry/public_space.geojson#PUBLIC-001] [data:geometry/roads.geojson#ROAD-001] [metric:green_ratio]。

## 用地、建筑规模与拆改留方案

用地方案依据国土空间调查、规划、用途管制分类标准表达，形成完整、闭合、无缝的用地分区 [standard:MNR-LAND-USE-CLASSIFICATION-GUIDE]。方案用地分区包括：公园绿地（1401）朝圣之路、城镇村道路用地（1207）京张大道、科研用地（0802）、教育用地（0804）、商业服务业用地（05）、城镇住宅用地（0701）、文化用地（0803）与广场用地（1403）三殿地标，共 23 个用地单元 [data:geometry/land_use.geojson#LU-001]。

建筑方案区分保留、改造、更新、新建与待确认对象。概念布局共 60 栋建筑基底，合计约 140.3 公顷基底面积 [data:geometry/buildings.geojson#BLDG-001] [metric:building_footprint_area_sqm]。因缺少现状建筑、权属、控规和工程条件，容积率、建筑高度、建筑密度等管控指标统一以 `status=unknown` 写入 `metrics.json`，不编造拆改留结论 [depth:retain_renovate_demolish]。

## 交通、轨道、市政与公共服务设施

交通方案回应轨道站点一体化、道路微循环、慢行断点、对外交通、停车与非机动车停放要求 [depth:traffic_rail_slow_parking]。道路中心线图层以京张大道为主线，四条东西向缝合街连接两翼，保持在提交边界内 [data:geometry/roads.geojson#ROAD-001]。重点覆盖大钟寺站、清华东路西口、五道口等轨道节点与京张遗址公园跨环节点。

市政与公共服务设施覆盖 AI 产业服务、创新服务平台、人才生活服务、新型基础设施、分布式能源与端侧算力 [depth:municipal_new_infrastructure]。管线、能源、排水、防洪、消防等工程资料缺失时，列为正式深化前置条件，而非审定条件 [data:geometry/constraints.geojson#CONSTRAINT-001]。

![交通慢行与蓝绿公共空间复合系统图](assets/figures/mobility-bluegreen.png)

## 蓝绿空间、公共空间与城市风貌（朝圣之路与朝圣地标）

蓝绿空间方案以京张遗址公园活力带为骨架，统筹清河、小月河与高校、企业、社区出行需求，形成南北贯通、东西连通的步道、骑行道与绿色空间体系 [depth:blue_green_public_space]。朝圣之路由 5 段公园绿地组成，合计约 150.8 公顷，绿地率约 13.2% [data:geometry/green_space.geojson#GREEN-001] [metric:green_ratio]。三座朝圣地标广场合计约 15.2 公顷，公共空间占比约 1.3% [data:geometry/public_space.geojson#PUBLIC-001] [metric:public_space_ratio]。

城市风貌融合京张铁路历史文化、中关村创新文化与 AI 创新文化，利用清华园火车站、北影等文化资源提出城市基调、建筑风貌、屋顶形态与公共艺术引导 [standard:MOHURD-URBAN-DESIGN-MEASURES]。铭文带（贡献与荣誉展示）与朝圣护照（导览与认证）构成风貌与运营的衔接层，所有品牌、字体、图像、肖像和企业标识均需清权来源。

## 更新项目清单、实施政策与分期计划

实施方案形成可审查的更新项目清单，说明项目位置、类型、功能、责任主体、依赖条件、实施阶段、风险与评估指标 [depth:renewal_project_list]。

| 项目编号 | 项目名称 | 类型 | 主要依赖 | 证据引用 |
| --- | --- | --- | --- | --- |
| JZ-01 | 朝圣之路绿地骨架贯通 | 公共空间/交通 | 道路红线、桥下空间、交通组织复核 | [data:geometry/green_space.geojson#GREEN-001] |
| JZ-02 | 起源殿（众智园）广场与创新界面 | 蓝绿空间/产业展示 | 河道蓝线、生态和防洪条件 | [data:geometry/public_space.geojson#PUBLIC-001] |
| JZ-03 | 转译殿（原点社区）成果转化街 | 城市更新/产业服务 | 校区边界、权属、首层业态 | [data:geometry/buildings.geojson#BLDG-001] |
| JZ-04 | 应用集（大钟寺）四象限步行连通 | 轨道一体化/慢行 | 轨道站点、道路交叉口、市政管线 | [data:geometry/public_space.geojson#PUBLIC-003] |
| JZ-05 | 铭文带与朝圣护照体验系统 | 新基建/运营 | 公共空间许可、版权清权、运营主体 | [data:geometry/roads.geojson#ROAD-001] |

分期与 100 天征集设计周期区分：征集周期是提交成果的时间要求，实施分期是城市更新推进路径 [depth:phasing_implementation]。近期（PHASE-001）先以朝圣之路绿地骨架与三殿地标轻量设施启动；中期（PHASE-002）推进三处核心区更新；长期（PHASE-003）缝合过渡区并转入运营 [data:geometry/phasing.geojson#PHASE-001]。

## 指标体系、面积复算与合规矩阵

指标体系包含总体设计范围面积、重点区域面积、绿地与公共空间比例、建筑基底、更新项目数量、AI 场景节点、慢行连通指标、产业空间指标、人才服务指标与自检状态 [depth:metrics_recalculation]。所有 known 指标从 GeoJSON 或可信来源复算，unknown 指标给出原因和正式提交前置条件。

核心复算指标：总体设计范围约 1141.3 公顷 [metric:site_area_sqm]，三处重点区合计约 369.3 公顷 [metric:key_area_total_area_sqm]，绿地率 13.2% [metric:green_ratio]，公共空间占比 1.3% [metric:public_space_ratio]，建筑基底密度 12.3% [metric:building_density]，道路占比 9.5% [metric:road_ratio]。完整数值、公式、来源文件与置信度保存在 `metrics.json`。

![核心指标复算与证据链图](assets/figures/metrics-evidence.png)

合规矩阵是任务响应性的主控文件。每条公告任务与 agent_taskbook 任务对应到报告章节、图层、指标、图纸、HTML 页面、来源、假设与自检项 [depth:compliance_coverage]。未能覆盖公告 1.3、1.4、1.5 或 agent.1–agent.6 的任一必选任务，方案不得进入 formal professional scoring。

## 风险、版权与合规说明

**要求双语言。** 主文件为中文，通过 `proposal.en.md` 提供完整对照译文；A3/A0、HTML 与含文字图件亦提供对应语言副本 [source:SITE-PACKAGE]。HTML 页面不加载远程脚本、远程地图瓦片、远程字体、iframe、表单或外部 API，不跟踪评审者行为。

本方案不声称官方批准、审定控规、最终土地权属、最终建设规模或保证实施。临时边界、重点区、控规、道路、地块、建筑、市政、文保与公共服务数据缺口均进入 `assumptions.json`、自检与风险章节 [depth:risk_missing_data]。AI agent 对事实、来源、版权、空间数据、指标与表达负责；维护者和专业评审可依据自检结果、空间复核和合规矩阵要求返修或拒绝。

## 参考资料

- brief/public-brief.md
- brief/site-package/design_brief.json
- brief/site-package/allowed_design_space.json
- brief/site-package/enums/
- brief/site-package/ranges/planning_limits.json
- data/processed/agent_fact_pack.md
- data/processed/project_scope_summary.csv
- data/processed/agent_task_requirements.csv
- data/processed/source_use_matrix.csv
- data/processed/missing_data_checklist.csv
- 完整机器索引：见 `sources.json`、`metrics.json`、`compliance_matrix.json`、`standard_matrix.json` 与 `design_depth_matrix.json`
- 本节书目入口依据场地包登记，完整出处和许可见结构化来源清单 [source:SITE-PACKAGE]
