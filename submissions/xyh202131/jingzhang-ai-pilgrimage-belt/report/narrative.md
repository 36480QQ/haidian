# 投稿包内验收参考 / Package-local acceptance reference

> 本文件只服务于 `submissions/xyh202131/jingzhang-ai-pilgrimage-belt/`，是投稿内可复制参考，不是仓库级 reusable template、公共 PR template 或维护者规范。复制到其他提交或后续 PR 时，不得继承任何 `[x]`。
>
> This file applies only to `submissions/xyh202131/jingzhang-ai-pilgrimage-belt/`. It is a package-local copy reference, not a repository-level reusable template, public PR template, or maintainer policy. No `[x]` may be inherited when it is copied into another submission or later PR.

## 方案叙事摘要 / Narrative summary

AI 朝圣·铁轨新生带 V2.4 将百年京张定义为一条可审计的 AI 公共创新生产线。小月河场景赋能翼提出真实问题，AI 原点社区共创，众智园验证，大钟寺发布与服务，中关村科技服务翼提供建议性的合规与转化支持，公众反馈和失败证据回流下一年度。

本轮不另起一套空间规划，而是把最新投稿 skill 的硬合同落实到现有方案：正文可读映射任务书三大定位与五大功能，合并三处重点区证据交叉表，补齐用地、分期、重点区、建筑密度与道路比例等必需指标族，统一中央来源 ID 与来源元数据，并把 OSM 背景和临时范围的 0% 相交、约 412.5 米最近距离诚实记录为未裁决的不确定性。中英文主稿、HTML、视觉首页、A3/A0、八组双语 PNG 展示对与两组双语 SVG 可编辑源对均为必交对照件。全部节点仍处于 G0；临时 geometry、字段覆盖、本地 PASS 与生成记录均不构成审批、现场结果或清权证明。

Jing-Zhang V2.4 treats the corridor as an auditable public AI innovation production line. This increment adds no competing spatial plan. It makes the current skill contract visible and testable by mapping the taskbook's three positioning statements and five functions in readable prose, consolidating the three-key-area evidence crosswalk, completing required metric families, normalizing source IDs and provenance metadata, and disclosing the 0% OSM/provisional overlap and approximately 412.5 m nearest distance as unresolved uncertainty only. Chinese and English narratives, HTML, visual homepages, A3/A0 outputs, eight bilingual PNG display pairs, and two bilingual SVG editable-source pairs are required counterparts. Every node remains at G0; provisional geometry, field coverage, local PASS results, and generation records are not approval, field-performance, or rights-clearance evidence.

## 本次增量状态 / Current increment status

> 本节只记录尚未产生可信 GitHub check 的当前增量。它不得继承下方 `e71ff206…` 历史快照的任何 `[x]`；最终 PR head 的可信 `submission-validation` 才能关闭最后一项。
>
> This section records the current increment before a trusted GitHub check exists. It inherits none of the `[x]` items in the historical `e71ff206…` snapshot below. Only trusted `submission-validation` on the final PR head can close the last item.

- [x] 任务书三大定位、五大功能和六个智能体任务均可从正文、矩阵、图层与展示物回查；未新增重复的第四套总矩阵。
- [x] `metrics.json` 包含 62 个 known 与 11 个 unknown 指标；正式资料缺失的建筑密度、道路比例等保持 unknown，不以体量或中心线替代。
- [x] 29 条来源均补齐采集、时空、复用、转换和限制字段；结构化来源引用全部回到稳定 ID，刷新审计完成数仍为 0。
- [x] 中英文正文、离线报告、视觉首页、八组双语 PNG 展示对、两组双语 SVG 可编辑源对与 A3/A0 均为必交对照件，并同步 provisional、G0、字段覆盖不是结果和权利未清边界。
- [x] 三处重点区证据交叉表只表示文档映射齐全；现场审计、责任主体确认、批准、测试执行和已知结果仍为 0。
- [x] 最终 manifest 覆盖 60 个包文件，所有 59 个非 manifest SHA-256 与暂存/提交 Git blob 匹配；权利台账同样恰好覆盖 60 个路径且每个路径只归组一次。
- [x] strict score、deterministic、spatial、visual、professional、self-check 与 participant preflight 在最终本地字节上通过。
- [ ] 最终 PR head 的可信 `submission-validation` 为 `SUCCESS`。

