import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WIDTH = 1400
HEIGHT = 900
MAP_LEFT = 72
MAP_TOP = 128
MAP_RIGHT = 1010
MAP_BOTTOM = 820

PROGRAM_COLORS = {
    "research_r_and_d": "#a7d8df",
    "innovation_testing": "#f6d35f",
    "enterprise_service": "#e8a06f",
    "mixed_public_commercial": "#efb7a2",
    "community_life_service": "#b8d79e",
    "cultural_heritage": "#d4b5d8",
    "blue_green_public_realm": "#82c9ad",
    "mobility_interface": "#c9ced3",
}


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_layers(root=ROOT):
    root = Path(root)
    return {
        path.stem: read_json(path)
        for path in sorted((root / "spatial").glob("*.geojson"), key=lambda item: item.name)
    }


def coordinate_pairs(value):
    if not isinstance(value, list):
        return
    if len(value) >= 2 and all(isinstance(item, (int, float)) for item in value[:2]):
        yield value[:2]
        return
    for item in value:
        yield from coordinate_pairs(item)


def feature_bounds(features):
    pairs = [
        pair
        for item in features
        if item.get("geometry") is not None
        for pair in coordinate_pairs(item["geometry"].get("coordinates", []))
    ]
    if not pairs:
        return (0.0, 0.0, 1.0, 1.0)
    xs = [pair[0] for pair in pairs]
    ys = [pair[1] for pair in pairs]
    padding_x = max((max(xs) - min(xs)) * 0.05, 0.0004)
    padding_y = max((max(ys) - min(ys)) * 0.05, 0.0004)
    return min(xs) - padding_x, min(ys) - padding_y, max(xs) + padding_x, max(ys) + padding_y


def projector(bounds):
    min_x, min_y, max_x, max_y = bounds
    source_width = max_x - min_x or 1.0
    source_height = max_y - min_y or 1.0
    target_width = MAP_RIGHT - MAP_LEFT
    target_height = MAP_BOTTOM - MAP_TOP
    scale = min(target_width / source_width, target_height / source_height)
    used_width = source_width * scale
    used_height = source_height * scale
    offset_x = MAP_LEFT + (target_width - used_width) / 2
    offset_y = MAP_TOP + (target_height - used_height) / 2

    def project(pair):
        return (
            offset_x + (pair[0] - min_x) * scale,
            offset_y + used_height - (pair[1] - min_y) * scale,
        )

    return project


