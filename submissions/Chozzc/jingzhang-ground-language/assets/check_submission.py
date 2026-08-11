#!/usr/bin/env python3
"""Small dependency-free integrity checks for Ground Language source data."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def load(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def main() -> None:
    cases = load("assets/data/case-studies.json")["cases"]
    required = {
        "id",
        "url",
        "source_type",
        "accessed_date",
        "applicability_zh",
        "applicability_en",
        "limitation_zh",
        "limitation_en",
        "difference_from_proposal_zh",
        "difference_from_proposal_en",
    }
    assert 5 <= len(cases) <= 8, "taskbook requires 5–8 global cases"
    assert len({case["id"] for case in cases}) == len(cases), "case ids must be unique"
    for case in cases:
        missing = required - case.keys()
        assert not missing, f"{case.get('id', '<unknown>')} missing {sorted(missing)}"
        assert case["url"].startswith("https://"), f"{case['id']} needs a primary HTTPS URL"
        assert case["accessed_date"] == "2026-08-11", f"{case['id']} access date mismatch"
        assert case["source_type"] in {
            "official_public",
            "official_standard",
            "primary_research",
            "primary_project",
        }, f"{case['id']} is not a primary source"
    print(f"PASS: {len(cases)} primary-source case studies are complete and internally consistent")


if __name__ == "__main__":
    main()
