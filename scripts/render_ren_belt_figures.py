#!/usr/bin/env python3
"""Render legible REN BELT evidence figures from the submission GeoJSON layers."""
from __future__ import annotations

import argparse
import json
import textwrap
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.lines import Line2D
from matplotlib import patheffects
from PIL import Image
from shapely.geometry import shape

FONT = "Microsoft YaHei"
COLORS = {
    "ink": "#19324A",
    "muted": "#667788",
    "paper": "#F7F4EE",
    "panel": "#FFFDF8",
    "rail": "#D78B4A",
    "spine": "#2F8F72",
    "green": "#BEE4C9",
    "public": "#F5C96A",
    "research": "#BBD7F1",
    "residential": "#F3C7C1",
    "commerce": "#D8C9F1",
    "provisional": "#D97B59",
    "road": "#D78B4A",
    "water": "#91C7D8",
    "white": "#FFFFFF",
}


def load_layer(root: Path, name: str) -> list[dict[str, Any]]:
    data = json.loads((root / "geometry" / f"{name}.geojson").read_text(encoding="utf-8"))
    return data["features"]


def geom(feature: dict[str, Any]):
    return shape(feature["geometry"])


def xy(g):
    if g.geom_type == "Point":
        return [g.x], [g.y]
    if g.geom_type in {"LineString", "LinearRing"}:
        x, y = g.xy
        return list(x), list(y)
    if g.geom_type == "Polygon":
        x, y = g.exterior.xy
        return list(x), list(y)
    if g.geom_type in {"MultiPolygon", "MultiLineString", "GeometryCollection"}:
        xs, ys = [], []
        for part in g.geoms:
            px, py = xy(part)
            xs.extend(px + [None])
            ys.extend(py + [None])
        return xs, ys
    return [], []


def draw_geom(ax, feature, *, face="none", edge=COLORS["ink"], lw=1.0, alpha=1.0, z=3, ls="-"):
    g = geom(feature)
    x, y = xy(g)
    ax.plot(x, y, color=edge, lw=lw, alpha=alpha, zorder=z, ls=ls)
    if g.geom_type in {"Polygon", "MultiPolygon"} and face != "none":
        ax.fill(x, y, color=face, alpha=alpha, zorder=z - 1)


def add_osm(ax, context_path: Path, extent=(116.33, 116.37, 39.93, 40.03), alpha=0.36):
    if not context_path.exists():
        return
    image = Image.open(context_path)
    ax.imshow(image, extent=extent, origin="upper", alpha=alpha, zorder=0, aspect="auto")
    ax.add_patch(Rectangle((extent[0], extent[2]), extent[1] - extent[0], extent[3] - extent[2], facecolor="#FFFFFF", alpha=0.20, zorder=1))


def setup(ax, title: str, subtitle: str, *, show_axis=False):
    ax.set_facecolor(COLORS["paper"])
    ax.set_title(title, loc="left", fontsize=22, fontweight="bold", color=COLORS["ink"], pad=18)
    ax.text(0, 1.01, subtitle, transform=ax.transAxes, fontsize=9, color=COLORS["muted"], va="bottom")
    ax.set_xlim(116.326, 116.368)
    ax.set_ylim(39.932, 40.031)
    ax.set_aspect("equal", adjustable="box")
    if not show_axis:
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values(): spine.set_visible(False)
    ax.annotate("N", xy=(0.97, 0.92), xytext=(0.97, 0.78), xycoords="axes fraction", ha="center", color=COLORS["ink"], fontsize=11, fontweight="bold", arrowprops={"arrowstyle": "-|>", "color": COLORS["ink"], "lw": 1.5})


def add_footer(fig, text: str):
    fig.text(0.05, 0.025, text, fontsize=8, color=COLORS["muted"])
    fig.text(0.95, 0.025, "REN BELT / 2026 · 概念方案", fontsize=8, color=COLORS["ink"], ha="right", fontweight="bold")


def style_axis(ax):
    ax.set_facecolor(COLORS["panel"])
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values(): spine.set_color("#D6DED9"); spine.set_linewidth(0.8)


