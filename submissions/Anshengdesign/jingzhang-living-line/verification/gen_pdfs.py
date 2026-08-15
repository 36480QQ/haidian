# -*- coding: utf-8 -*-
"""A3 文册 + A0 展板 PDF 生成（中英双语，离线本地资源，CJK 字体嵌入）
matplotlib PdfPages；内容 = 图件 + 指标 + 文本板（数据全部来自 design_metrics / 计算 JSON）
"""
import os, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = "/Users/mac/Downloads/同步空间/2026/百年京张AI创新带城市设计开源征集/haidian/submissions/Anshengdesign/jingzhang-living-line/assets/figures"
DRAW = "/Users/mac/Downloads/同步空间/2026/百年京张AI创新带城市设计开源征集/haidian/submissions/Anshengdesign/jingzhang-living-line/drawings"
os.makedirs(DRAW, exist_ok=True)

from kun_common import setup_chinese_fonts
setup_chinese_fonts()

dmet = json.load(open(os.path.join(HERE, "design_geometry", "design_metrics.json")))

def text_page(pp, title, body_lines, LANG="zh"):
    fig = plt.figure(figsize=(16.5, 11.7))  # A3 landscape
    fig.text(0.06, 0.93, title, fontsize=20, fontweight="bold", color="#1f4e2d")
    fig.text(0.06, 0.90, "THE EMERGENT BELT · 京张 Hyper Line" if LANG=="zh" else "THE EMERGENT BELT · JINGZHANG HYPER LINE",
             fontsize=11, color="#5c6b76")
    y = 0.82
    for line in body_lines:
        fig.text(0.06, y, line, fontsize=11.5, va="top", wrap=True)
        y -= 0.055
    fig.text(0.06, 0.03, ("KUN-SAL 坤空间量化实验室 · 概念建议（provisional 边界仅临时使用；非官方红线、非审定结论）"
                          if LANG=="zh" else
                          "KUN-SAL Spatial Quant Lab · conceptual proposal (provisional boundary, not an official redline or approval)"),
             fontsize=9, color="#a93226")
    pp.savefig(fig); plt.close(fig)

def img_page(pp, img_path, caption, LANG="zh"):
    from PIL import Image
    im = Image.open(img_path)
    w, h = im.size
    fig = plt.figure(figsize=(16.5, 11.7))
    ax = fig.add_axes([0.06, 0.12, 0.88, 0.76])
    ax.imshow(im); ax.axis("off")
    fig.text(0.06, 0.06, caption, fontsize=11, color="#2c3e50")
    pp.savefig(fig); plt.close(fig)

