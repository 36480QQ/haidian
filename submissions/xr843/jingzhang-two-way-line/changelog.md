# 方案迭代记录

## v1.2 - 2026-08-10

- **Logo 落地为可缩放矢量图**：§3.2 此前只有文字描述的「双箭同轨」方向，现绘制为 `assets/two-way-line-logo.svg`（彩色）与 `assets/two-way-line-logo-mono.svg`（单色，`currentColor`）。两版几何一致，无文字、无外链、无未授权字体商标；离线展示页双语页首各引入一次。
- **对开协议从散文变为可复算契约**：新增 `visual/assets/twoway-protocol.schema.json`（班次凭证机读契约）、`twoway-runbook.json`（十二张真实班次卡 + 六个必须被拒的变异班次）、`run_twoway_tabletop.js`（Node 18+，无外部依赖的桌面推演）与 `twoway-tabletop-evidence.json`（本包记录的运行结果）。
- **闸门做了变异测试，不是摆设**：推演除检验十二张卡是否满足协议六条规则外，另要求六个变异班次各自被其对应规则拦下，否则同样判失败；实测把真实班次的运营主体清空、或把隐私红线翻转，脚本立即判红并以非零码退出。本包记录结果为 12/12 可排图、6/6 变异被拦下。
- **补全协议第三要素**：§6.2 的班次表原本只公布节点与上下行清单，而协议要求「节点、运营主体、上下行清单」三要素齐全方可排图。§6.3 新增十二张卡的运营主体与叫停主体指派表，依本方案自设的运行图管委会、三站乘务组、两台协调人架构编制，并明示全部为概念性运营建议、非既有机构或已批准的行政安排。
- 中英正文等义同步，`report/proposal.html` 与 `report/proposal.en.html` 已用 `scripts/render_proposal_html.py` 重新渲染。
- 未改动几何、指标数值、图纸与许可声明；未触碰其它投稿包、`submissions-data.js` 与 `gallery-publication.json`。

## v1.1 - 2026-08-10

- 持久化本包在当前 main 提交上的真实四门自检结果（deterministic validation / spatial review / visual packaging / professional evidence 均为 PASS），并写入 `review_status=formal-review-ready` 与 `manifest.validation_claim.readiness_contract=persisted-self-check-v1`。响应 #883 测得的存量缺口与 #807 的 readiness 契约。
- 证据由 `scripts/self_check_submission.py --mark-self-checked` 实跑生成并回读，内嵌各门原始报告；这是作者侧的可复现回放记录，不是独立背书，provenance 仍以受信 CI 或维护者重跑为准。
- 保留本包原有的六项包级自检（BOUNDARY_TRUST / KEY_AREAS_TRUST / LAND_USE_TOPOLOGY / METRIC_RECALC / VISUAL_STATIC / BILINGUAL_PAIRING）与四门规范化记录并存，使 `compliance_matrix.json` 的 `self_check_ids` 引用保持完整。
- 三条 `KEY_AREA_PROVISIONAL` 仍如实保留为 minor、非阻断提示：重点区为推定范围，不是官方红线，也不构成精确面积依据。
- 未改动几何、指标数值、图纸、正文结论或许可声明；未改动 `submissions-data.js`、`gallery-publication.json`，也未触碰其它投稿包。

## v1.0 - 2026-08-09

- 初版 formal 概念方案包：「京张对开 THE TWO-WAY LINE」。
- 自行推导街道贴合临时边界：以公告文字四至的 OSM 街道中线重建走廊多边形，EPSG:4548 下校准至公告 11.40 km²（偏差 +0.0006%）；三处重点区以公开轨道站点与文保单位位置锚定，面积校准至公告值 ±0.01% 内。
- 披露 maintainer 登记临时边界整体东偏约 600 米的对照发现（清华园车站旧址、遗址公园已建段、五道口/大钟寺站、古钟博物馆均落在其外），计划以 Issue 提交社区复核；本包与登记边界同为 provisional，非官方红线。
- 生成九层几何（189 块全覆盖用地分区，缺口约 658 m²；244 处概念建筑；14 条现状路网；明线 7.8 km；三期分期）与 29 项复算指标；spatial review PASS。
- 中英双语报告（proposal.md / proposal.en.md，v2 + 双语契约 v1）、五图双语十张、A3 文册与 A0 展板双语四册、离线 visual 双语两页。
- 十二班次场景卡（含三个产业测试验证）、六类画像、四处朝圣地标、七个全球案例、十四项更新项目、对开协议与运行图制度设计。
- 待办：向社区提交边界偏移 Issue；官方红线发布后整包重算。
