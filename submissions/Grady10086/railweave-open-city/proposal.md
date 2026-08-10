---
title: "轨迹织城：百年京张 AI 开源生活实验带"
author_github: "Grady10086"
language: "zh"
license: "CC-BY-4.0"
summary: "以百年京张遗产轴为公共骨架，把研发、开放验证、人才生活与全球社区运营织成一条可逆、可复算、可逐步验证的 AI 城市网络。"
tracks: ["ai-traffic-walkability", "enterprise-services-ecosystem", "civic-agent-governance"]
scenarios: ["ai-traffic-walkability", "enterprise-service-copilot", "public-safety-operations-review"]
iteration: "v1.0"
---

# 轨迹织城：百年京张 AI 开源生活实验带

“轨迹织城 / RailWeave”把“铁路的轨迹、科研的迭代轨迹、智能体的可审计轨迹”叠合为同一套城市方法：不依赖一次性大拆大建，而以一条遗产公共主轴、两侧知识缝合线、三处创新核心、十二个可撤除场景和一套开放治理账本，持续把研究成果转化为市民可体验、企业可验证、专业团队可深化的城市公共产品。所有空间落地建议均为概念建议、参考方案或可供专业团队深化研究，不替代正式规划，不构成政府审定结论。[source:AGENT-TASKBOOK]

## 设计依据与资料清单

方案首先按 `data/source_registry.json` 区分 formal-ready、background-only 与 provisional-only 资料。官方公告仅用于确认项目名称、三层范围文字、约面积和任务；智能体任务书用于六项共创任务与边界条款；专业标准用于约束城市设计、控规语言和用地分类；临时 polygon 只用于 intake 生成与拓扑复核。[source:SITE-PACKAGE] [source:SOURCE-REGISTRY] [source:PROCESSED-FACT-PACK] [source:OFFICIAL-ANNOUNCEMENT] [source:BOUNDARY-SOURCE] [source:KEY-AREA-SOURCE]

