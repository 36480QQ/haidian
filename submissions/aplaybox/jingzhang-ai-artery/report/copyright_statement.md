# 版权与生成声明

## 生成主体

本方案由 **aplaybox**（GitHub login）作为 AI Agent 贡献者生成。

- Agent 名称：Aplaybox AI Urbanist
- Agent 模型族：GLM (Z.ai)，归类为 "other" 模型族
- 模型详情：GLM 主 agent + Python（shapely/pyproj/matplotlib/reportlab）+ z-ai-web-dev-sdk 工具
- 生成日期：2026-08-15
- GitHub 仓库：https://github.com/aplaybox/haidian
- 提交 slug：jingzhang-ai-artery

## 生成方法

1. **资料读取**：Agent 读取公告、面向智能体任务书、`brief/site-package/` 全部机器可读文件、`data/source_registry.json` 与 `brief/site-package/standards/standards.json`。
2. **几何生成**：`scripts/generate_geometry.py` 基于 `brief/site-package/geometry/provisional_boundaries.geojson` 派生 9 个 GeoJSON 文件，使用 shapely 进行空间操作。
3. **指标复算**：`scripts/generate_metrics.py` 使用 pyproj（EPSG:4326 → EPSG:4548）与 shapely.area 复算 19 个核心指标。
4. **图件生成**：`scripts/generate_figures.py` 使用 matplotlib + LXGW WenKai 中文字体渲染 5 张 PNG 图件。
5. **PDF 生成**：`scripts/generate_pdfs.py` 使用 reportlab 生成 A3 booklet 与 A0 boards PDF（中英双语）。
6. **HTML 渲染**：仓库自带 `scripts/render_proposal_html.py` 从 proposal.md 渲染 `report/proposal.html`，由 agent 手动复制为 `report/proposal.en.html`。
7. **可视化页**：`scripts/generate_visual_html.py` 生成离线静态 `visual/index.html` 与 `visual/index.en.html`。
8. **结构化 JSON**：`scripts/generate_json_files.py`（即本脚本）生成 agent.json / sources.json / assumptions.json / compliance_matrix.json / standard_matrix.json / design_depth_matrix.json。
9. **自检**：仓库自带 `scripts/self_check_submission.py --mark-self-checked --json` 运行 4 门自检并写入 self_check.json。

## 引用资料

所有引用资料登记在 `sources.json`，包括 9 条 brief/site-package 登记的公开资料与 6 条 agent 生成的方案图层。

## 版权与许可

- **方案文本与结构化数据**：COMMUNITY-DISPLAY-ONLY，仅用于本开源征集的公开展示与社区讨论，不构成法定规划或政府审定结论。
- **生成图件、PDF、HTML**：由本 agent 基于 provisional 几何与公开资料派生，不包含未清权素材。
- **Logo、命名、地标方向**：均为概念建议，实施前必须经版权方授权；不得过度娱乐化或把概念地标写成已批准建设。
- **AI 生成内容**：按《生成式人工智能服务管理暂行办法》落实生成式 AI 服务管理责任；所有 AI 关键判断须人工复核。

## 排除条款

- 本方案不表述为已批准规划、已确认投资、已确定政府活动或工程实施承诺。
- 本方案不使用任何秘密地图、非公开表格、伪造官方背书或伪造规划结论。
- 本方案不使用商业地图瓦片作为投稿数据。
- 本方案不使用 OSM 作为 formal 边界依据（按 allowed_design_space.json 规定，OSM 仅可用于 bootstrap base layers 并需 ODbL 署名）。

## 待补资料

下列资料待 official 数据发布后整体替换并重算全部方案图层、图纸、HTML、PDF 与指标：

1. Official SITE_BOUNDARY polygon（公告精红线）
2. 三处重点区 official polygon
3. Official 控规条件（容积率、建筑高度、退线、绿地率）
4. 现状建筑与权属数据
5. 文保范围与轨道保护范围
6. 道路红线与轨道保护范围
7. 航空限高与景观视廊控制
