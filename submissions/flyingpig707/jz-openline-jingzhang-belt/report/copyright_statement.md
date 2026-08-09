# 版权声明与资产清单

## 许可

本方案（"百年京张·智链 AI 创新带：开源共创城市设计提案"）采用 **COMMUNITY-DISPLAY-ONLY** 许可，仅供"百年京张AI创新带城市设计国际方案征集"赛事展示与学术交流使用。未经组织方书面授权，不得用于商业用途、二次分发或超出赛事范围的公开传播。

## 资产来源

| 资产类型 | 来源 | 许可状态 |
| --- | --- | --- |
| 方案文本（proposal.md / proposal.en.md） | WorkBuddy Urban Design Agent 原创撰写 | COMMUNITY-DISPLAY-ONLY |
| GeoJSON 图层（geometry/*.geojson） | 由 WorkBuddy Agent 从场地包 provisional boundary 程序化生成 | COMMUNITY-DISPLAY-ONLY |
| 指标数据（metrics.json） | 由 spatial_review.py 从提交图层在 EPSG:4548 下复算 | COMMUNITY-DISPLAY-ONLY |
| PNG 图纸（assets/figures/*.png） | 由 matplotlib 从 GeoJSON 图层程序化渲染，不含第三方素材 | COMMUNITY-DISPLAY-ONLY |
| PDF 文册/展板（drawings/*.pdf） | 由程序从 PNG 图纸和文本合成 | COMMUNITY-DISPLAY-ONLY |
| HTML 展示（report/*.html / visual/*.html） | 静态 HTML，不加载远程资源 | COMMUNITY-DISPLAY-ONLY |
| 字体 | 中文：Hiragino Sans GB（系统字体）；英文：DejaVu Sans（开源） | 系统预装 / 开源 |

## 无第三方素材声明

- 本方案所有图纸、图表、地图均由 Python 代码（matplotlib + shapely + pyproj）从提交的 GeoJSON 图层直接生成
- 不包含任何照片、卫星影像、第三方地图瓦片、图标库或 stock 图片
- 不包含任何企业 logo、品牌标识、人物肖像或受版权保护的图像
- HTML 页面不加载 CDN、远程脚本、iframe、外部 API 或跟踪代码

## 数据来源引用

方案使用的非原创数据来源均已在 `sources.json` 中登记，包括：
- 官方公告 [source:OFFICIAL-ANNOUNCEMENT]
- 面向智能体任务书 [source:AGENT-TASKBOOK]
- 场地包临时边界 [source:BOUNDARY-SOURCE]
- 重点区域公告面积 [source:KEY-AREA-SOURCE]
- 资料登记表 [source:SOURCE-REGISTRY]
- 加工事实包 [source:PROCESSED-FACT-PACK]

## 京张铁路文化遗产

方案中涉及京张铁路历史文化遗产的内容，均基于公开史料和官方公告信息，用于城市设计叙事和文化导览建议。具体保护范围、建设控制地带和保护措施以文物主管部门公布的官方文件为准。

## AI 生成内容披露

本方案由 WorkBuddy Urban Design Agent（基于大语言模型的多模态智能体运行时）在人类操作者监督下生成。Agent 的职责包括：
- 读取结构化任务书和场地资料包
- 生成符合规范格式的 GeoJSON 图层
- 从图层复算空间指标
- 渲染图纸和 HTML 展示
- 执行自检流程

最终内容由人类操作者审核后提交。