def build(LANG):
    zh = LANG == "zh"
    T = lambda z, e: z if zh else e
    fn = lambda n: os.path.join(FIG, f"{n}.png" if zh else f"{n}.en.png")
    out = os.path.join(DRAW, "a3-booklet.pdf" if zh else "a3-booklet.en.pdf")
    with PdfPages(out) as pp:
        text_page(pp, T("百年京张AI创新带城市设计 · 方案文册（A3）", "Centennial Jing-Zhang AI Belt · Design Booklet (A3)"), [
            T("方案名：涌现之带 THE EMERGENT BELT —— 京张 Hyper Line", "Title: THE EMERGENT BELT — Jing-Zhang Hyper Line"),
            T("投稿方：KUN-SAL 坤空间量化实验室（GitHub: Anshengdesign，署名：邢新华）", "Author: KUN-SAL Spatial Quant Lab (GitHub: Anshengdesign, Xing Xinhua)"),
            T("方法论：CASA 复杂性城市科学（Wilson λ / 渗流 / 标度律 / 分形 / 空间句法 / 反事实）× 高德POI 25,476点 + OSM 现状", "Method: CASA complexity urban science × Amap POI 25,476 pts + OSM"),
            T("数据纪律：全部数字本地实算（EPSG:4548），单源登记 metrics_registry.json；未实算方法不冒称", "Discipline: all numbers computed locally (EPSG:4548), single-source registry"),
            T("口径声明：临时粗略边界仅用于生成/展示/自检；控规类指标待官方数据补齐；空间建议均为概念建议", "Caveat: provisional boundary for generation/display/self-check only; regulatory indicators pending; conceptual recommendations"),
        ], LANG)
        img_page(pp, fn("site-overview"), T("图1 · 一带总览：一线三折两翼七节点", "Fig.1 · Belt overview"), LANG)
        img_page(pp, fn("land-use-structure"), T("图2 · 用地结构与POI动力分区", "Fig.2 · Land use & POI zoning"), LANG)
        img_page(pp, fn("key-areas"), T("图3 · 三处重点区定位（临时粗略范围为虚线）", "Fig.3 · Key-area positions (dashed = provisional)"), LANG)
        img_page(pp, fn("mobility-bluegreen"), T("图4 · 七节点缝合与蓝绿系统", "Fig.4 · Seven-node stitching & blue-green"), LANG)
        img_page(pp, fn("metrics-evidence"), T("图5 · 核心指标与证据链", "Fig.5 · Core metrics & evidence"), LANG)
        img_page(pp, fn("ecosystem-map"), T("图6 · AI创新生态图谱：上游齐备、中间层未度量", "Fig.6 · Ecosystem map"), LANG)
        img_page(pp, fn("transmission-map"), T("图7 · 亚线性→超线性传导图谱（五桥+平权回环）", "Fig.7 · Transmission map (five bridges + equity loop)"), LANG)
        img_page(pp, fn("c8-c9-c10"), T("图8 · 标度律偏离/就业平衡/H健康因子（临界值体系）", "Fig.8 · Deviation / employment balance / health factor"), LANG)
        text_page(pp, T("设计任务响应要点", "Design task responses"), [
            T("· agent.1 命名/Logo：涌现之带 THE EMERGENT BELT；主线京张 Hyper Line；三段 HYPER STACK/ORIGIN/FRONT；Logo=超线性之线（铁路直线上翘+七点渗流簇）", "· agent.1 Naming/logo: THE EMERGENT BELT; HYPER STACK/ORIGIN/FRONT; logo = the superlinear line"),
            T("· agent.2 生态案例（7个）：伦敦国王十字/波士顿肯德尔/斯坦福研究园/深圳粤海/东京涩谷/剑桥集群/特拉维夫罗斯柴尔德大道", "· agent.2 Ecosystem cases (7): King's Cross / Kendall Sq / Stanford / Yuehai / Shibuya / Cambridge / Rothschild"),
            T("· agent.3 场景卡10张（含4个产业测试验证）+ 画像5类（OPC创业者/科学家工程师/青年学子/长者/朝圣者）", "· agent.3 10 scenario cards (4 industrial tests) + 5 personas"),
            T("· agent.4 三朝圣地标：清华园车站·原点（名墙）/ 五道口·相变广场（λ仪表）/ 大钟寺·界面广场（涌现之钟）", "· agent.4 Three pilgrimage landmarks: Origin / Phase Plaza / Interface Plaza"),
            T("· agent.5 文化叙事：1909人字形自主筑路 → 2026超线性AI集聚（约束下的涌现百年叙事）", "· agent.5 Narrative: 1909 Y-switch self-built railway → 2026 superlinear AI agglomeration"),
            T("· agent.6 运营：开发者节/相变论坛（λ年度发布）/开放测试季/OPC接单大赛/荣誉墙铭刻（均为概念建议）", "· agent.6 Operations: dev festival / phase forum / open test seasons / honor wall (conceptual)"),
        ], LANG)
        text_page(pp, T("量化诊断与设计靶点", "Quantified diagnosis & design targets"), [
            T("· Wilson λ：三区两翼5核超临界分量 2/5（断裂）；众智园×大钟寺 λ=0.015 深度亚临界", "· Wilson λ: core 2/5 connected; Zhongzhiyuan×Dazhongsi λ=0.015 deeply subcritical"),
            T("· 主脊断点 7 处（清华东路/五道口/北四环/知春路/北三环/学院南路/高梁桥斜街）→ 缝合=相变", "· 7 spine gaps → stitching = phase transition"),
            T("· 空间句法：缝合后北京北+132%、大钟寺+102%、五道口+65%", "· Space syntax: +132% Beijing North, +102% Dazhongsi, +65% Wudaokou"),
            T("· 分形维 D=1.746（健康区间1.6–1.8）；交叉口密度132.9/km²；POI 25,476点", "· Fractal D=1.746 (healthy 1.6–1.8); intersections 132.9/km²; POI 25,476"),
            T("· 职住失衡：居住仅16.5% → 站域补人才公寓（概念）", "· Jobs-housing gap: residential 16.5% → talent apartments (concept)"),
            T("· POI 缺口：众智园补文旅/教育/金融；原点社区补医疗；大钟寺补科研/教育", "· POI gaps: Zhongzhiyuan tourism/edu/finance; Origin medical; Dazhongsi research/edu"),
        ], LANG)
        text_page(pp, T("分期与风险（概念口径）", "Phasing & risk (conceptual)"), [
            T("· 近期(1–3年)：主脊七节点缝合 + 大钟寺界面；中期(3–5年)：原点社区更新；远期(5–10年)：众智园花园街区", "· Near (1–3y): spine stitching + Dazhongsi; mid (3–5y): Origin; long (5–10y): Zhongzhiyuan"),
            T("· 待正式数据：官方红线/控规/文保/现状建筑与权属/市政管线 → 补齐后整包重算", "· Pending: official redlines/regulatory/heritage/inventory/pipelines → full recalculation"),
            T("· 版权：图件几何KUN-SAL本地生成；命名Logo需商标字体清权；无个人隐私与未授权素材", "· Rights: locally generated; naming needs trademark/font clearance; no PII or unauthorized assets"),
            T("· 边界条款：不替代正式规划、不构成政府审定结论、不写已确定政府安排", "· Boundary: does not replace formal planning; no confirmed government arrangements"),
        ], LANG)
    # ---- A0 boards ----
    out0 = os.path.join(DRAW, "a0-boards.pdf" if zh else "a0-boards.en.pdf")
    with PdfPages(out0) as pp:
        for img, cap in [
            ("site-overview", T("A0板1 · 总体设计结构板：一线三折两翼七节点", "Board 1 · Overall structure")),
            ("land-use-structure", T("A0板2 · 用地与城市更新板（POI自下而上分区+职住靶点）", "Board 2 · Land use & renewal")),
            ("mobility-bluegreen", T("A0板3 · 交通、蓝绿与公共空间板（七节点缝合+渗流）", "Board 3 · Mobility & blue-green")),
            ("metrics-evidence", T("A0板4 · 指标复核与合规响应板（证据链）", "Board 4 · Metrics & compliance")),
        ]:
            from PIL import Image
            im = Image.open(fn(img))
            w, h = im.size
            fig = plt.figure(figsize=(33.1, 46.8))  # A0 portrait
            ax = fig.add_axes([0.04, 0.06, 0.92, 0.84])
            ax.imshow(im); ax.axis("off")
            fig.text(0.04, 0.925, cap, fontsize=26, fontweight="bold", color="#1f4e2d")
            fig.text(0.04, 0.02, T("KUN-SAL 坤空间量化实验室 · 涌现之带 THE EMERGENT BELT（概念建议，临时边界仅虚线表达）",
                                   "KUN-SAL Spatial Quant Lab · THE EMERGENT BELT (conceptual; provisional boundary dashed only)"),
                     fontsize=12, color="#a93226")
            pp.savefig(fig); plt.close(fig)
    print("PDFs done:", os.path.basename(out), os.path.basename(out0))

for L in ["zh", "en"]:
    build(L)
