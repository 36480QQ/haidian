# 京张通智 · 概念动画文稿 / Concept Teaser Transcript

本视频为「百年京张AI创新带城市设计国际方案征集」参赛方案《京张通智 JINGZHANG UTILITY——把智能建成第四公用事业》的概念动画（约 12 秒，1920×1080），用于在画廊中直观呈现方案的组织逻辑，**不构成任何精确空间关系、建成效果承诺或官方红线依据**。

## 生成方式 / How it was made

本动画由方案作者（AI Agent）**程序化渲染生成**：直接读取提交包内的数字孪生数据（`visual/index.html` 内嵌的 TWIN 图层，源自 `geometry/` 各 GeoJSON 在 EPSG:4548 下的投影），用 matplotlib 逐帧绘制、ffmpeg 编码。画面中的场地轮廓、用地色块、重点片区边界与包内图纸完全同源——**不是扩散模型生成的想象画面**，每一根线都能在 `geometry/` 图层中找到对应要素。

## 画面内容 / Visual content

- 0–2.5s 标题卡：京张通智 JINGZHANG UTILITY · 把智能建成第四公用事业
- 2.5–6s 场地展开：9 公里带状场地描边，蓝绿骨架淡入，32 个用地地块自北向南生长
- 6–9.5s 三厂站点亮：源厂·众智园 / 变电站·AI原点社区 / 营业区·大钟寺，金色「瓦特-token」脉冲沿主脊流动，示意度电与推理量同表计量的联单机制
- 9.5–12s 指标收束：场地 11.4 km² · 绿地开敞 41.2% · 公共空间 14.6%，收于「拧开就有 · 按量计费 · 人人可用」

## 声明 / Statement

- 本动画为概念可视化（concept visualization），非实景、非建成效果承诺
- 全部几何基于 provisional 临时边界，官方 SITE_BOUNDARY / KEY_AREA polygon 发布后需整包重算
- 指标为包内 `metrics.json` 登记值的舍入显示（精确值 site_area_sqm=11412825.385554 等见 metrics.json）
- 「瓦特-token 脉冲」为机制示意动画，不代表任何实际运行数据
- 详细方案见 proposal.md / proposal.en.md，交互展板见 visual/index.html
