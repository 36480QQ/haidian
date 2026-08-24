# 方案迭代记录

## v1.1 - 2026-08-25

- 针对评审 CHANGES_REQUESTED 逐项修复（详见 compliance_matrix.json 与 proposal.md 新章节）：
  1. 双语包 v2：proposal.en.md 全量实质翻译（language=en、translation_of=proposal.md）；5 张英文图 + logo/协同机制图英文版；A0/A3 英文版；report/proposal.en.html 与 visual/index.en.html；manifest 条目补齐 language/translation_of。
  2. 字体无缺字：4 个最终 HTML（proposal.html / proposal.en.html / index.html / index.en.html）在最终渲染后内嵌 Noto Sans SC（OFL-1.1）子集字型（base64 @font-face，按4页实际用字裁剪，覆盖全部正文/图表字符）；离线复测正文、SVG/Canvas、图表与打印输出无缺字（tofu）后提交（人工检查项）。
  3. 专属成果补齐：Logo/VI 方向（logo.png 原始生成资产 + 命名体系 + VI 规则 + 品牌故事）；7 个全球案例表与发布主体级来源；10 张场景卡、3 项产业测试场景、5 类人群画像表（老人/儿童/视听障碍/低数字技能/非智能设备，含传统渠道兜底/共创反馈/概念验收条件与无障碍法适用范围边界）；荣誉展示体系与公共空间组件库；三级导视/符号系统与国际传播文案；开发者社区、场景开放运营与招引转化机制。
  4. 空间特异性：图件加入公开可核验街道/站点参照、图例、比例尺、指北针、PROVISIONAL 水印、现状/建议分层、场景编号（S4—S11）、节点放大内页与街段断面表达；A0 首版加密集说明块；全部图件声明非官方红线或工程结论。
  5. 分期实施矩阵（8 项目 × 12 列：牵头方/合作方/前置条件/成本级别/审批依赖/服务水平/人工兜底/评估阈值/扩展/退出回滚，全为概念建议）与长期运营责任矩阵（5 运营对象）。
  6. 指标展示精度：文本/前端按约11.4平方公里、约19.5%、约0.3% 展示，公式、置信度与官方几何到位后的自动重算触发条件成表；metrics.json 保留机器精度；metrics-evidence 图按比例% 与计数分栏。
  7. 资产权利台账：sources.json 新增 7 条全球案例（发布主体级）与 7 条资产台账（底图/街景照片/字体/图标/案例/数据/代码/生成资产），逐项许可+归属+转换+限制；未进入成果的调研材料明确用途边界（内部推导，不公开不引用不传播）；COMMUNITY-DISPLAY-ONLY 范围，不主张共同版权。
  8. 跨区协同与国际化传播：北纬社区/未来科学城/怀柔科学城/经开区/京津冀要素交换与合作接口 + 机制示意图 + 中英传播文案（简洁可核验、不过度承诺）。
  9. 矩阵与校验件更新：compliance_matrix.json 1.4.x 范围文本归位、agent.1—6 report_sections/evidence_summary_zh 重写为真实章节；design_depth_matrix.json 新增 7 项（品牌VI/荣誉展示组件库/导视符号/跨区协同/开发者社区/分期运营责任/指标展示精度）。
- 门禁：valroot 四门禁（deterministic/spatial/visual/professional）全部通过后由 self_check 按要求标记；评分脚本 reviewer_gaps 清零。

## v0.1.0 - 2026-08-24

- Initial assembly (concept package) for zhongguancun-avenue-ai-spine.
- Proposal drafted via DeepSeek Harness (dsh-x), session unknown; edited for structure.
- Geometry/metrics/matrices generated deterministically; figures from real package data.
- Valroot gates run on 2026-08-24 (results persisted in self_check.json).