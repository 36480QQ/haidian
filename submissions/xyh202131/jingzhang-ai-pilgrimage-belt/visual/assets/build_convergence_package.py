#!/usr/bin/env python3
"""Build the Round 58 human-facing convergence package deterministically.

Contributor-owned code is MIT licensed. Generated editorial artifacts are
covered by the package's CC BY 4.0 content notice. No network or model call is
made. Geometry and metrics are read but never modified.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
from typing import Any

import fitz
from PIL import Image
from fontTools import subset
from fontTools.ttLib import TTFont


ROOT = pathlib.Path(__file__).resolve().parents[2]
REPO = ROOT.parents[2]
FIG = ROOT / "assets" / "figures"
VISUAL = ROOT / "visual"
ASSETS = VISUAL / "assets"
DRAWINGS = ROOT / "drawings"
CHROME = pathlib.Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
FONT = pathlib.Path(r"C:\Windows\Fonts\Noto Sans SC (TrueType).otf")
PDF_FONT = pathlib.Path(tempfile.gettempdir()) / "jz-r58-NotoSansSC-subset.otf"
NAVY = "#102d46"
INK = "#17364d"
TEAL = "#00856f"
BLUE = "#1681aa"
AMBER = "#bd7700"
CORAL = "#e85c42"
PAPER = "#f4f0e7"
MUTED = "#647786"


def write_text(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.replace("\r\n", "\n"), encoding="utf-8", newline="\n")


def write_json(path: pathlib.Path, data: Any) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def read_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare_pdf_font() -> None:
    if not FONT.exists():
        raise RuntimeError(f"Noto Sans SC source font not found: {FONT}")
    corpus = (
        (ROOT / "proposal.md").read_text(encoding="utf-8")
        + (ROOT / "proposal.en.md").read_text(encoding="utf-8")
        + "TWIN-TRACK JING-ZHANG G0 PROVISIONAL NOT TO SCALE NOT APPROVED CC BY MIT ODbL 0123456789 / · × -"
    )
    options = subset.Options()
    options.name_IDs = [0, 1, 2, 3, 4, 5, 6, 13, 14]
    options.name_legacy = True
    options.name_languages = [0x409, 0x804]
    # PyMuPDF addresses CJK glyphs through the source font's glyph IDs when
    # embedding text. Preserve those IDs in the subset; compacting them makes
    # the PDF render valid-but-wrong characters in headers and footers.
    options.retain_gids = True
    options.recalc_bounds = True
    options.recalc_timestamp = False
    font = TTFont(FONT, recalcTimestamp=False)
    sub = subset.Subsetter(options=options)
    sub.populate(text="".join(sorted(set(corpus))))
    sub.subset(font)
    font.save(PDF_FONT, reorderTables=True)


def remove_values(value: Any, banned: set[str]) -> Any:
    if isinstance(value, list):
        return [remove_values(v, banned) for v in value if not (isinstance(v, str) and v in banned)]
    if isinstance(value, dict):
        return {k: remove_values(v, banned) for k, v in value.items()}
    return value


def update_source_governance() -> None:
    central = read_json(REPO / "data" / "source_registry.json")["sources"]
    central_by_id = {row["source_id"]: row for row in central}
    package = read_json(ROOT / "sources.json")
    removed_ids = {
        "SOURCE-JZ-ORDINARY-LIFE-MEDIA-REGISTER-R12",
        "SOURCE-ORDINARY-LIFE-MEDIA-R12",
        "SOURCE-JZ-REVIEW-WALK-R14",
    }
    removed_paths = {
        "visual/assets/ordinary-life-media-register.json",
        "visual/assets/jury-motion-journey.json",
        "assets/media/ordinary-life-scenes.md",
        "assets/media/ordinary-life-scenes.webp",
        "assets/media/twin-track-cover.webp",
        "assets/media/4-state-motion.mp4",
        "assets/media/4-state-motion-poster.webp",
        "assets/media/4-state-narration.mp3",
        "assets/media/4-state-narration.vtt",
        "assets/media/4-state-narration.en.vtt",
        "assets/media/4-state-narration-script.md",
    }
    package["sources"] = [s for s in package["sources"] if s["id"] not in removed_ids]
    package["rights_evidence_contract"] = {
        "instance": "visual/assets/source-governance-register.json",
        "asset_ledger": "visual/assets/rights-clearance-ledger.json",
        "status": "component_licenses_declared",
        "content_license": "CC-BY-4.0",
        "code_license": "MIT",
        "osm_database_license": "ODbL-1.0",
    }
    central_alias = {
        "AGENT-TASKBOOK": "DATA-SRC-AGENT-TASKBOOK-20260518",
        "STD-URBAN-DESIGN": "DATA-SRC-MOHURD-URBAN-DESIGN-MEASURES",
        "STD-CONTROL-PLAN": "DATA-SRC-MOHURD-CONTROL-DETAILED-PLANNING",
        "STD-LAND-USE": "DATA-SRC-MNR-LAND-USE-CLASSIFICATION-202311",
    }
    records = []
    for source in package["sources"]:
        sid = source["id"]
        central_id = sid if sid in central_by_id else central_alias.get(sid)
        authority = source.get("authority_level", "")
        stype = source.get("source_type", "")
        if central_id:
            c = central_by_id[central_id]
            use = c.get("usable_for_formal")
            status = (
                "central_approved_formal"
                if use == "yes"
                else "central_provisional_only"
                if use == "provisional_only"
                else "central_background_only"
            )
            claim_capacity = (
                "formal_claim_within_registered_scope"
                if use == "yes"
                else "provisional_geometry_only"
                if use == "provisional_only"
                else "background_context_only"
            )
        elif authority == "submission_author" or stype.startswith("package_") or stype.startswith("in_package") or stype in {"conceptual_proposal", "generated_figure"}:
            status = "package_authored_evidence"
            claim_capacity = "proposal_method_or_design_intent_only"
        elif sid == "OSM-CONTEXT":
            status = "external_open_database"
            claim_capacity = "directional_context_only_not_formal_boundary"
        else:
            status = "participant_collected_citation"
            claim_capacity = "bounded_background_or_case_comparison_only"
        if status == "package_authored_evidence":
            source["license"] = "CC-BY-4.0"
            source["rights_or_reuse"] = "contributor_owned_content_CC_BY_4_0; does not upgrade factual authority or maturity"
        records.append(
            {
                "source_id": sid,
                "central_registry_id": central_id,
                "governance_status": status,
                "claim_capacity": claim_capacity,
                "authority_level": authority,
                "redistributed_third_party_media": False,
                "review_rule": "Use only within the source record's stated scope, date, authority and limitations.",
            }
        )
    write_json(ROOT / "sources.json", package)
    write_json(
        ASSETS / "source-governance-register.json",
        {
            "schema_version": "1.0",
            "as_of": "2026-08-24",
            "central_registry_snapshot_count": len(central),
            "package_source_count": len(records),
            "method_zh": "中央登记只决定中央来源状态；投稿方自采与自编来源保持包内身份，不因公开或较新自动升级为正式依据。",
            "method_en": "The central registry governs central-source status only. Participant-collected and package-authored sources retain package-local status and are never upgraded merely for being public or recent.",
            "records": records,
        },
    )
    write_json(
        ASSETS / "source-rights-evidence.json",
        {
            "schema_version": "2.0",
            "as_of": "2026-08-24",
            "source_record_count": len(records),
            "third_party_media_redistributed": 0,
            "generated_media_paths": 0,
            "component_notices": [
                "LICENSE-CONTENT-CC-BY-4.0.md",
                "LICENSE-CODE-MIT.md",
                "NOTICE-DATA-ODBL.md",
            ],
            "source_records": [
                {
                    "source_id": r["source_id"],
                    "governance_status": r["governance_status"],
                    "claim_capacity": r["claim_capacity"],
                    "rights_use": "citation_only" if "citation" in r["governance_status"] else "see_component_notice",
                }
                for r in records
            ],
        },
    )
    for name in ["compliance_matrix.json", "standard_matrix.json", "design_depth_matrix.json"]:
        path = ROOT / name
        matrix = remove_values(read_json(path), removed_ids | removed_paths)
        if name == "compliance_matrix.json":
            matrix.pop("round_14_review_entry", None)
        write_json(path, matrix)


def write_handoff_candidate() -> None:
    write_json(
        ASSETS / "professional-handoff-candidate.json",
        {
            "schema_version": "1.0",
            "candidate_id": "PRE-G1-JZ05-SCENE011-T02",
            "status": "g0_no_go_professional_review_candidate",
            "selection_reason_zh": "唯一同时具有来源边界、拒答、停止、人工交接、恢复和无 PII 合成回放的既有对象组合；选择不代表成熟度更高。",
            "selection_reason_en": "The sole existing combination with source boundaries, refusal, stop, staffed handoff, recovery and PII-free synthetic replay; selection does not imply greater maturity.",
            "existing_objects": {
                "renewal_project": "JZ-05",
                "scenario": "SCENE-011",
                "protocol": "T-02",
                "key_area": "PROV-KEY-003",
            },
            "current_evidence": {
                "fixed_questions": 5,
                "synthetic_replay_cases": 10,
                "exact_decision_matches": 10,
                "stop_recovery_branches": 4,
                "network_calls": 0,
                "model_calls": 0,
                "real_service_interactions": 0,
                "field_tests": 0,
            },
            "blocking_handoff_items": [
                "H01 accountable-party acceptance",
                "H02 approved site, scope and time",
                "H03 field ordinary-task and non-AI baseline",
                "H04 data-security and prohibited-data review",
                "H05 stop, staffed takeover and recovery acceptance",
                "H06 accessibility and community parity co-test",
                "H07 independent retest and signed GO/NO-GO decision",
            ],
            "decision_rule": "Any missing, rejected or expired H01-H07 item keeps the candidate at G0 / NO-GO.",
            "non_equivalence": "Professional review candidate is not a pilot application, approval, procurement, deployment, field result, recovery duration or G1.",
        },
    )


def svg_document(title: str, eyebrow: str, body: str, footer: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1100" viewBox="0 0 1800 1100">
<rect width="1800" height="1100" fill="{PAPER}"/>
<rect width="1800" height="142" fill="{NAVY}"/>
<text x="56" y="52" fill="#ffc21a" font-family="Noto Sans SC, sans-serif" font-size="20" font-weight="700" letter-spacing="2">{html.escape(eyebrow)}</text>
<text x="56" y="108" fill="#ffffff" font-family="Noto Sans SC, sans-serif" font-size="42" font-weight="700">{html.escape(title)}</text>
{body}
<rect x="48" y="1016" width="1704" height="52" rx="20" fill="{NAVY}"/>
<text x="900" y="1050" text-anchor="middle" fill="#ffffff" font-family="Noto Sans SC, sans-serif" font-size="17">{html.escape(footer)}</text>
</svg>'''


def ordinary_svg(en: bool) -> str:
    places = [
        ("01 VERIFY · ZHONGZHIYUAN" if en else "01 验证 · 众智园", "PARALLEL BYPASS" if en else "平行绕行", BLUE),
        ("02 CO-CREATE · ORIGIN" if en else "02 共创 · 原点社区", "STREET + TWO COURTS" if en else "一街两院", AMBER),
        ("03 PUBLISH · DAZHONGSI" if en else "03 发布 · 大钟寺", "FOUR-WAY COMMUTE" if en else "四向通勤", CORAL),
    ]
    steps = ["ENTER", "READ", "STAFFED TASK", "CORRECT / EXIT"] if en else ["进入", "理解", "人工任务", "纠错 / 退出"]
    rows = []
    for i, (place, relation, color) in enumerate(places):
        y = 214 + i * 252
        rows.append(f'<text x="70" y="{y}" fill="{color}" font-family="Noto Sans SC, sans-serif" font-size="22" font-weight="700">{place}</text>')
        rows.append(f'<text x="70" y="{y+36}" fill="{INK}" font-family="Noto Sans SC, sans-serif" font-size="28" font-weight="700">{relation}</text>')
        x0 = 430
        for j, step in enumerate(steps):
            x = x0 + j * 285
            rows.append(f'<circle cx="{x}" cy="{y+28}" r="31" fill="#ffffff" stroke="{TEAL}" stroke-width="5"/>')
            rows.append(f'<text x="{x}" y="{y+35}" text-anchor="middle" fill="{INK}" font-family="Noto Sans SC, sans-serif" font-size="15" font-weight="700">{j+1}</text>')
            rows.append(f'<text x="{x}" y="{y+91}" text-anchor="middle" fill="{INK}" font-family="Noto Sans SC, sans-serif" font-size="18">{step}</text>')
            if j < 3:
                rows.append(f'<line x1="{x+36}" y1="{y+28}" x2="{x+249}" y2="{y+28}" stroke="{TEAL}" stroke-width="12" stroke-linecap="round"/>')
        rows.append(f'<rect x="1510" y="{y-16}" width="210" height="92" rx="18" fill="#fff" stroke="{color}" stroke-width="3" stroke-dasharray="10 8"/>')
        rows.append(f'<text x="1615" y="{y+17}" text-anchor="middle" fill="{color}" font-family="Noto Sans SC, sans-serif" font-size="17" font-weight="700">{"OPTIONAL G0" if en else "旁侧 G0"}</text>')
        rows.append(f'<text x="1615" y="{y+49}" text-anchor="middle" fill="{MUTED}" font-family="Noto Sans SC, sans-serif" font-size="15">{"STOPPABLE" if en else "可停止 / 可撤除"}</text>')
    title = "One ordinary task remains complete in every place" if en else "同一普通任务，在三处都必须完整"
    footer = "G0 concept · non-AI path first · no account / device required · not field evidence or an accessibility result" if en else "G0 概念 · 非 AI 路径优先 · 不要求账户或设备 · 非现场证据、非无障碍结果"
    return svg_document(title, "S05 / HUMAN-SCALE ORDINARY LIFE" if en else "S05 / 人尺度普通生活", "".join(rows), footer)


def state_svg(en: bool) -> str:
    names = ["ORDINARY", "VERIFY", "FAULT", "RECOVER"] if en else ["普通", "验证", "故障", "恢复"]
    desc = (
        ["task works first", "bounded overlay", "stop overlay only", "return ground, then recheck"]
        if en
        else ["普通任务先成立", "限域叠层出现", "只停验证对象", "先还场，再复核"]
    )
    colors = [TEAL, BLUE, CORAL, AMBER]
    body = []
    for i, (name, note, color) in enumerate(zip(names, desc, colors)):
        x = 70 + i * 430
        body.append(f'<rect x="{x}" y="265" width="360" height="470" rx="30" fill="#ffffff" stroke="{color}" stroke-width="5"/>')
        body.append(f'<circle cx="{x+72}" cy="337" r="34" fill="{color}"/><text x="{x+72}" y="346" text-anchor="middle" fill="#fff" font-family="Noto Sans SC, sans-serif" font-size="23" font-weight="700">{i+1}</text>')
        body.append(f'<text x="{x+42}" y="426" fill="{INK}" font-family="Noto Sans SC, sans-serif" font-size="34" font-weight="700">{name}</text>')
        body.append(f'<text x="{x+42}" y="474" fill="{MUTED}" font-family="Noto Sans SC, sans-serif" font-size="20">{note}</text>')
        body.append(f'<line x1="{x+42}" y1="560" x2="{x+318}" y2="560" stroke="{TEAL}" stroke-width="18" stroke-linecap="round"/>')
        if i == 1:
            body.append(f'<line x1="{x+110}" y1="620" x2="{x+250}" y2="620" stroke="{BLUE}" stroke-width="12" stroke-dasharray="18 12"/>')
        elif i == 2:
            body.append(f'<line x1="{x+110}" y1="620" x2="{x+250}" y2="620" stroke="{CORAL}" stroke-width="12" stroke-dasharray="8 10"/>')
            body.append(f'<path d="M{x+170} 590 l45 60 M{x+215} 590 l-45 60" stroke="{CORAL}" stroke-width="8"/>')
        elif i == 3:
            body.append(f'<path d="M{x+115} 630 C{x+160} 585 {x+230} 585 {x+275} 630" fill="none" stroke="{AMBER}" stroke-width="10"/>')
        body.append(f'<text x="{x+180}" y="694" text-anchor="middle" fill="{TEAL}" font-family="Noto Sans SC, sans-serif" font-size="16" font-weight="700">{"ORDINARY TASK CONTINUES" if en else "普通任务持续"}</text>')
        if i < 3:
            body.append(f'<path d="M{x+370} 500 h50 l-18 -18 m18 18 l-18 18" fill="none" stroke="{MUTED}" stroke-width="5"/>')
    body.append(f'<rect x="250" y="800" width="1300" height="104" rx="24" fill="#fff5df" stroke="{AMBER}" stroke-width="3"/>')
    msg = "Recovery is not authorization, approval, restart, a duration claim, or G1." if en else "恢复不等于授权、批准、重启、现实恢复时长或 G1。"
    body.append(f'<text x="900" y="862" text-anchor="middle" fill="{INK}" font-family="Noto Sans SC, sans-serif" font-size="28" font-weight="700">{msg}</text>')
    title = "Ordinary - Verify - Fault - Recover" if en else "普通—验证—故障—恢复：只改变验证叠层"
    footer = "Static sequence, not elapsed time · complete non-AI path and staffed handoff remain" if en else "静态顺序，不表示经过时长 · 完整非 AI 路径与人工交接始终保留"
    return svg_document(title, "S06 / FOUR-STATE JOURNEY" if en else "S06 / 四态旅程", "".join(body), footer)


def handoff_svg(en: bool) -> str:
    title = "One object for professional review, seven gates still closed" if en else "只交一个专业核验对象，七个现实门仍关闭"
    body = []
    body.append(f'<rect x="60" y="205" width="520" height="700" rx="28" fill="#ffffff" stroke="{BLUE}" stroke-width="4"/>')
    body.append(f'<text x="100" y="265" fill="{BLUE}" font-family="Noto Sans SC, sans-serif" font-size="20" font-weight="700">PRE-G1 CANDIDATE</text>')
    body.append(f'<text x="100" y="325" fill="{INK}" font-family="Noto Sans SC, sans-serif" font-size="35" font-weight="700">JZ-05 × SCENE-011 × T-02</text>')
    checks = (["5 bounded questions", "10/10 synthetic decisions", "4/4 stop-recovery branches", "0 model / API / real service"] if en else ["5 个来源边界问题", "10/10 合成决策匹配", "4/4 停止—恢复分支", "模型 / API / 现实服务均为 0"])
    for i, t in enumerate(checks):
        y = 410 + i * 82
        body.append(f'<circle cx="112" cy="{y}" r="15" fill="{TEAL}"/><path d="M104 {y} l7 8 l15 -19" fill="none" stroke="#fff" stroke-width="4"/>')
        body.append(f'<text x="145" y="{y+8}" fill="{INK}" font-family="Noto Sans SC, sans-serif" font-size="23">{t}</text>')
    body.append(f'<rect x="100" y="760" width="440" height="92" rx="20" fill="#fee5de" stroke="{CORAL}" stroke-width="3"/>')
    body.append(f'<text x="320" y="815" text-anchor="middle" fill="{CORAL}" font-family="Noto Sans SC, sans-serif" font-size="26" font-weight="700">G0 / NO-GO</text>')
    gates = ["H01 OWNER", "H02 SCOPE", "H03 BASELINE", "H04 DATA", "H05 RECOVERY", "H06 PARITY", "H07 RETEST"] if en else ["H01 接责", "H02 范围", "H03 基线", "H04 数据", "H05 恢复", "H06 同权", "H07 复测"]
    for i, gate in enumerate(gates):
        col = i % 2
        row = i // 2
        x = 650 + col * 500
        y = 220 + row * 170
        body.append(f'<rect x="{x}" y="{y}" width="430" height="126" rx="22" fill="#ffffff" stroke="{CORAL}" stroke-width="3"/>')
        body.append(f'<text x="{x+28}" y="{y+48}" fill="{CORAL}" font-family="Noto Sans SC, sans-serif" font-size="22" font-weight="700">{gate}</text>')
        note = "missing / unaccepted" if en else "缺失 / 未接受"
        body.append(f'<text x="{x+28}" y="{y+87}" fill="{MUTED}" font-family="Noto Sans SC, sans-serif" font-size="19">{note}</text>')
        body.append(f'<circle cx="{x+382}" cy="{y+63}" r="17" fill="none" stroke="{CORAL}" stroke-width="4"/><path d="M{x+371} {y+52} l22 22 M{x+393} {y+52} l-22 22" stroke="{CORAL}" stroke-width="4"/>')
    footer = "Candidate means next review object only · no pilot, approval, procurement, field result, recovery time or G1" if en else "候选只表示下一步核验对象 · 非试点、批准、采购、现场结果、恢复时长或 G1"
    return svg_document(title, "E01 / PROFESSIONAL HANDOFF" if en else "E01 / 专业交接", "".join(body), footer)


def render_svg(svg_path: pathlib.Path, png_path: pathlib.Path) -> None:
    if not CHROME.exists():
        raise RuntimeError(f"Chrome not found: {CHROME}")
    uri = svg_path.resolve().as_uri()
    with tempfile.TemporaryDirectory(prefix="jz-r58-chrome-") as tmp:
        cmd = [
            str(CHROME),
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--user-data-dir={tmp}",
            "--window-size=1800,1100",
            f"--screenshot={png_path.resolve()}",
            uri,
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with Image.open(png_path) as image:
        rgb = image.convert("RGB")
        rgb.save(png_path, format="PNG", optimize=True, compress_level=9)


def build_figures() -> None:
    pairs = [
        ("ordinary-life-journey", ordinary_svg(False), ordinary_svg(True)),
        ("four-state-journey", state_svg(False), state_svg(True)),
        ("review-professional-handoff", handoff_svg(False), handoff_svg(True)),
    ]
    for stem, zh, en in pairs:
        for suffix, source in [("", zh), (".en", en)]:
            svg = FIG / f"{stem}{suffix}.svg"
            png = FIG / f"{stem}{suffix}.png"
            write_text(svg, source)
            render_svg(svg, png)


def visual_html(en: bool) -> str:
    lang = "en" if en else "zh"
    suffix = ".en" if en else ""
    t = {
        "title": "Twin-Track Jing-Zhang | Review edition" if en else "双轨京张｜终稿评审版",
        "hero": "Ordinary ground first. Verification steps aside." if en else "普通地面先连续，验证退到旁侧。",
        "sub": "One concept · three non-interchangeable prototypes · one G0 handoff candidate" if en else "一个总纲 · 三种不可互换原型 · 一个 G0 专业交接候选",
        "nav": ["Decision", "Three places", "Four states", "Ordinary life", "Handoff", "Evidence"] if en else ["空间裁决", "三处原型", "四态旅程", "普通生活", "专业交接", "证据边界"],
        "heads": [
            "30 seconds: the spatial decision",
            "Three places cannot exchange answers",
            "3 minutes: ordinary - verify - fault - recover",
            "One complete non-AI task in every state",
            "One pre-G1 review candidate, still NO-GO",
            "15 minutes: trace claim, evidence, rights and veto",
        ] if en else [
            "30 秒：先看空间裁决",
            "三处不看标题也不能互换",
            "3 分钟：普通—验证—故障—恢复",
            "所有状态下，非 AI 同任务都完整",
            "只交一个 pre-G1 核验候选，仍是 NO-GO",
            "15 分钟：追到证据、权利与专业否决",
        ],
        "boundary": "G0 concept · provisional rough geometry · not approved · no field test · zero real-world results" if en else "G0 概念 · 临时粗略几何 · 非批准 · 未现场测试 · 现实结果 0",
    }
    image_stems = ["site-overview", "key-areas", "four-state-journey", "ordinary-life-journey", "review-professional-handoff"]
    sections = []
    for i, stem in enumerate(image_stems):
        sections.append(f'''<section id="s{i+1}" class="panel"><div class="copy"><span class="step">0{i+1}</span><h2>{html.escape(t["heads"][i])}</h2></div><img src="../assets/figures/{stem}{suffix}.png" alt="{html.escape(t["heads"][i])}"></section>''')
    evidence_title = t["heads"][5]
    evidence_body = (
        "Geometry and metrics remain frozen. Contributor content is CC BY 4.0, code MIT, OSM derivatives ODbL. H01-H07, official boundaries, approvals, field results and accepted professional duties remain absent."
        if en
        else "geometry 与 metrics 保持冻结。投稿方内容 CC BY 4.0、代码 MIT、OSM 衍生层 ODbL。H01—H07、官方边界、批准、现场结果和专业接责仍未提供。"
    )
    links = [
        ("proposal.en.md" if en else "proposal.md", "Proposal" if en else "正文"),
        ("metrics.json", "Metrics" if en else "指标"),
        ("sources.json", "Sources" if en else "来源"),
        ("visual/assets/source-governance-register.json", "Source governance" if en else "来源治理"),
        ("visual/assets/professional-handoff-candidate.json", "Handoff candidate" if en else "交接候选"),
        ("report/copyright_statement.md", "Rights" if en else "权利"),
    ]
    link_html = "".join(f'<a href="../{p}">{label}</a>' for p, label in links)
    coverage = (
        ["Overview map", "Three-level scope", "Key areas", "Land-use zoning", "Mobility", "Blue-green public space", "Architecture", "Renewal projects", "AI scenarios", "Core metrics", "Task coverage", "Self-check status", "Assumptions"]
        if en
        else ["总览地图", "三层范围", "重点区域", "用地分区", "交通慢行", "蓝绿公共空间", "建筑", "更新项目", "AI 场景", "核心指标", "任务覆盖", "自检状态", "假设"]
    )
    coverage_html = "".join(f'<li>{html.escape(item)}</li>' for item in coverage)
    return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(t["title"])}</title>
<style>
:root{{--navy:{NAVY};--ink:{INK};--teal:{TEAL};--blue:{BLUE};--amber:{AMBER};--coral:{CORAL};--paper:{PAPER};--muted:{MUTED}}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--paper);color:var(--ink);font-family:"Noto Sans SC","Noto Sans CJK SC","Source Han Sans SC",system-ui,sans-serif;line-height:1.55}}
a{{color:inherit}}.hero{{min-height:76vh;padding:clamp(32px,7vw,110px);display:grid;align-content:center;background:var(--navy);color:#fff;position:relative;overflow:hidden}}
.hero:after{{content:"";position:absolute;width:62vw;height:62vw;border:2px dashed #36a5c5;border-radius:50%;right:-22vw;top:-28vw;opacity:.5}}
.eyebrow{{color:#ffc21a;letter-spacing:.18em;font-weight:800}}h1{{font-size:clamp(44px,7vw,108px);line-height:1.02;max-width:1100px;margin:.25em 0}}.hero p{{font-size:clamp(18px,2vw,30px);max-width:900px}}
.status{{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}}.status span{{border:1px solid #7bb7c9;border-radius:999px;padding:8px 14px}}
nav{{position:sticky;top:0;z-index:10;display:flex;overflow:auto;gap:8px;padding:12px clamp(18px,5vw,72px);background:#fffdf8ee;backdrop-filter:blur(12px);border-bottom:1px solid #ccd4d7}}nav a{{white-space:nowrap;text-decoration:none;padding:9px 14px;border-radius:999px}}nav a:hover,nav a:focus{{background:#dcefe9;outline:2px solid var(--teal)}}
main{{max-width:1600px;margin:auto;padding:30px clamp(18px,4vw,64px) 90px}}.panel{{background:#fff;border:1px solid #c8d2d6;border-radius:26px;margin:28px 0;padding:clamp(18px,3vw,44px);box-shadow:0 14px 45px #102d4612}}
.copy{{display:flex;gap:18px;align-items:start}}.step{{font-size:20px;color:var(--coral);font-weight:800}}h2{{font-size:clamp(26px,3.5vw,52px);line-height:1.16;margin:0 0 24px}}img{{display:block;width:100%;height:auto;border-radius:16px;border:1px solid #cad3d7}}
.metrics{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:24px 0}}.metric{{background:#e8f3ef;border-radius:18px;padding:22px}}.metric strong{{display:block;font-size:clamp(25px,3vw,42px)}}.coverage{{display:flex;flex-wrap:wrap;gap:9px;padding:0;list-style:none}}.coverage li{{border-left:4px solid var(--teal);background:#edf4f2;padding:8px 12px;border-radius:5px}}.links{{display:flex;flex-wrap:wrap;gap:10px}}.links a{{padding:11px 15px;border:1px solid var(--blue);border-radius:12px;text-decoration:none;background:#fff}}footer{{background:var(--navy);color:#fff;padding:30px clamp(18px,5vw,72px)}}
@media(max-width:760px){{.hero{{min-height:62vh}}.metrics{{grid-template-columns:1fr}}.panel{{border-radius:16px}}}}
@media(prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}*{{animation:none!important;transition:none!important}}}}
@media print{{nav{{display:none}}.hero{{min-height:auto;break-after:page}}.panel{{box-shadow:none;break-inside:avoid}}}}
</style></head><body>
<header class="hero"><div><div class="eyebrow">TWIN-TRACK JING-ZHANG · R58</div><h1>{html.escape(t["hero"])}</h1><p>{html.escape(t["sub"])}</p><div class="status"><span>{html.escape(t["boundary"])}</span><span>12 / 8 / 3 / 36</span><span>CC BY 4.0 · MIT · ODbL</span></div></div></header>
<nav aria-label="{'Primary navigation' if en else '主导航'}">{''.join(f'<a href="#s{i+1}">{html.escape(label)}</a>' for i,label in enumerate(t["nav"]))}</nav>
<main>{''.join(sections)}
<section id="s6" class="panel"><div class="copy"><span class="step">06</span><h2>{html.escape(evidence_title)}</h2></div><p>{html.escape(evidence_body)}</p>
<div class="metrics"><div class="metric"><span>{'Provisional site model' if en else '临时场地模型'}</span><strong data-metric="site_area_sqm" data-value="11412825.385554">11.41 km²</strong></div><div class="metric"><span>{'Green ratio' if en else '绿地比例'}</span><strong data-metric="green_ratio" data-value="0.126157">12.62%</strong></div><div class="metric"><span>{'Public-space ratio' if en else '公共空间比例'}</span><strong data-metric="public_space_ratio" data-value="0.012831">1.28%</strong></div></div>
<h3>{'Task coverage' if en else '任务覆盖'}</h3><ul class="coverage">{coverage_html}</ul>
<div class="links">{link_html}</div></section></main>
<footer>{html.escape(t["boundary"])} · © OpenStreetMap contributors where applicable · {'No JavaScript or remote dependency' if en else '无 JavaScript、无远程依赖'}</footer>
</body></html>'''


def build_visual() -> None:
    write_text(VISUAL / "index.html", visual_html(False))
    write_text(VISUAL / "index.en.html", visual_html(True))


def add_text(page: fitz.Page, rect: fitz.Rect, text: str, size: float, color: tuple[float, float, float], bold: bool = False, align: int = 0) -> None:
    fontname = "NotoBold" if bold else "Noto"
    page.insert_font(fontname=fontname, fontfile=str(PDF_FONT))
    page.insert_textbox(rect, text, fontname=fontname, fontsize=size, color=color, align=align, lineheight=1.25)


def rgb(hex_value: str) -> tuple[float, float, float]:
    h = hex_value.lstrip("#")
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))


def make_pdf(path: pathlib.Path, en: bool, a0: bool) -> None:
    page_size = (3370.4, 2383.9) if a0 else (1190.6, 841.9)
    count = 8 if a0 else 14
    suffix = ".en" if en else ""
    page_specs = [
        ("Twin-Track Jing-Zhang" if en else "双轨京张", "Ordinary ground first; verification steps aside" if en else "普通地面先连续，验证退到旁侧", "site-overview"),
        ("One spatial decision" if en else "一次空间裁决", "Three non-interchangeable answers" if en else "三处给出不可互换的空间答案", "key-areas"),
        ("Three sections" if en else "三处剖面", "Ground floor, handoff and failure scope" if en else "首层、人工交接与故障范围", "key-area-sections"),
        ("Ordinary life" if en else "普通生活", "Complete non-AI task in every place" if en else "三处均保留完整非 AI 同任务", "ordinary-life-journey"),
        ("Four states" if en else "四态旅程", "Failure stops only the optional overlay" if en else "故障只停止可选验证叠层", "four-state-journey"),
        ("Land-use structure" if en else "用地结构", "Conceptual partition; not statutory control" if en else "概念分区，不是法定控制", "land-use-structure"),
        ("Mobility and blue-green" if en else "交通与蓝绿", "Continuity before technology" if en else "连续性先于技术叠加", "mobility-bluegreen"),
        ("Evidence and metrics" if en else "指标与证据", "Provisional values remain recomputable" if en else "临时指标仍可复算", "metrics-evidence"),
        ("Professional handoff" if en else "专业交接", "JZ-05 × SCENE-011 × T-02 remains G0 / NO-GO" if en else "JZ-05 × SCENE-011 × T-02 仍为 G0 / NO-GO", "review-professional-handoff"),
    ]
    if not a0:
        page_specs += [
            ("Public right" if en else "公共权利", "No account, device or automated decision required" if en else "不要求账户、设备或自动判断", "ordinary-life-journey"),
            ("Stop line" if en else "停止线", "H01-H07 must all be accepted" if en else "H01—H07 必须全部真实接受", "review-professional-handoff"),
            ("Source governance" if en else "来源治理", "Central, participant-collected and package-authored sources stay distinct" if en else "中央、自采与自编来源不混级", "metrics-evidence"),
            ("Rights by component" if en else "分层许可", "CC BY 4.0 · MIT · ODbL" if en else "CC BY 4.0 · MIT · ODbL", "site-overview"),
            ("Final boundary" if en else "终稿边界", "G0 · provisional · no field result · no approval" if en else "G0 · provisional · 无现场结果 · 非批准", "four-state-journey"),
        ]
    doc = fitz.open()
    for index, (title, subtitle, stem) in enumerate(page_specs[:count], 1):
        page = doc.new_page(width=page_size[0], height=page_size[1])
        page.draw_rect(page.rect, color=rgb(PAPER), fill=rgb(PAPER))
        header_h = page_size[1] * 0.135
        page.draw_rect(fitz.Rect(0, 0, page_size[0], header_h), color=rgb(NAVY), fill=rgb(NAVY))
        margin = page_size[0] * 0.045
        add_text(page, fitz.Rect(margin, header_h * .16, page_size[0] - margin, header_h * .58), f"{index:02d} / {count:02d} · TWIN-TRACK JING-ZHANG", header_h * .09, rgb("#ffc21a"), True)
        add_text(page, fitz.Rect(margin, header_h * .43, page_size[0] - margin, header_h * .9), title, header_h * .22, (1, 1, 1), True)
        add_text(page, fitz.Rect(margin, header_h + 18, page_size[0] - margin, header_h + page_size[1] * .065), subtitle, page_size[1] * .022, rgb(INK), True)
        image_path = FIG / f"{stem}{suffix}.png"
        if not image_path.exists():
            image_path = FIG / f"{stem}.png"
        img_rect = fitz.Rect(margin, header_h + page_size[1] * .09, page_size[0] - margin, page_size[1] - page_size[1] * .08)
        page.insert_image(img_rect, filename=str(image_path), keep_proportion=True)
        footer = ("G0 · PROVISIONAL · NOT TO SCALE · NOT APPROVED · CC BY 4.0 / MIT / ODbL") if en else ("G0 · 临时几何 · 不按比例 · 非批准 · CC BY 4.0 / MIT / ODbL")
        add_text(page, fitz.Rect(margin, page_size[1] * .945, page_size[0] - margin, page_size[1] * .978), footer, page_size[1] * .013, rgb(MUTED), False, 1)
    doc.set_metadata({"title": "Twin-Track Jing-Zhang", "author": "xyh202131", "subject": "G0 professional design package", "keywords": "Twin-Track Jing-Zhang, G0, provisional", "creator": "build_convergence_package.py", "producer": "PyMuPDF", "creationDate": "D:20260824000000+08'00'", "modDate": "D:20260824000000+08'00'"})
    doc.save(path, garbage=4, deflate=True, clean=True, no_new_id=True)
    doc.close()


def build_pdfs() -> None:
    DRAWINGS.mkdir(parents=True, exist_ok=True)
    make_pdf(DRAWINGS / "a3-booklet.pdf", False, False)
    make_pdf(DRAWINGS / "a3-booklet.en.pdf", True, False)
    make_pdf(DRAWINGS / "a0-boards.pdf", False, True)
    make_pdf(DRAWINGS / "a0-boards.en.pdf", True, True)


def update_manifest_for_paths() -> None:
    manifest = read_json(ROOT / "manifest.json")
    removed_prefixes = ("assets/media/",)
    removed_exact = {
        "visual/assets/ordinary-life-media-register.json",
        "visual/assets/jury-motion-journey.json",
        "visual/assets/source-rights-evidence.schema.json",
        "visual/assets/review-walkthrough.json",
        "visual/assets/review-walkthrough.js",
        "visual/assets/review-walkthrough.css",
        "visual/assets/round17-reading.css",
        "visual/assets/public-signal-interface.js",
        "visual/assets/public-signal-interface.css",
        "visual/assets/spatial-atlas.css",
    }
    manifest["files"] = [
        row for row in manifest["files"]
        if not row["path"].startswith(removed_prefixes) and row["path"] not in removed_exact
    ]
    manifest["cover_image"] = None
    extensions = manifest.setdefault("validation_claim", {}).setdefault("extensions", {})
    extensions.pop("x-legacy-validation-claim", None)
    extensions["x-rights-claim"] = {
        "schema_version": "2.0",
        "data": {
            "status": "component_licenses_declared",
            "content_license": "CC-BY-4.0",
            "code_license": "MIT",
            "osm_database_license": "ODbL-1.0",
            "generated_media_paths": 0,
            "statement": "Licensing does not establish field truth, approval, professional acceptance or G1.",
        },
    }
    extensions["x-release-claim"] = {
        "schema_version": "2.0",
        "data": {
            "repository_review": "allowed_with_component_notices",
            "professional_implementation": "not_authorized_requires_H01_H07_and_official_inputs",
            "known_blockers": [],
        },
    }
    existing = {row["path"] for row in manifest["files"]}
    additions = [
        ("LICENSE-CONTENT-CC-BY-4.0.md", "other", "content_license"),
        ("LICENSE-CODE-MIT.md", "other", "code_license"),
        ("NOTICE-DATA-ODBL.md", "other", "data_license_notice"),
        ("visual/assets/OFL-Noto-Sans-SC.txt", "other", "font_license_notice"),
        ("visual/assets/source-governance-register.json", "evidence_data", None),
        ("visual/assets/professional-handoff-candidate.json", "evidence_data", None),
        ("visual/assets/convergence-baseline.json", "evidence_data", None),
        ("visual/assets/build_convergence_package.py", "verification_script", None),
        ("assets/figures/ordinary-life-journey.svg", "other", "editable_figure_source"),
        ("assets/figures/ordinary-life-journey.png", "proposal_figure", None),
        ("assets/figures/ordinary-life-journey.en.svg", "other", "editable_figure_source"),
        ("assets/figures/ordinary-life-journey.en.png", "proposal_figure", None),
        ("assets/figures/four-state-journey.svg", "other", "editable_figure_source"),
        ("assets/figures/four-state-journey.png", "proposal_figure", None),
        ("assets/figures/four-state-journey.en.svg", "other", "editable_figure_source"),
        ("assets/figures/four-state-journey.en.png", "proposal_figure", None),
    ]
    for path, role, detail in additions:
        if path in existing:
            continue
        row = {"path": path, "role": role, "required": False}
        if detail:
            row["role_detail"] = detail
        manifest["files"].append(row)
    write_json(ROOT / "manifest.json", manifest)


def write_font_notice() -> None:
    write_text(
        ASSETS / "OFL-Noto-Sans-SC.txt",
        "Noto Sans SC font notice\n\n"
        "Font Software: Noto Sans SC\n"
        "Local source used for PDF embedding: C:/Windows/Fonts/Noto Sans SC (TrueType).otf\n"
        "Declared license: SIL Open Font License, Version 1.1\n"
        "License URL: https://openfontlicense.org/\n\n"
        "The font metadata states that the Font Software is licensed under SIL OFL 1.1 and is distributed AS IS. "
        "The source font binary is not shipped as a standalone package file; PDF subsets are embedded.\n",
    )


def verify_frozen() -> None:
    baseline = read_json(ASSETS / "convergence-baseline.json")["frozen_git_blob_sha256"]
    for rel, expected in baseline.items():
        actual = sha256(ROOT / rel)
        if actual != expected:
            raise RuntimeError(f"Frozen file drift: {rel}: {actual} != {expected}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-pdf", action="store_true")
    args = parser.parse_args()
    verify_frozen()
    write_font_notice()
    prepare_pdf_font()
    update_source_governance()
    write_handoff_candidate()
    build_figures()
    build_visual()
    if not args.skip_pdf:
        build_pdfs()
    update_manifest_for_paths()
    print(json.dumps({
        "status": "built",
        "figures": 6,
        "visuals": 2,
        "pdfs": 0 if args.skip_pdf else 4,
        "model_calls": 0,
        "network_calls": 0,
        "frozen_geometry_and_metrics": True,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
