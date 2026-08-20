---
title: "京张共地 / THE SHARED FLOOR — 换模型，不换城市 / REPLACE THE MODEL, NOT THE CITY"
author_github: "PozdnyakovMaxim"
language: "zh"
proposal_format_version: "2"
bilingual_contract_version: "1"
translation_file: "proposal.en.md"
license: "COMMUNITY-DISPLAY-ONLY"
summary: "换模型，不换城市：以既有京张遗产公共空间为一层共地，用七条转换街缝合校园、社区、站点与产业，并以验证院、原点廊院、城市交汇厅三种长期框架承载可替换的服务、内装和 AI 设备；官方边界到位后整包重绑定、复算。"
tracks: ["ai-traffic-walkability", "youth-friendly-public-space", "robotics-autonomous-mobility"]
scenarios: ["ai-traffic-walkability", "robot-delivery-low-speed", "ai-cultural-guide", "public-safety-operations-review"]
iteration: "v1.6-candidate"
---

# 京张共地 / THE SHARED FLOOR

> **换模型，不换城市 / REPLACE THE MODEL, NOT THE CITY.** 京张共地把“模型换代”画成一座可进入的城市空间：A 是当前服务模型，B 是候选替换模型，H 是始终有权接管的人工路径。A 与 B 在同一任务、同一数据边界和同一人群负担下比较；只有服务责任人与权利/安全责任人同时签署，B 才能替换 A。公共地面、普通服务和 H 路径在整个换模窗口不断线。

![三种长期框架把同一层共地变成可观察的验证院、可照护的原点廊院和全天候城市交汇厅](assets/figures/key-areas.png)

## 一块地面为什么比一代模型活得久

AI 的换代以月计，城市的地面以百年计。京张铁路从 1909 年的干线到 2019 年开通的高铁经历了设备与运行系统的持续更新；高铁入地后，原有地表又被系统改造为遗址公园。[source:JINGZHANG-HERITAGE] [source:JINGZHANG-HSR-2019] [source:JINGZHANG-SURFACE-PARK]

历史事实说明变化本身，至于“城市不随模型停摆”则是本方案提出的设计判断。本方案把持续工作的公共地面当作正式设计对象：一层连续、可进入、有人工兜底的共地，其上设置两个可拆模型位 A/B、一条永不中断的 H 路径和一个人人看得见的物理回退控制；模型、供应商或工具接口变化时，普通通行与服务仍继续。[depth:overall_spatial_structure]

这就是标题的含义——换模型，不换城市。十二种城市服务都使用同一份 `City Task Contract`：锁定任务、允许的数据/工具、A/H 基线、B 身份与配置、同组测试夹具、回退触发、两钥匙决定和删除/退役证明。B 不能自我晋升，任何数据或权限扩张都自动 `HOLD`；严重回归触发物理回退，任务转向 A 或 H，普通公共路线不关闭。[metric:scenario_card_count] [assumption:A-OPERATIONS-001]

> **这份方案怎么读。** 正文各章对应公告 1.5 章节与六项智能体任务；所有依赖几何的空间结论和指标出自提交包内同一套几何并可整包复算，登记库/叙事计数则明确列出各自来源；「假设」徽标标记推演与实测的边界。本方案没有开展现场踏勘与居民访谈，临时边界与全部未知项显式登记为 unknown；官方边界、控规与权属资料到位后，整包重新绑定并复算。[assumption:A-BND-001] [assumption:A-CONTROLS-001]

## 设计依据与资料清单

本方案先做了一个反常识判断：京张铁路遗址公园的主轴不是等待设计的空白。北京市园林绿化局在 2026 年 7 月宣布二期配套完工，北段约 30.01 公顷，并明确其“鱼骨状”慢行网络；一期清华东路至知春路段早在 2023 年已开放，长 2.5 公里、16.8 公顷。因此竞赛最有价值的任务不是再画一条南北绿带，而是把既有公共空间接入东西两侧的校园、社区、地铁、产业与河流，补足门槛、入口、路口和日夜运营。[source:BEIJING-PARK-PHASE-II] [source:BEIJING-PARK-PHASE-I]

