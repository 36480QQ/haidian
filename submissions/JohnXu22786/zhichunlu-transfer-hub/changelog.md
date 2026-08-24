# 方案迭代记录

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