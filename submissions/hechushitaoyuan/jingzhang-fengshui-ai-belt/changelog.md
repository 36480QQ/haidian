# 方案迭代记录

## v1.3 - 2026-08-23

外部上下文与证据指针轮（A+B+C+E），并按几何实证统一重点区面积口径。

- **A 外部上下文数据层**：新增"外部上下文数据层（背景辨识）"小节（中英各一处），登记 OpenStreetMap 快照 bbox（WGS84 南,西,北,东）39.92,116.31,40.06,116.39、快照时间 2026-08-22T18:47Z±、七类要素计数（waterway 109 / green 1780 / amenity 节点 2424 / road 4636 / railway 267 / building 14740 / 公共交通站点 2563，合计 26,519），配套图件 `context-basemap.png` / `context-basemap.en.png`；来源标注 © OpenStreetMap contributors · Overpass API · ODbL 1.0，方法与限制登记 `sources.json` 条目 SRC-OSM-CONTEXT-SNAPSHOT。该层三条硬性声明：仅背景辨识、不参与边界/用地/道路/指标计算、不作测绘成果或审批底图；building 双口径已注明（14,740 含量关系，图面渲染取 way 级 14,648）。风险章另补 ODbL 合规与非权威定位专段（中英各一处）。
- **B 引用规范核查**：核查正文官方文件引用的书名号全称，四处（《百年京张AI创新带城市设计国际方案征集资格预审公告》《生成式人工智能服务管理暂行办法》《无障碍环境建设法》《城市设计管理办法》）均为官方全称，无缩写错误，无需修正；`sources.json` 不在本轮内容面改动范围。
- **C KPI 证据指针挂接**：指标章 KPI 表增列"证据指针（`metrics.json` 键名）"，公共利益相关指标逐行括注精确键名与复算值——`green_ratio`=0.293695、`public_space_ratio`=0.204309、`greenway_length_m`=9721.9、`public_space_feature_count`=5、`key_area_count`=3 及三处 `key_area_*_sqm`、三期 `phasing_phase_1/2/3_area_sqm`，另补 `site_area_sqm`、`building_density` 与两项 `status=unknown` 控规指标；新增公共空间要素数、重点区域分项规模两行，三期分期句内联三键并补全 `[metric:]` 标记。评审者可按键名直查公式、来源文件与置信度，数值口径与 `metrics.json` 逐项一致。
- **E 署名更新**：v1.3 阶段署名定为"同济设计AI云：DeepSeek Harness + ox-alpha 以及子智能体 Codex（GPT-5.6-Sol）+ Claude Code（Claude Opus 5）"（EN: Tongji Design AI Cloud: DeepSeek Harness + ox-alpha, with subagent CLIs Codex (GPT-5.6-Sol) and Claude Code (Claude Opus 5)），proposal×2 / copyright_statement / agent.json / manifest 五处双语一致；历史链（初稿 opencode/kimi-k3 · 迭代 zcode/GLM-5.3）与人类参与者 hechushitaoyuan 署名与职责表述完整保留。agent 卡 `agent_name` 取短形"同济设计AI云"供画廊展示，全貌文本只落正文、条款与 `model_detail`；`model_family` 由 kimi 改为 deepseek（编排主体 ox-alpha 属 DeepSeek 系）。
- **重点区面积口径统一**：按 `geometry/key_areas.geojson` 重投影 EPSG:4548 复算，三处重点区分项和=并集=3,692,893 ㎡=369.29 ha（零重叠），与 `metrics.json` 三键完全一致；正文陈旧值"约 368.4 公顷"订正为"约 369.3 公顷"，共六处（proposal×2、report/proposal(.en).html、visual/index(.en).html）。

**管线**：待跑 render_proposal_html → refresh_submission_manifest → 四门自检 → participant_preflight（manifest 哈希与文件清单由 refresh 脚本统一重算）。

## v1.2 - 2026-08-20

精瘦收尾轮（A+B+E+F，经评审纪律裁定为最后一轮内容迭代）。

- **A 无障碍量化核验**：11 色语义色板 × 四类色觉（Machado 2009 模拟）× CIEDE2000（Sharma 2005 实现，官方测试向量 5/5 自检）两两核验，阈值 ΔE00≥20；220 项核验、39 对例外（同族色与红绿对集中），逐对结果登记于 `visual/assets/a11y-color-check.json`；正文新增无障碍专节（四条件结果表 + 例外清单 + 整改说明）；例外以既有文字冗余编码兜底，不触发图件重渲。metrics 新增 `a11y_color_pair_count=220`、`a11y_color_pair_fail_count=39`；方法登记 `sources.json` 条目 SRC-A11Y-CHECK-V12。
- **B 合规精化**：新增"法定下限 vs 自设标准"辨析表（生成式AI办法第14/15条、无障碍环境建设法第39条、国办发〔2020〕45号、城市设计管理办法——逐条说明实际规定/未规定/自设部分）；新增逐资产权利核验命令表（pdffonts、字体文件检索、指标复算、媒体生成链、色觉核验五项）。
- **E 画像表格化**：六类画像由散文段改为"画像/典型需求/空间响应（场景卡#）/自检边界"四列表。
- **F 读图引导**：九张图件各配一行"读图"引导块（主叙事 + 先看什么 + 无障碍冗余编码提示）。

