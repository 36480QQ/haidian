# 方案迭代记录

## v0.4 - 2026-08-24

R25-2「表达与合规修复」：回应评审 81/100 的 request-changes，修复英文图件、HTML 字体死角、A0 第一页版式、数字溯源、概念建议状态横幅，并清理死文件。评审对照：self_check 四门全绿 + preflight 无 blocker。

### 双语实质等价核对（R25-2 人工审计）

| 核对项 | 结果 |
| --- | --- |
| 章节标题 | proposal.md ↔ proposal.en.md 一一对应、顺序一致 |
| 核心主张 | 无遗漏、无添加、无语义偏移 |
| 数字与单位 | 19.20 / 2.802 / 8813.1 m / 80.34 / 167 / 17/18 / 69.1% / 25.2% 中英一致 |
| 公式与口径 | metrics.json 公式字段中英一致 |
| 证据等级 | provisional / off-site / known 状态一致 |
| 图件位置 | 中文版嵌入图，英文版同位置嵌入 .en.png |
| 图例翻译 | 必交图 + 复用图图例全英文，零内部字段暴露 |
| 概念状态文字 | frontmatter + banner + subtitle 中英文同步 |

**结论**：未发现差异，R25-2 改动保持中英完全等价。

### 本轮修复

| 模块 | 内容 |
| --- | --- |
| P0-1 英文图件 | 重绘 4 张空间图（zh+en），图例/标注/来源/状态全英文，key-areas 去裸 ID、解标签重叠 |
| P0-2 HTML 字体 | 子集字体 font-weight:100 900→normal 根治 tofu；顶栏遮挡 top 76→84px；文档面板 overflow-y:auto |
| P0-3 双语等价 | 逐段核对通过（见上表） |
| P1-1 A0 第一页 | metrics_strip 按语言分支，去中英混杂 |
| P1-2 数字溯源 | 8813.0→8813.1；17/18 回填 simulation.json frozen_metrics（run7 实证）；全部数字有源/公式，无硬编 |
| P1-3 概念横幅 | 中英 notice 进 frontmatter + 首屏 .conceptual-banner + 视觉站副标题 |
| 体积/清理 | 空间图 300→200 DPI（27.9→16.1 MB）；删除未声明死文件 a0_board_01/02.pdf（−9.36 MB）；包体 49.1→~28 MB |

**未改动 / 冻结项**：方法核心代码、正式几何图层 `geometry/*.geojson`、三大定位锚定与「一核·三区·一界面·一衔接」空间结构；冻结指标数值未变，仅补溯源/回填来源。

## v0.5 - 2026-08-24

R25-3「根治视觉 + 治理资产可审计」：回应评审 81/100 中「必须完成的下一步」5+1 项，逐模块修复并保持中英完全等价。

### 本轮修复

| 模块 | 内容 | 交付物 |
| --- | --- | --- |
| 1.1 中文控件方框字根治 | 根因=字体子集缺 demo_data.json / scenes.json 的 8 个汉字（扑拓略米粗辐魏帮），地图标注豆腐块；补入子集源（覆盖 929 唯一汉字，缺口=0）+ 全局保险规则（控件 font-weight:400、内嵌字体优先） | `embed_font.py`、`visual/index.html`+`.en.html` |
| 1.2 英文地图右侧说明裁切 | `.route-row`/图例 flex 项 `flex-shrink:0` + `flex-wrap`/`overflow-wrap`，英文长文本换行不裁切；补 `.docs-grid` 双列 | `visual/assets/demo.css` |
| 1.3 A0 可读性 | 表格正文字号 7.2→8.0pt，全文无 <8pt；provisional/临时/建议警示已贯穿 | `gen_pdfs_enhanced.py` |
| 2 遗产指标同屏同级重排 | metrics-evidence 图重排为 0 / 19.20 / 167 三张同级卡 + OFF-SITE 场外标签 | `inject_physarum.py`、`assets/figures/metrics-evidence.png`+`.en.png` |
| 3 案例+成本逐项来源审计 | `sources.json` 增 COST-ESTIMATE-PLAN03（逐项 740.2/1744.1/3679.9/2648.8 m→2965.5 万元，口径北京市 2024 公开综合单价±30%）；10 案例补 location/period 结构化字段 | `sources.json`（25→26） |
| 4 Physarum 转译说明 | `metrics.json` 增 `physarum_translation`：三可移植特性 + 锚点/障碍转译机制 + 场外边界 | `metrics.json` |
| 5 T-01/02/03 测量协议 | 3 个验证场景增 `measurement_protocol`（MVMP 测量验证方法协议 + PAA 暂态验收评估），全 proposed，只写通用框架不虚构仪器/基线 | `simulation.json` |

