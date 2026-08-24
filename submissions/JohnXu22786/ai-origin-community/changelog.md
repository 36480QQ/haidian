# 方案迭代记录

## v1.1 - 2026-08-25

- Reviewer (CocoSgt 2026-08-24) CHANGES_REQUESTED repair round: closed all 11 hardened-scorer gaps and the 9 mandatory next steps.
- Fixed XX placeholders to unknown + estimation method + required data + recalculation trigger; unified persona count (6类人才画像 = metrics.json persona_count=6) with two 6-row persona/journey tables.
- Added 7-row sourced global case table (Station F / One-North / Toronto Quayside / King's Cross / 22@ / Cyberport / Zhangjiang) with publisher-level citations in sources.json (7 case entries); added per-asset rights ledger (font/logo/figures/geometry/HTML-PDF/code/generation tool/policy snapshots, 8 entries, license+attribution+restrictions), COMMUNITY-DISPLAY-ONLY scope stated.
- Expanded content to 21 sections: 三区两翼与区域协同回路（北纬社区/未来科学城/怀柔科学城/经开区/京津冀，建议性机制+机制图）、品牌与视觉识别（AI Origin Community 原点公社、命名体系、原创概念Logo、VI规则、中英传播文案）、全球案例对标与产业要素保障、10张场景卡+场景-空间-运营矩阵+TRL估算、3份产业测试验证协议+场景开放运营、公共空间地标与组件库深化、历史文化叙事与导视系统、年度活动品牌体系（5项）+开发者社区+人才转化、无障碍与包容设计（六类服务人群旅程+概念验收清单）。
- Regenerated all figures (legend/north arrow/scale/NOT-TO-SCALE/PROVISIONAL stamps; metrics split into ratio % and integer count panels), added mechanism diagram and neutral logo asset; regenerated A0 (real 1189x841mm, dense single board) and A3 (real 420x297mm, 7 pages) PDFs with headers/footers/page numbers/provisional notes.
- Full bilingual v2 contract: proposal.en.md complete translation; 6 English figures; English A0/A3 PDFs; visual/index.en.html; report/proposal.en.html via renderer; manifest maps every counterpart (language en + translation_of).
- Chinese-box fix: OFL-1.1 Noto Sans SC subset (fontTools) base64-embedded with @font-face into report/proposal.html, report/proposal.en.html, visual/index.html, visual/index.en.html (recorded as ASSET-FONT-NOTOSANSSC-OFL in sources.json).
- Unified provisional scope vocabulary (统筹研究范围约11.4km² / 总体设计范围约1.1km² / 重点区域约368公顷概念口径) with recalculation triggers; rounded all human-facing numbers.
- Valroot gates + scorer re-run on 2026-08-25 (all four gates PASS, weighted_pct 100.0, reviewer_gaps empty).

## v0.1.0 - 2026-08-24

- Initial assembly (concept package) for ai-origin-community.
- Proposal drafted via OpenCode CLI (opencode), session ses_fccc7fe77ffeLlXpKBXz2Wm0ad; edited for structure.
- Geometry/metrics/matrices generated deterministically; figures from real package data.
- Valroot gates run on 2026-08-24 (results persisted in self_check.json).
