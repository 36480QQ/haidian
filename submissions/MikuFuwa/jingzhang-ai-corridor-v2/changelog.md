# 方案迭代记录

## v2.1 - 2026-08-11

### 改动摘要

- 消灭空壳 A0/A3：重做 ≥7 板 A0 与 10 页级 A3 图文 PDF（含真地图嵌入）。
- 五张 figure 改为由 GeoJSON 投影的互异空间图（总览/用地/三区/慢行蓝绿/指标证据），不再使用暗色卡片模板。
- 几何结构化：建筑 L/U/矩形混合基底；分级多段道路；加密绿/公空；constraints≥8；scenario_nodes 与三区 detail 资产（因 geometry 白名单，节点/详设 JSON 置于 `visual/assets/`）。
- 离线 visual：内嵌 SVG 真总图，指标 data-metric 与 metrics.json 对齐。
- 正文修复幽灵引用（eport/ssets/断 data 路径），中英等义加深；changelog 仅在落地后宣称完成项。
- metrics 全量按 EPSG:4548 重算，confidence 与 provisional 对齐为 medium。

### 采纳反馈

- 对照 v2 评审硬伤清单与专家升级 Plan（T1）执行，不重复自夸未完成项。

### 暂未采纳或待复核事项

- 官方红线 / 控规 / 权属 / 市政专项仍缺，FAR 等保持 unknown。
- 仓库不允许在 `geometry/` 新增文件名，故 scenario_nodes 与 detail_* 以 visual/assets JSON 交付并在正文披露。
- 人类专业红队（T2）未在本轮外部签字。
