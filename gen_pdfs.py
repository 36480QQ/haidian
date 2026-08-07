"""Generate A3 booklet and A0 board PDFs for 开源京张 AI 场景之都."""
import os
from reportlab.lib.pagesizes import A3, A0
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register CJK font
cjk_font = None
for path in [
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\simsun.ttc",
]:
    if os.path.exists(path):
        try:
            pdfmetrics.registerFont(TTFont("CJK", path))
            cjk_font = "CJK"
            print(f"Registered: {path}")
            break
        except Exception as e:
            print(f"Failed {path}: {e}")
if not cjk_font:
    cjk_font = "Helvetica"

BASE = "submissions/Microbiosis/kaiyuan-jingzhang-ai-city/drawings"

def draw_a3():
    path = os.path.join(BASE, "a3-booklet.pdf")
    c = canvas.Canvas(path, pagesize=A3)
    W, H = A3
    c.setTitle("A3 Booklet - Kaiyuan Jingzhang AI City")

    # Page 1: Cover
    c.setFillColor(colors.HexColor("#1a3a5c"))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont(cjk_font, 26)
    c.drawCentredString(W/2, H*0.75, "开源京张 · AI 场景之都")
    c.setFont(cjk_font, 14)
    c.drawCentredString(W/2, H*0.70, "Open Jingzhang AI Scenario Capital")
    c.drawCentredString(W/2, H*0.55, "AI 场景操作系统 · AI Scenario OS")
    c.drawCentredString(W/2, H*0.42, "百年京张文化带 | 都市AI生活体验带 | AI融合创新带")
    c.drawCentredString(W/2, H*0.28, "提交方: Microbiosis (ZCode Agent)")
    c.drawCentredString(W/2, H*0.18, "2026 年 8 月 · 概念性方案")
    c.showPage()

    # Page 2: Structure
    c.setFillColor(colors.white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#1a3a5c"))
    c.setFont(cjk_font, 22)
    c.drawString(30*mm, H - 25*mm, "总体空间结构 · 三带一心一廊")
    c.setFont(cjk_font, 12)
    y = H - 50*mm
    for line in [
        "一廊: 京张铁路遗址公园活力带 (约10km南北绿轴)",
        "一核: AI原点社区 (清华-五道口-北邮创新核)",
        "三带: 百年京张文化带 / 都市AI生活体验带 / AI融合创新带",
        "三区: 众智园 (北) / AI原点社区 (中) / 大钟寺 (南)",
        "两翼: 中关村科技服务翼 (东) / 小月河场景赋能翼 (西)",
    ]:
        c.drawString(30*mm, y, "  * " + line)
        y -= 15*mm

    # Schematic
    c.setStrokeColor(colors.HexColor("#c0392b"))
    c.setLineWidth(3)
    c.line(W/2 - 60*mm, H*0.12, W/2 - 60*mm, H*0.52)
    c.setStrokeColor(colors.HexColor("#27ae60"))
    c.line(W/2, H*0.12, W/2, H*0.52)
    c.setStrokeColor(colors.HexColor("#2980b9"))
    c.line(W/2 + 60*mm, H*0.12, W/2 + 60*mm, H*0.52)
    c.setFont(cjk_font, 11)
    c.setFillColor(colors.HexColor("#c0392b"))
    c.drawCentredString(W/2 - 60*mm, H*0.07, "文化带")
    c.setFillColor(colors.HexColor("#27ae60"))
    c.drawCentredString(W/2, H*0.07, "生活带")
    c.setFillColor(colors.HexColor("#2980b9"))
    c.drawCentredString(W/2 + 60*mm, H*0.07, "创新带")
    c.showPage()

    # Page 3: Key Areas
    c.setFillColor(colors.white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#1a3a5c"))
    c.setFont(cjk_font, 22)
    c.drawString(30*mm, H - 25*mm, "三处重点区域详细设计")
    c.setFont(cjk_font, 12)
    y = H - 50*mm
    areas = [
        ("众智园 AI 自主创新加速区 (192.1 ha)",
         "AI全栈自主创新体系 + AI治理全球话语权",
         "基础模型 / AI芯片 / Agent框架 / 标准评测"),
        ("北京 AI 原点社区 (104.3 ha)",
         "世界级AI创新生态 + AI+场景赋能新范式",
         "高校-开发者-初创-社区混合创新街区"),
        ("大钟寺 AI 产业聚集区 (72.0 ha)",
         "智能原生新业态 + 场景开放与产业转化",
         "AI产业总部 / 智能商业 / 公共体验"),
    ]
    for name, role, detail in areas:
        c.setFont(cjk_font, 14)
        c.drawString(30*mm, y, name)
        y -= 16*mm
        c.setFont(cjk_font, 11)
        c.drawString(35*mm, y, "定位: " + role)
        y -= 15*mm
        c.drawString(35*mm, y, "内容: " + detail)
        y -= 28*mm

    # Draw key area polygons
    c.setStrokeColor(colors.HexColor("#c0392b")); c.setFillColor(colors.HexColor("#f5b7b1"))
    c.rect(50*mm, 65*mm, 90*mm, 55*mm, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#1a3a5c"))
    c.setFont(cjk_font, 14)
    c.drawCentredString(95*mm, 88*mm, "众智园")
    c.setStrokeColor(colors.HexColor("#27ae60")); c.setFillColor(colors.HexColor("#abebc6"))
    c.rect(160*mm, 65*mm, 90*mm, 40*mm, stroke=1, fill=1)
    c.drawCentredString(205*mm, 80*mm, "AI原点")
    c.setStrokeColor(colors.HexColor("#2980b9")); c.setFillColor(colors.HexColor("#aed6f1"))
    c.rect(270*mm, 65*mm, 90*mm, 35*mm, stroke=1, fill=1)
    c.drawCentredString(315*mm, 80*mm, "大钟寺")
    c.showPage()

    # Page 4: AI Scenarios
    c.setFillColor(colors.white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#1a3a5c"))
    c.setFont(cjk_font, 22)
    c.drawString(30*mm, H - 25*mm, "AI 场景卡 (10张 · 含3张产业测试)")
    c.setFont(cjk_font, 10)
    y = H - 50*mm
    scenarios = [
        ("SC-TEST-001", "AI芯片端侧推理测试", "众智园"),
        ("SC-TEST-002", "AI Agent多智能体协作测试", "AI原点"),
        ("SC-TEST-003", "AI+自动驾驶城市测试", "大钟寺-小月河"),
        ("SC-APP-001", "AI+信软·模型评测", "众智园"),
        ("SC-APP-002", "AI+医疗·社区健康智能体", "AI原点"),
        ("SC-APP-003", "AI+教育·自适应学习", "AI原点"),
        ("SC-APP-004", "AI+法律·合规审查", "众智园"),
        ("SC-APP-005", "AI+生活服务·社区智能体", "AI原点"),
        ("SC-APP-006", "AI+交通·智能公交调度", "大钟寺"),
        ("SC-APP-007", "AI+公共空间·城市数字孪生", "全线"),
    ]
    for code, name, loc in scenarios:
        c.setFillColor(colors.HexColor("#1a3a5c"))
        c.drawString(30*mm, y, "[ " + code + " ] " + name + " (" + loc + ")")
        y -= 14*mm
    c.showPage()

    # Page 5: Metrics & Compliance
    c.setFillColor(colors.white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#1a3a5c"))
    c.setFont(cjk_font, 22)
    c.drawString(30*mm, H - 25*mm, "核心指标体系与合规覆盖")
    c.setFont(cjk_font, 12)
    y = H - 50*mm
    metrics = [
        ("总体设计面积", "1,140 ha", "[metric:site_area_sqm]"),
        ("重点区面积合计", "368.4 ha", "[metric:key_area_count]"),
        ("绿地比例", "~20% (待重算)", "[metric:green_ratio]"),
        ("公共空间比例", "~15% (待重算)", "[metric:public_space_ratio]"),
        ("AI场景卡数量", "10 张", "compliance"),
        ("朝圣地标数量", "3 个", "concept"),
    ]
    for name, val, ref in metrics:
        c.drawString(30*mm, y, name + ": " + val)
        c.setFont(cjk_font, 10)
        c.drawString(140*mm, y, ref)
        c.setFont(cjk_font, 12)
        y -= 22*mm
    y -= 10*mm
    c.setFont(cjk_font, 11)
    c.drawString(30*mm, y, "合规矩阵覆盖: agent.1 ~ agent.6 + 公告 1.3/1.4/1.5")
    y -= 18*mm
    c.drawString(30*mm, y, "专业标准覆盖: 城市设计管理办法 / 控规办法 / 用地分类指南")
    y -= 18*mm
    c.drawString(30*mm, y, "设计深度覆盖: 控规深度 + 规划综合实施方案深度")
    c.showPage()

    c.save()
    print(f"a3-booklet.pdf: {os.path.getsize(path)} bytes")

def draw_a0():
    path = os.path.join(BASE, "a0-boards.pdf")
    c = canvas.Canvas(path, pagesize=A0)
    W, H = A0
    c.setTitle("A0 Board - Kaiyuan Jingzhang AI City")

    c.setFillColor(colors.HexColor("#f8f9fa"))
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Header bar
    c.setFillColor(colors.HexColor("#1a3a5c"))
    c.rect(0, H - 70*mm, W, 70*mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont(cjk_font, 32)
    c.drawCentredString(W/2, H - 35*mm, "开源京张 · AI 场景之都 | Open Jingzhang AI Scenario Capital")

    # Left column: concept
    c.setFillColor(colors.HexColor("#1a3a5c"))
    c.setFont(cjk_font, 18)
    c.drawString(25*mm, H - 90*mm, "总体概念")
    c.setFont(cjk_font, 12)
    y = H - 112*mm
    for line in [
        "AI 场景操作系统 (AI Scenario OS)",
        "  * 场景即产品",
        "  * 数据即 API",
        "  * 公共空间即 UI",
        "  * 开发者即用户",
        "",
        "三带一心一廊:",
        "  * 京张遗址公园活力带 (一廊)",
        "  * AI原点社区 (一核)",
        "  * 三条主题带 (自北向南)",
        "  * 三区两翼协同",
        "",
        "三大定位:",
        "  * 百年京张文化带",
        "  * 都市AI生活体验带",
        "  * AI融合创新带",
    ]:
        c.drawString(25*mm, y, line)
        y -= 15*mm

    # Center: key areas
    cx, cy = W*0.5, H*0.50
    c.setStrokeColor(colors.HexColor("#c0392b")); c.setFillColor(colors.HexColor("#f5b7b1"))
    c.rect(cx - 50*mm, cy + 100*mm, 100*mm, 70*mm, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#1a3a5c"))
    c.setFont(cjk_font, 16)
    c.drawCentredString(cx, cy + 130*mm, "众智园 (192ha)")
    c.setFont(cjk_font, 11)
    c.drawCentredString(cx, cy + 115*mm, "AI全栈自主创新")

    c.setStrokeColor(colors.HexColor("#27ae60")); c.setFillColor(colors.HexColor("#abebc6"))
    c.rect(cx - 50*mm, cy, 100*mm, 60*mm, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#1a3a5c"))
    c.setFont(cjk_font, 16)
    c.drawCentredString(cx, cy + 35*mm, "AI原点社区 (104ha)")
    c.setFont(cjk_font, 11)
    c.drawCentredString(cx, cy + 18*mm, "世界级AI创新生态")

    c.setStrokeColor(colors.HexColor("#2980b9")); c.setFillColor(colors.HexColor("#aed6f1"))
    c.rect(cx - 50*mm, cy - 90*mm, 100*mm, 50*mm, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#1a3a5c"))
    c.setFont(cjk_font, 16)
    c.drawCentredString(cx, cy - 58*mm, "大钟寺 (72ha)")
    c.setFont(cjk_font, 11)
    c.drawCentredString(cx, cy - 72*mm, "智能原生新业态")

    c.setFont(cjk_font, 14); c.setFillColor(colors.black)
    c.drawCentredString(cx, cy + 180*mm, "^ 北")
    c.drawCentredString(cx, cy - 130*mm, "京张铁路遗址公园活力带 (南北贯通)")

    # Right: scenarios + landmarks
    c.setFillColor(colors.HexColor("#1a3a5c"))
    c.setFont(cjk_font, 18)
    c.drawString(W - 300*mm, H - 90*mm, "AI 场景与朝圣地标")
    c.setFont(cjk_font, 12)
    y = H - 112*mm
    for line in [
        "10 张 AI 场景卡:",
        "  * 3 张产业测试 (芯片/Agent/自动驾驶)",
        "  * 7 张 AI+ 应用 (信软/医疗/教育/法律/生活/交通/公共)",
        "",
        "3 个 AI 朝圣地标:",
        "  * 京张智脉碑 (青龙桥)",
        "  * AI 原点灯塔 (五道口)",
        "  * 开源之环 (大钟寺)",
        "",
        "5 类用户画像:",
        "  * 研究者 / 工程师 / 创业者 / 开发者 / 居民",
        "",
        "7 个全球案例比较:",
        "  * 硅谷/伦敦/深圳/首尔/东京/柏林/上海",
        "",
        "5 类年度活动:",
        "  * 年度大会/Hackathon/开放日/文化节/治理论坛",
    ]:
        c.drawString(W - 300*mm, y, line)
        y -= 15*mm

    # Bottom band
    c.setFillColor(colors.HexColor("#1a3a5c"))
    c.rect(0, 0, W, 45*mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont(cjk_font, 14)
    c.drawString(25*mm, 32*mm, "全球 AI 创新活动体系: 开源京张年度大会 | 京张 AI Hackathon | AI场景开放日 | 京张文化数字节 | AI治理全球论坛")
    c.setFont(cjk_font, 11)
    c.drawString(25*mm, 15*mm, "提交方: Microbiosis (ZCode Agent) | 概念性方案，不构成政府审定结论 | 基于 provisional boundary (待官方 polygon 发布后重算)")

    c.save()
    print(f"a0-boards.pdf: {os.path.getsize(path)} bytes")

draw_a3()
draw_a0()
print("Done")