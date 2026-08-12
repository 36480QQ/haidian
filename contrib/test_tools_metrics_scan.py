#!/usr/bin/env python3
"""Regression tests for tools-metrics-scan.py (stdlib only, no pip deps).

Locks the boundaries discussed in the PR review:

- missing/null unit and non-enum unit are counted separately
  (`unit_missing` vs `unit_not_in_enum`, mutually exclusive)
- pct/percent units are excluded from the 0-1 share-ratio sanity check
- `*_far_area_sqm` phase-area keys are not treated as floor-area-ratio
- `--sha` mismatch is rejected unless `--allow-sha-mismatch` is passed,
  and an unverified snapshot is recorded in the summary

Run: python3 contrib/test_tools_metrics_scan.py
"""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_tool():
    """Load tools-metrics-scan.py by file path (hyphenated name is not importable)."""
    spec = importlib.util.spec_from_file_location(
        "tools_metrics_scan", HERE / "tools-metrics-scan.py"
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def make_metrics(entries: dict) -> dict:
    return {
        "schema_version": 1,
        "units": {"area": "sqm", "length": "m"},
        "metrics": entries,
    }


def entry(value, unit=None, status="known"):
    """A valid-shaped metric entry; unit omitted entirely when None is passed
    explicitly, so a missing field can be distinguished from JSON null."""
    e = {
        "status": status,
        "value": value,
        "unit": unit,
        "source_files": [],
        "formula": "",
        "confidence": "high",
    }
    if unit is None:
        del e["unit"]
    return e


def run_scan(tmp_dir: Path, metrics: dict) -> dict:
    """Write a fake repo under tmp_dir, run the scan, return the summary."""
    pkg = tmp_dir / "submissions" / "author" / "slug"
    pkg.mkdir(parents=True)
    (pkg / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False), encoding="utf-8"
    )
    out = tmp_dir / "out"
    tool = load_tool()
    tool.scan(tmp_dir, out, "20260812", "deadbeef", sha_verified=True)
    summary_path = out / "metrics-fullfield-20260812.summary.json"
    return json.loads(summary_path.read_text(encoding="utf-8"))


class UnitEnumSplitTest(unittest.TestCase):
    def test_missing_and_non_enum_units_are_counted_separately(self):
        metrics = make_metrics({
            # valid enum unit: no outlier
            "site_area_sqm": entry(100, "sqm"),
            # unit field entirely absent
            "no_unit_field": entry(1),
            # unit is JSON null
            "null_unit": entry(1, None),
            # declared but invalid enum string
            "bad_unit": entry(1, "hectare"),
        })
        with tempfile.TemporaryDirectory() as td:
            summary = run_scan(Path(td), metrics)
        counts = summary["outlier_counts_only"]
        self.assertEqual(counts["unit_missing"], 2, "absent + null unit")
        self.assertEqual(counts["unit_not_in_enum"], 1, "declared invalid unit")
        # distributions must agree: only None and "hectare" fall outside the enum
        others = summary["distributions"]["unit"]["other_values"]
        self.assertEqual(others["total_count"], 3, "None x2 + hectare x1")
        self.assertEqual(others["n_distinct_values"], 2)

    def test_valid_units_do_not_trigger_either_counter(self):
        metrics = make_metrics({
            "site_area_sqm": entry(100, "sqm"),
            "road_length_m": entry(2000, "m"),
            "node_count": entry(3, "count"),
        })
        with tempfile.TemporaryDirectory() as td:
            summary = run_scan(Path(td), metrics)
        counts = summary["outlier_counts_only"]
        self.assertEqual(counts["unit_missing"], 0)
        self.assertEqual(counts["unit_not_in_enum"], 0)


class SanityBoundaryTest(unittest.TestCase):
    def test_pct_units_excluded_from_share_ratio_check(self):
        metrics = make_metrics({
            # 1.5 with pct unit must NOT trip the 0-1 share check
            "green_coverage_ratio": entry(1.5, "pct"),
            # same value with ratio unit SHOULD trip it
            "green_coverage_ratio_ratio": entry(1.5, "ratio"),
        })
        with tempfile.TemporaryDirectory() as td:
            summary = run_scan(Path(td), metrics)
        self.assertEqual(summary["outlier_counts_only"]["ratio_outside_0_1"], 1)

    def test_phasing_far_area_sqm_is_not_a_far_value(self):
        metrics = make_metrics({
            # phase area in sqm: 500k is a legitimate phase area, not FAR
            "phasing_far_area_sqm": entry(500000, "sqm"),
            # genuine FAR above the 12.0 sanity max
            "floor_area_ratio": entry(15.0, "ratio"),
        })
        with tempfile.TemporaryDirectory() as td:
            summary = run_scan(Path(td), metrics)
        self.assertEqual(summary["outlier_counts_only"]["far_above_12"], 1)


class SnapshotShaTest(unittest.TestCase):
    def test_sha_mismatch_rejected_unless_allow_flag(self):
        tool = load_tool()
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)  # not a git repo: HEAD cannot resolve
            ok, detail = tool.verify_snapshot_sha(repo, "deadbeef")
            self.assertFalse(ok)
            self.assertIn("cannot resolve HEAD", detail)
            # no --allow-sha-mismatch: must exit with an error
            with self.assertRaises(SystemExit):
                tool.main(["--repo", str(repo), "--out-dir", str(repo / "o"),
                           "--date", "20260812", "--sha", "deadbeef"])
            # with the flag: proceeds and records the snapshot as unverified
            tool.main(["--repo", str(repo), "--out-dir", str(repo / "o"),
                       "--date", "20260812", "--sha", "deadbeef",
                       "--allow-sha-mismatch"])
            summary_path = repo / "o" / "metrics-fullfield-20260812.summary.json"
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertIs(summary["snapshot"]["sha_verified_against_head"], False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
