"""
gen_brand.py
============
Generate the Brand Visual System figures for the Jing-Zhang Intelligence Loop
submission package. Produces 12 files (6 figures × {zh, en} × {png, svg}).

Methodology (for the "originality" claim)
----------------------------------------
1. All visual content is original to this proposal — no third-party logos,
   images, portraits, or brand marks are referenced.
2. Logo mark = an elliptical orbit with four star nodes around the
   character "京", symbolising the centennial Jing-Zhang Railway arc and
   the ring-and-node relationship of AI innovation sites.
3. Palette is a five-colour system: Jing-Blue (京智蓝) / Loop-Green (智环绿)
   / Gold (金纽带) / Neutrals (雅白) / Ink (墨黑). Each colour carries a
   bilingual name in the brand figure.
4. Type stack is declared in two tiers: heading (PingFang SC / Microsoft
   YaHei / Noto Sans CJK SC system-font fallback) and body (Source Han
   Sans / LXGW WenKai, both OFL-licensed open-source fonts).
5. The "Global AI City References" panel lists six public-reference cities
   with their public sources printed at the bottom of the figure; this is
   for research reference, not a government commitment.
6. The "Three AI Pilgrimage Landmarks" panel proposes three conceptual
   landmark locations; these are explicitly footnoted as concept proposals
   that are not confirmed government construction arrangements.

Reproduction
------------
Run from the package root:

    /Users/jiang/.workbuddy/binaries/python/envs/default/bin/python \
        scripts/gen_brand.py

The script overwrites the existing 12 brand figure files in
``assets/figures/``. After running, recompute sha256 in ``manifest.json``
with ``scripts/hash_brand.py`` (or any equivalent tool).

Dependencies
------------
- matplotlib >= 3.5
- (No cairosvg / no weasyprint — uses matplotlib's native SVG export with
  ``svg.fonttype = 'path'`` so text becomes vector paths and no font
  embedding is required at render time.)
"""

from __future__ import annotations

import os
from pathlib import Path

import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Ellipse, FancyBboxPatch, Rectangle
from matplotlib.lines import Line2D

