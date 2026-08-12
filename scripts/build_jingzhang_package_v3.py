# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A0, A3, landscape
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
SUB = ROOT / "submissions" / "CatNebulaaaa" / "grow-with-jingzhang"
FIG = SUB / "assets" / "figures"
DRAWINGS = SUB / "drawings"
VISUAL = SUB / "visual"
ASSETS = VISUAL / "assets"
W, H = 2480, 1754

PAPER = "#F2EFE7"
PANEL = "#FBFAF6"
INK = "#17324D"
MUTED = "#647382"
LINE = "#AAB5BD"
ORANGE = "#F15A3A"
GREEN = "#2F7D57"
BLUE = "#278CA8"
GOLD = "#D9B83F"
VIOLET = "#765A91"
RED = "#B74335"
PALE_GREEN = "#DCE9DF"
PALE_BLUE = "#D9EAF0"
PALE_ORANGE = "#F6DDD4"
PALE_GOLD = "#F0E8C7"
WHITE = "#FFFFFF"

FONT_REG = Path(r"C:\Windows\Fonts\Noto Sans SC (TrueType).otf")
FONT_MED = Path(r"C:\Windows\Fonts\Noto Sans SC Medium (TrueType).otf")
FONT_BOLD = Path(r"C:\Windows\Fonts\Noto Sans SC Bold (TrueType).otf")
if not FONT_REG.exists():
    FONT_REG = Path(r"C:\Windows\Fonts\msyh.ttc")
    FONT_MED = FONT_REG
    FONT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def fnt(size: int, bold: bool = False, medium: bool = False):
    path = FONT_BOLD if bold else FONT_MED if medium else FONT_REG
    return ImageFont.truetype(str(path), size=size)


def wrap(draw: ImageDraw.ImageDraw, text: str, font, width: int) -> list[str]:
    if not text:
        return []
    out, line = [], ""
    for paragraph in str(text).split("\n"):
        if not paragraph:
            out.append("")
            continue
        tokens = paragraph.split(" ") if " " in paragraph else list(paragraph)
        sep = " " if " " in paragraph else ""
        for token in tokens:
            trial = token if not line else line + sep + token
            if draw.textbbox((0, 0), trial, font=font)[2] <= width:
                line = trial
            else:
                if line:
                    out.append(line)
                line = token
        if line:
            out.append(line)
            line = ""
    return out


def text_block(draw, xy, text, size=26, color=INK, width=600, leading=None,
               bold=False, medium=False, max_lines=None):
    font = fnt(size, bold=bold, medium=medium)
    leading = leading or int(size * 1.42)
    lines = wrap(draw, text, font, width)
    if max_lines:
        lines = lines[:max_lines]
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font, fill=color)
        y += leading
    return y


def rounded(draw, box, fill=PANEL, outline=LINE, radius=16, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def line_label(draw, x, y, label, value, width=620, accent=ORANGE, lang="zh"):
    draw.line((x, y + 11, x + 34, y + 11), fill=accent, width=7)
    draw.text((x + 48, y), label, font=fnt(21, medium=True), fill=MUTED)
    text_block(draw, (x, y + 36), value, 29 if lang == "zh" else 25, INK, width, 40,
               medium=True, max_lines=3)


def page(code: str, title: str, subtitle: str, lang="zh"):
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 18), fill=INK)
    d.rectangle((0, 18, W, 28), fill=ORANGE)
    d.text((66, 66), code, font=fnt(24, bold=True), fill=ORANGE)
    d.text((66, 105), title, font=fnt(58 if lang == "zh" else 50, bold=True), fill=INK)
    d.text((66, 178), subtitle, font=fnt(24 if lang == "zh" else 21, medium=True), fill=MUTED)
    return im, d


def footer(draw, source: str, status: str, page_no: str, lang="zh"):
    y = H - 74
    draw.line((66, y - 20, W - 66, y - 20), fill=INK, width=2)
    draw.text((66, y), source, font=fnt(16), fill=MUTED)
    s = status
    sw = draw.textbbox((0, 0), s, font=fnt(16, medium=True))[2]
    draw.text((W - 120 - sw, y), s, font=fnt(16, medium=True), fill=ORANGE)
    draw.text((W - 84, y), page_no, font=fnt(16, bold=True), fill=INK)


def arrow(draw, a, b, color=INK, width=6, head=16):
    draw.line((*a, *b), fill=color, width=width)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    p1 = (b[0] - head * math.cos(ang - .55), b[1] - head * math.sin(ang - .55))
    p2 = (b[0] - head * math.cos(ang + .55), b[1] - head * math.sin(ang + .55))
    draw.polygon([b, p1, p2], fill=color)


def collect_coords(geom):
    typ = geom.get("type")
    coords = geom.get("coordinates", [])
    if typ == "Point":
        return [tuple(coords)]
    if typ in ("LineString", "MultiPoint"):
        return [tuple(p) for p in coords]
    if typ == "Polygon":
        return [tuple(p) for ring in coords for p in ring]
    if typ == "MultiLineString":
        return [tuple(p) for line in coords for p in line]
    if typ == "MultiPolygon":
        return [tuple(p) for poly in coords for ring in poly for p in ring]
    return []


def bbox_of(features):
    pts = [p for f in features for p in collect_coords(f["geometry"])]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def projector(bbox, box, pad=30):
    minx, miny, maxx, maxy = bbox
    x0, y0, x1, y1 = box
    sx = (x1 - x0 - 2 * pad) / max(maxx - minx, 1e-9)
    sy = (y1 - y0 - 2 * pad) / max(maxy - miny, 1e-9)
    scale = min(sx, sy)
    ox = x0 + (x1 - x0 - (maxx - minx) * scale) / 2
    oy = y0 + (y1 - y0 - (maxy - miny) * scale) / 2

    def p(pt):
        return (ox + (pt[0] - minx) * scale, y1 - (oy - y0) - (pt[1] - miny) * scale)
    return p


def geometry_paths(geom):
    typ, coords = geom.get("type"), geom.get("coordinates", [])
    if typ == "Point":
        return [[coords]]
    if typ == "LineString":
        return [coords]
    if typ == "MultiLineString":
        return coords
    if typ == "Polygon":
        return coords
    if typ == "MultiPolygon":
        return [ring for poly in coords for ring in poly]
    return []


def draw_layer(draw, features, proj, fill=None, outline=INK, width=3, point_r=8):
    for feat in features:
        typ = feat["geometry"]["type"]
        paths = geometry_paths(feat["geometry"])
        for path in paths:
            pts = [proj(tuple(p)) for p in path]
            if typ == "Point":
                x, y = pts[0]
                draw.ellipse((x - point_r, y - point_r, x + point_r, y + point_r),
                             fill=fill or outline, outline=outline, width=2)
            elif typ in ("Polygon", "MultiPolygon"):
                draw.polygon(pts, fill=fill, outline=outline)
                if width > 1:
                    draw.line(pts, fill=outline, width=width, joint="curve")
            else:
                draw.line(pts, fill=outline, width=width, joint="curve")


def layers():
    geo = SUB / "geometry"
    names = ["site_boundary", "land_use", "key_areas", "roads", "green_space",
             "public_space", "buildings"]
    return {n: load_json(geo / f"{n}.geojson")["features"] for n in names}


def draw_north_scale(draw, box, lang="zh"):
    x0, y0, x1, y1 = box
    x = x1 - 70
    draw.line((x, y0 + 90, x, y0 + 25), fill=INK, width=4)
    draw.polygon([(x, y0 + 10), (x - 10, y0 + 34), (x + 10, y0 + 34)], fill=INK)
    draw.text((x - 9, y0 - 16), "N", font=fnt(18, bold=True), fill=INK)
    draw.line((x0 + 28, y1 - 32, x0 + 180, y1 - 32), fill=INK, width=4)
    draw.line((x0 + 28, y1 - 40, x0 + 28, y1 - 24), fill=INK, width=3)
    draw.line((x0 + 180, y1 - 40, x0 + 180, y1 - 24), fill=INK, width=3)
    draw.text((x0 + 42, y1 - 64), "schematic scale" if lang == "en" else "示意比例尺",
              font=fnt(15), fill=MUTED)


def save_figure(name: str, lang: str, im: Image.Image):
    FIG.mkdir(parents=True, exist_ok=True)
    suffix = ".en.png" if lang == "en" else ".png"
    path = FIG / f"{name}{suffix}"
    for attempt in range(1, 5):
        try:
            im.save(path, "PNG", optimize=True)
            break
        except OSError:
            if attempt == 4:
                raise
            print(f"retrying locked output ({attempt}/3): {path.name}")
            time.sleep(0.4 * attempt)
    return path


def site_overview(lang="zh"):
    if lang == "zh":
        title, sub = "总体空间结构与公共服务契约", "一轴三片、两翼协同、多点支撑｜工作底图约 11.41 km²"
    else:
        title, sub = "Spatial Framework and Public-Service Contract", "One spine, three districts, two interfaces and twelve service nodes | 11.41 km² working base"
    im, d = page("01 / REVIEW GATE", title, sub, lang)
    L = layers(); map_box = (66, 270, 1570, 1620)
    rounded(d, map_box, fill="#E8E6DF", outline=INK, radius=12, width=3)
    proj = projector(bbox_of(L["site_boundary"]), map_box, 72)
    land_colors = ["#DCE5DE", "#E7E2D6", "#D5E4EA", "#EEE1D8", "#E8E0C9", "#DDE7D3"]
    for f, c in zip(L["land_use"], land_colors):
        draw_layer(d, [f], proj, fill=c, outline="#A9B1B6", width=2)
    draw_layer(d, L["green_space"], proj, fill="#BFD5C1", outline=GREEN, width=3)
    draw_layer(d, L["buildings"], proj, fill="#D0CBC0", outline="#7A858C", width=2)
    draw_layer(d, L["roads"], proj, outline=BLUE, width=7)
    draw_layer(d, L["site_boundary"], proj, outline=INK, width=5)
    draw_layer(d, L["key_areas"], proj, fill=None, outline=ORANGE, width=7)
    draw_layer(d, L["public_space"], proj, fill=ORANGE, outline=WHITE, width=2, point_r=11)
    draw_north_scale(d, map_box, lang)
    legend = [(GREEN, "蓝绿公共空间" if lang == "zh" else "blue-green commons"),
              (BLUE, "慢行主线" if lang == "zh" else "walk-cycle spine"),
              (ORANGE, "重点片区 / 服务节点" if lang == "zh" else "key districts / service nodes")]
    lx, ly = 100, 305
    for c, lab in legend:
        d.rectangle((lx, ly, lx + 28, ly + 12), fill=c)
        d.text((lx + 40, ly - 7), lab, font=fnt(17, medium=True), fill=INK)
        ly += 36

    x = 1620
    rounded(d, (x, 270, W - 66, 595), fill=PANEL, outline=INK, radius=12, width=3)
    d.text((x + 30, 300), "8-80 同等服务契约" if lang == "zh" else "8-80 equal-service contract",
           font=fnt(29 if lang == "zh" else 27, bold=True), fill=INK)
    contract = [
        ("01", "无需账户、手机或人脸" if lang == "zh" else "No account, phone or face required"),
        ("02", "人工或非数字路径同等可达" if lang == "zh" else "Equivalent human or non-digital path"),
        ("03", "责任主体、接管和退出公开" if lang == "zh" else "Named owner, takeover and exit"),
        ("04", "失败时基本公共服务连续" if lang == "zh" else "Basic public service continues on failure"),
    ]
    yy = 360
    for no, lab in contract:
        d.text((x + 30, yy), no, font=fnt(18, bold=True), fill=ORANGE)
        d.text((x + 86, yy - 3), lab, font=fnt(22 if lang == "zh" else 19, medium=True), fill=INK)
        d.line((x + 30, yy + 36, W - 98, yy + 36), fill="#D5D9DA", width=1)
        yy += 52

    rounded(d, (x, 625, W - 66, 1022), fill=PANEL, outline=LINE, radius=12, width=2)
    line_label(d, x + 30, 655, "空间范围" if lang == "zh" else "WORKING EXTENT", "工作底图复算 11.4128 km²；正式边界待主管部门确认" if lang == "zh" else "11.4128 km² recalculated from the working base; official boundary pending", 700, BLUE, lang)
    line_label(d, x + 30, 780, "首期动作" if lang == "zh" else "FIRST MOVES", "1 km 示范段、3 处服务节点、3000 m² 共享首层、1.5 ha 受控验证场" if lang == "zh" else "1 km pilot, 3 service nodes, 3,000 m² shared ground floor and 1.5 ha controlled test field", 700, GREEN, lang)
    line_label(d, x + 30, 920, "审查边界" if lang == "zh" else "REVIEW BOUNDARY", "红线、权属、轨道、消防、市政和现场条件均列为实施前置" if lang == "zh" else "Redline, tenure, rail, fire, utilities and site conditions remain preconditions", 700, ORANGE, lang)

    rounded(d, (x, 1052, W - 66, 1620), fill=INK, outline=INK, radius=12, width=2)
    d.text((x + 30, 1084), "五级决策关口" if lang == "zh" else "FIVE DECISION GATES", font=fnt(24, bold=True), fill=WHITE)
    gates = [
        ("G0", "资料归集" if lang == "zh" else "evidence lock"),
        ("G1", "可行协商" if lang == "zh" else "feasibility"),
        ("G2", "专项审查" if lang == "zh" else "specialist review"),
        ("G3", "验收开放" if lang == "zh" else "accept & open"),
        ("G4", "年度复审" if lang == "zh" else "annual review"),
    ]
    yy = 1150
    for i, (g, lab) in enumerate(gates):
        d.ellipse((x + 30, yy, x + 82, yy + 52), fill=[GREEN, BLUE, GOLD, ORANGE, VIOLET][i])
        d.text((x + 41, yy + 13), g, font=fnt(16, bold=True), fill=WHITE)
        d.text((x + 105, yy + 10), lab, font=fnt(22 if lang == "zh" else 19, medium=True), fill=WHITE)
        if i < 4:
            d.line((x + 56, yy + 52, x + 56, yy + 75), fill="#AFC0CE", width=3)
        yy += 86
    footer(d, "geometry/*.geojson · spatial.json · implementation-operation-contract.json",
           "公开事实 / 复算值 / 建议目标分列" if lang == "zh" else "facts / recalculations / targets separated", "01", lang)
    return im


