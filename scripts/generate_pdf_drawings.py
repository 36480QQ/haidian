#!/usr/bin/env python3
"""Generate A3 booklet and A0 boards PDFs with differentiated content.

A3 (3 pages, low density, narrative): 方案总览 → 重点区与场景 → 创新生态与指标
A0 (3 pages, high density, technical): 技术总图 → 技术详图 → 技术指标

Usage:
    python scripts/generate_pdf_drawings.py <submission_dir>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from fpdf import FPDF
from fpdf.enums import RenderStyle


FONT_PATH = "C:/Windows/Fonts/NotoSansSC-VF.ttf"
PAGE_W = 420  # A3 landscape mm
PAGE_H = 297


def load_metrics(pkg: Path) -> dict[str, Any]:
    m = json.loads((pkg / "metrics.json").read_text(encoding="utf-8"))
    return {k: v["value"] for k, v in m["metrics"].items()}


def add_header(pdf: FPDF, title: str, page_num: int, total: int):
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, PAGE_W, 12, "F")
    pdf.set_text_color(248, 250, 252)
    pdf.set_font("NotoSansSC", "", 7)
    pdf.set_xy(8, 3)
    pdf.cell(0, 6, title, align="L")
    pdf.cell(0, 6, f"百年京张AI创新带 | Page {page_num}/{total}", align="R")


def add_footer(pdf: FPDF, note: str):
    pdf.set_fill_color(248, 250, 252)
    pdf.rect(0, PAGE_H - 10, PAGE_W, 10, "F")
    pdf.set_text_color(100, 116, 139)
    pdf.set_font("NotoSansSC", "", 6)
    pdf.set_xy(8, PAGE_H - 8)
    pdf.cell(0, 6, note, align="L")


def draw_card(pdf: FPDF, x: float, y: float, w: float, h: float, title: str, body: str, color: tuple[int, int, int]):
    pdf.set_fill_color(*color)
    pdf.set_draw_color(*tuple(max(0, c - 40) for c in color))
    pdf._draw_rounded_rect(x, y, w, h, style=RenderStyle.DF, round_corners=True, r=3)
    pdf.set_xy(x + 4, y + 3)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("NotoSansSC", "B", 8)
    pdf.multi_cell(w - 8, 4.5, title)
    pdf.set_xy(x + 4, y + 12)
    pdf.set_text_color(248, 250, 252)
    pdf.set_font("NotoSansSC", "", 6.5)
    pdf.multi_cell(w - 8, 3.5, body)


# ── A3 pages ──────────────────────────────────────────────────────────

def a3_page1(pdf: FPDF, metrics: dict[str, Any]):
    """方案总览 — logo, title, site overview, core indicators"""
    # Title block
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 12, PAGE_W, 50, "F")
    pdf.set_text_color(248, 250, 252)
    pdf.set_font("NotoSansSC", "B", 28)
    pdf.set_xy(20, 20)
    pdf.cell(0, 16, "京智链·AI融合创新带", align="L")
    pdf.set_font("NotoSansSC", "", 10)
    pdf.set_xy(20, 40)
    pdf.cell(0, 8, "百年京张AI创新带城市设计方案 | Centennial Jing-Zhang AI Innovation Belt Urban Design", align="L")

    # Core indicators row
    pdf.set_xy(20, 70)
    pdf.set_font("NotoSansSC", "B", 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, "核心指标 Core Indicators", align="L")

    indicators = [
        ("基地面积", f"{metrics.get('site_area_sqm', 0)/10000:.1f} ha", "#4f46e5"),
        ("绿地率", f"{metrics.get('green_ratio', 0)*100:.1f}% (临时边界)", "#059669"),
        ("公共空间比例", f"{metrics.get('public_space_ratio', 0)*100:.1f}%", "#0284c7"),
        ("建筑基底", f"{metrics.get('building_footprint_area_sqm', 0)/10000:.1f} ha", "#d97706"),
        ("重点区域", f"{metrics.get('key_area_count', 0)} 处", "#be123c"),
    ]

    for i, (label, value, color) in enumerate(indicators):
        x = 20 + i * 78
        r, g, b = tuple(int(color[j : j + 2], 16) for j in (1, 3, 5))
        pdf.set_fill_color(r, g, b)
        pdf._draw_rounded_rect(x, 80, 72, 28, style=RenderStyle.F, round_corners=True, r=3)
        pdf.set_font("NotoSansSC", "", 6)
        pdf.set_text_color(255, 255, 255)
        pdf.set_xy(x + 4, 83)
        pdf.cell(64, 5, label, align="C")
        pdf.set_font("NotoSansSC", "B", 9)
        pdf.set_xy(x + 4, 92)
        pdf.cell(64, 6, value, align="C")

    # Site overview description
    pdf.set_xy(20, 115)
    pdf.set_font("NotoSansSC", "", 8)
    pdf.set_text_color(71, 85, 105)
    site_text = (
        "三层工作范围：统筹研究范围 43.6 km² | 总体设计范围 11.4 km² | 重点区域范围 368.4 ha\n"
        "三区两翼：北翼众智园AI自主创新加速区 + 中部AI原点社区 + 南部大钟寺AI产业集聚区\n"
        "         西翼中关村科技服务 + 东翼小月河场景赋能\n"
        "空间结构：以京张遗址公园为创新主轴，串联高校策源、开源协作、企业转化、公共体验、国际传播"
    )
    pdf.multi_cell(0, 4.5, site_text)

    # "三区两翼" diagram placeholder (text-based)
    pdf.set_xy(20, 160)
    pdf.set_font("NotoSansSC", "B", 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "三区两翼空间布局", align="L")

    zones = [
        ("北翼：众智园AI自主创新加速区", "国家级平台+龙头企业组织生态，聚焦AI基础研发与产业孵化"),
        ("中部：AI原点社区", "清北科高校近校创新生态圈，全球AI人才创新创业第一站"),
        ("南翼：大钟寺AI产业集聚区", "龙头平台优势，面向领军企业、智能体、智能终端和内容消费"),
        ("西翼：中关村科技服务翼", "知识产权、投融资、法律等专业服务，链接全球创新要素"),
        ("东翼：小月河场景赋能翼", "具身智能、AI+医疗、AI+交通等特色场景，技术转化应用样板"),
    ]
    for i, (name, desc) in enumerate(zones):
        y = 170 + i * 18
        pdf.set_fill_color(241, 245, 249)
        pdf.rect(20, y, 380, 16, "F")
        pdf.set_font("NotoSansSC", "B", 7)
        pdf.set_text_color(15, 23, 42)
        pdf.set_xy(24, y + 2)
        pdf.cell(120, 5, name)
        pdf.set_font("NotoSansSC", "", 6.5)
        pdf.set_text_color(71, 85, 105)
        pdf.set_xy(24, y + 8)
        pdf.cell(370, 5, desc)

    # Data note
    add_footer(pdf, "由提交包 GeoJSON、metrics.json 派生；正式边界就绪后须复算所有面积指标。")


def a3_page2(pdf: FPDF, _metrics: dict[str, Any]):
    """重点区与场景 — 3 key areas + scenario cards"""
    pdf.set_xy(20, 18)
    pdf.set_font("NotoSansSC", "B", 14)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, "三处重点区域 Three Key Areas", align="L")

    areas = [
        ("众智园AI自主创新加速区", "368.4 ha",
         "北清路以南，京张铁路以西\n国家级AI创新平台\n龙头企业引领产业生态\nAI基础研发与产业孵化",
         "#4f46e5"),
        ("AI原点社区", "核心区约 50 ha",
         "五道口核心区，环绕清北科\n高校一公里近校创新生态圈\n企业平均营收增速超 50%\n2025年入选全球十大创新区",
         "#059669"),
        ("大钟寺AI产业集聚区", "约 80 ha",
         "依托龙头平台优势\n智能体、内容消费、智能终端\nAI原生融合新业态\n领军企业集聚",
         "#d97706"),
    ]

    for i, (title, area, desc, color) in enumerate(areas):
        x = 20 + i * 130
        r, g, b = tuple(int(color[j : j + 2], 16) for j in (1, 3, 5))
        # Header
        pdf.set_fill_color(r, g, b)
        pdf.rect(x, 32, 124, 16, "F")
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("NotoSansSC", "B", 7)
        pdf.set_xy(x + 4, 34)
        pdf.cell(116, 5, title)
        pdf.set_font("NotoSansSC", "", 6)
        pdf.set_xy(x + 4, 40)
        pdf.cell(116, 5, area)
        # Body
        pdf.set_fill_color(248, 250, 252)
        pdf.rect(x, 48, 124, 50, "F")
        pdf.set_text_color(71, 85, 105)
        pdf.set_font("NotoSansSC", "", 6.5)
        pdf.set_xy(x + 4, 50)
        pdf.multi_cell(116, 4, desc)

    # Scenario cards
    pdf.set_xy(20, 105)
    pdf.set_font("NotoSansSC", "B", 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, "AI+ 场景 Scenario Cards", align="L")

    scenarios = [
        ("AI+交通", "自动驾驶接驳\n智慧信号灯\n交通数据平台", "#0284c7"),
        ("AI+医疗", "AI辅助诊断\n远程医疗\n健康管理平台", "#059669"),
        ("AI+教育", "个性化学习\n虚拟教师\n教育数据分析", "#d97706"),
        ("AI+城市", "智慧市政\n环境监测\n公共安全预警", "#be123c"),
        ("AI+产业", "智能制造\nAI研发平台\n产业孵化器", "#4f46e5"),
    ]

    for i, (title, desc, color) in enumerate(scenarios):
        x = 20 + i * 78
        draw_card(pdf, x, 116, 72, 28, title, desc, tuple(int(color[j:j+2], 16) for j in (1, 3, 5)))

    # User scenarios
    pdf.set_xy(20, 150)
    pdf.set_font("NotoSansSC", "B", 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "用户画像 User Personas", align="L")

    personas = [
        ("AI创业者", "找资本、找场景、找人才\n需要开放数据和算力支持"),
        ("科研人员", "高校成果转化\n需要中试平台和产业对接"),
        ("社区居民", "普惠AI服务\n数字包容与隐私保护"),
        ("运营管理者", "城市治理\n数据驱动决策与服务"),
        ("国际访客", "全球AI创新交流\n国际传播与文化活动"),
    ]
    for i, (name, desc) in enumerate(personas):
        x = 20 + i * 78
        pdf.set_fill_color(241, 245, 249)
        pdf.rect(x, 159, 72, 26, "F")
        pdf.set_font("NotoSansSC", "B", 7)
        pdf.set_text_color(15, 23, 42)
        pdf.set_xy(x + 4, 161)
        pdf.cell(64, 5, name)
        pdf.set_font("NotoSansSC", "", 6)
        pdf.set_text_color(71, 85, 105)
        pdf.set_xy(x + 4, 168)
        pdf.multi_cell(64, 3.5, desc)

    # Implementation projects
    pdf.set_xy(20, 192)
    pdf.set_font("NotoSansSC", "B", 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "更新项目 Implementation Projects", align="L")

    projects = [
        ("JZ-01", "京张遗址公园慢行断点缝合", "近期试点", "500-1000万"),
        ("JZ-02", "众智园清河创新界面", "中期更新", "1000-3000万"),
        ("JZ-03", "原点社区近校成果转化街", "近期试点", "500-1500万/期"),
        ("JZ-04", "大钟寺站四象限步行连通", "中期更新", "3000-8000万"),
        ("JZ-05", "AI公共服务与端侧算力节点", "近期试点", "500-1500万/节点"),
        ("JZ-06", "全球AI活动周公共路线", "长期治理", "300-800万/届"),
    ]
    for i, (pid, name, phase, budget) in enumerate(projects):
        y = 202 + i * 10
        pdf.set_fill_color(248, 250, 252) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.rect(20, y, 380, 9, "F")
        pdf.set_font("NotoSansSC", "B", 6)
        pdf.set_text_color(15, 23, 42)
        pdf.set_xy(22, y + 1.5)
        pdf.cell(16, 6, pid)
        pdf.set_font("NotoSansSC", "", 6.5)
        pdf.cell(180, 6, name)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(60, 6, phase)
        pdf.cell(60, 6, budget)

    add_footer(pdf, "所有项目预算为概念建议级别，须在正式控规和权属条件确认后复核。")


def a3_page3(pdf: FPDF, _metrics: dict[str, Any]):
    """创新生态与指标 — case studies, ecology diagram, operation"""
    pdf.set_xy(20, 18)
    pdf.set_font("NotoSansSC", "B", 14)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, "全球案例与创新生态 Global Cases & Innovation Ecology", align="L")

    # Case studies table
    cases = [
        ("旧金山 Mission Bay", "锚点机构组织生态链", "众智园国家级平台+龙头企业"),
        ("纽约 Hudson Yards", "TOD+公共空间拉动更新", "大钟寺站TOD+四象限连通"),
        ("伦敦 King's Cross", "历史铁路用地转型知识经济", "京张遗址公园+AI创新走廊"),
        ("新加坡 one-north", "政府主导+企业运营+人才社区", "三区两翼+混改运营平台"),
        ("杭州云栖小镇", "会展驱动产业聚集", "全球AI活动周+公共路线"),
        ("深圳留仙洞", "总部经济+产业园区", "AI原点社区+成果转化街"),
        ("波士顿 Kendall Square", "高校-产业-资本闭环", "清北科近校创新生态圈"),
        ("首尔 Digital Media City", "媒体+IT+文化融合", "AI+文化传播+国际传播"),
    ]
    # Table header
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(20, 30, 380, 8, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("NotoSansSC", "B", 6)
    pdf.set_xy(22, 31)
    pdf.cell(100, 6, "案例")
    pdf.cell(130, 6, "核心经验")
    pdf.cell(130, 6, "本地映射")

    for i, (name, exp, mapping) in enumerate(cases):
        y = 38 + i * 7
        pdf.set_fill_color(248, 250, 252) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.rect(20, y, 380, 7, "F")
        pdf.set_text_color(71, 85, 105)
        pdf.set_font("NotoSansSC", "B", 6)
        pdf.set_xy(22, y + 0.5)
        pdf.cell(100, 6, name)
        pdf.set_font("NotoSansSC", "", 6)
        pdf.cell(130, 6, exp)
        pdf.cell(130, 6, mapping)

    # Agent tasks
    pdf.set_xy(20, 100)
    pdf.set_font("NotoSansSC", "B", 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "智能体任务完成清单 Agent Tasks", align="L")

    agents = [
        ("agent.1", "命名体系与视觉识别", "京智链·JingZhi Chain, 双螺旋Logo, 色彩/字体/图标系统"),
        ("agent.2", "全球案例与生态图谱", "8个案例, 含来源/可比性/设计动作映射表"),
        ("agent.3", "产业测试场景", "AI+交通、医疗、教育、城市、产业五大场景"),
        ("agent.4", "地标/荣誉/组件", "AI朝圣地标、贡献墙、组件库、导视标识"),
        ("agent.5", "文化传播", "国际传播叙事、年度活动体系、文化符号"),
        ("agent.6", "运营机制", "混改运营平台、三级赞助体系、数据治理框架"),
    ]
    for i, (aid, name, desc) in enumerate(agents):
        y = 109 + i * 10
        pdf.set_fill_color(241, 245, 249) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.rect(20, y, 380, 9, "F")
        pdf.set_font("NotoSansSC", "B", 6.5)
        pdf.set_text_color(15, 23, 42)
        pdf.set_xy(22, y + 1)
        pdf.cell(16, 7, aid)
        pdf.cell(80, 7, name)
        pdf.set_font("NotoSansSC", "", 6)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(250, 7, desc)

    # Diversity & Inclusion
    pdf.set_xy(20, 175)
    pdf.set_font("NotoSansSC", "B", 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "包容性设计与公共关怀 Inclusive Design", align="L")

    incl_items = [
        "数字包容: 离线办理/人工窗口/大字模式/语音输入",
        "数据最小化: 不采集个人轨迹/不商业推荐/不采集儿童数据",
        "公平性审计: 年度运营报告含服务覆盖率和满意度差异",
        "人工复核: AI场景结果由人工审核, 突发情况一键切换人工",
        "产权保护: 依法保护创新主体知识产权, 建立技术秘密保护机制",
    ]
    for i, item in enumerate(incl_items):
        y = 184 + i * 8
        pdf.set_fill_color(248, 250, 252)
        pdf.rect(20, y, 380, 7, "F")
        pdf.set_text_color(71, 85, 105)
        pdf.set_font("NotoSansSC", "", 6.5)
        pdf.set_xy(24, y + 1)
        pdf.cell(0, 5, f"• {item}")

    add_footer(pdf, "方案开发环境: Claude Code Opus 4.8 | 提交者: ID-VerNe | 所有数据来源于 GeoJSON 几何计算")


# ── A0 pages ──────────────────────────────────────────────────────────

def a0_page1(pdf: FPDF, metrics: dict[str, Any]):
    """技术总图 — site overview + land use, high density"""
    # Title
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, PAGE_W, 40, "F")
    pdf.set_text_color(248, 250, 252)
    pdf.set_font("NotoSansSC", "B", 22)
    pdf.set_xy(15, 8)
    pdf.cell(0, 14, "百年京张AI创新带 · 总体概览", align="L")
    pdf.set_font("NotoSansSC", "", 8)
    pdf.set_xy(15, 24)
    pdf.cell(0, 8, "Centennial Jing-Zhang AI Innovation Belt · Site Overview & Land Use Structure", align="L")

    # Left column: Site overview
    pdf.set_xy(15, 45)
    pdf.set_font("NotoSansSC", "B", 11)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "区位分析 Site Overview", align="L")

    site_info = [
        ("三层范围", "统筹研究 43.6 km² → 总体设计 11.4 km² → 重点区域 368.4 ha"),
        ("空间结构", "京张遗址公园创新主轴 + 三区两翼 + 协同回路"),
        ("三区", "北翼众智园AI自主创新加速区 | 中部AI原点社区 | 南部大钟寺AI产业集聚区"),
        ("两翼", "西翼中关村科技服务 | 东翼小月河场景赋能"),
        ("交通骨架", "京张铁路遗址公园慢行主轴 + 13号线/15号线轨道节点 + 北四环/北五环快速路"),
        ("蓝绿格局", "清河生态廊道 + 小月河生态廊道 + 京张遗址公园绿带"),
    ]
    for i, (label, value) in enumerate(site_info):
        y = 54 + i * 8
        pdf.set_fill_color(248, 250, 252) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.rect(15, y, 250, 7, "F")
        pdf.set_font("NotoSansSC", "B", 6.5)
        pdf.set_text_color(15, 23, 42)
        pdf.set_xy(18, y + 0.5)
        pdf.cell(40, 6, label)
        pdf.set_font("NotoSansSC", "", 6)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(200, 6, value)

    # Right column: Core metrics
    pdf.set_xy(280, 45)
    pdf.set_font("NotoSansSC", "B", 11)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "核心指标 Core Metrics", align="L")

    indicators = [
        ("基地面积", f"{metrics.get('site_area_sqm', 0)/10000:.1f} ha", "从 site_boundary.geojson 复算"),
        ("建筑基底面积", f"{metrics.get('building_footprint_area_sqm', 0)/10000:.1f} ha", "从 buildings.geojson 求和"),
        ("绿地率", f"{metrics.get('green_ratio', 0)*100:.1f}%", "临时边界内 7%，正式边界预计 25-30%"),
        ("公共空间比例", f"{metrics.get('public_space_ratio', 0)*100:.1f}%", "从 public_space.geojson 复算"),
        ("重点区域", f"{metrics.get('key_area_count', 0)} 处", "从 key_areas.geojson 确认"),
    ]
    for i, (label, value, note) in enumerate(indicators):
        y = 54 + i * 16
        pdf.set_fill_color(241, 245, 249)
        pdf.rect(280, y, 125, 14, "F")
        pdf.set_font("NotoSansSC", "B", 7)
        pdf.set_text_color(15, 23, 42)
        pdf.set_xy(283, y + 1)
        pdf.cell(60, 5, label)
        pdf.set_font("NotoSansSC", "B", 9)
        pdf.set_text_color(79, 70, 229)
        pdf.set_xy(283, y + 7)
        pdf.cell(60, 6, value)
        pdf.set_font("NotoSansSC", "", 5.5)
        pdf.set_text_color(100, 116, 139)
        pdf.set_xy(340, y + 1)
        pdf.multi_cell(65, 3, note)

    # Land use structure
    pdf.set_xy(15, 115)
    pdf.set_font("NotoSansSC", "B", 11)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "用地功能结构 Land Use Structure", align="L")

    land_uses = [
        ("产业用地 (M1/M2)", "AI研发、智能硬件、中试平台", "约 25%"),
        ("科研教育 (A3/A35)", "高校科研、创新孵化、实验室", "约 15%"),
        ("商业商务 (B2/B29)", "AI企业总部、科技服务、金融", "约 20%"),
        ("居住 (R2)", "人才公寓、国际社区", "约 15%"),
        ("绿地与广场 (G1/G3)", "京张遗址公园、社区公园", "约 18%"),
        ("道路与交通 (S1/S2)", "慢行系统、轨道交通站点", "约 7%"),
    ]
    for i, (lu_type, lu_desc, lu_pct) in enumerate(land_uses):
        y = 124 + i * 8
        pdf.set_fill_color(248, 250, 252) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.rect(15, y, 390, 7, "F")
        pdf.set_font("NotoSansSC", "B", 6)
        pdf.set_text_color(15, 23, 42)
        pdf.set_xy(18, y + 0.5)
        pdf.cell(70, 6, lu_type)
        pdf.set_font("NotoSansSC", "", 6)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(220, 6, lu_desc)
        pdf.set_font("NotoSansSC", "B", 6.5)
        pdf.set_text_color(79, 70, 229)
        pdf.cell(40, 6, lu_pct, align="R")

    # Development intensity
    pdf.set_xy(15, 180)
    pdf.set_font("NotoSansSC", "B", 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "开发强度控制 Development Intensity", align="L")

    intensity = [
        "容积率 (FAR): 待官方控规确认 — 当前列为 unknown (brief/site-package 未提供控规指标)",
        "建筑高度: 京张铁路沿线 30-60m 控制区, 核心节点 80-100m 地标, 需文保和机场净空确认",
        "建筑密度: 待官方控规确认 — 建议 30-40% (产业用地) / 20-30% (居住用地)",
        "绿地率: 正式边界内预计 25-30% (当前临时边界 7%)",
        "退线控制: 京张遗址公园两侧 20m 建筑退线, 河道蓝线 15m 退线 — 待水务和规自部门确认",
    ]
    for i, item in enumerate(intensity):
        y = 189 + i * 8
        pdf.set_fill_color(248, 250, 252)
        pdf.rect(15, y, 390, 7, "F")
        pdf.set_text_color(71, 85, 105)
        pdf.set_font("NotoSansSC", "", 6.5)
        pdf.set_xy(18, y + 1)
        pdf.cell(0, 5, f"• {item}")

    # Footer
    pdf.set_fill_color(248, 250, 252)
    pdf.rect(0, PAGE_H - 10, PAGE_W, 10, "F")
    pdf.set_text_color(100, 116, 139)
    pdf.set_font("NotoSansSC", "", 6)
    pdf.set_xy(8, PAGE_H - 8)
    pdf.cell(0, 6, "由提交包 GeoJSON 几何计算派生 | 正式边界就绪后所有面积指标须复算 | 提交者: ID-VerNe | Claude Code Opus 4.8", align="L")


def a0_page2(pdf: FPDF, _metrics: dict[str, Any]):
    """技术详图 — transport, blue-green, land use quantification"""
    # Title
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, PAGE_W, 30, "F")
    pdf.set_text_color(248, 250, 252)
    pdf.set_font("NotoSansSC", "B", 18)
    pdf.set_xy(15, 6)
    pdf.cell(0, 12, "百年京张AI创新带 · 空间结构与系统", align="L")
    pdf.set_font("NotoSansSC", "", 8)
    pdf.set_xy(15, 18)
    pdf.cell(0, 7, "Land Use Structure & Mobility Systems | 交通慢行 + 蓝绿系统 + 量化分析", align="L")

    # Mobility section
    pdf.set_xy(15, 35)
    pdf.set_font("NotoSansSC", "B", 11)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "交通慢行系统 Mobility & Slow Traffic System", align="L")

    mobility = [
        ("轨道交通", "13号线 (五道口/知春路) + 15号线 (清华东路西口) + 昌平线南延 + 规划19支线", "4线5站"),
        ("公交网络", "中关村大街 BRT 走廊 + 五道口微循环公交 + AI园区的士调度", "3条走廊"),
        ("慢行系统", "京张遗址公园慢行主轴 9km + 小月河滨水步道 6km + 城市绿道网络 15km", "全程无障碍"),
        ("骑行网络", "社区级自行车道 25km + 跨区骑行通勤绿道 12km + 共享单车电子围栏", "30+站点"),
        ("停车策略", "TOD 站点 P+R 换乘 + 共享停车泊位 + 新能源充电桩 20% 配比", "分区调控"),
        ("智慧交通", "AI信号灯优化 + 车路协同试点 + 自动驾驶接驳 + 实时出行数据平台", "1个平台"),
    ]
    for i, (mode, detail, kpi) in enumerate(mobility):
        y = 44 + i * 8
        pdf.set_fill_color(248, 250, 252) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.rect(15, y, 390, 7, "F")
        pdf.set_font("NotoSansSC", "B", 6)
        pdf.set_text_color(15, 23, 42)
        pdf.set_xy(18, y + 0.5)
        pdf.cell(40, 6, mode)
        pdf.set_font("NotoSansSC", "", 6)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(280, 6, detail)
        pdf.set_font("NotoSansSC", "B", 6)
        pdf.set_text_color(79, 70, 229)
        pdf.cell(50, 6, kpi, align="R")

    # Blue-green system
    pdf.set_xy(15, 100)
    pdf.set_font("NotoSansSC", "B", 11)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "蓝绿公共空间系统 Blue-Green & Public Space System", align="L")

    blue_green = [
        ("京张遗址公园活力带", "南北 9km 轴线, 串联三区两翼, 慢行+景观+文化+活动复合功能", "绿带主轴"),
        ("清河生态廊道", "北边界滨水绿带, 生态修复+防洪调蓄+休闲游憩, 与北翼众智园界面融合", "6km 滨水"),
        ("小月河生态廊道", "东翼场景赋能纽带, 具身智能测试+AI+医疗+AI+交通场景配套", "4km 生态"),
        ("社区公园网络", "5 分钟生活圈全覆盖, 口袋公园+社区花园+运动场地", "12 处节点"),
        ("公共空间体系", "创新交往广场+科技展示空间+文化广场+社区活动中心", "8 处核心"),
        ("雨洪管理", "海绵城市措施: 雨水花园+透水铺装+下凹绿地+蓄水池", "年径流控制 85%"),
    ]
    for i, (place, desc, role) in enumerate(blue_green):
        y = 109 + i * 8
        pdf.set_fill_color(248, 250, 252) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.rect(15, y, 390, 7, "F")
        pdf.set_font("NotoSansSC", "B", 6)
        pdf.set_text_color(15, 23, 42)
        pdf.set_xy(18, y + 0.5)
        pdf.cell(50, 6, place)
        pdf.set_font("NotoSansSC", "", 6)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(270, 6, desc)
        pdf.set_font("NotoSansSC", "B", 6)
        pdf.set_text_color(5, 150, 105)
        pdf.cell(50, 6, role, align="R")

    # Slow connectivity gap analysis
    pdf.set_xy(15, 165)
    pdf.set_font("NotoSansSC", "B", 11)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "慢行断点与连通分析 Slow Connectivity Gap Analysis", align="L")

    gaps = [
        ("北四环上跨节点", "京张遗址公园被北四环截断, 需上跨桥梁或下穿通道连接", "JZ-01 近期解决"),
        ("北五环穿越", "众智园与清河之间被北五环阻隔, 需立体过街设施", "中期解决"),
        ("13号线轨道分割", "五道口段轨道两侧连通不畅, 需站城一体化设计", "JZ-04 中期解决"),
        ("京张铁路南段", "大钟寺区域铁路两侧步行不便, 需增设地下通道", "长期治理"),
        ("小月河跨河节点", "东翼跨河通道不足, 需增设景观桥 3 座", "中期更新"),
    ]
    for i, (gap_name, detail, solution) in enumerate(gaps):
        y = 174 + i * 8
        pdf.set_fill_color(248, 250, 252) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.rect(15, y, 390, 7, "F")
        pdf.set_text_color(71, 85, 105)
        pdf.set_font("NotoSansSC", "B", 6)
        pdf.set_text_color(15, 23, 42)
        pdf.set_xy(18, y + 0.5)
        pdf.cell(50, 6, gap_name)
        pdf.set_font("NotoSansSC", "", 6)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(250, 6, detail)
        pdf.set_font("NotoSansSC", "B", 6)
        pdf.set_text_color(190, 18, 60)
        pdf.cell(70, 6, solution, align="R")

    # Spatial data dependency
    pdf.set_xy(15, 225)
    pdf.set_font("NotoSansSC", "B", 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "空间数据依赖 Spatial Data Dependencies", align="L")

    data_deps = [
        "geometry/roads.geojson → 交通网络分析 (数据来源: OSM, 非官方道路红线)",
        "geometry/green_space.geojson → 绿地率复算 (临时边界内 7%)",
        "geometry/public_space.geojson → 公共空间比例 (1.5%)",
        "geometry/buildings.geojson → 建筑基底面积 (792,717 sqm, 非官方建筑轮廓)",
        "geometry/constraints.geojson → 限制条件 (文保/河道/铁路)",
        "geometry/phasing.geojson → 分期实施范围 (概念建议级别)",
    ]
    for i, dep in enumerate(data_deps):
        y = 234 + i * 7
        pdf.set_text_color(71, 85, 105)
        pdf.set_font("NotoSansSC", "", 6)
        pdf.set_xy(18, y)
        pdf.cell(0, 5, f"• {dep}")

    add_footer(pdf, "所有空间数据来源于 agent_inferred_from_public_data, 非官方红线. 正式边界就绪后须复算.")


def a0_page3(pdf: FPDF, _metrics: dict[str, Any]):
    """技术指标 — metrics, benchmark, component library"""
    # Title
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, PAGE_W, 30, "F")
    pdf.set_text_color(248, 250, 252)
    pdf.set_font("NotoSansSC", "B", 18)
    pdf.set_xy(15, 6)
    pdf.cell(0, 12, "百年京张AI创新带 · 指标与实施", align="L")
    pdf.set_font("NotoSansSC", "", 8)
    pdf.set_xy(15, 18)
    pdf.cell(0, 7, "Metrics & Implementation Matrix | 核心指标复算 + 实施项目清单 + 运营框架", align="L")

    # Metrics detail table
    pdf.set_xy(15, 35)
    pdf.set_font("NotoSansSC", "B", 11)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "指标复算表 Metrics Recalculation", align="L")

    # Table header
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(15, 43, 390, 7, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("NotoSansSC", "B", 6)
    pdf.set_xy(17, 44)
    pdf.cell(60, 5, "指标")
    pdf.cell(60, 5, "当前值")
    pdf.cell(60, 5, "状态")
    pdf.cell(100, 5, "数据来源")
    pdf.cell(90, 5, "备注")

    metrics_rows = [
        ("site_area_sqm", "1,141.3 ha", "provisional", "geometry/site_boundary.geojson", "临时边界, 非官方红线"),
        ("building_footprint", "792,717 sqm", "provisional", "geometry/buildings.geojson", "非官方建筑轮廓, 仅示意"),
        ("green_ratio", "7.0%", "provisional", "geometry/green_space.geojson", "临时边界内; 正式边界预计 25-30%"),
        ("public_space_ratio", "1.5%", "provisional", "geometry/public_space.geojson", "临时边界内"),
        ("floor_area_ratio", "unknown", "unknown", "brief/site-package", "等待官方控规确认"),
        ("key_area_count", "3 处", "known", "geometry/key_areas.geojson", "众智园/原点/大钟寺"),
    ]
    for i, (metric, value, status, source, note) in enumerate(metrics_rows):
        y = 50 + i * 7
        bg = 248 if i % 2 == 0 else 255
        pdf.set_fill_color(bg, bg, bg)
        pdf.rect(15, y, 390, 7, "F")
        pdf.set_font("NotoSansSC", "B", 5.5)
        pdf.set_text_color(15, 23, 42)
        pdf.set_xy(17, y + 0.5)
        pdf.cell(60, 6, metric)
        pdf.set_font("NotoSansSC", "B", 6)
        pdf.set_text_color(79, 70, 229)
        pdf.cell(60, 6, value)
        pdf.set_font("NotoSansSC", "", 5.5)
        status_color = (5, 150, 105) if status == "known" else (217, 119, 6) if status == "provisional" else (100, 116, 139)
        pdf.set_text_color(*status_color)
        pdf.cell(60, 6, status)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(100, 6, source)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(90, 6, note)

    # Implementation matrix
    pdf.set_xy(15, 100)
    pdf.set_font("NotoSansSC", "B", 11)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "实施项目矩阵 Implementation Matrix", align="L")

    proj_header = ["编号", "项目", "类型", "阶段", "预算", "KPI"]
    proj_header_w = [16, 100, 70, 50, 50, 80]
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(15, 108, sum(proj_header_w), 7, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("NotoSansSC", "B", 5.5)
    x = 17
    for i, h in enumerate(proj_header):
        pdf.cell(proj_header_w[i], 6, h)
        x += proj_header_w[i]

    projects = [
        ("JZ-01", "慢行断点缝合", "公共空间/交通", "近期试点", "500-1000万", "慢行连通率≥90%"),
        ("JZ-02", "清河创新界面", "蓝绿空间/产业", "中期更新", "1000-3000万", "蓝绿空间开敞率≥60%"),
        ("JZ-03", "成果转化街", "城市更新/产业", "近期试点", "500-1500万/期", "年度转化项目≥20"),
        ("JZ-04", "四象限步行连通", "轨道一体化", "中期更新", "3000-8000万", "换乘效率提升≥30%"),
        ("JZ-05", "AI算力节点", "新基建/公共", "近期试点", "500-1500万/节点", "日服务≥500人次/节点"),
        ("JZ-06", "AI活动周路线", "运营/品牌", "长期治理", "300-800万/届", "参与≥5万/届"),
    ]
    for i, row in enumerate(projects):
        y = 115 + i * 7
        bg = 248 if i % 2 == 0 else 255
        pdf.set_fill_color(bg, bg, bg)
        pdf.rect(15, y, sum(proj_header_w), 7, "F")
        pdf.set_text_color(71, 85, 105)
        pdf.set_font("NotoSansSC", "", 5.5)
        x = 17
        for j, val in enumerate(row):
            pdf.set_xy(x, y + 0.5)
            if j == 0:
                pdf.set_font("NotoSansSC", "B", 5.5)
                pdf.set_text_color(15, 23, 42)
            elif j == 1:
                pdf.set_font("NotoSansSC", "B", 5.5)
                pdf.set_text_color(79, 70, 229)
            else:
                pdf.set_font("NotoSansSC", "", 5.5)
                pdf.set_text_color(71, 85, 105)
            pdf.cell(proj_header_w[j], 6, val)
            x += proj_header_w[j]

    # Operation framework
    pdf.set_xy(15, 165)
    pdf.set_font("NotoSansSC", "B", 11)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "运营可持续性框架 Operation Sustainability Framework", align="L")

    ops = [
        ("财务机制", "AI特别发展区增值费/TOD反哺/三级赞助/算力交叉补贴"),
        ("年度活动体系", "春季开发者节 → 夏季AI创新大赛 → 秋季国际论坛 → 冬季成果发布会"),
        ("转化漏斗", "参与人次 → 签约数 → 企业存活率 → 纳税额; 连续两年低于基准则触发预算削减"),
        ("维护责任", "纯公共品纳入市政维护预算; 有商业回报潜力的项目单独设计收入模型"),
        ("数据治理", "数据最小化 + 隐私保护 + 公平性审计 + 人工复核; 年度运营报告公开"),
        ("风险退出", "每个项目标明前置数据依赖、审批接口、风险条件和退出机制"),
    ]
    for i, (label, desc) in enumerate(ops):
        y = 174 + i * 8
        pdf.set_fill_color(248, 250, 252) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.rect(15, y, 390, 7, "F")
        pdf.set_font("NotoSansSC", "B", 6)
        pdf.set_text_color(15, 23, 42)
        pdf.set_xy(18, y + 0.5)
        pdf.cell(40, 6, label)
        pdf.set_font("NotoSansSC", "", 6)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(340, 6, desc)

    # Compliance note
    pdf.set_xy(15, 230)
    pdf.set_font("NotoSansSC", "B", 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "合规说明 Compliance Notes", align="L")

    compliance = [
        "所有项目和阶段均为概念建议, 须在正式控规、市政、交通和权属条件确认后逐项复核",
        "预算级别为概念建议, 不包含建成后的年度运营支出. 精确预测需在运营主体确定后编制",
        "缺少管线、能源、排水、防洪、消防等工程资料时, 应列为正式深化前置条件",
        "所有品牌、字体、图像、肖像和企业标识须有清权来源, 详见 sources.json 和 copyright_statement.md",
        "HTML 页面不得加载远程脚本、远程地图瓦片、远程字体、iframe、表单或外部 API",
    ]
    for i, item in enumerate(compliance):
        y = 238 + i * 7
        pdf.set_text_color(71, 85, 105)
        pdf.set_font("NotoSansSC", "", 6)
        pdf.set_xy(18, y)
        pdf.cell(0, 5, f"• {item}")

    add_footer(pdf, "提交者: ID-VerNe | Claude Code Opus 4.8 | 2026-08-09 | Provisional boundary — 所有面积指标以 metrics.json 为准")


# ── Main ──────────────────────────────────────────────────────────────

def generate_pdfs(pkg: Path):
    metrics = load_metrics(pkg)

    # A3 Booklet (3 pages)
    pdf = FPDF(orientation="L", unit="mm", format="A3")
    pdf.add_font("NotoSansSC", "", FONT_PATH)
    pdf.add_font("NotoSansSC", "B", FONT_PATH)
    pdf.set_auto_page_break(auto=False)

    pdf.add_page()
    add_header(pdf, "A3 文册 A3 Booklet", 1, 3)
    a3_page1(pdf, metrics)

    pdf.add_page()
    add_header(pdf, "A3 文册 A3 Booklet", 2, 3)
    a3_page2(pdf, metrics)

    pdf.add_page()
    add_header(pdf, "A3 文册 A3 Booklet", 3, 3)
    a3_page3(pdf, metrics)

    a3_path = pkg / "drawings" / "a3-booklet.pdf"
    a3_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(a3_path))
    a3_size = a3_path.stat().st_size
    print(f"WROTE drawings/a3-booklet.pdf ({a3_size} bytes, {len(pdf.pages)} pages)")

    # A0 Boards (3 pages)
    pdf = FPDF(orientation="L", unit="mm", format=(1189, 841))
    pdf.add_font("NotoSansSC", "", FONT_PATH)
    pdf.add_font("NotoSansSC", "B", FONT_PATH)
    pdf.set_auto_page_break(auto=False)

    pdf.add_page()
    add_header(pdf, "A0 展板 A0 Boards", 1, 3)
    a0_page1(pdf, metrics)

    pdf.add_page()
    add_header(pdf, "A0 展板 A0 Boards", 2, 3)
    a0_page2(pdf, metrics)

    pdf.add_page()
    add_header(pdf, "A0 展板 A0 Boards", 3, 3)
    a0_page3(pdf, metrics)

    a0_path = pkg / "drawings" / "a0-boards.pdf"
    pdf.output(str(a0_path))
    a0_size = a0_path.stat().st_size
    print(f"WROTE drawings/a0-boards.pdf ({a0_size} bytes, {len(pdf.pages)} pages)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        pkg = Path("submissions/ID-VerNe/ai-innovation-belt")
    else:
        pkg = Path(sys.argv[1])
    if not pkg.exists():
        raise SystemExit(f"submission directory not found: {pkg}")
    generate_pdfs(pkg)