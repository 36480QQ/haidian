# 四态视频与旁白记录 / Four-state video and narration record

> 视频 / Video: `4-state-motion.mp4`
>
> 海报 / Poster: `4-state-motion-poster.webp`
>
> 中文字幕 / Chinese captions: `4-state-narration.vtt`
>
> 英文字幕 / English captions: `4-state-narration.en.vtt`
> 独立旁白 / Standalone narration: `4-state-narration.mp3`

## 旁白全文 / Narration transcript

百年京张 AI 创新带方案的普通、验证、故障、恢复四态。

普通态下，任何人不注册、不扫码、不使用 AI 也能完成完整普通任务。

验证态仅作为自愿、公告、限域、可停止的旁侧叠层。

故障态下，自动化、采集、显示或服务叠层被隔离，连续日常轨、完整非 AI 路径、人工接管、撤回、申诉继续。

恢复态只先还普通路径，不等于授权、批准或 G1。

---

The Centennial Jing-Zhang AI Innovation Belt proposal has four states: ordinary, proof, failure and recovery.

In the ordinary state, anyone can complete the full ordinary task without registration, scanning or AI.

Proof appears only as a voluntary, announced, bounded and stoppable side layer.

On failure, automation, collection, display or service overlays isolate; the ordinary track, complete non-AI path, staffed takeover, withdrawal and appeal continue.

Recovery first restores the ordinary path; it is not authorization, approval or G1.

## 视频生成与合成方法 / Video generation and composition method

### 1. MiniMax H3 概念母版 / MiniMax H3 concept master

- 提供方与模型 / provider and model: MiniMax, `MiniMax-H3`.
- 接口 / endpoint: MiniMax 中国站按量 API V2, `https://api.minimaxi.com/v2/video_generation`.
- 成功任务 / successful task: `432350371770812`, generated on 2026-08-19.
- 原始输出 / source output: 15.08 s, 2560×1440, 24 fps, H.264, native stereo AAC, with embedded MiniMax AIGC metadata. The 35,574,825-byte source master is not shipped because it exceeds the submission media-size limit.
- 生成模式 / mode: one reference-to-video request with one text instruction plus three package-local reference images. No alternative H3 output was selected or combined.
- 参考图 / references: `ordinary-life-scenes.webp` supplies the human-scale collage language; `spatial-atlas.png` supplies the three non-interchangeable spatial grammars; `key-area-sections.png` supplies the ordinary/proof/failure/recovery and staffed-handoff relations. Their labels, numbers, maps and geometry were expressly excluded from reproduction as evidence.
- 生成意图 / instruction summary: one non-photoreal architectural editorial sequence moving through Zhongzhiyuan's productive commons, Origin Community's ground-floor street and courts, Dazhongsi's commute/service-side relation, and a final bounded proof-layer failure. The instruction excluded real sites, station anchors, maps, recognizable people, legible text, approvals, results, recovery times and G1 claims.
- 模型限制 / model limitations: H3 produced a generic heritage-like frontage and repeated numeric markers despite the exclusions. The final composition labels the frontage as an abstract cultural frame, covers the generated markers with a deterministic optional-proof panel, and never treats either as site evidence.

### 2. 48 秒确定性合成 / Deterministic 48-second composition

- 工具 / tool: imageio-ffmpeg bundled `ffmpeg-win-x86_64-v7.1`, using H.264/libx264 and the locally installed Microsoft YaHei font; neither the binary nor font is redistributed.
- 发布输出 / publish output: exactly 48.000 s for both picture and audio, 1,152 frames at 24 fps, 1920×1080, H.264 High, yuv420p, AAC mono; 3,180,716 bytes. The 15,520,801-byte composition master was padded by cloning its final frame for 0.125 seconds, then re-encoded locally with ffmpeg (`libx264`, slow preset, 610 kb/s target / 680 kb/s ceiling; AAC mono 48 kb/s) solely to satisfy the repository's 40 MiB package limit. Sampled key-state frames remain legible; full-video SSIM against the composition master is 0.913354. The final Git-blob SHA-256 is recorded by `manifest.json` after refresh.
- 结构 / structure: 0–4 s bilingual Twin-Track entry; 4–15 s three human-scale ordinary prototypes; 15–26 s optional proof; 26–38 s package-authored three-section failure reading; 38–48 s ordinary-life recovery. This is presentation pacing, not a real recovery duration.
- 图层 / layers: the H3 master is combined with the existing package-authored `key-area-sections.png` and the disclosed generated concept image `ordinary-life-scenes.webp`. Bilingual state labels, place labels, G0/provisional/not-site-evidence/not-approved disclosure and the 48-second pacing warning are deterministic local overlays.
- 声音 / sound: the H3 source audio is excluded. The final video uses only the existing Chinese TTS narration `4-state-narration.mp3`; its 43.344-second audio is padded with silence to the 48-second video boundary and faded at the end. No music or generated ambience is added. The standalone MP3 bytes are unchanged.
- 海报 / poster: `4-state-motion-poster.webp` is extracted from the locally composed video at 1.0 s, so the first visible state and truth boundary are available before playback.

## 可访问性与播放 / Accessibility and playback

- 视频和独立音频都使用 visible controls、`preload="none"`，且绝不自动播放。
- The video exposes both Chinese and English WebVTT caption tracks. The Chinese visual page defaults to Chinese; the English page defaults to English.
- The Chinese narration remains separately downloadable. This bilingual transcript provides the non-audio equivalent.
- 无 JavaScript时，四张静态状态卡、字幕、文字稿、图件和媒体下载链接仍可读取。减少动态模式不启动任何播放。

## 权利、真实性与不可证明事项 / Rights, truth boundary and non-provable items

- 权利状态 / rights status: `not_fully_cleared`; independent file-level rights audits remain 0. MiniMax API/output terms, the exact generated master, system-font rasterization and final composed bytes remain pending independent review.
- 生成画面中的人物、建筑、庭院、柜台、寺庙式框景、数字标记和动作均为合成概念元素，不是现场照片、确认视点、真实人员、居民反馈、现状设施或已建成状态。
- The media do not prove an official boundary, exact location, parcel, station, building, dimensions, materials, accessibility result, staffing, schedule, approval, operation, public response, professional acceptance, incident or recovery duration.
- 故障只停止并隔离验证叠层；普通生活、完整非 AI 路径、人工交接、撤回和申诉继续。恢复只先还普通使用，绝不等于授权、批准、重启或 G1。
- Reuse is limited to this submission package while rights remain blocked. Do not extract the media to advertise that AI or any pictured place already exists or operates in Haidian.

## 锁步规则 / Lockstep rule

Any later change to the video, poster, audio, either VTT track, transcript, visual embed, provenance, rights record or manifest entry must update all affected counterparts and rerun the complete final validation on the exact PR head.
