# v1.4 全状态证据账本

本附录把方案从“单一渲染状态”扩展为可回退的城市运行状态。`evidence/ledger.json` 收录 52 条原子决策记录，覆盖气候、风环境、空气质量、雨洪、能源、材料、具身智能、人本、公平、交通、安全、文化、治理、运维、财务和传播。每条记录都区分 `design_target` 与已知事实：90 分是评审门槛目标，不是现状得分；只有官方边界、现场测绘、专业模拟或运营日志到位后才可转为 `known`。

## 复核顺序

1. 先确认边界、权属、管线、文保、气象和交通数据的来源与许可。
2. 再用几何、公式或演练记录复算指标，保留输入、版本、时间和责任人。
3. 对热浪、暴雨、断网、设备失效、活动峰值、施工和人口变化做压力测试。
4. 任何无障碍主链被阻断、机器人无法急停、排水单点失效或维护连续逾期，都触发降级、人工接管或停止扩容。

## 状态语义

| 状态 | 含义 | 可采取的动作 |
| --- | --- | --- |
| `known` | 有可追溯数据和复算方法 | 进入专业评审与运营复盘 |
| `design_target` | 方案提出的目标或门槛 | 先做试点、模拟和共同验收 |
| `unknown` | 资料或条件尚未取得 | 明示缺口，不得涂绿或冒充事实 |
| `blocked` | 触发停止条件 | 保持人工模式，修复后重新过门 |

## 关键证据组

- **气候—水系统：** `climate-risk-baseline`、`heat-comfort`、`airflow-network`、`stormwater-hierarchy`、`drainage-redundancy`、`water-reuse`、`flood-evacuation`、`heat-response`。
- **材料—能源—生态：** `winter-safety`、`soil-tree-health`、`biodiversity`、`embodied-carbon`、`circular-materials`、`energy-microgrid`、`water-energy-nexus`、`carbon-dashboard`。
- **具身智能—数据治理：** `edge-compute`、`embodied-ai-governance`、`privacy-minimization`、`model-card`、`sensor-resilience`、`cybersecurity`、`procurement`。
- **人的体验与公平：** `human-sensory`、`universal-access`、`wayfinding`、`child-safety`、`elder-care`、`worker-health`、`gender-safety`、`equity`。
- **运维—安全—实施：** `asset-ledger`、`maintenance-backlog`、`failure-drill`、`operations-staff`、`pollution-event`、`mobility-demand`、`active-travel`、`curb-logistics`、`phasing`、`phase-gate`。
- **文化—传播—可复现：** `heritage-rail`、`open-culture`、`participation-loop`、`night-economy`、`film-storyboard`、`scenario-testing`、`open-reproducibility`、`evaluation-dashboard`。

这份账本与 `metrics.json`、GeoJSON、矩阵、自检和离线 HTML 是并行证据层；它不改变 provisional boundary 的法律边界，也不把概念建议写成政府承诺。研究依据包括 IPCC 城市风险、WHO 城市健康、北京气候适应与排水计划、ISO 55001/13482 等已登记来源，仍需以本地正式资料和专业团队复核为准。
