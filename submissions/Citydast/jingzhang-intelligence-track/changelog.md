# 方案迭代记录

## v0.1 - 2026-08-08

- 建立 blobless 稀疏参与者工作区并同步 `main`。
- 阅读站点包（design_brief、agent_taskbook、allowed_design_space、sources、planning_limits、standards、provisional boundaries）与公开来源注册表。
- 确立总体概念「京张智轨（Jing-Zhang Intelligence Track）」：从百年钢轨到智能轨迹，形成「一带三核、多点场景、蓝绿智环」空间组织。
- 生成正式提交包骨架并替换全部模板内容：
  - `proposal.md`：13 章专业方案，覆盖公告 1.3/1.4/1.5 与 agent.1—agent.6，含证据引用、场景卡、画像、朝圣地标、文化叙事与运营体系。
  - 9 个 GeoJSON 图层（拓扑正确：land_use 全覆盖无重叠，指标可复算）。
  - `metrics.json`：12 个 known + 2 个 unknown（待补控规条件）。
  - 5 张演示级图、`visual/index.html` 离线可视化、A3 文册（4 页）与 A0 展板（2 页）。
  - 矩阵：compliance（23 项任务）、standard（6 项标准）、design_depth（15 项深度）。
- 运行 finalize、self_check 与 participant_preflight 至 PASS（见 self_check.json）。
- 已知限制：官方边界/控规/道路红线/权属/市政/文保待正式资料发布后重算；`floor_area_ratio`、`building_height_m` 为 unknown。

## v0.1.1 - 2026-08-08

- 新增 10 张结构化 AI 场景卡（proposal.md 场景章节内嵌结构化表格，字段对齐 `schema/scenario.schema.json`），
  含 3 张 AI 产业测试验证场景（jzit-card-02 安全治理沙盒、jzit-card-03 端侧算力驿站、jzit-card-10 城市智能体沙盒）；
  按任务书 agent.3「场景-空间-运营映射」要求逐卡登记空间位置、服务对象、数据来源、公共价值、风险点与人工复核。
  注：投稿包白名单不允许 scenarios/ 目录，结构化场景卡以表格形式落在 proposal.md 内，属合规落位。
- 场景卡重编号：卡10 由「全球 AI 活动周路线」调整为「城市智能体沙盒」；「全球 AI 活动周路线」归入年度活动与运营体系（agent.6），
  修复原稿「10 张枚举 + 额外沙盒」的计数不一致，保持 10 卡 / 3 测试验证与 metrics.json 一致。
- 合规矩阵差异化：为 agent.1—agent.6 与 1.5.2.3/1.5.2.4/1.5.2.5/1.5.3.x 补充任务专属章节/图层/指标证据，
  其余任务保持通用引用，任务覆盖 23 项不变。
- 字段统一：manifest.json 与 agent.json 的 agent_name / model 统一。
- metrics.json：scenario_card_count 来源更新为 proposal.md 结构化场景卡表。
- 术语核对：proposal.en.md 关键术语与赛事术语表保持一致。
- 已知限制：build_jzit_*.py 生成脚本尚未同步本次结构化场景卡与矩阵差异化内容，
  重新运行生成脚本将覆盖本版本手改内容，需在后续迭代中并入生成脚本。

## v0.2 - 2026-08-23

- 结合规划专家意见与官方最新发布优化方案（新增来源均已登记 sources.json，共 6 条）：
  - 引入「城市有机生命体」理论锚点，把百年钢轨转译为城市「动脉」、蓝绿智环为「生态脉动+智能神经」（吴志强院士、国家发改委）
  - 注入 2026 中关村论坛官方数据：9 公里创新廊道、AI 核心产业超 3500 亿元（约全国三成）、近 2000 家 AI 企业、30 余家高能级平台
  - 具身智能场景对接小月河翼具身智能产业园，纳入机器人配送/巡检/零售低速试点
  - 「算力网=继水网、电网、通信网后的新一代城市基础设施」概念落地到端侧算力驿站与分布式能源节点
  - 引用京张铁路遗址公园二期落地案例（约 9 公里绿廊贯通、清河连通、鱼骨状慢行道）支撑慢行缝合策略
  - 大钟寺铁路工业遗产活化清单（折返段转盘剧场、焊轨厂运动公园、冷库美术馆、路演厅）
  - 「从为人规划转向与人共同规划」开源共建运营机制（呼应海淀政策+技术+生态模式）
  - AI 公共服务「服务找人」主动服务模式（发改委城市智能体建议）
  - 「感知—数据—计算—明律—应用」城市智慧链条的空间映射
  - 指标颗粒度呼应 AIQ 地块街坊级评价趋势
- proposal.en.md 大模型重译同步（对照赛事术语表）
- 重渲染 report/proposal.html 与 proposal.en.html；manifest sha256 刷新

## v0.3 - 2026-08-24

- 针对评审 66 分（intake）补强可实施性、公共利益与风险合规维度：
  - 实施路径 KPI 表：6 更新项目各配概念 KPI（指标/基准口径/目标/责任主体/评估周期），基准值待官方数据校准
  - 公共利益与包容性矩阵：居民/青年人才/企业/高校师生/游客/弱势群体 × 空间举措 × 公共价值 × 包容性设计 × 数据边界
  - 新建 risk.json 风险应答矩阵：8 维（数据隐私/实施复杂度/公众接受度/运维成本/政策不确定性/空间争议/技术成熟度/公平包容性）1-5 分 + 缓解措施 + 人工复核
  - 风险章节回链 risk.json；「AI 治理全球话语权」落实到安全治理沙盒/标准工作坊/模型评测赛
