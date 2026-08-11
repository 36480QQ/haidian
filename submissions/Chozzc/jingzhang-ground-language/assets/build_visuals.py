#!/usr/bin/env python3
"""Build paired proposal figures from the submission's structured model."""

from __future__ import annotations

import json
import html
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "assets" / "figures"
DATA = ROOT / "assets" / "data"
MEDIA = ROOT / "assets" / "media"
W, H = 1600, 1000
INK, PAPER, AMBER, CYAN, GREEN, MUTED = (
    "#17201f", "#f3f0e9", "#e5a32d", "#3f8f9a", "#5d816f", "#67716e"
)


def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def font(size: int, bold: bool = False):
    candidates = [
        Path("C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def text(draw, xy, value, size, fill=INK, bold=False, anchor=None):
    draw.text(xy, value, font=font(size, bold), fill=fill, anchor=anchor)


def wrap(draw, value, width, size, max_lines=3):
    if " " in value:
        lines, current = [], ""
        for word in value.split():
            candidate = f"{current} {word}".strip()
            if draw.textlength(candidate, font=font(size)) <= width or not current:
                current = candidate
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return "\n".join(lines[:max_lines])
    lines, current = [], ""
    for char in value:
        candidate = current + char
        if draw.textlength(candidate, font=font(size)) <= width:
            current = candidate
        else:
            lines.append(current)
            current = char
    if current:
        lines.append(current)
    return "\n".join(lines[:max_lines])


def base(kicker, title, subtitle):
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 28, H), fill=AMBER)
    text(d, (80, 62), kicker.upper(), 24, AMBER, True)
    text(d, (80, 105), title, 54, INK, True)
    text(d, (80, 178), subtitle, 25, MUTED)
    d.line((80, 225, 1520, 225), fill="#c8c4bb", width=2)
    return im, d


def save(im, stem, lang):
    path = FIG / f"{stem}{'.en' if lang == 'en' else ''}.png"
    im.save(path, optimize=True)
    return path


def overview(lang):
    zh = lang == "zh"
    cover = Image.open(MEDIA / "ground-language-cover.png").convert("RGB")
    scale = max(W / cover.width, H / cover.height)
    cover = cover.resize((int(cover.width * scale), int(cover.height * scale)))
    left = (cover.width - W) // 2
    im = cover.crop((left, 0, left + W, H))
    im = ImageEnhance.Brightness(im).enhance(0.62)
    d = ImageDraw.Draw(im, "RGBA")
    d.rectangle((0, 0, 735, H), fill=(16, 25, 24, 220))
    d.rectangle((70, 72, 88, 910), fill=AMBER)
    text(d, (132, 90), "JING-ZHANG GROUND LANGUAGE", 23, "#f1b74e", True)
    text(d, (132, 150), "京张地语" if zh else "GROUND\nLANGUAGE", 78, "white", True)
    subtitle = "让机器在公共空间遵守\n人能看懂的规则" if zh else "Public-space rules\npeople can understand\nand machines must obey"
    text(d, (132, 365 if zh else 350), subtitle, 35, "#e8e7df", True)
    labels = ["一线 / 1 LINE", "三译 / 3 TRANSLATIONS", "六词 / 6 WORDS", "十二景 / 12 SCENARIOS"]
    for i, label in enumerate(labels):
        y = 585 + i * 70
        d.rounded_rectangle((132, y, 625, y + 48), radius=24, fill=(255, 255, 255, 32), outline=(255, 255, 255, 90))
        text(d, (158, y + 12), label, 21, "white", True)
    text(d, (132, 894), "概念氛围，非现场证据" if zh else "CONCEPT ATMOSPHERE — NOT SITE EVIDENCE", 18, "#ddd8cd")
    return save(im, "site-overview", lang)


