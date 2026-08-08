from __future__ import annotations

import argparse
import textwrap
from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A0, A3, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parents[1]
SUB = ROOT / "submissions" / "caulif" / "jingzhang-ren-belt"
FIG = SUB / "assets" / "figures"
CTX = SUB / "assets" / "context"
OUT = SUB / "drawings"

NAVY = colors.HexColor("#172235")
INK = colors.HexColor("#25354a")
MUTED = colors.HexColor("#667085")
GOLD = colors.HexColor("#c79838")
ORANGE = colors.HexColor("#d78539")
GREEN = colors.HexColor("#2e9b7b")
BLUE = colors.HexColor("#236b9b")
PALE = colors.HexColor("#f7f3ed")
LINE = colors.HexColor("#d8dee6")
SOFT = colors.HexColor("#f4f7fa")
RED = colors.HexColor("#a53a34")


def register_fonts() -> tuple[str, str]:
    cn = "MicrosoftYaHei"
    en = "Arial"
    pdfmetrics.registerFont(TTFont(cn, r"C:\Windows\Fonts\msyh.ttc", subfontIndex=0))
    pdfmetrics.registerFont(TTFont(en, r"C:\Windows\Fonts\arial.ttf"))
    return cn, en


def image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as image:
        return image.size


def draw_cover(c: Canvas, path: Path, x: float, y: float, w: float, h: float) -> None:
    iw, ih = image_size(path)
    scale = max(w / iw, h / ih)
    sw, sh = iw * scale, ih * scale
    c.drawImage(ImageReader(path), x + (w - sw) / 2, y + (h - sh) / 2, sw, sh, mask="auto")


def draw_contain(c: Canvas, path: Path, x: float, y: float, w: float, h: float) -> None:
    iw, ih = image_size(path)
    scale = min(w / iw, h / ih)
    sw, sh = iw * scale, ih * scale
    c.drawImage(ImageReader(path), x + (w - sw) / 2, y + (h - sh) / 2, sw, sh, mask="auto")


def figure_box(w: float, h: float) -> tuple[float, float, float, float]:
    """Give embedded analytical figures enough area on both A3 and A0 sheets."""
    image_y = h * 0.36
    title_gap = 110 if w >= 1500 else 95
    image_top = h - title_gap
    return 42, image_y, w - 84, image_top - image_y


def wrap_lines(text: str, font: str, size: float, max_width: float) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph:
            lines.append("")
            continue
        current = ""
        for char in paragraph:
            candidate = current + char
            if current and pdfmetrics.stringWidth(candidate, font, size) > max_width:
                lines.append(current)
                current = char
            else:
                current = candidate
        if current:
            lines.append(current)
    return lines


def text_block(c: Canvas, text: str, x: float, y: float, width: float, font: str, size: float,
               leading: float | None = None, color: colors.Color = INK, max_lines: int | None = None) -> float:
    leading = leading or size * 1.45
    lines = wrap_lines(text, font, size, width)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        if lines:
            lines[-1] = lines[-1][:-1] + "…"
    c.setFont(font, size)
    c.setFillColor(color)
    cursor = y
    for line in lines:
        c.drawString(x, cursor, line)
        cursor -= leading
    return cursor