def plot_base(ax, layers, context_path, *, osm=True):
    if osm:
        add_osm(ax, context_path)
    colors = [COLORS["residential"], COLORS["green"], COLORS["commerce"], COLORS["research"], COLORS["green"], COLORS["commerce"], COLORS["residential"], COLORS["green"], COLORS["commerce"]]
    for i, feature in enumerate(layers["land_use"]):
        draw_geom(ax, feature, face=colors[i % len(colors)], edge="#FFFFFF", lw=0.6, alpha=0.76, z=2)
    for feature in layers["green_space"]:
        draw_geom(ax, feature, face=COLORS["green"], edge="#77B590", lw=1.0, alpha=0.58, z=3)
    for feature in layers["public_space"]:
        draw_geom(ax, feature, face=COLORS["public"], edge="#C68E2D", lw=1.0, alpha=0.72, z=4)
    for feature in layers["roads"]:
        draw_geom(ax, feature, edge=COLORS["road"], lw=2.2, alpha=0.95, z=5)
    for feature in layers["site_boundary"]:
        draw_geom(ax, feature, edge=COLORS["provisional"], lw=1.6, alpha=0.95, z=6, ls=(0, (5, 3)))


def wrap_copy(value: str, width: int = 30) -> str:
    """Keep explanatory panel copy inside its card at print scale."""
    return "\n".join(textwrap.wrap(value, width=width, break_long_words=False, break_on_hyphens=False))


def label(ax, x, y, text, *, color=COLORS["ink"], size=9, weight="normal", ha="center", box=False):
    kwargs = dict(color=color, fontsize=size, fontweight=weight, ha=ha, va="center", zorder=10)
    if box:
        kwargs["bbox"] = dict(boxstyle="round,pad=0.25", facecolor=COLORS["panel"], edgecolor="#D6DED9", alpha=0.94)
    t = ax.text(x, y, text, **kwargs)
    t.set_path_effects([patheffects.withStroke(linewidth=2, foreground="#FFFFFF", alpha=0.85)])
    return t


def metric_card(ax, x, y, value, label_text, color=COLORS["ink"]):
    ax.text(x, y, value, transform=ax.transAxes, fontsize=20, fontweight="bold", color=color)
    ax.text(x, y - 0.08, label_text, transform=ax.transAxes, fontsize=9, color=COLORS["muted"])


def overview(root: Path, out: Path, layers: dict[str, list], context: Path):
    fig = plt.figure(figsize=(18, 10), facecolor=COLORS["paper"])
    gs = fig.add_gridspec(1, 3, width_ratios=[1.6, 0.76, 0.64], wspace=0.05)
    ax = fig.add_subplot(gs[0, 0]); setup(ax, "总览｜一脉三站 · 人字双翼", "以公开地图作地理参照；虚线为临时范围，不是官方红线")
    plot_base(ax, layers, context)
    for feature, name, col in zip(layers["key_areas"], ["众智园", "AI原点社区", "大钟寺"], [COLORS["commerce"], COLORS["spine"], COLORS["public"]]):
        g = geom(feature); c = g.centroid
        ax.scatter(c.x, c.y, s=105, color=col, edgecolor="white", linewidth=1.5, zorder=11)
        label(ax, c.x + 0.001, c.y + 0.0025, name, color=COLORS["ink"], size=9, weight="bold", ha="left", box=True)
    ax.plot([116.3482, 116.3482], [39.939, 40.0265], color=COLORS["spine"], lw=4, alpha=0.78, zorder=8)
    label(ax, 116.3500, 39.977, "京张遗址公园 9 km 主轴", color=COLORS["spine"], size=10, weight="bold", ha="left", box=True)
    ax.text(0.03, 0.05, "底图：OpenStreetMap contributors（位置参照）", transform=ax.transAxes, fontsize=7, color=COLORS["muted"], bbox=dict(facecolor="white", alpha=.8, edgecolor="none"))
    panel = fig.add_subplot(gs[0, 1]); style_axis(panel); panel.set_xlim(0,1); panel.set_ylim(0,1)
    panel.text(.08,.92,"设计判断",fontsize=16,fontweight="bold",color=COLORS["ink"])
    points=[("01", "遗产主轴", "把铁路遗产转译为连续可步行的公共空间骨架。"), ("02", "三站节点", "三个重点区分别承接产业、社区与文化交往。"), ("03", "双翼协同", "科技服务翼 × 场景赋能翼，形成跨区接口。"), ("04", "先试后扩", "轻量试点先行，依赖官方条件的项目分层推进。")]
    for i,(n,t,d) in enumerate(points):
        y=.78-i*.17; panel.text(.08,y,n,fontsize=12,fontweight="bold",color=COLORS["rail"]); panel.text(.22,y,t,fontsize=11,fontweight="bold",color=COLORS["ink"]); panel.text(.22,y-.05,wrap_copy(d, 29),fontsize=9,color=COLORS["muted"],va="top")
    panel.add_patch(FancyBboxPatch((.06,.08),.88,.13,boxstyle="round,pad=.02",facecolor="#F8EBDD",edgecolor="#E6B783")); panel.text(.1,.16,"边界状态",fontsize=9,fontweight="bold",color=COLORS["rail"]); panel.text(.1,.11,"provisional / 待官方几何替换",fontsize=9,color=COLORS["ink"])
    met = fig.add_subplot(gs[0, 2]); style_axis(met); met.set_xlim(0,1); met.set_ylim(0,1); met.text(.08,.92,"可复核指标",fontsize=16,fontweight="bold",color=COLORS["ink"])
    metric_card(met,.08,.78,"11.41", "km² 设计范围（临时）", COLORS["rail"]); metric_card(met,.08,.60,"24.0%", "绿地率", COLORS["spine"]); metric_card(met,.08,.42,"10.4%", "公共空间比例", COLORS["public"]); metric_card(met,.08,.24,"13.6", "km 慢行/连通廊", COLORS["ink"])
    add_footer(fig, "来源：geometry/*.geojson · metrics.json · OSM 位置参照；图中设计层均为概念建议")
    fig.savefig(out / "site-overview.png", dpi=160, bbox_inches="tight"); plt.close(fig)


