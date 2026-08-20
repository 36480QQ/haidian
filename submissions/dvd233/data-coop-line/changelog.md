# 方案迭代记录

## v1.4 - 2026-08-20

P1-02 Dazhongsi rehearsable MVP / 大钟寺可演练 MVP

- Baseline / 基线：从 `upstream/main` `0b9d540e8a2a56d525b56ab243d9d9e9764fba0e` 建立干净投稿分支 `codex/data-coop-line-key-area-mvp-20260820-v2`。此前冻结点 `d1ff9415abb4b0d916757f65658e7d77f5c91697` 之后的主线包含 `scripts/render_proposal_html.py` 及其测试，属于相关 helper，因此迁移到新基线并重跑生成与完整门禁；新旧 helper 生成的中英报告 SHA-256 完全一致，未为其他投稿变化重生成图件、PDF 或 manifest。
- Reason / 原因：上一轮 PR #3543 的维护者 intake 为 79/100，主要完成证据一致性；Issue #2955 要求城市设计不能停留在品牌叙事，同行 PR #3549 以可量测空间路径和演练逻辑获得 89/100。故本轮只选择一个能闭环的空间—运营样板，不扩展许可、数据使用或实施承诺。
- Before → After / 修正前后：正文把 `SCN-05` 归于大钟寺，但 GeoJSON 点位 `[116.3508, 40.013]` 实际落在北侧临时重点区且没有重点区和停机字段；现修正为 `[116.351, 39.946]`，位于 `PROV-KEY-003` 与 `BLDG-006` 概念测试基底内。`SCN-05 / 09 / 10` 统一挂接 `DAZHONGSI-MVP-01`，形成用途票、撤回回执、公共回报三阶段，并分别声明至少三项硬停止条件。
- Spatial evidence / 空间证据：EPSG:4548 复算得到临时重点区 `720,454.219 m²`、两处可逆房间测试基底 `13,361.508 m²`、公共回执空间 `32,739.258 m²`、临时范围内两条概念线网联合长度 `1,614.218 m`；3/3 节点具备人工复核与无数据等价字段，但这仍是设计目标而非已观测绩效。
- Carriers / 载体：同步 GeoJSON、metrics、设计深度/合规矩阵、假设、中英 Markdown 与派生报告 HTML；新增大钟寺“回执轨”双语离线段，以本地 Pillow/pypdf 构建步骤重绘双语重点区图，并只替换四份 PDF 中对应的重点区栅格。由于证据签名覆盖全部图层输入，十张 PNG 与四份 PDF 统一重签，其余八张图的像素内容不变；冻结 validator 不允许在 `visual/assets` 发布 Python，因此生成器不进入投稿包。
- Verification / 验证：故意在旧载体上刷新快照后，一致性审计精确报出 10 张图、4 份 PDF、2 份派生 HTML 和 manifest 过期；修正后证据签名为 `c880c438924399d40267391551669d937dcfc5e144850eb511a45bbf024c4a52`。最终 manifest、自检、preflight、PDF/HTML 视觉 QA 结果在发布前门禁完成后记录。
- Boundary / 边界：`geometry/key_areas.geojson` 与所有官方/共享文件不变；站口、路权、权属、现状建筑、文保、市政、消防、无障碍、运营主体与实际两线绩效仍待正式证据和实地演练，任一前置失败即迁移、缩减或停止原型。

## v1.3 - 2026-08-20

P0 source-hash correction / 场地证据源哈希纠偏

