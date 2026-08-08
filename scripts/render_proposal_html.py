#!/usr/bin/env python3
"""Render a submission proposal.md into an offline readable HTML report."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path, PurePosixPath


IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
REFERENCE_RE = re.compile(r"\[(source|standard|depth|data|metric|assumption):([^\]\s]+)\]")
INLINE_CODE_RE = re.compile(r"`([^`]+)`")


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    metadata: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata, text[end + 5 :]


def normalize_image_src(submission_dir: Path, raw_src: str) -> str:
    if re.match(r"^(?:https?:)?//", raw_src, re.I) or re.match(r"^(?:data|file|javascript):", raw_src, re.I):
        raise ValueError(f"remote or unsafe image source is not allowed: {raw_src}")
    clean = raw_src.split("#", 1)[0].split("?", 1)[0]
    pure = PurePosixPath(clean)
    if pure.is_absolute() or ".." in pure.parts:
        raise ValueError(f"image source must be a relative local path: {raw_src}")
    image_path = submission_dir / pure.as_posix()
    if not image_path.exists():
        raise ValueError(f"image source is missing: {raw_src}")
    return "../" + pure.as_posix()


def render_inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = INLINE_CODE_RE.sub(lambda m: f"<code>{html.escape(m.group(1))}</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)

    def replace_ref(match: re.Match[str]) -> str:
        kind = match.group(1)
        value = match.group(2)
        labels = {
            "source": ("源", "来源"),
            "standard": ("标", "标准"),
            "depth": ("深", "设计深度"),
            "data": ("数", "数据图层"),
            "metric": ("指标", "指标"),
            "assumption": ("设", "假设"),
        }
        short, label = labels[kind]
        full = f"[{kind}:{value}]"
        return (
            f'<details class="ev ev-{kind}">'
            f'<summary title="{html.escape(full)}">{short}</summary>'
            f'<div class="ev-card"><b>{label}</b><code>{html.escape(full)}</code></div>'
            "</details>"
        )

    return REFERENCE_RE.sub(replace_ref, escaped)


def render_markdown_body(submission_dir: Path, markdown: str) -> str:
    blocks: list[str] = []
    paragraph: list[str] = []
    in_list = False
    in_ordered_list = False
    table_rows: list[list[str]] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            blocks.append(f"<p>{render_inline(' '.join(paragraph))}</p>")
            paragraph = []

    def close_list() -> None:
        nonlocal in_list, in_ordered_list
        if in_list:
            blocks.append("</ul>")
            in_list = False
        if in_ordered_list:
            blocks.append("</ol>")
            in_ordered_list = False

    def flush_table() -> None:
        nonlocal table_rows
        if not table_rows:
            return
        rows = table_rows
        table_rows = []
        if len(rows) > 1 and all(re.fullmatch(r":?-{3,}:?", cell) for cell in rows[1]):
            header = rows[0]
            body_rows = rows[2:]
        else:
            header = rows[0]
            body_rows = rows[1:]
        head = "".join(f"<th>{render_inline(cell)}</th>" for cell in header)
        body = "".join(
            "<tr>" + "".join(f"<td>{render_inline(cell)}</td>" for cell in row) + "</tr>"
            for row in body_rows
        )
        blocks.append(
            '<div class="table-wrap"><table><thead><tr>'
            + head
            + "</tr></thead><tbody>"
            + body
            + "</tbody></table></div>"
        )

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        if line.strip().startswith("|") and line.strip().endswith("|"):
            flush_paragraph()
            close_list()
            table_rows.append([cell.strip() for cell in line.strip()[1:-1].split("|")])
            continue
        flush_table()
        if not line.strip():
            flush_paragraph()
            close_list()
            continue

        image_match = IMAGE_RE.fullmatch(line.strip())
        if image_match:
            flush_paragraph()
            close_list()
            alt = html.escape(image_match.group(1).strip() or "proposal figure")
            src = normalize_image_src(submission_dir, image_match.group(2).strip())
            blocks.append(
                '<figure class="proposal-figure">'
                f'<img src="{html.escape(src)}" alt="{alt}">'
                f"<figcaption>{alt}</figcaption>"
                "</figure>"
            )
            continue

        if line.startswith("#"):
            flush_paragraph()
            close_list()
            level = min(len(line) - len(line.lstrip("#")), 4)
            title = line[level:].strip()
            blocks.append(f"<h{level}>{render_inline(title)}</h{level}>")
            continue

        if line.startswith("> "):
            flush_paragraph()
            close_list()
            blocks.append(f"<blockquote>{render_inline(line[2:].strip())}</blockquote>")
            continue

        if line.startswith("- "):
            flush_paragraph()
            if in_ordered_list:
                close_list()
            if not in_list:
                blocks.append("<ul>")
                in_list = True
            blocks.append(f"<li>{render_inline(line[2:].strip())}</li>")
            continue

        ordered_match = re.match(r"^\d+\.\s+(.+)$", line)
        if ordered_match:
            flush_paragraph()
            if in_list:
                close_list()
            if not in_ordered_list:
                blocks.append("<ol>")
                in_ordered_list = True
            blocks.append(f"<li>{render_inline(ordered_match.group(1))}</li>")
            continue

        paragraph.append(line.strip())

    flush_paragraph()
    close_list()
    flush_table()
    return "\n".join(blocks)


def render_html(submission_dir: Path) -> str:
    proposal_path = submission_dir / "proposal.md"
    metadata, body = parse_front_matter(proposal_path.read_text(encoding="utf-8"))
    title = metadata.get("title") or submission_dir.name
    summary = metadata.get("summary", "")
    language = metadata.get("language", "zh")
    document_lang = "en" if language == "en" else "zh-CN"
    translation_match = re.search(r"(?m)^# 中文正式译文\s*$", body) if language == "en" else None
    if translation_match:
        english_body = body[: translation_match.start()]
        translation_body = body[translation_match.end() :]
        rendered_body = (
            f'<section lang="en">{render_markdown_body(submission_dir, english_body)}</section>'
            f'<section lang="zh-CN"><h1>中文正式译文</h1>'
            f'{render_markdown_body(submission_dir, translation_body)}</section>'
        )
    else:
        rendered_body = render_markdown_body(submission_dir, body)
    return f"""<!doctype html>