def land_use(root: Path, out: Path, layers: dict[str, list], context: Path):
    fig = plt.figure(figsize=(18, 10), facecolor=COLORS["paper"]); gs=fig.add_gridspec(1,2,width_ratios=[1.55,1],wspace=.07)
    ax=fig.add_subplot(gs[0,0]); setup(ax,"用地结构｜从条带到可读的空间层级","9类用地不再堆叠：以三段纵向生长 + 中央遗产绿廊组织阅读")
    plot_base(ax,layers,context)
    for i, feature in enumerate(layers["land_use"]):
        g=geom(feature); c=g.centroid; name=feature["properties"].get("name_zh","")
        short=name.replace("与","·")
        label(ax,c.x,c.y,short,size=8,color=COLORS["ink"],box=True)
    label(ax,116.3502,40.026,"北段｜众智园",color=COLORS["ink"],size=10,weight="bold",ha="left",box=True)
    label(ax,116.3502,39.988,"中段｜AI原点社区",color=COLORS["ink"],size=10,weight="bold",ha="left",box=True)
    label(ax,116.3502,39.946,"南段｜大钟寺",color=COLORS["ink"],size=10,weight="bold",ha="left",box=True)
    panel=fig.add_subplot(gs[0,1]); style_axis(panel); panel.set_xlim(0,1); panel.set_ylim(0,1)
    panel.text(.07,.92,"一张图回答三个问题",fontsize=16,fontweight="bold",color=COLORS["ink"])
    rows=[("读关系","中轴绿廊不是装饰，而是把公共空间、慢行与遗产叙事串起来。"),("读差异","北段偏研发与产业，中段偏社区与转化，南段偏交往与消费。"),("读边界","色块是设计分区；临时范围用橙色虚线表达，不能替代法定红线。")]
    for i,(h,t) in enumerate(rows):
        y=.78-i*.2; panel.add_patch(FancyBboxPatch((.06,y-.1),.88,.14,boxstyle="round,pad=.02",facecolor="#FFFFFF",edgecolor="#D6DED9")); panel.text(.1,y,h,fontsize=11,fontweight="bold",color=COLORS["rail"]); panel.text(.1,y-.055,wrap_copy(t, 28),fontsize=9,color=COLORS["muted"],va="top")
    handles=[Rectangle((0,0),1,1,facecolor=COLORS["residential"],label="居住/社区"),Rectangle((0,0),1,1,facecolor=COLORS["green"],label="公园/绿地"),Rectangle((0,0),1,1,facecolor=COLORS["research"],label="教育/科研"),Rectangle((0,0),1,1,facecolor=COLORS["commerce"],label="产业/商业")]
    panel.legend(handles=handles,loc="lower left",bbox_to_anchor=(.06,.07),frameon=False,ncol=2,fontsize=9)
    add_footer(fig,"来源：geometry/land_use.geojson · site_boundary.geojson · OSM 位置参照")
    fig.savefig(out/"land-use-structure.png",dpi=160,bbox_inches="tight"); plt.close(fig)