- Baseline / 基线：本轮从 `upstream/main` `fae639c40a0b51de971ed4cd98526351d07cbb74` 建立干净分支 `codex/data-coop-line-evidence-consistency-20260820`。后续 main 先后移动到 `b8ddfc8e10b27a3be9629d24e0317f4deaf5cfe1` 和 `58af9968147491c1b0f264890074f1235ceccdaa`；这两次相关路径核对均为 0。PR 创建时实际 base 为 `7019821bd606d020d0e8ca3b0120d2d312f1ab4d`，其中唯一相关路径是同行读取 helper `scripts/read_peer_proposals.py` 的异常 `Content-Length` 容错，不触及本稿、Skill、brief、schema、validator 或投稿门禁；其 2 项专项测试通过。因此不重建冻结点，也不生成无关图件或 PDF。
- Finding / 发现：P1-01 合并包的 `site-evidence-register.json`、`sources.json` 和 `constraints.geojson` 中四个 SHA-256 不对应其声称冻结的 `ce2c6bcee348accc3c354f585c9ad45e39ff2db7` Git blob。干净 sparse 工作树首先因未检出 `data/source_registry.json` 得到 13/17；补齐只读来源后证明四个哈希均错，而非上游内容后续漂移。
- Correction / 纠偏：直接对 `git show ce2c6b:<path>` 返回的原始 blob 字节计算 SHA-256，并同时确认这四个文件在 `ce2c6b` 与当前 main 字节相同。纠正后的公告快照、临时边界、边界依据与 source registry 哈希分别为 `158203872171…9cc3`、`0b9ae36bae6e…2306`、`295869f7aafe…4910` 和 `4784e80d2d36…1c66`。
- Scope / 范围：只同步机器台账、来源与约束缺口记录、中英正文哈希摘要、派生报告 HTML、changelog、manifest 和 self-check。冻结来源提交 `ce2c6b`、四组 geometry 映射、0 个 official-control feature、6 类缺口、许可边界、方案几何、指标、图件与 PDF 均不变。
- Boundary / 边界：这是证据完整性修复，不是官方精度提升，不新增来源、许可、数据用途、空间结论或实施承诺。

## v1.2 - 2026-08-20

P1-01 site provenance and verified control-data gap / 场地来源、许可与约束缺口可核验证据

- Baseline / 基线：场地证据最初冻结于 `upstream/main` `ce2c6bcee348accc3c354f585c9ad45e39ff2db7`，对应来源哈希仍逐项匹配。发布前发现 main 已移动且 `scripts/validate_submission.py` 新增双语同字节提示，因此从最新 `upstream/main` `fcaf7a9fccb7d9ca875a6fc37329fb1454e7b375` 重建干净 worktree 与新分支 `codex/data-coop-line-p1-02-site-evidence-20260820`，移植聚焦修改，并以 `fcaf7a9fc` 的门禁完整复验；未把证据快照 SHA 伪改成较新的代码基线。
- Reason / 原因：旧包在 `sources.json` 中列出场地来源，但缺少发布 / 获取日期、冻结源哈希、许可 / 署名、allowed / prohibited uses、精度与替换触发器；`constraints.geojson` 的空集虽诚实合法，却没有跨文件 fail-loud 证明。主控原先把“非空 constraints”当验收条件；冻结版 validator 明确没有可引用的官方 / 清权控制几何时空集合法且优于造线，最新同行 `kenshin-ai-101/openline-100` 即使补到已批街区控规公开文字也因无 parcel/redline polygon 保持空集。故本轮纠正验收口径，不复制临时范围制造假约束。
- Before → After / 修正前后：场地来源从简短 `path + usage` → 发布者、日期、冻结 SHA、源哈希、CRS、许可 / 用途边界与禁用项；临时总体范围和三处重点区从“相信同源” → 4/4 geometry 精确匹配冻结源；官方控制缺口从单文件说明 → 6 类 locked-layer 缺口、替换规则、禁止代填项、机器台账与审计。`constraints.geojson` 仍为 0 feature，含义是“缺口已核验”，不是现实中无控制。
- Machine evidence / 机器证据：新增 `visual/assets/site-evidence-register.json` 与 Node built-ins-only `site-evidence-audit.js`。审计固定公告快照、临时边界、依据说明与 source registry 四个 SHA-256，核对 4 组 geometry 映射、0 个 official-control feature、6 类缺口和三条核心来源的 allowed / prohibited uses；当前 18/18 PASS，任一漂移显式失败。
- Carriers / 载体：同步中英 Markdown、派生 HTML、离线 visual 的场地证据区、`site-overview` / `key-areas` 双语图页脚、四份 PDF 对应页面、来源 / 假设 / constraints、版权说明、manifest 与 self-check。空间面积、比例、场景、设计 geometry 与其余三组核心图不变，不制造无关载体 churn。
- Peer evidence / 同行证据：PR #2734 的 site-grounding register 与 PR #2736 的 machine-readable reviewer evidence 证明结构化交接的评审价值；`openline-100` 的控规文字 / 空 geometry 分线证明“文本获批不等于可写 polygon”。只借鉴证据分层与 fail-loud 思路，未复制任何同行文本、schema、图件、geometry 或媒体。
- Boundary / 边界：未新增外部来源、OSM geometry、许可或数据使用范围；brief 中 OSM 读数仍是背景，不进入本包控制 geometry。官方 / 清权控规、文保、道路红线、权属、轨道、蓝线或市政 geometry 到位后，先登记发布者、日期、版本、CRS、许可、转换与哈希，再整体重建 geometry → metrics → figures → HTML → PDFs。

