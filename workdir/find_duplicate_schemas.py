#!/usr/bin/env python3
"""Find exact and near-duplicate OpenAPI component schemas.

This script is report-only. It does not rewrite references or merge schemas.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

import yaml


DEFAULT_SPEC_PATH = Path("openapi.yaml")
DEFAULT_REPORT_PATH = Path("duplicate_schemas_report.md")
DEFAULT_JSON_PATH = Path("duplicate_schemas_report.json")

IGNORED_EXACT_KEYS = {
    "description",
    "example",
    "examples",
    "externalDocs",
    "summary",
    "title",
    "xml",
}
ORDER_INSENSITIVE_KEYS = {"allOf", "anyOf", "enum", "oneOf", "required"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Find duplicate OpenAPI component schemas.")
    parser.add_argument("--spec", type=Path, default=DEFAULT_SPEC_PATH)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT_PATH)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON_PATH)
    parser.add_argument("--max-groups", type=int, default=50)
    parser.add_argument(
        "--max-schemas-per-group",
        type=int,
        default=30,
        help="Maximum schema names to show in each Markdown group.",
    )
    parser.add_argument(
        "--include-readonly",
        action="store_true",
        help="Keep readOnly/writeOnly in near-duplicate signatures.",
    )
    return parser.parse_args()


def stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(stable_json(value).encode()).hexdigest()


def sorted_list(values: list[Any]) -> list[Any]:
    return sorted(values, key=stable_json)


def normalize_exact(value: Any, key: str | None = None) -> Any:
    if isinstance(value, dict):
        normalized = {}
        for child_key, child in value.items():
            if child_key in IGNORED_EXACT_KEYS or child_key.startswith("x-"):
                continue
            normalized[child_key] = normalize_exact(child, child_key)
        return normalized
    if isinstance(value, list):
        items = [normalize_exact(item, key) for item in value]
        if key in ORDER_INSENSITIVE_KEYS:
            return sorted_list(items)
        return items
    return value


def normalize_shape(value: Any, key: str | None = None, include_readonly: bool = False) -> Any:
    if isinstance(value, dict):
        normalized = {}
        for child_key, child in value.items():
            if child_key in IGNORED_EXACT_KEYS or child_key.startswith("x-"):
                continue
            if child_key in {"default", "deprecated", "format", "maximum", "minimum", "pattern"}:
                continue
            if not include_readonly and child_key in {"readOnly", "writeOnly"}:
                continue
            if child_key == "$ref":
                normalized[child_key] = "#/components/schemas/<ref>"
            elif child_key == "enum" and isinstance(child, list):
                normalized[child_key] = f"<enum:{len(child)}>"
            elif child_key == "const":
                normalized[child_key] = "<const>"
            else:
                normalized[child_key] = normalize_shape(child, child_key, include_readonly)
        return normalized
    if isinstance(value, list):
        items = [normalize_shape(item, key, include_readonly) for item in value]
        if key in ORDER_INSENSITIVE_KEYS:
            return sorted_list(items)
        return items
    return value


def collect_refs(value: Any, parts: tuple[str, ...] = ()) -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        ref = value.get("$ref")
        if isinstance(ref, str):
            yield ".".join(parts), ref
        for key, child in value.items():
            yield from collect_refs(child, (*parts, str(key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from collect_refs(child, (*parts, str(index)))


def schema_ref_name(ref: str) -> str | None:
    prefix = "#/components/schemas/"
    if ref.startswith(prefix):
        return ref[len(prefix) :]
    return None


def usage_summary(data: dict[str, Any]) -> tuple[Counter[str], dict[str, list[str]]]:
    counts: Counter[str] = Counter()
    examples: dict[str, list[str]] = defaultdict(list)
    for path, ref in collect_refs(data):
        name = schema_ref_name(ref)
        if name is None:
            continue
        counts[name] += 1
        if len(examples[name]) < 8:
            examples[name].append(path)
    return counts, examples


def schema_kind(schema: dict[str, Any]) -> str:
    if "$ref" in schema:
        return "ref"
    for key in ("oneOf", "anyOf", "allOf"):
        if key in schema:
            return key
    value = schema.get("type")
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "|".join(str(item) for item in value)
    if "properties" in schema:
        return "object"
    return "unknown"


def schema_preview(schema: dict[str, Any]) -> str:
    kind = schema_kind(schema)
    if kind == "array":
        items = schema.get("items")
        if isinstance(items, dict) and "$ref" in items:
            return f"array of `{items['$ref']}`"
        return "array"
    if kind == "object":
        properties = schema.get("properties")
        if isinstance(properties, dict):
            names = ", ".join(list(properties)[:8])
            suffix = "" if len(properties) <= 8 else f", ... +{len(properties) - 8}"
            return f"object with {len(properties)} properties: {names}{suffix}"
        if "additionalProperties" in schema:
            return "map object"
    if kind in {"oneOf", "anyOf", "allOf"}:
        return f"{kind} with {len(schema.get(kind, []))} variants"
    enum = schema.get("enum")
    if isinstance(enum, list):
        return f"{kind} enum with {len(enum)} values"
    return kind


def build_groups(
    schemas: dict[str, Any],
    include_readonly: bool,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    exact: dict[str, list[str]] = defaultdict(list)
    exact_normalized: dict[str, Any] = {}
    shape: dict[str, list[str]] = defaultdict(list)
    shape_normalized: dict[str, Any] = {}

    for name, schema in schemas.items():
        if not isinstance(schema, dict):
            continue
        exact_value = normalize_exact(schema)
        exact_key = digest(exact_value)
        exact[exact_key].append(name)
        exact_normalized[exact_key] = exact_value

        shape_value = normalize_shape(schema, include_readonly=include_readonly)
        shape_key = digest(shape_value)
        shape[shape_key].append(name)
        shape_normalized[shape_key] = shape_value

    exact_groups = [
        {
            "hash": key,
            "schemas": sorted(names),
            "normalized_schema": exact_normalized[key],
        }
        for key, names in exact.items()
        if len(names) > 1
    ]
    exact_groups.sort(key=lambda item: (-len(item["schemas"]), item["schemas"]))

    exact_group_sets = {tuple(group["schemas"]) for group in exact_groups}
    near_groups = []
    for key, names in shape.items():
        if len(names) <= 1:
            continue
        schema_names = sorted(names)
        if tuple(schema_names) in exact_group_sets:
            continue
        near_groups.append(
            {
                "hash": key,
                "schemas": schema_names,
                "shape_signature": shape_normalized[key],
            }
        )
    near_groups.sort(key=lambda item: (-len(item["schemas"]), item["schemas"]))
    return exact_groups, near_groups


def group_to_report_lines(
    group: dict[str, Any],
    schemas: dict[str, Any],
    ref_counts: Counter[str],
    ref_examples: dict[str, list[str]],
    max_schemas_per_group: int,
) -> list[str]:
    names = group["schemas"]
    lines = [f"### {len(names)} schemas", ""]
    lines.append(f"- Preview: {schema_preview(schemas[names[0]])}")
    lines.append("- Schemas:")
    for name in names[:max_schemas_per_group]:
        lines.append(f"  - `{name}` ({ref_counts[name]} refs)")
        for example in ref_examples.get(name, [])[:3]:
            lines.append(f"    - `{example}`")
    if len(names) > max_schemas_per_group:
        lines.append(f"  - ... {len(names) - max_schemas_per_group} more schemas")
    lines.append("")
    return lines


def enrich_groups(
    groups: list[dict[str, Any]],
    ref_counts: Counter[str],
    ref_examples: dict[str, list[str]],
) -> list[dict[str, Any]]:
    enriched = []
    for group in groups:
        enriched_group = dict(group)
        enriched_group["references"] = {
            name: {
                "count": ref_counts[name],
                "examples": ref_examples.get(name, []),
            }
            for name in group["schemas"]
        }
        enriched.append(enriched_group)
    return enriched


def render_report(
    spec_path: Path,
    schemas: dict[str, Any],
    exact_groups: list[dict[str, Any]],
    near_groups: list[dict[str, Any]],
    ref_counts: Counter[str],
    ref_examples: dict[str, list[str]],
    max_groups: int,
    max_schemas_per_group: int,
    include_readonly: bool,
) -> str:
    exact_schema_count = sum(len(group["schemas"]) for group in exact_groups)
    near_schema_count = sum(len(group["schemas"]) for group in near_groups)

    lines = [
        "# OpenAPI Duplicate Schema Report",
        "",
        f"Spec: `{spec_path}`",
        "",
        "This report is heuristic and read-only. Merging schemas can affect generated SDK model names even when structures match.",
        "",
        "## Normalization",
        "",
        "- Exact duplicates ignore: `description`, `example`, `examples`, `externalDocs`, `summary`, `title`, `xml`, and `x-*` keys.",
        "- Exact duplicates keep validation and API-shape fields such as `default`, `deprecated`, `readOnly`, `writeOnly`, `format`, and bounds.",
        "- Near duplicates additionally ignore selected value-level details and replace schema `$ref` targets with a placeholder.",
        f"- Near duplicates {'keep' if include_readonly else 'ignore'} `readOnly` and `writeOnly`.",
        "",
        "## Summary",
        "",
        f"- Schemas analyzed: {len(schemas)}",
        f"- Exact duplicate groups: {len(exact_groups)}",
        f"- Schemas in exact duplicate groups: {exact_schema_count}",
        f"- Near-duplicate groups: {len(near_groups)}",
        f"- Schemas in near-duplicate groups: {near_schema_count}",
        "",
        "## Exact Duplicate Groups",
        "",
    ]

    if not exact_groups:
        lines.append("No exact duplicate groups found.")
        lines.append("")
    for group in exact_groups[:max_groups]:
        lines.extend(
            group_to_report_lines(
                group,
                schemas,
                ref_counts,
                ref_examples,
                max_schemas_per_group,
            )
        )
    if len(exact_groups) > max_groups:
        lines.append(f"... {len(exact_groups) - max_groups} more exact duplicate groups omitted.")
        lines.append("")

    lines.extend(["## Near-Duplicate Groups", ""])
    if not near_groups:
        lines.append("No near-duplicate groups found.")
        lines.append("")
    for group in near_groups[:max_groups]:
        lines.extend(
            group_to_report_lines(
                group,
                schemas,
                ref_counts,
                ref_examples,
                max_schemas_per_group,
            )
        )
    if len(near_groups) > max_groups:
        lines.append(f"... {len(near_groups) - max_groups} more near-duplicate groups omitted.")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    data = yaml.safe_load(args.spec.read_text())
    schemas = data.get("components", {}).get("schemas", {})
    if not isinstance(schemas, dict):
        raise SystemExit("No components.schemas object found")

    ref_counts, ref_examples = usage_summary(data)
    exact_groups, near_groups = build_groups(schemas, args.include_readonly)

    json_data = {
        "summary": {
            "spec": str(args.spec),
            "schemas_analyzed": len(schemas),
            "exact_duplicate_groups": len(exact_groups),
            "near_duplicate_groups": len(near_groups),
            "include_readonly_in_near_duplicates": args.include_readonly,
        },
        "exact_duplicate_groups": enrich_groups(exact_groups, ref_counts, ref_examples),
        "near_duplicate_groups": enrich_groups(near_groups, ref_counts, ref_examples),
    }
    report = render_report(
        args.spec,
        schemas,
        exact_groups,
        near_groups,
        ref_counts,
        ref_examples,
        args.max_groups,
        args.max_schemas_per_group,
        args.include_readonly,
    )

    args.json.write_text(json.dumps(json_data, indent=2) + "\n")
    args.report.write_text(report + "\n")
    print(report)
    print(f"Markdown report written to: {args.report.resolve()}")
    print(f"JSON report written to: {args.json.resolve()}")


if __name__ == "__main__":
    main()
