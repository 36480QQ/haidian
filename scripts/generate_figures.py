"""Generate the 5 required presentation-quality figures for Jing-Zhang Temporal Stitch submission."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import numpy as np
import os

# Output directory
OUT = 'submissions/blackboxo/jingzhang-temporal-stitch/assets/figures'
os.makedirs(OUT, exist_ok=True)

# Color palette
NAVY = '#1a1a2e'
TEAL = '#16697a'
GOLD = '#ffa62b'
CORAL = '#e94560'
WHITE = '#f8f8f8'
LIGHT_GRAY = '#e0e0e0'
DARK_GRAY = '#2d2d2d'
GREEN = '#2d6a4f'
BLUE = '#1d3557'

# Node data
NODES = [
    ("知识渗透针", 40.005, 116.348, "Knowledge Permeation"),
    ("潮汐交织针", 39.998, 116.349, "Tidal Weave"),
    ("创业孵化针", 39.991, 116.347, "Innovation Incubation"),
    ("代际编织针", 39.984, 116.348, "Intergenerational"),
    ("自然渗透针", 39.977, 116.349, "Natural Permeation"),
    ("商业缝合针", 39.970, 116.348, "Commercial Suture"),
    ("记忆锚固针", 39.963, 116.347, "Memory Anchor"),
    ("健康缝合针", 39.956, 116.349, "Health Suture"),
    ("数据缝合针", 39.949, 116.348, "Data Suture"),
]

plt.rcParams['font.family'] = ['Arial Unicode MS', 'Heiti TC', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False


def fig1_site_overview():
    """Site overview with corridor and 9 suture nodes."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 14), facecolor=NAVY)
    ax.set_facecolor(NAVY)

    # Site boundary (simplified)
    boundary_x = [116.3407, 116.3553, 116.3553, 116.3533, 116.3553, 116.3427, 116.3417, 116.3397, 116.3407]
    boundary_y = [39.939, 39.939, 39.965, 39.99, 40.0265, 40.0265, 40.006, 39.975, 39.939]
    ax.fill(boundary_x, boundary_y, alpha=0.15, color=TEAL, linewidth=0)
    ax.plot(boundary_x, boundary_y, color=TEAL, linewidth=1.5, linestyle='--', alpha=0.6)

    # Railway park corridor (central spine)
    corridor_y = np.linspace(39.94, 40.025, 50)
    corridor_x = 116.348 + 0.001 * np.sin(corridor_y * 100)
    ax.plot(corridor_x, corridor_y, color=GREEN, linewidth=8, alpha=0.3)
    ax.plot(corridor_x, corridor_y, color=GREEN, linewidth=2, alpha=0.8)

    # 9 Suture nodes
    for i, (name_zh, lat, lon, name_en) in enumerate(NODES):
        # Node circle
        ax.scatter(lon, lat, s=200, c=GOLD, zorder=5, edgecolors=WHITE, linewidth=1.5)
        # East-west connection lines
        ax.plot([lon - 0.006, lon + 0.006], [lat, lat], color=CORAL, linewidth=1.5, alpha=0.7)
        # Label
        ax.annotate(f'{i+1}. {name_zh}', (lon + 0.002, lat + 0.001),
                   color=WHITE, fontsize=8, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor=DARK_GRAY, alpha=0.7))

    # Key areas
    areas = [
        ("众智园AI加速区", 39.998, 40.018, 116.342, 116.355, TEAL),
        ("AI原点社区", 39.975, 39.995, 116.341, 116.354, BLUE),
        ("大钟寺AI产业区", 39.945, 39.965, 116.340, 116.354, '#4a1942'),
    ]
    for name, y1, y2, x1, x2, color in areas:
        rect = mpatches.FancyBboxPatch((x1, y1), x2-x1, y2-y1,
                                        boxstyle="round,pad=0.001",
                                        facecolor=color, alpha=0.2, edgecolor=color, linewidth=1.5)
        ax.add_patch(rect)
        ax.text((x1+x2)/2, y2-0.001, name, ha='center', va='top', color=WHITE, fontsize=9, alpha=0.8)

    # Title and legend
    ax.set_title('京张缝合·时间织补\n场地总览与缝合节点分布',
                color=WHITE, fontsize=16, fontweight='bold', pad=20)
    ax.text(0.02, 0.02, '数据来源：provisional_boundaries.geojson（临时粗略边界，待正式数据替换）\n'
            '坐标系：EPSG:4326 | 面积校核：EPSG:4548',
            transform=ax.transAxes, color=LIGHT_GRAY, fontsize=7, alpha=0.6)

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor=GREEN, alpha=0.5, label='京张遗址公园廊道'),
        plt.Line2D([0], [0], color=CORAL, linewidth=2, label='东西向缝合连接'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=GOLD, markersize=10, label='缝合节点'),
        mpatches.Patch(facecolor=TEAL, alpha=0.3, edgecolor=TEAL, linestyle='--', label='总体设计范围（临时）'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', facecolor=DARK_GRAY,
             edgecolor=TEAL, labelcolor=WHITE, fontsize=8)

    ax.set_xlim(116.335, 116.360)
    ax.set_ylim(39.935, 40.030)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.tight_layout()
    fig.savefig(f'{OUT}/site-overview.png', dpi=150, bbox_inches='tight', facecolor=NAVY)
    plt.close()
    print("Generated: site-overview.png")


