# -*- coding: utf-8 -*-
"""全量英文图件再生：完整翻译映射 + matplotlib 文本 monkey-patch。"""
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib.patches import FancyBboxPatch

SCRIPTS = Path(r"C:/Users/wengyongsheng/Desktop/open-city-ai/haidian/scripts")
sys.path.insert(0, str(SCRIPTS))
REPO = SCRIPTS.parent
SUB = REPO / "submissions" / "wengyongsheng29-spec" / "jingzhang-agent-native-belt"
FIG_DIR = SUB / "assets" / "figures"

import gen_figures_real as g
g.REPO = REPO; g.SUB = SUB; g.FIG_DIR = FIG_DIR

# ── 完整翻译映射（中文 → 英文）──
T = {
    # 通用 / 单位 / 结构
    "个":"", "处":"", "栋":"", "核":"", "类":"", "一轴":"1 Axis", "三核":"3 Cores", "两翼":"2 Wings",
    "协同":"Synergy", "图例":"Legend", "图 例":"Legend", "保留":"Retain", "改造":"Renovate", "新建":"New Build",
    "协议":"Protocol", "展示":"Exhibit", "平台":"Platform", "保留（现状建筑）":"Retain (Existing)",
    "改造更新（老旧厂房/低效楼宇）":"Renovate (Old/Low-Efficiency)", "拆除新建（旗舰项目）":"Demolish & Build (Flagship)",
    # 标题
    "交通 · 蓝绿 · 公共空间":"Mobility · Blue-Green · Public Space",
    "指标体系与全球案例对照":"Metrics Dashboard & Global Case Comparison",
    "概念剖面 · 南北向天际线":"Concept Section — N-S Skyline",
    "实施路线图与治理结构":"Implementation Roadmap & Governance",
    "三核现状分析：机构锚点 · 可更新用地概念分类 · 利益相关者":"Three-Core Status: Institutional Anchors · Conceptual Renewal Land · Stakeholders",
    "三核详细设计  Key Areas Detailed Concept":"Key Areas Detailed Concept",
    "铁路信号 → 1909协议 转译表":"Railway Signal → Protocol 1909 Translation",
    "源自铁路信号的空间交互协议":"A Spatial Interaction Protocol Derived from Railway Signalling",
    "AI 原生创新带 · 概念方案总览":"AI-Native Innovation Belt — Concept Overview",
    "用地结构":"Land Use Structure",
    # 品牌/标题
    "智脉京张":"ZHIMAI JING-ZHANG",
    "智脉京张 · AI原生创新带概念方案":"ZHIMAI JING-ZHANG · AI-Native Innovation Belt Concept Proposal",
    "空间结构":"Spatial Structure",
    "结构要点":"Key Structural Elements",
    "用地分区":"Land Use Zones",
    "治理结构":"Governance Structure",
    "关键成功因素":"Key Success Factors",
    "政策对齐依据":"Policy Alignment Basis",
    "独特价值":"Distinctive Value",
    "设计范围":"Design Area",
    "统筹研究范围":"Coordinated Research Scope",
    "三核重点区域":"Three-Core Key Areas",
    "研究范围":"Research Area",
    "总体设计范围":"Overall Design Scope",
    # 范围/指标
    "绿地率":"Green Ratio", "公共空间率":"Public Space Ratio", "公共空间":"Public Space",
    "绿地/绿廊":"Green / Corridor", "绿地/公共空间":"Green / Public Space", "公共绿地":"Public Green",
    "水系":"Water", "建筑肌理":"Building Fabric", "铁路绿廊":"Railway Green Corridor",
    "铁路绿廊（一轴）":"Railway Green Corridor (Axis)", "京张铁路绿廊（一轴）":"Jingzhang Railway Green Corridor (Axis)",
    "京张铁路绿廊 — 全长约9km":"Jingzhang Railway Green Corridor — ~9 km",
    "京张绿廊·公共主轴":"Jingzhang Green Corridor · Public Axis",
    "京张绿廊主轴":"Jingzhang Green Corridor Axis",
    "设计范围边界":"Design Area Boundary",
    "AI场景节点":"AI Scenario Nodes", "AI场景":"AI Scenarios", "朝圣地标":"Pilgrimage Landmarks",
    "朝圣地标 ★":"Landmarks ★", "节点广场":"Node Plaza", "社区广场":"Community Plaza",
    "绿廊步行街":"Green Corridor Pedestrian Street", "地铁站点":"Metro Station", "500m覆盖圈":"500m Catchment",
    "自行车道":"Bike Lane", "主干路":"Arterial", "次干路":"Secondary", "慢行道":"Slow Path",
    "慢行交汇节点":"Slow-Mobility Junction", "公共空间连廊":"Public Space Connector",
    "高校/科研院所":"Univ / Research Inst",
    # 三核
    "众智园":"Zhongzhiyuan", "AI原点":"AI Origin", "AI原点社区":"AI Origin Community",
    "大钟寺":"Dazhongsi", "北京AI原点社区":"Beijing AI Origin Community",
    "众智园范围":"Zhongzhiyuan Boundary", "AI原点社区范围":"AI Origin Boundary", "大钟寺范围":"Dazhongsi Boundary",
    "众智园（北核）":"Zhongzhiyuan (N)", "AI原点社区（中核）":"AI Origin (C)", "大钟寺（南核）":"Dazhongsi (S)",
    "北核 · AI全栈自主创新加速区 · 191.9 ha":"N Core · AI Full-Stack Innovation · 191.9 ha",
    "中核 · 24h混合创新社区 · 104.3 ha":"C Core · 24h Mixed Community · 104.3 ha",
    "南核 · AI+产业门户 · 72.4 ha":"S Core · AI+ Industry Gateway · 72.4 ha",
    "AI自主创新加速区 · 191.9 ha":"AI Full-Stack Innovation Zone · 191.9 ha",
    "24h混合创新社区 · 104.3 ha":"24h Mixed Innovation Community · 104.3 ha",
    "AI+产业门户 · 72.4 ha":"AI+ Industry Gateway · 72.4 ha",
    "AI全栈自主创新加速区":"AI Full-Stack Innovation Accelerator",
    "24h混合创新社区":"24h Mixed Innovation Community",
    "AI+商业文化门户":"AI+ Business & Culture Gateway",
    "AI原点·混合社区":"AI Origin · Mixed Community",
    "众智园·研发中试":"Zhongzhiyuan · R&D Pilot",
    "大钟寺·商务消费":"Dazhongsi · Business & Retail",
    "三核 · 一轴 · 两翼":"3 Cores · 1 Axis · 2 Wings",
    "三核主体":"Three Cores", "三核功能主体":"Three-Core Functions",
    "众智园 · AI原点 · 大钟寺":"Zhongzhiyuan · AI Origin · Dazhongsi",
    "368.6 ha（众智园·AI原点·大钟寺）":"368.6 ha (Zhongzhiyuan · AI Origin · Dazhongsi)",
    # 两翼
    "科技服务翼（西）+ 场景赋能翼（东）":"Tech-Service Wing (W) + Scenario Wing (E)",
    "科技服务翼（西）· 场景赋能翼（东）":"Tech-Service Wing (W) · Scenario Wing (E)",
    "▲ 科技服务翼（西翼）":"▲ Tech-Service Wing (W)",
    "场景赋能翼（东翼）▼":"Scenario Empowerment Wing (E) ▼",
    "东翼·场景赋能":"E Wing · Scenario", "西翼·科技服务":"W Wing · Tech",
    "两翼城市更新":"Two-Wing Urban Renewal", "两翼城市腹地":"Two-Wing Urban Hinterland",
    # 高校/科研/机构
    "清华大学":"Tsinghua Univ", "北京大学":"Peking Univ", "北京航空航天大学":"Beihang Univ",
    "北京师范大学":"BNU", "北京邮电大学":"BUPT", "北京交通大学":"Beijing Jiaotong Univ",
    "北京林业大学":"Beijing Forestry Univ", "中国科学院":"CAS", "中国信通院":"CAICT",
    "中科院":"CAS", "中科院自动化所":"CAS Institute of Automation", "信通院":"CAICT",
    "北航":"Beihang", "北师大":"BNU", "北邮":"BUPT", "北交大":"BJTU", "清华":"Tsinghua",
    "清华·北大":"Tsinghua · PKU", "八大学院":"Eight Universities", "铁科院":"CARS",
    "中国农大(东校区)":"China Agricultural Univ (E)", "中国矿大(北京)":"CUMT (Beijing)",
    # 车站/道路
    "大钟寺站":"Dazhongsi Stn", "大钟寺站(12/13号线)":"Dazhongsi Stn (Line 12/13)",
    "五道口站":"Wudaokou Stn", "五道口站(13号线)":"Wudaokou Stn (Line 13)",
    "学知园站":"Xuezhiyuan Stn", "学知园站(昌平线)":"Xuezhiyuan Stn (Changping Line)",
    "知春路站":"Zhichunlu Stn", "西土城站":"Xitucheng Stn", "北京北站":"Beijing North Stn",
    "清华东路西口":"Tsinghua E Rd West", "清华东路":"Qinghua East Rd", "成府路":"Chengfu Rd",
    "中关村大街":"Zhongguancun St", "中关村东区":"ZGC East", "中关村科学城":"ZGC Science City",
    "京藏高速":"Jingzang Expwy", "北三环西路":"N 3rd Ring West Rd", "方恒·中坤广场":"Fangheng·Zhongkun Plaza",
    "紫竹院公园":"Zizhuyuan Park", "10/13号线":"Line 10/13", "12/13号线":"Line 12/13",
    "13号线":"Line 13", "15号线":"Line 15", "昌平线":"Changping Line", "10/昌平线":"Line 10/Changping",
    "地铁覆盖":"Metro Coverage", "轨道接驳枢纽":"Rail Interchange Hub",
    "双清路·东南门":"Shuangqing Rd · SE Gate", "学院路37号\\nAI学院·具身智能":"37 Xueyuan Rd · AI School · Embodied AI",
    "学院路丁11号":"Xueyuanlu Ding-11", "上园村3号":"3 Shangyuancun", "大柳树路2号":"2 Daliushu Rd",
    "新街口外大街19号":"19 Xinjiekouwai St", "中关村东路95号":"95 Zhongguancun E Rd",
    "花园北路52号":"52 Huayuan N Rd", "清华东路17号":"17 Qinghua E Rd", "清华东路35号":"35 Qinghua E Rd",
    "西土城路10号":"10 Xitucheng Rd",
    # 场景
    "健康导航":"Health Nav", "健康导航站":"Health Nav Station", "文化导览":"Cultural Guide",
    "AI导览":"AI Guide", "AI教育":"AI Education", "AI教育空间":"AI Education Space",
    "法律助手":"Legal Assistant", "公共议题路由":"Issue Routing", "机器人配送":"Robot Delivery",
    "自动接驳":"Auto Shuttle", "无障碍畅行":"Accessible Mobility", "AI定制零售":"AI Retail",
    "金融合规":"Finance Compliance", "金融合规顾问":"Finance Compliance Advisor", "沉浸体验":"Immersive Experience",
    "开源成果展示廊":"Open-Source Gallery", "开源成果廊":"Open-Source Gallery", "开发者步道":"Developer Trail",
    "联合办公":"Co-working", "研究者公寓":"Researcher Housing", "社区AI中心":"Community AI Center",
    "红队测试床":"Red-Team Testbed", "算力沙盒":"Compute Sandbox", "AI展示中心":"AI Exhibition Center",
    "AI总部大楼":"AI HQ Tower", "商业中心":"Commercial Center", "算力中心":"Compute Center",
    "模型机房":"Model Roundhouse", "孵化器集群":"Incubator Cluster", "大模型训练中试":"LLM Training Pilot",
    # 空间类型学
    "A  算力水塔":"A  Compute Tower", "B  提示广场":"B  Prompt Plaza",
    "C  模型机房":"C  Model Roundhouse", "D  道岔广场":"D  Switch Plaza",
    "算力水塔":"Compute Tower", "提示广场":"Prompt Plaza", "道岔广场":"Switch Plaza",
    "原型：铁路水塔（蒸汽机车补水）":"Archetype: railway water tower (steam refill)",
    "原型：广场 + 命令行":"Archetype: plaza + command line",
    "原型：铁路扇形车库+转车盘":"Archetype: railway roundhouse + turntable",
    "原型：铁路道岔（扳道工控制方向）":"Archetype: railway switch (pointsman)",
    # 1909协议
    "闭塞分区":"Block Section", "信号机":"Semaphore", "联锁":"Interlocking", "路签":"Token",
    "调度所":"Dispatch Center", "人字形折返":"Switchback", "空间沙箱":"Spatial Sandbox",
    "空间状态信号":"Spatial Semaphore", "安全联锁":"Safety Interlock", "空间凭证":"Spatial Token",
    "人在回路调度台":"Human-in-the-loop Dispatch", "问题分解路由":"Problem-decomposition Routing",
    "闭塞分区 Block Section":"Block Section", "信号机 Semaphore":"Semaphore",
    "联锁 Interlocking":"Interlocking", "路签/路牌 Token":"Token",
    "调度所 Dispatch":"Dispatch", "人字形折返 Switchback":"Switchback",
    "人字形折返 Switchback Routing":"Switchback Routing",
    "空间沙箱 Spatial Sandbox":"Spatial Sandbox",
    "AI agent持加密凭证\\n进入分区，含场景ID\\n权限/有效期/责任主体":"AI agent enters zone with encrypted token: scene ID, permissions / validity / responsible entity",
    "明确边界/时段/配额\\n分区内自主运行\\n故障不波及他区":"Clear boundary / time / quota; autonomous within zone; faults isolated",
    "数据权限 + 物理安全\\n+ 社区授权 三者联锁\\n任一不满足则禁止":"Data permission + physical safety + community authorization interlocked; any unmet = blocked",
    "加密路签由OS签发，社区可吊销，无签=入侵":"Encrypted token issued by OS, revocable by community; no token = intrusion",
    "透明人在回路审批台\\nAI提议→人类决策\\n市民可旁观质询":"Transparent human-in-the-loop desk; AI proposes → human decides; citizens observe",
    "AI场景有明确边界/时段/权限/配额，故障隔离":"AI scenes have clear boundary/time/permission/quota; faults isolated",
    "复杂AI问题自动分解 → 路由到专门agent → 在「折返点」汇总（源自詹天佑人字形展线智慧）":"Complex AI problems auto-decompose → route to specialists → converge at switchback (from Zhan Tianyou's wisdom)",
    "复杂问题分解→子agent处理→折返点汇总":"Complex problem → sub-agent handling → switchback convergence",
    "「人在回路」决策节点 · 三核各1处":"Human-in-the-loop decision node · 1 per core",
    "重新定义AI与城市空间的交互规则。\\n不是技术堆栈，而是空间-数字混合的\\n安全制度，可被其他城市复用。":"Redefines AI-city interaction rules — not a tech stack but a spatial-digital safety institution, reusable by other cities.",
    "现有「智慧城市」标准从IT视角出发（网络协议、数据标准）；":"Existing smart-city standards start from an IT view (network protocols, data standards);",
    # 1909协议背景
    "京张铁路通车 · 詹天佑「人」字形展线 · 信号闭塞制度（分区—联锁—凭证—闭塞）":"Jingzhang Railway opened · Zhan Tianyou's switchback · block signalling (section-interlock-token-block)",
    " → 117年后转译为AI时代的空间安全协议":" → translated 117 years later into an AI-era spatial safety protocol",
    # 类型学描述
    "分布式边缘计算 · 50-200 TOPS · 500m服务半径":"Distributed edge compute · 50-200 TOPS · 500m radius",
    "高8-15m塔状地标，屋顶光伏+绿电直供":"8-15m tower landmark, rooftop PV + green power",
    "底部半公共空间：咖啡/信息/座椅":"Semi-public base: café / info / seating",
    "余热":"Waste Heat", "余热→相邻温室/公共浴室":"Waste heat → adjacent greenhouse / bath",
    "余热回收→冬季户外供暖/温室":"Waste-heat recovery → winter outdoor heating / greenhouse",
    "人-AI协同创造 · 2000-3000㎡ · AI原点社区中心":"Human-AI co-creation · 2000-3000㎡ · AI Origin Center",
    "地面/墙面压感投影，可移动模块化家具":"Floor/wall pressure-projection, modular movable furniture",
    "高速WiFi + 户外电源，全天候可用":"High-speed WiFi + outdoor power, 24/7",
    "开放、无门槛的公共AI体验空间":"Open, no-threshold public AI experience space",
    "旧厂房改造AI训练设施，玻璃隔断可见机房":"Old factory → AI training facility, glass partitions reveal server room",
    "可见的AI训练 · 3000-5000㎡ · 众智园":"Visible AI training · 3000-5000㎡ · Zhongzhiyuan",
    "中央可旋转展示/演示平台":"Central rotating exhibit / demo platform",
    "玻璃隔断 · 可见机房":"Glass partition · visible server room",
    "服务器灯光=新工业景观，延续京张美学":"Server lights = new industrial landscape, continuing Jingzhang aesthetics",
    "真实可操作旧道岔+数字投票屏":"Real operable old switch + digital voting screen",
    "决策可回滚，结合现有广场设置":"Decisions rollback-able, set in existing plazas",
    "可决定：机器人配送时段/数据保留天数/AI导览开关":"Decidable: robot delivery hours / data retention days / AI guide on-off",
    "每月「扳道日」集体决策":"Monthly 'Switch Day' collective decision",
    "本月投票":"This Month's Vote", "扳道杆":"Switch Lever",
    "场景准入+伦理审查":"Scene admission + ethics review",
    "数据保留":"Data Retention", "配送时段":"Delivery Hours",
    "绿=运行  黄=测试\\n红=人工  蓝=维护\\n状态市民可见":"Green=running  Yellow=test; Red=manual  Blue=maintenance; visible to citizens",
    "绿/黄/红/蓝四色可见，市民一眼可知AI状态":"Green/yellow/red/blue visible; citizens see AI state at a glance",
    "咖啡 / 信息 / 座椅":"Café / Info / Seating",
    "边缘计算":"Edge Compute", "城市OS光纤骨干":"Urban OS Fiber Backbone",
    # 实施/分期
    "近期 1-3年\\n示范启动":"Near-term 1-3y · Pilot launch",
    "中期 3-5年\\n系统成型":"Mid-term 3-5y · System formation",
    "远期 5-10年\\n生态成熟":"Long-term 5-10y · Ecosystem maturity",
    "投资估算":"Investment Estimate", "政府引导+社会资本":"Gov guidance + social capital",
    "政府基建+专项债":"Gov infrastructure + special bonds", "社会资本+运营收入":"Social capital + operating revenue",
    "合计 115-185亿元":"Total ¥11.5-18.5bn", "15-25亿":"¥1.5-2.5bn", "40-60亿":"¥4-6bn", "60-100亿":"¥6-10bn",
    "区政府牵头":"District gov leads", "区属国企+专业团队":"District SOE + professional team",
    "运营平台公司":"Operating platform company", "领导小组":"Leading group", "专家委员会":"Expert committee",
    "社区议事会":"Community council", "居民+商户+运营方":"Residents + merchants + operator",
    "规划/科技/财政/街道":"Planning / S&T / Finance / Subdistrict",
    "规划与制度建设":"Planning & Institutional Building", "日常运营/场景/活动":"Daily Operation / Scenes / Events",
    "品牌从第一年启动：Open Week不等全部建成":"Brand launches year 1: Open Week needn't wait for full build-out",
    "场景即建即活：示范段建成时首批场景同步上线":"Scenes go live with the pilot: first scenes launch when demo section completes",
    "数据制度先行：开放细则+隐私标准+准入流程在建设前出台":"Data rules first: open rules + privacy standards + admission before construction",
    "人才公寓先建：首批开工即含人才公寓，安居留人":"Talent housing first: first groundbreakings include talent housing",
    "数据开放细则":"Data Open Rules", "数据保留":"Data Retention",
    "OS 1.0上线":"OS 1.0 live", "中试层投用":"Pilot floor operational",
    "首批AI场景落地":"First AI scenes live", "15场景运营":"15 scenes operating",
    "众智园改造建设":"Zhongzhiyuan renewal", "绿廊南北全贯通":"Corridor fully connected N-S",
    "约9km贯通":"~9km connected", "人才公寓建设":"Talent housing construction", "首批入住":"First move-ins",
    "大钟寺门户建设":"Dazhongsi gateway construction", "蓝景丽家建成":"Lanjing Lijia complete",
    "原点碑落成":"Origin stele complete", "首届举办":"First edition", "首次分红":"First dividend",
    "示范段开放":"Demo section open", "绿廊示范段贯通":"Corridor demo section connected",
    "AI原点社区建设":"AI Origin Community construction",
    # 机构/锚点
    "锚定机构":"Anchor Institutions", "开源文化":"Open-Source Culture", "中试共享":"Pilot Sharing", "公共性":"Publicness",
    "评分（1=弱  5=强）":"Score (1=Weak  5=Strong)",
    # 全球案例
    "蒙特利尔":"Montreal", "波士顿":"Boston", "伦敦":"London", "巴黎":"Paris",
    "巴塞罗那":"Barcelona", "纽约":"New York", "赫尔辛基":"Helsinki", "深圳":"Shenzhen",
    "北京海淀":"Beijing Haidian", "本方案":"This Plan",
    # 图注/免责
    "注：评分为概念性对照（1-5分），基于公开资料整理；评分规则：1=基础缺失 2=有概念无落地 3=有策略待验证 4=有落地路径和KPI 5=有实施机制和验证框架；评分主体为方案团队基于公开资料的概念性评估，非第三方专业评审；全球案例数据来自公开报道，可能存在统计口径差异。空间指标依据 GeoJSON 在 EPSG:4548 投影下复算。所有空间建议均为概念方案，不构成政府审定结论。":"Note: scores are conceptual comparison (1-5), compiled from public sources; rules: 1=foundation missing 2=concept only 3=strategy pending verification 4=landing path & KPIs 5=implementation mechanism & verification framework; scoring is the team's conceptual self-assessment, not third-party review; global case data from public reports may differ in statistical caliber. Spatial metrics recomputed in EPSG:4548. All spatial recommendations are conceptual and not government-approved conclusions.",
    "图注：1909协议为概念性制度设计建议，具体技术标准、工程做法、管理制度需专业团队深化研究和相关部门审批。":"Note: Protocol 1909 is a conceptual institutional proposal; technical standards, engineering and management require professional refinement and authority approval.",
    "图注：四种AI原生空间类型均为概念建议，具体建筑设计、结构、设备需专业团队深化研究。":"Note: the four AI-native spatial typologies are conceptual; architecture, structure and equipment require professional refinement.",
    "PROVISIONAL · CONCEPT ONLY — 本图为概念方案，边界为示意性表达，仅供专业团队深化研究参考":"PROVISIONAL · CONCEPT ONLY — conceptual scheme, schematic boundaries for professional refinement only",
    "现状基础：已建成园区·科研机构入驻（概念示意）":"Existing: built campus · research institutions (concept)",
    "更新策略：保留·改造·新建（具体规模待可研）":"Renewal: Retain · Renovate · New Build (scale pending feasibility)",
    "更新方向：国际交流中心（概念建议，待可研）":"Renewal: Intl Exchange Center (concept, pending feasibility)",
    # 站点/区位
    "五道口\\n(13号线)":"Wudaokou (L13)", "大钟寺\\n(12/13号线)":"Dazhongsi (L12/13)",
    "学知园\\n(昌平线)":"Xuezhiyuan (Changping)", "六道口\\n(15/昌平线)":"Liudaokou (L15/Changping)",
    "知春路\\n(10/13·31万/日)":"Zhichunlu (L10/13 · 310k/day)",
    "清华东路西口\\n(15号线)":"Tsinghua E Rd W (L15)", "西直门\\n(2/4/13·全网第一)":"Xizhimen (L2/4/13 · top interchange)",
    "北 ↑\\n北五环":"N ↑ North 5th Ring", "南 ↓\\n北京北站":"S ↓ Beijing North Stn",
    "中坤广场·12/13号线\\nAI+消费先导区":"Zhongkun Plaza · L12/13 · AI+ retail pilot",
    "大钟寺商圈\\nAI+消费升级":"Dazhongsi retail · AI+ consumption upgrade",
    "五道口\\n城市更新":"Wudaokou urban renewal", "六道口站\\n一体化更新":"Liudaokou Stn integrated renewal",
    "知春路\\n楼宇升级":"Zhichunlu building upgrade", "北京北站\\n枢纽提升":"Beijing North Stn hub upgrade",
    "学清路\\n轨道微中心":"Xueqing Rd rail micro-center", "中坤广场\\n功能转型":"Zhongkun Plaza function shift",
    "北航周边\\n混合功能":"Beihang mixed-use", "五环绿带\\n衔接节点":"5th Ring greenbelt junction",
    "清华校园\\n（保留）":"Tsinghua campus (retain)", "北大校园\\n（保留）":"PKU campus (retain)",
    "北航校园\\n（保留）":"Beihang campus (retain)", "矿大·地大\\n校园（保留）":"CUMT·CUGB campus (retain)",
    "农大·林大\\n校园（保留）":"CAU·BFU campus (retain)", "中科院院所\\n（保留）":"CAS institutes (retain)",
    "铁科院\\n（保留）":"CARS (retain)", "北交大校园\\n（保留）":"BJTU campus (retain)",
    "地大·矿大·林大\\n农大·北科·北语":"CUGB·CUMT·BFU · CAU·USTB·BLCU",
    "东升大厦·清华科技园\\n200+AI企业":"Dongsheng Tower · Tuspark · 200+ AI firms",
    "学院路37号\\nAI学院·具身智能":"37 Xueyuan Rd · AI School · Embodied AI",
    # 利益相关者
    "农大·林大·矿大·地大·学知园/六道口站·学院路街道·东升镇·京张遗址公园":"CAU·BFU·CUMT·CUGB·Xuezhiyuan/Liudaokou·Xueyuan Rd·Dongsheng·Jingzhang Park",
    "清华·北大·中科院·北航·信通院·东升大厦·200+AI企业·中关村街道·海淀街道":"Tsinghua·PKU·CAS·Beihang·CAICT·Dongsheng·200+AI firms·ZGC·Haidian",
    "北邮·北师大·北交大·铁科院·大钟寺商圈·北京北站·北下关街道":"BUPT·BNU·BJTU·CARS·Dazhongsi·Beijing North Stn·Beixiaguan",
    # 站点现状
    "6站500m覆盖率约62%，800m约85%":"6 stations: ~62% at 500m, ~85% at 800m",
    "京张铁路遗址公园规划":"Jingzhang Railway Heritage Park Plan",
    "13.5km线性公园，本方案绿廊为其核心段":"13.5km linear park; this scheme's corridor is its core section",
    "北京城市总体规划(2016-2035)":"Beijing Master Plan (2016-2035)",
    "北京市加快建设全球数字经济标杆城市":"Beijing accelerating global digital-economy benchmark city",
    "海淀科技创新中心核心区定位":"Haidian S&T innovation core positioning",
    "海淀街区控规(2026.8公告)":"Haidian block control plan (2026.8)",
    "学北园等更新地块已纳入控规":"Xuebeiyuan renewal parcels in control plan",
    "官方已公布投资计划，本方案对齐":"Official investment plan published; this scheme aligns",
    "蓝景丽家48.8亿社会投资(2026.8)":"Lanjing Lijia ¥4.88bn private (2026.8)",
    "约1km":"~1 km", "沿绿廊每2km一座，共6-8座":"one per 2km along corridor, 6-8 total",
    "441栋概念建筑，按功能分色":"441 concept buildings, color by function",
    "低多层混合+概念地标 · 104.3ha":"Low/mid mixed + landmark · 104.3ha",
    "中低层研发街区 · 191.9ha":"Mid/low R&D blocks · 191.9ha",
    "中高层商务集群 · 72.4ha":"Mid/high business cluster · 72.4ha",
    "南北贯通，三核外段为公园绿地":"Continuous N-S; park green outside cores",
    "京张绿廊·公共主轴  135.2 ha":"Jingzhang Corridor · Public Axis 135.2 ha",
    "京张铁路绿廊  ·  AI 数据主脉  ·  公共空间主轴":"Jingzhang Railway Corridor · AI Data Spine · Public Space Axis",
    "中关村科学城":"ZGC Science City", "未来科学城":"Future Science City", "怀柔科学城":"Huairou Science City",
    "北京经开区":"BDA", "鹏城实验室":"Pengcheng Lab",
    "三科学城 + 京津冀创新网络":"Three Science Cities + JJJ Innovation Network",
    "海淀科技创新中心核心区定位":"Haidian S&T innovation core",
    "三核驱动":"3-Core Engine",
    "Concept Section — N-S Skyline（示意性，非建筑方案）":"Concept Section — N-S Skyline (indicative, not architectural)",
    "Implementation Roadmap & Governance（概念性，非投资承诺）":"Implementation Roadmap & Governance (conceptual, not investment commitment)",
    "Land Use Structure — 11.4 km² 无重叠覆盖":"Land Use Structure — 11.4 km² non-overlapping coverage",
    "Site Readiness Analysis — Real Anchors · Conceptual Land ...":"Site Readiness Analysis — Real Anchors · Conceptual Land",
    "AI原生空间类型学  |  AI-Native Spatial Typologies":"AI-Native Spatial Typologies",
    "■ 保留区域（校园/公园/已建成）":"■ Retain (campus/park/built)",
    "■ 待研究区域（虚线）":"■ To study (dashed)",
    "■ 概念可更新区域（待权属调查）":"■ Concept-renewable (pending ownership)",
    "■ 轨道站点":"■ Rail Station", "◆ 铁路车站":"◆ Railway Station", "● 高校/科研院所":"● Univ/Research",
    "留白与弹性":"Resilience & Elasticity", "概念建筑段":"Concept Building Segments",
    "概念建议阶段预留弹性用地":"Reserved flexible land at concept stage",
    "异常 → 一键回滚（空间版本控制：分支测试 → 合并推广 → 回滚）":"Anomaly → one-click rollback (spatial versioning: branch → merge → rollback)",
    "数据权限×物理安全×社区授权，三者缺一不可":"Data permission × physical safety × community authorization, all required",
    "透明审批+监控+应急，市民可旁观可质询":"Transparent approval + monitoring + emergency; citizens observe & query",
    "AI安全/规划/隐私":"AI Safety / Planning / Privacy",
    "场景即建即活":"Scenes live at build-out",
    # 追加：组合串与标记
    "〔测试〕":"〔Test〕", "测试验证":"test verification", "概念建议":"conceptual suggestions",
    "约9 km 铁路绿廊 · 15 处 AI 场景节点":"~9 km Railway Green Corridor · 15 AI Scenario Nodes",
    "AI 场景节点（15 处：4 处测试验证 + 11 处概念建议）":"AI Scenario Nodes (15: 4 test verification + 11 conceptual)",
    "交通 · 蓝绿 · 公共空间":"Mobility · Blue-Green · Public Space",
    "知春路站(10/13号线)":"Zhichunlu Stn (L10/13)",
    "大钟寺站(12/13号线)":"Dazhongsi Stn (L12/13)",
    "五道口站(13号线)":"Wudaokou Stn (L13)",
    "学知园站(昌平线)":"Xuezhiyuan Stn (Changping Line)",
    "清华东路西口(15号线)":"Tsinghua E Rd West (L15)",
    "西直门(2/4/13·全网第一)":"Xizhimen (L2/4/13 · top interchange)",
}

