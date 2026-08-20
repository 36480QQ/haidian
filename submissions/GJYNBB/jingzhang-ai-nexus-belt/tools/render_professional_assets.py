#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render professional bilingual spatial figures and raster PDFs for this submission.

This renderer is intentionally submission-local. It never downloads fonts, maps, tiles,
or other remote assets. It reads the committed GeoJSON/metrics sources, reprojects
spatial data to EPSG:4548, and refuses to render Chinese text unless a local font with
working CJK glyph coverage is found.

Usage from repository root:
    python3 submissions/GJYNBB/jingzhang-ai-nexus-belt/tools/render_professional_assets.py

Optional:
    JZ_CJK_FONT=/path/to/NotoSansCJK-Regular.ttc python3 .../render_professional_assets.py
"""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
from pathlib import Path
from typing import Any, Iterable

from PIL import Image, ImageDraw, ImageFont
from pyproj import Transformer
from shapely.geometry import GeometryCollection, LineString, MultiLineString, MultiPolygon, Polygon, shape
from shapely.ops import transform, unary_union

ROOT = Path(__file__).resolve().parents[1]
GEOM_DIR = ROOT / "geometry"
FIG_DIR = ROOT / "assets" / "figures"
DRAW_DIR = ROOT / "drawings"
METRICS_PATH = ROOT / "metrics.json"

PROJECT = Transformer.from_crs("EPSG:4326", "EPSG:4548", always_xy=True)

INK = "#102034"
MUTED = "#52657a"
PAPER = "#f6f8fb"
WHITE = "#ffffff"
LINE = "#9badc0"
BLUE = "#376fa6"
BLUE_LIGHT = "#d8e9f8"
GREEN = "#2f7d63"
GREEN_LIGHT = "#dcefe7"
GOLD = "#a87925"
GOLD_LIGHT = "#f5e8c8"
RED = "#a84b46"
RED_LIGHT = "#f3deda"
VIOLET = "#6656a6"
VIOLET_LIGHT = "#e7e2f5"
GRAY_LIGHT = "#e6ebf0"

KEY_NAMES = {
    "PROV-KEY-001": {"zh": "众智园", "en": "Zhongzhiyuan"},
    "PROV-KEY-002": {"zh": "AI原点", "en": "AI Origin"},
    "PROV-KEY-003": {"zh": "大钟寺", "en": "Dazhongsi"},
    "KEY-001": {"zh": "众智园", "en": "Zhongzhiyuan"},
    "KEY-002": {"zh": "AI原点", "en": "AI Origin"},
    "KEY-003": {"zh": "大钟寺", "en": "Dazhongsi"},
}

TEXT = {
    "zh": {
        "project": "百年京张·AI智枢生态带",
        "subtitle": "Jing-Zhang Intelligence Commons · 专业空间证据图",
        "provisional": "PROVISIONAL：边界与重点区为临时粗略几何；不是官方红线、控规或审批依据",
        "site_overview": "总体空间结构与三层范围",
        "land_use": "用地—建筑—更新结构",
        "key_areas": "三处重点区域详细设计证据",
        "mobility": "交通慢行—蓝绿公共空间复合系统",
        "metrics": "指标—来源—假设审计图",
        "site_boundary": "总体设计范围（provisional）",
        "key_boundary": "重点区（provisional）",
        "green": "蓝绿空间设计层",
        "public": "公共空间设计层",
        "roads": "道路/慢行设计中心线",
        "buildings": "建筑基底设计层",
        "north": "北",
        "scale": "比例尺（EPSG:4548）",
        "not_survey": "概念城市设计图 · 非测绘成果",
        "low_conf": "低置信度 / official geometry 到位后重算",
        "source": "来源",
        "formula": "公式",
        "confidence": "置信度",
        "assumption": "假设",
        "responsibility": "专业前置：正式红线、控规、权属、轨道、市政、消防、防洪、文保条件需另行确认",
        "core_loop": "一带三核两翼：遗产公共主脊 + 原点源头核 + 众智园验证核 + 大钟寺市场核",
        "key_action_1": "开放研发花园：共享测试庭院—清河公共客厅—步行研发环",
        "key_action_2": "校园—街区转化缝：5–10分钟步行连续 + 开源发布/IP法务/人才服务",
        "key_action_3": "站城四象限交换厅：步行连续 + 路演/终端展示/数据合规服务",
        "scenario": "AI场景节点（概念）",
    },
    "en": {
        "project": "Centennial Jing-Zhang AI Nexus Belt",
        "subtitle": "Jing-Zhang Intelligence Commons · Professional Spatial Evidence",
        "provisional": "PROVISIONAL: overall and key-area geometry is rough and not an official redline, statutory plan, or approval basis",
        "site_overview": "Overall Spatial Structure and Three-Level Scope",
        "land_use": "Land Use · Building · Renewal Structure",
        "key_areas": "Three Key Areas — Detailed Design Evidence",
        "mobility": "Mobility · Slow Network · Blue-Green Public Realm",
        "metrics": "Metrics · Sources · Assumptions Audit",
        "site_boundary": "Overall design scope (provisional)",
        "key_boundary": "Key area (provisional)",
        "green": "Blue-green design layer",
        "public": "Public-realm design layer",
        "roads": "Road / slow-mobility design centerline",
        "buildings": "Building-base design layer",
        "north": "N",
        "scale": "Scale (EPSG:4548)",
        "not_survey": "Concept urban-design drawing · not a survey product",
        "low_conf": "low confidence / recalculate after official geometry",
        "source": "Source",
        "formula": "Formula",
        "confidence": "Confidence",
        "assumption": "Assumption",
        "responsibility": "Professional prerequisites: official redlines, statutory controls, ownership, rail, utilities, fire, flood and heritage conditions require confirmation",
        "core_loop": "One belt / three cores / two wings: heritage civic spine + AI Origin source + Zhongzhiyuan validation + Dazhongsi market",
        "key_action_1": "Open R&D Garden: shared test courtyards — Qinghe civic waterfront — walking R&D loop",
        "key_action_2": "Campus-to-Street Seam: 5–10 min walking continuity + open source / IP-legal / talent services",
        "key_action_3": "Four-Quadrant Exchange Hall: walking continuity + roadshows / devices / data-compliance services",
        "scenario": "AI scenario node (concept)",
    },
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def feature_id(item: dict[str, Any]) -> str:
    props = item.get("properties") or {}
    return str(item.get("id") or props.get("id") or props.get("area_id") or "")


def load_layer(name: str) -> list[tuple[str, dict[str, Any], Any]]:
    data = load_json(GEOM_DIR / name)
    out: list[tuple[str, dict[str, Any], Any]] = []
    for item in data.get("features", []):
        geom_data = item.get("geometry")
        if not geom_data:
            continue
        geom = transform(PROJECT.transform, shape(geom_data))
        out.append((feature_id(item), item.get("properties") or {}, geom))
    return out


def union_geometry(layer: Iterable[tuple[str, dict[str, Any], Any]]) -> Any:
    geoms = [g for _, _, g in layer if not g.is_empty]
    return unary_union(geoms) if geoms else GeometryCollection()


def candidate_font_paths() -> list[Path]:
    paths: list[Path] = []
    env = os.environ.get("JZ_CJK_FONT")
    if env:
        paths.append(Path(env))
    fixed = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJKsc-Regular.otf",
        "/usr/share/fonts/opentype/noto/NotoSansCJKsc-VF.otf",
        "/usr/share/fonts/opentype/source-han-sans/SourceHanSansSC-Regular.otf",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    windir = os.environ.get("WINDIR")
    if windir:
        fixed.extend([
            str(Path(windir) / "Fonts" / "msyh.ttc"),
            str(Path(windir) / "Fonts" / "msyhbd.ttc"),
            str(Path(windir) / "Fonts" / "simhei.ttf"),
        ])
    paths.extend(Path(p) for p in fixed)
    try:
        for family in ["Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Micro Hei", "PingFang SC", "Microsoft YaHei"]:
            result = subprocess.run(
                ["fc-match", "-f", "%{file}\n", family],
                check=False,
                capture_output=True,
                text=True,
                timeout=3,
            )
            for line in result.stdout.splitlines():
                if line.strip():
                    paths.append(Path(line.strip()))
    except (FileNotFoundError, subprocess.SubprocessError):
        pass
    seen: set[str] = set()
    unique: list[Path] = []
    for p in paths:
        key = str(p)
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return unique


def glyph_signature(font: ImageFont.FreeTypeFont, char: str) -> tuple[tuple[int, int], bytes]:
    mask = font.getmask(char)
    return mask.size, bytes(mask)


def font_has_cjk(path: Path) -> bool:
    try:
        font = ImageFont.truetype(str(path), 38)
        a = glyph_signature(font, "京")
        b = glyph_signature(font, "智")
        c = glyph_signature(font, "园")
        return a[0][0] > 0 and a != b and b != c and a != c
    except Exception:
        return False


def find_cjk_font() -> Path:
    for path in candidate_font_paths():
        if path.is_file() and font_has_cjk(path):
            return path
    raise SystemExit(
        "No local CJK-capable font was found. Rendering aborted to prevent tofu/missing-glyph squares. "
        "Install a CJK font such as Noto Sans CJK or set JZ_CJK_FONT to a local licensed font path."
    )


def font(path: Path, size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    # A single verified CJK font is deliberately used for both normal and bold text;
    # synthetic stroke is added by Pillow when requested at draw time if needed.
    return ImageFont.truetype(str(path), size)


def bbox_expand(bounds: tuple[float, float, float, float], frac: float = 0.045) -> tuple[float, float, float, float]:
    minx, miny, maxx, maxy = bounds
    dx = max(maxx - minx, 1.0)
    dy = max(maxy - miny, 1.0)
    return minx - dx * frac, miny - dy * frac, maxx + dx * frac, maxy + dy * frac


def mapper(bounds: tuple[float, float, float, float], rect: tuple[int, int, int, int]):
    minx, miny, maxx, maxy = bounds
    left, top, right, bottom = rect
    bw = max(maxx - minx, 1.0)
    bh = max(maxy - miny, 1.0)
    rw = max(right - left, 1)
    rh = max(bottom - top, 1)
    scale = min(rw / bw, rh / bh)
    ox = left + (rw - bw * scale) / 2
    oy = top + (rh - bh * scale) / 2

    def project_xy(x: float, y: float) -> tuple[float, float]:
        return ox + (x - minx) * scale, oy + (maxy - y) * scale

    return project_xy, scale


def iter_polygons(geom: Any) -> Iterable[Polygon]:
    if geom.is_empty:
        return
    if isinstance(geom, Polygon):
        yield geom
    elif isinstance(geom, MultiPolygon):
        yield from geom.geoms
    elif isinstance(geom, GeometryCollection):
        for part in geom.geoms:
            yield from iter_polygons(part)


def iter_lines(geom: Any) -> Iterable[LineString]:
    if geom.is_empty:
        return
    if isinstance(geom, LineString):
        yield geom
    elif isinstance(geom, MultiLineString):
        yield from geom.geoms
    elif isinstance(geom, GeometryCollection):
        for part in geom.geoms:
            yield from iter_lines(part)


def draw_polygon(draw: ImageDraw.ImageDraw, geom: Any, mapxy, fill: str | None, outline: str, width: int = 3) -> None:
    for poly in iter_polygons(geom):
        pts = [mapxy(x, y) for x, y in poly.exterior.coords]
        if fill:
            draw.polygon(pts, fill=fill)
        draw.line(pts, fill=outline, width=width, joint="curve")
        for ring in poly.interiors:
            hole = [mapxy(x, y) for x, y in ring.coords]
            draw.polygon(hole, fill=WHITE)
            draw.line(hole, fill=outline, width=max(1, width // 2))


def draw_line(draw: ImageDraw.ImageDraw, geom: Any, mapxy, color: str, width: int = 5) -> None:
    for line in iter_lines(geom):
        pts = [mapxy(x, y) for x, y in line.coords]
        if len(pts) >= 2:
            draw.line(pts, fill=color, width=width, joint="curve")


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    out: list[str] = []
    for paragraph in str(text).split("\n"):
        if not paragraph:
            out.append("")
            continue
        if " " in paragraph:
            tokens = paragraph.split(" ")
            joiner = " "
        else:
            tokens = list(paragraph)
            joiner = ""
        line = ""
        for token in tokens:
            test = token if not line else line + joiner + token
            if draw.textbbox((0, 0), test, font=fnt)[2] <= max_width:
                line = test
            else:
                if line:
                    out.append(line)
                line = token
        if line:
            out.append(line)
    return out


def text_block(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fnt: ImageFont.FreeTypeFont,
               color: str, max_width: int, line_gap: int = 6, max_lines: int | None = None) -> int:
    x, y = xy
    lines = wrap_text(draw, text, fnt, max_width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=color)
        box = draw.textbbox((x, y), line or "Ag", font=fnt)
        y += (box[3] - box[1]) + line_gap
    return y


def base_canvas(font_path: Path, lang: str, title: str, size: tuple[int, int] = (2400, 1600)) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGBA", size, PAPER)
    draw = ImageDraw.Draw(img)
    w, _ = size
    draw.rectangle((0, 0, w, 150), fill=INK)
    draw.text((70, 34), TEXT[lang]["project"], font=font(font_path, 54), fill=WHITE, stroke_width=1)
    draw.text((72, 98), title, font=font(font_path, 27), fill="#c9d8e7")
    draw.rectangle((0, 150, w, 206), fill=GOLD_LIGHT)
    draw.text((70, 163), TEXT[lang]["provisional"], font=font(font_path, 23), fill="#6f4e14")
    return img, draw


def draw_north_scale(draw: ImageDraw.ImageDraw, map_bounds: tuple[float, float, float, float], rect: tuple[int, int, int, int],
                     mapxy, scale: float, font_path: Path, lang: str) -> None:
    left, top, right, bottom = rect
    x = right - 75
    y = top + 55
    draw.polygon([(x, y - 34), (x - 13, y + 4), (x + 13, y + 4)], fill=INK)
    draw.line((x, y + 4, x, y + 50), fill=INK, width=4)
    draw.text((x - 11, y + 54), TEXT[lang]["north"], font=font(font_path, 19), fill=INK)

    width_m = map_bounds[2] - map_bounds[0]
    options = [200, 500, 1000, 2000, 5000]
    target = width_m * 0.14
    length_m = min(options, key=lambda v: abs(v - target))
    px = max(50, int(length_m * scale))
    sx = left + 45
    sy = bottom - 44
    draw.line((sx, sy, sx + px, sy), fill=INK, width=5)
    draw.line((sx, sy - 9, sx, sy + 9), fill=INK, width=3)
    draw.line((sx + px, sy - 9, sx + px, sy + 9), fill=INK, width=3)
    label = f"{length_m / 1000:g} km" if length_m >= 1000 else f"{length_m} m"
    draw.text((sx, sy - 34), label, font=font(font_path, 18), fill=INK)


def draw_map_layers(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], bounds: tuple[float, float, float, float],
                    layers: dict[str, list[tuple[str, dict[str, Any], Any]]], font_path: Path, lang: str,
                    land_use: bool = False, buildings: bool = True, mobility: bool = True) -> tuple[Any, float]:
    mapxy, sc = mapper(bounds, rect)
    draw.rounded_rectangle(rect, radius=12, fill=WHITE, outline=LINE, width=2)
    if land_use:
        palette = [BLUE_LIGHT, GREEN_LIGHT, GOLD_LIGHT, RED_LIGHT, VIOLET_LIGHT, GRAY_LIGHT]
        for i, (_, _, geom) in enumerate(layers["land_use"]):
            draw_polygon(draw, geom, mapxy, palette[i % len(palette)], "#8d9daf", 2)
    if buildings:
        for _, _, geom in layers["buildings"]:
            draw_polygon(draw, geom, mapxy, "#ccd5df", "#8a9aaa", 1)
    for _, _, geom in layers["green"]:
        draw_polygon(draw, geom, mapxy, GREEN_LIGHT, GREEN, 3)
    for _, _, geom in layers["public"]:
        draw_polygon(draw, geom, mapxy, BLUE_LIGHT, BLUE, 3)
    if mobility:
        for _, _, geom in layers["roads"]:
            draw_line(draw, geom, mapxy, "#5b6672", 6)
    for _, _, geom in layers["site"]:
        draw_polygon(draw, geom, mapxy, None, INK, 6)
    for fid, _, geom in layers["keys"]:
        draw_polygon(draw, geom, mapxy, None, GOLD, 7)
        p = geom.representative_point()
        x, y = mapxy(p.x, p.y)
        label = KEY_NAMES.get(fid, {"zh": fid or "重点区", "en": fid or "Key area"})[lang]
        box = draw.textbbox((0, 0), label, font=font(font_path, 26))
        pad = 8
        draw.rounded_rectangle((x - (box[2] - box[0]) / 2 - pad, y - 22, x + (box[2] - box[0]) / 2 + pad, y + 18), radius=8, fill=INK)
        draw.text((x, y - 20), label, anchor="ma", font=font(font_path, 26), fill=WHITE)
    draw_north_scale(draw, bounds, rect, mapxy, sc, font_path, lang)
    return mapxy, sc


def legend_box(draw: ImageDraw.ImageDraw, font_path: Path, lang: str, x: int, y: int, width: int = 490) -> None:
    entries = [
        (INK, TEXT[lang]["site_boundary"]),
        (GOLD, TEXT[lang]["key_boundary"]),
        (GREEN, TEXT[lang]["green"]),
        (BLUE, TEXT[lang]["public"]),
        ("#5b6672", TEXT[lang]["roads"]),
        ("#a9b6c5", TEXT[lang]["buildings"]),
    ]
    h = 52 + len(entries) * 42
    draw.rounded_rectangle((x, y, x + width, y + h), radius=12, fill="#fdfefe", outline=LINE, width=2)
    draw.text((x + 22, y + 16), "LEGEND / 图例" if lang == "zh" else "LEGEND", font=font(font_path, 22), fill=INK)
    yy = y + 56
    for color, label in entries:
        draw.rectangle((x + 24, yy + 3, x + 48, yy + 27), fill=color)
        draw.text((x + 63, yy), label, font=font(font_path, 20), fill=INK)
        yy += 42


def load_layers() -> dict[str, list[tuple[str, dict[str, Any], Any]]]:
    return {
        "site": load_layer("site_boundary.geojson"),
        "keys": load_layer("key_areas.geojson"),
        "land_use": load_layer("land_use.geojson"),
        "buildings": load_layer("buildings.geojson"),
        "roads": load_layer("roads.geojson"),
        "green": load_layer("green_space.geojson"),
        "public": load_layer("public_space.geojson"),
    }


def render_site_overview(layers: dict[str, Any], font_path: Path, lang: str) -> Path:
    img, draw = base_canvas(font_path, lang, TEXT[lang]["site_overview"])
    bounds = bbox_expand(union_geometry(layers["site"]).bounds)
    rect = (70, 245, 1775, 1450)
    draw_map_layers(draw, rect, bounds, layers, font_path, lang, land_use=True)
    legend_box(draw, font_path, lang, 1815, 260, 515)
    y = 650
    draw.rounded_rectangle((1815, y, 2330, 1115), radius=12, fill=WHITE, outline=LINE, width=2)
    y = text_block(draw, (1840, y + 24), TEXT[lang]["core_loop"], font(font_path, 25), INK, 455, 8)
    y += 18
    for fid, _, geom in layers["keys"]:
        name = KEY_NAMES.get(fid, {"zh": fid, "en": fid})[lang]
        area_ha = geom.area / 10000.0
        draw.text((1840, y), f"{name}: ≈ {area_ha:.0f} ha · provisional", font=font(font_path, 21), fill=GOLD)
        y += 42
    y += 10
    text_block(draw, (1840, y), TEXT[lang]["responsibility"], font(font_path, 19), MUTED, 455, 7)
    draw.text((72, 1508), TEXT[lang]["not_survey"], font=font(font_path, 19), fill=MUTED)
    path = FIG_DIR / ("site-overview.png" if lang == "zh" else "site-overview.en.png")
    img.convert("RGB").save(path, "PNG", optimize=True)
    return path


def render_land_use(layers: dict[str, Any], font_path: Path, lang: str) -> Path:
    img, draw = base_canvas(font_path, lang, TEXT[lang]["land_use"])
    bounds = bbox_expand(union_geometry(layers["site"]).bounds)
    rect = (70, 245, 1760, 1450)
    draw_map_layers(draw, rect, bounds, layers, font_path, lang, land_use=True, mobility=False)
    x = 1800
    draw.rounded_rectangle((x, 245, 2330, 1450), radius=12, fill=WHITE, outline=LINE, width=2)
    draw.text((x + 28, 275), "LAND USE / 用地" if lang == "zh" else "LAND USE", font=font(font_path, 26), fill=INK)
    palette = [BLUE_LIGHT, GREEN_LIGHT, GOLD_LIGHT, RED_LIGHT, VIOLET_LIGHT, GRAY_LIGHT]
    y = 335
    for i, (_, props, geom) in enumerate(layers["land_use"]):
        code = str(props.get("land_use_code") or f"LU-{i + 1}")
        name = str(props.get("name_zh") or code) if lang == "zh" else f"Land-use {code}"
        draw.rectangle((x + 30, y + 2, x + 58, y + 30), fill=palette[i % len(palette)], outline="#8d9daf")
        draw.text((x + 75, y), name, font=font(font_path, 20), fill=INK)
        draw.text((x + 75, y + 28), f"{geom.area / 10000:.1f} ha · design layer", font=font(font_path, 16), fill=MUTED)
        y += 72
    y += 12
    text_block(draw, (x + 30, y), TEXT[lang]["responsibility"], font(font_path, 19), MUTED, 455, 7)
    path = FIG_DIR / ("land-use-structure.png" if lang == "zh" else "land-use-structure.en.png")
    img.convert("RGB").save(path, "PNG", optimize=True)
    return path


def render_key_areas(layers: dict[str, Any], font_path: Path, lang: str) -> Path:
    img, draw = base_canvas(font_path, lang, TEXT[lang]["key_areas"])
    panel_w = 740
    gap = 25
    actions = [TEXT[lang]["key_action_1"], TEXT[lang]["key_action_2"], TEXT[lang]["key_action_3"]]
    keys = layers["keys"][:3]
    for i, (fid, _, key_geom) in enumerate(keys):
        left = 55 + i * (panel_w + gap)
        top = 245
        right = left + panel_w
        bottom = 1450
        draw.rounded_rectangle((left, top, right, bottom), radius=12, fill=WHITE, outline=LINE, width=2)
        name = KEY_NAMES.get(fid, {"zh": fid, "en": fid})[lang]
        draw.text((left + 25, top + 24), name, font=font(font_path, 32), fill=INK)
        draw.text((left + 25, top + 67), f"≈ {key_geom.area / 10000:.0f} ha · provisional / low confidence", font=font(font_path, 18), fill=GOLD)
        local_bounds = bbox_expand(key_geom.bounds, 0.18)
        map_rect = (left + 25, top + 110, right - 25, top + 760)
        mapxy, _ = mapper(local_bounds, map_rect)
        draw.rounded_rectangle(map_rect, radius=8, fill="#fbfdff", outline="#c9d4df")
        for _, _, geom in layers["buildings"]:
            if geom.intersects(key_geom.buffer(max(key_geom.bounds[2] - key_geom.bounds[0], 1) * 0.12)):
                draw_polygon(draw, geom, mapxy, "#d7dee6", "#9aa8b6", 1)
        for _, _, geom in layers["green"]:
            if geom.intersects(key_geom):
                draw_polygon(draw, geom, mapxy, GREEN_LIGHT, GREEN, 2)
        for _, _, geom in layers["public"]:
            if geom.intersects(key_geom):
                draw_polygon(draw, geom, mapxy, BLUE_LIGHT, BLUE, 2)
        for _, _, geom in layers["roads"]:
            if geom.intersects(key_geom.buffer(300)):
                draw_line(draw, geom, mapxy, "#596777", 4)
        draw_polygon(draw, key_geom, mapxy, None, GOLD, 7)
        action_y = top + 800
        draw.text((left + 25, action_y), "DESIGN ACTION / 设计动作" if lang == "zh" else "DESIGN ACTION", font=font(font_path, 19), fill=BLUE)
        text_block(draw, (left + 25, action_y + 38), actions[i], font(font_path, 23), INK, panel_w - 50, 8, 5)
        prereq = TEXT[lang]["responsibility"]
        text_block(draw, (left + 25, top + 1010), prereq, font(font_path, 17), MUTED, panel_w - 50, 6, 6)
    path = FIG_DIR / ("key-areas.png" if lang == "zh" else "key-areas.en.png")
    img.convert("RGB").save(path, "PNG", optimize=True)
    return path


def render_mobility(layers: dict[str, Any], font_path: Path, lang: str) -> Path:
    img, draw = base_canvas(font_path, lang, TEXT[lang]["mobility"])
    bounds = bbox_expand(union_geometry(layers["site"]).bounds)
    rect = (70, 245, 1775, 1450)
    mapxy, sc = mapper(bounds, rect)
    draw.rounded_rectangle(rect, radius=12, fill=WHITE, outline=LINE, width=2)
    for _, _, geom in layers["green"]:
        draw_polygon(draw, geom, mapxy, GREEN_LIGHT, GREEN, 3)
    for _, _, geom in layers["public"]:
        draw_polygon(draw, geom, mapxy, BLUE_LIGHT, BLUE, 3)
    for _, _, geom in layers["roads"]:
        draw_line(draw, geom, mapxy, "#4c5968", 8)
        draw_line(draw, geom, mapxy, WHITE, 3)
    for _, _, geom in layers["site"]:
        draw_polygon(draw, geom, mapxy, None, INK, 6)
    scenario_colors = [VIOLET, BLUE, GREEN, GOLD, RED]
    for i, (fid, _, geom) in enumerate(layers["keys"]):
        draw_polygon(draw, geom, mapxy, None, GOLD, 7)
        c = geom.representative_point()
        x, y = mapxy(c.x, c.y)
        for j, label in enumerate([f"S{1 + i*3:02d}", f"S{2 + i*3:02d}", f"S{3 + i*3:02d}"]):
            angle = j * 2 * math.pi / 3 - math.pi / 2
            px = x + math.cos(angle) * 58
            py = y + math.sin(angle) * 58
            draw.ellipse((px - 16, py - 16, px + 16, py + 16), fill=scenario_colors[(i + j) % len(scenario_colors)], outline=WHITE, width=3)
            draw.text((px, py - 1), label, anchor="mm", font=font(font_path, 14), fill=WHITE)
    draw_north_scale(draw, bounds, rect, mapxy, sc, font_path, lang)
    legend_box(draw, font_path, lang, 1815, 260, 515)
    y = 650
    draw.rounded_rectangle((1815, y, 2330, 1115), radius=12, fill=WHITE, outline=LINE, width=2)
    draw.text((1840, y + 24), TEXT[lang]["scenario"], font=font(font_path, 24), fill=VIOLET)
    text_block(draw, (1840, y + 70), TEXT[lang]["core_loop"], font(font_path, 21), INK, 455, 8)
    text_block(draw, (1840, y + 190), TEXT[lang]["responsibility"], font(font_path, 18), MUTED, 455, 7)
    path = FIG_DIR / ("mobility-bluegreen.png" if lang == "zh" else "mobility-bluegreen.en.png")
    img.convert("RGB").save(path, "PNG", optimize=True)
    return path


def metric_display(metric_id: str, metric: dict[str, Any], lang: str) -> str:
    value = metric.get("value")
    unit = metric.get("unit")
    if value is None:
        return "unknown"
    if metric_id == "site_area_sqm":
        return f"≈ {value / 1_000_000:.2f} km²"
    if unit == "ratio":
        return f"≈ {value * 100:.2f}%"
    if unit == "sqm":
        return f"≈ {value / 10000:.0f} ha"
    return str(value)


def render_metrics(layers: dict[str, Any], font_path: Path, lang: str) -> Path:
    metrics = load_json(METRICS_PATH).get("metrics", {})
    img, draw = base_canvas(font_path, lang, TEXT[lang]["metrics"])
    bounds = bbox_expand(union_geometry(layers["site"]).bounds)
    rect = (70, 245, 1275, 1450)
    draw_map_layers(draw, rect, bounds, layers, font_path, lang, land_use=False, buildings=False, mobility=True)
    ids = ["site_area_sqm", "green_ratio", "public_space_ratio", "zhongzhiyuan_area_sqm_provisional", "ai_origin_area_sqm_provisional", "dazhongsi_area_sqm_provisional"]
    x = 1320
    y = 245
    card_w = 1010
    card_h = 178
    for metric_id in ids:
        m = metrics.get(metric_id)
        if not m:
            continue
        draw.rounded_rectangle((x, y, x + card_w, y + card_h), radius=12, fill=WHITE, outline=LINE, width=2)
        draw.text((x + 24, y + 17), metric_id, font=font(font_path, 20), fill=MUTED)
        draw.text((x + 24, y + 48), metric_display(metric_id, m, lang), font=font(font_path, 36), fill=BLUE)
        status = f"{m.get('status')} · {m.get('confidence')} confidence"
        draw.text((x + 330, y + 57), status, font=font(font_path, 19), fill=GOLD if m.get("confidence") == "low" else GREEN)
        formula = str(m.get("formula") or "")
        text_block(draw, (x + 24, y + 105), f"{TEXT[lang]['formula']}: {formula}", font(font_path, 16), INK, card_w - 48, 4, 2)
        y += card_h + 18
    draw.rounded_rectangle((1320, 1435 - 155, 2330, 1435), radius=12, fill=GOLD_LIGHT, outline=GOLD, width=2)
    text_block(draw, (1345, 1305), TEXT[lang]["low_conf"] + ". " + TEXT[lang]["responsibility"], font(font_path, 18), "#6f4e14", 960, 6, 5)
    path = FIG_DIR / ("metrics-evidence.png" if lang == "zh" else "metrics-evidence.en.png")
    img.convert("RGB").save(path, "PNG", optimize=True)
    return path


def fit_image(canvas: Image.Image, source: Image.Image, rect: tuple[int, int, int, int]) -> None:
    left, top, right, bottom = rect
    max_w = right - left
    max_h = bottom - top
    copy = source.convert("RGB")
    copy.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
    x = left + (max_w - copy.width) // 2
    y = top + (max_h - copy.height) // 2
    canvas.paste(copy, (x, y))


def pdf_page(font_path: Path, lang: str, title: str, size: tuple[int, int]) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", size, WHITE)
    draw = ImageDraw.Draw(img)
    w, _ = size
    draw.rectangle((0, 0, w, 125), fill=INK)
    draw.text((52, 26), TEXT[lang]["project"], font=font(font_path, 37), fill=WHITE)
    draw.text((54, 78), title, font=font(font_path, 21), fill="#c9d8e7")
    draw.rectangle((0, 125, w, 168), fill=GOLD_LIGHT)
    draw.text((54, 134), TEXT[lang]["provisional"], font=font(font_path, 16), fill="#6f4e14")
    return img, draw


def make_a3_pdf(font_path: Path, lang: str, figures: dict[str, Path]) -> Path:
    size = (2480, 1754)
    pages: list[Image.Image] = []
    order = [
        (TEXT[lang]["site_overview"], "site"),
        (TEXT[lang]["land_use"], "land"),
        (TEXT[lang]["key_areas"], "keys"),
        (TEXT[lang]["mobility"], "mobility"),
        (TEXT[lang]["metrics"], "metrics"),
    ]
    for title, key in order:
        page, draw = pdf_page(font_path, lang, title, size)
        src = Image.open(figures[key])
        fit_image(page, src, (60, 195, 2420, 1635))
        draw.text((62, 1668), TEXT[lang]["not_survey"], font=font(font_path, 15), fill=MUTED)
        pages.append(page)
    final, draw = pdf_page(font_path, lang, "Implementation / Operations" if lang == "en" else "实施与运营", size)
    col = 735
    x_positions = [80, 870, 1660]
    cards = [
        ("JZ-01 / JZ-02", TEXT[lang]["key_action_1"]),
        ("JZ-03 / JZ-04", TEXT[lang]["key_action_2"]),
        ("JZ-05 / JZ-06", TEXT[lang]["key_action_3"]),
    ]
    for x, (head, body) in zip(x_positions, cards):
        draw.rounded_rectangle((x, 260, x + col, 720), radius=16, fill=PAPER, outline=LINE, width=2)
        draw.text((x + 28, 290), head, font=font(font_path, 28), fill=BLUE)
        text_block(draw, (x + 28, 350), body, font(font_path, 24), INK, col - 56, 10)
    draw.rounded_rectangle((80, 790, 2400, 1500), radius=18, fill=PAPER, outline=LINE, width=2)
    operations = (
        "Q1 Open Source Spring → Q2 Civic AI Test Month → Q3 Jing-Zhang AI Week → Q4 Responsible AI Review. "
        "Scenario opening: application → risk grading → prototype → human acceptance → limited opening → review/exit."
        if lang == "en" else
        "Q1 Open Source Spring → Q2 Civic AI Test Month → Q3 Jing-Zhang AI Week → Q4 Responsible AI Review。"
        "场景开放：申请 → 风险分级 → 小样测试 → 人工验收 → 限时开放 → 复盘/退出；保留线下预约。"
    )
    text_block(draw, (120, 850), operations, font(font_path, 31), INK, 2240, 13)
    text_block(draw, (120, 1160), TEXT[lang]["responsibility"], font(font_path, 27), RED, 2240, 12)
    pages.append(final)
    path = DRAW_DIR / ("a3-booklet.pdf" if lang == "zh" else "a3-booklet.en.pdf")
    pages[0].save(path, "PDF", resolution=150, save_all=True, append_images=pages[1:])
    return path


def make_a0_pdf(font_path: Path, lang: str, figures: dict[str, Path]) -> Path:
    size = (3508, 2480)
    pages: list[Image.Image] = []
    board1, draw = pdf_page(font_path, lang, "Board 01 / Spatial Structure" if lang == "en" else "展板 01 / 总体空间结构", size)
    fit_image(board1, Image.open(figures["site"]), (70, 200, 2260, 2320))
    fit_image(board1, Image.open(figures["keys"]), (2290, 200, 3440, 1280))
    fit_image(board1, Image.open(figures["metrics"]), (2290, 1310, 3440, 2320))
    pages.append(board1)

    board2, draw = pdf_page(font_path, lang, "Board 02 / Systems and Implementation" if lang == "en" else "展板 02 / 系统与实施", size)
    fit_image(board2, Image.open(figures["land"]), (70, 200, 1725, 1760))
    fit_image(board2, Image.open(figures["mobility"]), (1780, 200, 3440, 1760))
    draw.rounded_rectangle((70, 1820, 3440, 2320), radius=18, fill=PAPER, outline=LINE, width=2)
    ops = (
        "JZ-01 walking stitch · JZ-02 Qinghe innovation edge · JZ-03 near-campus translation street · "
        "JZ-04 Dazhongsi four-quadrant link · JZ-05 civic service/edge compute · JZ-06 Global AI Week route. "
        "Every project has a human owner, professional prerequisite, acceptance condition, and exit path."
        if lang == "en" else
        "JZ-01 慢行断点缝合 · JZ-02 清河创新界面 · JZ-03 近校成果转化街 · JZ-04 大钟寺四象限步行连通 · "
        "JZ-05 公共服务/端侧算力 · JZ-06 全球AI活动周路线。每项均需明确人工责任主体、专业前置、验收条件与退出路径。"
    )
    text_block(draw, (115, 1870), ops, font(font_path, 31), INK, 3250, 13)
    pages.append(board2)
    path = DRAW_DIR / ("a0-boards.pdf" if lang == "zh" else "a0-boards.en.pdf")
    pages[0].save(path, "PDF", resolution=120, save_all=True, append_images=pages[1:])
    return path


def render_language(layers: dict[str, Any], font_path: Path, lang: str, skip_pdf: bool) -> list[Path]:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    DRAW_DIR.mkdir(parents=True, exist_ok=True)
    figures = {
        "site": render_site_overview(layers, font_path, lang),
        "land": render_land_use(layers, font_path, lang),
        "keys": render_key_areas(layers, font_path, lang),
        "mobility": render_mobility(layers, font_path, lang),
        "metrics": render_metrics(layers, font_path, lang),
    }
    outputs = list(figures.values())
    if not skip_pdf:
        outputs.append(make_a3_pdf(font_path, lang, figures))
        outputs.append(make_a0_pdf(font_path, lang, figures))
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=["zh", "en", "both"], default="both")
    parser.add_argument("--skip-pdf", action="store_true")
    parser.add_argument("--font-check-only", action="store_true")
    args = parser.parse_args()

    font_path = find_cjk_font()
    print(f"CJK font: {font_path}")
    if args.font_check_only:
        print("CJK glyph check: PASS")
        return 0

    layers = load_layers()
    if not layers["site"] or not layers["keys"]:
        raise SystemExit("Required site/key-area geometry is missing; refusing to render misleading spatial figures.")

    languages = ["zh", "en"] if args.lang == "both" else [args.lang]
    outputs: list[Path] = []
    for lang in languages:
        outputs.extend(render_language(layers, font_path, lang, args.skip_pdf))

    print("Rendered professional assets:")
    for path in outputs:
        print(f"  {path.relative_to(ROOT)}")
    print("Manual QA required: inspect all PNG/PDF pages for glyphs, clipping, legends, provisional labels, and spatial readability.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
