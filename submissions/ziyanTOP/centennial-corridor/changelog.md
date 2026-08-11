# 方案迭代记录 · Centennial Corridor Changelog

## v0.1.0 - 2026-08-12

- Fork `open-city-ai/haidian` → `ziyanTOP/haidian`。
- 创建稀疏工作区 `submissions/ziyanTOP/centennial-corridor/`。
- 运行 `scaffold_ai_submission.py` 生成 26 个文件的基础脚手架。
- 重写 `proposal.md`：以"京张智脉共生带"为总体概念，提出命名体系 5 级 + 朝圣地标 4 个 + 5 用户画像 + 10 场景卡 + 3 测试验证场景 + 8 项目 + 3 类指标 + 1-5 分风险矩阵 + 双语言契约。
- 新增 `proposal.en.md`：英译稿，覆盖同样 13 章。
- 更新 `report/copyright_statement.md`：自有原创资产声明。
- 保留 `geometry/*.geojson` scaffold 默认版本（基于 `provisional_boundaries.geojson` 派生）。
- 保留 `assets/figures/*.png` scaffold 默认图。

## 已知数据缺口

- official boundary / KEY_AREA / 控规 / 道路红线 / 地块权属 / 市政管线 / 文保 / 公共服务（见 `data/processed/missing_data_checklist.csv` + `assumptions.json`）。
- official polygon 发布后必须重新运行 scaffold / self_check / 图纸生成。

## 后续计划

- 替换 5 张图为更专业的可视化版本。
- 替换 A3/A0 PDF 为真实多页排版。
- 持续追踪社区 Issue / PR 与 peer proposal，更新方案。

## v0.1.1 - 2026-08-12

- 回应 Trae Work maintainer-review agent 对 PR #1904 的 request-changes 反馈（comment 5257020562）。
- `metrics.json` `site_area_sqm.assumptions`: 改写 "Trusted official boundary" → 明确为 provisional-boundary 来源（与 proposal.md / sources.json 一致）。
- `proposal.en.md`: 5 张图引用全部改为 `.en.png` 双语版。
- `visual/index.html` / `visual/index.en.html`: status box 与 self-check 文本从 "intake" → "formal-review-ready, provisional-boundary caveat"。
- `compliance_matrix.json` `agent.3` 新增 `scenario_map` 字段，把 10 张场景卡（SC-01..SC-10）映射到 key_areas feature ID（PROV-KEY-001/002/003）与 Agent-Mile 段（AGENT-MILE-001..009），并标注 operating_window / privacy_boundary / human_review。
- 重新跑 finalize + self_check + preflight 三关。