# ── 第二轮补齐：实际未翻译的完整串（来自 _missed_en.txt）──
T.update({
    "京张Railway Green Corridor":"Jingzhang Railway Green Corridor",
    "1909协议从铁路安全——一种经过百年验证的、":"Protocol 1909 starts from railway safety — a century-validated,",
    "物理空间中的、高可靠分布式安全系统——出发，":"high-reliability distributed safety system in physical space — and extends it to",
    "3核":"3 Cores",
    "AI agent持加密凭证":"AI agent holds encrypted token",
    "进入分区，含场景ID":"enters zone with scene ID",
    "权限/有效期/责任主体":"permission / validity / responsible entity",
    "AI原生应用场景政策支持":"Policy support for AI-native application scenarios",
    "LM-01 智脉原点碑":"LM-01 Zhimai Origin Stele",
    "LM-04 全球AI里程碑亭":"LM-04 Global AI Milestone Pavilion",
    "Renovate更新（概念干预示意·非现状判定）":"Renovate (concept intervention indication · not status-quo determination)",
    "Retain（概念干预示意·非现状建筑判定）":"Retain (concept intervention indication · not status-quo building determination)",
    "Site Readiness Analysis — Real Anchors · Conceptual Land Availability · Stakeholders（概念性，待现状测绘与权属调查确认）":"Site Readiness Analysis — Real Anchors · Conceptual Land Availability · Stakeholders (conceptual, pending status survey & ownership confirmation)",
    "★ 提交者概念自评 · SUBMITTER CONCEPT SELF-EVALUATION（非第三方专业评审）":"★ SUBMITTER CONCEPT SELF-EVALUATION (not third-party professional review)",
    "东升大厦·清华科技园":"Dongsheng Tower · Tuspark",
    "200+AI企业":"200+ AI firms",
    "个":"",
    "中坤广场":"Zhongkun Plaza",
    "功能转型":"function transformation",
    "中坤广场·12/13号线":"Zhongkun Plaza · L12/13",
    "AI+消费先导区":"AI+ consumption pilot zone",
    "中期 3-5年":"Mid-term 3-5y",
    "系统成型":"system formation",
    "中科院院所":"CAS institutes",
    "（保留）":"(retain)",
    "五环绿带":"5th Ring greenbelt",
    "衔接节点":"junction node",
    "五道口":"Wudaokou",
    "(13号线)":"(L13)",
    "五道口\n城市更新":"Wudaokou\nurban renewal",
    "六道口":"Liudaokou",
    "(15/昌平线)":"(L15/Changping)",
    "六道口站":"Liudaokou Stn",
    "一体化更新":"integrated renewal",
    "农大·林大":"CAU·BFU",
    "校园（保留）":"campus (retain)",
    "利益相关者：农大·林大·矿大·地大·学知园/六道口站·学院路街道·东升镇·京张遗址公园":"Stakeholders: CAU·BFU·CUMT·CUGB·Xuezhiyuan/Liudaokou·Xueyuan Rd·Dongsheng·Jingzhang Park",
    "利益相关者：北邮·北师大·北交大·铁科院·大钟寺商圈·北京北站·北下关街道":"Stakeholders: BUPT·BNU·BJTU·CARS·Dazhongsi·Beijing North Stn·Beixiaguan",
    "利益相关者：清华·北大·中科院·北航·信通院·东升大厦·200+AI企业·中关村街道·海淀街道":"Stakeholders: Tsinghua·PKU·CAS·Beihang·CAICT·Dongsheng·200+AI firms·ZGC·Haidian",
    "北 ↑":"N ↑",
    "北五环":"North 5th Ring",
    "北交大校园":"BJTU campus",
    "北京北站":"Beijing North Stn",
    "枢纽提升":"hub upgrade",
    "北航周边":"around Beihang",
    "混合功能":"mixed-use",
    "北航校园":"Beihang campus",
    "南 ↓":"S ↓",
    "地大·矿大·林大":"CUGB·CUMT·BFU",
    "农大·北科·北语":"CAU·USTB·BLCU",
    "城市OS基础平台":"Urban OS foundation platform",
    "大钟寺商圈":"Dazhongsi retail district",
    "AI+消费升级":"AI+ consumption upgrade",
    "季度会议+参与式预算":"quarterly meeting + participatory budget",
    "学清路":"Xueqing Rd",
    "轨道微中心":"rail micro-center",
    "学知园":"Xuezhiyuan",
    "(昌平线)":"(Changping Line)",
    "学院路37号":"37 Xueyuan Rd",
    "AI学院·具身智能":"AI School · Embodied AI",
    "拆除New Build（概念干预示意·非现状判定）":"Demolish & Build (concept intervention indication · not status-quo determination)",
    "数据权限 + 物理安全":"Data permission + physical safety",
    "+ 社区授权 三者联锁":"+ community authorization, three interlocked",
    "任一不满足则禁止":"any unmet = prohibited",
    "明确边界/时段/配额":"clear boundary / time / quota",
    "分区内自主运行":"autonomous within zone",
    "故障不波及他区":"faults don't spread to other zones",
    "智能商务":"Smart Business",
    "概念干预类型示意":"Conceptual Intervention Type Indication",
    "注：本图为【提交者概念自评】，非第三方专业评审。评分为概念性对照（1-5分），基于公开资料整理；评分规则：1=基础缺失 2=有概念无落地 3=有策略待验证 4=有落地路径和KPI 5=有实施机制和验证框架；全球案例数据来自公开报道，可能存在统计口径差异，逐项评分规则与证据附表见 proposal.md 正文。空间指标依据 GeoJSON 在 EPSG:4548 投影下复算。所有空间建议均为概念方案，不构成政府审定结论。":"Note: this figure is a [submitter conceptual self-evaluation], not a third-party professional review. Scores are conceptual comparison (1-5), compiled from public sources; rules: 1=foundation missing 2=concept only 3=strategy pending verification 4=landing path & KPIs 5=implementation mechanism & verification framework; global case data from public reports may differ in statistical caliber. Spatial metrics recomputed in EPSG:4548. All spatial recommendations are conceptual and not government-approved conclusions.",
    "活动：设计马拉松/公民数据/学生编程/老人AI教学":"Activities: design marathon / civic data / student coding / elder AI tutoring",
    "清华校园":"Tsinghua campus",
    "知春路":"Zhichunlu",
    "(10/13·31万/日)":"(L10/13 · 310k/day)",
    "知春路\n楼宇升级":"Zhichunlu\nbuilding upgrade",
    "矿大·地大":"CUMT·CUGB",
    "社区分红机制":"community dividend mechanism",
    "类":"",
    "绿=运行  黄=测试":"Green=running  Yellow=test",
    "红=人工  蓝=维护":"Red=manual  Blue=maintenance",
    "状态市民可见":"status visible to citizens",
    "西直门":"Xizhimen",
    "(2/4/13·全网第一)":"(L2/4/13 · top interchange)",
    "近期 1-3年":"Near-term 1-3y",
    "示范启动":"pilot launch",
    "远期 5-10年":"Long-term 5-10y",
    "生态成熟":"ecosystem maturity",
    "透明人在回路审批台":"Transparent human-in-the-loop desk",
    "AI提议→人类决策":"AI proposes → human decides",
    "市民可旁观质询":"citizens observe & query",
    "重新定义AI与城市空间的交互规则。":"Redefine the interaction rules between AI and urban space.",
    "不是技术堆栈，而是空间-数字混合的":"Not a tech stack, but a spatial-digital hybrid",
    "安全制度，可被其他城市复用。":"safety institution, reusable by other cities.",
    "锚机构落地：1-2家头部AI企业/国家实验室作为首发锚租户":"Anchor landing: 1-2 leading AI firms / national labs as first anchor tenants",
    "处":"",
    "栋":"",
})

