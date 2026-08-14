# Origin Life Service Station Image-2 Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the Jing-Zhang Symbiotic Everyday Loop around the Origin Life Service Station 1:1 prototype and replace all A0/A3 visible pages with Image-2-only competition boards.

**Architecture:** Structured JSON and a zero-network tabletop runner provide the reviewable operational evidence. Image-2 generates five bilingual A0 boards and twelve bilingual A3 pages using one physical-model visual system; no programmatic drawing or text overlay is permitted. External scripts may only validate unchanged images, assemble them into PDFs, refresh canonical hashes, and run repository gates.

**Tech Stack:** Image-2 built-in generation/editing, JSON, Node.js standard library, Python unittest, Pillow/PyMuPDF for read-only validation and PDF image placement, repository validation scripts, Git.

## Global Constraints

- Final visible page content is authored only by `gpt-image-2`; do not use another image model.
- No PIL, SVG, HTML/CSS, Canvas, slide software, or PDF drawing operation may add or repair visible page content.
- Chinese and English outputs have identical page order, fixed counts, warnings, station/scenario IDs, and claims.
- Fixed counts: 1 spine, 3 loops, 9 stations, 5 prototype moments, 12 scenarios, 3 pilots, G0–G4, 8 first-100-days packages, 72 synthetic checks.
- Every concept page states that the proposal is conceptual/provisional and not an official redline or implementation approval.
- Final submission changes remain under `submissions/EthanHuangEbor/jingzhang-everyday-loop`; temporary specs/plans are removed from the final PR diff.
- Final changed-file total remains below 40 MiB; each PDF remains below 10 MiB.
- Windows worktree bytes never determine manifest hashes; canonical staged Git blobs determine SHA-256 values.

---

### Task 1: Add a failing iteration contract

**Files:**
- Create outside final PR: `D:\Beihang\PlayRepo\project-notes\test_origin_life_iteration.py`
- Test target: `submissions/EthanHuangEbor/jingzhang-everyday-loop`

**Interfaces:**
- Consumes: approved design specification and existing package files.
- Produces: one repeatable command that gates evidence, Image-2 page inventory, PDF page counts, and manifest coverage.

- [ ] **Step 1: Write the failing contract test**