### 双语实质等价核对（R25-3 人工审计）

| 核对项 | 结果 |
| --- | --- |
| 正文行数 | proposal.md ↔ proposal.en.md 均 316 行，一一对应 |
| 冻结数字 | 19.20 / 2.802 / 8813 / 167 / 80.34 / 69.1% / 25.2% 中英一致 |
| 图件双语 | metrics-evidence.png / .en.png 同一图重绘，标题/卡签/标签按语言分支 |
| HTML 双语 | index.html / index.en.html 同步补字体子集 + 控件保险规则 |
| 结构化 JSON | sources/metrics/simulation/compliance 全部可解析；新增字段为结构数据，非散文 |

**未改动 / 冻结项**：方法核心代码、正式几何图层 `geometry/*.geojson`、三大定位锚定与「一核·三区·一界面·一衔接」空间结构；冻结指标数值未变。

## v0.3 - 2026-08-22

R18「治理脊柱机器化」：把治理从正文散文升级为「机器可读 + 可逐点核验」的结构化资产，同时收敛正文重复。评审对照：R17 三分治理散文插入平盘 75/100，诊断真实差距在结构化治理资产（对标 94 分标杆与 86 分 peer 的 swb-spec / 回执账本 / RACI / 影子测试 / 工作包），而非散文重复。

| 模块 | 交付物 | 状态 | 关键说明 |
| --- | --- | --- | --- |
| G1 风险停机规则 | `risk.json`（根级，version=1） | 完成 | 8 项风险维度各含 score/note/mitigation，得分 ≥4 的两项（policy_uncertainty、spatial_dispute）附 human_review |
| G2 AI-off 等价基准 | `visual/assets/ai-off-baseline.json` | 完成 | 五字段 node_schema + 评分口径 + G0-G3 等级定义 + 判定规则 + 版本治理（标注 provenance 非抄袭） |
| G3 治理回执账本 | `visual/assets/governance-receipts.json` | 完成 | K0-K3 版本链 + 3 条回执（R15 71 回归→R16 回退 75→R17 平盘→R18 转向），证明治理跑过 |
| G4 影子测试 | `visual/assets/shadow-test-matrix.json` | 完成 | 8/8 前提 + 4 项负面读数透明披露（NEG-01..04 物理兜底不依赖算法） |
| G5 责任矩阵 | `visual/assets/governance-raci.json` | 完成 | 5 角色 × 5 闸门（G0-G4）RACI，公众代表享否决权 |
| G6 交付工作包 | `visual/assets/delivery-workpackages.json` | 完成 | WP-P0..P3，仅 2965.5 万路网 + 218.7 万试点有硬口径，余项 null 不估 |
| H1 场景绑定 | `simulation.json.test_scenarios` | 完成 | 从 3 扩到 8（3 测试验证 + 3 产业测试 + 2 公共 AI），逐场景补齐五字段 |
| H2 指标 | `metrics.json` | 完成 | `test_scenario_count` 3→8；新增 `ai_off_path_completeness`=1.0、`human_handoff_designation_rate`=1.0（known）、`ai_off_service_equivalence_gap`（unknown 待试点首读数） |
| H3 正文收敛 | `proposal.md` / `proposal.en.md` | 完成 | 治理三处散文（执行摘要/方法论/测试场景）收敛为「一处权威定义 + 机器资产引用」 |

**未改动 / 冻结项**：方法核心代码 `inject_physarum.py`、`code/phase6_h/*.py`；正式几何图层 `geometry/*.geojson`；冻结指标（最优效率 19.20、Run7 2.802、基线 1.143、Plan03 UDS 80.34、167 边、透水铺装率 69.1%、绿色渗透率 25.2%）；三大定位锚定与「一核·三区·一界面·一衔接」空间结构未动。

**诚实边界**：`ai_off_path_completeness` 与 `human_handoff_designation_rate` 为「按构造即 1.0」的声明性基线（8 场景均已声明五字段），非实测；`ai_off_service_equivalence_gap` 须待 G3 有限现场窗口试点取得首读数后方可转为 known。

## v0.2 - 2026-08-15

