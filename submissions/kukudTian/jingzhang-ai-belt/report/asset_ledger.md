# 逐资产版权与来源台账 · Asset Ledger

> 回应评审：「仅有『未使用未清权资料』的声明不足以完成权利审查」。下表逐项列明本包全部资产的作者身份、许可条款、署名与再分发证据。

## 1. 字体（Fonts）
| 资产 | 作者/权利人 | 许可 | 用途 |
|---|---|---|---|
| Noto Sans SC（思源黑体） | Google / Adobe | SIL OFL 1.1（可自由商用、可再分发） | 全部中文 PDF/图/HTML |
| Noto Sans Mono | Google | SIL OFL 1.1 | 代码语境等宽字 |

## 2. 第三方软件库（Libraries，用于本地生成，不随包分发）
| 库 | 许可 | 用途 |
|---|---|---|
| Python 3 | PSF License | 生成环境 |
| matplotlib | matplotlib license（BSD 类） | 图纸/图表 |
| reportlab | BSD 3-Clause | A0/A3 PDF |
| shapely / pyproj | BSD 3-Clause / MIT | 几何与投影计算 |
| numpy | BSD 3-Clause | 数值计算 |

## 3. 本项目自产资产（本项目原创，授权归本项目作者）
| 资产 | 作者 | 许可建议 | 说明 |
|---|---|---|---|
| 全部 GeoJSON（9 层） | kukudTian（本项目生成） | CC BY 4.0（建议） | 基于组织方 provisional boundary 与官方公告数值生成，含来源属性 |
| 全部图纸/图表（PNG/PDF） | kukudTian（本项目生成） | CC BY 4.0（建议） | matplotlib/reportlab 渲染，无第三方图片素材 |
| OPEN-JZ Logo 与视觉规范 | kukudTian（本项目设计） | CC BY 4.0（建议） | 原创标识，无商标冲突（本项目为参赛方案） |
| 方案正文（中/英） | kukudTian（本项目撰写） | CC BY 4.0（建议） | 含 AI 生成内容，见下条 |
| 代码（生成脚本） | kukudTian（本项目编写） | Apache-2.0（建议） | 位于 scripts-local/，不随投稿包分发 |

## 4. 外部引用资料（仅引用事实与数值，不复制版权表达）
| 引用 | 来源类型 | 版权处理 |
|---|---|---|
| 官方公告数值（43.6km²/11.4km²/368.4ha） | 组织方公告 | 事实数据引用，已注明来源（sources.json） |
| 8 个全球案例 | 公开报道/官网 | 仅提炼事实要点并注明来源，未复制原文表述 |
| 规划标准（GB 50763 等） | 国家标准 | 标准名称引用，不复制条文 |

## 5. AI 生成内容声明
- 本方案正文、图纸、几何均为 AI 智能体（opencode-go/deepseek-v4-flash，经 OpenClaw 运行时）生成，作者 kukudTian 已审阅
- 生成过程中未使用任何未授权版权素材：无第三方图片、无商业字体、无未清权地图底图；全部地图几何为自绘概念示意
- 若最终获奖/公开展示，本台账随包归档，任何第三方素材（如有新增）须在使用前逐项补录许可

## 6. 再分发
- 本投稿包以 CC BY 4.0（建议）向主办方授权展示与评审；任何再分发须保留署名与本台账
