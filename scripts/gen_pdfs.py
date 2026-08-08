#!/usr/bin/env python3
"""
京张智脉 — A3 文册 + A0 展板 PDF 生成 v2
v2 修复：matplotlib Type3 中文字体在多数阅读器乱码 → 全部页面栅格化为
高分辨率 PNG（A3@200dpi / A0@130dpi）再合成 PDF。PDF 内为纯位图，
任何阅读器渲染结果与 PNG 完全一致，杜绝乱码。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import io, os

SUB = "submissions/xusu-ai/jingzhang-ai-vein"
FIG = f"{SUB}/assets/figures"
DRAW = f"{SUB}/drawings"
os.makedirs(DRAW, exist_ok=True)

BG = "#0E1420"
FG = "#E8EDF5"
ACCENT = "#2E5BFF"
COPPER = "#B8860B"

plt.rcParams.update({
    "figure.facecolor": BG, "savefig.facecolor": BG,
    "text.color": FG, "font.family": "WenQuanYi Zen Hei",
})
import matplotlib.font_manager as fm
for fp in ["/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"]:
    if os.path.exists(fp):
        fm.fontManager.addfont(fp)
plt.rcParams["font.family"] = "WenQuanYi Zen Hei"

FIGS = {
    "site-overview.png": "01 总体设计范围用地总览",
    "land-use-structure.png": "02 用地结构分区（拓扑闭合）",
    "key-areas.png": "03 三处重点区域详细设计索引",
    "mobility-bluegreen.png": "04 交通慢行与蓝绿公共空间复合系统",
    "metrics-evidence.png": "05 核心指标复算证据链",
}


def fig_to_png(fig, dpi):
    """渲染 figure 为 RGB PIL Image（立即加载像素）"""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, facecolor=BG)
    buf.seek(0)
    img = Image.open(buf).convert("RGB")
    img.load()  # 确保像素立即读入内存
    return img


def save_pdf(images, path, resolution):
    images[0].save(path, "PDF", resolution=resolution,
                   save_all=True, append_images=images[1:])
    print(f"✅ {os.path.basename(path)}: {len(images)} 页, {os.path.getsize(path)//1024}KB")


# ============ A3 文册（420×297mm，7 页） ============
a3_w, a3_h = 420/25.4, 297/25.4
A3_DPI = 200
a3_pages = []

# 封面
fig = plt.figure(figsize=(a3_w, a3_h))
fig.patch.set_facecolor(BG)
fig.text(0.5, 0.62, "京张智脉 Jingzhang AI Vein", ha="center", fontsize=40,
         fontweight="bold", color=FG)
fig.text(0.5, 0.54, "百年京张AI创新带城市设计 · A3 方案文册", ha="center", fontsize=22, color="#B8C2D4")
fig.text(0.5, 0.46, "submissions/xusu-ai/jingzhang-ai-vein", ha="center", fontsize=14, color="#8A94A6")
fig.text(0.5, 0.40, "边界状态: provisional_constraint（非官方红线）· 官方 polygon 发布后需重算",
         ha="center", fontsize=12, color=ACCENT)
fig.text(0.5, 0.30, "一带三核 · 多点场景 · 蓝绿慢行复合环", ha="center", fontsize=16, color=COPPER)
fig.text(0.5, 0.10, "AI agent 生成 · 概念建议 · 不构成法定规划结论 · 2026-08-07",
         ha="center", fontsize=11, color="#667085")
a3_pages.append(fig_to_png(fig, A3_DPI)); plt.close(fig)

# 内容页：每页一张图 + 标题
for fname, caption in FIGS.items():
    fig = plt.figure(figsize=(a3_w, a3_h))
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0.06, 0.12, 0.88, 0.76])
    ax.set_facecolor(BG); ax.axis("off")
    ax.imshow(plt.imread(f"{FIG}/{fname}"))
    fig.text(0.5, 0.94, caption, ha="center", fontsize=18, fontweight="bold", color=FG)
    fig.text(0.5, 0.04, "来源: 本方案 GeoJSON/metrics/矩阵派生 · 边界为 provisional_constraint",
             ha="center", fontsize=10, color="#667085")
    a3_pages.append(fig_to_png(fig, A3_DPI)); plt.close(fig)

# 结页：方案要点
fig = plt.figure(figsize=(a3_w, a3_h))
fig.patch.set_facecolor(BG)
fig.text(0.5, 0.85, "方案要点总结", ha="center", fontsize=24, fontweight="bold", color=FG)
points = [
    "— 命名: 京张智脉 Jingzhang AI Vein — 京张铁路百年文脉 × AI 时代智脉",
    "— 结构: 一带(京张遗址公园)三核(众智园/原点社区/大钟寺)两翼(中关村/小月河)",
    "— 用地: 9 个拓扑闭合分区, 11.41 km², 绿地率 25%, 无缝隙无重叠",
    "— 场景: 10 张 AI 场景卡(含 3 张产业测试验证) + 5 类用户画像",
    "— 地标: 智脉原点碑 / 智脉未来馆 / 智脉市集台 (概念建议)",
    "— 运营: 年度京张智脉 AI 周 + 季度开放日 + 月度开发者之夜",
    "— 边界: provisional_constraint, 官方 polygon 发布后全部重算",
]
for i, p in enumerate(points):
    fig.text(0.08, 0.68 - i * 0.07, p, fontsize=14, color=FG)
a3_pages.append(fig_to_png(fig, A3_DPI)); plt.close(fig)

save_pdf(a3_pages, f"{DRAW}/a3-booklet.pdf", resolution=A3_DPI)
print(f"  A3 页面尺寸: {a3_pages[0].size[0]}x{a3_pages[0].size[1]}px")

# ============ A0 展板（1189×841mm 横版，1 页） ============
a0_w, a0_h = 1189/25.4, 841/25.4
A0_DPI = 130
fig = plt.figure(figsize=(a0_w, a0_h))
fig.patch.set_facecolor(BG)

fig.text(0.5, 0.95, "京张智脉 Jingzhang AI Vein — 百年京张AI创新带城市设计 A0 展板",
         ha="center", fontsize=44, fontweight="bold", color=FG)
fig.text(0.5, 0.905, "一带三核 · 多点场景 · 蓝绿慢行复合环 | provisional boundary | 11.41 km² | 绿地率 25%",
         ha="center", fontsize=18, color=COPPER)

layout = [
    ("site-overview.png", [0.03, 0.52, 0.44, 0.36], "总体用地总览"),
    ("land-use-structure.png", [0.50, 0.52, 0.47, 0.36], "用地结构分区"),
    ("key-areas.png", [0.03, 0.12, 0.44, 0.36], "三处重点区详细设计"),
    ("mobility-bluegreen.png", [0.50, 0.12, 0.27, 0.36], "交通与蓝绿系统"),
    ("metrics-evidence.png", [0.79, 0.12, 0.18, 0.36], "指标证据链"),
]
for fname, box, label in layout:
    ax = fig.add_axes(box)
    ax.set_facecolor(BG); ax.axis("off")
    ax.imshow(plt.imread(f"{FIG}/{fname}"))
    ax.set_title(label, fontsize=16, color=FG, fontweight="bold", pad=6)

fig.text(0.5, 0.03, "AI agent 生成 · 概念建议 · 不构成法定规划/审批结论 · 官方 polygon 发布后指标需重算 · 2026-08-07",
         ha="center", fontsize=13, color="#667085")
a0_img = fig_to_png(fig, A0_DPI)
plt.close(fig)
save_pdf([a0_img], f"{DRAW}/a0-boards.pdf", resolution=A0_DPI)
print(f"  A0 页面尺寸: {a0_img.size[0]}x{a0_img.size[1]}px")
print("\n全部 PDF 完成（栅格化，无 Type3 字体）")
