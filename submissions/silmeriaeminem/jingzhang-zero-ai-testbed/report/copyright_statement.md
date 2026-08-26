# Copyright Statement

本提交包（百年京张 AI 创新带城市设计开源征集 — 提案「京张新纪元·创想AI时轨」，`submissions/silmeriaeminem/jingzhang-zero-ai-testbed/`）的资产权利状态说明：

## 1. 文本与代码
- 中英文主提案（`proposal.md` / `proposal.en.md`）、配置文件（`manifest.json` / `metrics.json` / `assumptions.json` / `sources.json` / `self_check.json` / `compliance_matrix.json` / `standard_matrix.json` / `design_depth_matrix.json` / `agent.json`）由声明的 AI 智能体依据官方公开任务包（`SITE-PACKAGE`、`OFFICIAL-ANNOUNCEMENT`、`AGENT-TASKBOOK`）与已清权用户材料（`AGENT-TASKBOOK`，2026-05-18）撰写；
- 不含商业秘密、内部资料、个人隐私或非公开空间数据。

## 2. 几何（`geometry/*.geojson`，9 个图层）
- `site_boundary.geojson` 与 `key_areas.geojson` 为**临时多边形**（基于公告文字四至与约 11.4 km² 面积约束），**不构成官方红线或精确面积依据**；
- `land_use` / `buildings` / `roads` / `green_space` / `public_space` / `phasing` 为**概念设计提案**（建筑基底由 POI 点按约 36m 方形生成、道路按中心线约 16m 缓冲），**概念模型估计**，不得作为现状测绘或法定控制条件；
- `constraints.geojson` 保持空集合（无官方约束几何可用）；
- 正式几何与控规发布后，全部指标需重算。

## 3. 图像（`assets/figures/*.jpg` 共 21 张）
- 16 张概念图（`01_cotrack_testline_people_machines.jpg` 至 `16_masterplan_timetrack_v4.jpg`）由**用户本人即梦 AI 账号生成**，用户确认具有在本开源征集范围内使用的权利；
- 5 张数据图（`site-overview.png` / `land-use-structure.png` / `key-areas.png` / `mobility-bluegreen.png` / `metrics-evidence.png`）由 `matplotlib` 基于提交包内 GeoJSON 自动生成；
- **不含第三方 Logo、企业标识、商标、可识别人物肖像**。提案 §3.1 与 §9.2 中的"Logo 设计方向"与"双原点广场"仅为**概念描述**，未使用任何第三方标识或历史人物/企业 Logo；任何官方出版/落地使用前必须重新清权。

## 4. 字体（嵌入 HTML 的 Noto Sans SC woff2）
- 替代微软黑体（SimHei）；
- 许可：**SIL Open Font License 1.1**（允许自由分发、嵌入、商业使用）；
- 来源：https://fonts.google.com/noto/specimen/Noto+Sans+SC。

## 5. PDF（`drawings/*.pdf`）与 HTML（`report/*.html` / `visual/*.html`）
- 基于上述文本、几何、图像与字体自动生成；
- 渲染版 HTML 嵌入 Noto Sans SC 字体，离线打开不再依赖系统 CJK 字体；
- 视觉页（`visual/index.html`）无远程 CDN、瓦片、外部脚本、API、iframe 或表单提交。

## 6. 政策与企业引用（来源合规）
- `POLICY-01-HD-CONTROL-PLAN` / `POLICY-02-AGENT-MEASURES` / `POLICY-03-AUTONOMOUS-DRIVING` 三条政策声明当前为 **待核实状态**（`pending_verification`）：政策文号、发布日期、条款编号需对照北京/海淀官方原文核验；在核验前，正文相关表述已统一改写为"建议/参考机制"措辞；
- `CHAIN-ENTERPRISES-INDICATIVE` 链主企业清单为**指示性集合**（`indicative`）：8 类图谱与 6 类合作模式为框架性建议；具体企业总部地址、融资轮次、具体合作项目需对照企业官网/年报/权威新闻核验；在核验前，正文相关表述已统一改写为"已检索样本中可观察到的"等有限措辞。

## 7. 状态声明
- 本提交包**不**包含、**不**声称、**不**暗示已通过官方正式审批、控规批复或实施许可；
- 所有空间建议为开放共创的概念参考方案；
- 评审过程中可使用，正式落地/发布前**必须**重新核验政策原文、企业信息与资产权利。

—— 提交者：silmeriaeminem
