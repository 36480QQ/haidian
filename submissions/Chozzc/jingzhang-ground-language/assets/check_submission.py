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

    language = load("assets/data/ground-language.json")
    scenarios = load("assets/data/scenarios.json")["scenarios"]
    personas = load("assets/data/personas.json")["personas"]
    operations = load("assets/data/operations.json")
    glyphs = language["glyphs"]
    glyph_ids = {item["id"] for item in glyphs}
    field_ids = {item["id"] for item in language["fields"]}
    persona_ids = {item["id"] for item in personas}

    assert [item["token"] for item in glyphs] == [
        "LINE", "YIELD", "EDGE", "BERTH", "HELP", "CHANGE"
    ], "the six-glyph dictionary must stay ordered and complete"
    assert len(language["translations"]) == 3, "three translations required"
    assert len(language["fields"]) == 3 and len(language["wings"]) == 2, "three fields and two wings required"
    assert len(language["landmarks"]) == 3, "three landmarks required"
    assert len(scenarios) == 12, "twelve scenarios required"
    assert sum(item["kind"] == "testing_and_validation" for item in scenarios) >= 3, "three validation scenarios required"
    assert len(personas) >= 8, "at least eight personas required"
    assert len({item["id"] for item in scenarios}) == len(scenarios), "scenario ids must be unique"
    assert len(persona_ids) == len(personas), "persona ids must be unique"
    for scenario in scenarios:
        assert set(scenario["glyph_ids"]) <= glyph_ids, f"{scenario['id']} references an unknown glyph"
        assert scenario["field_id"] in field_ids, f"{scenario['id']} references an unknown field"
        assert set(scenario["persona_ids"]) <= persona_ids, f"{scenario['id']} references an unknown persona"
        assert scenario["fail_safe_zh"] and scenario["fail_safe_en"], f"{scenario['id']} needs bilingual fail-safe behavior"
    for glyph in glyphs:
        assert glyph["failure_behavior_zh"] and glyph["failure_behavior_en"], f"{glyph['id']} needs bilingual failure behavior"
    assert operations["privacy"]["principle"] == "public_state_not_personal_identity"
    assert "default_stop_on_uncertainty" in language["non_negotiables"]
    assert operations["pilot"]["length_target_m"] == {
        "minimum": 100, "maximum": 200, "status": "conceptual_target"
    }
    print(
        f"PASS: {len(cases)} cases, {len(glyphs)} glyphs, {len(scenarios)} scenarios, "
        f"{len(personas)} personas and safety/privacy invariants are consistent"
    )


if __name__ == "__main__":
    main()
