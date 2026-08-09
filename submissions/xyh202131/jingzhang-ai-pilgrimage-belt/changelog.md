# 方案迭代记录 / Changelog

> 本日志仅记录本投稿包的可追溯变化，不是审批、实施、现场测试、权利清除或 trusted CI 证明。每次内容变化后，均须从最终 Git blob 重新生成 manifest，并以绑定最终 PR head 的仓库验证为准。
>
> This log records traceable changes to this submission package only. It is not evidence of approval, implementation, field testing, rights clearance, or trusted CI. After any content change, regenerate the manifest from the final Git blobs and rely on repository validation attached to the final PR head.

## v2.4 - 2026-08-09

**Skill contract alignment and publication QA / Skill 合同对齐与发布质量复核**

### 已采纳 / Accepted

- 将 #998 的三处重点区证据交叉表纳入同一完整增量；三条记录只证明映射字段齐全，不证明现场覆盖、责任主体确认、批准、测试或结果。
- 按最新投稿 skill 补齐必需指标族：九类用地代码面积、三期面积、三处临时重点区面积；建筑密度与道路比例因正式资料缺失而明确保持待补，不用体量原型或道路中心线代替。
- 同步主线 `provisional_boundaries_basis.md` 的空间不确定性：OSM 背景核查与临时总体范围的 0% 相交和约 412.5 m 最近距离不裁决边界正误，也不触发非官方改线。
- 将双语主稿、HTML、视觉首页、A3/A0 和七组文字图件在 manifest 中全部标为必交；中英文主张、指标和限制保持配对。
- 补齐来源采集方法、时空覆盖、复用边界、转换和已知限制；中央来源使用稳定 ID，来源新鲜度策略仍不把访问日期写成完成刷新审计。
- 重排中英文 A0，使每张 1800×1100 核心板图占据 A0 主要安全版心；图件放大不提升数据精度或现实成熟度。
- 刷新 agent/toolchain 披露和 checked-in `self_check.json`，消除旧包体积、旧指标数量和旧变更清单快照。

### 未采纳 / Not adopted

- 未新增第四套“全包总矩阵”；现有 compliance、standard、design-depth、pilot-readiness 与 key-area crosswalk 已分别承担任务、专业深度、交接门和重点区证据职责，重复矩阵会增加漂移风险。
- 未将同行方案的具体命名、代码、JSON 结构或图形资产复制进本包；只使用公开评审中可复述的抽象方法，并保留各自许可边界。
- 未把临时 geometry、公开背景、机器 PASS、字段覆盖率或本地生成记录写成官方红线、法定指标、合作承诺、现场成果或发布许可。

### 仍待外部完成 / Still external or pending

- 官方 polygon、现状测绘、权属、控规、道路/铁路/水务/文保/市政/消防条件到位后，完成差异比对与 EPSG:4548 全量复算。
- 责任主体、审批、参与者保护、场地时窗和独立复测条件成立后，才可执行 G1；当前全部场景仍为 G0，现实执行与已知结果均为 0。
- 权利状态继续为 `not_fully_cleared`；完整 `COMMUNITY-DISPLAY-ONLY` 条款、OSM ODbL 处理、PDF 字体与工具输出、Logo/商标和可编辑源仍需独立复核。
- 当前增量的本地门槛与最终 trusted `submission-validation` 必须在最终字节、最终 manifest 和最终 PR head 上重新运行；不得继承历史快照的勾选状态。

## English summary

- Consolidates the #998 key-area crosswalk into one complete increment without treating documentation coverage as field evidence.
- Completes required metric families while keeping unsupported density, road, statutory, and operational values pending.
- Carries the main-branch boundary cross-check as uncertainty evidence only; it neither proves an error nor authorizes a replacement boundary.
- Makes every bilingual counterpart required, normalizes source provenance, enlarges the A0 boards to a usable safe frame, and refreshes tool/self-check records.
- Adds no approval, partner, funding, construction, operation, test, rights-clearance, or trusted-CI result. All scenes remain G0 and public/professional reuse remains blocked pending the stated rights work.