```python
import json
import unittest
from pathlib import Path

from PIL import Image
import fitz

ROOT = Path(r"D:\Beihang\PlayRepo\haidian")
PKG = ROOT / "submissions/EthanHuangEbor/jingzhang-everyday-loop"


class OriginLifeIterationContract(unittest.TestCase):
    def load(self, rel):
        return json.loads((PKG / rel).read_text(encoding="utf-8"))

    def test_origin_life_prototype(self):
        data = self.load("visual/assets/origin-life-service-station.json")
        self.assertEqual(data["prototype_id"], "OLS-1TO1-001")
        self.assertEqual(data["status"], "not_authorized_not_run")
        self.assertEqual([x["order"] for x in data["spatial_moments"]], [1, 2, 3, 4, 5])
        self.assertTrue(data["stop_authority"])
        self.assertTrue(data["restoration_acceptance"])

    def test_twelve_contracts_and_seventy_two_receipts(self):
        contracts = self.load("visual/assets/public-acceptance-tabletop/scenario-contracts.json")
        receipts = self.load("visual/assets/public-acceptance-tabletop/receipts.json")
        self.assertEqual(len(contracts["scenarios"]), 12)
        self.assertEqual(len(receipts["receipts"]), 72)
        self.assertEqual(receipts["qualified_cases_released"], 12)
        self.assertEqual(receipts["negative_cases_blocked"], 60)
        self.assertTrue(all(x["expectation_met"] for x in receipts["receipts"]))

    def test_first_100_days_and_raci(self):
        days = self.load("visual/assets/first-100-days.json")
        raci = self.load("visual/assets/raci-and-signoff.json")
        self.assertEqual(len(days["programme"]), 8)
        self.assertEqual([x["gate"] for x in days["programme"]], ["G0", "G1", "G1", "G2", "G2", "G3", "G3", "G4"])
        self.assertGreaterEqual(len(raci["items"]), 4)

    def test_five_bilingual_a0_pages_are_image2_pages(self):
        names = ["site-overview", "key-areas", "land-use-structure", "mobility-bluegreen", "metrics-evidence"]
        for stem in names:
            for suffix in [".png", ".en.png"]:
                path = PKG / "assets/figures" / f"{stem}{suffix}"
                with Image.open(path) as im:
                    self.assertGreaterEqual(im.width, 1536)
                    self.assertGreaterEqual(im.height, 1024)

    def test_pdf_page_counts(self):
        expected = {"a0-boards.pdf": 5, "a0-boards.en.pdf": 5, "a3-booklet.pdf": 12, "a3-booklet.en.pdf": 12}
        for name, count in expected.items():
            with fitz.open(PKG / "drawings" / name) as doc:
                self.assertEqual(doc.page_count, count)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify the expected failure**

Run:

```powershell
python D:\Beihang\PlayRepo\project-notes\test_origin_life_iteration.py -v
```

Expected: failures for the missing prototype, contracts, receipts, first-100-days, and RACI files. Existing page-count assertions may pass.

- [ ] **Step 3: Record the red-state output in the execution log**

Record the failing test names and confirm the failures are caused by missing iteration artifacts, not import or path errors.

---

### Task 2: Build the operational evidence and tabletop runner

**Files:**
- Create: `submissions/EthanHuangEbor/jingzhang-everyday-loop/visual/assets/origin-life-service-station.json`
- Create: `submissions/EthanHuangEbor/jingzhang-everyday-loop/visual/assets/first-100-days.json`
- Create: `submissions/EthanHuangEbor/jingzhang-everyday-loop/visual/assets/raci-and-signoff.json`
- Create: `submissions/EthanHuangEbor/jingzhang-everyday-loop/visual/assets/public-acceptance-tabletop/scenario-contracts.json`
- Create: `submissions/EthanHuangEbor/jingzhang-everyday-loop/visual/assets/public-acceptance-tabletop/run_tabletop.js`
- Generate: `submissions/EthanHuangEbor/jingzhang-everyday-loop/visual/assets/public-acceptance-tabletop/receipts.json`
- Create: `submissions/EthanHuangEbor/jingzhang-everyday-loop/simulation.json`
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/visual/assets/scenarios.json`

**Interfaces:**
- Consumes: existing scenario IDs `SC-01` through `SC-12`, pilot IDs, station IDs, and design specification.
- Produces: 12 scenario contracts; 72 deterministic receipts; fixed prototype, RACI, gate, and first-100-days records consumed by narrative, images, and validation.

- [ ] **Step 1: Define the five-moment prototype**

Create `origin-life-service-station.json` with `prototype_id="OLS-1TO1-001"`, `status="not_authorized_not_run"`, and `spatial_moments` in this exact order:

```json
[
  {"order":1,"id":"ordinary_passage","zh":"普通通行","en":"Ordinary Passage","ai_required":false},
  {"order":2,"id":"human_service_commons","zh":"人工服务厅","en":"Human Service Commons","ai_required":false},
  {"order":3,"id":"voluntary_ai_alcove","zh":"自愿 AI 小间","en":"Voluntary AI Alcove","ai_required":false},
  {"order":4,"id":"public_receipt_gallery","zh":"公开回执廊","en":"Public Receipt Gallery","personal_information":false},
  {"order":5,"id":"quiet_restoration_garden","zh":"安静恢复园","en":"Quiet Restoration Garden","screen":false}
]
```

Include proposed RACI, required inputs, human signoffs, stop authority, physical stop action, restoration acceptance, and data-expiry ownership. Every real-world role remains pending confirmation.

- [ ] **Step 2: Define the twelve scenario contracts**

For every `SC-01` through `SC-12`, provide these exact fields:

```json
{
  "id":"SC-01",
  "task":"complete_the_declared_public_task",
  "purpose":"bounded purpose in plain language",
  "accountable_role":"proposed_role_pending_confirmation",
  "responsible_role":"proposed_role_pending_confirmation",
  "data_ceiling":["minimum necessary declared input"],
  "same_task_human_route":"staffed, paper, telephone, or ordinary route",
  "success_evidence":"reviewable service receipt",
  "pause_action":"freeze AI path and keep the human route",
  "stop_authority":["responsible duty role","site safety controller"],
  "appeal_route":"staffed and written channel",
  "restoration_acceptance":["ordinary service restored","temporary access removed","disposition recorded"],
  "data_expiry_owner":"proposed_role_pending_confirmation",
  "public_revision_record":true
}
```

The actual names, tasks, inputs, and human routes come from the existing twelve cards and remain scenario-specific.

- [ ] **Step 3: Implement the zero-network runner**

The runner reads the contracts, creates one qualified case plus the five fixed negative variants, evaluates the five conditions, and writes deterministic receipts. The central evaluation is:

```javascript
function evaluate(candidate) {
  const failed = [];
  if (!candidate.accountable_role) failed.push("accountable_role");
  if (!candidate.same_task_human_route) failed.push("same_task_human_route");
  if (candidate.data_exceeds_declared_ceiling) failed.push("data_ceiling");
  if (!candidate.stop_authority?.length) failed.push("stop_authority");
  if (!candidate.restoration_acceptance?.length) failed.push("restoration_evidence");
  return {
    release_decision: failed.length ? "block_release" : "release_for_tabletop_only",
    failed_conditions: failed
  };
}
```

The runner must sort by scenario ID and variant order, write UTF-8 JSON with a trailing newline, and never read the network, clock, random values, environment secrets, or external files.

- [ ] **Step 4: Run the runner and verify exact totals**

Run:

```powershell
node submissions/EthanHuangEbor/jingzhang-everyday-loop/visual/assets/public-acceptance-tabletop/run_tabletop.js
```

Expected: `PASS: 72 synthetic cases; 12 qualified tabletop releases; 60 negative cases blocked`.

- [ ] **Step 5: Run the contract test**

Expected: the prototype, 72-receipt, first-100-days, and RACI tests pass; image work remains pending.

- [ ] **Step 6: Commit the operational evidence**

```powershell
git add submissions/EthanHuangEbor/jingzhang-everyday-loop/visual/assets submissions/EthanHuangEbor/jingzhang-everyday-loop/simulation.json
git commit -m "feat(submission): add origin life operational evidence"
```

---

### Task 3: Rewrite the human narrative around the prototype

