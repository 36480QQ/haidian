import re
import json
import subprocess
import sys
import unittest
import tempfile
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from generate_submissions_data import build_data, discover_submissions, load_publication_registry, package_sha256  # noqa: E402
DATA_FILE = ROOT / "submissions-data.js"
INDEX_FILE = ROOT / "index.html"
SUBMISSIONS_FILE = ROOT / "submissions.html"


class TestSubmissionsGallery(unittest.TestCase):
    def load_gallery_items(self):
        data = DATA_FILE.read_text(encoding="utf-8")
        match = re.search(r"window\.HAIDIAN_SUBMISSIONS = (\[.*\]);\s*$", data, re.S)
        self.assertIsNotNone(match)
        return json.loads(match.group(1))

    def test_every_merged_submission_is_listed_unless_explicitly_held(self):
        registry = json.loads((ROOT / "gallery-publication.json").read_text(encoding="utf-8"))
        held = {entry["path"] for entry in registry["entries"] if not entry["published"]}
        expected = {
            path.relative_to(ROOT).as_posix()
            for path in discover_submissions(ROOT)
            if path.relative_to(ROOT).as_posix() not in held
        }
        source_paths = {str(Path(item["sourceUrl"]).parent) for item in self.load_gallery_items()}
        self.assertEqual(expected, source_paths)

    def test_homepage_featured_state_comes_from_publication_registry(self):
        registry = json.loads((ROOT / "gallery-publication.json").read_text(encoding="utf-8"))
        publication = {entry["path"]: entry for entry in registry["entries"]}
        expected = {
            path.name: publication.get(path.relative_to(ROOT).as_posix(), {}).get("featured", False)
            for path in discover_submissions(ROOT)
            if publication.get(path.relative_to(ROOT).as_posix(), {}).get("published", True)
        }
        actual = {item["id"]: item["featured"] for item in self.load_gallery_items()}
        self.assertEqual(expected, actual)
        self.assertTrue(all("selectionReason" in item for item in self.load_gallery_items()))

    def test_merged_submission_is_public_without_registry_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            submission = root / "submissions" / "alice" / "example"
            (submission / "report").mkdir(parents=True)
            (submission / "proposal.md").write_text(
                "---\ntitle: Example proposal\nsummary: A merged proposal\n---\n",
                encoding="utf-8",
            )
            (submission / "report" / "proposal.html").write_text(
                "<!doctype html><title>Example proposal</title>",
                encoding="utf-8",
            )
            (root / "gallery-publication.json").write_text(
                '{"version": 1, "entries": []}\n',
                encoding="utf-8",
            )
            items = build_data(root)
            self.assertEqual(1, len(items))
            self.assertEqual("example", items[0]["id"])
            self.assertFalse(items[0]["featured"])
            self.assertEqual(
                "proposal-view.html?proposal=submissions/alice/example",
                items[0]["proposalUrl"],
            )

    def test_registry_can_explicitly_hold_a_merged_submission(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            submission = root / "submissions" / "alice" / "example"
            submission.mkdir(parents=True)
            (submission / "proposal.md").write_text("# Example\n", encoding="utf-8")
            entry = {
                "path": "submissions/alice/example",
                "published": False,
                "featured": False,
                "review_status": "not_approved",
                "quality_tier": "qualified",
                "reviewed_by": "maintainer",
                "reviewed_at": "2026-08-07",
                "rights_reviewed": False,
                "reviewed_package_sha256": "0" * 64,
                "selection_reason_zh": "维护者明确暂停公开展示",
                "selection_reason_en": "Explicitly held from public display",
                "selected_at": "2026-08-07",
            }
            (root / "gallery-publication.json").write_text(
                json.dumps({"version": 1, "entries": [entry]}),
                encoding="utf-8",
            )
            self.assertEqual([], build_data(root))

    def test_publication_registry_rejects_missing_selection_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "gallery-publication.json").write_text(
                json.dumps({"version": 1, "entries": [{"path": "submissions/alice/example", "published": False, "featured": False}]}),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(SystemExit, "missing fields"):
                load_publication_registry(root)

    def test_publication_registry_rejects_invalid_date_and_flag_types(self):
        base = {
            "path": "submissions/alice/example",
            "published": False,
            "featured": False,
            "review_status": "not_approved",
            "quality_tier": "qualified",
            "reviewed_by": "maintainer",
            "reviewed_at": "2026-08-05",
            "rights_reviewed": False,
            "reviewed_package_sha256": "0" * 64,
            "selection_reason_zh": "公开展示理由",
            "selection_reason_en": "Publication reason",
            "selected_at": "2026-08-05",
        }
        for field, value, message in [
            ("published", "yes", "published must be boolean"),
            ("selected_at", "August 5", "selected_at must be YYYY-MM-DD"),
        ]:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                entry = dict(base)
                entry[field] = value
                (root / "gallery-publication.json").write_text(
                    json.dumps({"version": 1, "entries": [entry]}), encoding="utf-8"
                )
                with self.assertRaisesRegex(SystemExit, message):
                    load_publication_registry(root)

    def test_publication_registry_requires_human_and_rights_approval(self):
        base = {
            "path": "submissions/alice/example",
            "published": True,
            "featured": False,
            "review_status": "approved_for_publication",
            "quality_tier": "qualified",
            "reviewed_by": "maintainer",
            "reviewed_at": "2026-08-05",
            "rights_reviewed": True,
            "reviewed_package_sha256": "0" * 64,
            "selection_reason_zh": "通过人工内容和版权审核",
            "selection_reason_en": "Approved after human content and rights review",
            "selected_at": "2026-08-05",
        }
        for field, value, message in [
            ("review_status", "not_approved", "needs approved_for_publication"),
            ("rights_reviewed", False, "needs rights_reviewed=true"),
            ("quality_tier", "featured", "quality_tier=featured requires featured=true"),
        ]:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                entry = dict(base)
                entry[field] = value
                submission = root / "submissions" / "alice" / "example"
                submission.mkdir(parents=True)
                (submission / "proposal.md").write_text("# proposal\n", encoding="utf-8")
                (root / "gallery-publication.json").write_text(
                    json.dumps({"version": 1, "entries": [entry]}), encoding="utf-8"
                )
                with self.assertRaisesRegex(SystemExit, message):
                    load_publication_registry(root)

    def test_publication_approval_is_invalidated_when_reviewed_package_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            submission = root / "submissions" / "alice" / "example"
            submission.mkdir(parents=True)
            (submission / "proposal.md").write_text("# reviewed proposal\n", encoding="utf-8")
            (submission / "manifest.json").write_text(
                json.dumps({"files": [{"path": "proposal.md"}]}), encoding="utf-8"
            )
            entry = {
                "path": "submissions/alice/example",
                "published": True,
                "featured": False,
                "review_status": "approved_for_publication",
                "quality_tier": "qualified",
                "reviewed_by": "maintainer",
                "reviewed_at": "2026-08-05",
                "rights_reviewed": True,
                "reviewed_package_sha256": package_sha256(submission),
                "selection_reason_zh": "通过人工内容和版权审核",
                "selection_reason_en": "Approved after human content and rights review",
                "selected_at": "2026-08-05",
            }
            (root / "gallery-publication.json").write_text(
                json.dumps({"version": 1, "entries": [entry]}), encoding="utf-8"
            )
            load_publication_registry(root)
            (submission / "proposal.md").write_text("# changed after review\n", encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "reviewed package SHA-256 is stale"):
                load_publication_registry(root)

    def test_gallery_paths_exist(self):
        data = DATA_FILE.read_text(encoding="utf-8")
        paths = re.findall(
            r'"(?:thumbnailUrl|visualUrl|proposalUrl|sourceUrl)"\s*:\s*"([^"]+)"',
            data,
        )
        missing = [path for path in paths if not (ROOT / urlsplit(path).path).exists()]
        self.assertEqual([], missing)

    def test_generated_gallery_data_is_current(self):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "generate_submissions_data.py"), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_public_gallery_matches_merged_submission_count(self):
        registry = json.loads((ROOT / "gallery-publication.json").read_text(encoding="utf-8"))
        publication = {entry["path"]: entry for entry in registry["entries"]}
        expected = sum(
            1
            for path in discover_submissions(ROOT)
            if publication.get(path.relative_to(ROOT).as_posix(), {}).get("published", True)
        )
        self.assertEqual(expected, len(self.load_gallery_items()))

    def test_human_readable_report_viewer_loads_structured_evidence(self):
        viewer = (ROOT / "proposal-view.html").read_text(encoding="utf-8")
        for required in [
            "sources.json",
            "metrics.json",
            "standard_matrix.json",
            "design_depth_matrix.json",
            "resolveDataRefs",
            "已解析证据",
        ]:
            self.assertIn(required, viewer)

    def test_gallery_pages_explain_review_statuses(self):
        index = INDEX_FILE.read_text(encoding="utf-8")
        submissions = SUBMISSIONS_FILE.read_text(encoding="utf-8")
        self.assertIn("View All Proposals", index)
        self.assertIn("STATUS_META", index)
        self.assertIn("data-filter=\"formal\"", submissions)
        self.assertIn("data-filter=\"intake\"", submissions)
        self.assertIn("data-filter=\"revision\"", submissions)
        self.assertIn("data-filter=\"fixture\"", submissions)
        self.assertIn("formal_review_ready", submissions)
        self.assertIn("intake_provisional", submissions)


if __name__ == "__main__":
    unittest.main()
