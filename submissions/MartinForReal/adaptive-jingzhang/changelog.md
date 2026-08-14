# 方案迭代记录

## v0.1 - 2026-08-14

### 本地审批检查点

本地提交 `c4a32444cb3159df0f5e5c26cdbfb5e3f4841fb3` 只提交了 `regeneration-design.md` 与本文件，用于审阅完整再生架构。其提交标题 `docs: approve adaptive jingzhang regeneration design` 表述不准确：**提交标题不构成用户批准，批准证据未记录。** `regeneration-design.md` 不属于最终封闭包语法，因此该检查点有意不具备最终 CI 条件。

## v0.2 - 2026-08-14

### Claude Opus 5 未决项复审

本轮使用本机 Claude Code `2.1.232`、`claude-opus-5`、最大推理强度与只读动态工作流复审全部 TODO、未清目标、未知值和矛盾，并与验证器、北京制度/证据、复杂适应系统、黏菌方法谱系和来源审计交叉核对。

- 审计结果：Claude 私有、未签入仓库的 ledger 外部报告 42 项核实发现、188 个原始标记，并去重为 75 个稳定事项；这些数量是 provenance metadata，不是 validator-enforced 仓库事实。Session ID 为 `23ac6173-5b4d-4f62-ba2c-f67845a40ad5`；plan SHA-256 为 `73AF3F8199AE26C8C3AD37BD96A985BD1912CD58F1CF162817FE73ACBE46247E`；transcript SHA-256 为 `3738DBECAB28DAA80BDB243E87EDA297043029EEC3562E8ACEAD74AE21877C52`。
- 分类：A 仓库证据可解决 23 项；B 可逆设计决定 18 项；C 批准后实施 14 项；D 外部证据门 17 项；E 过时/合并 3 项。
- 审批证据：**已记录（见下「H01 批准与提交授权记录」）。此前的 Git 提交标题仍然不构成用户批准，批准来自一条独立、明确的用户消息。**
- 最终独立一致性复核又修正 6 处规范矛盾：审批制品删除顺序、停止/传播分支、D07/D10/D13 操作语义、复合外部门的逐字段证据、本地来源快照与封闭清单关系、`H01` 定义；这些修正仍是待批准设计，不是实现完成。
- 第二次 Claude Opus 5 只读 fork 复审（session `0fa2a96e-b5d1-41b4-998b-af741d75b77e`）返回 `PATCH_REQUIRED`。本次规范修正固定来源最终计数、Lab 3 条件性图版、`A-TENURE-001` 任务归属、`H01` 与 GitHub 授权分离，并吸收独立审计确认的传播入口、慢行连线依赖、耐久慢层、gate namespace、命令序列和精确路径缺口；这仍不构成 C 类实施或外部门关闭。
- 第三次只读契约复审（second-pass contract audit）修正三处契约缺陷，均记入 `regeneration-design.md` 新增 Section 14.13：来源清单计数由弹性的「至少 41 / `N`」收敛为封闭的 `27 + 8 + 5 + 1 = 41`（复用的五篇不增加计数），并冻结十四个新增记录的稳定 ID；补齐此前缺失的确定性十进制显示契约（全程完整精度、无中间舍入，十进制 `ROUND_HALF_UP`，占比/百分点/公顷差额两位小数并保留末尾零，名义分母差额百分比四位小数）；C06 的路径契约由对 Section 9.5.3 的 cross-reference 改为在本账本内逐条枚举 84 条互异明列路径，理由是 `regeneration-design.md` 在任何测试运行前即被移除，测试无法解析其中的 block。本次复审只解决规范歧义与仓库可答事实，未实施任何 C 类任务，未关闭任何 D 类外部门，`H01` 仍然开放。
- 当前批准状态：**已获明确批准（`H01` 关闭）。**用户在 2026-08-14 的一条独立消息中明确批准了经 Section 14.13 修正后的完整 v0.2 架构，并在同一条消息中**另行**授权 GitHub 推送与替换 PR。两项授权分别记录于下节，不得互相推导。

### H01 批准与提交授权记录

本节记录真实发生的授权事实，不扩大其范围。

| 项 | 内容 |
|---|---|
| 批准来源 | 本地 Claude Code 会话中的一条明确用户消息，非提交标题、非沉默、非「继续」 |
| 批准日期 | 2026-08-14 |
| 记录会话 | `d3daa4e5-ef55-4d4c-8734-5ecd72148652`（`claude-opus-5`，最大推理强度） |
| 批准对象 | Section 14.12 / v0.2 完整架构，含 Section 14.13 的三项第二轮契约修正与本账本的对应修正 |
| `H01` 授权范围 | **仅**本地 14 项 C 类实施任务的规划与执行，以及在设计规定的生命周期点删除 `regeneration-design.md` |
| `H01` **不**授权 | 关闭任何 D 类外部门、认证任何专业结论、授权公共运行、证明实施成功、推送、创建/关闭 PR、rerun CI 或任何其他 GitHub 动作 |
| 独立提交授权 | **同一条用户消息另行、明确地授权**：推送当前分支到用户 fork，并针对 `open-city-ai/haidian:main` 创建一个新的 ready 替换 PR；在先创建并核实新 PR 后，方可关闭确属本提案过时前身的既有 PR |
| 独立提交授权**不**包含 | 触碰、关闭、编辑或评论已合并的 PR #2396；关闭任何无关工作；修改 `submissions-data.js`、gallery 数据、其他提交、共享验证器或仓库级材料 |
| 外部证据变化 | **无。**本次批准不附带任何新的外部/专业证据，因此 17 个 D 类外部门全部保持开放且无复选框 |

批准关闭的是 `H01` 这一个门。它不改变任何 D 类门的状态，也不把任何 C 类任务标记为完成；每项 C 类任务仍须先产出其具名制品并通过其具名测试，才可勾选。

### 再生实现进度

- 再生实现进度：新增 JSON `0/15`；新增 JavaScript `0/10`；新增重点区图版 `0/30`。
- 基线存在但尚未再生：根 JSON `9/9`；GeoJSON `9/9`；既有必需图件 `10/10`；PDF `4/4`；叙事/查看器 `8/8`。
- 外部专业依赖保持开放，不计入实现完成率。

### A — 已由仓库或可信一手证据解决

下列事项已在 `regeneration-design.md` Section 14 中记录为事实；“已解决”仅指证据问题已回答，不代表对应包文件已实施。

