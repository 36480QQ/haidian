# 版权、生成方式与逐路径权利台账 / Copyright and Per-path Rights Ledger

版本：v0.3（2026-08-14）  
作者署名：张洁静 / Joyzhang0923  
生成协作：OpenAI Codex（GPT-5 family；当前会话无法取得更精确部署标识）。

## 总体声明

本提交不包含商业地图瓦片、新闻图片、第三方Logo、人物肖像、企业标识或未经授权的规划图。国际案例仅引用机构官网的文字机制，不复制网页图片、品牌图形或版式。所有空间建议均为概念建议，不构成规划审批或政府承诺。

## 逐路径台账

| 路径 | 生成方式与来源 | 权利/限制 |
| --- | --- | --- |
| `proposal.md`, `proposal.en.md` | 张洁静提出主题与署名；Codex依据公开/清权任务资料协助重写，中英文人工审校待完成 | COMMUNITY-DISPLAY-ONLY；不得冒充官方文件 |
| `geometry/site_boundary.geojson`, `geometry/key_areas.geojson` | 仓库维护的临时粗略边界派生 | 仅用于概念生成、展示、自检；非官方红线 |
| 其他 `geometry/*.geojson` | Codex依据临时边界与本方案设计逻辑生成的原创概念几何 | 非法定规划、非工程线位、非权属判断 |
| `metrics.json` | 从结构化几何或成果计数复算；法定控制缺失项保持未知 | 不得作为批准指标 |
| `assets/figures/*.png` | 本地Python/Pillow从GeoJSON、metrics和任务矩阵绘制；未嵌入外部图片 | 原创派生图；Noto Sans SC字体按SIL Open Font License用于栅格化显示 |
| `report/proposal*.html` | 仓库离线渲染脚本从Markdown生成 | 无远程资源、脚本、跟踪或外部字体 |
| `visual/index*.html` | 本地生成的离线静态展示，引用提交内图件 | 无CDN、远程瓦片、iframe、表单或跟踪 |
| `drawings/*.pdf` | 本地Pillow将五张核心图排版为A3文册和三张A0展板 | 展示成果，不是权威数据源 |
| `sources.json` | 官方/清权资料与六个机构官网的来源登记 | 案例官网仅用于机制比较；不授权复制其品牌资产 |
| `agent.json`, 三个矩阵与 `self_check.json` | 仓库脚手架、Codex修订与官方校验脚本输出 | 机器审计资料；不得解释为维护者批准 |

## 字体与代码

- 图件使用 Noto Sans SC 栅格化，字体许可为 SIL Open Font License 1.1；字体文件不随包提交。
- 绘图与排版使用 Python 与 Pillow；仓库校验和渲染使用项目自带脚本。
- 如后续加入照片、地图、历史图像、企业Logo或人物资料，必须在进入图件前新增逐项来源、许可和署名记录；无法证明权利的资产应删除或替换。

## 人工复核待办

中英文主张、数字、图位和术语等义；PDF标签和阅读顺序；色觉可辨识性；A0远视距字号；第三方新增素材权利，均需人工签字复核。本台账不替代法律意见。
