# 版权与原创声明 / Copyright and Originality Statement

## 原创性 / Originality

本投稿包的全部内容——正文、英文译稿、空间结构、场景卡、演练机制、风险矩阵、概念空间节点、
图件、A3 文册、A0 展板与离线 HTML 展示页——均为本次投稿由参赛者 `BinHPdev` 使用
Claude Opus 5（`claude-opus-5`）原创生成，未复制他人方案。

All content in this package — the main text, the English translation, the spatial structure,
the scenario cards, the rehearsal mechanism, the risk matrix, the concept spatial notes, the
figures, the A3 booklet, the A0 boards, and the offline HTML exhibit — was originally produced
for this submission by participant `BinHPdev` using Claude Opus 5 (`claude-opus-5`).
No other entrant's work was copied.

## 生成方式 / How the artefacts were produced

- `geometry/*.geojson`：由参赛者编写的确定性生成脚本，从 `brief/site-package/geometry/provisional_boundaries.geojson`
  推导。同一输入产生同一输出，坐标在 EPSG:4548 下按 1 mm 网格对齐。
- `metrics.json`：全部数值由脚本从**已写入磁盘的** GeoJSON 与 `simulation.json` 复算，非手工填写。
- `simulation.json`：固定 seed = 20260824 的离线合成任务轨迹。**不调用在线模型，不接入真实机器人，
  不使用任何个人数据。** 读数为离线合成结果，非现场实测。
- `assets/figures/*.png`：使用 Matplotlib 从提交的 GeoJSON 与 metrics 渲染，非截图、非外部素材。
- `drawings/*.pdf`：由上述图件与文本在本地合成，未使用外部模板。
- `visual/index.html`：手写 HTML/CSS，无框架、无外部依赖。

## 字体与资产 / Fonts and assets

图件与 PDF 使用 macOS 系统自带字体 Hiragino Sans GB 与 Arial Unicode MS 进行**本地渲染**，
字体文件本身未被再分发。HTML 只声明字体族名称，不打包、不加载任何字体文件，
在缺少该字体的环境中回退到系统 sans-serif。

未使用任何未授权的图片、商标、人物肖像、论文图像或第三方素材库内容。
No unlicensed images, trademarks, portraits, paper figures, or third-party stock assets are used.

## 第三方开放贡献的署名 / Attribution for third-party open contributions

本方案的「AI-off 等价服务基准」概念参考了仓库上游 Issue #2549 公开的
**服务等价基准 SEB v0.5.0**，该贡献由其作者以 **CC BY-SA 4.0** 授予任何方案采用。
本方案对该概念的实例化（`simulation.json` 中的 `baselines.ai_off_equivalent` 与相关正文段落）
按 CC BY-SA 4.0 的相同方式共享条款提供，并在此标注来源与许可。

The "AI-off equivalent service baseline" concept draws on the **Service Equivalence Baseline
v0.5.0** published in upstream Issue #2549, granted by its author under **CC BY-SA 4.0** for any
proposal to adopt. This proposal's instantiation of that concept (`baselines.ai_off_equivalent`
in `simulation.json` and the related prose) is offered under the same ShareAlike terms, with the
source and licence attributed here.

## 数据边界 / Data boundary

本方案只使用官方公开资料与仓库内已登记的机器可读资料。
未使用、未声称使用任何非公开规划图件、内部控制指标、企业未公开经营数据或个人隐私数据。
临时几何的精度限制已在正文、`assumptions.json`、`sources.json` 与自检结果中一致标注。

Only public official materials and repository-registered machine-readable materials are used.
No non-public planning drawings, internal control indicators, non-public corporate operating
data, or personal data are used or claimed.

## 责任边界 / Boundary of responsibility

本方案全部空间落地、活动运营、品牌传播与政策机制内容，均为**概念建议、参考方案，
可供专业团队深化研究**，不替代法定规划，不构成政府审定结论、实施承诺或投资安排。
作者对事实、引用、版权与最终表达负责。

All spatial, event, branding, and policy content is a **conceptual suggestion, a reference
scheme, material for professional teams to develop further**. It does not replace statutory
planning and is not a government decision, an implementation commitment, or an investment
arrangement. The author is responsible for facts, citations, copyright, and final expression.

## 许可 / Licence

`COMMUNITY-DISPLAY-ONLY` —— 允许本仓库及其公开展示页展示本方案；其他用途请联系作者。
