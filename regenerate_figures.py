#!/usr/bin/env python3
"""Regenerate all 5 proposal figures with authoritative metrics from metrics.json.
Uses NotoSansSC-VF.ttf for proper Chinese rendering.
"""
import json
import math
from PIL import Image, ImageDraw, ImageFont

METRICS_FILE = "submissions/ID-VerNe/ai-innovation-belt/metrics.json"
FIGS_DIR = "submissions/ID-VerNe/ai-innovation-belt/assets/figures"
FONT_PATH = "C:/Windows/Fonts/NotoSansSC-VF.ttf"
FONT_BOLD = "C:/Windows/Fonts/msyhbd.ttc"

# Load metrics
with open(METRICS_FILE, encoding="utf-8") as f:
    m = json.load(f)["metrics"]

SITE_AREA = m["site_area_sqm"]["value"]
SITE_AREA_HA = SITE_AREA / 10000
BLDG_FOOTPRINT = m["building_footprint_area_sqm"]["value"]
GREEN_RATIO = m["green_ratio"]["value"]
PUBLIC_SPACE_RATIO = m["public_space_ratio"]["value"]
GREEN_AREA = GREEN_RATIO * SITE_AREA
PUBLIC_SPACE_AREA = PUBLIC_SPACE_RATIO * SITE_AREA
KEY_AREA_COUNT = m["key_area_count"]["value"]

W, H = 1200, 800


def get_font(size, bold=False):
    path = FONT_BOLD if bold else FONT_PATH
    return ImageFont.truetype(path, size)


def get_font_variable(size, weight=400):
    """Load a font at a specific weight."""
    return ImageFont.truetype(FONT_PATH, size)


def rounded_rect(draw, xy, r, fill=None, outline=None, width=1):
    x1, y1, x2, y2 = xy
    draw.pieslice([x1, y1, x1 + 2 * r, y1 + 2 * r], 180, 270, fill=fill, outline=outline, width=width)
    draw.pieslice([x2 - 2 * r, y1, x2, y1 + 2 * r], 270, 360, fill=fill, outline=outline, width=width)
    draw.pieslice([x1, y2 - 2 * r, x1 + 2 * r, y2], 90, 180, fill=fill, outline=outline, width=width)
    draw.pieslice([x2 - 2 * r, y2 - 2 * r, x2, y2], 0, 90, fill=fill, outline=outline, width=width)
    draw.rectangle([x1 + r, y1, x2 - r, y2], fill=fill, outline=outline, width=width)
    draw.rectangle([x1, y1 + r, x2, y2 - r], fill=fill, outline=outline, width=width)


def draw_card(draw, x, y, w, h, title, value, subtitle, color, title_size=18, value_size=32, sub_size=13):
    """Draw a metric card."""
    rounded_rect(draw, [x, y, x + w, y + h], 8, fill=(255, 255, 255), outline=color, width=2)
    # Color bar at top
    draw.rectangle([x + 2, y + 2, x + w - 2, y + 6], fill=color)
    # Title
    draw.text((x + 12, y + 14), title, fill=(100, 116, 139), font=get_font(title_size))
    # Value
    draw.text((x + 12, y + 40), value, fill=(15, 23, 42), font=get_font(value_size, bold=True))
    # Subtitle
    draw.text((x + 12, y + h - 24), subtitle, fill=(148, 163, 184), font=get_font(sub_size))