- [x] The taskbook's three positioning statements, five functions, and six agent tasks are traceable through prose, matrices, layers, and display artifacts; no duplicate fourth master matrix was added.
- [x] `metrics.json` contains 62 known and 11 unknown metrics. Building density, road ratio, and other unsupported formal values remain unknown rather than being replaced by massing or centerline proxies.
- [x] All 29 sources carry collection, temporal, spatial, reuse, transformation, and limitation metadata; structured references resolve to stable IDs, while completed freshness audits remain 0.
- [x] Chinese and English narratives, offline reports, visual homepages, eight bilingual PNG display pairs, two bilingual SVG editable-source pairs, and A3/A0 outputs are required counterparts and align on provisional, G0, coverage-is-not-result, and uncleared-rights boundaries.
- [x] The three-key-area evidence crosswalk represents documentation mapping only; field audits, accountable-role confirmation, approvals, test executions, and known results remain 0.
- [x] The final manifest covers 60 package files, all 59 non-manifest SHA-256 values match staged/committed Git blobs, and the rights ledger covers exactly the same 60 paths once each.
- [x] Strict score, deterministic, spatial, visual, professional, self-check, and participant preflight pass against the final local bytes.
- [ ] Trusted `submission-validation` on the final PR head reports `SUCCESS`.

## 本次 PDF 重生记录 / Current PDF regeneration record

最终 pass A（含 QA）的实际窗口为 2026-08-10 03:31:52 +08:00 至 03:32:36 +08:00；独立 pass B 的窗口为 03:34:32 +08:00 至 03:35:26 +08:00。两个 pass 均在全新的 Python 进程中运行，四份包内 PDF 与 pass A 逐文件字节相同，pass A 与 pass B 也逐文件字节相同。中文 A3 为 33 页、英文 A3 为 36 页，均为 297×420mm 纵向。八组 1800×1100 图件在每种语言 A3 中各自按 `[0,168,620,1060]`、`[590,168,1210,1060]`、`[1180,168,1800,1060]` 拆成三个 620×892 裁片，每片以 245mm 宽独占细节页，相邻裁片重叠 30px；因此每种语言为 8 组/24 个裁片，不再在 A3 嵌入整张 1800×1100 图。中文/英文栅格证据的有效最小文字指标分别为 10.865pt 与 9.297pt，所有 live text 不小于 9pt，443/443 个逻辑块可搜索。中英文 A0 各 8 页、均为 1189×841mm 横向，继续按“场地总览—用地—重点区—重点区剖面—交通—指标—创新—实施”顺序将整图置于 1149mm 安全版心，原字节未变。PyMuPDF 以 1.6 倍渲染并检查全部 85 页；未发现裁切、越界、空白页、孤立标题、错序或不可读字形。生成与版式 QA 不证明现实执行；T-02 仍为 G0：0 回放、0 回答输出、0 现场测试。

The final pass A window, including QA, was 2026-08-10 03:31:52 +08:00 to 03:32:36 +08:00; independent pass B ran from 03:34:32 +08:00 to 03:35:26 +08:00. Each pass ran in a fresh Python process. Every package PDF is byte-identical to pass A, and pass A is byte-identical to pass B file by file. The Chinese A3 booklet has 33 portrait 297 × 420 mm pages and the English booklet has 36. In each language, every one of the eight 1800 × 1100 figures is divided into crops `[0,168,620,1060]`, `[590,168,1210,1060]`, and `[1180,168,1800,1060]`; each 620 × 892 crop occupies a 245 mm-wide detail page, with 30 px overlap between adjacent panels. Each language therefore contains 8 sets/24 crops and no embedded 1800 × 1100 whole-board A3 image. The minimum effective raster-evidence text metrics are 10.865 pt for Chinese and 9.297 pt for English; all live text is at least 9 pt, and 443/443 logical blocks are searchable. Each language retains eight landscape 1189 × 841 mm A0 whole-board overview pages in the order site overview, land use, key areas, key-area sections, mobility, metrics, innovation, and implementation, inside the 1149 mm safe frame; those A0 bytes are unchanged. PyMuPDF rendered and checked all 85 pages at 1.6×; no clipping, media-box overflow, blank page, isolated heading, wrong order, or unreadable glyph was found. Generation and layout QA do not prove real-world execution. T-02 remains G0: 0 replays, 0 answer outputs, and 0 field tests.

