# 版权、来源与生成声明 / Copyright, Sources and Generation Statement

本方案文字、命名、Logo方向、图形符号、地图表达、版式、GeoJSON设计图层、离线HTML和PDF均为本次投稿原创，或由 `sources.json` 登记且允许使用的仓库公开/清权资料程序化派生。提交者为 Sonike；Codex（GPT-5）负责本轮审计、结构化数据、确定性制图与校验，用户操作的 Claude Opus 5 参与此前多轮方案编辑。不同轮次的智能体协作均不替代人类评审与专业团队的最终判断。

全部中英文对应**图件**（`assets/figures/` 下的 png）均由提交几何、`metrics.json` 与本方案数据在本地确定性渲染，没有使用外部底图、遥感截图、摄影、人物肖像、企业Logo、第三方插画、远程字体、CDN 或地图瓦片。

**生成式图像的单项例外与完整披露。** 自 v1.6.2 起，本包含有且仅含一张生成式图像：`assets/figures/handover-scene.jpg`，用于 A3 图册第 01 页与 A0 第 01 板的概念表现，并在正文开篇引用。

- 生成方式：Codex CLI 0.147.0 内置 `image_generation` 工具，模型 `gpt-image-2`，单次生成，无参考图、无底图、无遥感影像、无第三方图像作为输入。
- 生成后处理：仅等比缩放至 1600×1067 并重编码为 JPEG（质量 88），未做内容修改、拼贴、换脸或局部重绘。
- 完整提示词（原文照录）：

> 主体——一张建筑概念表现图（明确是设计可视化，不是照片），描绘一条沿保留的历史铁路轨道、穿过中国高校街区的线性公共走廊，时令为初秋。画面自前景至背景包含：铁轨齐平嵌在铺装中形成连续线；轨道旁一条深炭灰钢与浅木色的长条共用台面——"交接台"——台前一名穿制服的工作人员正把板夹和一串钥匙交给另一名工作人员，这一人对人的交接是画面的情感中心；一根独立矮柱，柱顶为大号红色急停按钮，从步道即可触及；一台白色四轮小型配送机器人行驶在地面标出的青色专用道内，与人行区域分开；空间中的普通使用者：一位坐轮椅者行进在连续平坦的路径上，一位老年人正在柜台由人工服务人员协助，学生坐在长椅上；成熟乔木带秋色叶，背景为低层砖砌与混凝土建筑。风格——温暖、平静、柔和光照的建筑可视化，略带插画感的哑光质地。克制的色板：暖米白铺装、炭灰构筑物、仅用于急停按钮与小标记的信号红、仅用于机器人专用道的电气青。阴天漫射日光，长横向构图，人视点沿走廊看去。硬性约束——画面任何位置绝对不得出现文字、字母、数字、标识文案、Logo、品牌标记或水印；不得出现可辨识的面部特写，人物保持中景、四分之三侧或背向；不得使用鸟瞰或地图视角；不得做成看起来像真实照片。

- 用途与限制：仅作非证据性的空间氛围示意。画面中人物为虚构形象而非真实个人；不对应任何真实地点、街道、建筑、单位或品牌；不构成现状记录、测绘成果、竣工效果或已批准方案；不得据以推断任何面积、尺寸、材料、树种、坡度、日照或工程条件。图纸与正文均已就地标注"概念表现（AI 生成示意图），非现状照片、非测绘成果、非批准方案"。来源登记见 `sources.json` 的 `IMAGEGEN-CONCEPT-SCENE`。

A3图册和A0展板只嵌入上述原创图件、该张已披露的概念表现图与本方案文字。

v1.6 新增的 `visual/assets/governance/shift-ledger.schema.json` 为本方案原创的 JSON Schema Draft 2020-12 机器契约；`example-scn05-shift-ledger.json` 是合成、未执行且角色未授权的沙盒结构样例，不含个人数据，也不连接真实导航、政务、维护或告警服务。`validation-report.json` 仅记录 Schema 元模式与样例结构校验，不能据此声称路线、性能、安全、无障碍质量、法律合规、公众接受度或现场运行已经验证。