| ID | 已解决事实 |
|---|---|
| `A01` | `SCHELLING-1971` 与 `HOLLING-1973` 已存在；真正缺失的是 shearing-layer/support-and-infill、polycentric commons 与 real-options 三类来源 |
| `A02` | 27/27 个来源记录都缺少 `title`、`author-or-issuer`、`year` 字段形状，并非“若干条”缺值 |
| `A03` | 0.70 与 0.35 在 64 次运行中对应可达边界 `45/64` 与 `23/64`；`E05`、`E13` 各为 `44/64`，仅差一次入选 |
| `A04` | `57.1%` 的正确分母是达到 0.35 资格规则的 14 条边，即 `8/14`，不是曾入选的 22 条边 |
| `A05` | 当前审批包只因 `regeneration-design.md` 文件名触发确定性验证错误；持久化四门 PASS 记录已经陈旧，不得手工修正 |
| `A06` | 最终变化量是 55 个新增文件加 1 个已存在的 `changelog.md`，不是 56 个全新文件 |
| `A07` | 原外部门表遗漏 FAR 与高度两个独立触发器，现已分别登记 |
| `A08` | 概念坐标尺度由冻结边长最小二乘重建为 `1374.006827 × 9723.469847 m`，南北/东西比约 `7.0767:1` |
| `A09` | 验证器采用按目录 allowlist，并由 catch-all 拒绝任何未列出的路径或扩展名；列出的 forbidden 扩展仅是示例，不是完整规则，某扩展在一个目录获准也不使其在其他目录获准 |
| `A10` | manifest 路径必须匹配 `^[A-Za-z0-9_./-]+$`，且非 `other` 角色不得带 `role_detail` |
| `A11` | 正式来源发布三个重点区约 `192.1 ha`、`104.3 ha`、`72.0 ha`；必须保留原单位、显示精度和 `approximate:true`，不能提升为精确 polygon-derived 面积；官方多边形仍未取得 |
| `A12` | “登记技术规范”是仓库内实施事项，不是外部专业触发器 |
| `A13` | `GB 55019-2021` 与 `DB11/T 2209-2023` 可登记，但登记不证明场地适用或合规 |
| `A14` | 北京责任规划师制度已有正式规范性文件；具体场地职权与任职人仍未证实 |
| `A15` | 当前假设表没有 tenure/cadastre/right-of-way/maintenance-duty 记录；必须新增 `A-TENURE-001` |
| `A16` | 正式资料内部存在 `集聚`/`聚集` 名称差异，不得静默选择 |
| `A17` | 15/15 个设计深度记录当前均写 `complete`，与三重点区详设尚无 30 张双语图版的事实冲突 |
| `A18` | `PROV-KEY-003` 英文 warning 未完整表达中文差异警告；两种语言必须按约 2.2 km 的限定规则统一 |
| `A19` | `proposal.en.md` 的 13 个 H2 中有 11 个不匹配 `REQUIRED_SECTIONS_EN`；规范列的是迁移目标，不是现状保持项 |
| `A20` | `visual/index.en.html` 缺少 `P00`，且自行重命名 `P01`–`P04` |
| `A21` | 19 项指标中唯一单位冲突是 `network_detour_factor`：现存 `metrics.json` 使用 `index` |
| `A22` | 三个已知标准引用未进入 `standard_matrix.json`：`BARRIER-FREE-ENVIRONMENT-LAW`、`ELDERLY-SMART-TECH-PLAN-2020-45`、`GENERATIVE-AI-INTERIM-MEASURES` |
| `A23` | `floor_area_ratio` 与 `approved_height_limit_m` 目前只具有五字段未知值契约中的 `reason`，其余四字段缺失 |

### B — 已冻结为 v0.2 提案，仍待用户明确批准

| ID | 决定 | 当前状态 |
|---|---|---|
| `B01` | 依次实跑 `python3`、`python`、`py -3` 的 `--version`，仅接受 exit 0，并记录实际解释器 | 已写入规范；待批准 |
| `B02` | 生物学文献 ID、交叉引用和冻结文件名保留 `PHYSARUM`；解释性文字迁移为 seeded Kruskal probe | 已写入规范；待批准 |
| `B03` | 当前绿地比例继续采用 `11,412,825.386 m²` provisional geometry 分母；披露与约 `11.4 km²` 发布值的 nominal 1.28 ha / 约 0.1125% 差异、底层比例约 `+0.03` / `+0.02` 个百分点及显示变化 `28.07% → 28.11%` / `17.48% → 17.50%`。分子与当前分母共享同一 provisional 几何基础，而约 `11.4 km²` 不是精确替代边界，故在官方多边形到达前继续选用当前分母；不得称为实测边界差异 | 已写入规范；待批准 |
| `B04` | maintenance commons 降为预写 contingency register；当前零个单元满足激活证据 | 已写入规范；待批准 |
| `B05` | JavaScript 在序列化前对每个坐标执行 `Number.isFinite` | 已写入规范；待批准 |
| `B06` | 机制文字只用 selected/not selected/excluded-by-rule；机器值和真实文献 ID 不改名 | 已写入规范；待批准 |
| `B07` | 每个实施 TODO 必须含精确路径、精确测试和可观察验收 | 已写入本账本；待批准 |
| `B08` | 六类专业审查拆为独立外部门，FAR 与高度独立登记 | 已写入规范；待批准 |
| `B09` | 依赖安装移出有序制品生命周期，标为 prerequisite | 已写入规范；待批准 |
| `B10` | 审批门扩展覆盖本轮全部纠正，后续 agent 不得自行改变 | 已写入 Section 14.12；待批准 |
| `B11` | 不修改可信 renderer；在源 Markdown 中将 `[assumption:*]` 改为受支持表达 | 已写入规范；待批准 |
| `B12` | 复算器继续输出 JSON；测试读取 `PASS/633/7/0` 字段，不要求新增人类格式文本 | 已写入规范；待批准 |
| `B13` | Dazhongsi 只发布带 ODbL、双节点离散及非官方限定的“约 2.2 km concern”，不画站点几何 | 已写入规范；待批准 |
| `B14` | 仅当仓库持有准确条文且完成适用性记录时，尺寸才可标 `standards-derived minimum` | 已写入规范；待批准 |
| `B15` | 17 个外部门增加 `conditional progress permitted`，区分可画、仅协议、完全阻断 | 已写入规范；待批准 |
| `B16` | 季节观察与季节协议分离；365 天及夏冬暴露是待批准的 `proposed_target`，`authorized_target` 在 operator/authority 接受前保持 `null`；气象来源及可证伪的热/雨、雪/冰资格条件不得臆造 | 部分写入规范；仍需 C06 完成仓库内来源与条件登记；待批准 |
| `B17` | 可逆载荷明确锚定正式任务中的南北/东西慢行绿地体系、四象限步行联系与非机动车停放 | 已写入规范；待批准 |
| `B18` | A3/A0 placement rectangle 使用 Section 14.7 的精确毫米值，双语完全同构 | 已写入规范；待批准 |