def fig2_land_use_structure():
    """Land use structure diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 10), facecolor=WHITE)
    ax.set_facecolor('#f5f5f5')

    # Simplified land use zones as colored strips
    zones = [
        ("科研教育用地", 40.00, 40.025, '#457b9d', 'Research & Education'),
        ("产业创新用地", 39.985, 40.00, '#2a9d8f', 'Industry & Innovation'),
        ("混合功能用地", 39.965, 39.985, '#e9c46a', 'Mixed Use'),
        ("商业服务用地", 39.945, 39.965, '#f4a261', 'Commercial & Service'),
        ("居住生活用地", 39.935, 39.945, '#e76f51', 'Residential'),
    ]

    for name, y1, y2, color, en_name in zones:
        rect = mpatches.FancyBboxPatch((116.340, y1), 0.018, y2-y1,
                                        boxstyle="round,pad=0.0005",
                                        facecolor=color, alpha=0.4, edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(116.349, (y1+y2)/2, f'{name}\n{en_name}', ha='center', va='center',
               fontsize=10, fontweight='bold', color=DARK_GRAY)

    # Central green corridor
    ax.fill_between([116.3475, 116.3505], 39.935, 40.025, alpha=0.4, color=GREEN)
    ax.text(116.349, 40.027, '京张遗址公园绿廊', ha='center', fontsize=9, color=GREEN, fontweight='bold')

    # Suture nodes as connecting dots
    for i, (_, lat, lon, _) in enumerate(NODES):
        ax.scatter(lon, lat, s=80, c=GOLD, zorder=5, edgecolors=DARK_GRAY, linewidth=1)

    ax.set_title('用地结构与空间组织\nLand Use Structure & Spatial Organization',
                fontsize=14, fontweight='bold', color=DARK_GRAY, pad=15)
    ax.text(0.02, 0.02, '概念建议·供专业团队深化 | Provisional boundary',
            transform=ax.transAxes, fontsize=7, color='gray')

    ax.set_xlim(116.336, 116.362)
    ax.set_ylim(39.932, 40.032)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.tight_layout()
    fig.savefig(f'{OUT}/land-use-structure.png', dpi=150, bbox_inches='tight', facecolor=WHITE)
    plt.close()
    print("Generated: land-use-structure.png")


def fig3_key_areas():
    """Three key areas detail diagram."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 8), facecolor=WHITE)

    areas_data = [
        {
            'name': '众智园AI自主创新加速区',
            'en': 'Zhongzhiyuan AI Acceleration',
            'area': '192.1 ha',
            'color': TEAL,
            'nodes': ['知识渗透针', '潮汐交织针'],
            'features': ['清河界面设计', '产业展示空间', '低碳创新交往', '开放测试场'],
        },
        {
            'name': '北京AI原点社区',
            'en': 'Beijing AI Origin Community',
            'area': '104.3 ha',
            'color': BLUE,
            'nodes': ['创业孵化针', '代际编织针', '自然渗透针'],
            'features': ['校区园区缝合', '成果发布空间', '人才社区配套', '开源协作基地'],
        },
        {
            'name': '大钟寺AI产业集聚区',
            'en': 'Dazhongsi AI Industry Cluster',
            'area': '72.0 ha',
            'color': '#4a1942',
            'nodes': ['商业缝合针', '记忆锚固针'],
            'features': ['站点一体化', '四象限步行连通', '智能终端体验', '国际路演客厅'],
        },
    ]

    for ax, data in zip(axes, areas_data):
        ax.set_facecolor('#fafafa')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 12)
        ax.axis('off')

        # Header
        ax.add_patch(FancyBboxPatch((0.5, 10), 9, 1.5, boxstyle="round,pad=0.2",
                                     facecolor=data['color'], alpha=0.8))
        ax.text(5, 11, data['name'], ha='center', va='center', color=WHITE, fontsize=10, fontweight='bold')
        ax.text(5, 10.3, f"{data['en']} | {data['area']}", ha='center', va='center', color=LIGHT_GRAY, fontsize=7)

        # Suture nodes
        ax.text(1, 9.2, '缝合节点:', fontsize=8, fontweight='bold', color=DARK_GRAY)
        for j, node in enumerate(data['nodes']):
            ax.scatter(1.5 + j*2.5, 8.5, s=60, c=GOLD, zorder=5)
            ax.text(1.5 + j*2.5, 8.0, node, ha='center', fontsize=7, color=DARK_GRAY)

        # Design features
        ax.text(1, 7.0, '设计动作:', fontsize=8, fontweight='bold', color=DARK_GRAY)
        for j, feat in enumerate(data['features']):
            y = 6.2 - j * 1.2
            ax.add_patch(FancyBboxPatch((1, y-0.3), 8, 0.8, boxstyle="round,pad=0.1",
                                         facecolor=data['color'], alpha=0.1, edgecolor=data['color'], linewidth=0.5))
            ax.text(1.5, y, f"▸ {feat}", fontsize=8, color=DARK_GRAY)

    fig.suptitle('三处重点区域设计索引\nThree Key Areas Design Index',
                fontsize=14, fontweight='bold', color=DARK_GRAY, y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(f'{OUT}/key-areas.png', dpi=150, bbox_inches='tight', facecolor=WHITE)
    plt.close()
    print("Generated: key-areas.png")


def fig4_mobility_bluegreen():
    """Mobility and blue-green network diagram."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 10), facecolor=WHITE)

    # Left: Mobility network
    ax1.set_facecolor('#f5f5f5')
    ax1.set_title('慢行与交通缝合\nMobility & Stitching Network', fontsize=11, fontweight='bold', pad=10)

    # Railway corridor
    corridor_y = np.linspace(39.94, 40.025, 30)
    corridor_x = np.full_like(corridor_y, 116.348)
    ax1.plot(corridor_x, corridor_y, color=GREEN, linewidth=6, alpha=0.3)

    # Cross connections (east-west)
    for _, lat, lon, _ in NODES:
        ax1.annotate('', xy=(lon+0.007, lat), xytext=(lon-0.007, lat),
                    arrowprops=dict(arrowstyle='<->', color=CORAL, lw=1.5))
        ax1.scatter(lon, lat, s=60, c=GOLD, zorder=5)

    # Metro lines (simplified)
    ax1.plot([116.345, 116.345], [39.94, 40.025], color='#e63946', linewidth=2, linestyle='-', alpha=0.5, label='地铁线路')
    ax1.plot([116.352, 116.352], [39.94, 40.025], color='#457b9d', linewidth=2, linestyle='-', alpha=0.5, label='地铁线路2')

    # Major roads
    for y in [39.95, 39.97, 39.99, 40.01]:
        ax1.plot([116.338, 116.358], [y, y], color=DARK_GRAY, linewidth=0.8, alpha=0.3)

    ax1.set_xlim(116.336, 116.360)
    ax1.set_ylim(39.935, 40.030)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.text(0.02, 0.02, '东西缝合：9条跨廊道慢行连接', transform=ax1.transAxes, fontsize=8, color=DARK_GRAY)

    # Right: Blue-green network
    ax2.set_facecolor('#f5f5f5')
    ax2.set_title('蓝绿空间与生态网络\nBlue-Green & Ecological Network', fontsize=11, fontweight='bold', pad=10)

    # Green corridor (wider)
    corridor_x_left = 116.347 + 0.001 * np.sin(corridor_y * 80)
    corridor_x_right = 116.349 + 0.001 * np.sin(corridor_y * 80)
    ax2.fill_betweenx(corridor_y, corridor_x_left, corridor_x_right, alpha=0.4, color=GREEN)

    # Water features (Xiaohe River approximation)
    river_y = np.linspace(39.99, 40.02, 20)
    river_x = 116.344 + 0.002 * np.sin(river_y * 200)
    ax2.plot(river_x, river_y, color='#219ebc', linewidth=3, alpha=0.7)
    ax2.text(116.343, 40.015, '清河', fontsize=8, color='#219ebc')

    # Green buffer zones at nodes
    for _, lat, lon, _ in NODES:
        circle = Circle((lon, lat), 0.002, facecolor=GREEN, alpha=0.15, edgecolor=GREEN, linewidth=0.5)
        ax2.add_patch(circle)

    ax2.set_xlim(116.336, 116.360)
    ax2.set_ylim(39.935, 40.030)
    ax2.set_aspect('equal')
    ax2.axis('off')
    ax2.text(0.02, 0.02, '绿色空间比例目标：32% | 公共空间比例目标：18%',
            transform=ax2.transAxes, fontsize=8, color=DARK_GRAY)

    fig.tight_layout()
    fig.savefig(f'{OUT}/mobility-bluegreen.png', dpi=150, bbox_inches='tight', facecolor=WHITE)
    plt.close()
    print("Generated: mobility-bluegreen.png")


def fig5_metrics_evidence():
    """Metrics and evidence dashboard."""
    fig, axes = plt.subplots(2, 3, figsize=(14, 9), facecolor=WHITE)
    fig.suptitle('核心指标与证据总览\nCore Metrics & Evidence Dashboard',
                fontsize=14, fontweight='bold', color=DARK_GRAY, y=0.98)

    metrics = [
        ('场地面积', '11,412,825', 'sqm', '~11.4 km²', TEAL),
        ('绿地率', '32%', '', '目标值（概念设计）', GREEN),
        ('公共空间率', '18%', '', '目标值（概念设计）', BLUE),
        ('缝合节点', '9', '个', '东西向界面修复点', GOLD),
        ('时间节律方案', '27', '套', '9节点×3时钟', CORAL),
        ('实施分期', '3', '期', '10年渐进式策略', '#6a4c93'),
    ]

    for ax, (name, value, unit, note, color) in zip(axes.flatten(), metrics):
        ax.set_facecolor('#fafafa')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')

        # Metric card
        ax.add_patch(FancyBboxPatch((0.5, 0.5), 9, 9, boxstyle="round,pad=0.3",
                                     facecolor=WHITE, edgecolor=color, linewidth=2))
        ax.text(5, 7.5, name, ha='center', va='center', fontsize=11, color=DARK_GRAY, fontweight='bold')
        ax.text(5, 5, value, ha='center', va='center', fontsize=24, color=color, fontweight='bold')
        ax.text(5, 3.5, unit, ha='center', va='center', fontsize=9, color='gray')
        ax.text(5, 2, note, ha='center', va='center', fontsize=8, color='gray', style='italic')

    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(f'{OUT}/metrics-evidence.png', dpi=150, bbox_inches='tight', facecolor=WHITE)
    plt.close()
    print("Generated: metrics-evidence.png")


if __name__ == '__main__':
    fig1_site_overview()
    fig2_land_use_structure()
    fig3_key_areas()
    fig4_mobility_bluegreen()
    fig5_metrics_evidence()
    print("\nAll 5 figures generated successfully.")
