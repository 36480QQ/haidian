# 方案迭代记录

## v1 - 2026-08-12

正式提交包（42 文件，11.8 MiB，formal-review-ready）。

- **方案定型**：京张算带 / Jing-Zhang Compute Belt（一脊五段两翼 + 知识溢出空间编排论证）
- **总审缺口修复**（2026-08-11）：sources.json 增补 11 个证据锚点；compliance_matrix 覆盖 23 项任务；design_depth_matrix 补齐 15 项；assumptions 增至 6 条；copyright_statement 具体化素材来源与边界声明
- **视觉体系升级**（2026-08-11/12）：10 张图全量重渲染——地图类图（总体概念/用地结构/交通蓝绿）改为低饱和城市设计色板 + 圆角卡片 + 隐藏科学坐标轴（比例尺/指北针替代）+ 徽章式标签；重点区域索引改为信息图卡片；指标图改为仪表盘面板（双轴、圆头柱）；双语图同步
- **媒体层**：新增 AI 生成封面概念图 `assets/media/cover.webp`（qwen-image-2.0-pro，解释层非证据，manifest.cover_image 启用）
- **证据披露补充**：assumptions.json 新增 A-BUILDINGS-001（11 栋概念建筑体量 disclosure）；copyright_statement 补充字体与渲染说明
- **图纸同步**：A3/A0 PDF 重渲染（嵌入新视觉图，配色与调色板对齐，版本号 v1）
- **校验**：self-check 四门 PASS（formal-review-ready）→ preflight PASS

## v0.1 - 2026-08-11

首轮成稿。

- scaffold 替换：proposal 正文（双语）、几何九层（GeoJSON，临时边界 provisional_rough）、指标复算（EPSG:4548）、矩阵（compliance/standards/design_depth）、五图首版、A3/A0 PDF、visual 离线页
- 数据：海淀 2025 统计公报 + OSM（ODbL）+ 任务书，来源登记于 sources.json
- 首轮 self-check 四门 PASS 后进入终审
