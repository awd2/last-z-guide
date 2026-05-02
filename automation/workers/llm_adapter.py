#!/usr/bin/env python3
"""Fail-closed provider adapter for future LLM worker calls."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_json, write_json


REPORTS_DIR = ROOT / "automation" / "reports"

REQUIRED_REQUEST_FIELDS = {
    "schema_version",
    "request_id",
    "worker_role",
    "task",
    "prompt",
    "inputs",
    "expected_response_keys",
}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def blocked_result(
    request: dict[str, Any] | None,
    provider: str,
    errors: list[str],
    request_path: Path | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "report_type": "llm_adapter_result",
        "generated_at": now_utc(),
        "state": "blocked",
        "provider": provider,
        "request_id": request.get("request_id", "") if request else "",
        "worker_role": request.get("worker_role", "") if request else "",
        "request_path": rel(request_path) if request_path else "",
        "response_json": None,
        "usage": None,
        "errors": errors,
        "safety": "No content, backlog, manifest, or production files were modified by the LLM adapter.",
    }


def completed_result(
    request: dict[str, Any],
    provider: str,
    response_json: dict[str, Any],
    request_path: Path,
    fixture_path: Path | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "report_type": "llm_adapter_result",
        "generated_at": now_utc(),
        "state": "completed",
        "provider": provider,
        "request_id": request["request_id"],
        "worker_role": request["worker_role"],
        "request_path": rel(request_path),
        "fixture_path": rel(fixture_path) if fixture_path else "",
        "response_json": response_json,
        "usage": None,
        "errors": [],
        "safety": "No content, backlog, manifest, or production files were modified by the LLM adapter.",
    }


def validate_request(request: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_REQUEST_FIELDS - set(request))
    if missing:
        errors.append("Request is missing required fields: " + ", ".join(missing))
    if request.get("schema_version") != 1:
        errors.append(f"Unsupported request schema_version `{request.get('schema_version')}`; expected `1`.")
    if not isinstance(request.get("inputs"), dict):
        errors.append("Request `inputs` must be an object.")
    expected_keys = request.get("expected_response_keys")
    if not isinstance(expected_keys, list) or not all(isinstance(item, str) and item for item in expected_keys):
        errors.append("Request `expected_response_keys` must be a list of non-empty strings.")
    for key in ["request_id", "worker_role", "task", "prompt"]:
        if key in request and not isinstance(request.get(key), str):
            errors.append(f"Request `{key}` must be a string.")
    return errors


def normalize_fixture_response(payload: dict[str, Any]) -> dict[str, Any]:
    response = payload.get("response_json", payload)
    if not isinstance(response, dict):
        raise ValueError("Fixture response must be an object or contain object field `response_json`.")
    return response


def validate_response(request: dict[str, Any], response_json: dict[str, Any]) -> list[str]:
    expected = request.get("expected_response_keys", [])
    return [f"Response is missing expected key `{key}`." for key in expected if key not in response_json]


def run_adapter(
    request_path: Path,
    provider: str,
    fixture_path: Path | None,
) -> tuple[int, dict[str, Any]]:
    try:
        request = load_json(request_path)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        return 1, blocked_result(None, provider, [f"Could not load request: {exc}"], request_path)

    request_errors = validate_request(request)
    if request_errors:
        return 1, blocked_result(request, provider, request_errors, request_path)

    if provider == "disabled":
        return 1, blocked_result(
            request,
            provider,
            ["No LLM provider is enabled. Use `--provider fixture` for offline tests or configure a supported provider later."],
            request_path,
        )

    if provider != "fixture":
        return 1, blocked_result(
            request,
            provider,
            [f"Provider `{provider}` is not implemented in this fail-closed adapter."],
            request_path,
        )

    if not fixture_path:
        return 1, blocked_result(request, provider, ["Fixture provider requires `--fixture`."], request_path)

    try:
        fixture_payload = load_json(fixture_path)
        response_json = normalize_fixture_response(fixture_payload)
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as exc:
        return 1, blocked_result(request, provider, [f"Could not load fixture response: {exc}"], request_path)

    response_errors = validate_response(request, response_json)
    if response_errors:
        return 1, blocked_result(request, provider, response_errors, request_path)

    return 0, completed_result(request, provider, response_json, request_path, fixture_path)


def write_output(result: dict[str, Any], output: str | None) -> Path | None:
    if not output:
        return None
    path = resolve_path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    write_json(path, result)
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a fail-closed LLM provider adapter for Worker requests.")
    parser.add_argument("--request", required=True, help="Path to a structured LLM request JSON file.")
    parser.add_argument(
        "--provider",
        default="disabled",
        choices=["disabled", "fixture", "openai"],
        help="Provider to use. Defaults to disabled/fail-closed.",
    )
    parser.add_argument("--fixture", help="Fixture response JSON for offline provider tests.")
    parser.add_argument("--output", help="Optional path for the adapter result artifact.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    request_path = resolve_path(args.request)
    fixture_path = resolve_path(args.fixture) if args.fixture else None
    code, result = run_adapter(request_path, args.provider, fixture_path)
    output_path = write_output(result, args.output)

    summary = {
        "state": result["state"],
        "provider": result["provider"],
        "request_id": result["request_id"],
        "worker_role": result["worker_role"],
        "errors": result["errors"],
        "output_path": rel(output_path) if output_path else None,
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"State: {summary['state']}")
        print(f"Provider: {summary['provider']}")
        print(f"Request: {summary['request_id']}")
        if output_path:
            print(f"Output: {rel(output_path)}")
        if summary["errors"]:
            print("Errors:")
            for error in summary["errors"]:
                print(f"- {error}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