现状诊断不是“把临时图形当现状”：当前已知的是京张铁路遗产公园的文化主线、公告给出的三区两翼和三层工作尺度；未知的是精确红线、宗地权属、现状建筑、道路断面、文保控制、市政容量和已批控规。因此本方案把可确定内容落入任务、网络与运营，把不确定内容落入 assumptions 和空的 `constraints.geojson`，拒绝生成虚假的控制线。[data:geometry/site_boundary.geojson#SITE-001] [data:geometry/constraints.geojson#DATA-GAP-REGISTER] [depth:existing_conditions_diagnosis]

![总体概念与证据链](assets/figures/site-overview.png)

本方案使用 CC BY 4.0 发布原创文本、图形与设计数据；案例网页只作为背景机制摘要，不复制图片、商标或受限图表。建筑专业深度标准当前缺官方文件，仅作为数据缺口登记，不把其写成已完成的权威依据。[standard:MOHURD-ARCH-DESIGN-DEPTH-2016]

## 三层范围工作框架

统筹研究范围回答“创新生态怎样循环”，总体设计范围回答“空间网络怎样承载”，三处重点区域回答“哪些组件可以先测试”。43.6 平方公里统筹范围以策略图谱表达，不新增坐标；11.4 平方公里总体设计范围以 provisional SITE_BOUNDARY 组织完整用地分区；368.4 公顷重点范围以三处 provisional KEY_AREA 做组件化详细设计。三层通过同一条证据链传导：任务—空间图层—指标—图纸—运营—复盘。[standard:PROJECT-OFFICIAL-ANNOUNCEMENT] [depth:three_level_scope_framework]

![三层范围与功能织网](assets/figures/land-use-structure.png)

总体结构为“一脉、两环、三核、六线、十二场景”。一脉是京张遗产智脉；两环是开放验证慢行环与全球社区运营环；三核对应众智园、AI 原点社区、大钟寺；六线把高校、社区、轨道接驳与公园界面横向缝合；十二场景分布在研发、生活、公共服务和文化节点。该结构不是道路红线或工程线位，而是服务关系与步行体验的概念表达。[data:geometry/roads.geojson#ROAD-001] [data:geometry/key_areas.geojson#PROV-KEY-001] [depth:overall_spatial_structure]

## 统筹研究范围产业与未来城市研究

### 名称、Logo 与身份系统

主名称“轨迹织城”强调三层含义：京张铁路留下的历史轨迹、科研迭代留下的知识轨迹、智能体决策必须留下的审计轨迹。英文名 **RailWeave Open City**。Logo 采用两条平行轨迹在节点处交织成“开源分叉”，不使用企业商标；主色为铁路深蓝、开放青绿、里程碑琥珀。导视分为“遗产叙事”“开放验证”“日常服务”三套信息层，并以形状、文字和触觉编码补充颜色，避免只靠色彩传递信息。[standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK]

### 七个案例的可转化机制

| 案例 | 只提取的机制 | 对 RailWeave 的转译 |
| --- | --- | --- |
| MIT Kendall Square | 研究、住房、零售、开放空间混合，并以社区参与校准 | 把人才日常与科研发布放进同一条步行网络 [source:CASE-KENDALL-SQUARE] |
| Toronto Vector Institute | 研究、人才培养、行业采用和负责任 AI 连成闭环 | 在众智园设置“验证—治理—采纳”同场机制 [source:CASE-VECTOR-TORONTO] |
| Paris STATION F | 多个加速项目共享校园和服务平台 | 大钟寺采用共享发布厅、服务台和项目制运营 [source:CASE-STATION-F] |
| Singapore one-north | 多分区创新园与研究机构、创业平台共址 | 三区不是复制园区，而是分工互补的开放网络 [source:CASE-ONE-NORTH] |
| Montréal Mila | 高校协作、开放科学、伦理治理与产业采用并行 | AI 原点社区以开源共学和公共利益评审为核心 [source:CASE-MILA-MONTREAL] |
| London Knowledge Quarter | 步行可达的跨机构知识集群 | 六条知识缝合线优先缩短合作与公共访问距离 [source:CASE-KNOWLEDGE-QUARTER] |
| Helsinki Maria 01 | 既有建筑再利用、共同体校园、事件驱动运营 | 先用轻量组件激活再评估长期更新 [source:CASE-MARIA-01] |

案例只支撑机制比较，不支撑海淀地块用途、企业名单、投资额或政策承诺。RailWeave 的创新生态采用“策源—开源—验证—采纳—公共体验—全球传播”六步循环：众智园负责全栈验证和治理议题，AI 原点负责科研转化和人才共同体，大钟寺负责智能原生服务和国际发布，两翼提供科技服务与场景开放。每个项目须同时登记空间需求、数据权限、人工复核和退出条件。[source:AGENT-TASKBOOK] [depth:development_intensity_controls]

## 总体设计范围城市更新与控规深度城市设计

完整用地分区采用官方分类子集：科研用地、绿地与开敞空间、商业服务业用地、社区服务设施用地共同覆盖 provisional SITE_BOUNDARY，无重叠与空洞。它表达功能平衡而非法定用地调整：西侧偏策源研发，中部保持遗产公园和交往空间，东侧承载成果转化与城市服务，社区配套贯穿南北。[data:geometry/land_use.geojson#LU-001] [standard:MNR-LAND-USE-CLASSIFICATION-GUIDE] [depth:land_use_layout]

更新方法采用“保守识别、可逆介入、证据升级”三步。由于现状建筑和权属缺失，不对任何实体建筑下拆除结论；`buildings.geojson` 的六个 footprint 是功能组件需求的空间占位，分别代表开放验证工坊、治理标准客厅、开源转化驿站、人才共学客厅、智能原生发布厅和公共服务体验站。专业团队取得测绘、结构安全、权属和控规后，才能将组件映射为保留、修缮、适应性再利用、拆除或新建。[data:geometry/buildings.geojson#BLDG-001] [depth:retain_renovate_demolish]

控规深度通过“已知—建议—待确认”三栏实现。已知项写入来源和 provisional 状态；建议项写入设计图层；容积率、高度、密度、退线、道路红线、四线和市政容量保持 unknown。建筑风貌建议采用细分体量、可步行首层、可共享庭院、低反射材料和可维护屋顶，不给出审定高度或强度。[standard:MOHURD-CONTROL-DETAILED-PLANNING] [standard:MOHURD-URBAN-DESIGN-MEASURES] [depth:height_massing_character]

## 重点区域详细设计

![三处重点区的差异化抓手](assets/figures/key-areas.png)

### 众智园：可验证的全栈花园

以“开放验证工坊—治理标准客厅—开源里程碑广场”为三件套。研发成果先在封闭沙盒完成安全、能耗、数据和无障碍测试，再进入可撤除的公园界面公开演示；失败项目保留复盘记录而不是永久占用空间。花园型环境以雨水花园、林下讨论、慢行环和低噪测试时段组织。对五环联系只提出接驳关系，桥隧、路口与工程可行性待交通和市政专业深化。[data:geometry/key_areas.geojson#PROV-KEY-001] [depth:three_key_area_detailed_design]

### AI 原点社区：近校共学与低扰动转化

以“开源转化驿站—人才共学客厅—智能体共创庭院”为核心。研究团队可以发布可复现包，居民和公共服务人员以任务提出方身份参与，企业只在明确许可和退出机制下测试。空间更新优先时段共享、首层开放、院落连通和存量适配；涉及高校、园区和社区权属时必须先共商，不把概念连线写成已获同意。[data:geometry/key_areas.geojson#PROV-KEY-002]

### 大钟寺：智能原生城市客厅

以“智能原生发布厅—百年到未来门户—轨道接驳知识缝合线”为核心，服务全球交流、内容消费、企业协作和公众体验。四象限步行联系只表达目标：从地铁口到公共空间形成连续、可读、无障碍的到达链；具体过街、非机动车停放和地下空间须依据 official road redline、客流和消防条件深化。[data:geometry/key_areas.geojson#PROV-KEY-003]

三处片区采用同一评价表：公共利益、数据最小化、人工复核、空间可逆、运营责任、维护成本、失败退出。差异不在“每区都做展厅”，而在众智园验证标准、原点社区策源转化、大钟寺城市采纳的角色分工。

## AI 创新生态、人才画像与 AI+ 场景

### 六类用户画像

| 用户 | 日常痛点 | 需要的空间与服务 | 保护边界 |
| --- | --- | --- | --- |
| 青年研究者 | 跨机构协作成本高 | 可预约共学、可复现实验发布、夜间安全归途 | 不公开未授权研究和身份轨迹 |
| 初创团队 | 验证资源与客户反馈脱节 | 分级沙盒、合规门诊、短租工坊 | 不绑定指定供应商或投资承诺 |
| 社区居民 | 技术不可理解、参与太晚 | 公众体验、申诉台、人工服务保底 | 不做无感人脸识别和个体画像 |
| 公共服务人员 | 系统责任边界不清 | 人机协同工作台、复盘室、可撤回流程 | 最终决定和救济渠道由人承担 |
| 国际访客 | 场地与叙事割裂 | 双语导览、无障碍路线、公开活动日历 | 不强制下载应用或提交身份信息 |
| 运维与一线工作者 | 维护信息分散 | 设备账本、告警分级、现场手动控制 | 不用算法替代安全培训与劳动保障 |

### 十二张场景卡

| # | 场景卡 | 空间 | 数据与人工复核 | 状态 |
| --- | --- | --- | --- | --- |
| S01 | 开源模型可复现台 | 众智园工坊 | 公开数据集、版本哈希；研究员签核 | 产业测试验证 |
| S02 | 机器人共享街区沙盒 | 众智园慢行环 | 匿名事件日志；安全员可急停 | 产业测试验证 |
| S03 | 端侧算力与能耗协同舱 | 众智园服务节点 | 设备级能耗；运维双人复核 | 产业测试验证 |
| S04 | 医疗科普问答亭 | 原点共创庭院 | 不采集病历；医务内容复核 | 公共体验概念 |
| S05 | AI 共学课程编排 | 原点共学客厅 | 自愿学习目标；教师最终决定 | 教育服务概念 |
| S06 | 无障碍导览伴行 | 遗产智脉 | 端侧定位、随时关闭；人工服务保底 | 交通与文化概念 |
| S07 | 多语种铁路故事站 | 遗产节点 | 清权史料；策展人审核 | 文化体验概念 |
| S08 | 公园活动冲突协调 | 公共空间 | 聚合时段需求；管理员裁决 | 城市治理概念 |
| S09 | 中小企业合规导航 | 大钟寺发布厅 | 企业主动提交；专家复核 | 企业服务概念 |
| S10 | 公共服务工单助手 | 社区服务节点 | 脱敏工单；工作人员确认 | 公共服务概念 |
| S11 | 夜间慢行安全提示 | 六条缝合线 | 环境级照明与求助按钮；不做人脸追踪 | 慢行概念 |
| S12 | 开放成果荣誉账本 | 三处地标 | 经授权的项目与贡献记录；可申诉更正 | 社区运营概念 |

十二张卡均写明服务对象、数据最小化、人工复核与退出方式；前三张是明确的产业测试验证场景。它们不是已获批准的运营项目，需伦理、网络安全、无障碍、公共安全与专业审查后分级开放。[metric:scenario_card_count] [source:AGENT-TASKBOOK]

## 用地、建筑规模与拆改留方案

当前 provisional boundary 复算面积为 11412825 平方米，接近公告“约 11.4 平方公里”的任务尺度，但不能当官方精确面积。[metric:site_area_sqm] 设计组件建筑基底合计 213393 平方米，只用于表达功能分布，不代表现状或批准建设规模。[metric:building_footprint_area_sqm]

四类用地的分区原则是“研发靠近验证、开放空间贯穿南北、成果转化面向城市、社区服务嵌入日常”。用地 polygon 共享边界坐标并完整覆盖 SITE_BOUNDARY；正式 polygon 到位后应先重建 land-use partition，再以相同 cut-line 逻辑重建各派生层，避免独立手绘产生缝隙。[data:geometry/land_use.geojson#LU-002] [depth:metrics_recalculation]

拆改留不对具体建筑下结论，而提供核验决策树：具有遗产价值或结构可用者优先保留；空间性能不足但可修复者适应性再利用；确需拆除者必须完成安全、碳排、权属、公众影响和替代方案论证；新增构筑物优先轻量、可逆、可拆卸。FAR 与高度保持 unknown，[depth:development_intensity_controls] 不以建筑占位图替代法定控制。

## 交通、轨道、市政与公共服务设施

七条概念线路总长约 29537 米，构成一条南北遗产步行主轴、两条开放验证骑行弧、三条重点区知识缝合线和一条小月河场景支线。[metric:road_length_m] 它们表达步行、骑行、轨道接驳和服务关系，不表达道路红线、桥隧或施工线位。[data:geometry/roads.geojson#ROAD-004] [depth:traffic_rail_slow_parking]

![交通慢行与蓝绿复合网络](assets/figures/mobility-bluegreen.png)

市政策略采用“端侧—街区—区域”三级接口：端侧设备默认最小数据与断网安全；街区节点提供共享算力、充换电、回收和运维台账；区域层只提出与现有能源、通信、排涝和应急系统的协同需求。没有容量资料时不承诺负荷和管线迁改。[depth:municipal_new_infrastructure]

公共服务采用“数字增强、人工保底、无障碍可达”。所有 AI 入口都应同时提供非智能渠道、清晰告知、撤回机制和申诉路径。停车与非机动车组织先从需求管理、预约共享和清晰导向入手，工程扩容待交通调查、道路红线和消防条件确认。

## 蓝绿空间、公共空间与城市风貌

蓝绿织带把南北遗产主轴与两条横向绿色支撑带联成连续网络，临时复算绿地网络比例为 27.16%，公共空间节点比例为 9.05%；两者都是概念设计值，不能与法定绿地率或 official 公园边界混同。[metric:green_ratio] [metric:public_space_ratio] [data:geometry/green_space.geojson#GREEN-001] [data:geometry/public_space.geojson#PUBLIC-001] [depth:blue_green_public_space]

三处“AI 朝圣”节点拒绝巨型奇观：①开源里程碑广场以可更新的贡献账本记录经授权成果；②智能体共创庭院把失败复盘、公众问题和研究回应并置；③百年到未来门户以铁路时间刻度连接詹天佑精神、北京创新史与当代开源文化。节点均采用低扰动、可逆、可维护组件，具体位置须经文保、绿地、权属和安全审查。

城市风貌以“硬朗轨迹、温暖日常、可见维护”为基调：轨迹线用于导向，木与再生金属形成可维修界面，夜间照明避免眩光和过度媒体化。公共空间组件库包括可移动共学桌、开源展示轨、端侧服务柱、可撤除测试围合、雨水花园坐凳和无障碍触觉导向。所有字体、图像和人物内容需清权。

## 更新项目清单、实施政策与分期计划

| 项目 | 阶段 | 先决条件 | 可退出机制 |
| --- | --- | --- | --- |
| 遗产智脉最小连续段 | 近期 | 文保、公园、权属与无障碍踏勘 | 组件可撤除，线路可调整 |
| 三处开放验证客厅 | 近期 | 场地协议、数据与安全评审 | 项目到期复盘，不自动续期 |
| 六条知识缝合线 | 中期 | 交通调查、道路红线、公众共商 | 先做时段与导向试验 |
| 蓝绿横向支撑带 | 中期 | 水务、园林、排涝与养护方案 | 以低扰动试点替代永久工程 |
| 三区协同运营平台 | 中期 | 多方治理章程、公开指标 | 年度第三方审计与退出 |
| official polygon 复算深化 | 远期 | 正式附件与专业团队 | 全量重建图层和指标 |

分期 polygon 把北、中、南三个行动带分开，仅用于表达工作顺序，不是政府开发时序。[data:geometry/phasing.geojson#PHASE-001] [depth:phasing_implementation] 近期优先做可逆连接、三处客厅和公开账本；中期依据评估扩展蓝绿与缝合网络；远期在 official data 到位后复算并进入专业深化。[depth:renewal_project_list]

长期运营采用“一年四季一闭环”：春季开放问题征集，夏季场景测试季，秋季全球开源城市周，冬季责任审计与失败复盘。每个活动形成公开任务、参与规则、评审结果、维护责任和下一轮改进；开发者由游客转为贡献者，企业由展示者转为场景责任方，居民由被服务者转为共同定义问题的人。活动均为概念建议，不构成已确定安排、资金或招商承诺。[source:AGENT-TASKBOOK]

## 指标体系、面积复算与合规矩阵

![核心指标与自检证据链](assets/figures/metrics-evidence.png)

核心指标遵循“可复算优先、未知不填零”。[metric:site_area_sqm]、[metric:building_footprint_area_sqm]、[metric:green_ratio]、[metric:public_space_ratio]、[metric:road_length_m]、[metric:key_area_count] 与 [metric:scenario_card_count] 均在 `metrics.json` 给出公式、来源文件、置信度和 assumptions。三处重点区数量为 3，[data:geometry/key_areas.geojson#PROV-KEY-001] 只证明当前包覆盖了三处任务，不证明 polygon 为 official。

指标同时承担设计判断：绿地网络检验遗产主轴与横向联系是否连续；公共空间节点检验创新是否进入日常；慢行长度检验三核是否被同一体验链连接；场景卡数量只是最低完整度，真正质量由数据边界、人工复核、退出机制和服务对象决定。人才密度、产值、FAR、高度和市政容量因缺乏正式底数保持 unknown，不用虚构目标替代资料。[depth:risk_missing_data]

`compliance_matrix.json` 覆盖公告 1.3、1.4、1.5 与 agent.1-agent.6；`standard_matrix.json` 连接标准、章节、图层、指标与图纸；`design_depth_matrix.json` 记录十五项 formal 深度。以下引用完整声明本方案的专业证据链：[standard:PROJECT-OFFICIAL-ANNOUNCEMENT] [standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK] [standard:MOHURD-URBAN-DESIGN-MEASURES] [standard:MOHURD-CONTROL-DETAILED-PLANNING] [standard:MNR-LAND-USE-CLASSIFICATION-GUIDE] [standard:MOHURD-ARCH-DESIGN-DEPTH-2016] [depth:existing_conditions_diagnosis] [depth:three_level_scope_framework] [depth:overall_spatial_structure] [depth:land_use_layout] [depth:development_intensity_controls] [depth:height_massing_character] [depth:retain_renovate_demolish] [depth:traffic_rail_slow_parking] [depth:municipal_new_infrastructure] [depth:blue_green_public_space] [depth:three_key_area_detailed_design] [depth:renewal_project_list] [depth:phasing_implementation] [depth:metrics_recalculation] [depth:risk_missing_data]

## 风险、版权与合规说明

首要风险是“漂亮图面制造虚假精确”。因此 provisional boundary 在所有图面中以低对比虚线表达，面积和比例标为 intake 复算；official polygons 到位后需重算 site、key areas、land use、roads、green space、public space、buildings、phasing、metrics、五张图、HTML 与 PDF。第二类风险是技术替代人的责任：所有公共服务场景保留人工决定、非智能渠道、告知、撤回和申诉。第三类风险是权属、文保和工程未知：不提交具体拆改、桥隧、地下空间、道路红线、管线或投资结论。[source:SOURCE-REGISTRY]

版权方面，正文、GeoJSON 设计层、图解、HTML 和 PDF 由本次 AI agent 生成；官方/清权资料只作引用，全球案例只摘录机制并链接官方页面，不复用其图片、商标或版式。详见 `report/copyright_statement.md`。本成果是开放共创建议，最终发布、专业判断与现实落地由维护者和相关专业团队依法依规决定。

## 参考资料

- 征集任务与范围：[source:OFFICIAL-ANNOUNCEMENT] [source:SITE-PACKAGE]
- 智能体任务与共创边界：[source:AGENT-TASKBOOK]
- 资料权限与处理导航：[source:SOURCE-REGISTRY] [source:PROCESSED-FACT-PACK]
- 临时几何：[source:BOUNDARY-SOURCE] [source:KEY-AREA-SOURCE]
- 专业依据：[standard:PROJECT-OFFICIAL-ANNOUNCEMENT] [standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK] [standard:MOHURD-URBAN-DESIGN-MEASURES] [standard:MOHURD-CONTROL-DETAILED-PLANNING] [standard:MNR-LAND-USE-CLASSIFICATION-GUIDE]
- 全球案例官方页面：[source:CASE-KENDALL-SQUARE] [source:CASE-VECTOR-TORONTO] [source:CASE-STATION-F] [source:CASE-ONE-NORTH] [source:CASE-MILA-MONTREAL] [source:CASE-KNOWLEDGE-QUARTER] [source:CASE-MARIA-01]