def land_use_structure(lang="zh"):
    title = "用地结构与复合功能组织" if lang == "zh" else "Land-use Structure and Mixed-use Logic"
    sub = "六类方案分区覆盖工作底图｜法定用地性质与比例由控规确定" if lang == "zh" else "Six concept zones cover the working base | statutory classifications follow regulatory planning"
    im, d = page("02 / SPATIAL LEDGER", title, sub, lang)
    L = layers(); box = (66, 270, 1530, 1460)
    rounded(d, box, fill="#E9E7E0", outline=INK, radius=12, width=3)
    proj = projector(bbox_of(L["site_boundary"]), box, 70)
    colors = [GREEN, GOLD, BLUE, ORANGE, VIOLET, "#6D9F76"]
    for f, c in zip(L["land_use"], colors):
        draw_layer(d, [f], proj, fill=c + "55", outline=c, width=4)
    draw_layer(d, L["roads"], proj, outline=INK, width=5)
    draw_layer(d, L["site_boundary"], proj, outline=INK, width=5)
    draw_layer(d, L["key_areas"], proj, outline=WHITE, width=7)
    draw_north_scale(d, box, lang)
    total = sum(float(f["properties"].get("area_sqm_declared", 0)) for f in L["land_use"])
    x = 1580
    d.text((x, 270), "方案土地平衡" if lang == "zh" else "CONCEPT LAND BALANCE", font=fnt(26, bold=True), fill=INK)
    names_en = ["R&D + responsible trials", "talent housing + care", "co-learning + transfer", "culture + civic service", "AI daily services + commerce", "blue-green resilience"]
    yy = 330
    for i, feat in enumerate(L["land_use"]):
        p = feat["properties"]; area = float(p.get("area_sqm_declared", 0)); ratio = area / total
        name = p.get("name_zh") if lang == "zh" else names_en[i]
        d.text((x, yy), f"{p.get('id')}  {name}", font=fnt(20 if lang == "zh" else 18, medium=True), fill=INK)
        d.text((W - 215, yy), f"{area/10000:.1f} ha", font=fnt(18, bold=True), fill=colors[i])
        d.rectangle((x, yy + 35, W - 90, yy + 52), fill="#D8DBD8")
        d.rectangle((x, yy + 35, x + int((W - 90 - x) * ratio / .22), yy + 52), fill=colors[i])
        yy += 122
    rounded(d, (x, 1095, W - 66, 1460), fill=PANEL, outline=LINE, radius=12, width=2)
    d.text((x + 28, 1125), "分类使用规则" if lang == "zh" else "HOW TO READ THIS LAYER", font=fnt(23, bold=True), fill=INK)
    rules = [
        "用地代码记录主导功能，用于方案数据交换。" if lang == "zh" else "Codes record dominant concept functions for data exchange.",
        "六个多边形组成完整分区，不留空白、不相互重叠。" if lang == "zh" else "Six polygons form a complete, non-overlapping partition.",
        "建筑规模、兼容比例和开发强度保持未知，待法定规划确定。" if lang == "zh" else "Floor area, compatibility ratios and intensity remain unknown pending statutory planning.",
        "首期项目以存量微改造和可逆设施为主。" if lang == "zh" else "First moves prioritize adaptive reuse and reversible facilities.",
    ]
    yy = 1180
    for i, r in enumerate(rules, 1):
        d.text((x + 28, yy), f"{i:02d}", font=fnt(17, bold=True), fill=ORANGE)
        text_block(d, (x + 78, yy - 3), r, 19 if lang == "zh" else 17, INK, 690, 30, max_lines=2)
        yy += 66
    footer(d, "geometry/land_use.geojson · metrics.json · MNR land-use classification guide",
           "方案分区，非控规用地" if lang == "zh" else "concept zones, not statutory land use", "02", lang)
    return im


def key_areas(lang="zh"):
    title = "三处重点片区：空间账本与首期入口" if lang == "zh" else "Three Key Districts: Spatial Ledgers and First Moves"
    sub = "公告面积、工作底图复算、项目预算、开放条件和未知项同图表达" if lang == "zh" else "Published areas, recalculations, program budgets, gates and unknowns on one sheet"
    im, d = page("03 / KEY DISTRICTS", title, sub, lang)
    sp = load_json(SUB / "spatial.json")
    colors = [GREEN, BLUE, ORANGE]
    cards = [(66, 270, 814, 1605), (866, 270, 1614, 1605), (1666, 270, 2414, 1605)]
    names_en = ["Zhongzhiyuan Innovation Validation District", "Beijing AI Origin Collaborative Innovation District", "Dazhongsi Station-City Integration District"]
    roles_zh = ["受控测试、公众审议、设施运维", "学习协作、开源发布、人才与家庭服务", "四向接驳、人工服务、多语言导向"]
    roles_en = ["controlled tests, public review and maintenance", "learning, open release, talent and family support", "four-way access, human service and multilingual wayfinding"]
    for i, (box, area) in enumerate(zip(cards, sp["key_areas"])):
        x0, y0, x1, y1 = box; c = colors[i]
        rounded(d, box, fill=PANEL, outline=c, radius=14, width=5)
        d.rectangle((x0, y0, x0 + 14, y1), fill=c)
        d.text((x0 + 34, y0 + 30), ["P-03", "P-04", "P-02"][i], font=fnt(20, bold=True), fill=c)
        name = area["name_zh"] if lang == "zh" else names_en[i]
        yy = text_block(d, (x0 + 34, y0 + 72), name, 31 if lang == "zh" else 25, INK, x1 - x0 - 68, 39, bold=True, max_lines=3)
        role = roles_zh[i] if lang == "zh" else roles_en[i]
        yy = text_block(d, (x0 + 34, yy + 12), role, 20 if lang == "zh" else 17, MUTED, x1 - x0 - 68, 30, max_lines=2)
        d.line((x0 + 34, yy + 16, x1 - 34, yy + 16), fill=LINE, width=2)
        yy += 46
        announced = area["announced_area_sqm"] / 10000
        calc = area["calculated_provisional_area_sqm"] / 10000
        d.text((x0 + 34, yy), "公告面积" if lang == "zh" else "PUBLISHED AREA", font=fnt(17, medium=True), fill=MUTED)
        d.text((x0 + 34, yy + 30), f"{announced:.1f} ha", font=fnt(34, bold=True), fill=INK)
        d.text((x0 + 332, yy), "底图复算" if lang == "zh" else "RECALCULATED", font=fnt(17, medium=True), fill=MUTED)
        d.text((x0 + 332, yy + 30), f"{calc:.1f} ha", font=fnt(34, bold=True), fill=c)
        yy += 105
        first = area["first_action"]
        first_name = first.get("name_zh") if lang == "zh" else ["controlled validation field", "shared ground-floor program", "station-city public hall interface"][i]
        rounded(d, (x0 + 30, yy, x1 - 30, yy + 126), fill=[PALE_GREEN, PALE_BLUE, PALE_ORANGE][i], outline=c, radius=10, width=2)
        d.text((x0 + 50, yy + 18), "首期入口" if lang == "zh" else "FIRST MOVE", font=fnt(17, bold=True), fill=c)
        text_block(d, (x0 + 50, yy + 51), first_name, 24 if lang == "zh" else 20, INK, x1 - x0 - 100, 31, medium=True, max_lines=2)
        yy += 156
        d.text((x0 + 34, yy), "空间预算 / 交付承诺" if lang == "zh" else "PROGRAM BUDGET / COMMITMENTS", font=fnt(19, bold=True), fill=INK)
        yy += 40
        items = area.get("pilot_area_budget_sqm") or area.get("shared_floor_program_sqm") or area.get("service_commitments")
        total_value = sum(float(v.get("value", 0)) for v in items)
        for item in items:
            lab = item["item"] if lang == "zh" else {
                "受控测试与安全缓冲":"controlled test + buffer", "公众审议与信息公示":"public review + notice", "设施运维实训":"maintenance training", "雨水花园和生态缓冲":"rain garden + eco buffer", "全龄测试环、消防及后勤通道":"8-80 loop + fire/logistics",
                "学习与议事空间":"learning + assembly", "开源发布与短期展陈":"open release + display", "人工人才服务和家庭支持":"human talent/family service", "共享工作与小型原型空间":"shared work + prototypes", "后勤、无障碍及消防调整预留":"support + access/fire reserve",
                "四向步行联系":"four approaches", "人工服务点":"human service nodes", "连续示范慢行":"continuous pilot", "双向骑行净宽建议":"two-way cycle width"
            }.get(item["item"], item["item"])
            val = float(item.get("value", 0)); unit = item.get("unit", "sqm")
            d.text((x0 + 34, yy), lab, font=fnt(17 if lang == "zh" else 15, medium=True), fill=INK)
            label_val = f"{val:g} {unit}"
            tw = d.textbbox((0, 0), label_val, font=fnt(16, bold=True))[2]
            d.text((x1 - 34 - tw, yy), label_val, font=fnt(16, bold=True), fill=c)
            d.line((x0 + 34, yy + 29, x1 - 34, yy + 29), fill="#D8DDDE", width=5)
            frac = val / total_value if total_value and unit == "sqm" else min(val / max(val, 4), 1)
            d.line((x0 + 34, yy + 29, x0 + 34 + (x1 - x0 - 68) * frac, yy + 29), fill=c, width=5)
            yy += 58
        yy += 10
        d.text((x0 + 34, yy), "开放条件" if lang == "zh" else "OPENING GATES", font=fnt(19, bold=True), fill=INK)
        yy += 38
        gates = area["open_gates"]
        for j, gate in enumerate(gates):
            gate_en = [
                ["tenure + permit", "traffic + fire", "ethics + data", "independent admission"],
                ["tenure + lease", "structure + fire", "operations agreement", "hours + fee notice"],
                ["flow + evacuation", "rail safety", "fire review", "tenure + commerce"]
            ][i][j]
            d.ellipse((x0 + 36, yy + 4, x0 + 48, yy + 16), fill=c)
            d.text((x0 + 60, yy), gate if lang == "zh" else gate_en, font=fnt(17 if lang == "zh" else 15), fill=INK)
            yy += 34
        yy += 12
        d.text((x0 + 34, yy), "空间界面" if lang == "zh" else "SPATIAL INTERFACES", font=fnt(18, bold=True), fill=INK)
        yy += 34
        interface_text = "；".join(area["interfaces"])
        if lang == "en":
            interface_text = [
                "rail-safety edge; 8-80 test loop; human stop point; public-review entry",
                "campus-community co-test; shared entrances; evening boundary; human-service desk",
                "station flow; rail safety; multilingual wayfinding; night stay and human service",
            ][i]
        yy = text_block(d, (x0 + 34, yy), interface_text, 16 if lang == "zh" else 14, MUTED,
                        x1 - x0 - 68, 24, max_lines=4)
        yy += 12
        d.text((x0 + 34, yy), "拆改留策略" if lang == "zh" else "RETAIN / ADAPT / ADD", font=fnt(18, bold=True), fill=INK)
        yy += 34
        rr = area["retain_renovate_remove"]
        strategy = f"改造：{rr['renovate']}；新增：{rr['new']}" if lang == "zh" else [
            "Adapt verified existing space; add demountable test facilities only.",
            "Light ground-floor adaptation; add demountable service elements after review.",
            "Retain transport continuity; renew wayfinding, paving, lighting and frontage first.",
        ][i]
        text_block(d, (x0 + 34, yy), strategy, 15 if lang == "zh" else 14, INK,
                   x1 - x0 - 68, 23, max_lines=4)
        d.text((x0 + 34, y1 - 90), "边界状态" if lang == "zh" else "BOUNDARY STATUS", font=fnt(15, bold=True), fill=ORANGE)
        text_block(d, (x0 + 34, y1 - 61), "方案研究示意范围，非地块、道路红线或权属边界" if lang == "zh" else "provisional study extent; not parcel, road or tenure boundary", 15, MUTED, x1 - x0 - 68, 22, max_lines=2)
    footer(d, "spatial.json · geometry/key_areas.geojson · official announcement area facts",
           "首期动作均须通过专项审查" if lang == "zh" else "all first moves remain subject to specialist review", "03", lang)
    return im


