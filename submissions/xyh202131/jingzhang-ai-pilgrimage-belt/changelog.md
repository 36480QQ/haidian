# 方案迭代记录 / Changelog

## v58.1 - 2026-08-24

**评审可读性与权利证据定向修复 / Targeted Readability and Rights-Evidence Repair**

- 响应 PR #3932 exact-head 评审：为中英 report/visual 共用一份本地 Noto Sans SC WOFF2 子集，覆盖四份 HTML 的完整字符并集与符号字符；干净 Chromium 截图不再出现中文方框，仍保持离线、无 JavaScript、无远程字体。
- 英文 `site-overview` 的页首长标题、说明与面板标题改为有界短句/双行说明，并同步重建英文 PNG 与引用它的 A3/A0；不改变空间事实、数字或冻结几何。
- 删除中英正文重复的第 13 章提示；两版仍保持 13 个正式章节、同一图件位置和证据边界。
- 定向复核 `CASE-22AT` 与 `CASE-KINGS-CROSS`：前者在 Barcelona 市政府页面确认可访问；后者原 workspace URL 仍为 403，改用同一项目运营方可访问的公共咨询页。两者继续仅作背景比较，不承担海淀控制、现实绩效或成熟度证据。
- 新增覆盖当前分发树每个路径的投稿方权利清单，记录 CC BY 4.0、MIT、ODbL、OFL、仓库临时输入与 citation-only 处理。独立法律意见、独立逐文件审计和商标检索仍为 0，不冒充外部专业结论。
- 新增双语实质等价记录与数据缺口关闭登记：投稿方可控的字体、越界、来源新鲜度、权利清单和双语审校已经闭合；官方 polygon/CAD/控规、现场审计、责任接收、预算、批准、真实复测和独立清权继续保持 unknown/0，且逐项记录责任来源、触发器和禁止替代物。
- 全页接触表进一步发现旧构建器的 CJK cmap 让中文版页眉/页题/页脚显示成错误汉字；改用 OFL 静态字面生成本地 2× 透明文字层，四份 PDF 保持 14+14 与 8+8 页并通过两次新进程字节一致构建。最终 SHA-256：中文 A3 `8f25771d6b943458805cf4bfc7db8038c5c5ea281d546352538da0f6076c93a5`、英文 A3 `4c0f273492f21c398904f7ff904c7354c996ce5a8cbaabed6bb28b19e6f3fee4`、中文 A0 `5fbc7f86c920cff1f3064fa81f4285ac2d9e5f2c343d0c3d32b3d9b2461ba0b8`、英文 A0 `4472306577021d01b80a34ba2a0efb4a94db4b4d7adbd73912c851b43444ca61`。

- Responded to the exact-head PR #3932 review by sharing one local Noto Sans SC WOFF2 subset across both report and visual counterparts. It covers the complete four-HTML character union and symbols; clean Chromium screenshots show no CJK tofu while the package remains offline, script-free and remote-font-free.
- Rebounded the English `site-overview` header, explanatory copy and panel heading, then rebuilt the English PNG and the A3/A0 outputs that cite it. No spatial fact, count or frozen geometry changed.
- Removed the duplicated Chapter 13 cue in both proposals while preserving all 13 formal chapters, figure positions and evidence boundaries.
- Narrowly refreshed `CASE-22AT` and `CASE-KINGS-CROSS`. The Barcelona City Council page is accessible; the former King's Cross workspace URL remains 403 and is replaced by an accessible public-consultation page from the same project operator. Both remain background comparisons only.
- Added a contributor rights decision for every current distribution path across CC BY 4.0, MIT, ODbL, OFL, repository provisional input and citation-only classes. Independent legal advice, independent file-level audit and trademark search remain zero.
- Added material bilingual-equivalence evidence and a data-gap closure register. Contributor-controlled typography, clipping, source freshness, rights inventory and bilingual review gaps are closed; official polygons/CAD/controls, field audit, accepted responsibility, budget, approvals, real retest and independent clearance remain unknown/zero with named source, trigger and invalid substitute.
- Full-page contact sheets exposed an additional legacy CJK cmap defect in Chinese page headers/titles/footers. Local 2x transparent text layers generated from OFL static faces replace that faulty mapping. The four PDFs retain 14+14 and 8+8 pages and match byte-for-byte across two fresh-process builds. Final SHA-256: ZH A3 `8f25771d6b943458805cf4bfc7db8038c5c5ea281d546352538da0f6076c93a5`; EN A3 `4c0f273492f21c398904f7ff904c7354c996ce5a8cbaabed6bb28b19e6f3fee4`; ZH A0 `5fbc7f86c920cff1f3064fa81f4285ac2d9e5f2c343d0c3d32b3d9b2461ba0b8`; EN A0 `4472306577021d01b80a34ba2a0efb4a94db4b4d7adbd73912c851b43444ca61`.