# ============================================================
# Figure 1: Site Overview (区位分析图)
# ============================================================
def gen_site_overview():
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, W, 60], fill=(15, 23, 42))
    draw.text((30, 16), "百年京张AI创新带 — 区位分析图", fill=(255, 255, 255), font=get_font(22, bold=True))
    draw.text((W - 30, 20), "Centennial Jing-Zhang AI Innovation Belt", fill=(148, 163, 184), font=get_font(13), anchor="rt")

    # Left panel: Site context
    cx, cy = 250, 380
    # Draw a rough site outline
    outline = [(cx - 120, cy - 180), (cx, cy - 200), (cx + 100, cy - 120), (cx + 140, cy),
               (cx + 100, cy + 100), (cx, cy + 180), (cx - 100, cy + 160), (cx - 150, cy + 60)]
    draw.polygon(outline, fill=(219, 234, 254), outline=(59, 130, 246), width=3)

    # Inside text
    draw.text((cx, cy - 20), "京张AI创新带", fill=(29, 78, 216), font=get_font(20, bold=True), anchor="mm")
    draw.text((cx, cy + 20), f"{SITE_AREA_HA:.2f} ha", fill=(59, 130, 246), font=get_font(16), anchor="mm")

    # Key areas
    for i, (label, dx, dy) in enumerate([
        ("众智园", -80, -140),
        ("AI原点社区", 40, -100),
        ("大钟寺", 80, 80)
    ]):
        px, py = cx + dx, cy + dy
        draw.ellipse([px - 10, py - 10, px + 10, py + 10], fill=(239, 68, 68))
        draw.text((px, py - 22), label, fill=(185, 28, 28), font=get_font(14, bold=True), anchor="mm")

    # Compass
    sx, sy = 50, 660
    draw.text((sx, sy), "N", fill=(71, 85, 105), font=get_font(16, bold=True))
    draw.polygon([(sx, sy - 12), (sx - 6, sy + 2), (sx + 6, sy + 2)], fill=(71, 85, 105))

    # Scale bar
    scale_x, scale_y = 120, 660
    for i in range(5):
        x = scale_x + i * 30
        draw.rectangle([x, scale_y, x + 15, scale_y + 4], fill=(71, 85, 105) if i % 2 == 0 else (255, 255, 255), outline=(71, 85, 105), width=1)
    draw.text((scale_x, scale_y + 10), "0  1  2 km", fill=(71, 85, 105), font=get_font(11))

    # Right panel: Metrics cards
    card_x = 480
    card_y = 90
    card_w = 200
    card_h = 100
    gap = 16

    metrics = [
        ("设计范围", f"{SITE_AREA_HA:.1f} ha", "总体规划设计范围", (59, 130, 246)),
        ("重点区域", f"{KEY_AREA_COUNT} 处", "三处重点详细设计片区", (239, 68, 68)),
        ("建筑基底", f"{BLDG_FOOTPRINT / 10000:.1f} ha", "建筑基底总面积", (245, 158, 11)),
        ("绿地率", f"{GREEN_RATIO * 100:.2f}%", "绿地空间占比", (34, 197, 94)),
        ("公共空间率", f"{PUBLIC_SPACE_RATIO * 100:.2f}%", "公共空间占比", (168, 85, 247)),
    ]
    for i, (t, v, s, c) in enumerate(metrics):
        row = i // 2
        col = i % 2
        x = card_x + col * (card_w + gap)
        y = card_y + row * (card_h + gap)
        draw_card(draw, x, y, card_w, card_h, t, v, s, c)

    # Right bottom: design scope
    bx, by = 480, 420
    draw.text((bx, by), "三层工作范围", fill=(15, 23, 42), font=get_font(18, bold=True))
    for i, (label, desc, area_text) in enumerate([
        ("统筹研究范围", "AI产业生态与战略定位", "43.6 km²"),
        ("总体设计范围", "城市更新与控规深度", "11.4 km²"),
        ("重点区域范围", "三处详细设计地区", "368.4 ha"),
    ]):
        y = by + 40 + i * 60
        # Color dot
        colors = [(59, 130, 246), (245, 158, 11), (239, 68, 68)]
        draw.ellipse([bx, y + 4, bx + 14, y + 18], fill=colors[i])
        draw.text((bx + 24, y), label, fill=(15, 23, 42), font=get_font(16, bold=True))
        draw.text((bx + 24, y + 22), desc, fill=(100, 116, 139), font=get_font(13))
        draw.text((bx + 280, y + 4), area_text, fill=(71, 85, 105), font=get_font(15, bold=True))

    # Footer
    draw.text((30, H - 30), "基线数据来源：2026年中关村论坛年会发布 | 边界为临时示意，非官方红线",
              fill=(148, 163, 184), font=get_font(11))
    draw.text((W - 30, H - 30), "Provisional boundary · Not official redline",
              fill=(148, 163, 184), font=get_font(11), anchor="rt")

    img.save(f"{FIGS_DIR}/site-overview.png", "PNG")
    print("site-overview.png saved")


