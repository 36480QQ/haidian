# 版权与权利声明

## 1. 归属与授权
- 本方案包全部内容（正文、图件、几何、指标、矩阵）由 KUN-SAL 坤空间量化实验室（投稿署名：邢新华，GitHub: Anshengdesign）通过 AI Agent 工作流生成，向"百年京张AI创新带城市设计开源征集"提交，按仓库 COMMUNITY-DISPLAY-ONLY 许可公开展示。
- 方案命名（涌现之带 THE EMERGENT BELT / 京张 Hyper Line / HYPER STACK / HYPER ORIGIN / HYPER FRONT）与 Logo 方向为概念提案，未经商标检索与授权确认；正式使用前需另行清权。

## 2. 第三方数据与素材
- 高德地图 POI 数据：经用户提供的开发者 Key 通过高德开放平台 Web Service API 获取（2026-08-15 快照，12 类 25,476 点）。本包仅使用聚合指标与密度场，不公开原始点位数据，不转售；高德数据权利归高德及其数据合作方所有。
- OpenStreetMap 数据：© OpenStreetMap contributors，ODbL 1.0 许可；本包在文字与图件中署名，仅用于现状底图与分析，不作为正式边界或权属依据。
- 官方公告、政府新闻与标准文本：均为政府公开信息，引用并注明来源；不推断页面版式、图片或第三方编辑内容的复用许可。
- 理论常数与公式（Wilson λc≈0.42、渗流 pc≈59.27%、标度律 β、分形 D 区间等）引自公开学术文献（Crosato et al. 2018；Batty/Stauffer；Bettencourt 2007 等），原始文献清单见 proposal.md 参考资料。

## 3. 生成方法与 AI 责任
- 生成模型：deepseek-v4-pro（经 DSH harness 运行）；本地计算管线：Python（shapely/networkx/numpy/pyproj/matplotlib），EPSG:4548 度量。
- 全部 7 项计算（Wilson λ、渗流、标度律、空间句法、反事实、分形、POI 动力学）在本次投稿准备中真实本地执行，数字单源登记于研究数据 metrics_registry.json；未实际执行的方法（GNN/ABM/Transformer 等）未在本包中声称实现。
- 图件与 PDF 由本地脚本从同一数据源生成；不包含个人隐私、肖像、未授权商标/字体/图像。

## 4. 边界声明
- 本方案为开放共创建议：不替代正式规划，不构成政府审定结论，不包含已确定政府安排或实施承诺。
- 临时粗略边界（provisional）不构成官方红线或精确面积依据；官方数据发布后整包重算。
