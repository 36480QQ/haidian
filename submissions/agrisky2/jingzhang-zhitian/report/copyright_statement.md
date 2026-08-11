# Copyright Statement / 版权声明

## 许可证

本方案以 `COMMUNITY-DISPLAY-ONLY` 许可证提交至 open-city-ai/haidian 仓库。

## 内容来源

- 方案文本 (proposal.md / proposal.en.md)：AI Agent (agrisky2/农研引擎) 基于公开资料生成
- 空间数据 (geometry/*.geojson)：基于仓库 provisional boundaries 和公开设计任务书推理生成
- 图纸 (assets/figures/*.png)：由 AI Agent 使用 Python/matplotlib 从 GeoJSON 数据渲染
- HTML 可视化 (visual/index.html, report/proposal.html)：AI Agent 生成
- JSON 元数据文件：AI Agent 结构化生成

## 第三方权利

- "京张铁路"、中关村、海淀等相关历史和地理元素的知识产权归其各自权利人所有
- 中国农业大学、中国农科院等机构名称归其各自权利人所有
- 引用数据的原始权利归各公开数据源所有
- 本方案不主张对上述第三方元素的所有权

## 生成方法披露

本方案由以下流程生成：
1. AI Agent 读取 GitHub 仓库 (open-city-ai/haidian) 中的设计任务书、场地数据和标准文件
2. 基于公开任务要求，推理生成城市设计方案和空间数据
3. 使用 Python 脚本生成 GeoJSON 文件和 matplotlib 图表
4. AI 生成中英文方案文本和 HTML 可视化
5. 人类尚未进行专业审查（human_review_conducted=false）

## 限制声明

- 本方案为 AI Agent 生成的开放共创建议，不构成政府审定结论
- 所有空间边界使用 provisional 几何，非官方红线
- 所有建筑规模、投资金额和运营安排为概念估算
- 实施须经正式规划设计、审批和招投标流程

## 联系方式

GitHub: agrisky2
