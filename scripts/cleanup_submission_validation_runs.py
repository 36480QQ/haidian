#!/usr/bin/env python3
"""Release a genuinely stuck submission-validation concurrency slot.

GitHub Actions can report a run as ``in_progress`` while it has never created
a job.  A stale run in that state can occupy the workflow's concurrency group
indefinitely.  This helper is deliberately conservative: it only considers
old ``pull_request_target`` runs for this workflow that are still
``in_progress``, have no ``run_started_at`` value, and have zero jobs.

The default mode is a dry run.  The scheduled maintainer workflow passes
``--apply`` after the age and no-job guards have been checked.
"""

from __future__ import annotations

import argparse
import datetime as datetime_module
import json
import os
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


API_ROOT = "https://api.github.com"
DEFAULT_WORKFLOW = ".github/workflows/submission-validation.yml"
DEFAULT_MIN_AGE_MINUTES = 20


def parse_timestamp(value: Any) -> datetime_module.datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime_module.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def is_stuck_run(
    run: dict[str, Any],
    *,
    job_count: int,
    now: datetime_module.datetime,
    min_age_minutes: int,
) -> bool:
    """Return whether a run is safe to classify as a pre-job zombie."""

    if run.get("event") != "pull_request_target":
        return False
    if run.get("status") != "in_progress":
        return False
    if run.get("run_started_at") is not None:
        return False
    if job_count != 0:
        return False
    created_at = parse_timestamp(run.get("created_at"))
    if created_at is None:
        return False
    if now.tzinfo is None:
        now = now.replace(tzinfo=datetime_module.timezone.utc)
    age = now - created_at
    return age >= datetime_module.timedelta(minutes=min_age_minutes)


class ActionsClient:
    def __init__(self, token: str, repository: str) -> None:
        self.token = token
        self.repository = repository

    def request(self, path: str, *, method: str = "GET") -> dict[str, Any]:
        request = Request(
            API_ROOT + path,
            data=b"" if method != "GET" else None,
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "haidian-submission-validation-watchdog",
            },
        )
        try:
            with urlopen(request, timeout=30) as response:
                payload = response.read().decode("utf-8")
        except (HTTPError, URLError) as exc:
            raise RuntimeError(f"GitHub Actions API request failed: {exc}") from exc
        if not payload:
            return {}
        parsed = json.loads(payload)
        if not isinstance(parsed, dict):
            raise RuntimeError("GitHub Actions API returned a non-object response")
        return parsed

    def list_in_progress_runs(self, workflow: str) -> list[dict[str, Any]]:
        query = urlencode({"status": "in_progress", "per_page": "100"})
        workflow_ref = quote(workflow, safe="")
        path = f"/repos/{self.repository}/actions/workflows/{workflow_ref}/runs?{query}"
        payload = self.request(path)
        runs = payload.get("workflow_runs", [])
        if not isinstance(runs, list):
            raise RuntimeError("GitHub Actions API returned invalid workflow_runs")
        return [item for item in runs if isinstance(item, dict)]

    def job_count(self, run_id: int) -> int:
        payload = self.request(
            f"/repos/{self.repository}/actions/runs/{run_id}/jobs?per_page=1"
        )
        count = payload.get("total_count")
        if not isinstance(count, int):
            raise RuntimeError(f"run {run_id} returned an invalid job count")
        return count

    def cancel(self, run_id: int) -> None:
        self.request(f"/repos/{self.repository}/actions/runs/{run_id}/cancel", method="POST")


def run_watchdog(
    client: ActionsClient,
    *,
    workflow: str,
    min_age_minutes: int,
    apply: bool,
    now: datetime_module.datetime | None = None,
) -> int:
    if min_age_minutes < 1:
        raise ValueError("min_age_minutes must be at least 1")
    now = now or datetime_module.datetime.now(datetime_module.timezone.utc)
    runs = client.list_in_progress_runs(workflow)
    candidates: list[dict[str, Any]] = []
    for run in runs:
        run_id = run.get("id")
        if not isinstance(run_id, int):
            continue
        jobs = client.job_count(run_id)
        if is_stuck_run(
            run,
            job_count=jobs,
            now=now,
            min_age_minutes=min_age_minutes,
        ):
            candidates.append(run)

    for run in candidates:
        run_id = run["id"]
        message = (
            f"stuck pre-job run {run_id}: created_at={run.get('created_at')} "
            f"head_sha={run.get('head_sha')}"
        )
        if apply:
            client.cancel(run_id)
            print(f"cancelled {message}")
        else:
            print(f"dry-run {message}")
    print(
        json.dumps(
            {
                "workflow": workflow,
                "inspected_in_progress_runs": len(runs),
                "stuck_pre_job_runs": len(candidates),
                "applied": apply,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", ""))
    parser.add_argument("--workflow", default=DEFAULT_WORKFLOW)
    parser.add_argument("--min-age-minutes", type=int, default=DEFAULT_MIN_AGE_MINUTES)
    parser.add_argument("--apply", action="store_true", help="cancel only matched zombie runs")
    args = parser.parse_args(argv)
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        parser.error("GITHUB_TOKEN is required")
    if not args.repo:
        parser.error("--repo or GITHUB_REPOSITORY is required")
    try:
        return run_watchdog(
            ActionsClient(token, args.repo),
            workflow=args.workflow,
            min_age_minutes=args.min_age_minutes,
            apply=args.apply,
        )
    except (RuntimeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