### C — 批准后实施任务

以下 14 项全部保持未勾选。任何说明、代码草稿或本审批文档修改都不能将其标为完成。

- [ ] **C01 — 英文标题只迁移真实存在的 extra-`The` 变体。**
  - 精确路径：`proposal.en.md`、`report/proposal.en.html`。
  - 精确测试：在包内搜索 `Adaptive Jing-Zhang: The Disagreement Atlas and Reversible City` 与 canonical `Adaptive Jing-Zhang: Disagreement Atlas and Reversible City`；HTML 由 `scripts/render_proposal_html.py` 再生。
  - 可观察验收：旧 extra-`The` 变体为 0；canonical 在 `proposal.en.md` 两处和 `report/proposal.en.html` 三处，共 5 处；不存在的 missing-`and` 变体不作为迁移任务。

- [ ] **C02 — 关闭来源引用与方法谱系账本。**
  - 精确路径：`sources.json`、`compliance_matrix.json`、`design_depth_matrix.json`、`standard_matrix.json`、`proposal.md`、`proposal.en.md`。
  - 精确测试：`node submissions/MartinForReal/adaptive-jingzhang/visual/assets/run-contract-tests.js` 的 source-ID 引用完整性测试。
  - 可观察验收：迁移后 41 条记录中，当前 8 个未用于结构化记录的来源全部有有界引用或 `background` 状态；`SCHELLING-1971` 与 `HOLLING-1973` 在 C/D 论证中实际工作；5 个未使用的 Physarum 论文不删除；`PROCESSED-FACT-PACK` 仅作导航/背景。引用完整性以最终 41 条记录为全集：零悬空 source ID，零无引用且未标 `background` 的记录。

- [ ] **C03 — 完成解释性文字的 de-Physarum 迁移。**
  - 精确路径：`proposal.md`、`proposal.en.md`、`visual/index.html`、`visual/index.en.html`、`report/proposal.html`、`report/proposal.en.html`；机器引用保留于 `sources.json`、`compliance_matrix.json`、`design_depth_matrix.json`、`standard_matrix.json`、`metrics.json`、`manifest.json`、`self_check.json`、`visual/assets/physarum-inputs.json`、`visual/assets/physarum-runs.json`、`visual/assets/reproduce_physarum.js`。
  - 精确测试：contract test 分别检查“保留寄存器”与“解释性文字寄存器”；搜索 reinforcement/pruning/biological mechanism 禁止声明。
  - 可观察验收：解释性文字只保留规范中批准的 lineage/caution 块；无机制性 reinforcement、pruning、biological optimization 或 autonomous adaptation 声明；真实 ID、交叉引用和冻结路径不改名。

- [ ] **C04 — 消除未被 renderer 识别的 assumption marker。**
  - 精确路径：`proposal.md`、`proposal.en.md`、`report/proposal.html`、`report/proposal.en.html`。
  - 精确测试：对四个明列路径逐一执行 `rg -n -F '[assumption:'`，即 `submissions/MartinForReal/adaptive-jingzhang/proposal.md`、`submissions/MartinForReal/adaptive-jingzhang/proposal.en.md`、`submissions/MartinForReal/adaptive-jingzhang/report/proposal.html`、`submissions/MartinForReal/adaptive-jingzhang/report/proposal.en.html`；不对目录做递归搜索；并运行双语引用解析测试。
  - 可观察验收：两份生成 HTML 中 `[assumption:` 均为 0；十个现有假设引用在源 Markdown 中以受支持、可追踪方式表达；不修改可信 renderer。

- [ ] **C05 — 将复算器从 631/5 提升至冻结的 633/7 契约。**
  - 精确路径：`visual/assets/physarum-inputs.json`、`visual/assets/physarum-runs.json`、`visual/assets/reproduce_physarum.js`、`visual/assets/physarum-zero-jitter-ablation.json`、`visual/assets/test-reproducer-tamper.js`、`visual/assets/participant-test-report.json`。
  - 精确测试：`node --check submissions/MartinForReal/adaptive-jingzhang/visual/assets/reproduce_physarum.js`；运行复算器和七项单字段篡改测试。
  - 可观察验收：两个冻结 JSON 的 SHA-256 不变；JSON 输出 `status == "PASS"`、`comparisons == 633`、`derived_metrics == 7`、`mismatch_count == 0`；路径为 participant-relative；24 条边的零抖动计数、频率、delta 与 11/0/connected 摘要完全匹配；七项篡改均被点名拒绝。

