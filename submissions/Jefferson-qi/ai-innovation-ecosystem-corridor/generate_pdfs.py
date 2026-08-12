"""
Generate A3 booklet and A0 boards PDF files using PIL.
A3: 297 x 420 mm at 150 DPI
A0: 841 x 1189 mm at 150 DPI
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Colors
TECH_BLUE = (59, 125, 216)
RAILWAY_ORANGE = (232, 146, 60)
ECO_GREEN = (91, 174, 111)
DARK = (26, 26, 46)
GRAY = (102, 102, 102)
LIGHT_GRAY = (245, 245, 245)
WHITE = (255, 255, 255)
BORDER = (224, 224, 224)

# Try to load a font
def get_font(size):
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",    # Microsoft YaHei
        "C:/Windows/Fonts/simhei.ttf",   # SimHei
        "C:/Windows/Fonts/arial.ttf",    # Arial
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except:
                pass
    return ImageFont.load_default()

def mm_to_px(mm, dpi=150):
    return int(mm * dpi / 25.4)

def draw_text_wrapped(draw, text, xy, font, fill, max_width, line_spacing=1.4):
    """Draw text with word wrapping for Chinese text."""
    x, y = xy
    lines = []
    current_line = ""
    for char in text:
        test_line = current_line + char
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] > max_width and current_line:
            lines.append(current_line)
            current_line = char
        else:
            current_line = test_line
    if current_line:
        lines.append(current_line)
    
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), line, font=font)
        y += int((bbox[3] - bbox[1]) * line_spacing) + 2
    return y

def create_a3_booklet(output_path, figures_dir):
    """Create A3 booklet with proposal summary."""
    w_px = mm_to_px(297)
    h_px = mm_to_px(420)
    
    pages = []
    
    # Page 1: Cover
    img = Image.new('RGB', (w_px, h_px), WHITE)
    draw = ImageDraw.Draw(img)
    
    # Background gradient effect
    for i in range(h_px // 3):
        r = int(26 + (15 - 26) * i / (h_px // 3))
        g = int(26 + (33 - 26) * i / (h_px // 3))
        b = int(46 + (60 - 46) * i / (h_px // 3))
        draw.line([(0, i), (w_px, i)], fill=(r, g, b))
    
    # Title
    font_title = get_font(48)
    font_sub = get_font(28)
    font_small = get_font(16)
    
    title_y = h_px // 3
    draw.text((w_px//2 - 300, title_y), "AI创新生态廊", font=font_title, fill=WHITE)
    draw.text((w_px//2 - 280, title_y + 70), "百年京张的智能新生", font=font_sub, fill=(200, 200, 220))
    draw.text((w_px//2 - 340, title_y + 120), "AI Innovation Ecosystem Corridor", font=font_small, fill=(150, 150, 180))
    
    # Meta
    meta_y = title_y + 200
    meta_items = ["提交者: Jefferson-qi", "智能体: WorkBuddy", "版本: v1.0", "日期: 2026-08-11", "许可: COMMUNITY-DISPLAY-ONLY"]
    for i, item in enumerate(meta_items):
        draw.text((w_px//2 - 150, meta_y + i * 30), item, font=font_small, fill=(180, 180, 200))
    
    # Footer
    draw.text((w_px//2 - 200, h_px - 60), "本方案由AI智能体生成，所有内容均为概念建议", font=font_small, fill=(120, 120, 140))
    
    pages.append(img)
    
    # Page 2-6: Content pages with figures
    figure_info = [
        ("site-overview.png", "图1：资料证据链与提交包关系图", "设计依据与资料清单", "本方案以《百年京张AI创新带城市设计国际方案征集资格预审公告》为主控依据，使用仓库提供的临时粗略边界进行空间生成。所有空间落地建议均为概念建议，不替代正式规划。"),
        ("land-use-structure.png", "图2：三层范围与空间工作框架图", "三层范围工作框架", "统筹研究范围43.6km²、总体设计范围11.4km²、重点区域范围3.684km²。三个空间层级严格对应公告规定。空间结构：一廊三区两翼多节点。"),
        ("key-areas.png", "图3：三处重点区域索引与设计任务图", "重点区域详细设计", "众智园AI加速区（研发核心+加速环+测试场）、AI原点社区（社区中心+生活街坊+交往节点）、大钟寺AI产业区（产业办公+商业服务+文化展示）。"),
        ("mobility-bluegreen.png", "图4：交通慢行与蓝绿公共空间复合系统图", "交通市政与蓝绿空间", "轨道优先、慢行成网、智能赋能。京张遗址公园为绿色主轴，小月河滨水绿带为次轴，形成廊-带-园三级蓝绿网络。4个AI朝圣地标。"),
        ("metrics-evidence.png", "图5：核心指标复算与证据链图", "指标体系与合规矩阵", "12个AI场景节点、5类用户画像、4个测试场景、4个AI地标、6个全球案例、10个用地分区、15组建筑足迹、14个更新项目。合规矩阵覆盖全部六项智能体任务。"),
    ]
    
    font_h = get_font(32)
    font_body = get_font(18)
    font_cap = get_font(14)
    
    for fig_name, caption, section_title, description in figure_info:
        img = Image.new('RGB', (w_px, h_px), WHITE)
        draw = ImageDraw.Draw(img)
        
        # Header bar
        draw.rectangle([(0, 0), (w_px, 60)], fill=TECH_BLUE)
        draw.text((40, 15), "AI创新生态廊 · A3图册", font=get_font(20), fill=WHITE)
        draw.text((w_px - 200, 15), section_title, font=get_font(18), fill=WHITE)
        
        # Section title
        draw.text((40, 80), section_title, font=font_h, fill=DARK)
        draw.line([(40, 125), (w_px - 40, 125)], fill=BORDER, width=2)
        
        # Description
        y = draw_text_wrapped(draw, description, (40, 140), font_body, GRAY, w_px - 80)
        
        # Figure
        fig_path = os.path.join(figures_dir, fig_name)
        if os.path.exists(fig_path):
            fig_img = Image.open(fig_path)
            max_fig_w = w_px - 80
            max_fig_h = h_px - y - 80
            ratio = min(max_fig_w / fig_img.width, max_fig_h / fig_img.height)
            new_size = (int(fig_img.width * ratio), int(fig_img.height * ratio))
            fig_img = fig_img.resize(new_size, Image.LANCZOS)
            fig_x = (w_px - new_size[0]) // 2
            img.paste(fig_img, (fig_x, y + 10))
            draw.text((w_px//2 - 150, y + new_size[1] + 25), caption, font=font_cap, fill=GRAY)
        
        # Footer
        draw.line([(40, h_px - 40), (w_px - 40, h_px - 40)], fill=BORDER, width=1)
        draw.text((40, h_px - 30), "Jefferson-qi | WorkBuddy AI Agent | v1.0 | COMMUNITY-DISPLAY-ONLY", font=get_font(12), fill=GRAY)
        
        pages.append(img)
    
    # Page 7: Scenarios summary
    img = Image.new('RGB', (w_px, h_px), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (w_px, 60)], fill=TECH_BLUE)
    draw.text((40, 15), "AI创新生态廊 · A3图册", font=get_font(20), fill=WHITE)
    draw.text((40, 80), "AI场景卡与朝圣地标", font=font_h, fill=DARK)
    draw.line([(40, 125), (w_px - 40, 125)], fill=BORDER, width=2)
    
    scenarios = [
        "01 AI+自动驾驶接驳    02 机器人配送网络    03 AI+医疗社区诊站",
        "04 AI+教育个性化      05 AI导览文化叙事    06 AI+公共安全感知",
        "07 AI+企业服务大厅    08 智能原生消费      09 AI+交通信号优化",
        "10 AI+能源管理        11 AI+环境监测       12 开源贡献者荣誉墙",
    ]
    y = 145
    for s in scenarios:
        draw.text((40, y), s, font=font_body, fill=DARK)
        y += 35
    
    y += 20
    draw.text((40, y), "AI朝圣地标：", font=font_h, fill=RAILWAY_ORANGE)
    y += 45
    landmarks = [
        "1. 智能体贡献荣誉墙 — 全球第一个为AI智能体设立的城市荣誉纪念碑",
        "2. 京张AI里程碑 — 1909-2026百年创新时间轴，AI交互装置",
        "3. 开源成果展示廊 — 开放式展览，每季度轮换",
        "4. 未来生活体验街 — AI原生生活方式现场体验",
    ]
    for l in landmarks:
        draw.text((40, y), l, font=font_body, fill=DARK)
        y += 30
    
    y += 20
    draw.text((40, y), "用户画像：", font=font_h, fill=ECO_GREEN)
    y += 45
    personas = [
        "1. AI研究员'李智' — 28岁，大模型训练，15分钟步行生活圈",
        "2. 创业者'王创' — 35岁，AI创业CEO，全链条支撑",
        "3. 居民'张阿姨' — 62岁，退休教师，AI提升生活",
        "4. 国际访客'Dr. Smith' — 45岁，硅谷学者，英文导览",
        "5. 开发者'陈代码' — 26岁，开源贡献者，归属感",
    ]
    for p in personas:
        draw.text((40, y), p, font=font_body, fill=DARK)
        y += 30
    
    draw.line([(40, h_px - 40), (w_px - 40, h_px - 40)], fill=BORDER, width=1)
    draw.text((40, h_px - 30), "Jefferson-qi | WorkBuddy AI Agent | v1.0 | COMMUNITY-DISPLAY-ONLY", font=get_font(12), fill=GRAY)
    
    pages.append(img)
    
    # Save as PDF
    pages[0].save(output_path, save_all=True, append_images=pages[1:], resolution=150.0)
    print(f"A3 booklet saved: {output_path} ({len(pages)} pages)")

def create_a0_boards(output_path, figures_dir):
    """Create A0 boards with key figures."""
    w_px = mm_to_px(841)
    h_px = mm_to_px(1189)
    
    pages = []
    
    font_title = get_font(72)
    font_h = get_font(48)
    font_body = get_font(28)
    font_cap = get_font(22)
    font_small = get_font(18)
    
    # Board 1: Overview
    img = Image.new('RGB', (w_px, h_px), WHITE)
    draw = ImageDraw.Draw(img)
    
    # Top banner
    draw.rectangle([(0, 0), (w_px, 100)], fill=DARK)
    draw.text((50, 25), "AI创新生态廊 · 百年京张的智能新生", font=font_title, fill=WHITE)
    
    # Three scope boxes
    box_w = (w_px - 150) // 3
    scopes = [("43.6", "km²", "统筹研究范围"), ("11.4", "km²", "总体设计范围"), ("3.684", "km²", "重点区域范围")]
    for i, (val, unit, label) in enumerate(scopes):
        bx = 50 + i * (box_w + 25)
        draw.rectangle([(bx, 130), (bx + box_w, 230)], fill=LIGHT_GRAY, outline=BORDER, width=2)
        draw.text((bx + box_w//2 - 60, 145), val, font=font_title, fill=TECH_BLUE)
        draw.text((bx + box_w//2 - 30, 195), unit, font=font_body, fill=GRAY)
        draw.text((bx + box_w//2 - 80, 225), label, font=font_body, fill=DARK)
    
    # Main figure - site overview
    fig_path = os.path.join(figures_dir, "site-overview.png")
    if os.path.exists(fig_path):
        fig_img = Image.open(fig_path)
        max_w = w_px - 100
        max_h = 400
        ratio = min(max_w / fig_img.width, max_h / fig_img.height)
        new_size = (int(fig_img.width * ratio), int(fig_img.height * ratio))
        fig_img = fig_img.resize(new_size, Image.LANCZOS)
        img.paste(fig_img, ((w_px - new_size[0])//2, 280))
        draw.text((w_px//2 - 200, 280 + new_size[1] + 10), "图1：资料证据链与提交包关系图", font=font_cap, fill=GRAY)
    
    # Structure description
    y = 720
    draw.text((50, y), "空间结构：一廊三区两翼多节点", font=font_h, fill=TECH_BLUE)
    y += 60
    structure_text = [
        "一廊：京张智脉走廊，全长约9公里，AI创新生态的物理主轴",
        "三区：众智园AI加速区（研发）→ AI原点社区（生活）→ 大钟寺AI产业区（转化）",
        "两翼：中关村科技服务翼（资本+IP）+ 小月河场景赋能翼（试验+活力）",
        "多节点：AI开发者广场、开源展示廊、荣誉墙、文化体验广场、测试广场、未来生活街",
    ]
    for line in structure_text:
        draw.text((50, y), line, font=font_body, fill=DARK)
        y += 40
    
    # Footer
    draw.rectangle([(0, h_px - 60), (w_px, h_px)], fill=DARK)
    draw.text((50, h_px - 45), "Board 1/2 — 总体概览 | Jefferson-qi | WorkBuddy AI Agent | v1.0 | COMMUNITY-DISPLAY-ONLY", font=font_small, fill=WHITE)
    
    pages.append(img)
    
    # Board 2: Key Areas + Metrics
    img = Image.new('RGB', (w_px, h_px), WHITE)
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([(0, 0), (w_px, 100)], fill=DARK)
    draw.text((50, 25), "AI创新生态廊 · 重点区域与指标体系", font=font_title, fill=WHITE)
    
    # Key areas figure
    fig_path = os.path.join(figures_dir, "key-areas.png")
    if os.path.exists(fig_path):
        fig_img = Image.open(fig_path)
        max_w = (w_px - 150) // 2
        max_h = 350
        ratio = min(max_w / fig_img.width, max_h / fig_img.height)
        new_size = (int(fig_img.width * ratio), int(fig_img.height * ratio))
        fig_img = fig_img.resize(new_size, Image.LANCZOS)
        img.paste(fig_img, (50, 130))
        draw.text((50, 130 + new_size[1] + 10), "图3：重点区域索引", font=font_cap, fill=GRAY)
    
    # Mobility figure
    fig_path = os.path.join(figures_dir, "mobility-bluegreen.png")
    if os.path.exists(fig_path):
        fig_img = Image.open(fig_path)
        max_w = (w_px - 150) // 2
        max_h = 350
        ratio = min(max_w / fig_img.width, max_h / fig_img.height)
        new_size = (int(fig_img.width * ratio), int(fig_img.height * ratio))
        fig_img = fig_img.resize(new_size, Image.LANCZOS)
        img.paste(fig_img, (w_px // 2 + 25, 130))
        draw.text((w_px//2 + 25, 130 + new_size[1] + 10), "图4：交通蓝绿系统", font=font_cap, fill=GRAY)
    
    # Metrics table
    y = 530
    draw.text((50, y), "核心指标体系", font=font_h, fill=TECH_BLUE)
    y += 55
    
    metrics = [
        ("AI场景节点", "12个", "design_concept"),
        ("用户画像", "5类", "design_concept"),
        ("测试验证场景", "4个", "design_concept"),
        ("AI朝圣地标", "4个", "design_concept"),
        ("全球生态案例", "6个", "background"),
        ("用地分区", "10个", "provisional"),
        ("建筑足迹", "15组", "design_concept"),
        ("更新项目", "14项", "design_concept"),
    ]
    
    col_w = (w_px - 100) // 4
    for i, (name, val, status) in enumerate(metrics):
        col = i % 4
        row = i // 4
        bx = 50 + col * col_w
        by = y + row * 80
        draw.rectangle([(bx, by), (bx + col_w - 15, by + 70)], fill=LIGHT_GRAY, outline=BORDER, width=1)
        draw.text((bx + 15, by + 10), name, font=font_small, fill=GRAY)
        draw.text((bx + 15, by + 35), val, font=font_h, fill=TECH_BLUE)
    
    # Metrics evidence figure
    y = y + 2 * 80 + 20
    fig_path = os.path.join(figures_dir, "metrics-evidence.png")
    if os.path.exists(fig_path):
        fig_img = Image.open(fig_path)
        max_w = w_px - 100
        max_h = h_px - y - 100
        ratio = min(max_w / fig_img.width, max_h / fig_img.height)
        new_size = (int(fig_img.width * ratio), int(fig_img.height * ratio))
        fig_img = fig_img.resize(new_size, Image.LANCZOS)
        img.paste(fig_img, ((w_px - new_size[0])//2, y))
    
    # Footer
    draw.rectangle([(0, h_px - 60), (w_px, h_px)], fill=DARK)
    draw.text((50, h_px - 45), "Board 2/2 — 重点区域与指标 | Jefferson-qi | WorkBuddy AI Agent | v1.0 | COMMUNITY-DISPLAY-ONLY", font=font_small, fill=WHITE)
    
    pages.append(img)
    
    # Save as PDF
    pages[0].save(output_path, save_all=True, append_images=pages[1:], resolution=150.0)
    print(f"A0 boards saved: {output_path} ({len(pages)} pages)")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    figures_dir = os.path.join(base_dir, "assets", "figures")
    drawings_dir = os.path.join(base_dir, "drawings")
    os.makedirs(drawings_dir, exist_ok=True)
    
    create_a3_booklet(os.path.join(drawings_dir, "a3-booklet.pdf"), figures_dir)
    create_a0_boards(os.path.join(drawings_dir, "a0-boards.pdf"), figures_dir)
    print("All PDFs generated successfully!")
