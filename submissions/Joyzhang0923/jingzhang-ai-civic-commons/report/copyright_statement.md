# 版权、生成方式与资产权利台账

本投稿由张洁静（GitHub: `Joyzhang0923`）以个人名义提交。正文、译文、图解、静态网页和图纸由 OpenAI Codex（GPT-5 系列；本次会话未暴露精确部署标识）协助生成，张洁静确定方案方向并承担最终人工判断责任。除下表所列字体外，投稿不包含第三方图片、商业地图瓦片、远程脚本、远程字体、追踪代码或私有数据。

| 路径 | 生成或派生方式 | 数据/素材来源 | 权利与限制 |
| --- | --- | --- | --- |
| `proposal.md`、`proposal.en.md` | Codex起草、翻译并由提交者确认方向 | 官方公告、清权任务书、仓库登记资料及本包结构化证据 | `COMMUNITY-DISPLAY-ONLY`；不得解释为官方审定成果 |
| `geometry/*.geojson` | 仓库脚手架生成后，以概念公共服务主轴等设计属性深化 | `brief/site-package/geometry/provisional_boundaries.geojson`及仓库规则 | 临时边界仅供生成、展示和内容评审；不得作为官方红线或精确面积依据 |
| `metrics.json`及三个矩阵 | 仓库脚本按GeoJSON、任务书和标准生成/复算 | 本包GeoJSON、仓库任务书与标准快照 | 指标置信度和假设以文件内记录为准；正式数据发布后重算 |
| `assets/figures/*.png` | 原创Python/Pillow程序从本包GeoJSON、metrics及方案逻辑绘制 | 不含外部图片；仅使用本包结构化数据 | 中文主图与英文`.en.png`为成对原创派生图；不得替代GeoJSON权威层 |
| `report/proposal.html`、`report/proposal.en.html` | 仓库`render_proposal_html.py`从对应Markdown渲染 | 本地正文和本地图件 | 完全离线，不加载远程资源 |
| `visual/index.html`、`visual/index.en.html` | 原创静态HTML/CSS生成 | 本包指标、图件和方案摘要 | 完全离线，无iframe、表单、API或追踪 |
| `drawings/a3-booklet*.pdf`、`drawings/a0-boards*.pdf` | 原创Python/ReportLab排版；Poppler用于目视校验 | 本地中英文图件和方案摘要 | 展示层文件，不作为空间边界、面积或控规结论的唯一依据 |
| PDF内嵌中文字体子集 | `Noto Sans SC`，通过`@fontsource/noto-sans-sc` 5.3.0获取并由ReportLab嵌入 | Google Noto项目 / Fontsource分发 | SIL Open Font License 1.1；仅在PDF中嵌入所需字形，不单独再分发字体文件 |
| `agent.json`、`manifest.json`、`self_check.json`、`assumptions.json`、`sources.json` | 仓库脚本生成并按真实生成流程补充 | 本投稿文件及仓库校验结果 | 用于来源、生成方式、校验和限制审计 |

所有路径级生成记录以本文件、`agent.json`、`sources.json`和`manifest.json`共同构成审计链。若后续替换官方边界、第三方图片、字体或其他素材，必须在重新提交前同步更新来源、许可、哈希、图件、PDF与自检结果。