## v1.1 - 2026-08-15

P0 evidence and scenario consistency / 指标与场景证据一致性

- Baseline / 基线：证据修订始于 `upstream/main` `683c627c4b2071c13ebc7f569cb4e56d2bc69aad`；发布前持续快进并最终核对至 `c55ef181cbfd1c636b04a644d17c64eaf464d656`。`c8f13bb…c55ef181` 的 7 个提交更新其他投稿并强化空 manifest 审计；目标投稿、Skill 与 brief 无 upstream 变化。强化后的校验器已纳入本轮复验，clean focused branch 为 `codex/data-coop-line-evidence-consistency-v4`。
- Reason / 原因：PR #2540 合并包中的 GeoJSON 与 `metrics.json` 已是新复算结果，但中英正文及其派生 HTML 仍保留旧指标；正文还把场景 01—03 标为产业测试，而 `public_space.geojson` 和离线展示均把 `SCN-04`—`SCN-06` 定义为产业测试。旧文本会让评审者得到与机器证据相反的结论。
- Single source / 单一事实源：投稿 `geometry/*.geojson` 是空间事实入口；面积统一投影到 EPSG:4548 后做多边形联合复算，`metrics.json` 保存派生指标，`visual/assets/evidence-snapshot.json` 保存输入哈希、复算结果、12 个场景注册表与跨载体签名。
- Before → After / 修正前后：
  - building footprint / 建筑基底：`310,807.184 m²` → `40,063.344 m²`;
  - green space / 绿地：`12.3423%` → `2,384,747.221 m² / 20.8953%`;
  - public space / 公共空间：`7.3281%` → `98,164.982 m² / 0.8601%`;
  - industry tests / 产业测试：narrative cards `01–03` → GeoJSON registry `SCN-04` Synthetic-Data Benchmark Cell, `SCN-05` Temporary-Use Licence Cell, and `SCN-06` Controlled-Compute Test Room.
- Carriers / 载体：同步中英 Markdown、派生 HTML、离线 visual 指标卡、双语指标图、A3/A0 PDF、manifest 和持久化 self-check；其余四组核心图视觉内容不变，只写入同一证据签名与发布核验基线以防漂移。双语报告另修复 390 px 下长路径代码造成的横向溢出。PDF 不只更新页脚：A0 第 5 页和 A3 第 6 页的内嵌指标栅格已逐像素替换为当前双语指标图。
- Verification / 验证：`visual/assets/evidence-consistency.js` 在旧载体上先失败，修复后 PASS；发布准备时按最新 main 重签为 `c880c438924399d40267391551669d937dcfc5e144850eb511a45bbf024c4a52`。EPSG:4548 联合面积复算、12 个场景注册表和全载体检查 PASS；审计器新增无额外仓库依赖的 PDF 内嵌 RGB 栅格校验，能阻止只更新 PDF 元数据而保留旧指标图。四份 PDF 共 24 页以 120 dpi 重渲染并逐页检查，双语标题、数值、页脚、留白和图面无裁切、重叠、乱码或旧 SHA；四份 HTML 在 1440 px 与 390 px 下无坏图、远程资源或横向页面溢出。
- Preflight / 预检：原工作区的管理 DOCX 和不可写远端问题通过新建 clean participant worktree、仅修改投稿目录、配置可写 fork 解决；不删除管理材料、不弱化 scope 检查。ready-package manifest refresh、持久化 self-check 四门、普通 preflight 与 `--check-push` 均 PASS；唯一警告是工作区并非 blobless partial clone，不影响投稿内容或上传权限。
- Remaining boundary / 剩余边界：所有数值仍是临时几何下的概念设计量；官方边界、控规、现状建筑、权属、道路、市政、文保与生态资料到位后必须整体重建拓扑并复算，不能把本次一致性修复理解为官方精度提升。
