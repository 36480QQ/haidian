"""
Generate the 5 required figures for the submission.
Uses matplotlib for professional urban design diagram styling.
"""
import json
import os
import sys

# Try importing matplotlib
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle, FancyArrowPatch
    import numpy as np
except ImportError:
    print("Installing matplotlib...")
    os.system(f"{sys.executable} -m pip install matplotlib numpy -q")
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import Polygon, Rectangle, FancyArrowPatch
    import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
GEOM_DIR = os.path.join(BASE, "geometry")
FIG_DIR = os.path.join(BASE, "assets", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# Color scheme: Agriculture Green + Tech Blue
C_GREEN_DARK = '#1B5E20'
C_GREEN = '#2E7D32'
C_GREEN_LIGHT = '#66BB6A'
C_GREEN_PALE = '#C8E6C9'
C_BLUE_DARK = '#0D47A1'
C_BLUE = '#1565C0'
C_BLUE_LIGHT = '#42A5F5'
C_BLUE_PALE = '#BBDEFB'
C_ORANGE = '#E65100'
C_ORANGE_LIGHT = '#FFB74D'
C_GREY = '#757575'
C_GREY_LIGHT = '#E0E0E0'
C_BG = '#FAFAFA'
C_TEXT = '#212121'
C_WHITE = '#FFFFFF'

# Use Chinese font
import matplotlib.font_manager as fm
simhei_path = 'C:/Windows/Fonts/simhei.ttf'
fm.fontManager.addfont(simhei_path)
plt.rcParams.update({
    'font.family': 'SimHei',
    'font.size': 9,
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'figure.facecolor': C_BG,
    'axes.facecolor': C_BG,
    'text.color': C_TEXT,
    'axes.unicode_minus': False,
})

# Load GeoJSON data
def load_geojson(name):
    path = os.path.join(GEOM_DIR, name)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None

site = load_geojson("site_boundary.geojson")
key_areas = load_geojson("key_areas.geojson")
land_use = load_geojson("land_use.geojson")
buildings = load_geojson("buildings.geojson")
roads = load_geojson("roads.geojson")
green = load_geojson("green_space.geojson")
public = load_geojson("public_space.geojson")
phases = load_geojson("phasing.geojson")

# ============================================================
# FIGURE 1: site-overview.png
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 7), gridspec_kw={'width_ratios': [2, 1]})

# Left: Map overview
ax1 = axes[0]
ax1.set_title('百年京张 AI 创新带 — 京张智田 总体范围\nJing-Zhang Smart Farm · Site Overview', fontweight='bold', pad=12)

# Draw site boundary
if site:
    for feat in site["features"]:
        coords = feat["geometry"]["coordinates"][0]
        xs = [c[0] for c in coords]
        ys = [c[1] for c in coords]
        ax1.fill(xs, ys, alpha=0.08, color=C_BLUE, edgecolor=C_BLUE_DARK, linewidth=2, linestyle='--')
        # Label
        cx, cy = sum(xs)/len(xs), sum(ys)/len(ys)
        ax1.annotate('总体设计范围\n11.4 km²\n(provisional)', (cx, cy + 0.003), fontsize=7, color=C_BLUE_DARK, ha='center')

# Draw key areas
if key_areas:
    colors_k = [C_GREEN, C_BLUE, C_ORANGE]
    names_k = ['众智园\n智慧育种', 'AI原点社区\nFoodTech', '大钟寺\n未来食品']
    for i, feat in enumerate(key_areas["features"]):
        coords = feat["geometry"]["coordinates"][0]
        xs = [c[0] for c in coords]
        ys = [c[1] for c in coords]
        ax1.fill(xs, ys, alpha=0.2, color=colors_k[i], edgecolor=colors_k[i], linewidth=1.5)
        cx, cy = sum(xs)/len(xs), sum(ys)/len(ys)
        ax1.annotate(names_k[i], (cx, cy), fontsize=7, color=colors_k[i], ha='center', fontweight='bold')