def style_for(item):
    props = item.get("properties", {})
    semantic = props.get("semantic_class", "")
    program = props.get("program_class")
    mobility = props.get("mobility_class")
    if program:
        return PROGRAM_COLORS.get(program, "#ddddda"), "#252525", 1.2, "", 0.72
    styles = {
        "main_if_segment": ("none", "#e6512e", 7.0, "", 1.0),
        "parallel_human_segment": ("none", "#008c99", 4.0, "10 7", 1.0),
        "east_west_public_stitch": ("none", "#3c8790", 2.4, "", 0.9),
        "service_resource_relationship": ("none", "#b14f77", 2.0, "9 6", 0.75),
        "schematic_ecosystem_edge": ("none", "#76569b", 2.3, "3 6", 0.9),
        "data_governance_relationship": ("none", "#de6d35", 2.6, "2 5", 0.95),
        "physical_corridor_background": ("none", "#72777b", 2.8, "", 0.55),
        "context_anchor": ("#f5f3ed", "#555b60", 1.5, "4 3", 0.9),
        "ecosystem_node": ("#ffffff", "#202020", 2.0, "", 1.0),
        "endpoint_public_room": ("#fff0d7", "#e6512e", 2.0, "", 0.75),
        "endpoint_gateway": ("#e6512e", "#ffffff", 2.0, "", 1.0),
        "human_service_node": ("#008c99", "#ffffff", 2.0, "", 1.0),
        "concept_massing": ("#d7d8d5", "#1d1d1b", 1.8, "", 0.92),
        "proposed_blue_green_heritage": ("#75bd9c", "#216a55", 2.0, "", 0.55),
        "background_blue_green_heritage": ("#e8eee8", "#60756b", 1.7, "6 5", 0.85),
        "controlled_test_yard": ("#f4cf4c", "#222222", 2.2, "", 0.7),
        "safety_buffer": ("#f9e8a2", "#d07a26", 2.0, "7 5", 0.45),
        "public_observation": ("none", "#008c99", 4.0, "", 1.0),
        "human_review_gate": ("#ef6c3e", "#ffffff", 2.0, "", 1.0),
        "ordinary_public_path": ("none", "#168c98", 3.5, "", 1.0),
        "cycle_test_loop": ("none", "#397c91", 3.0, "7 4", 1.0),
        "physical_emergency_stop": ("none", "#d52b2b", 4.0, "", 1.0),
        "permeability_path": ("none", "#008c99", 4.0, "", 1.0),
        "open_source_commons": ("#a8d9a1", "#245b2c", 2.0, "", 0.72),
        "pedestrian_convergence": ("none", "#008c99", 4.0, "", 1.0),
        "unresolved_station_relationship": ("none", "#7f7f7f", 2.0, "4 7", 0.8),
        "endpoint_landmark": ("#141414", "#ef6c3e", 3.0, "", 1.0),
        "spatial_component": ("#ffffff", "#2b2b2b", 2.0, "", 1.0),
    }
    if mobility:
        mobility_styles = {
            "background_road_context": ("none", "#7c8185", 3.0, "8 5", 0.55),
            "proposed_street": ("none", "#202020", 5.0, "", 0.9),
            "pedestrian_path": ("none", "#008c99", 3.5, "", 1.0),
            "cycleway": ("none", "#2a718b", 3.0, "7 4", 1.0),
            "service_logistics": ("none", "#8e5c3b", 3.0, "6 4", 0.9),
            "emergency_access": ("none", "#cf3333", 3.0, "2 4", 0.9),
        }
        return mobility_styles.get(mobility, ("none", "#777777", 2.0, "5 5", 0.8))
    if props.get("design_status") == "background_reference":
        return "#f3f1eb", "#777777", 1.5, "5 4", 0.75
    geometry_type = item.get("geometry", {}).get("type") if item.get("geometry") else ""
    if geometry_type in {"Polygon", "MultiPolygon"}:
        return "#e2e1dc", "#333333", 1.5, "", 0.7
    return "none", "#303030", 2.0, "", 0.9


def svg_style(item):
    fill, stroke, width, dash, opacity = style_for(item)
    dash_value = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'fill="{fill}" stroke="{stroke}" stroke-width="{width}" '
        f'opacity="{opacity}" vector-effect="non-scaling-stroke"{dash_value}'
    )


def points_attribute(coordinates, project):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in (project(pair) for pair in coordinates))


def render_geometry(item, project):
    geometry = item.get("geometry")
    if geometry is None:
        return ""
    geometry_type = geometry["type"]
    coordinates = geometry["coordinates"]
    style = svg_style(item)
    feature_id = html.escape(item.get("id", ""))
    title = f"<title>{feature_id}</title>"
    if geometry_type == "Point":
        x, y = project(coordinates)
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" {style}>{title}</circle>'
    if geometry_type == "MultiPoint":
        return "".join(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" {style}>{title}</circle>'
            for x, y in (project(pair) for pair in coordinates)
        )
    if geometry_type == "LineString":
        return f'<polyline points="{points_attribute(coordinates, project)}" {style}>{title}</polyline>'
    if geometry_type == "MultiLineString":
        return "".join(
            f'<polyline points="{points_attribute(line, project)}" {style}>{title}</polyline>'
            for line in coordinates
        )
    if geometry_type == "Polygon":
        parts = [
            f'<polygon points="{points_attribute(ring, project)}" {style}>{title}</polygon>'
            for ring in coordinates
        ]
        return "".join(parts)
    if geometry_type == "MultiPolygon":
        return "".join(
            f'<polygon points="{points_attribute(ring, project)}" {style}>{title}</polygon>'
            for polygon in coordinates
            for ring in polygon
        )
    return ""


def text(x, y, value, size=16, weight=400, fill="#222222", anchor="start", family="Arial, sans-serif"):
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" letter-spacing="0">'
        f'{html.escape(str(value))}</text>'
    )