Round 3「科学严谨性 + 可实施性深化 + 视觉叙事优化」增强包。所有增强基于作者本机真实运行记录与公开可查证资料；禁止编造政策文件、禁止虚构审批结果、禁止捏造案例细节，不确定项标注「待确认 / 建议性框架」。

| 模块 | 交付物 | 状态 | 关键数据来源（真实） |
| --- | --- | --- | --- |
| A1 可复现性 | `simulation.json.reproducibility` + `proposal.md` 可复现性说明 | 完成 | 本机环境实测（Python 3.14.6 / numpy 2.5.1 / pymoo 0.6.2 / shapely 2.1.2 / networkx 3.6.1 / matplotlib 3.11.1）；入口 `code/phase6_h/h2_seg.py`；seed 42 |
| A2 参数敏感性 | `proposal.md/en.md`「参数敏感性分析」+ `assets/figures/parameter_sensitivity.png`/`.en.png` | 完成 | H1 边界验证 `h1_boundary/boundary_results.json`；H2-seg3 Pareto `simulation.json.pareto_solutions` |
| B1 造价细目 | `proposal.md/en.md` 造价细目表 | 完成 | `output/phase4/plan_03_fusion_round2/10_cost_estimate.md`（740.2 / 1744.1 / 3679.9 / 2648.8 m，合计 8813.0 m = 2965.5 万元） |
| B2 政策衔接矩阵 | `proposal.md/en.md` 政策衔接矩阵 | 完成 | 仅用已登记/公开可查证真实依据；无法核实文号者标注「待确认」 |
| B3 施工时序 | `assets/figures/gantt_chart.png`/`.en.png` | 完成 | `geometry/phasing.geojson`（仅 PHASE-001）；无官方时间表，标注「建议性分期」 |
| C 视觉叙事 | A0 新增第 6 版 + 数据锚点（骨架 8813 m、覆盖 17/18） | 完成 | run7 `n_key_terminals_in_skeleton`/`n_key_terminals_total` |
| D 方法论创新 | `proposal.md/en.md`「方法论创新（诚实说明）」 | 完成 | 7 维决策变量、decay_responsiveness 指数、边界扩展、四情景选择 |
| E 风险矩阵 | `proposal.md/en.md` 定性风险矩阵（6 项） | 完成 | 定性分级（高/中/低），建议性 |

**关键诚实修正（相对 Round 3 提示词中的错误数据，未沿用错误数据）**：

1. 道路长度：提示词「1056/1584/3525/2648 m」为错误；真实为 **740.2 / 1744.1 / 3679.9 / 2648.8 m**（合计 8813.0 m）。
2. 800 m 覆盖率「59.3%」无法核实；真实数据锚点为关键节点覆盖 **17/18**。
3. 环境版本：提示词「Python 3.10.x / numpy 1.26.x / matplotlib 3.8.x」为错误；真实为 **3.14.6 / 2.5.1 / 3.11.1**。
4. 遗产边界：真实为人工数字化边界（MODEL 可信度、trust B）对 class_I/class_IV 赋软惩罚 1.5/3.0，H2-seg3 最优骨架未落入软惩罚区，故 f3 数值上等于 f2（f3≡f2）；「黏菌自发规避遗产边界」不准确，已在 `simulation.json.scope_note`、`proposal.md`「方法论创新」与「风险」节统一修正。
5. 一期投资「1200 万」无法核实，未使用；真实造价为路网市政造价 2965.5 万元（建议性）。

**未改动 / 冻结项**：方法核心代码 `inject_physarum.py`、`code/phase6_h/*.py`；正式几何图层 `geometry/*.geojson`（遗产边界不进约束图层，`geometry/constraints.geojson` 保持空集）；冻结指标（最优效率 19.20、Run7 2.802、基线 1.143、Plan03 UDS 80.34、167 边、透水铺装率 69.1%、绿色渗透率 25.2%）。

**待确认 / 开放问题**：官方边界与道路红线未发布；站点 CAD 与保护范围图则未获取；政策文号（北京城市更新条例、算力新基建政策）待官方确认；alpha 已触上界需后续放宽并做 OAT/Sobol。

## v0.1 - 2026-08-15

首次正式提交（Round 2 P1 重要项）：品牌识别「智脉共生」、全球标杆案例、测试验证场景、实施矩阵（JZ-01..JZ-06）、无障碍与包容性设计（GB 50763-2012）、A3/A0 视觉增强，及双语同步、字体内嵌、manifest 哈希与 self-check 通过。
