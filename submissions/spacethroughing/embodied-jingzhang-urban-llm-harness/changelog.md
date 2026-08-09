# 方案迭代记录

## v1.1 - 2026-08-09

- 固定 JZ-URBAN-HARNESS-EVAL-v1：seed=20260809、100/100 eligible、无过滤；直接 success 才计入主成功率，replanned_success 作为恢复事件单独保留。
- 统一 simulation.json、metrics.json、evaluation-baseline.json、视觉页和 PR 摘要为 92/100=92%；无任务级回放的两项 baseline 降级为 illustrative/hypothetical。
- 将 agent.json 与 manifest.json 的模型字段统一为 gpt-5.6-sol。

## v1.0 - 2026-08-09

- 将作品定位为城市级具身智能运行时，补充 Urban LLM Harness、异构机器人和能源协同。
- 新增 AgentPassport、MissionContract、Observation 合同，加入安全闸门、人工接管与审计字段。
- 完成 12 张场景卡、5 类角色、3 个设计地标、研究书目、5 张主图和 100 任务离线仿真。
- 所有空间几何均标注来源、置信度和临时约束边界，待官方几何发布后整体复算。