# ---------------------------------------------------------------------------
# Paths and font setup
# ---------------------------------------------------------------------------
PKG_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = PKG_ROOT / "assets" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Heiti TC is the system-bundled CJK font on macOS — the most reliable for
# producing clean, non-garbled Chinese in matplotlib output.
HEITI_TC = "/System/Library/Fonts/STHeiti Medium.ttc"
font_manager.fontManager.addfont(HEITI_TC)
plt.rcParams["font.sans-serif"] = ["Heiti TC", "Heiti SC", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["svg.fonttype"] = "path"  # text → vector paths, no font embeds
plt.rcParams["pdf.fonttype"] = 42     # TrueType, not Type-3, for PDF output

# Brand palette (5 colours, also documented in the brand-identity figure)
JING_BLUE = "#1f3a5f"   # 京智蓝
LOOP_GREEN = "#15803d"  # 智环绿
GOLD = "#c79838"        # 金纽带
NEUTRAL = "#eef2f6"     # 雅白
INK = "#162033"         # 墨黑
ACCENT_RED = "#b42318"  # used in ecosystem-map
ACCENT_BLUE = "#0f7490"  # used in ecosystem-map

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def save(fig, stem: str, lang: str) -> None:
    """Save a figure as both PNG and SVG, with optional .en suffix."""
    suffix = "" if lang == "zh" else ".en"
    png_path = FIG_DIR / f"{stem}.png" if lang == "zh" else FIG_DIR / f"{stem}.en.png"
    svg_path = FIG_DIR / f"{stem}.svg" if lang == "zh" else FIG_DIR / f"{stem}.en.svg"
    fig.savefig(png_path, dpi=200, bbox_inches="tight", facecolor="white")
    fig.savefig(svg_path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✓ {png_path.name} / {svg_path.name}")


def title_pair(zh: str, en: str, lang: str) -> str:
    return f"{zh} · {en}" if lang == "zh" else en


def footer(lang: str, text_zh: str, text_en: str) -> str:
    return text_zh if lang == "zh" else text_en


# ---------------------------------------------------------------------------
# 01 — Brand Identity System
# ---------------------------------------------------------------------------

def draw_brand_identity(lang: str) -> None:
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis("off")

    # Title
    ax.text(50, 56, title_pair("品牌视觉识别系统", "Brand Identity System", lang),
            ha="center", va="center", fontsize=20, color=INK, weight="bold")

    # Logo: ellipse + 4 star nodes + "京"
    cx, cy = 18, 32
    ax.add_patch(Ellipse((cx, cy), 16, 10, fill=False, edgecolor=GOLD, linewidth=2.2))
    ax.add_patch(Ellipse((cx, cy), 16, 10, fill=False, edgecolor=JING_BLUE, linewidth=1.2,
                         linestyle="--"))
    # 4 star nodes on the orbit
    for ang in (30, 150, 210, 330):
        import math
        rx, ry = 8 * math.cos(math.radians(ang)), 5 * math.sin(math.radians(ang))
        ax.plot(cx + rx, cy + ry, "o", color=JING_BLUE, markersize=8)
    ax.text(cx, cy + 1, "京", ha="center", va="center", fontsize=28, color=JING_BLUE, weight="bold")
    ax.text(cx, cy - 7, "京张智环" if lang == "zh" else "JING-ZHANG",
            ha="center", va="center", fontsize=13, color=INK, weight="bold")
    ax.text(cx, cy - 10, "百年铁路上的 AI 创新带" if lang == "zh" else "INTELLIGENCE LOOP",
            ha="center", va="center", fontsize=9, color="#475467")

    # Palette
    palette_x0 = 42
    ax.text(palette_x0 + 16, 47, title_pair("主色板", "Palette", lang),
            ha="center", va="center", fontsize=14, color=INK)
    swatches = [
        (JING_BLUE, "京智蓝", "Jing-Blue"),
        (LOOP_GREEN, "智环绿", "Loop-Green"),
        (GOLD, "金纽带", "Gold"),
        (NEUTRAL, "雅白", "Neutrals"),
        (INK, "墨黑", "Ink"),
    ]
    for i, (c, zh_l, en_l) in enumerate(swatches):
        x = palette_x0 + i * 8
        ax.add_patch(Rectangle((x, 38), 6, 5, facecolor=c, edgecolor="#cfd6e0", linewidth=0.6))
        label = f"{zh_l} {en_l}" if lang == "zh" else en_l
        ax.text(x + 3, 35.5, label, ha="center", va="center", fontsize=8.5, color=INK)

    # Typography
    ax.text(palette_x0 + 16, 30, title_pair("字体", "Typography", lang),
            ha="center", va="center", fontsize=14, color=INK)
    body_zh = "标题 PingFang SC / Microsoft YaHei / Noto Sans CJK SC\n正文 Source Han Sans / LXGW WenKai（开源）"
    body_en = "Headings PingFang SC / Microsoft YaHei / Noto Sans CJK SC\nBody Source Han Sans / LXGW WenKai (open-license)"
    ax.text(palette_x0, 24, body_zh if lang == "zh" else body_en,
            ha="left", va="top", fontsize=10, color=INK, linespacing=1.7)

    # Applications
    ax.text(palette_x0 + 16, 15, title_pair("应用规范", "Applications", lang),
            ha="center", va="center", fontsize=14, color=INK)
    apps = [("指示牌", "Signage", JING_BLUE),
            ("展板", "Exhibition", LOOP_GREEN),
            ("名片", "Card", "#ffffff"),
            ("APP", "App", GOLD)]
    for i, (zh_l, en_l, c) in enumerate(apps):
        x = palette_x0 + i * 8
        ax.add_patch(Rectangle((x, 7), 6, 5, facecolor=c,
                               edgecolor=("#1f3a5f" if c == "#ffffff" else "white"),
                               linewidth=1.0))
        label_color = "white" if c not in ("#ffffff",) else INK
        ax.text(x + 3, 9.5, zh_l if lang == "zh" else en_l,
                ha="center", va="center", fontsize=10.5, color=label_color)

    # Footer
    clearance_zh = "清权声明：Logo、字体与图形均为本方案原创或开源授权；不含任何企业或第三方未授权标识。"
    clearance_en = "Clearance: all marks are original or open-licensed; no un-cleared third-party brand."
    ax.text(50, 1.5, clearance_zh if lang == "zh" else clearance_en,
            ha="center", va="center", fontsize=9, color="#475467", style="italic")

    save(fig, "brand-identity", lang)


# ---------------------------------------------------------------------------
# 02 — AI Innovation Ecosystem
# ---------------------------------------------------------------------------

def draw_ecosystem_map(lang: str) -> None:
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis("off")

    ax.text(50, 55, title_pair("AI 创新生态图谱", "AI Innovation Ecosystem", lang),
            ha="center", va="center", fontsize=20, color=INK, weight="bold")

    # 5 stages in a horizontal chain
    stages = [
        ("高校策源", "University Sourcing", JING_BLUE, "清华/北航/中科院等" if lang == "zh" else "Tsinghua / Beihang / CAS"),
        ("开源协作", "Open-Source Collab.", LOOP_GREEN, "开源社区/代码墙" if lang == "zh" else "OSS / code wall"),
        ("企业转化", "Enterprise Translation", GOLD, "头部与初创企业" if lang == "zh" else "Leaders + startups"),
        ("公共体验", "Public Experience", ACCENT_BLUE, "遗址公园/慢行环" if lang == "zh" else "Heritage park / slow loop"),
        ("国际传播", "International Outreach", ACCENT_RED, "路演/活动周" if lang == "zh" else "Roadshow / week"),
    ]
    box_w, box_h = 14, 14
    y0 = 28
    spacing = 18
    for i, (zh_l, en_l, c, sub) in enumerate(stages):
        x = 8 + i * spacing
        ax.add_patch(FancyBboxPatch((x, y0), box_w, box_h,
                                    boxstyle="round,pad=0.5,rounding_size=0.6",
                                    facecolor=c, edgecolor="white", linewidth=1.2))
        ax.text(x + box_w / 2, y0 + box_h / 2 + 1, zh_l if lang == "zh" else en_l,
                ha="center", va="center", fontsize=12.5, color="white", weight="bold")
        ax.text(x + box_w / 2, y0 - 4, sub, ha="center", va="center",
                fontsize=9, color="#475467")
        # arrow
        if i < 4:
            arrow_x = x + box_w + 0.4
            ax.add_patch(mpatches.FancyArrow(arrow_x, y0 + box_h / 2,
                                             spacing - box_w - 0.8, 0,
                                             width=0.6, head_width=2.2,
                                             head_length=1.5,
                                             length_includes_head=True,
                                             color=INK))

    # Closed loop footer
    loop_zh = "闭环：人才→数据→算力→场景→反馈，由运营主体与年度活动体系驱动（详见第4项）"
    loop_en = "Closed loop: talent → data → compute → scenario → feedback, driven by operator and annual activity system (see Item 4)"
    ax.add_patch(Rectangle((6, 8), 88, 7, facecolor="#f6f8fb", edgecolor=LOOP_GREEN, linewidth=1.4))
    ax.text(50, 11.5, loop_zh if lang == "zh" else loop_en,
            ha="center", va="center", fontsize=10, color=INK)

    save(fig, "ecosystem-map", lang)


# ---------------------------------------------------------------------------
# 03 — Global AI City References
# ---------------------------------------------------------------------------

def draw_global_ai_cases(lang: str) -> None:
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis("off")

    ax.text(50, 56, title_pair("全球 AI 创新城市参照", "Global AI City References", lang),
            ha="center", va="center", fontsize=20, color=INK, weight="bold")
    ax.text(50, 51.5, footer(lang,
                              "均为公开资料参考，非政府承诺或实施安排；供专业团队深化研究。",
                              "Public references only — not government commitments; for further professional study."),
            ha="center", va="center", fontsize=9, color="#475467", style="italic")

    # Central node
    cx, cy = 50, 28
    ax.add_patch(Ellipse((cx, cy), 14, 8, facecolor=JING_BLUE, edgecolor="white", linewidth=2))
    ax.text(cx, cy, "京张智环" if lang == "zh" else "JZ-IL",
            ha="center", va="center", fontsize=12, color="white", weight="bold")

    # 6 surrounding nodes (radial)
    import math
    cities = [
        ("赫尔辛基 AI 注册表", "Helsinki AI Register",
         "公共 AI 用语登记与透明问责" if lang == "zh" else "transparent public-AI registry",
         ACCENT_BLUE),
        ("阿姆斯特丹 负责任 AI", "Amsterdam Responsible AI",
         "算法影响评估与市民可知" if lang == "zh" else "algorithmic impact assessment",
         ACCENT_BLUE),
        ("巴塞罗那 数字城市", "Barcelona Digital City",
         "开放城市平台与数据主权" if lang == "zh" else "open-source city platform",
         ACCENT_BLUE),
        ("首尔 数据开放城市", "Seoul Open Data City",
         "城市数据开放与市民共创" if lang == "zh" else "open urban data & co-creation",
         ACCENT_BLUE),
        ("蒙特利尔 AI 伦理宣言", "Montreal AI Ethics",
         "AI 伦理治理原则框架" if lang == "zh" else "AI ethics governance reference",
         ACCENT_BLUE),
        ("新加坡 Smart Nation", "Singapore Smart Nation",
         "国家级 AI 与数字政府协同" if lang == "zh" else "national AI & digital gov",
         ACCENT_BLUE),
    ]
    for i, (zh_l, en_l, sub, c) in enumerate(cities):
        ang = math.radians(60 + i * 60)
        rx = cx + 32 * math.cos(ang)
        ry = cy + 16 * math.sin(ang)
        ax.add_patch(Ellipse((rx, ry), 11, 4, fill=False, edgecolor=c, linewidth=1.6))
        ax.text(rx, ry + 0.8, zh_l if lang == "zh" else en_l,
                ha="center", va="center", fontsize=9, color=INK, weight="bold")
        ax.text(rx, ry - 1.4, sub, ha="center", va="center",
                fontsize=7.5, color="#475467")
        # connector
        ax.add_line(Line2D([cx, rx], [cy, ry], color=LOOP_GREEN, linewidth=1.2, alpha=0.8))

    ax.text(50, 2.5, "来源 Sources: hel.fi / city open data ; amsterdam.nl / Responsible AI Lab ; "
                     "data.seoul.go.kr ; montrealdeclaration-responsibleai.com ; "
                     "smartnation.gov.sg ; barcelona.cat / Decidim",
            ha="center", va="center", fontsize=8, color="#475467")

    save(fig, "global-ai-cases", lang)


# ---------------------------------------------------------------------------
# 04 — Three AI Pilgrimage Landmarks
# ---------------------------------------------------------------------------

def draw_ai_landmarks(lang: str) -> None:
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis("off")

    ax.text(50, 56, title_pair("三处 AI 朝圣地标", "Three AI Pilgrimage Landmarks", lang),
            ha="center", va="center", fontsize=20, color=INK, weight="bold")

    landmarks = [
        ("01", JING_BLUE,
         "开源发布厅", "Open-Source Release Hall",
         "北京AI原点社区", "Beijing AI Origin Community",
         "可预约路演台 · 公共代码墙 · 夜间协作舱",
         "bookable roadshow · public code wall · night collab"),
        ("02", LOOP_GREEN,
         "国际路演厅", "International Roadshow Hall",
         "大钟寺AI产业聚集区", "Dazhongsi AI Industry Cluster",
         "企业展示 · 洽谈 · 媒体发布 · 国际接待",
         "exhibition · talks · media · international reception"),
        ("03", ACCENT_RED,
         "全球AI活动周地标", "Global AI Activity Week Landmark",
         "一带公共空间系统", "One-belt public-space system",
         "可步行可传播体验路线与荣誉灯塔",
         "walkable + shareable route and honour beacon"),
    ]

    for i, (num, c, zh_t, en_t, zh_s, en_s, zh_d, en_d) in enumerate(landmarks):
        x = 12 + i * 30
        y = 32
        ax.add_patch(Ellipse((x, y), 7, 5, facecolor=c, edgecolor="white", linewidth=2))
        ax.text(x, y - 0.2, num, ha="center", va="center",
                fontsize=18, color="white", weight="bold")
        ax.text(x, y - 6, zh_t if lang == "zh" else en_t,
                ha="center", va="center", fontsize=11, color=INK, weight="bold")
        ax.text(x, y - 8.5, zh_s if lang == "zh" else en_s,
                ha="center", va="center", fontsize=9, color="#475467")
        # placeholder box
        ax.add_patch(Rectangle((x - 5, y - 16), 10, 4, facecolor=NEUTRAL, edgecolor=c, linewidth=1.2))
        ax.text(x, y - 14, "▽", ha="center", va="center", fontsize=10, color=c)
        ax.text(x, y - 19, zh_d if lang == "zh" else en_d,
                ha="center", va="center", fontsize=8.5, color="#475467")

    ax.text(50, 4, footer(lang,
                          "地标为概念提议/参考方案，待专业团队深化；非已确定政府建设安排。",
                          "Landmarks are conceptual proposals / reference schemes for professional deepening; not confirmed government construction arrangements."),
            ha="center", va="center", fontsize=9, color="#475467", style="italic")

    save(fig, "ai-landmarks", lang)


# ---------------------------------------------------------------------------
# 05 — Honor System + Component Library
# ---------------------------------------------------------------------------

def draw_honor_component_library(lang: str) -> None:
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis("off")

    ax.text(50, 56, title_pair("荣誉系统 + 公共空间组件库",
                                "Honor System + Public Space Component Library", lang),
            ha="center", va="center", fontsize=18, color=INK, weight="bold")

    # Honor wall (left)
    ax.text(22, 48, title_pair("贡献墙 / 荣誉系统", "Contribution Wall / Honor System", lang),
            ha="center", va="center", fontsize=12, color=JING_BLUE, weight="bold")
    for i in range(4):
        x = 8 + i * 8
        ax.add_patch(Rectangle((x, 36), 6, 8, facecolor="#fbf6e6", edgecolor=GOLD, linewidth=1.5))
        ax.text(x + 3, 40, "★", ha="center", va="center", fontsize=20, color=GOLD)
    ax.text(22, 32, footer(lang,
                            "开源贡献者 / 测试者 / 国际访客  可获数字徽章与实体铭牌（清权）",
                            "OSS contributors / testers / international visitors receive digital badges and physical plaques (clearance-cleared)"),
            ha="center", va="center", fontsize=9, color="#475467")

    # Component library (right)
    ax.text(72, 48, title_pair("组件库", "Component Library", lang),
            ha="center", va="center", fontsize=12, color=LOOP_GREEN, weight="bold")
    components = [
        ("座椅", "Bench"),
        ("导视", "Signage"),
        ("充电桩", "Charging Post"),
        ("算力亭", "Compute Kiosk"),
        ("慢行标", "Slow Marker"),
    ]
    for i, (zh_l, en_l) in enumerate(components):
        row, col = i // 3, i % 3
        x = 52 + col * 14
        y = 38 - row * 6
        ax.add_patch(Rectangle((x, y), 11, 4, facecolor=NEUTRAL, edgecolor=LOOP_GREEN, linewidth=1.2))
        ax.text(x + 5.5, y + 2, zh_l if lang == "zh" else en_l,
                ha="center", va="center", fontsize=10, color=INK)

    ax.text(72, 22, footer(lang,
                            "标准化 · 可复制 · 低侵入：纳入 A3 文册与 A0 展板",
                            "Standardised · replicable · low-intrusion: integrated into A3 booklet and A0 boards"),
            ha="center", va="center", fontsize=9, color="#475467", style="italic")

    save(fig, "honor-component-library", lang)


# ---------------------------------------------------------------------------
# 06 — Cultural Wayfinding + Annual Operations
# ---------------------------------------------------------------------------

def draw_wayfinding_ops(lang: str) -> None:
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis("off")

    ax.text(50, 56, title_pair("文化导视 + 长期运营图",
                                "Cultural Wayfinding + Annual Operations", lang),
            ha="center", va="center", fontsize=18, color=INK, weight="bold")

    # Wayfinding symbols (left)
    ax.text(25, 48, title_pair("文化导视符号", "Cultural Wayfinding Symbols", lang),
            ha="center", va="center", fontsize=12, color=JING_BLUE, weight="bold")
    symbols = [
        ("1", "枕木纹", "Tie Texture"),
        ("2", "AI节点", "AI Node"),
        ("3", "铁路弧", "Rail Arc"),
        ("4", "绿环", "Green Loop"),
    ]
    for i, (n, zh_l, en_l) in enumerate(symbols):
        x = 10 + i * 8
        ax.add_patch(Ellipse((x + 3, 42), 5, 3, facecolor="white", edgecolor=JING_BLUE, linewidth=1.4))
        ax.text(x + 3, 42.2, n, ha="center", va="center", fontsize=10, color=INK, weight="bold")
        ax.text(x + 3, 38, zh_l if lang == "zh" else en_l,
                ha="center", va="center", fontsize=9, color=INK)
    ax.text(25, 32, footer(lang,
                            "符号源自京张铁路与 AI 意象，统一应用于指示牌与 APP",
                            "Symbols derived from Jing-Zhang Railway and AI imagery; unified across signage and APP"),
            ha="center", va="center", fontsize=9, color="#475467")

    # Annual operations (right)
    ax.text(75, 48, title_pair("年度运营节奏", "Annual Operations Rhythm", lang),
            ha="center", va="center", fontsize=12, color=LOOP_GREEN, weight="bold")
    quarters = [
        ("Q1", "发布季", "Release Season"),
        ("Q2", "路演季", "Roadshow Season"),
        ("Q3", "测试季", "Test Season"),
        ("Q4", "活动周", "Activity Week"),
    ]
    for i, (q, zh_l, en_l) in enumerate(quarters):
        x = 53 + i * 12
        ax.add_patch(Rectangle((x, 38), 10, 8, facecolor=NEUTRAL, edgecolor=LOOP_GREEN, linewidth=1.2))
        ax.text(x + 5, 44, q, ha="center", va="center",
                fontsize=12, color=LOOP_GREEN, weight="bold")
        ax.text(x + 5, 41, zh_l if lang == "zh" else en_l,
                ha="center", va="center", fontsize=8.5, color=INK)
    ax.text(75, 32, footer(lang,
                            "运营主体 / 频率 / 责任边界 / 转化路径 详见第 4 项年度活动体系",
                            "Operator / frequency / accountability / conversion path — see Item 4 Annual Activity System"),
            ha="center", va="center", fontsize=9, color="#475467", style="italic")

    save(fig, "wayfinding-ops", lang)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print(f"Output directory: {FIG_DIR}")
    for lang in ("zh", "en"):
        print(f"-- {lang} --")
        draw_brand_identity(lang)
        draw_ecosystem_map(lang)
        draw_global_ai_cases(lang)
        draw_ai_landmarks(lang)
        draw_honor_component_library(lang)
        draw_wayfinding_ops(lang)
    print("Done. 12 files written.")


if __name__ == "__main__":
    main()
