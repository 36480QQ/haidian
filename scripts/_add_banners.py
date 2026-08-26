#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add OSM attribution and PROVISIONAL warning banners to key figures."""
from pathlib import Path
from PIL import Image as PILImage, ImageDraw, ImageFont

FIG = Path("submissions/wengyongsheng29-spec/jingzhang-agent-native-belt/assets/figures")

# Files that need PROVISIONAL warning (maps with site-specific data)
PROVISIONAL_FILES = [
    "site-overview.png",
    "site-overview.en.png",
    "key-areas.png",
    "key-areas.en.png",
    "site-readiness.png",
    "site-readiness.en.png",
    "land-use-structure.png",
    "land-use-structure.en.png",
    "mobility-bluegreen.png",
    "mobility-bluegreen.en.png",
]

# Files that need OSM attribution (maps using OSM road data)
OSM_ATTRIBUTION_FILES = [
    "site-overview.png",
    "site-overview.en.png",
    "key-areas.png",
    "key-areas.en.png",
    "site-readiness.png",
    "site-readiness.en.png",
    "land-use-structure.png",
    "land-use-structure.en.png",
    "mobility-bluegreen.png",
    "mobility-bluegreen.en.png",
]

def get_font(size):
    """Try to load a font that supports Chinese."""
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/msyhbd.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
    ]
    for fp in font_paths:
        if Path(fp).exists():
            try:
                return ImageFont.truetype(fp, size)
            except:
                continue
    return ImageFont.load_default()

def add_banner(img_path, text_zh, text_en, position="top", bg_color=(220, 50, 50), text_color=(255, 255, 255)):
    """Add a warning/attribution banner to an image."""
    p = FIG / img_path
    if not p.exists():
        print(f"  {img_path}: not found, skipping")
        return False
    try:
        with PILImage.open(p) as im:
            im = im.convert("RGBA")
            w, h = im.size
            # Idempotency guard: if the edge already carries a banner of the
            # same color, skip (prevents duplicate banners on re-run).
            edge = im.crop((0, 0, w, max(2, int(h*0.04)))) if position == "top" \
                   else im.crop((0, h - max(2, int(h*0.04)), w, h))
            ext = edge.getextrema()
            # extrema per channel: if the edge strip is ~uniform solid color
            # (low spread) and matches the banner color, it's already bannered.
            r_spread = ext[0][1] - ext[0][0]
            g_spread = ext[1][1] - ext[1][0]
            b_spread = ext[2][1] - ext[2][0]
            if r_spread < 25 and g_spread < 25 and b_spread < 25:
                print(f"  {img_path}: edge already solid (banner present), skip")
                return False
            # Banner height proportional to image
            banner_h = max(28, int(h * 0.035))
            font_size = max(12, int(banner_h * 0.55))
            font = get_font(font_size)

            # Create banner
            banner = PILImage.new("RGBA", (w, banner_h), bg_color + (230,))
            draw = ImageDraw.Draw(banner)

            # Text
            full_text = f"{text_zh}  |  {text_en}" if text_zh else text_en
            bbox = draw.textbbox((0, 0), full_text, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            tx = (w - tw) // 2
            ty = (banner_h - th) // 2 - 2
            draw.text((tx, ty), full_text, fill=text_color + (255,), font=font)

            # Paste banner
            result = PILImage.new("RGBA", (w, h + banner_h), (255, 255, 255, 255))
            if position == "top":
                result.paste(banner, (0, 0))
                result.paste(im, (0, banner_h))
            else:
                result.paste(im, (0, 0))
                result.paste(banner, (0, h))

            # Save as PNG (keep .png extension)
            result.convert("RGB").save(p, "PNG", optimize=True)
            print(f"  {img_path}: added {position} banner ({banner_h}px)")
            return True
    except Exception as e:
        print(f"  {img_path}: ERROR - {e}")
        return False

print("=== Adding PROVISIONAL warning banners (top) ===")
provisional_count = 0
for fname in PROVISIONAL_FILES:
    is_en = ".en." in fname
    if is_en:
        zh, en = "", "PROVISIONAL — Conceptual illustration only, not official boundary"
    else:
        zh, en = "临时边界·概念示意·非官方红线 PROVISIONAL", "Conceptual illustration only, not official boundary"
    if add_banner(fname, zh, en, position="top", bg_color=(200, 40, 40)):
        provisional_count += 1

print(f"\n=== Adding OSM attribution banners (bottom) ===")
osm_count = 0
for fname in OSM_ATTRIBUTION_FILES:
    is_en = ".en." in fname
    if is_en:
        zh, en = "", "Road basemap © OpenStreetMap contributors, ODbL"
    else:
        zh, en = "底图道路数据 © OpenStreetMap贡献者 ODbL", "Road basemap © OpenStreetMap contributors, ODbL"
    if add_banner(fname, zh, en, position="bottom", bg_color=(40, 80, 140)):
        osm_count += 1

print(f"\nDone! Added {provisional_count} provisional banners and {osm_count} OSM attribution banners.")
