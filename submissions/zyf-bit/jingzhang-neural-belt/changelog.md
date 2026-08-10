# 变更日志

## v1.0 - 2026-08-10
- 初始方案生成
- 基于 provisional boundary 完成空间设计和指标复算
- 覆盖 agent.1 至 agent.6 全部六项智能体任务
- 生成12张AI场景卡、6类用户画像、3个AI朝圣地标
- 完成7个全球AI创新生态案例研究
- 生成5张专业图表和HTML可视化
- 提交 Pull Request

## v1.1 - 2026-08-11
- 修复 manifest.json：重建为 schema 0.1.0 格式，匹配实际文件路径并写入 SHA-256
- 修复 self_check.json：填充 result/severity/target/message 字段，移除 null suggested_fix
- 修复 risk.json：迁移到 version=1 + dimensions[] schema，所有维度补齐 human_review
- 修复 geometry 文件：road_centerline→roads 重命名，删除 ai_service_zone/scenario_node，新建 constraints.geojson
- 移除 manifest 中不存在的 proposal.en.md 引用