# ============================================================
# Figure 2: Land Use Structure (用地结构图)
# ============================================================
def gen_land_use():
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, W, 60], fill=(15, 23, 42))
    draw.text((30, 16), "百年京张AI创新带 — 用地功能结构图", fill=(255, 255, 255), font=get_font(22, bold=True))

    # Main panel: Land use diagram
    cx, cy = 300, 400
    # Draw a stylized land use map
    # Industrial
    draw.polygon([(cx - 140, cy - 180), (cx - 40, cy - 190), (cx - 20, cy - 80), (cx - 120, cy - 70)],
                 fill=(254, 226, 226), outline=(239, 68, 68), width=2)
    draw.text((cx - 80, cy - 130), "产业用地", fill=(185, 28, 28), font=get_font(14, bold=True), anchor="mm")

    # Mixed use
    draw.polygon([(cx - 20, cy - 190), (cx + 80, cy - 180), (cx + 100, cy - 70), (cx, cy - 80)],
                 fill=(254, 243, 199), outline=(245, 158, 11), width=2)
    draw.text((cx + 40, cy - 130), "混合功能", fill=(180, 83, 9), font=get_font(14, bold=True), anchor="mm")

    # Green space
    draw.ellipse([cx - 80, cy - 60, cx + 40, cy + 60], fill=(220, 252, 231), outline=(34, 197, 94), width=2)
    draw.text((cx - 20, cy), "绿地/公园", fill=(22, 101, 52), font=get_font(14, bold=True), anchor="mm")

    # Public space
    draw.polygon([(cx + 60, cy - 60), (cx + 150, cy - 40), (cx + 130, cy + 50), (cx + 40, cy + 30)],
                 fill=(237, 233, 254), outline=(168, 85, 247), width=2)
    draw.text((cx + 95, cy - 5), "公共空间", fill=(107, 33, 168), font=get_font(14, bold=True), anchor="mm")

    # Water
    draw.polygon([(cx - 150, cy - 50), (cx - 80, cy - 60), (cx - 100, cy + 80), (cx - 170, cy + 100)],
                 fill=(219, 234, 254), outline=(59, 130, 246), width=2)
    draw.text((cx - 125, cy + 20), "水体", fill=(29, 78, 216), font=get_font(14, bold=True), anchor="mm")

    # Transport
    draw.polygon([(cx - 130, cy + 80), (cx + 120, cy + 70), (cx + 140, cy + 130), (cx - 110, cy + 140)],
                 fill=(226, 232, 240), outline=(100, 116, 139), width=2)
    draw.text((cx, cy + 106), "交通设施", fill=(71, 85, 105), font=get_font(14, bold=True), anchor="mm")

    # Legend
    lx, ly = 50, 700
    legend_items = [
        ("产业用地", (239, 68, 68)), ("混合功能", (245, 158, 11)), ("绿地/公园", (34, 197, 94)),
        ("公共空间", (168, 85, 247)), ("水体", (59, 130, 246)), ("交通设施", (100, 116, 139))
    ]
    for i, (label, color) in enumerate(legend_items):
        x = lx + i * 180
        draw.rectangle([x, ly, x + 16, ly + 16], fill=color)
        draw.text((x + 22, ly), label, fill=(71, 85, 105), font=get_font(14))

    # Right panel: Land use table
    rx, ry = 540, 90
    draw.text((rx, ry), "用地功能配比", fill=(15, 23, 42), font=get_font(18, bold=True))

    # Table
    table_data = [
        ("用地类型", "面积 (ha)", "占比"),
        ("产业用地", "~320", "~28%"),
        ("混合功能", "~240", "~21%"),
        ("绿地/公园", "~80", "~7.0%"),
        ("公共空间", "~17", "~1.5%"),
        ("交通设施", "~200", "~18%"),
        ("其他", "~284", "~24.5%"),
        ("合计", f"{SITE_AREA_HA:.1f}", "100%"),
    ]

    col_widths = [140, 100, 80]
    for i, row in enumerate(table_data):
        y = ry + 40 + i * 30
        for j, cell in enumerate(row):
            x = rx + sum(col_widths[:j])
            is_header = i == 0
            is_total = i == len(table_data) - 1
            color = (71, 85, 105) if is_header else (15, 23, 42) if is_total else (100, 116, 139)
            f = get_font(14, bold=True) if is_header or is_total else get_font(14)
            draw.text((x, y), cell, fill=color, font=f)
        if i == 0:
            draw.line([(rx, y + 22), (rx + sum(col_widths), y + 22)], fill=(203, 213, 225), width=1)

    # Key metrics
    draw.text((rx, ry + 330), "核心指标", fill=(15, 23, 42), font=get_font(18, bold=True))
    metrics_info = [
        (f"绿地率: {GREEN_RATIO * 100:.2f}%", (34, 197, 94)),
        (f"公共空间率: {PUBLIC_SPACE_RATIO * 100:.2f}%", (168, 85, 247)),
        (f"建筑基底面积: {BLDG_FOOTPRINT / 10000:.1f} ha", (245, 158, 11)),
    ]
    for i, (text, color) in enumerate(metrics_info):
        y = ry + 360 + i * 28
        draw.rectangle([rx, y, rx + 8, y + 8], fill=color)
        draw.text((rx + 16, y - 2), text, fill=(71, 85, 105), font=get_font(14))

    # Footer
    draw.text((30, H - 30), "用地分类依据国土空间调查、规划、用途管制分类标准 | 数据为概念方案估算，非正式控规结论",
              fill=(148, 163, 184), font=get_font(11))

    img.save(f"{FIGS_DIR}/land-use-structure.png", "PNG")
    print("land-use-structure.png saved")


