---
title: "百年京张·AI智枢生态带"
author_github: "GJYNBB"
language: "zh"
proposal_format_version: "2"
bilingual_contract_version: "1"
translation_file: "proposal.en.md"
license: "COMMUNITY-DISPLAY-ONLY"
summary: "以京张铁路遗产公共空间为城市主脊，构建‘一带三核两翼’AI创新生态、十类可测试城市AI场景、三处AI朝圣地标与长期运营机制；所有空间面积均保留 provisional 精度声明。"
tracks: ["ai-traffic-walkability", "enterprise-services-ecosystem", "civic-agent-governance"]
scenarios: ["ai-traffic-walkability", "enterprise-service-copilot", "public-safety-operations-review"]
---

# 百年京张·AI智枢生态带

## 设计依据与资料清单

本方案以《百年京张AI创新带城市设计国际方案征集资格预审公告》和面向智能体任务书为任务依据 [source:OFFICIAL-ANNOUNCEMENT] [source:AGENT-TASKBOOK] [standard:PROJECT-OFFICIAL-ANNOUNCEMENT] [standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK]。场地事实、任务边界和缺资料事项分别回到 `brief/site-package/`、`data/source_registry.json` 与 `data/processed/agent_fact_pack.md` [source:SITE-PACKAGE] [source:SOURCE-REGISTRY] [source:PROCESSED-FACT-PACK]。