| PDF | Pages / format | SHA-256 |
|---|---|---|
| `drawings/a3-booklet.pdf` | 33 / A3 portrait | `a1364afaa471b63d9e9ecc001129f5ff7fe01405dc34f6379842d38a68dc73d2` |
| `drawings/a3-booklet.en.pdf` | 36 / A3 portrait | `2ac3cc0c006789912a834bde5303c2e6a1a6d9f40bfffc8768751e9698b0e7dd` |
| `drawings/a0-boards.pdf` | 8 / A0 landscape | `77bcce2d7b1a17bc6db289358e63db228681eebc3ec4ea9288f4bf5af69e7d5e` |
| `drawings/a0-boards.en.pdf` | 8 / A0 landscape | `53ac76d1cc51f1eb19e8c4f9fa4b96acc3046c3c0db4f4e8f7c8c4034328c384` |

Reproduction basis: Python 3.13.12 (Anaconda build, 2026-02-24), ReportLab 5.0.0, fontTools 4.63.0, PyMuPDF 1.27.2.3, and Pillow 12.2.0 were used; Poppler was unavailable. ReportLab emitted compressed PDFs with `invariant=1`, fixed metadata, fixed input ordering, and the exact A3 crop boxes recorded above. `fontTools.varLib.instancer.instantiateVariableFont(..., optimize=True, updateFontNames=True, static=True)` instantiated in-memory 400/700 weights from `C:/Windows/Fonts/NotoSansSC-VF.ttf` (name-table version `2.04;241114210130;non-release`, SHA-256 `763146584cf0710223441356b4395e279021b0806c196614377a7a0174ae074a`, local name-table license SIL OFL 1.1). The source font binary and temporary static fonts are not shipped. Searchable final spans use only `NotoSansSC-Regular` and `NotoSansSC-Bold`; the A3 resource dictionaries retain an unused Helvetica declaration with zero Helvetica spans and no embedded Helvetica program. PyMuPDF and Pillow verified exact crop pixels, full x coverage, 30 px overlaps, 24 A3 crops/eight figure sets per language, zero whole-board A3 images, 443/443 searchable logical blocks, rendering, extraction, geometry, ordering, content bounds, and full-package contact sheets. A read-only Git diff against the pre-increment package baseline returned no geometry path or `metrics.json`; their Git blobs remained unchanged. No repository script was changed. Future source or figure changes require regeneration, manifest refresh, and full validation; this record makes no trusted-CI, human-review, rights-clearance, or field-success claim.

## 不可变验证证据 / Immutable validation evidence

