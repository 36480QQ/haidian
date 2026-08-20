#!/usr/bin/env python3
"""Lightweight submission verifier for jingzhang-ai-spine.

Checks that scenario, persona, landmark, case, and project counts in
proposal.md are consistent with metrics.json, risk.json, spatial.json,
and simulation.json. Does not execute external code or call APIs.
"""
import json
import re
import sys
from pathlib import Path

SUBMISSION_DIR = Path(__file__).resolve().parent


def load_json(filename):
    path = SUBMISSION_DIR / filename
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def count_pattern(text, pattern):
    return len(re.findall(pattern, text))


def main():
    errors = []
    warnings = []
    passed = 0

    proposal = (SUBMISSION_DIR / "proposal.md").read_text(encoding="utf-8")
    metrics = load_json("metrics.json")
    risk = load_json("risk.json")
    spatial = load_json("spatial.json")
    simulation = load_json("simulation.json")

    # 1. Scenario count: count | S01 | ... | S12 | in proposal
    scenario_count = count_pattern(proposal, r"\| S\d{2}\*? \||\| S\d{2}\*? ")
    expected_scenarios = 12
    if scenario_count >= expected_scenarios:
        passed += 1
    else:
        errors.append(
            f"Scenario count mismatch: found {scenario_count}, expected {expected_scenarios}"
        )

    # 2. Persona count: count rows in user persona table (5 rows)
    persona_matches = re.findall(r"\| 开源开发者|初创团队|头部企业访客|周边居民|高校师生", proposal)
    expected_personas = 5
    if len(persona_matches) >= expected_personas:
        passed += 1
    else:
        errors.append(
            f"Persona count mismatch: found {len(persona_matches)}, expected {expected_personas}"
        )

    # 3. Landmark count: count 地标一/二/三
    landmark_count = count_pattern(proposal, r"\*\*地标[一二三]")
    expected_landmarks = 3
    if landmark_count == expected_landmarks:
        passed += 1
    else:
        errors.append(
            f"Landmark count mismatch: found {landmark_count}, expected {expected_landmarks}"
        )

    # 4. Global case count: count case rows in the table (8 rows)
    case_count = count_pattern(
        proposal,
        r"硅谷|伦敦King|新加坡One-North|巴黎Station F|首尔Digital|深圳南山|东京涩谷|赫尔辛基",
    )
    expected_cases = 8
    if case_count >= expected_cases:
        passed += 1
    else:
        errors.append(
            f"Global case count mismatch: found {case_count}, expected {expected_cases}"
        )

    # 5. Project count: count JZ-01 through JZ-10
    project_count = count_pattern(proposal, r"JZ-\d{2}")
    expected_projects = 10
    # Each project appears multiple times (table + text), so check unique IDs
    unique_projects = set(re.findall(r"JZ-\d{2}", proposal))
    if len(unique_projects) >= expected_projects:
        passed += 1
    else:
        errors.append(
            f"Project count mismatch: found {len(unique_projects)}, expected {expected_projects}"
        )

    # 6. Risk dimensions check
    if risk:
        risk_dims = risk.get("dimensions", [])
        if len(risk_dims) == 8:
            passed += 1
        else:
            errors.append(f"Risk dimensions: {len(risk_dims)}, expected 8")

        high_risk = [d for d in risk_dims if d.get("score", 0) >= 4]
        has_review = all("human_review" in d for d in high_risk)
        if has_review:
            passed += 1
        else:
            errors.append("High-risk dimensions (score>=4) missing human_review")
    else:
        errors.append("risk.json not found")

    # 7. Spatial items check
    if spatial:
        items = spatial.get("items", [])
        nodes = [i for i in items if i.get("type") == "node"]
        corridors = [i for i in items if i.get("type") == "corridor"]
        areas = [i for i in items if i.get("type") == "area"]

        if len(nodes) >= 6:
            passed += 1
        else:
            errors.append(f"Spatial nodes: {len(nodes)}, expected >= 6")

        if len(corridors) >= 4:
            passed += 1
        else:
            errors.append(f"Spatial corridors: {len(corridors)}, expected >= 4")

        if len(areas) == 3:
            passed += 1
        else:
            errors.append(f"Spatial areas: {len(areas)}, expected 3")

        all_concept = all(
            i.get("geometry", {}).get("mode") == "concept" for i in items
        )
        if all_concept:
            passed += 1
        else:
            errors.append("Not all spatial items have geometry.mode=concept")
    else:
        errors.append("spatial.json not found")

    # 8. Simulation check
    if simulation:
        tasks = simulation.get("tasks", [])
        assertions = [a for t in tasks for a in t.get("assertions", [])]
        all_pass = all(t.get("result") == "pass" for t in tasks)
        if all_pass and len(tasks) > 0:
            passed += 1
        else:
            errors.append(
                f"Simulation: {len(tasks)} tasks, not all pass"
            )

        if len(assertions) == simulation.get("assertion_count", 0):
            passed += 1
        else:
            warnings.append(
                f"Assertion count: found {len(assertions)}, "
                f"declared {simulation.get('assertion_count', 0)}"
            )
    else:
        errors.append("simulation.json not found")

    # 9. Metrics consistency
    if metrics:
        metrics_obj = metrics.get("metrics", {})
        if isinstance(metrics_obj, dict):
            known_metrics = [k for k, v in metrics_obj.items() if isinstance(v, dict) and v.get("status") == "known"]
        else:
            known_metrics = []
        if len(known_metrics) >= 10:
            passed += 1
        else:
            warnings.append(f"Known metrics: {len(known_metrics)}, expected >= 10")
    else:
        errors.append("metrics.json not found")

    # Summary
    total_checks = passed + len(errors)
    print(f"\n=== Submission Verification ===")
    print(f"Passed: {passed}/{total_checks}")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(f"  FAIL: {e}")
    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for w in warnings:
            print(f"  WARN: {w}")
    print()

    if errors:
        print("RESULT: FAIL")
        sys.exit(1)
    else:
        print("RESULT: PASS")
        sys.exit(0)


if __name__ == "__main__":
    main()
