# 逐资产版权与来源台账 (Copyright and Asset Ledger)

本文件提供了本方案提交包中所有视觉资产、数据、代码和内容的版权、许可及来源声明。

## 1. 字体 (Fonts)
- **使用的字体**：图表和 PDF 文件中主要使用了开源中文字体（如 Noto Sans SC, WenQuanYi Micro Hei）或系统默认无衬线字体（sans-serif）。
- **许可信息**：Noto Sans 遵循 SIL Open Font License (OFL)；系统内置字体由本地渲染机制调用，不涉及字体文件打包分发。
- **嵌入状态**：图件和 PDF 生成过程中已遵循相关开源协议，不存在商业字体侵权风险。

## 2. 标志与视觉系统 (Logo & Visual Identity)
- **生成过程**：当前方案中的品牌标识与 Logo 均为概念性描述与占位符，由 AI Agent 纯文本生成或基础 CSS 渲染，未引用任何第三方注册商标。
- **版权声明**：相关概念设计归原作者/团队所有，完全支持根据后续落地需求重新设计或替换。

## 3. 图表与底图数据 (Charts & Basemaps)
- **图表数据来源**：所有量化图表的数据均基于 `metrics.json` 以及由 `geometry/*.geojson` 根据公开地形与场地范围（如资格预审公告提供的资料）演算得出的派生数据。
- **地图底图**：空间图件生成未使用专有商业地图 API，均由 Python Matplotlib 库基于生成的拓扑多边形（GeoJSON）直接渲染，图件本身版权归方案创作者所有。

## 4. 空间几何数据 (Spatial Geometry)
- **来源声明**：所有 `geometry/*.geojson` 均由 AI Agent 基于主办方提供的临时约束边界（provisional_constraint）运算生成，不代表政府审批或法定控规红线。

## 5. 代码与脚本 (Code & Scripts)
- **代码许可**：方案提交包内包含的可视化 HTML (`visual/index.html`)、交互脚本等采用 MIT 协议发布，仅供本次评审与学术交流使用，不涉及商业专有闭源库。

## 6. 其他外部素材 (Other Assets)
- 本方案完全依赖公开数据集与机器可读的 brief/site-package，无未经授权的私有数据或受版权保护的外部素材。

**声明**：若存在任何无法明确证明版权归属的外部资产，团队承诺将在后续阶段无条件替换。
