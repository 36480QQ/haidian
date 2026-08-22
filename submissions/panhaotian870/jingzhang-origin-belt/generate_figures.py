from PIL import Image, ImageDraw, ImageFont
import os

BASE = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 900
BG = (10, 22, 40)
TEAL = (0, 212, 170)
BLUE = (27, 58, 92)
WHITE = (229, 231, 235)
GRAY = (107, 114, 128)
GOLD = (255, 215, 0)
GREEN = (34, 197, 94)
CYAN = (6, 182, 212)
AMBER = (245, 158, 11)

try:
    font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 24)
    font_sm = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 16)
    font_xs = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 12)
    font_lg = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 32)
except:
    font = ImageFont.load_default()
    font_sm = font
    font_xs = font
    font_lg = font

def rounded_rect(d, xy, r, fill, outline=None):
    x0, y0, x1, y1 = xy
    d.rectangle([x0+r, y0, x1-r, y1], fill=fill)
    d.rectangle([x0, y0+r, x1, y1-r], fill=fill)
    d.pieslice([x0, y0, x0+2*r, y0+2*r], 180, 270, fill=fill)
    d.pieslice([x1-2*r, y0, x1, y0+2*r], 270, 360, fill=fill)
    d.pieslice([x0, y1-2*r, x0+2*r, y1], 90, 180, fill=fill)
    d.pieslice([x1-2*r, y1-2*r, x1, y1], 0, 90, fill=fill)
    if outline:
        d.arc([x0, y0, x0+2*r, y0+2*r], 180, 270, fill=outline, width=2)
        d.arc([x1-2*r, y0, x1, y0+2*r], 270, 360, fill=outline, width=2)
        d.arc([x0, y1-2*r, x0+2*r, y1], 90, 180, fill=outline, width=2)
        d.arc([x1-2*r, y1-2*r, x1, y1], 0, 90, fill=outline, width=2)
        d.line([x0+r, y0, x1-r, y0], fill=outline, width=2)
        d.line([x0+r, y1, x1-r, y1], fill=outline, width=2)
        d.line([x0, y0+r, x0, y1-r], fill=outline, width=2)
        d.line([x1, y0+r, x1, y1-r], fill=outline, width=2)

