#!/usr/bin/env python3
"""Fail-closed provider adapter for future LLM worker calls."""

from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_json, write_json


REPORTS_DIR = ROOT / "automation" / "reports"
OPENAI_RESPONSES_ENDPOINT = "https://api.openai.com/v1/responses"
DEFAULT_OPENAI_MODEL = "gpt-5.4-mini"

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
    usage: dict[str, Any] | None = None,
    provider_metadata: dict[str, Any] | None = None,
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
        "usage": usage,
        "provider_metadata": provider_metadata or {},
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
    if "response_schema" in request and not isinstance(request.get("response_schema"), dict):
        errors.append("Request `response_schema` must be an object when supplied.")
    if "max_output_tokens" in request:
        value = request.get("max_output_tokens")
        if not isinstance(value, int) or value < 1:
            errors.append("Request `max_output_tokens` must be a positive integer when supplied.")
    return errors


def normalize_fixture_response(payload: dict[str, Any]) -> dict[str, Any]:
    response = payload.get("response_json", payload)
    if not isinstance(response, dict):
        raise ValueError("Fixture response must be an object or contain object field `response_json`.")
    return response


def validate_response(request: dict[str, Any], response_json: dict[str, Any]) -> list[str]:
    expected = request.get("expected_response_keys", [])
    return [f"Response is missing expected key `{key}`." for key in expected if key not in response_json]


def safe_schema_name(request_id: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_-]+", "_", request_id.strip())[:64]
    return value or "llm_adapter_response"


def fallback_response_schema(request: dict[str, Any]) -> dict[str, Any]:
    """Build a strict, conservative schema when a request only names expected keys.

    Role-specific callers should prefer supplying `response_schema`. The fallback
    keeps the first provider milestone useful for simple string-valued contract
    checks without allowing arbitrary top-level keys.
    """

    expected = request.get("expected_response_keys", [])
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            key: {
                "type": "string",
                "description": f"Required response field `{key}`.",
            }
            for key in expected
        },
        "required": expected,
    }


def response_schema(request: dict[str, Any]) -> dict[str, Any]:
    return request.get("response_schema") or fallback_response_schema(request)


def openai_prompt_input(request: dict[str, Any]) -> list[dict[str, str]]:
    system = (
        "You are a constrained LLM worker inside the lastzguides.com automation pipeline. "
        "Return only JSON that matches the provided schema. Do not include markdown. "
        "Do not claim files were edited. Do not propose publication. Treat analytics as signals, not proof."
    )
    user = {
        "task": request["task"],
        "worker_role": request["worker_role"],
        "prompt": request["prompt"],
        "inputs": request["inputs"],
        "expected_response_keys": request["expected_response_keys"],
        "safety": "No content, backlog, manifest, or production files may be modified by this adapter call.",
    }
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": "Return JSON for this worker request:\n" + json.dumps(user, indent=2, sort_keys=True)},
    ]


def openai_request_body(request: dict[str, Any]) -> dict[str, Any]:
    model = os.getenv("OPENAI_MODEL", DEFAULT_OPENAI_MODEL).strip() or DEFAULT_OPENAI_MODEL
    max_output_tokens = request.get("max_output_tokens")
    if not isinstance(max_output_tokens, int):
        max_output_tokens = int(os.getenv("OPENAI_MAX_OUTPUT_TOKENS", "2000"))
    body: dict[str, Any] = {
        "model": model,
        "input": openai_prompt_input(request),
        "text": {
            "format": {
                "type": "json_schema",
                "name": safe_schema_name(request["request_id"]),
                "strict": True,
                "schema": response_schema(request),
            }
        },
        "max_output_tokens": max_output_tokens,
    }
    reasoning_effort = os.getenv("OPENAI_REASONING_EFFORT", "").strip()
    if reasoning_effort:
        body["reasoning"] = {"effort": reasoning_effort}
    return body


def post_openai_response(body: dict[str, Any]) -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Missing env var: OPENAI_API_KEY")

    endpoint = os.getenv("OPENAI_RESPONSES_ENDPOINT", OPENAI_RESPONSES_ENDPOINT).strip() or OPENAI_RESPONSES_ENDPOINT
    raw = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=raw,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    context = None
    try:
        import certifi  # type: ignore

        context = ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        context = None

    try:
        with urllib.request.urlopen(req, timeout=90, context=context) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI Responses API failed: HTTP {exc.code}: {error_body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"OpenAI Responses API failed: {exc}") from exc


def extract_output_text(payload: dict[str, Any]) -> str:
    if isinstance(payload.get("output_text"), str):
        return payload["output_text"]

    chunks: list[str] = []
    for item in payload.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and isinstance(content.get("text"), str):
                chunks.append(content["text"])
    return "".join(chunks).strip()


def openai_response_json(payload: dict[str, Any]) -> dict[str, Any]:
    output_text = extract_output_text(payload)
    if not output_text:
        raise ValueError("OpenAI response did not include output text.")
    parsed = json.loads(output_text)
    if not isinstance(parsed, dict):
        raise ValueError("OpenAI structured response must be a JSON object.")
    return parsed


def run_openai_provider(request: dict[str, Any], request_path: Path) -> tuple[int, dict[str, Any]]:
    body = openai_request_body(request)
    try:
        payload = post_openai_response(body)
        response_json = openai_response_json(payload)
    except (RuntimeError, json.JSONDecodeError, ValueError) as exc:
        return 1, blocked_result(request, "openai", [str(exc)], request_path)

    response_errors = validate_response(request, response_json)
    if response_errors:
        return 1, blocked_result(request, "openai", response_errors, request_path)

    metadata = {
        "model": payload.get("model") or body.get("model"),
        "response_id": payload.get("id", ""),
        "status": payload.get("status", ""),
        "endpoint": os.getenv("OPENAI_RESPONSES_ENDPOINT", OPENAI_RESPONSES_ENDPOINT).strip() or OPENAI_RESPONSES_ENDPOINT,
        "reasoning_effort": (body.get("reasoning") or {}).get("effort", ""),
        "max_output_tokens": body.get("max_output_tokens"),
    }
    return 0, completed_result(
        request,
        "openai",
        response_json,
        request_path,
        usage=payload.get("usage"),
        provider_metadata=metadata,
    )


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

    if provider == "openai":
        return run_openai_provider(request, request_path)

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