def svg_shell(title, subtitle, body, notes, legend):
    note_markup = "".join(
        text(1060, 360 + index * 54, f"{index + 1:02d}  {value}", 14, 400, "#343434")
        for index, value in enumerate(notes[:8])
    )
    legend_markup = "".join(
        f'<line x1="1060" y1="{176 + index * 31}" x2="1105" y2="{176 + index * 31}" '
        f'stroke="{color}" stroke-width="{width}" {dash}/>'
        + text(1120, 181 + index * 31, label, 13, 600)
        for index, (label, color, width, dash) in enumerate(legend)
    )
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <rect width="{WIDTH}" height="{HEIGHT}" fill="#f7f6f2"/>
  <rect x="0" y="0" width="{WIDTH}" height="8" fill="#111111"/>
  {text(72, 54, title, 28, 700)}
  {text(72, 83, subtitle, 15, 400, '#555555')}
  {text(1328, 48, 'INTERNAL GATE B REVIEW', 13, 700, '#e6512e', 'end')}
  {text(1328, 72, 'DESIGN TARGET / CONCEPT', 12, 600, '#555555', 'end')}
  <line x1="72" y1="102" x2="1328" y2="102" stroke="#222222" stroke-width="1"/>
  <rect x="1035" y="126" width="293" height="694" fill="#ffffff" stroke="#222222" stroke-width="1"/>
  {text(1060, 151, 'LEGEND', 13, 700)}
  {legend_markup}
  {text(1060, 326, 'REVIEW NOTES', 13, 700)}
  {note_markup}
  {body}
  <line x1="72" y1="850" x2="1328" y2="850" stroke="#222222" stroke-width="1"/>
  {text(72, 876, 'JINGZHANG OPEN INTERFACE / CIVIC PROTOCOL MODERNISM', 12, 700)}
  {text(1328, 876, 'Not a statutory plan. Alignments and envelopes require official evidence.', 12, 400, '#555555', 'end')}