def mobility_bluegreen(lang="zh"):
    title = "慢行、蓝绿与气候适应一体化设计" if lang == "zh" else "Integrated Mobility, Blue-green and Climate Adaptation"
    sub = "走廊网络、典型断面、气候基线和验收方法同图校核" if lang == "zh" else "Corridor network, typical section, climate baseline and acceptance methods"
    im, d = page("04 / MOBILITY + CLIMATE", title, sub, lang)
    L = layers(); box = (66, 270, 1440, 1065)
    rounded(d, box, fill="#E7ECE8", outline=INK, radius=12, width=3)
    proj = projector(bbox_of(L["site_boundary"]), box, 60)
    draw_layer(d, L["land_use"], proj, fill="#E6E3DA", outline="#C7CBC9", width=2)
    draw_layer(d, L["green_space"], proj, fill="#C4D9C5", outline=GREEN, width=4)
    draw_layer(d, L["roads"], proj, outline=BLUE, width=9)
    draw_layer(d, L["public_space"], proj, fill=ORANGE, outline=WHITE, width=2, point_r=11)
    draw_layer(d, L["site_boundary"], proj, outline=INK, width=4)
    draw_north_scale(d, box, lang)
    x = 1490
    rounded(d, (x, 270, W - 66, 1065), fill=PANEL, outline=LINE, radius=12, width=2)
    d.text((x + 28, 302), "十年气候基线" if lang == "zh" else "TEN-YEAR CLIMATE BASELINE", font=fnt(24, bold=True), fill=INK)
    climate = [
        ("35.58°C", "日最高温 P95" if lang == "zh" else "daily Tmax P95", ORANGE),
        ("22.3 d/y", "年均 ≥35°C 日数" if lang == "zh" else "annual days ≥35°C", RED),
        ("649.1 mm", "年均降水" if lang == "zh" else "annual precipitation", BLUE),
        ("4.05", "kWh/m²/日太阳辐射" if lang == "zh" else "kWh/m²/day solar", GOLD),
    ]
    yy = 365
    for val, lab, c in climate:
        d.text((x + 28, yy), val, font=fnt(37, bold=True), fill=c)
        d.text((x + 280, yy + 8), lab, font=fnt(19, medium=True), fill=INK)
        d.line((x + 28, yy + 55, W - 96, yy + 55), fill="#D8DDDE", width=1)
        yy += 84
    d.text((x + 28, yy + 10), "设计响应" if lang == "zh" else "DESIGN RESPONSES", font=fnt(22, bold=True), fill=INK)
    responses = [
        "连续遮阴与可坐靠休憩点" if lang == "zh" else "continuous shade and supportive seating",
        "雨水花园、溢流口和检修路径" if lang == "zh" else "rain gardens, overflow and maintenance access",
        "冬季向阳避风与夜间照明" if lang == "zh" else "winter sun, wind shelter and night lighting",
        "断网、停电时保留实体导向" if lang == "zh" else "physical wayfinding during network/power loss",
    ]
    yy += 58
    for i, r in enumerate(responses):
        d.text((x + 28, yy), f"{i+1:02d}", font=fnt(17, bold=True), fill=[GREEN, BLUE, GOLD, ORANGE][i])
        d.text((x + 75, yy - 2), r, font=fnt(19 if lang == "zh" else 17, medium=True), fill=INK)
        yy += 55

    sec = (66, 1110, W - 66, 1605); rounded(d, sec, fill=PANEL, outline=INK, radius=12, width=3)
    x0, y0, x1, y1 = sec; ground = y0 + 330
    d.line((x0 + 40, ground, x1 - 40, ground), fill=INK, width=5)
    parts = [(3.0, "连续步行" if lang == "zh" else "walk", "#D9D4C5"), (2.5, "雨水花园" if lang == "zh" else "rain garden", PALE_GREEN), (4.0, "双向骑行" if lang == "zh" else "two-way cycle", PALE_BLUE), (2.5, "服务停留" if lang == "zh" else "service bay", PALE_ORANGE)]
    sx = x0 + 70; usable = x1 - x0 - 140; total = sum(v for v, _, _ in parts)
    for value, lab, c in parts:
        ww = usable * value / total
        d.rectangle((sx, y0 + 105, sx + ww, ground), fill=c, outline=INK, width=3)
        d.text((sx + 18, y0 + 180), lab, font=fnt(22 if lang == "zh" else 18, bold=True), fill=INK)
        d.line((sx, ground + 55, sx + ww, ground + 55), fill=INK, width=2)
        d.line((sx, ground + 43, sx, ground + 67), fill=INK, width=2)
        d.line((sx + ww, ground + 43, sx + ww, ground + 67), fill=INK, width=2)
        val = f"{value:.1f} m"; tw = d.textbbox((0,0), val, font=fnt(18,bold=True))[2]
        d.rectangle((sx + ww/2 - tw/2 - 8, ground + 42, sx + ww/2 + tw/2 + 8, ground + 69), fill=PANEL)
        d.text((sx + ww/2 - tw/2, ground + 43), val, font=fnt(18,bold=True), fill=INK)
        sx += ww
    for tx in [x0 + 460, x0 + 1640]:
        d.line((tx, y0 + 92, tx, ground - 8), fill="#6C513B", width=10)
        d.ellipse((tx - 70, y0 + 45, tx + 70, y0 + 190), fill="#7FA278", outline=GREEN, width=3)
    footer(d, "geometry/roads.geojson · geometry/green_space.geojson · NASA POWER 2015-2024",
           "断面宽度为建议值，须经专项设计" if lang == "zh" else "section widths are proposed and require specialist design", "04", lang)
    return im


def metrics_evidence(lang="zh"):
    title = "指标证据表：基线、目标、状态与责任" if lang == "zh" else "Metric Evidence: Baseline, Target, Status and Accountability"
    sub = "建议目标不以完成态表达｜每项指标绑定测量方法与责任主体" if lang == "zh" else "Proposed targets are not shown as achieved | every metric has a method and owner"
    im, d = page("05 / METRIC EVIDENCE", title, sub, lang)
    x0, y0, x1, y1 = 66, 275, W - 66, 1588
    rounded(d, (x0, y0, x1, y1), fill=PANEL, outline=INK, radius=10, width=3)
    cols = [x0, x0+470, x0+770, x0+1040, x0+1370, x0+1900, x1]
    heads_zh = ["指标", "基线/复算", "建议目标", "当前状态", "测量方法", "责任主体"]
    heads_en = ["METRIC", "BASE / RECALC", "PROPOSED TARGET", "CURRENT STATUS", "MEASUREMENT", "OWNER"]
    heads = heads_zh if lang == "zh" else heads_en
    d.rectangle((x0, y0, x1, y0+78), fill=INK)
    for i, h in enumerate(heads):
        d.text((cols[i]+16, y0+25), h, font=fnt(18 if lang=="zh" else 15, bold=True), fill=WHITE)
    rows_zh = [
        ("总体设计范围", "11.4128 km²", "—", "工作底图复算", "EPSG:4548 面积复算", "规划技术/主管部门"),
        ("蓝绿空间比例", "18.95%", "专项校准", "概念方案复算", "图层并集/范围面积", "景观与规划"),
        ("连续步行净宽", "未调查", "≥3.0 m", "建议值，未实施", "最窄点逐段实测", "建设/无障碍验收"),
        ("双向骑行净宽", "未调查", "≥4.0 m", "建议值，未实施", "施工图+建成实测", "交通设计/建设"),
        ("有效休憩点间距", "未调查", "≤150 m", "建议值，未实施", "沿连续路径量测", "街道/园林运营"),
        ("主要停留空间遮阴", "未调查", "≥70%", "建议目标，未实施", "设计时段日照分析", "景观设计/运营"),
        ("人工服务可用率", "未运行", "100%", "运营目标，未实施", "公布时段月度抽测", "运营单位/街道"),
        ("协议有效场景", "12/12", "12/12", "桌面校验通过", "八条准入规则逐项检查", "方案技术团队"),
        ("负向测试拦截", "8/8", "8/8", "桌面变异测试通过", "注入缺陷并核对规则", "方案技术团队"),
    ]
    rows_en = [
        ("Design extent", "11.4128 km²", "—", "working-base recalc", "EPSG:4548 area", "planning / authority"),
        ("Blue-green ratio", "18.95%", "specialist calibration", "concept recalc", "union area / extent", "landscape + planning"),
        ("Clear walk width", "not surveyed", "≥3.0 m", "unbuilt target", "segment minimum", "client + access review"),
        ("Two-way cycle width", "not surveyed", "≥4.0 m", "unbuilt target", "drawing + as-built", "transport + client"),
        ("Rest-point spacing", "not surveyed", "≤150 m", "unbuilt target", "route measurement", "street + landscape ops"),
        ("Shade at stay spaces", "not surveyed", "≥70%", "unbuilt target", "design-hour solar test", "landscape + operator"),
        ("Human service uptime", "not operated", "100%", "unbuilt service target", "monthly spot tests", "operator + subdistrict"),
        ("Valid protocol services", "12/12", "12/12", "tabletop passed", "eight-rule validation", "design tech team"),
        ("Negative tests caught", "8/8", "8/8", "mutation tests passed", "inject + expected rule", "design tech team"),
    ]
    rows = rows_zh if lang == "zh" else rows_en
    rh = 134
    for r, row in enumerate(rows):
        yy = y0 + 78 + r*rh
        if r % 2 == 0: d.rectangle((x0, yy, x1, yy+rh), fill="#F3F2ED")
        for cx in cols[1:-1]: d.line((cx, yy, cx, yy+rh), fill="#D3D8D9", width=1)
        status_color = GREEN if r >= 7 else BLUE if r < 2 else ORANGE
        for i, val in enumerate(row):
            c = status_color if i == 3 else INK
            text_block(d, (cols[i]+16, yy+24), val, 18 if lang=="zh" else 15, c,
                       cols[i+1]-cols[i]-30, 28, medium=(i in (0,3)), max_lines=3)
        d.line((x0, yy+rh, x1, yy+rh), fill="#C8CFD2", width=1)
    d.text((x0+18, y1-46), "— 表示该指标不设方案目标；‘未调查’和‘未运行’保持为未知，不以零值替代。" if lang=="zh" else "— means no scheme target. Unknown surveys and unoperated services remain unknown rather than zero.", font=fnt(17 if lang=="zh" else 15, medium=True), fill=MUTED)
    footer(d, "metrics.json · growth-tabletop-evidence.json · spatial.json",
           "2 项复算证据 / 5 项建议目标 / 2 项桌面验证" if lang=="zh" else "2 recalculations / 5 targets / 2 tabletop results", "05", lang)
    return im


