---
title: "京张智脉·光晕 / Jing-Zhang AI Heritage Halo"
language: "zh"
author_github: "565431hzhang"
proposal_format_version: "2"
bilingual_contract_version: "1"
translation_file: "proposal.en.md"
license: "COMMUNITY-DISPLAY-ONLY"
summary: "基于 provisional boundary 和结构化自检要求生成的 formal AI 城市设计方案包；保留精度警示和复算要求，但组织方数据缺口不阻断内容评分。"
tracks: ["ai-traffic-walkability", "enterprise-services-ecosystem", "civic-agent-governance"]
scenarios: ["ai-traffic-walkability", "enterprise-service-copilot", "public-safety-operations-review"]
---

# 京张智脉·光晕 / Jing-Zhang AI Heritage Halo

## 设计概念：京张智脉·光晕

以京张铁路遗址公园为历史与公共空间主脉，三处重点区域（众智园、AI原点社区、大钟寺）为创新锚点，形成"一带三核、多点场景、蓝绿慢行复合环"的空间组织。"智脉"是铁路被AI能量激活后的新身份，"光晕"是三核向周边辐射创新能量的设计概念——光晕不是红线，不是开发量承诺，只是影响范围标注 [source:AGENT-TASKBOOK] [standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK]。

双轨并行：轨道一承载百年京张文化带（遗址保护、慢行贯通、公共空间、文化叙事），轨道二承载AI融合创新带（AI创新生态、智能基础设施、未来经济形态）。两条轨道并行不悖、相互赋能 [depth:overall_spatial_structure]。

## 设计依据与资料清单

本方案以《百年京张AI创新带城市设计国际方案征集资格预审公告》为第一依据 [source:OFFICIAL-ANNOUNCEMENT]，以 `brief/site-package/` 中经维护者登记的临时粗略边界、重点区域、枚举、指标和来源清单为机器可读依据 [source:SITE-PACKAGE]。完整来源和标准覆盖保存在 `sources.json`、`standard_matrix.json` 与 `design_depth_matrix.json`。

官方精确 polygon 未公开，仓库以 `provisional_boundaries.geojson` 提供临时粗略边界 [source:BOUNDARY-SOURCE]。所有 geometry 文件标注 `provisional_constraint`、`official_boundary=false`，只能用于方案生成和讨论，不能作为 official redline。组织方数据缺口不阻断内容评分，官方数据发布后全部图层与指标必须重算 [depth:risk_missing_data] [depth:metrics_recalculation]。

![资料证据链与提交包关系图](assets/figures/site-overview.png)

| 参数 | 阶段 | 证据级别 | 依据 |
|------|------|----------|----------------|
| 场地面积 11,412,825 ㎡ | 总体 | A 结构化复算 | [metric:site_area_sqm] |
| 绿地率 48.7%、公共空间率 2.5% | 总体 | A 结构化复算 | [metric:green_ratio] |
| 建筑覆盖率 5.7%、道路 42.3km | 总体 | A 结构化复算 | [metric:building_footprint_area_sqm] |
| 三个重点区 368.4 ha | 总体 | A 结构化复算 | [metric:key_area_count] |
| 建筑数量/高度/功能比例 | 重点区 | B 概念示意 | 待现状调查与控规确认 |
| 拆改留比例 | 重点区 | B 概念示意 | 待质量鉴定与结构评估 |
| 分期年份与资金渠道 | 实施 | C 实施假设 | 待权属、资金、审批确认 |

**分级**：A=可由GeoJSON复算；B=概念示意待确认；C=实施假设。任何B/C级参数不写入正式结论 [source:PROCESSED-MISSING-DATA-CHECKLIST] [depth:extant_conditions_evidence]。

## 三层范围工作框架

公告确定三个层次：统筹研究范围（43.6 km²）关注AI产业生态与战略定位；总体设计范围（11.4 km²）关注城市更新总体框架、产业空间布局和交通市政支撑；重点区域范围（368.4 ha）关注三处片区的详细设计 [source:OFFICIAL-ANNOUNCEMENT]。三层范围在 `compliance_matrix.json` 中逐条映射 [depth:three_level_scope_framework]。

![三层范围与空间工作框架图](assets/figures/land-use-structure.png)

