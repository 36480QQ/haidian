# 版权与生成说明 / Rights and Generation Statement

- 方案文字、结构化矩阵、GeoJSON、确定性图件与PDF排版由 Codex（GPT-5 family）为本次开源征集生成；提交者为 `loyal6`。
- `assets/media/cover.webp` 为 OpenAI 图像生成工具输出的原创概念封面；提示词要求不使用商标、文字或水印。该图仅作概念表达，不是场地现状、官方设计或空间证据。
- 五组 `assets/figures/*.png` 为从提交 GeoJSON、指标和结构化矩阵确定性绘制的原创图件。
- 官方和第三方案例只作事实与方法研究，未复制其受版权保护的图像；URL、用途与转译限制见 `sources.json` 和 `visual/assets/global-cases.json`。
- Microsoft YaHei/Arial 仅在本地作为排版字体使用并以PDF子集嵌入，不作为独立字体文件再发布。
- `report/proposal.html` 与 `visual/index.html` 共同加载本包内的 `visual/assets/cjk-font.css`；该样式表将同一份 281,144-byte WOFF2 子集作为 data URI 内嵌，并以 `JZAC Noto Sans SC` 为网页字体名。子集由 Google Fonts 官方 Noto Sans SC 可变字体按两处中文入口实际使用的 857 个 CJK 字形生成。字体依 SIL Open Font License 1.1 允许嵌入与再分发，完整许可附于本文件下方；来源见 `sources.json#FONT-NOTO-SANS-SC`，fallback 为平台 CJK UI 字体后接通用 `sans-serif`。网页不依赖 CDN、远程字体或运行时网络请求。
- 本包采用 `COMMUNITY-DISPLAY-ONLY` 声明；仓库与组织方的最终许可条款优先。

All narrative, data layers, deterministic figures and layouts are original submission outputs. The AI-generated cover is disclosed and is not evidence. External cases are cited as research only; no third-party imagery is reproduced. The packaged Noto Sans SC webfont subset is redistributed under SIL OFL 1.1 with its complete licence and attribution.

## Embedded font licence / 内嵌字体许可

Copyright 2014-2021 Adobe (http://www.adobe.com/), with Reserved Font Name 'Source'

This Font Software is licensed under the SIL Open Font License, Version 1.1.
This license is copied below, and is also available with a FAQ at:
https://scripts.sil.org/OFL

-----------------------------------------------------------
SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007
-----------------------------------------------------------

PREAMBLE
The goals of the Open Font License (OFL) are to stimulate worldwide
development of collaborative font projects, to support the font creation
efforts of academic and linguistic communities, and to provide a free and
open framework in which fonts may be shared and improved in partnership
with others.

The OFL allows the licensed fonts to be used, studied, modified and
redistributed freely as long as they are not sold by themselves. The
fonts, including any derivative works, can be bundled, embedded,
redistributed and/or sold with any software provided that any reserved
names are not used by derivative works. The fonts and derivatives,
however, cannot be released under any other type of license. The
requirement for fonts to remain under this license does not apply
to any document created using the fonts or their derivatives.

DEFINITIONS
"Font Software" refers to the set of files released by the Copyright
Holder(s) under this license and clearly marked as such. This may
include source files, build scripts and documentation.

"Reserved Font Name" refers to any names specified as such after the
copyright statement(s).

"Original Version" refers to the collection of Font Software components as
distributed by the Copyright Holder(s).

"Modified Version" refers to any derivative made by adding to, deleting,
or substituting -- in part or in whole -- any of the components of the
Original Version, by changing formats or by porting the Font Software to a
new environment.

"Author" refers to any designer, engineer, programmer, technical
writer or other person who contributed to the Font Software.

PERMISSION & CONDITIONS
Permission is hereby granted, free of charge, to any person obtaining
a copy of the Font Software, to use, study, copy, merge, embed, modify,
redistribute, and sell modified and unmodified copies of the Font
Software, subject to the following conditions:

1) Neither the Font Software nor any of its individual components,
in Original or Modified Versions, may be sold by itself.

2) Original or Modified Versions of the Font Software may be bundled,
redistributed and/or sold with any software, provided that each copy
contains the above copyright notice and this license. These can be
included either as stand-alone text files, human-readable headers or
in the appropriate machine-readable metadata fields within text or
binary files as long as those fields can be easily viewed by the user.

3) No Modified Version of the Font Software may use the Reserved Font
Name(s) unless explicit written permission is granted by the corresponding
Copyright Holder. This restriction only applies to the primary font name as
presented to the users.

4) The name(s) of the Copyright Holder(s) or the Author(s) of the Font
Software shall not be used to promote, endorse or advertise any
Modified Version, except to acknowledge the contribution(s) of the
Copyright Holder(s) and the Author(s) or with their explicit written
permission.

5) The Font Software, modified or unmodified, in part or in whole,
must be distributed entirely under this license, and must not be
distributed under any other license. The requirement for fonts to
remain under this license does not apply to any document created using
the Font Software.

TERMINATION
This license becomes null and void if any of the above conditions are
not met.

DISCLAIMER
THE FONT SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
OF COPYRIGHT, PATENT, TRADEMARK, OR OTHER RIGHT. IN NO EVENT SHALL THE
COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
INCLUDING ANY GENERAL, SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL
DAMAGES, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF THE USE OR INABILITY TO USE THE FONT SOFTWARE OR FROM OTHER
DEALINGS IN THE FONT SOFTWARE.
