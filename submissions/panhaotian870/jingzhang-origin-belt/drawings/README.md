# Drawings / 图纸

本目录需要包含以下 PDF 文件（硬性要求）：

- `a3-booklet.pdf` — A3 方案手册
- `a0-boards.pdf` — A0 展板

## 当前状态

⏳ **待生成** — 需要使用排版工具（如 InDesign、LaTeX、或 Python reportlab）将 proposal.md 内容排版为 A3/A0 格式 PDF。

## 生成建议

1. **A3 Booklet**: 将 proposal.md 渲染为多页 A3 横版 PDF，包含文字、图表、指标
2. **A0 Boards**: 将核心内容整理为 2-3 张 A0 竖版展板，包含空间结构图、场景卡、指标、案例对比

## 注意事项

- `finalize_submission.py` 会拒绝零页 PDF 和未修改的模板文件
- PDF 必须包含实际内容，不能是空白占位
- 建议使用 `report/proposal.html` 作为排版基础