| 层级 | 设计问题 | 方案回答 | 数据落点 |
| --- | --- | --- | --- |
| 统筹研究 | AI产业生态如何组织 | "高校策源-开源协作-企业转化-公共体验-国际传播"创新链 | compliance_matrix.json |
| 总体设计 | 产业空间、更新、交通如何落图 | 用地、建筑、道路、绿地、公共空间、分期图层 | [data:geometry/land_use.geojson#LU-001] |
| 重点区域 | 三处片区如何达到详细设计深度 | 分别提出定位、空间动作、AI场景和实施依赖 | [data:geometry/key_areas.geojson#PROV-KEY-001] |

## 统筹研究范围产业与未来城市研究

本方案提出"五段创新链"组织海淀AI产业资源：①高校策源（基础研究）→②开源协作（知识共享）→③企业转化（产品化）→④公共体验（场景开放）→⑤国际传播（全球对话）。"三区两翼"布局：三区形成"研发→转化→产业"南北主轴；中关村科技服务翼（西）提供IP、资本、标准服务；小月河场景翼（东）提供场景、数据、公共测试 [source:AGENT-TASKBOOK] [depth:overall_spatial_structure]。

未来城市形态研究聚焦AI如何改变六类日常活动：工作（智能体辅助，保留实体会议）、生活（AI便民终端，人工柜台兜底）、社交（活动匹配，不干预选择）、学习（AI教育，不替代课堂）、交通（慢行导航，静态地图等价）、公共服务（需求预测，电话纸本等价）。所有AI介入均保留非数字替代通道 [source:PROCESSED-FACT-PACK]。

品牌命名为"京张智脉·光晕"，以"双轨∞"为核心符号（`assets/logo.svg`），三色光晕对应三核：众智园（橙·创新加速）、AI原点社区（蓝·人才生态）、大钟寺（绿·产业集聚）。

## 总体设计范围城市更新与控规深度城市设计

总体设计范围（11.4 km²）要求达到控制性详细规划的城市设计深度。用地分区14宗，覆盖率100% [metric:land_use_coverage_ratio]。建筑基底648,798 m²，129栋 [metric:building_footprint_area_sqm] [metric:building_count]。道路网络42.3km [metric:road_network_total_length_m]。

用地以AI研发与产业（~30%）、公共服务（~12%）、居住与人才公寓（~15%）、绿地与广场（~35%）、交通设施（~8%）为概念分配（B级，待控规确认）。拆改留采用"微更新+节点激活"原则：保留~35%、改造~40%、新建~25%（概念假设，待现状鉴定）[depth:land_use_layout] [depth:retain_renovate_demolish]。

建筑高度分三档（概念建议，待控规确认）：众智园沿河60-80m、内部4-6层低密；原点社区3-5层近校过渡、6-8层骨干路；大钟寺站周边80-100m TOD、外围6-8层 [depth:height_massing_character]。容积率、建筑密度为unknown（待正式控规确认）[depth:development_intensity_controls]。

## 重点区域详细设计

![三处重点区域索引与设计任务图](assets/figures/key-areas.png)

### 众智园AI自主创新加速区 (192.92 ha)

花园型全栈自主创新街区。建筑概念示意约80-100栋，以AI研发办公（60%）、中试实验室（15%）、产业展示（10%）、配套（15%）为主。沿清河布局2-3栋标志性研发总部（概念高度60-80m），内部4-6层低密花园式。核心绿轴串联低碳创新广场、AI测试花园和标准治理展示区。清河滨水1.5km连续慢行步道+产业展示节点+生态雨洪花园。绿地率≥40%。

AI场景：自主模型测试场、标准制定与安全治理工作坊、低碳算力体验馆、创新成果展厅 [data:geometry/key_areas.geojson#PROV-KEY-001] [depth:three_key_area_detailed_design]。

### 北京AI原点社区 (104.32 ha)

近校型成果转化与人才社区。约40-50栋建筑，成果孵化办公（45%）、人才居住（25%）、开源协作（15%）、配套（15%）。紧邻高校3-5层低层过渡，骨干路6-8层混合。核心公共空间"原点广场"面向开源发布厅和成果展示中心。沿校区-社区边界800m"知识共享走廊"。3处校区-园区慢行联系通道。绿地率≥35%。

AI场景：开源社区发布厅、成果孵化展示长廊、人才特区服务中心、夜间协作空间 [data:geometry/key_areas.geojson#PROV-KEY-002]。

### 大钟寺AI产业聚集区 (72.05 ha)

城市型智能经济与国际交往街区。约30-40栋建筑，头部企业总部（50%）、智能体展示（20%）、商业文化（20%）、数据要素（10%）。站周边200m TOD高强度开发（概念高度80-100m），外围6-8层。核心公共空间为"四象限步行连通系统"——以轨道站点为中心，通过地下通道和地面慢行绿道连接四个象限。绿地率≥30%，强调垂直绿化与屋顶花园。

AI场景：智能体互操作性测试场、数据要素会客厅、国际路演中心、AI+消费体验街 [data:geometry/key_areas.geojson#PROV-KEY-003]。

## AI 创新生态、人才画像与 AI+ 场景

| 用户画像 | 典型需求 | 空间响应 | 自检边界 |
| --- | --- | --- | --- |
| 开源开发者 | 发布、协作、测试 | 原点社区开源发布厅、代码墙、夜间协作空间 | 不采集个人轨迹；聚合统计 |
| 初创团队 | 低成本办公、算力、试验场 | 众智园共享测试场、端侧算力服务点 | 算力和数据需另行授权 |
| 头部企业访客 | 展示、商务、人才招聘 | 大钟寺国际路演客厅、轨道接驳 | 企业标识须清权 |
| 周边居民 | 通勤、休闲、社区服务 | 遗址公园慢行环、社区服务嵌入 | 不将居民画像用于商业推荐 |
| 高校师生 | 成果转化、跨校协作、慢行 | 校区-园区慢行缝合、成果转化驿站 | 校园数据需授权 |

| 场景卡 | 空间载体 | AI能力 | 失败模式 | 人工升级 | 数据来源 | 运营主体 |
| --- | --- | --- | --- | --- | --- | --- |
| 01 开源发布厅 | AI原点社区 | 代码贡献热力图、PR分类 | 分类误判 | 管理员审核+社区仲裁 | GitHub公开API | 社区共建委员会 |
| 02 安全治理沙盒 | 众智园 | 模型行为分析、对抗测试 | 对抗样本绕过 | 独立安全审计 | 测试模型公开输出 | 标准治理联合体 |
| 03 端侧算力驿站 | 总体范围节点 | 负载预测、节能调度 | 负载偏差、节点离线 | 手动调度+人工巡检 | 匿名聚合统计 | 市政+运营商 |
| 04 AI慢行导航 | 遗址公园带 | 路径推荐、拥挤预测、无障碍 | 传感器盲区、预测不准 | 人工勘测+无障碍走查 | 匿名传感器（不采集轨迹） | 公共空间运营方 |
| 05 大钟寺路演客厅 | 大钟寺聚集区 | 参会者匹配、日程推荐 | 推荐偏差 | 人工协调 | 企业自报+公开信息 | 市场化平台 |
| 06 清河低碳创新廊 | 众智园临清河 | 环境预测、使用量识别、碳排估算 | 传感器漂移 | 人工巡检+数据校准 | 环境传感器 | 众智园运营方 |
| 07 近校成果转化街 | AI原点社区 | 技术匹配、专利图谱、投融资匹配 | 匹配不准 | 专家评审+IP审核 | 经授权成果披露 | 高校合作运营 |
| 08 数据要素会客厅 | 大钟寺片区 | 数据质量评估、合规检查、交易匹配 | 质量偏差、合规遗漏 | 独立数据合规审计 | 仅合规数据+审计日志 | 第三方数据治理 |
| 09 AI生活服务样板街 | 社区商业交汇 | 需求预测、资源匹配、异常检测 | 预测偏差、分配不公 | 社区团队人工审批 | 用户授权+公开数据 | 社区商业联合 |
| 10 全球AI活动周路线 | 一带公共空间 | 人流预测、多语言导览、活动推荐 | 翻译不准、人流预测偏差 | 安全审查+文化审核 | 场地方公开信息 | 活动组委会 |

所有AI场景遵守数据最小化、公开来源、可解释和人工复核原则。城市智能体辅助识别慢行断点、公共空间热力和安全风险，但不替代规划审批、不输出未授权个人画像、不声称获得官方实施承诺 [source:AGENT-TASKBOOK] [standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK]。

**三层智能体协同**：L1空间感知层（边缘智能体，匿名聚合环境数据）→ L2场景服务层（10个场景智能体）→ L3城市协调层（统筹调度，人工确认后执行）。所有智能体输出保持"建议"属性，故障时降级为人工操作。数据最小化原则：不采集个人轨迹，不进行个人画像，居民有权退出 [source:AGENT-TASKBOOK]。

**Agent任务响应**：Agent.1品牌（双轨∞符号，三色光晕，`assets/logo.svg`）；Agent.2 AI生态案例（8个全球案例提炼机制+8项本地设施）；Agent.3 AI场景（10张场景卡+3个产业测试场景）；Agent.4公共空间（3个朝圣地标+12个组件+5维荣誉体系）；Agent.5文化叙事（铁路遗产→中关村精神→AI新文化三层）；Agent.6活动运营（年度AI创新周+全球AI开放日+朝圣路线）。详见 `compliance_matrix.json`。

> 以上Agent任务内容均为概念建议，不构成已确定的政府活动或实施安排。

## 三区两翼协同与区域协作框架

三核通过"三区两翼"形成功能互补：众智园→原点社区（技术输出→人才回馈）、原点社区→大钟寺（孵化成果→产业落地）、大钟寺→众智园（市场反馈→技术迭代）。中关村科技服务翼提供IP/资本/标准，小月河场景翼提供场景/数据/公共测试 [depth:overall_spatial_structure]。

| 五大功能 | 空间锚点 | 产业机制 | 治理主体 | 实施项目 |
| --- | --- | --- | --- | --- |
| ① AI全栈自主创新 | 众智园+西翼 | 大模型训练评测、安全沙盒、标准制定 | 标准治理联合体 | 清河创新界面、安全治理沙盒 |
| ② 世界级AI生态 | 原点社区+东翼 | 开源协作、孵化加速、人才特区 | 社区共建委员会 | 成果转化街、开源发布厅 |
| ③ AI+场景赋能 | 小月河翼+一带 | 10个场景卡、3个测试场景 | 公共空间运营方 | 大钟寺步行连通、算力节点 |
| ④ 智能化AI活力城市 | 复合环 | 慢行AI导航、公共空间管理 | 公共空间运营方+市政 | 遗址公园AI慢行系统 |
| ⑤ AI治理话语权 | 众智园+大钟寺 | 安全治理、数据要素、国际活动 | 标准联合体+国际组委会 | 路演客厅、数据要素会客厅 |

区域协同只传递脱敏的任务模式、测试协议和版本化服务标准，不搬运个人记录或企业受限资料 [source:V11-REGIONAL-COLLABORATION]。

## 用地、建筑规模与拆改留方案

用地分类依据 [standard:MNR-LAND-USE-CLASSIFICATION-GUIDE]，14宗用地完整覆盖设计边界 [data:geometry/land_use.geojson#LU-001]。建筑基底648,798 m²，129栋 [metric:building_footprint_area_sqm] [metric:building_count]。拆改留：保留~35%（待质量鉴定）、改造~40%（待结构评估）、新建~25%（待用地确认）[depth:retain_renovate_demolish]。高度控制三档（概念建议，待控规确认）[depth:height_massing_character]。容积率为unknown [depth:development_intensity_controls]。

## 交通、轨道、市政与公共服务设施

交通以慢行优先为原则，道路网络42.3km [metric:road_network_total_length_m]。慢行主轴9km南北贯通，3条横向联系缝合校区-园区-社区，大钟寺站TOD一体化。关键慢行断点：北五环跨环路、五道口、大钟寺路口。先期缝合2-3处（JZ-01），以临时设施验证通行需求 [depth:traffic_rail_slow_parking] [data:geometry/roads.geojson#ROAD-001]。

市政设施：端侧算力节点5-10个（服务半径500m）、AI公共服务站三核各1处（800m）、分布式能源结合绿地和屋顶。管线、消防、防洪等工程资料缺失时列为深化前置条件 [depth:municipal_new_infrastructure]。

![交通慢行与蓝绿公共空间复合系统图](assets/figures/mobility-bluegreen.png)

## 蓝绿空间、公共空间与城市风貌

绿地面积5,561,347 m²，绿地率48.7% [metric:green_space_area_sqm] [metric:green_ratio]。公共空间279,961 m²，占比2.5% [metric:public_space_area_sqm]。"一轴三廊多节点"蓝绿系统：京张遗址公园活力带（9km）+清河滨水廊+小月河生态廊+校区绿廊。慢行与蓝绿重叠率≥60% [depth:blue_green_public_space] [data:geometry/green_space.geojson#GREEN-001] [data:geometry/public_space.geojson#PUBLIC-001]。

城市风貌融合三层文化：铁路遗产（清华园车站、铁轨枕木记忆）、中关村精神（电子一条街到AI策源地）、AI新文化（开源共享、人机协作）。风貌控制分三档：文保区（严格保护）、建成区（风貌引导）、新建区（弹性控制）[standard:MOHURD-URBAN-DESIGN-MEASURES]。

## 更新项目清单、实施政策与分期计划

| 项目编号 | 项目名称 | 类型 | 建议分期 | 投资层级 | 评估指标 | 证据 |
| --- | --- | --- | --- | --- | --- | --- |
| JZ-01 | 慢行断点缝合 | 公共空间/交通 | 近期(1-3年) | 中小型 | 断点缝合数、连通率 | [data:geometry/roads.geojson#ROAD-001] |
| JZ-02 | 清河创新界面 | 蓝绿/产业展示 | 近期(1-3年) | 中小型 | 滨水开放长度 | [data:geometry/green_space.geojson#GREEN-001] |
| JZ-03 | 成果转化街 | 城市更新/产业 | 中期(3-7年) | 中大型 | 转化率、入驻企业数 | [data:geometry/buildings.geojson#BLDG-001] |
| JZ-04 | 大钟寺站城连通 | 轨道/慢行 | 中期(3-7年) | 中大型 | 步行连通度 | [data:geometry/public_space.geojson#PUBLIC-001] |
| JZ-05 | AI公共服务算力节点 | 新基建 | 近期试点(1-3年) | 中大型 | 算力节点数、可用率 | [data:geometry/constraints.geojson#CONSTRAINTS] |
| JZ-06 | 全球AI活动周路线 | 运营/品牌 | 近期启动(1年内) | 小型 | 参与度、传播量 | [data:geometry/phasing.geojson#PHASE-001] |

> 投资估算仅给"中小型/中大型"相对层级。所有项目可先以轻量设施、运营活动或服务平台启动 [depth:renewal_project_list]。

### 京张四闸：实施放行机制（Jing-Zhang Four-Gate Release Protocol）

京张铁路的信号系统用"闸"控制列车能否通行。本方案把这个工程传统转化为实施管理规则：每个项目必须依次通过四道闸门，缺一闸则项目保持 `halted`，不得推进 [standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK] [depth:phasing_implementation]。

| 闸门 | 名称 | 必须确认的条件 | 未通过则 | 对应里程碑 |
| --- | --- | --- | --- | --- |
| **G0 资格闸** | Readiness | 权属边界、资金来源、审批路径、运营主体四项齐备 | 项目保持 `halted` | M1-M6 前置 |
| **G1 试点闸** | Pilot | 轻量先行验证完成：临时设施/运营活动/数据采集至少运行90天，产出试点报告 | 不进入正式建设 | M1-M4 |
| **G2 放行闸** | Release | 试点报告通过Go/No-Go评审：社会接受度达标、运营数据达标、安全合规达标 | 不进入二期，调整重来 | M5→M7 |
| **G3 退役闸** | Retirement | 服务/设施退出时：公开退役记录、说明原因、提供替代方案、完成现场恢复 | 不得拆除或废弃 | 生命周期末端 |

**四闸检验规则**：G0检查四项条件（权属/资金/审批/运营主体），缺一不可→`halted`。G1要求轻量先行90天后提交试点报告（含使用人次、满意度、成本、社区意见、安全事件）。G2是Go/No-Go决策点（社会接受度达标+运营数据达标+安全合规0重大事件，三项全过=Go）。G3要求退出留痕（退役原因、替代方案、现场恢复、居民反馈，记录保留≥3年）。

**一句话检验**：一个项目如果拿不出 G0 资格确认、G1 试点报告、G2 放行决议和 G3 退役预案中的任一项，它就还没有准备好进入下一阶段。（假设 A-GATE-001）

**分期实施**（概念分期，待权属、资金、审批路径确认）：
- **近期（1-3年）**：JZ-01慢行断点、JZ-06活动周、JZ-05算力试点。轻量运营和临时设施为主
- **中期（3-7年）**：JZ-02清河界面、JZ-03成果转化街、JZ-04站城连通。城市更新和公共空间
- **远期（7-15年）**：区域协作网络成型，全球AI创新朝圣地标建成

四层运营治理：L1战略统筹（联席治理委员会）→ L2片区运营（市场化运营公司）→ L3公共治理（社区+数据治理委员会）→ L4技术合规（独立安全审计）。运营主体通过公开比选产生 [depth:phasing_implementation]。每个阶段设Go/No-Go决策点，未达标不进入下一阶段。

经济可行性：6个项目概念级投资估算合计10.4-21.6亿元（±50%精度）。资金来源以财政引导资金（20-30%）、政策性贷款（15-25%）、产业基金（15-25%）、企业自投（20-30%）和运营收益（5-10%）组合。正式估算需专业造价机构完成。（假设 A-INVESTMENT-001）

> 概念分期不构成实施承诺。正式实施计划需在深化设计阶段由主管部门和运营主体共同确定。

## 指标体系、面积复算与合规矩阵

指标体系包含场地面积、重点区域面积、绿地与公共空间比例、建筑基底、更新项目数量、AI场景节点、慢行连通指标和自检状态。所有known指标可从GeoJSON复算；unknown指标给出原因和前置条件 [depth:metrics_recalculation]。完整数值保存在 `metrics.json` [metric:site_area_sqm] [data:geometry/green_space.geojson#GREEN-001]。

![核心指标复算与证据链图](assets/figures/metrics-evidence.png)

合规矩阵覆盖公告1.3、1.4、1.5与agent.1-agent.6全部必选任务，每条任务对应章节、图层、指标、图纸和HTML证据 `compliance_matrix.json`。

## 风险、版权与合规说明

**双语**：proposal.md与proposal.en.md提供完整中英对照。A3/A0、HTML和含文字图件均提供对应语言副本。所有图片、图纸、图标、数据和代码资产在 `sources.json` 或 `report/copyright_statement.md` 中说明来源、许可和授权状态。HTML不加载远程脚本、地图瓦片、字体、iframe、表单或外部API [depth:risk_missing_data]。

**版权**：所有视觉资产为原创矢量设计与程序绘制。不使用企业商标、人物肖像或第三方照片。字体许可：文泉驿微米黑（开源）、DejaVu Sans（开源）。

**假设管理**：未验证参数登记在 `assumptions.json`。任何B/C级参数不写入正式结论。

**数据隐私**：所有AI场景遵循数据最小化——不采集个人轨迹，不进行个人画像，不用于商业推荐。所有数据流向可审计、可追溯。居民有权退出任一AI服务且退出后服务质量不降级。

**自检**：提交包已通过全部四道门（确定性校验、空间校验、视觉包装、专业证据）。`self_check.json`。全部边界和面积标注为provisional；绩效声明统一为"未获授权·未现场运行"。

## 参考资料

- [source:OFFICIAL-ANNOUNCEMENT] — 竞赛资格预审公告
- [source:SITE-PACKAGE] — 机器可读设计任务书与边界数据
- [source:BOUNDARY-SOURCE] — 临时边界来源
- [source:SOURCE-REGISTRY] — 来源用途边界
- [source:AGENT-TASKBOOK] — 面向智能体任务书
- [source:PROCESSED-FACT-PACK] — 处理资料包
- [source:PROCESSED-MISSING-DATA-CHECKLIST] — 缺资料清单
- [standard:PROJECT-OFFICIAL-ANNOUNCEMENT] — 公告标准
- [standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK] — 智能体任务书标准
- [standard:MOHURD-URBAN-DESIGN-MEASURES] — 住建部城市设计措施
- [standard:MOHURD-CONTROL-DETAILED-PLANNING] — 住建部控规
- [standard:MNR-LAND-USE-CLASSIFICATION-GUIDE] — 自然资源部用地分类
- [standard:MOHURD-ARCH-DESIGN-DEPTH-2016] — 建筑设计深度
