#!/usr/bin/env python3
"""Reproduce the 8-80 equal-service runbook tabletop and negative tests."""

from __future__ import annotations

import json
from pathlib import Path


RULES = {
    "R1_OWNER": lambda s: bool(str(s.get("owner", "")).strip()),
    "R2_EQUAL_SERVICE": lambda s: bool(str(s.get("non_digital_equivalent", "")).strip()),
    "R3_MINIMUM_DATA": lambda s: s.get("personal_data") is False,
    "R4_NO_BIOMETRIC": lambda s: s.get("biometric_identification") is False,
    "R5_TAKEOVER": lambda s: bool(str(s.get("human_takeover", "")).strip()),
    "R6_STOP_AUTHORITY": lambda s: bool(str(s.get("stop_authority", "")).strip()),
    "R7_NOTICE": lambda s: s.get("public_notice") is True,
    "R8_RECEIPT": lambda s: len(s.get("evidence_receipt", [])) >= 2,
}


def failures(service: dict) -> list[str]:
    return [rule for rule, check in RULES.items() if not check(service)]


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    asset_root = (
        repo_root
        / "submissions"
        / "CatNebulaaaa"
        / "grow-with-jingzhang"
        / "visual"
        / "assets"
    )
    runbook = json.loads((asset_root / "growth-runbook.json").read_text(encoding="utf-8"))
    services = runbook["services"]
    negatives = runbook["negative_cases"]
    service_results = [{"id": item["id"], "failures": failures(item)} for item in services]
    mutation_results = []
    for item in negatives:
        caught = failures(item)
        expected = item["must_violate"]
        mutation_results.append(
            {
                "case_id": item["id"],
                "must_violate": expected,
                "caught_by": caught,
                "caught_by_expected_rule": expected in caught,
                "rejected": bool(caught),
            }
        )
    exercised = {rule: False for rule in RULES}
    for result in mutation_results:
        for rule in result["caught_by"]:
            exercised[rule] = True
    report = {
        "schema_version": "1.0.0",
        "protocol": runbook["protocol"],
        "status": "tabletop_only_not_authorized_not_run",
        "services_total": len(services),
        "services_passed": sum(not item["failures"] for item in service_results),
        "services_failed": [item for item in service_results if item["failures"]],
        "negative_cases_total": len(negatives),
        "negative_cases_caught": sum(
            item["caught_by_expected_rule"] for item in mutation_results
        ),
        "mutation_results": mutation_results,
        "dead_rules": [rule for rule, live in exercised.items() if not live],
        "ok": (
            len(services) == 12
            and all(not item["failures"] for item in service_results)
            and all(item["caught_by_expected_rule"] for item in mutation_results)
            and all(exercised.values())
        ),
        "proof_boundary_zh": (
            "本报告仅证明方案协议的字段和拦截规则可复算，不证明项目已获批准、"
            "场地安全、服务质量或公众接受度。"
        ),
    }
    (asset_root / "growth-tabletop-evidence.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
