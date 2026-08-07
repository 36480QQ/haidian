"""Generate 5 presentation-quality PNG figures for 开源京张 AI 场景之都.

Style: technical-schematic / blueprint / dashboard.
Uses site_boundary coordinates from provisional_boundaries.geojson.
"""
import os, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, FancyArrowPatch
import numpy as np
from matplotlib.font_manager import FontProperties

# Register CJK font
cjk_font_path = r"C:\Windows\Fonts\msyh.ttc"
font_prop = FontProperties(fname=cjk_font_path) if os.path.exists(cjk_font_path) else None
if font_prop:
    plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

# Color palette (professional urban design)
C = {
    "steel": "#1a3a5c",
    "blue": "#2980b9",
    "green": "#27ae60",
    "red": "#c0392b",
    "orange": "#e67e22",
    "purple": "#8e44ad",
    "gray": "#7f8c8d",
    "light_blue": "#aed6f1",
    "light_green": "#abebc6",
    "light_red": "#f5b7b1",
    "light_orange": "#fdebd0",
    "light_purple": "#e8daef",
    "light_gray": "#f2f4f4",
    "white": "#ffffff",
    "bg": "#f8f9fa",
}

# Key area coordinates (provisional)
ZZY = {"x": 116.3485, "y": 40.0168, "w": 0.011, "h": 0.0185}  # 众智园
OCT = {"x": 116.3475, "y": 39.9885, "w": 0.011, "h": 0.010}  # AI原点
DZS = {"x": 116.3485, "y": 39.947, "w": 0.013, "h": 0.00584}  # 大钟寺

FIGDIR = "submissions/Microbiosis/kaiyuan-jingzhang-ai-city/assets/figures"
os.makedirs(FIGDIR, exist_ok=True)

def add_legend(ax, handles, labels, loc="lower left", fontsize=9):
    ax.legend(handles, labels, loc=loc, fontsize=fontsize, framealpha=0.9,
              edgecolor=C["steel"], fancybox=True)

