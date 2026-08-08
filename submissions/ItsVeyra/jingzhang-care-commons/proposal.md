---
title: "共生京张：技能留存与自主开局社区"
author_github: "ItsVeyra"
language: "zh"
translation_file: "proposal.en.md"
license: "COMMUNITY-DISPLAY-ONLY"
summary: "以长者为发起者和贡献者，用一条共生照护廊、三个能力核与社区触点网络连接技能留存、自主开局和审慎的公共服务智能体；全部空间与运营内容均为待复核的概念建议。"
tracks: ["ai-public-services", "civic-agent-governance", "jingzhang-heritage-narrative"]
scenarios: ["ai-health-service-navigation", "public-safety-operations-review", "ai-cultural-guide"]
iteration: "v1.0"
---

# 共生京张：技能留存与自主开局社区

**Jingzhang Care Commons**　｜　**我来发起，我们开局。**

## 执行摘要与概念边界

本方案把“被照护的老人”改写为有经验、有作品、能发起公共生活的社区行动者。AI 只降低四类门槛：把一句自然语言转成可编辑的活动草案；在逐项同意后连接熟人或共同兴趣者；协调场地、志愿者、辅具、交通与陪伴；在具体活动中提供可解释的安全提示。它不持续追踪居民，不做情绪评分、信用排序、自动诊断或黑箱资格判断。人始终决定是否发起、邀请谁、公开什么以及何时撤回。

