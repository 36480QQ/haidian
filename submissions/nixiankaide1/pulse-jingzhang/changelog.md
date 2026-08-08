# 方案迭代记录

## v0.1 - 2026-08-08

首次提交「京张起跑线 / JINGZHANG START LINE」formal 方案包。

- 方案概念：从百年铁路起点到全球 AI 运动健康活力带；AI×运动健康活力城市实验室定位
- 差异化：避开已有 200+ 方案的「轴/廊/脉/平台」叙事，以运动健康主线 + 起跑线命名体系破题
- 成果：
  - proposal.md 13 章节（中文主稿，约 1.08 万汉字，238 处证据引用）
  - 9 个 GeoJSON 设计图层（land_use 44 分区零缝隙零重叠，EPSG:4548 复算）
  - 8 个 JSON 证据文件（24 指标 / 8 假设 / 10 来源 / 23 合规 / 6 标准 / 15 深度）
  - 5 张设计图 + 离线展示页 + A3 文册 10 页 + A0 展板 4 页
  - 12 场景卡（含 3 测试验证）、6 画像、6 案例、4 朝圣地标、3 期实施
- 自检：self_check PASS（formal-review-ready）；participant_preflight PASS
- 边界：全部几何为 provisional（official polygon 发布后整包复算）
- PR：open-city-ai/haidian#652

### 待复核事项

- [ ] official 边界与控规指标发布后：重算 site/key areas/land use/roads/green/public/buildings/phasing 与全部面积类指标
- [ ] 补英文译稿（proposal.en.md 及 HTML/图件/PDF 英文版）
- [ ] 跟踪 PR #652 的 CI 与维护者评审反馈，纳入下一轮迭代