v1.6 引用的三部法律法规与政策文件（《生成式人工智能服务管理暂行办法》《中华人民共和国无障碍环境建设法》、国办发〔2020〕45号）均为国家机关依法公开发布的文本。本包只引用条款要义并标注条号与施行日期，不复制全文、不再分发附件，也不构成法律意见；条款适用与个案认定由主管部门和具备资质的法律专业人员负责。海淀区2025年国民经济和社会发展统计公报为区级政府网站公开发布的 HTML 页面，未见明确开放数据许可，因此本包只摘录事实数值并保留发布者、标题与原始链接，不复制页面全文；每项数值的原文表述、采集方法、单位换算与可用/不可用边界逐条记录在 `sources.json`。

六个国际案例只根据机构官网或城市官方报告转述组织机制；未复制网页文字长段、照片、地图、商标、品牌视觉或受保护图表。案例URL、发布者、检索日期、用途和局限均记录在 `sources.json`。京张铁路与中关村文化叙事采用概念性公共叙事，不主张未核实历史细节。

场地与重点区域采用仓库 `provisional_boundaries.geojson`，明确保留 `official_boundary=false`、`provisional_constraint` 和低置信度；它们不构成官方红线、法定规划、权属或工程依据。官方几何和专业条件可用后，全部派生图层、指标、图件与图纸应重新生成。

本包授权标识为 `COMMUNITY-DISPLAY-ONLY`，用于本次开源征集的公共展示、评审和知识沉淀。任何第三方进一步使用应遵守上游仓库规则、逐项核验来源权利，并不得把概念建议表述为政府批准、专业审定或实施承诺。

---

All text, naming, identity direction, diagrams, map language, layouts, design GeoJSON, offline HTML and PDFs are original to this submission or programmatically derived from public/cleared repository inputs registered in `sources.json`. Sonike submits the work; Codex (GPT-5) carried out the current audit, structured-data authoring, deterministic graphics and validation, while user-operated Claude Opus 5 contributed to earlier editing rounds. All bilingual **figures** under `assets/figures/` (the png set) use no remote map, photography, portrait, company mark, third-party illustration, remote font, CDN or tile service.

**Single generative-image exception, fully disclosed.** From v1.6.2 the package contains exactly one generative image, `assets/figures/handover-scene.jpg`, used as the concept rendering on A3 page 01 and A0 board 01 and cited at the opening of the proposal. It was produced in a single pass by the built-in `image_generation` tool of Codex CLI 0.147.0 using the `gpt-image-2` model, with no reference photograph, basemap, satellite imagery or third-party image as input; post-processing was limited to proportional resizing to 1600×1067 and JPEG re-encoding at quality 88, with no content edit, collage, face swap or inpainting. The full prompt is recorded verbatim in the Chinese section above. Its use is strictly non-evidentiary spatial atmosphere: the people are fictional rather than real individuals; it corresponds to no real place, street, building, organisation or brand; it is not a record of existing conditions, a survey, a built result or an approved scheme; and no area, dimension, material, species, gradient, daylight or engineering condition may be inferred from it. Both the drawings and the proposal label it in place as a concept rendering that is not a photograph, survey or approved scheme. The source is registered as `IMAGEGEN-CONCEPT-SCENE` in `sources.json`.

Human and professional review retains final judgment.

The v1.6 `visual/assets/governance/shift-ledger.schema.json` is an original Draft 2020-12 JSON Schema data contract. `example-scn05-shift-ledger.json` is a synthetic, unexecuted and unauthorised-role sandbox fixture containing no personal data and touching no live navigation, government, maintenance or alert service. `validation-report.json` records schema and instance conformance only; it is not evidence of route quality, performance, safety, accessibility, legal compliance, public acceptance or field operation.

The three statutory and policy instruments cited in v1.6 (the Interim Measures for the Management of Generative AI Services, the Law on the Construction of a Barrier-Free Environment, and State Council General Office Document No. 45 of 2020) are texts published by state organs under law. This package cites the substance of specific articles with article numbers and commencement dates; it reproduces no full text, redistributes no attachment, and offers no legal opinion — application of any provision rests with the competent authorities and qualified legal professionals. The Haidian District 2025 Statistical Communiqué is a public HTML page on a district government site with no explicit open-data licence found, so this package extracts factual values only while preserving publisher, title and original link, and reproduces no page text; the original wording, collection method, unit conversion and usable / not-usable boundary of every value are recorded item by item in `sources.json`.

The six global cases are paraphrased from institutional pages or official city material; no protected image, map, trademark, branded layout or long passage is reproduced. The provisional site and key-area geometry explicitly remain non-official. This package is marked `COMMUNITY-DISPLAY-ONLY` for open-call review, public display and knowledge capture; it must not be represented as statutory approval or a professional implementation decision.