</svg>
'''


def map_svg(title, subtitle, features, notes, legend=None, outline_label=None):
    legend = legend or [
        ("physical design", "#202020", 5, ""),
        ("human/public route", "#008c99", 4, ""),
        ("service/resource", "#b14f77", 2, 'stroke-dasharray="9 6"'),
        ("schematic edge", "#76569b", 2, 'stroke-dasharray="3 6"'),
        ("background evidence", "#777777", 2, 'stroke-dasharray="5 4"'),
    ]
    active = [item for item in features if item.get("geometry") is not None]
    project = projector(feature_bounds(active))
    geometry_markup = "".join(render_geometry(item, project) for item in active)
    labels = []
    for item in active:
        geometry = item["geometry"]
        props = item.get("properties", {})
        if geometry["type"] != "Point":
            continue
        if props.get("semantic_class") not in {
            "ecosystem_node",
            "endpoint_gateway",
            "human_service_node",
            "endpoint_landmark",
            "human_review_gate",
            "non_digital_fallback",
        }:
            continue
        x, y = project(geometry["coordinates"])
        labels.append(text(x + 9, y - 8, item["id"], 10, 700, "#222222"))
    outline = ""
    if outline_label:
        outline = (
            f'<rect x="{MAP_LEFT}" y="{MAP_TOP}" width="{MAP_RIGHT - MAP_LEFT}" '
            f'height="{MAP_BOTTOM - MAP_TOP}" fill="none" stroke="#555555" stroke-width="1.5" '
            f'stroke-dasharray="8 6"/>'
            + text(MAP_LEFT + 10, MAP_TOP + 22, outline_label, 11, 700, "#555555")
        )
    north = (
        '<path d="M 974 164 L 984 194 L 974 188 L 964 194 Z" fill="#111111"/>'
        + text(974, 154, "N", 12, 700, "#111111", "middle")
    )
    body = f'<g>{outline}{geometry_markup}{"".join(labels)}{north}</g>'
    return svg_shell(title, subtitle, body, notes, legend)


def diagram_shell(title, subtitle, content, notes):
    legend = [
        ("public / access", "#008c99", 4, ""),
        ("human review", "#ef6c3e", 4, ""),
        ("bounded testing", "#e3bd25", 5, ""),
        ("commons / ecology", "#4d9a72", 5, ""),
        ("fixed civic frame", "#222222", 4, ""),
    ]
    return svg_shell(title, subtitle, content, notes, legend)


def sections_svg():
    panels = []
    section_data = [
        ("ZZY / CONTROLLED TEST YARD", ["ordinary path", "observation", "safety buffer", "test yard", "support"], ["#a7d8df", "#ef6c3e", "#f6e09a", "#f4cf4c", "#d7d8d5"]),
        ("ORG / POROUS COMMONS", ["research", "translation", "public commons", "prototype", "neighborhood"], ["#a7d8df", "#c8d9dc", "#8fc99d", "#e8a06f", "#b8d79e"]),
        ("DZS / URBAN SWITCHBOARD", ["appeal", "consent", "public switch", "adoption", "culture"], ["#efb7a2", "#ef6c3e", "#a7d8df", "#e8a06f", "#d4b5d8"]),
    ]
    for row, (label, zones, colors) in enumerate(section_data):
        y = 180 + row * 205
        panels.append(text(92, y, label, 15, 700))
        panels.append(f'<line x1="92" y1="{y + 102}" x2="970" y2="{y + 102}" stroke="#222" stroke-width="2"/>')
        for index, (zone, color) in enumerate(zip(zones, colors)):
            x = 92 + index * 176
            height = [54, 78, 40, 90, 62][index]
            panels.append(f'<rect x="{x}" y="{y + 102 - height}" width="166" height="{height}" fill="{color}" stroke="#222" stroke-width="1.5"/>')
            panels.append(text(x + 83, y + 128, zone, 12, 600, "#222", "middle"))
        panels.append(f'<line x1="92" y1="{y + 68}" x2="970" y2="{y + 68}" stroke="#008c99" stroke-width="4" stroke-dasharray="14 7"/>')
    notes = [
        "Relative envelopes only; no statutory height claim.",
        "Sections prove path, frontage, gradient, and fail-safe relationships.",
        "Existing ground levels and buildings require survey.",
        "All ordinary paths remain outside controlled test thresholds.",
        "DZS station relation is not represented as a physical section link.",
    ]
    return diagram_shell("SECTIONS / INTERFACE LOGIC", "Three endpoint transects, conceptual and not to construction scale", "".join(panels), notes)


def landmarks_svg(layers):
    panels = []
    landmarks = layers["landmarks"]["features"]
    for index, item in enumerate(landmarks):
        x = 92 + index * 300
        props = item["properties"]
        panels.append(text(x, 180, props["endpoint_identity"].upper(), 17, 700))
        panels.append(text(x, 205, item["id"], 11, 600, "#e6512e"))
        if props["endpoint"] == "ZZY":
            panels.append(f'<path d="M {x + 30} 530 L {x + 30} 275 L {x + 225} 275 L {x + 225} 530" fill="none" stroke="#222" stroke-width="12"/>')
            panels.append(f'<line x1="{x + 38}" y1="410" x2="{x + 217}" y2="410" stroke="#d52b2b" stroke-width="9"/>')
        elif props["endpoint"] == "ORG":
            panels.append(f'<path d="M {x + 75} 285 L {x + 25} 285 L {x + 25} 520 L {x + 75} 520" fill="none" stroke="#222" stroke-width="13"/>')
            panels.append(f'<path d="M {x + 180} 285 L {x + 230} 285 L {x + 230} 520 L {x + 180} 520" fill="none" stroke="#222" stroke-width="13"/>')
            panels.append(f'<line x1="{x + 30}" y1="402" x2="{x + 225}" y2="402" stroke="#008c99" stroke-width="5"/>')
        else:
            panels.append(f'<rect x="{x + 95}" y="280" width="70" height="240" fill="#222"/>')
            panels.append(f'<rect x="{x + 20}" y="370" width="220" height="55" fill="#a7d8df" stroke="#222" stroke-width="3"/>')
            panels.append(f'<line x1="{x + 130}" y1="300" x2="{x + 130}" y2="500" stroke="#ef6c3e" stroke-width="6"/>')
        panels.append(text(x, 574, props["role"], 12, 600))
        panels.append(text(x, 598, props["non_digital_state"], 11, 400, "#555"))
        panels.append(text(x, 622, props["nighttime_state"], 11, 400, "#555"))
        panels.append(text(x, 646, props["maintenance"], 11, 400, "#555"))
    notes = [
        "Three physically distinct forms correspond to endpoint identity.",
        "All retain legible non-digital states after power or network loss.",
        "Scale is relative design envelope, not statutory height.",
        "Night states are low-glare and carry no tracking or advertising.",
        "Forms use JZOI black, cyan, orange, green, and bounded-test yellow.",
    ]
    return diagram_shell("LANDMARK SYSTEM", "Safety Gantry / Open Bracket / Civic Switch", "".join(panels), notes)


def components_svg(layers):
    rows = []
    for index, item in enumerate(layers["components"]["features"]):
        y = 170 + index * 125
        props = item["properties"]
        rows.append(text(92, y, props["component_family"], 17, 700))
        rows.append(text(92, y + 24, props["dimensions_concept"], 11, 400, "#555"))
        rows.append(f'<line x1="360" y1="{y + 35}" x2="970" y2="{y + 35}" stroke="#222" stroke-width="2"/>')
        if props["component_family"] == "HUMAN-DESK":
            rows.append(f'<path d="M 510 {y + 32} L 510 {y - 25} L 740 {y - 25} L 740 {y + 32}" fill="none" stroke="#ef6c3e" stroke-width="7"/>')
        elif props["component_family"] == "TEST-RAIL":
            rows.append(f'<line x1="430" y1="{y}" x2="850" y2="{y}" stroke="#d52b2b" stroke-width="9"/>')
            rows.append(f'<line x1="450" y1="{y - 30}" x2="450" y2="{y + 34}" stroke="#222" stroke-width="5"/>')
            rows.append(f'<line x1="830" y1="{y - 30}" x2="830" y2="{y + 34}" stroke="#222" stroke-width="5"/>')
        else:
            rows.append(f'<rect x="590" y="{y - 42}" width="72" height="76" fill="#f7f6f2" stroke="#222" stroke-width="5"/>')
            rows.append(f'<line x1="603" y1="{y - 15}" x2="649" y2="{y - 15}" stroke="#008c99" stroke-width="4"/>')
        rows.append(text(760, y - 15, " / ".join(props["where_used"]), 11, 700, "#e6512e"))
        rows.append(text(760, y + 10, props["public_path_relationship"], 10, 400, "#555"))
    notes = [
        "Dimensions are conceptual and require detailed accessibility review.",
        "Components sit beside clear paths and cannot become ticketed choke points.",
        "Operational states remain legible without mandatory screens.",
        "Information hierarchy starts with purpose, stop/refusal, and human help.",
        "Scenario references are encoded in components.geojson.",
    ]
    return diagram_shell("COMPONENT SYSTEM", "Five spatial component families with clearance and operating logic", "".join(rows), notes)


def render_all(root=ROOT):
    root = Path(root)
    layers = load_layers(root)
    review = root / "review"
    review.mkdir(parents=True, exist_ok=True)
    common_legend = [
        ("MAIN-IF / physical", "#e6512e", 6, ""),
        ("PARALLEL-HUMAN", "#008c99", 4, 'stroke-dasharray="10 7"'),
        ("service/resource", "#b14f77", 2, 'stroke-dasharray="9 6"'),
        ("schematic ecosystem", "#76569b", 2, 'stroke-dasharray="3 6"'),
        ("background context", "#777777", 2, 'stroke-dasharray="5 4"'),
    ]
    outputs = {
        "overall_structure": map_svg(
            "43.6 KM2 REGIONAL / ECOSYSTEM STRUCTURE",
            "Three Areas + Two Wings; relationships are not roads",
            layers["regional_ecosystem"]["features"],
            [
                "Physical corridors use solid gray; resource links are dashed.",
                "All 25 accepted ecosystem edges remain DESIGN TARGET.",
                "Research anchors retain Gate A context confidence.",
                "Qinghe, Xiaoyuehe, and heritage are background relationships.",
                "No institutional agreement or local capacity is claimed.",
            ],
            common_legend,
            "PROVISIONAL 43.6 KM2 RESEARCH FRAME",
        ),
        "overall_masterplan": map_svg(
            "11.4 KM2 OVERALL URBAN DESIGN",
            "Civic Protocol Spine, distributed program mosaic, public stitches, and endpoint rooms",
            layers["land_use_program"]["features"] + layers["massing"]["features"] + layers["overall_structure"]["features"],
            [
                "18 program units replace four giant abstract bands.",
                "MAIN-IF bends through DZS, ORG, and ZZY public rooms.",
                "PARALLEL-HUMAN remains a connected staffed alternative.",
                "Massing envelopes are conceptual, not existing buildings.",
                "East-west stitches connect to the north-south spine.",
                "Parking remains UNKNOWN.",
            ],
            common_legend,
            "PROVISIONAL 11.4 KM2 OVERALL FRAME",
        ),
        "mobility": map_svg(
            "MOBILITY HIERARCHY",
            "Background road context, proposed streets, walking, cycling, logistics, and emergency access",
            layers["massing"]["features"] + layers["mobility"]["features"],
            [
                "Routes are separated by mode and operating responsibility.",
                "No proposed route crosses concept massing in semantic QA.",
                "Walking and cycling networks remain physically legible.",
                "DZS station relation is DATA GAP with null geometry.",
                "Road redlines, station entrances, and parking require evidence.",
            ],
            outline_label="PROVISIONAL OVERALL DESIGN FRAME",
        ),
        "blue_green_heritage": map_svg(
            "BLUE-GREEN + HERITAGE SYSTEM",
            "Background evidence and proposed rainwater/public-realm sequences remain distinct",
            layers["blue_green_heritage"]["features"] + layers["overall_structure"]["features"],
            [
                "Four frozen background references retain their evidence class.",
                "Nine proposed systems are non-statutory DESIGN TARGETS.",
                "Qinghe and Xiaoyuehe exact bank geometry remains unknown.",
                "Heritage sequence links public rooms without claiming protection lines.",
                "Rainwater functions remain low-tech first and manually operable.",
            ],
            outline_label="BACKGROUND EVIDENCE + PROPOSED SYSTEM",
        ),
        "zzy_plan": map_svg(
            "ZZY / CONTROLLED TEST YARD",
            "Public bypass, observation, safety gradient, controlled testing, ecology, and physical stop",
            layers["zzy_plan"]["features"] + [layers["landmarks"]["features"][0]],
            [
                "Ordinary pedestrian movement bypasses controlled testing.",
                "Cycle test loop is geometrically closed.",
                "Observation and Human Review Gate face the test boundary.",
                "TEST-RAIL provides a power-independent emergency stop.",
                "Qinghe relation is background only; rain garden is proposed.",
            ],
            outline_label="PROVISIONAL KEY-AREA GEOMETRY / NOT PARCEL EDGE",
        ),
        "org_plan": map_svg(
            "ORG / POROUS COMMONS",
            "Research to translation to prototype across a four-direction public permeability lattice",
            layers["org_plan"]["features"] + [layers["landmarks"]["features"][1]],
            [
                "Four-direction paths converge on the Open Bracket commons.",
                "Research, translation, prototype, and startup remain distinct.",
                "Neighborhood and talent services anchor the public edge.",
                "Active ground floors face commons and permeability routes.",
                "Campus/station relationships remain design intent where unverified.",
            ],
            outline_label="PROVISIONAL KEY-AREA GEOMETRY / NOT PARCEL EDGE",
        ),
        "dzs_plan": map_svg(
            "DZS / URBAN SWITCHBOARD",
            "Consent, appeal, adoption, enterprise, culture, talent, and non-digital fallback",
            layers["dzs_plan"]["features"] + [layers["landmarks"]["features"][2]],
            [
                "Pedestrian convergence organizes the provisional key area.",
                "Consent and appeal remain visible civic rooms.",
                "Civic Switch combines service orientation and cultural identity.",
                "No station entrance or physical station link is invented.",
                "Station relationship remains an unresolved interface condition.",
            ],
            outline_label="PROVISIONAL KEY-AREA GEOMETRY / STATION RELATION UNRESOLVED",
        ),
        "sections": sections_svg(),
        "massing": map_svg(
            "MASSING + FRONTAGE STRATEGY",
            "Concept buildings, public gaps, active ground floors, and relative hierarchy",
            layers["land_use_program"]["features"] + layers["massing"]["features"] + layers["overall_structure"]["features"],
            [
                "18 concept envelopes frame public routes without collisions.",
                "Low, medium, tall, and landmark are relative hierarchies.",
                "No object is labelled retained or renovated.",
                "Courtyard and chamfered footprints preserve permeability.",
                "Statutory height, FAR, ownership, and existing condition are unknown.",
            ],
            outline_label="RELATIVE DESIGN ENVELOPES / NON-STATUTORY",
        ),
        "landmarks": landmarks_svg(layers),
        "components": components_svg(layers),
    }
    paths = []
    for stem, content in outputs.items():
        path = review / f"{stem}.svg"
        path.write_text(content, encoding="utf-8")
        paths.append(path)
    return paths


if __name__ == "__main__":
    generated = render_all()
    print(json.dumps({"generated": [str(path.relative_to(ROOT)) for path in generated]}, indent=2))
