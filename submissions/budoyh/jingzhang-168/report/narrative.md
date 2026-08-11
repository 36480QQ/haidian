---
title: "京张168 v3.0：评审阅读索引"
author_github: "budoyh"
language: "zh"
license: "COMMUNITY-DISPLAY-ONLY"
---

# 京张168 v3.0：评审阅读索引

本文件是派生阅读索引，不是第二份方案正文。完整中文正文见 `proposal.md`，结构等价英文正文见 `proposal.en.md`；若展示层与机器可读资产冲突，以本包 JSON、GeoJSON、更高等级来源及后续人工专业复核为准。

## 三分钟阅读路径

1. 先看 `assets/figures/site-overview.png`：现状约9公里走廊、已开放一期、临时三层范围与三座城市站被明确分层，OSM约412.5米背景差异只披露、不替代边界。
2. 再看 `assets/figures/key-areas.png`：众智验证园、AI原点开放换乘厅与大钟寺城市公共终点站采用三种不同剖面，而不是复制同一“AI盒子”。
3. 看 `assets/figures/metrics-evidence.png`：12项服务合同、72个合成分支、24个停止分支、12个复原分支和0真实个人数据；现场绩效仍为 `null`。
4. 打开 `visual/index.html`：首屏说明“公共底盘不可关闭”，并以12个稳定定位码回指任务、空间、治理、实施、指标、风险与来源证据。
5. 审阅双语 A3 前三页与 A0 前三板：当前事实、空间总图、Layer 0/1、三站原型和运行协议均进入固定评审视窗。
6. 最后用 `compliance_matrix.json`、`standard_matrix.json`、`design_depth_matrix.json`、`visual/assets/civic-timetable.json`、`visual/assets/timetable-tabletop-evidence.json` 与 `risk.json` 逐项复核。

## 核心判断

京张铁路曾用运行图把工程、时间和责任组织成可执行系统。v3不再把“168”当活动口号，而把它做成城市公共时刻表：现状公共路径、静态信息、遮荫座椅、纸面/电话/人工求助构成不可关闭的 Layer 0；AI服务只作为按表到站、具名人工、最小数据、可停运、可复原的 Layer 1。

三站承担不同现实矛盾：众智验证园把公共观察边、限时合成测试场与隔离后勤分开；AI原点开放换乘厅把无账号前台、成果翻译工坊与知识产权/数据后室分开；大钟寺城市公共终点站把全天首层、有人柜台和与真实账户/支付隔离的合成沙盒分开。

`visual/assets/tabletop-runner.js --check` 对12份合同各演练6类合成分支。PASS只证明字段与失败路径闭合，不证明任何现场运营、容量、安全、授权或公共价值结果。v2的 `97M m²·h/week` 头部值已撤回；官方公园名录中的24小时开放事实只适用于现状名录对象，不外推到整个临时总体范围。

## 图像与版权边界

五张中英核心证据图、双语HTML和技术PDF由本包 GeoJSON/JSON 确定性生成。三张 2026-08-11 GPT Image 2 分站点概念图均为无文字 `presentation only` 体验层；大钟寺初稿出现的伪文字已通过定点编辑清除并复核。完整提示、原始输出标识、人工检查和禁止用途见 `visual/assets/rights-ledger.json`，许可总说明见 `report/copyright_statement.md`。