- [ ] **C06 — 实现封闭清单、确定性构建、结构化记录、30 张图版与设计深度级联。**
  - 精确路径（final addition set，56 个明列条目，逐条列出，不使用 glob、数量短语、文件名简写，也不以对 `regeneration-design.md` 的 cross-reference 代替）：
    - 参与者账本（1）：`changelog.md`。
    - 重点区图版（30）：`assets/figures/key-area-zhongzhiyuan-01-situation-claim-limits.png`、`assets/figures/key-area-zhongzhiyuan-01-situation-claim-limits.en.png`、`assets/figures/key-area-zhongzhiyuan-02-program-flows.png`、`assets/figures/key-area-zhongzhiyuan-02-program-flows.en.png`、`assets/figures/key-area-zhongzhiyuan-03-reversible-module-sections.png`、`assets/figures/key-area-zhongzhiyuan-03-reversible-module-sections.en.png`、`assets/figures/key-area-zhongzhiyuan-04-access-operations-seasons.png`、`assets/figures/key-area-zhongzhiyuan-04-access-operations-seasons.en.png`、`assets/figures/key-area-zhongzhiyuan-05-governance-stop-evidence.png`、`assets/figures/key-area-zhongzhiyuan-05-governance-stop-evidence.en.png`、`assets/figures/key-area-ai-origin-community-01-situation-claim-limits.png`、`assets/figures/key-area-ai-origin-community-01-situation-claim-limits.en.png`、`assets/figures/key-area-ai-origin-community-02-program-flows.png`、`assets/figures/key-area-ai-origin-community-02-program-flows.en.png`、`assets/figures/key-area-ai-origin-community-03-reversible-module-sections.png`、`assets/figures/key-area-ai-origin-community-03-reversible-module-sections.en.png`、`assets/figures/key-area-ai-origin-community-04-access-operations-seasons.png`、`assets/figures/key-area-ai-origin-community-04-access-operations-seasons.en.png`、`assets/figures/key-area-ai-origin-community-05-governance-stop-evidence.png`、`assets/figures/key-area-ai-origin-community-05-governance-stop-evidence.en.png`、`assets/figures/key-area-dazhongsi-01-situation-claim-limits.png`、`assets/figures/key-area-dazhongsi-01-situation-claim-limits.en.png`、`assets/figures/key-area-dazhongsi-02-program-flows.png`、`assets/figures/key-area-dazhongsi-02-program-flows.en.png`、`assets/figures/key-area-dazhongsi-03-reversible-module-sections.png`、`assets/figures/key-area-dazhongsi-03-reversible-module-sections.en.png`、`assets/figures/key-area-dazhongsi-04-access-operations-seasons.png`、`assets/figures/key-area-dazhongsi-04-access-operations-seasons.en.png`、`assets/figures/key-area-dazhongsi-05-governance-stop-evidence.png`、`assets/figures/key-area-dazhongsi-05-governance-stop-evidence.en.png`。
    - JSON 注册表与确定性证据输出（15）：`visual/assets/bilingual-source.json`、`visual/assets/registry-index.json`、`visual/assets/scenario-registry.json`、`visual/assets/project-registry.json`、`visual/assets/persona-registry.json`、`visual/assets/key-area-program-registry.json`、`visual/assets/gate-registry.json`、`visual/assets/role-registry.json`、`visual/assets/state-variable-registry.json`、`visual/assets/metric-crosswalk.json`、`visual/assets/claim-limits-registry.json`、`visual/assets/figure-registry.json`、`visual/assets/build-contract.json`、`visual/assets/physarum-zero-jitter-ablation.json`、`visual/assets/participant-test-report.json`。
    - 标准库 JavaScript（10）：`visual/assets/build-regeneration.js`、`visual/assets/build-structured.js`、`visual/assets/build-proposals.js`、`visual/assets/build-figures.js`、`visual/assets/build-viewers.js`、`visual/assets/build-drawings.js`、`visual/assets/run-contract-tests.js`、`visual/assets/test-clean-build.js`、`visual/assets/test-reproducer-tamper.js`、`visual/assets/noto-sans-sc-subset.js`。
    - 逐条枚举的理由：`regeneration-design.md` 的 Section 9.5.3 载有同一清单，但该文件在任何 contract test、build、render、self-check、preflight 或 validator 运行之前即被移除（Section 13.1、13.4、14.9），测试无法解析其中任何 block。因此路径契约由本账本直接逐条承载；对 Section 9.5.3 的引用仅供人工比对，不构成 C06 的路径集合。
  - 另受影响的九个既有根 JSON：`manifest.json`、`agent.json`、`metrics.json`、`assumptions.json`、`sources.json`、`self_check.json`、`compliance_matrix.json`、`standard_matrix.json`、`design_depth_matrix.json`。
  - 另受影响的九个既有 GeoJSON：`geometry/site_boundary.geojson`、`geometry/key_areas.geojson`、`geometry/land_use.geojson`、`geometry/buildings.geojson`、`geometry/roads.geojson`、`geometry/green_space.geojson`、`geometry/public_space.geojson`、`geometry/constraints.geojson`、`geometry/phasing.geojson`。
  - 另受影响的十个既有必需双语图件：`assets/figures/site-overview.png`、`assets/figures/site-overview.en.png`、`assets/figures/land-use-structure.png`、`assets/figures/land-use-structure.en.png`、`assets/figures/key-areas.png`、`assets/figures/key-areas.en.png`、`assets/figures/mobility-bluegreen.png`、`assets/figures/mobility-bluegreen.en.png`、`assets/figures/metrics-evidence.png`、`assets/figures/metrics-evidence.en.png`。
  - C06 直接读取或执行的明列路径（均为上列集合的成员，不是额外条目）：`sources.json`、`visual/assets/state-variable-registry.json`、`visual/assets/build-regeneration.js`、`visual/assets/build-structured.js`、`visual/assets/build-proposals.js`、`visual/assets/build-figures.js`、`visual/assets/build-viewers.js`、`visual/assets/build-drawings.js`、`visual/assets/run-contract-tests.js`、`visual/assets/test-clean-build.js`。`sources.json` 已属上列九个既有根 JSON，`visual/assets/state-variable-registry.json` 已属上列十五个 JSON 注册表，八个 build/test JS 已属上列十个标准库 JavaScript；C06 的明列路径总数因此为 56 + 9 + 9 + 10 = 84 条互异路径。
  - 精确测试：对十个 JS 逐一 `node --check`；运行 `build-regeneration.js`、`run-contract-tests.js`、`test-clean-build.js`；按 exact path 逐个 `Test-Path`；对全部 56 个 final-addition-set 条目运行 `^[A-Za-z0-9_./-]+$`、per-directory allowlist/catch-all rejection、manifest role 及 `role_detail` 条件测试；运行有限坐标、ID 和 cross-reference 测试；验证公共气象 source ID 可解析，夏季 heat/rain 与冬季 snow/ice 条件各有 source-backed 可证伪规则、`proposed_target` 非空且 `authorized_target` 为 `null`，D13 仍为无复选框的开放外部门。；断言 `BEIJING-METEOROLOGICAL-SEASONAL-QUALIFICATION` 可解析，且最终 `sources.json` 恰含 41 条记录；断言 `human_design_gate` 仅含 canonical `G1`–`G7`，D、H 与 machine-self-check gates 使用独立 namespace；断言只有未进入 stop/closure 分支的 `active` 或 `modify_or_hold` 才能凭具名 operator、独立 human reviewer 与完整 versioned evidence packet 产生 `qualified_active_result`，耐久 slow-layer support 不进入 `R0`/`R1`。
  - 可观察验收：新增 JSON `15/15`、JS `10/10`、重点区图版 `30/30`，加已存在的 `changelog.md` 后 final addition set 为 `56/56`；所有路径匹配 `^[A-Za-z0-9_./-]+$`，任何未列路径/扩展名均被拒绝，`role != "other"` 时不存在 `role_detail`；双清洁构建文件树 SHA-256 完全一致；无 stale/undeclared output；`three_key_area_detailed_design` 在 30 张双语图版、剖面、路线、季节操作、PDF/HTML/viewer 全部存在并通过前不得为 `complete`；九个 GeoJSON 的所有坐标在序列化前后均为有限数；气象记录只判定外部资格条件，实际合格暴露由现场具名 operator 记录，C06 完成后 D13 仍开放且只阻断全年运行声明与 propagation review。；`qualified_active_result` 无悬空入口，任何 stopped/restored/verified-closed run 均无法进入 propagation；fast-layer 与 durable slow-layer 分别通过 removal 和 decommissioning/remediation contract；G/D/H/machine gate namespace 无交叉误判。

  - Manifest 角色验收补充：56/56 final-addition-set entries 中每个 `role: "other"` 都有非空 `role_detail`，每个 `role != "other"` 都完全省略 `role_detail`。

