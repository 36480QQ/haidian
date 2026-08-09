# 方案迭代记录

本文件记录「京张·智缝带 JingZhang AI Stitch Belt」方案的版本演进。

## v0.1 - 2026-08-09

### 新增

- **概念确立**：确定方案主名「京张·智缝带 JingZhang AI Stitch Belt」与双主线（京张缝合 + AI 自主创新）。
- **proposal.md**：13 章节 formal 完整稿，含 front matter、统一边界声明、三层范围对照表、命名体系与 Logo 方向、6 个全球案例（含非照搬边界声明）、一脊两带三区两翼空间结构、三区详细设计（七维结构）、12 张 AI 场景卡（含 4 张产业测试验证场景）、5 类用户画像、3 个 AI 朝圣地标、年度活动与运营机制、指标复算与风险合规。
- **机器可读证据**：
  - `metrics.json`：已知面积 known + 控规项 unknown/null 纪律；EPSG:4548 复算。
  - `compliance_matrix.json`：23 条全覆盖（17 official + agent.1-6）。
  - `standard_matrix.json`：5 mandatory（addressed）+ 1 data_gap。
  - `design_depth_matrix.json`：15 深度项全 complete。
  - `sources.json` / `assumptions.json` / `agent.json`。

### 边界声明

- 本版本基于 provisional 边界：`package_state` 将在 finalize 后转为 ready_for_review。
- 全部空间落地均为概念建议，待官方边界与控规发布后复算。

### 模型披露

- agent: lugoudu (ZCode)，model_family=glm，model_detail=GLM-5.2。