def key_areas(root: Path, out: Path, layers: dict[str, list], context: Path):
    fig=plt.figure(figsize=(18,8.8),facecolor=COLORS["paper"]); fig.text(.05,.94,"重点区域｜三个可落位的操作单元",fontsize=22,fontweight="bold",color=COLORS["ink"]); fig.text(.05,.905,"不把矩形当红线：每个片区同时标出公开地图参照、连接线、节点与下一步专业复核事项。",fontsize=10,color=COLORS["muted"])
    gs=fig.add_gridspec(1,3,left=.04,right=.96,top=.86,bottom=.1,wspace=.035)
    names=["众智园 AI 自主创新加速区","北京 AI 原点社区","大钟寺 AI 产业聚集区"]; colors=[COLORS["commerce"],COLORS["spine"],COLORS["public"]]; areas=["约 192.1 ha","约 104.3 ha","约 72.0 ha"]
    for i,(feature,name,col,area) in enumerate(zip(layers["key_areas"],names,colors,areas)):
        ax=fig.add_subplot(gs[0,i]); style_axis(ax); g=geom(feature); minx,miny,maxx,maxy=g.bounds; pad=.004
        ax.set_xlim(minx-pad,maxx+pad); ax.set_ylim(miny-pad,maxy+pad); ax.set_aspect("equal")
        add_osm(ax,context,alpha=.28)
        ax.fill(*xy(g),color=col,alpha=.28,zorder=3); ax.plot(*xy(g),color=COLORS["provisional"],lw=2,ls=(0,(5,3)),zorder=5)
        # nearby design corridors
        for road in layers["roads"]:
            draw_geom(ax,road,edge=COLORS["road"],lw=1.5,alpha=.9,z=6)
        c=g.centroid; ax.scatter(c.x,c.y,s=100,color=col,edgecolor="white",lw=1.5,zorder=8)
        ax.text(.05,.95,name,transform=ax.transAxes,fontsize=12,fontweight="bold",color=COLORS["ink"],va="top",wrap=True)
        ax.text(.05,.83,area,transform=ax.transAxes,fontsize=11,fontweight="bold",color=col)
        notes=["依赖：官方边界、权属、控规条件","动作：创新广场 + 受控测试场景","连接：清河 / 遗产主轴 / 慢行"] if i==0 else ["依赖：社区参与、公共服务容量","动作：人字广场 + 成果转化街","连接：高校 / 原点站 / 公园绿廊"] if i==1 else ["依赖：轨交接口、文保与市政条件","动作：智能交往广场 + 路演客厅","连接：大钟寺站 / 南向门户"]
        for j,n in enumerate(notes): ax.text(.05,.22-j*.065,n,transform=ax.transAxes,fontsize=8.5,color=COLORS["muted"])
        ax.text(.05,.04,"provisional / 概念落位",transform=ax.transAxes,fontsize=8,color=COLORS["provisional"],fontweight="bold")
    add_footer(fig,"来源：geometry/key_areas.geojson · roads.geojson · OSM 位置参照；矩形边界不可作为法定红线")
    fig.savefig(out/"key-areas.png",dpi=160,bbox_inches="tight"); plt.close(fig)


def mobility(root: Path, out: Path, layers: dict[str, list], context: Path):
    fig=plt.figure(figsize=(18,10),facecolor=COLORS["paper"]); gs=fig.add_gridspec(1,2,width_ratios=[1.55,.85],wspace=.06)
    ax=fig.add_subplot(gs[0,0]); setup(ax,"交通慢行 × 蓝绿公共空间","把 9 km 绿色主轴、东西连通廊、五处绿地和公共节点放在同一张图里")
    add_osm(ax,context,alpha=.3)
    for feature in layers["green_space"]: draw_geom(ax,feature,face=COLORS["green"],edge="#77B590",lw=1.2,alpha=.6,z=3)
    for feature in layers["public_space"]: draw_geom(ax,feature,face=COLORS["public"],edge="#C68E2D",lw=1.1,alpha=.72,z=4)
    for feature in layers["roads"]:
        draw_geom(ax,feature,edge=COLORS["spine"] if feature["properties"].get("road_class")=="greenway" else COLORS["road"],lw=4 if feature["properties"].get("road_class")=="greenway" else 2,alpha=.92,z=6)
        g=geom(feature); c=g.centroid; label(ax,c.x+.001,c.y,feature["properties"].get("name_zh","").replace("京张遗址公园","京张公园"),size=8,color=COLORS["ink"],ha="left",box=True)
    for f in layers["public_space"]:
        c=geom(f).centroid; ax.scatter(c.x,c.y,s=38,color=COLORS["public"],edgecolor="white",lw=1,zorder=10)
    for f in layers["key_areas"]:
        g=geom(f); ax.plot(*xy(g),color=COLORS["provisional"],lw=1,ls=(0,(4,3)),zorder=7)
    panel=fig.add_subplot(gs[0,1]); style_axis(panel); panel.set_xlim(0,1); panel.set_ylim(0,1)
    panel.text(.08,.92,"系统动作",fontsize=16,fontweight="bold",color=COLORS["ink"])
    actions=[("主轴","绿色步行优先 · 9 km 连续叙事"),("横向","三条东西连接廊 · 跨社区缝合"),("节点","五处公共空间 · 站点 10 分钟可达"),("蓝绿","清河、小月河与遗产公园互联"),("安全","无人配送/治理沙盒仅限受控路段")]
    for i,(h,t) in enumerate(actions):
        y=.78-i*.13; panel.add_line(Line2D([.08,.9],[y-.015,y-.015],color="#D6DED9",lw=.8)); panel.text(.08,y,h,fontsize=10,fontweight="bold",color=COLORS["spine"]); panel.text(.25,y,t,fontsize=9,color=COLORS["ink"])
    panel.text(.08,.12,wrap_copy("道路为示意中心线；正式红线、消防、市政、轨道与防洪条件待官方资料和专业复核。", 32),fontsize=9,color=COLORS["muted"],va="top")
    add_footer(fig,"来源：geometry/roads.geojson · green_space.geojson · public_space.geojson · OSM 位置参照")
    fig.savefig(out/"mobility-bluegreen.png",dpi=160,bbox_inches="tight"); plt.close(fig)


