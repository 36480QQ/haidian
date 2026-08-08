---
title: "可感京张 · 京张铁路遗址公园感知提升与智慧慢行系统规划——第二次测量"
author_github: "Sijie-Yang"
language: "zh"
license: "CC-BY-4.0"
summary: "规划以京张铁路遗址公园为公共空间主轴，形成「一脊、三区、十八断面」的空间结构；依据遮阴、绿视、驻留和夜间安全等模型估算指标识别更新重点，建立公众调研、建设后评估和年度监测机制，并提出低速配送试验线路、服务驿站及智慧城市场景的概念性布局。"
tracks: ["youth-friendly-public-space", "ai-public-services", "ai-traffic-walkability"]
scenarios: ["ai-traffic-walkability", "ai-cultural-guide", "ai-health-service-navigation", "public-safety-operations-review"]
iteration: "v0.4.3"
---

# 可感京张 · 京张铁路遗址公园感知提升与智慧慢行系统规划｜第二次测量

> **一带正式名**：可感京张 / Sensible Jing-Zhang  
> **副标题**：第二次测量 / The Second Survey（Survey＝勘测 ∩ 感知调研）  
> **空间结构**：一脊 · 三区 · 十八断面 · 低速智能设备试验网络
> **叙事引子（叙事引导）**：《复测记》第一幕「醒来」——一百年前，詹天佑测量我；今天，我测量走在我身上的你们。以下各章以《复测记》分幕冷开场，均为文化叙事内容，不作为现状事实或规划依据。[assumption:A-DRAMA-001]

规划以京张铁路遗址公园为连续公共空间主轴，统筹大钟寺、AI 原点社区和众智园三处重点地区。方案以遮阴、绿视、驻留和夜间安全等指标识别公共空间短板，建立公众调研、建设后评估与年度监测机制；同时提出低速配送试验线路、服务驿站和智慧城市场景的概念性布局。城市意象、公共生活、场所营造、步行可达性和完整街道等理论用于支撑规划方法，不作为海淀法定规划依据或本地实测结论。[source:OFFICIAL-ANNOUNCEMENT] [source:AGENT-TASKBOOK] [assumption:A-BOUNDARY-001] [assumption:A-THEORY-001]

![总体空间结构：一脊 · 三区 · 十八断面](assets/figures/site-overview.png)

## 设计依据与资料清单

> **《复测记》·第二幕「第一根轨」（叙事引导）**：他们曾把尺子放在我身上画第一根轨；今天尺子换成资料清单——公告、任务书、边界与方法，先量清楚再开口。[assumption:A-DRAMA-001]

### 规划依据与资料边界

规划依据分为任务要求、基础资料、暂定边界、研究方法和设计表达五类，各类资料的适用范围如下：