# ============================================================
# Figure 3: Key Areas (重点区域图)
# ============================================================
def gen_key_areas():
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, W, 60], fill=(15, 23, 42))
    draw.text((30, 16), "百年京张AI创新带 — 三处重点区域详细设计", fill=(255, 255, 255), font=get_font(22, bold=True))

    # Three key area panels
    areas = [
        {
            "name": "众智园·AI自主创新加速区",
            "name_en": "Zhongzhiyuan · AI Innovation Accelerator",
            "color": (59, 130, 246),
            "bg": (239, 246, 255),
            "content": [
                "花园型全栈自主创新街区",
                "国家AI平台与标准制定",
                "安全治理沙盒、模型红队测试",
                "清河低碳创新界面",
                "产业展示与对外交通",
                "绿色空间承载开放测试",
            ],
            "tag": "北部 · 学北园"
        },
        {
            "name": "北京AI原点社区",
            "name_en": "Beijing AI Origin Community",
            "color": (239, 68, 68),
            "bg": (255, 241, 242),
            "content": [
                "近校型成果转化与人才社区",
                "3 km² · 439家企业 · 日均7000人",
                "开源评测走廊、成果发布厅",
                "校区-园区-街区慢行缝合",
                "人才特区服务与居住配套",
                "2025全球十大创新区",
            ],
            "tag": "中部 · 五道口"
        },
        {
            "name": "大钟寺·AI产业聚集区",
            "name_en": "Dazhongsi · AI Industry Cluster",
            "color": (245, 158, 11),
            "bg": (255, 247, 237),
            "content": [
                "城市型智能经济与国际交往街区",
                "领军企业、智能体、智能终端",
                "智能体实景测试场",
                "大钟寺站一体化开发",
                "四象限步行连通",
                "数据要素会客厅",
            ],
            "tag": "南部 · 大钟寺"
        },
    ]

    panel_w = 360
    panel_h = 520
    gap = 30
    start_x = (W - 3 * panel_w - 2 * gap) // 2

    for i, area in enumerate(areas):
        x = start_x + i * (panel_w + gap)
        y = 90

        # Panel background
        rounded_rect(draw, [x, y, x + panel_w, y + panel_h], 12, fill=area["bg"], outline=area["color"], width=2)

        # Tag
        tag_w = 160
        draw.rectangle([x + panel_w - tag_w, y, x + panel_w, y + 28], fill=area["color"])
        draw.text((x + panel_w - tag_w // 2, y + 14), area["tag"], fill=(255, 255, 255), font=get_font(13, bold=True), anchor="mm")

        # Title
        draw.text((x + 20, y + 40), area["name"], fill=(15, 23, 42), font=get_font(18, bold=True))
        draw.text((x + 20, y + 66), area["name_en"], fill=(148, 163, 184), font=get_font(11))

        # Color bar
        draw.rectangle([x + 20, y + 90, x + panel_w - 20, y + 94], fill=area["color"])

        # Content items
        for j, item in enumerate(area["content"]):
            item_y = y + 110 + j * 32
            draw.ellipse([x + 24, item_y + 5, x + 32, item_y + 13], fill=area["color"])
            draw.text((x + 42, item_y), item, fill=(71, 85, 105), font=get_font(14))

        # Bottom metric
        metric_y = y + panel_h - 60
        draw.rectangle([x + 20, metric_y, x + panel_w - 20, metric_y + 40], fill=area["color"] + (30,), outline=area["color"], width=1)
        draw.text((x + panel_w // 2, metric_y + 20), f"→ 对应 {['PROV-KEY-001', 'PROV-KEY-002', 'PROV-KEY-003'][i]}",
                  fill=area["color"], font=get_font(14, bold=True), anchor="mm")

    # Footer
    draw.text((30, H - 30), "三处重点区域范围均为临时边界(provisional)，非官方红线 | 详细设计深度：规划综合实施方案级",
              fill=(148, 163, 184), font=get_font(11))

    img.save(f"{FIGS_DIR}/key-areas.png", "PNG")
    print("key-areas.png saved")


# ============================================================
# Figure 4: Mobility & Blue-Green System (交通与蓝绿系统图)
# ============================================================
def gen_mobility_bluegreen():
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, W, 60], fill=(15, 23, 42))
    draw.text((30, 16), "百年京张AI创新带 — 交通慢行与蓝绿公共空间复合系统", fill=(255, 255, 255), font=get_font(22, bold=True))

    # Left: Mobility diagram
    cx, cy = 300, 400

    # Green corridor
    draw.ellipse([cx - 180, cy - 200, cx + 180, cy + 200], fill=(220, 252, 231), outline=(34, 197, 94), width=2)
    draw.text((cx, cy - 30), "京张遗址公园活力带", fill=(22, 101, 52), font=get_font(16, bold=True), anchor="mm")
    draw.text((cx, cy), "慢行·骑行·活动·文化", fill=(22, 101, 52), font=get_font(13), anchor="mm")

    # Blue corridor
    draw.ellipse([cx - 100, cy - 120, cx + 100, cy + 120], fill=(219, 234, 254), outline=(59, 130, 246), width=2)
    draw.text((cx, cy + 30), "清河生态廊道", fill=(29, 78, 216), font=get_font(14, bold=True), anchor="mm")

    # East wing
    draw.ellipse([cx + 190, cy - 80, cx + 300, cy + 80], fill=(237, 233, 254), outline=(168, 85, 247), width=2)
    draw.text((cx + 245, cy), "小月河场景赋能翼", fill=(107, 33, 168), font=get_font(13, bold=True), anchor="mm")

    # West wing
    draw.ellipse([cx - 300, cy - 80, cx - 190, cy + 80], fill=(254, 243, 199), outline=(245, 158, 11), width=2)
    draw.text((cx - 245, cy), "中关村科技服务翼", fill=(180, 83, 9), font=get_font(13, bold=True), anchor="mm")

    # Subway stations
    stations = [("清华东路西口", -80, -140), ("五道口", 0, -100), ("大钟寺", 60, 80)]
    for label, dx, dy in stations:
        px, py = cx + dx, cy + dy
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=(239, 68, 68), outline=(185, 28, 28), width=2)
        draw.text((px, py - 20), label, fill=(185, 28, 28), font=get_font(12, bold=True), anchor="mm")

    # Connecting lines
    draw.line([(cx - 180, cy), (cx + 180, cy)], fill=(34, 197, 94), width=3)
    draw.line([(cx, cy - 200), (cx, cy + 200)], fill=(34, 197, 94), width=2)

    # Right panel: Metrics
    rx, ry = 580, 90
    draw.text((rx, ry), "蓝绿与交通系统指标", fill=(15, 23, 42), font=get_font(18, bold=True))

    metrics = [
        ("绿地率", f"{GREEN_RATIO * 100:.2f}%", "绿地空间占比", (34, 197, 94)),
        ("公共空间率", f"{PUBLIC_SPACE_RATIO * 100:.2f}%", "公共空间占比", (168, 85, 247)),
        ("绿地面积", f"{GREEN_AREA / 10000:.1f} ha", "绿色空间总面积", (34, 197, 94)),
        ("公共空间面积", f"{PUBLIC_SPACE_AREA / 10000:.1f} ha", "公共空间总面积", (168, 85, 247)),
        ("建筑基底面积", f"{BLDG_FOOTPRINT / 10000:.1f} ha", "建筑基底总面积", (245, 158, 11)),
    ]
    for i, (t, v, s, c) in enumerate(metrics):
        y = ry + 40 + i * 70
        draw_card(draw, rx, y, 280, 62, t, v, s, c, title_size=13, value_size=24, sub_size=11)

    # Bottom: System components
    bx, by = 580, 470
    draw.text((bx, by), "系统构成", fill=(15, 23, 42), font=get_font(18, bold=True))
    components = [
        "慢行系统：京张遗址公园活力带（南北贯通）",
        "绿道系统：小月河生态廊道（东西连通）",
        "蓝带系统：清河生态廊道（滨水界面）",
        "轨道站点：清华东路西口、五道口、大钟寺",
        "慢行断点缝合：北五环、知春路等跨环节点",
    ]
    for i, comp in enumerate(components):
        y = by + 35 + i * 28
        draw.ellipse([bx, y + 5, bx + 8, y + 13], fill=(59, 130, 246))
        draw.text((bx + 18, y), comp, fill=(71, 85, 105), font=get_font(14))

    # Footer
    draw.text((30, H - 30), "慢行连通率目标≥90% | 无障碍达标率100% | 符合GB 50763无障碍设计规范",
              fill=(148, 163, 184), font=get_font(11))

    img.save(f"{FIGS_DIR}/mobility-bluegreen.png", "PNG")
    print("mobility-bluegreen.png saved")


