## v1.4.0 - 2026-08-09

高分冲刺与合规审计提档（v1.4.0 formal sprint）：

### 新增内容
- **区间路签制（Block Token）治理协议**：把京张单线铁路的路签/令牌闭塞制度用作城市 AI 治理协议内核——一个街区区间 = 一枚路签，三处重点区 = 三座"站"、两翼 = 两处"道岔"
- **Proof-Mile 验算接口**：JZ-01 至 JZ-06 更新项目表格新增验证状态列（claimed → synthetic-tested → field-pending + 验收标准）
- **场景卡责任条款矩阵**：12 张场景卡逐项补齐六类责任条款（公共目的/最小数据/人工责任/非AI替代/申诉删除/硬停止条件）
- **零假设免责声明**：开篇双态声明——全部空间边界为 Provisional 概念划定（official_boundary=false）、全部模拟为 Synthetic Tabletop（Field Pilot: NOT AUTHORIZED / NOT RUN）
- **Civic Value Protocol**：概念建议 15% 算力运营收益反哺社区无障碍与湿地维护
- **Wind Health Field**：9.5km 主导风廊降低热岛 1.5°C 的气象模拟方向

### 机器可读资产
- 新增 `spatial.json`（5 个概念节点/廊道，disclaimer=concept-only）
- 新增 `visual/assets/execution-brief.json`（三阶段执行节奏 + 治理门）
- 新增 `visual/assets/risk-release-register.json`（6 项风险释放条件）
- `agent.json` 补充 capabilities/tools_used/methodology
- `visual/index.html` 关键指标全部带 data-metric 标记

### 合规与修复
- proposal.md 与 proposal.en.md frontmatter 同步 v1.4.0，补充 proposal_format_version: "2" 与 bilingual_contract_version: "1"
- 中英章节 16:16 对齐；manifest 48 文件 SHA-256 全部刷新
- 所有 AI 场景模拟标注为 Synthetic Tabletop 结果，责任角色统一标注 Unassigned Role Specification

# 方案迭代记录

## v1.3.0 - 2026-08-09

深度优化与评审增项：

- **新增**「城市即代码库（City-as-Repo）开源空间治理体系」：借鉴同行 y-line 方案，引入空间 Pull Request 机制、三方 Code Review 与一键回滚概念，置于第 12 章（agent.6 治理创新增强）。
- **新增**「基于公园已建成区域的精细化拆改留原则」：借鉴 ren-belt 方案，恪守公园一期已建成开放、二期已推进的事实，空间动作聚焦断点缝合与创新线补充（第 7 章增补）。
- **新增**「清河低碳水岸多物种生态感知与韧性系统」：借鉴 all-life-speaks 方案，补充多模态环境 AI 感知网、雨洪碳汇调控与多物种友好界面（第 9 章增补 + 场景卡 06 扩展）。
- **新增**「无障碍数字包容与非数字替代服务」：借鉴 verifiable-city 方案，强化全场景实体兜底、线下办事窗口与 Human-in-the-Loop 申诉（第 12 章增补）。
- **扩展**场景卡从 10 张增至 12 张：新增"多物种生态感知节点"（#11，AI 测试验证场景）与"非数字替代服务站"（#12）。
- **扩展**用户画像从 5 类增至 6 类：新增"国际访客与学术嘉宾"画像。
- **同步** proposal.en.md 全部新增内容的 1:1 英文镜像。
- **修正**优化方案中 3 类合规风险：政府机构点名改为概念建议表述、实施承诺语气加限定语、不可验证日期改为保守表述。
- **重渲染** report/proposal.html / report/proposal.en.html；重新生成 manifest 哈希。

## v1.2.0 - 2026-08-09

全面合规与精细化改造：
- **SVG 与可视化升级**：重构 `visual/index.html` 总览图，以实际 GeoJSON 为基础提取 5 组矢量 Path 与智轨轴脊曲线，补齐 5 大专题系统展示模块；修正前端仪表盘指标为 `31.11%`，严格对齐 `metrics.json`。
- **主标题与品牌名收敛**：统一元数据 (frontmatter) 与 H1 标题为《百年京张AI创新带城市设计方案:京张智脉·绿意无界(智轨轴脊主线)》，确保前置品牌名一致。
- **正文规范排版与结构对齐**：彻底修复正文孤立 `#`、重复 `## 1.` 标题及跳号问题；完美对齐 12 个硬性主主章结构，将文化叙事、运营治理等模块作为子节精准收容。
- **场景卡与 Agent.3 显式回应**：在 10 张场景卡表中显式新增「AI产业测试验证场景」专属列，并勾选 S-02 安全沙盒、S-06 低碳水岸、S-08 数据会客厅 3 大测试验证节点。
- **解耦四大合规矩阵**：对 `standard_matrix.json`、`design_depth_matrix.json` 与 `compliance_matrix.json` 进行了全量逐项拆分映射，消除“共享同一组章节”的雷同问题；在 `assumptions.json` 中补齐 A-DATA/SCENARIO/CULTURE/OPS 风险假设。
- **实施分期矢量与表格补全**：补全 `geometry/phasing.geojson` 至 6 个独立分期要素，并在更新项目清单中补齐“近期/中期/远期”实施阶段划分。

## v1.1.0 - 2026-08-09

评审符合性改造：

- **新增**「三大定位与功能统筹」小节：将百年京张文化带、都市AI生活体验带、AI融合创新带逐一映射到总体空间结构。
- **新增**「百年京张文化、中关村文化与 AI 新文化叙事」专章，完整回应 agent.5：历史文化资源三级体系、三线叙事、空间文化段落、导视标识符号系统、国际传播叙事。
- **新增** Logo 概念图（`assets/figures/logo.png` / `logo.en.png`）：钢轨双线 × 神经网络拓扑，嵌入 proposal 正文、报告 HTML 与视觉展示页。
- **补充** 区域协同：加入与北纬社区共享京张绿环的社区协同表述。
- **补充** `geometry/constraints.geojson`：新增文保节点、清河蓝线、遗址廊道 3 个概念约束要素，修复 JZ-05 悬空引用。
- **修正** 建筑高度与建筑基底表述为「概念建议 / 概念规划 / 情景测算」，统一任务书边界条款措辞要求。
- **新增** `risk.json` 八维风险矩阵（数据隐私/实施复杂度/公众接受度/运维成本/政策不确定性/空间争议/技术成熟度/公平包容）。
- **重写** `proposal.en.md` 完整译稿（与中文版章节、表格、指标、证据引用一致）。
- **重渲染** `report/proposal.html` / `report/proposal.en.html`；`visual/index.html` / `visual/index.en.html` 嵌入 Logo 与六项任务覆盖矩阵。

## v1.0.0 - 2026-08-08

首版提交：

- 基于 brief/site-package 与 provisional 边界生成 formal 提交包，通过确定性自检（formal-review-ready）。
