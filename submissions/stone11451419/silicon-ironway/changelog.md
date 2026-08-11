# 方案迭代记录

## v1.0 - 2026-08-11

首次正式提交（First formal submission）。

### 变更内容

- 主题：京张智轨 SILICON IRONWAY —— 一条百年铁轨的 AI 自主创新带（一脊三站两翼）
- 生成全部 9 个几何图层（boundary / key areas / land use / buildings / roads / green space / public space / constraints / phasing），用地分区完整覆盖临时边界（gap < 30㎡）
- 计算 24 项指标（metrics.json）：空间指标在 EPSG:4548 下从提交几何复算；管控指标记为 unknown（待正式控规条件）
- 撰写中英双语方案正文（proposal.md / proposal.en.md，v2 格式 + bilingual contract v1）
- 填充 compliance_matrix（23 项必答）、standard_matrix（9 项）、design_depth_matrix（15 项 complete）、assumptions（7 条）、sources（22 项）
- 生成 10 张图纸（5 张 × 中英双语）、A3/A0 图纸 PDF（4 份）、离线可视化页面（visual/index.html + index.en.html）
- 渲染 report/proposal.html + proposal.en.html（离线阅读版）
- 边界说明：全部几何基于仓库临时粗略边界（provisional constraint），正式 polygon 发布后须整链重算

### 待跟进（Pending follow-up）

- 官方 SITE_BOUNDARY / KEY_AREA polygon 发布后：替换几何并重算全部指标、图纸与 HTML
- 现状建筑、权属、市政管线、文保控制线等资料到位后：更新拆改留、市政与风貌章节
- 持续关注上游 Issues/PR 与评审意见，按反馈迭代
