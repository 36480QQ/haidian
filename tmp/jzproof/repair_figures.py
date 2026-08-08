from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("F:/Haidian/submissions/shanshui2024/jingzhang-proof-commons")
FIGURES = ROOT / "assets" / "figures"
FONT_REGULAR = "C:/Windows/Fonts/NotoSansSC-VF.ttf"
FONT_BOLD = "C:/Windows/Fonts/msyhbd.ttc"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


FOOTERS = {
    "site-overview.png": "同源图面：site_boundary / land_use / buildings / roads / green_space / public_space / metrics；边界虚线为 provisional。",
    "land-use-structure.png": "用地代码遵循项目枚举与 MNR 分类逻辑；彩色面为设计建议，非控规批准用地。",
    "key-areas.png": "重点区编号对应 key_areas.geojson；色彩只表达角色差异，不表达审批等级。",
    "mobility-bluegreen.png": "交通与蓝绿图由 roads / green_space / public_space 同源派生；不包含远程底图。",
    "metrics-evidence.png": "条形采用同类语义尺度：绿地/建筑 20%，公共空间 10%，慢行 50 km；不是目标值。",
}


def redraw_footer(image: Image.Image, left: str) -> None:
    draw = ImageDraw.Draw(image)
    bg = image.getpixel((20, 1085))
    draw.rectangle((0, 1027, image.width, image.height), fill=bg)
    draw.line((70, 1040, 1732, 1040), fill="#c6d2de", width=2)
    draw.text((70, 1067), left, font=font(16), fill="#5f7188", anchor="lm")
    draw.text(
        (1725, 1067),
        "PROVISIONAL INTAKE",
        font=font(16, bold=True),
        fill="#c96545",
        anchor="rm",
    )


def add_missing_key_number(image: Image.Image, center: tuple[int, int]) -> None:
    draw = ImageDraw.Draw(image)
    x, y = center
    draw.text(
        (x, y - 39),
        "1",
        font=font(19, bold=True),
        fill="#7166cf",
        stroke_width=3,
        stroke_fill="#f4f7fa",
        anchor="mm",
    )


def redraw_metric_bars(image: Image.Image) -> None:
    draw = ImageDraw.Draw(image)
    track_left, track_right = 425, 921
    track_width = track_right - track_left
    track_height = 41
    rows = [
        (300, 1.0, "#13263d", None),
        (415, 0.093021 / 0.20, "#2c9b6b", "尺度 20%"),
        (530, 0.047169 / 0.10, "#df9a2d", "尺度 10%"),
        (646, (947895.940 / 11412825.386) / 0.20, "#7166cf", "尺度 20%"),
        (760, 38101.593 / 50000.0, "#2789b2", "尺度 50 km"),
    ]

    draw.rectangle((410, 270, 945, 825), fill="#ffffff")
    draw.text(
        (921, 278),
        "条形按同类指标尺度归一化",
        font=font(14),
        fill="#6b7d92",
        anchor="ra",
    )
    for y, ratio, color, scale_label in rows:
        draw.rounded_rectangle(
            (track_left, y, track_right, y + track_height),
            radius=10,
            fill="#e9f0f4",
        )
        width = max(2, round(track_width * min(1.0, ratio)))
        draw.rounded_rectangle(
            (track_left, y, track_left + width, y + track_height),
            radius=10,
            fill=color,
        )
        if scale_label:
            draw.text(
                (907, y + track_height / 2),
                scale_label,
                font=font(13),
                fill="#6b7d92",
                anchor="rm",
            )


for filename, footer in FOOTERS.items():
    path = FIGURES / filename
    image = Image.open(path).convert("RGB")
    if filename == "site-overview.png":
        add_missing_key_number(image, (638, 512))
    elif filename == "key-areas.png":
        add_missing_key_number(image, (590, 514))
    elif filename == "metrics-evidence.png":
        redraw_metric_bars(image)
    redraw_footer(image, footer)
    image.save(path, format="PNG", optimize=True)

