# 叙事摘要与 SP-Survey 协议附件

权威正文为 `../proposal.md`。本文件提供阅读摘要，并收录可部署的人在环路调研协议（本次未实跑）。

## 叙事摘要

京张铁路以第一人称觉醒感知系统；可感京张用感知断面与 SP-Survey 协议把公共空间优先序变成可复算、可问人的概念建议。

## SP-Survey 感知复测协议

# SP-Survey 感知复测协议（可部署，未实跑）

> 本文件是投稿附件：描述如何用人在环路评价校准「可感京张」感知基线。  
> 本次提交**不包含**已完成的受访者数据，不把空结果写成事实。

## 1. 目的

校准模型估计的断面短板排序，比较干预前后（概念方案 A/B）的公众偏好，回写 `assumptions.json` 与下一轮 `geometry/public_space` 优先级。

## 2. 工具

- 平台：SP-Survey（https://sp-survey.org）及开源部署
- 配置：同目录 `project-config.json`
- 方法参考：SP-Survey 论文；热舒适/街景感知仅作方法背景，不直接使用未清权街景图

## 3. 样本与伦理

- 目标人群：青年通勤者、居民、访客、骑手、行动不便使用者（配额抽样概念）
- 知情同意、可随时退出、不采集可识别生物特征
- 不上传个人轨迹；媒体仅用自制图示/概念渲染/清权示意图
- 未成年人数据不采集

## 4. 问卷模块

1. 人口背景（可选、粗粒度）
2. 断面图示两两比较（stated preference）
3. 遮阴/停留/夜间安全感李克特量表
4. 干预前后场景偏好
5. 开放反馈（可选）

## 5. 回写机制

- 聚合偏好 → 更新 shortfall 权重假设
- 显著分歧条目 → 进入人工复核清单
- 结果进入 changelog，并触发感知合约看板更新（概念流程）

## 6. 与方案的接口

- 空间对象：`PS-SEC-*` 感知断面、`PS-LM-*` 地标
- 指标：`mean_perception_shortfall`, `high_shortfall_section_count`
- 运营：年度感知普查 + 微短剧共创的公众触点


## 可部署配置（JSON）

```json
{
  "project_id": "sensible-jingzhang-second-survey",
  "title": "可感京张 · 第二次测量（感知偏好协议）",
  "version": "0.1.0",
  "language": "zh",
  "status": "protocol_ready_not_fielded",
  "ethics": {
    "informed_consent": true,
    "allow_quit_anytime": true,
    "no_biometrics": true,
    "no_raw_trajectories": true,
    "media_policy": "self_generated_or_cleared_diagrams_only"
  },
  "modules": [
    {"id": "consent", "type": "consent", "required": true},
    {"id": "persona_block", "type": "matrix", "required": false},
    {"id": "section_pairwise", "type": "ranking", "trials": 12, "required": true},
    {"id": "likert_comfort", "type": "matrix", "dimensions": ["shade", "stay", "night_safety"], "required": true},
    {"id": "intervention_ab", "type": "image_choice", "required": true},
    {"id": "open_feedback", "type": "text", "required": false}
  ],
  "stimuli": {
    "source": "assets/figures/* and self-generated diagrams",
    "forbid": ["uncleared_street_view", "faces", "copyrighted_photos"]
  },
  "linkage": {
    "geometry_features": ["PS-SEC-01", "PS-SEC-02", "PS-LM-1", "PS-LM-2", "PS-LM-3"],
    "metrics": ["mean_perception_shortfall", "high_shortfall_section_count"]
  }
}

```