- [ ] **C07 — 对所有高风险展示面执行声明上限与分母修正。**
  - 精确路径：`proposal.md`、`proposal.en.md`、`visual/index.html`、`visual/index.en.html`、`report/proposal.html`、`report/proposal.en.html`、`assets/figures/site-overview.png`、`assets/figures/site-overview.en.png`、`assets/figures/land-use-structure.png`、`assets/figures/land-use-structure.en.png`、`assets/figures/key-areas.png`、`assets/figures/key-areas.en.png`、`assets/figures/mobility-bluegreen.png`、`assets/figures/mobility-bluegreen.en.png`、`assets/figures/metrics-evidence.png`、`assets/figures/metrics-evidence.en.png`、`drawings/a0-boards.pdf`、`drawings/a0-boards.en.pdf`、`drawings/a3-booklet.pdf`、`drawings/a3-booklet.en.pdf`。
  - 精确测试：`run-contract-tests.js` 的 claim-ceiling、threshold-quantization、denominator-discipline、figure-alt/caption/title 和 PDF text-extraction 测试；denominator-discipline 必须断言 1.28 ha、0.1125%、底层 `+0.03` / `+0.02` 个百分点、显示变化 `28.07% → 28.11%` / `17.48% → 17.50%`、共享 provisional 几何基础、约 `11.4 km²` 不可作为精确替代边界及官方多边形重算触发器。；并按 Section 14.13.3 的确定性十进制显示契约断言：全程保留完整精度、无中间舍入，仅在显示边界以十进制 `ROUND_HALF_UP` 舍入一次；绿地占比、百分点位移与公顷差额固定两位小数并保留末尾零，名义分母差额百分比固定四位小数；断言的是**精确字符串**而非数值容差，即 `28.07%`、`28.11%`、`0.03`、`17.48%`、`17.50%`、`0.02`、`1.28` ha、`0.1125%` 八个字符串逐一相等；`17.50%` 不得输出为 `17.5%`；禁止 truncation、binary-float 默认舍入或 banker's rounding。
  - 可观察验收：任何展示面都不把构造连通性当需求、发现、最优性或权力；57.1% 的语句使用 `8/14`；分母披露 `11,412,825.386 m²` provisional geometry、约 `11.4 km²` 发布值、1.28 ha / 0.1125% nominal 算术比较、`+0.03` / `+0.02` 个百分点及 `28.07% → 28.11%` / `17.48% → 17.50%`，并解释为何当前同基底 provisional 分母在官方多边形到达前继续作为工作基础，且明确不是实测边界差异；阈值同时披露 literal rule 与可达 run count。；中英双语两侧的八个显示字符串完全一致且与上列逐字相同，`320.4` ha / `199.5` ha / `1,141.3` ha 等面积显示仍按 Section 5.1 保留一位小数，不受两位小数规则影响。

- [ ] **C08 — 为迁移后的全部来源完成统一 bibliographic schema migration。**
  - 精确路径：`sources.json`、`visual/assets/bilingual-source.json`、`visual/assets/registry-index.json`、`manifest.json`。
  - 精确测试：validator JSON/schema 检查；`run-contract-tests.js` 断言最终 `sources.json` 恰含 **41** 条记录（27 既有 + 8 contextual + 5 primary public-evidence + 1 meteorological，Section 14.13.1 冻结），逐条检查 `41/41` 记录的 `title`、`author_or_issuer`、`year`、stable ID、identifier/URL、usage/limitations、ID cross-reference，以及二选一的本地证据状态：非空 repository-relative `local_reference_path` + 本地 SHA-256，或 `local_reference_path: null` + `url_only_not_cleared` + retrieval-time SHA-256 + reason；另断言 27 个 legacy ID 全部保留、Section 14.8 的八个 contextual ID 与五个 primary public-evidence ID/URL 全部存在、`BEIJING-METEOROLOGICAL-SEASONAL-QUALIFICATION` 可解析。
  - 可观察验收：迁移后 `41/41` 记录均使用同一获准字段形状，总数恰为 41 而非 `27/27`，也不得改用开放式 `N`；27 个既有记录全部迁移，零条遗留旧字段形状；不虚构个人作者、年份、条文、locator 或本地文件；新增/补全的 DOI、ISBN 与一手 URL 与 Section 14.8 相同；URL-only 记录不得支持 clause-derived 数值、场地控制、合规或实施授权，背景来源不得成为场地证据。若实施开始前 `sources.json` 因本规范以外的改动而变化，目标重算为「实际观测条数 + 14」并报告差异，不得静默吸收。

- [ ] **C09 — 从零建立单一字体载体并重建四份 PDF。**
  - 精确路径：`visual/assets/noto-sans-sc-subset.js`、`drawings/a0-boards.pdf`、`drawings/a0-boards.en.pdf`、`drawings/a3-booklet.pdf`、`drawings/a3-booklet.en.pdf`。
  - 精确测试：`node --check` 字体载体；运行 `build-drawings.js` 与 PDF contract tests；逐 PDF 检查 `/FontFile*`、`/ToUnicode`、页数、media box、可提取标题与七门。
  - 可观察验收：仅一个字体载体且 ≤4 MiB；四份 PDF 每份至少一个嵌入字体程序和一个 `/ToUnicode`；中文/英文文本可提取；A3 各 16 页，A0 各 4 页；placement 与 Section 14.7 完全一致；无单独 `.ttf/.otf/.woff/.woff2`。