# === Figure 1: Site Overview ===
img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)
d.text((W//2, 30), '京张·智廊 | 场地总览 Site Overview', fill=TEAL, font=font, anchor='mt')
d.text((W//2, 65), '统筹研究范围 ~43.6km² · 总体设计范围 ~11.4km²', fill=GRAY, font=font_sm, anchor='mt')
rounded_rect(d, (100, 90, 1100, 820), 16, (15, 25, 45), outline=(55, 65, 85))
rounded_rect(d, (180, 120, 1020, 780), 10, (0, 30, 25), outline=TEAL)
d.rectangle([580, 120, 620, 780], fill=(0, 40, 35))
d.line([600, 120, 600, 780], fill=TEAL, width=4)
d.text((600, 800), '京张铁路遗址公园 ~9km', fill=TEAL, font=font_sm, anchor='mt')
rounded_rect(d, (260, 150, 560, 280), 8, BLUE, outline=TEAL)
d.text((410, 195), '众智园AI自主创新加速区', fill=WHITE, font=font_sm, anchor='mm')
d.text((410, 225), '智·创（研发）| 192.1 ha', fill=TEAL, font=font_xs, anchor='mm')
d.text((410, 250), 'AI全栈创新 · AI治理 · 国际人才', fill=GRAY, font=font_xs, anchor='mm')
rounded_rect(d, (260, 370, 560, 500), 8, BLUE, outline=TEAL)
d.text((410, 415), '北京AI原点社区', fill=WHITE, font=font_sm, anchor='mm')
d.text((410, 445), '智·居（生活）| 104.3 ha', fill=TEAL, font=font_xs, anchor='mm')
d.text((410, 470), 'AI人才社区 · 生活服务 · 社区智能化', fill=GRAY, font=font_xs, anchor='mm')
rounded_rect(d, (260, 580, 560, 700), 8, BLUE, outline=TEAL)
d.text((410, 625), '大钟寺AI产业集聚区', fill=WHITE, font=font_sm, anchor='mm')
d.text((410, 655), '智·享（产业）| 72.0 ha', fill=TEAL, font=font_xs, anchor='mm')
d.text((410, 680), '智能原生 · 企业总部 · 体验', fill=GRAY, font=font_xs, anchor='mm')
rounded_rect(d, (120, 340, 220, 520), 6, (31, 41, 55), outline=GRAY)
d.text((170, 420), '中关村\n科技服务翼', fill=GRAY, font=font_xs, anchor='mm')
rounded_rect(d, (640, 340, 740, 520), 6, (31, 41, 55), outline=GRAY)
d.text((690, 420), '小月河\n场景赋能翼', fill=GRAY, font=font_xs, anchor='mm')
for cx, cy, name in [(410, 415, '智·塔'), (410, 625, '智·门'), (410, 195, '智·碑')]:
    d.ellipse([cx-10, cy-10, cx+10, cy+10], fill=GOLD)
d.text((W//2, 855), '临时边界数据，不等同于官方红线 | 所有空间建议为概念建议', fill=GRAY, font=font_xs, anchor='mt')
img.save(os.path.join(BASE, 'assets/figures/site-overview.png'), quality=95)
print('1/5 site-overview.png')

# === Figure 2: Land Use ===
img2 = Image.new('RGB', (W, H), BG)
d2 = ImageDraw.Draw(img2)
d2.text((W//2, 30), '京张·智廊 | 用地结构 Land Use Structure', fill=TEAL, font=font, anchor='mt')
d2.text((W//2, 65), '概念建议 · 待正式控规确定', fill=GRAY, font=font_sm, anchor='mt')
import math
cx, cy, r = 350, 480, 200
data = [('科研与产业用地', 35, BLUE), ('公共管理与服务', 15, TEAL), ('商业服务业', 12, CYAN),
        ('居住用地', 18, AMBER), ('绿地与广场', 12, GREEN), ('道路交通', 8, GRAY)]
start = 0
for name, pct, color in data:
    angle = pct / 100 * 360
    d2.pieslice([cx-r, cy-r, cx+r, cy+r], start, start+angle, fill=color)
    start += angle
d2.ellipse([cx-120, cy-120, cx+120, cy+120], fill=BG)
d2.text((cx, cy-15), '11.4 km²', fill=WHITE, font=font, anchor='mm')
d2.text((cx, cy+15), '总体设计范围', fill=GRAY, font=font_xs, anchor='mm')
ly = 200
for name, pct, color in data:
    d2.rectangle([600, ly, 620, ly+16], fill=color)
    d2.text((630, ly+8), name, fill=WHITE, font=font_sm, anchor='lm')
    d2.text((870, ly+8), f'{pct}%', fill=TEAL, font=font_sm, anchor='lm')
    ly += 40
d2.text((W//2, 855), '概念建议比例，不构成法定控规指标 | 来源: 用地分类指南 (2023)', fill=GRAY, font=font_xs, anchor='mt')
img2.save(os.path.join(BASE, 'assets/figures/land-use-structure.png'), quality=95)
print('2/5 land-use-structure.png')

# === Figure 3: Key Areas ===
img3 = Image.new('RGB', (W, H), BG)
d3 = ImageDraw.Draw(img3)
d3.text((W//2, 30), '京张·智廊 | 重点区域 Key Areas', fill=TEAL, font=font, anchor='mt')
areas = [('众智园', '智·创（研发）', '192.1 ha', ['AI自主创新加速区', '全栈研发集群', '国际AI人才社区', '智·碑纪念碑']),
         ('AI原点社区', '智·居（生活）', '104.3 ha', ['AI原点社区', '15分钟AI生活圈', '智·塔地标(100m)', '知春路枢纽']),
         ('大钟寺', '智·享（产业）', '72.0 ha', ['智·大模型广场', 'AI企业总部集群', '智·门门户地标', '城市智能体中心'])]
for i, (name, brand, area, features) in enumerate(areas):
    x = 60 + i * 380
    rounded_rect(d3, (x, 80, x+350, 620), 12, (17, 24, 39), outline=TEAL)
    rounded_rect(d3, (x, 80, x+350, 135), 12, BLUE)
    d3.rectangle([x, 115, x+350, 135], fill=BLUE)
    d3.text((x+175, 105), name, fill=WHITE, font=font_sm, anchor='mm')
    d3.text((x+175, 165), f'{brand} | {area}', fill=TEAL, font=font_xs, anchor='mm')
    rounded_rect(d3, (x+20, 190, x+330, 350), 6, (10, 22, 40), outline=(31, 41, 55))
    d3.text((x+175, 260), '概念空间布局', fill=GRAY, font=font_xs, anchor='mm')
    d3.text((x+175, 280), '待专业团队深化', fill=GRAY, font=font_xs, anchor='mm')
    for j, feat in enumerate(features):
        d3.text((x+30, 370+j*25), f'• {feat}', fill=WHITE, font=font_xs, anchor='lm')
rounded_rect(d3, (60, 650, 1140, 760), 12, (17, 24, 39), outline=(31, 41, 55))
d3.text((W//2, 670), '三区协同：基础研究 → 交叉创新 → 产业转化 → 场景体验', fill=TEAL, font=font_sm, anchor='mt')
d3.text((W//2, 700), '京张铁路遗址公园 9km 创新主轴贯穿三区', fill=WHITE, font=font_xs, anchor='mm')
d3.text((W//2, 725), '中关村科技服务翼提供资本与IP支撑 · 小月河场景赋能翼提供场景试验场', fill=GRAY, font=font_xs, anchor='mm')
d3.text((W//2, 855), '所有空间布局为概念建议 | 数据来源: 公告推算(临时)', fill=GRAY, font=font_xs, anchor='mt')
img3.save(os.path.join(BASE, 'assets/figures/key-areas.png'), quality=95)
print('3/5 key-areas.png')

# === Figure 4: Mobility & Blue-Green ===
img4 = Image.new('RGB', (W, H), BG)
d4 = ImageDraw.Draw(img4)
d4.text((W//2, 30), '京张·智廊 | 蓝绿公共空间与交通', fill=TEAL, font=font, anchor='mt')
d4.rectangle([570, 80, 630, 780], fill=(0, 40, 35))
d4.line([600, 80, 600, 780], fill=GREEN, width=4)
d4.text((600, 800), '京张铁路遗址公园 9km', fill=GREEN, font=font_sm, anchor='mt')
for y in [200, 320, 440, 560]:
    d4.line([200, y, 1000, y], fill=CYAN, width=2)
    d4.text((1010, y), '缝合通道', fill=CYAN, font=font_xs, anchor='lm')
d4.line([680, 80, 680, 780], fill=AMBER, width=2)
d4.text((692, 400), '创新大道', fill=AMBER, font=font_xs, anchor='lm')
for y, name, brand in [(140, '众智园', '智·创 192ha'), (340, 'AI原点社区', '智·居 104ha'), (560, '大钟寺', '智·享 72ha')]:
    rounded_rect(d4, (240, y, 520, y+80), 6, BLUE, outline=TEAL)
    d4.text((380, y+28), name, fill=WHITE, font=font_sm, anchor='mm')
    d4.text((380, y+55), brand, fill=TEAL, font=font_xs, anchor='mm')
for y in [180, 380, 600]:
    d4.ellipse([585, y-12, 615, y+12], fill=(0, 50, 40), outline=GREEN)
# Legend
d4.rectangle((40, 830, 1160, 870), fill=(17, 24, 39), outline=(31, 41, 55))
d4.text((W//2, 850), '遗址公园绿廊 + 6条东西缝合通道 + 创新大道 + 智轨(概念)', fill=GRAY, font=font_xs, anchor='mm')
img4.save(os.path.join(BASE, 'assets/figures/mobility-bluegreen.png'), quality=95)
print('4/5 mobility-bluegreen.png')

# === Figure 5: Metrics & Evidence ===
img5 = Image.new('RGB', (W, H), BG)
d5 = ImageDraw.Draw(img5)
d5.text((W//2, 30), '京张·智廊 | 指标与证据 Metrics & Evidence', fill=TEAL, font=font, anchor='mt')
d5.text((W//2, 75), '任务覆盖 Task Coverage', fill=WHITE, font=font_sm, anchor='mt')
tasks = [('agent.1 总体概念', 100, '命名体系+视觉'), ('agent.2 创新生态', 100, '8个全球案例'),
         ('agent.3 场景赋能', 100, '10场景+3测试'), ('agent.4 公共空间', 100, '3地标+荣誉体系'),
         ('agent.5 文化叙事', 100, '三重叙事'), ('agent.6 长期运营', 100, '5活动+社区')]
for i, (name, pct, detail) in enumerate(tasks):
    y = 105 + i * 28
    d5.text((60, y+5), name, fill=WHITE, font=font_xs, anchor='lm')
    d5.rectangle([240, y, 850, y+16], fill=(31, 41, 55))
    d5.rectangle([240, y, 240+int(610*pct/100), y+16], fill=TEAL)
    d5.text((870, y+5), f'✓ {detail}', fill=TEAL, font=font_xs, anchor='lm')
d5.text((W//2, 300), '核心指标', fill=WHITE, font=font_sm, anchor='mt')
metrics = [('43.6', 'km² 统筹', '临时'), ('11.4', 'km² 设计', '临时'), ('368.4', 'ha 重点', '临时'),
           ('9', 'km 公园', '概念'), ('10', '场景卡', '完成'), ('8', '案例', '完成')]
for i, (val, label, status) in enumerate(metrics):
    x = 60 + i * 190
    rounded_rect(d5, (x, 330, x+170, 430), 8, BLUE)
    d5.text((x+85, 360), val, fill=TEAL, font=font_lg, anchor='mm')
    d5.text((x+85, 395), label, fill=GRAY, font=font_xs, anchor='mm')
    sc = GOLD if status == '临时' else GREEN
    d5.text((x+85, 415), status, fill=sc, font=font_xs, anchor='mm')
d5.text((W//2, 470), '数据来源', fill=WHITE, font=font_sm, anchor='mt')
for i, src in enumerate(['公告 (2026-05-09)', '任务书 (2026-05-18)', '城市设计管理办法', '用地分类指南 (2023)', '临时边界数据 (provisional)']):
    d5.text((80, 500+i*22), f'• {src}', fill=GRAY, font=font_xs, anchor='lm')
d5.text((W//2, 855), '临时数据待正式复核 | 远期指标非政府承诺 | 概念建议不替代正式规划', fill=GOLD, font=font_xs, anchor='mt')
img5.save(os.path.join(BASE, 'assets/figures/metrics-evidence.png'), quality=95)
print('5/5 metrics-evidence.png')
print('All figures generated!')