当前 `geometry/site_boundary.geojson` 和 `geometry/key_areas.geojson` 均为 **provisional rough geometry**，不是官方红线、法定控规或审批边界。GeoJSON 以 EPSG:4326 存储，面积复算转 EPSG:4548；总体范围面积、绿地比例、公共空间比例和三处重点区面积均是低置信度的可复算设计模型值，正式 polygon 到位后必须整体重算 [data:geometry/site_boundary.geojson#SITE-001] [data:geometry/key_areas.geojson#PROV-KEY-001] [metric:site_area_sqm] [metric:green_ratio] [metric:public_space_ratio]。

本方案不把外部案例当作海淀场地事实。Kendall Square、Toronto Vector、STATION F、one-north/Kampong AI、Seoul AI Hub 与 Mila 仅用于比较“创新生态如何组织空间与运营”，不复制其企业名单、数值或政策承诺 [source:CASE-KENDALL-SQUARE] [source:CASE-TORONTO-VECTOR] [source:CASE-PARIS-STATION-F] [source:CASE-SINGAPORE-ONE-NORTH] [source:CASE-SEOUL-AI-HUB] [source:CASE-MONTREAL-MILA]。

## 三层范围工作框架

三层范围被设计成同一套“研究—空间—原型”递进系统 [depth:three_level_scope_framework] [depth:overall_spatial_structure]：

| 层级 | 本方案完成的工作 | 可审计证据 |
| --- | --- | --- |
| 统筹研究范围 | AI创新生态、三区两翼、区域协作接口、品牌与长期运营 | 本文 agent.1/2/6、`compliance_matrix.json` |
| 总体设计范围 | 一带三核两翼、用地/交通/蓝绿/公共空间/分期和六项更新项目 | [data:geometry/land_use.geojson#LU-001] [data:geometry/roads.geojson#ROAD-001] [data:geometry/phasing.geojson#PHASE-001] |
| 三处重点区域 | 众智园“开放研发花园”、AI原点“校园—街区转化缝”、大钟寺“站城四象限交换厅” | [data:geometry/key_areas.geojson#PROV-KEY-001] [data:geometry/key_areas.geojson#PROV-KEY-002] [data:geometry/key_areas.geojson#PROV-KEY-003] |

总体空间概念为 **“京张智脉共生带 / Jing-Zhang Intelligence Commons”**。京张遗址公园是公共空间与文化主脊；三处重点区是创新核；中关村科技服务翼和小月河场景赋能翼是两条概念协作接口。两翼不是新增规划红线，而是把资本/IP/专业服务与社区/测试/公共服务分别接入三核的运营网络。

## 统筹研究范围产业与未来城市研究

### agent.1 一带总体概念、品牌与三区两翼

**主名称**：京张智脉共生带。英文名：**Jing-Zhang Intelligence Commons**。传播短名：**JZ·AI Commons**。命名把“铁路遗产的连续公共空间”与“AI公共知识、开源协作和城市服务”绑定，避免把项目识别仅做成产业园品牌。

**Logo/VI 方向**：标志由三种基本构件组成：两条平行轨线代表京张铁路记忆；三个节点代表众智园、AI原点、大钟寺三核；轨线在节点间形成连续数据脉冲，构成近似“JZ”与开放回路的负形。图形必须可用单色线稿、16 px 图标和大尺度导视三种尺度复现。视觉系统采用“遗产石墨黑 + 公共空间青绿 + 智能电光蓝”三色语义；不绑定专有字体，成图时优先使用本机可合法嵌入的 CJK 开源/系统字体，并在缺字时改用字形覆盖完整的替代字体。任何新增字体或图像资产必须登记来源和许可。

**三大定位—五大功能**直接对应任务书 [source:AGENT-TASKBOOK]：

- 百年京张文化带：遗产叙事、公共空间和步行体验作为“公共底座”。
- 都市AI生活体验带：把AI服务放进日常通勤、社区、教育、健康、法律信息与公共空间。
- AI融合创新带：形成从科研、开源、测试、企业转化到国际传播的闭环。
- 五大功能分别落到：自主创新（众智园）、世界级生态（原点+两翼）、AI+场景（小月河翼+全带）、AI活力城市（公共空间+生活服务）、AI治理话语权（众智园安全治理沙盒+公开审计）。

**三区两翼协同回路**：

1. AI原点社区：科研成果、人才和开源社区的“源头核”。
2. 众智园：全栈研发、模型评测、安全治理和低碳基础设施的“验证核”。
3. 大钟寺：智能终端、内容消费、路演和国际交流的“市场核”。
4. 中关村科技服务翼：以知识产权、法务、投融资、企业服务和全球资源配置为服务接口，不虚构新增行政边界。
5. 小月河场景赋能翼：把社区、蓝绿空间、慢行和公共服务作为开放测试界面，优先验证公共利益。

区域协作采用“接口而非承诺”的表达：北纬社区作为社区型日常服务协同接口；未来科学城、怀柔科学城作为科研设施/科学装置成果协同接口；经开区作为制造验证与产业化接口；京津冀作为跨区域人才、应用场景与供应链协作接口。任何具体合作项目都需相关主体另行确认，本文不声称政府间合作已建立。

### agent.2 六个全球案例与 AI 创新生态图谱

| 案例 | 可验证特征 | 对京张的转译 |
| --- | --- | --- |
| Cambridge Kendall Square [source:CASE-KENDALL-SQUARE] | 研究创新与住房、零售、公共空间、交通共存 | 不做封闭园区；创新空间必须与居民公共空间共享 |
| Toronto Vector Institute [source:CASE-TORONTO-VECTOR] | 研究人才连接企业采用与产业转化 | 原点负责人才/研究，众智园负责测试，大钟寺负责应用展示 |
| Paris STATION F / F/ai [source:CASE-PARIS-STATION-F] | 高密度创业、伙伴服务、项目制孵化和活动社区 | 把“空间招商”改为“项目+服务+活动”的持续运营 |
| Singapore one-north / Kampong AI [source:CASE-SINGAPORE-ONE-NORTH] | 工作—生活、专用基础设施、测试床和社区营造 | 人才空间与测试空间邻近，但日常公共服务保持非AI兜底 |
| Seoul AI Hub [source:CASE-SEOUL-AI-HUB] | 城市级AI集群、企业支持与人才生态 | 建立可公开预约的企业服务/测试接口，而非一次性展示 |
| Montréal Mila [source:CASE-MONTREAL-MILA] | 大学研究锚点、开放科学、产业伙伴与创业转化 | 把开源发布、研究交流与创业转化组织在可步行街区 |

由案例提炼出本项目的 **8 层 AI 生态图谱**：知识源（高校/研究）→人才与开源→算力/工具→数据治理→资本/IP/专业服务→企业转化→城市测试场景→公共利益与国际传播。空间映射为：原点负责“知识—人才—开源”，众智园负责“算力—治理—测试”，大钟寺负责“企业—市场—传播”，中关村翼补“资本/IP/服务”，小月河翼补“社区场景—公共利益”。这是一张运营关系图，不是企业现状清单。

**全要素保障机制**：土地和空间以可逆更新/共享首层为优先；产业以开放课题和场景清单连接；资金只提出多元投入方法，不虚构额度；人才通过短租、夜间协作、公共服务和国际活动支持；算力采用分级接入和能耗/散热前置评估；数据以授权、最小化、审计、退出为前提；场景通过公开申请、风险分级、沙盒测试、人工验收后再扩大。

## 总体设计范围城市更新与控规深度城市设计

空间结构采用“一带三核两翼、多点场景、蓝绿慢行复合环”。用地、建筑、道路、绿地和公共空间均为设计提案图层 [data:geometry/land_use.geojson#LU-001] [data:geometry/buildings.geojson#BLDG-001] [data:geometry/roads.geojson#ROAD-001] [data:geometry/green_space.geojson#GREEN-001] [data:geometry/public_space.geojson#PUBLIC-001]，不替代控规 [standard:MOHURD-CONTROL-DETAILED-PLANNING] [standard:MNR-LAND-USE-CLASSIFICATION-GUIDE]。

空间动作分四类：

- **缝合**：修补京张遗址公园慢行断点、跨路口和站点接驳。
- **打开**：把园区首层、共享庭院、滨水界面转成可预约但日常可进入的公共/半公共界面。
- **嵌入**：把成果发布、企业服务、公共服务、轻量算力嵌入已有街区，而不是依赖大拆大建。
- **可逆**：活动、测试和展示优先采用可拆卸设施，官方红线、文保、消防和市政条件确认前不形成永久工程承诺。

[depth:land_use_layout] [depth:development_intensity_controls] [depth:retain_renovate_demolish]

## 重点区域详细设计

| 重点区 | 空间原型 | 核心空间动作 | AI/产业动作 | 实施前置 |
| --- | --- | --- | --- | --- |
| 众智园，约 193 ha（provisional）[metric:zhongzhiyuan_area_sqm_provisional] | **开放研发花园** | 共享测试庭院—清河公共客厅—步行研发环；首层打开、滨水连续 | 安全治理沙盒、模型评测、低碳算力体验、标准工作坊 | 河道/防洪、消防、产权、能源与正式边界 |
| AI原点，约 104 ha（provisional）[metric:ai_origin_area_sqm_provisional] | **校园—街区转化缝** | 5–10分钟步行连续、首层成果发布/服务、低扰动微更新 | 开源发布、知识产权/法务、近校孵化、人才社区 | 校园/园区边界、权属、轨道和首层业态确认 |
| 大钟寺，约 72 ha（provisional）[metric:dazhongsi_area_sqm_provisional] | **站城四象限交换厅** | 站点四象限步行接驳、公共客厅、商业/产业界面连续 | 智能终端展示、国际路演、数据合规会客厅 | PROV-KEY-003 不证明站点包含；需站点工程/道路/管线复核 |

三处 polygon 均是粗略占位，面积只以约数展示；正式边界发布后，指标、图件和所有重点区结论必须整体重算 [depth:three_key_area_detailed_design]。

## AI 创新生态、人才画像与 AI+ 场景

### 8 类用户画像

| 画像 | 关键需求 | 非数字兜底/公共利益边界 |
| --- | --- | --- |
| 开源开发者 | 发布、协作、测试、社区声誉 | 不采集个人轨迹；可匿名参加开放活动 |
| 初创团队 | 低成本空间、算力入口、试验场 | 算力/数据另行授权，试验失败可退出 |
| 企业访客 | 展示、商务、招聘、国际接待 | 企业标识/演示数据需清权，不暗示政府背书 |
| 高校师生 | 成果转化、跨校协作、学习 | 校园数据与科研成果需授权 |
| 周边居民 | 通勤、休闲、社区服务、低扰动更新 | 不做商业画像或信用评分 |
| 老年人 | 易读导视、休息、人工咨询 | 保留纸质/实体导视和人工窗口 |
| 残障及非智能终端使用者 | 连续无障碍路径、可感知信息 | 无手机也能完成基本通行和服务 |
| 夜间劳动者/服务人员 | 夜间通勤、安全、休息与基本服务 | 不以人脸或持续定位作为安全前提 |

[metric:persona_count]

### agent.3 十张可运营、可退出 AI 场景卡

| ID | 空间ID/载体 | 数据与AI能力 | 运营角色 | 人工接管与失败降级 | 验收/KPI与退出 |
| --- | --- | --- | --- | --- | --- |
| S01 开源成果发布厅 | PROV-KEY-002 / 原点首层 | 投稿者自愿提交的代码/模型元数据；检索、摘要、展陈辅助 | 社区运营+活动主持 | 不追踪参会轨迹；人工主持可独立完成 | 发布内容权利可核验；争议内容下架 |
| S02 AI安全治理沙盒 | PROV-KEY-001 | 经授权测试集；评测、红队、日志分析 | 测试运营+安全负责人 | 高风险测试人工审批，一键停止/隔离 | 日志完整、越权阻断；无法隔离即停场景 |
| S03 端侧算力驿站 | 总体节点 | 设备健康/环境状态；边缘推理 | 设施运营+IT | 断网时导视/公共设施保持基础功能 | 可用性/能耗受控；能耗或散热不满足则降级 |
| S04 无障碍慢行导航 | ROAD-001 / PUBLIC-001 | 临时障碍、坡度、设施状态等非个人数据；路径建议 | 公共空间运营+人工服务点 | 实体导视、人工问询、无手机路线始终存在 | 错误路线可申诉；高误报时关闭AI提示 |
| S05 国际路演客厅 | PROV-KEY-003 | 经清权企业资料；多语摘要/字幕 | 场地运营+人工策展 | 人工审核敏感/商业内容 | 权利状态清晰；无授权内容不展示 |
| S06 清河低碳创新廊 | GREEN-001 / 众智园水岸 | 环境监测；低功耗状态提示 | 公共空间运营 | 生态/通行优先，传感器失效不影响步骑 | 绿地通行与生态优先；设备干扰即撤除 |
| S07 近校成果转化街 | PROV-KEY-002 | 公开政策/企业自愿需求；信息匹配 | 企业服务+专业机构 | 法律/投资判断必须人工签署 | 仅作线索匹配；错误推荐可更正/退出 |
| S08 数据合规会客厅 | PROV-KEY-003 | 授权记录/公开规则；合规解释 | 专业咨询+场地运营 | 无明确授权即不处理，保留申诉 | 授权可追溯；无法说明用途即停止处理 |
| S09 AI生活服务样板街 | PUBLIC-001 / 社区节点 | 公开服务信息；问答/导航 | 社区服务+专业窗口 | 医疗/法律/教育高影响事项转人工 | 不做资格自动决定；错误信息可纠正 |
| S10 全球AI活动周公共路线 | PHASE-001 / 全带 | 活动公开信息；多语导览 | 活动运营+公共安全岗位 | 平日仍是普通公共空间；活动许可独立获取 | 不影响基本通行；安全条件不足即缩减/取消 |

[metric:scenario_card_count] [data:geometry/public_space.geojson#PUBLIC-001] [data:geometry/roads.geojson#ROAD-001]

### 3 个产业测试验证场景

- **T1 无障碍导航故障注入**：模拟定位漂移、断网、设施状态过期和错误拥堵提示；通过标准是非AI导视仍可完成基本通行，错误建议有人工申诉和快速撤回路径。
- **T2 安全治理沙盒安全退出**：模拟异常输出、越权数据请求、测试域高负载；通过标准是人工一键停止、日志可追溯、测试域隔离、未授权数据不进入模型流程。
- **T3 公共服务人工复核**：向教育/医疗/法律信息助手输入低置信度和冲突问题；通过标准是高影响事项自动升级人工，系统明确“不确定”，人工结论不被模型覆盖。

以上是验证协议设计，不声称已经完成真实世界测试 [metric:validation_scenario_count]。

## 用地、建筑规模与拆改留方案

用地和建筑采用“先核现状—再分保留/改造/更新/新建—最后校准强度”的方法 [depth:land_use_layout] [depth:height_massing_character] [depth:retain_renovate_demolish]。当前缺少完整权属、现状建筑、正式控规和工程条件，因此不在本方案中给出审定容积率、建筑高度、建筑密度、退线或最终拆除对象；`floor_area_ratio` 保持 unknown [metric:floor_area_ratio]。

更新策略优先采用首层开放、可逆内装、共享庭院、桥下/边角空间提升和站点步行缝合；涉及永久建筑增量、结构改造、消防改变或历史文化资源的动作进入专业深化清单，不以概念图代替审批。

## 交通、轨道、市政与公共服务设施

交通系统把“轨道接驳—遗产公园慢行—两翼横向连接—三核步行环”作为骨架 [depth:traffic_rail_slow_parking]。ROAD-001 仅是设计中心线提案，不是道路红线 [data:geometry/roads.geojson#ROAD-001]。大钟寺的“四象限”是步行连续性设计命题，不声称已有站城一体化工程获批。

新型基础设施采用小型、分布式、可关闭原则 [depth:municipal_new_infrastructure]：端侧算力节点先验证能源、散热、噪声、消防和网络安全；公共服务不依赖单一数字入口；社区、老年人、残障人士和无智能终端使用者均保留人工/实体服务渠道。

## 蓝绿空间、公共空间与城市风貌

京张遗址公园、清河和小月河共同形成“文化主脊+蓝绿横向接口” [depth:blue_green_public_space] [standard:MOHURD-URBAN-DESIGN-MEASURES]。绿地比例和公共空间比例只作为 provisional 设计模型指标，不是控规承诺 [metric:green_ratio] [metric:public_space_ratio]。

### agent.4 三个 AI 朝圣地标、荣誉体系与组件库

1. **JZ-01 轨迹之门 / Trace Gate**：在遗产主脊的公共节点，用“铁路里程刻度+开源贡献时间轴”形成可步行穿越的知识门廊；不改变历史文物本体，位置需文保/产权核对。
2. **JZ-02 开源星图 / Open-source Constellation**：原点社区的可更新公共贡献墙，把开源项目、研究成果和公共价值贡献以人工审核后的非商业排行榜展示；支持撤回和更正。
3. **JZ-03 AI公共测试庭 / Civic AI Test Yard**：众智园的可预约开放测试庭院，以可拆卸设施展示安全评测、无障碍、低碳和城市服务原型；测试失败可立即撤场。

三地标共同构成“朝圣路线”，但保持日常公共空间属性 [metric:pilgrimage_landmark_count]。

**荣誉展示体系**不以资本规模排名，而设“开放贡献、公共利益、可靠性、安全治理、跨域协作”五类标签；每项展示必须有贡献主体、证据链接、授权状态、更新时间和撤回机制。

**公共空间组件库**包括：JZ-Bench 模块化休息/充电座椅、JZ-Beacon 双语低位无障碍导视、JZ-Canopy 可拆遮荫/雨棚、JZ-Edge 可关闭端侧算力柜、JZ-Stage 微型发布平台、JZ-Garden 雨洪/传感共构花园。组件优先采用可逆安装；工程规格在消防、结构、电力和市政条件确认后由专业团队深化。

### agent.5 文化叙事、导视与国际传播

叙事结构采用“三层时间”：**铁路把知识带进城市—中关村把知识变成创新—AI时代把知识变成公共协作能力**。历史事实只引用清权资料，不把概念叙事替代史实。

导视语法采用“轨线（方向）+节点（地点）+脉冲（活动/数字服务）”三种图形；中英文同位呈现，重要无障碍信息不依赖二维码。国际传播固定使用状态标签：`Concept Proposal / Provisional Geometry / Not Approved for Construction`，防止把投稿描述成已入选或已实施。

## 更新项目清单、实施政策与分期计划

六项更新项目从“设计动作”升级为可执行责任矩阵 [depth:renewal_project_list] [depth:phasing_implementation] [metric:renewal_project_count]：

| 编号 | 项目 | 牵头角色（建议） | 协作角色 | 时间窗口 | 关键资源/审批触点 | 验收与退出 |
| --- | --- | --- | --- | --- | --- | --- |
| JZ-01 | 遗产公园慢行断点缝合 | 公共空间/交通专业团队 | 公园、道路、社区运营 | 近期试点→中期工程 | 道路红线、桥下、无障碍、文保 | 基本通行连续；条件不明处仅做临时导视 |
| JZ-02 | 众智园清河创新界面 | 城市设计+景观团队 | 河道、防洪、园区、企业 | 中期 | 蓝线、防洪、产权、消防 | 生态/通行优先；未获条件不做永久建设 |
| JZ-03 | 原点近校成果转化街 | 更新运营主体 | 高校、园区、专业服务机构 | 近期运营→中期更新 | 权属、首层业态、消防 | 首层开放/服务可用；租赁/权属不成立则缩小范围 |
| JZ-04 | 大钟寺四象限步行连通 | 交通/站城专业团队 | 轨道、道路、商业运营 | 中长期 | 站点工程、道路交叉口、管线 | 步行连续性验证；不具备工程条件则保留地面级策略 |
| JZ-05 | 公共服务与端侧算力节点 | 数字设施运营 | 能源、网络安全、社区服务 | 近期小样 | 能源、散热、消防、网络安全 | 断网基本服务仍可用；能耗/安全不达标则关闭AI能力 |
| JZ-06 | 全球AI活动周公共路线 | 活动运营团队 | 场地、安全、社区、国际传播 | 年度运营 | 场地许可、安全、版权 | 不影响日常通行；许可或安全不足则缩线/取消 |

`geometry/phasing.geojson` 仅表达概念分期 [data:geometry/phasing.geojson#PHASE-001]。

### agent.6 年度活动与长期运营机制

年度活动不是“固定政府安排”，而是可由后续运营主体选择的参考日历：

- Q1 **Open Source Spring**：开源发布、贡献墙年度校验、青年开发者工作坊。
- Q2 **Civic AI Test Month**：无障碍、低碳、公共服务和安全沙盒公开测试。
- Q3 **Jing-Zhang AI Week**：三核联动的国际交流、路演、公共体验路线。
- Q4 **Responsible AI Review**：年度安全、隐私、公共利益和运营绩效复盘。

开发者社区采用公开行为准则、贡献署名、内容撤回、利益冲突披露和活动安全规则；场景开放采用“申请—风险分级—小样测试—人工验收—限时开放—复盘/退出”六步；预约同时保留线下窗口。国际传播通过双语网页、开放数据摘要、可复现案例说明和人类审核后的社交媒体素材进行。人才/企业转化路径是“活动参与→需求诊断→专业服务→测试场景→人工评审→自愿入驻/合作”，不以自动评分决定资源资格。

长期运营只设置方法性预算框架：公共空间基础运维、活动运营、数字设施、安全/合规、研究评估五类成本分别核算；具体金额、政府补贴、投资承诺均待真实运营主体和财务条件确认。

## 指标体系、面积复算与合规矩阵

`metrics.json` 将指标分成三类：

1. **provisional 可复算空间指标**：总体范围、绿地比例、公共空间比例、建筑基底和三处重点区派生面积，均为 low confidence，正式边界发布后重算 [depth:metrics_recalculation]。
2. **任务书结构计数**：三处重点区、10 场景、3 验证、8 画像、3 地标、6 项更新项目，可由当前方案文件直接计数。
3. **待真实数据/控规指标**：容积率、建筑高度、产业产值、人才密度、活动参与量、服务满意度等不得伪造；缺少可信基线时保持 unknown 或作为未来 KPI 方法，不写成既有成绩。

中英文可视化不得使用未登记的“18、0.85 HHI、42.8%、57.2%、18.6 km、500 m/85%、100%任务覆盖”等数字作为事实或已完成绩效；若未来需要展示，必须先在 `metrics.json` 中定义来源、公式、状态和置信度。

合规矩阵按公告与 agent.1–agent.6 分别指向专属章节、图层、指标和可视化位置，不再用同一组泛化证据机械覆盖所有任务。

## 风险、版权与合规说明

**双语合同**由 `proposal.md + proposal.en.md` 构成；两种语言必须对三处重点区、10 场景、3 验证、8 画像、3 地标、指标状态和风险声明保持实质等价。HTML、A3/A0 与含文字图件在重新渲染后也需逐页人工核对字形、裁切、对比度、图例和 provisional 警示。

当前主要专业前置条件为：正式总体/重点区 polygon、控规、道路红线、轨道工程、权属/现状建筑、市政管线、能源/排水、防洪、消防、文保和公共服务设施资料 [depth:risk_missing_data] [data:geometry/constraints.geojson#CONSTRAINTS]。在这些条件未确认前，本方案不声称官方批准、最终建设规模、拆改留结论、政府活动安排或资金支持。

所有外部案例只作文字比较研究，未复制其图片、Logo 或受保护版式；本方案新增的命名、Logo方向、组件和地标为投稿者概念设计。实际使用第三方字体、图片、企业标识、肖像或地图素材前必须另行完成许可登记。HTML 继续保持离线，不加载远程脚本、远程字体、地图瓦片、iframe、表单或外部 API。

## 参考资料

- `brief/public-brief.md`
- `brief/site-package/design_brief.json`
- `brief/site-package/agent_taskbook.json`
- `data/processed/agent_task_requirements.csv`
- `data/processed/project_scope_summary.csv`
- `data/processed/source_use_matrix.csv`
- `data/processed/missing_data_checklist.csv`
- 完整来源：`sources.json`
- 指标：`metrics.json`
- 逐项任务证据：`compliance_matrix.json`
- 专业标准与设计深度：`standard_matrix.json`、`design_depth_matrix.json`
