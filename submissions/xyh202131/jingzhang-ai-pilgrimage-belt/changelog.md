# 方案迭代记录 / Changelog

> 本日志仅记录本投稿包的可追溯变化，不是审批、实施、现场测试、权利清除或 trusted CI 证明。每次内容变化后，均须从最终 Git blob 重新生成 manifest，并以绑定最终 PR head 的仓库验证为准。
>
> This log records traceable changes to this submission package only. It is not evidence of approval, implementation, field testing, rights clearance, or trusted CI. After any content change, regenerate the manifest from the final Git blobs and rely on repository validation attached to the final PR head.

## v2.5 - 2026-08-10

**Key-area spatial-reading integration / 重点区空间读法整合**

- 新增中英文可编辑 SVG 与确定性 PNG，以既有 `PROV` / `PUBLIC` / `I-GATE` / `AI-ZONE` / `SCENE` ID 深化三处临时重点区，并展示三层关系、连续非 AI / 无障碍路径、人工交接、停止/恢复、可撤回叠层与四种模式。
- 在双语正文和离线视觉首页配对整合两组图件；每处重点区仅新增一段“图面读法 / 尚缺资料”，不重复完整矩阵。
- All bilingual editable SVG and deterministic PNG deepen the three provisional areas using only existing `PROV` / `PUBLIC` / `I-GATE` / `AI-ZONE` / `SCENE` IDs, with three-layer relationships, continuous non-AI / accessible routes, staffed handoff, stop/recovery, removable overlays, and four modes.
- Both figure pairs are integrated into the bilingual proposal and offline visual indexes; each key area gains only one reading/missing-evidence paragraph, without duplicating the complete matrix.
- 所有图面仍不按比例、临时且为 G0；批准、现场审计、测试执行和已知结果均为 0，权利状态仍为 `not_fully_cleared`。geometry、metrics 与规划内容未改；未新增项目、节点、路线、地块、伙伴、批准、现场或运营结果。
- All diagrams remain not to scale, provisional, and G0; approvals, field audits, test executions, and known results remain 0, and rights remain `not_fully_cleared`. Geometry, metrics, and planning content are unchanged; no projects, nodes, routes, parcels, partners, approvals, field results, or operating results are added.

**PDF and package-evidence integration / PDF 与包证据整合**

- 将八组双语 PNG 展示对（包含新增的重点区剖面展示对）与两组双语 SVG 可编辑源对纳入最终包合同；manifest 现覆盖 60 个路径/59 个非 manifest 内容文件，权利台账按相同路径集合逐项归组。新增 SVG 只补足两组重点区图件的可编辑源，不代表其他 PNG/PDF 已具有完整可编辑布局源，也不将 `not_fully_cleared` 或 0 次独立逐文件审计升级。
- Integrated eight bilingual PNG display pairs, including the new key-area-sections pair, plus two bilingual SVG editable-source pairs into the final package contract. The manifest now covers 60 paths / 59 non-manifest content files, and the rights ledger groups the identical path set once each. These SVGs provide editable sources only for the two key-area figure pairs; they do not complete editable-layout coverage for the other PNG/PDF outputs or upgrade `not_fully_cleared` and 0 independent file-level audits.
- 用最终正文和八组 1800×1100 图件离线重生四份 PDF：中文/英文 A3 分别为 10/13 页，双语 A0 各 8 页。最终 pass A 与独立 pass B 均在新 Python 进程运行且逐文件字节相同；包内四份 PDF 的 SHA-256 分别为 `22edb9b1…`, `55df4d89…`, `77bcce2d…`, `53ac76d1…`。生成工具为 Python 3.13.12、ReportLab 5.0.0、fontTools 4.63.0、PyMuPDF 1.27.2.3 与 Pillow 12.2.0；页面、顺序、字体、图像和内容边界 QA 覆盖全部 39 页。
- Regenerated all four PDFs offline from the final narratives and eight 1800 × 1100 figure pairs: Chinese/English A3 contain 10/13 pages and each A0 language contains eight pages. Final pass A and independent pass B ran in fresh Python processes and are byte-identical file by file; the four package SHA-256 values begin `22edb9b1…`, `55df4d89…`, `77bcce2d…`, and `53ac76d1…`. The actual toolchain was Python 3.13.12, ReportLab 5.0.0, fontTools 4.63.0, PyMuPDF 1.27.2.3, and Pillow 12.2.0; page, order, font, image, and content-bound QA covered all 39 pages.
- A3/PDF 文字由旧 Arial Unicode MS 路径替换为 `NotoSansSC-VF.ttf` 的确定性 400/700 内存实例与嵌入子集；记录源版本 `2.04;241114210130;non-release`、SHA-256 `76314658…074a` 和本地 name table 的 SIL OFL 1.1 声明，且不随包分发字体二进制。该元数据记录不等于独立许可合规结论。
- Replaced the prior Arial Unicode MS path with deterministic in-memory 400/700 instances and embedded subsets from `NotoSansSC-VF.ttf`; recorded source version `2.04;241114210130;non-release`, SHA-256 `76314658…074a`, and the local name table's SIL OFL 1.1 declaration, without shipping the font binary. This metadata record is not an independent license-compliance conclusion.
- 本轮只整合展示与包证据；只读 Git 对比确认 `geometry/*.geojson` 与 `metrics.json` 的 Git blobs 未变。最终 PR head 的 trusted CI 与维护者人工内容、视觉、版权审查仍未发生，不能由本日志预先勾选。
- This increment integrates presentation and package evidence only; a read-only Git comparison confirms that the Git blobs for `geometry/*.geojson` and `metrics.json` did not change. Trusted CI on the final PR head and maintainer human content, visual, and rights reviews have not occurred and are not pre-claimed here.

## v2.4 - 2026-08-09

**Skill contract alignment and publication QA / Skill 合同对齐与发布质量复核**

### 已采纳 / Accepted

- 将 #998 的三处重点区证据交叉表纳入同一完整增量；三条记录只证明映射字段齐全，不证明现场覆盖、责任主体确认、批准、测试或结果。
- 按最新投稿 skill 补齐必需指标族：九类用地代码面积、三期面积、三处临时重点区面积；建筑密度与道路比例因正式资料缺失而明确保持待补，不用体量原型或道路中心线代替。
- 同步主线 `provisional_boundaries_basis.md` 的空间不确定性：OSM 背景核查与临时总体范围的 0% 相交和约 412.5 m 最近距离不裁决边界正误，也不触发非官方改线。
- 将当时已有的双语主稿、HTML、视觉首页、A3/A0 和文字图件在 manifest 中全部标为必交；本轮新增重点区剖面 PNG 对与两组 SVG 可编辑源对后，最终合同为八组双语 PNG 展示对、两组双语 SVG 可编辑源对，中英文主张、指标和限制保持配对。
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