# ============================================================
# Figure 5: Metrics Evidence (指标证据图)
# ============================================================
def gen_metrics_evidence():
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, W, 60], fill=(15, 23, 42))
    draw.text((30, 16), "百年京张AI创新带 — 核心指标复算与证据链", fill=(255, 255, 255), font=get_font(22, bold=True))

    # Main metrics cards
    card_w = 260
    card_h = 120
    gap = 20
    start_x = (W - 3 * card_w - 2 * gap) // 2

    metrics = [
        ("SITE-001", "基地面积", f"{SITE_AREA_HA:.1f} ha", "1141.28 ha", "geometry/site_boundary.geojson", (59, 130, 246)),
        ("BLDG-001", "建筑基底面积", f"{BLDG_FOOTPRINT / 10000:.1f} ha", "792,717.2 m²", "geometry/buildings.geojson", (245, 158, 11)),
        ("GREEN-001", "绿地面积", f"{GREEN_AREA / 10000:.1f} ha", f"{GREEN_RATIO * 100:.2f}%", "geometry/green_space.geojson", (34, 197, 94)),
    ]

    for i, (ref, title, val, sub, src, color) in enumerate(metrics):
        x = start_x + i * (card_w + gap)
        y = 90
        # Card
        rounded_rect(draw, [x, y, x + card_w, y + card_h], 10, fill=(255, 255, 255), outline=color, width=2)
        draw.rectangle([x + 2, y + 2, x + card_w - 2, y + 6], fill=color)
        draw.text((x + 15, y + 14), f"[{ref}] {title}", fill=(100, 116, 139), font=get_font(14, bold=True))
        draw.text((x + 15, y + 40), val, fill=(15, 23, 42), font=get_font(28, bold=True))
        draw.text((x + 15, y + 80), sub, fill=(148, 163, 184), font=get_font(12))
        draw.text((x + 15, y + 96), src, fill=(203, 213, 225), font=get_font(10))

    # Secondary metrics row
    metrics2 = [
        ("PUBLIC-001", "公共空间面积", f"{PUBLIC_SPACE_AREA / 10000:.1f} ha", f"{PUBLIC_SPACE_RATIO * 100:.2f}%", "geometry/public_space.geojson", (168, 85, 247)),
        ("KEY-001", "重点区域", "3 处", "众智园/原点社区/大钟寺", "geometry/key_areas.geojson", (239, 68, 68)),
        ("PHASE-001", "实施分期", "近期/中期/长期", "3 阶段", "geometry/phasing.geojson", (100, 116, 139)),
    ]

    for i, (ref, title, val, sub, src, color) in enumerate(metrics2):
        x = start_x + i * (card_w + gap)
        y = 240
        rounded_rect(draw, [x, y, x + card_w, y + card_h - 10], 10, fill=(255, 255, 255), outline=color, width=2)
        draw.rectangle([x + 2, y + 2, x + card_w - 2, y + 6], fill=color)
        draw.text((x + 15, y + 14), f"[{ref}] {title}", fill=(100, 116, 139), font=get_font(14, bold=True))
        draw.text((x + 15, y + 40), val, fill=(15, 23, 42), font=get_font(28, bold=True))
        draw.text((x + 15, y + 80), sub, fill=(148, 163, 184), font=get_font(12))
        draw.text((x + 15, y + 96), src, fill=(203, 213, 225), font=get_font(10))

    # Bottom: Evidence chain
    by = 380
    draw.text((start_x, by), "数据证据链", fill=(15, 23, 42), font=get_font(18, bold=True))

    chain_steps = [
        ("GeoJSON 图层", "geometry/*.geojson", (59, 130, 246)),
        ("面积复算", "shapely (EPSG:4548)", (34, 197, 94)),
        ("metrics.json", "结构化指标表", (245, 158, 11)),
        ("proposal.md", "正文引用与解释", (239, 68, 68)),
        ("HTML/PNG/PDF", "可视化展示", (168, 85, 247)),
    ]

    for i, (step, desc, color) in enumerate(chain_steps):
        x = start_x + i * ((card_w + gap) // 2 + 20)
        y = by + 40
        # Node
        draw.ellipse([x, y, x + 30, y + 30], fill=color)
        draw.text((x + 15, y + 15), str(i + 1), fill=(255, 255, 255), font=get_font(14, bold=True), anchor="mm")
        draw.text((x + 15, y + 38), step, fill=(15, 23, 42), font=get_font(13, bold=True), anchor="mm")
        draw.text((x + 15, y + 56), desc, fill=(100, 116, 139), font=get_font(11), anchor="mm")
        # Arrow
        if i < len(chain_steps) - 1:
            ax = x + 40
            draw.line([(x + 30, y + 15), (ax + 5, y + 15)], fill=(203, 213, 225), width=2)
            draw.polygon([(ax + 5, y + 11), (ax + 12, y + 15), (ax + 5, y + 19)], fill=(203, 213, 225))

    # Status indicators
    sy = 540
    draw.text((start_x, sy), "指标状态", fill=(15, 23, 42), font=get_font(18, bold=True))
    status_items = [
        ("known", "6 项", "可直接从 GeoJSON 复算", (34, 197, 94)),
        ("unknown", "1 项", "需官方控规数据支撑", (245, 158, 11)),
        ("provisional", "边界", "临时边界，待官方数据替换", (239, 68, 68)),
    ]
    for i, (status, count, desc, color) in enumerate(status_items):
        x = start_x + i * 280
        y = sy + 40
        rounded_rect(draw, [x, y, x + 250, y + 60], 8, fill=(255, 255, 255), outline=color, width=2)
        draw.ellipse([x + 12, y + 12, x + 24, y + 24], fill=color)
        draw.text((x + 32, y + 8), f"{status}: {count}", fill=(15, 23, 42), font=get_font(14, bold=True))
        draw.text((x + 32, y + 32), desc, fill=(100, 116, 139), font=get_font(11))

    # Footer
    draw.text((30, H - 30), "所有已知指标均从 GeoJSON 在 EPSG:4548 下复算 | 面积指标为 provisional boundary 估算，非官方审定数据",
              fill=(148, 163, 184), font=get_font(11))

    img.save(f"{FIGS_DIR}/metrics-evidence.png", "PNG")
    print("metrics-evidence.png saved")


# Generate all figures
gen_site_overview()
gen_land_use()
gen_key_areas()
gen_mobility_bluegreen()
gen_metrics_evidence()
print("All 5 figures regenerated successfully!")