## v58.0 - 2026-08-24

**终稿收敛重建 / Final Convergence Rebuild**

- 从 canonical `main@37f5541dfab74d7f89aa0f57bf1c64ab542b036b` 建立新分支；前序 PR #3904 已关闭并由本轮替代，同包无其他开放 PR，开工树洁净。
- 修复前基线写入 `visual/assets/convergence-baseline.json`：156 个路径、23,720,803 字节、双语正文各 640 行、四份 PDF 共 44 页、9 个可选媒体路径；九份 geometry 与 `metrics.json` 的 Git-blob SHA-256 被锁定。RED-01—04 是投稿方编辑/包审查，不是公众反馈、专家意见、现场观察、审批或评审结果。
- 权利与来源不再用互相矛盾的总开关表达。`report/copyright_statement.md` 完整记录投稿方内容 CC BY 4.0、代码 MIT、OSM ODbL、Noto Sans SC OFL 与第三方排除；48 条来源保留中央正式/临时/背景、投稿方自采或包内自编身份。独立法律意见、逐文件独立权利审计和商标检索仍为 0，不冒充专业结论。
- 清退 9 个非必要模型媒体路径与 10 个旧漫游/样式/重复入口。新增双语普通生活、四态和专业交接三组原创静态 SVG/PNG；visual 收束为 6 个导航、6 个可见段落、0 JavaScript、0 远程资源、0 autoplay，并显式覆盖总览、三层范围、重点区、用地、交通、蓝绿、建筑、更新项目、AI 场景、指标、任务、自检和假设。
- 仅把既有 `JZ-05 × SCENE-011 × T-02` 设为 pre-G1 专业核验候选。其 10 个合成回放、10 个决策匹配与 4/4 停止恢复分支不升级成熟度；H01—H07 任一缺失、拒绝或过期均保持 G0 / NO-GO，现实服务、现场测试、批准、采购、责任接受与恢复时长均为 0 或 unknown。
- 四份 PDF 不增页，保持 A3 14+14、A0 8+8，共 44 页。首次逐页 QA 发现页眉/页脚字体子集 glyph ID 错位，修复后重建；空白页、替换字形与加密页均为 0。两次新进程逐文件字节一致：中文 A3 `8c176a11e728495e95e701ba45d0df47c610836fe00ce53c5be3fca1c3bfcec5`、英文 A3 `c4b08b805115eed429dc632d8caf7912bd2b9e0c90e0f51447332c1506d72828`、中文 A0 `186ee3983dade183dce138472d6708d36c8350d45200c267bc57a940f807c910`、英文 A0 `c03f457c268191e313ea3d73c8e188074d310ac30a97f7671a72ab7428d2cfcb`。
- 最终树保留 148 个路径，双语正文各 642 行。十个冻结对象（九份 geometry 与 `metrics.json`）SHA-256 与基线 10/10 一致；12/8/3/36、唯一“双轨京张”、三处不可互换原型、JZ-AIOS、G0—G3、四轴、三载体、NO-GO、provisional、现实结果 0、完整非 AI 路径、故障只停验证叠层、恢复非授权/批准/G1 与专业否决全部冻结。
- T-02 为 10/10 exact、4/4 停止恢复分支、13/13 控制项，模型/网络/现实服务调用均为 0。严格评分、空间、视觉、专业、marked self-check、participant preflight、manifest、作者与范围检查绑定最终 exact head；临时边界警告按真实性要求保留。