# Draw green spaces
if green:
    for feat in green["features"]:
        coords = feat["geometry"]["coordinates"][0]
        xs = [c[0] for c in coords]
        ys = [c[1] for c in coords]
        ax1.fill(xs, ys, alpha=0.25, color=C_GREEN_LIGHT)

# Draw roads
if roads:
    for feat in roads["features"]:
        coords = feat["geometry"]["coordinates"]
        xs = [c[0] for c in coords]
        ys = [c[1] for c in coords]
        ax1.plot(xs, ys, color=C_GREY, linewidth=0.5, alpha=0.6)

# Draw railway line (conceptual)
ax1.plot([116.346, 116.346], [39.94, 40.026], color='#555', linewidth=2.5, linestyle='-', alpha=0.7)
ax1.annotate('京张铁路遗址公园\nJing-Zhang Railway Heritage Park', (116.347, 39.975), fontsize=7,
             color='#555', rotation=90, ha='center', va='center')

ax1.set_xlabel('Longitude (°E)')
ax1.set_ylabel('Latitude (°N)')
ax1.grid(True, alpha=0.3)

# Right: Concept diagram
ax2 = axes[1]
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis('off')
ax2.set_title('核心概念: 从"铁路运粮"到"AI种粮"\nFrom Grain Transport to AI Cultivation', fontweight='bold', pad=12, fontsize=10)

# Draw concept flow
y_positions = [8, 6, 4, 2]
labels = [
    '1909 京张铁路通车\n西北粮食进京主通道',
    '2026 AI创新带\n全球AI产业高地',
    '京张智田\nAI + 农业科技跨界融合',
    '2035 愿景\n全球AgTech创新策源地'
]
colors_flow = [C_GREY, C_BLUE, C_GREEN, C_ORANGE]
for i, (y, label, color) in enumerate(zip(y_positions, labels, colors_flow)):
    ax2.add_patch(FancyBboxPatch((1.5, y-0.6), 7, 1.2, boxstyle="round,pad=0.1",
                                  facecolor=color, alpha=0.15, edgecolor=color, linewidth=1.5))
    ax2.text(5, y, label, ha='center', va='center', fontsize=8, fontweight='bold', color=color)
    if i < 3:
        ax2.annotate('', xy=(5, y_positions[i+1]+0.6), xytext=(5, y-0.6),
                     arrowprops=dict(arrowstyle='->', color=C_GREY, lw=1.5))

# Legend
legend_elements = [
    mpatches.Patch(facecolor=C_GREEN, alpha=0.2, edgecolor=C_GREEN, label='AgTech R&D'),
    mpatches.Patch(facecolor=C_BLUE, alpha=0.2, edgecolor=C_BLUE, label='FoodTech Hub'),
    mpatches.Patch(facecolor=C_ORANGE, alpha=0.2, edgecolor=C_ORANGE, label='Food Experience'),
    mpatches.Patch(facecolor=C_GREEN_LIGHT, alpha=0.25, label='Green Space'),
]
ax1.legend(handles=legend_elements, loc='lower left', fontsize=7, framealpha=0.9)
ax1.text(0.02, 0.98, 'Source: Provisional boundary (DATA-SRC-PROVISIONAL-BOUNDARIES-20260605)\n'
         'Design: AI Agent concept proposal, not official redline',
         transform=ax1.transAxes, fontsize=6, color=C_GREY, va='top')

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "site-overview.png"), dpi=200, bbox_inches='tight')
plt.close()
print("Figure 1: site-overview.png generated")

# ============================================================
# FIGURE 2: land-use-structure.png
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Left: Land use plan
ax1 = axes[0]
ax1.set_title('用地布局与空间结构\nLand Use Structure', fontweight='bold')

