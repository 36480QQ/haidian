"""Generate all 5 proposal figures using HTML+CSS + Playwright screenshots.

Redesigned with:
- Rich graphical layouts (not just text cards)
- Proper bullet/list formatting (no negative-margin headers)
- Full canvas utilization (1600x1200)
- Distinct visual identity per figure
"""
import os, sys, json
from playwright.sync_api import sync_playwright

SUBMISSION = os.path.join(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(SUBMISSION, 'assets', 'figures')
os.makedirs(ASSETS, exist_ok=True)

W, H = 1600, 1200

# ── Base CSS ──────────────────────────────────────────────
CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
body{
  width:1600px;height:1200px;overflow:hidden;
  font-family:"Microsoft YaHei","PingFang SC",-apple-system,sans-serif;
  background:#f8fafc;color:#1e293b;font-size:14px;line-height:1.55;
}
.title-bar{
  background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);
  padding:22px 32px 18px;border-bottom:4px solid #c79838;
}
.title-bar h1{font-size:24px;color:#c79838;font-weight:700;letter-spacing:0.03em}
.title-bar .sub{font-size:12px;color:#94a3b8;margin-top:6px}
.footer-bar{
  background:#0f172a;padding:10px 32px;color:#64748b;font-size:10px;
  position:absolute;bottom:0;left:0;right:0;display:flex;justify-content:space-between;
}
.content{padding:24px 32px;position:relative;height:1070px}

/* ── Common atoms ── */
h3{font-size:15px;margin-bottom:10px;color:#334155;display:flex;align-items:center;gap:8px}
h3::before{content:'';display:inline-block;width:4px;height:18px;border-radius:2px;background:var(--hdr,#4f46e5)}

.row{display:flex;gap:18px;margin-bottom:18px}
.col{flex:1;display:flex;flex-direction:column;gap:12px}
.col-15{flex:1.5}
.col-2{flex:2}
.col-3{flex:3}

/* ── Cards ── */
.card{
  background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:16px;
  box-shadow:0 1px 3px rgba(0,0,0,.04);
}
.card-top{border-top:3px solid var(--accent,#4f46e5)}
.card .card-label{font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px}
.card .card-number{font-size:36px;font-weight:800;color:var(--accent,#4f46e5);line-height:1}
.card .card-desc{font-size:12px;color:#64748b;margin-top:4px;line-height:1.5}

/* ── Metric mini-cards ── */
.mgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.mcard{
  background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:14px 16px;
  border-top:3px solid var(--clr,#4f46e5);box-shadow:0 1px 3px rgba(0,0,0,.04);
}
.mcard .mlabel{font-size:11px;color:#64748b;margin-bottom:4px}
.mcard .mvalue{font-size:28px;font-weight:800;color:#0f172a;line-height:1.1}
.mcard .msrc{font-size:10px;color:#94a3b8;margin-top:4px}

/* ── Bar chart ── */
.bar-row{display:flex;align-items:center;gap:10px;margin-bottom:8px}
.bar-label{width:100px;text-align:right;font-size:11px;color:#475569;flex-shrink:0}
.bar-track{flex:1;height:26px;background:#f1f5f9;border-radius:4px;overflow:hidden}
.bar-fill{height:100%;border-radius:4px;display:flex;align-items:center;padding-left:10px;font-size:11px;color:#fff;font-weight:600}

/* ── Evidence row ── */
.ev-block{display:flex;align-items:flex-start;gap:12px;padding:12px 16px;
  background:#fff;border:1px solid #e2e8f0;border-left:4px solid var(--clr,#4f46e5);
  border-radius:0 6px 6px 0;margin-bottom:8px;box-shadow:0 1px 2px rgba(0,0,0,.03);
}
.ev-block .ev-icon{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:16px}
.ev-block .ev-name{font-family:Consolas,monospace;font-size:12px;font-weight:700;min-width:170px;flex-shrink:0}
.ev-block .ev-desc{font-size:12px;color:#475569;line-height:1.5}

/* ── Flow diagram ── */
.flow{display:flex;align-items:center;justify-content:center;gap:0}
.flow-step{flex:1;text-align:center;padding:14px 8px;background:#fff;border:2px solid #e2e8f0;border-radius:8px;font-size:12px;font-weight:600;position:relative}
.flow-step.active{background:#eef2ff;border-color:#4f46e5;color:#4f46e5}
.flow-step.dark{background:#0f172a;color:#fff;border-color:#c79838}
.flow-arrow{font-size:22px;color:#94a3b8;flex-shrink:0;padding:0 4px;font-weight:300}

/* ── Key area cards (vertical) ── */
.ka-col{flex:1;display:flex;flex-direction:column;gap:10px}
.ka-card{border-radius:10px;overflow:hidden;border:1px solid #e2e8f0;display:flex;flex-direction:column;flex:1;box-shadow:0 2px 8px rgba(0,0,0,.05)}
.ka-head{color:#fff;padding:14px 16px;font-weight:700;font-size:15px;display:flex;align-items:center;gap:10px}
.ka-head .ka-num{width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.25);display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:800}
.ka-body{background:#fff;padding:14px 16px;flex:1}
.ka-body .ka-type{font-size:12px;font-weight:600;margin-bottom:10px}
.ka-body ul{list-style:none;padding:0}
.ka-body ul li{font-size:12px;color:#475569;padding:5px 0 5px 22px;position:relative;line-height:1.4;border-bottom:1px solid #f1f5f9}
.ka-body ul li::before{content:'';position:absolute;left:0;top:11px;width:10px;height:10px;border-radius:2px;background:var(--dot,#4f46e5)}
.ka-foot{padding:10px 16px;font-size:10px;color:#64748b;background:#f8fafc;border-top:1px solid #f1f5f9}

/* ── Tags / Pills ── */
.tag-row{display:flex;flex-wrap:wrap;gap:6px}
.pill{
  display:inline-flex;align-items:center;gap:4px;padding:5px 12px;border-radius:999px;
  font-size:11px;font-weight:600;border:1px solid #e2e8f0;background:#fff;color:#475569;
}
.pill.done{background:#f0fdf4;border-color:#86efac;color:#15803d}
.pill.warn{background:#fffbeb;border-color:#fcd34d;color:#b45309}

/* ── Number block ── */
.num-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.num-block{
  text-align:center;padding:18px 12px;background:#fff;border:1px solid #e2e8f0;
  border-radius:8px;border-top:3px solid var(--clr,#4f46e5);
}
.num-block .nb-num{font-size:32px;font-weight:800;color:var(--clr,#4f46e5);line-height:1}
.num-block .nb-label{font-size:11px;color:#64748b;margin-top:6px}
.num-block .nb-sub{font-size:10px;color:#94a3b8;margin-top:3px}

/* ── Badge ── */
.badge-ring{
  display:flex;align-items:center;justify-content:center;
  width:120px;height:120px;border-radius:50%;margin:0 auto;
  border:5px solid #15803d;background:#f0fdf4;font-size:16px;font-weight:800;
  color:#15803d;text-align:center;line-height:1.3;white-space:pre-line;
}
"""

# ── Helper functions to avoid nested f-string issues ──────

def _proc_row(n, t, d):
    return '<div class="card" style="display:flex;align-items:center;gap:12px;padding:12px 16px"><span style="font-size:20px;width:32px;text-align:center">%s</span><div><div style="font-weight:700;font-size:13px">%s</div><div style="font-size:11px;color:#64748b">%s</div></div></div>' % (n, t, d)

def make_process_rows(lang, L):
    items = [
        ('①', L('结构化提取', 'Structured Extraction'), L('公告→任务→条件→指标 逐层解析', 'Announcement→tasks→conditions→metrics')),
        ('②', L('矩阵编制', 'Matrix Compilation'), L('合规/标准/深度/自检 4矩阵全覆盖', 'Compliance/Standard/Depth/Self-Check 4-matrix')),
        ('③', L('空间落图', 'Spatial Mapping'), L('8层GeoJSON 临时边界+EPSG:4548', '8-layer GeoJSON provisional+EPSG:4548')),
        ('④', L('双语编制', 'Bilingual Production'), L('中英文proposal+visual+figures+矩阵', 'zh+en proposal/visual/figures/matrices')),
        ('⑤', L('自检验证', 'Self-Check Validation'), L('确定性/空间/视觉/证据 4项全部PASS', 'Deterministic/Spatial/Visual/Evidence 4 PASS')),
    ]
    return ''.join(_proc_row(n, t, d) for n, t, d in items)

def make_gap_rows(lang, L):
    items = [
        ('G1', L('北五环跨线节点', 'N5th Ring Crossing'), L('景观桥方案', 'Landscape bridge')),
        ('G2', L('清华东路西口', 'Tsinghua E Rd West'), L('地下通道方案', 'Underpass')),
        ('G3', L('知春路-大钟寺段', 'Zhichun-Dazhongsi'), L('共享街道方案', 'Shared street')),
        ('G4', L('四道口路', 'Sidaokou Rd'), L('交通稳静化', 'Traffic calming')),
        ('G5', L('西直门外大街端头', 'Xizhimen Terminal'), L('立体接驳', 'Multi-level connection')),
    ]
    tmpl = '<div style="display:flex;align-items:flex-start;gap:8px;padding:6px 0;border-bottom:1px solid #f1f5f9;font-size:12px"><span style="flex-shrink:0;width:22px;height:22px;border-radius:50%%;background:#fef2f2;color:#b42318;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700">%s</span><span><b>%s</b> — %s</span></div>'
    return ''.join(tmpl % (n, t, d) for n, t, d in items)

def make_tod_rows(lang, L):
    items = [
        (L('五道口(13号线)', 'Wudaokou (L13)'), '#4f46e5', L('创新社区TOD', 'Innovation Community TOD')),
        (L('清华东路西口(13/15号线)', 'Tsinghua E Rd (L13/15)'), '#15803d', L('学术交流TOD', 'Academic Exchange TOD')),
        (L('大钟寺(13号线)', 'Dazhongsi (L13)'), '#b7791f', L('四象限连通 · 智能经济TOD', '4-Quadrant · Intelligent Economy TOD')),
    ]
    tmpl = '<div style="display:flex;align-items:flex-start;gap:8px;padding:6px 0;border-bottom:1px solid #f1f5f9;font-size:12px"><span style="flex-shrink:0;display:inline-block;width:8px;height:8px;border-radius:50%%;background:%s;margin-top:4px"></span><span><b>%s</b> — %s</span></div>'
    return ''.join(tmpl % (c, n, d) for n, c, d in items)

def make_psn_rows(lang, L):
    items = [
        ('L1', '#15803d', L('城市级', 'City-Level'), L('京张遗址公园 · 众智创新公园 · 大钟寺站前广场', 'Heritage Park · Innovation Park · Dazhongsi Station Plaza')),
        ('L2', '#4f46e5', L('片区级', 'District-Level'), L('三处重点区内部广场与开放空间', 'Key-area internal plazas & open spaces')),
        ('L3', '#0f7490', L('社区级', 'Community-Level'), L('嵌入式公共空间与AI服务节点 ≤800m半径', 'Embedded public spaces & AI service nodes ≤800m')),
        ('L4', '#b7791f', L('建筑界面级', 'Building-Interface'), L('首层开放 · 骑楼 · 空中花园 · AI交互界面', 'Open ground floors · Arcades · Sky gardens · AI interfaces')),
    ]
    tmpl = '<div style="display:flex;align-items:flex-start;gap:10px;padding:8px 0;border-bottom:1px solid #f1f5f9;font-size:12px"><span style="flex-shrink:0;background:%s;color:#fff;width:24px;height:24px;border-radius:50%%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700">%s</span><div><b>%s</b><div style="color:#64748b;margin-top:2px">%s</div></div></div>'
    return ''.join(tmpl % (c, n, t, d) for n, c, t, d in items)


# ── Main HTML builders ────────────────────────────────────

def make_html(lang, figure_id):
    L = lambda zh, en: zh if lang == 'zh' else en

    head = '<!DOCTYPE html><html lang="%s"><head><meta charset="utf-8"><style>%s</style></head><body>' % (lang, CSS)

    if figure_id == 'site-overview':
        body = """
<div class="title-bar">
  <h1>%s</h1>
  <div class="sub">%s</div>
</div>
<div class="content">

  <!-- 四段式流程 -->
  <div class="flow" style="margin-bottom:22px">
    <div class="flow-step active">%s<br><span style="font-size:10px;font-weight:400;color:#64748b">%s</span></div>
    <div class="flow-arrow">→</div>
    <div class="flow-step active">%s<br><span style="font-size:10px;font-weight:400;color:#64748b">%s</span></div>
    <div class="flow-arrow">→</div>
    <div class="flow-step active">%s<br><span style="font-size:10px;font-weight:400;color:#64748b">%s</span></div>
    <div class="flow-arrow">→</div>
    <div class="flow-step dark">%s<br><span style="font-size:10px;font-weight:400;color:#94a3b8">%s</span></div>
  </div>

  <!-- 三列：来源 / 处理 / 产出 -->
  <div class="row" style="margin-bottom:20px">
    <div class="col">
      <h3 style="--hdr:#4f46e5">%s</h3>
      <div class="card card-top" style="--accent:#4f46e5">
        <div class="card-label">OFFICIAL-ANNOUNCEMENT</div>
        <div style="font-size:13px;font-weight:600">%s</div>
        <div class="card-desc">%s</div>
      </div>
      <div class="card card-top" style="--accent:#15803d">
        <div class="card-label">AGENT-TASKBOOK</div>
        <div style="font-size:13px;font-weight:600">%s</div>
        <div class="card-desc">%s</div>
      </div>
      <div class="card card-top" style="--accent:#b7791f">
        <div class="card-label">SITE-PACKAGE</div>
        <div style="font-size:13px;font-weight:600">%s</div>
        <div class="card-desc">%s</div>
      </div>
      <div class="card card-top" style="--accent:#b42318">
        <div class="card-label">GLOBAL-CASES</div>
        <div style="font-size:13px;font-weight:600">%s</div>
        <div class="card-desc">%s</div>
      </div>
    </div>
    <div class="col">
      <h3 style="--hdr:#0f172a">%s</h3>
      <div style="display:flex;flex-direction:column;gap:8px">
        %s
      </div>
    </div>
    <div class="col">
      <h3 style="--hdr:#c79838">%s</h3>
      <div class="card card-top" style="--accent:#4f46e5;margin-bottom:8px">
        <div style="font-size:13px;font-weight:600">\U0001f4dd proposal.md / proposal.en.md</div>
        <div class="card-desc">%s</div>
      </div>
      <div class="card card-top" style="--accent:#15803d;margin-bottom:8px">
        <div style="font-size:13px;font-weight:600">\U0001f4ca %s</div>
        <div class="card-desc">compliance / standard / design_depth / self_check</div>
      </div>
      <div class="card card-top" style="--accent:#b7791f;margin-bottom:8px">
        <div style="font-size:13px;font-weight:600">\U0001f5fa GeoJSON ×8</div>
        <div class="card-desc">%s</div>
      </div>
      <div class="card card-top" style="--accent:#b42318;margin-bottom:8px">
        <div style="font-size:13px;font-weight:600">\U0001f3a8 visual HTML ×2 + %s ×10</div>
        <div class="card-desc">%s</div>
      </div>
    </div>
  </div>

  <!-- 证据闭环 -->
  <h3 style="--hdr:#15803d">%s</h3>
  <div class="row">
    <div class="col-3">
      <div class="ev-block" style="--clr:#4f46e5"><div class="ev-icon" style="background:#eef2ff;color:#4f46e5">S</div><span class="ev-name">sources.json</span><span class="ev-desc">%s</span></div>
      <div class="ev-block" style="--clr:#15803d"><div class="ev-icon" style="background:#f0fdf4;color:#15803d">M</div><span class="ev-name">metrics.json</span><span class="ev-desc">%s</span></div>
      <div class="ev-block" style="--clr:#b7791f"><div class="ev-icon" style="background:#fffbeb;color:#b7791f">C</div><span class="ev-name">compliance_matrix</span><span class="ev-desc">%s</span></div>
      <div class="ev-block" style="--clr:#b42318"><div class="ev-icon" style="background:#fef2f2;color:#b42318">A</div><span class="ev-name">assumptions.json</span><span class="ev-desc">%s</span></div>
    </div>
    <div class="col" style="align-items:center;justify-content:center">
      <div class="badge-ring">%s</div>
      <div style="margin-top:12px;font-size:12px;color:#64748b;text-align:center">
        %s
      </div>
    </div>
  </div>
</div>
<div class="footer-bar">
  <span>AI Artery · Beijing — AI-Native Urban Co-Evolution Lab</span>
  <span>Provisional Geometry · Intake Only</span>
</div>""" % (
            # title
            L('资料证据链与提交包关系', 'Evidence Chain & Submission Package'),
            L('从官方公告到可查证结构化证据 — 全流程可追溯 · AI Artery·Beijing', 'Official Announcement → Verifiable Structured Evidence — Full Traceability'),
            # flow
            L('\U0001f4cb 资料收集', '1. Sources'), L('5项官方+开源', '5 official + open'),
            L('⚙ 结构化处理', '2. Processing'), L('提取·矩阵·落图', 'Extract·Matrix·Map'),
            L('\U0001f4e6 提交产出', '3. Deliverables'), L('md+json+geojson+html+png', 'md+json+geojson+html+png'),
            L('✅ 自检验证', '4. Self-Check'), L('4/4 PASS', '4/4 PASS'),
            # sources col
            L('数据来源 Sources', 'Data Sources'),
            L('官方资格预审公告', 'Pre-qualification Announcement'),
            L('任务定义、评分标准、提交规范', 'Task definition, scoring, submission spec'),
            L('Agent开放征集任务书', 'Agent Open-Call Taskbook'),
            L('6项Agent任务 + 10张场景卡', '6 agent tasks + 10 scenario cards'),
            L('场地数据包', 'Site Data Package'),
            L('临时边界、路网、建筑、绿地、水系', 'Provisional boundary, roads, buildings, green, water'),
            L('全球AI生态案例 ×8', '8 Global AI Ecosystem Cases'),
            L('硅谷→东京→新加坡→柏林 对标', 'Silicon Valley → Tokyo → Singapore → Berlin'),
            # processing col
            L('处理流程 Processing', 'Processing Pipeline'),
            make_process_rows(lang, L),
            # deliverables col
            L('提交产出 Deliverables', 'Deliverables'),
            L('4章双语完整提案', '4-chapter bilingual proposal'),
            L('矩阵 ×4', '4× Matrices'),
            L('land_use/buildings/roads/water/green/...', 'land_use / buildings / roads / water / green / ...'),
            L('配图', 'figures'),
            L('中英文可视化+5×2高清配图', 'zh/en visual + 5×2 high-res PNG figures'),
            # evidence loop
            L('结构化证据闭环', 'Structured Evidence Loop'),
            L('资料登记与使用许可 · 5项可用+1项暂不可用 · 每个来源标注使用边界', 'Source registry & licenses · 5 usable + 1 provisional · boundary notes per source'),
            L('从GeoJSON可复算的空间指标 · 设计面积/容积率/绿地率 · 替换官方边界后自动刷新', 'GeoJSON-reproducible spatial metrics · Site area/FAR/green ratio · Auto-refresh with official boundary'),
            L('23项公告任务 + agent.1-6全映射 · 每项有证据路径 · missing标记数据缺口', '23 announcement tasks + agent.1-6 mapping · Evidence path per item · missing=gaps flagged'),
            L('5项假设 · 每项注明状态+影响 · pending_professional_confirmation不阻断评分', '5 assumptions · status+impact per item · pending_confirmation does NOT block scoring'),
            # badge
            L('自检\n4/4\nPASS', 'SELF-CHECK\n4/4\nPASS'),
            L('确定性验证 ✅ · 空间审查 ✅\n视觉包装 ✅ · 专业证据 ✅', 'Deterministic ✅ · Spatial ✅\nVisual ✅ · Evidence ✅'),
        )

    elif figure_id == 'land-use-structure':
        body = """
<div class="title-bar">
  <h1>%s</h1>
  <div class="sub">%s</div>
</div>
<div class="content">

  <!-- 三层指标卡片 -->
  <div class="num-grid" style="margin-bottom:20px">
    <div class="num-block" style="--clr:#4f46e5">
      <div class="nb-num">43.6<span style="font-size:14px">km²</span></div>
      <div class="nb-label">%s</div>
      <div class="nb-sub">%s</div>
    </div>
    <div class="num-block" style="--clr:#15803d">
      <div class="nb-num">11.4<span style="font-size:14px">km²</span></div>
      <div class="nb-label">%s</div>
      <div class="nb-sub">%s</div>
    </div>
    <div class="num-block" style="--clr:#b7791f">
      <div class="nb-num">368<span style="font-size:14px">ha</span></div>
      <div class="nb-label">%s</div>
      <div class="nb-sub">%s</div>
    </div>
    <div class="num-block" style="--clr:#0f7490">
      <div class="nb-num">~8<span style="font-size:14px">km</span></div>
      <div class="nb-label">%s</div>
      <div class="nb-sub">%s</div>
    </div>
  </div>

  <div class="row">
    <!-- 左: 用地结构图 + 空间结构 -->
    <div class="col-15">
      <h3 style="--hdr:#4f46e5">%s</h3>
      <div class="card" style="padding:20px">
        <div class="bar-row"><span class="bar-label">%s</span><div class="bar-track"><div class="bar-fill" style="width:62%%;background:linear-gradient(90deg,#4f46e5,#6366f1)">25%% (285 ha)</div></div></div>
        <div class="bar-row"><span class="bar-label">%s</span><div class="bar-track"><div class="bar-fill" style="width:65%%;background:#b42318">26%% (296 ha)</div></div></div>
        <div class="bar-row"><span class="bar-label">%s</span><div class="bar-track"><div class="bar-fill" style="width:45%%;background:#475569">18%% (205 ha)</div></div></div>
        <div class="bar-row"><span class="bar-label">%s</span><div class="bar-track"><div class="bar-fill" style="width:33%%;background:#b7791f">13%% (148 ha)</div></div></div>
        <div class="bar-row"><span class="bar-label">%s</span><div class="bar-track"><div class="bar-fill" style="width:25%%;background:linear-gradient(90deg,#15803d,#22c55e)">10%% (114 ha)</div></div></div>
        <div class="bar-row"><span class="bar-label">%s</span><div class="bar-track"><div class="bar-fill" style="width:20%%;background:#0f7490">8%% (91 ha)</div></div></div>
      </div>

      <h3 style="--hdr:#c79838;margin-top:6px">%s</h3>
      <div class="card" style="padding:16px">
        <div style="display:flex;flex-wrap:wrap;gap:10px">
          <span class="pill" style="background:#eef2ff;border-color:#c7d2fe;color:#4f46e5;font-weight:700">%s</span>
          <span style="font-size:12px;color:#475569;padding-top:5px">%s</span>
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:8px">
          <span class="pill" style="background:#f0fdf4;border-color:#bbf7d0;color:#15803d;font-weight:700">%s</span>
          <span style="font-size:12px;color:#475569;padding-top:5px">%s</span>
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:8px">
          <span class="pill" style="background:#fffbeb;border-color:#fde68a;color:#b45309;font-weight:700">%s</span>
          <span style="font-size:12px;color:#475569;padding-top:5px">%s</span>
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:8px">
          <span class="pill" style="background:#f0fdf4;border-color:#bbf7d0;color:#15803d;font-weight:700">%s</span>
          <span style="font-size:12px;color:#475569;padding-top:5px">%s</span>
        </div>
      </div>
    </div>

    <!-- 右: 设计问题→回答 -->
    <div class="col">
      <h3 style="--hdr:#15803d">%s</h3>

      <div class="card" style="border-left:4px solid #4f46e5;margin-bottom:10px">
        <div style="font-size:11px;color:#4f46e5;font-weight:700;margin-bottom:4px">%s</div>
        <div style="font-size:13px;color:#64748b;margin-bottom:6px">%s</div>
        <div style="font-size:13px;font-weight:700;color:#0f172a">→ %s</div>
        <div style="font-size:11px;color:#94a3b8;margin-top:4px">%s</div>
      </div>

      <div class="card" style="border-left:4px solid #15803d;margin-bottom:10px">
        <div style="font-size:11px;color:#15803d;font-weight:700;margin-bottom:4px">%s</div>
        <div style="font-size:13px;color:#64748b;margin-bottom:6px">%s</div>
        <div style="font-size:13px;font-weight:700;color:#0f172a">→ %s</div>
        <div style="font-size:11px;color:#94a3b8;margin-top:4px">%s</div>
      </div>

      <div class="card" style="border-left:4px solid #b7791f;margin-bottom:10px">
        <div style="font-size:11px;color:#b7791f;font-weight:700;margin-bottom:4px">%s</div>
        <div style="font-size:13px;color:#64748b;margin-bottom:6px">%s</div>
        <div style="font-size:13px;font-weight:700;color:#0f172a">→ %s</div>
        <div style="font-size:11px;color:#94a3b8;margin-top:4px">%s</div>
      </div>

      <div class="card" style="border-left:4px solid #0f7490">
        <div style="font-size:11px;color:#0f7490;font-weight:700;margin-bottom:4px">%s</div>
        <div style="font-size:13px;color:#64748b;margin-bottom:6px">%s</div>
        <div style="font-size:13px;font-weight:700;color:#0f172a">→ %s</div>
        <div style="font-size:11px;color:#94a3b8;margin-top:4px">%s</div>
      </div>
    </div>
  </div>
</div>
<div class="footer-bar">
  <span>AI Artery · Beijing — Provisional Geometry</span>
  <span>%s</span>
</div>""" % (
            # title
            L('三层范围与空间结构', 'Three-Level Scope & Spatial Structure'),
            L('统筹研究(43.6km²)→总体设计(11.4km²)→重点区域(368ha) · 一脊三核多廊复合环', 'Research(43.6km²)→Design(11.4km²)→Key(368ha) · 1-Spine 3-Core Multi-Corridor Ring'),
            # num blocks
            L('统筹研究范围', 'Coordinated Research'), L('AI产业生态 · 三区两翼', 'AI ecosystem · 3-zone 2-wing'),
            L('总体设计范围', 'Overall Design Area'), L('更新·用地·交通·市政', 'Renewal·Land·Transport·Utility'),
            L('重点区域合计', 'Key Areas Total'), L('3处重点片区详细设计', '3 detailed design areas'),
            L('京张遗址公园脊骨', 'Heritage Park Spine'), L('北五环→西直门 南北贯通', 'N5th→Xizhimen N-S through'),
            # land use
            L('总体设计范围 用地结构', 'Overall Design Area — Land Use'),
            L('科研/创新产业', 'R&D / Innovation'),
            L('居住用地', 'Residential'),
            L('道路/交通设施', 'Roads / Transport'),
            L('商业/商务', 'Commercial'),
            L('绿地/广场', 'Green / Squares'),
            L('公服设施', 'Public Services'),
            # spatial structure
            L('空间结构', 'Spatial Structure'),
            L('一脊', '1 Spine'), L('京张遗址公园公共空间脊骨', 'Jing-Zhang Heritage Park public space spine'),
            L('三核', '3 Cores'), L('众智园 · AI原点社区 · 大钟寺 三处创新锚点', 'Zhongzhiyuan · AI Origin · Dazhongsi innovation anchors'),
            L('多廊', 'Multi-Corridor'), L('北四环/知春路/学院路 三条创新横轴', 'N4th Ring / Zhichun / Xueyuan 3 innovation axes'),
            L('复合环', 'Composite Ring'), L('清河-小月河-公园绿道 蓝绿生态环', 'Qinghe-Xiaoyuehe-Park greenway blue-green loop'),
            # Q&A
            L('设计问题 → 方案回答', 'Design Questions → Answers'),
            L('统筹研究', 'COORDINATED RESEARCH'),
            L('AI产业生态如何组织？未来城市形态概念？', 'How to organize AI ecosystem? Future form?'),
            L('五环创新链 × 三区两翼 空间协同', '5-Ring Innovation Chain × 3-Zone 2-Wing'),
            L('8个全球案例对标 · 差异化定位 · AI原生三层架构', '8 global cases · Differentiated positioning · AI-Native 3-layer'),
            L('总体设计', 'OVERALL DESIGN'),
            L('空间结构如何落图？用地如何分区？', 'Spatial structure on map? Land-use zoning?'),
            L('一脊三核多廊复合环 · 4类创新用地融合', '1-Spine 3-Core Multi-Corridor · 4 Innovation Land Types'),
            L('AI研发·蓝绿公园·产业服务·生活配套 无缝拼接', 'AI R&D · Blue-Green · Industry Services · Living — seamless'),
            L('重点区域', 'KEY AREAS'),
            L('三处重点区如何差异化？详细设计深度？', 'How to differentiate 3 key areas? Design depth?'),
            L('各有定位+空间动作+AI场景+实施依赖', 'Positioning+Actions+Scenarios+Dependencies each'),
            L('众智园(192ha)·原点(104ha)·大钟寺(72ha)', 'Zhongzhiyuan(192ha)·Origin(104ha)·Dazhongsi(72ha)'),
            L('更新项目清单', 'PROJECT PIPELINE'),
            L('如何从设计走向实施？谁负责？', 'From design to implementation? Who is responsible?'),
            L('7个项目 · 3期推进 · 多元资金模型', '7 projects · 3 phases · Blended funding model'),
            L('每项有责任主体+关键审批+可衡量成果指标', 'Each: responsible actor+approval+measurable outcome indicator'),
            # footer
            L('所有指标基于临时边界复算 替换官方多边形后更新', 'All metrics provisional; recalibrate with official boundary'),
        )

    elif figure_id == 'key-areas':
        areas_zh = [
            {'name': '众智园AI自主创新加速区', 'type': '花园型自主创新街区', 'area': '~192 ha', 'color': '#4f46e5', 'dot': '#818cf8', 'num': '01',
             'actions': ['清河创新界面 — 滨水AI交往带 800m', '自主创新展示环路 — 1.2km环形展示路径', '众智创新公园 — 开放式创新绿地+算力节点', 'AI朝圣地标·智枢 — 成果展示+盲测+荣誉'],
             'deps': '关键依赖: 控规条件 / 河道蓝线 / 产业入驻协议 / 市政容量'},
            {'name': '北京AI原点社区', 'type': '近校型成果转化街区', 'area': '~104 ha', 'color': '#15803d', 'dot': '#4ade80', 'num': '02',
             'actions': ['开源协作街 — 800m 步行协作+黑客松空间', '人才共生组团 — 公寓×服务×AI商业×社区', '成果转化中庭 — 路演厅+IP服务中心+创投', 'AI朝圣地标·开源之环 — 全球开源脉搏可视化'],
             'deps': '关键依赖: 校区边界协商 / 权属确认 / 商户腾退方案 / 建设时序'},
            {'name': '大钟寺AI产业聚集区', 'type': '城市型智能经济街区', 'area': '~72 ha', 'color': '#b7791f', 'dot': '#fbbf24', 'num': '03',
             'actions': ['四象限步行连通 — 下沉广场+空中连廊+地面', '智能经济长廊 — 智能体展示+具身智能体验', '古钟×AI叙事 — 公共艺术+历史AI对话', 'AI朝圣地标·钟鸣塔 — 路演+观景+光影秀'],
             'deps': '关键依赖: 轨道站点改造 / 地下空间规划许可 / 投资概算'},
        ]
        areas_en = [
            {'name': 'Zhongzhiyuan AI Zone', 'type': 'Garden Innovation District', 'area': '~192 ha', 'color': '#4f46e5', 'dot': '#818cf8', 'num': '01',
             'actions': ['Qinghe Innovation Interface — 800m waterfront', 'Innovation Loop — 1.2km circular path', 'Innovation Park — open green + edge compute', 'Landmark: AI Pivot — showcase+blind test+honor'],
             'deps': 'Depends on: Regulatory conditions / River blue-line / Tenant agreements / Utility capacity'},
            {'name': 'AI Origin Community', 'type': 'Univ-Proximate Transfer District', 'area': '~104 ha', 'color': '#15803d', 'dot': '#4ade80', 'num': '02',
             'actions': ['Open-Source Street — 800m walkable hackathon', 'Talent Co-Living — apartment×service×retail', 'Transfer Atrium — roadshow+IP center+VC', 'Landmark: Open Source Ring — global pulse viz'],
             'deps': 'Depends on: Campus boundary / Ownership / Tenant relocation / Construction phasing'},
            {'name': 'Dazhongsi AI Cluster', 'type': 'Urban Intelligent Economy District', 'area': '~72 ha', 'color': '#b7791f', 'dot': '#fbbf24', 'num': '03',
             'actions': ['4-Quadrant Connectivity — sunken+bridge+surface', 'Intelligent Economy Corridor — agents+embodied AI', 'Bell×AI Narrative — public art+historical dialogue', 'Landmark: Bell Echo Tower — pitch+view+light show'],
             'deps': 'Depends on: Station renovation / Underground planning / Investment estimate'},
        ]
        areas = areas_zh if lang == 'zh' else areas_en

        cards_html_parts = []
        for a in areas:
            actions_html = ''.join('<li>%s</li>' % act for act in a['actions'])
            cards_html_parts.append("""
            <div class="ka-col">
              <div class="ka-card">
                <div class="ka-head" style="background:linear-gradient(135deg,%s,%sdd)">
                  <span class="ka-num">%s</span>
                  <span>%s</span>
                </div>
                <div class="ka-body">
                  <div class="ka-type" style="color:%s">%s · %s</div>
                  <ul style="--dot:%s">%s</ul>
                </div>
                <div class="ka-foot">%s</div>
              </div>
            </div>""" % (a['color'], a['color'], a['num'], a['name'],
                         a['color'], a['type'], a['area'], a['dot'], actions_html, a['deps']))
        cards_html = ''.join(cards_html_parts)

        body = """
<div class="title-bar">
  <h1>%s</h1>
  <div class="sub">%s</div>
</div>
<div class="content">

  <!-- 三列垂直卡片 -->
  <div class="row" style="height:430px;margin-bottom:16px">%s</div>

  <!-- 底部: 三地标联动 -->
  <h3 style="--hdr:#c79838">%s</h3>
  <div class="row">
    <div class="col">
      <div class="card" style="text-align:center;border-top:3px solid #4f46e5;padding:20px">
        <div style="font-size:40px;margin-bottom:8px">\U0001f3db</div>
        <div style="font-size:16px;font-weight:800;color:#4f46e5">%s</div>
        <div style="font-size:12px;color:#64748b;margin-top:4px">%s</div>
      </div>
    </div>
    <div class="col" style="justify-content:center;align-items:center;font-size:32px;color:#c79838;flex:0 0 auto;width:50px">⟷</div>
    <div class="col">
      <div class="card" style="text-align:center;border-top:3px solid #15803d;padding:20px">
        <div style="font-size:40px;margin-bottom:8px">\U0001f504</div>
        <div style="font-size:16px;font-weight:800;color:#15803d">%s</div>
        <div style="font-size:12px;color:#64748b;margin-top:4px">%s</div>
      </div>
    </div>
    <div class="col" style="justify-content:center;align-items:center;font-size:32px;color:#c79838;flex:0 0 auto;width:50px">⟷</div>
    <div class="col">
      <div class="card" style="text-align:center;border-top:3px solid #b7791f;padding:20px">
        <div style="font-size:40px;margin-bottom:8px">\U0001f514</div>
        <div style="font-size:16px;font-weight:800;color:#b7791f">%s</div>
        <div style="font-size:12px;color:#64748b;margin-top:4px">%s</div>
      </div>
    </div>
  </div>

  <p style="color:#94a3b8;font-size:11px;margin-top:8px;text-align:center">
    %s
  </p>
</div>
<div class="footer-bar">
  <span>AI Artery · Beijing — Conceptual Proposals</span>
  <span>Provisional Geometry · To be confirmed</span>
</div>""" % (
            L('三处重点区域 — 设计特征与空间动作', 'Three Key Areas — Design Features & Actions'),
            L('各有定位 · 各有空间动作 · 各有AI场景 · 各有AI朝圣地标 · 各有实施依赖', 'Each: positioning · spatial actions · AI scenarios · Landmark · dependencies'),
            cards_html,
            L('三处AI朝圣地标 · 京张AI信仰轴线', 'Three AI Pilgrimage Landmarks — Jing-Zhang AI Axis of Belief'),
            L('智枢', 'AI Pivot'), L('众智园 · 成果展示+盲测+荣誉', 'Zhongzhiyuan · Showcase+Blind Test+Honor'),
            L('开源之环', 'Open Source Ring'), L('AI原点 · 全球开源脉搏可视化', 'AI Origin · Global Open-Source Pulse'),
            L('钟鸣塔', 'Bell Echo Tower'), L('大钟寺 · 路演+观景+光影秀', 'Dazhongsi · Pitch+View+Light Show'),
            L('所有重点区动作和地标均为概念建议，待正式条件补齐后由专业团队深化实施', 'All key-area actions and landmarks are conceptual; deepen with formal conditions by professional teams'),
        )

    elif figure_id == 'mobility-bluegreen':
        body = """
<div class="title-bar">
  <h1>%s</h1>
  <div class="sub">%s</div>
</div>
<div class="content">

  <div class="row">
    <!-- 左列: 慢行系统 -->
    <div class="col">
      <h3 style="--hdr:#15803d">%s</h3>

      <div class="card" style="border-left:5px solid #15803d;padding:14px 16px;margin-bottom:8px">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">
          <span style="display:inline-block;width:16px;height:16px;background:#15803d;border-radius:3px"></span>
          <b style="font-size:14px">%s</b>
        </div>
        <div style="font-size:12px;color:#64748b;margin-left:24px">%s</div>
      </div>

      <div class="card" style="padding:14px 16px;margin-bottom:8px">
        <div style="font-size:12px;font-weight:700;color:#0f7490;margin-bottom:8px">%s</div>
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
          <span style="display:inline-block;width:12px;height:12px;background:#0f7490;border-radius:2px"></span>
          <span style="font-size:12px"><b>%s</b></span>
        </div>
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
          <span style="display:inline-block;width:12px;height:12px;background:#0f7490;border-radius:2px"></span>
          <span style="font-size:12px"><b>%s</b></span>
        </div>
        <div style="display:flex;align-items:center;gap:8px">
          <span style="display:inline-block;width:12px;height:12px;background:#0f7490;border-radius:2px"></span>
          <span style="font-size:12px"><b>%s</b></span>
        </div>
      </div>

      <h3 style="--hdr:#b42318;margin-top:4px">%s</h3>
      <div class="card" style="padding:14px 16px">
        %s
      </div>

      <h3 style="--hdr:#0f7490;margin-top:4px">%s</h3>
      <div class="card" style="padding:14px 16px">
        %s
      </div>
    </div>

    <!-- 右列: 蓝绿空间 -->
    <div class="col">
      <h3 style="--hdr:#15803d">%s</h3>

      <div class="card" style="border-left:5px solid #15803d;padding:14px 16px;margin-bottom:10px">
        <div style="font-size:14px;font-weight:700;color:#15803d;margin-bottom:6px">%s</div>
        <div style="font-size:12px;color:#64748b">%s</div>
      </div>

      <div class="row" style="gap:10px;margin-bottom:10px">
        <div class="col">
          <div class="card" style="padding:14px;text-align:center;border-top:3px solid #0f7490">
            <div style="font-size:28px;margin-bottom:4px">\U0001f30a</div>
            <div style="font-size:13px;font-weight:700">%s</div>
            <div style="font-size:11px;color:#64748b;margin-top:4px">%s</div>
          </div>
        </div>
        <div class="col">
          <div class="card" style="padding:14px;text-align:center;border-top:3px solid #0f7490">
            <div style="font-size:28px;margin-bottom:4px">\U0001f4a7</div>
            <div style="font-size:13px;font-weight:700">%s</div>
            <div style="font-size:11px;color:#64748b;margin-top:4px">%s</div>
          </div>
        </div>
      </div>

      <h3 style="--hdr:#15803d;margin-top:4px">%s</h3>
      <div class="card" style="padding:14px 16px">
        %s
      </div>

      <!-- 分布式算力 -->
      <div class="card" style="border:2px solid #4f46e5;padding:16px;margin-top:10px;background:linear-gradient(135deg,#f8fafc,#eef2ff)">
        <div style="display:flex;align-items:center;gap:10px">
          <span style="font-size:32px">⚡</span>
          <div>
            <div style="font-size:14px;font-weight:700;color:#4f46e5">%s</div>
            <div style="font-size:12px;color:#64748b">%s</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<div class="footer-bar">
  <span>AI Artery · Beijing — Conceptual Proposals</span>
  <span>Provisional Geometry · To be confirmed</span>
</div>""" % (
            L('交通慢行与蓝绿公共空间复合系统', 'Mobility, Slow-Traffic & Blue-Green Composite System'),
            L('一纵三横慢行骨架 · 五处断点缝合 · 京张遗址公园脊骨 · 四级公共空间 · 分布式端侧算力节点', '1-V 3-H Slow-Traffic · 5 Gap Sutures · Park Spine · 4-Level Public Space · Edge Compute Nodes'),
            L('慢行系统骨架', 'Slow-Traffic Network Skeleton'),
            L('京张慢行主廊（一纵）', 'Jing-Zhang Slow-Traffic Spine (V)'),
            L('约8km 北五环→西直门 · 宽30-80m · 南北贯通 · 自行车+步行专用', '~8km N5th Ring → Xizhimen · 30-80m wide · N-S through · Bike+Ped only'),
            L('三条创新横轴（三横）', 'Three Innovation Horizontal Axes'),
            L('北四环创新横轴', 'N4th Ring Innovation Axis'),
            L('知春路生活横轴', 'Zhichun Rd Living Axis'),
            L('学院路学术横轴', 'Xueyuan Rd Academic Axis'),
            L('五处慢行断点缝合', '5 Slow-Traffic Gap Sutures'),
            make_gap_rows(lang, L),
            L('轨道一体化TOD', 'TOD Integration'),
            make_tod_rows(lang, L),
            L('蓝绿空间体系', 'Blue-Green System'),
            L('京张遗址公园（一级脊骨）', 'Heritage Park (Level-1 Spine)'),
            L('宽30-80m 南北贯通 · 铁路遗产再生 · 连续公共空间', '30-80m wide N-S through · Railway heritage · Continuous public space'),
            L('清河生态廊道', 'Qinghe Eco-Corridor'), L('北侧蓝绿界面', 'Northern blue-green edge'),
            L('小月河生态廊道', 'Xiaoyuehe Eco-Corridor'), L('东侧蓝绿界面', 'Eastern blue-green edge'),
            L('四级公共空间网络', '4-Level Public Space Network'),
            make_psn_rows(lang, L),
            L('分布式端侧算力节点', 'Distributed Edge Compute Nodes'),
            L('8-12处 与公园/广场/社区中心叠合 覆盖半径≤800m · 5G+边缘推理', '8-12 nodes at parks/squares/community centers ≤800m radius · 5G+Edge inference'),
        )

    elif figure_id == 'metrics-evidence':
        body = """
<div class="title-bar">
  <h1>%s</h1>
  <div class="sub">%s</div>
</div>
<div class="content">

  <!-- 核心空间指标 6格 -->
  <h3 style="--hdr:#4f46e5">%s</h3>
  <div class="mgrid" style="margin-bottom:20px">
    <div class="mcard" style="--clr:#4f46e5">
      <div class="mlabel">%s</div>
      <div class="mvalue">11.41 <span style="font-size:14px">km²</span></div>
      <div class="msrc">%s</div>
    </div>
    <div class="mcard" style="--clr:#15803d">
      <div class="mlabel">%s</div>
      <div class="mvalue">12.3<span style="font-size:14px">%%</span></div>
      <div class="msrc">%s</div>
    </div>
    <div class="mcard" style="--clr:#b7791f">
      <div class="mlabel">%s</div>
      <div class="mvalue">7.3<span style="font-size:14px">%%</span></div>
      <div class="msrc">%s</div>
    </div>
    <div class="mcard" style="--clr:#b42318">
      <div class="mlabel">%s</div>
      <div class="mvalue" style="font-size:18px">%s</div>
      <div class="msrc">%s</div>
    </div>
    <div class="mcard" style="--clr:#0f7490">
      <div class="mlabel">%s</div>
      <div class="mvalue" style="font-size:18px">%s</div>
      <div class="msrc">%s</div>
    </div>
    <div class="mcard" style="--clr:#667085">
      <div class="mlabel">%s</div>
      <div class="mvalue" style="font-size:18px;color:#b42318">UNKNOWN</div>
      <div class="msrc">%s</div>
    </div>
  </div>

  <div class="row">
    <!-- 左: 结构化证据矩阵 -->
    <div class="col">
      <h3 style="--hdr:#15803d">%s</h3>
      <div class="ev-block" style="--clr:#15803d"><div class="ev-icon" style="background:#f0fdf4;color:#15803d">✓</div><span class="ev-name">compliance_matrix</span><span class="ev-desc">%s</span></div>
      <div class="ev-block" style="--clr:#4f46e5"><div class="ev-icon" style="background:#eef2ff;color:#4f46e5">✓</div><span class="ev-name">standard_matrix</span><span class="ev-desc">%s</span></div>
      <div class="ev-block" style="--clr:#b7791f"><div class="ev-icon" style="background:#fffbeb;color:#b7791f">✓</div><span class="ev-name">design_depth_matrix</span><span class="ev-desc">%s</span></div>
      <div class="ev-block" style="--clr:#15803d"><div class="ev-icon" style="background:#f0fdf4;color:#15803d">✓</div><span class="ev-name">self_check.json</span><span class="ev-desc">%s</span></div>
    </div>

    <!-- 右: Agent任务覆盖 -->
    <div class="col">
      <h3 style="--hdr:#c79838">%s</h3>
      <div class="card" style="padding:18px">
        <div class="tag-row" style="margin-bottom:10px">
          <span class="pill done">%s</span>
          <span class="pill done">%s</span>
          <span class="pill done">%s</span>
          <span class="pill done">%s</span>
          <span class="pill done">%s</span>
          <span class="pill done">%s</span>
        </div>

        <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:6px;font-size:11px;color:#475569">
          <div>agent.1 = %s</div>
          <div>agent.2 = %s</div>
          <div>agent.3 = %s</div>
          <div>agent.4 = %s</div>
          <div>agent.5 = %s</div>
          <div>agent.6 = %s</div>
        </div>
      </div>

      <div style="display:flex;gap:16px;margin-top:14px;align-items:center">
        <div class="badge-ring">%s</div>
        <div>
          <div style="font-size:12px;color:#475569;line-height:1.8">
            <span class="pill done" style="margin-right:6px">%s</span>
            <span class="pill done" style="margin-right:6px">%s</span>
            <span class="pill done" style="margin-right:6px">%s</span>
            <span class="pill done">%s</span>
          </div>
          <div style="margin-top:12px;font-size:11px;color:#94a3b8;line-height:1.6">
            %s
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<div class="footer-bar">
  <span>AI Artery · Beijing — All metrics provisional</span>
  <span>%s</span>
</div>""" % (
            L('核心指标复算与证据链', 'Core Metrics Recalculation & Evidence Chain'),
            L('GeoJSON复算 → 矩阵交叉验证 → 合规性确认 · 自检4/4 PASS', 'GeoJSON Recalc → Matrix Cross-Validation → Compliance Confirmation · Self-Check 4/4 PASS'),
            L('核心空间指标', 'Core Spatial Metrics'),
            L('设计面积', 'Site Area'), L('临时边界 · EPSG:4548', 'Provisional boundary · EPSG:4548'),
            L('绿地面积占比', 'Green Coverage Ratio'), L('来源: green_space.geojson', 'From: green_space.geojson'),
            L('公共空间占比', 'Public Space Ratio'), L('来源: public_space.geojson', 'From: public_space.geojson'),
            L('建筑基底面积', 'Building Footprint'), L('known/prov.', 'known / prov.'), L('来源: buildings.geojson', 'From: buildings.geojson'),
            L('道路面积', 'Road Area'), L('known/prov.', 'known / prov.'), L('来源: roads.geojson', 'From: roads.geojson'),
            L('容积率/高度/密度', 'FAR / Height / Density'), L('待控规条件补齐', 'Awaiting regulatory data'),
            L('结构化证据矩阵', 'Structured Evidence Matrix'),
            L('23项公告任务全映射 + agent.1-6全覆盖 · 每项标注证据路径', '23 announcement tasks mapped + agent.1-6 complete · evidence path per item'),
            L('5项强制性专业标准覆盖 · 含引用条款和方案响应', '5 mandatory professional standards · with clause references & proposal response'),
            L('15项设计深度ID全覆盖 · agent.4三地标深度扩展', '15 design depth IDs complete · agent.4 3-landmark depth extension'),
            L('确定性/空间/视觉/专业证据 4项全部PASS · 数据缺口不阻断', 'Deterministic/Spatial/Visual/Evidence 4/4 PASS · Data gaps flagged not blocked'),
            L('Agent任务覆盖图谱', 'Agent Task Coverage Map'),
            L('agent.1 ✅ 概念', 'agent.1 ✅ Concept'),
            L('agent.2 ✅ 生态', 'agent.2 ✅ Ecosystem'),
            L('agent.3 ✅ 场景', 'agent.3 ✅ Scenarios'),
            L('agent.4 ✅ 地标', 'agent.4 ✅ Landmarks'),
            L('agent.5 ✅ 文化', 'agent.5 ✅ Culture'),
            L('agent.6 ✅ 运营', 'agent.6 ✅ Ops'),
            L('命名+Logo+3定位+标语', 'Name+Logo+3 positions+Tagline'),
            L('8案例+5角色+资源清单', '8 cases+5 roles+Resource list'),
            L('10场景卡+3测试+5画像', '10 scenario cards+3 tests+5 personas'),
            L('3地标+荣誉体系+索引图', '3 landmarks+Honor system+Index map'),
            L('三重地层+人→智博物馆', '3-strata narrative+Human→AI Museum'),
            L('四季AI+飞轮+社区+转化', '4-season AI+Flywheel+Community+Conversion'),
            L('自检\n4/4\nPASS', 'SELF-CHECK\n4/4\nPASS'),
            L('确定性验证 PASS', 'Deterministic PASS'),
            L('空间审查 PASS', 'Spatial PASS'),
            L('视觉包装 PASS', 'Visual PASS'),
            L('专业证据 PASS', 'Evidence PASS'),
            L('数据缺口: 控规条件(FAR/高度/密度) + 官方精确边界 polygon\n所有缺口已标记在 assumptions.json · 不阻断设计评分', 'Data gaps: Regulatory conditions(FAR/Height/Density) + Official boundary polygon\nAll flagged in assumptions.json · Do NOT block design scoring'),
            L('自检4/4 PASS · 数据缺口已标记不阻断', 'Self-Check 4/4 PASS · Gaps flagged not blocked'),
        )

    return head + body + '</body></html>'


def screenshot_html(page, html_str, path):
    page.set_content(html_str)
    page.set_viewport_size({"width": W, "height": H})
    page.screenshot(path=path, full_page=False, type="png")
    print('Saved ' + path)


def main():
    figure_ids = ['site-overview', 'land-use-structure', 'key-areas', 'mobility-bluegreen', 'metrics-evidence']

    with sync_playwright() as p:
        browser = p.chromium.launch(channel='chrome', headless=True)
        page = browser.new_page(device_scale_factor=2)

        for lang in ['zh', 'en']:
            for fid in figure_ids:
                html_str = make_html(lang, fid)
                suffix = '.en' if lang == 'en' else ''
                path = os.path.join(ASSETS, fid + suffix + '.png')
                screenshot_html(page, html_str, path)

        browser.close()

    print('All 10 figures generated (HTML+CSS+Playwright).')


if __name__ == '__main__':
    main()