- proposal.en.md 大模型重译同步；manifest 登记 risk.json；validate/self_check PASS

## v0.4 - 2026-08-24

- 电子展示页 visual/index.html 全面重写（图文并茂版）：
  - 封面底图：纯 SVG 原创插画（钢轨人字形展线+AI 节点+数据流+城市剪影+点阵）
  - 新增可视化：9 公里廊道 KPI 条、三层范围面积比例 SVG、三区两翼九宫格、用地分区堆叠条
  - 新增专家叙事（自然融入）：感知-数据-计算-明律-应用 城市智慧链条（5 节点映射）、算力网=第五张网
  - 风险雷达 8 维 SVG、合规矩阵 4 卡进度条
  - 6 更新项目三期时间线、公共利益矩阵表
  - 数据-metric 完整保留（CI 校验要求）
- visual/index.en.html 大模型完整翻译（56K，仅 1 处品牌对照保留中英）
- 离线无远程依赖；validate/self_check PASS（formal-review-ready）

## v0.5 - 2026-08-24

- 针对 v0.4 评审（71 分，request-changes）五项短板整改：
  - 来源注册合规：6 条 2026 新增来源标 review_status=needs_review（仅背景支撑），
    发起 [source-registry] Issue #3905 申请中央正式登记，正文措辞降级
  - 区域协同补强：新增与北纬社区/未来科学城/怀柔科学城/北京经开区/京津冀的五组协同机制
    （策源-中试接力、算力数据要素走廊、具身智能互补、服务-场景双向接口、标准输出+场景回填）
  - KPI 落地化：6 项目 KPI 表扩展为 10 列（数据口径/基线来源/成本级别/决策门 Go/No-Go/退出条件）
  - 公共利益可测试化：矩阵新增可测试指标列 + 四承诺（无障碍指标/传统渠道保留/参与式设计/投诉补救 48h）
  - 公共空间组件库目录化（agent.4）：5 类组件×规格×应用节点 + Logo 三型定稿候选（A展线标/B智轨环/C百年钢印）
- proposal.en.md 大模型翻译同步；validate/self_check PASS

## v0.6 - 2026-08-24

- 针对 v0.5 评审（81 分，request-changes）五项硬骨头整改：
  - 中文字体栈：visual/index.html 的 4 处 svg font-family 由 ui-sans-serif 改为
    PingFang SC/Microsoft YaHei/Noto Sans CJK SC 全栈；CSS 兜底 svg text 字体
  - 图片排版：land-use-structure 底部"用地分区"信息并入 figure_shell note 参数（消除重叠）；
    key-areas 警示文字拆两行（消除右侧截断）；A0 板 1 标题拆两行（消除右侧裁切），
    命名/Logo 文字下移避开大钟寺色块；A0 板 2 同步拆两行、卡片下移
  - 视觉页来源状态：visual/index.html 与 en.html 9 KM CORRIDOR 区域顶部新增 notebox，
    显式标注 3500 亿/2000 家/30+ 平台/具体企业/9 公里最高 AI 浓度等数据为
    review_status=needs_review、Issue #3905 申请中央登记
  - 全球案例证据表：proposal.md/EN 新增 7 案逐案表（来源等级/许可边界/可迁移机制/
    场地适配/不可类推），附使用规则（概念参考、不可独立核验为正式事实）
  - Logo 定稿级原型：PIL 生成 assets/figures/logo-prototypes.png（3×3 网格，
    A 展线标/B 智轨环/C 百年钢印 × 主版本含跨语言/小尺寸 16-72 px/浅中深背景适配），
    proposal.md/EN 补"原型测试证据+建议规范+禁用场景"段落；visual/index.html 与
    EN 末尾新增 LOGO PROTOTYPES 区块引用 PNG 证据图
- KPI 量化+责任主体真实化：KPI 表后补量化目标+真实授权对应表（贯通率/服务点/
  转化项目/无障碍覆盖率/PUE/活动场次/开发者数/国际触达国数等均给量化值）
- 同步修复 build_jzit_visuals.py 的 SUBMISSION 路径（workbuddy-agent → Citydast）
  与三处布局 bug
- proposal.en.md 大模型翻译同步
- validate/self_check PASS（formal-review-ready）
- 不提交、不推送；待与用户沟通后定夺

### v0.6 增项 (sprint 2) - 2026-08-24
- 9 公里数据措辞微调：proposal/EN 中"AI 浓度最高的 9 公里"改"约 9 公里（公开报道口径，待官方数据校准）"
- Logo 原型图重画（H=1300 增大画布）：建议规范文字移出第三行 panel 之外
- A0 板 2 逐字段排版复核：AI 场景行 30px→26px + 缩短文字，消除右侧裁切；A3/A0 重生成
- 新增「智能体沙盒安全测试机制」段落（proposal/EN）：5 项机制（分级/安全评估/人工复核/退出条件/表述边界）
- risk.json 扩展第 9 维「AI 治理全球话语权」(score 3)：proposal 风险章节 + visual 雷达色块同步
- 9 项 detailed required repairs checklist 比对报告：F:\workbuddy\城市设计竞赛\workspace\checklist_v06.md