def glyphs(lang):
    zh = lang == "zh"
    model = load("ground-language.json")
    im, d = base(
        "01 / OPEN GRAMMAR",
        "六词，三种翻译" if zh else "SIX WORDS, THREE TRANSLATIONS",
        "视觉 × 触觉 × 机器；识读失败时默认停下" if zh else "Visual × tactile × machine; uncertainty always defaults to stop",
    )
    colors = [AMBER, CYAN, GREEN, "#9a7655", "#8e6b92", "#65758a"]
    for i, g in enumerate(model["glyphs"]):
        x = 80 + (i % 3) * 500
        y = 275 + (i // 3) * 325
        d.rounded_rectangle((x, y, x + 455, y + 270), 28, fill="white", outline="#d6d0c5", width=2)
        d.ellipse((x + 25, y + 28, x + 137, y + 140), fill=colors[i])
        text(d, (x + 81, y + 84), g["name_zh"] if zh else g["name_en"][0], 52, "white", True, "mm")
        text(d, (x + 165, y + 35), f"{g['id']}  {g['name_zh'] if zh else g['name_en']}", 30, INK, True)
        desc = g["public_state_zh" if zh else "public_state_en"]
        text(d, (x + 165, y + 82), wrap(d, desc, 255, 20, 3), 20, MUTED)
        for j, label in enumerate((["视觉", "触觉", "机器"] if zh else ["VISUAL", "TACTILE", "MACHINE"])):
            bx = x + 28 + j * 137
            d.rounded_rectangle((bx, y + 202, bx + 120, y + 240), 18, fill="#eef0ec")
            text(d, (bx + 60, y + 221), label, 16, INK, True, "mm")
    return save(im, "land-use-structure", lang)


def fields(lang):
    zh = lang == "zh"
    model = load("ground-language.json")
    im, d = base(
        "02 / VALIDATION CHAIN",
        "三区两翼：标准进入日常" if zh else "THREE FIELDS, TWO WINGS",
        "验证 → 共读 → 交接；两翼提供专业服务与社区反馈" if zh else "Validate → co-read → hand over; two wings connect expertise and community feedback",
    )
    y = 450
    field_colors = [AMBER, CYAN, GREEN]
    for i, f in enumerate(model["fields"]):
        x = 110 + i * 500
        if i < 2:
            d.line((x + 350, y, x + 500, y), fill="#a7aaa4", width=8)
            d.polygon(((x + 490, y - 12), (x + 520, y), (x + 490, y + 12)), fill="#a7aaa4")
        d.ellipse((x, y - 145, x + 300, y + 155), fill=field_colors[i])
        text(d, (x + 150, y - 47), f["id"], 25, "white", True, "mm")
        name = f["name_zh"] if zh else f["name_en"]
        text(d, (x + 150, y + 15), wrap(d, name, 245, 26, 3), 26, "white", True, "mm")
    wings = model["wings"]
    for i, wing in enumerate(wings):
        y2 = 760 + i * 80
        d.rounded_rectangle((205, y2, 1395, y2 + 55), 27, fill="#263331" if i == 0 else "#455d57")
        label = f"{wing['id']}  {wing['name_zh'] if zh else wing['name_en']}"
        text(d, (800, y2 + 28), label, 23, "white", True, "mm")
    note = "大钟寺仅表达片区功能逻辑；临时几何存在已知定位问题" if zh else "Dazhongsi shows programme logic only; its provisional geometry has a known location issue"
    text(d, (800, 947), note, 18, "#8a4d35", False, "mm")
    return save(im, "key-areas", lang)


def scenarios(lang):
    zh = lang == "zh"
    scenarios = load("scenarios.json")["scenarios"]
    personas = load("personas.json")["personas"]
    im, d = base(
        "03 / PUBLIC USE",
        "十二场景，八类使用者" if zh else "TWELVE SCENARIOS, EIGHT USER GROUPS",
        "前三景验证产业互操作；其余场景检验日常公平与恢复" if zh else "The first three validate interoperability; the rest test everyday equity and recovery",
    )
    for i, s in enumerate(scenarios):
        col, row = i % 4, i // 4
        x, y = 80 + col * 375, 270 + row * 135
        fill = "#fff5df" if i < 3 else "white"
        outline = AMBER if i < 3 else "#d6d0c5"
        d.rounded_rectangle((x, y, x + 335, y + 102), 18, fill=fill, outline=outline, width=3 if i < 3 else 2)
        text(d, (x + 18, y + 18), s["id"], 18, AMBER if i < 3 else CYAN, True)
        name = s["name_zh"] if zh else s["name_en"]
        text(d, (x + 68, y + 17), wrap(d, name, 245, 19, 2), 19, INK, True)
    text(d, (80, 706), "共同放行人群" if zh else "RELEASE-GATE USERS", 21, AMBER, True)
    for i, p in enumerate(personas):
        col, row = i % 4, i // 4
        x, y = 80 + col * 375, 753 + row * 82
        d.rounded_rectangle((x, y, x + 335, y + 55), 16, fill="#e7ece8")
        label = p["name_zh"] if zh else p["name_en"]
        text(d, (x + 16, y + 28), wrap(d, f"{p['id']}  {label}", 300, 16, 2), 16, INK, False, "lm")
    text(d, (800, 958), "机器没有效率优先权 / MACHINES GAIN NO PRIORITY FROM EFFICIENCY", 18, MUTED, True, "mm")
    return save(im, "mobility-bluegreen", lang)


def pilot(lang):
    zh = lang == "zh"
    ops = load("operations.json")
    im, d = base(
        "04 / REVERSIBLE PILOT",
        "先验证，再决定是否扩展" if zh else "TEST FIRST. EXPAND ONLY WITH EVIDENCE.",
        "100–200 米，有人值守，可撤回；安全、无障碍与公开治理共同放行" if zh else "100–200 m, staffed and removable; safety, accessibility and public governance release together",
    )
    stages_zh = ["0 数据与许可", "1 封闭试验", "2 公共试点", "3 独立评估"]
    stages_en = ["0 DATA + PERMISSION", "1 CLOSED TEST", "2 PUBLIC PILOT", "3 INDEPENDENT REVIEW"]
    for i, label in enumerate(stages_zh if zh else stages_en):
        x = 90 + i * 375
        d.rounded_rectangle((x, 310, x + 315, 440), 28, fill=["#dfe5df", "#dce9eb", "#fff0d1", "#dfe8e2"][i])
        text(d, (x + 157, 375), label, 24, INK, True, "mm")
        if i < 3:
            d.line((x + 315, 375, x + 365, 375), fill=AMBER, width=8)
    gates = (["使用者共创", "防滑防绊", "多厂商识读", "默认停止", "人工接管", "无手机路线", "投诉回滚"] if zh else
             ["USER CO-DESIGN", "SLIP + TRIP", "MULTI-VENDOR", "DEFAULT STOP", "HUMAN TAKEOVER", "PHONE-FREE ROUTE", "COMPLAINT + ROLLBACK"])
    text(d, (90, 505), "七道放行门" if zh else "SEVEN RELEASE GATES", 22, AMBER, True)
    for i, label in enumerate(gates):
        x = 90 + (i % 4) * 375
        y = 552 + (i // 4) * 82
        d.rounded_rectangle((x, y, x + 315, y + 54), 18, fill="white", outline="#c8c4bb")
        text(d, (x + 157, y + 27), label, 17, INK, True, "mm")
    metrics = ops["metrics"][:4]
    text(d, (90, 742), "不以铺设面积衡量" if zh else "MEASURE OUTCOMES, NOT INSTALLED AREA", 22, AMBER, True)
    for i, metric in enumerate(metrics):
        label = metric.get("name_zh" if zh else "name_en", metric.get("id", ""))
        x = 90 + i * 375
        d.rounded_rectangle((x, 790, x + 315, 905), 20, fill="#263331")
        text(d, (x + 157, 848), wrap(d, label, 270, 18, 3), 18, "white", True, "mm")
    text(d, (800, 958), "NO FACE · NO DEVICE ID · NO CONTINUOUS TRAJECTORY", 18, MUTED, True, "mm")
    return save(im, "metrics-evidence", lang)


def web_page(lang):
    zh = lang == "zh"
    model = load("ground-language.json")
    scenarios_data = load("scenarios.json")["scenarios"]
    suffix = "" if zh else ".en"
    other = "index.en.html" if zh else "index.html"
    glyph_cards = "".join(
        f'''<details class="glyph"><summary><b>{g["id"]}</b><span>{html.escape(g["name_zh"] if zh else g["name_en"])}</span></summary>
        <p>{html.escape(g["public_state_zh"] if zh else g["public_state_en"])}</p>
        <dl><dt>{"视觉" if zh else "Visual"}</dt><dd>{html.escape(g["visual_zh"] if zh else g["visual_en"])}</dd>
        <dt>{"触觉" if zh else "Tactile"}</dt><dd>{html.escape(g["tactile_zh"] if zh else g["tactile_en"])}</dd>
        <dt>{"机器" if zh else "Machine"}</dt><dd>{html.escape(g["machine_zh"] if zh else g["machine_en"])}</dd></dl></details>'''
        for g in model["glyphs"]
    )
    scenario_cards = "".join(
        f'<li><b>{s["id"]}</b><span>{html.escape(s["name_zh"] if zh else s["name_en"])}</span></li>'
        for s in scenarios_data
    )
    title = "京张地语" if zh else "JING-ZHANG GROUND LANGUAGE"
    strap = "让机器在公共空间遵守人能看懂的规则。" if zh else "Public-space rules people can understand and machines must obey."
    intro = ("一套开放、被动、无身份的公共地面语言，使普通行人、无障碍使用者、维护人员和不同厂商机器人共同理解六种状态。机器不确定时停下，人永远优先。" if zh else
             "An open, passive and identity-free public ground language lets pedestrians, disabled users, maintainers and robots from different vendors share six states. Machines stop when uncertain; people always retain priority.")
    evidence_labels = (["总览地图", "三层范围", "重点区域", "用地分区", "交通慢行", "蓝绿公共空间", "建筑", "更新项目", "AI 场景", "核心指标", "任务覆盖", "自检状态", "来源", "假设"] if zh else
                       ["Overview map", "Three scope levels", "Key areas", "Land-use zones", "Mobility", "Blue-green public space", "Buildings", "Renewal projects", "AI scenarios", "Core metrics", "Task coverage", "Self-check", "Sources", "Assumptions"])
    evidence_cards = "".join(f"<li>{label}</li>" for label in evidence_labels)
    path = ROOT / "visual" / ("index.html" if zh else "index.en.html")
    path.parent.mkdir(exist_ok=True)
    page = f'''<!doctype html>
<html lang="{'zh-CN' if zh else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><circle cx=%2250%22 cy=%2250%22 r=%2248%22 fill=%22%23e5a32d%22/><path d=%22M25 52h50M50 27v50%22 stroke=%22%2317201f%22 stroke-width=%2210%22/></svg>"><style>
:root{{--ink:#17201f;--paper:#f3f0e9;--amber:#e5a32d;--cyan:#3f8f9a;--green:#5d816f;--muted:#67716e}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--paper);color:var(--ink);font-family:"Microsoft YaHei","Segoe UI",sans-serif;line-height:1.65}}
a{{color:inherit}}header{{min-height:92vh;background:linear-gradient(90deg,rgba(13,22,21,.91) 0 43%,rgba(13,22,21,.12)),url('../assets/media/ground-language-cover.png') center/cover;color:white;padding:28px 6vw;display:flex;flex-direction:column}}
nav{{display:flex;justify-content:space-between;align-items:center;font-size:.86rem;letter-spacing:.08em}}nav a{{text-decoration:none;border:1px solid #ffffff66;border-radius:999px;padding:.45rem .8rem}}
.hero{{margin:auto 0;max-width:800px;border-left:12px solid var(--amber);padding-left:3vw}}.hero .eyebrow{{color:#f1b74e;font-weight:700;letter-spacing:.14em}}h1{{font-size:clamp(3rem,8vw,7.5rem);line-height:.92;margin:.35em 0}}.strap{{font-size:clamp(1.3rem,2.2vw,2rem);font-weight:700;max-width:720px}}
.concept-note{{font-size:.78rem;color:#ddd8cd;margin-top:auto}}main{{overflow:hidden}}section{{padding:7rem 6vw}}.lead{{display:grid;grid-template-columns:1.1fr .9fr;gap:6vw;align-items:center}}h2{{font-size:clamp(2rem,4vw,4rem);line-height:1.1;margin:.2em 0 .6em}}.kicker{{color:#a96e00;font-weight:800;letter-spacing:.12em}}.lead p{{font-size:1.25rem}}.statline{{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:#cbc6bb;margin-top:3rem}}.stat{{background:white;padding:1.4rem}}.stat b{{display:block;font-size:2rem;color:var(--amber)}}
.dark{{background:var(--ink);color:white}}.dark .kicker{{color:#f1b74e}}.glyphs{{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}}.glyph{{background:#263331;border-radius:18px;padding:0 1.2rem}}.glyph summary{{cursor:pointer;list-style:none;display:flex;gap:1rem;align-items:center;padding:1.2rem 0}}.glyph summary b{{width:3rem;height:3rem;border-radius:50%;display:grid;place-items:center;background:var(--amber)}}.glyph summary span{{font-size:1.35rem;font-weight:700}}.glyph dt{{color:#f1b74e;font-weight:700}}.glyph dd{{margin:0 0 .8rem;color:#d9dedb}}
.diagram{{width:100%;height:auto;border-radius:24px;box-shadow:0 20px 50px #17201f1b}}.scenarios{{list-style:none;padding:0;display:grid;grid-template-columns:repeat(4,1fr);gap:.8rem}}.scenarios li{{background:white;border:1px solid #d6d0c5;border-radius:16px;padding:1rem;display:flex;gap:.7rem}}.scenarios b{{color:#a96e00}}.warning{{background:#fff1d6;border-left:8px solid var(--amber);padding:1.2rem 1.5rem;margin-top:2rem}}
.evidence-grid{{list-style:none;padding:0;display:grid;grid-template-columns:repeat(7,1fr);gap:.6rem}}.evidence-grid li{{background:white;border:1px solid #d6d0c5;border-radius:12px;padding:.8rem;text-align:center;font-weight:700}}.metric-row{{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:2rem 0}}.metric-box{{background:#263331;color:white;border-radius:18px;padding:1.2rem}}.metric-box b{{display:block;color:#f1b74e;font-size:1.7rem}}.cta{{background:var(--amber);text-align:center}}.cta p{{max-width:900px;margin:1rem auto;font-size:1.2rem}}footer{{background:#101817;color:#cdd4d1;padding:2.5rem 6vw;display:flex;justify-content:space-between;gap:2rem;font-size:.82rem}}
@media(max-width:850px){{header{{background-position:65% center}}.lead{{grid-template-columns:1fr}}.glyphs,.scenarios{{grid-template-columns:1fr 1fr}}.statline{{grid-template-columns:1fr 1fr}}section{{padding:4rem 6vw}}}}@media(max-width:520px){{.glyphs,.scenarios{{grid-template-columns:1fr}}}}
</style></head><body>
<header><nav><b>JZ·GL / OPEN DESIGN</b><a href="{other}">{'EN' if zh else '中文'}</a></nav><div class="hero"><div class="eyebrow">ONE LINE · THREE TRANSLATIONS · SIX WORDS</div><h1>{title}</h1><div class="strap">{strap}</div></div><div class="concept-note">{'概念氛围图，不是现场照片或工程证据。' if zh else 'Concept atmosphere; not a site photograph or engineering evidence.'}</div></header>
<main><section class="lead"><div><div class="kicker">00 / PUBLIC COVENANT</div><h2>{'不是机器专用道，<br>是共同读得懂的规则' if zh else 'NOT A ROBOT LANE.<br>A RULE EVERYONE CAN READ.'}</h2><p>{intro}</p><div class="statline"><div class="stat"><b>6</b>{'开放词汇' if zh else 'open words'}</div><div class="stat"><b>3</b>{'翻译层' if zh else 'translations'}</div><div class="stat"><b>12</b>{'使用场景' if zh else 'scenarios'}</div><div class="stat"><b>100–200m</b>{'可撤回试点' if zh else 'reversible pilot'}</div></div></div><img class="diagram" src="../assets/figures/key-areas{suffix}.png" alt="Three fields and two wings"></section>
<section class="dark"><div class="kicker">01 / OPEN GRAMMAR</div><h2>{'六词构成最小公共语法' if zh else 'SIX WORDS FORM A MINIMAL PUBLIC GRAMMAR'}</h2><div class="glyphs">{glyph_cards}</div></section>
<section><div class="kicker">02 / EVERYDAY RELEASE GATES</div><h2>{'十二个场景，由八类使用者共同放行' if zh else 'TWELVE SCENARIOS, RELEASED WITH EIGHT USER GROUPS'}</h2><ul class="scenarios">{scenario_cards}</ul><p class="warning">{'前三个场景验证跨厂商识读、天气遮挡和人机互相理解；任何公共试点都必须保留无手机路径、人工接管和公开回滚。' if zh else 'The first three scenarios validate multi-vendor reading, weather and occlusion, and mutual comprehension. Every public pilot retains a phone-free route, human takeover and public rollback.'}</p></section>
<section class="dark"><div class="kicker">03 / REVERSIBLE PILOT</div><h2>{'先验证，再决定是否扩展' if zh else 'TEST FIRST. EXPAND ONLY WITH EVIDENCE.'}</h2><img class="diagram" src="../assets/figures/metrics-evidence{suffix}.png" alt="Pilot phases and release gates"></section>
<section><div class="kicker">04 / EVIDENCE INDEX</div><h2>{'总览地图与可审查证据' if zh else 'OVERVIEW MAP AND REVIEWABLE EVIDENCE'}</h2><img class="diagram" src="../assets/figures/site-overview{suffix}.png" alt="Overall concept"><ul class="evidence-grid">{evidence_cards}</ul>
<div class="metric-row"><div class="metric-box" data-metric="site_area_sqm" data-value="11412825.386"><b>11,412,825.386 m²</b>{'临时总体边界复算面积' if zh else 'area recalculated from provisional overall boundary'}</div><div class="metric-box" data-metric="green_ratio" data-value="0.123423"><b>12.3423%</b>{'概念分析绿地叠层' if zh else 'conceptual analytical green overlay'}</div><div class="metric-box" data-metric="public_space_ratio" data-value="0.073281"><b>7.3281%</b>{'概念分析公共空间叠层' if zh else 'conceptual analytical public-space overlay'}</div></div>
<p class="warning">{'以上三项仅用于脚手架几何一致性复核，不是现状测量、法定控制或实施承诺。建筑层为低可信占位；容积率未知。完整来源见 sources.json，完整假设见 assumptions.json，自检状态见 self_check.json，任务覆盖见 compliance_matrix.json。' if zh else 'These three values check scaffold geometry consistency only; they are not surveys, statutory controls or delivery commitments. The building layer is a low-confidence placeholder and FAR is unknown. See sources.json, assumptions.json, self_check.json and compliance_matrix.json for the full evidence chain.'}</p></section>
<section class="cta"><h2>{'机器可以更新，公共原则不能静默改写。' if zh else 'TECHNOLOGY MAY UPDATE. PUBLIC PRINCIPLES MAY NOT CHANGE SILENTLY.'}</h2><p>{'人优先、无身份可用、失败可见、责任可追溯。若试验失败，地面恢复；若试验成功，成果以开放版本和采购中立条款进入下一阶段。' if zh else 'Human priority, identity-free access, visible failure and accountable responsibility. If the test fails, restore the ground. If it succeeds, advance through an open version and vendor-neutral procurement.'}</p></section></main>
<footer><span>Chozzc × OpenAI Codex (GPT-5) · COMMUNITY-DISPLAY-ONLY</span><span>{'临时边界，仅供概念生成和内容评审' if zh else 'Provisional geometry for concept generation and content review only'}</span></footer></body></html>'''
    path.write_text(page, encoding="utf-8")
    return path


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    outputs = []
    for lang in ("zh", "en"):
        outputs += [overview(lang), glyphs(lang), fields(lang), scenarios(lang), pilot(lang)]
    for path in outputs:
        with Image.open(path) as im:
            assert im.size == (W, H) and im.mode == "RGB", path
    pages = [web_page("zh"), web_page("en")]
    assert all("https://" not in path.read_text(encoding="utf-8") for path in pages)
    print(f"PASS: built and verified {len(outputs)} paired figures and {len(pages)} offline pages")


if __name__ == "__main__":
    main()
