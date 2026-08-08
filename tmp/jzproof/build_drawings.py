from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A3, A0, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path("F:/Haidian/submissions/shanshui2024/jingzhang-proof-commons")
FIG = ROOT / "assets" / "figures"
OUT = ROOT / "drawings"
FONT = "C:/Windows/Fonts/NotoSansSC-VF.ttf"
pdfmetrics.registerFont(TTFont("Noto", FONT))

NAVY = colors.HexColor("#13263d")
INK = colors.HexColor("#17273a")
MUTED = colors.HexColor("#617286")
LINE = colors.HexColor("#cbd6e2")
PAPER = colors.HexColor("#f5f8fb")
WHITE = colors.white
BLUE = colors.HexColor("#2789b2")
GREEN = colors.HexColor("#2c9b6b")
RUST = colors.HexColor("#c96545")
AMBER = colors.HexColor("#df9a2d")
VIOLET = colors.HexColor("#7166cf")

BODY = ParagraphStyle("body", fontName="Noto", fontSize=10.2, leading=15, textColor=INK, wordWrap="CJK")
SMALL = ParagraphStyle("small", fontName="Noto", fontSize=8.5, leading=12, textColor=MUTED, wordWrap="CJK")
CARD = ParagraphStyle("card", fontName="Noto", fontSize=9.2, leading=13.5, textColor=INK, wordWrap="CJK")
CARD_SMALL = ParagraphStyle("cardsmall", fontName="Noto", fontSize=8.2, leading=11.5, textColor=MUTED, wordWrap="CJK")
BOARD_BODY = ParagraphStyle("boardbody", fontName="Noto", fontSize=18, leading=27, textColor=INK, wordWrap="CJK")
BOARD_SMALL = ParagraphStyle("boardsmall", fontName="Noto", fontSize=14, leading=21, textColor=MUTED, wordWrap="CJK")
BOARD_CARD = ParagraphStyle("boardcard", fontName="Noto", fontSize=15, leading=22, textColor=INK, wordWrap="CJK")


def para(c, text, x, top, width, style=BODY):
    p = Paragraph(text, style)
    _, h = p.wrap(width, 2000)
    p.drawOn(c, x, top - h)
    return top - h


def image_contain(c, path, x, y, w, h, border=True):
    img = ImageReader(str(path))
    iw, ih = img.getSize()
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    dx, dy = x + (w - dw) / 2, y + (h - dh) / 2
    if border:
        c.setStrokeColor(LINE)
        c.rect(x, y, w, h, stroke=1, fill=0)
    c.drawImage(img, dx, dy, width=dw, height=dh, preserveAspectRatio=True, mask="auto")


def header(c, width, height, index, title, accent=AMBER, dark=False):
    if dark:
        c.setFillColor(NAVY)
        c.rect(0, height - 96, width, 96, stroke=0, fill=1)
        c.setFillColor(WHITE)
        c.setFont("Noto", 10)
        c.drawString(40, height - 34, f"{index:02d} / JZ BENCHLINE")
        c.setFont("Noto", 25)
        c.drawString(40, height - 72, title)
        c.setFillColor(accent)
        c.rect(0, height - 100, width, 4, stroke=0, fill=1)
    else:
        c.setFillColor(WHITE)
        c.rect(0, height - 78, width, 78, stroke=0, fill=1)
        c.setFillColor(accent)
        c.rect(0, height - 82, width, 4, stroke=0, fill=1)
        c.setFillColor(RUST)
        c.setFont("Noto", 9)
        c.drawString(40, height - 29, f"{index:02d} / JZ BENCHLINE")
        c.setFillColor(INK)
        c.setFont("Noto", 21)
        c.drawString(40, height - 61, title)


def footer(c, width, page, label):
    c.setStrokeColor(LINE)
    c.line(40, 31, width - 40, 31)
    c.setFillColor(MUTED)
    c.setFont("Noto", 7.5)
    c.drawString(40, 17, "京张智证公地 / JZ BENCHLINE · 概念建议 · provisional intake")
    c.drawRightString(width - 40, 17, f"{label}  /  {page}")