总体概念是“一条共生照护廊、三个能力核、多个社区触点”：京张遗址公园及其相邻慢行—蓝绿系统被建议为日常交往廊；众智园“百工留存站”、北京 AI 原点社区“万技开局厅”、大钟寺“传承作品场”承担保存、发起、展示三种能力；四类分布式网络触点分别是开局桌、共享声音廊、慢行客厅和邻里平台。三个地标加四类网络特征合计七个**概念性公共空间项目特征**，不是七处已经运营的物理网点。[data:geometry/public_space.geojson#PUBLIC-001] [data:geometry/public_space.geojson#PUBLIC-004] [metric:community_touchpoint_count]

范围和数值必须在开篇降级说明：公告给出三层研究任务，本提交的总体边界和三处重点区 polygon 来自仓库临时粗略数据，均为低置信度、非正式控制边界。[source:DATA-SRC-OFFICIAL-ANNOUNCEMENT-20260509] [source:DATA-SRC-PROVISIONAL-BOUNDARIES-20260605] [data:geometry/site_boundary.geojson#PROV-SITE-001] 当前几何复算约 1,141 公顷，仅用于方案组织和技术自检；取得正式地理配准边界后，用地、道路、建筑、绿地、公共空间、分期和全部面积比例须整体重算。[metric:submitted_site_area_sqm] [depth:risk_missing_data]

![资料证据链、概念边界与提交包关系图](assets/figures/site-overview.png)

## 设计依据与资料清单

### 资料分级

正式任务依据包括征集公告、面向智能体任务书、住房城乡建设与自然资源主管部门公开标准；临时粗略边界只能支撑概念生成；七个全球案例仅为背景比较。提交包以 `sources.json` 登记来源，以 `assumptions.json` 声明缺口，以 `compliance_matrix.json` 对应任务，以 `standard_matrix.json` 和 `design_depth_matrix.json` 约束专业深度。正文中的来源、标准、深度、数据与指标证据标记均可回到这些机器可读记录。

正式依据为：[source:DATA-SRC-OFFICIAL-ANNOUNCEMENT-20260509]、[source:DATA-SRC-AGENT-TASKBOOK-20260518]、[source:DATA-SRC-MOHURD-URBAN-DESIGN-MEASURES]、[source:DATA-SRC-MOHURD-CONTROL-DETAILED-PLANNING]、[source:DATA-SRC-MNR-LAND-USE-CLASSIFICATION-202311]。对应标准为 [standard:PROJECT-OFFICIAL-ANNOUNCEMENT]、[standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK]、[standard:MOHURD-URBAN-DESIGN-MEASURES]、[standard:MOHURD-CONTROL-DETAILED-PLANNING]、[standard:MNR-LAND-USE-CLASSIFICATION-GUIDE] 和 [standard:MOHURD-ARCH-DESIGN-DEPTH-2016]。

### 缺失数据与使用纪律

尚缺正式总体及重点区 polygon、现状地块与权属、建筑普查、法定控规、市政管线、道路红线与交通运行、消防防洪、文保边界、设施容量和居民基线。故本方案只给出城市设计结构、核验方法和概念性项目，不给出法定容积率、高度、退线、拆迁对象或工程线位。[depth:existing_conditions_diagnosis] [data:geometry/constraints.geojson#PROV-SITE-001]

设计判断遵循四步证据链：先说明意图，再说明空间理由，再指向几何/指标/标准，最后列出缺口。例如“沿廊组织慢行客厅”的意图是让活动从室内延伸到可停留路径；理由是概念绿地和公共空间均位于同一临时边界内；证据为 [data:geometry/green_space.geojson#GREEN-001]、[data:geometry/public_space.geojson#PUBLIC-006] 和 [depth:blue_green_public_space]；缺口是现状树木、无障碍坡度、过街和河道条件仍待勘察。

## 三层范围工作框架

统筹研究范围约 43.6 平方公里，用于讨论产业生态、未来城市与公共服务协同，不据此新增控制线；总体设计范围按仓库临时 polygon 复算约 1,141 公顷，用于组织概念用地、廊道和项目；三处重点区临时 polygon 合计约 369 公顷，与公告约数存在复算口径差，必须在正式边界到位后校准。[source:DATA-SRC-OFFICIAL-ANNOUNCEMENT-20260509] [data:geometry/key_areas.geojson#PROV-KEY-001] [metric:key_area_total_sqm]

“一条共生照护廊”不是新增道路红线，而是把京张文化、蓝绿慢行和社区服务串成活动路径；“三个能力核”分别处理技能存档、活动开局与作品传播；“多个社区触点”通过四类可复制组件接近居民日常。三层关系是：统筹层确定“长者主体性与全龄协作”的城市议题；总体层把议题转译为廊、核、触点和更新清单；重点区层以地标、首层空间、慢行接口和试点流程进行验证。[depth:three_level_scope_framework] [depth:overall_spatial_structure]

![三层范围与“一廊三核多触点”空间工作框架](assets/figures/land-use-structure.png)

临时用地层以九个概念分区完整覆盖临时边界，覆盖率 100% 只是拓扑自检结果，不表示现状用地调查或法定用地方案。[data:geometry/land_use.geojson#LU-001] [metric:land_use_coverage_ratio] 替换正式 polygon 后，必须重新切分边缘单元并复核三个重点区、分期与所有面积。

## 统筹研究范围产业与未来城市研究

### 产业与城市策略

“共生京张”把 AI 全栈自主创新从单一企业链扩展为“技术研发—公共服务验证—居民共同治理—文化传播”的回路。三区两翼协同被解释为：众智园偏全栈研发与安全治理，北京 AI 原点社区偏开源转化与人才生活，大钟寺偏智能终端、内容与国际传播；高校/创新策源和京张遗址公共空间是两翼。三大定位为“自主创新试验带、全龄共生生活带、京张文化叙事带”；五大功能为研发转化、公共验证、人才生活、技能传承、国际交流。[source:DATA-SRC-AGENT-TASKBOOK-20260518] [standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK]

空间上，产业服务用地、社区生活与公共文化分区只是概念供给结构：代码 05 约 422 公顷、0701 约 107 公顷、0702 约 112 公顷、0802 约 215 公顷、0803 约 51 公顷、0804 约 27 公顷，均由临时边界内的规则化设计分区复算，不能理解为现状或法定分类。[metric:land_use_05_area_sqm] [metric:land_use_0701_area_sqm] [metric:land_use_0702_area_sqm] [metric:land_use_0802_area_sqm] [metric:land_use_0803_area_sqm] [metric:land_use_0804_area_sqm]

未来城市策略把数字能力放到社区柜台、公共客厅和可撤回的关系网络中。技术团队提供可解释工具和接口；社区组织者制定活动规则；居民决定内容和可见性；专业人员处理医疗、安全、法律与规划判断。产业价值来自真实但受控的公共问题验证，而不是把居民生活变成无边界数据源。

### 品牌、Logo 与文化叙事

中文名“共生京张：技能留存与自主开局社区”，英文名 “Jingzhang Care Commons”，口号“我来发起，我们开局。”文化主线为“自主筑路—自主创新—自主生活”：京张铁路的自主筑路精神，经中关村自主创新，落到居民自主发起日常生活。Logo 建议以两条轨线向外打开、围合成一张圆桌；铁路炭灰作为基底、社区松绿表示照护与常青、里程琥珀标识一次次开局。所有字形、图形与字体须原创或取得许可，不能直接挪用企业标志或历史照片。[depth:height_massing_character]

## 总体设计范围城市更新与控规深度城市设计

总体结构建议为“遗址文化—蓝绿慢行复合廊 + 三处能力核 + 社区首层触点 + 产业服务横向联系”。设计意图是把大尺度产业片区转成步行可达、可停留、可发起的小尺度公共界面；空间理由是现有提交图层可以校核用地、绿地、公共空间、建筑基底和分期的相互覆盖；证据为 [data:geometry/land_use.geojson#LU-005]、[data:geometry/buildings.geojson#BLDG-001]、[data:geometry/phasing.geojson#PHASE-001]；缺口是地块权属、现状建筑价值和控规条件未取得。[standard:MOHURD-CONTROL-DETAILED-PLANNING] [depth:land_use_layout]

城市更新采用“先运营验证、再小微改造、后专业深化”的逆向校准：近期用可移动家具、标识和预约机制测试停留与开局；验证通过后才研究首层改造、无障碍连续和蓝绿节点；涉及道路、河道、轨道、市政或建筑工程的内容必须由相应专业团队复核。概念建筑基底约 9.5 公顷，仅表示三个示范性设计 footprint，既非现状建筑量，也不能推出总建筑规模。[metric:building_footprint_area_sqm] [depth:development_intensity_controls]

法定容积率、总建筑面积、建筑密度、道路面积与比例目前均未知；取得正式控规、建筑普查和交通资料后才可计算。[metric:floor_area_ratio] [metric:total_floor_area_sqm] [metric:building_density] [metric:road_area_sqm] [metric:road_area_ratio] 这五项不以经验值补齐，避免概念图变成伪精确控制。

## 重点区域详细设计

![众智园、AI 原点社区与大钟寺重点区域索引](assets/figures/key-areas.png)

### 众智园：百工留存站

定位为全栈自主创新与居民技能档案的交界面。空间结构建议把靠近清河和园区公共界面的首层作为“留存—展示—教学”连续带，百工留存站提供录音、扫描、作品摄影和小型工作坊；室外接入慢行客厅。建筑策略优先评估可逆改造与共享首层，不先指定拆除；交通策略强调步行、骑行和预约接送的落客分离；公共空间承载百工夜校与安全治理展示。[data:geometry/key_areas.geojson#PROV-KEY-001] [data:geometry/public_space.geojson#PUBLIC-001]

AI 只协助整理口述、生成待核对标签和授权范围，原作者逐项确认。风险包括河道、防洪、园区安全、噪声和档案版权，须在正式勘察及运营协议后深化。[depth:three_key_area_detailed_design]

### 北京 AI 原点社区：万技开局厅

定位为近校成果转化与居民自主发起的公共客厅。空间建议以万技开局厅连接校区—园区—社区步行界面，设置一句话开局台、活动草案墙、可分隔小组空间、辅具借用与社区资源柜台；首层界面保持全天候可见但不要求全天候运营。建筑更新先做可达性、声环境和消防评估，再决定保留、改造或新增轻量构筑物。[data:geometry/key_areas.geojson#PROV-KEY-002] [data:geometry/public_space.geojson#PUBLIC-002]

运营上，居民可把“今晚下棋”“明早慢走”转成时间、人数、无障碍需求和邀请范围清晰的草案；发布前由发起者确认，敏感需求转人工。风险是校园边界、场地权属、夜间扰民和服务责任，应以小规模受控试点验证。

### 大钟寺：传承作品场

定位为城市型智能经济、文化传播与代际共创展示场。空间建议利用轨道站周边公共界面组织可穿行作品场，以阶段性展陈连接铁路记忆、职业作品、修理成果和青年共创；四象限步行联系只作为待交通与市政复核的方向。展陈不以“大屏监控”制造科技感，而以可阅读的作品、授权卡和创作者声音构成公共叙事。[data:geometry/key_areas.geojson#PROV-KEY-003] [data:geometry/public_space.geojson#PUBLIC-003]

建筑与风貌控制建议采用低饱和炭灰基底、松绿色路径、琥珀色里程标记；高度、体量、文保关系和站城接口均待正式资料。风险包括高峰客流、商业化挤压、数字内容授权和展陈维护。

## AI 创新生态、人才画像与 AI+ 场景

### 六类人物与服务关系

| 人物 | 主体能力与需求 | 设计回应 |
| --- | --- | --- |
| 独居老人 | 想主动找棋友、散步伙伴，同时控制谁能看到自己 | 一句话开局、熟人优先、小圈邀请、随时撤回 |
| 行动不便或康复居民 | 需要辅具、交通、无障碍场地与陪伴协同 | 资源柜台生成待人工确认的组合方案，不作医疗判断 |
| 有经验的长者 | 有手艺、职业经验、作品和愿意教授的内容 | 技能里程卡、百工留存站、微课程与顾问角色 |
| 家庭照护者 | 需要经授权了解活动状态、安排喘息 | 只接收活动级更新，不获得连续位置或情绪推断 |
| 儿童与青年 | 希望参与铁路故事、修理、游戏和 AI 共创 | 在监护与版权规则下进行代际共同创作 |
| 社区组织者 | 需要协调场地、志愿者、安全和冲突 | 可解释排班建议、人工复核、审计与停止条件 |

十二张卡均映射到 `ai-health-service-navigation`、`public-safety-operations-review`、`ai-cultural-guide` 三个仓库标准场景：健康服务只导航与协调，不诊断；公共安全只做活动级复核；文化导览只使用有来源、有授权的内容。

### 场景 01｜一句话发起棋局或慢走

独居老人说“明早想在公园慢走半小时”，开局助手生成可编辑草案；位置为万技开局厅或开局桌网络，数据只含自愿填写的时间、人数、可达性与邀请范围，发布前由发起者确认，不确定时转社区工作人员。[data:geometry/public_space.geojson#PUBLIC-004]

### 场景 02｜小圈熟人重新连接

系统仅在双方已有联系或分别同意共同兴趣匹配后提出邀请建议；不展示关系评分，不扩大通讯录。发起者与受邀者均可拒绝，争议由人工处理。

### 场景 03｜远程合唱与共读

行动不便居民可从慢行客厅或家中加入小型合唱/共读；声音是否录制、谁可收听和保留多久分别授权，网络故障时提供电话或线下名单的人工备选。[data:geometry/public_space.geojson#PUBLIC-005]

### 场景 04｜辅具、交通与陪伴协调

开局助手汇总公开服务目录和人工维护资源表，为康复居民生成“辅具—无障碍场地—预约车辆—陪伴人”清单；任何健康判断、资格确认与费用承诺都交由专业人员。[source:DATA-SRC-AGENT-TASKBOOK-20260518]

### 场景 05｜手艺与职业记忆工作坊

有经验的长者在百工留存站展示修理、木工、编织、工程或职业经验；AI 可生成待核对目录和字幕，原作者决定公开范围，实物操作由具备安全能力的人带领。[data:geometry/public_space.geojson#PUBLIC-001]

### 场景 06｜居民微课程与社区顾问

技能里程卡把“会什么、做过什么、允许怎样联系、下一次想发起什么”转成课程草案。社区组织者核验场地、材料、安全与报酬规则，不以算法排名决定谁有资格授课。

### 场景 07｜经授权的家庭活动更新

家庭照护者只在居民主动授权后收到“已签到/活动结束/需要联系工作人员”等活动级消息；不共享连续轨迹、聊天内容或推断状态，授权可单次、限时或撤回。

### 场景 08｜喘息与陪伴接力

家庭照护者提出一个明确时间窗，社区柜台建议经过培训且愿意参与的陪伴资源；工作人员复核冲突、责任和应急联系人，匹配失败时直接回到人工排班。

### 场景 09｜铁路记忆与青年共述

儿童与青年在传承作品场与长者共同核对铁路、厂区和职业记忆；公开史料与个人叙述明确分栏，AI 修复或补全内容必须标注，不得冒充原始记录。[data:geometry/public_space.geojson#PUBLIC-003]

### 场景 10｜游戏、音乐与 AI 共创

青年与长者共同设计棋谱、音乐或小游戏；AI 只作为可关闭的创作工具，作品页列明人类作者、工具参与和授权，不把参与者素材用于未同意的训练。

### 场景 11｜匿名兴趣—需求图

社区组织者只能查看达到最低汇总门槛的兴趣与设施需求，不显示个人点位，不做情绪或脆弱性评分；样本过少时不出图，居民可要求删除原始提交。[data:geometry/public_space.geojson#PUBLIC-007]

### 场景 12｜场地与志愿者排班建议

系统依据场地开放时段、无障碍条件、志愿者明确可用时段生成多个可解释方案；社区组织者核对公平性、负担和安全后发布，任何冲突、缺员或系统异常均转人工。

## 三个受控验证试点与智能体治理

**试点一“一句话开局”可用性测试**：在万技开局厅，以小样本、短周期测试从自然语言到可编辑草案的完成路径。采集最少的步骤事件，不录制无关语音；观察首次完成率和居民主动发起占比，当前均无基线。[metric:first_launch_completion_rate] [metric:elder_initiated_activity_share]

**试点二“代际共创客厅”**：在百工留存站/传承作品场验证技能里程卡、共同创作、署名和撤回流程。参与者逐项选择公开范围；观察重复参与率与经验证的居民主体感量表，当前值未知，不能预填。[metric:repeat_participation_rate] [metric:resident_agency_score]

**试点三“社区安全协作沙盒”**：用虚构或去标识化活动事件演练拥挤、走失联络、天气和设备故障；AI 只给提示，工作人员决定行动。观察规定时窗内人工复核率与撤回完成率，当前均待真实运营日志。[metric:human_review_timeliness_rate] [metric:consent_withdrawal_completion_rate]

共同停止条件为：同意状态无法验证、敏感数据超范围、模型无法说明依据、人工负责人缺位、误报连续造成干扰、参与者提出停止、系统/网络故障或现实风险超出活动预案。触发后立即暂停自动输出，保留最小审计记录，向现场负责人和相应专业人员转交；紧急情况使用既有人工应急流程。三个试点均不连接连续人脸识别，不用于执法、诊断、福利资格或信用评价。

## 技能留存打卡地与“技能里程卡”

技能里程卡有四格：**技能**（本人如何描述）、**作品**（实物/照片/音频及来源）、**授权**（谁可见、可否改编、可否用于 AI、保留多久）、**下一次开局**（想教、想修、想与谁共创）。每次“打卡”不是被动考勤，而是创作者主动更新一段经验或发起一次行动；纸质、口述和数字方式并行。

百工留存站负责采集与著录，万技开局厅把技能转成活动，传承作品场让经授权成果进入公共叙事。撤回必须同步撤下公开页、检索索引和受治理副本；AI 生成摘要、修复图像或字幕都与原作分层显示。设计意图是建立可持续的贡献关系，而不是把长者经历一次性“数字化”。

## 用地、建筑规模与拆改留方案

概念用地结构中，绿地代码 1401 约 141 公顷，广场与防护类分区代码 1402、1403 各约 33 公顷；这些数值均从规则化临时分区复算，不是现状调查或法定指标。[metric:land_use_1401_area_sqm] [metric:land_use_1402_area_sqm] [metric:land_use_1403_area_sqm] [standard:MNR-LAND-USE-CLASSIFICATION-GUIDE]

拆改留采用“价值—安全—碳—可达—运营”五项核验：有历史、社区记忆或适应性价值者优先保留；结构可用但界面封闭者研究改造；确有安全或功能问题者须经专业鉴定后再讨论拆除；新增只补足无障碍、公共服务和共享空间缺口。当前三个建筑 footprint [data:geometry/buildings.geojson#BLDG-001]、[data:geometry/buildings.geojson#BLDG-002]、[data:geometry/buildings.geojson#BLDG-003] 均为概念性示意，不能对应现实房屋或权属。[depth:retain_renovate_demolish]

建筑总规模、高度、强度、退线和停车配建保持待确认。正式深化须导入建筑普查和控规条件，逐栋建立保留/改造/拆除/新建表，评估安置、消防、结构、日照、无障碍、文保与全生命周期碳。

## 交通、轨道、市政与公共服务设施

四条概念性道路线只表达“廊道慢行、三核联系、社区接驳、服务后勤”四类组织关系，不是道路红线或工程中心线。[data:geometry/roads.geojson#ROAD-001] [data:geometry/roads.geojson#ROAD-004] [depth:traffic_rail_slow_parking] 轨道站点一体化建议优先核查出入口、过街、轮椅连续、非机动车停放、预约接送和高峰冲突；大钟寺四象限连通、跨环路和河道节点须经交通及产权部门资料复核。

![交通慢行、蓝绿廊道与公共服务复合系统](assets/figures/mobility-bluegreen.png)

市政策略采用“传统设施先行、数字设施可退出”：供电、排水、消防、通信、应急呼叫和室内环境先满足专业要求，再部署端侧算力与预约终端；终端离线时，纸质清单、电话和现场人员仍可完成核心服务。[depth:municipal_new_infrastructure] 公共服务包括辅具与交通导航、照护者喘息转介、文化教育、技能工作坊和社区组织支持；涉及医疗仅做 `ai-health-service-navigation`，不作诊疗。

## 蓝绿空间、公共空间与城市风貌

概念绿地约 141 公顷、公共空间约 86 公顷，占临时总体边界约 12.3% 和 7.5%；二者合并去重约占 19.8%。这些低置信度比例用于比较设计分配，不能替代绿地率、广场现状或法定公共空间统计。[metric:green_space_area_sqm] [metric:green_ratio] [metric:public_space_area_sqm] [metric:public_space_ratio] [metric:green_public_space_ratio]

蓝绿廊道建议形成“走得通—坐得下—看得懂—能开局”的连续体验：慢行断点设人工可读导视与休息点，慢行客厅提供遮阴、照明和轮椅回转，里程标记讲述自主筑路/创新/生活，地标内部承接技能活动。[data:geometry/green_space.geojson#GREEN-001] [data:geometry/public_space.geojson#PUBLIC-006] 具体铺装、树种、水文和照明须在现场调查后决定。

风貌以铁路炭灰、社区松绿、里程琥珀形成三级识别；两条轨线打开成圆桌的视觉母题用于 Logo、地面里程点、技能卡和导视。文化内容必须区分公开史实、居民口述、AI 派生三种来源；国际传播采用中英双语短叙事与创作者授权页，不使用未清权照片、字体、人物或企业标志。

## 七个国际案例与可迁移机制

以下页面由相关机构、城市或网络发布，全部登记为 `background_only`。它们支持“这种机制在别处如何被组织”的比较，不支持海淀的空间控制、实施结果或效果数字。

| 案例与登记来源 | 页面支持的机制 | 可迁移建议 | 局限 |
| --- | --- | --- | --- |
| 日本 Ibasho [source:CASE-IBASHO-OFFICIAL] | 强调长者作为社区资产与参与者 | 由长者共同制定留存站规则并担任导师 | 治理、文化和运营条件不同，不能预测本地参与成效 |
| 新加坡 Kampung Admiralty [source:CASE-KAMPUNG-ADMIRALTY-HDB] | 复合组织居住、社区、照护和公共空间 | 三核周边优先做跨服务协同与可达界面 | 不能据其建筑形态推导海淀容量或控规 |
| Barcelona VinclesBCN [source:CASE-VINCLES-BCN-CITY] | 以数字工具和人际支持促进长者联系 | 数字联系必须与社区工作人员和小圈同意结合 | 不移植用户规模或效果主张，也不支持持续跟踪 |
| Helsinki Oodi [source:CASE-OODI-OFFICIAL] | 公共图书馆作为开放的学习、制作与相遇空间 | 把三核做成可学习、可制作、可发起的公共客厅 | 运营体系和公共文化供给不同，不能预测客流 |
| UK Men’s Sheds [source:CASE-MENS-SHEDS-UK] | 通过并肩制作形成同伴关系 | 以做事为中心的修理/手艺小组，避免强迫表达 | 本地设计必须全龄、性别包容，不能照搬组织边界 |
| Repair Café network [source:CASE-REPAIR-CAFE-NETWORK] | 志愿修理、技能交换和可复制活动格式 | 采用工具清单、安全分工、预约与复盘协议 | 不能提前声称减废量或志愿者供给 |
| WHO age-friendly cities [source:CASE-WHO-AGE-FRIENDLY] | 以环境、服务与参与过程持续改善适老性 | 用参与式检查表和迭代循环审查廊道与服务 | 是方法参考，不构成认证或本地成效证明 |

## 更新项目清单、实施政策与分期计划

| 项目 | 位置与类型 | 依赖条件 | 建议阶段 |
| --- | --- | --- | --- |
| JZ-01 共生照护廊可达性审计 | 全廊，调查/轻量更新 | 正式边界、道路、河道、无障碍现场资料 | 近期验证 |
| JZ-02 百工留存站 | 众智园，首层/运营 | 权属、消防、档案授权、运营团队 | 近期试点后深化 |
| JZ-03 万技开局厅 | AI 原点社区，公共客厅 | 校园园区边界、噪声、开放时段 | 近期试点后深化 |
| JZ-04 传承作品场 | 大钟寺，公共空间/展陈 | 轨道客流、文保、商业界面、版权 | 中期深化 |
| JZ-05 慢行客厅与四类触点 | 廊道网络，公共空间 | 坡度、树木、照明、维护责任 | 分段实施建议 |
| JZ-06 社区资源与同意平台 | 三核与社区，数字公共服务 | 数据保护评估、人工团队、退出机制 | 沙盒通过后扩展 |

概念分期图以三个覆盖临时边界的阶段表达依赖顺序，总面积约 1,141 公顷与临时 site 相同，只说明工作分层，不意味着同期开发或投资安排。[data:geometry/phasing.geojson#PHASE-001] [data:geometry/phasing.geojson#PHASE-003] [metric:phasing_area_total_sqm] [depth:phasing_implementation]

运营建议形成固定节律：每周技能开局；每月“百工夜校/作品展”；每季度代际修理季；每年“京张万技节”。这些活动均为可供运营主体深化的建议。治理结构建议由居民代表、社区组织者、场地运营者、技术团队和安全/隐私专业人员组成共治小组，季度公开问题清单、停止记录和改进结果。[depth:renewal_project_list]

政策建议包括：允许小尺度、可逆公共空间试点；建立居民作品分级授权与撤回规则；将人工服务能力列为数字项目的必要成本；以真实完成路径而非注册量评估；建立跨场地资源目录和责任清单；在正式空间资料更新时触发全包复算。国际传播以创作者为主语，用双语里程卡、开放工作坊和年度节事连接开发者、社区与来访者。

## 指标体系、面积复算与合规矩阵

![核心指标复算、状态与证据链](assets/figures/metrics-evidence.png)

### 已知但低置信度的设计复算

临时总体面积约 1,141 公顷，[metric:site_area_sqm] 与 [metric:submitted_site_area_sqm] 使用同一临时 polygon；三处重点区 [metric:key_area_count] 合计约 369 公顷 [metric:key_area_total_sqm]；用地拓扑覆盖 [metric:land_use_coverage_ratio] 为 100%；概念建筑基底 [metric:building_footprint_area_sqm] 约 9.5 公顷；绿地、公共空间及合并比例分别由 [metric:green_space_area_sqm]、[metric:green_ratio]、[metric:public_space_area_sqm]、[metric:public_space_ratio]、[metric:green_public_space_ratio] 复算；分期覆盖见 [metric:phasing_area_total_sqm]；七个项目特征见 [metric:community_touchpoint_count]。所有正文显示值均按公顷约数或百分比一位小数表达，JSON 保留原始确定性计算值以便审计。[depth:metrics_recalculation]

九类概念用地的完整复算引用为：[metric:land_use_05_area_sqm]、[metric:land_use_0701_area_sqm]、[metric:land_use_0702_area_sqm]、[metric:land_use_0802_area_sqm]、[metric:land_use_0803_area_sqm]、[metric:land_use_0804_area_sqm]、[metric:land_use_1401_area_sqm]、[metric:land_use_1402_area_sqm]、[metric:land_use_1403_area_sqm]。它们只检验概念结构能否复算，不证明现状或法定用地。

### 未知且必须保留为空的指标

法定/调查类指标 [metric:floor_area_ratio]、[metric:total_floor_area_sqm]、[metric:building_density]、[metric:road_area_sqm]、[metric:road_area_ratio] 需正式控规、建筑和道路资料。试点类指标 [metric:elder_initiated_activity_share]、[metric:first_launch_completion_rate]、[metric:repeat_participation_rate]、[metric:resident_agency_score]、[metric:human_review_timeliness_rate]、[metric:consent_withdrawal_completion_rate] 需先固定分子、分母、时间窗、样本、同意和排除规则，再由真实试点采集。未知不是失败，而是防止把愿景包装成调查结果。

合规矩阵逐项链接公告和 `agent.1`—`agent.6`，标准矩阵链接六条标准，深度矩阵覆盖现状诊断、范围、结构、用地、强度、风貌、拆改留、交通、市政、蓝绿、重点区、项目、分期、复算和风险。临时边界更新时，应自动重跑空间审查并由专业人员复核文本中的近似值。

## 风险、版权与合规说明

边界风险：所有提交 polygon 为低置信度临时资料，不能用于审批、征拆、地价、工程或精确容量。专业风险：交通、市政、结构、消防、防洪、文保、无障碍、环境和运营结论须由相应专业团队深化。社会风险：试点可能造成数字排斥、照护劳动不均、活动扰民或“为长者代言”；因此提供纸笔/电话入口、合理便利、居民席位和申诉渠道。

隐私伦理风险：每项作品、联系人、可见范围、AI 使用和保留期分别同意；默认最小可见；不做连续跟踪、情绪评分、信用排名、自动诊断或黑箱资格判断；高风险输出必须人工复核并具备失败转人工路径。版权规则详见 `report/copyright_statement.md`：文本、图解、几何和代码派生图由 AI 生成，公共事实保持归属，不包含真实居民私密故事或作品，AI 修复必须标注。[depth:risk_missing_data]

本方案不代表审批、投资、工程可行性、运营授权或时间承诺。其价值在于提出一套可追溯、可撤回、可试点、可复算的概念方案，供居民、组织者和专业团队共同修正。

## 面向智能体任务书逐项回应

- **agent.1 一带总体概念与功能统筹方案设计**：以“一条共生照护廊、三个能力核、多个社区触点”贯通三层范围，明确三大定位、五大功能和三区两翼协同。[depth:overall_spatial_structure]
- **agent.2 AI 全栈自主创新体系与世界级 AI 创新生态设计**：形成研发—公共验证—居民共治—文化传播回路，并以七个背景案例提炼可迁移机制，不以案例替代本地验证。
- **agent.3 AI+场景赋能新范式与智能化 AI 活力城市设计**：提供六类人物、十二张场景卡和三个受控试点，统一采用最小数据、人工复核、停止与转人工规则。
- **agent.4 AI 公共空间、智能原生新业态与朝圣地标设计**：提出百工留存站、万技开局厅、传承作品场及四类分布式触点，明确七项为概念性项目特征而非既成网点。
- **agent.5 百年京张文化、中关村文化与 AI 新文化融合叙事设计**：用“自主筑路—自主创新—自主生活”和两轨开桌的视觉母题，建立史实、口述、AI 派生分层的文化叙事。
- **agent.6 一带全球 AI 创新活动体系与长期运营设计**：提出周、月、季、年活动节律，共治小组、贡献授权、场景开放、双语传播与问题公开机制，均作为概念建议。

## 参考资料

- `brief/public-brief.md`：用于核对公开征集主题、参与方式与公共议题，设计意图是让方案回应京张、海淀、AI 创新带和城市公共利益；它不含精确空间控制，不能替代正式边界或控规。[source:DATA-SRC-OFFICIAL-ANNOUNCEMENT-20260509]
- 提交来源登记：`sources.json`；正式依据与七个背景案例均以可解析的来源 ID 回引。
- 假设与缺口：`assumptions.json`。
- 任务、标准与深度：`compliance_matrix.json`、`standard_matrix.json`、`design_depth_matrix.json`。
- 空间与指标：`geometry/*.geojson`、`metrics.json`。
- 版权与衍生摘要：`report/copyright_statement.md`、`report/narrative.md`。

参考资料的分工是：公告和任务书界定为什么设计，专业标准约束应达到何种表达深度，临时 GeoJSON 与指标只校验概念结构是否自洽，案例页面只比较运营机制。空间建议必须回到具体 feature 和近似指标，例如总体临时边界 [data:geometry/site_boundary.geojson#PROV-SITE-001] 与 [metric:site_area_sqm]；取得正式 polygon、现状建筑、权属、道路、市政、文保和设施资料后，需重跑面积、拓扑及矩阵审查。[standard:MOHURD-URBAN-DESIGN-MEASURES] [depth:metrics_recalculation] 任何来源层级变化都应同步更新 `sources.json`、假设、正文和图件，避免背景材料被误用为控制证据。
