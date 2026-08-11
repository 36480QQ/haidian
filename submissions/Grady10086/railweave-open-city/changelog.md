# 方案迭代记录

## v2.1 - 2026-08-12

### 从专业方案包到可失败关闭的研究接口 / From professional package to a fail-closed research interface

相对 v2.0，本轮深化不改变“开放共创概念建议”的法律和事实状态，也不声称政府批准、项目立项、预算落实、采购结果、合作关系、投资承诺或工程可行。新增成果用于提高空间可读性、实施交接和协议可复核性；正式边界、权属、现状、专业条件、责任主体和真实绩效仍待依法核验。

Relative to v2.0, this revision does not change the package's status as an open-co-creation conceptual recommendation. It does not claim government approval, project establishment, secured budget, procurement outcome, partnership, investment commitment, or engineering feasibility. New artifacts improve spatial legibility, implementation handover, and protocol reviewability. Official boundaries, site rights, baseline conditions, professional constraints, accountable entities, and real performance remain subject to lawful verification.

### 1. 空间与专业表达 / Spatial and professional expression

- 新增总体设计、众智园、AI 原点、大钟寺、典型剖面、AI 服务蓝图、品牌与地标、实施台账、公共价值治理和证据缺口等中英文图件；所有工作范围和功能组件继续标为临时、概念或待核验。
- 新增无障碍节点、核查线段、设计组件、分期组件和剖面线等研究性 GeoJSON，用于交接设计意图和现场核查任务，不作为官方红线、产权、建筑、道路或工程依据。
- 重建中英文 HTML、A3 文册和 A0 展板的表达层，使图、表和说明在双语版本中对应；本项只改善交付完整性，不提高资料的法定等级。

- Added bilingual figures for the overall design, Zhongzhiyuan, AI Origin, Dazhongsi, typical sections, AI service blueprints, identity and landmarks, implementation register, public-value governance, and the evidence-gap atlas. Working extents and functional components remain labelled as provisional, conceptual, or pending verification.
- Added research GeoJSON for accessibility nodes, audit segments, design components, phasing components, and section lines. These hand over design intent and field-audit tasks; they are not official redlines or evidence for ownership, buildings, roads, or engineering.
- Rebuilt the Chinese and English HTML, A3 booklets, and A0 boards so figures, tables, and notes correspond across languages. This improves delivery completeness only and does not elevate the statutory status of the evidence.

### 2. 场景与实施交接 / Scenario and implementation handover

- 新增 `visual/assets/scenario_prototypes.json`，将 S01、S06 和 S11 深化为可供专业团队研究的端—边—平台—人工复核原型；原型不表示场地、数据、设备、预算、采购、运营主体或审批已经落实。
- 新增 `visual/assets/implementation_register.json`，把 AI 原点需求协同室、众智园独立测试验证实验室和大钟寺首用转化与运营池写成带进入、验收、停止、退出和全寿命成本边界的概念项目登记。
- S06 增加 0—30 日无 AI 基线、31—60 日封闭合成与影子验证、61—90 日有条件限量共测的时间切片；任何阶段均不自动扩展。
- S06 增加 10%—15% 概念退出准备金控制带，覆盖接口停用、数据清理、导视校正、人工服务恢复、设备撤离、场地修复和独立退出复核。该范围不是报价、预算批复、采购条件、资金来源或拨款承诺。

- Added `visual/assets/scenario_prototypes.json`, developing S01, S06, and S11 as endpoint–edge–platform–human-review prototypes for further professional study. The prototypes do not indicate secured sites, data, equipment, budgets, procurement, operators, or approvals.
- Added `visual/assets/implementation_register.json`, recording the AI Origin Demand Coordination Room, Zhongzhiyuan Independent Testing and Validation Laboratory, and Dazhongsi First-Use Conversion and Operations Pool as conceptual projects with admission, acceptance, stop, exit, and whole-life-cost boundaries.
- Added an S06 time slice: a non-AI baseline on Days 0–30, closed synthetic and shadow validation on Days 31–60, and conditionally authorised limited co-testing on Days 61–90. No stage expands automatically.
- Added a conceptual 10–15% exit-reserve control band for S06 covering interface shutdown, data clearance, sign correction, restoration of staffed service, equipment removal, site repair, and independent exit review. It is not a quotation, approved budget, procurement condition, funding source, or funding commitment.

### 3. RailWeave 织入契约与合成回归 / RailWeave weave contracts and synthetic regression