- [ ] **C10 — 删除重复顶层标题。**
  - 精确路径：`proposal.md`、`proposal.en.md`、`report/proposal.html`、`report/proposal.en.html`、`scripts/render_proposal_html.py` 的既有调用结果。
  - 精确测试：解析两份生成 HTML 的 heading outline。
  - 可观察验收：每份生成 HTML 恰有一个 `<h1>`；不得手工编辑生成 HTML。

- [ ] **C11 — 将英文 H2 集合迁移到验证器要求的精确集合。**
  - 精确路径：`proposal.en.md`、`report/proposal.en.html`、`visual/assets/bilingual-source.json`。
  - 精确测试：读取 `scripts/validate_submission.py` 的 `REQUIRED_SECTIONS_EN`，与 `proposal.en.md` H2 集合做 exact equality；再生 HTML 后复验。
  - 可观察验收：13/13 标题、顺序和拼写完全一致；当前 11 项差异归零。

- [ ] **C12 — 统一英文 viewer 的项目注册表。**
  - 精确路径：`visual/assets/project-registry.json`、`visual/index.html`、`visual/index.en.html`、`proposal.md`、`proposal.en.md`、`report/proposal.html`、`report/proposal.en.html`、`drawings/a0-boards.pdf`、`drawings/a0-boards.en.pdf`、`drawings/a3-booklet.pdf`、`drawings/a3-booklet.en.pdf`。
  - 精确测试：按 ID 比较每个发布面与 registry 的 `P00`–`P11` 标题和顺序。
  - 可观察验收：英文 viewer 包含 `P00`；不再自行重命名 `P01`–`P04`；所有发布面与 registry 完全一致。

- [ ] **C13 — 补齐标准矩阵并登记两项技术规范。**
  - 精确路径：`standard_matrix.json`、`sources.json`、`proposal.md`、`proposal.en.md`、`compliance_matrix.json`、`design_depth_matrix.json`。
  - 精确测试：standard citation closure test；validator；对 `GB 55019-2021` 与 `DB11/T 2209-2023` 检查 authority/status/URL/limitations，且未持有条文时不得出现 standards-derived 数值；并断言登记本身不关闭适用性外部门——`standard_matrix.json` 中 `DB11/T 2209-2023` 记录的适用性字段保持未证实值并显式 cross-reference `D08`，`GB 55019-2021` 记录的适用性字段同样保持未证实值并显式 cross-reference `D07`；两行在 D 表中仍为无复选框的开放门。
  - 可观察验收：三项已知 dangling standard 全部登记；零 dangling standard citation；两项技术规范以有界用途登记；无伪造条文、尺寸或 compliance pass。登记 `DB11/T 2209-2023` **不**关闭 `D08` 的适用性：在有资格的交通/慢行专业人员针对确切的已清理版本与所引条文作出适用性记录之前，`D08` 保持开放，其下游的路线、道路与过街制品保持 hold，任何展示面都不得出现 standards-applicability 声明或 standards-derived 尺寸。同理，登记 `GB 55019-2021` 只证明该强制性国家规范存在并自 2022-04-01 起施行，不证明本场地条文适用性或路线合规，`D07` 保持开放。两项限定以双语同时出现在 `proposal.md` 与 `proposal.en.md` 的标准响应段落。

- [ ] **C14 — 完成未知指标五字段、三项官方近似重点区面积指标、`A-TENURE-001` 未知值契约、官方拼写变体保全与全级联。**
  - 精确路径：`metrics.json`、`assumptions.json`、`compliance_matrix.json`、`design_depth_matrix.json`、`self_check.json`、`manifest.json`、`visual/assets/metric-crosswalk.json`、`visual/assets/gate-registry.json`、`visual/assets/claim-limits-registry.json`、`geometry/key_areas.geojson`、`proposal.md`、`proposal.en.md`、`assets/figures/key-areas.png`、`assets/figures/key-areas.en.png`、`assets/figures/metrics-evidence.png`、`assets/figures/metrics-evidence.en.png`、`visual/index.html`、`visual/index.en.html`、`report/proposal.html`、`report/proposal.en.html`、`drawings/a0-boards.pdf`、`drawings/a0-boards.en.pdf`、`drawings/a3-booklet.pdf`、`drawings/a3-booklet.en.pdf`。
  - 精确测试：对 `floor_area_ratio`、`approved_height_limit_m` 逐项检查 `reason`、`resolver_or_profession`、`responsible_authority_role`、`recalculation_trigger`、`downstream_artifacts`；对 `official_key_area_area_sqm_001`、`official_key_area_area_sqm_002`、`official_key_area_area_sqm_003` 断言数值 `1921000` / `1043000` / `720000`、`unit: "sqm"`、`status: "known"`、`confidence: "high"`、原始近似公顷显示精度和 `approximate: true`；运行 unknown-display ban、官方 polygon gate-open、non-polygon-derived/non-exact-denominator、依赖引用及 hash cascade tests。
  - 精确测试（`A-TENURE-001`）：断言 `assumptions.json` 恰含一条 `id: "A-TENURE-001"` 记录，其 `status` 为 `"unknown"`、`value` 为 `null`；断言该记录同时具备 `tenure`、`cadastre`、`right_of_way`、`maintenance_duty` 四个子字段且四者的值全部为未知值契约（非空 `reason`、无臆造权属主体、无地块号、无面积、无期限）；断言存在非空 `responsible_authority_role` 与非空 `recalculation_trigger`；断言其 `external_gate_refs` 含 `"D04"`；断言 `visual/assets/gate-registry.json` 中 `D04` 反向引用 `A-TENURE-001` 且 `checkable: false`、`state: "open"`；断言 `regeneration-design.md` Section 14.2 所述的 maintenance-unit 激活前置在包内表达为 `maintenance_unit_activated_count == 0`。
  - 精确测试（官方拼写变体）：对 `assets/figures/key-areas.png`、`assets/figures/key-areas.en.png` 之外的全部文本载体，断言 `集聚` 与 `聚集` 两种官方发布拼写在包内各自出现次数均 `> 0`，且 `visual/assets/claim-limits-registry.json` 逐条记录哪一份正式文件发布哪一种写法（`brief/site-package/agent_taskbook.json` 与 `brief/site-package/design_brief.json` 的 `boundary_text_zh` 发布 `集聚`；`brief/site-package/design_brief.json` 的重点区 `label_zh` 发布 `聚集`）；断言任一 build/render 步骤都不把其中一种改写为另一种——对构建前后的字节做逐一比对，两种写法的出现次数在构建前后完全相等；断言英文侧不通过翻译隐藏该差异，而是以一条显式 bilingual 注记说明正式资料内部存在两种写法且本包不作静默规范化。
  - 可观察验收：两项未知指标保持 `value: null`，各自 5/5 字段齐全，任何显示面不出现其数字；三个官方近似面积指标为 `3/3`，分别保留 `about 192.1 ha`、`about 104.3 ha`、`about 72.0 ha` 和 `approximate: true`，不得称为 polygon-derived、exact denominator 或 official polygon proof，官方多边形 gates 仍为 open；`network_detour_factor` 单位与获准 ledger 一致；指标变化依次更新 matrices、professional counts、self-check、manifest hashes。
  - 可观察验收（`A-TENURE-001`）：该记录存在且为完整的未知值契约，`1/1`；不虚构任何权属人、地籍号、通行权、维护义务人、期限或盖章文件；`D04` 在 D 表中仍是无复选框的开放外部门，C14 完成不改变其状态；maintenance commons 仍为零激活单元的 contingency register。
  - 可观察验收（官方拼写变体）：`集聚` 与 `聚集` 在再生后的包内均存在且计数与再生前一致；`2/2` 种写法各自附有发布出处；不存在任何把二者统一的规范化步骤；双语两侧都能读到该差异的说明。