lu_colors = {
    'AI_agritech_rd': '#1B5E20',
    'urban_farming_demo': '#66BB6A',
    'foodtech_commercial': '#1565C0',
    'talent_residential': '#FFB74D',
    'food_experience': '#E65100',
    'heritage_park': '#4CAF50',
    'tech_service': '#42A5F5',
    'scenario_mixed': '#90CAF9'
}
lu_labels = {
    'AI_agritech_rd': 'AgTech R&D',
    'urban_farming_demo': 'Urban Farm Demo',
    'foodtech_commercial': 'FoodTech Hub',
    'talent_residential': 'Talent Housing',
    'food_experience': 'Food Experience',
    'heritage_park': 'Heritage Park',
    'tech_service': 'Tech Service Wing',
    'scenario_mixed': 'Scenario Wing'
}

# Draw site boundary
if site:
    for feat in site["features"]:
        coords = feat["geometry"]["coordinates"][0]
        xs = [c[0] for c in coords]
        ys = [c[1] for c in coords]
        ax1.plot(xs + [xs[0]], ys + [ys[0]], color=C_GREY, linewidth=1.5, linestyle='--')

if land_use:
    for feat in land_use["features"]:
        coords = feat["geometry"]["coordinates"][0]
        xs = [c[0] for c in coords]
        ys = [c[1] for c in coords]
        cat = feat["properties"]["area_category"]
        color = lu_colors.get(cat, C_GREY)
        ax1.fill(xs, ys, alpha=0.3, color=color, edgecolor=color, linewidth=0.8)
        cx, cy = sum(xs)/len(xs), sum(ys)/len(ys)
        label = lu_labels.get(cat, cat)
        ax1.annotate(label, (cx, cy), fontsize=5.5, ha='center', va='center', fontweight='bold', color='#333')

ax1.set_xlabel('Longitude (°E)')
ax1.set_ylabel('Latitude (°N)')

# Right: Structure diagram
ax2 = axes[1]
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis('off')
ax2.set_title('三区两翼 空间结构\nThree Areas · Two Wings', fontweight='bold')

# Three areas
areas_info = [
    (5, 8, '众智园\nAI自主创新加速区\n智慧育种·农业AI研发', C_GREEN_DARK),
    (5, 5, '北京AI原点社区\nFoodTech孵化转化区\n食品科技·创新人才', C_BLUE_DARK),
    (5, 2, '大钟寺AI产业聚集区\n未来食品体验中心\n全球粮食安全论坛', C_ORANGE),
]
for x, y, label, color in areas_info:
    ax2.add_patch(FancyBboxPatch((x-3.5, y-1), 7, 2, boxstyle="round,pad=0.15",
                                  facecolor=color, alpha=0.15, edgecolor=color, linewidth=2))
    ax2.text(x, y, label, ha='center', va='center', fontsize=7.5, fontweight='bold', color=color)

# Wings
ax2.add_patch(FancyBboxPatch((0.5, 1.5), 2.5, 7, boxstyle="round,pad=0.1",
                              facecolor=C_BLUE_LIGHT, alpha=0.1, edgecolor=C_BLUE, linewidth=1, linestyle='--'))
ax2.text(1.75, 5, '中关村\n科技服务翼\nIP与资本\n赋能', ha='center', va='center', fontsize=7, color=C_BLUE, rotation=90)

ax2.add_patch(FancyBboxPatch((7, 1.5), 2.5, 7, boxstyle="round,pad=0.1",
                              facecolor=C_GREEN_LIGHT, alpha=0.1, edgecolor=C_GREEN, linewidth=1, linestyle='--'))
ax2.text(8.25, 5, '小月河\n场景赋能翼\nAI+场景\n测试展示', ha='center', va='center', fontsize=7, color=C_GREEN, rotation=90)

# Arrows
for y in [7, 4, 1]:
    ax2.annotate('', xy=(3.5, y), xytext=(6.5, y),
                arrowprops=dict(arrowstyle='<->', color=C_GREY, lw=1))

ax1.text(0.02, 0.98, 'Source: Provisional geometry; design layers are concept proposal\n'
         'Provisional boundary shown as dashed line', transform=ax1.transAxes, fontsize=6, color=C_GREY, va='top')

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "land-use-structure.png"), dpi=200, bbox_inches='tight')
plt.close()
print("Figure 2: land-use-structure.png generated")