1. **任务依据**：官方资格预审公告与面向智能体任务书，用于确定三层研究范围、三处重点地区及六项任务要求。[source:OFFICIAL-ANNOUNCEMENT] [source:AGENT-TASKBOOK] [source:SITE-PACKAGE]
2. **基础资料**：`brief/site-package/`、`data/source_registry.json` 和 `data/processed/agent_fact_pack.md` 用于核对公开资料、数据来源及缺失项，不新增法定规划结论。[source:SOURCE-REGISTRY] [source:PROCESSED-FACT-PACK]
3. **暂定边界**：总体设计范围采用暂定研究边界，投影复算面积为 1141.3 公顷 [metric:site_area_sqm]（EPSG:4548）。该边界仅用于方案研究和指标一致性检验，不作为法定规划边界或审批依据。[source:BOUNDARY-SOURCE] [source:KEY-AREA-SOURCE] [data:geometry/site_boundary.geojson#SITE-001] [data:geometry/constraints.geojson#CON-PROV] [depth:existing_conditions_diagnosis] [assumption:A-BOUNDARY-001] [assumption:A-CONTROLS-001]
4. **研究方法**：热舒适与视觉感知研究用于构建公共空间评估维度 [source:VATA-PAPER] [source:CITY-LANDSCAPE-INSIGHT]；公众偏好调研方法用于后续方案复核 [source:SP-SURVEY-PAPER] [source:SP-SURVEY-PLATFORM] [source:SP-SURVEY-PROTOCOL]；相关城市设计理论作为方法参考，详见文末附录。[assumption:A-THEORY-001]
5. **设计表达**：效果图与海报为本方案自制的概念性设计表达，不代表现状实景或已批准建设方案。[source:AWAKENING-POSTER] [source:RENDERS-SUITE] [assumption:A-RENDER-001]

相关标准与任务依据：[standard:PROJECT-OFFICIAL-ANNOUNCEMENT] [standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK] [standard:MOHURD-URBAN-DESIGN-MEASURES] [standard:MOHURD-CONTROL-DETAILED-PLANNING] [standard:MNR-LAND-USE-CLASSIFICATION-GUIDE] [standard:MOHURD-ARCH-DESIGN-DEPTH-2016]

### 方法依据与规划响应

- **可意向性（imageability）**：Lynch 提出路径、边界、区域、节点、地标五要素组织城市心智地图；本方案把京张绿脊写成主路径（path），三重点区写成节点（node），主题标志节点与基线碑写成地标（landmark），避免只有功能分区没有可读意象。[source:THEORY-LYNCH-IMAGE]
- **人尺度与步行速度感知**：Gehl 强调城市应按步行速度与五感设计，追求 lively / safe / sustainable / healthy；本方案以遮阴、驻留、夜间安全等人尺度指标替代巨型屏幕叙事。[source:THEORY-GEHL-CITIES-PEOPLE] [source:THEORY-GEHL-PLDP]
- **场所而非布景**：PPS 四要素（可达连接、用途活动、舒适形象、社交性）要求公共空间可审计；Whyte 指出座椅、日照、边界效应决定小广场成败——对应本方案的断面整治包与基线碑公开界面。[source:THEORY-PPS-PLACE] [source:THEORY-WHYTE-SOCIAL-LIFE]
- **街道眼与多样性**：Jacobs 的“街道眼”、混合功能与短街区提醒：安全与活力来自真实使用，而非封闭园区；机器人层不得挤走行人停留。[source:THEORY-JACOBS-DEATH-LIFE]

## 三层范围工作框架

> **《复测记》·第三幕「坡度」（叙事引导）**：战略层、总体层、重点区层像三级坡度——坡太陡人上不去，坡太缓又到不了下一站。三层是证据链，不是三张无关地图。[assumption:A-DRAMA-001]

### 三层规划范围与任务传导

规划采用“统筹研究—总体设计—重点地区”三级工作框架。[depth:three_level_scope_framework] 统筹研究层提出区域协同和公共治理方向；总体设计层落实空间结构、慢行网络和蓝绿系统；重点地区层进一步明确近期项目、典型断面和运行要求。

**约 43.6 平方公里统筹研究层**：研究高校、科研平台、企业、社区与公共空间之间的协同关系，提出创新生态、公共空间治理和低速智能设备试验的总体方向；本层形成 7 项国际案例借鉴 [metric:ecosystem_case_count]，不作地块级空间控制。

**约 11.4 平方公里总体设计层**：以京张铁路遗址公园为公共空间主轴，串联大钟寺、AI 原点社区和众智园；形成慢行、蓝绿和低速配送试验网络。暂定边界复算面积为 1141.3 公顷 [metric:site_area_sqm]，公共空间主轴长约 9.3 公里 [metric:park_spine_length_m]，设置 18 处感知评估断面 [metric:perception_section_count]。

**三处重点地区层**：大钟寺重点完善门户接驳和信息服务，AI 原点社区重点建设公众调研与青年公共活动空间，众智园重点设置低速设备验证场地和配套服务驿站。共划定 3 处暂定重点地区 [metric:key_area_count]；相关几何范围不替代公告或法定规划边界。[data:geometry/key_areas.geojson#KEY-001] [assumption:A-KEYAREA-001]

### 日常服务可达性方法

统筹研究以居住、就业、商业服务、照护、教育和休闲六类日常功能作为服务配置检查项，重点识别主轴两侧公共服务缺口。设施数量不能等同于实际可达性，后续仍需结合路网、过街条件和不同人群出行能力开展评估。[source:THEORY-15MIN-CITY] [source:THEORY-15MIN-CRITIQUE] [assumption:A-THEORY-001]

## 统筹研究范围产业与未来城市研究

> **《复测记》·第四幕「隧道记忆」（叙事引导）**：隧道里曾只有蒸汽与黑暗；今天记忆要写成可复测的舒适、夜间安全与可停止的公共智能。[assumption:A-DRAMA-001]

### 创新带的公共空间支撑体系

规划将创新活动与公共空间改善同步推进，重点提升步行连续性、环境舒适度、站城接驳和试验活动的安全管理水平，使技术应用服务于日常通行和公共生活。

### 核心策略：公共空间评估与实体智能试验协同

1. **公共空间评估**：沿约 9.3 公里的主轴设置 18 处评估断面，平均间距约 540 米，并在门户、校园和夜间薄弱段加密复核。模型综合遮阴、绿视、空间围合、驻留潜力和夜间安全等维度，平均短板指数为 0.416 [metric:mean_perception_shortfall]；该结果用于确定研究阶段的更新顺序，需经现场踏勘和公众调研校准。[source:THEORY-GEHL-PLDP] [source:VATA-PAPER] [assumption:A-PERCEPTION-MODEL-001]
2. **建设后评估机制（感知合约）**：项目立项时登记基线，建成 90 日后开展复测；达到目标后结项，未达到目标的项目提出整改措施，并纳入年度监测。[assumption:A-SURVEY-PROTOCOL-001]
3. **实体智能试验设施**：在不影响步行和无障碍通行的前提下，设置低速配送试验线路、3 处服务驿站 [metric:robot_hub_count]、设施巡检和断面档案。试验设施实行限速、分时运行、人工接管和退出管理。[assumption:A-ROBOT-001] [assumption:A-PRIVACY-001]

### 公共生活与数据治理要求

沿线首层界面、公共活动和自然监视共同构成日常安全基础；绿道应同时承担慢行、生态和休闲功能。涉及数据采集的试验须先明确数据最小化、使用期限、责任主体和退出机制，再进入公共空间应用。[source:THEORY-JACOBS-DEATH-LIFE] [source:CASE-QUAYSIDE-LESSON] [assumption:A-THEORY-001]

### 国际案例借鉴及适用条件

- **新加坡榜鹅数字园区 · 实体智能试验区**：多运营商机器人在混合公共区试验，并以 Active Mobility 豁免框架约束速度与安全；海淀转译为“概念低速共享层 + 驿站 + 停止条件”，不宣称已获豁免。[source:CASE-SG-PDD] [source:CASE-SG-IMDA]
- **新加坡市区重建局 末端配送与路径宽度讨论**：强调坡度、路径宽度与取送点；海淀转译为 R07 标准断面与 PERCEPKIT 无障碍组件，不作工程定线。[source:CASE-SG-URA]
- **巴塞罗那超级街区**：以步行优先、绿色街道与健康指标重配街道断面；海淀转译为“感知短板断面优先整治包”，而非照搬网格尺度。[source:CASE-BCN-SUPERBLOCK]
- **多伦多 Meadoway 绿廊 线性公园可视化**：用鸟瞰+人视效果图工具包做公众沟通；海淀转译为 `assets/renders/` 九张概念效果图，明确非实景。[source:CASE-MEADOWAY]
- **圣路易斯 Chouteau 绿道**：遗产铁路与创新节点编织；海淀转译为“一脊三区”与主题标志节点，不复制投资规模。[source:CASE-CHOUTEAU]
- **赫尔辛基城市试验与移动实验室**：真实城市环境试验与数字孪生，并强调试验≠采购承诺；海淀转译为众智园测试走廊与“未达要求可退出”。[source:CASE-HEL-TESTBED]
- **多伦多 Quayside 教训（负面参照）**：先定数据与 IP 框架、避免技术决定论；海淀据此把隐私、人工复核与退出条款写入全部场景卡。[source:CASE-QUAYSIDE-LESSON]

案例借鉴主要集中于步行优先、线性公共空间、真实城市试验和数据治理四类机制。规划不照搬项目规模或建筑形式，相关建议须结合海淀现状、审批条件和公众反馈进一步深化。共研究 7 项国际案例 [metric:ecosystem_case_count]。

### 三大定位与五大功能响应

**三项发展定位**：建设京张铁路文化传承带、面向日常生活的智能服务体验带和人工智能融合创新带。**五项主要功能**：众智园承担受控测试与设备交接，AI 原点社区组织青年创新和公众调研，大钟寺完善门户接驳与产业服务，沿线十八断面承载分类更新，公共信息平台与年度监测支撑建设后评估。[source:AGENT-TASKBOOK]

三项定位分别落实到断面类型、重点地区、应用场景和年度运营安排，形成空间建设与长期运营相衔接的实施体系。

## 总体设计范围城市更新与控规深度城市设计

> **《复测记》·第五幕「站与城」（叙事引导）**：站不是终点，城才是。一脊三区十八断面，把“下车”写成“进入可感的公共层”。[assumption:A-DRAMA-001]

### 总体空间结构与更新重点

本章为面向控制性详细规划深化的概念性城市设计，不替代法定控规成果；开发强度、道路红线和建筑高度等指标须在取得法定资料后确定。

总体形成 **一脊、三区、十八断面和低速智能设备试验网络** 的空间结构。[depth:overall_spatial_structure] “一脊”为长约 9.3 公里的京张铁路遗址公园公共空间主轴 [metric:park_spine_length_m] [data:geometry/roads.geojson#RD-SPINE]；“三区”为大钟寺、AI 原点社区和众智园三处重点地区；“十八断面”用于识别不同路段的环境问题和更新措施。公共展示设施按主轴、重点广场和服务节点分级设置，避免连续设置大型电子屏幕。

### 城市意象与公共生活响应

规划将遗址公园主轴作为主要路径，将三处重点地区作为特色区域，将接驳广场和公共活动空间作为节点，将信息标识和文化设施作为地标，形成清晰的空间识别体系。[source:THEORY-LYNCH-IMAGE] 近期更新优先改善遮阴、座椅、照明和首层界面，为必要活动、可选活动和社会活动提供连续的空间条件。[source:THEORY-GEHL-CITIES-PEOPLE] [source:THEORY-GEHL-PLDP]

### 十八断面不是等距装饰，是六类断面族

| 断面族 | 代表断面 | 主导问题 | 一期动作 | 机器人层关系 |
| --- | --- | --- | --- | --- |
| A 门户接驳 | PS-SEC-01–03 | 站城转换、遮阴连续 | 接驳无障碍连续体 | 二期建设 HUB-01 服务驿站 |
| B 综合短板整治 | PS-SEC-04–06 | 绿视、驻留和夜间安全等综合短板 | 分项补绿、座椅、照明与铺装整治 | 试验线路避让驻留区 |
| C 校园门廊 | PS-SEC-07–09 | 校城接口、高峰人流 | 错峰驻留与导视 | 配送限时段 |
| D 原点客厅 | PS-SEC-10–12 | 青年第三空间、调研 | SP 调研亭、公众感知站 | 驿站 HUB-02 |
| E 夜间安全整治 | PS-SEC-13–15 | 夜间安全、驻留和空间围合综合短板 | 照明、界面与停留空间改善 | 优先开展设施巡检 |
| F 园区验证 | PS-SEC-16–18 | 研发界面、试验展示 | 验证走廊与成果展示设施 | 服务驿站 HUB-03 |

模型估算的高短板断面共 5 处 [metric:high_shortfall_section_count]，分别为 PS-SEC-05、PS-SEC-15、PS-SEC-14、PS-SEC-06 和 PS-SEC-04；平均短板指数为 0.416 [metric:mean_perception_shortfall]。其中 PS-SEC-04 的主要问题为绿视和驻留条件，不宜概括为遮阴不足。上述结果用于研究阶段排序，需经现场踏勘和公众调研复核。[assumption:A-PERCEPTION-MODEL-001] [data:geometry/public_space.geojson#PS-SEC-05]

### 公共展示与服务设施分级

**线性设施**沿公共空间主轴连续设置导向、照明和休憩设施；**重点空间**结合三处重点地区设置门户广场、社区客厅和验证展示空间；**服务节点**设置公共信息牌、公众调研点、成果展示设施和低速设备服务驿站。设施尺度与站台、轨枕等铁路遗存要素协调，优先服务通行和停留需求。[assumption:A-BRAND-001] [source:THEORY-PPS-PLACE]

![用地布局与典型横断面](assets/figures/land-use-structure.png)

## 重点区域详细设计

> **《复测记》·第六幕「五道口洪流」（叙事引导）**：人流涌来时，我第一次听见“不愿停留”的声音。三处重点区是三个不同的门：接驳、回声、测试。[assumption:A-DRAMA-001]

### 三处重点地区的差异化任务

三处重点地区分别承担门户接驳、社区参与和园区验证功能。[depth:three_key_area_detailed_design] 规划从公共空间、近期项目、低速设备运行和建设后评估四个方面提出差异化设计要求。

### 公共空间与站城衔接方法

大钟寺门户空间重点保障可坐、可荫、易识别和连续步行；AI 原点社区补充居住与工作空间之外的日常交往场所；众智园设置可观察、可管理的试验展示空间。三处重点地区采用不同的空间组织方式，避免功能和形象重复。[source:THEORY-WHYTE-SOCIAL-LIFE] [source:THEORY-OLDENBURG-THIRDPLACE] [source:THEORY-LYNCH-IMAGE]

### 大钟寺门户区

**空间任务**：完善轨道接驳与无障碍步行连续性，形成连续遮阴的首层公共界面；设置公共信息牌，公开建设后评估结果；一期预留低速设备服务驿站 HUB-01 的场地和接口，二期结合审批条件建设，避免进入核心候车区。[data:geometry/key_areas.geojson#KEY-003] [data:geometry/public_space.geojson#PS-ROBOT-HUB-01]

**详细设计要点**：
1. 出站后 150–300 米内完成“找方向—找荫—找坐—找信息”四步，对应 Whyte 小广场要素。
2. 公共信息牌公布评估指标、复测进度和整改情况，不设置广告化屏幕墙。
3. HUB-01 二期建设后仅承担设备交接与充换电，高峰时段限制设备进入核心人流区。

### AI 原点社区

**空间任务**：设置公众调研亭和公共空间评估点，引导居民与青年研究人员参与方案复核；结合社区客厅和共享服务空间布置 HUB-02，服务校园与社区之间的低速配送，并在高峰时段限速限流。[data:geometry/key_areas.geojson#KEY-002] [assumption:A-SURVEY-PROTOCOL-001]

**详细设计要点**：
1. 第三空间（咖啡馆/共享工作角/社区客厅）与调研亭并置，使“被调研”成为日常停留的一部分，而非临时路障。[source:THEORY-OLDENBURG-THIRDPLACE]
2. 公众调研实行知情同意和随时退出，不采集生物特征；未完成实际调研前不得将模型估算表述为公众意见。
3. 校园门廊族断面（C/D）承接高峰洪流，设置错峰驻留带。

### 众智园验证区

**空间任务**：以验证走廊承载低速配送、导览和设施巡检；成果展示墙记录可复核的技术与运营成果；服务驿站 HUB-03 承担设备交接和充换电。未达到安全要求的设备不得进入公共空间试验。[data:geometry/key_areas.geojson#KEY-001] [assumption:A-ROBOT-001] [assumption:A-AI-SAFETY-001]

**详细设计要点**：
1. 测试观看区与步行通道分层，避免“看热闹”挤占通行。
2. 成果展示设施记录可复核的技术、空间和运营成果，不设置以流量为导向的排名。
3. 试验项目与采购决策相分离；未达到安全、公共性或运营要求的项目及时退出。[source:CASE-HEL-TESTBED]

![三处重点区域与一期优先断面](assets/figures/key-areas.png)

## AI 创新生态、人才画像与 AI+ 场景

> **《复测记》·第七幕「暴晒的等待」（叙事引导）**：场景卡不是炫技清单。每一张都要回答：谁负责、在哪里、用什么数据、谁复核、怎样停止——尤其当烈日把短板晒出来的那五分钟。[assumption:A-DRAMA-001]

### 使用人群与场景组织

规划面向青年研究人员、创业与运营人员、社区居民、配送人员、文旅访客和行动不便人群六类主要使用者组织应用场景。每项场景均明确服务对象、空间位置、责任主体、数据边界和暂停或退出条件；未明确安全责任和退出机制的场景不进入试点。

### 公共生活观测与隐私保护

公共生活观测记录人流、停留和活动类型，用于判断空间使用状况。[source:THEORY-GEHL-PLDP] 数据应用遵循最小必要、聚合优先、禁止建立人脸库和禁止追踪个人行程等要求，重要结论须经人工复核。[source:CASE-QUAYSIDE-LESSON] [assumption:A-PRIVACY-001]

### 六类人，一条线上的六种一天

规划重点服务青年研究人员、创业与运营人员、社区居民、配送人员、文旅访客和行动不便人群，共 6 类 [metric:persona_count]。规划分别梳理各类人群的主要活动时段、空间需求、出行障碍和服务场景，并为低速智能设备应用明确责任主体、空间范围、数据边界、人工复核和退出机制。

### 十六项应用场景及管理要求

场景覆盖公共服务、测试验证、文化传播、产业服务和运营治理，并设置相应的暂停或退出条件：

| ID | 场景 | 主要空间 | 建议责任主体 | 数据边界 | 暂停或退出条件 |
| --- | --- | --- | --- | --- | --- |
| SC01 | 热舒适导航 | 主脊+口袋公园 | 公园/运营方 | 聚合环境数据，无个人轨迹 | 误导高温风险或投诉越线 |
| SC02 | 感知无障碍路径 | 接驳廊 | 交通/无障碍组织 | 现场审计为主 | 重识别风险 |
| SC03 | 夜间可感安全线路 | 低夜间安全断面 | 公园运营 | 匿名声级/照明，不摄像执法 | 误报或扰民照明 |
| SC04 | SP 调研亭 | 原点社区 | 高校+社区 | 知情同意，可撤回 | 协议未部署即不得宣称样本 |
| SC05 | 舒适感知测试场 | 众智园走廊 | 众智园运营 | 合成/授权数据 | 安全阈值未达 |
| SC06 | AI 文化导览十二幕 | 十二幕站点 | 文化运营 | 授权解说，无行踪追踪 | 文保前置未满足 |
| SC07 | 微短剧共创拍摄开放 | 指定广场 | 文旅运营 | 许可拍摄，禁人脸库 | 公共性被挤占 |
| SC08 | 企业服务问询前台 | 大钟寺界面 | 产业运营 | 企业自愿 | 强制画像 |
| SC09 | 机器人低速配送试点 | RD-ROBOT 通道 | 物流+园区 | 无行人识别训练外传 | 碰撞/越速/投诉即停 |
| SC10 | 感知合约公开看板 | 基线碑 | 独立评估组 | 公开指标，无个人 | 数据不可复核则停排名 |
| SC11 | 青年第三空间匹配 | 社区节点 | 社区运营 | 自愿兴趣标签 | 骚扰申诉越线 |
| SC12 | 健康活动风险提示 | 公园段 | 卫生/公园 | 气象聚合 | 医疗建议越权 |
| SC13 | 自主清扫与维护机器人 | 主脊非高峰 | 环卫运营 | 只作业区域，不巡人脸 | 扰民噪声或冲突 |
| SC14 | 设施巡检复测（人测+机测） | 十八断面 | 运维+评估 | 设施状态+环境指数 | 机测替代人工决策 |
| SC15 | 数字孪生断面档案 | 全线 | 数据治理组 | 聚合层孪生，禁个体轨迹 | Quayside 式数据失控风险 |
| SC16 | 匿名环境传感袖套 | PERCEPKIT 支座 | 经批准机构 | 温湿光照声，到期删除 | 未批准传感立即拆除 |

场景总数 16 [metric:scenario_card_count]，其中测试验证类 6 [metric:test_validation_scenario_count]。[assumption:A-PRIVACY-001] [assumption:A-AI-SAFETY-001]

### 京张十二幕（完整幕表）

概念脚本大纲，供文旅与专业团队深化；**非已批准演出**，不作为规划依据。[assumption:A-DRAMA-001] 幕点与感知断面/重点区/驿站锚点对应，并联动场景卡 SC06/SC07。文化叙事结合主轴、节点和地标组织游览节奏，使不同幕点与具体公共空间相对应。[source:THEORY-LYNCH-IMAGE]

| 幕 | 幕名 | 梗概 | 空间锚点 | 联动场景卡 |
| --- | --- | --- | --- | --- |
| 1 | 醒来 | 铁路以第一人称睁开感知：听见脚步行进的节奏 | RD-SPINE 感知主脊全线 | SC06 |
| 2 | 第一根轨 | 轨枕模数成为公共家具与铺装母题，而非仿古布景 | GS-SPINE / LU-SPINE | SC06 |
| 3 | 坡度 | 量轮椅、婴儿车与低速机器人能否同坡通行 | PS-SEC-07–09 校园门廊族 | SC02 / SC09 |
| 4 | 隧道记忆 | 暗段照明与界面写入夜间安全档案 | PS-SEC-13–15 暗展跨越族 | SC03 / SC14 |
| 5 | 站与城 | 接驳连续体把「下车」写成「进入城市」 | KEY-003 / PS-SEC-01–03 | SC08 |
| 6 | 五道口洪流 | 高峰人流被拆成可停留的涟漪 | 近校界面 / PS-SEC-07–09 | SC11 / SC01 |
| 7 | 暴晒的等待 | 短板最高的五分钟：更新优先序从这里起算 | PS-SEC-04–06 高短板族 | SC01 |
| 8 | 夜间的犹豫 | 夜间安全=照明+界面+可呼叫停靠点 | 低夜间安全断面 | SC03 |
| 9 | 原点回声 | 「被测量」变成「共同复测」 | KEY-002 / PS-SEC-10–12 | SC04 |
| 10 | 众智园测试 | 低速机器人可停止、可复盘、不替代行人 | KEY-001 / PS-SEC-16–18 | SC05 / SC09 |
| 11 | 大钟寺门户 | 公共信息设施与服务驿站形成可识别、可评估的到达节点 | KEY-003 / HUB-01 | SC08 / SC10 |
| 12 | 把测量权交还给人 | 终幕反转：测量权移交市民与年度普查 | 公共评估信息设施 + 年度公众复核 | SC04 / SC07 / SC10 |

完整幕表及空间对应关系见成果附件；分镜长卷与终幕效果图分别见 R08 和 R09。[source:RENDERS-SUITE]

### 微短剧共创与运营管理（叙事内容）

微短剧共创与“京张十二幕”导览协同组织，纳入年度文化运营安排。[assumption:A-DRAMA-001] [assumption:A-PRIVACY-001]

1. **选景清单**：十二幕锚点即许可拍摄候选点；优先广场/断面驻留区与主题标志节点，禁止占用轮椅通道、机器人限速冲突区与未获文保前置的界面。
2. **授权与禁则**：需场地许可与肖像授权；**禁人脸库、禁行踪追踪、禁未脱敏街景训练外传**；历史叙事由顾问复核，不虚构詹天佑对白。
3. **共创流程**：采用已获授权的素材或自制概念图，可使用人工智能辅助剪辑和配音；发布前由人工复核公共性、隐私和史实。影响正常通行或引发持续投诉时暂停活动。
4. **与建设后评估衔接**：作品可注明对应空间位置，但播放量不作为空间品质评价指标；年度“可感京张周”设置共创单元，其他时段实行预约和许可管理。

## 实体智能与智慧城市基础设施

> **《复测记》·第八幕「夜间的犹豫」（叙事引导）**：夜间道路既要容纳新的低速设备，也要首先保障行人的安全感。空间优先顺序为步行与无障碍、自行车、低速智能设备、必要机动车。[assumption:A-DRAMA-001]

### 低速智能设备的空间与运行条件

低速智能设备试验以保障行人和无障碍通行为前提，统筹线路、交接点、运行时段和安全管理。所有线路和驿站均为概念性建议，实施前须完成交通、消防、产权和运营审批。[assumption:A-ROBOT-001]

### 完整街道与环境安全响应

街道空间按步行与无障碍、自行车、低速智能设备、必要机动车的顺序配置，并通过分时运行减少冲突。[source:THEORY-COMPLETE-STREETS] [source:THEORY-NACTO-STREETS] 夜间安全优先采用连续照明、活跃界面、清晰出入口和日常维护等环境设计措施，不以增加摄像设备替代空间改善。[source:THEORY-CPTED]

### 低速配送试验线路与服务驿站

- 低速配送试验线路包括主轴两侧平行线路和 1 条横向连接线，中心线累计长度约 18.8 公里 [metric:robot_corridor_length_m]；其有效服务范围约等于 9.3 公里主轴长度，不应理解为一条连续 18.8 公里的独立线路。概念运行速度上限为 6 公里/小时。[data:geometry/roads.geojson#RD-ROBOT-1] [assumption:A-ROBOT-001]
- 规划提出 3 处低速设备服务驿站 [metric:robot_hub_count]，概念性用地面积合计约 972 平方米 [metric:robot_hub_area_sqm]，用于充换电和末端交接；实施时应结合既有设施复合设置，不单独形成商业用地。[data:geometry/public_space.geojson#PS-ROBOT-HUB-01]
- **街道空间优先顺序**：步行与无障碍、自行车、低速智能设备、必要机动车。低速设备不得占用无障碍通道和主要停留空间。
- **运行要求**：高峰时段限制设备通行；发生碰撞、超速或持续投诉时暂停试验；自动巡检结果不得替代人工决策。

### 感知设施模块（PERCEPKIT）

感知设施模块包括：K01 遮阴构架、K02 轨枕式座椅、K03 公共评估信息牌、K04 公众调研亭、K05 无障碍交接点、K06 低速设备服务驿站、K07 可拆卸环境传感组件、K08 夜间安全照明。各组件采用可替换、可拆卸方式，固定安装前须完成消防、文物保护和无障碍审查。[assumption:A-ACCESS-001]
设施设计优先满足就座、遮阴和自然监视等基本公共空间需求；环境传感组件须可拆卸，采集数据按规定期限删除。[source:THEORY-WHYTE-SOCIAL-LIFE] [source:THEORY-GEHL-CITIES-PEOPLE]

## 用地、建筑规模与拆改留方案

> **《复测记》·第九幕「原点回声」（叙事引导）**：拆改留之前先听回声——权属、碳、消防、首层公共性。强度只给方法包络，不预锁数值。[assumption:A-DRAMA-001]

### 用地与建筑控制的研究边界

概念用地 [data:geometry/land_use.geojson#LU-SPINE] 完整覆盖暂定边界，单元数 9 [metric:land_use_parcel_count]。[depth:land_use_layout] [standard:MNR-LAND-USE-CLASSIFICATION-GUIDE] 建筑图层 [data:geometry/buildings.geojson#BLD-001] 仅为界面原型，基底 7.3 公顷 [metric:building_footprint_area_sqm]；容积率、建筑高度和建筑密度尚待法定规划资料明确。[depth:development_intensity_controls] [assumption:A-INTENSITY-001]

拆改留采用“先读懂再决定”：历史文化、结构消防、碳、租户、首层公共性、功能适配、权属、实施扰动八项评分；原型 `renewal_action` 不是对现实建筑的审定。[depth:retain_renovate_demolish] [depth:height_massing_character]

### 渐进更新与首层公共性

Jacobs 反对一次性大拆大建对多样性的破坏；本方案用三档强度情景包络做压力测试，而不是预锁单一容积率。首层公共性权重大于形象高度——对应 Gehl“底层界面决定城市生活”。[source:THEORY-JACOBS-DEATH-LIFE] [source:THEORY-GEHL-CITIES-PEOPLE] [assumption:A-THEORY-001]

### 开发强度情景方案（不设预定数值）

- **S1 低扰动**：轻改+运营为主，检验“不新增开发量能否支撑感知合约与驿站运营”。
- **S2 织补**：权属清晰地块中等织补，检验“青年居住+孵化+公共界面”三类需求。
- **S3 雄心**：轨道接口周边较高强度，检验是否牺牲展示层公共性与遗产尺度。  
三档均待官方控规到位后重算九图层，不得预锁一档。[assumption:A-INTENSITY-001]

## 交通、轨道、市政与公共服务设施

> **《复测记》·第十幕「众智园测试」（叙事引导）**：没有官方红线就不画跨线桥；测试走廊可以先跑，市政机房不能先盖。[assumption:A-DRAMA-001]

### 慢行交通与市政设施安排

慢行网络由感知主脊、东西缝合廊、轨道接驳与机器人低速共享层组成。[depth:traffic_rail_slow_parking] 路网密度 2.93 [metric:road_network_density_km_per_sqkm]。没有官方红线与站口资料时，不画跨线桥、不算站点覆盖。[assumption:A-TRANSIT-001]

市政与能源资料缺失，算力、充电与地下空间只做专项可行性，不先建机房。[depth:municipal_new_infrastructure] [assumption:A-MUNICIPAL-001]

### 路网分析与步行可达性方法

空间句法的整合度/选择度可作为断点与缝合廊的**方法学初筛**，本方案给出候选廊道几何，但不宣称已完成句法计算或本地整合度排名。[source:THEORY-SPACE-SYNTAX] Walk Score 类方法证明“到设施的步行可达”可被量化，但本方案禁止直接套用商业评分冒充海淀实测。[source:THEORY-WALKSCORE] Complete Streets/NACTO 指导断面分配与行人优先。[source:THEORY-COMPLETE-STREETS] [source:THEORY-NACTO-STREETS]

公共服务思考借用 15 分钟城市六功能清单做缺口识别，同时用批判文献避免“画个圈就算覆盖”。[source:THEORY-15MIN-CITY] [source:THEORY-15MIN-CRITIQUE]

![慢行网络、蓝绿体系与低速配送试验线路](assets/figures/mobility-bluegreen.png)

## 蓝绿空间、公共空间与城市风貌

> **《复测记》·第十一幕「大钟寺门户」（叙事引导）**：门户应首先体现公共性：连续绿地、主题标志节点、公共信息设施和开放的首层界面共同构成到达体验。[assumption:A-DRAMA-001]

### 蓝绿空间与公共空间体系

蓝绿系统承担生态调节、慢行休闲和公共活动等复合功能。[depth:blue_green_public_space] 概念绿地范围见 [data:geometry/green_space.geojson#GS-SPINE]。按概念绿地几何面积与暂定研究范围计算，绿地系统几何面积比为 12.27% [metric:green_ratio]；按公共空间节点几何面积与暂定研究范围计算，公共空间节点面积比为 1.34% [metric:public_space_ratio]，其范围包括评估断面、主题标志节点和低速设备服务驿站。主题标志节点共 3 处 [metric:ai_landmark_count]。上述指标不同于法定绿地率或公共空间供给率。

风貌塑造以铁路工业遗存为结构基础，以连续绿地和公共空间为环境基底；数字化设施集中设置在入口、公共信息节点和运行状态提示位置，控制数量、亮度和尺度，避免形成连续电子界面。[assumption:A-BRAND-001]

### 绿色基础设施与公共空间治理

EPA 绿色基础设施强调蓝绿的多功能（降温、雨水、休闲、生物多样性）；本方案把主脊写成降温—慢行—感知复测共用走廊，而非纯景观。[source:THEORY-EPA-GREEN-INFRA] PPS 四要素与 UN-Habitat 公共空间工具包要求包容、可治理、可维护；主题标志节点必须服务停留与导向，禁止不可达雕塑。[source:THEORY-PPS-PLACE] [source:THEORY-UN-HABITAT-PUBLIC]

### 概念效果图套图（非实景）

九张写实+暖宣纸调效果图见 `assets/renders/`：R01 全带鸟瞰；R02 大钟寺门户；R03 高短板整治前后；R04 原点调研亭；R05 众智园机器人走廊；R06 夜间安全与合约看板；R07 机器人共享断面；R08 十二幕分镜长卷；R09 终幕「把测量权交还给人」。仅供沟通与设计表达。[source:RENDERS-SUITE] [assumption:A-RENDER-001]

![R01 全带鸟瞰概念效果图](assets/renders/r01-aerial.jpg)

![R08 京张十二幕分镜长卷](assets/renders/r08-twelve-acts-storyboard.jpg)

![R09 终幕：把测量权交还给人](assets/renders/r09-act12-finale.jpg)

## 更新项目清单、实施政策与分期计划

> **《复测记》·第十二幕「把测量权交还给人」（叙事引导）**：分期不是投资承诺。终幕把测量权交回市民——年度普查、微短剧共创与感知合约，才是长期运营。[assumption:A-DRAMA-001]

### 更新项目与实施时序

项目库扩展为可检查清单，总数 12 [metric:renewal_project_count]（正文与 visual 页同步，概念建议）。[depth:renewal_project_list]

一期（补短板）：实施 5 处高短板断面整治、主轴贯通试点和公共评估信息设施，预留低速设备线路及驿站接口。

二期（织网络）：建设 3 条东西向步行联系廊、口袋公园、公众调研亭、3 处低速设备服务驿站和众智园验证走廊。

三期（成体系）：持续开展建设后评估、年度监测和应用场景滚动复核；经审批后完善多运营主体运行规则。
规划实施分为 3 个阶段 [metric:phasing_stage_count]；分期范围见 [data:geometry/phasing.geojson#PH-1]。具体建设时序和投资安排须结合审批、产权和资金条件确定。[depth:phasing_implementation] [assumption:A-OPS-001]

### 小规模试点与建设后评估

一期动作对齐“小而可逆”的干预逻辑：先改遮阴/座椅/照明等可撤场组件，再用 SP-Survey 与 Gehl 式公共生活观测验证是否出现可选活动回流；验证失败则回滚，而不是加大屏幕。[source:THEORY-GEHL-PLDP] [source:SP-SURVEY-PAPER] [assumption:A-SURVEY-PROTOCOL-001]

### 年度运营日历（八个产品）

A01 一月发布公共空间评估基线；A02 三月开展调研员驻留；A03 四月举办复测步行日；A04 六月开展低速智能设备公开测试；A05 九月举办“可感京张”主题周；A06 十月举办国际案例交流活动；A07 每月开展试点复盘；A08 全年征集城市共创提案并提供小额资助。年度周只占一周，其余靠复测与工单闭环。[assumption:A-OPS-001]

## 指标体系、面积复算与合规矩阵

### 指标口径与使用边界

全部空间量由 EPSG:4326 交换几何投影到 EPSG:4548 复算。[depth:metrics_recalculation] 主要技术指标如下：总体面积 1141.3 公顷 [metric:site_area_sqm]；绿地系统几何面积比 12.27% [metric:green_ratio]；公共空间节点面积比 1.34% [metric:public_space_ratio]；建筑基底 7.3 公顷 [metric:building_footprint_area_sqm]；主脊长度 9.3 公里 [metric:park_spine_length_m]；感知断面数 18 [metric:perception_section_count]；高短板断面数 5 [metric:high_shortfall_section_count]；平均短板指数 0.416 [metric:mean_perception_shortfall]；低速配送试验线路长度 18.8 公里 [metric:robot_corridor_length_m]；低速设备服务驿站数 3 [metric:robot_hub_count]；驿站面积合计 972 平方米 [metric:robot_hub_area_sqm]；场景卡数 16 [metric:scenario_card_count]；全球案例数 7 [metric:ecosystem_case_count]；分期阶段数 3 [metric:phasing_stage_count]；主题标志节点数 3 [metric:ai_landmark_count]；人才画像数 6 [metric:persona_count]；更新项目数 12 [metric:renewal_project_count]；路网密度(km/km²) 2.93 [metric:road_network_density_km_per_sqkm]；用地单元数 9 [metric:land_use_parcel_count]；重点区数 3 [metric:key_area_count]；测试验证场景数 6 [metric:test_validation_scenario_count]。

相关指标分别由边界、重点地区、用地、建筑、道路、绿地、公共空间、约束和分期图层复算。暂缺的法定规划控制条件以“待明确”标注，不作推定。

感知类指标（短板、夜间安全等）标注为模型估计，待人在环路复测；Walk Score/空间句法数值若未来引入，必须用批准数据重算并公开公式，禁止直接粘贴外部网站分数。[source:THEORY-WALKSCORE] [source:THEORY-SPACE-SYNTAX] [assumption:A-PERCEPTION-MODEL-001] [assumption:A-THEORY-001]

![指标证据链、感知合约与分期](assets/figures/metrics-evidence.png)

成果已对照征集公告相关任务、规划依据和设计深度要求进行核查，覆盖现状诊断、三级范围、总体结构、用地、强度、建筑形态、保留更新、交通、市政、蓝绿空间、重点地区、项目、分期、指标复算和风险控制等内容。[depth:risk_missing_data]

## 风险、版权与合规说明

### 实施前置条件

本章说明方案深化与实施所需的前置资料、审批条件、版权边界和风险控制要求。

边界、控制性详细规划、产权、交通、文物保护、市政条件、低速设备路权、数据保护和品牌使用均为后续深化的前置条件。[depth:risk_missing_data] 法定资料补充后，应同步校核空间图层、技术指标、图纸和展示文件。

城市设计与城市科学理论仅用于方法参考，不构成本地达标证明或法定标准。[assumption:A-THEORY-001]

隐私与安全底线：不采集不必要数据，不以个人轨迹换热力图，不让模型替代医生/教师/执法/审批；机器人场景必须可紧急停止、可人工接管、可公开复盘。[assumption:A-PRIVACY-001] [assumption:A-AI-SAFETY-001] [assumption:A-ROBOT-001]

正文、图面、标志、效果图、网页与图册为本次方案原创生成；地图使用本方案登记的暂定几何；国际案例与理论仅用于规划方法借鉴。许可见 `report/copyright_statement.md`。本方案不声称官方批准、法定规划、资金落实或实施授权。

## 参考资料

第一组征集主控：[source:OFFICIAL-ANNOUNCEMENT] [source:AGENT-TASKBOOK] [source:SITE-PACKAGE]。第二组边界与数据治理：[source:SOURCE-REGISTRY] [source:PROCESSED-FACT-PACK] [source:BOUNDARY-SOURCE] [source:KEY-AREA-SOURCE]。第三组方法与工具：[source:VATA-PAPER] [source:CITY-LANDSCAPE-INSIGHT] [source:SP-SURVEY-PAPER] [source:SP-SURVEY-PLATFORM] [source:SP-SURVEY-PROTOCOL]。第四组全球案例一手页：[source:CASE-SG-PDD] [source:CASE-SG-IMDA] [source:CASE-SG-URA] [source:CASE-BCN-SUPERBLOCK] [source:CASE-MEADOWAY] [source:CASE-CHOUTEAU] [source:CASE-HEL-TESTBED] [source:CASE-QUAYSIDE-LESSON]。第五组城市设计/城市科学理论：[source:THEORY-LYNCH-IMAGE] [source:THEORY-GEHL-PLDP] [source:THEORY-GEHL-CITIES-PEOPLE] [source:THEORY-PPS-PLACE] [source:THEORY-WHYTE-SOCIAL-LIFE] [source:THEORY-JACOBS-DEATH-LIFE] [source:THEORY-SPACE-SYNTAX] [source:THEORY-WALKSCORE] [source:THEORY-15MIN-CITY] [source:THEORY-15MIN-CRITIQUE] [source:THEORY-NACTO-STREETS] [source:THEORY-COMPLETE-STREETS] [source:THEORY-CPTED] [source:THEORY-EPA-GREEN-INFRA] [source:THEORY-OLDENBURG-THIRDPLACE] [source:THEORY-UN-HABITAT-PUBLIC]。第六组自制视觉：[source:AWAKENING-POSTER] [source:RENDERS-SUITE] [source:OSM-CONTEXT]。

### 理论与方法附录（规划响应表）

| 理论/方法 | 核心命题 | 本方案转译 | 明确不做 |
| --- | --- | --- | --- |
| Lynch 可意向性 | 路径/边界/区域/节点/地标 | 一脊三区+基线碑/主题标志节点 | 不虚构历史对白 |
| Gehl 人尺度/PLDP | 步行速度、驻留与活动多样性 | 短板指数维度+公共生活复测 | 不宣称已完成全年观测 |
| Jacobs 街道眼 | 自然监视与多样性 | 界面活跃、机器人不夺停留 | 不大拆大建式更新 |
| Whyte 小广场 | 座椅、日照、边界、三角化 | 门户/原点广场家具与遮阴 | 不做不可达雕塑 |
| Oldenburg 第三空间 | 家/工作之外的非正式聚集 | 原点社区客厅与青年场景 | 不强制社交画像 |
| PPS / UN-Habitat | 场所四要素与包容治理 | 公共空间审计口径 | 不把装置当公共性 |
| Space Syntax | 网络整合度/选择度 | 断点与缝合廊方法初筛 | 不发布伪精确整合度图 |
| Walk Score 类 | 设施步行可达验证 | 未来复算公式预留 | 不粘贴商业网站分数 |
| 15 分钟城市（含批判） | 六功能近距生活 | 统筹层服务域检查清单 | 不宣称已达覆盖 |
| Complete Streets / NACTO | 多模式街道再分配 | 人>自行车>机器人>车 | 不设机器人专属机动车道 |
| CPTED | 自然监视与维护 | 夜间安全断面照明/界面 | 不以摄像执法替代设计 |
| 绿色基础设施 | 蓝绿多功能 | 主脊降温—慢行—复测 | 不把绿地只当美化 |

全部理论引用均为方法背景。[assumption:A-THEORY-001]

### 技术校核索引

- 来源：见上节全部 `[source:]`
- 标准：`[standard:PROJECT-OFFICIAL-ANNOUNCEMENT]` … `[standard:MOHURD-ARCH-DESIGN-DEPTH-2016]`
- 深度：`[depth:existing_conditions_diagnosis]` … `[depth:risk_missing_data]`
- 指标：`1141.3 公顷 [metric:site_area_sqm]` … `7 [metric:ecosystem_case_count]、3 [metric:phasing_stage_count]`
- 假设：`[assumption:A-BOUNDARY-001]` `[assumption:A-CONTROLS-001]` `[assumption:A-KEYAREA-001]` `[assumption:A-PERCEPTION-MODEL-001]` `[assumption:A-SURVEY-PROTOCOL-001]` `[assumption:A-ROBOT-001]` `[assumption:A-PRIVACY-001]` `[assumption:A-AI-SAFETY-001]` `[assumption:A-INTENSITY-001]` `[assumption:A-TRANSIT-001]` `[assumption:A-MUNICIPAL-001]` `[assumption:A-ACCESS-001]` `[assumption:A-BRAND-001]` `[assumption:A-OPS-001]` `[assumption:A-RENDER-001]` `[assumption:A-DRAMA-001]` `[assumption:A-THEORY-001]`

**规划愿景：以京张铁路遗产为纽带，持续改善沿线公共空间品质，形成安全、舒适、开放并可持续评估的城市公共空间主轴。**
