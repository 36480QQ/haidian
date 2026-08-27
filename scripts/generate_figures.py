#!/usr/bin/env python3
"""Generate Chinese and English figures for the submission."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SUBMISSION = Path("submissions/kati-99/jingzhang-intelligence-loop")
FIGURES = SUBMISSION / "assets/figures"


def load_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def font(size):
    for fp in [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/Library/Fonts/Arial.ttf",
    ]:
        try:
            return ImageFont.truetype(fp, size)
        except Exception:
            pass
    return ImageFont.load_default()


def make_figure1(lang="zh"):
    """site-overview: evidence chain diagram"""
    W, H = 1600, 1000
    img = Image.new("RGB", (W, H), (250, 250, 252))
    d = ImageDraw.Draw(img)
    title = "资料证据链与提交包" if lang == "zh" else "Evidence Chain & Submission Package"
    d.text((60, 40), title, fill=(22, 32, 51), font=font(48))
    sub = "boundary=provisional intake; proposal.md 是主体，JSON/GeoJSON 是证据层" if lang == "zh" else "boundary=provisional intake; proposal.md is narrative, JSON/GeoJSON is evidence"
    d.text((60, 100), sub, fill=(102, 112, 133), font=font(26))

    boxes = [
        (120, 220, 400, 700, "公告 / Announcement", "blue"),
        (500, 220, 780, 700, "图层 / Layers", "green"),
        (880, 220, 1160, 700, "自检 / Self-check", "orange"),
    ]
    labels = [
        ("边界", "Boundary"),
        ("指标", "Metrics"),
        ("来源", "Sources"),
    ]
    for x1, y1, x2, y2, label, color in boxes:
        fill = {"blue": (239, 246, 255), "green": (240, 253, 244), "orange": (255, 251, 235)}[color]
        outline = {"blue": (59, 130, 246), "green": (34, 197, 94), "orange": (245, 158, 11)}[color]
        d.rounded_rectangle([x1, y1, x2, y2], radius=20, fill=fill, outline=outline, width=4)
        d.text((x1 + 20, y1 + 30), label, fill=(17, 24, 39), font=font(32))

    # connector arrows
    d.line([400, 470, 500, 470], fill=(156, 163, 175), width=6)
    d.polygon([(500, 470), (490, 460), (490, 480)], fill=(156, 163, 175))
    d.line([780, 470, 880, 470], fill=(156, 163, 175), width=6)
    d.polygon([(880, 470), (870, 460), (870, 480)], fill=(156, 163, 175))

    # small nodes
    d.ellipse([210, 620, 310, 720], fill=(79, 70, 229))
    d.text((260, 660), labels[0][0] if lang == "zh" else labels[0][1], fill=(255, 255, 255), font=font(28), anchor="mm")
    d.ellipse([620, 620, 720, 720], fill=(21, 128, 61))
    d.text((670, 660), labels[1][0] if lang == "zh" else labels[1][1], fill=(255, 255, 255), font=font(28), anchor="mm")
    d.ellipse([1000, 620, 1100, 720], fill=(199, 152, 56))
    d.text((1050, 660), labels[2][0] if lang == "zh" else labels[2][1], fill=(255, 255, 255), font=font(28), anchor="mm")

    foot = "由提交包 GeoJSON、metrics.json、矩阵与自检结果派生；不得替代 official boundary 或专业图纸。" if lang == "zh" else "Derived from submitted GeoJSON, metrics.json, matrices and self-check; not a substitute for official boundary or professional drawings."
    d.text((60, 920), foot, fill=(102, 112, 133), font=font(22))
    return img


def make_figure2(lang="zh"):
    """land-use-structure: three-level scope framework"""
    W, H = 1600, 1000
    img = Image.new("RGB", (W, H), (250, 250, 252))
    d = ImageDraw.Draw(img)
    title = "三层范围与空间工作框架" if lang == "zh" else "Three-Level Scope Framework"
    d.text((60, 40), title, fill=(22, 32, 51), font=font(48))

    levels = [
        ("统筹研究范围\n43.6 km²", "Coordinated Research\n43.6 km²", "产业生态 / Ecosystem", (239, 246, 255), (59, 130, 246)),
        ("总体设计范围\n11.4 km²", "Overall Design\n11.4 km²", "城市更新 / Urban Renewal", (240, 253, 244), (34, 197, 94)),
        ("重点区域范围\n3.68 km²", "Key Areas\n3.68 km²", "详细设计 / Detailed Design", (255, 251, 235), (245, 158, 11)),
    ]
    x = 140
    for zh, en, tag, fill, outline in levels:
        label = zh if lang == "zh" else en
        d.rounded_rectangle([x, 220, x + 380, 800], radius=24, fill=fill, outline=outline, width=5)
        d.text((x + 190, 300), label, fill=(17, 24, 39), font=font(34), anchor="mm")
        d.text((x + 190, 520), tag, fill=(75, 85, 99), font=font(26), anchor="mm")
        x += 440

    # arrows
    for x0 in [520, 960]:
        d.line([x0, 510, x0 + 60, 510], fill=(107, 114, 128), width=6)
        d.polygon([(x0 + 60, 510), (x0 + 50, 500), (x0 + 50, 520)], fill=(107, 114, 128))

    foot = "三层范围从产业战略、总体城市设计、重点片区详细设计逐级落实。" if lang == "zh" else "Three scopes cascade from industrial strategy to overall urban design to key-area detailed design."
    d.text((60, 920), foot, fill=(102, 112, 133), font=font(22))
    return img


def make_figure3(lang="zh"):
    """key-areas: three key areas spatial diagram + design-task cards."""
    W, H = 1600, 1300
    img = Image.new("RGB", (W, H), (250, 250, 252))
    d = ImageDraw.Draw(img)

    # ---- header band ----
    title = "三处重点区域索引与设计任务" if lang == "zh" else "Three Key Areas — Index & Design Tasks"
    d.text((60, 36), title, fill=(22, 32, 51), font=font(46))
    sub_zh = "总体设计范围内由北至南的三处详细设计片区 · 临时粗略范围 · 不得作为 official boundary"
    sub_en = "Three detailed-design districts from north to south within the overall design scope · provisional · not an official boundary"
    d.text((60, 92), sub_zh if lang == "zh" else sub_en, fill=(102, 112, 133), font=font(22))

    # provisional badge
    badge_x0, badge_y0, badge_x1, badge_y1 = 1290, 36, 1568, 80
    d.rounded_rectangle([badge_x0, badge_y0, badge_x1, badge_y1], radius=10, fill=(254, 226, 226), outline=(220, 38, 38), width=2)
    d.text(((badge_x0 + badge_x1) / 2, (badge_y0 + badge_y1) / 2),
           "provisional · intake only", fill=(153, 27, 27), font=font(20), anchor="mm")

    # ---- map area ----
    bounds = (116.337, 116.360, 39.935, 40.030)  # lon_min, lon_max, lat_min, lat_max
    map_box = (60, 150, 940, 1010)  # x0, y0, x1, y1 (height 860)

    def proj(lon, lat):
        lon_min, lon_max, lat_min, lat_max = bounds
        x0, y0, x1, y1 = map_box
        x = x0 + (lon - lon_min) / (lon_max - lon_min) * (x1 - x0)
        y = y1 - (lat - lat_min) / (lat_max - lat_min) * (y1 - y0)
        return x, y

    def poly_px(coords):
        return [proj(lon, lat) for lon, lat in coords]

    def load(rel):
        with open(SUBMISSION / rel, "r", encoding="utf-8") as fh:
            return json.load(fh)

    # map background (paper)
    d.rectangle(map_box, fill=(248, 250, 252), outline=(180, 188, 200), width=2)

    # ---- backdrop: 4 land-use columns (very light) ----
    lu_pale = {
        "0802": (231, 231, 255),
        "1401": (223, 248, 233),
        "05":   (255, 242, 204),
        "0702": (255, 227, 223),
    }
    lu_feats = load("geometry/land_use.geojson")["features"]
    for f in lu_feats:
        code = f["properties"]["land_use_code"]
        d.polygon(poly_px(f["geometry"]["coordinates"][0]),
                  fill=lu_pale[code], outline=None)
    # add pale column tick labels (top)
    col_label_y = map_box[1] - 6
    for f in lu_feats:
        coords = f["geometry"]["coordinates"][0]
        lons = [c[0] for c in coords]
        cx, _ = proj((min(lons) + max(lons)) / 2, bounds[3])
        code = f["properties"]["land_use_code"]
        zh_short = {
            "0802": "AI研发",
            "1401": "公园",
            "05":   "产业",
            "0702": "社区",
        }[code]
        en_short = {
            "0802": "AI R&D",
            "1401": "Park",
            "05":   "Industry",
            "0702": "Community",
        }[code]
        d.text((cx, col_label_y), zh_short if lang == "zh" else en_short,
               fill=(75, 85, 99), font=font(20), anchor="ms")

    # ---- site boundary (dashed provisional) ----
    site = load("geometry/site_boundary.geojson")["features"][0]["geometry"]["coordinates"][0]
    d.polygon(poly_px(site), fill=None, outline=(22, 32, 51), width=3)
    # add small "provisional" marker in empty space top-right of map (inside site boundary, outside all KEYS)
    bx, by = proj(116.357, 40.025)
    d.rounded_rectangle([bx - 100, by - 18, bx + 100, by + 18], radius=8,
                       fill=(255, 251, 235), outline=(217, 119, 6), width=2)
    d.text((bx, by),
           "SITE-001 · 11.4 km²",
           fill=(146, 64, 14), font=font(20), anchor="mm")

    # ---- heritage park spine (LU-002) — bold green ----
    park = next(f for f in lu_feats if f["properties"]["land_use_code"] == "1401")
    park_px = poly_px(park["geometry"]["coordinates"][0])
    d.polygon(park_px, fill=(34, 197, 94, 100), outline=(21, 128, 61), width=4)
    # park label (in the empty corridor between KEY-002 and KEY-003, lat ~39.972)
    pcx, pcy = proj(116.3456, 39.972)
    d.rounded_rectangle([pcx - 134, pcy - 22, pcx + 134, pcy + 22], radius=10,
                       fill=(255, 255, 255), outline=(21, 128, 61), width=2)
    d.text((pcx, pcy),
           "京张遗址公园 · 绿脊" if lang == "zh" else "Jingzhang Heritage Park",
           fill=(21, 128, 61), font=font(22), anchor="mm")

    # ---- 3 key area polygons + callouts ----
    area_palette = {
        "PROV-KEY-001": {
            "fill": (199, 210, 254), "stroke": (79, 70, 229),
            "zh": "众智园 · AI自主创新加速区", "en": "Zhongzhiyuan · AI Acceleration",
            "ha": 192.1, "code": "0802+1401+05+0702",
            "moves_zh": ["· 高校策源—开源协作—企业转化三链闭环",
                         "· 改造低效工业基底，补全青年人才公寓",
                         "· 街坊化研发街区 + 公共小馆展厅",
                         "· 与京张公园连通的步行+骑行车流"],
            "moves_en": ["· University sourcing → enterprise translation loop",
                         "· Retrofit low-efficiency industrial sites + talent housing",
                         "· Neighborhood R&D blocks + public small-museum nodes",
                         "· Pedestrian + bike links to Jingzhang park spine"],
            "risk_zh": "权属复杂，需先做城市更新单元规划",
            "risk_en": "Mixed ownership; needs urban-renewal unit plan first",
        },
        "PROV-KEY-002": {
            "fill": (187, 247, 208), "stroke": (21, 128, 61),
            "zh": "北京AI原点社区", "en": "Beijing AI Origin Community",
            "ha": 104.3, "code": "0802+1401+05+0702",
            "moves_zh": ["· 近校型成果转化与开源实验室集群",
                         "· 高校—社区—公共生活三向渗透",
                         "· 慢行骨架串联 5 个创新节点",
                         "· 文化母题：1909 年“人字形”精神"],
            "moves_en": ["· Campus-linked translation + open-source labs cluster",
                         "· University ↔ community ↔ public life interlock",
                         "· Slow-traffic spine linking 5 innovation nodes",
                         "· Cultural motif: 1909 '人字形' railway spirit"],
            "risk_zh": "高校红线外溢，须与学校协议先签",
            "risk_en": "University boundary overlap; needs MOUs first",
        },
        "PROV-KEY-003": {
            "fill": (254, 215, 170), "stroke": (183, 121, 31),
            "zh": "大钟寺 · AI产业集聚区", "en": "Dazhongsi · AI Industry Cluster",
            "ha": 72.0, "code": "0802+1401+05+0702",
            "moves_zh": ["· 城市型智能经济街区（商务+消费）",
                         "· 轨道站点一体化上盖开发",
                         "· 城市更新：保留—改造—拆除分级",
                         "· 大钟寺历史场景作为公共客厅"],
            "moves_en": ["· Urban smart-economy district (office + retail)",
                         "· Integrated over-station development at Dazhongsi",
                         "· Tiered retain / retrofit / demolish strategy",
                         "· Dazhongsi heritage as a public 'living room'"],
            "risk_zh": "轨道施工期与商业运营的统筹",
            "risk_en": "Coordination between metro construction and retail",
        },
    }
    key_feats = load("geometry/key_areas.geojson")["features"]
    # sort by lat (north→south)
    key_feats_sorted = sorted(key_feats, key=lambda f: -f["geometry"]["coordinates"][0][0][1])

    for f in key_feats_sorted:
        fid = f["id"]
        info = area_palette[fid]
        coords = f["geometry"]["coordinates"][0]
        lons = [c[0] for c in coords]; lats = [c[1] for c in coords]
        cx, cy = proj(sum(lons) / len(lons), sum(lats) / len(lats))
        d.polygon(poly_px(coords), fill=info["fill"], outline=info["stroke"], width=4)
        # white-pill background behind 4 label lines (always readable on any land-use tint)
        pill_x0, pill_x1 = cx - 138, cx + 138
        pill_top = cy - 22
        pill_bot = cy + 76
        d.rounded_rectangle([pill_x0, pill_top, pill_x1, pill_bot], radius=10,
                           fill=(255, 255, 255), outline=info["stroke"], width=2)
        d.text((cx, pill_top + 14), fid, fill=info["stroke"], font=font(20), anchor="mm")
        d.text((cx, pill_top + 38),
               f"{info['ha']:.1f} ha",
               fill=(31, 41, 55), font=font(22), anchor="mm")
        d.text((cx, pill_top + 62),
               info["zh"] if lang == "zh" else info["en"],
               fill=(31, 41, 55), font=font(20), anchor="mm")
        d.text((cx, pill_top + 86),
               f"LU: {info['code']}",
               fill=(75, 85, 99), font=font(16), anchor="mm")

    # ---- north arrow (top-right of map) ----
    na_x, na_y = map_box[2] - 80, map_box[1] + 80
    d.polygon([(na_x, na_y - 50), (na_x - 18, na_y + 18), (na_x + 18, na_y + 18)],
              fill=(22, 32, 51))
    d.text((na_x, na_y + 36), "N", fill=(22, 32, 51), font=font(24), anchor="mm")

    # ---- schematic disclaimer + scale bar in a clear strip BELOW the map ----
    info_strip_y0 = map_box[3] + 8   # 1018
    info_strip_y1 = map_box[3] + 56  # 1066

    # scale bar (left half)
    sb_x0 = map_box[0] + 30
    sb_y0 = info_strip_y0 + 18
    sb_len_deg = 0.0060
    sb_x1 = sb_x0 + (sb_len_deg / (bounds[1] - bounds[0])) * (map_box[2] - map_box[0])
    d.rectangle([sb_x0, sb_y0, sb_x1, sb_y0 + 8], fill=(22, 32, 51))
    d.rectangle([sb_x0, sb_y0 + 8, sb_x1, sb_y0 + 16], fill=(255, 255, 255), outline=(22, 32, 51), width=1)
    d.text((sb_x0, sb_y0 - 8), "0", fill=(22, 32, 51), font=font(18), anchor="mm")
    d.text(((sb_x0 + sb_x1) / 2, sb_y0 - 8), "≈ 0.5 km", fill=(22, 32, 51), font=font(18), anchor="mm")
    d.text((sb_x1, sb_y0 - 8), "≈ 1 km", fill=(22, 32, 51), font=font(18), anchor="mm")

    # disclaimer (right half)
    sd_text = ("示意图，非真实比例；矩形边不代表地块或道路红线"
               if lang == "zh" else
               "Schematic, not to scale; rectangle edges are not plot or redline boundaries")
    sd_x0, sd_y0 = map_box[2] - 540, info_strip_y0 + 4
    d.rounded_rectangle([sd_x0, sd_y0, map_box[2] - 16, sd_y0 + 44], radius=8,
                       fill=(254, 243, 199), outline=(217, 119, 6), width=1)
    d.text((sd_x0 + 12, sd_y0 + 22), sd_text, fill=(146, 64, 14), font=font(20), anchor="lm")

    # ---- right rail: 3 design task cards ----
    rail_x0, rail_x1 = 980, 1560
    rail_w = rail_x1 - rail_x0
    card_h = 290
    rail_y0 = 150
    for i, f in enumerate(key_feats_sorted):
        fid = f["id"]
        info = area_palette[fid]
        cy0 = rail_y0 + i * (card_h + 14)
        cy1 = cy0 + card_h
        # card body
        d.rounded_rectangle([rail_x0, cy0, rail_x1, cy1], radius=14,
                            fill=(255, 255, 255), outline=info["stroke"], width=3)
        # left color bar
        d.rectangle([rail_x0, cy0, rail_x0 + 10, cy1], fill=info["stroke"])
        # header
        d.rounded_rectangle([rail_x0 + 22, cy0 + 14, rail_x0 + 22 + 130, cy0 + 50],
                           radius=8, fill=info["stroke"])
        d.text((rail_x0 + 22 + 65, cy0 + 32), fid, fill=(255, 255, 255), font=font(20), anchor="mm")
        # area name + hectares
        d.text((rail_x0 + 162, cy0 + 26), info["zh"] if lang == "zh" else info["en"],
               fill=(17, 24, 39), font=font(22), anchor="lm")
        d.text((rail_x0 + 162, cy0 + 50),
               f"≈ {info['ha']:.1f} ha · LU: {info['code']}",
               fill=(75, 85, 99), font=font(18), anchor="lm")
        # design moves bullets
        moves = info["moves_zh"] if lang == "zh" else info["moves_en"]
        for j, m in enumerate(moves):
            d.text((rail_x0 + 30, cy0 + 86 + j * 32), m,
                   fill=(31, 41, 55), font=font(17), anchor="lm")
        # risk footer
        risk = info["risk_zh"] if lang == "zh" else info["risk_en"]
        risk_y = cy1 - 36
        d.rounded_rectangle([rail_x0 + 22, risk_y - 18, rail_x1 - 22, risk_y + 18], radius=8,
                           fill=(254, 226, 226), outline=(220, 38, 38), width=1)
        d.text((rail_x0 + 36, risk_y),
               ("⚠ 实施风险：" if lang == "zh" else "⚠ Risk: ") + risk,
               fill=(153, 27, 27), font=font(18), anchor="lm")

    # ---- footer: legend + data source + provisional warning ----
    foot_y0 = 1100
    d.line([(60, foot_y0), (1540, foot_y0)], fill=(180, 188, 200), width=2)

    # legend title
    d.text((60, foot_y0 + 14),
           "图例 / Legend" if lang == "zh" else "Legend",
           fill=(22, 32, 51), font=font(24))

    legend_items = [
        ("SITE-001", (255, 255, 255), (22, 32, 51), "总体设计范围 11.4 km²", "Overall design scope 11.4 km²"),
        ("PROV-KEY-001", (199, 210, 254), (79, 70, 229), "众智园 192.1 ha", "Zhongzhiyuan 192.1 ha"),
        ("PROV-KEY-002", (187, 247, 208), (21, 128, 61), "AI 原点 104.3 ha", "AI Origin 104.3 ha"),
        ("PROV-KEY-003", (254, 215, 170), (183, 121, 31), "大钟寺 72.0 ha", "Dazhongsi 72.0 ha"),
        ("HERITAGE", (34, 197, 94), (21, 128, 61), "京张遗址公园", "Jingzhang Heritage Park"),
        ("LU 0802/1401/05/0702", (231, 231, 255), (79, 70, 229), "AI研发/公园/产业/社区", "AI R&D / Park / Industry / Community"),
    ]
    lx = 60
    ly = foot_y0 + 50
    for tag, fill, stroke, zh, en in legend_items:
        d.rectangle([lx, ly, lx + 28, ly + 22], fill=fill, outline=stroke, width=2)
        d.text((lx + 36, ly + 4), tag, fill=(22, 32, 51), font=font(20), anchor="lm")
        d.text((lx + 36, ly + 28), zh if lang == "zh" else en,
               fill=(75, 85, 99), font=font(18), anchor="lm")
        lx += 240

    # data source line + provisional warning
    d.text((60, foot_y0 + 100),
           "数据来源 / Data: geometry/site_boundary.geojson · geometry/land_use.geojson · geometry/key_areas.geojson (boundary=provisional_rough, intake only)",
           fill=(75, 85, 99), font=font(18))
    d.text((60, foot_y0 + 128),
           "临时粗略范围 · 不得作为 official boundary · 评审用 / Provisional · not an official boundary · for review only",
           fill=(220, 38, 38), font=font(20))
    return img


def make_figure4(lang="zh"):
    """mobility-bluegreen: transport + blue-green public space"""
    W, H = 1600, 1000
    img = Image.new("RGB", (W, H), (250, 250, 252))
    d = ImageDraw.Draw(img)
    title = "交通慢行与蓝绿公共空间复合系统" if lang == "zh" else "Mobility & Blue-Green Public Space System"
    d.text((60, 40), title, fill=(22, 32, 51), font=font(48))

    # Map frame
    d.rectangle([120, 150, 1400, 850], fill=(255, 255, 255), outline=(120, 130, 150), width=2)
    # Site boundary rough
    d.polygon([(180, 780), (360, 780), (380, 640), (500, 520), (700, 420), (900, 360), (1100, 300), (1300, 260), (1320, 200), (180, 200)],
              fill=(240, 242, 246), outline=(120, 130, 150), width=2)
    # Green corridor (Jingzhang park)
    d.line([(200, 760), (400, 600), (650, 460), (920, 360), (1280, 240)], fill=(34, 197, 94), width=18)
    # Roads
    for x in [300, 600, 950]:
        d.line([(x, 200), (x, 780)], fill=(15, 116, 144), width=6)
    for y in [350, 550]:
        d.line([(180, y), (1320, y)], fill=(15, 116, 144), width=6)
    # Nodes
    for cx, cy, name_zh, name_en, col in [
        (320, 620, "众智园", "Zhongzhiyuan", (79, 70, 229)),
        (660, 430, "AI原点", "AI Origin", (21, 128, 61)),
        (1020, 310, "大钟寺", "Dazhongsi", (183, 121, 31)),
    ]:
        d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=col)
        d.text((cx, cy), name_zh if lang == "zh" else name_en, fill=(255, 255, 255), font=font(22), anchor="mm")

    # Legend
    legend_x = 1450
    items = [
        ("京张遗址公园活力带", "Jingzhang Park Belt", (34, 197, 94)),
        ("交通微循环", "Microcirculation Roads", (15, 116, 144)),
        ("重点片区", "Key Areas", (107, 114, 128)),
    ]
    y = 200
    for zh, en, col in items:
        d.rectangle([legend_x, y, legend_x + 40, y + 20], fill=col)
        d.text((legend_x + 50, y), zh if lang == "zh" else en, fill=(22, 32, 51), font=font(20))
        y += 50

    foot = "以京张遗址公园为骨架，构建南北贯通、东西缝合的慢行与蓝绿公共空间网络。" if lang == "zh" else "Use Jingzhang heritage park as the spine to build a north-south and east-west slow-traffic and blue-green network."
    d.text((60, 920), foot, fill=(102, 112, 133), font=font(22))
    return img


def make_figure5(lang="zh"):
    """metrics-evidence: key metrics dashboard"""
    W, H = 1600, 1000
    img = Image.new("RGB", (W, H), (250, 250, 252))
    d = ImageDraw.Draw(img)
    title = "核心指标复算与证据链" if lang == "zh" else "Key Metrics Recalculation & Evidence Chain"
    d.text((60, 40), title, fill=(22, 32, 51), font=font(48))

    metrics = [
        ("site_area_sqm", "总体设计范围面积", "Overall design area", "11,412,825", "m²", "geometry/site_boundary.geojson"),
        ("green_ratio", "绿地比例", "Green ratio", "12.34", "%", "geometry/green_space.geojson"),
        ("public_space_ratio", "公共空间比例", "Public space ratio", "7.33", "%", "geometry/public_space.geojson"),
        ("building_footprint", "建筑基底面积", "Building footprint", "310,807", "m²", "geometry/buildings.geojson"),
    ]
    x = 120
    for key, zh_label, en_label, value, unit, source in metrics:
        label = zh_label if lang == "zh" else en_label
        d.rounded_rectangle([x, 220, x + 340, 520], radius=16, fill=(255, 255, 255), outline=(215, 223, 235), width=2)
        d.text((x + 170, 280), label, fill=(22, 32, 51), font=font(26), anchor="mm")
        d.text((x + 170, 360), value, fill=(79, 70, 229), font=font(42), anchor="mm")
        d.text((x + 170, 420), unit, fill=(102, 112, 133), font=font(22), anchor="mm")
        d.text((x + 170, 470), source, fill=(156, 163, 175), font=font(16), anchor="mm")
        x += 370

    # Evidence chain arrows
    y = 600
    steps = [
        ("GeoJSON 图层", "GeoJSON layers"),
        ("metrics.json 复算", "metrics.json recalc"),
        ("合规矩阵", "Compliance matrix"),
        ("自检通过", "Self-check PASS"),
    ]
    x = 120
    for zh, en in steps:
        label = zh if lang == "zh" else en
        d.rounded_rectangle([x, y, x + 300, y + 120], radius=12, fill=(240, 253, 244), outline=(34, 197, 94), width=2)
        d.text((x + 150, y + 60), label, fill=(17, 24, 39), font=font(24), anchor="mm")
        if x < 1200:
            d.line([x + 300, y + 60, x + 370, y + 60], fill=(107, 114, 128), width=4)
            d.polygon([(x + 370, y + 60), (x + 360, y + 50), (x + 360, y + 70)], fill=(107, 114, 128))
        x += 370

    foot = "指标从同一组 GeoJSON 复算；FAR、高度等控规指标因缺少官方条件暂列为 unknown。" if lang == "zh" else "Metrics are recalculated from the same GeoJSON; FAR and height remain unknown pending official controls."
    d.text((60, 920), foot, fill=(102, 112, 133), font=font(22))
    return img


def make_figure_site_structure(lang="zh"):
    """site-structure: overall spatial structure plan derived from GeoJSON layers."""
    W, H = 1600, 1000
    img = Image.new("RGB", (W, H), (250, 250, 252))
    d = ImageDraw.Draw(img)
    title = "总体空间结构图" if lang == "zh" else "Overall Spatial Structure"
    d.text((60, 40), title, fill=(22, 32, 51), font=font(48))
    sub = ("用地分区 · 京张遗址公园活力带 · 三处重点区域 · 一期可讨论范围 · 慢行廊道（临时边界，intake 用）"
           if lang == "zh" else
           "Land-use zones · Jingzhang heritage park belt · three key areas · phase-1 · slow corridor (provisional, intake)")
    d.text((60, 104), sub, fill=(102, 112, 133), font=font(23))

    bounds = (116.3397, 116.3553, 39.939, 40.0265)  # lon_min, lon_max, lat_min, lat_max
    plot = (120, 170, 1180, 680)  # x0, y0, w, h

    def proj(lon, lat):
        lon_min, lon_max, lat_min, lat_max = bounds
        x0, y0, w, h = plot
        x = x0 + (lon - lon_min) / (lon_max - lon_min) * w
        y = y0 + (lat_max - lat) / (lat_max - lat_min) * h
        return x, y

    def poly_px(coords):
        return [proj(lon, lat) for lon, lat in coords]

    def load(rel):
        with open(SUBMISSION / rel, "r", encoding="utf-8") as fh:
            return json.load(fh)

    # 1) site boundary
    site = load("geometry/site_boundary.geojson")["features"][0]["geometry"]["coordinates"][0]
    d.polygon(poly_px(site), fill=(255, 255, 255), outline=(22, 32, 51), width=5)

    # 2) land-use zones
    lu_colors = {
        "0802": ((231, 231, 255), (79, 70, 229)),
        "1401": ((223, 248, 233), (21, 128, 61)),
        "05":   ((255, 242, 204), (183, 121, 31)),
        "0702": ((255, 227, 223), (180, 35, 24)),
    }
    lu_feats = load("geometry/land_use.geojson")["features"]
    for f in lu_feats:
        code = f["properties"]["land_use_code"]
        fill, outline = lu_colors[code]
        d.polygon(poly_px(f["geometry"]["coordinates"][0]), fill=fill, outline=outline, width=3)

    # 2b) heritage park belt caption
    green_cx, _ = proj(116.3456, 39.98)
    d.text((green_cx, 190), "京张遗址公园活力带" if lang == "zh" else "Jingzhang Heritage Park Belt",
           fill=(21, 128, 61), font=font(22), anchor="mm")

    # 3) public space marker
    pub = load("geometry/public_space.geojson")["features"][0]["geometry"]["coordinates"][0]
    d.polygon(poly_px(pub), fill=(255, 255, 255), outline=(15, 116, 144), width=3)
    pcx, pcy = proj(116.34867, 39.970)
    d.text((pcx, pcy), "公共活动界面" if lang == "zh" else "Public Interface",
           fill=(15, 116, 144), font=font(18), anchor="mm")

    # 4) building footprint
    bldg = load("geometry/buildings.geojson")["features"][0]["geometry"]["coordinates"][0]
    d.polygon(poly_px(bldg), fill=(79, 70, 229), outline=(49, 46, 129), width=2)

    # 4b) land-use labels (drawn after building; white pill keeps them readable over fills)
    lu_names = {
        "0802": ("AI研发创新用地", "AI R&D Innovation"),
        "1401": ("公园绿地与开敞空间", "Parks & Open Space"),
        "05":   ("产业服务与商业服务用地", "Industry & Commercial"),
        "0702": ("社区服务与配套用地", "Community & Support"),
    }
    for f in lu_feats:
        code = f["properties"]["land_use_code"]
        coords = f["geometry"]["coordinates"][0]
        cx, _ = proj(sum(c[0] for c in coords) / len(coords), sum(c[1] for c in coords) / len(coords))
        name = lu_names[code][0] if lang == "zh" else lu_names[code][1]
        cy = 700
        tw = len(name) * 22 + 16
        d.rounded_rectangle([cx - tw / 2, cy - 14, cx + tw / 2, cy + 14], radius=8,
                            fill=(255, 255, 255), outline=(180, 190, 210), width=1)
        d.text((cx, cy), name, fill=(17, 24, 39), font=font(22), anchor="mm")

    # 5) roads / greenway corridor
    road = load("geometry/roads.geojson")["features"][0]["geometry"]["coordinates"]
    d.line([proj(*p) for p in road], fill=(15, 116, 144), width=8)
    rcx, rcy = proj(road[-1][0], road[-1][1])
    d.text((rcx, rcy - 22), "慢行与创新服务廊道" if lang == "zh" else "Slow & Innovation Corridor",
           fill=(15, 116, 144), font=font(18), anchor="mm")

    # 6) phasing phase-1
    phase = load("geometry/phasing.geojson")["features"][0]["geometry"]["coordinates"][0]
    d.polygon(poly_px(phase), outline=(245, 158, 11), width=4)
    phx, phy = proj(116.3445, 40.0)
    d.text((phx, phy), "一期可讨论范围" if lang == "zh" else "Phase 1 (discussable)",
           fill=(180, 120, 10), font=font(18), anchor="mm")

    # 7) key areas (provisional)
    key_names = {
        "PROV-KEY-001": ("众智园AI自主创新加速区", "Zhongzhiyuan AI Acceleration"),
        "PROV-KEY-002": ("北京AI原点社区", "Beijing AI Origin Community"),
        "PROV-KEY-003": ("大钟寺AI产业聚集区", "Dazhongsi AI Industry Cluster"),
    }
    for f in load("geometry/key_areas.geojson")["features"]:
        kid = f["properties"]["id"]
        pts = poly_px(f["geometry"]["coordinates"][0])
        d.polygon(pts, outline=(15, 23, 42), width=4)
        coords = f["geometry"]["coordinates"][0]
        cx, cy = proj(sum(c[0] for c in coords) / len(coords), sum(c[1] for c in coords) / len(coords))
        name = key_names.get(kid, (kid, kid))[0] if lang == "zh" else key_names.get(kid, (kid, kid))[1]
        tw = max(len(name), 6) * (20 if lang == "zh" else 11)
        d.rounded_rectangle([cx - tw / 2 - 8, cy - 20, cx + tw / 2 + 8, cy + 20], radius=8,
                            fill=(255, 255, 255), outline=(15, 23, 42), width=2)
        d.text((cx, cy), name, fill=(15, 23, 42), font=font(20), anchor="mm")

    # 8) north arrow
    d.text((1480, 200), "N↑", fill=(22, 32, 51), font=font(34), anchor="mm")

    # 9) legend
    lx = 1360
    ly = 270
    leg = [
        ((79, 70, 229), "AI研发创新", "AI R&D"),
        ((21, 128, 61), "公园绿地", "Parks"),
        ((183, 121, 31), "产业服务", "Industry"),
        ((180, 35, 24), "社区服务", "Community"),
        ((15, 116, 144), "慢行/公共空间", "Mobility/Public"),
        ((15, 23, 42), "重点区域(临时)", "Key area (prov.)"),
        ((245, 158, 11), "一期范围", "Phase 1"),
    ]
    d.rounded_rectangle([lx - 10, ly - 30, 1560, ly + 40 * len(leg) + 10], radius=12,
                        fill=(255, 255, 255), outline=(215, 223, 235), width=2)
    for i, (col, zh, en) in enumerate(leg):
        yy = ly + i * 40
        d.rectangle([lx, yy, lx + 28, yy + 20], fill=col)
        d.text((lx + 38, yy), zh if lang == "zh" else en, fill=(22, 32, 51), font=font(20))

    foot = ("由同一组 GeoJSON 派生；临时边界以 intake 讨论为限，不作为正式专业评分图纸，待官方边界替换后重算。"
            if lang == "zh" else
            "Derived from the same GeoJSON; provisional boundary for intake only, not a formal scoring drawing; recalculate after official boundary replacement.")
    d.text((60, 930), foot, fill=(102, 112, 133), font=font(20))
    return img


def make_figure_implementation_roadmap(lang="zh"):
    """implementation-roadmap: JZ projects + phasing + annual activities (Item 4 visual)."""
    W, H = 1600, 1200
    img = Image.new("RGB", (W, H), (248, 250, 252))
    d = ImageDraw.Draw(img)

    # ---- title bar ----
    d.rectangle([0, 0, W, 72], fill=(15, 23, 42))
    title = "第4项 · 可实施性：JZ 项目 · 实施分期 · 年度活动" if lang == "zh" else \
            "Item 4 · Implementability: JZ Projects · Phasing · Annual Activities"
    d.text((50, 46), title, fill=(255, 255, 255), font=font(29), anchor="lm")
    sub = "JZ = 京张（JingZhang）。六项更新项目把「设计图」连接到「真能落地」。" if lang == "zh" else \
          "JZ = JingZhang. Six renewal projects connect the design with real delivery."
    d.text((50, 100), sub, fill=(100, 116, 139), font=font(21))

    # ---- palette ----
    phase_fill = {"green": (34, 197, 94), "blue": (37, 99, 235), "purple": (126, 34, 156)}
    phase_tint = {
        "green": ((220, 252, 231), (21, 128, 61)),
        "blue": ((219, 234, 254), (30, 64, 175)),
        "purple": ((243, 232, 255), (126, 34, 156)),
    }

    # ===================== ① JZ 项目清单 =====================
    d.text((50, 130), "① 更新项目清单（JZ-01 ~ JZ-06）" if lang == "zh" else
           "① Renewal Project List (JZ-01 ~ JZ-06)", fill=(15, 23, 42), font=font(26))

    jz = [
        ("01", "京张遗址公园慢行断点缝合", "公共空间/交通", "海淀区城管委 + 京张公园管理处 + 属地街道", "green"),
        ("02", "众智园清河创新界面", "蓝绿空间/产业展示", "众智园运营公司 + 海淀区水务局", "green"),
        ("03", "原点社区近校成果转化街", "城市更新/产业服务", "海淀区 + 高校技转办 + 属地街道", "blue"),
        ("04", "大钟寺站四象限步行连通", "轨道一体化/慢行", "京投 + 属地街道 + 市政单位", "blue"),
        ("05", "AI公共服务与端侧算力节点", "新基建/公共服务", "算力服务商(招引) + 场地物业 + 海淀区", "blue"),
        ("06", "全球AI活动周公共路线", "运营/品牌", "海淀区 + 合作机构", "green"),
    ] if lang == "zh" else [
        ("01", "Jingzhang Park slow-traffic mending", "Public space / transit", "UC Dist. + Park Mgmt + Subdist.", "green"),
        ("02", "Zhongzhiyuan Qinghe interface", "Blue-green / showcase", "Park operator + Water auth.", "green"),
        ("03", "Origin community conversion st.", "Urban renewal / service", "Haidian + Univ. TTO + Subdist.", "blue"),
        ("04", "Dazhongsi 4-quadrant walk link", "TOD / slow-traffic", "BII + Subdist. + Utility", "blue"),
        ("05", "AI public & edge-compute node", "New infra / public", "Compute vendor + Site + Haidian", "blue"),
        ("06", "Global AI Week public route", "Operation / brand", "Haidian + Partners", "green"),
    ]

    top = 160
    step = 64
    for i, (num, name, typ, resp, ph) in enumerate(jz):
        y = top + i * step
        d.rounded_rectangle([50, y, 1550, y + 58], radius=10,
                            fill=(255, 255, 255), outline=(226, 232, 240), width=2)
        # number badge (phase color)
        d.rounded_rectangle([62, y + 11, 116, y + 47], radius=8, fill=phase_fill[ph])
        d.text((89, y + 29), num, fill=(255, 255, 255), font=font(22), anchor="mm")
        # name + responsibility
        d.text((128, y + 14), name, fill=(17, 24, 39), font=font(21), anchor="lm")
        d.text((128, y + 42), resp, fill=(100, 116, 139), font=font(16), anchor="lm")
        # type pill
        tint, dark = phase_tint[ph]
        d.rounded_rectangle([1240, y + 15, 1540, y + 43], radius=14, fill=tint)
        d.text((1390, y + 29), typ, fill=dark, font=font(17), anchor="mm")

    # ===================== ② 实施分期 =====================
    d.text((50, 562), "② 实施分期（与 100 天征集周期严格区分）" if lang == "zh" else
           "② Implementation Phasing (distinct from 100-day intake)", fill=(15, 23, 42), font=font(26))

    phase = [
        ("近期 0–12 月", "轻量试点", "JZ-01 · JZ-02 · JZ-06", "不需控规调整，征集期后立即启动", "green"),
        ("中期 1–3 年", "主体更新", "JZ-03 · JZ-04 · JZ-05", "需官方控规/红线/市政/能源确认", "blue"),
        ("长期 3–10 年", "治理框架", "年度活动 · 招引转化链", "年度评估与策略迭代", "purple"),
    ] if lang == "zh" else [
        ("Near 0–12 mo", "Light pilot", "JZ-01 · 02 · 06", "No rezoning; start right after intake", "green"),
        ("Mid 1–3 yr", "Core renewal", "JZ-03 · 04 · 05", "Needs official zoning/redline/utilities", "blue"),
        ("Long 3–10 yr", "Governance", "Annual events · funnel", "Annual review & strategy iteration", "purple"),
    ]
    px = [50, 556, 1062]
    pw = 486
    py, ph_ = 588, 200
    for k, (head, tag, projs, cond, ph) in enumerate(phase):
        x = px[k]
        tint, dark = phase_tint[ph]
        d.rounded_rectangle([x, py, x + pw, py + ph_], radius=14, fill=tint, outline=phase_fill[ph], width=3)
        d.text((x + 24, 608), head, fill=dark, font=font(23), anchor="lm")
        d.text((x + 24, 638), tag, fill=(71, 85, 105), font=font(17), anchor="lm")
        d.text((x + 24, 676), projs, fill=(15, 23, 42), font=font(19), anchor="lm")
        d.text((x + 24, 712), cond, fill=(71, 85, 105), font=font(16), anchor="lm")
        # small footer line in card
        if k == 0:
            foot_line = "由属地街道 + 公园管理处牵头" if lang == "zh" else "led by subdistrict + park mgmt"
        elif k == 1:
            foot_line = "与官方控规/市政大修同步" if lang == "zh" else "with official zoning/utility works"
        else:
            foot_line = "海淀区年度复盘机制" if lang == "zh" else "Haidian annual review"
        d.text((x + 24, 752), foot_line, fill=(100, 116, 139), font=font(14), anchor="lm")

    # ===================== ③ 年度活动体系 =====================
    d.text((50, 814), "③ 年度活动体系（Q1–Q4 节奏）" if lang == "zh" else
           "③ Annual Activity System (Q1–Q4 cadence)", fill=(15, 23, 42), font=font(26))

    q = [
        ("Q1", "发布季", "场景 01 开源发布厅", "海淀区科委 + 高校开源联盟", "成果发布 → 媒体 → 高校PR"),
        ("Q2", "路演季", "场景 05 国际路演 + 场景 07 转化街", "物业 + 国际运营 + 高校技转", "路演 → 投融资 → 签约"),
        ("Q3", "测试季", "场景 02·03·08 产业测试验证", "评测机构 + 算力商 + 数据所", "评测 → 证书 → 算力 → 数据"),
        ("Q4", "活动周", "场景 10 全球AI活动周路线", "海淀区 + 合作机构", "导视 → 传播 → 国际邀约"),
    ] if lang == "zh" else [
        ("Q1", "Launch", "Scenario 01 open-release", "Haidian Sci-Tec + OSS alliance", "Release → media → PR"),
        ("Q2", "Roadshow", "Scn 05 · 07 conversion", "Property + intl ops + TTO", "Roadshow → funding → deal"),
        ("Q3", "Test", "Scn 02·03·08 industry test", "Evaluator + compute + exchange", "Eval → cert → compute → data"),
        ("Q4", "Festival", "Scn 10 Global AI Week route", "Haidian + Partners", "Signage → media → invite"),
    ]
    qx = [50, 430, 810, 1190]
    qw = 360
    qy, qh = 840, 240
    for k, (qid, theme, scenes, op, conv) in enumerate(q):
        x = qx[k]
        d.rounded_rectangle([x, qy, x + qw, qy + qh], radius=12,
                            fill=(255, 255, 255), outline=(203, 213, 225), width=2)
        d.rounded_rectangle([x + 20, qy + 18, x + 70, qy + 62], radius=10, fill=(15, 23, 42))
        d.text((x + 45, qy + 40), qid, fill=(255, 255, 255), font=font(20), anchor="mm")
        d.text((x + 82, qy + 40), theme, fill=(15, 23, 42), font=font(20), anchor="lm")
        d.text((x + 20, qy + 86), scenes, fill=(30, 41, 59), font=font(15), anchor="lm")
        d.text((x + 20, qy + 120), (op if lang == "zh" else op), fill=(100, 116, 139), font=font(14), anchor="lm")
        d.text((x + 20, qy + 158), conv, fill=(71, 85, 105), font=font(14), anchor="lm")
        d.text((x + 20, qy + 196), "不采集个人行为轨迹" if lang == "zh" else "no personal tracking",
               fill=(220, 38, 38), font=font(13), anchor="lm")

    # ===================== ④ 诚实风险管控原则 =====================
    d.rounded_rectangle([50, 1102, 1550, 1148], radius=12, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    honesty = ("诚实原则：无权属/资金/实施主体/审批路径 → 写为实施风险，而非承诺落地；每个项目含 阶段门槛 + 退出机制。"
               if lang == "zh" else
               "Honesty: no tenure/funding/owner/approval → state it as an implementation risk, not a delivery promise; "
               "each project carries a phase gate + exit plan.")
    d.text((800, 1125), honesty, fill=(146, 64, 14), font=font(16 if lang == "zh" else 13), anchor="mm")

    # ---- footer ----
    foot = ("数据源：proposal.md §更新项目清单/分期/年度活动 · geometry/phasing.geojson (PHASE-001) · 示意图 intake 用，非官方边界"
            if lang == "zh" else
            "Source: proposal.md §renewal/phasing/annual · geometry/phasing.geojson (PHASE-001) · schematic for intake, not official boundary")
    d.text((50, 1168), foot, fill=(100, 116, 139), font=font(15))

    return img


if __name__ == "__main__":
    FIGURES.mkdir(parents=True, exist_ok=True)
    makers = [
        ("site-overview", make_figure1),
        ("land-use-structure", make_figure2),
        ("key-areas", make_figure3),
        ("mobility-bluegreen", make_figure4),
        ("metrics-evidence", make_figure5),
        ("site-structure", make_figure_site_structure),
    ]
    for name, maker in makers:
        for lang, suffix in [("zh", ""), ("en", ".en")]:
            img = maker(lang)
            out = FIGURES / f"{name}{suffix}.png"
            img.save(out, "PNG")
            print(f"saved {out}")