# ============================================================
# Figure 1: Overview - 三带一心一廊
# ============================================================
def fig_overview():
    fig, ax = plt.subplots(1, 1, figsize=(14, 10), dpi=150)
    ax.set_xlim(116.340, 116.357)
    ax.set_ylim(39.940, 40.030)
    ax.set_aspect('equal')

    # Background grid
    for x in np.linspace(116.340, 116.357, 10):
        ax.axvline(x, color=C["light_gray"], linewidth=0.3)
    for y in np.linspace(39.940, 40.030, 10):
        ax.axhline(y, color=C["light_gray"], linewidth=0.3)

    # Site boundary (dashed - provisional)
    boundary_x = [116.3407, 116.3553, 116.3553, 116.3533, 116.3553, 116.3427, 116.3417, 116.3397, 116.3407]
    boundary_y = [39.939, 39.939, 39.965, 39.990, 40.0265, 40.0265, 40.006, 39.975, 39.939]
    ax.fill(boundary_x, boundary_y, alpha=0.03, color=C["gray"])
    ax.plot(boundary_x, boundary_y, color=C["gray"], linewidth=1.2, linestyle='--', label="总体设计范围 (provisional)")

    # Three corridors (bands)
    # Cultural band (red, left)
    cx1, cy1 = 116.3435, 40.010
    cx2, cy2 = 116.3435, 39.950
    ax.annotate("", xy=(cx1, cy1), xytext=(cx1, cy2),
                arrowprops=dict(arrowstyle="->", color=C["red"], lw=2.5, ls="--"))
    # Living band (green, center)
    ax.annotate("", xy=(ZZY["x"], ZZY["y"]+ZZY["h"]/2), xytext=(DZS["x"], DZS["y"]+DZS["h"]/2),
                arrowprops=dict(arrowstyle="->", color=C["green"], lw=3.0, connectionstyle="arc3,rad=0.05"))
    # Innovation band (blue, right)
    ax.annotate("", xy=(116.352, 40.010), xytext=(116.352, 39.950),
                arrowprops=dict(arrowstyle="->", color=C["blue"], lw=2.5, ls="--"))

    # Key areas (filled)
    def draw_area(ax, rect, color, label, alpha=0.35):
        r = FancyBboxPatch((rect["x"]-rect["w"]/2, rect["y"]-rect["h"]/2),
                           rect["w"], rect["h"],
                           boxstyle="round,pad=0.001",
                           facecolor=color, edgecolor=C["steel"],
                           linewidth=1.5, alpha=alpha)
        ax.add_patch(r)
        ax.text(rect["x"], rect["y"], label, ha="center", va="center",
                fontsize=10, fontweight="bold", color=C["steel"],
                fontproperties=font_prop)

    draw_area(ax, ZZY, C["light_red"], "众智园\n(192ha)", 0.4)
    draw_area(ax, OCT, C["light_green"], "AI原点\n(104ha)", 0.4)
    draw_area(ax, DZS, C["light_blue"], "大钟寺\n(72ha)", 0.4)

    # Corridor labels
    ax.text(116.342, 39.985, "百年京张\n文化带", fontsize=8, color=C["red"],
            ha="center", fontproperties=font_prop, rotation=90, fontweight="bold")
    ax.text(116.353, 39.985, "AI融合\n创新带", fontsize=8, color=C["blue"],
            ha="center", fontproperties=font_prop, rotation=90, fontweight="bold")
    ax.text(116.347, 39.963, "都市AI生活\n体验带", fontsize=7.5, color=C["green"],
            ha="center", fontproperties=font_prop, rotation=90, fontweight="bold")

    # North arrow
    ax.annotate("N", xy=(116.355, 40.028), xytext=(116.355, 40.023),
                fontsize=12, fontweight="bold", color=C["steel"],
                arrowprops=dict(arrowstyle="->", color=C["steel"], lw=2),
                ha="center", va="bottom")

    # Title
    ax.set_title("总体空间结构 · 三带一心一廊\nOverall Spatial Structure · Three Belts, One Core, One Corridor",
                 fontsize=13, fontweight="bold", color=C["steel"], pad=15,
                 fontproperties=font_prop)

    # Legend
    h1 = mpatches.Patch(color=C["light_red"], label="众智园 (AI自主创新)")
    h2 = mpatches.Patch(color=C["light_green"], label="AI原点社区 (创新生态)")
    h3 = mpatches.Patch(color=C["light_blue"], label="大钟寺 (产业集聚)")
    h4 = mlines.Line2D([], [], color=C["red"], ls="--", lw=2, label="文化带")
    h5 = mlines.Line2D([], [], color=C["green"], lw=3, label="生活带")
    h6 = mlines.Line2D([], [], color=C["blue"], ls="--", lw=2, label="创新带")
    add_legend(ax, [h1, h2, h3, h4, h5, h6],
               ["众智园", "AI原点", "大钟寺", "文化带", "生活带", "创新带"],
               loc="upper left", fontsize=9)

    # Note
    ax.text(116.342, 39.935, "注: 边界为 provisional，非 official redline | 概念性方案，不构成政府审定结论",
            fontsize=7, color=C["gray"], fontproperties=font_prop, style="italic")

    plt.tight_layout()
    out = os.path.join(FIGDIR, "overview.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=C["bg"])
    plt.close(fig)
    print(f"overview.png: {os.path.getsize(out)} bytes")
    return out

# ============================================================
# Figure 2: Key Areas - 三区两翼协同
# ============================================================
def fig_key_areas():
    fig, ax = plt.subplots(1, 1, figsize=(14, 9), dpi=150)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.set_aspect('equal')
    ax.axis('off')

    # Title
    ax.text(7, 8.5, "三处重点区域详细设计 · 三区两翼协同回路",
            fontsize=14, fontweight="bold", color=C["steel"], ha="center",
            fontproperties=font_prop)
    ax.text(7, 8.0, "Three Key Areas Detailed Design · Three-Area-Two-Wing Synergy",
            fontsize=10, color=C["gray"], ha="center")

    # Three boxes with details
    boxes = [
        (2.5, 5.0, 4, 2.2, C["light_red"], C["red"],
         "众智园 AI自主创新加速区",
         ["面积: 192.1 ha", "定位: AI全栈自主创新", "AI治理全球话语权",
          "基础模型 / AI芯片 / Agent框架", "SC-TEST-001, 002 (芯片/Agent测试)",
          "SC-APP-001, 004 (信软/法律)"]),
        (7.0, 5.0, 4, 2.2, C["light_green"], C["green"],
         "AI原点社区",
         ["面积: 104.3 ha", "定位: 世界级AI创新生态", "AI+场景赋能新范式",
          "高校-开发者-初创-社区混合", "SC-TEST-002 (Agent协作测试)",
          "SC-APP-002, 003, 005 (医疗/教育/生活)"]),
        (11.5, 5.0, 2.5, 2.2, C["light_blue"], C["blue"],
         "大钟寺\n产业集聚区",
         ["面积: 72.0 ha", "定位: 智能原生新业态",
          "AI产业总部 / 智能商业",
          "SC-TEST-003 (自动驾驶测试)",
          "SC-APP-006, 007 (交通/公共)"]),
    ]

    for (x, y, w, h, bg, border, title, lines) in boxes:
        r = FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.1",
                           facecolor=bg, edgecolor=border, linewidth=2, alpha=0.8)
        ax.add_patch(r)
        ax.text(x, y+h/2-0.3, title, ha="center", va="top", fontsize=10,
                fontweight="bold", color=C["steel"], fontproperties=font_prop)
        for i, line in enumerate(lines):
            ax.text(x, y+h/2-0.8-i*0.28, "  " + line, fontsize=7.5,
                    color=C["steel"], va="top", fontproperties=font_prop)

    # Two wings
    wings = [
        (2.5, 1.5, 3.5, 1.5, C["light_orange"], C["orange"],
         "中关村科技服务翼", "资本/IP/法律/技术服务业"),
        (11.5, 1.5, 2.5, 1.5, C["light_purple"], C["purple"],
         "小月河\n场景赋能翼", "蓝绿空间/场景测试\n公共体验路径"),
    ]
    for (x, y, w, h, bg, border, title, desc) in wings:
        r = FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.1",
                           facecolor=bg, edgecolor=border, linewidth=1.5, alpha=0.7)
        ax.add_patch(r)
        ax.text(x, y+0.2, title, ha="center", va="top", fontsize=9,
                fontweight="bold", color=C["steel"], fontproperties=font_prop)
        ax.text(x, y-0.15, desc, ha="center", va="top", fontsize=7,
                color=C["steel"], fontproperties=font_prop)

    # Synergy arrows
    arrows = [
        ((4.5, 5.0), (7.0, 5.0), C["green"], "技术→孵化"),
        ((9.0, 5.0), (11.5, 5.0), C["blue"], "孵化→转化"),
        ((2.5, 3.0), (7.0, 3.5), C["orange"], "服务支撑"),
        ((11.5, 3.0), (7.0, 3.5), C["purple"], "场景赋能"),
    ]
    for (start, end, color, label) in arrows:
        ax.annotate("", xy=end, xytext=start,
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.5))
        mx, my = (start[0]+end[0])/2, (start[1]+end[1])/2
        ax.text(mx, my+0.15, label, fontsize=6.5, color=color,
                ha="center", fontproperties=font_prop, fontweight="bold")

    # Bottom note
    ax.text(7, 0.3, "三区两翼协同: 众智园(全栈技术) → AI原点(生态孵化) → 大钟寺(产业转化) + 中关村翼(要素服务) + 小月河翼(场景赋能)",
            fontsize=7.5, color=C["gray"], ha="center", fontproperties=font_prop, style="italic")

    plt.tight_layout()
    out = os.path.join(FIGDIR, "key-areas.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=C["bg"])
    plt.close(fig)
    print(f"key-areas.png: {os.path.getsize(out)} bytes")
    return out

# ============================================================
# Figure 3: Land Use - 用地布局与空间结构
# ============================================================
def fig_land_use():
    fig, ax = plt.subplots(1, 1, figsize=(14, 10), dpi=150)
    ax.set_xlim(116.340, 116.357)
    ax.set_ylim(39.940, 40.030)
    ax.set_aspect('equal')

    # Site boundary
    boundary_x = [116.3407, 116.3553, 116.3553, 116.3533, 116.3553, 116.3427, 116.3417, 116.3397, 116.3407]
    boundary_y = [39.939, 39.939, 39.965, 39.990, 40.0265, 40.0265, 40.006, 39.975, 39.939]
    ax.plot(boundary_x, boundary_y, color=C["gray"], linewidth=1, linestyle='--', alpha=0.6)

    # Land use zones (conceptual, covering key areas and surroundings)
    zones = [
        # Research/Innovation (07)
        (116.343, 40.005, 0.015, 0.022, C["light_blue"], "07 科研/创新\n(20%)"),
        # Commercial (08)
        (116.343, 39.945, 0.015, 0.005, C["light_orange"], "08 商服/消费\n(25%)"),
        # Residential (01)
        (116.348, 39.980, 0.015, 0.006, C["light_green"], "01 居住/社区\n(20%)"),
        # Green (10)
        (116.343, 39.955, 0.012, 0.025, C["light_green"], "10 公园绿地\n(20%)"),
        # Industry/R&D (04)
        (116.350, 40.005, 0.010, 0.020, C["light_purple"], "04 工业/研发\n(10%)"),
    ]
    for (x, y, w, h, color, label) in zones:
        r = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.0005",
                           facecolor=color, edgecolor=C["steel"],
                           linewidth=0.8, alpha=0.5)
        ax.add_patch(r)
        ax.text(x+w/2, y+h/2, label, ha="center", va="center", fontsize=7,
                color=C["steel"], fontproperties=font_prop, fontweight="bold")

    # Key areas highlight
    def draw_area(ax, rect, color, label, alpha=0.5):
        r = FancyBboxPatch((rect["x"]-rect["w"]/2, rect["y"]-rect["h"]/2),
                           rect["w"], rect["h"],
                           boxstyle="round,pad=0.001",
                           facecolor="none", edgecolor=color,
                           linewidth=2.5, linestyle="-")
        ax.add_patch(r)
        ax.text(rect["x"], rect["y"]+rect["h"]/2+0.003, label, ha="center",
                fontsize=8, fontweight="bold", color=color, fontproperties=font_prop)

    draw_area(ax, ZZY, C["red"], "众智园", 0.5)
    draw_area(ax, OCT, C["green"], "AI原点", 0.5)
    draw_area(ax, DZS, C["blue"], "大钟寺", 0.5)

    # Title
    ax.set_title("用地布局与空间结构 · Land Use Layout",
                 fontsize=13, fontweight="bold", color=C["steel"], pad=15,
                 fontproperties=font_prop)

    # Legend
    legend_items = [
        mpatches.Patch(color=C["light_blue"], label="07 科研/创新 (20%)"),
        mpatches.Patch(color=C["light_orange"], label="08 商服/消费 (25%)"),
        mpatches.Patch(color=C["light_green"], label="01 居住/社区 (20%)"),
        mpatches.Patch(color=C["light_green"], label="10 公园绿地 (20%)"),
        mpatches.Patch(color=C["light_purple"], label="04 工业/研发 (10%)"),
    ]
    add_legend(ax, legend_items,
               ["07 科研", "08 商服", "01 居住", "10 绿地", "04 工业"],
               loc="upper left", fontsize=8)

    ax.text(116.342, 39.935, "注: 用地比例为概念性分配，基于临时 polygon 计算 [metric:land_use_ration]，待官方 polygon 发布后重算",
            fontsize=6.5, color=C["gray"], fontproperties=font_prop, style="italic")

    plt.tight_layout()
    out = os.path.join(FIGDIR, "land-use.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=C["bg"])
    plt.close(fig)
    print(f"land-use.png: {os.path.getsize(out)} bytes")
    return out

# ============================================================
# Figure 4: Mobility & Blue-Green - 交通慢行与蓝绿公共空间
# ============================================================
def fig_mobility():
    fig, ax = plt.subplots(1, 1, figsize=(14, 10), dpi=150)
    ax.set_xlim(116.340, 116.357)
    ax.set_ylim(39.940, 40.030)
    ax.set_aspect('equal')

    # Site boundary
    boundary_x = [116.3407, 116.3553, 116.3553, 116.3533, 116.3553, 116.3427, 116.3417, 116.3397, 116.3407]
    boundary_y = [39.939, 39.939, 39.965, 39.990, 40.0265, 40.0265, 40.006, 39.975, 39.939]
    ax.plot(boundary_x, boundary_y, color=C["gray"], linewidth=1, linestyle='--', alpha=0.4)

    # Blue-green corridors (water)
    # Qinghe / Xiaoyuehe river (horizontal)
    ax.fill_between([116.340, 116.355], [39.978, 39.978], [39.982, 39.982],
                    color=C["blue"], alpha=0.25, label="清河/小月河 蓝线")

    # Jingzhang park green corridor (vertical)
    park_x = [116.342, 116.345, 116.344, 116.343, 116.344, 116.345, 116.348, 116.349, 116.348, 116.347, 116.342]
    park_y = [39.944, 39.955, 39.975, 39.995, 40.015, 40.026, 40.026, 40.015, 39.995, 39.975, 39.944]
    ax.fill(park_x, park_y, color=C["green"], alpha=0.2, label="京张遗址公园 绿轴")

    # Rail lines
    ax.plot([116.346, 116.352], [39.946, 39.946], color=C["red"], linewidth=2, label="13号线/昌平线 (轨道)")
    ax.plot([116.348, 116.353], [39.988, 39.988], color=C["red"], linewidth=2)

    # Slow road network
    ax.plot([116.343, 116.353], [39.955, 39.955], color=C["green"], linewidth=1.5,
            linestyle=':', label="慢行廊道 (步行+骑行)")
    ax.plot([116.343, 116.353], [39.995, 39.995], color=C["green"], linewidth=1.5, linestyle=':')
    ax.plot([116.343, 116.353], [40.015, 40.015], color=C["green"], linewidth=1.5, linestyle=':')

    # AI scenario nodes
    nodes = [
        (116.3485, 40.0168, "SC-TEST-001\n芯片测试", C["red"]),
        (116.3485, 40.008, "SC-APP-001\n模型评测", C["blue"]),
        (116.3475, 39.9885, "SC-APP-002\n社区健康", C["green"]),
        (116.3475, 39.984, "SC-APP-003\n自适应学习", C["orange"]),
        (116.3475, 39.992, "SC-TEST-002\nAgent协作", C["purple"]),
        (116.3485, 39.947, "SC-TEST-003\n自动驾驶", C["red"]),
        (116.3485, 39.950, "SC-APP-006\n智能公交", C["blue"]),
        (116.350, 39.947, "SC-APP-007\n数字孪生", C["green"]),
    ]
    for (x, y, label, color) in nodes:
        ax.plot(x, y, 'o', color=color, markersize=8, markeredgecolor=C["steel"], markeredgewidth=1)
        ax.text(x+0.001, y+0.001, label, fontsize=5.5, color=C["steel"],
                fontproperties=font_prop, va="bottom")

    # Landmarks (stars)
    landmarks = [
        (116.345, 40.024, "京张智脉碑", C["red"]),
        (116.3475, 39.985, "AI原点灯塔", C["orange"]),
        (116.350, 39.948, "开源之环", C["blue"]),
    ]
    for (x, y, label, color) in landmarks:
        ax.plot(x, y, '*', color=color, markersize=15, markeredgecolor=C["steel"], markeredgewidth=1)
        ax.text(x, y+0.002, label, fontsize=6, color=color, ha="center",
                fontweight="bold", fontproperties=font_prop)

    # Title
    ax.set_title("交通慢行与蓝绿公共空间复合系统\nMobility · Slow Road · Blue-Green Public Space",
                 fontsize=13, fontweight="bold", color=C["steel"], pad=15,
                 fontproperties=font_prop)

    # Legend
    legend_items = [
        mlines.Line2D([], [], color=C["green"], lw=2, label="京张遗址公园 绿轴"),
        mlines.Line2D([], [], color=C["blue"], lw=2, label="清河/小月河 蓝线"),
        mlines.Line2D([], [], color=C["red"], lw=2, label="轨道 (13/昌平线)"),
        mlines.Line2D([], [], color=C["green"], lw=1.5, ls=':', label="慢行廊道"),
        mlines.Line2D([], [], color=C["steel"], lw=0, marker='o', markersize=8, label="AI场景节点"),
        mlines.Line2D([], [], color=C["red"], lw=0, marker='*', markersize=12, label="AI朝圣地标"),
    ]
    add_legend(ax, legend_items,
               ["京张绿轴", "蓝线水域", "轨道", "慢行", "场景节点", "朝圣地标"],
               loc="upper left", fontsize=8)

    ax.text(116.342, 39.935,
            "京张遗址公园活力带 (~10km南北) + 清河/小月河 (东西) 形成十字蓝绿骨架 [metric:slow_road_length]",
            fontsize=6.5, color=C["gray"], fontproperties=font_prop, style="italic")

    plt.tight_layout()
    out = os.path.join(FIGDIR, "mobility.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=C["bg"])
    plt.close(fig)
    print(f"mobility.png: {os.path.getsize(out)} bytes")
    return out

# ============================================================
# Figure 5: AI Ecosystem & Scenarios - 生态图谱与场景卡
# ============================================================
def fig_ecosystem():
    fig, ax = plt.subplots(1, 1, figsize=(14, 11), dpi=150)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 11)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.text(7, 10.5, "AI 创新生态图谱与场景卡矩阵\nAI Ecosystem Map & Scenario Card Matrix",
            fontsize=14, fontweight="bold", color=C["steel"], ha="center",
            fontproperties=font_prop)
    ax.text(7, 10.0, "五层生态: 基础层 → 平台层 → 应用层 → 空间层 → 运营层",
            fontsize=10, color=C["gray"], ha="center", fontproperties=font_prop)

    # Five-layer stack (horizontal bars)
    layers = [
        (5.5, 8.7, 9, 0.7, C["light_blue"], C["blue"],
         "⑤ 运营层", "年度活动体系 · 开发者社区 · 场景开放 · 国际传播"),
        (5.5, 7.8, 9, 0.7, C["light_green"], C["green"],
         "④ 空间层", "三处重点区 · 京张遗址公园 · 慢行廊道 · 蓝绿空间"),
        (5.5, 6.9, 9, 0.7, C["light_orange"], C["orange"],
         "③ 应用层", "10+ AI场景卡 (信软/医疗/教育/法律/生活/交通/公共)"),
        (5.5, 6.0, 9, 0.7, C["light_purple"], C["purple"],
         "② 平台层", "AI场景操作系统 · MCP/Agent框架 · 场景测试沙箱"),
        (5.5, 5.1, 9, 0.7, C["light_gray"], C["gray"],
         "① 基础层", "算力(端侧+云侧) · 数据(公共+场景) · 模型(基础+垂直)"),
    ]
    for (x, y, w, h, bg, border, title, desc) in layers:
        r = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                           facecolor=bg, edgecolor=border, linewidth=1.5)
        ax.add_patch(r)
        ax.text(x+0.3, y+h/2, title, fontsize=10, fontweight="bold",
                color=border, va="center", fontproperties=font_prop)
        ax.text(x+2.5, y+h/2, desc, fontsize=8, color=C["steel"],
                va="center", fontproperties=font_prop)

    # Scenario cards grid (bottom)
    ax.text(0.5, 4.2, "AI 场景卡矩阵 (10张 · 含3张产业测试验证)", fontsize=11,
            fontweight="bold", color=C["steel"], fontproperties=font_prop)

    scenarios = [
        ("SC-TEST-001", "AI芯片\n端侧推理", "众智园", C["red"]),
        ("SC-TEST-002", "AI Agent\n多智能体", "AI原点", C["purple"]),
        ("SC-TEST-003", "AI+驾驶\n城市测试", "大钟寺", C["red"]),
        ("SC-APP-001", "AI+信软\n模型评测", "众智园", C["blue"]),
        ("SC-APP-002", "AI+医疗\n社区健康", "AI原点", C["green"]),
        ("SC-APP-003", "AI+教育\n自适应学", "AI原点", C["orange"]),
        ("SC-APP-004", "AI+法律\n合规审查", "众智园", C["blue"]),
        ("SC-APP-005", "AI+生活\n社区智能", "AI原点", C["orange"]),
        ("SC-APP-006", "AI+交通\n智能公交", "大钟寺", C["blue"]),
        ("SC-APP-007", "AI+公共\n数字孪生", "全线", C["green"]),
    ]

    for i, (code, name, loc, color) in enumerate(scenarios):
        col = i % 5
        row = i // 5
        x = 0.5 + col * 2.7
        y = 2.5 - row * 1.5
        r = FancyBboxPatch((x, y), 2.4, 1.2, boxstyle="round,pad=0.08",
                           facecolor="white", edgecolor=color, linewidth=1.5)
        ax.add_patch(r)
        ax.text(x+0.15, y+0.95, code, fontsize=7, fontweight="bold",
                color=color, fontproperties=font_prop)
        ax.text(x+1.2, y+0.55, name, fontsize=7.5, color=C["steel"],
                ha="center", va="center", fontproperties=font_prop)
        ax.text(x+1.2, y+0.15, "[" + loc + "]", fontsize=6.5,
                color=C["gray"], ha="center", fontproperties=font_prop)

    # 5 personas
    ax.text(0.5, 0.7, "五类用户画像: ", fontsize=9, fontweight="bold",
            color=C["steel"], fontproperties=font_prop)
    personas = ["🔬 研究者(22-28)", "⚙️ 工程师(28-35)", "🚀 创业者(25-40)",
                "💻 开发者(20-35)", "🏠 居民(25-60)"]
    for i, p in enumerate(personas):
        ax.text(0.5 + i * 2.7, 0.35, p, fontsize=7, color=C["steel"],
                fontproperties=font_prop)

    # Legend: test vs app
    h1 = mpatches.Patch(color="white", edgecolor=C["red"], label="产业测试验证场景 (3张)")
    h2 = mpatches.Patch(color="white", edgecolor=C["blue"], label="AI+ 应用场景 (7张)")
    add_legend(ax, [h1, h2], ["产业测试", "AI+ 应用"], loc="upper right", fontsize=9)

    plt.tight_layout()
    out = os.path.join(FIGDIR, "ecosystem.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=C["bg"])
    plt.close(fig)
    print(f"ecosystem.png: {os.path.getsize(out)} bytes")
    return out

# ============================================================
# Figure 6: Metrics dashboard
# ============================================================
def fig_metrics():
    fig, ax = plt.subplots(1, 1, figsize=(14, 9), dpi=150)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.text(7, 8.5, "核心指标复算与证据链\nCore Metrics & Evidence Chain Dashboard",
            fontsize=14, fontweight="bold", color=C["steel"], ha="center",
            fontproperties=font_prop)

    # Metric cards
    metrics = [
        ("总体设计面积", "1,140", "ha", "site_area_sqm", C["blue"]),
        ("重点区面积", "368.4", "ha", "key_area_count", C["red"]),
        ("众智园", "192.1", "ha", "KA-ZZY", C["red"]),
        ("AI原点", "104.3", "ha", "KA-OCT", C["green"]),
        ("大钟寺", "72.0", "ha", "KA-DZS", C["blue"]),
        ("绿地比例", "~20", "%", "green_ratio", C["green"]),
        ("公共空间", "~15", "%", "public_space_ratio", C["green"]),
        ("AI场景卡", "10", "张", "ai_scenario_count", C["orange"]),
        ("朝圣地标", "3", "个", "landmarks", C["purple"]),
        ("用户画像", "5", "类", "personas", C["steel"]),
        ("全球案例", "7", "个", "case_studies", C["steel"]),
        ("年度活动", "5", "类", "events", C["steel"]),
    ]

    for i, (name, val, unit, metric_id, color) in enumerate(metrics):
        col = i % 4
        row = i // 4
        x = 1.0 + col * 3.2
        y = 6.5 - row * 1.8
        r = FancyBboxPatch((x, y), 2.8, 1.5, boxstyle="round,pad=0.1",
                           facecolor=color, edgecolor=C["steel"],
                           linewidth=1.5, alpha=0.15)
        ax.add_patch(r)
        ax.text(x+1.4, y+1.15, name, fontsize=8, fontweight="bold",
                color=C["steel"], ha="center", fontproperties=font_prop)
        ax.text(x+1.4, y+0.55, val + " " + unit, fontsize=16, fontweight="bold",
                color=color, ha="center")
        ax.text(x+1.4, y+0.15, "[" + metric_id + "]", fontsize=6.5,
                color=C["gray"], ha="center")

    # Compliance coverage bar
    ax.text(1.0, 1.2, "合规覆盖进度", fontsize=11, fontweight="bold",
            color=C["steel"], fontproperties=font_prop)

    categories = [
        ("compliance_matrix", 1.0, C["green"]),
        ("standard_matrix", 1.0, C["green"]),
        ("design_depth_matrix", 1.0, C["green"]),
        ("agent.1-6", 1.0, C["green"]),
        ("GeoJSON layers", 1.0, C["green"]),
        ("Figures (5)", 1.0, C["green"]),
    ]
    for i, (name, ratio, color) in enumerate(categories):
        y = 0.6 - i * 0.15
        bar = FancyBboxPatch((1.5, y), 10*ratio, 0.1, boxstyle="round,pad=0.02",
                             facecolor=color, edgecolor="none", alpha=0.7)
        ax.add_patch(bar)
        bg = FancyBboxPatch((1.5, y), 10, 0.1, boxstyle="round,pad=0.02",
                            facecolor=C["light_gray"], edgecolor="none")
        ax.add_patch(bg)
        ax.text(1.1, y+0.05, name, fontsize=7, color=C["steel"],
                va="center", fontproperties=font_prop, ha="right")
        ax.text(1.5+10*ratio+0.2, y+0.05, f"{int(ratio*100)}%",
                fontsize=7, color=color, va="center")

    plt.tight_layout()
    out = os.path.join(FIGDIR, "metrics.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=C["bg"])
    plt.close(fig)
    print(f"metrics.png: {os.path.getsize(out)} bytes")
    return out

# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    fig_overview()
    fig_key_areas()
    fig_land_use()
    fig_mobility()
    fig_ecosystem()
    fig_metrics()
    print("All figures generated.")