# ============================================================
# FIGURE 3: key-areas.png
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))

key_info = [
    ('众智园: 智慧育种与农业AI研发验证区\nZhongzhiyuan: Smart Breeding & AgTech R&D',
     '192.1 ha', ['国家作物表型组学研究设施', 'AI驱动分子育种平台', '农业机器人测试场',
                  '数字孪生农田', '都市农业示范园', '国际农业AI峰会永久会址']),
    ('AI原点社区: FoodTech孵化转化区\nAI Origin: FoodTech Innovation Hub',
     '104.3 ha', ['食品AI加速器', '精准营养研发中心', '细胞培养蛋白中试基地',
                  'AI+食品安全检测中心', '创新人才社区', '开源食品数据共享平台']),
    ('大钟寺: 未来食品体验与全球粮食安全论坛\nDazhongsi: Future Food Forum',
     '72.0 ha', ['全球粮食安全论坛', '未来食品体验馆', 'AI+餐饮新零售实验区',
                  '国际食品科技展示交易中心', '农业文化遗产数字馆', '粮食安全大数据中心'])
]

for ax, (title, area, items) in zip(axes, key_info):
    ax.set_title(title, fontsize=8, fontweight='bold', pad=8)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Area box
    colors_seq = [C_GREEN_DARK, C_BLUE_DARK, C_ORANGE]
    idx = key_info.index((title, area, items))
    col = colors_seq[idx]

    ax.add_patch(FancyBboxPatch((0.5, 0.5), 9, 9, boxstyle="round,pad=0.2",
                                 facecolor=col, alpha=0.06, edgecolor=col, linewidth=1.5))
    ax.text(5, 9.3, f'面积 Area: {area}', ha='center', fontsize=8, fontweight='bold', color=col)

    # Function items
    for j, item in enumerate(items):
        y = 8 - j * 1.2
        ax.add_patch(FancyBboxPatch((1, y-0.4), 8, 0.8, boxstyle="round,pad=0.05",
                                     facecolor=col, alpha=0.1, edgecolor=col, linewidth=0.8))
        ax.text(5, y, f'{j+1}. {item}', ha='center', va='center', fontsize=7, color='#333')

    ax.text(0.5, 0.1, 'Provisional boundary. Concept design proposal.',
            fontsize=5.5, color=C_GREY, transform=ax.transAxes)

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "key-areas.png"), dpi=200, bbox_inches='tight')
plt.close()
print("Figure 3: key-areas.png generated")

# ============================================================
# FIGURE 4: mobility-bluegreen.png
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(14, 8))
ax.set_title('交通慢行与蓝绿公共空间复合系统\nMobility, Blue-Green & Public Space System', fontweight='bold', pad=12)

# Site boundary
if site:
    for feat in site["features"]:
        coords = feat["geometry"]["coordinates"][0]
        xs = [c[0] for c in coords]
        ys = [c[1] for c in coords]
        ax.plot(xs + [xs[0]], ys + [ys[0]], color=C_GREY, linewidth=1.5, linestyle='--', alpha=0.7)

# Green spaces
if green:
    for feat in green["features"]:
        coords = feat["geometry"]["coordinates"][0]
        xs = [c[0] for c in coords]
        ys = [c[1] for c in coords]
        ax.fill(xs, ys, alpha=0.35, color=C_GREEN_LIGHT, edgecolor=C_GREEN, linewidth=0.5)

# Public spaces
if public:
    for feat in public["features"]:
        coords = feat["geometry"]["coordinates"][0]
        xs = [c[0] for c in coords]
        ys = [c[1] for c in coords]
        ax.fill(xs, ys, alpha=0.5, color=C_ORANGE_LIGHT, edgecolor=C_ORANGE, linewidth=1)
        name = feat["properties"]["name_zh"]
        cx, cy = sum(xs)/len(xs), sum(ys)/len(ys)
        ax.annotate(name, (cx, cy), fontsize=5, ha='center', color=C_ORANGE, fontweight='bold')