**管线**：render_proposal_html → refresh_submission_manifest → 四门自检 → participant_preflight（结果见提交记录）。

## v1.1 - 2026-08-19

评审迭代轮（P3 任务书合规修补 + P1 表达完整度）。

**P3 任务书合规修补**：
- 新增第 13 张场景卡「藏风算力亭」（端侧推理试验站），产业测试验证场景补齐为 3 个（#4 路权 / #8 模型 / #13 硬件），满足任务书"不少于 3 个"要求。
- 十二张一句话场景卡重构为 13 行 × 7 列结构化表格（空间载体 / 最小数据与边界 / 人工接管·无AI通道 / 责任主体类型 / 退出后空间用途），即 agent.3 要求的场景-空间-运营映射本体。
- metrics 新增 `scenario_card_count=13`、`testbed_count=3`；compliance agent.3 补登 AI 章节；visual 双语计数行同步。

**P1 表达完整度**：
- 多媒体资产从无到有：画廊封面 `cover.png`（宣纸+金脉确定性导出，金脊取自真实绿脊中心线）；中英音频导览 `audio-guide-zh/en.mp3`（各约 2 分钟，SAPI 逐句合成 + vtt 字幕 + md 文稿）；概念视频 `experience.mp4`（24 秒金脊生长动画 + 海报帧 + 双语字幕 + 分镜文稿）。全部媒体在 copyright_statement.md 与 sources.json（SRC-MEDIA-RENDER-V11）披露生成方法，标注"概念氛围/导览内容，非空间依据"。
- 图件 5 → 9 张（中英各一套）：新增 logo-identity（品牌识别）、scenario-cards（场景卡全景）、phasing-renewal（分期与项目）、cultural-narrative（三层时间叙事）。
- 正文双语扩写（184 → 275 行，信息量约翻倍）：新增读本导引、三层传导表、气数四次转译表、区域协同节、现状诊断问题-动作对照表、五带设计要点、重点区落位逻辑与边界条件、画像-场景映射细则、指标三分类表、风险归属段落、多模态表达专节；修复更新项目清单编号跳 ③（现 ①-⑥ 与图件一致，③ 为藏风算力亭试点）。
- 署名更新为多智能体协作（初稿 opencode/kimi-k3 · 迭代 zcode/GLM-5.3），proposal×2 / copyright_statement / agent.json / manifest 五处一致。

**P2 可实施性**：
- 分期改为条件门制：三期各设"进入门 / 验收门 / 回滚后城市状态"（正文条件门表，二元门槛、不设固定年份），验收门对公众公示。
- 六项更新项目扩为行动包表：试点空间与规模区间 / 责任主体类型 / 成本级 S-M-L（概念估算类别，非投资测算）/ 进入门 / 回滚后状态。
- 新增八类岗位规格 `visual/assets/governance/role-spec.json`（治理原则"岗位先于人选"，独立复核者与全部运营岗互斥，全部 assignment_status=unassigned）。
- 指标 26 → 43 项：新增 9 项几何复算计数（building_count=368、qi_gateway_street_count=5 等）与 8 项概念计数（persona_count、role_count、renewal_project_count、no_ai_path_count 等）；两项 unknown 指标（容积率/建筑高度）补测量协议与复算触发条件。
- compliance（1.5.2.2 / agent.2 / agent.3 / agent.6）与 design_depth（phasing）证据同步；visual 双语页新增 3 张计数指标卡与条件门说明。

**P4 AI 创新机制化**：
- "气数"锻造为**气数协议 v0.1**（察气—演气—验气—养气四步 + QP-1..7 规则），登记于 `visual/assets/governance/qi-protocol.json`；配套确定性离线演练：脚本解析双语场景卡表逐项检查，156 项全部通过、可复算。
- 八案例表加"在本方案的落点 / 明确不迁移"两列，每个案例同时说明取什么、不取什么。
- 指标 43 → 45（qi_protocol_rule_count=7、qi_protocol_check_count=156）；compliance agent.2、visual 双语计数行同步。

**管线**：render_proposal_html → refresh_submission_manifest → 四门自检（deterministic / spatial / visual / professional 全 PASS）→ participant_preflight PASS。

## v1.0 - 2026-08-18

初版 formal 双语包（opencode/kimi-k3 生成）：一条龙脉、三区五带空间结构，全部图层从临时边界确定性派生，四门自检通过，PR #3243 合并（intake 评审 70/100）。
