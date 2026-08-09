#!/usr/bin/env python3
"""Validate a manifest against the published site-package schema.

The import is intentionally lazy: the pull-request validator remains usable
for non-package checks when the optional jsonschema dependency is absent.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SCHEMA_PATH = Path(__file__).resolve().parents[1] / "brief" / "site-package" / "schemas" / "manifest.schema.json"


def _json_path(parts: list[object]) -> str:
    result = ""
    for part in parts:
        if isinstance(part, int):
            result += f"[{part}]"
        elif result:
            result += f".{part}"
        else:
            result = str(part)
    return result or "<root>"


def schema_errors(manifest: dict[str, Any], schema_path: Path = SCHEMA_PATH) -> list[str]:
    """Return deterministic, human-readable schema errors for one manifest."""
    try:
        import jsonschema
    except ImportError:
        return [
            "jsonschema is required for manifest schema validation; "
            "install requirements-validation.txt"
        ]

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(
        schema,
        format_checker=jsonschema.FormatChecker(),
    )
    errors = sorted(
        validator.iter_errors(manifest),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    return [f"{_json_path(list(error.absolute_path))}: {error.message}" for error in errors]


def manifest_paths(repo_root: Path) -> list[Path]:
    """Return repository submission manifests in stable path order."""
    return sorted((repo_root / "submissions").glob("*/*/manifest.json"))