def title(c: Canvas, heading: str, subheading: str, w: float, h: float, font: str, index: int, total: int) -> None:
    c.setFillColor(PALE)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.rect(0, h - 84, w, 84, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, h - 84, 12, 84, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont(font, 24 if w < 1500 else 30)
    c.drawString(42, h - 40, heading)
    text_block(c, subheading, 42, h - 60, w - 180, font, 9 if w < 1500 else 12, 13 if w < 1500 else 17, colors.HexColor("#d9e2ec"), 2)
    c.setFont(font, 9 if w < 1500 else 12)
    c.drawRightString(w - 42, h - 40, f"REN BELT  /  {index:02d}—{total:02d}")


def footer(c: Canvas, w: float, font: str, note: str, english: bool = False) -> None:
    c.setStrokeColor(LINE)
    c.line(42, 30, w - 42, 30)
    c.setFont(font, 7.5 if w < 1500 else 10)
    c.setFillColor(MUTED)
    c.drawString(42, 15, note)
    right_note = "Concept proposal / provisional · not an official redline or approval conclusion" if english else "概念方案 / provisional · 不构成官方红线或审批结论"
    c.drawRightString(w - 42, 15, right_note)


def card(c: Canvas, x: float, y: float, w: float, h: float, heading: str, body: str, font: str,
         accent: colors.Color = ORANGE, body_size: float = 9) -> None:
    c.setFillColor(colors.white)
    c.setStrokeColor(LINE)
    c.roundRect(x, y, w, h, 8, fill=1, stroke=1)
    c.setFillColor(accent)
    c.rect(x, y + h - 5, w, 5, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont(font, body_size + 2)
    c.drawString(x + 12, y + h - 25, heading)
    text_block(c, body, x + 12, y + h - 45, w - 24, font, body_size, body_size * 1.45, INK, max_lines=max(2, int(h / (body_size * 1.45)) - 2))


def flow_strip(
    c: Canvas,
    w: float,
    h: float,
    font: str,
    english: bool,
    steps: list[tuple[str, str, colors.Color]],
    y: float,
    strip_height: float,
) -> None:
    """Show a compact handoff chain so each proposal has an observable gate."""
    gap = 10
    card_width = (w - 84 - gap * (len(steps) - 1)) / len(steps)
    body_size = 7.5 if w < 1500 else 11
    for i, (heading, body, accent) in enumerate(steps):
        x = 42 + i * (card_width + gap)
        card(c, x, y, card_width, strip_height, heading, body, font, accent, body_size)
        if i < len(steps) - 1:
            arrow_x = x + card_width + gap * 0.35
            c.setStrokeColor(MUTED)
            c.setLineWidth(1.2 if w < 1500 else 2)
            c.line(arrow_x - 5, y + strip_height / 2, arrow_x + 5, y + strip_height / 2)
            c.setFillColor(MUTED)
            c.setFont(font, body_size + 1)
            c.drawCentredString(arrow_x + 8, y + strip_height / 2 - 4, ">")


def metric(c: Canvas, x: float, y: float, w: float, value: str, label: str, font: str, accent: colors.Color = ORANGE) -> None:
    c.setFillColor(accent)
    c.setFont(font, 24 if w < 1500 else 35)
    c.drawString(x, y, value)
    text_block(c, label, x, y - 16 if w < 1500 else y - 22, 180 if w < 1500 else 300, font, 8 if w < 1500 else 12, 12 if w < 1500 else 17, MUTED, 2)


def cover_page(c: Canvas, w: float, h: float, font: str, english: bool) -> None:
    c.setFillColor(NAVY)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    photo = CTX / "qinglongqiao-station.jpg"
    draw_cover(c, photo, w * 0.53, 0, w * 0.47, h)
    c.setFillColor(colors.Color(0.05, 0.09, 0.15, alpha=0.76))
    c.rect(w * 0.53, 0, w * 0.47, h, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(42, h - 118, 96, 6, fill=1, stroke=0)
    c.setFillColor(colors.white)
    if english:
        heading = "CENTENNIAL JING-ZHANG\nREN BELT"
        sub = "A human-centred AI innovation belt for Haidian"
        body = "One heritage spine · three civic stations · two complementary wings\n1905 / 1949 / 2019 / 2026"
        caveat = "Concept design package | Provisional geometry, public evidence, offline deliverables"
    else:
        heading = "百年京张·人带\nREN BELT"
        sub = "以人为核心的 AI 创新带城市设计"
        body = "一脉遗产主轴 · 三站公共节点 · 人字双翼协同\n1905 / 1949 / 2019 / 2026"
        caveat = "概念方案包｜临时几何、公开证据、离线成果"
    y = h - 210
    c.setFont(font, 36 if w < 1500 else 58)
    for line in heading.split("\n"):
        c.drawString(42, y, line)
        y -= 48 if w < 1500 else 72
    c.setFillColor(colors.HexColor("#b7d8c6"))
    c.setFont(font, 16 if w < 1500 else 24)
    text_block(c, sub, 42, y - 12, w * 0.43, font, 16 if w < 1500 else 24, 25 if w < 1500 else 35, colors.HexColor("#b7d8c6"), 3)
    text_block(c, body, 42, y - 100 if w < 1500 else y - 145, w * 0.42, font, 12 if w < 1500 else 18, 19 if w < 1500 else 27, colors.white, 4)
    c.setFillColor(colors.HexColor("#d9e2ec"))
    text_block(c, caveat, 42, 55, w * 0.42, font, 9 if w < 1500 else 13, 13 if w < 1500 else 18, colors.HexColor("#d9e2ec"), 2)


def overview_page(c: Canvas, w: float, h: float, font: str, english: bool, index: int, total: int) -> None:
    title(c, "01  OVERVIEW" if english else "01  总览", "一脉三站·一字双翼；地图底图仅为位置参照，边界为 provisional design frame。" if not english else "One spine, three stations and two wings; the map is locational reference only and the boundary is provisional.", w, h, font, index, total)
    img = FIG / ("site-overview.en.png" if english else "site-overview.png")
    draw_contain(c, img, *figure_box(w, h))
    gap = 14
    cw = (w - 84 - gap * 2) / 3
    cards = [("Design judgement" if english else "设计判断", "Heritage spine as everyday public space; three stations carry production, community and culture." if english else "遗产主轴转译为日常公共空间；三站承载生产、社区与文化。", ORANGE), ("Boundary status" if english else "边界状态", "Provisional / not an official red line; replace authoritative geometry before approval." if english else "Provisional／非官方红线；审批前替换为权威几何。", RED), ("Three-level scope" if english else "三层范围", "43.6 km² coordination / 11.4 km² design / 9 km heritage spine." if english else "43.6 km² 统筹／11.4 km² 设计／9 km 遗产主轴。", BLUE)]
    for i, (head, body, accent) in enumerate(cards):
        card(c, 42 + i * (cw + gap), h * 0.16, cw, h * 0.20, head, body + ("\nPilot first; recalculate after official data replacement." if english else "\n先试点；官方资料替换后复算。"), font, accent, 9 if w < 1500 else 13)
    footer(c, w, font, "Sources: geometry/*.geojson · metrics.json · OSM contributors (locational reference)", english)


def landuse_page(c: Canvas, w: float, h: float, font: str, english: bool, index: int, total: int) -> None:
    title(c, "02  LAND USE + KEY AREAS" if english else "02  用地与重点区", "Three key areas make the belt legible and phaseable." if english else "三区形成可识别、可分期的空间骨架。", w, h, font, index, total)
    img = FIG / ("land-use-structure.en.png" if english else "land-use-structure.png")
    draw_contain(c, img, *figure_box(w, h))
    names = [("众智园 / ZHONGZHI", "AI governance, public computing and blue-green testing", "AI 治理、公共算力与蓝绿测试"), ("原点社区 / ORIGIN", "Open-source exchange, learning and neighbourhood services", "开源交往、学习与邻里服务"), ("大钟寺 / DAZHONGSI", "Heritage gateway, culture and international dialogue", "遗产门户、文化与国际交流")]
    gap = 14
    cw = (w - 84 - gap * 2) / 3
    for i, (head, en, cn) in enumerate(names):
        body = en if english else cn
        card(c, 42 + i * (cw + gap), h * 0.12, cw, h * 0.24, head, body + ("\n\nPublic-space anchor · local operator · measurable acceptance\nConcept only; subject to planning, ownership and heritage review." if english else "\n\n公共空间锚点·属地运营者·可量化验收\n概念建议，需结合控规、权属与文保条件深化。"), font, [GREEN, ORANGE, GOLD][i], 9 if w < 1500 else 13)
    footer(c, w, font, "Layers: land_use.geojson · key_areas.geojson · phasing.geojson", english)


def mobility_page(c: Canvas, w: float, h: float, font: str, english: bool, index: int, total: int) -> None:
    title(c, "03  MOBILITY + BLUE-GREEN" if english else "03  交通与蓝绿", "A visible, safe and low-carbon public-space loop." if english else "形成可见、安全、低碳的公共空间循环。", w, h, font, index, total)
    img = FIG / ("mobility-bluegreen.en.png" if english else "mobility-bluegreen.png")
    draw_contain(c, img, *figure_box(w, h))
    cards = [("Daily movement" if english else "日常移动", "Continuous walking and cycling links; transit interfaces are wayfinding anchors." if english else "连续步行与骑行联系；公共交通接口作为导视锚点。", BLUE), ("Blue-green repair" if english else "蓝绿修复", "Shade, rainwater detention and maintenance routes are designed together." if english else "遮荫、雨洪调蓄与维护通道一体设计。", GREEN), ("Guardrail" if english else "边界条件", "Road lines, utilities, flood control and heritage protection require professional review." if english else "道路红线、市政管线、防洪与文保必须经专业复核。", RED)]
    gap = 14
    cw = (w - 84 - gap * 2) / 3
    for i, (head, body, accent) in enumerate(cards):
        card(c, 42 + i * (cw + gap), h * 0.12, cw, h * 0.24, head, body + ("\n\nPrioritise the spine before adding smart devices." if english else "\n\n先贯通主轴，再叠加智能设备。"), font, accent, 9 if w < 1500 else 13)
    footer(c, w, font, "Layers: roads.geojson · public_space.geojson · site_boundary.geojson (provisional)", english)


def scenarios_page(c: Canvas, w: float, h: float, font: str, english: bool, index: int, total: int) -> None:
    title(c, "04  SCENARIOS" if english else "04  场景与运营", "Twelve scenarios are tied to space, operators, guardrails and acceptance checks." if english else "12 个场景均绑定空间载体、运营者、护栏与验收。", w, h, font, index, total)
    items_en = [("01 Open-source hall", "Origin community · publish and collaborate"), ("02 Safety sandbox", "Zhongzhi · evaluate and govern"), ("03 Edge-compute station", "Belt nodes · public capacity"), ("04 AI slow-mobility guide", "Heritage spine · accessible wayfinding"), ("05 Global pitch lounge", "Dazhongsi · exchange and showcase"), ("06 Qinghe low-carbon corridor", "Blue-green repair and cycling"), ("07 Campus transfer street", "Prototype, IP and investment"), ("08 Data commons lounge", "Authorised and auditable exchange"), ("09 AI life-service street", "Care, education and daily services"), ("10 Global AI Belt Week", "A walkable annual programme"), ("11 Journey-to-Beijing guide", "Railway memory and learning"), ("12 Human-shaped plaza art", "Public art with a clear off switch")]
    items_cn = [("01 开源发布厅", "原点社区·发布与协作"), ("02 安全治理沙盒", "众智园·评测与治理"), ("03 端侧算力驿站", "带状节点·公共算力"), ("04 AI 慢行导航", "遗产主轴·无障碍导视"), ("05 国际路演客厅", "大钟寺·交流与展示"), ("06 清河低碳创新廊", "蓝绿修复与骑行"), ("07 近校成果转化街", "原型、知识产权与投融资"), ("08 数据要素会客厅", "授权、可审计流通"), ("09 AI 生活服务样板街", "照护、教育与日常服务"), ("10 全球 AI 活动周路线", "可步行的年度活动"), ("11 进京赶考数字导览", "铁路记忆与学习"), ("12 人字广场智能艺术", "可关闭的公共艺术")]
    items = items_en if english else items_cn
    gap = 10
    cols = 3
    cw = (w - 84 - gap * 2) / cols
    ch = h * 0.115
    y = h * 0.72
    for i, (head, body) in enumerate(items):
        col, row = i % cols, i // cols
        x = 42 + col * (cw + gap)
        yy = y - row * (ch + gap)
        card(c, x, yy, cw, ch, head, body + ("\nHuman review, privacy boundary and exit path." if english else "\n人工复核、隐私边界与退出路径。"), font, [ORANGE, GREEN, BLUE][i % 3], 8.5 if w < 1500 else 12)
    flow_steps = (
        [("SPACE", "Anchor and access", BLUE), ("OPERATOR", "Named steward", GREEN), ("GUARDRAIL", "Privacy + safety", RED), ("ACCEPT", "Measure + appeal", GOLD)]
        if english
        else [("空间", "明确载体与入口", BLUE), ("运营", "明确责任人", GREEN), ("护栏", "隐私与安全", RED), ("验收", "指标与申诉", GOLD)]
    )
    flow_strip(c, w, h, font, english, flow_steps, h * 0.08, h * 0.10)
    footer(c, w, font, "Evidence: scenario-operations-matrix.json · human takeover and non-digital access are mandatory", english)


def implementation_page(c: Canvas, w: float, h: float, font: str, english: bool, index: int, total: int) -> None:
    title(c, "05  BRAND + DELIVERY" if english else "05  品牌与实施", "A repeatable identity system turns the heritage narrative into an operating promise." if english else "可复用的识别系统，把遗产叙事转成运营承诺。", w, h, font, index, total)
    # Human-shaped mark, drawn directly to keep the PDF fully offline.
    c.setStrokeColor(GOLD)
    c.setLineWidth(12 if w < 1500 else 18)
    c.line(70, h * 0.72, 145, h * 0.58)
    c.line(220, h * 0.72, 145, h * 0.58)
    c.line(145, h * 0.58, 145, h * 0.36)
    c.setFillColor(NAVY)
    c.setFont(font, 28 if w < 1500 else 42)
    c.drawString(70, h * 0.78, "REN BELT")
    text_block(c, "One mark / one spine / many human-scale services" if english else "一个标记／一条主轴／多种以人为尺度的服务", 70, h * 0.32, w * 0.34, font, 11 if w < 1500 else 16, 16 if w < 1500 else 23, MUTED, 3)
    x = w * 0.43
    stages = [
        (
            "Near term 2026–2030" if english else "近期 2026–2030",
            "Connect the heritage park and pilot the origin plaza.\nOwner: district + park operator · Gate: heritage/access review · Stop: restore manual service"
            if english
            else "贯通遗产公园并试点原点广场。\n责任：属地+公园运营 · 门槛：文保/可达性复核 · 退出：恢复人工服务",
        ),
        (
            "Mid term 2030–2035" if english else "中期 2030–2035",
            "Scale the blue-green corridor and station interfaces.\nOwner: municipal partners · Gate: flood/traffic review · Stop: pause at safety threshold"
            if english
            else "扩展蓝绿廊道与站点接口。\n责任：市政协同单位 · 门槛：防洪/交通复核 · 退出：触及安全阈值即暂停",
        ),
        (
            "Long term 2035–2040" if english else "远期 2035–2040",
            "Open the governance sandbox only after independent audit and public consent.\nOwner: authorised operator · Gate: privacy/fairness audit · Stop: disable automated decision"
            if english
            else "独立审计与公众同意后再开放治理沙盒。\n责任：授权运营者 · 门槛：隐私/公平审计 · 退出：关闭自动化决策",
        ),
    ]
    for i, (head, body) in enumerate(stages):
        card(c, x, h * 0.66 - i * h * 0.19, w * 0.52, h * 0.16, head, body + ("\nOwner / dependency / acceptance / stop condition are recorded for each project." if english else "\n每项工程均登记责任、依赖、验收与退出条件。"), font, [ORANGE, GREEN, BLUE][i], 10 if w < 1500 else 14)
    card(c, 70, h * 0.10, w * 0.32, h * 0.16, "Brand promise" if english else "品牌承诺", "Heritage is not a backdrop: it is a public operating system for learning, exchange and care.\nOPEN · HUMAN · REPEATABLE" if english else "遗产不是背景布景，而是用于学习、交往与照护的公共运营系统。\n开放 · 以人为本 · 可复用", font, GOLD, 9 if w < 1500 else 13)
    card(c, x, h * 0.10, w * 0.52, h * 0.12, "Delivery gate" if english else "实施闸门", "Reversible pilot → monitored service → independent audit → accountable scale." if english else "可逆试点 → 监测运营 → 独立审计 → 责任化扩展。", font, BLUE, 9 if w < 1500 else 13)
    footer(c, w, font, "Evidence: ren-belt-brand-sheet.svg · renewal-implementation-cards.json · annual-operations.json", english)


def inclusion_page(c: Canvas, w: float, h: float, font: str, english: bool, index: int, total: int) -> None:
    title(c, "06  INCLUSION + METRICS" if english else "06  包容性与指标", "No service requires a smartphone, payment or continuous location tracking." if english else "任何服务不以手机、支付或持续定位为前提。", w, h, font, index, total)
    img = FIG / ("metrics-evidence.en.png" if english else "metrics-evidence.png")
    draw_contain(c, img, *figure_box(w, h))
    groups = [("Accessibility" if english else "残障人士", "Continuous accessible paths, tactile/audio wayfinding, 48h complaint closure.", GREEN), ("Low-income users" if english else "低收入群体", "Free public space, transparent prices and ≥20% public-interest quota.", ORANGE), ("Care + night work" if english else "照护与夜间工作", "Care points, toilets, water, safe lighting and human night response.", BLUE), ("Digital exclusion" if english else "数字弱势", "Paper, phone and staffed service desks run in parallel with digital tools.", RED)]
    gap = 14
    cw = (w - 84 - gap * 3) / 4
    for i, (head, body_en, accent) in enumerate(groups):
        body = body_en if english else ["连续无障碍路径、触觉/语音导视、48 小时投诉闭环。", "免费公共空间、价格透明、公益名额 ≥20%。", "照护点、厕所、饮水、安全照明与夜间人工响应。", "纸质、电话与人工服务台和数字工具并行。"][i]
        card(c, 42 + i * (cw + gap), h * 0.12, cw, h * 0.24, head, body + ("\n\nAnnual audit by user group." if english else "\n\n按群体开展年度审计。"), font, accent, 8.5 if w < 1500 else 12)
    footer(c, w, font, "Metrics are recalculable from GeoJSON; boundary and key areas remain provisional until official data arrives.", english)


def evidence_page(c: Canvas, w: float, h: float, font: str, english: bool, index: int, total: int) -> None:
    title(c, "07  EVIDENCE + NEXT STEP" if english else "07  证据与下一步", "A reviewable package: sources, assumptions, geometry, drawings and self-checks travel together." if english else "可审查的成果包：来源、假设、几何、图纸与自检结果一起交付。", w, h, font, index, total)
    boxes = [
        ("Evidence chain" if english else "证据链", "Public facts are cited in sources.json; downloaded context images carry credits; OSM is explicitly labelled as locational reference." if english else "公开事实登记于 sources.json；下载图像附来源与版权说明；OSM 明确标注为位置参照。", BLUE),
        ("Replace + recalculate" if english else "替换与复算", "Replace provisional boundary, key areas, road lines and utilities with authoritative data, then rerun spatial review and refresh all hashes." if english else "替换临时边界、重点区、道路红线与市政数据后，重新运行空间复核并刷新全部哈希。", ORANGE),
        ("Stop conditions" if english else "停止条件", "Safety, flood control, heritage, privacy or fairness failure pauses the pilot and restores a staffed/manual service." if english else "安全、防洪、文保、隐私或公平性不达标即暂停试点，恢复人工/线下服务。", RED),
        ("Decision gate" if english else "决策门槛", "This is a concept package for professional teams. No area, investment or implementation claim is an approval conclusion." if english else "本包仅供专业团队深化；面积、投资与实施均不构成审批结论。", GREEN),
    ]
    gap = 16
    cw = (w - 84 - gap) / 2
    ch = h * 0.20
    for i, (head, body, accent) in enumerate(boxes):
        col, row = i % 2, i // 2
        card(c, 42 + col * (cw + gap), h * 0.56 - row * (ch + gap), cw, ch, head, body, font, accent, 10 if w < 1500 else 15)
    flow_steps = (
        [("SOURCES", "cited", BLUE), ("ASSUMPTIONS", "qualified", ORANGE), ("GEOMETRY", "provisional", GOLD), ("DRAWINGS", "rendered", GREEN), ("CHECKS", "re-run", RED), ("OFFICIAL DATA", "replace + recalc", NAVY)]
        if english
        else [("来源", "登记可核查", BLUE), ("假设", "标注适用性", ORANGE), ("几何", "保持临时", GOLD), ("图纸", "离线生成", GREEN), ("复核", "重新运行", RED), ("官方数据", "替换并复算", NAVY)]
    )
    flow_strip(c, w, h, font, english, flow_steps, h * 0.24, h * 0.09)
    c.setFillColor(NAVY)
    c.setFont(font, 18 if w < 1500 else 26)
    c.drawString(42, h * 0.19, "Submission contents" if english else "提交包内容")
    files = "proposal.md · proposal.en.md · visual/index.html · geometry/*.geojson · assets/figures/*.png · drawings/*.pdf · report/*.json"
    text_block(c, files, 42, h * 0.15, w - 84, font, 10 if w < 1500 else 15, 16 if w < 1500 else 22, INK, 3)
    footer(c, w, font, "REN BELT / 2026 · Offline-first deliverables · self-check claim is only set after validation", english)


def build_pdf(path: Path, english: bool, pagesize: tuple[float, float], landscape_mode: bool) -> None:
    font_cn, font_en = register_fonts()
    font = font_en if english else font_cn
    w, h = pagesize
    c = Canvas(str(path), pagesize=pagesize, pageCompression=1)
    pages = [cover_page, overview_page, landuse_page, mobility_page, scenarios_page, implementation_page, inclusion_page, evidence_page]
    # Eight pages make both the booklet and board set readable instead of compressing evidence into blank/overcrowded sheets.
    for i, page in enumerate(pages, 1):
        if page is cover_page:
            page(c, w, h, font, english)
        else:
            page(c, w, h, font, english, i, len(pages))
        c.showPage()
    c.save()


def main() -> None:
    parser = argparse.ArgumentParser(description="Build offline REN BELT A3/A0 drawing packages.")
    parser.add_argument("--english", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    suffix = ".en" if args.english else ""
    build_pdf(OUT / f"a3-booklet{suffix}.pdf", args.english, A3, False)
    build_pdf(OUT / f"a0-boards{suffix}.pdf", args.english, landscape(A0), True)
    print(f"wrote A3/A0 PDFs ({'English' if args.english else 'Chinese'})")


if __name__ == "__main__":
    main()