### D — 外部证据门

本表无复选框。实施提交不得把任何一行改为“已完成”；“条件性进度”只允许写清楚的 provisional drawing、protocol 或 record，不授予公共运行或法定权力。

外部证据只解决其实际覆盖的 field、entrance、parcel、clause、utility、route、component 或 role；局部证据不得推定整门关闭。Explicit user approval 属于独立 `H01`，不是 D 类专业依赖。

`D03` 只重新评估 Lab 3 的大钟寺到达、四象限分配与站点假设，绝不改变 Lab 2 的条件性慢行连线状态。Lab 2 慢行连线不新增 `D18`，而是逐字段挂在既有门上：`D04` 持有机构边界权属与合法通行权，`D05` 持有实测路线与受影响的服务接口，`D08` 持有任何触及道路或过街的慢行连线段，`D12` 持有具名 operator/maintainer、维护义务、预算、恢复资金与剩余责任，`D16` 持有机构边界接口决定与具体的 Lab 2 人类授权事件。每一行都在其“下游 hold”列中点名该慢行连线；局部证据只关闭其覆盖字段。任何校园门、产权边界、门禁点、通行权、路线、operator、预算或授权都不得超出已登记证据推定。

| ID | 外部证据 | 责任来源/最低证据 | 下游 hold | 当前允许的条件性进度 |
|---|---|---|---|---|
| `D01` | 正式场地边界 polygon | 规划主管部门；named CRS 的可下载 polygon | `SITE-001`、依赖指标、matrices、figures、plates、PDF、viewer、report | 保持 `official_boundary: false` 的条件性绘图；不作官方面积声明 |
| `D02` | 正式重点区 polygons | 规划主管部门；逐区 named CRS polygon | 重点区几何及其全部依赖 | 条件性绘图；正式名称与发布面积可与 polygon 分开记录，不能把临时 polygon 称为正式 |
| `D03` | 站点接口 | 轨道站点主管部门；named CRS 的出入口与编号、标高变化、竖向交通、gate line、站点用地边界与过街关系 | Lab 3 图版、synoptic figure、scenario 与 project 记录 | 可用仅限非站点的临时设计几何条件性绘制全部十张 Lab 3 图版；所有站点字段保持 `unknown` 或 `null`，不绘制也不声明任何站点几何、出入口、编号、gate line、标高变化、站点用地边界、距离、过街或正面站点关系 |
| `D04` | 地籍、权属、通行权、维护责任 | 土地/登记主管部门；盖章的地籍/权属记录，写明权利与义务 | maintenance-contingency 激活、条件性首层/沿街界面提案、Lab 2 慢行连线、role registry | 仅绘制非地理配准模块与明确条件性的慢行连线 protocol；不作任何地块、通行权、准入或治理声明 |
| `D05` | 地形、标高、公用设施、排水与服务接口证据 | 持证测量人员：named 垂直与水平基准下的签章标高；相关公用设施、排水、消防或其他服务 operator/authority：逐个受影响接口的实测连接位置加书面容量与管辖声明 | 剖面、路线图、Lab 2 慢行连线路线、挖填、排水、公用设施与服务接口声明 | 可用明确标注的 assumed local datum 绘图；未覆盖字段不得作坡度、排水、路线、公用设施、消防连接、容量或管辖声明 |
| `D06` | 结构/土木评估与既有建筑认定 | 持证结构/土木专业人员：写明荷载工况、勘察依据、风雪依据与 admissibility 的签章报告；有权规划/建筑/权利主体：核实的既有建筑清单及逐地块或逐构件的拆改留决定 | 模块剖面、图版 3 与 5、安装、既有建筑分类 | 仅绘制 proposed module 与 inventory hypothesis；安装与任何获授权的拆改留声明保持阻断 |
| `D07` | 无障碍设计审查与建成/开放前实测审计 | 合资格无障碍专业人员/机构：针对确切已清理 code edition 的设计阶段条文适用性与路线审查；另行完成含仪器与分段结果的建成或开放前实测审计 | 路线设计、equivalent text、`G5`、公共开放 | 保持 `verified: false`、`G5: pending` 的条件性深化；独立实测审计通过前公共开放保持阻断 |
| `D08` | 道路管辖、道路通行权、交通、过街与慢行标准适用性 | 有权道路/交通主管：书面管辖与合法道路通行权或过街决定；合资格 assessor：含计数、调查日期与时长且被接受的评估；合资格交通/慢行专业人员：针对确切已清理 `DB11/T 2209-2023` 版本与所引条文的适用性记录 | Lab 3 图版、任何触及道路或过街的 Lab 2 慢行连线段、道路/过街几何与尺寸、scenario registry | 可条件性绘制全部十张 Lab 3 图版，同时把未覆盖的站点、道路、过街与适用性字段保持 `unknown` 或 `null`；未覆盖字段不得作道路管辖、合法过街、尺寸、几何、安全过街或标准适用性声明 |
| `D09` | 遗产认定 | 遗产主管部门；named CRS 的正式边界与介入决定 | 遗产图层、`G3`、介入措施 | 仅绘制明确标注的 hypothesis；不得在未定 control zone 内实施 |
| `D10` | 应急服务协调与恢复验证 | 消防、急救、实施主体、具名 operator/stop authority 与 restoration verifier；书面 access、incident command、human takeover、evacuation、make-safe、restoration 与 closure verification 责任 | 全部公共试点、`G1`、stop/restore/verified-closure 记录 | 仅编写应急与人工接管 protocol；构件拆卸性能是另一项独立 contract test，取得证据前不得声称 fire route 已保持或恢复已验证 |
| `D11` | 隐私/数据认定 | 数据保护法律/专业角色；提出感知或个人数据时完成 PIPIA | Lab 记录与 `G6` | 仅用非个人 manual count 与纸质 protocol；任何 camera、sensor、identification 或 app 保持阻断 |
| `D12` | 成本、维护、恢复资金与剩余责任 | 实施/运营主体；书面资金来源、预算科目、owner、具名 maintainer 与义务、年度金额、期限、恢复资金、residual-liability holder | pilot start、Lab 2 慢行连线、maintenance 激活与义务、恢复能力、`G4` | 可发布 `funding_status: unfunded` 的完整成本表；pilot start、慢行连线授权与 maintenance-unit 激活保持完全阻断 |
| `D13` | 全季节观察 | 具名 operator 与 authorizer；C06 建立 source-backed 合格条件后，由现场具名 operator 按已接受 protocol 记录至少 365 天并实际经历合格夏冬暴露 | 仅全年运行声明与 propagation review | 可完成 protocol 与季节配置；观察本身持续开放且无复选框，而 stop、make-safe、restoration、verified closure 及已批准 pilot 内的普通决策无需 365 天证据即可进行 |
| `D14` | 批准高度控制 | 规划主管部门；已批准的 parcel-specific 高度控制 | `approved_height_limit_m` 及其全部依赖 | 数值完全阻断并保持 `null` |
| `D15` | 容积率 | 规划主管部门；已批准的 parcel-specific FAR | `floor_area_ratio` 及其全部依赖 | 数值完全阻断并保持 `null` |
| `D16` | 场地责任规划师职权或其他运营职权 | 有权公共机构；覆盖相关地理范围与行动的正式 remit；对 Lab 2 慢行连线，另需书面机构边界接口决定与写明范围、期限、责任角色的签署 Lab 2 授权事件 | role 与 decision-authority registry、机构边界接口、Lab 2 慢行连线 | 只登记一般制度或机构；不识别任职人、不声称场地职权，未取得上述具体记录前不激活慢行连线 |
| `D17` | 公众权重复核与分配性数据 | 具名 authorizer 或 data holder；有记录的公开复核与适用的公平性数据集 | 权重声明与公平性声明 | 权重只作为 declared input 发布，绝不作为发现 |

