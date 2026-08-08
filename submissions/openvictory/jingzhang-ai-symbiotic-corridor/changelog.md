# 方案迭代记录

## v0.3 - 2026-08-08

响应七维评审 55.0/100，在 v0.2 基础上继续推进：

### 空间几何丰度大幅提升

- buildings.geojson: 6→24 个建筑基底（众智园6+原点社区6+大钟寺6），覆盖 ai_r_and_d / incubator / lab / office / mixed_use / cultural / education / retail / talent_apartment / community_service 全部建筑类型
- roads.geojson: 5→20 条道路（含 secondary / branch / cycleway / pedestrian / greenway / transit_connection / local_access），构成三区互联慢行网络
- green_space.geojson: 1→5 块绿地（遗址公园主轴 / 众智园生态廊道 / 原点口袋公园群 / 大钟寺绿轴 / 小月河缓冲带），面积按多边形并集去重后与 site 取交集计算
- public_space.geojson: 1→6 块公共空间（开源广场 / 创享广场 / AI展演广场 / 遗址公园活动节点 / 小月河社区客厅）
- phasing.geojson: 1→3 期（一期众智园+原点 / 二期原点社区深化 / 三期大钟寺+小月河）

### P2 公共利益与治理证据

- 新增弱势群体设计验证表：老年人 / 儿童 / 残障人士 / 低收入劳动者 / 非数字用户，各含核心需求 / 空间响应 / 服务替代 / 验证指标
- 新增公众参与与申诉机制：社区共治委员会（10席）、季度公开会议、15工作日回复承诺
- 新增算法纠错机制：3次投诉触发自动降级转人工审核
- 新增活动扰民控制：夜间55dB限值、低噪声活动100m缓冲

### 数据修正

- green_ratio 和 public_space_ratio 多边形缩小到现实城市设计尺度，按并集去重后与 site 取交集计算
- 新增 building_count=24, road_segment_count=20, green_space_count=5, public_space_count=6 指标
- 参考资料章节重写为分级排列（A0/A1/标准），含来源限制声明

## v0.2 - 2026-08-08

响应维护者评审意见（PR #92 评审，七维加权分 55.0/100，request-changes）：

- P0 统一建筑基底面积证据：geometry/buildings.geojson 全部 declared 面积按 EPSG:4548 投影复算核对；metrics.json、assets/figures/*.png、drawings/*.pdf、report/proposal.html 全部以复算值重新生成。
- P0 重做 A0 与 A3：消除大面积留白，A3 册扩展为 5 页，A0 展板扩展为三栏布局。
- P0 版权与来源尽调：report/copyright_statement.md 重写为逐资产权利登记表。
- P1 补充 agent.1-6：英文命名、Logo、全球案例、场景矩阵、AI地标、文化叙事、年度运营。
- P1 修正临时数据表达：provisional 派生指标降级为 medium 置信度。

## v0.1 - 2026-08-07

- 由 AI agent OpenSquilla（GitHub: openvictory）生成 formal 投稿包。
- 六项 agent 任务在 proposal.md 与 compliance_matrix.json 中逐条响应。
- 自检全部 PASS，审核状态 formal-review-ready。

## 待复核事项

- 官方红线、地块与控规条件到位后，替换 provisional 边界并复算全部面积指标。
- A3/A0 图纸随方案内容迭代继续完善图面表达。
- 全球案例参考文献待正式提交前补充详细比较研究。
- 字体商用授权在正式出版前需单独确认。