def tr(s):
    if s is None:
        return s
    s = str(s)
    # 最长优先子串替换，处理嵌入在 f-string 中的中文（如 "SC-14 金融合规"）
    for k in _KEYS:
        if k and k in s:
            s = s.replace(k, T[k])
    return s

_KEYS = sorted([k for k in T.keys()], key=len, reverse=True)

# ── master monkey-patch: catch ALL text via Text.set_text (covers ax.text,
#    fig.text, set_title, set_xlabel, set_ylabel, set_yticklabels, set_xticklabels,
#    annotate, suptitle, legend labels, etc.) ──
import matplotlib.text as _mtext
_MISSED = set()
def _tr_text(self, s, *a, **kw):
    if isinstance(s, str) and s:
        t = tr(s)
        if any('\u4e00' <= c <= '\u9fff' for c in t):
            _MISSED.add(s)
        s = t
    return _orig_set_text(self, s, *a, **kw)
_orig_set_text = _mtext.Text.set_text
_mtext.Text.set_text = _tr_text

# keep explicit patches too (harmless, helps Patch/Line2D label before render)
_orig_patch_init = mpatches.Patch.__init__
def _patched_patch_init(self, *a, **kw):
    if "label" in kw and isinstance(kw["label"], str):
        kw["label"] = tr(kw["label"])
    _orig_patch_init(self, *a, **kw)