def card(c, x, y, w, h, title, text, accent=BLUE, style=CARD):
    c.setFillColor(colors.white)
    c.setStrokeColor(LINE)
    c.rect(x, y, w, h, stroke=1, fill=1)
    c.setFillColor(accent)
    c.rect(x, y + h - 5, w, 5, stroke=0, fill=1)
    para(c, f"<b>{title}</b>", x + 14, y + h - 18, w - 28, style)
    para(c, text, x + 14, y + h - 47, w - 28, CARD_SMALL)


def a3_cover(c, page):
    width, height = landscape(A3)
    c.setFillColor(NAVY)
    c.rect(0, 0, width, height, stroke=0, fill=1)
    c.setFillColor(AMBER)
    c.rect(0, height - 9, width, 9, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#9bd2b6"))
    c.setFont("Noto", 11)
    c.drawString(50, height - 60, "百年京张 AI 创新带 · 开源投稿")
    c.setFillColor(WHITE)
    c.setFont("Noto", 42)
    c.drawString(50, height - 122, "京张智证公地")
    c.setFillColor(AMBER)
    c.setFont("Noto", 15)
    c.drawString(52, height - 150, "JZ BENCHLINE")
    para(c, "可逆更新与公共验证驱动的 AI 创新带", 52, height - 190, 470, ParagraphStyle("coverlead", parent=BODY, fontSize=19, leading=28, textColor=WHITE))
    para(c, "研发基准 / 公共基准 / 应用基准\n一带三核 / 两翼串联 / 四类公共接口", 52, height - 260, 430, ParagraphStyle("covermeta", parent=BODY, fontSize=12, leading=20, textColor=colors.HexColor("#d8e4ef")))
    c.setFillColor(colors.HexColor("#203a55"))
    c.rect(52, 70, 450, 86, stroke=0, fill=1)
    para(c, "边界、三处重点区和依赖图层目前均为 provisional geometry。成果支持内容评审、讨论和入口自检，不构成官方红线、法定控规、工程设计或实施承诺。", 70, 138, 415, ParagraphStyle("covernote", parent=BODY, fontSize=9.5, leading=14, textColor=colors.HexColor("#f3c67e")))
    image_contain(c, FIG / "site-overview.png", 555, 78, width - 605, height - 150, border=False)
    c.setFillColor(colors.HexColor("#b9cadb"))
    c.setFont("Noto", 8)
    c.drawRightString(width - 52, 35, "SHANSHUI2024 · COMMUNITY-DISPLAY-ONLY")
    c.showPage()


def a3_scope(c, page):
    width, height = landscape(A3)
    header(c, width, height, 2, "设计依据、三层范围与证据基线", BLUE)
    top = height - 112
    para(c, "方案以公开、清权、可追溯资料为基础。正式公告和清权任务书支撑任务响应；仓库 provisional geometry 只作临时生成、离线展示与入口自检。", 46, top, width - 92, BODY)
    y = height - 235
    gap = 16
    w = (width - 92 - gap * 2) / 3
    card(c, 46, y, w, 125, "统筹研究范围 / 43.6 km²", "提出 AI 产业生态、人才链、文化叙事、三区两翼协同和全球机制比较。", VIOLET)
    card(c, 46 + w + gap, y, w, 125, "总体设计范围 / 11.41 km²", "组织城市更新、用地结构、交通市政、京张遗址公园活力带与风貌框架。", BLUE)
    card(c, 46 + (w + gap) * 2, y, w, 125, "重点区域 / 约 368.4 ha", "众智园、AI 原点社区、大钟寺三处临时详细设计接口。", AMBER)
    image_contain(c, FIG / "land-use-structure.png", 46, 94, width * .57, 285)
    para(c, "三层范围不是三个孤立图框，而是“研究提出机制、总体组织空间、重点区验证接口”的连续证据链。", width * .60, 365, width * .34, ParagraphStyle("scopecall", parent=BODY, fontSize=15, leading=22, textColor=INK))
    para(c, "设计边界语言：所有空间动作均为概念建议、参考方案或可供专业团队深化研究的材料。官方 polygon、道路红线、控规、产权、文保、市政和交通资料到位后，须替换并整体复算。", width * .60, 287, width * .34, CARD)
    footer(c, width, page, "DESIGN BASIS")
    c.showPage()


def a3_overall(c, page):
    width, height = landscape(A3)
    header(c, width, height, 3, "总体空间结构与城市更新框架", GREEN)
    image_contain(c, FIG / "site-overview.png", 46, 260, width * .57, 430)
    para(c, "一带三核、两翼串联、四类公共接口", width * .60, 685, width * .34, ParagraphStyle("big", parent=BODY, fontSize=19, leading=26, textColor=INK))
    para(c, "一带：沿京张文化线索和蓝绿慢行系统形成公共体验带。\n三核：研发基准核、公共基准核、应用基准核。\n两翼：中关村科技服务翼、小月河场景赋能翼。\n四类接口：站点、校区园区、社区、企业公共界面。", width * .60, 625, width * .34, CARD)
    y = 180
    w = (width - 92 - 20) / 2
    card(c, 46, y, w, 120, "更新逻辑", "保留 - 可逆改造 - 小尺度补充 - 待确认。先做可撤回公共空间试验，再由专业团队依据正式资料深化。", RUST)
    card(c, 56 + w, y, w, 120, "控制边界", "不从概念基底推导 FAR、建筑高度、道路红线、工程管线、拆除结论、投资测算或政府承诺。", AMBER)
    footer(c, width, page, "OVERALL FRAME")
    c.showPage()


def a3_key_areas(c, page):
    width, height = landscape(A3)
    header(c, width, height, 4, "三处重点区域详细设计", VIOLET)
    image_contain(c, FIG / "key-areas.png", 46, 280, width * .56, 415)
    x = width * .60
    card(c, x, 525, width * .34, 135, "01 众智园 / 研发基准核", "安全治理实验室、标准共创工坊、低碳创新廊和可预约验证庭院。", VIOLET)
    card(c, x, 360, width * .34, 135, "02 AI 原点社区 / 公共基准核", "开源发布厅、成果转化客厅、人才服务节点和社区生活接口。", GREEN)
    card(c, x, 195, width * .34, 135, "03 大钟寺 / 应用基准核", "国际路演客厅、智能终端展示、数据要素会客厅和站点步行接口。", AMBER)
    para(c, "三个 polygon 均为 provisional；面积、权属、文保、控规、交通和工程条件待官方及专业资料补齐。", x, 160, width * .34, SMALL)
    footer(c, width, page, "KEY AREAS")
    c.showPage()


def a3_ai(c, page):
    width, height = landscape(A3)
    header(c, width, height, 5, "AI+ 场景、人才画像与公共验证", BLUE)
    image_contain(c, FIG / "mobility-bluegreen.png", 46, 350, width * .50, 330)
    para(c, "五类用户画像", width * .55, 682, width * .38, ParagraphStyle("subhead", parent=BODY, fontSize=17, leading=23, textColor=INK))
    para(c, "开源开发者 / 初创团队 / 企业访客 / 周边居民 / 高校师生", width * .55, 645, width * .38, CARD)
    para(c, "十张场景卡", width * .55, 585, width * .38, ParagraphStyle("subhead2", parent=BODY, fontSize=17, leading=23, textColor=INK))
    para(c, "开源发布厅、城市智能体沙盒、慢行断点诊断、人才生活服务台、AI 安全治理廊、校企转化客厅、数据要素剧场、低碳算力驿站、京张记忆线路、全球 AI 活动周路线。", width * .55, 548, width * .38, CARD)
    y = 160
    w = (width - 92 - 20) / 2
    card(c, 46, y, w, 130, "产业测试 01 / 安全治理沙盒", "公开规则、人工复核和聚合化红队记录；未经授权不采集个人身份信息。", VIOLET)
    card(c, 56 + w, y, w, 130, "产业测试 02-03 / 转化与公共服务", "校企成果转化和低速慢行试验均设置主动授权、知识产权清权、可退出和停止条件。", GREEN)
    footer(c, width, page, "AI SCENARIOS")
    c.showPage()


def a3_delivery(c, page):
    width, height = landscape(A3)
    header(c, width, height, 6, "建筑、更新项目与可逆分期", RUST)
    image_contain(c, FIG / "metrics-evidence.png", 46, 395, width * .46, 295)
    para(c, "建筑层只表达概念基底、动作和待确认控制。30 个基底 feature 的合计面积约 947,895.94 sqm；FAR、总楼面、层数和高度均保持 unknown。", width * .51, 678, width * .42, BOARD_SMALL)
    para(c, "六类更新项目包", width * .51, 585, width * .42, ParagraphStyle("dsub", parent=BODY, fontSize=17, leading=24, textColor=INK))
    para(c, "京张遗址公共客厅 / 三核公共验证庭院 / 校区园区成果转化街 / 清河蓝绿慢行接口 / 大钟寺站四象限步行改善 / 开发者与居民共同运营的夜间知识廊", width * .51, 545, width * .42, CARD)
    y = 180
    w = (width - 92 - 20) / 2
    card(c, 46, y, w, 130, "Phase 01 / 先行公共验证", "铁路记忆步行线、公共接口、无障碍导视、居民服务试点和公开数据说明。", AMBER)
    card(c, 56 + w, y, w, 130, "Phase 02-03 / 联动与扩展", "三核接口联动后，再按人工评估和公众反馈扩展开发者社区、场景卡和国际活动路线。", BLUE)
    footer(c, width, page, "RENEWAL + PHASING")
    c.showPage()


def a3_mobility(c, page):
    width, height = landscape(A3)
    header(c, width, height, 7, "交通慢行、蓝绿公共空间与城市风貌", GREEN)
    image_contain(c, FIG / "mobility-bluegreen.png", 46, 230, width - 92, 455)
    para(c, "六条概念中心线约 38.10 km：慢行主环、铁路记忆步行线、小月河骑行线、三核轨道接驳线和两条社区低速出入线。中央蓝绿公共公地串联口袋空间、铁路记忆公共客厅和线性公共验证台。", 46, 198, width * .53, CARD)
    para(c, "风貌以铁路工程理性、清河蓝绿开放性和中关村创新可见性为三类表达。公共空间优先保障安全、无障碍、基本服务和居民非参与权，不以高科技设备替代日常使用。", width * .58, 198, width * .36, CARD)
    footer(c, width, page, "MOBILITY + BLUE-GREEN")
    c.showPage()


def a3_audit(c, page):
    width, height = landscape(A3)
    header(c, width, height, 8, "指标复算、任务覆盖与风险边界", AMBER)
    image_contain(c, FIG / "metrics-evidence.png", 46, 360, width * .50, 320)
    para(c, "核心指标", width * .56, 680, width * .36, ParagraphStyle("audithead", parent=BODY, fontSize=18, leading=25, textColor=INK))
    para(c, "site_area_sqm = 11,412,825.386 sqm\ngreen_ratio = 0.093021\npublic_space_ratio = 0.047169\nroad_centerline_length_m = 38,101.593 m\nland_use_band_count = 5 / phase_count = 3 / key_area_count = 3", width * .56, 645, width * .36, CARD)
    para(c, "任务与深度", width * .56, 485, width * .36, ParagraphStyle("audithead2", parent=BODY, fontSize=18, leading=25, textColor=INK))
    para(c, "compliance_matrix：23 / 23 mandatory mapped\nstandard_matrix：5 addressed，1 data gap\ndesign_depth_matrix：15 / 15 complete", width * .56, 450, width * .36, CARD)
    c.setFillColor(colors.HexColor("#fff5df"))
    c.rect(46, 120, width - 92, 105, stroke=0, fill=1)
    para(c, "待补资料与法律边界", 66, 205, width - 132, ParagraphStyle("riskhead", parent=BODY, fontSize=16, leading=22, textColor=colors.HexColor("#6f4d16")))
    para(c, "官方 boundary / KEY_AREA polygon、控规与建筑控制、道路红线、权属、文保、交通、市政容量、隐私与安全评估均需由组织方和专业团队补齐。所有空间、建筑、交通、运营和政策内容仅为概念建议。", 66, 175, width - 132, ParagraphStyle("riskbody", parent=BODY, fontSize=10, leading=15, textColor=colors.HexColor("#6f4d16")))
    footer(c, width, page, "AUDIT TRAIL")
    c.showPage()


def build_a3(path):
    width, height = landscape(A3)
    c = canvas.Canvas(str(path), pagesize=(width, height), pageCompression=1)
    c.setTitle("京张智证公地 / JZ BENCHLINE A3 booklet")
    a3_cover(c, 1)
    a3_scope(c, 2)
    a3_overall(c, 3)
    a3_key_areas(c, 4)
    a3_ai(c, 5)
    a3_delivery(c, 6)
    a3_mobility(c, 7)
    a3_audit(c, 8)
    c.save()


def a0_board(c, index, title, accent, image_name, lead, left_title, left_text, right_title, right_text):
    width, height = landscape(A0)
    header(c, width, height, index, title, accent, dark=True)
    image_contain(c, FIG / image_name, 70, 760, width * .57, 1300)
    x = width * .61
    para(c, lead, x, height - 145, width * .31, ParagraphStyle(f"lead{index}", parent=BOARD_BODY, fontSize=24, leading=36, textColor=INK))
    card(c, x, 1180, width * .31, 250, left_title, left_text, accent, BOARD_CARD)
    card(c, x, 875, width * .31, 250, right_title, right_text, BLUE if accent != BLUE else GREEN, BOARD_CARD)
    para(c, "概念建议 / provisional geometry / 供专业团队深化研究", x, 820, width * .31, BOARD_SMALL)
    footer(c, width, index, "A0 BOARD")
    c.showPage()


def build_a0(path):
    width, height = landscape(A0)
    c = canvas.Canvas(str(path), pagesize=(width, height), pageCompression=1)
    c.setTitle("京张智证公地 / JZ BENCHLINE A0 boards")
    a0_board(c, 1, "总体设计结构板", AMBER, "site-overview.png", "一带三核、两翼串联、三类基准互相校验。", "三层范围", "统筹研究范围 43.6 km²；总体设计范围 11.41 km²；三处重点区约 368.4 ha。", "证据主线", "GeoJSON 锁定空间关系，metrics.json 复算比例，矩阵把任务和专业深度挂回正文与图纸。")
    a0_board(c, 2, "用地与城市更新板", VIOLET, "land-use-structure.png", "五类用地共边覆盖临时 site boundary，更新逻辑从保留与可逆改造开始。", "用地分区", "研发与安全治理、社区与人才生活、京张蓝绿公地、铁路文化与公共知识、应用验证与国际交往服务。", "建筑与更新", "30 个概念建筑基底；六类可逆更新项目包；FAR、高度、总楼面和拆改留待正式资料确认。")
    a0_board(c, 3, "交通、蓝绿与公共接口板", GREEN, "mobility-bluegreen.png", "慢行先行，公共空间可达，AI 场景以授权和人工复核进入城市日常。", "交通慢行", "六条概念中心线约 38.10 km，包含主环、铁路记忆线、小月河骑行线和三核接驳线。", "蓝绿公共空间", "中央蓝绿公共公地串联公共客厅、验证庭院和线性公共验证台，居民不参与试验也可正常使用。")
    a0_board(c, 4, "三处重点区域详细设计板", VIOLET, "key-areas.png", "三核承担不同基准，不做同质化科技园。", "01 / 众智园", "研发基准核：安全治理实验室、标准共创工坊、低碳创新廊和验证庭院。", "02-03 / AI 原点与大钟寺", "公共基准核聚焦知识共享和人才生活；应用基准核聚焦国际路演、智能终端和站点步行。")
    a0_board(c, 5, "AI 场景与长期运营板", BLUE, "mobility-bluegreen.png", "十张场景卡把知识生产、产业验证、城市服务和文化体验连成公共路线。", "用户与场景", "五类用户画像、十张场景卡、三类产业测试场景；数据最小化、主动授权、人工复核和可撤回是前置条件。", "长期运营", "春季开发者周、夏季公共开放日、秋季论坛、冬季公开评估为概念节奏，需由运营团队深化。")
    a0_board(c, 6, "指标复核与合规响应板", AMBER, "metrics-evidence.png", "每个空间判断都留有回程证据；未知项保持 unknown。", "核心指标", "site_area_sqm 11,412,825.386；green_ratio 0.093021；public_space_ratio 0.047169；road_centerline_length_m 38,101.593。", "合规状态", "23 / 23 mandatory task mapped；5 项专业标准 addressed、1 项 data gap；15 / 15 design depth complete。provisional 警示不等同于官方批准。")
    c.save()


build_a3(OUT / "a3-booklet.pdf")
build_a0(OUT / "a0-boards.pdf")
print("built", OUT / "a3-booklet.pdf", OUT / "a0-boards.pdf")