# Roads
if roads:
    for feat in roads["features"]:
        coords = feat["geometry"]["coordinates"]
        xs = [c[0] for c in coords]
        ys = [c[1] for c in coords]
        rtype = feat["properties"]["road_type"]
        lw = 1.2 if rtype == 'primary' else 0.6
        color = '#555' if rtype == 'primary' else '#999'
        ax.plot(xs, ys, color=color, linewidth=lw, alpha=0.7)

# Railway line
ax.plot([116.346, 116.346], [39.94, 40.026], color='#333', linewidth=2.5, linestyle='-', alpha=0.8)

# Key area polygons
if key_areas:
    colors_k = [C_GREEN_DARK, C_BLUE_DARK, C_ORANGE]
    for feat, col in zip(key_areas["features"], colors_k):
        coords = feat["geometry"]["coordinates"][0]
        xs = [c[0] for c in coords]
        ys = [c[1] for c in coords]
        ax.plot(xs + [xs[0]], ys + [ys[0]], color=col, linewidth=2, alpha=0.5)

# Legend
legend_elements = [
    mpatches.Patch(facecolor=C_GREEN_LIGHT, alpha=0.35, edgecolor=C_GREEN, label='Blue-Green Space'),
    mpatches.Patch(facecolor=C_ORANGE_LIGHT, alpha=0.5, edgecolor=C_ORANGE, label='Public Space / AI Landmark'),
    mpatches.Patch(facecolor='none', edgecolor='#555', label='Primary Road'),
    mpatches.Patch(facecolor='none', edgecolor='#333', label='Jing-Zhang Railway (Heritage)'),
]
ax.legend(handles=legend_elements, loc='lower left', fontsize=7, framealpha=0.9)

# Labels for water bodies
ax.annotate('清 河\nQing River', (116.348, 40.024), fontsize=8, color=C_BLUE, ha='center', fontweight='bold')
ax.annotate('小月河\nXiaoyue River', (116.348, 39.99), fontsize=8, color=C_BLUE, ha='center', fontweight='bold')
ax.annotate('京张铁路遗址公园\n(线性绿廊)', (116.347, 39.96), fontsize=7, color=C_GREEN_DARK, ha='center',
            rotation=90, fontweight='bold')

ax.set_xlabel('Longitude (°E)')
ax.set_ylabel('Latitude (°N)')
ax.grid(True, alpha=0.2)

ax.text(0.02, 0.98, 'Concept design. Blue-green & public space network is provisional.',
        transform=ax.transAxes, fontsize=6, color=C_GREY, va='top')

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "mobility-bluegreen.png"), dpi=200, bbox_inches='tight')
plt.close()
print("Figure 4: mobility-bluegreen.png generated")

# ============================================================
# FIGURE 5: metrics-evidence.png
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('核心指标复算与证据链\nCore Metrics & Evidence Dashboard', fontweight='bold', fontsize=14, y=0.98)

# Top-left: Land use composition (pie)
ax = axes[0, 0]
labels = ['AgTech R&D\n(19.2%)', 'FoodTech\nCommercial\n(35.1%)', 'Talent\nResidential\n(10.9%)',
          'Green &\nPublic Space\n(24.5%)', 'Mixed &\nService\n(10.3%)']
sizes = [19.2, 35.1, 10.9, 24.5, 10.3]
colors_pie = [C_GREEN_DARK, C_BLUE, C_ORANGE, C_GREEN_LIGHT, C_BLUE_LIGHT]
wedges, texts = ax.pie(sizes, labels=labels, colors=colors_pie, startangle=90,
                        textprops={'fontsize': 7}, wedgeprops={'alpha': 0.85, 'edgecolor': 'white', 'linewidth': 1})
ax.set_title('Land Use Composition', fontweight='bold', fontsize=10)

# Top-right: Key metrics bars
ax = axes[0, 1]
metrics = ['Total Area\n(km²)', 'Green Ratio\n(%)', 'Public Space\n(%)', 'AI Service\nNodes', 'Scenario\nCards',
           'AI Landmarks']