def implementation_protocol(lang="zh"):
    title = "实施协议、负向测试与退出条件" if lang == "zh" else "Implementation Protocol, Negative Tests and Exit Conditions"
    sub = "十二项服务通过八条准入规则｜八类缺陷均被预期规则拦截" if lang == "zh" else "Twelve services pass eight admission rules | eight defects rejected by the expected rules"
    im, d = page("06 / PROTOCOL TABLETOP", title, sub, lang)
    ev = load_json(ASSETS / "growth-tabletop-evidence.json")
    x0, y0, x1 = 66, 280, W-66
    d.text((x0, y0), "决策关口" if lang=="zh" else "DECISION GATES", font=fnt(24,bold=True), fill=INK)
    gates = [("G0", "资料锁定" if lang=="zh" else "evidence lock"), ("G1", "共同协商" if lang=="zh" else "co-negotiate"), ("G2", "专项审查" if lang=="zh" else "specialist review"), ("G3", "验收开放" if lang=="zh" else "accept + open"), ("G4", "年度复审" if lang=="zh" else "annual decision")]
    gx = x0
    for i,(g,lab) in enumerate(gates):
        c=[GREEN,BLUE,GOLD,ORANGE,VIOLET][i]
        d.ellipse((gx, y0+58, gx+92, y0+150), fill=c)
        d.text((gx+23,y0+88),g,font=fnt(23,bold=True),fill=WHITE)
        d.text((gx-8,y0+168),lab,font=fnt(19 if lang=="zh" else 16,medium=True),fill=INK)
        if i<4: arrow(d,(gx+112,y0+104),(gx+430,y0+104),INK,4,14)
        gx += 470
    d.text((x0, 560), "八条准入规则" if lang=="zh" else "EIGHT ADMISSION RULES", font=fnt(24,bold=True), fill=INK)
    rules_zh=["责任主体","同等服务","最少数据","禁用生物识别","人工接管","停止权限","公开告知","证据回执"]
    rules_en=["named owner","equal service","minimum data","no biometrics","human takeover","stop authority","public notice","evidence receipt"]
    for i,lab in enumerate(rules_zh if lang=="zh" else rules_en):
        cx=x0+(i%4)*585; cy=620+(i//4)*130
        rounded(d,(cx,cy,cx+540,cy+96),fill=PANEL,outline=[GREEN,BLUE,GOLD,ORANGE][i%4],radius=10,width=3)
        d.text((cx+18,cy+18),f"R{i+1}",font=fnt(18,bold=True),fill=[GREEN,BLUE,GOLD,ORANGE][i%4])
        d.text((cx+72,cy+17),lab,font=fnt(23 if lang=="zh" else 20,medium=True),fill=INK)
        d.text((cx+72,cy+54),"缺失即拒绝" if lang=="zh" else "missing = reject",font=fnt(16),fill=MUTED)
    rounded(d,(x0,910,x1,1520),fill=INK,outline=INK,radius=12,width=2)
    d.text((x0+30,942),"桌面验证结果" if lang=="zh" else "TABLETOP EVIDENCE",font=fnt(25,bold=True),fill=WHITE)
    stats=[(f"{ev['services_passed']}/{ev['services_total']}","有效服务通过" if lang=="zh" else "valid services passed",GREEN),(f"{ev['negative_cases_caught']}/{ev['negative_cases_total']}","负向样例拦截" if lang=="zh" else "negative cases caught",ORANGE),(str(len(ev['dead_rules'])),"失效规则" if lang=="zh" else "dead rules",BLUE)]
    sx=x0+30
    for val,lab,c in stats:
        d.text((sx,1005),val,font=fnt(48,bold=True),fill=c)
        d.text((sx,1065),lab,font=fnt(19,medium=True),fill=WHITE)
        sx+=390
    d.text((x0+30,1140),"负向测试 X01-X08" if lang=="zh" else "NEGATIVE TESTS X01-X08",font=fnt(20,bold=True),fill="#BFCAD2")
    for i,res in enumerate(ev["mutation_results"]):
        xx=x0+30+(i%4)*575; yy=1190+(i//4)*120
        c=[GREEN,BLUE,GOLD,ORANGE][i%4]
        d.ellipse((xx,yy,xx+52,yy+52),fill=c)
        d.text((xx+8,yy+14),res['case_id'],font=fnt(14,bold=True),fill=WHITE)
        d.text((xx+70,yy+4),res['must_violate'],font=fnt(17,bold=True),fill=WHITE)
        d.text((xx+70,yy+33),"由预期规则拦截" if lang=="zh" else "caught by expected rule",font=fnt(15),fill="#C8D1D7")
    note="验证仅证明字段和拦截规则可复算；不证明项目获批、场地安全、服务质量或公众接受度。" if lang=="zh" else "This proves reproducible fields and rejection rules only; it does not prove approval, site safety, service quality or public acceptance."
    text_block(d,(x0+30,1430),note,18 if lang=="zh" else 16,"#D7DEE3",x1-x0-60,28,max_lines=2)
    footer(d,"growth-protocol.schema.json · growth-runbook.json · growth-tabletop-evidence.json","TABLETOP ONLY / NOT AUTHORIZED","06",lang)
    return im


def inclusion_incidence(lang="zh"):
    title = "公共利益与包容性影响台账" if lang=="zh" else "Public-interest and Inclusion Incidence Ledger"
    sub = "九类人群的受益、负担、盲区、所需输入和程序性权利逐项登记" if lang=="zh" else "Benefits, burdens, blind spots, required inputs and procedural standing for nine groups"
    im,d=page("07 / INCLUSION LEDGER",title,sub,lang)
    data=load_json(ASSETS/"inclusion-ledger.json"); groups=data.get("groups",data.get("entries",[]))
    x0,y0,x1,y1=66,280,W-66,1590
    cols=[x0,x0+420,x0+820,x0+1235,x0+1650,x0+2050,x1]
    heads=(['人群','主要受益','潜在负担','现有盲区','实施前输入','程序性权利'] if lang=='zh' else ['GROUP','BENEFIT','BURDEN','BLIND SPOT','INPUT BEFORE ACTION','PROCEDURAL STANDING'])
    d.rectangle((x0,y0,x1,y0+74),fill=INK)
    for i,h in enumerate(heads): d.text((cols[i]+12,y0+23),h,font=fnt(17 if lang=='zh' else 13,bold=True),fill=WHITE)
    translations=["children + families","older people + carers","disabled people","long-term residents","renters + small businesses","students + young talent","commuters + visitors","frontline workers","nearby institutions"]
    english_rows = {
        "children_families": ["safe routes + human AI-literacy service", "detours, noise + attention burden", "independent travel and peak paths unknown", "guardian/school co-test + after-school audit", "representative may stop unsafe tests"],
        "older_people_caregivers": ["supportive rest points + account-free help", "interface change + service downtime", "care chains and winter use unknown", "walking-time, seating + wayfinding co-test", "may require an equivalent human process"],
        "disabled_users": ["continuous accessible route + human help", "works may sever routes; digital exclusion", "barriers and task completion unknown", "access adviser + multi-user task tests", "may block acceptance while barriers remain"],
        "long_term_residents": ["daily services + deliberation channel", "works, detours, noise + activity pressure", "affected homes and tenure duration unknown", "authorized aggregate data + night survey", "may require reversible trials before impact is known"],
        "renters_small_business": ["shared ground floor + low-cost interface", "rent, footfall + construction loss", "lease term and business impact unknown", "anonymous lease/business survey + mitigation", "may object before permanent adaptation"],
        "students_young_talent": ["learning, work + open-release space", "hours may misalign; events may replace service", "affordability and night demand unknown", "campus/community survey + fee co-test", "may challenge fees, hours and data barriers"],
        "commuters_visitors": ["four-way access + multilingual wayfinding", "longer transfers + event crowding", "time-based flow and language demand unknown", "transport survey + arrival-task test", "may report faults and stop unsafe events"],
        "frontline_workers": ["clear takeover authority + maintainable kit", "extra staffing, records + failure pressure", "shift load, budget and spares unknown", "staff-time audit + maintenance drill", "may refuse opening without staff or training"],
        "nearby_institutions": ["shared tests, courses + issue interfaces", "site, staff, review + exit costs", "authority, cost and benefit allocation unknown", "formal intent + rights/procurement review", "may refuse unauthorized name or resource use"],
    }
    rh=137
    for r,g in enumerate(groups[:9]):
        yy=y0+74+r*rh
        if r%2==0:d.rectangle((x0,yy,x1,yy+rh),fill="#F3F2ED")
        c=[GREEN,BLUE,GOLD,ORANGE,VIOLET][r%5]
        d.rectangle((x0,yy,x0+10,yy+rh),fill=c)
        vals=[]
        name=g.get('label_zh') or g.get('name_zh') or g.get('group_zh') or g.get('group') or f"G{r+1}"
        vals.append(name if lang=='zh' else g.get('label_en', translations[r]))
        keysets=[('benefits_zh','benefits'),('burdens_zh','burdens'),('blind_spots_zh','blind_spots'),('required_inputs_zh','required_inputs'),('standing_zh','procedural_standing')]
        for zhkey,key in keysets:
            v=g.get(zhkey,g.get(key,""))
            if isinstance(v,list): v='；'.join(str(x) for x in v[:2]) if lang=='zh' else '; '.join(str(x) for x in v[:2])
            if isinstance(v,dict): v='；'.join(str(x) for x in v.get('rights', [])[:2])
            vals.append(str(v))
        for i,val in enumerate(vals):
            if lang=='en' and i>0:
                val=english_rows[g.get('group_id')][i-1]
            text_block(d,(cols[i]+14,yy+18),val,17 if lang=='zh' else 14,c if i==0 else INK,cols[i+1]-cols[i]-26,25 if lang=='zh' else 22,medium=(i==0),max_lines=4)
            if i>0:d.line((cols[i],yy,cols[i],yy+rh),fill="#D2D7D8",width=1)
        d.line((x0,yy+rh,x1,yy+rh),fill="#CBD1D2",width=1)
    footer(d,"inclusion-ledger.json · inclusion-ledger.schema.json · user-cotest-plan.json","未知项保持为未知，不以平均值替代差异" if lang=='zh' else "unknowns remain explicit; averages do not erase differences","07",lang)
    return im


def area_action_plan(lang="zh"):
    title="近期项目包与实施前置条件" if lang=='zh' else "Near-term Work Packages and Preconditions"
    sub="六个项目包按责任、成本级别、工期、验收和退出条件组织" if lang=='zh' else "Six work packages organized by owner, cost class, duration, acceptance and exit"
    im,d=page("08 / DELIVERY LEDGER",title,sub,lang)
    data=load_json(ASSETS/"implementation-operation-contract.json"); pkgs=data['packages']
    x0,y0,x1=66,300,W-66
    d.text((x0,y0),"月份" if lang=='zh' else "MONTH",font=fnt(18,bold=True),fill=MUTED)
    gantt_x=x0+760; gantt_w=x1-gantt_x
    for m in range(0,25,3):
        xx=gantt_x+gantt_w*m/24
        d.line((xx,y0+38,xx,1220),fill="#D2D7D8",width=1)
        d.text((xx-8,y0),str(m),font=fnt(16),fill=MUTED)
    colors=[GREEN,ORANGE,BLUE,GOLD,VIOLET,RED]
    names_en=["innovation spine pilot","Dazhongsi station-city pilot","Zhongzhiyuan validation field","AI Origin shared ground floor","service-node prototypes","AI public-service governance"]
    yy=y0+70
    for i,p in enumerate(pkgs):
        c=colors[i]; d.text((x0,yy),p['id'],font=fnt(22,bold=True),fill=c)
        name=p['name_zh'] if lang=='zh' else names_en[i]
        text_block(d,(x0+80,yy-4),name,22 if lang=='zh' else 18,INK,430,30,medium=True,max_lines=2)
        d.text((x0+560,yy),p['class'],font=fnt(20,bold=True),fill=c)
        lo,hi=[int(v) for v in p['duration_months'].split('-')]
        bx=gantt_x; bw=gantt_w*hi/24
        d.rounded_rectangle((bx,yy-2,bx+bw,yy+38),radius=18,fill=c)
        d.text((bx+12,yy+5),f"{lo}-{hi} m",font=fnt(16,bold=True),fill=WHITE)
        text_block(d,(gantt_x,yy+55),("前置：" if lang=='zh' else "Gate: ")+('；'.join(p['start'][:3]) if lang=='zh' else ' / '.join(["tenure","specialist review","operations owner"])),15 if lang=='zh' else 13,MUTED,gantt_w,23,max_lines=2)
        d.line((x0,yy+128,x1,yy+128),fill="#CDD3D4",width=1)
        yy+=145
    rounded(d,(x0,1260,x1,1570),fill=INK,outline=INK,radius=12,width=2)
    d.text((x0+28,1290),"停止与缩减原则" if lang=='zh' else "STOP AND SCALE-DOWN RULES",font=fnt(23,bold=True),fill=WHITE)
    rules=["连续路径无法形成时，缩减为单点可逆试验。","疏散或轨道安全不满足时，停止空间扩建。","重大事件或两轮整改失败后，停止测试并独立复核。","维护经费或人员未落实时，撤除设备并保留基础公共设施。"] if lang=='zh' else ["If continuity fails, scale down to one reversible test.","If evacuation or rail safety fails, stop spatial expansion.","After a major incident or two failed remedies, stop and review independently.","Without maintenance funds or staff, remove equipment and keep basic public amenities."]
    for i,r in enumerate(rules):
        xx=x0+28+(i%2)*1130; ry=1350+(i//2)*92
        d.text((xx,ry),f"0{i+1}",font=fnt(17,bold=True),fill=ORANGE)
        text_block(d,(xx+50,ry-2),r,18 if lang=='zh' else 15,WHITE,1000,27,max_lines=2)
    footer(d,"implementation-operation-contract.json · spatial.json · Beijing Urban Renewal Regulation","S/M/L 为概念比较级别，不构成投资承诺" if lang=='zh' else "S/M/L are concept comparison classes, not investment commitments","08",lang)
    return im


def implementation_section(lang="zh"):
    title="京张创新发展轴典型断面与设施界面" if lang=='zh' else "Typical Innovation-spine Section and Facility Interfaces"
    sub="连续步行、雨水花园、双向骑行和人工服务形成 12 m 弹性组合" if lang=='zh' else "Walk, rain garden, two-way cycling and human service form a flexible 12 m combination"
    im,d=page("09 / TYPICAL SECTION",title,sub,lang)
    x0,y0,x1,y1=90,360,W-90,1240
    d.rectangle((x0,y0,x1,y1),fill="#E8E5DD",outline=INK,width=3)
    ground=950
    d.rectangle((x0,ground,x1,y1),fill="#D2CFC5")
    total=12; parts=[(3,"步行" if lang=='zh' else "WALK", "#D9D5C7"),(2.5,"雨水花园" if lang=='zh' else "RAIN GARDEN",PALE_GREEN),(4,"双向骑行" if lang=='zh' else "TWO-WAY CYCLE",PALE_BLUE),(2.5,"人工服务" if lang=='zh' else "HUMAN SERVICE",PALE_ORANGE)]
    sx=x0+60; usable=x1-x0-120
    centers=[]
    for value,lab,c in parts:
        ww=usable*value/total
        d.rectangle((sx,670,sx+ww,ground),fill=c,outline=INK,width=3)
        centers.append((sx+ww/2,ww))
        d.text((sx+20,790),lab,font=fnt(22 if lang=='zh' else 18,bold=True),fill=INK)
        d.line((sx,1020,sx+ww,1020),fill=INK,width=2);d.line((sx,1008,sx,1032),fill=INK,width=2);d.line((sx+ww,1008,sx+ww,1032),fill=INK,width=2)
        val=f"{value:.1f} m"; tw=d.textbbox((0,0),val,font=fnt(19,bold=True))[2]
        d.rectangle((sx+ww/2-tw/2-8,1007,sx+ww/2+tw/2+8,1035),fill=PAPER)
        d.text((sx+ww/2-tw/2,1008),val,font=fnt(19,bold=True),fill=INK)
        sx+=ww
    # Refined section elements.
    for tx in [centers[0][0]+80,centers[1][0],centers[3][0]-50]:
        d.line((tx,665,tx,475),fill="#66513F",width=10)
        d.ellipse((tx-105,350,tx+105,610),fill="#759773",outline=GREEN,width=3)
    # Rainwater arrows and check dams.
    rgx=centers[1][0]
    d.arc((rgx-135,720,rgx+135,930),0,180,fill=BLUE,width=5)
    arrow(d,(rgx-180,735),(rgx-40,820),BLUE,4,14);arrow(d,(rgx+180,735),(rgx+40,820),BLUE,4,14)
    # Service canopy, counter and manual notice.
    sx=centers[3][0]
    d.line((sx-150,660,sx-150,430),fill=INK,width=8);d.line((sx+150,660,sx+150,430),fill=INK,width=8)
    d.rectangle((sx-190,410,sx+190,445),fill=ORANGE)
    d.rectangle((sx-95,750,sx+95,790),fill="#AA7E58")
    d.rectangle((sx+15,505,sx+120,640),fill=PANEL,outline=INK,width=2)
    d.text((sx+38,548),"i",font=fnt(38,bold=True),fill=ORANGE)
    # Dimension and callouts.
    callouts=[((centers[0][0],350),"连续遮阴与可坐靠设施" if lang=='zh' else "continuous shade + supportive seating",(150,280),GREEN),((rgx,820),"汇水、溢流、退水和检修路径" if lang=='zh' else "inlet, overflow, drain + maintenance",(800,1190),BLUE),((centers[2][0],740),"骑行净宽建议 4.0 m" if lang=='zh' else "proposed cycle clear width 4.0 m",(1250,280),GOLD),((sx,520),"24-36 m² 人工服务空间" if lang=='zh' else "24-36 m² human-service room",(1800,280),ORANGE)]
    for anchor,lab,pos,c in callouts:
        arrow(d,pos,anchor,c,3,12)
        rounded(d,(pos[0]-10,pos[1]-10,pos[0]+480,pos[1]+60),fill=PANEL,outline=c,radius=8,width=2)
        text_block(d,(pos[0]+8,pos[1]+6),lab,18 if lang=='zh' else 15,INK,450,25,medium=True,max_lines=2)
    rounded(d,(90,1300,W-90,1585),fill=PANEL,outline=LINE,radius=10,width=2)
    notes=[("校核","道路红线、轨道安全、消防和市政条件确认后，在 10.5-14.0 m 内组合。\n补充地形、树木和管线测绘。\n施工图复核连续净宽及交叉口。"),("无障碍","连续路线按最窄点实测。\n服务区保留轮椅回转和陪护空间。\n导向同时提供文字、图形和人工说明。"),("运行","停电或断网时保留照明、实体导向和人工服务。\n每月巡检排水、座椅和照明。\n一般故障 24 小时内形成工单。")]
    notes_en=[("CHECK","Confirm redline, rail, fire and utilities before combining within 10.5-14.0 m.\nAdd survey of levels, trees and utilities.\nReview clear width and intersections in detailed design."),("ACCESS","Measure continuity at the narrowest point.\nKeep wheelchair turning and companion space.\nProvide text, graphic and human wayfinding."),("OPERATE","Keep lighting, physical wayfinding and human service during failure.\nInspect drainage, seats and light monthly.\nIssue routine-fault work orders within 24 hours.")]
    for i,(lab,val) in enumerate(notes if lang=='zh' else notes_en):
        xx=120+i*770; d.text((xx,1330),lab,font=fnt(18,bold=True),fill=[GREEN,BLUE,ORANGE][i]);text_block(d,(xx,1370),val,17 if lang=='zh' else 14,INK,690,27,max_lines=7)
    footer(d,"spatial.json · Beijing Walk/Cycle Standard · Accessibility Law · Sponge-city standards","建议断面，工程参数待专项审查" if lang=='zh' else "proposed section; engineering parameters pending specialist review","09",lang)
    return im


def service_node_kit(lang="zh"):
    title="公共服务节点：可拆装构造与运行标准" if lang=='zh' else "Public-service Node: Demountable Kit and Operating Standard"
    sub="250-400 m² 模块｜人工服务、遮阴停留、饮水充电、雨水花园和信息公示" if lang=='zh' else "250-400 m² module | human service, shaded stay, water/charging, rain garden and public notice"
    im,d=page("10 / SERVICE NODE KIT",title,sub,lang)
    # Pseudo-axonometric exploded assembly.
    ox,oy=700,880
    def iso_rect(cx,cy,w,h,z,fill,outline=INK):
        pts=[(cx,cy-z),(cx+w,cy-h/2-z),(cx,cy-h-z),(cx-w,cy-h/2-z)]
        d.polygon(pts,fill=fill,outline=outline);d.line(pts+[pts[0]],fill=outline,width=3)
        return pts
    layers_ax=[(420,250,0,"#D9D5C8","可逆基础与无障碍环路" if lang=='zh' else "reversible base + access loop"),(370,210,130,PALE_GREEN,"雨水花园与植栽模块" if lang=='zh' else "rain garden + planting"),(320,180,260,PALE_BLUE,"人工服务与开放设施" if lang=='zh' else "human service + open amenities"),(390,220,410,PALE_ORANGE,"遮阴、照明与信息公示" if lang=='zh' else "shade, light + notice")]
    layer_details_zh=["最小土建干预；保留轮椅回转和消防通道","汇水、溢流、退水和检修口同步设置","24-36 m² 人工服务；饮水、充电和纸质地图","公布用途、责任、故障和退出；按月巡检"]
    layer_details_en=["minimum civil works; keep turning and fire access","provide inlet, overflow, drain and maintenance port","24-36 m² human service, water, charging and paper map","publish purpose, owner, fault and exit; inspect monthly"]
    for i,(w,h,z,c,lab) in enumerate(layers_ax):
        pts=iso_rect(ox,oy,w,h,z,c)
        anchor=(pts[1][0],pts[1][1]);pos=(1260,420+i*220)
        arrow(d,anchor,pos,[GREEN,BLUE,GOLD,ORANGE][i],3,12)
        rounded(d,(pos[0],pos[1]-24,pos[0]+740,pos[1]+82),fill=PANEL,outline=[GREEN,BLUE,GOLD,ORANGE][i],radius=9,width=2)
        d.text((pos[0]+20,pos[1]-5),f"0{i+1}",font=fnt(18,bold=True),fill=[GREEN,BLUE,GOLD,ORANGE][i])
        text_block(d,(pos[0]+70,pos[1]-8),lab,21 if lang=='zh' else 18,INK,640,30,medium=True,max_lines=2)
        text_block(d,(pos[0]+70,pos[1]+32),(layer_details_zh if lang=='zh' else layer_details_en)[i],14 if lang=='zh' else 13,MUTED,640,21,max_lines=2)
    # Vertical assembly lines.
    for dx in [-300,0,300]: d.line((ox+dx,420,ox+dx,930),fill="#A3ADB2",width=2)
    rounded(d,(66,1180,W-66,1580),fill=INK,outline=INK,radius=12,width=2)
    entries=[("人工服务","24-36 m²，公布服务时段和责任人\n60 秒内确认求助；按月抽测在岗状态\n接管失效即切换实体流程","HUMAN SERVICE","24-36 m²; publish hours and owner\nacknowledge help within 60 seconds\nfailed takeover switches to physical service"),("基本设施","饮水、充电、座椅、照明、纸质地图\n雨水花园设置安全溢流和检修口\n每月巡检并公开故障状态","BASIC AMENITIES","water, charging, seating, light, paper map\nprovide safe overflow and maintenance port\ninspect monthly and publish fault status"),("数据边界","不以账户、手机或人脸作为服务条件\n节点仅处理完成任务所需的最少数据\n用途变更须重新告知和审查","DATA BOUNDARY","no account, phone or face prerequisite\nprocess only task-minimum data\nnew purpose requires notice and review"),("退出条件","维护经费或人员未落实时撤除设备\n连续两轮整改失败时暂停智能功能\n保留座椅、遮阴、导向和人工公告","EXIT","remove equipment without maintenance resources\npause smart functions after two failed remedies\nkeep seats, shade, wayfinding and human notice")]
    for i,e in enumerate(entries):
        xx=100+i*580;lab,val=(e[0],e[1]) if lang=='zh' else (e[2],e[3])
        d.text((xx,1220),lab,font=fnt(19,bold=True),fill=[GREEN,BLUE,GOLD,ORANGE][i]);text_block(d,(xx,1265),val,17 if lang=='zh' else 14,WHITE,500,27,max_lines=7)
    footer(d,"spatial.json · implementation-operation-contract.json · service-node design targets","模块面积与构造需结合管线、消防和场地许可" if lang=='zh' else "module area and construction require utilities, fire and site permits","10",lang)
    return im


def regional_collaboration(lang="zh"):
    title="区域协作接口与责任回执" if lang=='zh' else "Regional Collaboration Interfaces and Accountability Receipts"
    sub="五类接口以输入、输出、责任主体、进入条件和退出条件组织" if lang=='zh' else "Five interfaces organized by input, output, owner, entry and exit conditions"
    im,d=page("11 / REGIONAL INTERFACES",title,sub,lang)
    data=load_json(ASSETS/"regional-collaboration-ledger.json"); items=data.get('interfaces',data.get('entries',[]))
    # Central spine and interface routes.
    cx=610; d.line((cx,360,cx,1450),fill=INK,width=18)
    d.text((340,300),"京张创新发展轴" if lang=='zh' else "JINGZHANG INNOVATION SPINE",font=fnt(24,bold=True),fill=INK)
    colors=[GREEN,BLUE,GOLD,ORANGE,VIOLET]
    labels_en=["research + open source","public service + community","rail + mobility","industry + testing","climate + maintenance"]
    for i,item in enumerate(items[:5]):
        yy=390+i*215;c=colors[i]
        d.ellipse((cx-38,yy-38,cx+38,yy+38),fill=c,outline=WHITE,width=3)
        d.text((cx-18,yy-12),f"I{i+1}",font=fnt(17,bold=True),fill=WHITE)
        arrow(d,(cx+52,yy),(850,yy),c,5,16)
        rounded(d,(870,yy-82,W-66,yy+115),fill=PANEL,outline=c,radius=12,width=3)
        name=item.get('name_zh') or item.get('interface_zh') or item.get('id',f'I{i+1}')
        if lang=='en':name=labels_en[i]
        d.text((900,yy-55),name,font=fnt(24 if lang=='zh' else 21,bold=True),fill=INK)
        fields=[]
        for key,labzh,laben in [('input','输入','INPUT'),('output','输出','OUTPUT'),('owner','责任','OWNER')]:
            val=item.get(key) or item.get(key+'s') or item.get(key+'_zh') or (item.get('owner_types') if key=='owner' else '') or ''
            if isinstance(val,list): val='；'.join(str(x) for x in val[:2])
            if isinstance(val,dict): val='；'.join(str(x) for x in val.values())
            if lang=='en': val=["registered need + source","published deliverable + receipt","named accountable and responsible parties"][len(fields)]
            fields.append((labzh if lang=='zh' else laben,str(val)))
        fx=900
        for lab,val in fields:
            d.text((fx,yy-5),lab,font=fnt(15,bold=True),fill=c)
            text_block(d,(fx,yy+22),val,16 if lang=='zh' else 14,INK,400,23,max_lines=3)
            fx+=465
    rounded(d,(66,1490,W-66,1605),fill=INK,outline=INK,radius=10,width=2)
    note="每个接口须形成可公开的输入清单、交付回执和退出记录；跨区协作不替代属地审批、采购和专业责任。" if lang=='zh' else "Each interface requires a public input list, delivery receipt and exit record. Regional collaboration does not replace local approvals, procurement or professional duties."
    text_block(d,(100,1522),note,19 if lang=='zh' else 16,WHITE,W-200,28,medium=True,max_lines=2)
    footer(d,"regional-collaboration-ledger.json · implementation-operation-contract.json","协作接口为建议机制，责任须在实施协议中确认" if lang=='zh' else "proposed interfaces; responsibilities require implementation agreements","11",lang)
    return im


def ai_governance(lang="zh"):
    title="人工智能公共服务全生命周期治理" if lang=='zh' else "Lifecycle Governance for AI-enabled Public Services"
    sub="准入、运行、接管、整改、复审与退出形成可追溯闭环" if lang=='zh' else "Admission, operation, takeover, remedy, review and exit form a traceable loop"
    im,d=page("12 / SERVICE GOVERNANCE",title,sub,lang)
    center=(W//2,850);r=440
    steps_zh=["用途登记","最少数据","独立审查","受控运行","人工接管","公开回执","整改复测","延续或退出"]
    steps_en=["purpose register","minimum data","independent review","controlled operation","human takeover","public receipt","remedy + retest","continue or exit"]
    colors=[GREEN,BLUE,GOLD,ORANGE,RED,VIOLET,BLUE,GREEN]
    pts=[]
    for i,lab in enumerate(steps_zh if lang=='zh' else steps_en):
        ang=-math.pi/2+i*2*math.pi/8; x=center[0]+r*math.cos(ang);y=center[1]+r*math.sin(ang);pts.append((x,y))
        d.ellipse((x-88,y-88,x+88,y+88),fill=PANEL,outline=colors[i],width=5)
        d.text((x-22,y-46),f"{i+1:02d}",font=fnt(20,bold=True),fill=colors[i])
        text_block(d,(x-68,y-12),lab,20 if lang=='zh' else 16,INK,136,26,medium=True,max_lines=3)
    for i in range(8):arrow(d,pts[i],pts[(i+1)%8],colors[i],4,15)
    d.ellipse((center[0]-220,center[1]-220,center[0]+220,center[1]+220),fill=INK)
    d.text((center[0]-117,center[1]-85),"8-80",font=fnt(70,bold=True),fill=WHITE)
    text_block(d,(center[0]-165,center[1]+5),"同等服务契约" if lang=='zh' else "equal-service contract",28 if lang=='zh' else 22,WHITE,330,38,medium=True,max_lines=2)
    # Side stop triggers.
    rounded(d,(66,310,520,1410),fill=PANEL,outline=RED,radius=12,width=3)
    d.text((94,345),"立即停止触发项" if lang=='zh' else "IMMEDIATE STOP TRIGGERS",font=fnt(22,bold=True),fill=RED)
    stops=["责任主体缺失","人工接管失效","未经同意扩大数据用途","发生重大安全事件","两轮整改仍不通过"] if lang=='zh' else ["no named owner","human takeover unavailable","unconsented data expansion","major safety incident","two failed remedies"]
    yy=420
    for i,s in enumerate(stops):
        d.text((94,yy),f"S{i+1}",font=fnt(17,bold=True),fill=RED);text_block(d,(148,yy-3),s,19 if lang=='zh' else 16,INK,330,28,max_lines=3);yy+=150
    rounded(d,(W-520,310,W-66,1410),fill=PANEL,outline=GREEN,radius=12,width=3)
    d.text((W-492,345),"基本服务连续项" if lang=='zh' else "SERVICE CONTINUITY",font=fnt(22,bold=True),fill=GREEN)
    cont=["实体导向持续可见","人工窗口按公示在岗","纸质或现金渠道可用","故障状态公开标识","申诉和退出渠道开放"] if lang=='zh' else ["physical wayfinding visible","human desk staffed as published","paper or cash path available","fault status publicly marked","appeal and exit channel open"]
    yy=420
    for i,s in enumerate(cont):
        d.text((W-492,yy),f"C{i+1}",font=fnt(17,bold=True),fill=GREEN);text_block(d,(W-438,yy-3),s,19 if lang=='zh' else 16,INK,330,28,max_lines=3);yy+=150
    footer(d,"growth-runbook.json · implementation-operation-contract.json · risk.json","方案治理协议，须经责任主体和法定程序确认" if lang=='zh' else "scheme governance protocol; requires accountable and statutory approval","12",lang)
    return im


def delivery_program(lang="zh"):
    title="90 天共测、建设分期与公开回执" if lang=='zh' else "90-day Co-test, Delivery Phases and Public Receipts"
    sub="先锁定资料，再模拟流程、开展红队测试，最后决定实施、调整或退出" if lang=='zh' else "Lock evidence, mock the service, red-team failures, then decide implement, revise or exit"
    im,d=page("13 / CO-TEST PROGRAM",title,sub,lang)
    phases=[("LOCK","0-15 天" if lang=='zh' else "days 0-15","边界、权属、使用者、责任和数据清单" if lang=='zh' else "boundaries, tenure, users, owners and data register",GREEN),("MOCK","16-45 天" if lang=='zh' else "days 16-45","无建设条件下演练服务流程和人工接管" if lang=='zh' else "rehearse service and human takeover before construction",BLUE),("RED TEAM","46-75 天" if lang=='zh' else "days 46-75","注入故障、误导、排斥和维护中断" if lang=='zh' else "inject failure, misleading output, exclusion and maintenance gaps",ORANGE),("DECIDE","76-90 天" if lang=='zh' else "days 76-90","公开证据，决定实施、缩减、整改或退出" if lang=='zh' else "publish evidence and decide implement, scale down, remedy or exit",VIOLET)]
    x=66; y=340
    for i,(key,time,desc,c) in enumerate(phases):
        w=560; rounded(d,(x,y,x+w,y+350),fill=PANEL,outline=c,radius=14,width=4)
        d.text((x+28,y+28),key,font=fnt(25,bold=True),fill=c);d.text((x+28,y+78),time,font=fnt(21,medium=True),fill=INK)
        text_block(d,(x+28,y+130),desc,21 if lang=='zh' else 18,INK,w-56,31,max_lines=5)
        d.text((x+28,y+285),f"R{i+1}",font=fnt(18,bold=True),fill=c);d.text((x+82,y+285),"公开阶段回执" if lang=='zh' else "public phase receipt",font=fnt(17),fill=MUTED)
        if i<3:arrow(d,(x+w+8,y+175),(x+w+48,y+175),INK,4,12)
        x+=590
    rounded(d,(66,760,W-66,1545),fill=INK,outline=INK,radius=12,width=2)
    d.text((96,800),"参与结构与证据要求" if lang=='zh' else "PARTICIPATION AND EVIDENCE REQUIREMENTS",font=fnt(25,bold=True),fill=WHITE)
    groups=[("使用者","儿童家庭、长者、残障人士、通勤者","USERS","children/families, older people, disabled people, commuters"),("运营者","街道、园区、站区、设施维护和人工服务人员","OPERATORS","subdistrict, park, station, maintenance and human-service staff"),("专业方","规划、交通、消防、市政、无障碍、数据和安全","SPECIALISTS","planning, transport, fire, utilities, accessibility, data and safety"),("异议方","受影响居民、租户、小商户和产权单位","AFFECTED PARTIES","residents, tenants, small businesses and owners")]
    yy=875
    for i,e in enumerate(groups):
        lab,val=(e[0],e[1]) if lang=='zh' else (e[2],e[3]);c=[GREEN,BLUE,GOLD,ORANGE][i]
        d.text((105,yy),lab,font=fnt(20,bold=True),fill=c);text_block(d,(260,yy-3),val,19 if lang=='zh' else 16,WHITE,900,28,max_lines=3)
        receipt=["到达任务与使用障碍","在岗、维护与降级记录","专项意见和整改闭环","负担、补偿与异议处理"][i] if lang=='zh' else ["task completion + barriers","staffing, maintenance + degraded mode","specialist opinion + remedy closure","burden, mitigation + objection handling"][i]
        d.text((1320,yy),"回执" if lang=='zh' else "RECEIPT",font=fnt(16,bold=True),fill=c);text_block(d,(1410,yy-3),receipt,18 if lang=='zh' else 15,WHITE,850,27,max_lines=3)
        d.line((96,yy+100,W-96,yy+100),fill="#5D7183",width=1);yy+=145
    footer(d,"user-cotest-plan.json · inclusion-ledger.json · implementation-operation-contract.json","共测结果不代替法定审批和工程验收" if lang=='zh' else "co-test results do not replace statutory approval or engineering acceptance","13",lang)
    return im


def brand_system(lang="zh"):
    title="“京张共长线”品牌与公共信息系统" if lang=='zh' else "Grow with Jingzhang Brand and Public-information System"
    sub="名称、标志、色彩和服务公示采用统一语义，不使用宣传性技术承诺" if lang=='zh' else "Name, mark, color and service notices share one meaning without promotional technology claims"
    im,d=page("14 / IDENTITY SYSTEM",title,sub,lang)
    # Mark: two rail lines crossed by growth rings/open gate.
    cx,cy=580,850
    for off in [-34,34]:d.line((210,cy+off,950,cy+off),fill=INK,width=16)
    for rr,c in [(260,GREEN),(190,BLUE),(120,ORANGE)]:
        d.arc((cx-rr,cy-rr,cx+rr,cy+rr),25,330,fill=c,width=18)
    d.rectangle((800,cy-110,930,cy+110),fill=PAPER)
    arrow(d,(790,cy),(950,cy),ORANGE,14,28)
    d.text((220,1190),"京张共长线" if lang=='zh' else "GROW WITH JINGZHANG",font=fnt(58 if lang=='zh' else 46,bold=True),fill=INK)
    text_block(d,(220,1275),"开放缺口对应公众反馈、服务退出与持续更新" if lang=='zh' else "The open gate records feedback, service exit and continuing revision",24 if lang=='zh' else 20,MUTED,800,35,max_lines=3)
    x=1120
    d.text((x,330),"公共语义" if lang=='zh' else "PUBLIC MEANING",font=fnt(24,bold=True),fill=INK)
    meanings=[("轨线","京张铁路的连续时间与空间骨架","RAILS","continuity of the Jingzhang railway"),("年轮","不同年龄和使用群体共同成长","RINGS","growth shared across ages and user groups"),("缺口","可反馈、可申诉、可退出","GATE","feedback, appeal and exit remain open")]
    yy=390
    for i,e in enumerate(meanings):
        lab,val=(e[0],e[1]) if lang=='zh' else (e[2],e[3]);c=[INK,GREEN,ORANGE][i]
        d.text((x,yy),lab,font=fnt(22,bold=True),fill=c);text_block(d,(x+130,yy-3),val,20 if lang=='zh' else 17,INK,760,30,max_lines=3);yy+=120
    d.text((x,780),"标准色" if lang=='zh' else "CORE PALETTE",font=fnt(24,bold=True),fill=INK)
    palette=[("铁路墨",INK),("公共橙",ORANGE),("林荫绿",GREEN),("证据蓝",BLUE),("档案纸",PAPER)]
    yy=840
    for i,(lab,c) in enumerate(palette):
        xx=x+(i%3)*390;ry=yy+(i//3)*125
        d.rectangle((xx,ry,xx+82,ry+82),fill=c,outline=INK,width=2)
        d.text((xx+100,ry+8),lab if lang=='zh' else ["rail ink","public orange","canopy green","evidence blue","archive paper"][i],font=fnt(18,medium=True),fill=INK)
        d.text((xx+100,ry+42),c,font=fnt(15),fill=MUTED)
    rounded(d,(1120,1120,W-66,1540),fill=PANEL,outline=LINE,radius=12,width=2)
    d.text((1150,1150),"应用规则" if lang=='zh' else "USE RULES",font=fnt(22,bold=True),fill=INK)
    rules=["公共橙仅用于服务入口、警示和退出信息。","图纸必须同时标记事实、建议目标和未知项。","名称不替代项目审批名称或法定地名。","所有数字服务公示人工路径和责任主体。"] if lang=='zh' else ["Public orange is reserved for service entry, warning and exit.","Drawings label facts, proposed targets and unknowns.","The name does not replace statutory project or place names.","Every digital service notice names the human path and owner."]
    yy=1210
    for i,r in enumerate(rules):d.text((1150,yy),f"{i+1:02d}",font=fnt(16,bold=True),fill=ORANGE);text_block(d,(1200,yy-3),r,18 if lang=='zh' else 15,INK,1080,27,max_lines=2);yy+=72
    footer(d,"brand-system.json · rights-clearance-ledger.json","方案品牌，用于本次开源征集成果表达" if lang=='zh' else "scheme identity for this open-call submission","14",lang)
    return im


def rights_evidence(lang="zh"):
    title="证据、版权与主张边界清单" if lang=='zh' else "Evidence, Rights and Claim-boundary Register"
    sub="数据来源、加工方式、许可条件和可表达范围逐项对应" if lang=='zh' else "Source, transformation, licence condition and permitted claim are paired item by item"
    im,d=page("15 / RIGHTS + EVIDENCE",title,sub,lang)
    rows=[
        ("项目公告与任务书","官方公开资料","任务范围与公告面积","不得替代正式红线"),
        ("工作底图 GeoJSON","仓库资料+方案推导","空间复算与概念分区","边界为 provisional"),
        ("OpenStreetMap","ODbL 1.0","城市纹理与网络背景","标注 © contributors"),
        ("NASA POWER","公开气候数据","2015-2024 概念基线","不替代本地专项模型"),
        ("Blender/Three.js","本地生成模型","空间方案展示","不主张建成效果"),
        ("图像生成场景","方案团队提示与生成","空间气质参考","人物和材料为意向"),
        ("技术图与 PDF","本地脚本+结构化数据","评审与公开讨论","建议值不表达为现状"),
        ("字体","系统许可字体","图件与 PDF 嵌入","随文件分发，不单独再授权"),
    ]
    rows_en=[
        ("official notice + taskbook","official public sources","scope + published areas","not an official redline"),
        ("working-base GeoJSON","repository + scheme derivation","recalculation + concept zones","boundary remains provisional"),
        ("OpenStreetMap","ODbL 1.0","urban texture + network context","credit © contributors"),
        ("NASA POWER","public climate data","2015-2024 concept baseline","not a local specialist model"),
        ("Blender / Three.js","locally generated model","scheme visualization","no built-result claim"),
        ("generated scenes","team prompt + generation","spatial atmosphere reference","people/materials are indicative"),
        ("technical sheets + PDF","local script + structured data","review + public discussion","targets not shown as existing"),
        ("fonts","system-licensed fonts","embedded in figures + PDFs","distributed only as embedded output"),
    ]
    rows=rows if lang=='zh' else rows_en
    x0,y0,x1=66,300,W-66;cols=[x0,x0+480,x0+930,x0+1540,x1]
    heads=['材料','来源/许可','本方案用途','表达边界'] if lang=='zh' else ['ASSET','SOURCE / LICENCE','USE IN SCHEME','CLAIM BOUNDARY']
    d.rectangle((x0,y0,x1,y0+76),fill=INK)
    for i,h in enumerate(heads):d.text((cols[i]+16,y0+24),h,font=fnt(18 if lang=='zh' else 15,bold=True),fill=WHITE)
    rh=130
    for r,row in enumerate(rows):
        yy=y0+76+r*rh
        if r%2==0:d.rectangle((x0,yy,x1,yy+rh),fill="#F3F2ED")
        for i,val in enumerate(row):text_block(d,(cols[i]+16,yy+22),val,18 if lang=='zh' else 15,ORANGE if i==3 else INK,cols[i+1]-cols[i]-32,28,medium=(i in (0,3)),max_lines=3)
        for cx in cols[1:-1]:d.line((cx,yy,cx,yy+rh),fill="#D0D6D7",width=1)
        d.line((x0,yy+rh,x1,yy+rh),fill="#C9D0D2",width=1)
    rounded(d,(x0,1450,x1,1585),fill=INK,outline=INK,radius=10,width=2)
    note="最终成果仅主张：结构化方案可复算、准入规则可测试、实施前置条件可追踪。正式边界、建设许可、运营授权和建成绩效仍需后续程序确认。" if lang=='zh' else "The final package claims only reproducible scheme data, testable admission rules and traceable preconditions. Official boundaries, construction permission, operational authorization and built performance require later procedures."
    text_block(d,(x0+28,1482),note,19 if lang=='zh' else 16,WHITE,x1-x0-56,29,medium=True,max_lines=3)
    footer(d,"sources.json · rights-clearance-ledger.json · report/copyright_statement.md","来源、许可与主张边界已登记" if lang=='zh' else "sources, rights and claim boundaries registered","15",lang)
    return im


FIGURE_BUILDERS = {
    "site-overview": site_overview,
    "land-use-structure": land_use_structure,
    "key-areas": key_areas,
    "mobility-bluegreen": mobility_bluegreen,
    "metrics-evidence": metrics_evidence,
    "implementation-protocol": implementation_protocol,
    "inclusion-incidence": inclusion_incidence,
    "area-action-plan": area_action_plan,
    "implementation-section": implementation_section,
    "service-node-kit": service_node_kit,
    "regional-collaboration": regional_collaboration,
    "ai-governance": ai_governance,
    "delivery-program": delivery_program,
    "brand-system": brand_system,
    "rights-evidence": rights_evidence,
}


BOOKLET_ORDER = [
    "site-overview", "key-areas", "implementation-protocol", "land-use-structure",
    "mobility-bluegreen", "metrics-evidence", "inclusion-incidence", "area-action-plan",
    "implementation-section", "service-node-kit", "regional-collaboration", "ai-governance",
    "delivery-program", "rights-evidence", "brand-system",
]


def make_pdf(path: Path, figure_names: list[str], lang="zh", a0=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    size = landscape(A0 if a0 else A3)
    c = canvas.Canvas(str(path), pagesize=size, pageCompression=1)
    pw, ph = size
    if not a0:
        for name in figure_names:
            p = FIG / f"{name}{'.en.png' if lang == 'en' else '.png'}"
            c.drawImage(str(p), 0, 0, width=pw, height=ph, preserveAspectRatio=False, mask='auto')
            c.showPage()
    else:
        groups = [figure_names[i:i+4] for i in range(0, len(figure_names), 4)]
        margin = 22
        gap = 12
        cell_w = (pw - 2*margin - gap) / 2
        cell_h = (ph - 2*margin - gap) / 2
        for group in groups:
            c.setFillColorRGB(0.949, 0.937, 0.906)
            c.rect(0, 0, pw, ph, fill=1, stroke=0)
            for j, name in enumerate(group):
                p = FIG / f"{name}{'.en.png' if lang == 'en' else '.png'}"
                col, row = j % 2, j // 2
                x = margin + col*(cell_w+gap)
                y = ph-margin-(row+1)*cell_h-row*gap
                c.drawImage(str(p), x, y, width=cell_w, height=cell_h,
                            preserveAspectRatio=False, mask='auto')
            c.showPage()
    c.save()


def build_visual_html(lang="zh"):
    en = lang == "en"
    title = "Grow with Jingzhang | Evidence Atlas" if en else "京张共长线｜证据型城市设计图集"
    intro = "An 8-80 equal-service contract links spatial design, implementation and AI-service governance." if en else "以 8-80 同等服务契约统筹空间设计、项目实施与人工智能公共服务治理。"
    metric_data = load_json(SUB / "metrics.json")["metrics"]
    green_value = metric_data["green_ratio"]["value"]
    public_value = metric_data["public_space_ratio"]["value"]
    coverage = (
        "Overview map · three-level scope · key areas · land-use zoning · "
        "walk-cycle network · blue-green public space · buildings · renewal projects · "
        "AI scenarios · core metrics · task coverage · self-check status · sources · assumptions"
        if en
        else "总览地图 · 三层范围 · 重点区域 · 用地分区 · 交通慢行 · 蓝绿公共空间 · 建筑 · 更新项目 · AI 场景 · 核心指标 · 任务覆盖 · 自检状态 · 来源 · 假设"
    )
    nav = [(n, (n.replace('-', ' ').title() if en else {
        'site-overview':'总体空间','key-areas':'重点片区','implementation-protocol':'实施协议','land-use-structure':'用地结构','mobility-bluegreen':'慢行蓝绿','metrics-evidence':'指标证据','inclusion-incidence':'包容性','area-action-plan':'项目包','regional-collaboration':'区域协作','rights-evidence':'证据版权'}[n])) for n in ['site-overview','key-areas','implementation-protocol','land-use-structure','mobility-bluegreen','metrics-evidence','inclusion-incidence','area-action-plan','regional-collaboration','rights-evidence']]
    buttons=''.join(f'<button data-fig="{n}" aria-pressed="{str(i==0).lower()}">{html.escape(lab)}</button>' for i,(n,lab) in enumerate(nav))
    sources = "Sources: official brief, submitted GeoJSON, OSM/Overpass and NASA POWER. Provisional boundaries are not official redlines." if en else "资料来源：征集公告、任务书、提交 GeoJSON、OSM/Overpass 与 NASA POWER。示意边界不作为正式红线。"
    suffix='.en.png' if en else '.png'
    body=f'''<!doctype html><html lang="{'en' if en else 'zh'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>
    :root{{--paper:#f2efe7;--ink:#17324d;--muted:#647382;--orange:#f15a3a;--green:#2f7d57;--blue:#278ca8;--panel:#fbfaf6}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font-family:"Noto Sans SC","Microsoft YaHei",sans-serif}}main{{min-height:100vh;display:grid;grid-template-columns:310px 1fr}}aside{{padding:30px 24px;background:var(--ink);color:white;position:sticky;top:0;height:100vh;overflow:auto}}.eyebrow{{font-size:11px;letter-spacing:.16em;color:#f7a38f;font-weight:700}}h1{{font-size:32px;line-height:1.08;margin:12px 0}}.intro{{font-size:15px;line-height:1.65;color:#d7e0e6}}.metrics{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:24px 0 14px}}.metric{{border:1px solid #ffffff36;padding:10px}}.metric b{{display:block;font-size:21px;color:#fff}}.metric span{{font-size:10px;color:#b9c6cf}}.coverage{{font-size:10px;line-height:1.55;color:#b9c6cf;border-left:3px solid var(--orange);padding:0 0 0 10px;margin:0 0 16px}}nav{{display:grid;gap:7px}}button{{background:transparent;color:#d6e0e6;border:1px solid #ffffff35;padding:9px;text-align:left;cursor:pointer}}button[aria-pressed="true"]{{background:var(--orange);border-color:var(--orange);color:white;font-weight:700}}.source{{font-size:10px;line-height:1.6;color:#9fb0bb;margin-top:22px}}section{{padding:24px;min-width:0}}header{{display:flex;justify-content:space-between;align-items:end;margin:0 0 16px}}header b{{font-size:13px;color:var(--orange)}}header span{{font-size:11px;color:var(--muted)}}figure{{margin:0;background:var(--panel);border:1px solid #c9d0d2;box-shadow:0 10px 34px #17324d14}}img{{width:100%;height:auto;display:block}}.proof{{margin-top:12px;display:grid;grid-template-columns:repeat(4,1fr);gap:8px}}.proof div{{background:var(--panel);border-left:4px solid var(--blue);padding:12px;font-size:12px;line-height:1.5}}@media(max-width:900px){{main{{grid-template-columns:1fr}}aside{{position:relative;height:auto}}.proof{{grid-template-columns:1fr 1fr}}}}
    </style></head><body><main><aside><div class="eyebrow">EVIDENCE ATLAS / V3</div><h1>{html.escape(title)}</h1><p class="intro">{html.escape(intro)}</p><div class="metrics"><div class="metric"><b data-metric="site_area_sqm" data-value="11412825.386">11.41 km²</b><span>{'working extent' if en else '工作底图范围'}</span></div><div class="metric"><b data-metric="key_area_count" data-value="3">3</b><span>{'key districts' if en else '重点片区'}</span></div><div class="metric"><b data-metric="green_ratio" data-value="{green_value}">{green_value:.2%}</b><span>{'concept green ratio' if en else '概念绿地比例'}</span></div><div class="metric"><b data-metric="public_space_ratio" data-value="{public_value}">{public_value:.2%}</b><span>{'concept public-space ratio' if en else '概念公共空间比例'}</span></div><div class="metric"><b data-metric="protocol_service_pass_count" data-value="12">12/12</b><span>{'tabletop services passed' if en else '服务协议校验'}</span></div><div class="metric"><b data-metric="negative_test_caught_count" data-value="8">8/8</b><span>{'negative tests caught' if en else '负向测试拦截'}</span></div></div><p class="coverage">{html.escape(coverage)}</p><nav>{buttons}</nav><p class="source">{html.escape(sources)}</p></aside><section><header><b>{'FACTS · RECALCULATIONS · PROPOSED TARGETS · UNKNOWNS' if en else '公开事实 · 复算值 · 建议目标 · 未知项'}</b><span>{'Local, self-contained delivery' if en else '离线、自包含交付'}</span></header><figure><img id="main-figure" src="../assets/figures/site-overview{suffix}" alt="{html.escape(title)}"></figure><div class="proof"><div>{'12 services pass eight protocol rules.' if en else '12 项服务通过八条准入规则。'}</div><div>{'Eight injected defects are rejected by expected rules.' if en else '8 类注入缺陷均被预期规则拦截。'}</div><div>{'Nine population groups have benefit, burden and standing records.' if en else '9 类人群登记受益、负担和程序性权利。'}</div><div>{'All engineering targets remain subject to specialist review.' if en else '全部工程建议值仍须经过专项审查。'}</div></div></section></main><script>const img=document.getElementById('main-figure');document.querySelectorAll('button[data-fig]').forEach(b=>b.addEventListener('click',()=>{{document.querySelectorAll('button[data-fig]').forEach(x=>x.setAttribute('aria-pressed','false'));b.setAttribute('aria-pressed','true');img.src='../assets/figures/'+b.dataset.fig+'{suffix}'}}));</script></body></html>'''
    out = VISUAL / ("index.en.html" if en else "index.html")
    out.write_text(body, encoding="utf-8")


def build_equivalence_audit():
    pairs = [
        ("proposal.md", "proposal.en.md"),
        ("report/proposal.html", "report/proposal.en.html"),
        ("visual/index.html", "visual/index.en.html"),
        ("drawings/a3-booklet.pdf", "drawings/a3-booklet.en.pdf"),
        ("drawings/a0-boards.pdf", "drawings/a0-boards.en.pdf"),
    ] + [(f"assets/figures/{n}.png", f"assets/figures/{n}.en.png") for n in FIGURE_BUILDERS]
    result=[]
    for zh,en in pairs:
        zp,ep=SUB/zh,SUB/en
        result.append({"zh":zh,"en":en,"zh_exists":zp.exists(),"en_exists":ep.exists(),"status":"paired" if zp.exists() and ep.exists() else "missing"})
    audit={"schema_version":"1.0.0","scope":"human_facing_primary_deliverables","pair_count":len(result),"missing_count":sum(x['status']!='paired' for x in result),"pairs":result,"equivalence_rule_zh":"英文版保留相同空间范围、数字、证据状态、图件次序、实施条件和主张边界；语言按专业英语表达，不逐字直译。"}
    (ASSETS/"bilingual-equivalence-audit.json").write_text(json.dumps(audit,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest_entry(path: str, role: str, required: bool, language=None, translation_of=None):
    e={"path":path,"role":role,"required":required}
    p=SUB/path
    if path!="manifest.json" and p.exists():e["sha256"]=sha(p)
    if language:e["language"]=language
    if translation_of:e["translation_of"]=translation_of
    return e


def refresh_manifest():
    files=[]
    files.append(manifest_entry("manifest.json","manifest",True))
    core=[("proposal.md","narrative"),("agent.json","agent_card"),("metrics.json","metrics"),("assumptions.json","assumptions"),("sources.json","sources"),("self_check.json","self_check"),("compliance_matrix.json","compliance_matrix"),("standard_matrix.json","standard_matrix"),("design_depth_matrix.json","design_depth_matrix")]
    for p,r in core:files.append(manifest_entry(p,r,True,"zh" if p=="proposal.md" else None))
    files += [manifest_entry("proposal.en.md","narrative",True,"en","proposal.md"),manifest_entry("report/proposal.html","rendered_proposal_html",True,"zh"),manifest_entry("report/proposal.en.html","rendered_proposal_html",True,"en","report/proposal.html"),manifest_entry("report/narrative.md","narrative",False),manifest_entry("report/copyright_statement.md","copyright_statement",True)]
    for base in ["a3-booklet","a0-boards"]:
        files.append(manifest_entry(f"drawings/{base}.pdf","drawing",True,"zh"))
        files.append(manifest_entry(f"drawings/{base}.en.pdf","drawing",True,"en",f"drawings/{base}.pdf"))
    files += [manifest_entry("visual/index.html","visualization",True,"zh"),manifest_entry("visual/index.en.html","visualization",True,"en","visual/index.html")]
    for n in FIGURE_BUILDERS:
        files.append(manifest_entry(f"assets/figures/{n}.png","proposal_figure",True,"zh"))
        files.append(manifest_entry(f"assets/figures/{n}.en.png","proposal_figure",True,"en",f"assets/figures/{n}.png"))
    for p in sorted((SUB/"geometry").glob("*.geojson")):
        files.append(manifest_entry(p.relative_to(SUB).as_posix(),"geometry",True))
    for p in [SUB/"spatial.json",SUB/"risk.json"]+sorted(ASSETS.glob("*.json"))+sorted(ASSETS.glob("*.js")):
        if p.exists():files.append(manifest_entry(p.relative_to(SUB).as_posix(),"visualization",False,"neutral"))
    for rel,role in [("assets/renders/blender-corridor-overview.png","visualization"),("assets/generated-scenes/generated-responsible-prototyping.png","visualization"),("assets/generated-scenes/generated-co-learning-commons.png","visualization"),("assets/generated-scenes/generated-curious-arrival.png","visualization"),("assets/generated-scenes/generated-service-node-axonometric.jpg","visualization"),("assets/generated-scenes/generated-corridor-section.jpg","visualization")]:
        if (SUB/rel).exists():files.append(manifest_entry(rel,role,False,"neutral"))
    for rel in [
        "assets/generated-scenes/image2-climate-promenade.jpg",
        "assets/generated-scenes/image2-corridor-masterplan.jpg",
        "assets/generated-scenes/image2-program-rooms.jpg",
        "assets/generated-scenes/image2-public-identity.jpg",
        "assets/generated-scenes/image2-three-layer-story.jpg",
    ]:
        if (SUB/rel).exists():files.append(manifest_entry(rel,"visualization",False,"neutral"))
    protocol_primary="assets/generated-scenes/image2-protocol-infographic.jpg"
    protocol_english="assets/generated-scenes/image2-protocol-infographic.en.jpg"
    if (SUB/protocol_primary).exists():files.append(manifest_entry(protocol_primary,"visualization",False,"zh"))
    if (SUB/protocol_english).exists():files.append(manifest_entry(protocol_english,"visualization",False,"en",protocol_primary))
    manifest={"schema_version":"0.1.0","package_id":"grow-with-jingzhang","project_id":"centennial-jingzhang-ai-belt","site_package_version":"0.1.0","package_type":"professional_design_package","package_state":"ready_for_review","submission_stage":"formal","submission_type":"ai_agent","agent":{"agent_id":"CatNebulaaaa","agent_name":"Codex · 京张共长线","model":"OpenAI Codex","model_family":"gpt","model_detail":"OpenAI Codex"},"generated_at":datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'),"files":files,"validation_claim":{"self_checked":True,"known_blockers":[],"data_confidence":"medium"}}
    (SUB/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--manifest-only",action="store_true")
    args=parser.parse_args()
    if args.manifest_only:
        refresh_manifest();print("manifest refreshed");return
    FIG.mkdir(parents=True,exist_ok=True);DRAWINGS.mkdir(parents=True,exist_ok=True);ASSETS.mkdir(parents=True,exist_ok=True)
    for lang in ("zh","en"):
        for name,builder in FIGURE_BUILDERS.items():
            save_figure(name,lang,builder(lang))
        make_pdf(DRAWINGS/("a3-booklet.en.pdf" if lang=="en" else "a3-booklet.pdf"),BOOKLET_ORDER,lang,a0=False)
        a0_order=["site-overview","key-areas","implementation-protocol","metrics-evidence","land-use-structure","mobility-bluegreen","inclusion-incidence","area-action-plan","implementation-section","service-node-kit","regional-collaboration","rights-evidence"]
        make_pdf(DRAWINGS/("a0-boards.en.pdf" if lang=="en" else "a0-boards.pdf"),a0_order,lang,a0=True)
        build_visual_html(lang)
    build_equivalence_audit();refresh_manifest()
    print(f"built {len(FIGURE_BUILDERS)*2} figures, four PDFs and two visual atlases")


if __name__ == "__main__":
    main()
