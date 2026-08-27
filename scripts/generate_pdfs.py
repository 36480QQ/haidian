#!/usr/bin/env python3
"""Generate A3 booklet and A0 board PDFs in Chinese and English."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, A0, landscape
from reportlab.lib.units import mm
from PIL import Image

SUBMISSION = Path("submissions/kati-99/jingzhang-intelligence-loop")
DRAWINGS = SUBMISSION / "drawings"
FIGURES = SUBMISSION / "assets/figures"

FONT = "Helvetica"


def draw_text(c, x, y, text, size=12, font=FONT):
    c.setFont(font, size)
    c.drawString(x, y, text)


def make_a3_booklet(lang="zh", suffix=""):
    pagesize = landscape(A3)
    w, h = pagesize
    out = DRAWINGS / f"a3-booklet{suffix}.pdf"
    c = canvas.Canvas(str(out), pagesize=pagesize)

    title = "京张智环：百年铁路上的AI创新带" if lang == "zh" else "JingZhang Intelligence Loop"
    subtitle = "A3 文册 / A3 Booklet" if lang == "zh" else "A3 Booklet"

    # Page 1: cover + overview
    c.setFillColorRGB(0.06, 0.12, 0.2)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    draw_text(c, 40 * mm, h - 60 * mm, title, 32)
    draw_text(c, 40 * mm, h - 80 * mm, subtitle, 18)
    draw_text(c, 40 * mm, h - 110 * mm,
              "Agent: KnightAgent | GitHub: kati-99" if lang == "zh" else "Agent: KnightAgent | GitHub: kati-99", 14)
    c.showPage()

    # Page 2: scope framework
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColorRGB(0.1, 0.12, 0.2)
    draw_text(c, 30 * mm, h - 30 * mm,
              "三层范围与空间工作框架" if lang == "zh" else "Three-Level Scope Framework", 24)
    draw_text(c, 30 * mm, h - 55 * mm,
              "统筹研究范围 43.6 km² | 总体设计范围 11.4 km² | 重点区域范围 3.68 km²" if lang == "zh"
              else "Coordinated 43.6 km² | Overall 11.4 km² | Key Areas 3.68 km²", 14)
    img_path = FIGURES / f"land-use-structure{suffix}.png"
    c.drawImage(str(img_path), 30 * mm, 40 * mm, width=w - 60 * mm, height=h - 110 * mm, preserveAspectRatio=True)
    c.showPage()

    # Page 3: key areas
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColorRGB(0.1, 0.12, 0.2)
    draw_text(c, 30 * mm, h - 30 * mm,
              "三处重点区域详细设计" if lang == "zh" else "Three Key Areas Detailed Design", 24)
    c.drawImage(str(FIGURES / f"key-areas{suffix}.png"), 30 * mm, 40 * mm, width=w - 60 * mm, height=h - 100 * mm, preserveAspectRatio=True)
    c.showPage()

    # Page 4: mobility & metrics
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColorRGB(0.1, 0.12, 0.2)
    draw_text(c, 30 * mm, h - 30 * mm,
              "交通慢行、蓝绿空间与核心指标" if lang == "zh" else "Mobility, Blue-Green Space & Metrics", 24)
    c.drawImage(str(FIGURES / f"mobility-bluegreen{suffix}.png"), 30 * mm, h / 2 + 10 * mm, width=(w - 70 * mm) / 2, height=h / 2 - 50 * mm, preserveAspectRatio=True)
    c.drawImage(str(FIGURES / f"metrics-evidence{suffix}.png"), w / 2 + 5 * mm, h / 2 + 10 * mm, width=(w - 70 * mm) / 2, height=h / 2 - 50 * mm, preserveAspectRatio=True)
    draw_text(c, 30 * mm, 80 * mm,
              "注：所有指标基于 provisional boundary 复算，待官方边界公布后替换并重新核算。" if lang == "zh"
              else "Note: All metrics are recalculated from provisional boundary and will be updated when official boundary is released.", 12)
    c.showPage()

    c.save()
    print(f"saved {out}")


def make_a0_boards(lang="zh", suffix=""):
    pagesize = landscape(A0)
    w, h = pagesize
    out = DRAWINGS / f"a0-boards{suffix}.pdf"
    c = canvas.Canvas(str(out), pagesize=pagesize)

    title = "京张智环：百年铁路上的AI创新带" if lang == "zh" else "JingZhang Intelligence Loop: AI Innovation Belt"

    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColorRGB(0.06, 0.12, 0.2)
    draw_text(c, 60 * mm, h - 80 * mm, title, 56)
    draw_text(c, 60 * mm, h - 120 * mm,
              "A0 展板 / A0 Presentation Board" if lang == "zh" else "A0 Presentation Board", 28)

    # Main map/overview on A0
    c.drawImage(str(FIGURES / f"site-overview{suffix}.png"), 60 * mm, 180 * mm, width=w - 120 * mm, height=h - 420 * mm, preserveAspectRatio=True)

    # Bottom strip with key stats
    c.setFillColorRGB(0.95, 0.96, 0.98)
    c.rect(60 * mm, 60 * mm, w - 120 * mm, 100 * mm, fill=1, stroke=0)
    c.setFillColorRGB(0.1, 0.12, 0.2)
    stats = [
        ("总体设计范围 / Overall area", "11.4 km²"),
        ("绿地比例 / Green ratio", "12.34%"),
        ("公共空间比例 / Public space", "7.33%"),
        ("建筑基底 / Building footprint", "310,807 m²"),
    ]
    x = 90 * mm
    for label, value in stats:
        draw_text(c, x, 130 * mm, label, 14)
        draw_text(c, x, 100 * mm, value, 24)
        x += (w - 180 * mm) / 4

    draw_text(c, 60 * mm, 30 * mm,
              "注：本方案为概念建议，所有空间结论待官方数据发布后复算。" if lang == "zh"
              else "Note: This proposal is conceptual; spatial conclusions will be recalculated after official data release.", 14)
    c.showPage()
    c.save()
    print(f"saved {out}")


if __name__ == "__main__":
    DRAWINGS.mkdir(parents=True, exist_ok=True)
    for lang, suffix in [("zh", ""), ("en", ".en")]:
        make_a3_booklet(lang, suffix)
        make_a0_boards(lang, suffix)
