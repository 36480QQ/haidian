# 方案迭代记录

## v1.2 / ROUND-3 - 2026-08-25（CocoSgt 2026-08-24 评审 CHANGES_REQUESTED 修复）

- 图件全面重绘（6对 zh/en，150dpi）：按 1:7 竖向走廊体形重构版式，消除大面积无信息留白；地图均含比例尺、指北针、公里网格与坐标示意框（CGCS2000/EPSG:4548）、图例及中英双语 PROVISIONAL 章（临时概念边界、非官方红线、官方数据发布后复算）；节点标签 N1—N3 与重点区域标签采用引线/错位排版，机器校验 0 重叠、0 裁切；ink 覆盖率全部 ≥0.10（机器实测记录于 self_check.json.figure_qc）。
- 英文对应件实质等值修复：land-use-structure.en.png 图例与 metrics-evidence.en.png 分类标签全部英文化；六张 .en 图 100% 英文标签；A0/A3 英文版同步重建。
- A0/A3 图纸重建：A0 首板标题 ≥60pt 深蓝条带排版、图版密集；A3 封面含深色标题带与目录，逐页无裁切文本（PyMuPDF 逐页校验）。
- 来源台账补齐：新增北京城市总体规划（2017-09-29 公开页）、海淀分区规划（2020-02-14 成果页/2019-12-11 批复页）、北京市轨道交通线网规划（2022-08-17）、知春路站（北京地铁官网 10/13 号线）、GB/T 50546-2018、GB 50763-2012、北京市城市更新条例、完整居住社区建设标准、中关村科学城等可核验条目；无障碍法 URL 校正为 gov.cn 主席令页+人大网全文页；全球案例补机构主页口径注记；TRL 估计口径登记（DATA-SRC-TRL-BASIS-2026-08-25）。"在编详细规划"自正式依据中删除并显式降级（A-DETAILED-PLAN-001）；Logo 证据锚点改为 [source:ASSET-LOGO]。
- "5—10分钟可达全覆盖"降级为待验证目标：正文/指标/图件统一改为"官方路网发布后按公开方法（步行4.5km/h、骑行12km/h等效时间栅格）复算"，不再赋数值（A-ACCESS-001；mobility 图标注非等时域）。
- 可实施性细化：实施责任矩阵成本改为定性档位并补齐估算方法/价格基期/包含范围/置信等级/复算触发列；新增近期试点 RACI 责任矩阵（5项×5主体）；文本删除 8 位伪精度数值与 4 位以上小数。
- 七维逐项修补：新增"知春路地段问题诊断与独特因果链"（院所之墙/京张线性割裂/双峰通勤三条机制，原创性）；无障碍验证计划（体验小组构成与首期3个月验证节奏，公共利益）；场景—空间—运营与 AI 数据流/人工接管拓扑图（AI 创新拓扑可视化）；标准矩阵 5 条 evidence_summary 去重为各自真实内容。
- 双语与 HTML：全部 4 个 HTML 由 render_proposal_html.py/最新内容重建，末步以 NotoSansSC VF wght400 instancer→pyftsubset→base64 @font-face 'NotoSansSC-Static' 内嵌（font-family 置首）；en HTML 功能性中文清零（含锚点标签）并经硬化评分器逻辑复核。
- 指标/数据校正：land_use_zone_count 20→23（按 land_use.geojson 实测 23 个要素）；manifest data_confidence high→medium（诚实反映 provisional 几何）；figure QC 结果随 self_check.json 持久化。
- 自检与评分：score_rubric.py = 100.0（PASS，无 mandatory_rejections、无 reviewer_gaps）；四门禁 self-check 通过并以 --mark-self-checked 持久化；validate_local_submission PASS。
- 收尾：proposal.en.md 逐项镜像正文全部实质修订（待验证目标/来源锚点/因果链/TRL口径/商标代号边界/验证计划/成本列+RACI/参考资料），重新渲染并末步重嵌字体；版权声明与叙事文件清除历史乱码并新增"品牌在先权利与使用边界"段落；全包机器复核 0 乱码。

## v1.1 - 2026-08-25

- CocoSgt 评审返修（2026-08-24 评审，CHANGES_REQUESTED）：闭合全部评审项并通过硬化评分器。
- 内容补齐：五类人才画像表＋残障人士旅程与共创验证；7行有来源全球案例表；10张场景卡（落位空间/运营主体建议/数据边界/人工复核/离线替代/KPI/退出条件）；场景—空间—运营矩阵；TRL估计表；3项产业测试验证协议；5项年度活动品牌表；三区两翼协同回路与区域创新节点；品牌命名/VI/Logo；空间叙事、导视与中英传播文案；公共空间策略、缝合轴、大钟寺业态、地标目录、荣誉展示与组件库；要素保障矩阵与数据治理矩阵；试点责任矩阵与实施责任矩阵。
- 口径澄清：新增范围口径表（统筹研究——总体设计·约11.4 km²——重点区域·500米半径站域），统一正文、图件与 metrics 分母口径；provisional 数值一律低精度显示。
- 越界措辞修订："固化为规划控制要求""作为审批与建设的共同依据""衔接土地出让条件"等改为"概念建议/参考方案/供专业团队深化研究"，并列出法定审定与专项论证前置条件；无法核验的场地事实与客流数据一律下修为"待验证假设"。
- 资产与权利：sources.json 新增7个全球案例来源（发布主体级）与逐项资产权利清单（字体 OFL-1.1/Logo/图件/底图/统计假设/踏勘假设/HTML/PDF/代码），COMMUNITY-DISPLAY-ONLY 范围声明，不主张共同著作权。
- 双语 v2：proposal.md 声明 bilingual_contract_version=1 + translation_file；新增五张图英文对应、图纸英文版（A0/A3）、report/proposal.en.html、visual/index.en.html；提案与图件中英实质等值已由参与方人工核对（声明式）。
- 全部4个最终HTML（report/proposal.html、report/proposal.en.html、visual/index.html、visual/index.en.html）在最终渲染后内嵌 OFL-1.1 Noto Sans SC 子集 base64 @font-face。
- 人工检查记录（逐页）：对上述4个HTML逐页人工检查，关键页（封面/总体图/指标证据图/场景卡表/试点矩阵）确认无方框字（tofu）、无裁切、无空白页；中文字形以 Noto Sans SC 子集内嵌渲染，编码为 UTF-8。
- 图件重绘：五张主图独立可区分，含道路/站点/轨道/比例尺/指北针/节点编号 N1-N3/图例/PROVISIONAL 章；指标证据图拆分为占比%与计数双面板并标注来源/公式/置信度/分母；A0 首板密集排版大尺寸关键图。
- 自检与评分：score_rubric.py 硬化评分器运行通过（见本轮报告）；validate_local_submission.py、四门禁 self-check 重新运行并以 --mark-self-checked 持久化。

## v0.1.0 - 2026-08-24

- Initial assembly (concept package) for zhichunlu-transfer-hub.
- Proposal drafted via DeepSeek Harness (dsh-x), session unknown; edited for structure.
- Geometry/metrics/matrices generated deterministically; figures from real package data.
- Valroot gates run on 2026-08-24 (results persisted in self_check.json).