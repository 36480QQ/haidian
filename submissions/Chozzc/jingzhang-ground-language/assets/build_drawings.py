#!/usr/bin/env python3
"""Build paired A3 booklets and A0 boards, then verify PDF size and page count."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont
from pypdf import PdfReader
from reportlab.lib.pagesizes import A0, A3, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas


ROOT = Path(__file__).resolve().parents[1]
FIG, MEDIA, OUT = ROOT / "assets" / "figures", ROOT / "assets" / "media", ROOT / "drawings"
INK, PAPER, AMBER, CYAN, GREEN, MUTED = "#17201f", "#f3f0e9", "#e5a32d", "#3f8f9a", "#5d816f", "#67716e"


def font(size, bold=False):
    options = [
        Path("C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for path in options:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def wrap(draw, value, width, size):
    units = value.split() if " " in value else list(value)
    sep = " " if " " in value else ""
    lines, current = [], ""
    for unit in units:
        candidate = f"{current}{sep if current else ''}{unit}"
        if draw.textlength(candidate, font=font(size)) <= width or not current:
            current = candidate
        else:
            lines.append(current)
            current = unit
    if current:
        lines.append(current)
    return lines


def add_text(draw, box, value, size, fill=INK, bold=False, leading=1.35, max_lines=None):
    x, y, x2, _ = box
    lines = wrap(draw, value, x2 - x, size)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=font(size, bold), fill=fill)
        y += int(size * leading)
    return y


def blank(size, kicker, title, subtitle, page_no):
    w, h = size
    im = Image.new("RGB", size, PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, int(w * .018), h), fill=AMBER)
    d.text((int(w * .05), int(h * .055)), kicker, font=font(int(h * .024), True), fill=AMBER)
    d.text((int(w * .05), int(h * .095)), title, font=font(int(h * .054), True), fill=INK)
    d.text((int(w * .05), int(h * .17)), subtitle, font=font(int(h * .022)), fill=MUTED)
    d.line((int(w * .05), int(h * .22), int(w * .95), int(h * .22)), fill="#c8c4bb", width=2)
    d.text((int(w * .93), int(h * .945)), f"JZ.GL / {page_no:02d}", font=font(int(h * .016), True), fill=MUTED)
    return im, d


def paste_fit(dst, src_path, box, crop=False):
    src = Image.open(src_path).convert("RGB")
    x, y, x2, y2 = box
    bw, bh = x2 - x, y2 - y
    ratio = max(bw / src.width, bh / src.height) if crop else min(bw / src.width, bh / src.height)
    src = src.resize((int(src.width * ratio), int(src.height * ratio)), Image.Resampling.LANCZOS)
    if crop:
        sx, sy = max(0, (src.width - bw) // 2), max(0, (src.height - bh) // 2)
        src = src.crop((sx, sy, sx + bw, sy + bh))
        dst.paste(src, (x, y))
    else:
        dst.paste(src, (x + (bw - src.width) // 2, y + (bh - src.height) // 2))


def cover(size, lang, kind):
    zh = lang == "zh"
    w, h = size
    cover = Image.open(MEDIA / "ground-language-cover.png").convert("RGB")
    ratio = max(w / cover.width, h / cover.height)
    cover = cover.resize((int(cover.width * ratio), int(cover.height * ratio)), Image.Resampling.LANCZOS)
    cover = cover.crop(((cover.width - w) // 2, 0, (cover.width - w) // 2 + w, h))
    cover = ImageEnhance.Brightness(cover).enhance(.58)
    d = ImageDraw.Draw(cover, "RGBA")
    d.rectangle((0, 0, int(w * .48), h), fill=(12, 23, 21, 225))
    d.rectangle((int(w * .055), int(h * .18), int(w * .065), int(h * .82)), fill=AMBER)
    x = int(w * .095)
    d.text((x, int(h * .17)), "ONE LINE · THREE TRANSLATIONS · SIX WORDS", font=font(int(h * .022), True), fill="#f1b74e")
    title = "京张地语" if zh else "GROUND\nLANGUAGE"
    d.multiline_text((x, int(h * .25)), title, font=font(int(h * (.105 if zh else .085)), True), fill="white", spacing=5)
    strap = "让机器在公共空间遵守\n人能看懂的规则" if zh else "PUBLIC-SPACE RULES\nPEOPLE CAN UNDERSTAND\nAND MACHINES MUST OBEY"
    d.multiline_text((x, int(h * (.44 if zh else .48))), strap, font=font(int(h * .035), True), fill="#eeeae0", spacing=int(h * .012))
    d.text((x, int(h * .84)), "Chozzc × OpenAI Codex (GPT-5)", font=font(int(h * .018), True), fill="white")
    note = "概念氛围，非现场或工程证据" if zh else "CONCEPT ATMOSPHERE - NOT SITE OR ENGINEERING EVIDENCE"
    d.text((x, int(h * .89)), note, font=font(int(h * .014)), fill="#ddd8cd")
    d.text((int(w * .88), int(h * .94)), kind, font=font(int(h * .016), True), fill="white")
    return cover


def booklet_pages(lang):
    zh, size = lang == "zh", (2100, 1485)
    suffix = "" if zh else ".en"
    pages = [cover(size, lang, "A3 BOOKLET")]
    specs = [
        ("01 / OPEN GRAMMAR", "六词，三种翻译" if zh else "SIX WORDS, THREE TRANSLATIONS", "视觉、触觉和机器读取同一公共状态" if zh else "Visual, tactile and machine readings share one public state", "land-use-structure"),
        ("02 / VALIDATION CHAIN", "三区两翼" if zh else "THREE FIELDS, TWO WINGS", "众智园验证、原点共读、大钟寺交接" if zh else "Validate at Zhongzhiyuan, co-read at AI Origin, hand over at Dazhongsi", "key-areas"),
        ("03 / EVERYDAY USE", "十二场景，八类使用者" if zh else "TWELVE SCENARIOS, EIGHT USER GROUPS", "前三景做产业验证，九景检验日常公平" if zh else "Three industrial tests and nine everyday equity scenarios", "mobility-bluegreen"),
        ("04 / REVERSIBLE PILOT", "先验证，再扩展" if zh else "TEST FIRST, THEN DECIDE", "100-200 米、有人值守、可撤回" if zh else "100-200 metres, staffed and removable", "metrics-evidence"),
    ]
    for i, (k, title, sub, stem) in enumerate(specs, 2):
        im, _ = blank(size, k, title, sub, i)
        paste_fit(im, FIG / f"{stem}{suffix}.png", (100, 350, 2000, 1335))
        pages.append(im)

    im, d = blank(size, "05 / CIVIC LANDMARKS", "三个公共地标" if zh else "THREE PUBLIC LANDMARKS", "把机器规则变成可触摸、可讨论的京张文化" if zh else "Make machine rules tangible and debatable within Jing-Zhang culture", 6)
    landmarks = ([('让行标', '机器先让人：走廊的公共承诺'), ('地语零号碑', '公开六词版本、测试方法与修改历史'), ('交接钟', '人工接管或重大更新成为可感知时刻')] if zh else
                 [('YIELD MARKER', 'Machines yield first: the corridor covenant'), ('STONE ZERO', 'Publish the grammar, tests and revision history'), ('HANDOVER BELL', 'Make takeover and major updates perceptible')])
    for j, (name, desc) in enumerate(landmarks):
        x = 105 + j * 665
        color = [AMBER, CYAN, GREEN][j]
        d.ellipse((x + 100, 420, x + 455, 775), fill=color)
        d.text((x + 277, 597), str(j + 1), font=font(95, True), fill="white", anchor="mm")
        d.text((x + 277, 850), name, font=font(42, True), fill=INK, anchor="mm")
        add_text(d, (x + 45, 925, x + 520, 1180), desc, 26, MUTED, False, 1.45, 4)
    add_text(d, (110, 1250, 1960, 1380), "可逆装置，不附着于未经核实的铁路遗产本体，不替代法定标志。" if zh else "Reversible installations; never attach to unverified railway heritage fabric or replace statutory signs.", 24, "#8a4d35", True)
    pages.append(im)

    im, d = blank(size, "06 / EVIDENCE BOUNDARY", "证据边界与专业深化" if zh else "EVIDENCE BOUNDARIES AND NEXT WORK", "临时几何支持概念评审，不支持审批或工程结论" if zh else "Provisional geometry supports concept review, not approval or engineering claims", 7)
    warnings = (["官方范围与重点区 polygon 缺失", "大钟寺临时质心存在约 2.26 km 定位问题", "道路、地块、建筑、遗产、市政调查缺失", "容积率、拆改留和工程量保持未知"] if zh else
                ["Official scope and key-area polygons are absent", "The provisional Dazhongsi centroid has a known ~2.26 km location issue", "Road, parcel, building, heritage and utility surveys are absent", "FAR, retain-renovate-demolish quantities and engineering quantities remain unknown"])
    for j, warning in enumerate(warnings):
        y = 400 + j * 185
        d.rounded_rectangle((120, y, 1980, y + 130), 22, fill="white", outline="#d6d0c5", width=2)
        d.ellipse((155, y + 35, 215, y + 95), fill=AMBER)
        d.text((185, y + 65), "!", font=font(35, True), fill=INK, anchor="mm")
        add_text(d, (250, y + 30, 1920, y + 115), warning, 29, INK, True, 1.3, 2)
    add_text(d, (120, 1190, 1980, 1360), "下一步：官方数据 - 使用者共创 - 材料与识读测试 - 多专业审查 - 独立安全放行。" if zh else "Next: official data - user co-design - material and reading tests - multidisciplinary review - independent safety release.", 28, GREEN, True)
    pages.append(im)

    im, d = blank(size, "07 / OPEN VALUE", "一份可被公众否决的机器契约" if zh else "A MACHINE COVENANT THE PUBLIC CAN REJECT", "机器可以更新，公共原则不能静默改写" if zh else "Technology may update; public principles may not change silently", 8)
    quote = "人优先 · 无身份可用 · 失败可见 · 责任可追溯" if zh else "HUMAN PRIORITY · IDENTITY-FREE ACCESS · VISIBLE FAILURE · ACCOUNTABLE RESPONSIBILITY"
    add_text(d, (120, 390, 1980, 650), quote, 60 if zh else 46, AMBER, True, 1.4, 3)
    body = ("若试验失败，地面可以恢复；若试验成功，城市获得的不是专有设施，而是一层开放、可复制、可审计的公共 AI 基础设施。" if zh else
            "If the test fails, the ground can be restored. If it succeeds, the city gains an open, replicable and auditable layer of public AI infrastructure rather than a proprietary facility.")
    add_text(d, (120, 715, 1900, 960), body, 38, INK, False, 1.55, 5)
    sources = ("公开案例：日本与英国触觉铺装指引、MTA Accessible Station Lab、ITU-T F.921、AprilTag、ISO/TR 4448-1、Open-RMF、Boston 配送机器人试验。完整链接与适用边界见 sources.json。" if zh else
               "Public cases: Japanese and UK tactile guidance, MTA Accessible Station Lab, ITU-T F.921, AprilTag, ISO/TR 4448-1, Open-RMF and Boston's delivery-robot pilot. Full links and limits are in sources.json.")
    add_text(d, (120, 1050, 1900, 1300), sources, 25, MUTED, False, 1.45, 6)
    pages.append(im)
    return pages


def board_pages(lang):
    zh, size = lang == "zh", (3508, 2480)
    suffix = "" if zh else ".en"
    pages = [cover(size, lang, "A0 BOARD 01 / 03")]
    im, d = blank(size, "BOARD 02 / SYSTEM", "六词语法与三区两翼" if zh else "SIX-WORD GRAMMAR AND VALIDATION CHAIN", "从共同识读到真实运营的开放试验链" if zh else "An open validation chain from co-reading to real operations", 2)
    paste_fit(im, FIG / f"land-use-structure{suffix}.png", (150, 470, 1750, 1500))
    paste_fit(im, FIG / f"key-areas{suffix}.png", (1780, 470, 3358, 1500))
    paste_fit(im, FIG / f"mobility-bluegreen{suffix}.png", (700, 1570, 2808, 2260))
    pages.append(im)
    im, d = blank(size, "BOARD 03 / DELIVERY", "可撤回试点与证据边界" if zh else "REVERSIBLE PILOT AND EVIDENCE BOUNDARY", "100-200 米先验证；不以伪精确替代专业深化" if zh else "Validate 100-200 metres first; never substitute false precision for professional work", 3)
    paste_fit(im, FIG / f"metrics-evidence{suffix}.png", (150, 470, 2100, 1700))
    points = (["七道放行门共同决定是否进入公共空间", "不采集人脸、设备身份或连续轨迹", "官方边界、道路、地块、遗产与市政资料待补", "大钟寺仅作片区功能表达，禁止具体站点落位", "失败即回滚；成功以开放版本进入下一阶段"] if zh else
              ["Seven release gates jointly decide public entry", "No faces, device identities or continuous trajectories", "Official boundary, road, parcel, heritage and utility data remain pending", "Dazhongsi is programme logic only, with no station-level placement", "Failure triggers rollback; success advances through an open version"])
    for j, point in enumerate(points):
        y = 500 + j * 285
        d.rounded_rectangle((2200, y, 3350, y + 210), 30, fill="white", outline="#d6d0c5", width=3)
        d.ellipse((2250, y + 62, 2335, y + 147), fill=AMBER)
        d.text((2292, y + 105), str(j + 1), font=font(40, True), fill=INK, anchor="mm")
        add_text(d, (2380, y + 42, 3290, y + 180), point, 34, INK, True, 1.35, 3)
    add_text(d, (190, 1910, 3270, 2240), "机器可以更新，公共原则不能静默改写。" if zh else "TECHNOLOGY MAY UPDATE. PUBLIC PRINCIPLES MAY NOT CHANGE SILENTLY.", 68, AMBER, True, 1.3, 3)
    pages.append(im)
    return pages


def write_pdf(path, pages, page_size):
    page_w, page_h = landscape(page_size)
    canvas = Canvas(str(path), pagesize=(page_w, page_h), pageCompression=1)
    for page in pages:
        buf = BytesIO()
        page.save(buf, format="JPEG", quality=92, optimize=True)
        buf.seek(0)
        canvas.drawImage(ImageReader(buf), 0, 0, page_w, page_h)
        canvas.showPage()
    canvas.save()


def main():
    OUT.mkdir(exist_ok=True)
    outputs = []
    for lang in ("zh", "en"):
        suffix = "" if lang == "zh" else ".en"
        a3 = OUT / f"a3-booklet{suffix}.pdf"
        a0 = OUT / f"a0-boards{suffix}.pdf"
        write_pdf(a3, booklet_pages(lang), A3)
        write_pdf(a0, board_pages(lang), A0)
        outputs += [(a3, 8, landscape(A3)), (a0, 3, landscape(A0))]
    for path, count, expected_size in outputs:
        reader = PdfReader(path)
        assert len(reader.pages) == count, path
        box = reader.pages[0].mediabox
        actual = (float(box.width), float(box.height))
        assert all(abs(a - b) < 1 for a, b in zip(actual, expected_size)), (path, actual)
    print("PASS: built 2 paired A3 booklets (8 pages) and 2 paired A0 board sets (3 pages)")


if __name__ == "__main__":
    main()
