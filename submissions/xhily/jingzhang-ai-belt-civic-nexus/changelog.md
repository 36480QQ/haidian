# 方案迭代记录

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