def metrics(root: Path, out: Path, layers: dict[str, list], context: Path):
    fig=plt.figure(figsize=(18,9),facecolor=COLORS["paper"]); gs=fig.add_gridspec(1,2,width_ratios=[1.4,1],wspace=.07)
    ax=fig.add_subplot(gs[0,0]); setup(ax,"指标证据｜设计判断与复算口径","所有数字来自 geometry / metrics.json；临时边界只支持概念讨论")
    plot_base(ax,layers,context,osm=False)
    ax.set_xlim(116.336,116.359); ax.set_ylim(39.937,40.028)
    ax.plot([116.3482,116.3482],[39.939,40.0265],color=COLORS["spine"],lw=5,zorder=8)
    for f in layers["key_areas"]:
        c=geom(f).centroid; ax.scatter(c.x,c.y,s=70,color=COLORS["rail"],edgecolor="white",lw=1,zorder=10)
    panel=fig.add_subplot(gs[0,1]); style_axis(panel); panel.set_xlim(0,1); panel.set_ylim(0,1); panel.text(.08,.92,"核心指标",fontsize=16,fontweight="bold",color=COLORS["ink"])
    data=[("11.41 km²","site_area_sqm","总体设计范围（provisional）",COLORS["rail"]),("24.0%","green_ratio","绿地率",COLORS["spine"]),("10.4%","public_space_ratio","公共空间比例",COLORS["public"]),("72.3 万㎡","building_footprint_area_sqm","示意建筑基底",COLORS["commerce"]),("13.6 km","road_greenway_length_km","慢行/连通廊总长",COLORS["ink"])]
    for i,(value,key,desc,col) in enumerate(data):
        y=.79-i*.13; panel.add_patch(FancyBboxPatch((.06,y-.07),.88,.1,boxstyle="round,pad=.015",facecolor="#FFFFFF",edgecolor="#D6DED9")); panel.text(.1,y,value,fontsize=16,fontweight="bold",color=col); panel.text(.42,y+.003,desc,fontsize=9,fontweight="bold",color=COLORS["ink"]); panel.text(.42,y-.04,key,fontsize=7.5,color=COLORS["muted"])
    panel.add_patch(FancyBboxPatch((.06,.06),.88,.12,boxstyle="round,pad=.02",facecolor="#F8EBDD",edgecolor="#E6B783")); panel.text(.1,.135,"证据链",fontsize=9,fontweight="bold",color=COLORS["rail"]); panel.text(.1,.095,"geometry → EPSG:4548 复算 → metrics.json → 本图",fontsize=8.5,color=COLORS["ink"])
    add_footer(fig,"来源：metrics.json · scripts/spatial_review.py · geometry/*.geojson；FAR/高度等控制指标保持 unknown")
    fig.savefig(out/"metrics-evidence.png",dpi=160,bbox_inches="tight"); plt.close(fig)


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("submission",type=Path); args=parser.parse_args(); root=args.submission.resolve(); out=root/"assets/figures"; out.mkdir(parents=True,exist_ok=True); context=root/"assets/context/osm-site-context.png"
    layers={name:load_layer(root,name) for name in ["site_boundary","land_use","roads","green_space","public_space","key_areas"]}
    plt.rcParams.update({"font.family":FONT,"axes.unicode_minus":False})
    overview(root,out,layers,context); land_use(root,out,layers,context); key_areas(root,out,layers,context); mobility(root,out,layers,context); metrics(root,out,layers,context)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