<html lang="{document_lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} - proposal report</title>
<style>
:root {{
  --ink: #2b2118;
  --muted: #6b5b4b;
  --line: #c9b8a0;
  --paper: #fbf6ec;
  --bg: #efe3cf;
  --accent: #b33a2b;
  --celadon: #3e7a62;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  font-family: "Songti SC", "STSong", "PingFang SC", "Microsoft YaHei", serif;
  color: var(--ink);
  background: var(--bg);
  line-height: 1.75;
}}
main {{
  max-width: 980px;
  margin: 0 auto;
  padding: 42px 24px 72px;
  background: var(--paper);
  min-height: 100vh;
  box-shadow: 0 0 0 1px rgba(23, 32, 51, 0.05);
}}
.hero {{
  border-bottom: 3px solid var(--accent);
  padding-bottom: 24px;
  margin-bottom: 30px;
}}
h1 {{ font-size: 34px; line-height: 1.22; margin: 0 0 10px; }}
h2 {{ font-size: 25px; margin: 34px 0 12px; border-top: 1px solid var(--line); padding-top: 24px; }}
h3 {{ font-size: 20px; margin: 26px 0 10px; }}
p, li {{ font-size: 16px; }}
blockquote {{
  margin: 10px 0 16px;
  padding: 10px 14px;
  border-left: 3px solid #c29b48;
  background: #f7f0e2;
  color: var(--muted);
}}
code {{
  background: #f0e6d4;
  color: var(--ink);
  padding: 0.1em 0.35em;
  border-radius: 4px;
}}
.summary {{ color: var(--muted); font-size: 17px; }}
.toolbar {{
  position: sticky;
  top: 0;
  z-index: 20;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  align-items: center;
  padding: 10px 0;
  background: linear-gradient(var(--paper) 75%, transparent);
}}
.ev-toggle {{ position: absolute; opacity: 0; pointer-events: none; }}
.ev-toggle-label {{
  font-size: 13px;
  border: 1px solid var(--line);
  background: #f7f0e2;
  padding: 6px 12px;
  cursor: pointer;
}}
.ev-toggle:checked + .ev-toggle-label {{
  background: #f8e8df;
  border-color: var(--accent);
  color: #6e2c22;
}}
.hint {{ font-size: 12px; color: var(--muted); }}
.note {{
  background: #f8e8df;
  border: 1px solid var(--accent);
  color: #6e2c22;
  padding: 10px 12px;
  font-size: 13px;
  margin: 0 0 16px;
}}
.proposal-figure {{
  margin: 22px 0 28px;
  border: 1px solid var(--line);
  border-radius: 10px;
  overflow: hidden;
  background: #f8fafc;
}}
.proposal-figure img {{
  display: block;
  width: 100%;
  height: auto;
}}
.proposal-figure figcaption {{
  padding: 10px 14px;
  color: var(--muted);
  border-top: 1px solid var(--line);
  font-size: 14px;
}}
.table-wrap {{ overflow-x: auto; margin: 14px 0 20px; border: 1px solid var(--line); }}
table {{ width: 100%; border-collapse: collapse; background: #fff; }}
th, td {{ padding: 8px 9px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
th {{ background: #efe3cf; }}
.ev {{ display: none; position: relative; margin-left: 3px; vertical-align: super; }}
body:has(.ev-toggle:checked) .ev {{ display: inline-block; }}
.ev > summary {{
  list-style: none;
  cursor: pointer;
  font-size: 11px;
  line-height: 1;
  border: 1px solid var(--line);
  border-radius: 3px;
  padding: 1px 5px;
  color: var(--muted);
  background: #f7f0e2;
}}
.ev > summary::-webkit-details-marker {{ display: none; }}
.ev[open] > summary {{ border-color: var(--accent); color: var(--accent); }}
.ev-metric > summary {{ color: var(--accent); border-color: #e2b8b0; }}
.ev-source > summary {{ color: var(--celadon); border-color: #b7d0c4; }}
.ev-card {{
  position: absolute;
  left: 0;
  top: 1.6em;
  z-index: 30;
  min-width: 220px;
  max-width: 300px;
  padding: 10px 12px;
  background: #2b2118;
  color: #f8f0e0;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.22);
  font-size: 12px;
  line-height: 1.45;
}}
.ev-card b {{ display: block; color: #e2c98a; margin-bottom: 4px; }}
.ev-card code {{ display: block; background: rgba(255, 255, 255, 0.08); color: #f8f0e0; word-break: break-all; }}
@media (max-width: 720px) {{
  main {{ padding: 26px 16px 52px; }}
  h1 {{ font-size: 26px; }}
  h2 {{ font-size: 21px; }}
}}
</style>
</head>
<body>
<main>
<section class="hero">
<h1>{html.escape(title)}</h1>
<p class="summary">{html.escape(summary)}</p>
</section>
<div class="toolbar">
  <input class="ev-toggle" type="checkbox" id="toggle-ev">
  <label class="ev-toggle-label" for="toggle-ev">显示证据角标</label>
  <span class="hint">默认隐藏；需要技术核对时打开，再点击角标查看完整编号。</span>
</div>
<div class="note">正文优先呈现规划判断和可读指标；来源、标准、数据、假设等技术标签默认隐藏。</div>
{rendered_body}
</main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("submission_dir")
    parser.add_argument("--out", default="report/proposal.html")
    args = parser.parse_args()

    submission_dir = Path(args.submission_dir).resolve()
    out_path = submission_dir / args.out
    if not (submission_dir / "proposal.md").exists():
        raise SystemExit(f"{submission_dir}/proposal.md is missing")
    html_text = render_html(submission_dir)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_text, encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
