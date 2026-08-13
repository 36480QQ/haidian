# 品牌与视觉识别系统（Logo / VI）

> 配套可视化见 `visual/logo-vi.html`（标志、色彩、字体、应用规范，含内联 SVG 与双语界面）。
> 本文件为文字规范（Brand Guidelines），供评审、深化与落地使用。

## 1. 命名逻辑

- **中文名**：**京张智脉**（Jīngzhāng Zhìmài）
  - 「京张」锚定地理与文化遗产——京张铁路（中国首条自建干线，詹天佑主持）；
  - 「智脉」双关：既指**智能之脉络**（AI 创新带如血管般串联三区与绿脉），又谐音「智迈」（智能迈进），呼应「铁路遗产 → 智能原生城区」的跃迁。
- **英文名**：**Rail-to-Brain**
  - 直译「从铁轨到大脑」：铁轨（rail，工业遗产）进化为城市智能体之脑（brain，AI 原生），点明方案核心叙事。
- **组合**：`京张智脉 · Rail-to-Brain`，中文名为主、英文名为辅，全域统一。

## 2. 标志（Logomark）概念

标志为「铁路 → 神经网络」的形变单体：

- **底部两条铁轨**（金 #E8B04B）由两侧向中心收束，象征京张铁路遗产与线性公园主轴；
- 轨道在中心汇为一**竖干**（蓝 #2E6FF2），向上分叉为**三组神经节点**（紫 #7B5CFF），象征铁路进化为城市智能体的「脑」与「脉」；
- 中心**金色节点**为汇聚点，喻「众智园—AI 原点—大钟寺」三核一体。

标志含义可概括为：**以百年铁路为基，生长出面向未来的智能脉络**。矢量文件见 `visual/assets/logo.svg`（可无限缩放，无字体依赖）。

## 3. 色彩系统（Color Tokens）

| 名称 | 用途 | HEX | RGB |
| -- | -- | -- | -- |
| 铁轨金 Rail Gold | 遗产/主轴/强调 | `#E8B04B` | 232,176,75 |
| 智脉蓝 Brain Blue | 科技/智能体/主色 | `#2E6FF2` | 46,111,242 |
| 京张紫 Jingzhang Purple | 创新/文化/节点 | `#7B5CFF` | 123,92,255 |
| 绿脉 Green | 蓝绿/公共空间 | `#3FB68B` | 63,182,139 |
| 墨 Ink | 背景/正文（深） | `#0B0E13` | 11,14,19 |
| 纸 Paper | 背景/正文（浅） | `#F4F1EA` | 244,241,234 |

- **主色**：智脉蓝；**辅色**：铁轨金 + 京张紫；**自然色**：绿脉。
- 深色背景用墨，浅色背景用纸；标志在墨/纸底上均保证对比度 ≥ 4.5:1。

## 4. 字体（Typography）

- **中文**：思源黑体 / 思源宋体（Source Han Sans / Serif）优先，回退 `PingFang SC`、`Microsoft YaHei`、`Noto Sans CJK SC`。
- **西文**：无衬线 grotesk，回退 `Inter`、`Helvetica Neue`、`Arial`。
- **层级**：标题 28–44pt / 正文 14–16pt / 标注 11–12pt；中文标题可用宋体增强文化气质，西文与数据用黑体/等宽。
- **注**：本交付不内嵌字体文件，遵循系统字体栈，避免字体再分发许可问题（详见 `report/copyright_statement.md` §3）。

## 5. 应用规范（Applications）

| 场景 | 规范要点 |
| -- | -- |
| 主标识 | 标志 + 中英组合，留白 ≥ 标志高度的 1/2；深底用纸色字，浅底用墨色字。 |
| 导视系统 | 铁轨金用于主线/箭头，智脉蓝用于信息，绿脉用于生态节点；节点编号与 `scenarios/scenario-cards.json` 的 NODE-xx 对齐。 |
| 节点徽标 | 14 个 AI 服务节点各取标志的「单节点」变体，配 NODE-xx 编号与片区色（众智园金、AI 原点蓝、大钟寺紫、绿脉绿）。 |
| 工牌 / 发布物料 | 标志居左，Rail-to-Brain 英文小字置于中文名下方；发布厅物料用京张紫作强调。 |
| 数字端 | favicon 用标志单色版；网页沿用墨底 + 金/蓝/紫强调，与 `visual/index.html` 一致。 |

## 6. 使用禁忌（Do / Don't）

- **Do**：保持标志比例与留白；深色/浅色版本按需切换；节点徽标与 NODE 编号配套使用。
- **Don't**：不拉伸/旋转标志；不更改色彩（尤其不用纯红/纯绿替代主色）；不在低对比背景上叠加；不将标志与无关商业品牌并列；不声称标志已由官方注册或获批（本标志为投稿方案概念稿，非注册商标）。

## 7. 法律状态声明

本 Logo / VI 为**投稿方案的概念性视觉提案**，非任何机构已注册标识；名称「京张智脉 · Rail-to-Brain」及标志图形版权归作者（生成式辅助设计，见 `report/copyright_statement.md`），如被采纳须由相关主体另行完成商标注册与品牌合规审查。

---

## EN · Brand & Visual Identity (summary)

- **Name**: 京张智脉 · **Rail-to-Brain** — railway heritage evolving into an AI-native urban "brain/vein".
- **Logomark**: two gold rails converge into a blue stem that branches into three purple neural nodes; a gold hub denotes the three-core union. Vector: `visual/assets/logo.svg`.
- **Palette**: Rail Gold `#E8B04B`, Brain Blue `#2E6FF2` (primary), Jingzhang Purple `#7B5CFF`, Greenway `#3FB68B`, Ink `#0B0E13`, Paper `#F4F1EA`.
- **Type**: Source Han Sans/Serif (CJK) + grotesk (Latin); system stacks, no embedded fonts.
- **Applications**: signage, 14 node badges aligned to NODE-xx, staff/credentials, launch materials, digital favicon.
- **Legal**: conceptual proposal only; not a registered trademark; copyright rests with the author; trademark clearance required if adopted.
