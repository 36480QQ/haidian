## 提交摘要
**方案名**: 开源京张：AI 场景之都
**GitHub 用户名**: Microbiosis
**主题**: AI 融合创新带（产业驱动）
**包类型**: professional_design_package
**自检状态**: **PASS** (deterministic / spatial / visual / professional evidence 全部通过)

---

## 评审快速指引

本 PR 建议按以下顺序评审：

1. **Executive Summary**（proposal.md 前 300 字）— 30 秒掌握方案核心
2. **核心差异化** — 三区两翼协同回路 + 3 张产业测试验证场景（SC-TEST-001~003）
3. **证据链完整性** — metrics.json 的 evidence_chain 字段直接链接 data/source/standard/depth
4. **合规覆盖** — compliance_matrix.json + standard_matrix.json + design_depth_matrix.json 三矩阵 100% 覆盖
5. **空间结论声明** — 所有 GeoJSON 均为 provisional，标注为「概念建议/参考方案」

---

## 设计核心

- **三处重点区协同**: 众智园(192ha, 全栈自主创新) / AI原点社区(104ha, 创新生态) / 大钟寺(72ha, 产业集聚)
- **三区两翼协同回路**: 中关村科技服务翼 + 小月河场景赋能翼
- **五层 AI 生态**: 基础层 -> 平台层 -> 应用层 -> 空间层 -> 运营层
- **10 张 AI 场景卡** (含 3 张产业测试验证 SC-TEST-001~003) + 5 类用户画像 + 3 处朝圣地标

## 交付内容

- proposal.md (618 行): 所有 9 章 + Executive Summary + Evidence Chain 附录
- geometry/*.geojson (9 层): site_boundary / key_areas / land_use / buildings / roads / green_space / public_space / constraints / phasing
- assets/figures/*.png (6 张): site-overview / land-use-structure / key-areas / mobility-bluegreen / metrics-evidence + ecosystem (备用)
- drawings/a3-booklet.pdf: 5 页 A3 方案文本
- drawings/a0-boards.pdf: 1 页 A0 总平面
- visual/index.html: 离线可视化仪表盘
- report/proposal.html: 完整离线 HTML 阅读版
- metrics.json: 核心指标复算 + evidence_chain 链接
- sources.json: 6 个来源（含 3 个 2025-2026 年官方产业数据源）
- compliance_matrix.json: 公告 1.3/1.4/1.5 + agent.1~6 覆盖
- standard_matrix.json: 全部 mandatory standards
- design_depth_matrix.json: 控规深度 + 规划综合实施方案深度

## 边界说明

所有空间结论基于 **provisional geometry** (brief/site-package/geometry/provisional_boundaries.geojson)，已明确标注官方 polygon 处于密码保护状态，待 2026-11-30 公开后重算以下核心指标：
- [metric:site_area_sqm] / [metric:key_area_count] / [metric:green_ratio] / [metric:building_footprint_area_sqm]

## 合规覆盖

- **Agent tasks agent.1~6** 全部覆盖（35+ 处 agent.* 引用）
- **compliance_matrix / standard_matrix / design_depth_matrix** 三矩阵 100% 覆盖
- 所有空间结论标注「概念建议/参考方案，不构成政府审定结论」

## 近期优化（v1.1）

- 新增 Executive Summary（300 字内核心结论）
- metrics.json 全部指标增加 evidence_chain 链接（data -> source -> standard -> depth）
- 补充 3 个 2025-2026 年官方产业数据源（海淀 AI 创新图鉴、2026 年计划、中关村论坛 AI 主题日）
- PNG 优化 + PR 描述结构化

## 致谢

感谢 @open-city-ai/haidian 提供的 open-city AI toolkit 与 agent 框架。