values = [11.4, 28.5, 8.2, 15, 12, 5]
colors_bar = [C_BLUE, C_GREEN, C_GREEN_LIGHT, C_BLUE_LIGHT, C_ORANGE, C_ORANGE_LIGHT]
bars = ax.bar(range(len(metrics)), values, color=colors_bar, alpha=0.75, edgecolor='white')
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3, str(val),
            ha='center', fontsize=8, fontweight='bold')
ax.set_xticks(range(len(metrics)))
ax.set_xticklabels(metrics, fontsize=7)
ax.set_title('Key Design Metrics', fontweight='bold', fontsize=10)
ax.set_ylim(0, max(values) * 1.2)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Bottom-left: Phasing timeline
ax = axes[1, 0]
phases_info = [
    ('Near Term\n2026-2028', '大钟寺未来食品体验区\n先导项目', 30, C_ORANGE),
    ('Mid Term\n2028-2031', 'AI原点社区FoodTech\n孵化转化区', 50, C_BLUE),
    ('Long Term\n2031-2035', '众智园智慧育种\n研发区', 20, C_GREEN),
]
y_pos = [2.5, 1.5, 0.5]
for y, (label, desc, width, color) in zip(y_pos, phases_info):
    ax.barh(y, width, height=0.7, color=color, alpha=0.7, edgecolor='white')
    ax.text(width + 1, y, label, va='center', fontsize=7, fontweight='bold')
    ax.text(width + 8, y, desc, va='center', fontsize=6.5, color=color)

ax.set_xlim(0, 50)
ax.set_ylim(0, 3.2)
ax.set_title('Implementation Phasing', fontweight='bold', fontsize=10)
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Bottom-right: Evidence chain
ax = axes[1, 1]
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('Evidence Chain', fontweight='bold', fontsize=10)

evidence_chain = [
    (1, 8.5, 'Official\nAnnouncement', C_BLUE, 'A0'),
    (1, 6.5, 'Agent\nTaskbook', C_GREEN, 'Cleared'),
    (1, 4.5, 'Public\nStandards', C_BLUE, 'A0'),
    (1, 2.5, 'Provisional\nGeometry', C_ORANGE, 'Temp'),
]
for i, (x, y, label, color, auth) in enumerate(evidence_chain):
    ax.add_patch(FancyBboxPatch((x, y-0.6), 3, 1.2, boxstyle="round,pad=0.1",
                                 facecolor=color, alpha=0.1, edgecolor=color, linewidth=1.5))
    ax.text(x+1.5, y, f'{label}\n[{auth}]', ha='center', va='center', fontsize=7, fontweight='bold', color=color)
    if i < 3:
        ax.annotate('', xy=(x, evidence_chain[i+1][1]+0.6), xytext=(x, y-0.6),
                   arrowprops=dict(arrowstyle='->', color=C_GREY, lw=1.5))
    # Output
    if i == 0:
        ax.annotate('', xy=(x+3, y), xytext=(x+4.5, y),
                   arrowprops=dict(arrowstyle='->', color=C_GREEN, lw=2))
        ax.text(7, y, 'Proposal\n+ 9 GeoJSON\n+ 5 Figures\n+ Matrices\n+ A3/A0 PDF\n+ HTML Viz',
               fontsize=6.5, ha='center', va='center', fontweight='bold',
               bbox=dict(boxstyle='round', facecolor=C_GREEN_PALE, alpha=0.5))

ax.text(0.5, 0.3, 'Status: provisional, subject to professional review',
        fontsize=6, color=C_GREY)

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "metrics-evidence.png"), dpi=200, bbox_inches='tight')
plt.close()
print("Figure 5: metrics-evidence.png generated")

print("\nAll 5 figures generated successfully!")
for fname in sorted(os.listdir(FIG_DIR)):
    size = os.path.getsize(os.path.join(FIG_DIR, fname))
    print(f"  {fname} ({size:,} bytes)")
