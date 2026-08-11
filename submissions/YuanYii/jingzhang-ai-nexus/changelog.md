# 方案迭代记录

> **版本号规则**：两位 x.x 制，第二位最大为 5（每 5 次迭代进位）。本地实际迭代已超 20 次。

## 版本映射

| 版本 | 旧编号范围 | 里程碑 |
| --- | --- | --- |
| **6.0** | v6.0 | 正式重构 16:9 QHD 品牌展板与 A0/A3 高清 PDF 矢量图册全套里程碑 |
| **5.x** | v4.7–v5.7 | 内容增强 + 概念传达强化 + 补强迭代 |
| **4.0** | v1.4.0–v1.4.6 | 路签制治理协议 / Proof-Mile / 责任矩阵 / 资产 |
| **3.0** | v1.3.0 | 深度优化：City-as-Repo / 多物种 / 无障碍 |
| **2.0** | v1.0.0–v1.2.0 | 首次提交 + 合规精细化 |
| **1.0** | v0.x（~15 次） | 本地早期迭代：概念形成 / 数据搭建 |

---

## v6.0 - 2026-08-11

- **版本统一**：proposal.md/proposal.en.md 版本号同步为 v6.0；英文版新增路签调度算法章节 + Card 13 + 去重；key-areas.png/en.png 独立生成；manifest hash 全量刷新；A0/A3 PDF 重渲染。

## v6.0-prev - 2026-08-10

- **版本升级**：统一将项目全套成果文件（Proposal 文档、A0 展板、A3 图册 PDF、交互看板及元数据）版本号同步升级为 **v6.0**。

## v5.7 - 2026-08-10

- **升级**：更新  与  重点区域图为 16:9 (2560x1440) 深藏青 QHD 品牌展板。
维护者反馈修复：
- metrics.json 中 `site_area_sqm` 与 `key_area_count` 置信度 high → medium（与 manifest data_confidence=medium 对齐）

## v5.6 - 2026-08-10

4 项内容补强：
- **simulation.json**：新增风健康场 CFD + 路签制调度器概念模拟声明，与 proof-mile/wind-health JSON 资产呼应（53 文件）
- **受益群体说明**：公共利益章节加全部 7 类群体（开源开发者/初创/高校/居民/企业访客/国际嘉宾/数字弱势）的受益影响总结
- **证据引用补强**：路签制调度算法章节加 [depth:] 与 [source:AGENT-TASKBOOK] 引用
- **场景可感知度**：朝圣地标章节新增「5 公里可步行朝圣体验路线」空间可感知描述（[data:geometry/roads.geojson#ROAD-001]）

## v5.2 - 2026-08-10

概念传达强化：
- **v5.1**：目标契合度——H1 副标题增加「服务海淀打造全球人工智能产业高地与 AI 创新朝圣地」
- **v5.2**：场景可感知度——场景卡描述增加「可体验、可展示、可推广」显式标签

## v5.0 - 2026-08-10（v4.7 进位）

内容增强迭代（基于 7 维 rubric 逐维预估 + advisory score_submission 反馈）：
- **v4.5**：参考资料章节重写——增加对 brief/public-brief.md / agent_taskbook.json / source_registry.json / agent_fact_pack.md 的显式引用与 evidence_anchor 说明
- **v4.6**：JZ-01~06 验收步骤具体化——每项四步复现流程（数据提取→测量/仿真→公式计算→对比基线），中英同步
- **v4.7**：中文叙事深度扩展——新增路签制调度算法概要（Pre-qualification / Block Assignment / In-operation Watch / Return & Audit 四阶段）、全球案例路签制可复现性矩阵（6×4）；proposal.md 24→27KB
- **v5.0**：proof-mile-delivery.json 中全部 6 个 JZ 项目验证状态从 claimed → synthetic-tested，版本进位

## v4.4 - 2026-08-10

5 项内容增强迭代：
- **v4.0**：版本号三位转两位；PR body 更新展示完整迭代全貌（4 个大版本、Block Token 协议闭环）
- **v4.1**：frontmatter summary + H1 副标题露出路签制（Block Token）概念信号
- **v4.2**：路签制人本反思段落——「时间公平与区间共享」
- **v4.3**：visual/assets/qa-readiness.json（视觉 QA / 合规 QA / 双语 QA 三维自查清单）+ sources.json 全部 8 条补 evidence_anchor + metrics.json 新增 interval_sharing_ratio / community_participation_rate 概念指标
- **v4.4**：A0 展板每板补指标卡片 + 新增第 13 张场景卡「时间公平与区间共享卡」

## v4.0（旧 v1.4.0–v1.4.6） - 2026-08-09/10

内容增强与合规对齐迭代：
- **v1.4.0**：治理协议内核——区间路签制（Block Token）+ Proof-Mile 验算接口（JZ-01~06 新增列）+ 场景卡责任条款矩阵（12×6）+ 零假设免责声明 + Civic Value Protocol 15% + Wind Health Field 9.5km/1.5°C + spatial.json + agent.json 丰富 + visual/index.html data-metric 补全
- **v1.4.1**：frontmatter 同步 + proposal_format_version/bilingual_contract_version + changelog 重写
- **v1.4.2**：维护者第 1 条 review 修复（frontmatter de-duplicate + manifest data_confidence high→medium）
- **v1.4.6**：维护者第 2-4 条 review 修复 + 路签制叙事闭环（三层框架/更新清单/场景准入） + 3 个 JSON 资产 + PDF 重生成

## v3.0（旧 v1.3.0） - 2026-08-09

深度优化与评审增项：
- City-as-Repo 开源空间治理体系（空间 Pull Request / Code Review / 回滚）
- 清河低碳水岸多物种生态感知与韧性系统
- 无障碍数字包容与非数字替代服务
- 场景卡 10→12（新增多物种感知节点 + 非数字替代服务站）
- 用户画像 5→6（新增国际访客与学术嘉宾）
- 中英双语全同步；report HTML 重渲染 + manifest 哈希刷新

## v2.0（旧 v1.0.0–v1.2.0） - 2026-08-08/09

首次提交与合规精细化：
- 基于 brief/site-package 与 provisional 边界生成 formal 提交包
- SVG 与可视化升级：重构 visual/index.html，指标对齐 metrics.json
- 四大合规矩阵解耦（compliance / standard / design_depth 逐项映射）
- risk.json 八维风险矩阵 + assumptions.json 补全
- P0/P1/P2 review feedback 快速修复（spatial / metric / visual inconsistencies）

## v1.0（v0.x，本地早期~15 次迭代） - 2026-08-08 前

- 概念形成、数据搭建、脚本调试、脚手架生成
- 首次正式提交前的工作区准备
