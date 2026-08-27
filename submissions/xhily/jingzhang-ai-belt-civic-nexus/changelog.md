# 方案迭代记录

## v1.2 - 2026-08-26

针对 AI Agent 第二轮评审意见（request-changes，七维加权 77.0/100，表达完整度 3/5）执行可视化精修，全部 P0 已完成并通过本地四闸门自检。

### P0 修复（可视化阻断项）
- **metrics-evidence 中英文图**：改用 figure-fraction 坐标 + 显式预留底部边距，移除 `fig.tight_layout()` 对 metrics 轴的影响，将临时边界警示居中置于底部预留区；彻底解决底部字段裁切/叠印问题，所有指标卡、证据链完整可读。
- **site-overview 中英文图**：保留核心星形图标，将 L-01/L-02/L-03 与核心名合并为带白底圆角框的 callout，通过 leader line 引出到多边形外侧，消除中文标签与节点图标的重叠。
- **key-areas 中英文图**：片区名与说明改为右侧白底圆角框 callout，leader line 指向各核心中心；移除原两翼标注（避免与 callout 重叠），两翼信息由正文与 site-overview 覆盖；图幅加宽至 9×11 以容纳英文长文本，消除描边超出画布造成的残影。
- **A0/A3/HTML 同步重生成**：以修复后的源图重新运行 `build_drawings.py`（4 份 PDF）与 `render_proposal_html.py`（2 份 report HTML），并重新内嵌中文字体；完成桌面/移动视口人工视觉 QA，确认无裁切、无标签遮挡、临时边界警示醒目、中英文图位对应。

## v1.1 - 2026-08-24

针对 AI Agent 评审意见（request-changes，七维加权 68.0/100）执行修复，覆盖 P0 与 P1 项，并完成中英文人工对照复核。

### P0 修复（阻塞项，已全部完成）
- 内嵌子集化 Noto Sans SC 字体（woff2 base64 `@font-face`）到 report/proposal.html、report/proposal.en.html、visual/index.html、visual/index.en.html，消除评审核对环境下的中文方框（tofu）。
- 修复 visual/index.html 与 visual/index.en.html 的离线资源路径：`assets/figures/*.png` 修正为 `../assets/figures/*.png`，恢复 5 张核心图件。
- 重排并重新导出五组中英文图件（portrait 朝向、图例外置、去除面内标签互压、水印避让指北针、metrics-evidence 底部留白），消除标签互压、图例遮挡、裁切与叠字；英文图清除中文残留。
- 更正 visual/index 状态文字：明确为 provisional 非官方边界、非精确用途、未来复算说明，不再出现"官方 polygons 到位前不得 formal scoring"的冲突表述。

### P1 修复（已完成）
- 为 C-01—C-06 六个全球案例补充逐项来源、事实范围、获取时间与复用边界，新增 sources.json 条目 CASE-C01—CASE-C06；全部标注"仅作机制类比、未声称官方合作"。
- 新增"区域创新协同关系（三核两翼 × 区域创新网络）"矩阵，明确北纬社区、未来科学城、怀柔科学城、经开区、京津冀与三核两翼的差异化角色、要素流与协同接口；跨节点合作一律标为概念建议。
- 完成中英文人工对照复核：proposal.md 与 proposal.en.md 的案例来源核验表、区域协同矩阵、概念建议标注已逐节对照，确保语义一致、无遗漏翻译与无新增中文残留。

### 待办 / 开放项
- 修复包重新上传至 PR（需新的 GitHub PAT），并触发 CI 复跑。
- 待组织方发布正式 polygons 后，统一替换 provisional 边界并复算指标。

## v1.2.1 - 2026-08-27
- 重新触发 submission-validation：上一轮（v1.2）校验因 15 分钟全局 API 锁排队超时被判 cancelled，round3 图件修复（metrics-evidence 底部裁切、site-overview/key-areas 标签重叠）未进入 AI 评审队列；本次以一次真实提交重新触发 pull_request_target 校验，投稿内容不变，仅补充本变更记录。
