#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Safe entrypoint for the professional asset renderer.

This wrapper reuses render_professional_assets.py and replaces only the metrics-page
layout with a two-column grid so all six provisional metrics remain legible and the
professional-warning block cannot overlap a metric card.

Run from repository root:
    python3 submissions/GJYNBB/jingzhang-ai-nexus-belt/tools/render_professional_assets_safe.py --font-check-only
    python3 submissions/GJYNBB/jingzhang-ai-nexus-belt/tools/render_professional_assets_safe.py
"""

from __future__ import annotations

import render_professional_assets as core


def render_metrics_safe(layers, font_path, lang):
    metrics = core.load_json(core.METRICS_PATH).get("metrics", {})
    img, draw = core.base_canvas(font_path, lang, core.TEXT[lang]["metrics"])
    bounds = core.bbox_expand(core.union_geometry(layers["site"]).bounds)

    map_rect = (70, 245, 1275, 1450)
    core.draw_map_layers(
        draw,
        map_rect,
        bounds,
        layers,
        font_path,
        lang,
        land_use=False,
        buildings=False,
        mobility=True,
    )

    metric_ids = [
        "site_area_sqm",
        "green_ratio",
        "public_space_ratio",
        "zhongzhiyuan_area_sqm_provisional",
        "ai_origin_area_sqm_provisional",
        "dazhongsi_area_sqm_provisional",
    ]

    x0 = 1320
    y0 = 245
    gap_x = 18
    gap_y = 18
    card_w = 496
    card_h = 300

    for idx, metric_id in enumerate(metric_ids):
        metric = metrics.get(metric_id)
        if not metric:
            continue

        col = idx % 2
        row = idx // 2
        x = x0 + col * (card_w + gap_x)
        y = y0 + row * (card_h + gap_y)

        draw.rounded_rectangle(
            (x, y, x + card_w, y + card_h),
            radius=12,
            fill=core.WHITE,
            outline=core.LINE,
            width=2,
        )
        draw.text(
            (x + 22, y + 16),
            metric_id,
            font=core.font(font_path, 17),
            fill=core.MUTED,
        )
        draw.text(
            (x + 22, y + 47),
            core.metric_display(metric_id, metric, lang),
            font=core.font(font_path, 31),
            fill=core.BLUE,
        )

        confidence = str(metric.get("confidence") or "unknown")
        status = str(metric.get("status") or "unknown")
        status_color = core.GOLD if confidence == "low" else core.GREEN
        draw.text(
            (x + 22, y + 94),
            f"{status} · {confidence} confidence",
            font=core.font(font_path, 16),
            fill=status_color,
        )

        formula_label = core.TEXT[lang]["formula"]
        formula = str(metric.get("formula") or "")
        core.text_block(
            draw,
            (x + 22, y + 130),
            f"{formula_label}: {formula}",
            core.font(font_path, 15),
            core.INK,
            card_w - 44,
            4,
            4,
        )

        source_files = metric.get("source_files") or []
        if source_files:
            source_label = core.TEXT[lang]["source"]
            source_text = ", ".join(str(item) for item in source_files[:2])
            core.text_block(
                draw,
                (x + 22, y + 225),
                f"{source_label}: {source_text}",
                core.font(font_path, 14),
                core.MUTED,
                card_w - 44,
                3,
                2,
            )

    warning_top = 1212
    warning_bottom = 1435
    draw.rounded_rectangle(
        (1320, warning_top, 2330, warning_bottom),
        radius=12,
        fill=core.GOLD_LIGHT,
        outline=core.GOLD,
        width=2,
    )
    warning = (
        core.TEXT[lang]["low_conf"]
        + ". "
        + core.TEXT[lang]["responsibility"]
    )
    core.text_block(
        draw,
        (1345, warning_top + 25),
        warning,
        core.font(font_path, 18),
        "#6f4e14",
        960,
        7,
        6,
    )

    path = core.FIG_DIR / (
        "metrics-evidence.png" if lang == "zh" else "metrics-evidence.en.png"
    )
    img.convert("RGB").save(path, "PNG", optimize=True)
    return path


def main() -> int:
    # render_language resolves render_metrics from the core module at runtime,
    # so replacing this symbol fixes both Chinese and English metric figures.
    core.render_metrics = render_metrics_safe
    return core.main()


if __name__ == "__main__":
    raise SystemExit(main())