mpatches.Patch.__init__ = _patched_patch_init

_orig_line_init = mlines.Line2D.__init__
def _patched_line_init(self, *a, **kw):
    if "label" in kw and isinstance(kw["label"], str):
        kw["label"] = tr(kw["label"])
    _orig_line_init(self, *a, **kw)
mlines.Line2D.__init__ = _patched_line_init

# ── savefig 重定向到 .en.png ──
_name_map = {
    "site-overview": "site-overview.en.png",
    "land-use-structure": "land-use-structure.en.png",
    "key-areas": "key-areas.en.png",
    "mobility-bluegreen": "mobility-bluegreen.en.png",
    "metrics-evidence": "metrics-evidence.en.png",
    "concept-section": "concept-section.en.png",
    "implementation-roadmap": "implementation-roadmap.en.png",
    "site-readiness": "site-readiness.en.png",
    "ai-typologies": "ai-typologies.en.png",
    "protocol-1909": "protocol-1909.en.png",
}
_orig_savefig = plt.Figure.savefig
def _patched_savefig(self, fname, *a, **kw):
    fn = str(fname)
    for base, en in _name_map.items():
        if base in fn:
            fn = str(g.FIG_DIR / en)
            break
    return _orig_savefig(self, fn, *a, **kw)
plt.Figure.savefig = _patched_savefig

# ── 生成全部 EN 图件 ──
for name, fn in [
    ("site-overview", g.fig_site_overview),
    ("land-use-structure", g.fig_land_use),
    ("key-areas", g.fig_key_areas),
    ("mobility-bluegreen", g.fig_mobility),
    ("metrics-evidence", g.fig_metrics),
    ("concept-section", g.fig_section),
    ("implementation-roadmap", g.fig_roadmap),
    ("site-readiness", g.fig_site_readiness),
    ("ai-typologies", g.fig_ai_typologies),
    ("protocol-1909", g.fig_protocol_1909),
]:
    try:
        fn()
        print(f"OK  {name}.en.png")
    except Exception as e:
        print(f"ERR {name}.en.png: {e}")
print("ALL EN DONE")

# ── dump untranslated strings for iteration ──
if _MISSED:
    with open(SCRIPTS / "_missed_en.txt", "w", encoding="utf-8") as fh:
        for s in sorted(_MISSED):
            fh.write(s + "\n")
    print(f"MISSED {len(_MISSED)} untranslated strings -> _missed_en.txt")
else:
    print("MISSED 0 — fully translated")