**Files:**
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/proposal.md`
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/proposal.en.md`
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/metrics.json`
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/compliance_matrix.json`
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/design_depth_matrix.json`
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/standard_matrix.json`
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/visual/assets/professional-evidence.json`
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/visual/assets/repair-matrix.json`
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/visual/assets/asset-rights-ledger.json`

**Interfaces:**
- Consumes: Task 2 evidence paths and fixed identifiers.
- Produces: claim-adjacent bilingual narrative and matrix pointers consumed by HTML/PDF and professional review.

- [ ] **Step 1: Add prototype and evidence-gate sections**

Add bounded bilingual sections for the five spatial moments, same-task equivalence, 72 synthetic checks, G0–G4, first 100 days, RACI, and stop/restore decisions. Every field-status claim states `not_authorized_not_run`.

- [ ] **Step 2: Add precise evidence anchors**

Use adjacent markers including:

```text
[data:visual/assets/origin-life-service-station.json#/spatial_moments]
[data:visual/assets/public-acceptance-tabletop/scenario-contracts.json#/scenarios]
[data:simulation.json#/task_count]
[metric:synthetic_tabletop_check_count]
[depth:phasing_implementation]
[standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK]
```

- [ ] **Step 3: Add machine metrics without field claims**

Add metrics for five prototype moments, twelve qualified contracts, sixty blocked negative cases, seventy-two total checks, five evidence gates, and eight first-100-days packages. Mark all as concept/tabletop evidence, not field performance.

- [ ] **Step 4: Update rights and repair ledgers**

Record `gpt-image-2` as the visual creation method, list only owned/current-project inputs, prohibit PR #2247 visual assets as generation references, and add evidence paths for the new operational claims.

- [ ] **Step 5: Run bilingual and professional validators**

Run the repository bilingual and professional-review scripts. Expected: no missing translation mapping, source marker, mandatory matrix entry, or duplicated long section.

- [ ] **Step 6: Commit the narrative iteration**

```powershell
git add submissions/EthanHuangEbor/jingzhang-everyday-loop
git commit -m "docs(submission): center the origin life prototype"
```

---

### Task 4: Generate five Chinese A0 Image-2 masters

**Files:**
- Replace: `submissions/EthanHuangEbor/jingzhang-everyday-loop/assets/figures/site-overview.png`
- Replace: `submissions/EthanHuangEbor/jingzhang-everyday-loop/assets/figures/key-areas.png`
- Replace: `submissions/EthanHuangEbor/jingzhang-everyday-loop/assets/figures/land-use-structure.png`
- Replace: `submissions/EthanHuangEbor/jingzhang-everyday-loop/assets/figures/mobility-bluegreen.png`
- Replace: `submissions/EthanHuangEbor/jingzhang-everyday-loop/assets/figures/metrics-evidence.png`
- Create: `submissions/EthanHuangEbor/jingzhang-everyday-loop/visual/assets/image2-production-record.json`

**Interfaces:**
- Consumes: Tasks 2–3 fixed facts, B-style reference generated during brainstorming, and only current-project owned visual inputs.
- Produces: five accepted Chinese Image-2 pages that are both core figures and A0 PDF pages.

- [ ] **Step 1: Use the common Image-2 board contract**

Every prompt specifies: physical architectural model and technical editorial board; ivory paper; graphite linework; brick red, brass, and blue-green accents; inclusive public use; 3:2 landscape; exact sparse text; no other readable text; no invented measurement, approval, operator, government mark, company logo, pseudo-writing, or watermark.

- [ ] **Step 2: Generate page 01 — Overall proposition**

Required exact visible text:

```text
京张共生日常环
一脊 · 三环 · 九站
众智园验证 · 原点转译 · 大钟寺采用
概念方案｜临时边界非官方红线｜尚未获准实施
```

Required visible counts: one spine, three named loops, nine stations numbered 1–9 once.

- [ ] **Step 3: Generate page 02 — Three areas and nine stations**

Required exact visible text:

```text
三区与九站
众智园 AI 自主创新加速区
北京 AI 原点社区
大钟寺 AI 产业聚集区
验证 · 转译 · 采用
概念位置｜真实边界与主体待确认
```

Required visible counts: three areas, three stations per area, nine stations total.

- [ ] **Step 4: Generate page 03 — Origin Life Service Station**

Required exact visible text:

```text
原点生活服务站
1:1 公共原型
01 普通通行
02 人工服务厅
03 自愿 AI 小间
04 公开回执廊
05 安静恢复园
概念方案｜尚未获准实施
```

Required visible counts: moments 01–05 once each; accessible ordinary route remains continuous.

- [ ] **Step 5: Generate page 04 — Twelve scenario contracts**

Required exact visible text:

```text
十二场景合同
同任务人工路径
数据上限
人工签认
停止与申诉
恢复与退役
12 场景｜3 试点｜概念验证
```

Required visible counts: scenario IDs 01–12 once each and three pilots.

- [ ] **Step 6: Generate page 05 — Tabletop to field**

Required exact visible text:

```text
从桌面到现场
G0 证据与权利
G1 同任务等价
G2 受控服务
G3 停止与恢复
G4 独立续行
72 合成检查｜12 放行｜60 拦截
首个 100 天｜8 步
非现场绩效｜非实施批准
```

Required visible counts: G0–G4 once; 72, 12, 60, 100, and 8 consistent with evidence.

- [ ] **Step 7: Inspect and repair each page with Image-2 only**

At original resolution, check every title, number, warning, label, model element, person, route, and material panel. Use a targeted Image-2 edit for any error; change only the failed region and preserve accepted composition.

- [ ] **Step 8: Record accepted prompt, inputs, dimensions, checks, and file hash**

Write one record per accepted page to `image2-production-record.json`, with `language="zh"`, `model="gpt-image-2"`, `visual_authoring="image2_only"`, prompt, input references, iteration count, fixed-count disposition, text disposition, and SHA-256.

---

### Task 5: Localize the five A0 pages with Image-2

**Files:**
- Replace: the five corresponding `assets/figures/*.en.png` files.
- Modify: `visual/assets/image2-production-record.json`
- Modify: `visual/assets/bilingual-equivalence.json`

**Interfaces:**
- Consumes: accepted Chinese masters from Task 4.
- Produces: five English Image-2 edits with composition and fixed counts preserved.

- [ ] **Step 1: Load each Chinese master as the edit target**

Use the Chinese master as the only target image. Preserve model, people, material, page grid, numbering, color, and warning placement.

- [ ] **Step 2: Replace only Chinese text with exact English copy**

Use these fixed titles:

```text
JING-ZHANG SYMBIOTIC EVERYDAY LOOP
THREE AREAS + NINE STATIONS
ORIGIN LIFE SERVICE STATION
TWELVE SCENARIO CONTRACTS
FROM TABLETOP TO FIELD
```

Use `COMMUNITY + CARE`, never `COMMUNITY + CART`. Use `CONCEPT PROPOSAL · PROVISIONAL BOUNDARY IS NOT AN OFFICIAL REDLINE · NOT AUTHORIZED FOR IMPLEMENTATION` on relevant pages.

- [ ] **Step 3: Inspect and repair English pages with Image-2 only**

Fail any pseudo-text, spelling error, changed count, added measurement, altered person/route, or factual mismatch. Repair only with Image-2.

- [ ] **Step 4: Complete the bilingual equivalence records**

Record title, count, warning, layout-difference, and disposition for all five pairs.

- [ ] **Step 5: Run the A0 portion of the contract test**

Expected: ten figures decode and meet minimum dimensions.

- [ ] **Step 6: Commit the A0 Image-2 set**

```powershell
git add submissions/EthanHuangEbor/jingzhang-everyday-loop/assets/figures submissions/EthanHuangEbor/jingzhang-everyday-loop/visual/assets
git commit -m "feat(submission): rebuild A0 boards with Image-2"
```

---

### Task 6: Generate the twelve bilingual A3 Image-2 page pairs

**Files:**
- Create outside final PR: `D:\Beihang\PlayRepo\project-notes\origin-life-image2\a3\zh\01.png` through `12.png`
- Create outside final PR: `D:\Beihang\PlayRepo\project-notes\origin-life-image2\a3\en\01.png` through `12.png`
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/visual/assets/image2-production-record.json`

**Interfaces:**
- Consumes: accepted B visual system and Tasks 2–5 facts.
- Produces: 24 accepted Image-2 booklet pages, stored outside the final PR and embedded unchanged into PDFs.

- [ ] **Step 1: Generate Chinese pages in fixed order**

Generate exactly these subjects:

```text
01 封面与公共承诺
02 为什么是日常环：五项公众判断
03 三层范围与一脊三环
04 三区两翼与区域接口
05 九站台账
06 原点生活服务站五段原型
07 十二场景与人物旅程
08 同任务等价与公众验收
09 三试点与 72 条合成检查
10 首个 100 天与 G0–G4
11 RACI、年度运营、停止与恢复
12 来源、版权、未知数据与非批准边界
```

Each page uses one title, one short subtitle, five to eight short labels, and one concise concept/non-approval warning. Do not render paragraph-sized copy.

- [ ] **Step 2: Repair every Chinese page with Image-2 only**

Apply the fixed-count and stop-ship contract from the design specification.

- [ ] **Step 3: Produce English pages as Image-2 localizations**

Use each accepted Chinese page as the edit target; preserve all non-language content and counts.

- [ ] **Step 4: Repair every English page with Image-2 only**

Reject any fact mismatch, changed count, spelling error, added claim, or pseudo-text.

- [ ] **Step 5: Record all 24 accepted pages**

Add prompts, hashes, input references, iteration counts, language pair, fixed-count checks, and human disposition to `image2-production-record.json`.

---

### Task 7: Assemble image-only PDFs and refresh offline reports

**Files:**
- Create outside final PR: `D:\Beihang\PlayRepo\project-notes\package_origin_life_image2_pdfs.py`
- Replace: `submissions/EthanHuangEbor/jingzhang-everyday-loop/drawings/a0-boards.pdf`
- Replace: `submissions/EthanHuangEbor/jingzhang-everyday-loop/drawings/a0-boards.en.pdf`
- Replace: `submissions/EthanHuangEbor/jingzhang-everyday-loop/drawings/a3-booklet.pdf`
- Replace: `submissions/EthanHuangEbor/jingzhang-everyday-loop/drawings/a3-booklet.en.pdf`
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/report/proposal.html`
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/report/proposal.en.html`
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/visual/index.html`
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/visual/index.en.html`

**Interfaces:**
- Consumes: ten A0 core images and 24 external A3 page images.
- Produces: four image-only PDFs and offline HTML that references the accepted A0 boards and operational evidence.

- [ ] **Step 1: Implement image-only PDF placement**

The packaging script creates a page and inserts exactly one unchanged source image per page:

```python
import fitz
from pathlib import Path

def build_pdf(images: list[Path], output: Path, page_size: tuple[float, float]):
    doc = fitz.open()
    rect = fitz.Rect(0, 0, page_size[0], page_size[1])
    for image in images:
        page = doc.new_page(width=rect.width, height=rect.height)
        page.insert_image(rect, filename=str(image), keep_proportion=True, overlay=True)
    doc.save(output, garbage=4, deflate=True)
    doc.close()
```

The script must not draw text, vectors, borders, backgrounds, annotations, links, or additional images.

- [ ] **Step 2: Build the four PDFs**

Use the five accepted A0 image pairs and twelve accepted A3 image pairs. Expected page counts: 5, 5, 12, 12.

- [ ] **Step 3: Update offline HTML**

Regenerate text-only HTML narrative and reference the five accepted bilingual A0 images. Do not reconstruct PDF pages in HTML/CSS.

- [ ] **Step 4: Render every PDF page for inspection**

Render all 34 pages to an external review directory. Inspect contact sheets, then inspect every page at original resolution.

- [ ] **Step 5: Run the full contract test**

Expected: all origin-life evidence, ten core figures, and four PDF page-count tests pass.

- [ ] **Step 6: Commit PDFs and reports**

```powershell
git add submissions/EthanHuangEbor/jingzhang-everyday-loop/drawings submissions/EthanHuangEbor/jingzhang-everyday-loop/report submissions/EthanHuangEbor/jingzhang-everyday-loop/visual submissions/EthanHuangEbor/jingzhang-everyday-loop/assets/figures
git commit -m "feat(submission): publish image-only bilingual deliverables"
```

---

### Task 8: Run visual, bilingual, rights, and operational acceptance

**Files:**
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/visual/assets/accessibility-audit.json`
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/visual/assets/bilingual-equivalence.json`
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/visual/assets/asset-rights-ledger.json`
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/visual/assets/repair-matrix.json`
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/report/copyright_statement.md`

**Interfaces:**
- Consumes: all accepted visible and structured artifacts.
- Produces: human review records with no unresolved stop-ship item.

- [ ] **Step 1: Verify every fixed count and warning**

Inspect 10 A0 images, 10 A0 PDF pages, and 24 A3 PDF pages. Confirm required counts and warnings independently in Chinese and English.

- [ ] **Step 2: Verify pseudo-text and readability**

At 100% and 200%, inspect all readable regions. Fail pseudo-Chinese, tofu, broken glyphs, misspelled English, decorative micro-writing, cropping, and illegible warnings.

- [ ] **Step 3: Verify bilingual equivalence**

Check title, fixed counts, IDs, scenario meaning, warnings, unknowns, and layout differences for all 17 page pairs.

- [ ] **Step 4: Verify rights and generation provenance**

Confirm every distributed visual has a `gpt-image-2` creation record, cleared current-project inputs, no copied PR #2247 visual, and explicit redistribution/PDF/Web use status.

- [ ] **Step 5: Verify tabletop determinism**

Run the runner twice and compare receipt SHA-256 values. Expected: byte-identical receipts and `12/12` qualified tabletop releases plus `60/60` negative blocks.

- [ ] **Step 6: Repair any stop-ship visual only with Image-2**

After a repair, reassemble the affected PDF language set and reinspect the page, its pair, and dependent counts.

---

### Task 9: Finalize manifest and repository gates

**Files:**
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/changelog.md`
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/manifest.json`
- Modify: `submissions/EthanHuangEbor/jingzhang-everyday-loop/self_check.json`
- Remove before final PR: `docs/superpowers/specs/2026-08-14-origin-life-image2-redesign.md`
- Remove before final PR: `docs/superpowers/plans/2026-08-14-origin-life-image2-redesign.md`

**Interfaces:**
- Consumes: final staged submission inventory.
- Produces: canonical manifest, persisted four-gate self-check, clean submission-only PR diff.

- [ ] **Step 1: Update changelog and inventory**

Record the core prototype, Image-2-only 34-page rebuild, 72-case rehearsal, first 100 days, RACI, and validation scope without claiming field results.

- [ ] **Step 2: Remove temporary docs from the final diff**

Delete the committed design specification and implementation plan so the final PR remains submission-only.

- [ ] **Step 3: Stage every final submission file**

Ensure no unrelated path is staged and every new allowed file is present in `manifest.json` with canonical roles and translations.

- [ ] **Step 4: Refresh SHA-256 from staged canonical Git blobs**

Do not hash the Windows CRLF worktree. Read every staged blob using `git cat-file blob :<path>` and write those hashes to `manifest.json`.

- [ ] **Step 5: Run the complete verification suite**

Run:

```powershell
python D:\Beihang\PlayRepo\project-notes\test_origin_life_iteration.py -v
python D:\Beihang\PlayRepo\project-notes\audit_index_manifest.py
python scripts/validate_local_submission.py submissions/EthanHuangEbor/jingzhang-everyday-loop --repo-root . --pr-author EthanHuangEbor --strict-manifest --json
python scripts/self_check_submission.py submissions/EthanHuangEbor/jingzhang-everyday-loop --repo-root . --pr-author EthanHuangEbor --json
git diff --cached --check
```

Expected: contract tests pass; manifest canonical blobs all match; deterministic, spatial, visual, and professional gates pass; only disclosed provisional-boundary notices remain; no whitespace errors.

- [ ] **Step 6: Persist self-check and re-audit canonical hashes**

Mark self-checked, stage `self_check.json`, update its canonical manifest hash, and rerun the 100% canonical audit.

- [ ] **Step 7: Commit the verified package**

```powershell
git commit -m "feat(submission): deliver origin life Image-2 iteration"
```

---

### Task 10: Update PR #2398 and monitor CI

**Files:**
- No additional repository files unless CI reveals a reproducible submission defect.

**Interfaces:**
- Consumes: verified final commit on the existing submission branch.
- Produces: updated PR head and evidence-backed CI status.

- [ ] **Step 1: Inspect final worktree and commit range**

Run `git status --short`, `git diff upstream/main --stat`, and `git log --oneline upstream/main..HEAD`. Confirm the diff contains only the intended submission package.

- [ ] **Step 2: Push the existing PR branch over SSH**

Run:

```powershell
git push origin codex/formal-jingzhang-proposal
```

- [ ] **Step 3: Verify PR head and mergeability**

Confirm PR #2398 points at the final commit and remains open/mergeable.

- [ ] **Step 4: Monitor the new submission-validation run**

Do not reuse an old SHA's result. If the new run fails, inspect the exact job and reproduce the failure locally before changing files.

- [ ] **Step 5: Report exact final state**

Report final commit, PR URL, local test totals, canonical hash total, four gate results, PDF page counts, and current CI run status without claiming success while it is pending.
