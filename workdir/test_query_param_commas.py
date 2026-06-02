#!/usr/bin/env python3
"""Probe whether list-operation query filters accept comma-separated values.

The script discovers GET "list" operations from openapi.yaml, calls each endpoint
without the tested filter, extracts real candidate values from the response, and
then retries the filter with single values and with a comma-separated pair.

Each request/query-parameter result is classified as:

* `unsupported`: single-value filter requests are rejected.
* `supported`: at least one single-value filter request is accepted, but the
  comma-separated request is rejected or cannot be proven.
* `supported with comma separated values`: single-value and comma-separated
  filter requests are accepted.
* `inconclusive`: the script could not collect values, the base request failed,
  the unfiltered response collection was empty, or the operation could not be
  called with the supplied path parameters.

The result is an empirical signal, not a formal proof. Validation against
returned records is best-effort because some filters are fuzzy, computed, or not
echoed in the response.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


DEFAULT_SPEC_PATH = Path("openapi.yaml")
DEFAULT_BASE_URL = os.getenv("MIST_HOST") or "https://api.mist.com"
LIST_TEXT_PREFIXES = ("list ", "get list", "get a list", "get the list")
LIST_TEXT_PHRASES = (
    " returns a list",
    " return a list",
    " this gets all",
    " gets all ",
)
RESULT_KEYS = ("results", "data", "items")
CONTROL_QUERY_PARAMS = {
    "duration",
    "end",
    "fields",
    "interval",
    "limit",
    "page",
    "search_after",
    "sort",
    "start",
}


@dataclass(frozen=True)
class Operation:
    path: str
    operation_id: str
    description: str
    parameters: list[dict[str, Any]]


@dataclass(frozen=True)
class PlannedOperation:
    operation: Operation
    path: str
    parameters: list[dict[str, Any]]


@dataclass(frozen=True)
class SkippedOperation:
    operation: Operation
    reason: str
    parameters: list[dict[str, Any]]
    missing_path_parameters: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Test whether query parameters on OpenAPI list GET operations accept "
            "comma-separated values."
        )
    )
    parser.add_argument("--spec", type=Path, default=DEFAULT_SPEC_PATH)
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=(
            "Mist API base URL. Defaults to MIST_HOST or https://api.mist.com. "
            "Hostnames without a scheme use https."
        ),
    )
    parser.add_argument(
        "--token",
        default=os.getenv("MIST_APITOKEN", "").split(",")[0],
        help="Mist API token. Defaults to MIST_APITOKEN.",
    )
    parser.add_argument(
        "--auth-scheme",
        default="Token",
        help='Authorization scheme, usually "Token" for Mist APIs.',
    )
    parser.add_argument(
        "--path-param",
        action="append",
        default=[],
        metavar="NAME=VALUE",
        help=(
            "Path parameter value. Repeat as needed, e.g. "
            "--path-param org_id=... --path-param site_id=..."
        ),
    )
    parser.add_argument(
        "--scope",
        choices=("all", "org", "site"),
        default="all",
        help="Limit discovered list operations by path scope.",
    )
    parser.add_argument(
        "--operation",
        action="append",
        default=[],
        metavar="OPERATION_ID_OR_PATH",
        help="Only test matching operationId or path. Repeatable.",
    )
    parser.add_argument(
        "--param",
        action="append",
        default=[],
        metavar="NAME",
        help="Only test query parameters with this name. Repeatable.",
    )
    parser.add_argument(
        "--exclude-param",
        action="append",
        default=[],
        metavar="NAME",
        help="Skip this query parameter name. Repeatable.",
    )
    parser.add_argument(
        "--include-control-params",
        action="store_true",
        help="Also test pagination, sorting, field-selection, and time-window parameters.",
    )
    parser.add_argument(
        "--include-search",
        action="store_true",
        help="Also test GET /search operations whose response is not list-shaped.",
    )
    parser.add_argument(
        "--include-count",
        action="store_true",
        help="Also test GET /count operations whose response is not list-shaped.",
    )
    parser.add_argument("--sample-limit", type=int, default=100)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--delay", type=float, default=0.2)
    parser.add_argument("--max-values", type=int, default=20)
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-csv", type=Path)
    parser.add_argument(
        "--log-requests",
        action="store_true",
        help="Log each tested request URL and HTTP response code to stderr.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List planned probes without making HTTP requests.",
    )
    parser.add_argument(
        "--show-skipped",
        action="store_true",
        help="Show list operations that will not be tested and why.",
    )
    parser.add_argument(
        "--include-collection-get",
        action="store_true",
        help=(
            "Also include GET operations whose path looks like a collection even "
            "when the operationId/description does not say list."
        ),
    )
    return parser.parse_args()


def parse_path_params(values: list[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise SystemExit(f"Invalid --path-param {value!r}; expected NAME=VALUE")
        key, raw = value.split("=", 1)
        parsed[key] = raw
    return parsed


def normalize_base_url(base_url: str) -> str:
    if "://" in base_url:
        return base_url
    return f"https://{base_url}"


def ref_name(ref: str) -> str:
    return ref.rsplit("/", 1)[-1]


def resolve_component_ref(
    spec: dict[str, Any],
    value: Any,
    section: str,
    seen: set[tuple[str, str]] | None = None,
) -> Any:
    if not isinstance(value, dict):
        return value
    ref = value.get("$ref")
    prefix = f"#/components/{section}/"
    if not isinstance(ref, str) or not ref.startswith(prefix):
        return value

    name = ref_name(ref)
    seen = seen or set()
    key = (section, name)
    if key in seen:
        return value
    component = ((spec.get("components") or {}).get(section) or {}).get(name)
    if component is None:
        return value
    return resolve_component_ref(spec, component, section, seen | {key})


def resolve_parameter(spec: dict[str, Any], parameter: dict[str, Any]) -> dict[str, Any]:
    resolved = resolve_component_ref(spec, parameter, "parameters")
    return resolved if isinstance(resolved, dict) else parameter


def description_text(operation: dict[str, Any]) -> str:
    value = operation.get("description")
    return value.strip() if isinstance(value, str) else ""


def has_path_segment(path: str, segment: str) -> bool:
    return segment in path.strip("/").split("/")


def response_schema(spec: dict[str, Any], operation: dict[str, Any]) -> dict[str, Any] | None:
    for status_code, response in (operation.get("responses") or {}).items():
        status_text = str(status_code)
        if status_text != "default":
            try:
                if not 200 <= int(status_text) < 300:
                    continue
            except ValueError:
                continue

        resolved_response = resolve_component_ref(spec, response, "responses")
        if not isinstance(resolved_response, dict):
            continue
        content = resolved_response.get("content") or {}
        json_schema = (content.get("application/json") or {}).get("schema")
        if isinstance(json_schema, dict):
            return json_schema
        for media_type in content.values():
            schema = media_type.get("schema") if isinstance(media_type, dict) else None
            if isinstance(schema, dict):
                return schema
    return None


def schema_is_collection(
    spec: dict[str, Any], schema: dict[str, Any], depth: int = 0
) -> bool:
    if depth > 8:
        return False

    resolved_schema = resolve_component_ref(spec, schema, "schemas")
    if not isinstance(resolved_schema, dict):
        return False
    if resolved_schema.get("type") == "array":
        return True

    for key in ("oneOf", "anyOf", "allOf"):
        if any(
            schema_is_collection(spec, child, depth + 1)
            for child in resolved_schema.get(key) or []
            if isinstance(child, dict)
        ):
            return True

    properties = resolved_schema.get("properties") or {}
    for key in RESULT_KEYS:
        property_schema = properties.get(key)
        if isinstance(property_schema, dict) and schema_is_collection(
            spec, property_schema, depth + 1
        ):
            return True
    return False


def operation_has_list_language(operation: dict[str, Any]) -> bool:
    operation_id = str(operation.get("operationId") or "")
    summary = str(operation.get("summary") or "").lower()
    description = description_text(operation).lower()
    combined_text = f" {summary} {description} "
    if operation_id.lower().startswith("list"):
        return True
    if summary.startswith(LIST_TEXT_PREFIXES):
        return True
    if description.startswith(LIST_TEXT_PREFIXES):
        return True
    return any(phrase in combined_text for phrase in LIST_TEXT_PHRASES)


def is_search_endpoint(path: str, operation: dict[str, Any]) -> bool:
    operation_id = str(operation.get("operationId") or "").lower()
    summary = str(operation.get("summary") or "").lower()
    return (
        has_path_segment(path, "search")
        or operation_id.startswith("search")
        or summary.startswith("search")
    )


def is_count_endpoint(path: str, operation: dict[str, Any]) -> bool:
    operation_id = str(operation.get("operationId") or "").lower()
    summary = str(operation.get("summary") or "").lower()
    return (
        has_path_segment(path, "count")
        or operation_id.startswith("count")
        or summary.startswith("count")
    )


def is_collection_path(path: str) -> bool:
    tail = path.rsplit("/", 1)[-1]

    return "{" not in tail


def is_list_operation(
    spec: dict[str, Any],
    path: str,
    operation: dict[str, Any],
    include_collection_get: bool,
    include_search: bool,
    include_count: bool,
) -> bool:
    schema = response_schema(spec, operation)
    if isinstance(schema, dict) and schema_is_collection(spec, schema):
        return True

    if is_count_endpoint(path, operation):
        return include_count
    if is_search_endpoint(path, operation):
        return include_search
    if has_path_segment(path, "search") or has_path_segment(path, "count"):
        return False
    if operation_has_list_language(operation):
        return True

    return include_collection_get and is_collection_path(path)


def discover_operations(
    spec: dict[str, Any],
    scope: str,
    only_operations: set[str],
    include_collection_get: bool,
    include_search: bool,
    include_count: bool,
) -> list[Operation]:
    discovered: list[Operation] = []
    for path, path_item in (spec.get("paths") or {}).items():
        if not isinstance(path_item, dict):
            continue
        if scope == "org" and not path.startswith("/api/v1/orgs/{org_id}/"):
            continue
        if scope == "site" and not path.startswith("/api/v1/sites/{site_id}/"):
            continue

        operation = path_item.get("get")
        if not isinstance(operation, dict):
            continue

        operation_id = str(operation.get("operationId") or "")
        if only_operations and path not in only_operations and operation_id not in only_operations:
            continue
        if not is_list_operation(
            spec,
            path,
            operation,
            include_collection_get,
            include_search,
            include_count,
        ):
            continue

        inherited = path_item.get("parameters") or []
        parameters = [
            resolve_parameter(spec, parameter)
            for parameter in [*inherited, *(operation.get("parameters") or [])]
            if isinstance(parameter, dict)
        ]
        discovered.append(
            Operation(
                path=path,
                operation_id=operation_id,
                description=description_text(operation),
                parameters=parameters,
            )
        )
    return discovered


def path_param_names(path: str) -> set[str]:
    names: set[str] = set()
    for part in path.split("{")[1:]:
        names.add(part.split("}", 1)[0])
    return names


def missing_path_params(path: str, path_params: dict[str, str]) -> list[str]:
    return sorted(path_param_names(path) - set(path_params))


def build_path(path: str, path_params: dict[str, str]) -> str | None:
    if missing_path_params(path, path_params):
        return None
    result = path
    for key, value in path_params.items():
        result = result.replace("{" + key + "}", urllib.parse.quote(value, safe=""))
    return result


def url_for(base_url: str, path: str, query: dict[str, Any]) -> str:
    base = base_url.rstrip("/")
    encoded = urllib.parse.urlencode(
        {key: value for key, value in query.items() if value is not None},
        doseq=False,
        safe=",",
    )
    return f"{base}{path}" + (f"?{encoded}" if encoded else "")


def request_json(
    url: str,
    token: str,
    auth_scheme: str,
    timeout: float,
) -> tuple[int | None, Any, str | None]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "Authorization": f"{auth_scheme} {token}",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read()
            status = response.status
    except urllib.error.HTTPError as exc:
        body = exc.read()
        status = exc.code
        try:
            payload = json.loads(body.decode("utf-8"))
        except Exception:
            payload = body.decode("utf-8", errors="replace")[:500]
        return status, payload, f"HTTP {status}"
    except urllib.error.URLError as exc:
        return None, None, str(exc)

    if not body:
        return status, None, None
    try:
        return status, json.loads(body.decode("utf-8")), None
    except json.JSONDecodeError:
        return status, body.decode("utf-8", errors="replace")[:500], None


def log_request(enabled: bool, label: str, url: str, status: int | None) -> None:
    if not enabled:
        return
    status_text = str(status) if status is not None else "no_response"
    print(f"[{label}] GET {url} -> {status_text}", file=sys.stderr)


def unwrap_records(payload: Any) -> tuple[list[Any], bool]:
    if isinstance(payload, list):
        return payload, True
    if isinstance(payload, dict):
        for key in RESULT_KEYS:
            value = payload.get(key)
            if isinstance(value, list):
                return value, True
    return [], False


def is_success(status: int | None) -> bool:
    return status is not None and 200 <= status < 300


def scalar_values_for_key(value: Any, key: str) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for item_key, item_value in value.items():
            if item_key == key and isinstance(item_value, (str, int, float, bool)):
                found.append(str(item_value).lower() if isinstance(item_value, bool) else str(item_value))
            found.extend(scalar_values_for_key(item_value, key))
    elif isinstance(value, list):
        for item in value:
            found.extend(scalar_values_for_key(item, key))
    return found


def schema_candidate_values(schema: dict[str, Any], max_values: int) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()

    def add(value: Any) -> None:
        if isinstance(value, bool):
            text = str(value).lower()
        elif isinstance(value, (str, int, float)):
            text = str(value)
        else:
            return
        if text and "," not in text and text not in seen:
            seen.add(text)
            values.append(text)

    def walk(node: Any) -> None:
        if len(values) >= max_values:
            return
        if isinstance(node, dict):
            for item in node.get("enum") or []:
                add(item)
            for item in node.get("examples") or []:
                add(item)
            if "example" in node:
                add(node["example"])
            for key in ("oneOf", "anyOf", "allOf"):
                for child in node.get(key) or []:
                    walk(child)
            if isinstance(node.get("items"), dict):
                walk(node["items"])

    walk(schema)
    return values[:max_values]


def candidate_values(records: list[Any], query_name: str, max_values: int) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()
    for record in records:
        for value in scalar_values_for_key(record, query_name):
            if value and "," not in value and value not in seen:
                seen.add(value)
                values.append(value)
                if len(values) >= max_values:
                    return values
    return values


def candidate_values_for_parameter(
    records: list[Any], parameter: dict[str, Any], max_values: int
) -> tuple[list[str], str]:
    name = parameter["name"]
    response_values = candidate_values(records, name, max_values)
    if len(response_values) >= 2:
        return response_values, "response"

    combined = list(response_values)
    seen = set(combined)
    for value in schema_candidate_values(parameter.get("schema") or {}, max_values):
        if value not in seen:
            seen.add(value)
            combined.append(value)
            if len(combined) >= max_values:
                break

    if combined:
        source = "response" if len(combined) == len(response_values) else "response+schema"
        if not response_values:
            source = "schema"
        return combined, source

    return [], "none"


def query_parameters(
    operation: Operation,
    selected_names: set[str],
    excluded_names: set[str],
    include_control_params: bool,
) -> list[dict[str, Any]]:
    params = []
    for parameter in operation.parameters:
        if parameter.get("in") != "query":
            continue
        name = parameter.get("name")
        if not isinstance(name, str):
            continue
        if selected_names and name not in selected_names:
            continue
        if name in excluded_names:
            continue
        if not selected_names and not include_control_params and name in CONTROL_QUERY_PARAMS:
            continue
        params.append(parameter)
    return params


def default_query(operation: Operation, sample_limit: int) -> dict[str, Any]:
    names = {
        parameter.get("name")
        for parameter in query_parameters(operation, set(), set(), True)
    }
    query: dict[str, Any] = {}
    if "limit" in names:
        query["limit"] = sample_limit
    return query


def validate_records(records: list[Any], query_name: str, allowed: set[str]) -> str:
    values = candidate_values(records, query_name, max_values=1000)
    if not values:
        return "not_echoed"
    unexpected = sorted({value for value in values if value not in allowed})
    if unexpected:
        return f"unexpected_values:{','.join(unexpected[:5])}"
    return "matched"


def support_classification(
    single_statuses: list[int | None],
    comma_status: int | None,
    value_count: int,
    validation: str,
    candidate_value_source: str,
) -> tuple[str, str]:
    if not single_statuses:
        return "inconclusive", "no_single_value_probe"
    if not any(is_success(status) for status in single_statuses):
        if candidate_value_source == "schema":
            return "inconclusive", "schema_candidate_filter_rejected"
        return "unsupported", "single_value_filter_rejected"
    if value_count < 2:
        return "supported", "single_value_filter_accepted_but_only_one_candidate_value"
    if is_success(comma_status):
        if validation.startswith("unexpected_values:"):
            return "supported", "single_value_filter_accepted_but_comma_validation_failed"
        return "supported with comma separated values", "comma_separated_filter_accepted"
    if comma_status is None:
        return "supported", "single_value_filter_accepted_but_comma_probe_failed"
    return "supported", "single_value_filter_accepted_but_comma_filter_rejected"


def skipped_results(skipped_operations: list[SkippedOperation]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for skipped in skipped_operations:
        if skipped.reason != "missing_path_parameters":
            continue
        for parameter in skipped.parameters:
            results.append(
                {
                    "operationId": skipped.operation.operation_id,
                    "path": skipped.operation.path,
                    "parameter": parameter["name"],
                    "classification": "inconclusive",
                    "reason": "missing_path_parameters",
                    "missing_path_parameters": skipped.missing_path_parameters,
                    "validation": "not_tested",
                }
            )
    return results


def probe_operation(
    operation: Operation,
    path: str,
    args: argparse.Namespace,
    token: str,
    selected_params: set[str],
    excluded_params: set[str],
    include_control_params: bool,
) -> list[dict[str, Any]]:
    base_query = default_query(operation, args.sample_limit)
    unfiltered_url = url_for(args.base_url, path, base_query)
    status, payload, error = request_json(
        unfiltered_url, token, args.auth_scheme, args.timeout
    )
    log_request(args.log_requests, "base", unfiltered_url, status)
    time.sleep(args.delay)
    records, is_collection_response = unwrap_records(payload)

    results: list[dict[str, Any]] = []
    if status is None or status >= 400:
        for parameter in query_parameters(
            operation, selected_params, excluded_params, include_control_params
        ):
            results.append(
                {
                    "operationId": operation.operation_id,
                    "path": operation.path,
                    "parameter": parameter["name"],
                    "classification": "inconclusive",
                    "reason": "unfiltered_request_failed",
                    "unfiltered_status": status,
                    "unfiltered_empty": None,
                    "error": error,
                }
            )
        return results

    if is_collection_response and not records:
        for parameter in query_parameters(
            operation, selected_params, excluded_params, include_control_params
        ):
            results.append(
                {
                    "operationId": operation.operation_id,
                    "path": operation.path,
                    "parameter": parameter["name"],
                    "classification": "inconclusive",
                    "reason": "unfiltered_response_empty",
                    "unfiltered_status": status,
                    "unfiltered_empty": True,
                    "record_count": 0,
                    "candidate_values": [],
                    "candidate_value_source": "none",
                    "validation": "not_tested",
                }
            )
        return results

    for parameter in query_parameters(
        operation, selected_params, excluded_params, include_control_params
    ):
        name = parameter["name"]
        values, values_source = candidate_values_for_parameter(
            records, parameter, args.max_values
        )
        if not values:
            results.append(
                {
                    "operationId": operation.operation_id,
                    "path": operation.path,
                    "parameter": name,
                    "classification": "inconclusive",
                    "reason": "no_candidate_values",
                    "unfiltered_status": status,
                    "unfiltered_empty": False,
                    "record_count": len(records),
                    "candidate_values": [],
                    "candidate_value_source": values_source,
                }
            )
            continue

        value_a = values[0]
        value_b = values[1] if len(values) > 1 else None
        single_statuses = []
        for value in values[:2]:
            query = {**base_query, name: value}
            single_url = url_for(args.base_url, path, query)
            single_status, _, single_error = request_json(
                single_url,
                token,
                args.auth_scheme,
                args.timeout,
            )
            log_request(args.log_requests, f"single {name}", single_url, single_status)
            single_statuses.append(single_status)
            if single_error:
                break
            time.sleep(args.delay)

        if value_b is not None:
            comma_query = {**base_query, name: f"{value_a},{value_b}"}
            comma_url = url_for(args.base_url, path, comma_query)
            comma_status, comma_payload, comma_error = request_json(
                comma_url,
                token,
                args.auth_scheme,
                args.timeout,
            )
            log_request(args.log_requests, f"comma {name}", comma_url, comma_status)
            comma_records, _ = unwrap_records(comma_payload)
            validation = validate_records(comma_records, name, {value_a, value_b})
        else:
            comma_status = None
            comma_error = None
            comma_records = []
            validation = "not_tested"

        classification, reason = support_classification(
            single_statuses,
            comma_status,
            len(values),
            validation,
            values_source,
        )

        results.append(
            {
                "operationId": operation.operation_id,
                "path": operation.path,
                "parameter": name,
                "classification": classification,
                "reason": reason,
                "unfiltered_status": status,
                "unfiltered_empty": False,
                "single_statuses": single_statuses,
                "comma_status": comma_status,
                "record_count": len(records),
                "comma_record_count": len(comma_records),
                "candidate_values": values[:2],
                "candidate_value_source": values_source,
                "validation": validation,
                "error": comma_error,
            }
        )
        time.sleep(args.delay)
    return results


def write_outputs(results: list[dict[str, Any]], args: argparse.Namespace) -> None:
    if args.output_json:
        args.output_json.write_text(json.dumps(results, indent=2) + "\n")
    if args.output_csv:
        fieldnames = [
            "operationId",
            "path",
            "parameter",
            "classification",
            "reason",
            "unfiltered_status",
            "unfiltered_empty",
            "missing_path_parameters",
            "single_statuses",
            "comma_status",
            "record_count",
            "comma_record_count",
            "candidate_values",
            "candidate_value_source",
            "validation",
            "error",
        ]
        with args.output_csv.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                row = {key: result.get(key) for key in fieldnames}
                for key in (
                    "single_statuses",
                    "candidate_values",
                    "missing_path_parameters",
                ):
                    if isinstance(row.get(key), list):
                        row[key] = ",".join(str(value) for value in row[key])
                writer.writerow(row)


def print_plan_summary(
    planned: list[PlannedOperation],
    skipped: list[SkippedOperation],
    stream: Any,
) -> None:
    planned_probes = sum(len(item.parameters) for item in planned)
    print(
        f"planned_operations={len(planned)} planned_probes={planned_probes} "
        f"skipped_operations={len(skipped)}",
        file=stream,
    )
    counts: dict[str, int] = {}
    for item in skipped:
        counts[item.reason] = counts.get(item.reason, 0) + 1
    for reason in sorted(counts):
        print(f"skipped_{reason}={counts[reason]}", file=stream)


def print_skipped(skipped: list[SkippedOperation], stream: Any) -> None:
    for item in skipped:
        detail = ""
        if item.missing_path_parameters:
            detail = ": " + ", ".join(item.missing_path_parameters)
        print(
            f"SKIP {item.reason} {item.operation.operation_id or '<no operationId>'} "
            f"{item.operation.path}{detail}",
            file=stream,
        )


def main() -> None:
    args = parse_args()
    args.base_url = normalize_base_url(args.base_url)
    path_params = parse_path_params(args.path_param)
    selected_operations = set(args.operation)
    selected_params = set(args.param)
    excluded_params = set(args.exclude_param)
    spec = yaml.safe_load(args.spec.read_text())
    operations = discover_operations(
        spec,
        args.scope,
        selected_operations,
        args.include_collection_get,
        args.include_search,
        args.include_count,
    )

    planned: list[PlannedOperation] = []
    skipped: list[SkippedOperation] = []
    for operation in operations:
        parameters = query_parameters(
            operation,
            selected_params,
            excluded_params,
            args.include_control_params,
        )
        if not parameters:
            skipped.append(
                SkippedOperation(
                    operation=operation,
                    reason="no_query_parameters_after_exclusions",
                    parameters=[],
                    missing_path_parameters=[],
                )
            )
            continue

        missing = missing_path_params(operation.path, path_params)
        if missing:
            skipped.append(
                SkippedOperation(
                    operation=operation,
                    reason="missing_path_parameters",
                    parameters=parameters,
                    missing_path_parameters=missing,
                )
            )
            continue

        resolved_path = build_path(operation.path, path_params)
        if resolved_path is None:
            continue
        planned.append(
            PlannedOperation(
                operation=operation,
                path=resolved_path,
                parameters=parameters,
            )
        )

    if args.dry_run:
        for item in planned:
            print(
                f"{item.operation.operation_id or '<no operationId>'} "
                f"{item.operation.path}: "
                + ", ".join(parameter["name"] for parameter in item.parameters)
            )
        print_plan_summary(planned, skipped, sys.stdout)
        if args.show_skipped:
            print_skipped(skipped, sys.stdout)
        return

    if not args.token:
        raise SystemExit("Provide --token or set MIST_APITOKEN.")

    print_plan_summary(planned, skipped, sys.stderr)

    results: list[dict[str, Any]] = skipped_results(skipped)
    for item in planned:
        results.extend(
            probe_operation(
                item.operation,
                item.path,
                args,
                args.token,
                selected_params,
                excluded_params,
                args.include_control_params,
            )
        )

    write_outputs(results, args)
    json.dump(results, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