- 新增 `visual/assets/weave_contracts.json`，为 S01—S12 分别登记公共问题、经线保障、纬线接入、结点责任、数据禁区、人工复核、普通服务等价、解编触发和残留维护物。
- 新增不能互相替代的“织体成熟门”和“线程准入门”：前者审查空间、权利、专业、人员资源和恢复能力；后者审查单项 AI 服务的公共目的、数据、人审、等价服务与解编条件。进入现场须同时通过两门。
- 新增无第三方依赖的 `visual/assets/railweave_runner.js`、72 个显式合成案例和输入哈希 receipt。每个场景包含正常、缺人工、缺普通后备、数据越界、责任漂移和解编失败六个分支。
- 当前合成 receipt 记录 12 个正常分支通过、60 个缺陷分支全部阻断，共 1498/1498 条结构与用例断言通过。PASS 只证明这些合成输入上的协议逻辑，不证明现场绩效、合规、安全、无障碍、资金、采购或实施。

- Added `visual/assets/weave_contracts.json`, recording the public problem, warp safeguard, weft connection, node responsibility, prohibited data, human review, ordinary-service equivalence, unweaving trigger, and maintained residual for each of S01–S12.
- Added two gates that cannot substitute for each other. The Fabric Maturity Gate reviews space, rights, professional conditions, staffing resources, and restoration capability. The Thread Admission Gate reviews the public purpose, data, human review, equivalent service, and unweaving conditions of one AI service. Both are required before field entry.
- Added the dependency-free `visual/assets/railweave_runner.js`, 72 explicit synthetic cases, and an input-hashed receipt. Every scenario includes normal, missing-human, missing-ordinary-fallback, prohibited-data, responsibility-drift, and failed-unweaving branches.
- The current synthetic receipt records 12 normal branches passing and all 60 defective branches blocked, with 1,498/1,498 structural and case assertions passing. PASS proves protocol logic for these synthetic inputs only; it does not prove field performance, compliance, safety, accessibility, funding, procurement, or implementation.

### 4. 多模态、版权与双语叙事 / Multimodal, rights, and bilingual narrative

- 新增众智园、AI 原点和大钟寺三张 AI 生成概念图的 WebP 提交版本，并以本地编排形成封面和中英文短视频材料；生成图只解释空间体验，不作为现状、场地、建筑、工程、投资或建成效果证据。
- `report/copyright_statement.md` 逐字登记三次实际生成提示词，说明未向生成工具输入第三方受保护视觉素材，并记录 AI 生成性质、文件、衍生处理、禁止用途、OSM ODbL 和 CC BY 4.0 的适用边界。
- 新增本中英文对应的评审叙事简报，集中说明 RailWeave、两套独立门、S06 90 日切片、10%—15% 概念退出准备金和 72 个合成分支的证据上限。

- Added submitted WebP versions of three AI-generated concept images for Zhongzhiyuan, AI Origin, and Dazhongsi, with local composition into a cover and bilingual short-video materials. Generated imagery explains spatial experience only and is not evidence of current conditions, sites, buildings, engineering, investment, or built outcomes.
- Updated `report/copyright_statement.md` with verbatim copies of the three actual generation prompts, confirmation that no third-party protected visual material was supplied to the generator, and records of synthetic status, files, derivation, prohibited uses, OSM ODbL, and the scope of CC BY 4.0.
- Added corresponding Chinese and English review narrative briefs covering RailWeave, the two independent gates, the S06 90-day slice, the conceptual 10–15% exit reserve, and the evidence ceiling of the 72 synthetic branches.

### 5. 仍未改变的边界 / Boundaries unchanged

- 临时工作几何不构成官方边界、法定规划、产权、控规指标、拆改留、工程线位或精确面积依据。
- 合成测试不构成现场试验、公众同意、法律合规、专业验收、采购决定或政府背书。
- 项目名、机构类型、角色、阶段、活动、成本控制带和合作接口均为研究建议，须在有权主体、公众和专业团队参与下另行确认。

- Provisional working geometry is not an official boundary or evidence for statutory planning, ownership, development controls, retain–renovate–demolish decisions, engineering alignment, or precise area.
- Synthetic tests are not field trials, public consent, legal compliance, professional acceptance, procurement decisions, or government endorsement.
- Project names, institution types, roles, phases, events, cost-control bands, and partnership interfaces remain research proposals to be confirmed separately with authorised entities, affected publics, and professional teams.
