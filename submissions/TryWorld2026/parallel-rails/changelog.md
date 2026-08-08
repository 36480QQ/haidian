# 方案迭代记录

## v0.1 - 2026-08-08

- **首版生成**：基于脚手架生成完整 formal 方案包「双轨·百年 The Parallel Rails」（`submissions/TryWorld2026/parallel-rails/`）。
- **概念**：以「轨距即标准权」为第一性原理——京张铁路为第一次标准选择（1435mm），AI 创新带为第二次标准选择；空间转译"一基双轨三站"。
- **空间证据**：9 层 GeoJSON（19 个用地单元拓扑完整，gap≈0/overlap≈0）；27 项指标 EPSG:4548 复算；控规指标如实 unknown。
- **任务覆盖**：公告 1.3–1.5 共 17 项任务 + agent.1–agent.6 六项任务（compliance_matrix 23 条）；5 个强制标准；15 个设计深度项全部 complete。
- **成果物**：proposal.md（13 章）、5 张专业图、A3 文册 10 页、A0 展板 7 块、离线 visual/index.html。
- **自检**：Deterministic / Spatial / Visual / Professional 四项本地 gate 全部 PASS（formal-review-ready）。

## v0.1.1 - 2026-08-08

- **对抗式审查修复**：按独立 reviewer 意见实质重写 proposal.md 正文，清除与参考方案的表述雷同；修复催化剂指标公式（补充 buildings assumed_floors 字段，公式可复算）；统一三站面积表述（公告约值＋复算值）；修正拓扑措辞。
- **内容增补**：新增全球案例对照表、区域协同（北纬社区/未来科学城/怀柔/经开区/京津冀）、规划多智能体协作机制、六类画像表、场景—空间—运营映射表、五处朝圣地标目录、公共空间组件库、自选区域场景设计（科教走廊·AI 教育生活融合带，公告可选项）。
- **新增资产**：AI 创新生态图谱 ecosystem-map.png、risk.json（8 维风险矩阵）、changelog.md。
- **双语**：新增 proposal.en.md、visual/index.en.html 及 report/proposal.en.html（非阻断改进）。
- **状态**：四项本地 gate 仍全部 PASS。

## v0.1.2 - 2026-08-08

- **竞争力提升（第一性原理诊断）**：对照任务书 13 个补充评审维度，补强 `function_match` 与 `brief_alignment`——新增"三大定位、五大功能与三区两翼对应"专节，逐条点名三大定位、五大功能并落到三站两翼；三站标题与命名体系补注公告官方名（众智园AI自主创新加速区/北京AI原点社区/大钟寺AI产业集聚区）。
- **AI 规划创新**：新增"规划即代码 planning-as-code"节——将可校验规划规则代码化、方案先通过"编译"再评审；以本包拓扑校验与 EPSG:4548 复算为演示。
- **实施可行性**：新增"参与主体分工建议"五方分工（政府定标准/设计院深化/企业运营/社区共治/开发者贡献场景）。
- **表达完整度**：英文版按 `docs/terminology-glossary.md` 对齐关键术语（Jing-Zhang Railway Heritage Park、Zhongguancun Technology Services Wing、Xiaoyue River Scenario Enablement Wing、Zhongzhiyuan AI Independent Innovation Acceleration Area 等）。
- 四项本地 gate 重新验证 PASS。
