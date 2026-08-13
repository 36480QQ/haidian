# 方案迭代记录

## v0.1 - 2026-08-13

### 本次完成

- 确定聚焦方向：AI 公共空间与朝圣地标（agent.4）。
- 确定方案命名与核心概念：京张朝圣带（三殿·一路·一铭文·一护照）。
- 完成九层几何生成（site_boundary / key_areas / land_use / buildings / roads / green_space / public_space / phasing / constraints），land_use 对 site_boundary 无缝无重叠分区，面积以 EPSG:4548 投影复算。
- 完成 metrics.json（site_area_sqm、key_area、green_ratio、public_space_ratio、building_density、road_ratio 等为 known；floor_area_ratio、building_height_m、green_space_per_capita_sqm 为 unknown 并注明原因）。
- 完成中英双语提案 proposal.md / proposal.en.md，含证据标记（source/standard/depth/data/metric）。
- 生成五张展示级图件（site-overview / land-use-structure / key-areas / mobility-bluegreen / metrics-evidence，语言 neutral）。
- 生成 A3 文册与 A0 展板（中英双语各一）。
- 生成 report/proposal.html 与 report/proposal.en.html。
- 完成 visual/index.html 与 visual/index.en.html（完全离线，data-metric/data-value 与 metrics.json 一致）。
- 更新 compliance_matrix.json / standard_matrix.json / design_depth_matrix.json / assumptions.json / sources.json。

### 待办与开放问题

- 边界为 provisional 临时几何（official_boundary=false），替换官方红线后需重算全部图层与指标。
- 控规、道路红线、权属、市政、文保、工程条件等资料缺失项已在 assumptions.json 登记，待正式数据补齐。
- 全部校验门（finalize / self_check / participant_preflight）通过后再提交 PR。

### 反馈记录

- 无（首版提交）。