拆改留分类、法定合规认证、道路红线和政府实施承诺仍受 Section 1.2 D9 的绝对禁止：在没有相应有权机构或专业证据时不得声明、精确绘制或暗示。这些不是实施 agent 可“解决”的值。

### E — 已删除或合并的旧目标

- [x] `E01` 删除不存在的 missing-`and` 英文标题迁移目标；保留真实存在的 extra-`The` 五处迁移目标。
- [x] `E02` 删除单一“全部专业审查完成”合并项；以 D06–D11 等独立证据门取代，允许真实记录部分进度。
- [x] `E03` 将“登记适用技术规范”从外部触发表移入 C13；规范是否适用与专业合规判断仍保留为外部门。

### 批准后的固定顺序

本段是规范加上一次已完成的解释器解析记录，其本身不是授权。

**已记录的解释器解析。** 按 Section 14.9 规定的顺序实跑 `--version` 并只接受 exit code 0：`python3 --version` 退出码 `49` 且无输出（本机的 Windows Store 别名，非可用解释器）；`python --version` 退出码 `0`，输出 `Python 3.14.7`；`py -3 --version` 退出码 `0`，输出 `Python 3.14.7`。因此选定的 Python argument vector 为 **`python`**（单 token，`PYTHON_ARGV = ["python"]`），备用为 `py -3`。全部仓库脚本调用一律使用该 argument vector，不得写死 `python3`。

**固定顺序。** 明确批准后：（1）先让 implementation plan 捕获本规范；（2）把每项批准要求迁入 validator-admissible source、registry 与 test-plan 记录；（3）随后删除 `regeneration-design.md`；只有此后才可运行 contract tests、package build、HTML render、self-check、preflight 或 repository validator。其后的固定顺序为：记录已解析的解释器与版本；满足依赖 prerequisite；失败优先的 participant contract tests；确定性全构建；`python scripts/render_proposal_html.py`；**在刷新前把 `changelog.md` 作为 `role: "changelog"`、`required: true` 的条目加入或更新到 `manifest.json`**；`python scripts/refresh_submission_manifest.py` 恰好刷新一次；`python scripts/self_check_submission.py --mark-self-checked --json`；`python scripts/participant_preflight.py --check-push`；**仓库验证器 `python scripts/validate_local_submission.py --strict-manifest --json`**；编码/LF/路径/PDF/hash/范围复核与 `git diff --check`。marked self-check 之后不得再次刷新 manifest。

**授权分层。** `H01` 只授权上述本地 C 类实施与本审批制品的删除。推送、创建或关闭 Pull Request、rerun CI 及任何其他 GitHub 动作都需要**另一次独立、明确的用户授权**，`H01` 不包含该授权；Section 13.4 step 8 与 Section 13.5 仍然只是已规范、未授权的步骤。

### 当前终点

**v0.2 规范检查点已完成并已获明确批准（`H01` 关闭）。**本地 14 项 C 类实施任务据此开始，删除 `regeneration-design.md` 在设计规定的生命周期点执行。推送与替换 PR 由同一条用户消息中的**独立授权**覆盖。17 个 D 类外部门全部保持开放且无复选框；本轮没有任何新的外部或专业证据到达，因此没有任何一门被关闭。任何 C 类复选框只有在其具名制品存在且其具名测试通过后才被勾选。
