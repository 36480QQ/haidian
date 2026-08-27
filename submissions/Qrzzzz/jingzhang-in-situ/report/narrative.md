# 京张在场 / Jing-Zhang In Situ

“京张在场”是一项面向百年京张 AI 创新带的概念性城市设计建议。主命题是把 AI 变成三处公众可见、可人工接管、可验证、可撤回的城市界面。“人在场、证据在场、责任在场”是共同评价准则：公众能够理解和申诉，证据与失败可追溯，责任角色能够切换人工、低技术替代或撤场。

固定空间语法是“一条在场脊柱＋三处在场原型＋十二条候选责任横断面＋一个有期限、可逆的首用试验”。京张铁路遗址公园是南北脊柱；众智园、北京 AI 原点和大钟寺分别承担验证、人工匹配转译和公共试用；中关村与小月河两翼是候选支撑。外部区域仅为待授权接口，不代表现有合作。

成果以 SC01、SC05、SC10 三旗舰＋九支持组织十二场景，同时保留 TVS-1—3；场景归属按 ID 明列为众智园 SC01/02/03/04、AI 原点 SC05/06/07、大钟寺 SC09/10/11、脊柱跨区支持 SC08、三原型跨区支持 SC12。六个 agent 的 31 项 required outputs 已逐项锚到章节、图页、表格或结构化文件。

T06 前台以 AP1—AP7 映射后台 IM01—IM13；13 个逐项专业对象在 `design_depth_matrix.json#/items/11/implementation_projects` 保存责任、依赖、定性成本、证据/维护/评价、人工接管和停止/退出。唯一首用试验绑定既有 SC10＋IM06，期限由获授权角色书面设定，届满或失败即撤场；它不新增场景或项目。所有行动以正式边界、现场调查、权属、安全、许可和运营条件为 Gate，不构成政府日程、资金、招商或工程承诺。

中文压缩只保留两个可直接复算口径：相对 `upstream/main` 基线提交 `70cd369cbb80d6b5da743422a3d0aa2d3a98e333` 的 `proposal.md` blob `e03228ed0c29f56c569cd289408fd40cdfd98ebd`，本稿 blob `68cce229de863cdf2e8e482eb0e3bfc98abfef44` 的全正文汉字为 7502→6058（-19.25%），正文行汉字为 5791→4431（-23.48%）。完整归一化、正则、公式与代入式见 `compliance_matrix.json#review_navigation.compression_audit`；未固化算法的 21.94% 口径已删除。

当前 SITE 与 KEY_AREA 是临时粗略约束。正式 polygon、控规、逐栋现状、道路、无障碍、市政、文保和真实需求数据仍待补齐；临时面积和比例只能用于方案内复算。官方资料到位后，九类图层、指标、F01—F11、HTML 和 PDF 必须统一更新。

---

Jing-Zhang In Situ is a conceptual urban-design proposal for the Centennial Jing-Zhang AI Innovation Belt. Its thesis is to make AI visible, human-takeover-ready, verifiable, and withdrawable at three urban interfaces. “People present, evidence present, responsibility present” is the shared test: people can understand and appeal, evidence and failure remain traceable, and accountable roles can switch to a human or low-tech service or remove the intervention.

The fixed spatial grammar is one in-situ spine + three in-situ prototypes + twelve candidate responsibility cross-sections + one time-bounded reversible first-use trial. The heritage park is the north–south spine. Zhongzhiyuan validates, Beijing AI Origin translates through human matching, and Dazhongsi hosts public trials. The two wings and external regions remain candidate interfaces pending evidence and authorization.

The twelve scenarios appear as three flagships—SC01, SC05, and SC10—plus nine supports, while TVS-1–3 remain visible. Canonical ownership is enumerated as Zhongzhiyuan SC01/02/03/04, AI Origin SC05/06/07, Dazhongsi SC09/10/11, cross-area spine support SC08, and all-prototypes cross-area support SC12. All 31 required outputs for six agents have exact section, figure, table, or structured-file anchors.

AP1–AP7 preserve all backend IM01–IM13. Thirteen per-item professional objects at `design_depth_matrix.json#/items/11/implementation_projects` retain roles, dependencies, qualitative cost, evidence/maintenance/evaluation, Human Takeover, and stop/exit. The only first-use trial uses existing SC10 + IM06, receives its time limit in writing, and withdraws at expiry or failure; it creates no new scenario or project and claims no measured performance.

Only two directly reproducible Chinese-compression measures are retained. Against `proposal.md` at upstream base commit `70cd369cbb80d6b5da743422a3d0aa2d3a98e333`, blob `e03228ed0c29f56c569cd289408fd40cdfd98ebd`, the measured head blob `68cce229de863cdf2e8e482eb0e3bfc98abfef44` changes all-body Han characters from 7,502 to 6,058 (-19.25%) and prose-line Han characters from 5,791 to 4,431 (-23.48%). The full normalization, regex, formula, and substitutions are stored at `compliance_matrix.json#review_navigation.compression_audit`; the former 21.94% measure is removed because its tokenization contract was not persisted.

SITE and KEY_AREA remain provisional rough constraints. Official polygons, regulatory controls, building conditions, transport, accessibility, municipal, heritage, and observed-demand data are still missing. When authoritative data arrives, all spatial layers, metrics, F01–F11, HTML, and PDFs must be recomputed together.

## Audit measurement / 审计量测

- Definition / 定义：`final_git_blob_payload_bytes` is the sum of Git blob sizes in the final staged tree under this submission, excluding only the recursive audit envelopes `manifest.json` and `self_check.json`. It is independent of Windows checkout conversion; text generators write UTF-8/LF and this worktree explicitly sets local `core.autocrlf=false`. / `final_git_blob_payload_bytes` 是最终暂存树中本投稿所有 Git blob 的字节和，仅排除会自指的审计封套 `manifest.json` 与 `self_check.json`；它不受 Windows 工作区换行转换影响，文本生成器固定写 UTF-8/LF，且本工作树本地明确设置 `core.autocrlf=false`。
- Included / 包含：56 payload blobs, including bilingual Markdown, matrices, GeoJSON, F01–F11 pairs, four HTML files, four PDFs, local font assets, and the reviewable generator source. / 56 个 payload blob，包括双语 Markdown、矩阵、GeoJSON、F01—F11 双语图、4 份 HTML、4 份 PDF、本地字体资产和可审阅生成源。
- Measurement point and formula / 测量时点与公式：after final regeneration and content repair, stage the submission, create the candidate tree with `git write-tree`, then sum the object sizes reported by `git ls-tree -rl <tree> -- submissions/Qrzzzz/jingzhang-in-situ`, excluding the two envelopes. The separate final manifest audit covers all 58 package files and proves zero missing, undeclared, or mismatched hashes. / 最终重建和内容修复后暂存投稿，以 `git write-tree` 生成候选树，再对 `git ls-tree -rl <tree> -- submissions/Qrzzzz/jingzhang-in-situ` 报告的对象大小求和并排除两份封套；独立最终 manifest 审计覆盖全部 58 个包文件，并证明缺失、未登记和哈希不符均为零。
- `payload_blob_count = 56`; `final_git_blob_payload_bytes = 11167768`. This fixed-width value was replaced from the final candidate tree before manifest refresh and commit; no physical-checkout byte total is claimed. / 该定宽值已在 manifest 刷新和提交前由最终候选树实测替换；不再声称物理工作区字节总量。
