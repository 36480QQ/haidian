# 听得见的断点 / The Audible Break · 数据可听化档案与权利记录

**关联媒体：** `assets/media/audible-break.m4a`（中文旁白版，80.6 秒）· `assets/media/audible-break-en.m4a`（英文旁白版，78.9 秒）；同步字幕 `audible-break.vtt` / `audible-break-en.vtt`
**性质：** OP-04 节点连通性档案数据的可听化（sonification）。概念交付物；程序合成，非实地录音，不产生任何绩效指标数值。

## 一、这是什么

方案的核心命题是 AI 开启与 AI 关闭服务等价。OP-04 的证据链档案里有两组读数：AI 开启状态沿直接路径 605.811 米可达 OP-08；AI 关闭状态在接入段 88.816 米之后不存在连续路径。本音频把这两组数字翻译成声音——**声音停止的位置，就是数据里断点的位置**。数据的另一条感官通道：图版给眼睛（op04-detail），本档给耳朵。

## 二、数据 → 声音映射规则（逐项可核）

| 规则 | 取值 | 核对方式 |
| --- | --- | --- |
| 时间比例 | 1 秒 = 20 米 | 设计常数 |
| 行进声 | 连续 440 Hz 基音 + 每 0.5 秒一声 1600 Hz 轻响（= 每 10 米一响） | 数波形脉冲数 |
| 段一时长（AI 开启全程） | 605.811 ÷ 20 = 30.29 秒 | `seb-op04-chain-data.json` stage_4 BASE_ON 读数 |
| 段二中断时刻（AI 关闭） | 88.816 ÷ 20 = 4.44 秒（段内） | 同档案 BASE_OFF 接入段读数 |
| 到达音 | 上行三音（523/659/784 Hz） | 段一结尾 |
| 断点表达 | 行进声戛然而止 → 1.6 秒静默 → 110 Hz 低音三响 | 段二结尾；静默区实测 RMS = 0 |

中文版时间轴：段一起点 20.047s · 段二起点 62.499s · **断点时刻 66.94s** · 全长 80.567s。英文版对应 16.935/59.724/**64.165**/78.941s。

## 三、生成方法与权利

- 数据音：纯程序合成（正弦波与包络，Python 标准库），零采样素材、零第三方音源；
- 旁白：MiniMax `speech-2.8-hd` 预置合成音色（中文 Reliable_Executive / 英文 Trustworthy_Man），与包内导览同一权利链（条款存档与快照指纹见 `sources.json`）；
- 无音乐、无实地录音、无真人声音；容器内嵌标题、作者、合成声明与许可指针；
- 许可：随包 COMMUNITY-DISPLAY-ONLY；
- **非观测声明：** 本音频呈现的是桌面复算档案中的两组数字，不是现场测量，不是可达性结论；「断点」的空间前提本身仍待现场审计（档案原文如此登记）。

## Rights and synthesis statement (English summary)

This piece is a **data sonification** of two archived readings from the OP-04 connectivity chain (605.811 m reachable with AI on; no continuous route beyond the 88.816 m stub with AI off), at one second per twenty metres — where the sound stops is where the data holds no route. Data tones are pure program synthesis (sine waves, standard library, zero samples); narration uses the MiniMax preset synthetic voices under the same registered terms as the package's audio guides. No music, no field recording, no human voice. The silence at the break measures RMS 0. It is a desk-replay rendering, not a field measurement, and the break's spatial premise itself remains pending site audit.