证据按可靠程度分为五类：官方资料（`official`）、背景资料（`background`）、待核实的临时资料（`provisional`）、本方案提出且可重新计算的设计建议（`design`），以及目前没有可靠资料、必须留空的未知项（`unknown`）。仓库中的总体设计范围和三处重点区只是临时粗略边界。背景核对发现，已命名的 OpenStreetMap（OSM）公园范围与临时总体范围重叠率为 0%，最近相距 412.5 米。现有资料不足以判断哪一方准确，因此本方案不自行移动边界，而要求正式边界公布后重新调整图纸并计算指标。[source:BOUNDARY-BASIS] [data:geometry/site_boundary.geojson#SITE-001] [depth:risk_missing_data]

本次提交使用公告给出的 43.6 平方公里统筹研究范围、11.4 平方公里总体设计范围和三处共 368.4 公顷重点区作为规模口径；任何地块、道路红线、容积率、高度、权属、拆改留和文保缓冲结论都保持 `unknown`，直到官方附件补齐。除四幅单独署名、固定哈希并保留来源权利状态的 1909 年京张工程档案缩略图外，外部研究只引用文字事实和开放数据，不复制政府网页图像、商业地图或其他参赛者图面。来源类型、URL 或本地路径、获取日、权利、用途与局限见 `sources.json`。[source:OFFICIAL-ANNOUNCEMENT] [source:SOURCE-REGISTRY] [source:LOC-JINGZHANG-ALBUM-1909]

本次智能体工作流程没有开展现场踏勘、获授权的居民访谈或问卷调查，也没有替任何本地机构作出承诺。因此十五种日常生活情景只用于规定“下一步要观察什么、由谁负责、什么情况必须停止”，不被当作已发生的需求或绩效。人流、夜间安全、价格承受力、开放时段、运营者与接受度必须在实施前通过现场观察、伴随路线和正式访谈建立基线。[assumption:A-SOCIAL-BASELINE-001] [depth:risk_missing_data]

![临时总图：同一模型贯穿总体空间、三处重点区、建筑与指标](assets/figures/masterplan-spatial-authority.png)
> **这张图怎么看。** 一套几何同时生成总图、三处重点区、18 个概念体量与全部依赖几何的指标；图上要素变动时这些指标随整包复算。边界为临时裁切，不是法定红线。

## 三层范围工作框架

在 43.6 平方公里统筹研究范围内，方案组织的是一条创新代谢链，而不是一条用地色带：高校与研究机构产生知识，众智园承担受控验证，AI 原点承担从 0 到 1 的转译和人才生活，大钟寺承担面向公众与市场的采用，真实运营结果再返回研究端。这个回路把公告要求的三大定位、五大功能和“三区两翼”转化为 `研究—转译—验证—采用—反馈` 五个可观察动作。[source:AGENT-TASKBOOK] [standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK]

在 11.4 平方公里总体设计范围内，方案只提出可重新绑定的空间语法：一条既有遗产公共底板、七类横向 `Switch` 接口、三座重点城市房间和一组全年气候庇护点。七类接口分别服务校园边界、社区入口、轨道换乘、河流绿网、夜间安静转换、后勤装卸和遗产解说；提交几何中的七条线是临时边界内的概念性测试位置，不是道路中心线或建设承诺。[data:geometry/roads.geojson#SWITCH-01] [depth:overall_spatial_structure] [assumption:A-BND-001]

在三处重点区域内，设计进一步落到 6 米结构网格、建筑进深、院落尺度、首层界面、遮荫构件、雨水花园、服务带和人工值守点。每个原型暂放在临时重点区中心附近，仅用于核对尺寸和空间关系，不代表真实地块已选定。正式边界图公布后，先核实入口和边界，再按新边界重新绘制建筑、道路、绿地、公共空间和分期，并重新计算全部指标；不能只把旧图缩放后继续使用。[data:geometry/key_areas.geojson#PROV-KEY-001] [metric:prototype_count] [depth:three_level_scope_framework]

![真实京张走廊背景上的一层共地、七座候选城市房间与三处重点区；仅作定位，不是法定地图](assets/figures/corridor-atlas.png)
> **这张图怎么看。** 底图只作定位。看三样东西：共地脊线怎样沿遗产线连续、七座城市房间落在哪些缝合点、三处重点区的相对距离。

走廊图以带 ODbL 署名的 OSM 轨道、水系、公园、站点和校园中心点构成总体定位，再以七个 300 米局部窗口重绘建筑并集、道路、轨道、水系、教育边界与已映射门点；数据空白保持空白，不被补画成城市，某要素未出现在 extract 中也不证明其现场不存在。三处重点区仅为文字标签锚点，七座城市房间是等待实测地址和运营协议的设计候选，不得用作红线、地块、建筑清单、测绘、门禁协议、导航、审批或建设依据。[source:OSM-CORRIDOR-CONTEXT-2026] [source:OSM-SEVEN-ROOM-FIGURE-GROUND-2026] [assumption:A-MOBILITY-001]

![从开放城市背景切换到可整体重绑定的参赛者空间模型：共地脊线、三座长期框架与七处横向接口](assets/figures/site-overview.png)

上图是参赛者的空间假设层，不是现状底图：它把同一套共地语法组织成可审计、可整体重绑定的研究模型；正式边界、权属、管线与审批资料到位后，所有位置和数量必须重新计算。[data:geometry/site_boundary.geojson#SITE-001] [metric:binding_offset_m]

![开放建筑的时间层：公共地面、长期支撑、服务底盘、可换填充与 AI 设备](assets/figures/land-use-structure.png)

## 统筹研究范围产业与未来城市研究

任务书要求形成总体概念与视觉识别方向。[source:AGENT-TASKBOOK] 本方案名称“京张共地”把品牌的重心放在公共地面而非科技装置。标志由一条未封闭的方形“城市房间”和一条穿过它的横线组成：方形代表可进入、可停留的共同空间，横线代表京张遗产和横向缝合，开口代表任何 AI 服务都必须保留人工入口与退出路径。主色为铁路氧化铁红、树荫绿、纸本米白和低饱和青色；不使用企业商标、人物肖像或仿制铁路徽记。[depth:height_massing_character]

任务书要求提供 5–8 个全球 AI 创新生态案例；本方案选择六个有公开来源的案例，并把它们作为本地约束的压力测试，而不是造型目录。[source:AGENT-TASKBOOK] [source:PRECEDENTS-OFFICIAL]

| 案例 | 公开证据中的城市机制 | 对京张的压力问题 | A/B/H 空间回应 | 仍待本地证据 |
|---|---|---|---|---|
| Singapore one-north | 工作—生活—学习混合与公共空间运营 | 同一服务入口能否在全天不同人群之间保持非排他 | 交汇厅共用入口、同一队列与可选 H | 住房负担、具名运营者与使用基线 |
| Punggol Digital District | 大学—产业协同与区域能源系统 | 候选 B 能否在不扩大基础设施或数据权限的前提下比较 | 验证院把能源、材料与机器人约束冻结为同任务夹具 | 对口机构、能源接口与授权数据 |
| Barcelona 22@ | 存量工业片区再利用 | 可换模型位能否不挤走既有日常服务 | 原点廊院保留公共 H 路并采用可逆插入 | 建筑、权属、租约与住房影响 |
| Paris-Saclay | 多机构网络与公共交通依赖 | 一个任务契约能否跨机构携带而不取消各自边界 | 七类横向接口与有运营者的分时校园通行 | 通行协议、运力与责任边界 |
| London Knowledge Quarter | 在既有城市中连接机构而非圈占园区 | 普通公共路线能否穿过机构边界持续工作 | H 公共底盘连接七类接口，模型位不控制通行 | 地役权、开放时段与运营主体 |
| Cambridge Kendall Square | 公共空间与创新就业共同进入规划讨论 | 模型更替能否成为公众可见、可申诉的城市事件 | 三处见证空间与删节差分票据墙 | 本地融资、公众接受度与长期维护 |

本方案只吸收上述来源支持的城市层经验，不复制任何案例的治理结构、开发节奏、视觉语言或技术工作流。A/B/H 换模面与三种空间拓扑来自“换模型，不换城市”的本项目命题；城市设计方法仍须服从公开性、可实施性和公共利益要求。[standard:MOHURD-URBAN-DESIGN-MEASURES]


本方案把产业空间分成四类，可按需要组合：试验制造（实验、样机和查找系统漏洞的安全测试）、成果转化（知识产权、融资、标准和孵化）、生活配套（住房、托育、运动、餐饮和夜间学习）、公共交流（展览、市场、论坛和人工服务）。这些只是建筑和首层的使用建议，不是新的法定用地分类；国土空间用地仍使用任务包允许的代码，并明确标为概念分区。[data:geometry/land_use.geojson#LU-RESEARCH] [standard:MNR-LAND-USE-CLASSIFICATION-GUIDE]

海淀官方材料区分三种口径：AI 原点社区约 3 平方公里；东升大厦周边 1 公里口径内有 30 多所高校和科研机构、1000 余名 AI 科学家、1.3 万名开发者和 10 万名相关专业学生；东升镇已建设 4000 多套人才公寓。数字不能被合并成同一边界内的人数，但共同说明校园外侧的实验、展示、餐饮、服务和晚间学习需要被当作公共界面研究。[source:AI-ORIGIN-2026] [depth:existing_conditions_diagnosis]

这里的中国特定性首先是制度与日常生活的叠合：校园/单位、封闭小区、车站、遗址公园和服务劳动共同塑造城市。北京大学机构研究新闻摘要转述的学院路六校研究显示，从完全封闭转向有限开放主要通道已经带来最大的空间整合增益，全面开放的追加效果小得多；因此方案采用有运营者、有时段、有紧急规则的“分时协同开放校门”，而不是拆掉所有围墙。清华东路南侧已获批的七节点公共空间项目则被视为必须衔接、不得冒领或重复建设的邻接工程。[source:PKU-XUEYUANLU-CAMPUS-2025] [source:QINGHUA-EAST-PUBLIC-SPACE-2026]


### 区域协同接口

走廊不是孤岛。按任务书区域协同要求，五个接口各自写明输出、回流与协商状态，全部为待协商的概念建议：[source:AGENT-TASKBOOK] [assumption:A-REGIONAL-001]

| 协同对象 | 走廊输出 | 回流承接 | 协商状态 |
|---|---|---|---|
| 北纬社区 | 共地 H 人工路径与无手机任务契约 | 照护者、老人和非智能终端使用者的失败夹具与人工完成负担 | 待协商 |
| 未来科学城 | 可复用的 A/B 双跨与 H 中带空间规范 | 能源、材料与机器人任务对候选 B 的约束，写入同任务差分票据 | 待协商 |
| 怀柔科学城 | 同任务夹具的校准、来源与哈希记录方法 | 大装置计量与标定能力，用来核验 A/B 输入是否真正相同 | 待协商 |
| 北京经济技术开发区 | 版本、工具权限与回退结果的删节票据格式 | 真实运行事件 schema 与供应商换代约束，不接收个人或商业敏感原始数据 | 待协商 |
| 京津冀走廊 | 可携带的城市任务契约、H 连续服务规则与三种空间拓扑 | 跨地点同任务差值、人工接管负担与恢复时间，用于判断机制能否迁移 | 待协商 |

每个接口的落地都需要对方主体确认；未确认前仅作为空间与运营预留，不构成任何已达成的协作安排。

## 总体设计范围城市更新与控规深度城市设计

总体结构概括为“一层共地、七类横向连接、三处重点空间”。“一层共地”指已建公园和与之相连的公共地面；“七类横向连接”针对校园、社区、车站、河流等不同条件；“三处重点空间”分别在众智园、AI 原点和大钟寺检验一种建筑与公共空间的关系。临时边界的矩形边不是街道，概念建筑也不是现状建筑，七个测试位置更不是最终工程点位。[data:geometry/site_boundary.geojson#SITE-001] [data:geometry/public_space.geojson#ROOM-PROOF] [depth:overall_spatial_structure]

用地层采用四个无缝概念分区，只表达总体功能重心：研究验证、教育转译、公共商业采用与社区生活；真实现状和法定用途待官方地籍与控规补齐。建筑层只有三组参考原型，均带 `reference_prototype=true`、概念层数与 `not_regulatory` 说明。道路层只画步行、骑行、站点接驳与横向公共接口，既有主干路和地铁结构没有数据就不伪造。绿地与公共空间层可独立复算，分期层则把调查、临时原型、网络连接和资本更新分开。[data:geometry/land_use.geojson#LU-RESEARCH] [data:geometry/buildings.geojson#ZY-NORTH] [metric:building_footprint_area_sqm]

开放建筑研究为长期支撑与可换填充分离提供方法依据。[source:OPEN-BUILDING-KENDALL-1999] 本方案只对外提交一个优选深化的城市世界：京张共地；生成阶段的两个其他空间根只作为已执行比较的紧凑过程证据公开，不是并列终稿。最终形态还必须同时满足：公共路线形成一张连通网络并到达每个公共空间；所有空间 ID 唯一；南侧保留冬日太阳；夏季阴影达到根级阈值；官方边界到位后可以整体重绑定。三座框架共享这些规则，却分别形成院、廊、厅三种空间秩序。[metric:prototype_count] [assumption:A-OPEN-BUILDING-001]

京张共地不继承传统建筑的轮廓，而继承一组可工作的营造规则：以“间”理解可维护的现代模数，以“院”承载共同生活，以“巷”保持横向渗透，以“廊/灰空间”调节四季，以“门—廊—院”的连续门槛表达公共、协商与受控权利。6 米和 8 米柱网只是当代结构选择，不声称源自《营造法式》；任何“借景”也必须等现场照片、坐标和视线验证后才能成立。[source:PALACE-MUSEUM-YINGZAO-MODULE] [source:VECTOR-COURTYARD-HYBRID]

上述营造语法是本方案对中国城市日常关系的当代转译，不是历史复原、样式挪用或未经现场验证的谱系事实。[assumption:A-CHINESE-LINEAGE-001] [depth:overall_spatial_structure]

控制性详细规划所需要的 FAR、建筑密度、法定高度、退线、道路红线、消防、市政容量和公共设施指标均未在公开包中给出。方案把这些项目完成为“待确认条件—触发资料—受影响成果”的清单，而不是用虚构数字填满表格。形式完整不等于法定有效；设计可以进入内容评审，实施仍需本地规划、建筑、交通、消防、结构、机电、文保和无障碍专业复核。[standard:MOHURD-CONTROL-DETAILED-PLANNING] [metric:floor_area_ratio] [assumption:A-CONTROLS-001]

## 重点区域详细设计

**众智园：验证院 / Proof Yard（COURT）。** 156×156 米参考框以 6 米网格组织长期支撑：北侧高跨验证楼、两条实验/服务翼、分开的低矮公众观察廊，以及院心一座可替换具身 AI 测试单元。进入序列是“前院 → 观察廊 → 透明门槛 → 受控试验院”，南缘同时提供冬日太阳口袋与夏季阴影等待区；公共、机器人与后勤路线不交叉。失联即停、人工接管。它是一台公众可以观察、但不会误入的城市仪器。[data:geometry/buildings.geojson#ZY-NORTH] [data:geometry/buildings.geojson#ZY-TEST-CELL] [data:geometry/public_space.geojson#ROOM-PROOF]

**北京 AI 原点：原点廊院 / Origin Cloister（CLOISTER）。** 海淀官方材料把 AI 原点描述为社区型创新语境。[source:AI-ORIGIN-2026] 本方案在该语境中提出一座 172×140 米、6 米参考网格的开放廊院：一条只在协商公共开放时段连续可达的公共巷依次经过照护院、讲学庭、试作院和安静环，把校园侧的共享实验连接到社区侧的托育、餐饮、运动、夜间学习与人工服务。早晨服务老人慢行与晨练，下午支持祖辈—儿童照护，晚上转为邻里长桌和学习；连续廊檐同时处理雨、夏季辐射与冬季避风。[data:geometry/buildings.geojson#AO-NW] [data:geometry/buildings.geojson#AO-COMMONS]

它遵循“先调查、优先再利用、再可逆插入”，不把任何现状建筑预先写成可拆对象。[assumption:A-PROTOTYPE-001]

**大钟寺：城市交汇厅 / Exchange Hall（HALL）。** 148×148 米参考框由四个 38×38 米角部支撑体、四向公共十字和一座 46×46 米可替换全天候大厅组成；较大跨度部分采用 8 米参考网格。四座城市门先进入 4–6 米深的共享檐，再汇入即使侧翼关闭仍可穿越的市厅；南侧两条装卸支线止于角部服务体，不穿越公共十字。便宜日常餐食、修理、骑手驿站、企业服务、论坛、夜间等候和人工接管共享首层，部分座位无需消费。数字系统停机时，市厅仍依靠固定标识、纸本信息、照明和现场人员工作。[data:geometry/buildings.geojson#DZ-NE] [data:geometry/buildings.geojson#DZ-CANOPY] [data:geometry/public_space.geojson#ROOM-EXCHANGE]

三处不是一条先后放行的流水线，而是同时展示三种换模拓扑。**验证院是“双跨同测”**：A/B 两跨接受相同的已清理或合成夹具，中间 H 观察/紧急带始终开放，比较的是同任务差值而非各自最漂亮的得分。**原点廊院是“差分回廊”**：同一任务的 A/B 回答、来源/权限变化与未解决分歧并排可读，任何人可以直接沿 H 桌完成任务而不参加比较。**城市交汇厅是“单队列三出口”**：同一入口和排队规则后才分向 A、B 或 H，禁止 B 只挑容易用户；H 出口与申诉始终可达。三处都保留稳定服务台/任务 schema、两个可拆模型位、固定版本标识、可见的 H 席位和物理回退控制。[assumption:A-OPERATIONS-001] [depth:three_key_area_detailed_design]

官方材料要求先分清四个不能互换的范围：72.0 公顷竞赛重点区、约 5.03 公顷蓝景丽家规划研究、39,522.11 平方米供地包，以及车站周边 300 米站城协同范围。300 米是协调范围，不是地块、红线、通行权或普遍建设许可；供地包也不授权本方案的 P0 落位。[source:BEIJING-STATION-CITY-INTEGRATION-2024] [source:DAZHONGSI-LANJINGLIJIA-INTEGRATION-2026] [source:DAZHONGSI-LANJINGLIJIA-LAND-SALE-2025]

蓝景丽家方案把 B2、B1、地面和 2F 列为“鼓励共享层”，不等于这些楼层已经开放、形成公共地役权或可以 24 小时通行；M12 大钟寺站 E 出入口东西两侧的两处公共非机动车停车场合计约 0.14 公顷，属于规划要求，未核实建成。[source:DAZHONGSI-LANJINGLIJIA-INTEGRATION-2026] [source:DAZHONGSI-LANJINGLIJIA-BIKE-2025]

最终供地审查还要求绿地与京张铁路遗址公园互渗，并研究以高架连廊或地下通道连接车站；文件同时记录项目邻近全国重点文物保护单位觉生寺。因此本方案只画关系，不猜具体线路或文保缓冲线，正式保护范围、建控地带和主管部门意见到位后再套核。[source:DAZHONGSI-LANJINGLIJIA-LAND-REVIEW-2025] [source:JUESHENG-TEMPLE-NATIONAL-HERITAGE]

其“便宜餐食—小修小补—多年龄舒适—运营者负责”的基线来自北京兆君盛菜市场更新；骑手饮水、休息、充电和交接则有北大南门驿站的海淀现实依据。两者只定义必须落实的服务与运营问题，不授权复制现有建筑。[source:BEIJING-ZHAOJUNSHENG-MARKET] [source:BEIJING-PKU-RIDER-STATION-2024]

城市交汇厅在大钟寺的第一条结论不是“落地”，而是“原样落地失败”。以两条 OSM 站点记录的工作中点为锚，将 148×148 米参考框直接居中，会与 34 条映射记录相交；这些记录包括建筑轮廓、轨道/站台、站点和道路，但不是 34 个经核验的独立实体。这个失败否决把通用原型压在站上的做法，也证明当前提交中的临时 `ROOM-EXCHANGE` 不能被悄悄搬到真实站点。[source:OSM-DAZHONGSI-CONTEXT-2026] [metric:dazhongsi_literal_frame_mapped_intersection_record_count] [metric:dazhongsi_overlay_to_submitted_room_centroid_m]

这只是设计时方向筛查，不是测绘、权属、地铁保护或可建性结论。[assumption:A-DAZHONGSI-FIRST-BAY-001]

因此第一项可逆设计工作缩小为 **P0 站前共享檐**：36×36 米只是定位筛查包络，设计对象只有一跨 8×8 米可拆支撑和 16×16 米可逆地面。平面预留 3.0 米无台阶公共带、Ø1.50 米回转、1.5 米后勤带和两向 1.8 米开敞疏散目标；这些是本方案的设计储备，不是合规结论。[source:GB55019-2021] P0 是开敞雨棚，不设烹饪、电动自行车动力电池充电、燃料储存或封闭活动；消防车接口、出口数量/宽度/距离、人数、结构、基础和市政均保持未知。[source:GB55037-2022] A0 原尺寸的 1:20 净几何接口把 4.2 米檐下净高目标、屋面内 3.6 米公共庇护区、可检查服务轨、2% 排水假设、独立溢流和 1.5 米湿边画清楚；构件和产品厚度仍待结构、消防和机电确定。64 平方米屋面每 10 毫米降雨对应 0.64 立方米水量，但出口、蓄水与渗透仍由地形、土壤和市政排水决定。[metric:dazhongsi_p0_test_envelope_sqm] [metric:dazhongsi_p0_covered_bay_sqm] [metric:dazhongsi_p0_treated_ground_sqm] 映射冲突筛查单独记录为 [metric:dazhongsi_first_bay_mapped_collision_area_sqm]。[assumption:A-DAZHONGSI-FIRST-BAY-001] [assumption:A-LIFE-SAFETY-001]

参赛者概算为 ¥1.9–3.8M，按 64 平方米结构/屋面、256 平方米可逆地面、水电照明数据/消防接口、家具帮助点、调查设计和 35% 不可预见费构成；它不是北京投标价，且不含土地、税、涨价、重大地铁/道路/市政迁改、土壤和融资。[metric:dazhongsi_p0_rom_cost_low_million_cny] [metric:dazhongsi_p0_rom_cost_high_million_cny]

06:00–24:00 单柜台覆盖按 6,570 小时/年、每 FTE 1,680 个生产小时和 1.20 假期培训系数得到 4.69，向上取 5 FTE 轮班；工作运维区间 ¥1.2–2.2M/年仍不是报价。没有具名运营者、12 个月运维储备、通行协议、地铁保护、消防/结构/机电审查和许可，就不建设或开放；01:00 夜间城市房在额外人员与安全合同到位前不成立。[metric:dazhongsi_p0_opex_working_low_million_cny_per_year] [metric:dazhongsi_p0_opex_working_high_million_cny_per_year] [assumption:A-OPERATIONS-001]

![大钟寺：真实四象限图底否决错误落位，并以同一几何给出 1:500 落位、1:100 平面、1:200 剖面、1:20 接口、轴测、造价与运营停止门](assets/figures/dazhongsi-demonstrator.png)
> **这张图怎么看。** 先看左上四象限图底——它否决了两个候选落位；再顺同一几何走 1:500 → 1:100 → 1:200 → 1:20，最后停在右下的运营停止门：这一跨随时可以拆回去。

开放建筑先例只为长期支撑与可换填充分离提供概念依据。[source:OPEN-BUILDING-KENDALL-1999] 本方案为三种类型提出同一时间契约而非同一造型：公共地面保留 100+ 年公共价值；长期支撑采用 100 年设计目标；服务底盘按 25–40 年更新；填充按 5–20 年替换；AI 场景设备从数天到不超过 5 年。以上均为参赛者提出的设计目标和更换周期，不是先例结论、经认证的结构寿命或质保承诺。[assumption:A-OPEN-BUILDING-001] [assumption:A-LIFE-SAFETY-001]

共同构造语言不是仿古屋顶，而是一跨可重复的当代共享檐：长期支撑优先保留并检测现状框架，否则采用可检查的 6 米或 8 米规则网格；次结构用螺栓连接，1.2 米协调的干式填充可独立拆换，机电走在外露可维护服务带。檐下深度 3.6–6 米，南/东侧开放，西北侧形成挡风与服务背板；屋面水经过外露落水、沉砂前池、雨水花园和待校核安全溢流。铺地须防滑、耐冻融并可拆修；旧砖、石材、道砟或钢轨只有在现场盘点、检测和权属确认后，才能作为非结构性候选材料进入材料护照。[depth:three_key_area_detailed_design] [assumption:A-DRAINAGE-001] [assumption:A-LIFE-SAFETY-001]

这种“保留城市谱系—独立插入—让日常公共路线继续工作”的机制来自对金威啤酒厂与南头混合大楼的比较学习；本方案只转译机制，不复制其深圳气候、形式、图纸或材料细节。[source:URBANUS-KINGWAY-REUSE] [source:URBANUS-NANTOU-HYBRID]

三种类型仍共享几条不可协商的空间规则：至少一条不依赖智能终端的无障碍通行与服务链连续；后勤有独立路线或时间窗；具身 AI 测试有物理边界、人工值守和安全停车；结构、消防、防水、声学、机电与地基必须在下一阶段经本地专业复核。[depth:three_key_area_detailed_design] [assumption:A-LIFE-SAFETY-001]

![三处重点区域：验证院、原点廊院与城市交汇厅](assets/figures/key-areas.png)

![验证院：平面、轴测、剖面与类型护照](assets/figures/proof-yard.png)

![验证院冬至正午：概念体验图；空间权威仍为平面、剖面和 GeoJSON](assets/media/proof-yard-winter.jpg)

![原点廊院：平面、轴测、剖面与类型护照](assets/figures/origin-cloister.png)

![原点廊院夏日雨后：概念体验图；不代表现状场地](assets/media/origin-cloister-summer.jpg)

![城市交汇厅：平面、轴测、剖面与类型护照](assets/figures/exchange-hall.png)

![城市交汇厅 19:00：概念体验图；数字停机时由固定标识和现场人员接管](assets/media/exchange-hall-evening.jpg)

## AI 创新生态、人才画像与 AI+ 场景

设计面向七类登记人物（P01–P07），而不是抽象“人才”。海淀 2020 年人口普查显示 60 岁及以上人口占 18.5%、65 岁及以上占 13.1%；因此触觉导向、座椅、厕所、人工问询和无手机路径不是附加福利，而是 AI 城区的基本性能。每类人物写明首要需求、排斥风险与挂钩场景卡：[source:HAIDIAN-CENSUS-2020] [standard:BARRIER-FREE-ENVIRONMENT-LAW] [metric:scenario_card_count]

| 编号 | 人物 | 首要需求 | 排斥风险 | 挂钩场景卡 |
|---|---|---|---|---|
| P01 | 老年居民 | 休息、冬日向阳、厕所与可读的人工帮助 | 长路线、仅限 App 的服务、无靠背座椅 | ③⑤⑫ |
| P02 | 轮椅使用者与同行者 | 连续无高差干燥路线与例外服务台 | 断点、临时占道与不可预告的关闭 | ①⑩ |
| P03 | 骑手与配送员 | 清晰的停靠、交接与安全停止口袋 | 被驱离、无交接位、与行人混流 | ②⑫ |
| P04 | 学生与研究人员 | 可预约的设备、实验与政策入口 | 门槛不透明、设备被少数人锁定 | ④⑥⑦⑪ |
| P05 | 现场服务与维护人员 | 纸本巡检路线与直接安全上报 | 工单黑箱、责任下移、无停机权 | ⑥⑨⑪ |
| P06 | 照护者、祖辈与儿童 | 慢速通行、看护视线与气候庇护 | 机器人混行、夜间盲区、无处等候 | ②⑤⑩ |
| P07 | 夜间使用者与非智能终端访客 | 无手机路径、人工窗口与多语种帮助 | 仅二维码服务、夜间无人受理 | ③④⑦⑧⑩⑫ |

十二份换模契约把原有场景卡绑定到三个空间拓扑。每份契约都用 normal / ambiguous / hard-stop 三类同任务夹具检查 A/B/H 路由；表中 H 不是失败后的补丁，而是从入口就可选择、并有最终决定权的普通服务路径：[data:geometry/public_space.geojson#ROOM-PROOF] [metric:scenario_card_count] [metric:test_scenario_count]

| 契约 | 同一城市任务 | 换模拓扑 | 必须比较的 A/B 差值 | H 的不可撤销权力 |
|---|---|---|---|---|
| AI01 | 无障碍换乘校核 | 原点差分回廊 | 断点、绕行与求助负担 | 陪同完成并关闭危险路线 |
| AI02 | 受控低速配送 | 验证院双跨同测 | 冲突、让行、停机与数据范围 | 接管手推车并物理停机 |
| AI03 | 公共服务导航 | 交汇厅单队列三出口 | 完成率、等待与信息最小化 | 柜台完成同一任务并受理申诉 |
| AI04 | 可溯源京张导览 | 原点差分回廊 | 来源缺失、虚构与发布权限 | 采用固定铭牌/人工讲解并否决发布 |
| AI05 | 气候庇护提示 | 验证院双跨同测 | 误报、漏报与设施动作差异 | 人工开闭并发布现场状态 |
| AI06 | 共享设备匹配 | 原点差分回廊 | 匹配失败、排斥与预约负担 | 人工分配并保留锁定权 |
| AI07 | 企业合规入口 | 交汇厅单队列三出口 | 错误引用与越权决定 | 合格人员作最终判断 |
| AI08 | 安静夜间协调 | 原点差分回廊 | 噪声误判与隐私范围 | 人工巡查、处置并停止感知 |
| AI09 | 公共空间维护分级 | 验证院双跨同测 | 漏报、积压与责任转移 | 直接安全上报并封闭危险设施 |
| AI10 | 非人脸活动安全复核 | 交汇厅单队列三出口 | 人数误差、身份保留与限流负担 | 人工计数并掌握物理限流 |
| AI11 | 开放模型基准实验室 | 验证院双跨同测 | 同夹具回归、schema 与工具差异 | 签署结果并断电断网 |
| AI12 | 多语种帮助台 | 交汇厅单队列三出口 | 翻译分歧、等待与数据留存 | 人工译员完成任务并立即删除请求 |

这些都是设计时契约，不是已运行服务。只有获批的真实试点才能产生现场完成率、用户负担或安全绩效；当前运行只证明三类夹具、两钥匙权限、H 路径和回退逻辑是否被完整接线。

为避免只凭一个构想作答，方案生成阶段在同一标准化比较范围内运行三条相互独立的因果根：`R1 路径序列对照` 隔离“分阶段空间路径”这一变量；`R2 气候照护对照` 隔离“气候与照护节点”这一变量；`R3 A/B/H 交接共地` 才把同任务换模、持续 H 路径和不同构件寿命合成优选方案。惰性回执中的内部 ID 明确对应为 `R1=C01 / R2=C02 / R3=C03`；R1 与 R2 是生成对照，不是另外两套品牌化公共系统，也不是终稿。每条根先通过几何有效、唯一 ID、零非预期重叠、公共网络连通、每个公共空间可达、参考功能量和根特定硬性排除条件，再进入 Pareto 比较。不可变运行回执阻止无效状态并记录 Pareto 资格；最终选择仍由空间论证和设计评议决定，不能由标准化代理分数冒充专家判断。最新不可变运行中，3/3 条根通过自身硬性排除条件。提交包附有完整惰性源代码快照、依赖说明和结构化运行回执供公开核查；离线展示不执行参赛者代码，如需重跑，评审者须在可信环境中提取源文件并安装依赖，本方案不声称一键复现。[metric:design_root_count] [metric:hard_gate_pass_rate] [data:visual/assets/reproducibility.json]

![三个独立设计根的同基准硬性条件比较](assets/figures/design-roots.png)

校核流程还执行 6 个一跨重绑定探针、18 个带预期失败门槛的定向故障注入，以及 12 条“发现故障—停止不安全自动化—保留公共服务—具名人员接管—到达安全终态”的编码恢复路径；结果为 6/6、18/18、12/12。[metric:valid_rebind_pass_count] [metric:targeted_fault_detection_count] [metric:handoff_recovery_pass_count]

对应安全计数为零错误放行、零禁区事件和零不安全继续动作。这证明的是验证器和编码交接契约，不是正式边界适配、现场运营性能或专业认证。[metric:gate_challenge_false_accept_count] [metric:handoff_minefield_hit_count] [metric:handoff_unsafe_action_count]

在简化正午代理中，R3（即选中的京张共地）室外公共空间的冬至正午日照面积占比为 68.0%，夏至正午遮阴面积占比为 36.6%；全年热舒适、风环境与法定日照仍待专业模拟。[metric:shared_floor_winter_public_sun_proxy] [metric:shared_floor_summer_public_shade_proxy]

选中根的公共路线是一张连通网络，触达全部五个公共空间，且建筑、路线、公共空间之间没有重复 ID。[metric:shared_floor_public_route_component_count] [metric:shared_floor_public_room_route_gap_count] [metric:shared_floor_duplicate_feature_id_count]

两套互补的设计时校核被明确分开。原有空间状态机执行 12 个可复算任务，检查普通公共路线、可换填充和数字停机后的人工接管，12/12 通过。[metric:simulation_task_count] [metric:simulation_success_rate] [metric:tool_schema_pass_rate]

新增换模验证器则对 AI01–AI12 各运行 normal、ambiguous、hard-stop 三类契约夹具，共生成 36 份哈希寻址的差分票据。它故意向 AI02、AI04、AI07、AI10 注入数据、工具、权限或留存范围回归，四项全部被 HOLD；其余八项仅得到“可进入未来获批 shadow 试验”的设计时资格。[metric:changeover_contract_count] [metric:changeover_fixture_count] [metric:changeover_held_regression_count]

错误晋升为 0，实际晋升为 0；两者都不是现场成功率。[metric:changeover_unsafe_promotion_count] [metric:changeover_promotion_executed_count]

这些结果只证明契约、H 路径、两钥匙授权和默认回退已经接线，并未调用任何在线模型、招募用户、运行现场或证明服务绩效。模型输出质量、真实用户负担、现场回退时间与非劣效性仍为 unknown。[metric:changeover_live_model_run_count] [metric:changeover_field_trial_count] [assumption:A-OPERATIONS-001]

另有十五张“北京日常”日常生活情景推演卡，不把用户缩成一张人物拼贴：老人晨练、站点骑行、跨校研究、骑手交接、可负担午餐、祖辈与儿童、缺少本地社会网络者的重复共同活动、服务班次、女性夜行、青年活动、不依赖智能终端的服务、完整无障碍链、有运营者的分时校园通行、公众 AI 试验和夜间城市房。每张卡在 `simulation.json` 中记录人物、时间/季节、地点、冲突、空间响应、运营者、数据边界、人工兜底、失败指标和状态。[metric:social_rehearsal_count]

这些卡只定义必须观察的冲突与测量方法，不把区级人口比例外推成项目边界内人数；所有流量、价格、开放时段与安全感都标记为需要现场基线。[source:HAIDIAN-CENSUS-2020] [assumption:A-SOCIAL-BASELINE-001]

低速机器人只使用 1.5 米概念服务带和指定交叉点，6 km/h 是本方案的临时设计上限而不是法规速度；官方无人配送测试规则只提供测试制度背景。机器人永远向行人、轮椅和婴儿车让行，定位或通信失败时安全停车并由人接管。[source:ROBOT-SCENARIO-CARD] [source:BEIJING-ROBOT-DELIVERY-RULES-2024]

无障碍导航不得要求安装 App；公共服务 AI 只导航到权威入口，不提供医疗诊断或替代法律意见；文化导览把“史实”“策展解释”“AI 生成”明显分开。[source:AI-CULTURAL-GUIDE-CARD] [assumption:A-OPERATIONS-001]

每次换模只打开一个可撤回窗口：冻结任务契约与 A/H 基线 → A/B 同夹具重放 → 检查数据、工具、权限和人群负担差值 → 在 A 与 H 保持热备时做获批 shadow/opt-in → 两名独立责任人决定保留 A、继续限制 B、替换为 B 或交给 H → 发布删节后的差分票据并确认删除/退役。屏幕、传感器和机器人可以撤走，厕所、坡道、树荫、座椅、排水和人工服务仍然有用。[standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK] [depth:municipal_new_infrastructure]


### 算力、资金与数据的进入和退出

三类资源都服从同一换模边界：[assumption:A-OPERATIONS-001]

- **算力**：A/B 使用可替换的供应商中立模型位，票据固定模型、配置、prompt 与 tool-schema 哈希；配额按换模窗口计费，窗口关闭即释放，不把城市接口锁给单一供应商。
- **资金**：公共地面、H 柜台和物理回退由公共更新包保障；A/B 运行成本由候选运营者承担。出资不能购买个人数据、排他入口或晋升决定。
- **数据**：每份契约固定允许字段、工具、保存期和删除方式；B 只要扩大数据、工具或权限范围就保持 HOLD。公共票据只发聚合值、哈希和决定，敏感原始记录留在受控审计区，不保存 CoT。

### 城市任务契约与差分票据

每份 City Task Contract 由九类字段组成：城市任务和受影响人物；H 与当前 A 基线；允许的输入/输出/schema/工具/保存期；B 身份与固定配置；三类同任务夹具；A/B 差值；硬回退触发；服务责任人 + 权利/安全责任人的两钥匙决定；数据删除与旧模型退役确认。[assumption:A-BASELINE-001]

每次验证留下可公开核查的 Delta Receipt：contract_id、site_id、topology_id、contract_hash、fixture_hash、A/B/H version、data/tool/authority delta、disagreement、new regression、H override、selected route、rollback state、decision keys、deletion/retirement state、receipt_hash。公开票据不是“成功分数”，而是可验证的改变记录；任何字段缺失、严重回归或单钥匙决定都保持 A/H，不允许 B 晋升。

现场效果阈值必须在获批试点前由具名运营者与使用者代表共同确定。当前 field completion、真实用户负担、投诉、服务非劣效性和恢复秒数全部为空值；不得用 36 份设计时票据冒充 36 次现场服务。

## 用地、建筑规模与拆改留方案

`land_use.geojson` 是一个完整无缝的概念分区，用来通过空间校验，不是法定用途调整：北段以科研 `0802` 为主，中段以教育 `0804` 和公共服务为主，南段以商业服务 `05` 与社区生活 `07` 为主。分区边界由临时总体范围按投影坐标切分，官方 polygon 或控规一到即全部重算；不能从这些色块推导征地、开发权或地价。[data:geometry/land_use.geojson#LU-RESEARCH] [metric:site_area_sqm] [standard:MNR-LAND-USE-CLASSIFICATION-GUIDE]

建筑图层由十八个可复算构件组成：验证院 6 个、原点廊院 7 个、城市交汇厅 5 个；其中 13 个标记为长期 `support`，5 个标记为可替换 `infill`。每个构件记录 `open_building_layer`、参考网格、概念层数、高度、用途、设计寿命目标和 `not_regulatory=true`。建筑基底可以精确复算，因为它是本方案自己生成的几何；以临时总体范围为分母的比例仍只有低置信度，不能转译成官方建筑密度。[data:geometry/buildings.geojson#ZY-NORTH] [metric:building_mass_count] [assumption:A-OPEN-BUILDING-001]

由于没有现状建筑、年代、结构、价值、权属和租约数据库，本方案拒绝给具体建筑贴“拆除”标签。拆改留采用五步调查决策序列：`证据保护`（文物及档案先行）→ `现场调查` → `可逆再利用` → `选择性插入` → `经审批新建`。官方公告要求三处重点区形成拆改留分类，并要求大钟寺研判潜力地块与高校更新、改善公共环境和站点四象限步行连通；它授权调查和分类方法，不授权拆除任何具体建筑。[source:DAZHONGSI-RENEWAL-2026] [depth:retain_renovate_demolish]

原型优先采用规则柱网、干式可替换内装、外露可检查服务带和可拆雨棚，目的是让空间能从实验室变为教学、展市或社区服务，而不是预设一种材料体系。结构、防火、防水、声学、幕墙、机电、地基和碳排必须在下一阶段由本地专业团队基于调查和法规计算。[depth:development_intensity_controls] [assumption:A-LIFE-SAFETY-001]

## 交通、轨道、市政与公共服务设施

共同地面采用一条可按现场压缩或展开的参考剖面：3.0 米连续无障碍步行净带、2.5 米自行车带、1.5 米受控低速服务带、2.0 米雨水/树池带和约 3.0 米廊檐或可变遮荫带。它们是设计目标而非现行道路标准；在窄处，优先顺序是无障碍步行、应急、排水、骑行，机器人服务首先退出。所有路口保持平坡或最小高差，触觉路径不被补能柜、共享单车或户外餐座占用。[data:geometry/roads.geojson#SHARED-FLOOR-SPINE] [standard:BARRIER-FREE-ENVIRONMENT-LAW] [assumption:A-SECTION-001]

七类 `Switch` 不是七座相同天桥。校园接口通过外侧共享首层开放受控资源；社区接口增加厕所、座椅和人工服务；站点接口组织无台阶换乘和自行车停放；河流接口把雨水花园接入蓝绿网络；夜间接口用照度、声环境和营业时间分区；后勤接口把装卸与机器人补能放进时间窗；遗产接口只使用可逆标识和真实档案。每一处的桥、隧道、路口改造或轨道结构均需交通、市政、消防与产权单位确认。[data:geometry/roads.geojson#SWITCH-01] [depth:traffic_rail_slow_parking]

因此七条 `Switch` 在建筑层被深化为七座可识别但不相同的“轨道城市房间”：遗产门槛、骑手驿站、站前廊、海绵穿越、分时协同开放校门、社区照护廊和夜间城市房。统一的不是造型，而是一座可拆的北方“共享檐”：冬日朝阳座位、夏雨遮蔽、厕所/饮水/人工帮助、不依赖智能终端的服务链、服务时间窗和机器人撤离点。2024 年官方计划识别了 9 条城市支路和 8 处社区功能活动场地，邻近另有获批七节点项目；本包尚未逐项核实其交付状态，因此都作为待核对的规划/邻接基线，不得重复计功。[source:BEIJING-PARK-INTERFACES-2024] [source:QINGHUA-EAST-PUBLIC-SPACE-2026] [assumption:A-CAMPUS-GATES-001]

图面的站点链以北京北/西直门、大钟寺、知春路、五道口、清华东路西口等公开站名作参赛者定位标签，不构成地铁设施证据。当前包没有站体、出入口、客流和无障碍设施的权威 GIS，因此只把 `Transit Threshold` 作为类型，不声称具体出口位置。下一步必须取得官方站点索引/图纸并做七天分时人流、轮椅全程、夜间照明、噪声、路口等待、骑行停车、装卸和应急通道调查。[assumption:A-MOBILITY-001]

任务书要求回应市政与新型基础设施。[source:AGENT-TASKBOOK] 本方案把新型基础设施藏进可维护的边缘：低压电与数据接口、端侧算力柜、传感器、机器人补能和雨水监测均可独立关闭与更换；不得阻塞公共路线，也不得把个人身份识别作为空间使用条件。公共服务节点至少保留电力/网络中断时的纸本信息、固定标识和人工联系人。[depth:municipal_new_infrastructure]

![共同地面：横向接口、蓝绿网络与全年气候剖面](assets/figures/mobility-bluegreen.png)

## 蓝绿空间、公共空间与城市风貌

NASA POWER 对 116.347E、39.982N 的 1991–2020 月度点位序列经 30 年聚合后给出年均 11.52°C、一月 −5.34°C、七月 26.49°C；冬春 10 米风以西北向为主，夏季转为南—东南向，七八月相对湿度约 65–68%。该数据来自粗再分析网格，返回高程也不代表现场，所以只用于概念朝向和敏感性，不用于暖通、风环境或海绵工程验收。[source:NASA-POWER-1991-2020] [assumption:A-CLIMATE-001]

在纬度 39.982° 的简化太阳几何中，冬至正午太阳高度约 26.6°；18 米高体量在无地形条件下投下约 36.0 米长的正午影子。[metric:winter_noon_sun_altitude_deg] [metric:winter_shadow_length_18m] 夏至正午太阳高度约 73.5°，同一体量的正午影子约 5.3 米。[metric:summer_noon_sun_altitude_deg] [metric:summer_shadow_length_18m]

这个季节差异驱动三条形态规则：南边翼降低或断开，主要冬季口袋至少大于参考冬影，夏季遮荫用廊檐、落叶树和可拆构件而不是继续加高建筑。[depth:height_massing_character]

全年气候剖面把季节动作直接放进共同地面：夏季接受南—东南风，并以分布式树冠、共享檐和饮水点形成一串阴影停留处；冬季用西北侧建筑/常绿防风和朝南坐凳形成太阳口袋；暴雨时由树池、下凹绿地和临时滞蓄空间减缓径流；春秋则保持可开可关的廊檐。任何下凹深度、蓄水量、溢流口和管径都等待地形、土壤、地下水和市政排水模型。[data:geometry/green_space.geojson#GREEN-SPINE] [depth:blue_green_public_space] [assumption:A-DRAINAGE-001]

“全年气候—雨水链”是本方案提出、等待水力与无障碍专业校核的设计要求，不以绿色面积代替水力逻辑：屋面汇水 → 轨床式生态沟 → 沉砂前池 → 树池/雨水花园 → 密闭回用池 → 灌溉与清洁 → 安全溢流。下一阶段为每个重点区建立 catchment、临时调蓄、溢流与维护记录，并校核冬季排空、积雪不得压住触觉路径、冻融、春季扬尘与西北风。当前没有地形、渗透率和排水资料，因此图上只保留空间与维护通道，不给虚假的容量。[metric:green_space_area_sqm] [assumption:A-DRAINAGE-001]

城市风貌不采用赛博霓虹。遗产层使用氧化铁红、再生砖/石的触感和真实里程信息；气候层使用树、土、水和浅色遮荫；AI 层只以细薄、可拆、低亮度的青色构件出现。三处公共见证空间直接表达换模差异：众智园的 A/B 双跨与 H 中带、AI 原点的差分回廊与 H 桌、大钟寺的单队列 A/B/H 三出口。它们是普通人可读、可绕行、可申诉的工作空间，不是未经批准的巨型雕塑。[data:geometry/public_space.geojson#ROOM-ORIGIN]

1905–1909 的自主铁路工程史以公开遗产材料和同期工程影集为依据。[source:JINGZHANG-HERITAGE] [source:LOC-JINGZHANG-ALBUM-1909] 本方案把它与改革开放以来的中关村创新文化、当代开放模型与公共 AI 文化并列为三条策展时间线。

文化传承的不是铁路造型，而是本方案提出的“记录—实测—试用—评估—维护”工程方法：C1–C7 每一处候选城市房间都先建立现场基线，再做可逆 P0 试用，并由专业人员与居民针对同一组指标并行评估；差异触发修改或退出，而不是被平均成漂亮分数。该方法借鉴北京市公开报道的一个责任规划师案例。[source:BEIJING-RESPONSIBILITY-PLANNER-DUAL-ASSESSMENT-2025] 它属于本方案自愿采用的协议，不是全市强制标准；目前尚未开展任何评分，也没有责任规划师被任命。史实来源、策展解释和生成内容使用不同底色与编号；AR 只是可选层，实体文字、触觉模型和人工讲解始终存在。


### 换模面的空间不变量

A/B/H 首先是每处平面和剖面都必须保持的关系：同一入口与任务定义；两个可拆、同尺度的 A/B 模型位；一条无手机也能完成任务的连续 H 路径；同一排队与申诉规则；人人看得到的版本牌、停止控制和差分票据；B 永远不能关闭 A/H 或扩大自己的数据、工具与决定权。[assumption:A-OPERATIONS-001]

任务书要求 `landmark_catalog / honor_display_system / component_library` 三类输出。[source:AGENT-TASKBOOK] 本方案把 A/B/H 关系登记为公共空间接口套件而不是商品目录：`CH-01` 同任务门槛与版本标识、`CH-02` 两个可拆 A/B 模型位、`CH-03` 连续 H 路与人工柜台、`CH-04` 物理停止/回退控制、`CH-05` 同队列与申诉界面、`CH-06` 删节差分票据墙。[metric:changeover_interface_component_count]

三处 AI 朝圣地标不是娱乐雕塑，而是可核查的见证空间：`LM-ABH-01` 验证院双跨、`LM-ABH-02` 原点差分回廊、`LM-ABH-03` 交汇厅单队列三出口。每处各设一面删节差分票据墙作为荣誉展示，共三面；它们只展示可复演的公共贡献、暴露的新失败、H 决定与回退结果，不做个人或模型排行榜。[metric:changeover_witness_landmark_count] [metric:changeover_honor_display_count]

尺寸只使用已经有空间依据的口径：验证院在众智园的 6 米参考网格内布置双跨，不借用大钟寺尺寸；8×8 米可拆支撑与 16×16 米可逆地面只属于大钟寺 P0 站前共享檐。蓝绿图层登记的是 1 条廊道脊线、3 个气候庇护环、25 个树冠代理面和 8 个湿链空间预留，共 37 个设计 polygon；它们不是 37 个已建气候节点。[data:geometry/green_space.geojson#GREEN-SPINE] [assumption:A-DAZHONGSI-FIRST-BAY-001]

公众面展示的是删节后的票据与 H 决定，不展示个人数据、原始敏感输出或思维链。受控审计区保存核查所需记录；现场没有责任人、授权、无障碍链与回退演练时，模型位保持空置，公共地面照常工作。

## 更新项目清单、实施政策与分期计划

**Phase 0 / 0–6 个月：先把未知变成资料。** 取得官方范围和重点区 polygon，完成现状建筑/权属/文保/市政/消防/交通/树木和无障碍调查；七天记录步行、骑行、轮椅、装卸、夜间、温湿度与照度；把三座参考房间重新绑定真实候选地块。此阶段不发布拆建结论。[data:geometry/phasing.geojson#PHASE-0] [assumption:A-BND-001]

**Phase 1 / 6–18 个月：三个可撤回原型。** 用临时铺装、树箱/雨棚、纸本与数字双重导视、人工服务台和围合清楚的机器人测试区，在三个经批准的候选点各做一个 `Shared Floor` 样段；发布基线与使用后数据，达不到无障碍、热舒适、安全和公众接受阈值就修改或撤除。资本工程仅开展设计与审批。[data:geometry/phasing.geojson#PHASE-1] [metric:prototype_count]

**Phase 2 / 18–36 个月：横向网络。** 选择调查证明价值最高的校园、社区、站点、河流和后勤接口，实施连续步行骑行、公共首层和气候庇护；先做可逆更新和存量利用，再讨论新建。**Phase 3 / 3–8 年：条件成熟的重点区建设。** 只有在控规、权属、交通、市政、文保、资金和运营主体明确后，才把验证院、原点廊院和城市交汇厅深化为建筑项目。[data:geometry/phasing.geojson#PHASE-2] [depth:phasing_implementation]

九项更新项目清单依赖真实审批：边界与数字底图；无障碍/夜间现场审计；三段 Shared Floor；验证院；原点廊院；城市交汇厅；七类横向接口；蓝绿气候庇护网络；文化与开放贡献档案。每项记录空间类型、实施主体建议、前置资料、可逆部分、不可逆部分、成功指标和退出条件，不把概念运营主体写成政府承诺。[data:geometry/phasing.geojson#PHASE-3] [depth:renewal_project_list]

## A/B/H 换模面的长期运行与交付

任务书要求提出长期运营机制。[source:AGENT-TASKBOOK] 本方案以每次真实模型、供应商或工具变更为基本单元。城市服务台和 H 路径属于公共底盘；A/B 模型位按合同短租；每个换模窗口结束时，删节票据按既定保留期归档，候选算力和临时数据按契约释放或删除。赞助、运营或模型供应方都不能购买排他入口、个人数据或晋升权。[assumption:A-OPERATIONS-001]

任务书要求年度活动与开发者转化产物。[source:AGENT-TASKBOOK] 本方案把二者压缩为一个可审计、尚未排期的 **京张换模公开周 / Jing-Zhang Changeover Week**。只有具名运营者、场地许可、两名独立责任人和现场基线到位才举办：社区与专业人员先冻结城市任务和失败夹具，开发者提交 B 候选，三处见证空间按同一契约运行 shadow/opt-in 与回退演练，最后发布双语差分票据。未通过者删除临时数据并退出；通过者也只进入有期限、可回退的后续服务合同，不获得独占入口。品牌视觉只用 A/B/H、Δ 和三种空间拓扑；国际传播发布可复核票据而非“冠军模型”。这是 participant-authored `annual_event_system / developer_community_operation / conversion_pathway` 提案，不是政府承诺、已确定活动或现场成果。[assumption:A-OPERATIONS-001]

### 三处见证换模

| 见证包 | 场所与场景 | 同任务比较 | 空间为何不同 | 当前诚实状态 |
|---|---|---|---|---|
| LM-ABH-01 / W1 | 众智园验证院 / AI11 | 冻结 A/B 配置，在公开或已清理基准上运行 normal、ambiguous、hard-stop | 双跨同测让相同夹具、观察距离与 H 急停同时可见；差分负担决定 H 带和跨间隔 | 契约接线已验证；真实 A/B 模型尚未运行，场地未授权 |
| LM-ABH-02 / W2 | AI 原点原点廊院 / AI04 | 同一已清理铁路资料库的两份回答、来源和权限差值 | 差分回廊把分歧与 H 史家裁决并排；公众可沿 H 路径直接完成导览 | 契约接线已验证；史家、资料授权和现场试点未落实 |
| LM-ABH-03 / W3 | 大钟寺城市交汇厅 / AI12 | 同一多语种请求进入共同队列；A/B 只 shadow，公众答案由 H 发出 | 单队列阻止候选挑选容易用户；A、B、H 三出口与回退控制决定柜台和安全等候容量 | 契约接线已验证；真实请求、运营者和现场回退演练未发生 |

三项见证必须先通过专业与公众可达性审查；任何试点都以 no forced participation、H 可选、A/H 热备和可立即恢复普通服务为前提。设计时的 8 项 eligible 不是上线许可，4 项 injected regression 被 HOLD 才是当前最重要的结果。[metric:changeover_eligible_shadow_count] [metric:changeover_held_regression_count]

### 六个可交付更新包

| 包 | 权威范围与空间产物 | 责任主体类型 / 资金类 | 不放行或重绑定条件 |
|---|---|---|---|
| SF-01 官方底图与边界 | 只对约 11.4 km² 临时 SITE-001 做整包重绑定/复算；43.6 km² 统筹研究保持非空间策略，等待官方 polygon | 规划主管类型 + 测绘类型 / 前期研究 | 官方边界、权属或文保控制改变即撤回受影响结论并全包重算 |
| SF-02 无障碍、夜间与运营基线 | 三处重点区各七天观察、伴随路线、站口/门禁/装卸/照明调查 | 街道/交通/无障碍使用者代表类型 / 前期研究 | 无授权参与、无连续无障碍链或无具名运营者即不进入现场试点 |
| SF-03 连续共地与 H 公共底盘 | 七类横向接口、无手机路径、人工柜台、3 个气候庇护环与 8 个湿链空间预留 | 更新实施 + 公共空间运营类型 / 可逆公共工程 | 25 个树冠代理面、1 条脊线和临时范围均须现场核验；不得把 37 polygon 当已建节点 |
| SF-04 验证院双跨同测 | 众智园 6 m 参考网格内 A/B 双跨、H 中带、隔离与急停；规模随官方场地重绑定 | 受控试验运营 + 权利/安全复核类型 / 小型试点 | 同夹具、两钥匙、回退或地面恢复任一失败即保持空置 |
| SF-05 原点差分回廊 | AI 原点公共侧回廊、A/B 来源差分、H 桌与无手机路线 | 高校/社区/文化复核类型 / 可逆更新 | 校门协议、安静时段、资料权利或 H 人员未落实即保持普通公共巷 |
| SF-06 交汇厅单队列三出口 | 大钟寺 P0 先做 8×8 m 可拆共享檐 + 16×16 m 可逆地面；完整厅待控规 | 交通/公共服务运营类型 / 小型试点至条件性更新 | 地铁保护、权属、消防、市政、运营储备或 H 出口缺一即不开放；P0 可拆回原状 |

上述规模与主体均为 participant-authored planning envelopes，不是造价、采购包或机构承诺。[assumption:A-PROJECTS-001] [data:geometry/phasing.geojson#PHASE-3] [depth:renewal_project_list]

## 指标体系、面积复算与合规矩阵

提交的 `known` 指标只描述提交自身：临时总体边界面积、三处临时重点区数量、设计建筑基底、设计绿地/公共空间比例、三座原型、七条横向接口、十二张场景卡、四个测试场景和七类人物。`site_area_sqm` 在 EPSG:4548 下从提交 polygon 复算；`green_ratio` 与 `public_space_ratio` 使用同一临时分母，因此可重复但低置信。任何值都不应改写为官方统计。[metric:site_area_sqm] [metric:green_ratio] [metric:public_space_ratio]

`unknown` 指标包括 FAR、法定高度、建筑密度、道路红线、文保缓冲、拆改留数量、工程投资、市政容量和真实客流。它们没有数字；每项只记录缺失原因、需要的正式来源和更新后必须重算的图层。这样，零不是“没有”，`unknown` 也不会被漂亮图表掩盖。[metric:floor_area_ratio] [assumption:A-CONTROLS-001] [depth:metrics_recalculation]

评审对象只有京张共地这一套方案。性能护照同时检查公共地面连续性、三种类型差异、支撑/填充分离、冬日太阳、夏季遮荫、不依赖智能终端的无障碍通行与服务链、机器人安全停车和边界重绑定；任何生命安全、无障碍或重绑定失败均为刚性淘汰，而不是被总分平均掉。[metric:prototype_count] [metric:building_mass_count] [metric:winter_noon_sun_altitude_deg]

![核心指标、气候计算、未知项与证据链](assets/figures/metrics-evidence.png)

`compliance_matrix.json` 对公告 1.3、1.4、1.5 与设计智能体任务 1–6 的 23 项要求逐项连接章节、图层、指标、来源、假设与自检；`standard_matrix.json` 覆盖六项必选依据，其中包括《无障碍环境建设法》；`design_depth_matrix.json` 的 15 项成果深度均以“已知—未知—设计建议—重算触发”解释成果完成状态。所有图层使用同一要素 ID，HTML、A3/A0 与正文引用相同指标，避免图面出现另一套项目。[standard:PROJECT-OFFICIAL-ANNOUNCEMENT] [depth:metrics_recalculation]


### 换模基线与现场未知项

基线分成“现在可验证的契约事实”和“必须在获批现场试点才可测的效果”，二者不得相互代替：[assumption:A-BASELINE-001]

| 编号 | 现在可验证 | 当前值 | 现场效果字段 | 当前状态 / 停止规则 |
|---|---|---|---|---|
| CB-01 | 12 份契约 × 3 类夹具与票据哈希完整 | 12 / 36 | 同任务完成与非劣效性 | null；未授权前不运行 |
| CB-02 | 每份契约都有 H 路径、两钥匙与默认回退 | 12/12 | 真实 H 可达率、等待与申诉负担 | null；任一 H 断点即停止 B |
| CB-03 | 注入的数据/工具/权限/留存回归被拦截 | 4/4 HOLD，错误晋升 0 | 未知回归与真实事故率 | null；严重回归立即回到 A/H |
| CB-04 | 几何中的普通公共路线连通并触达五处公共空间 | 编码检查通过 | 无手机同任务完成率与残障使用者负担 | null；现场链不连续即不开放 |
| CB-05 | 回退控制与安全终态已在设计时接线 | 编码检查通过 | 现场恢复秒数、服务中断与投诉 | null；演练失败即保持候选空置 |

冬至日照 68.0% 与夏至遮阴 36.6% 仍只是提交几何的简化正午代理，不是 CB 现场基线；法定日照、全年热舒适、风环境和真实使用必须由本地专业与使用者测试。[metric:shared_floor_winter_public_sun_proxy] [metric:shared_floor_summer_public_shade_proxy]

## 风险、版权与合规说明

最大风险是空间证据不足。官方范围、重点区、现状建筑、道路、站口、权属、文保、市政和控规未齐，本方案的真实贡献是原型、关系和重算方法，不是选址审批。临时边界与已命名 OSM 公园的 412.5 米背景差异被醒目标出；官方数据发布后必须触发全包重建，而不是用免责声明继续沿用旧图。[source:BOUNDARY-BASIS] [assumption:A-BND-001] [depth:risk_missing_data]

第二类风险来自公共 AI 与换模本身：机器人可能碰撞或占路，传感可能越界，A/B schema 或工具可能漂移，候选可能把困难用户转给 H 以伪造优势。生成式 AI 管理办法只提供一般治理背景；人优先、同任务同队列、两钥匙、数据最小化、无身份识别、物理停止、纸本/固定标识与 H 热备均是本方案提出、仍待责任主体和专业审核的缓解措施。医疗、法律、公共安全和规划判断永远不由模型单独发布。[source:GENERATIVE-AI-MEASURES] [standard:BARRIER-FREE-ENVIRONMENT-LAW]

第三类风险是“可建造”被误读为“已经可以开工”。本包的 6/8 米参考网格、尺度和影子计算用于检验建筑逻辑；它们不替代地勘、结构、消防、机电、声学、排水、造价、交通影响、文保、无障碍和审批。A3/A0 中的构造剖面均标注为 reference prototype。[assumption:A-LIFE-SAFETY-001] [depth:development_intensity_controls]

版权策略保守：正文、参赛者几何、图表、HTML 和 PDF 版式由本次 agent 工作流创作。外部视觉输入包括带 ODbL 署名的 OSM 数据所派生的定位几何，以及四幅 1909 年《京张路工撮影》低分辨率缩略图；没有复制 OSM 瓦片、页面版式或第三方方案图。[source:OSM-CORRIDOR-CONTEXT-2026] [source:OSM-SEVEN-ROOM-FIGURE-GROUND-2026]

四幅档案图逐项记录来源、IIIF URL、字节哈希与署名；Library of Congress 表示不知道该 World Digital Library 条目存在版权或其他限制，并只在不存在限制时说明可自由使用和再利用，因此本包不把它们简化标为 `public domain`。[source:LOC-JINGZHANG-ALBUM-1909]

图纸内嵌 Noto Sans SC 2.004 Regular 子集；其字节哈希、固定 commit 来源、生成方法与 OFL 1.1 许可链接记录在 `visual/assets/reproducibility.json`。NASA POWER 数据按 NASA 开放数据政策署名；没有嵌入其他投稿作品。由于 agent-track 与专业公告知识产权条款的关系尚未得到书面澄清，方案暂用 `COMMUNITY-DISPLAY-ONLY`，详细记录见 `report/copyright_statement.md`。[source:NASA-DATA-POLICY] [source:OFFICIAL-ANNOUNCEMENT]

模型披露：初版概念、参数化几何、图纸与三张体验图由 OpenAI Codex 工作流生成；体验图使用 Codex 暴露的 OpenAI 图像生成工具，该工具未向本工作流提供模型 ID。v1.2–v1.5b 的文字、表格、打包、校验与 PR 修订由 Claude Code 辅助完成；本地会话记录明确标识 Claude Fable 5，其他 Claude Code 回合没有可核验到同等精度的模型 ID，因此不作更具体断言。当前 v1.6 候选的来源审计、A/B/H 契约验证器、语义修订与可见评审面由 OpenAI Codex 工作流完成。各工作流都没有现场踏勘、获授权访谈或本地专业签署；最终公开身份、提交与实施决定始终属于用户和未来具名责任主体。

## 参考资料

1. 北京市规划和自然资源委员会海淀分局，《百年京张 AI 创新带城市设计国际方案征集资格预审公告》，2026。
2. open-city.ai，《面向智能体任务书》及 formal submission package，当前仓库版本。
3. 北京市园林绿化局，《京张铁路遗址公共空间改造提升工程（二期）配套项目完工》，2026。
4. 北京市园林绿化局，《京张铁路遗址公园（一期）全面建成开放》，2023。
5. 北京市海淀区人民政府，《北京 AI 原点社区，全球 AI 人才创新创业的“第一站”》，2026。
6. 北京市海淀区第七次全国人口普查公报，2021（统计时点 2020-11-01）。
7. 北京市城市更新服务平台，《百年京张 AI 创新带—南部大钟寺 AI 产业集聚区更新片区》，2026。
8. NASA POWER，1991–2020 monthly point API（116.347E, 39.982N）的 30 年聚合及方法说明。
9. 《中华人民共和国无障碍环境建设法》，2023。
10. 《生成式人工智能服务管理暂行办法》，2023。
11. 自然资源部，《国土空间调查、规划、用途管制用地用海分类指南》，2023。
12. 六个国际创新区官方资料索引，详见 `sources.json`；仅用于机制比较，不复用图片或品牌资产。
13. Stephen Kendall, “Open Building: An Approach to Sustainable Architecture,” *Journal of Urban Technology* 6(3), 1999。
14. 故宫博物院，《营造法式》模数研究；仅用于说明中国营造文化的多尺度模数性，不为本项目柱网背书。
15. 北京大学城市治理研究院，学院路六所校园空间整合研究的机构新闻摘要，2025。
16. 北京市发展和改革委员会，《关于清华东路南侧公共空间改造提升项目实施方案的批复》，2026。
17. 直向建筑，Courtyard Hybrid，北京；仅借鉴杂院、可变界面与隐性通路机制。
18. 北京市园林绿化局，《北京市全龄友好型公园建设导则》，2024。
19. 海淀区，北大南门骑手友好驿站，2024。
20. 北京市交通委员会，《无人配送车道路测试与示范应用管理实施细则》，2024。

完整机器索引、URL 或本地路径、获取日期、权利、用途与局限见 `sources.json`；逐项来源审计以相邻 evidence marker 为依据，任何未解析 marker 都阻止 formal-ready 状态。[source:SOURCE-REGISTRY] [source:PRECEDENTS-OFFICIAL]
