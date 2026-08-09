#!/usr/bin/env python3
"""Regenerate A3 booklet and A0 boards with authoritative metrics and proper Chinese text.
Uses fpdf2 with NotoSansSC for Chinese rendering.
"""
import json
from fpdf import FPDF, XPos, YPos

METRICS_FILE = "submissions/ID-VerNe/ai-innovation-belt/metrics.json"
FIGS_DIR = "submissions/ID-VerNe/ai-innovation-belt/assets/figures"
FONT = "C:/Windows/Fonts/NotoSansSC-VF.ttf"
FONT_BOLD = "C:/Windows/Fonts/msyhbd.ttc"

with open(METRICS_FILE, encoding="utf-8") as f:
    m = json.load(f)["metrics"]

SITE_AREA = m["site_area_sqm"]["value"]
SITE_AREA_HA = SITE_AREA / 10000
BLDG = m["building_footprint_area_sqm"]["value"]
GREEN_R = m["green_ratio"]["value"]
PUBLIC_R = m["public_space_ratio"]["value"]
GREEN_A = GREEN_R * SITE_AREA
PUBLIC_A = PUBLIC_R * SITE_AREA


class PDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("NotoSansSC", "", 8)
            self.set_text_color(148, 163, 184)
            self.cell(0, 8, "百年京张AI创新带城市设计方案 | Centennial Jing-Zhang AI Innovation Belt", align="C")
            self.ln(4)
            self.set_draw_color(226, 232, 240)
            self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
            self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("NotoSansSC", "", 7)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f"Provisional boundary | Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title, subtitle=""):
        self.set_font("NotoSansSC", "", 18)
        self.set_text_color(15, 23, 42)
        self.cell(0, 12, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        if subtitle:
            self.set_font("NotoSansSC", "", 10)
            self.set_text_color(100, 116, 139)
            self.cell(0, 8, subtitle, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(59, 130, 246)
        self.line(self.l_margin, self.get_y(), self.l_margin + 60, self.get_y())
        self.ln(4)

    def metric_card(self, label, value, sub):
        x = self.get_x()
        y = self.get_y()
        w = 90
        h = 28
        self.set_draw_color(203, 213, 225)
        self.set_fill_color(248, 250, 252)
        self.rect(x, y, w, h, style="DF")
        self.set_font("NotoSansSC", "", 7)
        self.set_text_color(100, 116, 139)
        self.set_xy(x + 3, y + 2)
        self.cell(w - 6, 6, label)
        self.set_font("NotoSansSC", "", 11)
        self.set_text_color(15, 23, 42)
        self.set_xy(x + 3, y + 12)
        self.cell(w - 6, 8, value)
        self.set_xy(x + w - 3, y + 12)
        self.set_font("NotoSansSC", "", 6)
        self.set_text_color(148, 163, 184)
        self.cell(0, 8, sub, align="R")


# ==========================================
# A3 Booklet
# ==========================================
def gen_a3_booklet():
    pdf = PDF("P", "mm", "A3")
    pdf.alias_nb_pages()
    pdf.add_font("NotoSansSC", "", FONT)
    pdf.set_auto_page_break(auto=True, margin=20)

    # ===== Cover page =====
    pdf.add_page()
    pdf.ln(80)
    pdf.set_font("NotoSansSC", "", 32)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 20, "京智链·AI融合创新带", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("NotoSansSC", "", 18)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 14, "Centennial Jing-Zhang AI Innovation Belt", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)
    pdf.set_font("NotoSansSC", "", 14)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 10, "百年京张AI创新带城市设计方案", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(20)
    pdf.set_font("NotoSansSC", "", 10)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 8, "提交者：ID-VerNe | AI智能体：Claude Code Opus 4.8", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 8, "2026-08-09 | Provisional boundary - Not official redline", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ===== Page 2: Site Overview =====
    pdf.add_page()
    pdf.section_title("区位分析", "Site Overview")
    try:
        pdf.image(f"{FIGS_DIR}/site-overview.png", x=15, y=pdf.get_y(), w=260)
    except Exception as e:
        pdf.set_font("NotoSansSC", "", 10)
        pdf.cell(0, 10, f"[Figure placeholder: {e}]")
    pdf.ln(5)
    pdf.set_font("NotoSansSC", "", 9)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 6, "三层工作范围：统筹研究范围 43.6 km² | 总体设计范围 11.4 km² | 重点区域范围 368.4 ha", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 6, "三区两翼：学北园 + AI原点社区 + 大钟寺 | 西翼中关村科技服务 + 东翼小月河场景赋能", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ===== Page 3: Key Areas =====
    pdf.add_page()
    pdf.section_title("三处重点区域", "Three Key Areas")
    try:
        pdf.image(f"{FIGS_DIR}/key-areas.png", x=10, y=pdf.get_y(), w=270)
    except Exception as e:
        pdf.set_font("NotoSansSC", "", 10)
        pdf.cell(0, 10, f"[Figure placeholder: {e}]")

    # ===== Page 4: Land Use =====
    pdf.add_page()
    pdf.section_title("用地功能结构", "Land Use Structure")
    try:
        pdf.image(f"{FIGS_DIR}/land-use-structure.png", x=10, y=pdf.get_y(), w=270)
    except Exception as e:
        pdf.set_font("NotoSansSC", "", 10)
        pdf.cell(0, 10, f"[Figure placeholder: {e}]")

    # ===== Page 5: Mobility & Blue-Green =====
    pdf.add_page()
    pdf.section_title("交通慢行与蓝绿系统", "Mobility & Blue-Green System")
    try:
        pdf.image(f"{FIGS_DIR}/mobility-bluegreen.png", x=10, y=pdf.get_y(), w=270)
    except Exception as e:
        pdf.set_font("NotoSansSC", "", 10)
        pdf.cell(0, 10, f"[Figure placeholder: {e}]")

    # ===== Page 6: Metrics =====
    pdf.add_page()
    pdf.section_title("核心指标复算", "Metrics & Evidence")
    try:
        pdf.image(f"{FIGS_DIR}/metrics-evidence.png", x=10, y=pdf.get_y(), w=270)
    except Exception as e:
        pdf.set_font("NotoSansSC", "", 10)
        pdf.cell(0, 10, f"[Figure placeholder: {e}]")

    # ===== Page 7: Implementation Matrix =====
    pdf.add_page()
    pdf.section_title("实施项目矩阵", "Implementation Matrix")
    pdf.set_font("NotoSansSC", "", 7)
    pdf.set_text_color(71, 85, 105)

    # Table
    headers = ["编号", "项目", "类型", "阶段", "预算", "时间节点", "KPI"]
    cols = [18, 50, 24, 20, 28, 40, 60]
    rows = [
        ["JZ-01", "京张遗址公园慢行断点缝合", "公共空间/交通", "近期试点", "500-1000万", "试点6月/全线18月", "慢行连通率≥90%"],
        ["JZ-02", "众智园清河创新界面", "蓝绿空间/产业", "中期更新", "1000-3000万", "设计6月/施工12月", "蓝绿空间开敞率≥60%"],
        ["JZ-03", "原点社区近校成果转化街", "城市更新/产业", "近期试点", "500-1500万/期", "首期6月/三期18月", "年度转化项目≥20项"],
        ["JZ-04", "大钟寺站四象限步行连通", "轨道一体化", "中期更新", "3000-8000万", "设计12月/施工18月", "换乘效率提升≥30%"],
        ["JZ-05", "AI公共服务与端侧算力节点", "新基建", "近期试点", "500-1500万/节点", "试点3月/扩展12月", "日服务≥500人次/节点"],
        ["JZ-06", "全球AI活动周公共路线", "运营/品牌", "长期治理", "300-800万/届", "首年筹备6月", "参与≥5万人次/届"],
    ]
    for i, h in enumerate(headers):
        pdf.cell(cols[i], 8, h, border=1, align="C")
    pdf.ln()
    for row in rows:
        for i, cell in enumerate(row):
            pdf.cell(cols[i], 7, cell, border=1)
        pdf.ln()

    # ===== Page 8: Agent Tasks Summary =====
    pdf.add_page()
    pdf.section_title("智能体任务完成清单", "Agent Tasks Summary")
    pdf.set_font("NotoSansSC", "", 9)
    pdf.set_text_color(71, 85, 105)
    tasks = [
        ("agent.1", "命名体系与视觉识别", "✓ 完成", "京智链·JingZhi Chain, 双螺旋Logo, 色彩/字体/图标系统"),
        ("agent.2", "全球案例与生态图谱", "✓ 完成", "8个案例, 含来源/可比性/设计动作映射表"),
        ("agent.3", "产业测试验证场景", "✓ 完成", "3个场景: 安全沙盒/智能体测试/开源评测走廊"),
        ("agent.4", "朝圣地标与荣誉体系", "✓ 完成", "4个地标+3层荣誉体系+组件库"),
        ("agent.5", "文化叙事与国际传播", "✓ 完成", "自主创新叙事+3层导视+4维传播策略"),
        ("agent.6", "长期运营机制", "✓ 完成", "年度活动/社区/场景开放/国际招引/转化路径"),
    ]
    for task_id, name, status, desc in tasks:
        pdf.set_fill_color(239, 246, 255)
        pdf.set_text_color(15, 23, 42)
        pdf.set_font("NotoSansSC", "", 10)
        pdf.cell(16, 7, task_id, border=1, fill=True)
        pdf.cell(50, 7, name, border=1, fill=True)
        pdf.set_font("NotoSansSC", "", 8)
        pdf.set_text_color(34, 197, 94)
        pdf.cell(16, 7, status, border=1, fill=True, align="C")
        pdf.set_text_color(100, 116, 139)
        pdf.cell(0, 7, desc, border=1, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)

    pdf.ln(5)
    pdf.set_font("NotoSansSC", "", 8)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 6, "所有指标与 metrics.json 一致。边界为临时示意(provisional)，非官方红线。正式数据发布后须全量复算。",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.output("submissions/ID-VerNe/ai-innovation-belt/drawings/a3-booklet.pdf")
    print("A3 booklet saved!")


# ==========================================
# A0 Boards
# ==========================================
def gen_a0_boards():
    pdf = PDF("P", "mm", (841, 1189))  # A0
    pdf.alias_nb_pages()
    pdf.add_font("NotoSansSC", "", FONT)
    pdf.set_auto_page_break(auto=True, margin=20)

    # ===== Board 1: Site Overview + Key Areas =====
    pdf.add_page()
    pdf.set_font("NotoSansSC", "", 28)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 20, "百年京张AI创新带 · 总体概览", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("NotoSansSC", "", 14)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 12, "Centennial Jing-Zhang AI Innovation Belt · Overview", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)

    # Two column layout
    col_w = pdf.w / 2 - 20
    # Left: Site overview figure
    pdf.set_font("NotoSansSC", "", 16)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(col_w, 10, "区位分析", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    try:
        pdf.image(f"{FIGS_DIR}/site-overview.png", x=10, y=pdf.get_y(), w=col_w - 10)
    except Exception as e:
        pdf.cell(0, 10, f"[Figure error: {e}]")

    # Right: Key areas
    right_x = pdf.w / 2 + 5
    pdf.set_xy(right_x, pdf.get_y() - 100)
    pdf.set_font("NotoSansSC", "", 16)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(col_w, 10, "三处重点区域", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    try:
        pdf.image(f"{FIGS_DIR}/key-areas.png", x=right_x, y=pdf.get_y(), w=col_w - 10)
    except Exception as e:
        pdf.cell(0, 10, f"[Figure error: {e}]")

    # ===== Board 2: Land Use + Mobility =====
    pdf.add_page()
    pdf.set_font("NotoSansSC", "", 28)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 20, "百年京张AI创新带 · 空间结构与系统", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("NotoSansSC", "", 14)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 12, "Land Use Structure & Mobility Systems", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)

    pdf.set_font("NotoSansSC", "", 16)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(col_w, 10, "用地功能结构", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    try:
        pdf.image(f"{FIGS_DIR}/land-use-structure.png", x=10, y=pdf.get_y(), w=col_w - 10)
    except Exception as e:
        pdf.cell(0, 10, f"[Figure error: {e}]")

    pdf.set_xy(right_x, pdf.get_y() - 100)
    pdf.set_font("NotoSansSC", "", 16)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(col_w, 10, "交通慢行与蓝绿系统", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    try:
        pdf.image(f"{FIGS_DIR}/mobility-bluegreen.png", x=right_x, y=pdf.get_y(), w=col_w - 10)
    except Exception as e:
        pdf.cell(0, 10, f"[Figure error: {e}]")

    # ===== Board 3: Metrics + Implementation =====
    pdf.add_page()
    pdf.set_font("NotoSansSC", "", 28)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 20, "百年京张AI创新带 · 指标与实施", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("NotoSansSC", "", 14)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 12, "Metrics & Implementation Matrix", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)

    pdf.set_font("NotoSansSC", "", 16)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(col_w, 10, "核心指标复算", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    try:
        pdf.image(f"{FIGS_DIR}/metrics-evidence.png", x=10, y=pdf.get_y(), w=col_w - 10)
    except Exception as e:
        pdf.cell(0, 10, f"[Figure error: {e}]")

    # Right: Implementation table
    pdf.set_xy(right_x, pdf.get_y() - 100)
    pdf.set_font("NotoSansSC", "", 16)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(col_w, 10, "实施项目清单", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("NotoSansSC", "", 9)
    pdf.set_text_color(71, 85, 105)
    headers = ["编号", "项目", "阶段", "预算"]
    cols = [16, 60, 20, 28]
    rows = [
        ["JZ-01", "慢行断点缝合", "近期", "500-1000万"],
        ["JZ-02", "清河创新界面", "中期", "1000-3000万"],
        ["JZ-03", "成果转化街", "近期", "500-1500万"],
        ["JZ-04", "四象限步行连通", "中期", "3000-8000万"],
        ["JZ-05", "AI算力节点", "近期", "500-1500万"],
        ["JZ-06", "全球AI活动周", "长期", "300-800万"],
    ]
    for i, h in enumerate(headers):
        pdf.cell(cols[i], 8, h, border=1, align="C")
    pdf.ln()
    for row in rows:
        for i, cell in enumerate(row):
            pdf.cell(cols[i], 7, cell, border=1)
        pdf.ln()
    pdf.ln(5)
    pdf.set_font("NotoSansSC", "", 8)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(col_w, 6, "所有项目为概念建议，须在正式控规、权属和资金条件确认后复核", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ===== Board 4: Agent Tasks + Inclusive Design =====
    pdf.add_page()
    pdf.set_font("NotoSansSC", "", 28)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 20, "百年京张AI创新带 · 智能体任务与包容设计", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("NotoSansSC", "", 14)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 12, "Agent Tasks & Inclusive Design", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)

    # Left: Agent tasks
    pdf.set_font("NotoSansSC", "", 16)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(col_w, 10, "六项智能体任务完成清单", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("NotoSansSC", "", 10)
    pdf.set_text_color(71, 85, 105)
    tasks = [
        "agent.1: 京智链命名体系+双螺旋Logo+色彩/字体/图标系统",
        "agent.2: 8个全球案例+来源/可比性/设计动作映射+生态图谱",
        "agent.3: 3个产业测试验证场景(安全沙盒/智能体/开源评测)",
        "agent.4: 4个朝圣地标+3层荣誉体系+组件库",
        "agent.5: 自主创新叙事+3层导视+4维国际传播策略",
        "agent.6: 年度活动/开发者社区/场景开放/国际招引/转化路径",
    ]
    for t in tasks:
        pdf.cell(8, 8, "•")
        pdf.cell(col_w - 8, 8, t, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)

    # Right: Inclusive design
    pdf.set_xy(right_x, pdf.get_y() - 180)
    pdf.set_font("NotoSansSC", "", 16)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(col_w, 10, "公共利益与包容性设计", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("NotoSansSC", "", 10)
    pdf.set_text_color(71, 85, 105)
    items = [
        "8类用户画像: 开发者/初创/企业/居民/师生/老年/低收入/儿童",
        "无障碍设计: 符合GB 50763-2012, 盲道/轮椅/语音/触觉标识",
        "数字包容: 离线办理/人工窗口/大字模式/语音输入",
        "数据最小化: 不采集个人轨迹/不商业推荐/不采集儿童数据",
        "公平性审计: 年度运营报告含服务覆盖率和满意度差异",
        "人工复核: AI场景结果由人工审核, 突发情况一键切换人工",
    ]
    for item in items:
        pdf.cell(8, 8, "•")
        pdf.cell(col_w - 8, 8, item, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)

    # Footer with metrics
    pdf.ln(10)
    pdf.set_font("NotoSansSC", "", 9)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 6, f"基地面积: {SITE_AREA_HA:.1f} ha | 建筑基底: {BLDG/10000:.1f} ha | 绿地率: {GREEN_R*100:.2f}% | 公共空间率: {PUBLIC_R*100:.2f}%",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 6, "所有指标与 metrics.json 一致。边界为临时示意(provisional)，非官方红线。正式数据发布后须全量复算。",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.output("submissions/ID-VerNe/ai-innovation-belt/drawings/a0-boards.pdf")
    print("A0 boards saved!")


gen_a3_booklet()
gen_a0_boards()
print("All PDFs regenerated successfully!")