- Built from canonical `main@37f5541dfab74d7f89aa0f57bf1c64ab542b036b`; closed PR #3904 is replaced, no competing package PR existed, and the start tree was clean.
- The RED baseline records 156 paths, 23,720,803 bytes, 640 lines in each proposal, 44 PDF pages, nine optional media paths and ten frozen geometry/metrics blob hashes. The four findings are contributor editorial/package audits, not public feedback, expert opinion, field observation, approval or a jury result.
- Component rights are explicit: CC BY 4.0 for contributor content, MIT for contributor code, ODbL for OSM derivatives, OFL for the embedded Noto Sans SC subset, and third-party exclusions. Forty-eight sources retain their central or package-local governance status. Independent legal advice, file-level audit and trademark search remain zero.
- Nine optional model-media paths and ten obsolete walkthrough/style/redundant entrances are removed. Three bilingual original static SVG/PNG families carry ordinary life, four states and professional handoff. The visual has six navigation items, six visible sections, zero JavaScript, zero remote resource and zero autoplay.
- Only `JZ-05 × SCENE-011 × T-02` is named as a pre-G1 professional review candidate. Any missing, rejected or expired H01-H07 item keeps G0 / NO-GO; no field result, approval, procurement, accepted duty, duration or G1 is claimed.
- Four PDFs keep 14+14 A3 and 8+8 A0 pages. Full-page QA exposed and repaired a subset-glyph mapping defect. The four byte-identical hashes are recorded above; blank, replacement-glyph and encrypted pages are zero.
- The final tree retains 148 paths and both proposals have 642 lines. All ten frozen geometry/metrics hashes match baseline. T-02 is 10/10 exact, 4/4 stop/recovery and 13/13 controls with zero model, network or real-service call.

## 历史索引 / Historical index

为保持人读可用并满足 Markdown 256 KiB 上限，v56.0—v2.4 的重复长篇中英记录在 v58 收束为索引。完整原文仍在本轮基线提交 `37f5541dfab74d7f89aa0f57bf1c64ab542b036b` 的 `changelog.md` 中，可逐行恢复和比较；本索引不改变当时事实、边界或提交 SHA。

To keep the log human-readable and below the 256 KiB Markdown gate, repeated bilingual prose for v56.0–v2.4 is compacted into this index. The complete prior text remains recoverable at baseline commit `37f5541dfab74d7f89aa0f57bf1c64ab542b036b`; this index does not alter historical facts, boundaries or commit SHAs.

- 2026-08-23: v56.0 — 已批规划语境对位与前台图件去重。
- 2026-08-21: v55.0 — 海淀日常证据化与前后台压缩；v54.0 — 空间裁决前置与前台去元叙事。
- 2026-08-20: v53.0 — 评审图集完整性与定页出版终审；v52.0 — 公共地面详细设计图集；v51.0 — 人尺度行动剖面；v50.0 — 终稿证据缺口关闭；v49.0 — 城市代谢与退出成本。
- 2026-08-19: v48.0 — 最终预检与提交冻结；v47.0 — PDF 出版终审；v46.1/v46.0 — 证据新鲜度与现场对位；v45.0 — 视听真实性；v44.0 — 可访问公共信号。
- 2026-08-18: v43.0 — 实施移交矩阵；v42.0 — 故障治理写回；v41.0 — 非 AI 同任务服务蓝图；v40.0 — 冷读修复。
- 2026-08-17: v39.0 — 冷读基线；v38.0/v37.0 — 前序终稿链收束。
- 2026-08-15: v36.0—v22.0 — 权利、专业交接、维护、失败、气候、公共利益、可逆构件与出版多轮深化。
- 2026-08-14: v21.0—v19.0 — 终稿视觉、证据与双语质量深化。
- 2026-08-13: v18.0—v12.0 — 普通生活、四态、三处原型、视觉与移交合同深化。
- 2026-08-12: v11.0—v5.0 — 运营、场景、文化、产业、AI 基础设施与空间系统深化。
- 2026-08-11—10: v4.0—v2.5 — 早期方案与正式包结构演进。
- 2026-08-09: v2.4 — 初始正式化记录。

所有历史轮次均受当时仓库规则与其记录的 provisional/G0/rights 边界约束；较早的“就绪”表述不得覆盖 v58 当前分层许可、来源治理、现实结果 0 与 H01—H07 未接受状态。