| Field | Immutable value |
|---|---|
| `validated_commit` | `e71ff206800fbd154cbcb8a3b9b139e600f1bd97` |
| `validation_run_id` | `31273071020` |
| `validation_run_url` | [submission-validation Run 31273071020](https://github.com/open-city-ai/haidian/actions/runs/31273071020) |
| `validation_status` | `SUCCESS` |
| `validation_completed_at_utc` | `2026-08-08T18:55:03Z` |
| `validated_manifest_sha256` | `4b7fc901c06065872b496f8f481914ec9fc6044d23f248946793b17c3445f506` |
| `snapshot_generated_at_utc` | `2026-08-08T19:02:52Z` |

上述记录只证明 exact head `e71ff206…` 及其 manifest 原始 Git blob。任何后续提交都会使这些 `[x]` 对新 head 失去自动继承资格；新 head 是否通过，以 GitHub 上绑定该 head 的可信 check 为准。包内 Markdown 无法在不制造新提交的情况下自证“当前最终 commit”，因此这里保留上一份已完成验证的不可变指针，不把未来运行写成既成事实。

The record above validates only exact head `e71ff206…` and its raw manifest Git blob. A later commit cannot inherit these `[x]` automatically; the trusted GitHub check attached to that later head is authoritative. A package-local Markdown file cannot self-record its own final commit without creating another commit, so this section preserves the last completed immutable pointer and does not claim a future run as completed.

## 状态语义 / Status semantics

- `[x]`：已由上方 exact commit/run 快照或可复现命令验证，只适用于该不可变快照。
- `[ ]`：尚待人工决定、正式资料或现实测试；不自动等于本地 gate 失败。
- 任一内容文件变化后，必须把准备复制的所有 `[x]` 重置为 `[ ]`，重新核验 manifest 哈希并等待新 head 的可信验证。

- `[x]`: verified by the exact commit/run snapshot above or a reproducible command, and valid only for that immutable snapshot.
- `[ ]`: pending a human decision, official material, or real-world testing; it is not automatically a local-gate failure.
- After any content-file change, reset every checkbox intended for copying from `[x]` to `[ ]`, revalidate all manifest hashes, and wait for the trusted check on the new head.

## 已验证快照（仅对应 `e71ff206…`）/ Validated snapshot (`e71ff206…` only)

### 范围与完整性 / Scope and integrity

- [x] 变更只位于 `submissions/xyh202131/jingzhang-ai-pilgrimage-belt/`。
- [x] `package_type=professional_design_package` 且 `package_state=ready_for_review`。
- [x] manifest 登记 48 个路径，47 个非自引用内容文件均有 SHA-256。
- [x] 权利台账覆盖 48 个 manifest 路径，无漏项、未知路径或重复归组。
- [x] 中文主稿、英文展示稿及对应离线 HTML 的关键数字与边界一致。

- [x] Changes stay inside `submissions/xyh202131/jingzhang-ai-pilgrimage-belt/`.
- [x] `package_type=professional_design_package` and `package_state=ready_for_review`.
- [x] The manifest declares 48 paths and SHA-256 values for all 47 non-self-referential content files.
- [x] The rights ledger covers all 48 manifest paths with no missing, unknown, or duplicate grouping.
- [x] Key numbers and boundaries align across the Chinese report, English display copy, and paired offline HTML.

### 自动化 gate / Automated gates

- [x] 严格 advisory score 为 8/8，`needs-work=0`、`missing=0`。
- [x] deterministic、spatial、visual 与 professional review 均为 PASS。
- [x] 综合 self-check 为 `ok=true`、`review_status=formal-review-ready`。
- [x] participant preflight 无目录外文件和内容 blocker。
- [x] 47 个内容文件哈希与暂存/提交 Git blob 逐项一致。
- [x] `git diff --check` 无空白错误。

- [x] Strict advisory score is 8/8 with `needs-work=0` and `missing=0`.
- [x] Deterministic, spatial, visual, and professional review gates pass.
- [x] Combined self-check reports `ok=true` and `review_status=formal-review-ready`.
- [x] Participant preflight reports no out-of-scope file or content blocker.
- [x] All 47 content hashes match staged/committed Git blobs.
- [x] `git diff --check` reports no whitespace error.

### 证据边界 / Evidence boundaries

- [x] 场地与三处重点区保持 provisional，不冒充官方红线或精确面积依据。
- [x] 25 条来源均记录可用与禁用范围；已完成刷新审计数保持为 0。
- [x] 全部 AI 场景保持 G0，不声明已批准、已建设、已运行或已获机构承诺。
- [x] 非 AI 通道、人工兜底、申诉、停止与退役字段只证明设计覆盖，不冒充现场效果。
- [x] 权利总体状态保持 `not_fully_cleared`，独立逐文件清权审计完成数为 0。

- [x] The site and three key areas remain provisional and are not represented as official redlines or precise-area evidence.
- [x] All 25 sources record permitted and prohibited uses; completed refresh audits remain at 0.
- [x] Every AI scenario remains at G0, with no claim of approval, construction, operation, or institutional commitment.
- [x] Non-AI access, human fallback, grievance, stop, and retirement fields prove design coverage only, not field performance.
- [x] Overall rights status remains `not_fully_cleared`, with 0 completed independent file-level clearance audits.

## 仍需人工或外部完成 / Human or external completion still required

- [ ] 维护者完成人工内容、视觉与版权判断并决定是否合并/发布。
- [ ] 正式边界、控规和现状资料到位后完成差异比对与全量复算。
- [ ] 完成许可条款、字体、OSM 衍生数据库、工具输出、Logo/商标和可编辑源的独立权利审计。
- [ ] 完成适用的规划、建筑、交通、市政、景观、消防、铁路安全、无障碍、数据安全和法律审查。
- [ ] 在获批、限时、限域和有责任主体的条件下完成现场或受控测试。

- [ ] Maintainers complete human content, visual, and rights judgment and decide whether to merge or publish.
- [ ] After official geometry, controls, and existing-condition material arrive, complete difference analysis and full recalculation.
- [ ] Complete independent review of license terms, fonts, OSM-derived databases, tool outputs, logo/trademarks, and editable sources.
- [ ] Complete applicable planning, architecture, transport, municipal, landscape, fire, railway-safety, accessibility, data-security, and legal review.
- [ ] Complete field or controlled testing only under approved, time-bounded, place-bounded, and accountable conditions.

## 下次 PR 可复制模板 / Copyable checklist for the next PR

> 以下项目故意保持未勾选。开始下一次增量时，只复制本节并保持全部 `[ ]`；不得复制或继承上方任何 `[x]`、commit、run、manifest SHA 或生成时间。完成一项再勾选一项。
>
> The items below are intentionally unchecked. For the next increment, copy only this section and keep every item at `[ ]`. Do not copy or inherit any `[x]`, commit, run, manifest SHA, or timestamp above. Check each item only after completion.

- [ ] 从最新 `origin/main` 创建独立分支，确认前一个投稿 PR 已合并或关闭。
- [ ] 只实现一个可命名、可验证的小增量，只修改自己的投稿目录。
- [ ] 同步中文主稿、英文展示稿和对应离线 HTML。
- [ ] 不新增虚构审批、合作方、资金、建设、运行、测试或清权结果。
- [ ] 内容先暂存；从暂存 Git blob 计算 SHA-256；manifest 最后暂存。
- [ ] 运行 strict score、deterministic、spatial、visual、professional、self-check 与 participant preflight。
- [ ] 提交后复核 committed Git blob 哈希；fork 推送 dry-run 通过。
- [ ] 创建 Ready PR（非 Draft），确认文件范围、无冲突和可信 `submission-validation`。

- [ ] Branch from the latest `origin/main` after the previous submission PR is merged or closed.
- [ ] Implement one named, verifiable increment and modify only the contributor-owned package.
- [ ] Synchronize the Chinese report, English display copy, and paired offline HTML.
- [ ] Add no fabricated approval, partner, funding, construction, operation, test, or rights-clearance result.
- [ ] Stage content first, calculate SHA-256 from staged Git blobs, and stage the manifest last.
- [ ] Run strict score, deterministic, spatial, visual, professional, self-check, and participant preflight gates.
- [ ] Reverify committed Git blob hashes and pass the fork push dry-run.
- [ ] Open a Ready PR (not Draft) and confirm file scope, mergeability, and trusted `submission-validation`.

## 复现命令 / Reproduction commands

```powershell
$pkg = 'submissions/xyh202131/jingzhang-ai-pilgrimage-belt'
python scripts/score_submission.py "$pkg/proposal.md" --strict --json
python scripts/spatial_review.py $pkg --stage formal --json
python scripts/visual_review.py $pkg --json
python scripts/professional_review.py $pkg --json
python scripts/self_check_submission.py $pkg --pr-author xyh202131 --json
python scripts/participant_preflight.py $pkg --pr-author xyh202131 --json
git diff --check
```

若 `origin` 指向只读公共仓库，对可写 fork 另行执行 `git push --dry-run fork HEAD:<branch>`。

If `origin` is the read-only canonical repository, separately run `git push --dry-run fork HEAD:<branch>` against the writable fork.
