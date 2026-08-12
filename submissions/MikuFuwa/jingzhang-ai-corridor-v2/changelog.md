# 方案迭代记录

## v2.3 - 2026-08-12

### 改动摘要（哈希验收通过后写入）

- **用地形态**：`land_use` 重建为街坊/功能单元拼贴（median aspect≈3.4，否决通长竖向彩带）；units=50。
- **建筑形态**：三核簇群 + 脊缘界面；buildings=177；核密廊疏叙事。
- **慢行**：命名断点 B1/B2/B3 + 站城口袋提示 + 机器人可回退试验段。
- **真重渲**：site-overview / land-use-structure / key-areas / mobility-bluegreen / metrics-evidence 及 en 副本；A0 8 板、A3 16 页；overview.svg；**五图 SHA-256 相对 v2.2 均已变化**（见包外 `_build_v23/render_veto_report.json`）。
- 指标：green_ratio=0.257067；public_space_ratio=0.095189；building_density=0.015007（概念）；FAR unknown；confidence medium。
- manifest 保持 schema 0.2.0；agent_detail 更新为 v2.3。

### 硬规则执行说明

- 先几何与重渲，后人眼/哈希否决，**最后**写本 changelog。
- 未宣称未完成的官方红线/控规指标。

### 暂未采纳或待复核

- 真实测绘底图与 official polygon 仍缺。
- 人类 T2 专业红队未外部签字。
- GitHub CI 以 push 后 submission-validation 为准。

## v2.2 - 2026-08-11

### 改动摘要

- 几何二次结构化、图面 2.0、A0 八板/A3 十六页、renewal_projects、英文等义加深。
- 后续 **v2.2.1**：manifest schema 0.2.0（去 size、规范 role）以通过 CI。

## v2.1 - 2026-08-11

### 改动摘要

- 消灭空壳 A0/A3：重做 ≥7 板 A0 与 10 页级 A3 图文 PDF（含真地图嵌入）。
- 五张 figure 改为由 GeoJSON 投影的互异空间图；几何结构化与离线 visual；metrics medium + provisional。
