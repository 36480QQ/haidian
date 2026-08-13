# 方案迭代记录

## v0.1 - 2026-08-13

State: `FORMAL-BASELINE-V0.1 / NOT READY FOR REVIEW`  
Working candidate: `京张续城 / Jing-Zhang In Place`  
Final winner: `OWNER_DECISION_REQUIRED`

The package is intentionally reversible. It uses the organizer's provisional geometry as a computational envelope and does not convert it into statutory precision. The proposal, sources, assumptions and scenarios are real baseline content; diagrams and PDFs are deterministic v0 outputs; geometry and matrices require professional deepening before `ready_for_review`.

## Build

```powershell
# Run the pinned builder from the design-lab production-readiness workspace.
.\.venv\Scripts\python.exe scripts\render_proposal_html.py submissions\JerrySkywalker\jingzhang-in-place
.\.venv\Scripts\python.exe scripts\refresh_submission_manifest.py submissions\JerrySkywalker\jingzhang-in-place
```

Pinned host strategy:

- figures: Python 3.12 + Pillow 12.3.0;
- vector source: deterministic SVG emitted by the participant builder;
- PDFs: ReportLab installed in project `.venv`;
- HTML: official `render_proposal_html.py` plus participant static visual shell;
- Chinese font: Microsoft YaHei from the Windows host; English font: Arial; no font files are redistributed;
- fallback: SimHei for Chinese and Pillow/ReportLab built-in sans-serif for English;
- all outputs are offline and contain no external asset request.

## Current production gaps

1. Official exact polygons and statutory controls are absent; a full geometry/metric rebuild is mandatory when received.
2. Building, access, utility and incumbent-user surveys have not been performed.
3. Concept geometry needs topology-safe status/action patches and three professional sections after survey inputs.
4. A3/A0 are pipeline-valid baseline boards, not final competition layouts.
5. Bilingual prose has semantic parity at v0.1; sentence-level and figure-label parity still require the 08-17 audit.
