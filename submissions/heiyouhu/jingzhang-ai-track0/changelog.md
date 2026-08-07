# 方案迭代记录

## v1.0 - 2026-08-07

- 基于仓库脚手架生成 formal 提交包，完成「京张智带 · 零号智轨（TRACK-0）」总体概念、命名体系、空间结构与机制亮点。
- 撰写中文正式方案 `proposal.md`（正文非空白字符约 1.5 万字），覆盖 13 个必选章节、5 张嵌入图、7 条来源、6 条标准、15 个设计深度项与 5 项 known 指标。
- 完成 geometry 图层：site boundary（provisional）、三处 key areas（provisional）、用地分区（9 类，无缝闭合）、建筑基底、道路中心线、绿地、公共空间、约束界面与三期实施范围；面积均按 EPSG:4548 投影复算。
- 生成 5 张核心图（总体概念/用地结构/重点区域/交通蓝绿/指标证据）、A3 文册（11 页）与 A0 展板（2 页）、离线展示页 `visual/index.html`。
- 运行 `render_proposal_html.py`、`finalize_submission.py`、`self_check_submission.py` 与本地校验；`package_state` 更新为 `ready_for_review`。
- 已知限制：site boundary 与 key areas 为 provisional，官方 polygon 发布后需整体复算；容积率等管控指标待官方控规。
